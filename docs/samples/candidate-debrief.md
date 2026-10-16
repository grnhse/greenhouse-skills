*Sample output for `candidate-debrief` on a fictional organization, default MCP Access ceiling, as of Wed 14 Oct 2026, 09:00 EDT. The recruiter, Riley Morgan, asked "Pull the debrief for Priya Shah on Senior Backend Engineer" and had given their Greenhouse sign-in email, so the skill knows the open draft is not theirs before it shows any rating. The brief is answered in chat; a page is built only when asked. Every name and number is fictional.*

---

4 of 5 scorecards are in: Strong Yes 2 · Yes 1 · No 1. Dana Okafor's is still a draft.
[Priya Shah](https://app.greenhouse.io/people/9001?application_id=8001) · Senior Backend Engineer · stage Onsite (4 of 5), next Offer · Needs Decision: Greenhouse marks a decision as waiting · scorecards that you can see · as of Wed 14 Oct, 09:00 EDT

| Interviewer | Interviewed | Rating | Status | Takeaways |
|---|---|---|---|---|
| Sam Lindqvist | 7 Oct | Strong Yes | complete | "Drove the design of a multi-region event pipeline end to end and spotted the idempotency gap before I raised it." · "sized the reconciliation job sensibly" · to the team: "Strongest system design round I have run this quarter." |
| Ana Ruiz | 7 Oct | Strong Yes | complete | "Finished both coding problems with tests and stated assumptions early." · "caught an off-by-one in her own code while explaining it" |
| Tom Lee | 8 Oct | Yes | complete | "Good ownership stories from the payments migration; she led the rollback plan when the first cutover slipped." · "asked sharp questions about on-call load" |
| Mei Tanaka | 8 Oct | No | complete | "the failure-mode analysis was thin: no answer for partial writes across regions and the reconciliation job was hand-waved" · to the team: "I would want one more design conversation before we extend an offer." |
| Dana Okafor | 8 Oct | — | draft, not submitted | |

### Where they agree and disagree
- Lone dissent: Mei Tanaka (No), resting on the architecture deep dive: "When I pushed on the design from the earlier round, the failure-mode analysis was thin."
- Sam Lindqvist (Strong Yes): "sized the reconciliation job sensibly" vs Mei Tanaka (No): "the reconciliation job was hand-waved"; the same design, pushed on in two different rounds.
- Ana Ruiz (Strong Yes): "Finished both coding problems with tests" vs Mei Tanaka (No): "Strong on breadth, not yet on depth under pressure."
- Tom Lee (Yes): "she led the rollback plan when the first cutover slipped" vs Mei Tanaka (No): "no answer for partial writes across regions"
- Where they agree: three of four landed on the Yes side (Sam Lindqvist and Ana Ruiz at Strong Yes, Tom Lee at Yes).

### Owed
- Dana Okafor: interviewed 8 Oct, scorecard still draft (6 days)
  ```
  The debrief for Priya Shah (Senior Backend Engineer) is coming up and your scorecard dated 8 Oct is still a draft. Could you submit it before then?
  If the interview moved or you weren't on it, let Riley Morgan know.
  ```

### Open questions for the panel
- Do we decide without Dana Okafor's scorecard, or wait?
- Mei Tanaka's No is the only rating on that side: what would the "one more design conversation" she asks for need to show?
- Sam Lindqvist and Mei Tanaka saw the same reconciliation job differently ("sized sensibly" against "hand-waved"): did the deep dive add a constraint the morning round did not have?
- Mei Tanaka's "not yet on depth under pressure": which part of the failure-mode discussion sat behind that?

Not visible with your Greenhouse MCP access: attribute splits, interviews still to come and unstarted scorecards, recruiter notes (needs harvest:scorecard_candidate_attributes:list, harvest:interviews:list, harvest:notes:list). A Site Admin can enable them under Configure > Dev Center > MCP Access > Endpoints, or you may have left them unticked when connecting; saving makes everyone in the organization reconnect, and the tool list can take up to 10 minutes to refresh. /greenhouse:configure lists everything.
AI opt-out status could not be checked.
For the hiring team only, never a candidate; private notes are left out, ask to see them.
The decision is yours. Tell me what you decided and I'll preview the note or the move.
Next: /greenhouse:candidate-status Priya Shah · /greenhouse:configure

*Asked how it was counted, the skill adds one line:* How this was counted: complete scorecards only; a draft is owed once its interview date has passed; "submitted n days after" shows past two calendar days: the gap is worth knowing, never a discount; k of n counts active stages. Tell me different numbers and I'll redo it.

## After "We are taking her to Offer. Log a note that the panel split on system design and Dana is comfortable, then move her." (with `add_candidate_note` and `move_application` enabled)

Two changes, each confirmed on its own: the note first, because it is quiet and records why; the move after, because it runs the Offer stage's rules. Nothing is written in this turn.

**Note on Priya Shah (Senior Backend Engineer)**

```
Debrief 14 Oct: We are taking Priya Shah to Offer. Open points: the panel split on system design; Dana Okafor is comfortable with it. Next step: move to Offer.
```

Visibility: private (say public or admin_only to change it). Notifies: nobody; the note carries no @-mentions. Undo: not from here; delete it on the profile in Greenhouse. Add the note? Reply "yes" to proceed.

*On the yes, the skill calls `add_candidate_note` with `visibility: "private"`, confirms from the response because `list_notes` is still hidden, and says:* Note added to Priya Shah's profile. https://app.greenhouse.io/people/9001?application_id=8001

*It then re-reads the application (the brief was an earlier turn), finds it still in Onsite, and shows the second card:*

Scorecards still draft: Dana Okafor, 8 Oct.

**Move Priya Shah (Senior Backend Engineer)**

From Onsite to Offer. Notifies: Greenhouse runs Offer's rules, which can email the candidate or the team and send forms, tests or scheduling requests; no email is sent from here. Undo: move back to Onsite with its own card; an email already sent can't be recalled. Not in this: rejecting, hiring, any email from me. Move them? Reply "yes" to proceed.

*On the yes, the skill calls `move_application` with the application id and the Onsite and Offer stage ids only, reads the application back, and closes with:* Now in Offer as of Wed 14 Oct, 09:03 EDT. Undo: "Move Priya Shah back to Onsite". https://app.greenhouse.io/people/9001?application_id=8001
Next: /greenhouse:candidate-status Priya Shah · Re-run the debrief once Dana Okafor's scorecard is in
