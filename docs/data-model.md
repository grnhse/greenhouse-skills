# Data model

Author reference, not shipped in the plugin. Sources: the Harvest V3 API reference, the Greenhouse MCP server's tool schemas, and behaviour confirmed by Greenhouse.

Harvest V3 is flat: child rows carry the parent's id and parents never list children, so every answer is "find the parent id, then list the children filtered by it". Greenhouse returns records, not totals: page to the end (`paging.next` goes back alone as `cursor`) before calling a number a total.

Shared traps: an empty id list is no filter and returns everything you can see; at most 50 ids per list; `per_page` defaults to 100, max 500 (search 10, max 100); a date range is one lower bound (`gte` or `gt`) plus one upper (`lte` or `lt`), lower strictly before upper, else 422.

## Join tree

```
job (list_jobs, search_jobs, get_job)
|- stages (list_job_stages: job_ids)           sort_order, active
|- hiring team: reverse only, via search_jobs(user_id, user_role), or
|  list_job_owners / list_job_hiring_managers (job_ids) when enabled
|- interview slots (list_job_interviews: job_ids)   name, duration, job_interview_stage_id
|- applications (list_applications: job_ids)   candidate_id, status, job_interview_stage_id
   |- candidate (list_candidates: ids)
   |- source_id -> list_sources(ids)              name, type (sourcing strategy)
   |- referrer_id -> list_referrers               a referrer, not a user
   |- scorecards (list_scorecards: application_ids)
   |     interviewer_id -> list_users(ids); interview_kit_id -> list_interview_kits
   |     -> job_interview_id -> list_job_interviews (slot name, job_interview_stage_id)
   |- interviews (list_interviews: application_ids or job_ids)
   |     job_interview_id -> list_job_interviews
   |     id -> list_interviewers(interview_ids)   user_id -> list_users; scorecard_id -> list_scorecards
   |- application_stages, offers, notes (application_ids)
```

## Default-ceiling tools

| Tool | Holds | Filters | Traps |
|---|---|---|---|
| `list_applications` | candidate_id, job_id, status, stage_id, job_interview_stage_id, stage_name, needs_decision, rejected_at, last_activity_at, recruiter_id, coordinator_id, source_id, referrer_id | `job_ids`, `candidate_ids`, `source_ids`, `referrer_ids`; `status` active, rejected, hired, converted (default all); `stage_name`; `job_interview_stage_ids`; `stage_ids`; `created_at`, `updated_at`, `last_activity_at` ranges | `active` reads back `in_process`. `stage_name`: one exact, case-sensitive name. `stage_ids` are application-stage ids; `job_interview_stage_ids` are stage definition ids. `needs_decision`, `rejected_at` and stage ids are fields, not filters; rejections in a window: `status: "rejected"`, wide `updated_at`, keep rows whose `rejected_at` fits. `source_id` null is "no source recorded". `referrer_id` points at a referrer, not a user, and a referrer may be an agency, a LinkedIn recruiter or a tracking link's attribution, so it alone is not an employee referral. |
| `search_applications` | same shape | `search`; `job_ids`; `stage_name` (array, exact); `stage_status` in_process, hired, rejected, paused, completed; `job_status` all, open, closed, draft | Open reqs only unless `job_status: "all"`. No `status` filter. |
| `list_candidates` | first_name, last_name, email_addresses, private | `email` (case-insensitive); `tag`; `is_private` | No name filter. A candidate is a person; applications are per job. |
| `search_candidates` | same shape | `search`; `job_id`; `status` candidates, prospects, all; `job_status`; `stage_name`; `stage_status` | Open reqs only unless `job_status: "all"`. |
| `list_job_stages` | job_id, name, sort_order, active | `job_ids` (or `job_id`); `active` | Omitting `active` includes retired stages. |
| `list_jobs` | name, status, requisition_id, is_template | `status` open, draft, closed; `requisition_id` (exact, not unique); `opened_at`, `closed_at` | No name search, no hiring team fields; skip templates. |
| `search_jobs` | same shape | `search`; `status` all, open, closed, draft; `user_id` with `user_role` any_role, hiring_manager, recruiter, coordinator, sourcer, following; `templates` (default exclude) | Every status unless `status: "open"`. `user_role` needs `user_id`. |
| `get_job` | one job | `job_id` | Returns an array; `[]` is not found or not visible. |
| `list_rejection_reasons` | name, type {id, key, name} | `include_defaults` | Built-ins need `include_defaults: true`. Keys WE_REJECTED_THEM, THEY_REJECTED_US, NONE_SPECIFIED, SECURITY_CONCERN. |
| `list_scorecards` | application_id, interviewer_id, submitter_id, interview_kit_id, interviewed_at, submitted_at, candidate_rating | `application_ids`, `interviewer_ids`, `interview_kit_ids`; `status` draft, complete; `interviewed_at`, `submitted_at` | No job filter: go through applications. `submitted_at` only on complete. No stage or interview name: join `interview_kit_id` to kits, then slots. |
| `list_users` | name, primary_email, site_admin | `primary_email`; `deactivated` | `primary_email` is exact and case-sensitive: lowercase it; aliases find nobody. No name filter; the signed-in user comes from `whoami` (below), with `list_users(ids: [ME])` for the fields it lacks. |

