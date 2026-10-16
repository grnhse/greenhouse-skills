#!/usr/bin/env python3
"""Build a Greenhouse page from page data and the template next to this script.

One shell call, the data on standard input:

    python3 build_page.py --out greenhouse-pipeline.html <<'GH_PAGE_DATA'
    { ...page data, JSON... }
    GH_PAGE_DATA

or from a file: python3 build_page.py --data data.json --out page.html

The template (page.html) is fixed: this script only checks the data and drops it into
the template's data block. daily-brief and pipeline-review send a short form (see
PAGE.md) that is expanded here; the other skills send the page schema directly.
It reads the data, writes --out, and does nothing else: no network, nothing executed
from the data. Exit code 0 and the output path on success; 1 and a list of problems otherwise.
"""
import argparse
import html
import json
import os
import re
import sys
from urllib.parse import urlsplit

MAX_BYTES = 400_000
MAX_ROWS = 500
MAX_PANELS = 14
MAX_TEXT = 1200
MAX_MESSAGE = 4000
DATA_TOKEN = '{"__GH_DATA__":true}'
TITLE_TOKEN = "__GH_TITLE__"
CHIP_KINDS = {"act", "wait", "good", "info", "idle"}
CELL_KINDS = {"text", "link", "num", "chip", "days", "stages"}
STEP_STATES = {"done", "here", "ahead"}
SKILLS = {"configure", "daily-brief", "pipeline-review", "candidate-debrief", "candidate-status", "interview-week", "source-review"}
# Scorecard text may appear only on the single-candidate debrief page.
FEEDBACK_AUDIENCE = {"candidate-debrief": "hiring-team"}

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+")
MONEY = re.compile(r"(?:[$£€¥]\s?\d)|(?:\b\d[\d,.]*\s?(?:USD|EUR|GBP)\b)")
PHONE = re.compile(r"(?<![\w/=.-])(?:\+\d{1,3}[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?![\w-])")


class Problems(list):
    def bad(self, where, msg):
        self.append(f"{where}: {msg}")


def check_href(value, where, out):
    try:
        parts = urlsplit(value)
    except ValueError:
        parts = None
    if not isinstance(value, str) or parts is None or parts.scheme != "https" or parts.hostname != "app.greenhouse.io":
        out.bad(where, "links may only point to https://app.greenhouse.io/")


def check_text(value, where, out, limit=MAX_TEXT, required=False):
    if value is None and not required:
        return
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        out.bad(where, "must be text or a number")
        return
    text = str(value)
    if required and not text.strip():
        out.bad(where, "is required")
    if len(text) > limit:
        out.bad(where, f"is longer than {limit} characters")
    if EMAIL.search(text):
        out.bad(where, "contains an email address; contact details never go on a page")
    if MONEY.search(text):
        out.bad(where, "contains an amount of money; compensation never goes on a page")
    if PHONE.search(text):
        out.bad(where, "looks like a phone number; contact details never go on a page")


def check_keys(obj, where, allowed, required, out):
    if not isinstance(obj, dict):
        out.bad(where, "must be an object")
        return False
    for key in obj:
        if key not in allowed:
            out.bad(where, f"unknown key '{key}' (allowed: {', '.join(sorted(allowed))})")
    for key in required:
        if key not in obj:
            out.bad(where, f"missing '{key}'")
    return True


def check_chip(chip, where, out):
    if check_keys(chip, where, {"kind", "label"}, {"label"}, out):
        if chip.get("kind", "idle") not in CHIP_KINDS:
            out.bad(where, f"chip kind must be one of {', '.join(sorted(CHIP_KINDS))}")
        check_text(chip.get("label"), where + ".label", out, 60, True)


def check_number(value, where, out):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        out.bad(where, "must be a number, zero or more")


def check_cell(value, col, where, out):
    kind = col.get("kind", "text")
    if value is None:
        return
    if kind == "chip":
        check_chip(value, where, out)
    elif kind == "stages":
        if not isinstance(value, list) or len(value) > 20:
            out.bad(where, "must be a list of at most 20 {name, n}")
            return
        for i, item in enumerate(value):
            if check_keys(item, f"{where}[{i}]", {"name", "n"}, {"name", "n"}, out):
                check_text(item.get("name"), f"{where}[{i}].name", out, 80, True)
                check_number(item.get("n"), f"{where}[{i}].n", out)
    elif isinstance(value, dict):
        allowed = {"text", "sub", "chip"} | ({"href"} if kind == "link" else set()) | ({"value"} if kind == "days" else set())
        check_keys(value, where, allowed, set(), out)
        check_text(value.get("text"), where + ".text", out)
        check_text(value.get("sub"), where + ".sub", out)
        if "href" in value:
            check_href(value["href"], where + ".href", out)
        if "chip" in value:
            check_chip(value["chip"], where + ".chip", out)
        if kind == "days":
            check_number(value.get("value"), where + ".value", out)
    else:
        check_text(value, where, out)
        if kind == "days":
            check_number(value, where, out)


def check_table(p, where, out):
    cols = p.get("columns")
    if not isinstance(cols, list) or not 1 <= len(cols) <= 8:
        out.bad(where + ".columns", "needs one to eight columns")
        return
    keys = set()
    for i, col in enumerate(cols):
        if not check_keys(col, f"{where}.columns[{i}]", {"key", "label", "kind"}, {"key", "label"}, out):
            continue
        if not isinstance(col.get("key"), str) or not re.fullmatch(r"[a-z][a-zA-Z0-9]{0,23}", col.get("key") or ""):
            out.bad(f"{where}.columns[{i}].key", "must be a short camelCase word")
        if col.get("kind", "text") not in CELL_KINDS:
            out.bad(f"{where}.columns[{i}].kind", f"must be one of {', '.join(sorted(CELL_KINDS))}")
        check_text(col.get("label"), f"{where}.columns[{i}].label", out, 60, True)
        keys.add(col.get("key"))
    rows = p.get("rows")
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        out.bad(where + ".rows", f"must be a list of at most {MAX_ROWS} rows")
        return
    by_key = {c.get("key"): c for c in cols if isinstance(c, dict)}
    for r, row in enumerate(rows):
        rw = f"{where}.rows[{r}]"
        if not isinstance(row, dict):
            out.bad(rw, "must be an object")
            continue
        for key, value in row.items():
            if key == "_detail":
                if not isinstance(value, list) or len(value) > 12:
                    out.bad(rw + "._detail", "must be a list of at most 12 {label, value}")
                    continue
                for d, item in enumerate(value):
                    if check_keys(item, f"{rw}._detail[{d}]", {"label", "value", "href"}, {"label", "value"}, out):
                        check_text(item.get("label"), f"{rw}._detail[{d}].label", out, 60, True)
                        check_text(item.get("value"), f"{rw}._detail[{d}].value", out)
                        if "href" in item:
                            check_href(item["href"], f"{rw}._detail[{d}].href", out)
            elif key == "_prompt":
                check_text(value, rw + "._prompt", out, 300, True)
            elif key in by_key:
                check_cell(value, by_key[key], f"{rw}.{key}", out)
            else:
                out.bad(rw, f"'{key}' is not a column of this table")
    if "filter" in p and p["filter"] not in keys:
        out.bad(where + ".filter", "must name one of this table's columns")
    if "search" in p and not isinstance(p["search"], bool):
        out.bad(where + ".search", "must be true or false")
    check_text(p.get("more"), where + ".more", out, 120)


