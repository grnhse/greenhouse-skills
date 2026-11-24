*Sample output for `configure` on a fictional organization, default MCP Access ceiling, as of Wed 14 Oct 2026, 09:00 EDT. The recruiter said "Get me set up with Greenhouse", with their sign-in email and New York time. The app can show a file, so the skill builds the page and sends this short reply beside it; the chooser is a numbered list. The profile line carries the sign-in email exactly as Greenhouse holds it; this sample shows a placeholder there. Every name and number is fictional.*

---

You're set up, Riley: matched to Riley Morgan, the recruiter on 4 open reqs. 7 of the 7 data skills work from here; the one worth asking your Site Admin for is harvest:interviews:list; a note you can send them is on the page. Re-run it after your admin saves.

4 applications are sitting in Application Review across your reqs, 2 of them on Senior Backend Engineer. Your setup and your open reqs are on the page.

Greenhouse profile: Riley Morgan · <sign-in email as Greenhouse holds it> · user_id=4001 · site_admin=false · role=recruiter · tz=America/New_York

Counting the open reqs where you're recruiter or coordinator that you can see, as of Wed 14 Oct, 09:00 EDT.

Where do you want to start?
1. Run my daily brief: 4 open reqs, 3 decisions waiting, 4 candidates quiet 14 or more days
2. Review Senior Backend Engineer: 6 active candidates
3. Check on a candidate: tell me who
4. Debrief a candidate: tell me who

## The page beside it

**Greenhouse setup** · Riley Morgan's view · as of Wed 14 Oct, 09:00 EDT. Headline "You're set up, Riley: matched to Riley Morgan, the recruiter on 4 open reqs."; scope line "Covering the tools listed in this session and the open reqs where you're recruiter or coordinator that you can see". The profile line and the email address are not on the page.

Facts: Matched to Riley Morgan · Role recruiter.

Tiles: **Open reqs** 4 · **Active applications** 16 · **Decisions waiting** 3 · **Quiet 14 or more days** 4. No tile is highlighted, because the story sentence is about applications in review, which no tile counts.

1. **What works from here**. "A tool can be missing because a Site Admin hasn't enabled it, your Greenhouse permissions don't allow it, or you didn't tick it when connecting." Try prompts without a <name> placeholder have a copy button.

   | Skill | Status | Try | If something is missing |
   |---|---|---|---|
   | Daily brief | Partial: missing `list_interviews`, `list_offers`, `list_job_hiring_managers` | "What needs me today?" | For now: today's interviews and offers from your Greenhouse dashboard |
   | Candidate status | Partial: missing `list_interviews`, `list_offers`, `list_application_stages`, `list_notes` | "Where is <name>?" (you supply the name) | For now: next interview and offer from the candidate's profile |
   | Candidate debrief | Partial: missing `list_ai_opt_out_statuses`, `list_scorecard_candidate_attributes`, `list_interviews`, `list_notes`; writes `add_candidate_note`, `move_application` | "Who still owes a scorecard on Senior Backend Engineer?" | For now: add the note or move the stage yourself in Greenhouse |
   | Pipeline review | Partial: missing `list_application_stages`, `list_offers`, `list_openings`, `list_job_hiring_managers`, `list_interviews`, `list_sources` | "How is Senior Backend Engineer doing?" | For now: days in stage and source from the job's pipeline view |
   | Scorecard draft | Partial (paste-ready text): missing `list_interview_kits` with `create_scorecard`, `list_job_interviews`, `list_scorecard_questions` | "Write up my interview feedback for <name>" | For now: paste the text into the scorecard |
   | Interview week | Partial: missing `list_interviews`, `list_interviewers`, `list_job_interviews` | "What interviews are on this week?" | For now: interview times and panels from your Greenhouse dashboard |
   | Source review | Partial: missing `list_sources`, `list_application_stages` | "Where are Senior Backend Engineer's applicants coming from?" | For now: source names from the job's reports |

   Status chips: Partial on all seven rows (the chip reads Partly).
