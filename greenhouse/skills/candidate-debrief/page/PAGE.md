# Candidate debrief: how to answer

Read this before rendering. Finish the skill's steps, then:

1. **Chat reply, always.** The debrief ends in a decision the user states and a confirm-first card, so the answer is in chat.
2. **Page as well, only when asked** ("as a page", "something I can put on screen in the debrief") and your app can show a file or a rendered document. Never for an opted-out candidate, and never while the user's own scorecard on this application is a draft: say why in one line.

## Chat reply

Send "Output, full version" (at the end of this file) with these cuts, so the evidence is all there and nothing else is:

- Line 1's tally names only the rating words someone gave: "3 of 4 scorecards are in: Yes 2 · No 1." No zero slots.
- With fewer than two complete scorecards, leave out "Where they agree and disagree" and say "One view so far." in line 1.
- A section with nothing in it is left out, not printed empty: no "Owed" when every scorecard is in (say so in line 1), no "Recruiter notes" when there are none.
- The opt-out check gets one plain sentence at most, with no tool name: "I couldn't check whether <Name> opted out of AI review; that is a permission on your Greenhouse account." when the call was declined, else "AI opt-out status could not be checked."
- Line 2 opens with the candidate's name linked to the profile, never a bare address.
- The "How this was counted" line only when asked.
- Close with one line, "For the hiring team only, never a candidate; private notes are left out, ask to see them.", then "The decision is yours. Tell me what you decided and I'll preview the note or the move.", then Next.

With a page: after the first two Output lines say "The evidence brief is on the page.", then the opt-out sentence when one applies, the closing lines and Next. Cards for a note or a move are always in chat.

## Panels

File name: `greenhouse-debrief-<candidate name in lower-case words joined by hyphens>.html`. Title: "<Name> debrief". `audience` is `hiring-team`.

`meta`: Job, Stage ("<Current>, k of n"), Next stage, Needs Decision ("Greenhouse marks a decision as waiting" or "not set"), Greenhouse (`value` "Open the profile", `href` the profile link). `tiles`: Scorecards in ("<N> of <M>", `focus`), Still owed, Interviews to come (only with `list_interviews`).

| # | Panel | From step 5 |
|---|---|---|
| 1 | `steps` "Where <Name> is in the plan" | one pill per active stage in plan order: `done` before the current stage, `here` on it, `ahead` after |
| 2 | `tally` "Ratings as given (complete scorecards only)" | one entry per rating word that someone gave, in the order Strong Yes, Yes, No, Definitely Not, No Decision, `people` the interviewers who gave it; `foot` "Shown as given: no average, no majority, no leaning." |
| 3 | `table` "Interviewers" | columns Interviewer, Interviewed, Rating, Status, Takeaways (the quotes exactly as chosen for the chat table; "to the team:" quotes labelled); draft rows carry no rating and no quote |
| 4 | `list` "Where they agree and disagree", `half` | only with two or more complete scorecards: one item per pairing, the lone dissent first; `lead` the names and ratings |
| 5 | `list` "Open questions for the panel", `half` | one item per question, `copy: true` |
| 6 | `list` "Owed" | `lead` the interviewer, `text` "interviewed <date>, scorecard still draft (<n> days)", `copy` the two-line nudge; `empty` "Every scorecard for this round is in." |

Private notes never go on the page, even when the user asked to see them in chat. `notes` carries "Private notes not shown.", the opt-out sentence and "Interview feedback: hiring team only, never to a candidate."

## Build

1. Finish the skill's steps first. The page shows what they computed and what the chat answer would have shown, nothing more: the same guards, caps and hidden rows apply.
2. Send the short reply as text first, so the answer is on screen while the page is built. Then, in the same turn, build the page with one shell call, the data on standard input:

   ```
   python3 "<this skill's folder>/page/build_page.py" --out "<outputs folder>/<the file name this file gives>" <<'GH_PAGE_DATA'
   { ...the data this file describes, as JSON... }
   GH_PAGE_DATA
   ```

   The outputs folder is where your app keeps files it shows the user (its outputs directory; in a terminal app the session's scratch or temporary directory, never the user's project). On success it prints the path of the page. No data file is written, so there is nothing to delete.
3. If it prints problems, fix the data and run it again, twice at most. Never edit `page.html`, and never write or patch the HTML yourself.
4. Show the page the way your app shows files (its file tool, or a link to the file), giving it that path. After it, say nothing more than "The page is up." or what you could not build.
5. However the page gets made, the user never hears how: no mention of Python, code, scripts, a builder, files or folders, and no "since your app can..." or "because I can't run...". They asked a question; they get the answer and a page.

If Python cannot run, or the build still fails after two fixes, write the page yourself as "Without Python" below says. If the app can show neither a file nor a rendered document: send the chat reply on its own and add one plain line, "I couldn't open a page here, so it's all in chat: ask for any section."

To keep it quick: read this file in your first turn, alongside the skill's first Greenhouse calls, not after them; keep each batch of Greenhouse calls in one turn; write the data once, compactly, with no keys the format does not ask for.

## Without Python