def check_panel(p, where, out):
    common = {"type", "title", "note", "half", "empty", "foot"}
    kind = p.get("type") if isinstance(p, dict) else None
    shapes = {
        "table": {"columns", "rows", "filter", "search", "more"},
        "funnel": {"stages", "unit", "activeLabel", "rejectedLabel", "reachedLabel"},
        "bars": {"items"},
        "message": {"text", "copyLabel"},
        "list": {"items"},
        "steps": {"stages"},
        "tally": {"ratings"},
        "timeline": {"events"},
    }
    if kind not in shapes:
        out.bad(where, f"type must be one of {', '.join(sorted(shapes))}")
        return
    check_keys(p, where, common | shapes[kind], {"type", "title"}, out)
    for key in ("title", "note", "empty", "foot", "unit", "activeLabel", "rejectedLabel", "reachedLabel", "copyLabel"):
        check_text(p.get(key), f"{where}.{key}", out, 400, key == "title")
    if "half" in p and not isinstance(p["half"], bool):
        out.bad(where + ".half", "must be true or false")

    def items(key, limit, allowed, required):
        value = p.get(key, [])
        if not isinstance(value, list) or len(value) > limit:
            out.bad(f"{where}.{key}", f"must be a list of at most {limit}")
            return []
        return [(f"{where}.{key}[{i}]", x) for i, x in enumerate(value) if check_keys(x, f"{where}.{key}[{i}]", allowed, required, out)]

    if kind == "table":
        check_table(p, where, out)
    elif kind == "funnel":
        for w, x in items("stages", 30, {"name", "active", "rejected", "reached", "pass", "flag", "sub", "scale"}, {"name", "active"}):
            if "scale" in x and not isinstance(x["scale"], bool):
                out.bad(w + ".scale", "must be true or false")
            check_text(x.get("name"), w + ".name", out, 80, True)
            check_number(x.get("active"), w + ".active", out)
            if "rejected" in x:
                check_number(x["rejected"], w + ".rejected", out)
            for key in ("reached", "pass", "flag", "sub"):
                check_text(x.get(key), f"{w}.{key}", out, 80)
    elif kind == "bars":
        for w, x in items("items", 30, {"label", "value", "sub"}, {"label", "value"}):
            check_text(x.get("label"), w + ".label", out, 160, True)
            check_number(x.get("value"), w + ".value", out)
            check_text(x.get("sub"), w + ".sub", out, 160)
    elif kind == "message":
        check_text(p.get("text"), where + ".text", out, MAX_MESSAGE, True)
    elif kind == "list":
        for w, x in items("items", 60, {"text", "lead", "sub", "href", "chip", "copy"}, {"text"}):
            check_text(x.get("text"), w + ".text", out, MAX_TEXT, True)
            check_text(x.get("lead"), w + ".lead", out, 120)
            check_text(x.get("sub"), w + ".sub", out)
            if "href" in x:
                check_href(x["href"], w + ".href", out)
            if "chip" in x:
                check_chip(x["chip"], w + ".chip", out)
            if "copy" in x and not isinstance(x["copy"], bool):
                check_text(x["copy"], w + ".copy", out, MAX_MESSAGE)
    elif kind == "steps":
        for w, x in items("stages", 30, {"name", "state", "sub"}, {"name"}):
            check_text(x.get("name"), w + ".name", out, 80, True)
            check_text(x.get("sub"), w + ".sub", out, 60)
            if x.get("state", "ahead") not in STEP_STATES:
                out.bad(w + ".state", "must be done, here or ahead")
    elif kind == "tally":
        for w, x in items("ratings", 8, {"label", "people"}, {"label", "people"}):
            check_text(x.get("label"), w + ".label", out, 40, True)
            people = x.get("people")
            if not isinstance(people, list) or len(people) > 40:
                out.bad(w + ".people", "must be a list of names")
            else:
                for i, name in enumerate(people):
                    check_text(name, f"{w}.people[{i}]", out, 120, True)
    elif kind == "timeline":
        for w, x in items("events", 80, {"when", "title", "sub", "href", "chip"}, {"when", "title"}):
            check_text(x.get("when"), w + ".when", out, 60, True)
            check_text(x.get("title"), w + ".title", out, 300, True)
            check_text(x.get("sub"), w + ".sub", out)
            if "href" in x:
                check_href(x["href"], w + ".href", out)
            if "chip" in x:
                check_chip(x["chip"], w + ".chip", out)


def validate(data):
    out = Problems()
    top = {"skill", "title", "view", "asOf", "headline", "scope", "audience", "meta", "tiles", "filter", "panels", "judged", "notes", "next", "cap"}
    if not check_keys(data, "data", top, {"skill", "title", "asOf", "headline", "scope", "panels"}, out):
        return out
    if data.get("skill") not in SKILLS:
        out.bad("skill", f"must be one of {', '.join(sorted(SKILLS))}")
    check_text(data.get("title"), "title", out, 60, True)
    for key, limit in (("view", 80), ("asOf", 60), ("headline", 240), ("scope", 400), ("judged", 2400), ("cap", 240)):
        check_text(data.get(key), key, out, limit, key in ("asOf", "headline", "scope"))
    if isinstance(data.get("scope"), str) and "that you can see" not in data["scope"]:
        out.bad("scope", 'must carry the words "that you can see"')
    audience = data.get("audience", "private")
    if audience not in ("private", "hiring-team"):
        out.bad("audience", "must be private or hiring-team")
    expected = FEEDBACK_AUDIENCE.get(data.get("skill"), "private")
    if audience != expected:
        out.bad("audience", f"must be '{expected}' for {data.get('skill')}")
    for i, m in enumerate(data.get("meta") or []):
        if check_keys(m, f"meta[{i}]", {"label", "value", "href"}, {"label", "value"}, out):
            check_text(m.get("label"), f"meta[{i}].label", out, 40, True)
            check_text(m.get("value"), f"meta[{i}].value", out, 160, True)
            if "href" in m:
                check_href(m["href"], f"meta[{i}].href", out)
    tiles = data.get("tiles") or []
    if not isinstance(tiles, list) or len(tiles) > 4:
        out.bad("tiles", "at most four tiles")
        tiles = []
    for i, t in enumerate(tiles):
        if check_keys(t, f"tiles[{i}]", {"label", "value", "sub", "focus"}, {"label", "value"}, out):
            check_text(t.get("label"), f"tiles[{i}].label", out, 60, True)
            check_text(t.get("value"), f"tiles[{i}].value", out, 24, True)
            check_text(t.get("sub"), f"tiles[{i}].sub", out, 80)
    if sum(1 for t in tiles if isinstance(t, dict) and t.get("focus")) > 1:
        out.bad("tiles", "only one tile carries the focus accent")
    if "filter" in data and check_keys(data["filter"], "filter", {"key", "label"}, {"key"}, out):
        check_text(data["filter"].get("label"), "filter.label", out, 40)
    panels = data.get("panels")
    if not isinstance(panels, list) or not 1 <= len(panels) <= MAX_PANELS:
        out.bad("panels", f"needs one to {MAX_PANELS} panels")
        panels = []
    for i, p in enumerate(panels):
        check_panel(p, f"panels[{i}]", out)
    if data.get("skill") != "candidate-debrief" and any(isinstance(p, dict) and p.get("type") == "tally" for p in panels):
        out.bad("panels", "a rating tally belongs only on the candidate-debrief page")
    for key, limit, each in (("notes", 8, 800), ("next", 4, 300)):
        value = data.get(key) or []
        if not isinstance(value, list) or len(value) > limit:
            out.bad(key, f"must be a list of at most {limit}")
            continue
        for i, text in enumerate(value):
            check_text(text, f"{key}[{i}]", out, each, True)
    return out


