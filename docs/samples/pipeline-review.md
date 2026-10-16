*Sample output for `pipeline-review` on a fictional organization, default MCP Access ceiling, as of Wed 14 Oct 2026, 09:00 EDT. The recruiter asked "How is the Senior Backend Engineer req doing? I have a sync with Dana this afternoon." and had given their Greenhouse sign-in email and New York time earlier in the conversation. The app can show a file, so the skill builds the page and sends this short reply beside it; Next is text. Every name and number is fictional.*

---

Riley, 1 candidate is waiting on a decision on Senior Backend Engineer.

It reads as On track: someone is in Onsite or later and not quiet, and no rule fires.

- [Priya Shah](https://app.greenhouse.io/people/9001?application_id=8001) has a decision waiting since 9 Oct.
- Dana Okafor's scorecard on [Priya Shah](https://app.greenhouse.io/people/9001?application_id=8001), dated 8 Oct, is still a draft.
- [Marcus Bell](https://app.greenhouse.io/people/9003?application_id=8003) has had no activity recorded for 19 days in Recruiter Screen.

Hiring-manager message (safe to share):
```
Hi Dana,
Omar Haddad is at the Offer stage on Senior Backend Engineer, and Priya Shah is in Onsite with a decision waiting. Four more are in process behind them: 1 in Technical Phone Screen, 1 in Recruiter Screen and 2 in Application Review; nobody has been rejected in the last 30 days.
One ask: Priya Shah has a decision waiting since 9 Oct: what's the call?
Riley
Numbers as of Wed 14 Oct
```

The stage flow, the funnel, the full roster and the rejections are on the page, with a next prompt to copy on each row.

I couldn't see days in stage, offers, seats, the hiring manager, interview times or sources with your current access, and the AI opt-out check couldn't run; /greenhouse:configure shows what to turn on.

Counting what you can see in Greenhouse, as of Wed 14 Oct, 09:00 EDT.

Next: /greenhouse:candidate-debrief Priya Shah on Senior Backend Engineer · /greenhouse:candidate-status Elena Marsh

## The page beside it

**Senior Backend Engineer pipeline** · Riley Morgan's view · as of Wed 14 Oct, 09:00 EDT. Headline as in the reply; scope line "Senior Backend Engineer · On track · 6 active (complete) · roster shows 3 of 3 roster rows that you can see".

Facts: Open 72 days · Req ENG-204 · Furthest Offer, stage 5 of 5 · Recruiter Riley Morgan · Coordinator Chris Patel · Greenhouse: Open the req. Seats and offers are not shown, because neither is visible.

Tiles: **Active applications** 6 (complete count) · **In review** 2 (longest waiting 9 days since applying) · **Decisions waiting** 1 (past review; interviews done, none recorded; the headline's tile) · **Quiet 7 or more days** 1 (of 4 past review).

1. **Hiring-manager message (safe to share)**: the message above with a copy button. "Names, stages and counts only. Confirm the recipient is on this job's hiring team before sending." Foot: "The numbers behind it: 6 active · 0 rejected in 30 days · 0 hired · by stage Application Review 2 · Recruiter Screen 1 · Technical Phone Screen 1 · Onsite 1 · Offer 1 · interviews next 7 days: not visible · offers outstanding: not visible"
2. **Risks**: "No rule fires; not a green light."
3. **Questions for the sync**, each with a copy button
   - Ask the hiring manager: Priya Shah has a decision waiting since 9 Oct: what's the call? (linked)
   - Stays with you: 2 in review, longest 9 days.
4. **Where the active applications stand**: the five stages in plan order, each with its active count (Application Review 2 · Recruiter Screen 1 · Technical Phone Screen 1 · Onsite 1 · Offer 1). Foot: "Each stage in plan order with its active applications; a dashed stage holds nobody now."
5. **Funnel, plan order**. "Bars count applications, not people. Reached is rebuilt from where each application ended or stands today." The review row is not drawn to scale.

   | Stage | Active | Rejected from here, 30 days | Reached at least (derived) | Pass-through |
   |---|---:|---:|---:|---|
   | Application Review (Bottleneck) | 2 | 0 | 6 | — |
   | Recruiter Screen | 1 | 0 | 4 | — |
   | Technical Phone Screen | 1 | 0 | 3 | — |
   | Onsite | 1 | 0 | 2 | — |
   | Offer | 1 | 0 | 1 | — |

   Foot: "Bottleneck: Application Review: 2 active, 9 and 0 days without recorded activity (a median needs 3 or more values)."
6. **Late stages: Technical Phone Screen, Onsite, Offer**, chips by stage, search box. "Ordered by stage reached, not by strength. Ratings are shown as given, never totalled." Each row carries a copyable prompt: a debrief for the row with a decision waiting, a status check for the others.

   | Candidate | Stage | Days quiet | Feedback | Status |
   |---|---|---:|---|---|
   | Omar Haddad | Offer | 1 | 3 complete, 0 started but not submitted · 1 Strong Yes, 2 Yes | |
   | Priya Shah | Onsite | 0 | 4 complete, 1 started but not submitted · 2 Strong Yes, 1 Yes, 1 No | Needs decision |
   | Elena Marsh | Technical Phone Screen | 3 | 1 complete, 0 started but not submitted · 1 Yes | |

   Opening Priya Shah's row shows Decision waiting since 9 Oct and Draft: Dana Okafor, dated 8 Oct. Omar Haddad's row carries no status chip because offers are not visible. Foot: "AI opt-out status could not be checked for these candidates."
7. **Rejections, last 30 days (0: we declined 0 · withdrew 0 · other or none recorded 0)**. "Reasons as recorded in Greenhouse." Then "None that you can see in the last 30 days."

How this was judged: bottleneck = the stage with the most active candidates, tie broken by the oldest median activity; quiet = no activity recorded for 7 or more days (a week untouched is when candidates accept other interviews); an offer is outstanding after 7 days in Created (a week unanswered needs a follow-up); rejections cover the last 30 days by rejected_at; the roster shows at most 50 rows, latest stage first, then longest without activity; questions on Onsite go to the hiring manager, the rest stay with you. Risk rules: at risk = 30+ days open, nobody past the first interview; slow = 60+ days, no finalist; gone quiet = 3+ past review, half quiet; thin = 2 or fewer past review; pass-through needs 20 resolved (10 for an early signal); a median needs 3 values; a draft within 30 days hides a tally. Every threshold is inclusive. Tell me different numbers and I'll redo it.

Notes under the panels: "Not visible with your Greenhouse MCP access: days in stage and pass-through, offers, seats, hiring manager, interviews, sources, opt-out flags (needs harvest:application_stages:list, harvest:offers:list plus the private-data permission, harvest:openings:list, harvest:job_hiring_managers:list, harvest:interviews:list, harvest:sources:list, harvest:ai_opt_out_statuses:list). A Site Admin can enable them under Configure > Dev Center > MCP Access > Endpoints, or you may have left them unticked when connecting; saving makes everyone in the organization reconnect, and the tool list can take up to 10 minutes to refresh. /greenhouse:configure lists everything." and "AI opt-out status could not be checked for these candidates."

Next prompts with copy buttons: /greenhouse:candidate-debrief Priya Shah on Senior Backend Engineer · /greenhouse:candidate-status Elena Marsh · /greenhouse:configure

## When no page can be built

If the app can show a file or an artifact but cannot run the builder, the skill writes the same page by hand as a still page: the same facts, tiles and sections, with no buttons, so the reply says only "It's all on the page." If the app has no way to show a file or an artifact at all: the short reply above on its own, with "Ask for the funnel, the roster, the rejections or the full review." in place of the page line, then one plain line: "I couldn't open a page here, so it's all in chat: ask for any section."
