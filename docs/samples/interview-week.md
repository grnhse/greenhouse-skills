*Sample output for `interview-week` on a fictional organization, as of Wed 14 Oct 2026, 09:00 EDT. The recruiter asked "What interviews do I have this week?" and gave their Greenhouse sign-in email and New York time. The app can show a file, so in both runs below the skill builds a page and sends the short reply beside it; Next is text. Every name and number is fictional.*

---

## On the default tools

*`list_interviews`, `list_interviewers` and `list_job_interviews` are not listed, so the calendar, what is still to schedule and the panels are not visible. The skill still reads the applications on the recruiter's reqs and the scorecards started on them in the last 30 days, and builds the page from those.*

Morning, Riley. I can't see interview times with your current access; 3 scorecards from the last 30 days are started and not submitted.

Dana Okafor has two, on Priya Shah (Senior Backend Engineer, Thu 8 Oct) and Nate Cole (Account Executive, Mid-Market, Sat 10 Oct); Sam Lindqvist has one, on Hannah Weiss (Customer Support Specialist, Tue 13 Oct).

The scorecards are on the page by interviewer, and the reminders are there to copy.

I couldn't see interview times or who is on each panel with your current access; /greenhouse:configure shows what to turn on.

Across your 4 open reqs, Wed 14 to Tue 20 Oct, counting what you can see in Greenhouse, as of Wed 14 Oct, 09:00 EDT.

Next: /greenhouse:daily-brief · /greenhouse:configure

### The page beside it

**Interviews, 14 to 20 Oct** · Riley Morgan's view · as of Wed 14 Oct, 09:00 EDT · chips by Req. Headline as in the reply; scope line "Across your 4 open reqs as recruiter or coordinator, interviews from Wed 14 Oct to Tue 20 Oct that you can see, times in EDT".