PEOPLE = "https://app.greenhouse.io/people/{}?application_id={}"
SDASH = "https://app.greenhouse.io/sdash/{}"


class ShortFormError(Exception):
    pass


def _need(obj, where, *keys):
    if not isinstance(obj, dict):
        raise ShortFormError(f"{where}: must be an object")
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ShortFormError(f"{where}: missing {', '.join(missing)}")


def _rows(value, where):
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(r, dict) for r in value):
        raise ShortFormError(f"{where}: must be a list of objects")
    return value


def _person(row, sub=None):
    cell = {"text": row.get("name") or "Candidate"}
    if isinstance(row.get("cand"), int) and isinstance(row.get("app"), int):
        cell["href"] = PEOPLE.format(row["cand"], row["app"])
    if row.get("private"):
        cell = {"text": "Private candidate", "sub": "Private candidate: don't forward", **({"href": cell["href"]} if "href" in cell else {})}
    elif sub:
        cell["sub"] = sub
    return cell


def _job(name, job):
    cell = {"text": name or "Req"}
    if isinstance(job, int):
        cell["href"] = SDASH.format(job)
    return cell


def _plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def _detail(pairs):
    return [{"label": k, "value": str(v)} for k, v in pairs if v not in (None, "", [])]


def _common(data, page):
    for key in ("view", "asOf", "headline", "scope", "notes", "next", "cap"):
        if key in data:
            page[key] = data[key]
    return page


def expand_daily_brief(d):
    _need(d, "data", "asOf", "headline", "scope", "day")
    th = {"quiet": 14, "first": 7, "cards": 14, **(d.get("thresholds") or {})}
    age = d.get("ageLabel") or "Days quiet"
    totals = d.get("totals") or {}
    dec, quiet = _rows(d.get("decisions"), "decisions"), _rows(d.get("quiet"), "quiet")
    sc = d.get("scorecards") or {}
    sc_rows = _rows(sc.get("rows"), "scorecards.rows")
    owed = bool(sc.get("owed"))
    new = d.get("new") or {}
    n_dec, n_sc, n_quiet = totals.get("decisions", len(dec)), totals.get("scorecards", len(sc_rows)), totals.get("quiet", len(quiet))
    n_int = sc.get("interviewers", len({r.get("who") for r in sc_rows}))
    focus = d.get("focus")
    tiles = [
        {"label": "Decisions waiting", "value": str(n_dec), "sub": "interviews done, no decision recorded", "focus": focus == "decisions"},
        {"label": "Feedback owed" if owed else "Scorecards not submitted", "value": str(n_sc), "sub": f"{_plural(n_int, 'interviewer')}, last {th['cards']} days", "focus": focus == "scorecards"},
        {"label": "Quiet candidates", "value": str(n_quiet), "sub": f"{th['quiet']} or more days, {th['first']} in the first stage", "focus": focus == "quiet"},
        {"label": "New since yesterday", "value": str(new.get("applicants", 0)), "sub": f"applicants · {_plural(new.get('fresh', 0), 'fresh scorecard')}", "focus": focus == "new"},
    ]
    for t in tiles:
        if not t["focus"]:
            del t["focus"]
    panels = []

    def more(total, shown):
        return {"more": f"and {total - shown} more"} if total > shown else {}

    panels.append({
        "type": "table", "title": f"Decisions waiting ({n_dec})",
        "note": "Greenhouse flags these as ready for a decision: interviews are done and none is recorded. Already decided and holding the move on purpose? Ignore the flag.",
        "columns": [{"key": "candidate", "label": "Candidate", "kind": "link"}, {"key": "req", "label": "Req"}, {"key": "stage", "label": "Stage"},
                    {"key": "scorecards", "label": f"Scorecards ({th['cards']} days)"}, {"key": "days", "label": age, "kind": "days"}, {"key": "status", "label": "Status", "kind": "chip"}],
        "rows": [{"candidate": _person(r), "req": r.get("req"), "stage": r.get("stage"), "scorecards": r.get("cards"), "days": r.get("days", 0),
                  "status": {"kind": "act", "label": "Needs decision"},
                  **_prompt(None if r.get("private") else f"/greenhouse:candidate-debrief {r.get('name')} on {r.get('req')}"),
                  "_detail": _detail([("Hiring manager", r.get("hm")),
                                      ("Why it is here", r.get("why") or f"In {r.get('stage')}, decision waiting, {'in stage' if age == 'Days in stage' else 'no activity recorded for'} {r.get('days', 0)} days"),
                                      ("Next step", r.get("step") or "Debrief, then record the outcome in Greenhouse")])} for r in dec],
        "empty": "Nothing is waiting on a decision.", **more(n_dec, len(dec))})
    title = "Feedback owed" if owed else "Scorecards started but not submitted"
    panels.append({
        "type": "table", "title": f"{title} ({_plural(n_sc, 'scorecard')}, {_plural(n_int, 'interviewer')}, last {th['cards']} days)",
        **({} if owed else {"note": "Interviewers who haven't opened their scorecard show up only with interview access (harvest:interviews:list)."}),
        "filter": "interviewer",
        "columns": [{"key": "interviewer", "label": "Interviewer"}, {"key": "candidate", "label": "Candidate", "kind": "link"}, {"key": "req", "label": "Req"},
                    {"key": "interviewed", "label": "Interviewed"}, {"key": "hours", "label": "Hours since interview", "kind": "num"}],
        "rows": [{"interviewer": r.get("who") or "name not visible", "candidate": _person(r, r.get("note") or ("last open scorecard" if r.get("last") else None)),
                  "req": r.get("req"), "interviewed": r.get("on"), "hours": r.get("hours")} for r in sc_rows],
        "empty": sc.get("empty") or "No scorecards are outstanding that you can see.", **more(n_sc, len(sc_rows))})
    reminders = _reminders(sc_rows, d.get("view"))
    if reminders:
        panels.append({"type": "list", "title": f"Reminders to copy ({_plural(len(reminders), 'interviewer')})",
                       "note": "One per interviewer with a scorecard outstanding. Copy one and send it yourself: nothing is sent from Greenhouse.", "items": reminders})
    if d.get("interviews") is not None:
        rows = _rows(d["interviews"], "interviews")
        panels.append({
            "type": "table", "title": f"Interviews today and tomorrow ({len(rows)})", "half": True,
            "columns": [{"key": "when", "label": "Starts"}, {"key": "candidate", "label": "Candidate", "kind": "link"}, {"key": "req", "label": "Req"}, {"key": "status", "label": "Status", "kind": "chip"}],
            "rows": [{"when": r.get("when"), "candidate": _person(r), "req": r.get("req"), "status": {"kind": "idle", "label": r.get("status") or "Scheduled"}} for r in rows],
            "empty": "No interviews today or tomorrow that you can see."})
    panels.append({
        "type": "table", "title": f"Quiet candidates ({n_quiet})",
        "columns": [{"key": "candidate", "label": "Candidate", "kind": "link"}, {"key": "req", "label": "Req"}, {"key": "stage", "label": "Stage"},
                    {"key": "days", "label": d.get("quietAgeLabel") or ("Days in stage" if age == "Days in stage" else "Days since last activity"), "kind": "days"}, {"key": "next", "label": "Next step"}],
        "rows": [{"candidate": _person(r), "req": r.get("req"), "stage": r.get("stage"), "days": r.get("days", 0),
                  **_prompt(None if r.get("private") else f"/greenhouse:candidate-status {r.get('name')}"),
                  "next": r.get("step") or ("Check decision or offer status" if r.get("late") else "Schedule the next step" + (f" (coordinator: {r['co']})" if r.get("co") else ""))} for r in quiet],
        "empty": "Nobody has gone quiet.", **more(n_quiet, len(quiet))})
    items = [{"lead": f"{name}:", "text": _plural(n, "new applicant")} for name, n in (new.get("byReq") or [])]
    items += [{"lead": "Fresh feedback:", "text": f"{r.get('name') or 'Candidate'} ({r.get('req')})",
               **({"href": PEOPLE.format(r["cand"], r["app"])} if isinstance(r.get("cand"), int) and isinstance(r.get("app"), int) else {})} for r in _rows(new.get("feedback"), "new.feedback")]
    panels.append({"type": "list", "title": f"New since yesterday ({_plural(new.get('applicants', 0), 'applicant')}, {_plural(new.get('fresh', 0), 'fresh scorecard')})",
                   "half": True, "items": items, "empty": "Nothing new since yesterday that you can see."})
    if d.get("offers") is not None:
        rows = _rows(d["offers"], "offers")
        panels.append({
            "type": "table", "title": f"Offers in flight ({len(rows)})", "half": True, "note": "No amounts are shown.",
            "columns": [{"key": "candidate", "label": "Candidate", "kind": "link"}, {"key": "req", "label": "Req"}, {"key": "sent", "label": "Sent"}, {"key": "start", "label": "Start date"}],
            "rows": [{"candidate": _person(r), "req": r.get("req"), "sent": r.get("sent") or "not sent yet", "start": r.get("start")} for r in rows],
            "empty": d.get("offersEmpty") or "No offers in flight that you can see."})
    kinds = {"Decisions waiting": "act", "Nobody past review": "wait", "No candidates": "wait", "Gone quiet": "wait", "Quiet": "wait", "Moving": "good", "New": "info"}
    snap = []
    for r in _rows(d.get("snapshot"), "snapshot"):
        row = {"req": _job(r.get("req"), r.get("job")), **_prompt(f"/greenhouse:pipeline-review {r.get('req')}"), "open": r.get("open"), "active": r.get("active", 0), "inReview": r.get("review", 0),
               "byStage": [{"name": s[0], "n": s[1]} for s in (r.get("stages") or []) if isinstance(s, list) and len(s) == 2 and s[1]],
               "decisions": r.get("decisions", 0), "quiet": r.get("quiet", 0),
               "_detail": _detail([("New since yesterday", r.get("new", 0)), ("Needs review", r.get("needs")), ("Hiring manager", r.get("hm")), ("Coordinator", r.get("coordinator"))])}
        if r.get("status"):
            row["status"] = {"kind": kinds.get(r["status"], "idle"), "label": r["status"]}
        if not row["byStage"]:
            del row["byStage"]
        snap.append(row)
    panels.append({
        "type": "table", "title": "Pipeline snapshot",
        "note": "One row per req. In review is its own number; the bar shows active applications past review, by stage in plan order, early stages light and late stages dark.",
        "columns": [{"key": "req", "label": "Req", "kind": "link"}, {"key": "open", "label": "Days open", "kind": "num"}, {"key": "status", "label": "Status", "kind": "chip"},
                    {"key": "active", "label": "Active", "kind": "num"}, {"key": "inReview", "label": "In review", "kind": "num"}, {"key": "byStage", "label": "Past review by stage", "kind": "stages"},
                    {"key": "decisions", "label": "Decisions", "kind": "num"}, {"key": "quiet", "label": "Quiet", "kind": "num"}],
        "rows": snap, "empty": "No open reqs that you can see."})
    page = {"skill": "daily-brief", "title": f"Daily brief, {d['day']}", "filter": {"key": "req", "label": "Req"}, "tiles": tiles, "panels": panels,
            "judged": d.get("judged") or (f"How this was ranked: quiet is {th['quiet']} or more days without recorded activity ({th['first']} in the first stage, where the clock runs from the day they applied), "
                      "because a week without a first look is when applicants start accepting other interviews; scorecards count when started and not submitted within "
                      f"{th['cards']} days; \"Decisions waiting\" is Greenhouse's needs_decision flag on applications past the first stage: interviews are complete and no decision is recorded; "
                      "applications still in review are counted under Needs review. Every threshold is inclusive. Tell me different numbers and I'll redo it.")}
    return _common(d, page)


