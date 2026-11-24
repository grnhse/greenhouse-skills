# Configure: how to answer

This is the first thing a new user sees, so it should feel like being shown to their desk, not handed a manual. Read this before the final answer of a completed run; the stops and questions in steps 2 to 4 stay plain chat. Then pick the first shape that fits:

1. **Page and a short reply.** Your app can show a file or a rendered document (one it renders beside the chat), and the user did not ask for chat only (the builder makes the page; where Python cannot run you write it, as "Without Python" says). Build the page (Build, below) and send the short reply.
2. **Short reply only.** No page is possible, or the user asked for chat.
3. **One part, or the full report, in chat.** Only when the user asks ("what's missing", "note for my admin", "rollout", "how was this judged", "full report"): give that part of "Output, full version" at the end of this file, and all of it only for "full report".

## Short reply

Sound like a colleague who has just looked this up for them: plain words, short sentences, the person's first name once when you know it. No headings, no tables, no tool or rule names, nothing about how you got the answer. Everything in the reply is something they can act on or need to know today; the rest waits on the page or for a question. Keep it under about 120 words, not counting a fenced message.

In this order, which replaces the rules block's "headline, then scope line" for this reply:

1. The first two landing sentences from step 7: who they are matched to, and how many of the seven skills work. End the second one for where the remedy now lives: with a page, "...the one worth asking your Site Admin for is <PICK>; a note you can send them is on the page." (a Site Admin: "...the first scope worth enabling is <PICK>; the rollout table is on the page."); chat only, "...say 'note for my admin' and I'll write it." Nothing missing: step 7's sentence as written. On a re-run, lead with what changed.
2. The story sentence from step 6: the one number worth their attention today, with its req. With a page, add: "Your setup and your open reqs are on the page."
3. The profile line from step 8, exactly as written, on its own line. It is how the other skills know who they are for the rest of the conversation, so it is never left out; the tip and the closing line are, unless asked, with one exception: when you had to ask for their email, or the address Greenhouse holds differs from the one they typed, add the tip as one line with the address to save.
4. The scope line, short: "Counting the open reqs where you're recruiter or coordinator that you can see, as of <Wed 14 Oct, 09:00 EDT>."
5. "Where do you want to start?" and the options the Next section builds, as a short numbered list with their numbers. It replaces the Try line: do not print both. Never use a question tool for it.

The capability table, the scope keys, the note, the thresholds line and the footnote are not in the short reply: they are on the page, and in chat when asked.

## Rolling this out (Site Admins)

For a Site Admin with something missing, in chat when asked and as `rollout` on the page. Keep only the keys missing in this session, and give the link `https://app.greenhouse.io/configure/dev_center/mcp_scope_configuration/edit`.

| Persona | Scope keys | What they get |
|---|---|---|
| Recruiter | harvest:interviews:list, harvest:application_stages:list, harvest:offers:list, harvest:openings:list | today's interviews, exact days in stage, offers in flight, target start dates |
| Recruiter running debriefs | harvest:notes:list, harvest:notes:create, harvest:applications:move, harvest:scorecard_candidate_attributes:list, harvest:ai_opt_out_statuses:list | notes and stage moves recorded after a confirmation, attribute ratings, the opt-out check |
| Interviewer | harvest:interview_kits:list, harvest:scorecards:create, harvest:job_interviews:list, harvest:scorecard_questions:list | draft scorecards filed from here |
| Coordinator | harvest:job_hiring_managers:list, harvest:job_owners:list, harvest:sources:list | hiring team per req and source per candidate |

## Data file

File name: `greenhouse-setup.html`. Send this short form; the builder writes the tiles, titles, columns, links, status chips, fixed notes and the "Copy prompt" on each row from it. Use only these keys, write each value once, and leave a key out when its section was not read (a section that was read and is empty is an empty list).

| Key | What goes in it |
|---|---|
| `skill` | `"configure"` |
| `view`, `asOf`, `headline`, `scope` | "<Name>'s view" or "your view"; date, time and zone; the first landing sentence; "Covering the tools listed in this session and the open reqs where you're recruiter or coordinator that you can see" |
| `matched`, `role` | the matched user's name (never the email) and their role; leave both out without `ME` |
| `counts` | `{reqs, active, decisions, decisionsNote?, quiet}` from step 6; leave out without `ME`. `decisionsNote` is where most of them sit ("2 on Senior Backend Engineer") |
| `focus` | the tile the story sentence is about: `reqs`, `active`, `decisions` or `quiet` |
| `skills` | step 5's seven rows: `{skill, status, try, missing?}` with `skill` the skill's name (`daily-brief`), `status` Ready, Partial or Not yet, `try` the filled prompt, `missing` "For now: ..." or "Ask your Site Admin for ..." (leave out when Ready) |
| `caveat` | one sentence, only when the same caveat applies to every row |
| `allListed` | `true` when nothing is missing |
| `note` | the note for the Site Admin from step 5, whole; only when something is missing and `ADMIN` is false |
| `rollout` | instead of `note` when `ADMIN` is true and something is missing: rows `{persona, keys, gets}`, only the missing keys |
| `reqs` | with `ME`: rows `{req, job, active, decisions, quiet, new}`, busiest first; `job` the job id as a number |
| `notes` | rule 1's footnote when anything is missing |
| `next` | the chooser's options written as prompts ("/greenhouse:daily-brief", "/greenhouse:pipeline-review <busiest req>") |

The profile line and the email address never go on the page. A filled example is in `page/example.json`.

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

This is the Output the skill's steps refer to. In chat, give one part of it when the user asks for that part, and all of it only for "full report".

On a re-run (an earlier configure report is in this conversation), lead with what changed: "New since last time: you can now move candidates from here." then the numbers that moved. Line 1: the step 7 headline. Line 2: "Covering the tools listed in this session and the open reqs where you're recruiter or coordinator that you can see, as of <date and time in the user's time zone; UTC when unknown, and say so>." Then: the capability table (seven rows); the note (`ADMIN` false) or the Rolling this out table with its link (`ADMIN` true), only when anything is missing, else "Every tool the seven data skills use is listed."; the k-of-7 sentence, the story and the Try line; "How this was judged: Ready means every core tool is listed, Partial only enhancements or the user lookup missing, Not yet another core tool missing; quiet is 14 or more days with no activity recorded, because two working weeks without a touch is when candidates start accepting other interviews; new is the last 24 hours; busiest is most active applications. Thresholds are inclusive. Tell me different numbers and I'll redo it."; rule 1's footnote when anything is missing, naming the sibling sections the hidden tools feed; the profile line and tip; Next: the chooser from step 7, whose options are the Next prompts.