2. **A note for your Site Admin**: the note, whole, with a Copy note button, and under it "Saving signs everyone in your organization out of Greenhouse MCP; each person reconnects once, and the tool list can take up to 10 minutes to refresh."

   ```
   Hi, I've started using Greenhouse from my AI assistant, and a few things I'd use every week aren't switched on for the connector. Could you turn these on under Configure > Dev Center > MCP Access > Endpoints?
   - harvest:interviews:list: today's interviews and who hasn't started a scorecard
   - harvest:application_stages:list: exact days in stage
   - harvest:offers:list: offers in flight (also needs the private and salary data permission)
   - harvest:openings:list: open seats and target start dates
   - harvest:notes:list: recruiter notes and the last logged email
   - harvest:notes:create: a debrief note recorded from here
   - harvest:applications:move: a stage move from here
   - harvest:job_hiring_managers:list and harvest:job_owners:list: hiring manager and co-owners per req
   - harvest:scorecard_candidate_attributes:list: attribute ratings in the debrief
   - harvest:ai_opt_out_statuses:list: the AI opt-out check (also needs Talent Matching)
   - harvest:sources:list: source names per candidate and per req
   - harvest:interviewers:list: interview panels and who has not started a scorecard
   - harvest:interview_kits:list with harvest:scorecards:create: a draft scorecard filed from here
   - harvest:job_interviews:list: interview names on the draft
   - harvest:scorecard_questions:list: question headings on the draft
   Nothing changes in Greenhouse without me: I confirm every change myself, one at a time, and nothing is ever deleted. Once it's done I'll reconnect Greenhouse so the new permissions take effect. Thanks, Riley
   ```

3. **Your open reqs**, busiest first, each row with a copyable pipeline-review prompt

   | Req | Active | Decisions waiting | Quiet | New in 24 hours |
   |---|---:|---:|---:|---:|
   | Senior Backend Engineer | 6 | 1 | 1 | 1 |
   | Product Designer | 4 | 1 | 1 | 1 |
   | Account Executive, Mid-Market | 3 | 1 | 1 | 0 |
   | Customer Support Specialist | 3 | 0 | 1 | 0 |

How this was judged: Ready means every core tool is listed, Partial only enhancements or the user lookup missing, Not yet another core tool missing; quiet is 14 or more days with no activity recorded, because two working weeks without a touch is when candidates start accepting other interviews; new is the last 24 hours; busiest is most active applications. Thresholds are inclusive. Tell me different numbers and I'll redo it.

Notes under the panels: "Seeing a tool doesn't guarantee access: Greenhouse applies your own permissions when it's called." and the footnote: "Not visible with your Greenhouse MCP access: this week's interview calendar and today's interviews, who hasn't started a scorecard, exact days in stage, offers in flight, open seats and target start dates, recruiter notes and the last logged email, notes and stage moves recorded from here, hiring manager and co-owners per req, attribute ratings in the debrief, the AI opt-out check, source names, interview panels and replies, draft scorecards filed from here, interview names, question headings on the draft (needs harvest:interviews:list, harvest:application_stages:list, harvest:offers:list, harvest:openings:list, harvest:notes:list, harvest:notes:create, harvest:applications:move, harvest:job_hiring_managers:list, harvest:job_owners:list, harvest:scorecard_candidate_attributes:list, harvest:ai_opt_out_statuses:list, harvest:sources:list, harvest:interviewers:list, harvest:interview_kits:list, harvest:scorecards:create, harvest:job_interviews:list, harvest:scorecard_questions:list). A Site Admin can enable them under Configure > Dev Center > MCP Access > Endpoints, or you may have left them unticked when connecting; saving makes everyone in the organization reconnect, and the tool list can take up to 10 minutes to refresh. /greenhouse:configure lists everything."

Next prompts with copy buttons, the chooser's options written as prompts: /greenhouse:daily-brief · /greenhouse:pipeline-review Senior Backend Engineer · /greenhouse:candidate-status <name> · /greenhouse:candidate-debrief <name> on Senior Backend Engineer. The two person prompts carry a placeholder because nobody is named yet.

## When no page can be built

If the app can show a file or a rendered document but cannot run the builder, the skill writes the same page by hand as a still page: the same facts, tiles, table, note and open reqs, with no buttons, so the reply says only that it is all on the page. If the app can show neither a file nor a rendered document: the short reply above on its own, its second sentence ending "...the one worth asking your Site Admin for is harvest:interviews:list; say 'note for my admin' and I'll write it." and without "Your setup and your open reqs are on the page.", then one plain line: "I couldn't open a page here, so it's all in chat: ask for any section."
