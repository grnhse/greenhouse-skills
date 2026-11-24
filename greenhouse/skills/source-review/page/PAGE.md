# Source review: how to answer

Read this before answering. Finish the skill's steps, then pick the first shape that fits:

1. **Page and a short reply.** Your app can show a file or a rendered document (one it renders beside the chat), and the user did not ask for chat only (the builder makes the page; where Python cannot run you write it, as "Without Python" says). Build the page (Build, below) and send the short reply.
2. **Short reply only.** No page is possible, or the user asked for chat ("in chat", "no page", "I'm on my phone"). Stay in chat for the rest of the conversation unless they ask for the page.
3. **One part, or the full review, in chat.** Only when the user asks ("show me the table", "the referrals", "the questions", "full review", "how was this counted?"): give that part of "Output, full version" at the end of this file, and all of it only for "full review".

## Short reply

Sound like a colleague who has just looked this up for them: plain words, short sentences, the person's first name once when you know it. No headings, no tables, no tool or rule names, nothing about how you got the answer. Everything in the reply is something they can act on or need to know today; the rest waits on the page or for a question. Keep it under about 120 words.

In this order, which replaces the rules block's "headline, then scope line" for this reply:

1. The headline sentence, with their first name in front the first time ("Priya, 30 applications on Senior Backend Engineer in the last 90 days came from 6 sources; Careers page brought the most, 11.").
2. One sentence on how far they got, in counts ("19 reached Recruiter Screen, 10 reached Onsite and 1 was hired."), and the fresh-applications clause when a third or more of them are 14 days old or less.
3. Up to three bullets, in this order, each a source and its numbers, never a person: applications with no source recorded; sources with applications and nobody past review; the sources behind the people now in late stages ("Technical Interview, Onsite and Offer hold 8: Careers page 3, Referral 3, Agency 1, Sourced 1"). When the ask was about one source or about referrals, the first bullet is that row or the referrer line with what it counts. Nothing to flag: one sentence saying so, no bullets.
4. The first question for the sourcing sync, as a sentence: "One to raise: ...".
5. Where the rest is. With a page: "Every source, the referrer line and the other questions are on the page." Chat only: "Ask for the table, the referrals, the questions or the full review."
6. One sentence, only if something was hidden or declined: what you could not see, in their words, and the one thing that would fix it ("I couldn't see source names with your current access, so this is totals only; /greenhouse:configure shows what to turn on."; for a declined call, that it is a Greenhouse permission and an admin can change it). The exact footnote goes on the page. An empty list is not a gap: leave it out.
7. The scope line, short: "Counting applications created since <17 Jul> that you can see in Greenhouse, as of <Thu 15 Oct, 09:00 EDT>." Across reqs: "on your <N> open reqs".
8. Next: two prompts as text, real names filled in. Never end with a question tool: a pending question can leave the conversation looking stuck.

The counting line and the long footnotes are not in the short reply: they are on the page in `judged` and `notes`, and in chat when asked. The reply never calls a source good, bad, best or worst, and names no candidate, recruiter, sourcer or referrer.

## Data file

File name: `greenhouse-sources-<req name in lower-case words joined by hyphens>.html`, or `greenhouse-sources-my-reqs-<yyyy-mm-dd>.html` across reqs. Send this short form; the builder writes the tiles, titles, columns, links, status chips, fixed notes and the "Copy prompt" on each row from it. Use only these keys, write each value once, and leave a key out when its section was not read (a section that was read and is empty is an empty list).

| Key | What goes in it |
|---|---|
| `skill` | `"source-review"` |
| `view`, `asOf`, `headline`, `scope` | "<Name>'s view" or "your view"; date, time and zone; the headline sentence; the scope line without "as of" (it must contain "that you can see") |
| `job` | one req: `{name, id, open, req?, first, final, confidential?}`: `id` the job id as a number, `open` "41 days", `first` and `final` the stage names used. Across reqs: leave it out and send `reqs` ("4 open reqs") |
| `window`, `since`, `days`, `windowWords?` | "17 Jul to 15 Oct, 90 days, by application date"; "17 Jul"; 90; `windowWords` only when it is not "the last <days> days" ("since it opened on 1 Dec 2025") |
| `reached` | `derived`, or `history` when stage history was read |
| `focus` | the tile the headline is about: `applications`, `first`, `referrer`, `blank` or `sources` |
| `counts` | `{applications, note, first, final, hired, referrer, blank, sources, nobodyPast}`: `note` "created in the last 90 days · complete count" or "at least" |
| `sources` | one row per source in the skill's order, "No source recorded" first: `{name, type?, blank?, apps, active, first, final, hired, ended, by?, from?, byReq?, notPlaced?}`: `active` `[[stage name, count], ...]` in plan order (across reqs the three groups), `by` "we declined 5 · withdrew 2", `from` the stage most of them ended from. The builder works out the percentages, and only for ten or more applications |
| `namesVisible` | `false` when `list_sources` was hidden (the rows are then "No source recorded", "Source recorded, name not visible" and "All applications") |
| `all`, `fresh` | the "All applications: ..." line and the fresh-applications sentence |
| `shows` | rows `{lead, text, sub?}` for No source recorded, With a referrer, Nobody past review and Behind the late stages, as step 4 words them |
| `questions` | the questions for the sourcing sync, one string each |
| `notes` | rule 1's footnote, rule 2 and rule 3 sentences |
| `next` | the Next prompts, one string each |

