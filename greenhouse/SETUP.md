# Setup

In order: Greenhouse enables Greenhouse MCP for your organization and a Site Admin sets the scope ceiling (A); on a team or enterprise plan a workspace admin adds the connector (B); each person installs the plugin and connects with their own Greenhouse login (C, or D for a command-line client). Sandbox notes are in (E) and troubleshooting by exact error text in (F).

## A. Greenhouse Site Admin

1. **Get Greenhouse MCP enabled.** It is in open beta on Greenhouse Recruiting Core, Plus and Pro. Greenhouse enables MCP Access for your organization (a Site Admin cannot switch it on): ask your account team. Without it, Greenhouse sends the connection attempt back to the app with the error `Public OAuth clients are not enabled for this organization`.

2. **Let non-Site-Admins connect.** Recruiters are usually Job Admins, not Site Admins. Your Greenhouse account team enables non-admin MCP authorization (a Site Admin cannot), so ask them; until then a connection by anyone who is not a Site Admin fails with `Only organization administrators can authorize MCP applications.`

3. **Set the scope ceiling.** Open **Configure > Dev Center > MCP Access > Endpoints** (`https://app.greenhouse.io/configure/dev_center/mcp_scope_configuration/edit`). The page reads:

   > Users from your organization may approve MCP clients to access these API scopes. This list is a ceiling of what users can approve. Users may only approve scopes that their user or role can access.

   An organization that never saved this page gets the read-only defaults: List applications, List candidates, List job interview stages, List jobs, List rejection reasons, List scorecards, List users. The Greenhouse setup article warns: "After a Site Admin saves changes on the MCP Access page, those selections replace the defaults. Saving the page with no scopes selected removes MCP access to all Greenhouse data." Keep the seven defaults ticked and add the rows you want:

   | Add this scope | Unlocks | Kind |
   |---|---|---|
   | `harvest:interviews:list` | the calendar, what still needs scheduling and interviews awaiting feedback in `interview-week`; interviews today and tomorrow and feedback owed (`daily-brief`), next interview (`candidate-status`), rounds ahead and interviews awaiting feedback (`candidate-debrief`), interviews in the next 7 days (`pipeline-review`) | read |
   | `harvest:application_stages:list` | exact days in stage and pass-through instead of days since last activity; how far each source's applications got, from stage history, in `source-review` | read |
   | `harvest:offers:list` | offers in flight and offer state; the user also needs the private and salary data permission | read |
   | `harvest:openings:list` | open seats and target start dates in `pipeline-review` | read |
   | `harvest:notes:list` | recruiter notes, last logged email | read |
   | `harvest:job_hiring_managers:list` | the hiring manager per req in `daily-brief`; the hiring-manager message's addressee in `pipeline-review` | read |
   | `harvest:scorecard_candidate_attributes:list` | attribute-level ratings in the debrief | read |
   | `harvest:ai_opt_out_statuses:list` | AI opt-out check before a candidate is summarized in a debrief or a pipeline review; needs Talent Matching | read |
   | `harvest:sources:list` | source names and types per row in `source-review`; source names on the roster in `pipeline-review` | read |
   | `harvest:interviewers:list` | interview panels, calendar replies and scorecards not yet started in `interview-week` | read |
   | `harvest:interview_kits:list` | `scorecard-draft` can pick the interview kit | read |
   | `harvest:job_interviews:list`, `harvest:scorecard_questions:list` | interview names and planned length in `interview-week`; `scorecard-draft` names each interview and structures notes under the kit's questions | read |
   | `harvest:notes:create` | `candidate-debrief` records a decision note after the user confirms | write |
   | `harvest:applications:move` | `candidate-debrief` moves a stage after the user confirms | write |
   | `harvest:scorecards:create` | `scorecard-draft` creates a draft scorecard after the user confirms | write |

   Every skill runs on the seven defaults; a scope outside the ceiling only hides the section it feeds, and the answer's footnote names it. The `whoami` tool the skills use to find your user belongs to the MCP server, not to Harvest, so it is not on this page.

   When you save, Greenhouse asks you to confirm:

   > Saving any change will require existing MCP connections in your organization to reconnect and reauthorize.

   This is literal: the moment you save a changed scope set, every MCP connection in the organization is signed out, for every AI tool connected to it. Saving the page with no change leaves connections alone. Tell people to disconnect and reconnect Greenhouse in their AI assistant once. New tools can take up to 10 minutes to show in a conversation. Make ceiling changes outside busy hours.

4. **Clients tab.** The redirect URLs of the AI tools Greenhouse lists there are pre-approved. Add patterns here only for tools Greenhouse does not list.

5. **User permissions still apply.** The connection acts as the user, so Greenhouse applies that user's permissions on every call. Job Admins see their jobs. Offers come back empty without the "See private notes, private fields, salary info, and manage offers" permission (or its variant that adds "request approval, and approve jobs/offers"). `list_ai_opt_out_statuses` needs Talent Matching and the job-level permission. A user whose permissions do not let them look users up cannot be matched to their email; with the `whoami` tool on the connection no email match is needed. Nothing in the plugin bypasses any of this.

