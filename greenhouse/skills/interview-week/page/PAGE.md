# Interview week: how to answer

Read this before answering. Finish the skill's steps, then pick the first shape that fits:

1. **Page and a short reply.** Your app can show a file or a rendered document (one it renders beside the chat), and the user did not ask for chat only (the builder makes the page; where Python cannot run you write it, as "Without Python" says). Build the page (Build, below) and send the short reply. A second run in the same conversation builds a new page and opens the reply with what moved.
2. **Short reply only.** No page is possible, or the user asked for chat ("in chat", "no page", "I'm on my phone"). Stay in chat for the rest of the conversation unless they ask for the page.
3. **One section, or the full schedule, in chat.** Only when the user asks ("show me Friday", "what's still to schedule", "who owes feedback", "who's interviewing tomorrow", "full schedule", "how was this read?"): give that section of "Output, full version" at the end of this file, and all of it only for "full schedule".

## Short reply

Sound like a colleague who has just looked this up for them: plain words, short sentences, the person's first name once when you know it. No headings, no tables, no tool or rule names, nothing about how you got the answer. Everything in the reply is something they can act on or need to know today; the rest waits on the page or for a question. Keep it under about 120 words, not counting a fenced message.

In this order, which replaces the rules block's "headline, then scope line" for this reply:

1. A greeting with their first name when you know it, by their local time ("Morning, Priya." before noon, "Afternoon, Priya." after; no name and no zone: skip it), then the headline sentence.
2. Up to three bullets, soonest first: what is on today, or on the first day that has interviews ("Yusuf Demir, Hiring Manager Interview with Renata Aguilar, 13:00"), each with the candidate linked, the req and the time; then one bullet for a panel that needs a change (someone declined, or nobody is on it), when there is one. An empty week: no bullets; after the headline, one warm, plain sentence with who has waited longest and what is owed, not a second headline ("Nothing is on the calendar for the next 7 days. Four candidates are waiting for an interview to be scheduled, Oluwaseun Park longest at 16 days, and 5 scorecards are still owed.").
3. One line for what else there is, counts only, leaving out zeros and anything the headline already said: "Also: 4 candidates still to schedule, 5 scorecards owed by 4 interviewers, 2 panel replies missing."
4. Where the rest is. With a page: "The whole week is on the page; filter it by day or by req, and the reminders are there to copy." (no reminders clause when no feedback is owed) Chat only: "Ask for a day, what's still to schedule, or who owes feedback."
5. The reminders offer as one short question, only when feedback is owed and no page was built: "Want the reminders for the 4 interviewers?"
6. One sentence, only if something was hidden or declined: what you could not see, in their words, and the one thing that would fix it ("I couldn't see who is on each panel with your current access; /greenhouse:configure shows what to turn on."; for a declined call, that it is a Greenhouse permission and an admin can change it). The exact footnote goes on the page. An empty list is not a gap: leave it out.
7. The scope line, short: "Across your <N> open reqs, <Thu 15 to Wed 21 Oct>, counting what you can see in Greenhouse, as of <Thu 15 Oct, 09:00 EDT>." When the reqs were named by the user, say "the <N> reqs you named" or the req's name.
8. Next: two prompts as text, real names filled in. Never end with a question tool: a pending question can leave the conversation looking stuck.

The "how this was read" line, the long footnotes and the per-section lead lines are not in the short reply: they are on the page in `judged`, `notes` and each panel's `note`, and in chat when asked. Sending a nudge stays in the conversation, as step 9 says. Nothing in the reply or on the page describes a candidate or an interviewer beyond where and when: no ratings, no scorecard text, no comment on anyone's pace.

## Data file

File name: `greenhouse-interviews-<yyyy-mm-dd of the window's first day>.html`. Send this short form; the builder writes the tiles, titles, columns, links, status chips, fixed notes and the "Copy prompt" on each row from it. Use only these keys, write each value once, and leave a key out when its section was not read (a section that was read and is empty is an empty list).

