*Sample output for `daily-brief` on a fictional organization, default MCP Access ceiling, as of Wed 14 Oct 2026, 09:00 EDT. The recruiter asked "What needs me today?" and gave their Greenhouse sign-in email and New York time. The app can show a file, so the skill builds the page and sends this short reply beside it; Next is text. Every name and number is fictional.*

---

Morning, Riley. 4 candidates are waiting on a decision or a scorecard; Leo Fischer has gone longest without recorded activity, 2 days.

- [Leo Fischer](https://app.greenhouse.io/people/9007?application_id=8007), Product Designer: decision waiting, quiet 2 days.
- [Priya Shah](https://app.greenhouse.io/people/9001?application_id=8001), Senior Backend Engineer: decision waiting, quiet 0 days, and Dana Okafor's scorecard dated 8 Oct is still a draft (138 hours since interview).
- [Sofia Brandt](https://app.greenhouse.io/people/9008?application_id=8008), Product Designer: in Portfolio Review, quiet 24 days.

Also: 1 more decision waiting, 2 more scorecards not submitted, 3 more quiet candidates, 2 new applicants.

It's all on the page: filter it by req, and each row has its next prompt to copy.

Reminders for the 2 interviewers are on the page to copy.

I couldn't see interview times, offers or hiring managers with your current access; /greenhouse:configure shows what to turn on.

Across your 4 open reqs, counting what you can see in Greenhouse, as of Wed 14 Oct, 09:00 EDT.

Next: /greenhouse:candidate-debrief Leo Fischer on Product Designer · /greenhouse:pipeline-review Account Executive, Mid-Market

## The page beside it

**Daily brief, 14 Oct** · Riley Morgan's view · as of Wed 14 Oct, 09:00 EDT · chips by Req. Headline as in the reply; scope line "Across your 4 open reqs as recruiter or coordinator, counting active candidates that you can see".

Tiles: **Decisions waiting** 3 (interviews done, no decision recorded; the headline's tile) · **Scorecards not submitted** 3 (2 interviewers, last 14 days) · **Quiet candidates** 4 (14 or more days, 7 in the first stage) · **New since yesterday** 2 (applicants · 0 fresh scorecards).

1. **Decisions waiting (3)**. "Greenhouse flags these as ready for a decision: interviews are done and none is recorded. Already decided and holding the move on purpose? Ignore the flag." Each row's chip reads Needs decision and carries a copyable debrief prompt; opening it shows why it is here ("In Onsite, decision waiting, no activity recorded for 2 days") and the next step, "Debrief, then record the outcome in Greenhouse".

   | Candidate | Req | Stage | Scorecards (14 days) | Days quiet | Status |
   |---|---|---|---|---:|---|
   | Leo Fischer | Product Designer | Onsite | 2 in, 0 draft | 2 | Needs decision |
   | Nate Cole | Account Executive, Mid-Market | Panel Interview | 2 in, 1 draft | 1 | Needs decision |
   | Priya Shah | Senior Backend Engineer | Onsite | 4 in, 1 draft | 0 | Needs decision |

2. **Scorecards started but not submitted (3 scorecards, 2 interviewers, last 14 days)**, chips by interviewer. "Interviewers who haven't opened their scorecard show up only with interview access (harvest:interviews:list)."

   | Interviewer | Candidate | Req | Interviewed | Hours since interview |
   |---|---|---|---|---:|
   | Dana Okafor | Priya Shah (last open scorecard) | Senior Backend Engineer | Thu 8 Oct | 138 |
   | Dana Okafor | Nate Cole (last open scorecard) | Account Executive, Mid-Market | Sat 10 Oct | 93 |
   | Sam Lindqvist | Hannah Weiss (last open scorecard) | Customer Support Specialist | Tue 13 Oct | 22 |

3. **Reminders to copy (2 interviewers)**. "One per interviewer with a scorecard outstanding. Copy one and send it yourself: nothing is sent from Greenhouse." Dana Okafor's reads:

   ```
   Hi Dana, Greenhouse still shows your scorecards for Priya Shah (Senior Backend Engineer, scorecard dated Thu 8 Oct) and Nate Cole (Account Executive, Mid-Market, scorecard dated Sat 10 Oct) as drafts, and the team is waiting on them to decide. If an interview moved or you weren't on it, let me know. Thanks, Riley
   ```

   Sam Lindqvist's names Hannah Weiss the same way.
4. **Quiet candidates (4)**. Each Next step reads "Schedule the next step (coordinator: Chris Patel)", and each row carries a copyable status prompt.

   | Candidate | Req | Stage | Days since last activity |
   |---|---|---|---:|
   | Sofia Brandt | Product Designer | Portfolio Review | 24 |
   | Isabel Moreno | Account Executive, Mid-Market | Hiring Manager Screen | 18 |
   | Marcus Bell | Senior Backend Engineer | Recruiter Screen | 19 |
   | Kwame Mensah | Customer Support Specialist | Phone Screen | 15 |

5. **New since yesterday (2 applicants, 0 fresh scorecards)**: Senior Backend Engineer: 1 new applicant · Product Designer: 1 new applicant.
6. **Pipeline snapshot**. "One row per req. In review is its own number; the bar shows active applications past review, by stage in plan order, early stages light and late stages dark." Each row carries a copyable pipeline-review prompt; opening it shows New since yesterday, Needs review and Coordinator Chris Patel (the hiring manager is not visible).

   | Req | Days open | Status | Active | In review | Past review by stage | Decisions | Quiet |
   |---|---:|---|---:|---:|---|---:|---:|
   | Senior Backend Engineer | 72 | Decisions waiting | 6 | 2 | Recruiter Screen 1 · Technical Phone Screen 1 · Onsite 1 · Offer 1 | 1 | 1 |
   | Product Designer | 43 | Decisions waiting | 4 | 1 | Recruiter Screen 1 · Portfolio Review 1 · Onsite 1 | 1 | 1 |
   | Account Executive, Mid-Market | 91 | Decisions waiting | 3 | 0 | Recruiter Screen 1 · Hiring Manager Screen 1 · Panel Interview 1 | 1 | 1 |
   | Customer Support Specialist | 24 | Moving | 3 | 1 | Phone Screen 1 · Onsite 1 | 0 | 1 |

   Opened, the rows read: Senior Backend Engineer, New since yesterday 1 · Needs review 2 in review · 1 at 7 or more days · oldest applied 5 Oct; Product Designer, 1 · 1 in review · 0 at 7 or more days · oldest applied 13 Oct; Account Executive, Mid-Market, 0 · 0 in review; Customer Support Specialist, 0 · 1 in review · 1 at 7 or more days · oldest applied 2 Oct.

Interviews today and tomorrow and Offers in flight are left off the page: their tools are not listed, and the footnote names them.

How this was ranked: quiet is 14 or more days without recorded activity (7 in the first stage, where the clock runs from the day they applied), because a week without a first look is when applicants start accepting other interviews; scorecards count when started and not submitted within 14 days; "Decisions waiting" is Greenhouse's needs_decision flag on applications past the first stage: interviews are complete and no decision is recorded; applications still in review are counted under Needs review. Every threshold is inclusive. Tell me different numbers and I'll redo it.

Footnote: "Not visible with your Greenhouse MCP access: interviews, and interviewers who haven't started a scorecard, offers, hiring manager (needs harvest:interviews:list, harvest:offers:list plus the private-data permission and harvest:job_hiring_managers:list). A Site Admin can enable them under Configure > Dev Center > MCP Access > Endpoints, or you may have left them unticked when connecting; saving makes everyone in the organization reconnect, and the tool list can take up to 10 minutes to refresh. /greenhouse:configure lists everything."

Next prompts with copy buttons: /greenhouse:candidate-debrief Leo Fischer on Product Designer · /greenhouse:pipeline-review Account Executive, Mid-Market · /greenhouse:configure

## When no page can be built

If the app can show a file or a rendered document but cannot run the builder, the skill writes the same page by hand as a still page: the same tiles and sections, with no buttons, so the reply says only "It's all on the page." If the app can show neither a file nor a rendered document: the short reply above on its own, with "Ask for decisions, scorecards, quiet candidates, new applicants or the snapshot." in place of the page line and "Want me to draft reminders for the 2 interviewers?" in place of the reminders line, then one plain line: "I couldn't open a page here, so it's all in chat: ask for any section."
