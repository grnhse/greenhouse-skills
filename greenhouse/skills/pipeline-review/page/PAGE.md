# Pipeline review: how to answer

Read this before answering. Finish the skill's steps, then pick the first shape that fits:

1. **Page and a short reply.** Your app can show a file or a rendered document (one it renders beside the chat), and the user did not ask for chat only (the builder makes the page; where Python cannot run you write it, as "Without Python" says). Build the page (Build, below) and send the short reply.
2. **Short reply only.** No page is possible, or the user asked for chat ("in chat", "no page", "I'm on my phone"). Stay in chat for the rest of the conversation unless they ask for the page.
3. **One part, or the full review, in chat.** Only when the user asks ("show me the funnel", "the roster", "full review", "how was this judged?"): give that part of "Output, full version" at the end of this file, and all of it only for "full review".

## Short reply

Sound like a colleague who has just looked this up for them: plain words, short sentences, the person's first name once when you know it. No headings, no tables, no tool or rule names, nothing about how you got the answer. Everything in the reply is something they can act on or need to know today; the rest waits on the page or for a question. Keep it under about 120 words, not counting a fenced message.

In this order, which replaces the rules block's "headline, then scope line" for this reply:

1. The headline sentence, with their first name in front the first time ("Priya, Onsite holds 6 of 11 active candidates on Senior Backend Engineer.").
2. One sentence with the status word and the number behind it ("It reads as Watch: 4 of the 9 past review have had no activity for a week or more."). On track: say so in a few words.
3. Up to three bullets, most pressing first: who is waiting on a decision, which scorecard is holding things up, who has gone quiet longest. Name and link each person, with the reason in a few words. Nothing pressing: one sentence saying so, no bullets.
4. The hiring-manager message in a code fence, only when the user asked for a sync, an update or a message, or a chat or email tool is connected (then with the send offer from step 5). Otherwise leave it to the page, or in chat-only offer it: "Want a note for the hiring manager?"
5. Where the rest is. With a page: "The stage flow, the funnel, the full roster and the rejections are on the page, with a next prompt to copy on each row." Chat only: "Ask for the funnel, the roster, the rejections or the full review."
6. One sentence, only if something was hidden, declined or could not be checked (the AI opt-out check included): what you could not see, in their words, and the one thing that would fix it ("I couldn't see offers or interview times with your current access; /greenhouse:configure shows what to turn on."; for a declined call, that it is a Greenhouse permission and an admin can change it). The exact footnote goes on the page. An empty list is not a gap: leave it out.
7. The scope line, short: "Counting what you can see in Greenhouse, as of <Wed 14 Oct, 09:00 EDT>."
8. Next: two prompts as text, real names filled in. Never end with a question tool: a pending question can leave the conversation looking stuck.

The thresholds line and the long footnotes are not in the short reply: they are on the page in `judged` and `notes`, and in chat when asked. The headline names the req.

## Data file

File name: `greenhouse-pipeline-<req name in lower-case words joined by hyphens>.html`. Send this short form; the builder writes the tiles, titles, columns, links, status chips and fixed notes from it. Use only these keys, write each value once, and leave a key out when its section was not read.

| Key | What goes in it |
|---|---|
| `skill` | `"pipeline-review"` |
| `view`, `asOf`, `headline`, `scope` | "<Name>'s view" or "your view"; date, time and zone; the headline sentence, naming the req; the scope line without "as of" (it must contain "that you can see") |
| `focus` | the tile whose number the headline states: `active`, `review`, `decisions` or `quiet` |
| `status` | the status word |
| `job` | `{name, id, open, req?, furthest, recruiter?, coordinator?, seats?, offers?, confidential?}`: `id` the job id as a number, `open` "41 days" or "closed; open 41 days", `furthest` "Offer, stage 5 of 5" |
| `counts` | `{active, activeNote?, review, reviewLongest?, decisions, quiet, pastReview}`: `review` the review stage's count and `reviewLongest` its longest wait in days since applying; `decisions` and `quiet` count only applications past review; `activeNote` "at least" when capped |
| `message` | `{text, numbers}`: the hiring-manager message with its line breaks, and the "numbers behind it" line without that label |
| `risks` | rows `{rule, text, why}`, worst first; an empty list when no rule fires |
| `questions` | rows `{to, text, cand?, app?}`: `to` is `hm` or `you` |
| `funnel` | one row per plan stage in plan order: `{name, active, rejected, reached, pass, bottleneck?}`; `bottleneck` on that stage only, as its sub-line ("median 8 days without recorded activity"). The first row is the review stage and is not drawn to scale |
| `reached` | `derived`, or `history` when stage history was read |
| `bottleneck` | the Bottleneck line |
| `managerStages` | the hiring manager's stage names, for the "how this was judged" line |
| `roster` | `{stages, ageLabel, rows, optOut?, more?}`: `stages` the names of the stages holding roster rows; `ageLabel` "Days quiet" or "Days in stage"; rows `{name, cand, app, stage, days, feedback, tally?, status?, detail?}` with `feedback` "4 complete, 1 started but not submitted", `tally` the rating words or the draft-guard sentence, `status` one of Needs decision, Scorecard due, Offer to send, Scheduled, Waiting on candidate (leave out when none applies), `detail` a small object of facts that are visible (Source, Interview, Decision waiting since, Draft); `optOut` the opt-out sentence when the check was absent or declined |
| `rejections` | `{total, we, they, other, rows}`: rows `{reason, n, who, from}` with "No reason recorded" first |
| `notes` | what the chat answer would print under its tables: rule 1's footnote, rule 2 and rule 3 sentences |
| `next` | the Next prompts, one string each |

