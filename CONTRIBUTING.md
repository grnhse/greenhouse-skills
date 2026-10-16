# Contributing

## During the open beta

We are not accepting external pull requests while Greenhouse MCP is in open beta. The skills are proprietary and licensed for Greenhouse customer use only (see [LICENSE](LICENSE)). Bug reports and feature requests go through your Greenhouse account team or [Greenhouse Support](https://support.greenhouse.io). Security issues: see [SECURITY.md](SECURITY.md).

## Maintainers

Read [docs/SKILL-CONVENTIONS.md](docs/SKILL-CONVENTIONS.md) first. It defines the frontmatter, the description formula, the body order, the call budgets and the hard rules the linter enforces.

### Rules block

The block between `<!-- greenhouse-rules v8 -->` and `<!-- /greenhouse-rules -->` in every data skill's SKILL.md is a copy of `docs/shared-rules.md`. Edit the source, then run the injector. CI fails on any drift. The style skill (`brand`, `metadata: kind: style`) carries no block and the injector skips it.

```
python3 .github/scripts/inject_shared_rules.py          # rewrite every data skill
python3 .github/scripts/inject_shared_rules.py --check  # CI mode
```

### Before you open a PR

```
python3 .github/scripts/inject_shared_rules.py --check
python3 .github/scripts/lint_skills.py
claude plugin validate --strict ./greenhouse
claude plugin validate --strict .
```

All of them must pass; the last two run the plugin CLI, at the version pinned in `.github/workflows/validate.yml`. The linter checks frontmatter keys, that the description is one double-quoted line of 120-1024 characters (aim for 300-900), the kebab-case name, the 200-line and 32 KiB limits, that every tool a skill mentions (bare or as a call shape) is in `.github/scripts/tool_catalog.json` and in that skill's `metadata` (`core`, `enhancement`, `write`), that forbidden tools (including any `bulk_` or `delete_` tool), `mcp__` prefixes, plugin-root variables in paths, `!` dynamic context and `references/` paths are absent, that `confirm` is never passed to a write, that `/greenhouse:<skill>` references resolve, that a style skill carries no rules block and names no tool, that a skill folder holds only `SKILL.md` and an optional `page/` folder with exactly its four files, that `page.html` and `build_page.py` are byte-identical across skills, that the plugin folder holds no other code, no hooks, junk files, symlinks or Windows-invalid names, no tracked file that `.gitignore` matches, no more than 512 files a commit would hold and no file other than an image or font over 256 KiB, and that `plugin.json`'s version equals the first CHANGELOG heading.

Manual checks: `claude --plugin-dir ./greenhouse` in a command-line client that supports plugin directories, and a zip of the committed plugin folder (`git archive --format=zip -o greenhouse.zip HEAD:greenhouse`) uploaded through **Customize > Plugins > Add > Upload plugin** in the desktop or web app. Don't zip the working folder: it also holds gitignored files, the eval suite among them.

### Evals

The eval suite lives in the gitignored `greenhouse/evals/` folder on the maintainer's machine and is maintained outside the repository. The gate is `python3 .github/scripts/inject_shared_rules.py --check && python3 .github/scripts/lint_skills.py && claude plugin validate --strict ./greenhouse && claude plugin validate --strict .`.

### Adding or changing a skill

- New data skill: directory and SKILL.md, `metadata` listing every tool by role, a row in `configure`'s capability table, a row in `greenhouse/README.md`, a sample in `docs/samples/` rendered on a fictional organization, a CHANGELOG entry, and eval cases for its trigger and its degradation on the default tools in the maintainer's suite (Evals, above). The linter fails on a `/greenhouse:` reference to a skill that does not exist, so land the skill before the references to it.
- Page folder: `page/` holds exactly `PAGE.md`, `page.html`, `build_page.py` and `example.json`. `page.html` and `build_page.py` are byte-identical in every skill: edit the `daily-brief` copy, then copy it into every other `page/` folder (`for d in greenhouse/skills/*/page; do [ "$d" = greenhouse/skills/daily-brief/page ] || cp greenhouse/skills/daily-brief/page/build_page.py greenhouse/skills/daily-brief/page/page.html "$d"/; done`). `PAGE.md` gives the page's file name and the run line, which is one shell call with the page data on standard input as a heredoc and the file's path on `--out`: `python3 "<this skill's folder>/page/build_page.py" --out "<outputs folder>/<the file name this file gives>" <<'GH_PAGE_DATA'`; no data file is written (see also [docs/SKILL-CONVENTIONS.md](docs/SKILL-CONVENTIONS.md#pages)). `PAGE.md` also carries the "Without Python" frame the assistant copies when the builder cannot run. The SKILL.md points to it with a `Page:` line (``Page: read `page/PAGE.md` in this skill's folder before rendering and follow it.``) and lists its fallback. `example.json` is fictional and must build.
- Style skill: there is one, `brand`; change it rather than adding another. It carries `metadata: kind: style`, no rules block and no Greenhouse tool name.
- New tool use: the tool must be in `.github/scripts/tool_catalog.json`. Add it by hand, with the Greenhouse MCP server's tool list as the source: copy the name and the read-only annotation as the server declares them, and keep the list sorted. There is no generator script.
- Sanctioned writes: the three Greenhouse writes in the linter's set, and a message through the user's connected chat or email tool, gated in the skill that sends it rather than in the rules block: `daily-brief` step 8, `interview-week` step 9 and `pipeline-review` step 5 each show the whole message and its one named recipient, end with a line asking for a yes, send one message per explicit yes, to that person and never a channel or group; `daily-brief` step 7 and `interview-week` step 8 may send a counts-only snapshot (no candidate names) to a shared destination, one send on an explicit yes after showing the exact text and destination. The linter checks only the Greenhouse set, so review each message gate by hand.
- New write: needs maintainer approval in the pull request and, for a Greenhouse tool, a change to the sanctioned set in the linter. Writes stay preview-first, one record per confirmation, read back after, never `confirm`.
- Every data skill must be useful on the eleven default Harvest tools and degrade per the rules block for everything else; no shipped skill requires a non-default tool. `whoami` is a Greenhouse MCP server tool with no scope, listed whenever the server enables it, and a skill must also run without it. Test it with a connection that has only the defaults.

### Commits and versions

- Conventional Commits, scoped to the skill when there is one: `fix(daily-brief): shorten the footnote`.
- `greenhouse/.claude-plugin/plugin.json` `version` equals the first heading in `CHANGELOG.md`; bump both in the same commit and tag `vX.Y.Z` on main.
- The plugin CLI version pinned in `.github/workflows/validate.yml` is bumped to the current release in the same PR as each version bump, and whenever a `plugin validate` change is announced.
- Patch: wording, degradation and documentation fixes. Minor: a new skill or a new write. Major: removing a skill or changing what an existing write does.

### Never commit

Customer or prospect names, real candidate or employee data (including pages built from it), internal links, people's contact details or credentials. Treat the repository as public: the plugin is distributed from it, and the license does not make its history private.