## Enhancement tools

| Tool | Holds | Filters | Traps |
|---|---|---|---|
| `whoami` | the signed-in user (`user.id`, `user.name`, `user.email`), the organization, the connected client and the token's `scopes` | none: it takes no arguments | A tool of the Greenhouse MCP server, not a Harvest endpoint: it has no scope key, so it sits outside the MCP Access ceiling and is listed on every connection where the server enables it. The skills take `user.id` as `ME` and the name when it carries one, and never ask for an email while it is listed; `configure` reads `first_name`, `site_admin` and the stored email with `list_users(ids: [ME])`. A connection that is no longer active answers "Your Greenhouse connection is no longer active. Reconnect Greenhouse in your AI client, then try again." (it begins with neither "Permission denied." nor a revoked-token text, so no rule in the block matches it); when the server cannot confirm the identity it answers "Couldn't confirm your Greenhouse identity right now. Try again in a moment." |
| `list_interviews` | application_id, job_id, job_interview_id, starts_at, ends_at, all_day_start_on, all_day_end_on, status, organizer_id, availability_received_at | `application_ids`, `job_ids`, `job_interview_ids`, `organizer_ids`, `ids`; `status`; `starts_at`, `ends_at`, `all_day_start_on` ranges | A `starts_at` range drops null starts: unscheduled interviews and all-day events (read those by `all_day_start_on`). Status to_be_scheduled, scheduled, awaiting_feedback, complete, skipped, collect_feedback; take-homes to_be_sent, sent, received. Sending a take-home sets `starts_at` to the send time. A stage move deletes the old stage's interviews still to_be_scheduled, collect_feedback or to_be_sent. |
| `list_interviewers` | interview_id, user_id, scorecard_id, response_status, email | `interview_ids`, `user_ids`, `scorecard_ids`; `response_status` needs_action, declined, tentative, accepted | One row per panel member per interview: join `interview_id` to the interview's `id`, `user_id` to `list_users`, `scorecard_id` to the scorecard's `id` (when null, match by application, interviewer and date). Carries the member's `email`: never print it. |
| `list_application_stages` | application_id, job_interview_stage_id, entered_at, exited_at, days_in_stage | `application_ids`, `job_interview_stage_ids`; `current` | The only real time in stage, in calendar days; retired stages' rows are gone. Every plan stage has a row from the day the application was created; `entered_at` is null until it enters that stage, so "reached" = a non-null `entered_at`. |
| `list_offers` | application_id, candidate_id, job_id, status, version, sent_on, starts_on, resolved_at, custom_fields | `application_ids`, `job_ids`, `candidate_ids`; `status` Created, Accepted, Rejected, Deprecated; `current_only` | `[]` also means no offer permission on the req. Compensation sits in `custom_fields`. |
| `list_openings` | job_id, open, target_start_on, application_id | `job_ids`; `open` | `application_id` is set when a hire fills it. |
| `list_notes` | candidate_id, application_id, type, visibility | `candidate_ids`, `application_ids`; `type` (array); `visibility` | `visibility` reads admin_only_visible, privately_visible, publicly_visible. `type` rejects an empty array. |
| `list_job_owners`, `list_job_hiring_managers` | job_id, user_id; owners add type and responsible | `job_ids`, `user_ids`; owners `type` sourcer, recruiter, coordinator | One row per user per role. |
| `list_scorecard_candidate_attributes` | scorecard_id, job_candidate_attribute_id, candidate_attribute_rating | `scorecard_ids` | Ratings definitely_not, no, yes, strong_yes, mixed, no_decision. |
| `list_ai_opt_out_statuses` | job_id, candidate_ids, opted_out | `job_ids`, `candidate_ids`; `opted_out` | Per job, not per candidate. No row is no decision, never consent. |
| `list_sources` | name, type {id, name} (the sourcing strategy) | `ids` | No name filter: join from `applications.source_id`, 50 ids per call. Referrals are sources whose strategy name is Referral. A source can be named after a person. |
| `list_interview_kits` | job_id, job_interview_id, exercises | `job_ids`, `job_interview_ids` | One kit per slot. |
| `list_job_interviews` | job_id, job_interview_stage_id, name, duration, scheduling_type | `job_ids`, `job_interview_stage_ids`; `active`; `scheduling_type` none, needs_scheduling, take_home_test, offer | Its `id` is `job_interview_id` on interviews and kits. `duration` is planned minutes. Omit `active` to keep retired slots, which older interviews still point to. |
| `list_scorecard_questions` | interview_kit_id, question, answer_type, required | `interview_kit_ids`; `active` | Removed questions return unless `active: true`. |