Tiles: **Scorecards not submitted** 3 (2 interviewers, last 30 days; the headline's tile). There is no tile for the week, what is still to schedule or panel replies, because none of those was read.

1. **Scorecards started but not submitted (3 scorecards, 2 interviewers, last 30 days)**. "Copy a reminder and send it yourself: nothing is sent from Greenhouse. Counts and dates only; no ratings or scorecard text are read. Interviewers who haven't opened their scorecard show up only with interview access (harvest:interviews:list)." One item per interviewer, oldest interview first, each with a reminder to copy; an interview is named by the application's stage, because interview names are not visible.
   - Dana Okafor · chip 2 scorecards · Priya Shah, Senior Backend Engineer, interview in Onsite, Thu 8 Oct, started, not submitted, 138 hours since the interview · Nate Cole, Account Executive, Mid-Market, interview in Panel Interview, Sat 10 Oct, started, not submitted, 93 hours since the interview

     ```
     Hi Dana, Greenhouse is still waiting on your scorecards for Priya Shah (Senior Backend Engineer, interview in Onsite, Thu 8 Oct) and Nate Cole (Account Executive, Mid-Market, interview in Panel Interview, Sat 10 Oct).
     The team needs them to decide; if an interview moved or you weren't on it, let me know. Thanks, Riley
     ```

   - Sam Lindqvist · chip Scorecard due · Hannah Weiss, Customer Support Specialist, interview in Onsite, Tue 13 Oct, started, not submitted, 22 hours since the interview

     ```
     Hi Sam, Greenhouse is still waiting on your scorecard for Hannah Weiss (Customer Support Specialist, interview in Onsite, Tue 13 Oct).
     The team needs it to decide; if the interview moved or you weren't on it, let me know. Thanks, Riley
     ```

The "How this was read" line is the same as on the second run's page, below.

Footnote: "Not visible with your Greenhouse MCP access: interview times, still to schedule, interviews awaiting feedback, panels, replies, scorecards not started, interview names (needs harvest:interviews:list, harvest:interviewers:list, harvest:job_interviews:list). A Site Admin can enable them under Configure > Dev Center > MCP Access > Endpoints, or you may have left them unticked when connecting; saving makes everyone in the organization reconnect, and the tool list can take up to 10 minutes to refresh. /greenhouse:configure lists everything."

Next prompts with copy buttons: /greenhouse:daily-brief · /greenhouse:configure

## Default tools plus `list_interviews`

*`list_interviewers` and `list_job_interviews` stay hidden, so panels and interview names are not visible, and an interview is named by the application's stage. Only Dana Okafor's scorecard on Priya Shah sits on a calendar interview Greenhouse marks as awaiting feedback; the other two drafts above were collected without a calendar time, so they stay with the daily brief.*

Morning, Riley. 2 interviews are on the calendar in the next 7 days across your 4 open reqs, 1 of them today.

- [Hannah Weiss](https://app.greenhouse.io/people/9014?application_id=8014), Customer Support Specialist, interview in Onsite, today 13:00–14:00.

Also: 1 scorecard owed by 1 interviewer.

The whole week is on the page; filter it by day or by req, and the reminders are there to copy.

I couldn't see who is on each panel or the interview names with your current access; /greenhouse:configure shows what to turn on.

Across your 4 open reqs, Wed 14 to Tue 20 Oct, counting what you can see in Greenhouse, as of Wed 14 Oct, 09:00 EDT.

Next: /greenhouse:pipeline-review Customer Support Specialist · /greenhouse:configure

### The page beside it

**Interviews, 14 to 20 Oct** · Riley Morgan's view · as of Wed 14 Oct, 09:00 EDT · chips by Req. Headline as in the reply; scope line "Across your 4 open reqs as recruiter or coordinator, interviews from Wed 14 Oct to Tue 20 Oct that you can see, times in EDT".

Tiles: **Interviews, next 7 days** 2 (1 today · 1 tomorrow; the headline's tile) · **Still to schedule** 0 · **Awaiting feedback** 1 (1 interviewer, last 30 days). There is no tile for missing panel replies, because panels are not visible.

1. **This week (2 interviews)**, chips by day, search box. "Times are EDT. Rooms and video links are on each interview in Greenhouse."

   | Day | Time | Candidate | Req | Interview | Panel | Status |
   |---|---|---|---|---|---|---|
   | Wed 14 Oct | 13:00–14:00 | Hannah Weiss (linked) | Customer Support Specialist | interview in Onsite | panel: not visible | Scheduled |
   | Thu 15 Oct | 11:00–11:30 | Dan Kim (linked) | Product Designer | interview in Recruiter Screen | panel: not visible | Scheduled |

   Opening either row shows Coordinator Chris Patel and Organizer Chris Patel; length and replies are not visible.
2. **Still to schedule (0 candidates)**. "Greenhouse marks these interviews as to be scheduled in the candidate's current stage. Days count from when the slot opened. This may include interviews from stages already passed." Then "Nothing is waiting to be scheduled."
3. **Awaiting feedback (1 scorecard, 1 interviewer, last 30 days)**. "Copy a reminder and send it yourself: nothing is sent from Greenhouse. Counts and dates only; no ratings or scorecard text are read."
   - Dana Okafor · chip Scorecard due · Priya Shah, Senior Backend Engineer, interview in Onsite, Thu 8 Oct, started, not submitted, 137 hours since the interview · reminder to copy:

     ```
     Hi Dana, Greenhouse is still waiting on your scorecard for Priya Shah (Senior Backend Engineer, interview in Onsite, Thu 8 Oct).
     The team needs it to decide; if the interview moved or you weren't on it, let me know. Thanks, Riley
     ```

How this was read: the window is 7 days from today, in EDT; an interview counts when Greenhouse has a start time for it in the window, and all-day events such as take-home tests are listed as "All day"; still to schedule = interviews Greenhouse marks as to be scheduled in the candidate's current stage on an active application, with days counted from when the slot opened; awaiting feedback = interviews in the last 30 days that Greenhouse marks as awaiting feedback, one line per interviewer whose scorecard is not submitted, with hours counted from the interview's end; a panel needs a change when someone declined or nobody is on it. Nothing here rates anyone: counts describe calendars. Tell me different numbers and I'll redo it.

Footnote: "Not visible with your Greenhouse MCP access: panels, replies, scorecards not started, interview names (needs harvest:interviewers:list, harvest:job_interviews:list). A Site Admin can enable them under Configure > Dev Center > MCP Access > Endpoints, or you may have left them unticked when connecting; saving makes everyone in the organization reconnect, and the tool list can take up to 10 minutes to refresh. /greenhouse:configure lists everything."

Next prompts with copy buttons: /greenhouse:pipeline-review Customer Support Specialist · /greenhouse:configure

## When no page can be built

Either run. If the app can show a file or a rendered document but cannot run the builder, the skill writes the same page by hand as a still page: the same tiles and sections, with no buttons, so the reply says only "It's all on the page." If the app can show neither a file nor a rendered document: the short reply on its own, with "Ask for a day, what's still to schedule, or who owes feedback." in place of the page line and the reminders question after it ("Want the reminders for the 2 interviewers?" on the default tools; "Want the reminder for the 1 interviewer?" with `list_interviews`), then one plain line: "I couldn't open a page here, so it's all in chat: ask for any section."
