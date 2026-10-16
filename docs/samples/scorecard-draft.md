*Sample output for `scorecard-draft` on a fictional organization, signed in as the interviewer Tom Lee, default MCP Access ceiling, as of Wed 14 Oct 2026, 09:00 EDT. Every name and number is fictional.*

---

Priya Shah on Senior Backend Engineer, currently in Onsite
From the records that you can see, as of Wed 14 Oct, 09:00 EDT.
Not visible with your Greenhouse MCP access: creating the draft, interview names, question headings (needs harvest:interview_kits:list, harvest:scorecards:create, harvest:job_interviews:list, harvest:scorecard_questions:list). A Site Admin can enable them under Configure > Dev Center > MCP Access > Endpoints, or you may have left them unticked when connecting; saving makes everyone in the organization reconnect, and the tool list can take up to 10 minutes to refresh. /greenhouse:configure lists everything.

```
Scorecard text for Priya Shah · Senior Backend Engineer · your interview
Overall: Yes
Key takeaways:
Good ownership stories from the payments migration; she led the rollback plan when the first cutover slipped. Wants to grow into a tech lead role within a year. Asked sharp questions about on-call load.
Open the scorecard in Greenhouse and paste the text above: https://app.greenhouse.io/people/9001?application_id=8001
```

Next: /greenhouse:candidate-debrief Priya Shah on Senior Backend Engineer once the panel's feedback is in · /greenhouse:configure

*Asked how it was judged, the skill adds one line after the scope line:* How this was judged: the rating comes only from your words (strong yes → Strong Yes, lean yes → Yes, lean no or "I'd pass" → No, definitely not → Definitely Not, nothing said → not set) because a draft needs no rating; the interview date is saved at noon in your time zone so the day survives any zone shift; a card more than one message old is re-checked before the write. Tell me different numbers and I'll redo it.

## With `list_interview_kits` and `create_scorecard` enabled

Filing mode runs the duplicate check, which finds the scorecard you (Tom Lee) submitted on 8 Oct for this kit, so the skill stops before the card. The job has seven kits and `list_job_interviews` is still hidden, so the kit was asked for by position first (kit 5 of 7, "Onsite, hiring manager: ownership, growth, on-call expectations."), together with the interview date.

Priya Shah on Senior Backend Engineer, currently in Onsite
From the records that you can see, as of Wed 14 Oct, 09:00 EDT.
Not visible with your Greenhouse MCP access: interview names, question headings (needs harvest:job_interviews:list, harvest:scorecard_questions:list). A Site Admin can enable them under Configure > Dev Center > MCP Access > Endpoints, or you may have left them unticked when connecting; saving makes everyone in the organization reconnect, and the tool list can take up to 10 minutes to refresh. /greenhouse:configure lists everything.

You submitted a scorecard for this interview on 8 Oct; a second one would duplicate it.

```
Scorecard text for Priya Shah · Senior Backend Engineer · kit 5 of 7
Overall: Yes · Interviewed: 8 Oct
Key takeaways:
Good ownership stories from the payments migration; she led the rollback plan when the first cutover slipped. Wants to grow into a tech lead role within a year. Asked sharp questions about on-call load.
Open the scorecard in Greenhouse and paste the text above: https://app.greenhouse.io/people/9001?application_id=8001
```

Next: /greenhouse:candidate-debrief Priya Shah on Senior Backend Engineer once the panel's feedback is in · /greenhouse:candidate-status Priya Shah

## The preview card, had no scorecard of Tom's existed on this kit

Same headline, scope and footnote lines as above, then the card ends the message (no Next after it):

```
Draft scorecard · Priya Shah
Checked just now: no scorecard of yours on this interview.
Candidate: Priya Shah · Job: Senior Backend Engineer · Stage: Onsite
Interview: kit 5 of 7
Interviewer and submitter: you
Interviewed: 8 Oct (Greenhouse records the date only)
Overall rating: Yes
---
Key takeaways:
Good ownership stories from the payments migration; she led the rollback plan when the first cutover slipped. Wants to grow into a tech lead role within a year. Asked sharp questions about on-call load.
---
Notifies: nobody until you submit. Undo: discard the draft in Greenhouse. Not in this: submitting.
Greenhouse saves this as a draft; you review and submit it in Greenhouse. Reply "yes" to proceed.
```

On "yes" the skill would call `create_scorecard` with `status: "draft"`, `interviewed_at: "2026-10-08T12:00:00-04:00"` and no `confirm`, read the draft back, and close with: Draft saved as of Wed 14 Oct, 09:01 EDT. Review and submit it in Greenhouse: https://app.greenhouse.io/people/9001?application_id=8001