| Write | Required | Also takes | Traps |
|---|---|---|---|
| `add_candidate_note` | `body`, `visibility` admin_only, private, public | `candidate_id`, `application_id`, `user_id` | `note_type` is always NOTE and rejected as an argument. Harvest needs `candidate_id`. |
| `move_application` | `application_id`, `from_stage_id` | `to_stage_id` or `to_job_id` | Stage ids are `list_job_stages` ids, never `application.stage_id`; a stale `from_stage_id` is a 422. Runs the destination stage's rules, which can email the candidate or the team and send forms, tests or scheduling requests (never tasks). Prospect and hired applications cannot be moved; a move to the current stage changes nothing. Returns 204, so read back. |
| `create_scorecard` | `interview_kit_id`, `interviewer_id`, `interviewed_at`, `application_id`, `submitter_id` | `status` draft, complete; `candidate_rating`; `notes` | Kit must belong to the application's job. `complete` stamps `submitted_at`. |

## Record semantics

- Rejected keeps its stage (`stage_id`, `job_interview_stage_id`, `stage_name`); hired has them null (count it as having reached the last stage); prospects have no stage. There is no hire timestamp.
- `last_activity_at` is the candidate's latest activity, copied to each of their applications; not time in stage.
- `needs_decision` is true only when every interview in the current stage is complete or skipped and the stage is not Offer; it never says whose.
- A draft scorecard exists only once an interviewer started one; `interviewed_at` defaults to then and is editable. One scorecard per interviewer per interview; `submitter_id` differs when entered on someone's behalf.
- Retired stages hold no applications; retiring one moves them to the previous stage.
- Application Review first and Offer last is a convention, not guaranteed (stages get renamed and reordered): use the lowest and highest `sort_order`.
- Private candidates are omitted from reads, never masked. A 404 on a member action means not in the org or not readable.

## Permissions

A token's scopes are the intersection of the org ceiling (Configure > Dev Center > MCP Access; default: the seven read scopes of the eleven tools above), what the user's own permissions can grant, and what they ticked at consent. Saving a changed ceiling invalidates every MCP token in the org. Clients may keep the old tool list for a few minutes: use the rules block's wording for the delay.

A missing tool means the token lacks the scope; a listed one can still 403. Every denial begins "Permission denied."; on the current server the next sentence says which: "This connection is missing the scope(s)" (reconnect and tick it) or "Your Greenhouse account doesn't have permission" (the user's role on that req; reconnecting cannot help). An earlier wording of the same error is "Your token is missing the scope(s) required by this tool".

The server does not expose deletes. The skills preview every write themselves and pass only arguments the tool schema lists. Move, reject, unreject and hire return 204 with no body: read the record back.