No row names a candidate, a recruiter, a sourcer or a referrer. A filled example is in `page/example.json`.

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

<Headline sentence from step 4.>
<Job name, or "Your <n> open reqs as recruiter or coordinator"> · applications created <17 Jul> to <15 Oct> (<90 days>) · <N> applications (complete | at least) from <k> sources that you can see, as of <Thu 15 Oct, 09:00 EDT>.

**<Job name>** · <open n days | closed; open n days> · req <requisition_id or "no req id"> · first interview = <stage> · final stage = <stage> · https://app.greenhouse.io/sdash/<job_id>
<F> of the <N> were created in the last 14 days and have had little time to move. (the req opened <d> days ago, so this is every application on it.)

### How far each source's applications got
| Source (type) | Applications | Active now, by stage | Reached first interview (derived) | Reached final stage (derived) | Hired | Ended (we declined · withdrew · other or none recorded) |
|---|---|---|---|---|---|---|
| No source recorded | 2 | 1: Application Review 1 | 1 | 0 | 0 | 1 (1 · 0 · 0) |
| Careers page (Company marketing) | 11 | 3: Technical Interview 1 · Onsite 2 | 8 of 11 (73%) | 4 of 11 (36%) | 1 | 7 (5 · 2 · 0) |
| Job board (Third-party boards) | 8 | 2: Application Review 1 · Recruiter Screen 1 | 2 | 0 | 0 | 6 (5 · 0 · 1) |
| **All applications** | <N> | <a> | <k> of <N> (p%) | <k> of <N> (p%) | <h> | <e> (<d> · <w> · <o>) |
Counts are applications, not people. Ordered by number of applications, not by merit. Reached is rebuilt from where each application stands or ended. (with stage history: "Reached is from each application's stage history." and no "(derived)" in the headings)
Without source names: the rows are "No source recorded", "Source recorded, name not visible" and "All applications", then "<n> applications across <k> recorded sources, names not visible."

### Referrals
<R> of the <N> applications carry a referrer: <a> active, <k> reached <first interview stage>, <k> reached <final stage>, <h> hired, <e> ended. <m> of them sit under a source named or typed Referral. (only with source names)
This is Greenhouse's "who gets credit" field; it can also hold an agency recruiter or the colleague who added the candidate, and these applications are also counted under their source. Referrers are not named here.
Empty: "No application in this window carries a referrer that you can see."

### Nobody past review
- <Source>: <n> applications, none reached <first interview stage>: <k> still active before it, <m> ended before it.
<s> of the <k> sources have applications and nobody who reached <first interview stage>. Empty: "Every source has someone past review."

### Behind the late stages
<Late stage names> hold <n> active applications: <Source> <a>, <Source> <b>, ... Empty: "Nobody is in <late stage names> from this window."

### Questions for the sourcing sync
1. <the first four that apply, step 4, each with its numbers>
Empty: "No question follows from these numbers."

How this was counted: applications created in the last 90 days by created_at, prospects left out, counted as applications and not people; a source is the application's source as recorded and a blank one reads "No source recorded"; first interview = <stage>, the first stage after review with Screen, Interview, Onsite or Panel in its name (a pre-screen, assessment or test does not count); final stage = <stage>, the last stage that is neither Offer nor Reference; late stages = the last three on the plan; reached = last known stage at or past that point (a hire reached every stage), or an entry in stage history when it is visible; who ended it comes from the rejection reason's type; a percentage needs 10 or more applications behind it (fewer is noise); fresh = created in the last 14 days (two weeks is rarely enough to reach an interview); a source question needs 5 or more applications, a withdrawal question 3 or more. Sources are ordered by volume and are not ranked. Every threshold is inclusive. Tell me different numbers and I'll redo it.

Hidden tools only: rule 1's footnote naming just those items: source names (harvest:sources:list), reached from stage history (harvest:application_stages:list). Declined: rule 2's sentence.

Next: "/greenhouse:pipeline-review <req>" · "/greenhouse:source-review <another open req, or this req since it opened>" · "/greenhouse:daily-brief"
