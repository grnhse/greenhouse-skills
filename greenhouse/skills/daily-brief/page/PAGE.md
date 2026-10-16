# Daily brief: how to answer

Read this before answering. Finish the skill's steps, then pick the first shape that fits:

1. **Page and a short reply.** Your app can show a file or an artifact, and the user did not ask for chat only (the builder makes the page; where Python cannot run you write it, as "Without Python" says). Build the page (Build, below) and send the short reply. A second brief in the same conversation builds a new page and opens the reply with what moved.
2. **Short reply only.** No page is possible, or the user asked for chat ("in chat", "no page", "I'm on my phone"). Stay in chat for the rest of the conversation unless they ask for the page.
3. **One section, or the full brief, in chat.** Only when the user asks ("show me the quiet ones", "the snapshot", "full brief", "how was this ranked?"): give that section of "Output, full version" at the end of this file, and all of it only for "full brief".

## Short reply

Sound like a colleague who has just looked this up for them: plain words, short sentences, the person's first name once when you know it. No headings, no tables, no tool or rule names, nothing about how you got the answer. Everything in the reply is something they can act on or need to know today; the rest waits on the page or for a question. Keep it under about 120 words, not counting a fenced message.

In this order, which replaces the rules block's "headline, then scope line" for this reply:

1. A greeting with their first name when you know it, by their local time ("Morning, Priya." before noon, "Afternoon, Priya." after; no name and no zone: skip it), then the headline sentence.
2. Up to three bullets, most urgent first, starting with whatever the headline is about (when it is a count on one req, say so in one bullet with the req linked), then across decisions waiting, scorecards holding things up and people gone quiet: name and link each person, their req, and why in a few words ("decision waiting, quiet 11 days"), using the same age the page's column shows for that row. Nothing needs them: say exactly that in one warm, plain sentence and skip the bullets.
3. One line for what else there is beyond the bullets, counts only, leaving out zeros: "Also: 4 scorecards not submitted, 5 quiet candidates, 9 new applicants."
4. Where the rest is. With a page: "It's all on the page: filter it by req, and each row has its next prompt to copy." Chat only: "Ask for decisions, scorecards, quiet candidates, new applicants or the snapshot."
5. Only when scorecards are outstanding. With a page: "Reminders for the 3 interviewers are on the page to copy." Chat only, one short question: "Want me to draft reminders for the 3 interviewers?"
6. One sentence, only if something was hidden or declined: what you could not see, in their words, and the one thing that would fix it ("I couldn't see interview times or offers with your current access; /greenhouse:configure shows what to turn on."; for a declined call, that it is a Greenhouse permission and an admin can change it). The exact footnote goes on the page. An empty list is not a gap: leave it out, with one exception: people stand in the stage named Offer and no offer came back ("No offer is on record for the 2 people in Offer, or your access hides offers.").
7. The scope line, short: "Across your <N> open reqs, counting what you can see in Greenhouse, as of <Wed 14 Oct, 09:00 EDT>." When the reqs were named by the user, say "the <N> reqs you named".
8. Next: two prompts as text, real names filled in. Never end with a question tool: a pending question can leave the conversation looking stuck.

The ranking line, the long footnotes and the per-section lead lines are not in the short reply: they are on the page in `judged`, `notes` and each panel's `note`, and in chat when asked. Nudges and posting a snapshot stay in the conversation, as steps 7 and 8 say.

## Data file

File name: `greenhouse-daily-brief-<yyyy-mm-dd>.html`. Send this short form; the builder writes the tiles, titles, columns, links, status chips and fixed notes from it. Use only these keys, write each value once, and leave a key out when its section was not read (a section that was read and is empty is an empty list).

| Key | What goes in it |
|---|---|
| `skill` | `"daily-brief"` |
| `view`, `asOf`, `headline`, `scope` | "<Name>'s view" or "your view"; date, time and zone; the headline sentence; the scope line without "as of" (it must contain "that you can see") |
| `day` | the date for the title: "15 Oct" |
| `focus` | which tile the headline is about: `decisions`, `scorecards`, `quiet` or `new`; leave out when none |
| `decisions` | rows `{name, cand, app, req, stage, cards, days, hm?}`: `cand` and `app` are the candidate and application ids as numbers (the builder makes the link), `cards` is "3 in, 0 draft", `hm` the hiring manager when visible |
| `scorecards` | `{interviewers, owed?, rows}`; `owed: true` when interviews were visible (the section is then "Feedback owed"); rows `{who, name, cand, app, req, on, hours, last?}`: `who` the interviewer, `on` the interview date, `last: true` for the last open scorecard on that application |
| `interviews` | rows `{when, name, cand, app, req, status?}` |
| `quiet` | rows `{name, cand, app, req, stage, days, late?, co?}`: `late: true` for the last two stages, `co` the coordinator's name |
| `new` | `{applicants, fresh, byReq, feedback}`: `byReq` is `[[req name, count], ...]`, `feedback` rows `{name, cand, app, req}` |
| `offers` | rows `{name, cand, app, req, sent?, start?}`; never an amount |
| `snapshot` | one row per req: `{req, job, open, status?, active, review, stages, decisions, quiet, new, needs, hm?, coordinator?}`: `job` the job id as a number, `review` the first stage's count, `stages` `[[stage name, count], ...]` past the first stage in plan order, `needs` the Needs review text ("0 in review" when nobody is), `hm` the hiring managers' names joined with commas |
| `totals` | `{decisions, scorecards, quiet}` only when a section was capped at 10 rows |
| `thresholds` | `{quiet, first, cards}` only when the user changed them |
| `notes` | what the chat answer would print under its tables: rule 1's footnote, rule 2 and rule 3 sentences, how the run was scoped when not the default |
| `next` | the Next prompts, one string each |