6. **Tokens.** Access tokens last one hour and refresh silently; a connection unused for 14 days needs a fresh sign-in. Each person can disconnect their own AI tools under **My Info > Greenhouse MCP Connections** in Greenhouse. A Site Admin has no per-user revoke: the user disconnects the tool themselves, changing the scope set on the MCP Access page signs out every MCP connection in the organization, and deactivating a user ends their access.

## B. Workspace admin (team and enterprise plans)

1. Add the Greenhouse connector for the organization at the plugin's URL, `https://mcp.greenhouse.io/mcp`. Members authenticate individually with their own Greenhouse login; there is no shared credential.
2. Set the Greenhouse plugin to **Available to install** (or **Installed by default** for the teams that recruit) in the organization's plugin settings.
3. If the workspace already has another connector entry for the same server, at `mcp.us.greenhouse.io`, it appears as a second set of tools. Keep one.

## C. End user (desktop and web app)

1. Open **Customize > Plugins** and install Greenhouse from **Discover** if the plugin directory lists it there, or use **Add > Add marketplace** with `grnhse/greenhouse-skills`.
2. Open the plugin's **Connectors** tab, click Connect on Greenhouse, and enter the email you sign in to Greenhouse with. Greenhouse sends you to the consent page of the organization your browser is signed in to; if you use more than one Greenhouse organization, sign in to the one you want first (see (E) for sandboxes).
3. On the consent page leave the data categories ticked that you want the assistant to use; the button reads "Authorize N of M permissions". If the page says `You don't have access to any resources this application can use. Contact your organization administrator if you need access.`, your organization's ceiling or your role grants nothing; see (A).
4. Back in the app, say "set me up with Greenhouse" or run `/greenhouse:configure` (type `/` in the message box and pick it). It checks the connection, finds your user, lists what your access unlocks and offers a place to start.
5. Only if a skill asks for your email (a connection without the `whoami` tool): add "My Greenhouse email is [your email]" to the standing instructions you give your assistant, so the skills already have it and need not ask each conversation.
6. Pages: setup, the daily brief, the interview week, the pipeline review and the source review open as a page whenever your app can show a file or an artifact; the debrief and candidate status build one when you ask. The page is the only file the plugin leaves, kept where the app keeps the files it shows you until you delete it; see [DATA_HANDLING.md](DATA_HANDLING.md). When the app can show neither a file nor an artifact, the same answer arrives in chat, ending "I couldn't open a page here, so it's all in chat: ask for any section."

## D. Command-line clients

These steps are for a command-line client that supports plugin marketplaces. If you installed the plugin in the desktop or web app and the client syncs plugins from the same account, it appears there at your next session start (or after `/reload-plugins`): skip the two `/plugin` lines below, run `/mcp`, choose the Greenhouse server under that plugin, and sign in. Install from the marketplace only where the client does not sync from your account; a client loads one plugin per name.

```
/plugin marketplace add grnhse/greenhouse-skills
/plugin install greenhouse@greenhouse-skills
/mcp
/greenhouse:configure
```

In `/mcp` choose `plugin:greenhouse:greenhouse` and sign in. The plugin bundles the server, so do not also add Greenhouse as a separate MCP server in the client; you would get two copies of every tool. A command-line client shows the tools with a prefix, for example `mcp__plugin_greenhouse_greenhouse__list_jobs`; the skills name them bare (`list_jobs`), and it is the same tool.

Building a page runs `python3 <skill folder>/page/build_page.py` as one shell command, with the page data passed on standard input, so the client asks your permission first unless you have already allowed it; allow that one command, not the shell in general. The page is the only file written, into the session's scratch or temporary directory, never your project; no data file is written. If you decline, or Python cannot run, the skill writes a plain still page itself, with no script and Greenhouse links only.

## E. Sandbox organizations

Greenhouse sends the consent page for whichever Greenhouse organization your browser is signed in to. To connect a sandbox, sign out of production Greenhouse in the browser first, then connect; reverse it when you switch back. The sandbox needs the same MCP Access settings as (A), and its tokens are separate from production.

## F. Troubleshooting

Match the text you see.

