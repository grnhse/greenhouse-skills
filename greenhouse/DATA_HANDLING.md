# Data handling

How the Greenhouse plugin treats data. The plugin is nine markdown skills, a pointer to the hosted Greenhouse MCP server, and in seven of the skills a `page/` folder: instructions, a fixed HTML template (`page.html`), one small Python script that fills it (`build_page.py`, the same in every folder) and a fictional example. It holds no credentials.

## 1. What data does it access?

Candidate and user records from your Greenhouse organization, read through the Greenhouse MCP connector with your own OAuth sign-in. That includes candidate names, contact details, application history, stages, scorecards and their notes, interviews, offers, openings, sources, notes and user records, each only when the matching scope is enabled and only as far as your Greenhouse permissions allow. Greenhouse applies those permissions on every call; the plugin cannot see anything you could not see in Greenhouse yourself.

The skills are written not to read:

- Resume or attachment content. The connector exposes only metadata and a short-lived link, and the skills are written not to open the link.
- EEOC or demographic data at any level, and the skills are written not to infer protected traits or their proxies.
- Your assistant's memory, chat history or your uploaded files. The skills use only what Greenhouse returns and what you tell the assistant in the conversation or in the instructions you give it.

AI output can be wrong, so review anything before you act on it.

## 2. What does it store?

No memories, schedules or caches. The one thing it leaves is a page: a file, or a rendered document where your app supports them.