def expand_pipeline_review(d):
    _need(d, "data", "asOf", "headline", "scope", "job", "counts")
    job, c = d["job"], d["counts"]
    _need(job, "job", "name")
    focus = d.get("focus")
    meta = _detail([("Open", job.get("open")), ("Req", job.get("req") or "no req id"), ("Furthest", job.get("furthest")), ("Recruiter", job.get("recruiter")),
                    ("Coordinator", job.get("coordinator")), ("Seats", job.get("seats")), ("Offers", job.get("offers")),
                    ("Confidential", "share only with its hiring team" if job.get("confidential") else None)])
    if isinstance(job.get("id"), int):
        meta.append({"label": "Greenhouse", "value": "Open the req", "href": SDASH.format(job["id"])})
    tiles = [
        {"label": "Active applications", "value": str(c.get("active", 0)), "sub": c.get("activeNote") or "complete count", "focus": focus == "active"},
        {"label": "In review", "value": str(c.get("review", 0)), **({"sub": f"longest waiting {c['reviewLongest']} days since applying"} if c.get("reviewLongest") is not None else {}), "focus": focus == "review"},
        {"label": "Decisions waiting", "value": str(c.get("decisions", 0)), "sub": "past review; interviews done, none recorded", "focus": focus == "decisions"},
        {"label": "Quiet 7 or more days", "value": str(c.get("quiet", 0)), **({"sub": f"of {c['pastReview']} past review"} if c.get("pastReview") is not None else {}), "focus": focus == "quiet"},
    ]
    for t in tiles:
        if not t["focus"]:
            del t["focus"]
    panels = []
    msg = d.get("message") or {}
    if msg.get("text"):
        panels.append({"type": "message", "title": "Hiring-manager message (safe to share)",
                       "note": "Names, stages and counts only. Confirm the recipient is on this job's hiring team before sending.",
                       "text": msg["text"], **({"foot": "The numbers behind it: " + msg["numbers"]} if msg.get("numbers") else {})})
    risks = _rows(d.get("risks"), "risks")
    panels.append({"type": "list", "title": "Risks", "half": True, "empty": "No rule fires; not a green light.",
                   "items": [{"lead": f"{r.get('rule')}:", "text": r.get("text") or "", **({"sub": r["why"]} if r.get("why") else {}),
                              **({"chip": {"kind": "wait", "label": d["status"]}} if i == 0 and d.get("status") else {})} for i, r in enumerate(risks)]})
    qs = _rows(d.get("questions"), "questions")
    qs = [q for q in qs if q.get("to") == "hm"] + [q for q in qs if q.get("to") != "hm"]
    panels.append({"type": "list", "title": "Questions for the sync", "half": True, "empty": "No question follows from these numbers.",
                   "items": [{"lead": "Ask the hiring manager:" if q.get("to") == "hm" else "Stays with you:", "text": q.get("text") or "", "copy": True,
                              **({"href": PEOPLE.format(q["cand"], q["app"])} if isinstance(q.get("cand"), int) and isinstance(q.get("app"), int) else {})} for q in qs]})
    flow = [{"name": s.get("name"), "sub": f"{s.get('active', 0)} active", "state": "done" if s.get("active") else "ahead"} for s in _rows(d.get("funnel"), "funnel")]
    if flow:
        panels.append({"type": "steps", "title": "Where the active applications stand", "stages": flow,
                       "foot": "Each stage in plan order with its active applications; a dashed stage holds nobody now."})
    stages = []
    for i, s in enumerate(_rows(d.get("funnel"), "funnel")):
        row = {"name": s.get("name"), "active": s.get("active", 0)}
        for key in ("rejected",):
            if key in s:
                row[key] = s[key]
        for key in ("reached", "pass"):
            if s.get(key) is not None:
                row[key] = str(s[key])
        if s.get("bottleneck"):
            row["flag"] = "Bottleneck"
            if isinstance(s["bottleneck"], str):
                row["sub"] = s["bottleneck"]
        if s.get("review", i == 0):
            row["scale"] = False
        stages.append(row)
    history = d.get("reached") == "history"
    panels.append({"type": "funnel", "title": "Funnel, plan order", "unit": "Applications",
                   **({} if history else {"reachedLabel": "Reached at least (derived)"}),
                   "note": "Bars count applications, not people. " + ("Reached is from each application's stage history." if history else "Reached is rebuilt from where each application ended or stands today."),
                   "stages": stages, **({"foot": d["bottleneck"]} if d.get("bottleneck") else {})})
    ro = d.get("roster") or {}
    kinds = {"Needs decision": "act", "Scorecard due": "wait", "Offer to send": "wait", "Scheduled": "idle", "Waiting on candidate": "idle"}
    rows = []
    for r in _rows(ro.get("rows"), "roster.rows"):
        verb = "candidate-debrief" if r.get("status") == "Needs decision" else "candidate-status"
        row = {"candidate": _person(r), "stage": r.get("stage"), "days": r.get("days", 0),
               **_prompt(None if r.get("private") else f"/greenhouse:{verb} {r.get('name')}" + (f" on {job['name']}" if verb == "candidate-debrief" else "")),
               "feedback": {"text": r.get("feedback") or "no scorecards that you can see", **({"sub": r["tally"]} if r.get("tally") else {})}}
        if r.get("status"):
            row["status"] = {"kind": kinds.get(r["status"], "idle"), "label": r["status"]}
        extra = r.get("detail") or {}
        if isinstance(extra, dict) and extra:
            row["_detail"] = _detail(list(extra.items()))
        rows.append(row)
    panels.append({"type": "table", "title": f"Late stages: {ro.get('stages') or 'none'}", "filter": "stage", "search": True,
                   "note": "Ordered by stage reached, not by strength. Ratings are shown as given, never totalled.",
                   "columns": [{"key": "candidate", "label": "Candidate", "kind": "link"}, {"key": "stage", "label": "Stage"}, {"key": "days", "label": ro.get("ageLabel") or "Days quiet", "kind": "days"},
                               {"key": "feedback", "label": "Feedback"}, {"key": "status", "label": "Status", "kind": "chip"}],
                   "rows": rows, "empty": "Nobody is in the late stages that you can see.",
                   **({"foot": ro["optOut"]} if ro.get("optOut") else {}), **({"more": ro["more"]} if ro.get("more") else {})})
    rej = d.get("rejections") or {}
    panels.append({"type": "bars", "title": f"Rejections, last 30 days ({rej.get('total', 0)}: we declined {rej.get('we', 0)} · withdrew {rej.get('they', 0)} · other or none recorded {rej.get('other', 0)})",
                   "note": "Reasons as recorded in Greenhouse.", "empty": "None that you can see in the last 30 days.",
                   "items": [{"label": r.get("reason") or "No reason recorded", "value": r.get("n", 0),
                              "sub": " · ".join(x for x in (r.get("who"), f"mostly from {r['from']}" if r.get("from") else None) if x)} for r in _rows(rej.get("rows"), "rejections.rows")]})
    page = {"skill": "pipeline-review", "title": f"{job['name']} pipeline"[:60], "meta": meta, "tiles": tiles, "panels": panels,
            "judged": d.get("judged") or ("How this was judged: bottleneck = the stage with the most active candidates, tie broken by the oldest median activity; quiet = no activity recorded for 7 or more days "
                      "(a week untouched is when candidates accept other interviews); an offer is outstanding after 7 days in Created; rejections cover the last 30 days by rejected_at; "
                      "the roster shows at most 50 rows, latest stage first, then longest without activity"
                      + (f"; questions on {d['managerStages']} go to the hiring manager, the rest stay with you" if d.get("managerStages") else "")
                      + ". Risk rules: at risk = 30+ days open, nobody past the first interview; slow = 60+ days, no finalist; gone quiet = 3+ past review, half quiet; thin = 2 or fewer past review; "
                      "pass-through needs 20 resolved (10 for an early signal); a median needs 3 values; a draft within 30 days hides a tally. Every threshold is inclusive. Tell me different numbers and I'll redo it.")}
    return _common(d, page)