| Key | What goes in it |
|---|---|
| `skill` | `"interview-week"` |
| `view`, `asOf`, `headline`, `scope` | "<Name>'s view" or "your view"; date, time and zone; the headline sentence; the scope line without "as of" (it must contain "that you can see") |
| `window`, `windowWords`, `zone` | "15 to 21 Oct" (one day: "Fri 16 Oct"); the window in words for the tile ("next 7 days", "tomorrow"); the time zone's short name |
| `read` | only when the window is not the default: "the week you named", "tomorrow" |
| `focus` | the tile the headline is about: `interviews`, `schedule`, `feedback` or `replies` |
| `counts` | `{today, tomorrow, declined?, notReplied?}`; the two reply counts only when `list_interviewers` was read |
| `job` | for one named req only: `{req, id}` (requisition id, job id as a number) |
| `week` | rows `{day, time, name, cand, app, req, interview, stage?, panel?, replies?, status, detail?}`: `day` "Fri 16 Oct", `time` "10:00–11:00" or "All day", `cand` and `app` ids as numbers, `panel` the names, `replies` the reply counts, `status` one of Scheduled, Panel change needed, Application closed, Scorecard due, Feedback in, Skipped, Test sent, Test received, `detail` a small object (Length, Replies, Coordinator, Organizer) |
| `toSchedule` | rows `{name, cand, app, req, interview, sub?, days, availability?, detail?}`: `sub` "<stage> · <n> interviews" when more than one, `availability: true` when availability is in |
| `toScheduleTotal` | only when the list was capped at 25 |
| `passedCaveat` | `true` when interview names were not visible |
| `feedback` | one row per interviewer, oldest interview first: `{who, cards}` with `cards` `[{name, req, interview, on, state, hours}]`, `state` "started, not submitted" or "not started". The builder writes the reminder. The user's own row: `who` "You"; interviewers not visible: leave `who` out |
| `defaultTools` | `true` when `list_interviews` was not listed (the section is then "Scorecards started but not submitted") |
| `notes` | what the chat answer would print under its tables: rule 1's footnote, rule 2 and rule 3 sentences, a req with nothing on the calendar |
| `next` | the Next prompts, one string each |

A private candidate: `"private": true` in place of `name`. Nothing on the page describes a candidate or an interviewer beyond where and when. A filled example is in `page/example.json`.

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

This is the Output the skill's steps refer to. In chat, give one section of it when the user asks for that section, and all of it only for "full schedule".

```
<headline from the step 7 ladder>
Across your <N> open reqs as recruiter or coordinator ("the <N> reqs you named" or the req's name when run from names), interviews from <Thu 15 Oct> to <Wed 21 Oct> that you can see, times in <EDT> · as of <Thu 15 Oct, 09:00 EDT>.

### This week (<N> interviews)   (the window in words when it is not the default: "Tomorrow", "Next week")
**<Thu 15 Oct>**
| Time | Candidate | Req | Interview | Panel | Status |
| 13:00–13:45 | [Name](https://app.greenhouse.io/people/<candidate_id>?application_id=<application_id>) | <req> | Hiring Manager Interview (<stage>) | <Interviewer>, <Interviewer> · 1 not replied | Scheduled |
| All day | [Name](...) | <req> | Take-Home Test | panel: not visible | Test sent |
**<Fri 16 Oct>**
...
Rooms and video links are on each interview in Greenhouse.
Empty: "No interviews are on the calendar <window> that you can see."

### Still to schedule (<n> candidates)
Greenhouse marks these interviews as to be scheduled in the candidate's current stage; days count from when the slot opened.   (without interview names: "This may include interviews from stages already passed.")
| Candidate | Req | Interview | Days waiting | Availability | Coordinator |
| [Name](...) | <req> | Technical Interview | 16 | none recorded | <name> |
| [Name](...) | <req> | Onsite: Values Interview, System Design (2 interviews) | 9 | in since 13 Oct | <name> |
Empty: "Nothing is waiting to be scheduled."

### Awaiting feedback (<F> scorecards, <I> interviewers, last 30 days)   ("Scorecards started but not submitted" on default tools)
Interviewers who haven't opened their scorecard show up only with interview access (harvest:interviews:list).   (default tools only)
**<Interviewer name>** (2)
| Candidate | Req | Interview | Interviewed | Scorecard | Hours since the interview |
| [Name](...) | <req> | System Design | Thu 8 Oct | started, not submitted | 166 |
Reminder to copy (nothing is sent from Greenhouse):
Hi <first>, Greenhouse is still waiting on your scorecard for <candidate> (<req>, <interview>, <Thu 8 Oct>).
The team needs it to decide; if the interview moved or you weren't on it, let me know. Thanks, <user first name>
Empty: "No feedback is owed from the last 30 days that you can see."

### By interviewer   (only when asked: "who's interviewing tomorrow")
- <Interviewer name>: <Fri 16 Oct, 10:00> <candidate> (<req>, <interview>) · <Tue 20 Oct, 14:00> <candidate> (<req>, <interview>)
A count here is that person's calendar for the window and nothing else.

How this was read: the window is <7 days from today | the day or week you named>, in <zone>; an interview counts when Greenhouse has a start time for it in the window, and all-day events such as take-home tests are listed as "All day"; still to schedule = interviews Greenhouse marks as to be scheduled in the candidate's current stage on an active application, with days counted from when the slot opened; awaiting feedback = interviews in the last 30 days that Greenhouse marks as awaiting feedback, one line per interviewer whose scorecard is not submitted, with hours counted from the interview's end; a panel needs a change when someone declined or nobody is on it. Nothing here rates anyone: counts describe calendars. Tell me different numbers and I'll redo it.
Not visible with your Greenhouse MCP access: <sections> (needs <scope keys>). <the rest of rule 1's footnote, verbatim>
Next: /greenhouse:candidate-status <name> · /greenhouse:pipeline-review <req> · /greenhouse:daily-brief
```

An empty section is one plain sentence; never estimate a count, and never list an interview that Greenhouse does not have on the calendar.