- **When.** Setup, the daily brief, the interview week, the pipeline review and the source review are shown as a page when your app can show a file or a rendered document; the debrief and candidate status build one when you ask. Say "in chat" and no page is made.
- **How.** The assistant hands the figures already retrieved in the conversation to the bundled `build_page.py` on standard input, in one shell call, and the script writes the page; no data file is written and nothing else is saved (the skills are written never to use your project). The script uses only the Python standard library, makes no network request and runs nothing from the data; it checks the data and places it in the fixed template. If Python cannot run, or the build still fails after two fixes, the assistant writes a plain still page itself from the fixed frame in the skill's page instructions: no script, no font or other outside resource, links only to Greenhouse, and the same rule against contact details and amounts of money; the script's checks do not run on that page, so the skills' own rules are the only guard. If your app can show neither a file nor a rendered document, the answer arrives in chat.
- **Where.** An HTML file named `greenhouse-<topic>-<req, candidate or date>.html` (`greenhouse-setup.html`, `greenhouse-daily-brief-2026-10-16.html`; a debrief or status page carries the candidate's name), or a rendered document where your app supports them, in the folder where your app keeps files it shows you; in a command-line client, the skills are written to use the session's scratch or temporary directory, not your project. It stays until you delete it, or until that temporary directory is cleared.
- **What it holds.** Candidate and interviewer names, req and stage names, dates, counts and links to Greenhouse, plus the reminders and the hiring-manager message to copy; a debrief page also holds each interviewer's overall rating and quoted key takeaways, and a pipeline-review page rating tallies as words. The script refuses common formats of email addresses, phone numbers and amounts of money, and any link that does not point to `app.greenhouse.io`; when it finds one it rejects the whole data set, and the assistant fixes the data and tries again, twice at most. A detail written in an unusual format could get past the script, which is why the skills are also written to keep contact details and compensation off every page.
- **Who sees it.** You. It is private until you share it. Share it only with people who can see the same records in Greenhouse. A debrief page is for the hiring team only, never a candidate, and its footer says so; it is not built for a candidate who opted out of AI review or while your own scorecard on that application is still a draft. The skills are written not to show an interviewer other interviewers' ratings before they submit, so share a debrief or pipeline-review page only with people who have submitted their own scorecard.

`configure` prints a profile line and, only on a connection without the `whoami` tool, suggests you add your Greenhouse email to the standing instructions you give your assistant; that is your choice and your assistant account, not the plugin. With `whoami` the skills recognize the signed-in user and nobody is asked for an email. When you ask for any other chart, page, document or spreadsheet, your app creates it at your request and keeps it where that app keeps such things (the conversation, or a folder you chose). Greenhouse data the skills read becomes part of your conversation with the assistant, which is processed and retained under your assistant plan and organization settings; Greenhouse receives the tool calls, not the conversation.

## 3. Where does it send data?

To Greenhouse, over the connector you authorized. The plugin has no endpoint of its own. Two other requests can happen:

- **Fonts.** When you open a page the bundled script built, or any page or rendered document the `brand` skill styles, your browser asks Google Fonts (`fonts.googleapis.com`, which serves the files from `fonts.gstatic.com`) for two typefaces. The request carries no Greenhouse data; Google receives it as it would from any website using its fonts, with your IP address and browser details, under [Google's privacy policy](https://policies.google.com/privacy). If it is blocked, the page uses system fonts. The page's own script makes no other request. A page the assistant wrote by hand, when Python could not run, loads no font and makes no request at all.
- **Messages you approve.** Only if you have connected a chat or email tool to your assistant yourself. `daily-brief` and `interview-week` can send an interviewer a scorecard nudge, and `pipeline-review` can send its hiring-manager message. The skills are written so that each shows you the one recipient and the whole message and sends it only after your explicit "yes", one message per "yes". An interviewer's address is read from Greenhouse only when sending and is not printed. Nudges and hiring-manager messages are addressed to one named person, never to a channel, a group or a candidate. Asked to post somewhere shared, `daily-brief` and `interview-week` can send a snapshot of counts only (the daily brief: counts with no names, confidential reqs counted rather than named; the interview week: counts and times with no candidate names) to the destination you name, after showing you the exact text and destination, one send per explicit "yes". Messages are written to carry names, stages, dates, counts and Greenhouse links, and to leave out ratings, scorecard text, private notes, contact details and compensation. They are sent from your account in that tool, under its terms.

## 4. How long is data retained?

The plugin keeps nothing of its own except the page, which stays in your app's outputs folder, or among its rendered documents, until you delete it; no other file is written. Data lives in Greenhouse under your organization's retention settings, in the conversation under your assistant plan's retention, and in any chat or email tool you sent a message through under that tool's retention.

## Writes to Greenhouse

Three, all opt-in per record:

| Write | Skill | Gate |
|---|---|---|
| Candidate note | `candidate-debrief` | Preview of the exact text, its visibility, that nobody is notified and how to undo it (delete it on the profile); your explicit "yes" |
| Stage move | `candidate-debrief` | Preview naming the candidate, job, from and to stage, and that Greenhouse may run the destination stage's rules, which can email the candidate or the team and send forms, tests or scheduling requests, and how to undo it (move back, with its own card); your explicit "yes" |
| Draft scorecard in your name | `scorecard-draft` | Preview of kit, rating and notes; your explicit "yes"; created as a draft you submit in Greenhouse |

After each write the skill reads the record back and links it. These gates are part of the skills; if you ask your assistant to write to Greenhouse in a conversation where no skill is running, the only check is your client's own tool-approval prompt. The skills are written never to reject, hire, un-reject, merge, anonymize, bulk-edit or email a candidate, and never to move a candidate to another stage unless you state that decision; the Greenhouse MCP server exposes no delete tools. MCP activity, including these writes, appears in the Greenhouse audit log under your user (events tagged `mcp_access`). Messages sent through your own chat or email tool (section 3) change nothing in Greenhouse.

## Audience

For Greenhouse users acting in their work capacity. Not for anyone under 18, and not for use on data about minors beyond what your organization already lawfully holds in Greenhouse.

## Your controls

- What the assistant can see: the data categories you tick at consent, within the ceiling your Site Admin sets under Configure > Dev Center > MCP Access.
- Stopping access: disconnect Greenhouse in your app's plugin or connector settings (or the MCP command, often `/mcp`, in a command-line client), or disconnect the tool under **My Info > Greenhouse MCP Connections** in Greenhouse. A Site Admin can invalidate every MCP connection in the organization by changing the scopes on the MCP Access page.
- Pages and messages: say "in chat" and no page is made; delete a page file whenever you like; the skills send a message only on your "yes" to that exact message, and you can disconnect the chat or email tool at any time.
- Candidate AI opt-out: when `list_ai_opt_out_statuses` is enabled (scope harvest:ai_opt_out_statuses:list, which also needs Talent Matching), the debrief checks it before reading any scorecard and is written not to summarize interview feedback for a candidate who opted out, and the pipeline review withholds feedback counts and tallies for opted-out candidates on its roster. A decision you state yourself can still be recorded. When the tool is not enabled or the call is declined, both say the status could not be checked; no row means no decision is recorded, never consent.

The Greenhouse MCP server itself is described in the [Greenhouse MCP security FAQ](https://support.greenhouse.io/hc/en-us/articles/53944054829083-Greenhouse-MCP-security-FAQ). The [Greenhouse AI Addendum](https://www.greenhouse.com/ai-addendum) and Greenhouse's [legal terms](https://www.greenhouse.com/legal) apply.