def _prompt(text):
    return {"_prompt": text} if text and "None" not in text else {}


def _first_name(view):
    if isinstance(view, str) and view.endswith("'s view"):
        return view[:-len("'s view")].split()[0]
    return None


def _reminders(rows, view):
    """One copyable reminder per interviewer, from the scorecard rows already on the page."""
    by = {}
    for r in rows:
        who = r.get("who")
        if who and who != "name not visible" and not r.get("note"):
            by.setdefault(who, []).append(r)
    me, items = _first_name(view), []
    for who, mine in by.items():
        parts = [f"{'a candidate' if r.get('private') else r.get('name')} ({r.get('req')}, scorecard dated {r.get('on')})" for r in mine]
        many = len(parts) > 1
        text = (f"Hi {who.split()[0]}, Greenhouse still shows your {'scorecards' if many else 'scorecard'} for {' and '.join(parts)} as "
                f"{'drafts' if many else 'a draft'}, and the team is waiting on {'them' if many else 'it'} to decide. "
                f"If {'an' if many else 'the'} interview moved or you weren't on it, let me know. Thanks" + (f", {me}" if me else ""))
        items.append({"lead": f"{who}:", "text": text, "copy": True})
    return items


SKILL_NAMES = {"daily-brief": "Daily brief", "interview-week": "Interview week", "candidate-status": "Candidate status", "candidate-debrief": "Candidate debrief",
               "pipeline-review": "Pipeline review", "source-review": "Source review", "scorecard-draft": "Scorecard draft"}


