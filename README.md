# Greenhouse plugin

The Greenhouse plugin gives Greenhouse recruiters skills on top of the hosted Greenhouse MCP connector, in any AI assistant that supports plugins and MCP connectors: a desktop or web app, or a command-line client. The plugin lives in [`greenhouse/`](greenhouse/); start with its [README](greenhouse/README.md).

## Install

**Desktop or web app.** Install from the plugin directory (**Customize > Plugins > Discover**) if it is listed there, or open **Customize > Plugins > Add > Add marketplace** and enter `grnhse/greenhouse-skills`. Connect Greenhouse in the plugin's **Connectors** tab, then run `/greenhouse:configure`. A command-line client signed in to the same account may pick the plugin up as a synced plugin at its next session start.

**Command-line client** that supports plugin marketplaces, if the plugin is not already synced:

```
/plugin marketplace add grnhse/greenhouse-skills
/plugin install greenhouse@greenhouse-skills
/mcp                      (choose plugin:greenhouse:greenhouse and sign in)
/greenhouse:configure
```

## Before you install

- Greenhouse MCP is in **open beta** on Greenhouse Recruiting Core, Plus and Pro. Greenhouse enables it for your organization (a Site Admin cannot), and a Site Admin sets the scope ceiling under **Configure > Dev Center > MCP Access**. For anyone who is not a Site Admin to connect, your Greenhouse account team also enables non-admin MCP authorization. Admin and user steps are in [greenhouse/SETUP.md](greenhouse/SETUP.md).
- Reads follow your own Greenhouse permissions. The skills write to Greenhouse only a candidate note, a stage move or a draft scorecard. An interviewer nudge or a hiring-manager message can go out only through a chat or email tool you connected yourself. The skills are written to preview each write or message and make it only after you reply "yes", one per "yes". Asked to post somewhere shared, the daily brief and the interview week send only a snapshot of counts with no candidate names, again on your "yes". See [greenhouse/DATA_HANDLING.md](greenhouse/DATA_HANDLING.md).
- Setup, the daily brief, the interview week and the pipeline and source reviews open as a page when your app can show a file or an artifact: a bundled Python script fills a fixed template where the app can run it, and the assistant writes a plain still page where it cannot, with a short reply in chat. Say "in chat" to skip it. Any other chart, diagram, document or deck is made when you ask, in Greenhouse's visual style from the `brand` skill. Everything the plugin runs, sends and fetches is listed in [the plugin README](greenhouse/README.md#what-the-plugin-runs-sends-and-fetches).

## In this repo

| Path | What |
|---|---|
| `greenhouse/` | The plugin: manifest, `.mcp.json`, skills and their page builders, README, SETUP, DATA_HANDLING, LICENSE, NOTICE |
| `docs/` | Source of the shared rules block, failure states, skill conventions, data-model reference, rendered samples |
| `.github/` | Lint, rules injection, tool catalog, CI |

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md) (external pull requests are not accepted). Support: [Greenhouse Support](https://support.greenhouse.io). Security: [SECURITY.md](SECURITY.md). Changes: [CHANGELOG.md](CHANGELOG.md).

© 2026 Greenhouse Software, Inc. Proprietary, for Greenhouse customer use only; see [LICENSE](LICENSE) and [NOTICE](NOTICE).
