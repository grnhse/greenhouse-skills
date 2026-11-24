# Greenhouse plugin

Recruiter workflows on your own Greenhouse data, in any AI assistant that supports plugins and MCP connectors: a desktop or web app or a command-line client. The plugin bundles the Greenhouse MCP connector (`https://mcp.greenhouse.io/mcp`) and nine skills: a daily brief of what needs you, the week's interviews, candidate status, evidence-based debriefs, pipeline reviews, a review of where applications come from, draft scorecards, a `configure` entrypoint that checks your access and tells you what works, and a `brand` skill that gives any chart, diagram, page or document you ask for the Greenhouse look.

- Greenhouse MCP is in **open beta** on Greenhouse Recruiting Core, Plus and Pro.
- Every read respects your own Greenhouse permissions. The skills' only writes to Greenhouse are a candidate note, a stage move and a draft scorecard; the skills are written to show you each one first and make it only after you reply "yes". Outside Greenhouse, a skill is written to send a message (an interviewer nudge, a hiring-manager message) only through a chat or email tool you connected yourself, to one named person per "yes"; asked to post somewhere shared, the daily brief and the interview week send only a counts-only snapshot with no candidate names, again on one explicit yes.
- Five skills show their answer as a page and two more build one when you ask; a small bundled Python script builds it where your app can run one, and a plain still page is written where it cannot. See [What the plugin runs, sends and fetches](#what-the-plugin-runs-sends-and-fetches).

## Skills

| Skill | Try | What it shows | Page | What it writes |
|---|---|---|---|---|
| `configure` | "Set me up with Greenhouse" or `/greenhouse:configure` | Connection check, your Greenhouse user and open reqs, which skills your MCP access unlocks, the scopes a Site Admin would need to add, and a place to start | Opens one by default | Nothing |
| `daily-brief` | "What needs me today?" | A headline for the day, then across every req you own: decisions waiting, scorecards started but not submitted, quiet candidates, new applicants since the last working day, a pipeline snapshot with a status word and the review backlog per req; interviews, offers with their start dates, and the hiring manager per req when those scopes are enabled | Opens one by default | Nothing in Greenhouse. Reminder nudges to interviewers through your connected chat or email tool, one per "yes" |
| `candidate-status` | "Where is [candidate]?" or "Have we talked to [candidate] before?" | One sentence that answers the question, then every application for one person: job, stage k of n, outcome and recorded reason, days since recorded activity, scorecards in and owed, what is next and whom to ask; next interview, offer state and last logged email when enabled | When you ask, on a full status | Nothing |
| `candidate-debrief` | "Pull the debrief for [candidate] on [job]" | Whether the panel's input is in, each interviewer's rating and quoted takeaways as given, where they disagree and agree, questions for the room, current and next stage. No recommendation: you decide | When you ask; never for an opted-out candidate or while your own scorecard is still a draft | A candidate note and/or a stage move, each on its own card (what changes, who is notified, how to undo it), only after you state a decision and reply "yes" |
| `pipeline-review` | "How is [job] doing?" or "Prep my sync with the hiring manager on [job]" | One req's status and risks with their numbers, funnel with how far people got, bottleneck, late-stage roster with scorecard tallies, who ended the rejections in the last 30 days, questions for the sync, and a hiring-manager message under 120 words that is safe to share | Opens one by default | Nothing in Greenhouse. The hiring-manager message to one person through your connected chat or email tool, only after you reply "yes" |
| `interview-week` | "What interviews do I have this week?" or "What still needs scheduling?" | The next 7 days of interviews by day and time with candidate, req, interview and status, who is on each panel, what is still waiting to be scheduled, and interviews from the last 30 days still waiting on feedback with a nudge per interviewer. No ratings, no scorecard text. Without `harvest:interviews:list` it shows only scorecards started and not submitted in the last 30 days and names the scope in a footnote | Opens one by default | Nothing in Greenhouse; it schedules nothing. A nudge to one interviewer through your connected chat or email tool, only after you reply "yes"; otherwise you copy it |
| `source-review` | "Where are our applicants coming from?" or "Which sources are working for [job]?" | For one req or all of yours, over a stated window (90 days by default): applications per source, how many are active, reached the first interview and the final stage, were hired or ended and who ended it, referrals as their own line, sources with nobody past review, and questions for a sourcing sync. Counts of sources, never a comparison of people. Without `harvest:sources:list` it still counts applications and referrals but cannot name sources, and says so | Opens one by default | Nothing |
| `scorecard-draft` | "Draft my scorecard for [candidate] from these notes: ..." | Your own interview notes turned into a scorecard for the right interview kit | No | A **draft** scorecard in your name, only after you reply "yes"; you submit it in Greenhouse. Without the scorecard scopes it gives you paste-ready text instead |
| `brand` | "Chart this funnel", "Turn this review into a page", "Put this brief in a deck" | Greenhouse's colours, type and chart rules applied to the tables, SVG diagrams, charts, pages, documents, decks and spreadsheets you ask for; the skills above build their own pages in the same style | No | Nothing; it reads nothing from Greenhouse |

`configure` hands off to the other skills, `candidate-status` offers the debrief, and `daily-brief` offers a review of any req it lists. A page opens where your app can show a file or a rendered document; say "in chat" to skip it.

### How every answer is shaped

- The headline answers the question with its biggest number; a scope line says what was counted ("that you can see") and when.
- Answers are short: a sentence that answers the question, up to three things that need you, and where the rest is. Ask for any one table, the full review, or "how was this judged?" and you get it.
- Every threshold is stated with its reason and ends "Tell me different numbers and I'll redo it."; the skills that build a page keep that line on the page and give it in chat when asked.
- Anything your MCP access hides ends up in one footnote naming the scope keys, never in a guess; beside a page the chat reply says it in plain words and the exact footnote is on the page.
- Each answer ends with two or three prompts filled with the real names and reqs from your data, so the next step is one tap or one paste away.
- Setup, the daily brief, the interview week, the pipeline review and the source review open as a page when your app can show a file or a rendered document: interactive where it can run code (filter by req or stage, sort, open a row, copy the hiring-manager message, a nudge or a next prompt), a simpler still page where it cannot. The chat reply beside it stays short: the headline, up to three bullets or sentences on what needs you, where the rest is, a short scope line and Next, plus a few lines particular to each skill (the daily brief and the interview week add an "Also:" counts line; the pipeline review adds its status word and, when you asked for a sync or a message or have a chat or email tool connected, the hiring-manager message; the source review adds how far applications got and one question to raise; setup gives the profile line and a numbered list of where to start); the threshold line and the exact access footnote live on the page and come to chat when asked. Say "in chat" to skip the page. The debrief and candidate status answer in chat and build a page when you ask.
- Any other chart, diagram, document or deck is made only when you ask, and the `brand` skill styles it with Greenhouse's visual guidelines.
- Rendered examples on a fictional organization: [docs/samples](https://github.com/grnhse/greenhouse-skills/tree/main/docs/samples).

## Quick start

### Desktop or web app

1. Open **Customize > Plugins** and install Greenhouse from **Discover** if it is listed there, or choose **Add > Add marketplace** and enter `grnhse/greenhouse-skills`.
2. Open the plugin's **Connectors** tab and connect Greenhouse. Sign in with the email you use for Greenhouse and leave the data categories you need ticked.
3. Say "set me up with Greenhouse" or run `/greenhouse:configure` (type `/` in the message box and pick it).

On a team or enterprise plan your workspace owner may need to add the Greenhouse connector first. Admin steps are in [SETUP.md](SETUP.md).

### Command-line client

In a command-line client that supports plugin marketplaces, run the four lines below. If you installed the plugin in the desktop or web app and the client syncs plugins from the same account, it appears as a synced plugin at your next session start: skip the two `/plugin` lines, run `/mcp`, choose the Greenhouse server under that plugin, and sign in. Install from the marketplace only where the client does not sync plugins from your account; a client loads one plugin per name.

```
/plugin marketplace add grnhse/greenhouse-skills
/plugin install greenhouse@greenhouse-skills
/mcp                      (choose plugin:greenhouse:greenhouse and sign in)
/greenhouse:configure
```

## Prerequisites and common blockers

| You need | Otherwise |
|---|---|
| Greenhouse Recruiting Core, Plus or Pro with Greenhouse MCP enabled for your organization (open beta; Greenhouse enables it, so contact your account team) | Greenhouse sends the connection attempt back to the app with `Public OAuth clients are not enabled for this organization` |
| If you are not a Site Admin: non-admin MCP authorization, which your Greenhouse account team enables (a Site Admin cannot) | The connection fails with `Only organization administrators can authorize MCP applications.` |
| Your own Greenhouse permissions for the data you ask about | Skills show only what you can see in Greenhouse; empty sections name the likely cause instead of guessing |

### What the default scopes unlock

An organization that has never changed **Configure > Dev Center > MCP Access** exposes seven read-only scopes. With those, `daily-brief`, `candidate-status` and `pipeline-review` run with their core sections (interviews, offers, exact days in stage and the hiring team need the scopes below), `candidate-debrief` produces the complete brief but cannot record a note or move a stage, `scorecard-draft` prints paste-ready text instead of creating a draft, `interview-week` shows only scorecards started and not submitted (the calendar, what still needs scheduling and interviews awaiting feedback need `harvest:interviews:list`), and `source-review` counts applications and referrals without naming their sources (names need `harvest:sources:list`); each names the missing scope in a footnote. `configure` names exactly which of the scopes below are missing in your session and rates every data skill Ready or Partial on these defaults. `brand` needs no Greenhouse tool.

| Scope a Site Admin can add | What it unlocks |
|---|---|
| `harvest:interviews:list` | The interview calendar, what still needs scheduling and interviews waiting on feedback in `interview-week`; today's and tomorrow's interviews and feedback owed in the daily brief; the next interview per candidate; interviews still to come and awaiting feedback in debriefs; interviews in the next 7 days in pipeline reviews |
| `harvest:interviewers:list` | Who is on each interview panel, and who has not started a scorecard (`interview-week`) |
| `harvest:application_stages:list` | Exact days in stage, stage-by-stage pass-through, and how far each source's applications got in `source-review` from stage history (otherwise skills use days since last activity or where each application stands, and say so) |
| `harvest:offers:list` (plus your private and salary data permission) | Offers in flight and offer state |
| `harvest:openings:list` | Open seats and target start dates in pipeline reviews |
| `harvest:notes:list` | Recruiter notes and the last logged email |
| `harvest:notes:create` | `candidate-debrief` can record a decision note after you confirm |
| `harvest:applications:move` | `candidate-debrief` can move a stage after you confirm |
| `harvest:job_hiring_managers:list` | The hiring manager per req in the daily brief and the addressee of the pipeline review's hiring-manager message |
| `harvest:job_owners:list` | Read by no skill yet; `configure` only reports whether it is enabled |
| `harvest:scorecard_candidate_attributes:list` | Attribute-level ratings in debriefs |
| `harvest:ai_opt_out_statuses:list` (plus Talent Matching) | The debrief and the pipeline review check a candidate's AI opt-out status before summarizing them |
| `harvest:sources:list` | Source names and types in the source review (without it the review counts applications and referrals without naming sources); source names on the pipeline review's roster |
| `harvest:interview_kits:list`, `harvest:scorecards:create` | `scorecard-draft` can create a draft scorecard after you confirm |
| `harvest:job_interviews:list`, `harvest:scorecard_questions:list` | Interview names and planned length in `interview-week`; `scorecard-draft` names each interview and structures your notes under the kit's questions |

Saving a changed scope set on the MCP Access page signs every MCP connection in the organization out, for every AI tool. Each person reconnects once, and the new tool list can take up to 10 minutes to appear in a conversation. Full admin steps: [SETUP.md](SETUP.md).

## What the skills are designed not to do

The skills are written to stay inside these limits. AI output can be wrong, so review anything before you act on it.

- Reject, hire, un-reject, merge, anonymize or bulk-edit anyone, or move a candidate to another stage unless you state that decision. No hire or no-hire recommendation, no "fit" language.
- Email a candidate. A stage move runs the rules your organization configured on the destination stage, which can email the candidate or the team and send forms, tests or scheduling requests; the preview says so before you confirm.
- Read resume or attachment content, or open an attachment link.
- Call EEOC or demographic tools, or infer protected traits or their proxies.
- Show an interviewer other interviewers' ratings before they submit.
- Put contact details, compensation, private notes or scorecard text into anything meant for a shared channel or group (they link to the Greenhouse profile instead), or put candidate names into a shared snapshot, which carries counts only.
- Send a message without showing you the recipient (or the shared destination) and the whole text first and getting your "yes", send more than one message per "yes", send a nudge or the hiring-manager message to a channel or group, or message a candidate.
- Widen an empty "my reqs" result to the whole organization, invent records, or create schedules or memories on their own. The one file they make unasked is the page for setup, a daily brief, an interview week, a pipeline review or a source review, saved in your app's outputs folder (or shown as a rendered document), outside your project folders; any other chart, page or document exists only when you ask for one.

## What the plugin runs, sends and fetches

- **Runs.** One Python 3 script, `build_page.py`, in the `page/` folder of each of the seven skills that can build a page (the copies are identical). It uses only the standard library, makes no network request and runs nothing from its input. To build a page, the assistant passes the figures already shown in the conversation to the script on standard input in one shell call and names the output file; no data file is written or deleted, and the page is the only file (a `--data` file is an option the skills do not use). The script checks the data, accepts links only on `https://app.greenhouse.io/`, refuses the whole data set when it finds a common format of an email address, a phone number or an amount of money (the assistant fixes the data and runs it again, twice at most), fills the fixed template `page.html` and writes the page. If Python cannot run, or the build still fails after two fixes, the assistant writes a plain still page itself from the frame in `PAGE.md`: no script, no font or other outside resource, links only to `app.greenhouse.io`, at most 10 rows per table; the script's checks do not run on it, so the skill's own rules are the only guard. If the app can show neither a file nor a rendered document, the answer arrives in chat ("I couldn't open a page here, so it's all in chat"). In a command-line client the build is a shell command, so the client asks your permission first unless you have already allowed it.
- **Keeps.** The page is an HTML file named `greenhouse-<topic>-<req, candidate or date>.html` (for example `greenhouse-daily-brief-2026-10-16.html` or `greenhouse-setup.html`), or a rendered document where your app supports them, in the folder where your app keeps files it shows you (in a command-line client, the skills are written to use the session's scratch or temporary folder, not your project). It stays until you delete it. It holds candidate and interviewer names, stages, dates and counts, on a debrief page each interviewer's rating and quoted takeaways, and on a pipeline-review page rating tallies as words. It is private to you: share it only with people who can see the same records in Greenhouse; a debrief page is for the hiring team only, never a candidate, only with people who have submitted their own scorecard, and is not built while yours is still a draft; a pipeline-review page only with people who have submitted their own scorecard.
- **Fetches.** Greenhouse data, only through the connector. When you open a page the bundled script built, or any page or rendered document the `brand` skill styles, your browser asks Google Fonts (`fonts.googleapis.com`, which serves the files from `fonts.gstatic.com`) for two typefaces; the request carries no Greenhouse data and falls under [Google's privacy policy](https://policies.google.com/privacy), and the page uses system fonts when it is blocked. The hand-written still page loads no font or other outside resource. The page's own script makes no other request and stores nothing; its copy buttons write to your clipboard. When Greenhouse is not connected in a desktop or web app, `configure` looks up the Greenhouse connector in the app's connector directory to offer a Connect button.
- **Sends.** Nothing, unless you have connected a chat or email tool to your assistant yourself. Then a skill can send an interviewer nudge (`daily-brief`, `interview-week`) or the hiring-manager message (`pipeline-review`) to one named person after showing you the recipient and the whole text, one message per "yes", never to a channel or group. Asked to post somewhere shared, `daily-brief` and `interview-week` can send a counts-only snapshot with no candidate names (the interview week may include interview times; the daily brief counts confidential reqs without naming them) to the destination shown, after showing you the exact text, one send per explicit yes. Nudges carry no ratings, notes or contact details, and the hiring-manager message carries no ratings, scorecard text, contact details or compensation.

## Data handling

The plugin reads candidate and user data only through the Greenhouse connector and only what the signed-in user can see. It keeps no memories, schedules or caches; the only file it leaves is the page described above. The skills are written to send data to another connector only after you confirm a specific message. The skills' writes to Greenhouse are limited to a candidate note, a stage move and a draft scorecard, which the skills are written to make only after your explicit confirmation, and they appear in the Greenhouse audit log under your user. Details: [DATA_HANDLING.md](DATA_HANDLING.md).

## Known limits

- Harvest V3 exposes no "who am I" endpoint, but the connector's `whoami` tool returns the signed-in user, so when it is listed the skills recognise you and nobody is asked for an email. On a connection without it, `configure` asks for your Greenhouse login email once per conversation; if you add it to the standing instructions you give your assistant, the skills use what you have told it instead of asking. The plugin itself keeps no profile of you and reads nothing from your assistant's memory or history.
- Without `harvest:application_stages:list`, aging means "no activity recorded for N days" on the candidate (Greenhouse copies the latest activity to every application they hold), not days in stage, and pass-through is rebuilt from where each application ended. Skills label the difference.
- Offers come back empty both when there are none and when you lack the private and salary data permission; skills say so rather than pick one.
- Accounts with limited permissions may not be able to look users up. With `whoami` the skills still scope to your reqs; without it, when the email lookup finds nobody or is declined, "my reqs" scoping is skipped and you name a req instead.
- Greenhouse rate-limits requests; the limit is shared with your organization's other custom Harvest integrations. Skills batch reads and cap pages; on a 429 they deliver what they have and ask you to re-run in a minute.
- A single-req review covers the first 1,000 applications Greenhouse returns; the daily brief covers up to 50 reqs and the first 1,500 active applications, and asks you to narrow beyond that.
- The preview-and-confirm gate on writes lives in the skills. A request that no skill picks up goes to the Greenhouse tools directly, with only your client's tool-approval prompt in between, so phrase decisions as "debrief", "log a note" or "move to <stage>".
- A page is a snapshot as of the time printed on it: it does not refresh and it cannot change anything in Greenhouse. Pages need an app that can show a file or a rendered document: interactive where it can run Python, a simpler still page where it cannot; where it can show neither, the same answer arrives in chat. There are no live dashboards or scheduled exports.
- Two Greenhouse connectors can appear in one account: this plugin's at `mcp.greenhouse.io` and another connector entry for the same server at `mcp.us.greenhouse.io`. Keep one connected to avoid duplicate tools.

## Support

- Greenhouse Support: <https://support.greenhouse.io>
- [Greenhouse MCP overview](https://support.greenhouse.io/hc/en-us/articles/52090956642075-Greenhouse-MCP)
- [Set up Greenhouse MCP with supported AI tools](https://support.greenhouse.io/hc/en-us/articles/52096319906971-Set-up-Greenhouse-MCP-with-supported-AI-tools)
- [Greenhouse MCP use cases by role](https://support.greenhouse.io/hc/en-us/articles/52193605120155-Greenhouse-MCP-use-cases-by-role)
- [Greenhouse MCP security FAQ](https://support.greenhouse.io/hc/en-us/articles/53944054829083-Greenhouse-MCP-security-FAQ)
- Security issues: report them privately through Greenhouse's bug bounty program on HackerOne (<https://hackerone.com/greenhouse>), linked from <https://www.greenhouse.com/security>; see [SECURITY.md](https://github.com/grnhse/greenhouse-skills/blob/main/SECURITY.md).

Greenhouse MCP is currently in open beta. Access depends on your subscription tier and admin configuration; contact your account team to learn about access and pricing. Use of the connector and this plugin is subject to the [Greenhouse legal terms](https://www.greenhouse.com/legal) and the [Greenhouse AI Addendum](https://www.greenhouse.com/ai-addendum). The skills are proprietary, for Greenhouse customer use only; see [LICENSE](LICENSE) and [NOTICE](NOTICE).