def expand_configure(d):
    _need(d, "data", "asOf", "headline", "scope", "skills")
    c, focus = d.get("counts") or {}, d.get("focus")
    meta = _detail([("Matched to", d.get("matched")), ("Role", d.get("role"))])
    tiles = []
    if c:
        tiles = [{"label": "Open reqs", "value": str(c.get("reqs", 0)), "focus": focus == "reqs"},
                 {"label": "Active applications", "value": str(c.get("active", 0)), "focus": focus == "active"},
                 {"label": "Decisions waiting", "value": str(c.get("decisions", 0)), **({"sub": c["decisionsNote"]} if c.get("decisionsNote") else {}), "focus": focus == "decisions"},
                 {"label": "Quiet 14 or more days", "value": str(c.get("quiet", 0)), **({"sub": c["quietNote"]} if c.get("quietNote") else {}), "focus": focus == "quiet"}]
        for t in tiles:
            if not t["focus"]:
                del t["focus"]
    kinds = {"Ready": ("good", "Ready"), "Partial": ("wait", "Partly"), "Partly": ("wait", "Partly"), "Not yet": ("idle", "Not yet")}
    rows = []
    for r in _rows(d["skills"], "skills"):
        kind, label = kinds.get(r.get("status"), ("idle", r.get("status") or "Not yet"))
        rows.append({"skill": SKILL_NAMES.get(r.get("skill"), r.get("skill")), "status": {"kind": kind, "label": label}, "try": r.get("try"),
                     "missing": r.get("missing") or "", **_prompt(r.get("try") if label != "Not yet" and "<" not in (r.get("try") or "<") else None)})
    note = "A tool can be missing because a Site Admin hasn't enabled it, your Greenhouse permissions don't allow it, or you didn't tick it when connecting."
    panels = [{"type": "table", "title": "What works from here", "note": note + (" " + d["caveat"] if d.get("caveat") else ""),
               "columns": [{"key": "skill", "label": "Skill"}, {"key": "status", "label": "Status", "kind": "chip"}, {"key": "try", "label": "Try"}, {"key": "missing", "label": "If something is missing"}],
               "rows": rows, **({"foot": "Every tool the seven data skills use is listed."} if d.get("allListed") else {})}]
    if d.get("note"):
        panels.append({"type": "message", "title": "A note for your Site Admin", "text": d["note"], "copyLabel": "Copy note",
                       "foot": "Saving signs everyone in your organization out of Greenhouse MCP; each person reconnects once, and the tool list can take up to 10 minutes to refresh."})
    if d.get("rollout"):
        panels.append({"type": "table", "title": "Rolling this out",
                       "columns": [{"key": "persona", "label": "Persona"}, {"key": "keys", "label": "Scope keys"}, {"key": "gets", "label": "What they get"}],
                       "rows": [{"persona": r.get("persona"), "keys": r.get("keys"), "gets": r.get("gets")} for r in _rows(d["rollout"], "rollout")],
                       "foot": "Change them under Configure > Dev Center > MCP Access > Endpoints."})
    if d.get("reqs") is not None:
        panels.append({"type": "table", "title": "Your open reqs",
                       "columns": [{"key": "req", "label": "Req", "kind": "link"}, {"key": "active", "label": "Active", "kind": "num"}, {"key": "decisions", "label": "Decisions waiting", "kind": "num"},
                                   {"key": "quiet", "label": "Quiet", "kind": "num"}, {"key": "fresh", "label": "New in 24 hours", "kind": "num"}],
                       "rows": [{"req": _job(r.get("req"), r.get("job")), "active": r.get("active", 0), "decisions": r.get("decisions", 0), "quiet": r.get("quiet", 0), "fresh": r.get("new", 0),
                                 **_prompt(f"/greenhouse:pipeline-review {r.get('req')}")} for r in _rows(d["reqs"], "reqs")],
                       "empty": "You're not on an open job's hiring team as recruiter or coordinator. Name a job and I'll work from there."})
    page = {"skill": "configure", "title": "Greenhouse setup", "meta": meta, "tiles": tiles, "panels": panels,
            "judged": "How this was judged: Ready means every core tool is listed, Partial only enhancements or the user lookup missing, Not yet another core tool missing; quiet is 14 or more days with no "
                      "activity recorded, because two working weeks without a touch is when candidates start accepting other interviews; new is the last 24 hours; busiest is most active applications. "
                      "Thresholds are inclusive. Tell me different numbers and I'll redo it."}
    if not meta:
        del page["meta"]
    if not tiles:
        del page["tiles"]
    page = _common(d, page)
    page["notes"] = ["Seeing a tool doesn't guarantee access: Greenhouse applies your own permissions when it's called."] + list(d.get("notes") or [])
    return page