A private candidate: `"private": true` in place of `name`. A person whose name could not be resolved: "name not visible". A filled example is in `page/example.json`.

## Build

1. Finish the skill's steps first. The page shows what they computed and what the chat answer would have shown, nothing more: the same guards, caps and hidden rows apply.
2. Send the short reply as text first, so the answer is on screen while the page is built. Then, in the same turn, build the page with one shell call, the data on standard input:

   ```
   python3 "<this skill's folder>/page/build_page.py" --out "<outputs folder>/<the file name this file gives>" <<'GH_PAGE_DATA'
   { ...the data this file describes, as JSON... }
   GH_PAGE_DATA
   ```

   The outputs folder is where your app keeps files it shows the user (its outputs or artifacts directory; in a terminal app the session's scratch or temporary directory, never the user's project). On success it prints the path of the page. No data file is written, so there is nothing to delete.
3. If it prints problems, fix the data and run it again, twice at most. Never edit `page.html`, and never write or patch the HTML yourself.
4. Show the page with your app's own file or artifact tool, giving it that path. After it, say nothing more than "The page is up." or what you could not build.
5. However the page gets made, the user never hears how: no mention of Python, code, scripts, a builder, files or folders, and no "since your app can..." or "because I can't run...". They asked a question; they get the answer and a page.

If Python cannot run, or the build still fails after two fixes, write the page yourself as "Without Python" below says. If the app has no way to show a file or an artifact at all: send the short reply on its own and add one plain line, "I couldn't open a page here, so it's all in chat: ask for any section."

To keep it quick: read this file in your first turn, alongside the skill's first Greenhouse calls, not after them; keep each batch of Greenhouse calls in one turn; write the data once, compactly, with no keys the format does not ask for.

## Without Python

The same page written by hand, for an app that can show an artifact or an HTML file and cannot run the builder. It is a still page, not an app, so keep it small and it stays quick.

1. Send the short reply first, as always. This page has no buttons, so where the reply says what the page can do, say only where the rest is ("It's all on the page."): nothing about filtering, copying or prompts on rows.
2. Write one self-contained HTML document, as an artifact when your app has them and otherwise as a file with the name this file gives. Copy this frame and its style block exactly, and change only the words in capitals and the rows:

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


## Output, full version

This is the Output the skill's steps refer to. In chat, give one section of it when the user asks for that section, and all of it only for "full brief".

```
<headline from the step 6 ladder>
Across your <N> open reqs as recruiter or coordinator ("the <N> reqs you named" when run from names), counting active candidates that you can see · as of <Wed 14 Oct, 09:00 EDT>.

### Decisions waiting (<D>)
Greenhouse flags these as ready for a decision: interviews are done and none is recorded. Already decided and holding the move on purpose? Ignore the flag.
| Candidate | Req | Hiring manager (when visible) | Stage | Scorecards (14 days) | Days quiet | Next step |
| [Name](https://app.greenhouse.io/people/<candidate_id>?application_id=<application_id>) | <req> | <name> | Onsite | 3 in, 0 draft | 4 | in Onsite, decision waiting, no activity recorded for 4 days; debrief, then record the outcome in Greenhouse |

### Scorecards started but not submitted (<F> scorecards, <I> interviewers, last 14 days)   ("Feedback owed" when interviews are visible)
Interviewers who haven't opened their scorecard show up only with interview access (harvest:interviews:list).   (default tools only)
**<Interviewer name>** (2)
| Candidate | Req | Interviewed | Hours since interview | Last open scorecard |
Want reminders drafted for the <n> interviewers with an unsubmitted scorecard?

### Quiet candidates (<Q>)
| Candidate | Req | Stage | Days since last activity | Next step |

### New since yesterday (<X> applicants, <S> fresh scorecards)
- <Req>: 4 new applicants ([Name], [Name], ...)
- Fresh feedback: [Name] (<req>)

### Pipeline snapshot
| Req | Days open | Status | Active | In review | Past review, by stage (plan order) | Needs review (in review · 7+ days · oldest applied) | Decisions | Quiet | New | Hiring manager (Coordinator when it isn't visible) |
| [Req](https://app.greenhouse.io/sdash/<job_id>) | 41 | Decisions waiting | 23 | 12 | Phone Screen 6 · Onsite 4 · Other stage 1 | 12 · 5 · 29 Sep | 3 | 1 | 2 | <name> |

How this was ranked: quiet is 14 or more days without recorded activity (7 in the first stage, where the clock runs from the day they applied), because a week without a first look is when applicants start accepting other interviews; scorecards count when started and not submitted within 14 days; "Decisions waiting" is Greenhouse's needs_decision flag on applications past the first stage: interviews are complete and no decision is recorded; applications still in review are counted under Needs review. Every threshold is inclusive. Tell me different numbers and I'll redo it.
Not visible with your Greenhouse MCP access: <sections> (needs <scope keys>). <the rest of rule 1's footnote, verbatim>
Next: /greenhouse:candidate-debrief <name> on <req> · /greenhouse:pipeline-review <req> · /greenhouse:candidate-status <name>
```

An empty section is one plain sentence ("Nothing is waiting on a decision."), except the scorecard visibility line in step 6; never estimate a count.