| You see | Cause | Fix |
|---|---|---|
| "Greenhouse isn't connected in this session." (no Greenhouse tools in the tool list) | Connector not added or not connected in this client; on a team or enterprise plan the workspace admin has not added it | Desktop and web app: connect in the plugin's Connectors tab. Command-line client: `/mcp`, `plugin:greenhouse:greenhouse`, sign in. Then re-run |
| `Public OAuth clients are not enabled for this organization` (returned to the app when you connect) | Greenhouse has not enabled MCP Access for the organization | Account team enables Greenhouse MCP (A1) |
| `Only organization administrators can authorize MCP applications.` (returned to the app when you connect) | Non-admin authorization is off | Account team enables it (A2); a Site Admin can connect meanwhile |
| `Email address is invalid or doesn't exist` (sign-in page) | Not the email on your Greenhouse user | Use the primary email on your Greenhouse user |
| `You don't have access to any resources this application can use. Contact your organization administrator if you need access.` (consent page) | The ceiling is empty or your role grants nothing | Site Admin checks the Endpoints tab (A3) and your user's permissions (A5) |
| "You're connected, but your Greenhouse consent didn't include any readable data." (`configure`) | Every data category was unticked at consent | Disconnect, reconnect, tick the categories you need |
| "Not visible with your Greenhouse MCP access: ... (needs ...)" (footnote in a result) | The scope is outside the ceiling or you unticked it | Site Admin adds the scope (A3), or reconnect and tick it; allow up to 10 minutes |
| `Permission denied. This connection is missing the scope(s) ... Reconnect and select them. If they aren't offered, ask a Greenhouse admin for that permission first.` | The token lacks that scope: unticked at consent, or outside the ceiling | Reconnect and tick it; if it is not offered, a Site Admin adds it to the ceiling first (A3) |
| `Permission denied. Your Greenhouse account doesn't have permission to perform this action. Ask a Greenhouse admin if you need access.` | Your own Greenhouse permission or role on that req (private candidates, offers, a product your organization lacks) | Ask a Greenhouse admin; reconnecting cannot help |
| `Permission denied. Your token is missing the scope(s) required by this tool: ...` (earlier wording of the same error) | Any Greenhouse 403: a missing scope, your own user permission, or a product your organization lacks | Check the ceiling, then your permissions. Reconnecting helps only when the scope is in the ceiling and grantable to you |
| `Harvest API rejected the request (HTTP 401): Unauthorized; Token has already been refreshed or revoked. Please generate a new token.` | A Site Admin changed the MCP Access scopes, or your organization's MCP access changed; existing connections were signed out | Desktop and web app: disconnect and reconnect in the Connectors tab. Command-line client: `/mcp`, clear authentication, sign in again |
| `User is unknown or disabled. Please contact the user or greenhouse administrator for assistance.` | Your Greenhouse user was deactivated | Site Admin |
| `Organization is disabled. Please contact your greenhouse administrator for assistance.` | Organization disabled | Account team |
| `Harvest API returned an error (HTTP 429). Please try again or contact support.` or `Rate limit exceeded. Try again later.` | Greenhouse rate-limits requests; the limit is shared with your organization's other custom Harvest integrations | Wait a minute and re-run; narrow the request (one req, fewer days) |
| `An unexpected error occurred. Please try again.` | An argument the tool does not accept, or a request that took too long | Re-run once; narrow the request. If one prompt always fails, send it to Greenhouse Support |
| `Invalid arguments: ...` or `Missing required arguments: ...` | Schema rejection; the skill corrects itself once | If it repeats, send the prompt to Greenhouse Support |
| `Harvest API rejected the request (HTTP 422): Unprocessable Content; This application is not currently on this stage.` | Someone moved the candidate after the preview | The skill re-reads and shows a new preview; confirm again |
| `Harvest API rejected the request (HTTP 404): Resource not found; ...` | Wrong id, or a record you cannot see | Check the record in Greenhouse |
| `Harvest API returned an error (HTTP 5xx). Please try again or contact support.` | Greenhouse-side error | Check <https://status.greenhouse.io>, retry later |
| `Tool not found: ...` | A tool the server does not expose, such as any delete tool, single or bulk | Not available by design |
| `Invalid redirect_uri: ...` (browser) | The client registered a redirect outside the allowlist | Should not happen with a pre-approved client; Site Admin checks the Clients tab and contacts Support |
| "No Greenhouse user I can see has [email] as its primary email." (`configure`) | Different primary email, or your permissions do not let you look users up | Use the primary email on your user; otherwise continue without "my reqs" scoping |
| An admin added scopes but nothing changed | Cached tool list, or the old token | Disconnect and reconnect; allow up to 10 minutes; run `/greenhouse:configure` |
| Two Greenhouse connectors, every tool twice; `configure` says "Two Greenhouse connectors are connected; I'm using this plugin's." | Another connector entry for the same server, at `mcp.us.greenhouse.io`, beside this plugin's `mcp.greenhouse.io` | Disconnect the other one; the skills keep working meanwhile |
| "I can't see interview times with your current access; ..." (`interview-week`) or "... source names are not visible with your access" (`source-review`) | The skill ran on the default scopes; `harvest:interviews:list` or `harvest:sources:list` is outside the ceiling or you unticked it | The answer is complete without that section. Site Admin adds the scope (A3), or reconnect and tick it; allow up to 10 minutes |
| "I couldn't open a page here, so it's all in chat: ask for any section." (last line of a reply) | The app can show neither a file nor an artifact | The answer above it is complete; ask for any section in chat |
| Greenhouse listed twice in `/plugin` in a command-line client, one copy not loaded | Installed in the desktop or web app and again from the marketplace in the command-line client | `/plugin uninstall greenhouse@greenhouse-skills`; keep the synced one |