def expand_interview_week(d):
    _need(d, "data", "asOf", "headline", "scope", "window")
    c, focus = d.get("counts") or {}, d.get("focus")
    words = d.get("windowWords") or "next 7 days"
    week = None if d.get("week") is None else _rows(d["week"], "week")
    todo = None if d.get("toSchedule") is None else _rows(d["toSchedule"], "toSchedule")
    fb = None if d.get("feedback") is None else _rows(d["feedback"], "feedback")
    default_tools = bool(d.get("defaultTools"))
    tiles = []
    if week is not None:
        sub = " · ".join(x for x in (f"{c['today']} today" if "today" in c else None, f"{c['tomorrow']} tomorrow" if "tomorrow" in c else None) if x)
        tiles.append({"label": f"Interviews, {words}", "value": str(len(week)), **({"sub": sub} if sub else {}), "focus": focus == "interviews"})
    if todo is not None:
        longest = max([r.get("days", 0) for r in todo] or [0])
        tiles.append({"label": "Still to schedule", "value": str(d.get("toScheduleTotal", len(todo))), **({"sub": f"longest waiting {longest} days"} if todo else {}), "focus": focus == "schedule"})
    if fb is not None:
        owed = c.get("owed", sum(r.get("n", len(r.get("cards") or []) or 1) for r in fb))
        tiles.append({"label": "Scorecards not submitted" if default_tools else "Awaiting feedback", "value": str(owed),
                      "sub": f"{_plural(c.get('owedInterviewers', len(fb)), 'interviewer')}, last 30 days", "focus": focus == "feedback"})
    if "declined" in c or "notReplied" in c:
        tiles.append({"label": "Panel replies missing", "value": str(c.get("declined", 0) + c.get("notReplied", 0)),
                      "sub": f"declined {c.get('declined', 0)} · not replied {c.get('notReplied', 0)}", "focus": focus == "replies"})
    for t in tiles:
        if not t["focus"]:
            del t["focus"]
    kinds = {"Scheduled": "idle", "Panel change needed": "act", "Application closed": "act", "Scorecard due": "wait", "Feedback in": "good",
             "Skipped": "info", "Test sent": "info", "Test received": "info"}
    panels = []
    if week is not None:
        rows = []
        for r in week:
            row = {"day": r.get("day"), "time": r.get("time"), "candidate": _person(r), "req": r.get("req"),
                   "interview": {"text": r.get("interview") or "interview", **({"sub": r["stage"]} if r.get("stage") else {})},
                   "panel": {"text": r.get("panel") or "panel: not visible", **({"sub": r["replies"]} if r.get("replies") else {})},
                   "status": {"kind": kinds.get(r.get("status"), "idle"), "label": r.get("status") or "Scheduled"}}
            if isinstance(r.get("detail"), dict) and r["detail"]:
                row["_detail"] = _detail(list(r["detail"].items()))
            rows.append(row)
        panels.append({"type": "table", "title": f"{d.get('weekTitle') or 'This week'} ({_plural(len(week), 'interview')})", "filter": "day", "search": True,
                       "note": f"Times are {d.get('zone') or 'UTC'}. Rooms and video links are on each interview in Greenhouse.",
                       "columns": [{"key": "day", "label": "Day"}, {"key": "time", "label": "Time"}, {"key": "candidate", "label": "Candidate", "kind": "link"}, {"key": "req", "label": "Req"},
                                   {"key": "interview", "label": "Interview"}, {"key": "panel", "label": "Panel"}, {"key": "status", "label": "Status", "kind": "chip"}],
                       "rows": rows, "empty": "No interviews are on the calendar in this window that you can see."})
    if todo is not None:
        rows = []
        for r in todo:
            row = {"candidate": _person(r), "req": r.get("req"), "interview": {"text": r.get("interview") or "interview", **({"sub": r["sub"]} if r.get("sub") else {})},
                   "days": r.get("days", 0), "status": {"kind": "act", "label": "Availability in" if r.get("availability") else "To schedule"},
                   **_prompt(None if r.get("private") else f"/greenhouse:candidate-status {r.get('name')}")}
            if isinstance(r.get("detail"), dict) and r["detail"]:
                row["_detail"] = _detail(list(r["detail"].items()))
            rows.append(row)
        total = d.get("toScheduleTotal", len(todo))
        panels.append({"type": "table", "title": f"Still to schedule ({_plural(total, 'candidate')})",
                       "note": "Greenhouse marks these interviews as to be scheduled in the candidate's current stage. Days count from when the slot opened."
                               + (" This may include interviews from stages already passed." if d.get("passedCaveat") else ""),
                       "columns": [{"key": "candidate", "label": "Candidate", "kind": "link"}, {"key": "req", "label": "Req"}, {"key": "interview", "label": "Interview"},
                                   {"key": "days", "label": "Days waiting", "kind": "days"}, {"key": "status", "label": "Status", "kind": "chip"}],
                       "rows": rows, "empty": "Nothing is waiting to be scheduled.", **({"more": f"and {total - len(todo)} more"} if total > len(todo) else {})})
    if fb is not None:
        owed = c.get("owed", sum(r.get("n", len(r.get("cards") or []) or 1) for r in fb))
        title = "Scorecards started but not submitted" if default_tools else "Awaiting feedback"
        me, items = _first_name(d.get("view")), []
        for r in fb:
            cards = _rows(r.get("cards"), "feedback.cards")
            n = r.get("n", len(cards) or 1)
            who, nudge, lines = r.get("who"), r.get("nudge"), r.get("lines")
            if cards:
                lines = " · ".join(", ".join(str(x) for x in ("a private candidate" if k.get("private") else k.get("name"), k.get("req"), k.get("interview"), k.get("on"), k.get("state"),
                                                              f"{k['hours']} hours since the interview" if k.get("hours") is not None else None) if x) for k in cards)
                if who and who != "You" and not r.get("noNudge"):
                    many = len(cards) > 1
                    parts = " and ".join(f"{'a candidate' if k.get('private') else k.get('name')} ({', '.join(str(x) for x in (k.get('req'), k.get('interview'), k.get('on')) if x)})" for k in cards)
                    nudge = (f"Hi {who.split()[0]}, Greenhouse is still waiting on your {'scorecards' if many else 'scorecard'} for {parts}.\n"
                             f"The team needs {'them' if many else 'it'} to decide; if {'an' if many else 'the'} interview moved or you weren't on it, let me know. Thanks" + (f", {me}" if me else ""))
            item = {"lead": f"{who or 'Interviewers not visible'}:", "text": nudge or lines or "", "chip": {"kind": "wait", "label": _plural(n, "scorecard") if n > 1 else "Scorecard due"}}
            if nudge:
                item["copy"] = True
                if lines:
                    item["sub"] = lines
            items.append(item)
        panels.append({"type": "list", "title": f"{title} ({_plural(owed, 'scorecard')}, {_plural(c.get('owedInterviewers', len(fb)), 'interviewer')}, last 30 days)",
                       "note": "Copy a reminder and send it yourself: nothing is sent from Greenhouse. Counts and dates only; no ratings or scorecard text are read."
                               + (" Interviewers who haven't opened their scorecard show up only with interview access (harvest:interviews:list)." if default_tools else ""),
                       "items": items, "empty": "No feedback is owed from the last 30 days that you can see."})
    zone = d.get("zone") or "UTC"
    page = {"skill": "interview-week", "title": f"Interviews, {d['window']}"[:60], "filter": {"key": "req", "label": "Req"}, "tiles": tiles, "panels": panels,
            "judged": d.get("judged") or (f"How this was read: the window is {d.get('read') or '7 days from today'}, in {zone}; an interview counts when Greenhouse has a start time for it in the window, and all-day events "
                      "such as take-home tests are listed as \"All day\"; still to schedule = interviews Greenhouse marks as to be scheduled in the candidate's current stage on an active application, "
                      "with days counted from when the slot opened; awaiting feedback = interviews in the last 30 days that Greenhouse marks as awaiting feedback, one line per interviewer whose scorecard "
                      "is not submitted, with hours counted from the interview's end; a panel needs a change when someone declined or nobody is on it. Nothing here rates anyone: counts describe calendars. "
                      "Tell me different numbers and I'll redo it.")}
    job = d.get("job") or {}
    if job:
        page["meta"] = _detail([("Req", job.get("req") or "no req id")]) + ([{"label": "Greenhouse", "value": "Open the req", "href": SDASH.format(job["id"])}] if isinstance(job.get("id"), int) else [])
    if not tiles:
        del page["tiles"]
    return _common(d, page)