A private candidate: `"private": true` in place of `name`. An opted-out candidate: `feedback` "feedback withheld: opted out of AI review" and no `tally`. A person whose name could not be resolved: "name not visible". A filled example is in `page/example.json`.

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
4. Show the page at that path the way your app shows files (its file tool, or a link to the file), or as a rendered document when your app shows them beside the chat. After it, say nothing more than "The page is up." or what you could not build.
5. However the page gets made, the user never hears how: no mention of Python, code, scripts, a builder, files or folders, and no "since your app can..." or "because I can't run...". They asked a question; they get the answer and a page.

If Python cannot run, or the build still fails after two fixes, write the page yourself as "Without Python" below says. If the app can show neither a file nor a rendered document: send the short reply on its own and add one plain line, "I couldn't open a page here, so it's all in chat: ask for any section."

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


## Output, full version

This is the Output the skill's steps refer to. In chat, give one part of it when the user asks for that part, and all of it only for "full review".

<Headline sentence from step 5.>
<Job name> · <status word> · <n> active (complete | at least) · roster shows <k> of <m> roster rows that you can see (rejections capped at 1,000: say so here), as of <Wed 14 Oct, 09:00 EDT>.

**<Job name>** · <open n days | closed; open n days> · req <requisition_id or "no req id"> · furthest: <stage>, stage k of n · recruiter <name> · coordinator <name> · seats and offers when visible · https://app.greenhouse.io/sdash/<job_id>

### Hiring-manager message (safe to share)
```
Hi <HM first name>,
<One or two sentences by rung (step 4).>
One ask: <first "Ask the hiring manager" question, its candidate named only when in the final stage or Offer and otherwise "a candidate in <stage>"; or "Nothing needed from you this week.">
<User first name, when known>
Numbers as of <Wed 14 Oct>
```
The numbers behind it: <a> active · <r> rejected in 30 days · <h> hired · by stage <Stage> <n> · ... · interviews next 7 days: <n | not visible> · offers outstanding: <n | not visible | none that you can see>

### Risks
- **<Rule name>**: <the req's numbers and the why>. Empty: "No rule fires; not a green light."

### Funnel, plan order
| Stage | Active now | Rejected from here, last 30 days | Reached at least (derived) | Pass-through to next |
|---|---|---|---|---|
Reached is rebuilt from where each application ended or stands today.

**Bottleneck:** <stage>: <n> active, median <d> days without recorded activity | in stage.

### Late stages: <names of the stages holding roster rows> (Ordered by stage reached, not by strength.)
| Candidate | Stage | Days quiet or in stage | Feedback | Flags |
|---|---|---|---|---|
| [Name](https://app.greenhouse.io/people/<candidate_id>?application_id=<application_id>) | Onsite | 11 without recorded activity | 3 complete, 1 started but not submitted: 2 Yes, 1 No | decision waiting · interview Thu 10:00 · source Referral |
AI opt-out status could not be checked for these candidates. (only when the tool is absent)

### Questions for the sync
**Ask the hiring manager**: the manager-stage questions, each with its link. **Stays with you**: "<n> in review, longest <d> days", then the rest.

### Rejections, last 30 days (<n>: we declined <n> · withdrew <n> · other or none recorded <n>)
| Reason (as recorded) | Who ended it | Count | Mostly from stage |
|---|---|---|---|
Empty: "None that you can see in the last 30 days."

How this was judged: bottleneck = the stage with the most active candidates, tie broken by the oldest median activity; quiet = no activity recorded for 7 or more days (a week untouched is when candidates accept other interviews); an offer is outstanding after 7 days in Created (a week unanswered needs a follow-up); rejections cover the last 30 days by rejected_at; the roster shows at most 50 rows, latest stage first, then longest without activity; questions on <manager stages> go to the hiring manager, the rest stay with you. Risk rules: at risk = 30+ days open, nobody past the first interview; slow = 60+ days, no finalist; gone quiet = 3+ past review, half quiet; thin = 2 or fewer past review; pass-through needs 20 resolved (10 for an early signal); a median needs 3 values; a draft within 30 days hides a tally. Every threshold is inclusive. Tell me different numbers and I'll redo it.

Hidden tools only: rule 1's footnote naming just those items: days in stage and pass-through (harvest:application_stages:list), offers (harvest:offers:list plus the private-data permission), seats (harvest:openings:list), hiring manager (harvest:job_hiring_managers:list), interviews (harvest:interviews:list), sources (harvest:sources:list), opt-out flags (harvest:ai_opt_out_statuses:list). Declined: rule 2's sentence.

Next: "/greenhouse:candidate-debrief <first roster row with a decision waiting> on <req>" · "/greenhouse:candidate-status <roster row quiet longest>" · "/greenhouse:daily-brief"