The same page written by hand, for an app that can show a rendered document or an HTML file and cannot run the builder. It is a still page, not an app, so keep it small and it stays quick.

1. Send the short reply first, as always. This page has no buttons, so where the reply says what the page can do, say only where the rest is ("It's all on the page."): nothing about filtering, copying or prompts on rows.
2. Write one self-contained HTML document, as a rendered document when your app shows them beside the chat, and otherwise as a file with the name this file gives. Copy this frame and its style block exactly, and change only the words in capitals and the rows:

   ```html
   <!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TITLE</title>
   <style>:root{--s:#fff;--a:#efefef;--i:#15372c;--m:#526b63;--r:#d8d8d8;--l:#054ab2;--o:#ffa52e;--act:#ffe5e3;--wait:#ffecd4;--good:#e6fff8}@media(prefers-color-scheme:dark){:root{--s:#15372c;--a:#031c17;--i:#fff;--m:#a1b4ad;--r:#335247;--l:#a7c4f1;--act:#335247;--wait:#335247;--good:#335247}}*{box-sizing:border-box}body{margin:0;background:var(--s);color:var(--i);font:14px/1.35 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}main{max-width:1100px;margin:0 auto;padding:20px 16px 40px}h1{font:400 26px/1.15 Georgia,serif;margin:6px 0 8px}h2{font-size:14px;margin:0 0 8px}small,.m{color:var(--m);font-size:12px}a{color:var(--l)}.t{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0 12px}.p{border:1px solid var(--r);border-radius:8px;padding:12px 14px;margin:0 0 12px;overflow-x:auto}.t .p{margin:0}.t b{display:block;font-size:26px}.f{border-top:3px solid var(--o)}table{width:100%;border-collapse:collapse}th{text-align:left;font-size:12px;color:var(--m);font-weight:400}th,td{padding:7px 8px;border-bottom:1px solid var(--r);vertical-align:top}.n{text-align:right}.c{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;background:var(--a);white-space:nowrap}.c.act{background:var(--act)}.c.wait{background:var(--wait)}.c.good{background:var(--good)}.b{display:inline-block;height:10px;border-radius:0 4px 4px 0;background:#24a47f;vertical-align:middle;margin-right:6px}</style>
   <main>
   <small>Greenhouse data via the Greenhouse plugin · VIEW · as of AS OF</small>
   <h1>HEADLINE</h1><p class="m">SCOPE</p>
   <div class="t"><div class="p f"><small>TILE LABEL</small><b>3</b><small>TILE SUB-LINE</small></div></div>
   <section class="p"><h2>SECTION TITLE (COUNT)</h2><p class="m">ITS LEAD LINE</p>
   <table><tr><th>CANDIDATE</th><th class="n">DAYS QUIET</th><th>STATUS</th></tr>
   <tr><td><a href="https://app.greenhouse.io/people/1?application_id=2">NAME</a></td><td class="n"><span class="b" style="width:60px"></span>11</td><td><span class="c act">Needs decision</span></td></tr></table></section>
   <p class="m">THE "HOW THIS WAS ..." LINE</p><p class="m">FOOTNOTES</p><p class="m">Next: THE NEXT PROMPTS</p>
   </main></html>
   ```

   Up to four tiles: the counts the sections lead with, the headline's first; class `f` only on the tile the headline is about. A chip goes wherever the Output has a status word, and a bar beside any column of days. Then one section per section of "Output, full version" at the end of this file, in the same order with the same columns; a section that is empty is its one plain sentence, and a section that was not read is left out.
3. The builder is not there to check the page, so you do: no script, no image, no font or other outside resource; links only to `https://app.greenhouse.io/`; write `&amp;`, `&lt;` and `&gt;` for &, < and > in every value; never an email address, a phone number or an amount of money; at most 10 rows in a table, then "and N more". A bar's width is its number as a share of the largest in that column, up to 120px. Chips describe a step, never a person: `act` a decision or action is outstanding, `wait` waiting on a scorecard or a review, `good` done or healthy, no class for the rest.
4. Show it, then say "The page is up." Say nothing about Python, and do not call it a simpler page.

## Next prompts

The page lists the Next prompts with copy buttons, because a page cannot send a message into the conversation. In chat, print them as text. Do not offer them through a question tool: a pending question can leave the conversation looking stuck. A prompt for the daily brief needs no name in it; a debrief or status prompt always names a candidate, and is left out when there is nobody to name.

## Data file

One JSON object. Unknown keys are rejected, so use only these. Every value comes from a tool result in this conversation; write text exactly as Greenhouse returned it and let the builder do the escaping.