def expand_source_review(d):
    _need(d, "data", "asOf", "headline", "scope", "counts", "sources")
    c, focus, job = d["counts"], d.get("focus"), d.get("job") or {}
    history = d.get("reached") == "history"
    n = c.get("applications", 0)
    meta = _detail([("Window", d.get("window")), ("Open", job.get("open")), ("Reqs", d.get("reqs")), ("Req", job.get("req") if job else None),
                    ("First interview", job.get("first") or ("set per req from its plan" if d.get("reqs") else None)), ("Final stage", job.get("final") or ("set per req from its plan" if d.get("reqs") else None)),
                    ("Reached", "from stage history" if history else "derived from where each application stands or ended"),
                    ("Confidential", "share only with its hiring team" if job.get("confidential") else None)])
    if isinstance(job.get("id"), int):
        meta.append({"label": "Greenhouse", "value": "Open the req", "href": SDASH.format(job["id"])})
    blank = c.get("blank", 0)
    tiles = [{"label": "Applications", "value": str(n), "sub": c.get("note") or "complete count", "focus": focus == "applications"},
             {"label": "Reached first interview", "value": str(c.get("first", 0)), "sub": f"{c.get('final', 0)} reached the final stage · {c.get('hired', 0)} hired", "focus": focus == "first"},
             {"label": "With a referrer", "value": str(c.get("referrer", 0)), "sub": "also counted under their source", "focus": focus == "referrer"},
             ({"label": "No source recorded", "value": str(blank), "sub": "blank in Greenhouse", "focus": focus == "blank"} if blank
              else {"label": "Sources", "value": str(c.get("sources", 0)), "sub": f"{c.get('nobodyPast', 0)} with nobody past review", "focus": focus == "sources"})]
    for t in tiles:
        if not t["focus"]:
            del t["focus"]
    srcs = _rows(d["sources"], "sources")
    panels = []
    if d.get("namesVisible", True):
        items = []
        for s in srcs:
            active = sum(x[1] for x in (s.get("active") or []) if isinstance(x, list) and len(x) == 2)
            parts = [s.get("type") or ("blank in Greenhouse" if s.get("blank") else None)] + [f"{v} {w}" for v, w in ((active, "active"), (s.get("ended", 0), "ended"), (s.get("hired", 0), "hired")) if v]
            items.append({"label": s.get("name") or "No source recorded", "value": s.get("apps", 0), "sub": " · ".join(x for x in parts if x)})
        panels.append({"type": "bars", "title": f"Applications by source ({n}, created since {d.get('since') or 'the window opened'})",
                       "note": "Bars count applications, not people. Ordered by number of applications, not by merit.", "items": items,
                       "empty": "No applications were created in this window that you can see."})
    rows = []
    for s in srcs:
        apps = s.get("apps", 0)
        src = {"text": s.get("name") or "No source recorded", **({"sub": s["type"]} if s.get("type") else {}), **({"sub": "blank in Greenhouse", "chip": {"kind": "info", "label": "Blank"}} if s.get("blank") else {})}
        row = {"source": src, "applications": apps, "reachedFirst": s.get("first", 0), "reachedFinal": s.get("final", 0), "hired": s.get("hired", 0), "ended": s.get("ended", 0)}
        stages = [{"name": x[0], "n": x[1]} for x in (s.get("active") or []) if isinstance(x, list) and len(x) == 2 and x[1]]
        if stages:
            row["activeNow"] = stages
        rate = lambda k: f"{k} of {apps} ({round(100 * k / apps)}%)" if apps >= 10 else None
        det = _detail([("Ended by", s.get("by")), ("Mostly ended from", s.get("from")), ("Reached first interview", rate(s.get("first", 0))), ("Reached final stage", rate(s.get("final", 0))),
                       ("By req", s.get("byReq")), ("Not placed", s.get("notPlaced"))])
        if det:
            row["_detail"] = det
        rows.append(row)
    foot = " ".join(x for x in (d.get("all"), d.get("fresh")) if x)
    panels.append({"type": "table", "title": "How far each source's applications got", **({"search": True} if len(rows) > 10 else {}),
                   "note": "One row per source. " + ("Reached is from each application's stage history." if history else "Reached is rebuilt from where each application stands or ended (derived)."),
                   "columns": [{"key": "source", "label": "Source"}, {"key": "applications", "label": "Applications", "kind": "num"}, {"key": "activeNow", "label": "Active now", "kind": "stages"},
                               {"key": "reachedFirst", "label": "Reached first interview", "kind": "num"}, {"key": "reachedFinal", "label": "Reached final stage", "kind": "num"},
                               {"key": "hired", "label": "Hired", "kind": "num"}, {"key": "ended", "label": "Ended", "kind": "num"}],
                   "rows": rows, **({"foot": foot} if foot else {})})
    shows = [{"lead": f"{x.get('lead')}:", "text": x.get("text") or "", **({"sub": x["sub"]} if x.get("sub") else {})} for x in _rows(d.get("shows"), "shows")]
    if shows:
        panels.append({"type": "list", "title": "What the numbers show", "half": True, "items": shows})
    panels.append({"type": "list", "title": "Questions for the sourcing sync", "half": bool(shows), "empty": "No question follows from these numbers.",
                   "items": [{"text": q, "copy": True} for q in (d.get("questions") or []) if isinstance(q, str)]})
    days = d.get("days") or 90
    title = f"{job['name']} sources" if job.get("name") else "Sources, my reqs"
    page = {"skill": "source-review", "title": title[:60], "meta": meta, "tiles": tiles, "panels": panels,
            "judged": d.get("judged") or (f"How this was counted: applications created in {d.get('windowWords') or f'the last {days} days'} by created_at, prospects left out, counted as applications and not people; "
                      "a source is the application's source as recorded and a blank one reads \"No source recorded\"; "
                      + (f"first interview = {job['first']}, the first stage after review with Screen, Interview, Onsite or Panel in its name (a pre-screen, assessment or test does not count); " if job.get("first") else "")
                      + (f"final stage = {job['final']}, the last stage that is neither Offer nor Reference; " if job.get("final") else "")
                      + "late stages = the last three on the plan; reached = last known stage at or past that point (a hire reached every stage), or an entry in stage history when it is visible; "
                      "who ended it comes from the rejection reason's type; a percentage needs 10 or more applications behind it (fewer is noise); fresh = created in the last 14 days "
                      "(two weeks is rarely enough to reach an interview); a source question needs 5 or more applications, a withdrawal question 3 or more. Sources are ordered by volume and are not ranked. "
                      "Every threshold is inclusive. Tell me different numbers and I'll redo it.")}
    page = _common(d, page)
    page["notes"] = ["Counts are applications, not people. No candidate, recruiter, sourcer or referrer is named on this page."] + list(d.get("notes") or [])
    return page


SHORT_FORMS = {"configure": expand_configure, "daily-brief": expand_daily_brief, "interview-week": expand_interview_week,
               "pipeline-review": expand_pipeline_review, "source-review": expand_source_review}


def expand(data):
    """Turn a skill's short form into the page schema; pass the page schema through."""
    if isinstance(data, dict) and "panels" not in data and data.get("skill") in SHORT_FORMS:
        return SHORT_FORMS[data["skill"]](data)
    return data


def embed(data):
    """JSON that is safe inside a <script type="application/json"> block."""
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for ch, esc in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026"), (" ", "\\u2028"), (" ", "\\u2029")):
        text = text.replace(ch, esc)
    return text


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default="-", help="page data, JSON (see PAGE.md); \"-\" or omitted: standard input")
    ap.add_argument("--out", required=True, help="where to write the .html page")
    ap.add_argument("--template", default=os.path.join(here, "page.html"))
    ap.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = ap.parse_args()

    try:
        if args.data == "-":
            raw = sys.stdin.buffer.read()
        else:
            with open(args.data, "rb") as fh:
                raw = fh.read()
        if len(raw) > MAX_BYTES:
            sys.exit(f"error: the data is over {MAX_BYTES // 1000} KB; cap the rows and say so in 'cap'")
        data = expand(json.loads(raw.decode("utf-8")))
    except (OSError, ValueError) as exc:
        sys.exit(f"error: cannot read the data: {exc}")
    except ShortFormError as exc:
        sys.exit(f"error: {exc}")
    except (TypeError, KeyError, AttributeError, IndexError) as exc:
        sys.exit(f"error: the short form is malformed ({exc!r}); check it against PAGE.md")

    problems = validate(data)
    if problems:
        print(f"{len(problems)} problem(s); fix the data and run again (never edit the template):", file=sys.stderr)
        for line in problems[:40]:
            print("  - " + line, file=sys.stderr)
        sys.exit(1)
    if args.check:
        print("ok")
        return
    if not args.out.lower().endswith(".html"):
        sys.exit("error: --out must end in .html")
    try:
        with open(args.template, encoding="utf-8") as fh:
            template = fh.read()
    except OSError as exc:
        sys.exit(f"error: cannot read the template: {exc}")
    if template.count(DATA_TOKEN) != 1 or template.count(TITLE_TOKEN) != 1:
        sys.exit("error: the template is not the one shipped with this skill")
    page = template.replace(TITLE_TOKEN, html.escape(str(data["title"]), quote=True)).replace(DATA_TOKEN, embed(data))
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(os.path.abspath(args.out))


if __name__ == "__main__":
    main()
