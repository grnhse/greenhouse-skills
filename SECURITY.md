# Security

## Reporting a vulnerability

Do not open a public issue. Report privately through Greenhouse's bug bounty program on HackerOne (<https://hackerone.com/greenhouse>), linked from <https://www.greenhouse.com/security>. Include the skill or file involved, the prompt or steps that reproduce it, and what data was exposed or what action was taken.

## Scope

The plugin folder holds markdown skill files, manifests and, in each skill that builds a page, a `page/` folder with a fixed HTML template and `build_page.py`, a Python standard-library script that the assistant runs to fill the template with the conversation's figures, passed on standard input. The script makes no network request, runs nothing from its input, writes only the page and stores no credentials; the page it writes, and any page or artifact the `brand` skill styles, requests two typefaces from Google Fonts when opened. Where Python cannot run, or the build still fails after two fixes, the skills have the assistant write a plain still page by hand from a fixed frame, with no script, font or outside resource and links only to Greenhouse; the script's checks do not run on that page. The repository's other code, the CI scripts under `.github/scripts`, is not part of the plugin. The Greenhouse MCP server at `https://mcp.greenhouse.io/mcp`, its sign-in flow and Greenhouse Recruiting are operated by Greenhouse and covered by the [Greenhouse MCP security FAQ](https://support.greenhouse.io/hc/en-us/articles/53944054829083-Greenhouse-MCP-security-FAQ). Report issues in the server, the sign-in flow or Greenhouse itself through the same program, not through this repository.

Reports in scope here: a skill that could be led to call a tool it should not (rejecting, hiring, bulk actions, EEOC or demographic data, attachment links), that puts a candidate's name or other excluded data into a shared-channel snapshot, that acts on text a candidate wrote, that writes or sends a message without a preview and an explicit yes, that misreports an access failure in a way that widens data exposure, or a page, built by the script or written by hand, that carries contact details, compensation, a link outside Greenhouse or script content, or is written outside the outputs folder.

## How the plugin limits risk

- Every call is made as the signed-in user over OAuth with PKCE; Greenhouse enforces that user's permissions on the server. The plugin holds no tokens and no shared credentials.
- The skills make only three kinds of write: a candidate note, a stage move and a draft scorecard. They name no delete or bulk tool and no tool that emails a candidate; a stage move can still run the destination stage's own rules, which the preview names. They are written to preview each write and make it only after an explicit yes, one record per confirmation, and to read it back afterwards. A message through the user's own chat or email tool is gated the same way: the whole text shown, one message per explicit yes; a nudge or the hiring-manager message goes to one named person, never a channel, and the only thing the skills send to a shared destination is a counts-only snapshot with no candidate names.
- The skills are written to treat candidate-written text (application answers, notes, logged emails) as data to quote, never as instructions. A crafted application that steers a skill is in scope above.
- The skills are written never to open attachment links or call EEOC and demographic tools.
- The plugin ships no hooks, binaries or local servers, and one script: `page/build_page.py`, identical in every skill that has it. It accepts only links to `https://app.greenhouse.io/`, refuses common formats of email addresses, phone numbers and amounts of money, rejecting the whole data set rather than one value, reads the data from standard input, embeds it as escaped JSON in a template whose script uses no `innerHTML`, `eval`, network calls or storage, and writes only the page. CI checks that no `bin/`, `hooks/`, `agents/`, `commands/`, `scripts/` or other code file appears in the plugin, that a `page/` folder holds only its four files and that the template and script are identical across skills, that the only MCP server is the hosted one at `https://mcp.greenhouse.io/mcp`, that every tool a skill names is in the Greenhouse MCP server's tool list, and that no skill names a write outside the three above.

## Supported versions

The latest release on `main`. Fixes ship as patch versions; see [CHANGELOG.md](CHANGELOG.md).