| Key | What goes in it |
|---|---|
| `skill` | this skill's name |
| `title` | two to four words naming the thing ("Senior Backend Engineer pipeline"), never "Dashboard" |
| `view` | "<Name>'s view" with as much of their name as you know, or "your view" |
| `asOf` | date, time and zone: "Wed 14 Oct, 09:00 EDT" |
| `headline` | the skill's headline sentence, unchanged |
| `scope` | the scope line without its "as of" part; must contain "that you can see" |
| `audience` | `"hiring-team"`, always, on this page |
| `meta` | up to 8 facts under the headline, each `{label, value, href?}` |
| `tiles` | up to four `{label, value, sub?, focus?}`; `focus: true` on the one tile the headline is about, on none when the headline is about something no tile counts; a tile whose count is zero stays, a tile whose section was not read is left out |
| `filter` | optional `{key, label}`: one row of chips that filters every table having that column key |
| `panels` | the panels listed under "Panels", in that order; leave out a panel whose section is hidden by a missing tool |
| `judged` | the skill's "How this was ..." line, whole |
| `notes` | everything the chat answer would print under its tables, as separate strings: rule 1's footnote, rule 2 and rule 3 sentences, the opt-out sentence, how the run was scoped when it was not the default |
| `cap` | one clause when rows were capped ("roster capped at 50 rows") |
| `next` | the Next prompts, one string each, filled with real names |

Every panel has `type` and `title`, and may have `note` (one muted line under the title), `empty` (the skill's empty-state sentence for that section, or "None that you can see." where it has none; shown when the panel has no rows), `foot`, and `half: true` (sits beside the next half panel on a wide screen; only for a list or a table of four columns or fewer).

| `type` | Fields |
|---|---|
| `table` | `columns`: one to eight `{key, label, kind}` (`kind` is `text` when left out). `rows`: objects keyed by column key, plus optional `_detail`: up to 12 `{label, value, href?}` shown when the row is opened. Optional `filter` (a column key: chips with counts), `search: true`, `more` ("and 4 more"). At most 500 rows. |
| `funnel` | `stages` in plan order, each `{name, active, rejected?, reached?, pass?, flag?, sub?, scale?}` (`scale: false` shows that stage as a number without a bar); `unit` |
| `bars` | `items`: `{label, value, sub?}`, drawn in the order given |
| `message` | `text` (line breaks kept); the page adds a copy button |
| `list` | `items`: `{text, lead?, sub?, href?, chip?, copy?}`; `copy: true` adds a copy button for the text; `href` shows as "Open in Greenhouse" beside the text |
| `steps` | `stages`: `{name, state, sub?}` with `state` one of `done`, `here`, `ahead`: the stage plan as connected pills |
| `timeline` | `events`: `{when, title, sub?, href?, chip?}`, oldest first |
| `tally` | candidate-debrief only. `ratings`: `{label, people}` in Greenhouse's order, `people` a list of interviewer names |

Column kinds: `text` (a string, or `{text, sub?, chip?}`), `link` (`{text, href, sub?}`), `num` (right-aligned), `days` (a number, drawn with a bar), `chip` (`{kind, label}`), `stages` (`[{name, n}]`: the stages holding at least one active application, in plan order, drawn as one segmented bar with the counts written under it).

Chip kinds describe a step in the process, never a person: `act` (a hiring-team decision or action is outstanding: Needs decision, Offer to send), `wait` (waiting on a scorecard, review or approval: Scorecard due, Bottleneck), `idle` (nothing needed now: Scheduled, Waiting on candidate), `good` (done or healthy: Submitted, Moving), `info` (a fact: Referral, New).

The builder enforces: links only to `https://app.greenhouse.io/`, and no email address, phone number or amount of money anywhere on the page. The skill's own rules still apply to every string: names and stage names, never raw ids; a person whose name could not be resolved reads "name not visible", never an empty cell; a blank is written as the finding it is ("no recruiter"), never dropped. A filled example on a fictional organization is in `page/example.json`.

## Output, full version

This is the Output the skill's steps refer to. The chat reply above says which parts of it to send.

```
<N> of <M> scorecards are in: Strong Yes <n> · Yes <n> · No <n> · Definitely Not <n> · No Decision <n>. <Owed>'s is still a draft. One interview is still to come on <date> (omit without `list_interviews`).
<profile link> · <Job> · stage <Current> (k of n), next <Next> · Needs Decision: <Greenhouse marks a decision as waiting | not set> · scorecards that you can see · as of <date and time>

| Interviewer | Interviewed | Rating | Status | Takeaways |
|---|---|---|---|---|
| <name> | <date> | Yes | complete, submitted 5 days after the interview | "<quote>" · to the team: "<quote>" |
| <name> | <date> | — | draft, not submitted | |

### Where they agree and disagree
- <A> (Strong Yes): "<quote>" vs <B> (No): "<quote>"
- Where they agree: <rating or attribute>
### Owed
- <name>: interviewed <date>, scorecard still draft (<n> days)
  ```<nudge>```
### Open questions for the panel
- <question>

How this was counted: complete scorecards only; a draft is owed once its interview date has passed; "submitted n days after" shows past two calendar days: the gap is worth knowing, never a discount; k of n counts active stages. Tell me different numbers and I'll redo it.
Not visible with your Greenhouse MCP access: <sections> (needs <scope keys>). <rest of the rule 1 footnote>
AI opt-out status could not be checked.
Private notes not shown; ask to see them.
Interview feedback: hiring team only, never to a candidate.
The decision is yours. Tell me what you decided and I'll preview the note or the move.
Next: /greenhouse:candidate-status <Name> · /greenhouse:pipeline-review <Job>
```
