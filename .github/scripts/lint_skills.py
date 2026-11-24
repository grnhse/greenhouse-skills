#!/usr/bin/env python3
"""Content checks for the greenhouse plugin that `claude plugin validate` does not make.

Run from anywhere: lint_skills.py. Exit 1 on any failure.
"""
import json
import pathlib
import re
import struct
import subprocess
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "greenhouse"
SKILLS = PLUGIN / "skills"
CATALOG = json.loads((ROOT / ".github" / "scripts" / "tool_catalog.json").read_text())
REGISTERED = {t["name"] for t in CATALOG["tools"]}
WRITE_TOOLS = {t["name"] for t in CATALOG["tools"] if t["read_only"] is False}
HOST_TOOLS = {"AskUserQuestion", "ToolSearch", "search_mcp_registry", "suggest_connectors"}
ALLOWED_KEYS = {"name", "description", "allowed-tools", "argument-hint", "compatibility",
                "disable-model-invocation", "license", "metadata", "model"}
FORBIDDEN = {"list_eeoc", "list_attachments", "reject_application", "hire_application", "merge_candidate",
             "anonymize_candidate", "unreject_application", "create_job_note"}
FORBIDDEN_PREFIXES = ("bulk_", "delete_", "list_demographic")
ALLOWED_WRITES = {"add_candidate_note", "move_application", "create_scorecard"}
KINDS = {"data", "style"}
VERBS = {t["name"].split("_", 1)[0] for t in CATALOG["tools"]} | {"bulk", "delete", "list"}
TOOL_RE = re.compile(r"`((?:%s)_[a-z_]+)(?:\(|`)" % "|".join(sorted(VERBS)))
MAX_LINES = 200
MAX_BYTES = 32 * 1024
DESC_MIN, DESC_MAX = 120, 1024
RULES_START, RULES_END = "<!-- greenhouse-rules v8 -->", "<!-- /greenhouse-rules -->"
MCP_URL = "https://mcp.greenhouse.io/mcp"
PRIVACY_URL = "https://www.greenhouse.com/ai-addendum"
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "__MACOSX"}
WINDOWS_BAD = re.compile(r'[<>:"|?*\x00-\x1f]|[. ]$|^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$', re.I)
CODE_SUFFIXES = {".sh", ".py", ".js", ".ts", ".rb", ".mjs", ".cjs"}
SIZE_EXEMPT_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".woff", ".woff2", ".ttf", ".otf"}
PAGE_FILES = {"PAGE.md", "page.html", "build_page.py", "example.json"}
SHARED_PAGE_FILES = ("page.html", "build_page.py")
MAX_PLUGIN_FILES = 512
MAX_FILE_BYTES = 256 * 1024
ROLES = ("core", "required", "enhancement", "write")
OPENAI_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
OPENAI_MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
OPENAI_PLUGIN_KEYS = {"$schema", "name", "version", "description", "author", "homepage", "repository",
                      "license", "keywords", "extensions"}
OPENAI_TEXT_LIMITS = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}
OPENAI_ONE_LINE_KEYS = ("displayName", "shortDescription", "developerName")
LINE_BREAK = re.compile("[\n\r\u2028\u2029]")
OPENAI_URL_KEYS = ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL")
OPENAI_ICON_KEYS = ("composerIcon", "logo")
OPENAI_CATEGORIES = {"Productivity", "Creativity", "Developer Tools", "Business & Operations", "Data & Analytics",
                     "Communication", "Education & Research", "Security", "Finance", "Healthcare", "Travel",
                     "Entertainment", "Other"}
OPENAI_MCP_KEYS = {"$schema", "mcpServers"}
OPENAI_SERVER_KEYS = {"type", "url", "extensions"}
OPENAI_SERVER_EXTENSION_KEYS = {"com.openai"}
OPENAI_SERVER_VENDOR_KEYS = {"auth"}
CLAUDE_SERVER_KEYS = {"type", "url"}
OPENAI_AUTH = {"type": "oauth", "client": {"mode": "cimd"}}
MANIFEST_SYNC = (("name", "name"), ("version", "version"), ("description", "description"), ("author", "author"),
                 ("homepage", "homepage"), ("repository", "repository"), ("license", "license"),
                 ("keywords", "keywords"), ("displayName", "interface.displayName"),
                 ("homepage", "interface.websiteURL"), ("supportUrl", "interface.supportURL"),
                 ("privacyPolicyUrl", "interface.privacyPolicyURL"),
                 ("termsOfServiceUrl", "interface.termsOfServiceURL"))
CREDENTIAL_KEYS = {"headers", "env", "clientid", "client_id", "clientsecret", "client_secret", "apikey", "api_key",
                   "token", "access_token", "authorization"}

errors = []


def fail(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def parse_frontmatter(text, path):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail(path, "missing YAML frontmatter")
        return {}
    fm = {}
    section = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        top = re.match(r"^([A-Za-z-]+):\s*(.*)$", line)
        if top:
            key, value = top.groups()
            fm[key] = value.strip()
            section = key
            if key == "description" and (value.strip() in {">", ">-", "|", "|-"}
                                         or (value.strip()[:1] in "\"'" and value.strip()[-1] != value.strip()[0])):
                fail(path, "description must be one double-quoted line")
            continue
        nested = re.match(r"^\s+([a-z_]+):\s*(.*)$", line)
        if nested and section == "metadata":
            key, value = nested.groups()
            fm.setdefault("metadata", {})
            if isinstance(fm["metadata"], str):
                fm["metadata"] = {}
            if value.startswith("["):
                fm["metadata"][key] = [v.strip() for v in value.strip("[]").split(",") if v.strip()]
            else:
                fm["metadata"][key] = value
            continue
        if section == "description":
            fm["description"] = (fm["description"] + " " + line.strip()).strip()
            continue
        fail(path, f"unparsed frontmatter line: {line!r}")
    return fm


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].replace('\\"', '"')
    return value


def check_skill(skill_dir):
    path = skill_dir / "SKILL.md"
    if not path.exists():
        fail(skill_dir, "SKILL.md missing")
        return
    text = path.read_text()
    lines = text.splitlines()
    if len(lines) > MAX_LINES:
        fail(path, f"{len(lines)} lines (max {MAX_LINES})")
    if len(text.encode()) > MAX_BYTES:
        fail(path, f"{len(text.encode())} bytes (max {MAX_BYTES})")
    fm = parse_frontmatter(text, path)
    unknown = set(fm) - ALLOWED_KEYS
    if unknown:
        fail(path, f"unknown frontmatter keys: {sorted(unknown)}")
    name = unquote(fm.get("name", ""))
    if name != skill_dir.name:
        fail(path, f"name {name!r} does not match directory {skill_dir.name!r}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail(path, "name must be kebab-case")
    raw_desc = fm.get("description", "")
    if not (raw_desc.startswith('"') and raw_desc.endswith('"')):
        fail(path, "description must be one double-quoted line")
    desc = unquote(raw_desc)
    if not DESC_MIN <= len(desc) <= DESC_MAX:
        fail(path, f"description is {len(desc)} chars (want {DESC_MIN}-{DESC_MAX})")
    if "<" in desc or ">" in desc:
        fail(path, "description contains angle brackets")
    if "Use " not in desc and "Use:" not in desc:
        fail(path, "description lacks a 'Use ...' trigger sentence")
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    kind = meta.get("kind", "data")
    if kind not in KINDS:
        fail(path, f"metadata.kind {kind!r} is not one of {sorted(KINDS)}")
    if kind == "style":
        if RULES_START in text or RULES_END in text:
            fail(path, "style skill must not carry the shared rules block")
        body = text.split("\n---\n", 1)[-1]
    else:
        if RULES_START not in text or RULES_END not in text:
            fail(path, "shared rules markers missing")
        body = text.split(RULES_END, 1)[-1]
    if "mcp__" in body or "mcp__" in desc:
        fail(path, "fully qualified mcp__ tool name in skill body")
    if re.search(r"\$\{CLAUDE_PLUGIN_ROOT\}|^\s*!`|\breferences/", body, re.M):
        fail(path, "scripts, dynamic context or sibling-file paths are not allowed")
    declared = set()
    for role in ROLES:
        declared.update(meta.get(role, []) if isinstance(meta.get(role), list) else [])
    if kind == "style" and declared:
        fail(path, "style skill must not declare Greenhouse tools")
    if kind == "data" and not declared and skill_dir.name != "configure":
        fail(path, "metadata.tools.core/enhancement/write not declared")
    for tool in declared:
        if tool not in REGISTERED and tool not in HOST_TOOLS:
            fail(path, f"declared tool {tool!r} is not a registered Greenhouse tool")
    for tool in set(meta.get("write", []) or []) - ALLOWED_WRITES:
        fail(path, f"write tool {tool!r} is outside the sanctioned set {sorted(ALLOWED_WRITES)}")
    mentioned = set(TOOL_RE.findall(body)) - HOST_TOOLS
    if kind == "style" and mentioned:
        fail(path, f"style skill names Greenhouse tools: {sorted(mentioned)}")
    for tool in mentioned:
        if tool in FORBIDDEN or tool.startswith(FORBIDDEN_PREFIXES):
            fail(path, f"forbidden tool mentioned: {tool}")
        elif tool not in REGISTERED:
            fail(path, f"unknown Greenhouse tool mentioned: {tool}")
        elif tool not in declared and skill_dir.name != "configure":
            fail(path, f"tool {tool} used in body but not declared in metadata.tools")
    for tool in mentioned & WRITE_TOOLS:
        if tool not in ALLOWED_WRITES:
            fail(path, f"write tool {tool} is not sanctioned")
    for m in re.finditer(r"(add_candidate_note|move_application|create_scorecard)\([^)]*\bconfirm\b", body):
        fail(path, f"`confirm` passed to a write: {m.group(0)[:60]}")
    check_skill_files(skill_dir, body, kind)
    for ref in set(re.findall(r"/greenhouse:([a-z-]+)", body)):
        if not (SKILLS / ref).is_dir():
            fail(path, f"dangling skill reference /greenhouse:{ref}")


def check_skill_files(skill_dir, body, kind):
    for p in skill_dir.iterdir():
        if p.name == "SKILL.md":
            continue
        if p.name != "page" or not p.is_dir():
            fail(p, "a skill folder holds only SKILL.md and page/")
            continue
        present = {f.name for f in p.iterdir()}
        for name in sorted(present - PAGE_FILES):
            fail(p / name, f"page/ holds only {sorted(PAGE_FILES)}")
        for name in sorted(PAGE_FILES - present):
            fail(p, f"page/{name} missing")
        if "page/PAGE.md" not in body:
            fail(skill_dir / "SKILL.md", "has a page/ folder but never points to page/PAGE.md")
    if kind == "data" and "page/PAGE.md" in body and not (skill_dir / "page" / "PAGE.md").exists():
        fail(skill_dir / "SKILL.md", "points to page/PAGE.md, which does not exist")


def check_shared_page_files():
    for name in SHARED_PAGE_FILES:
        copies = {p.read_bytes() for p in SKILLS.glob(f"*/page/{name}")}
        if len(copies) > 1:
            fail(SKILLS, f"page/{name} differs between skills; every copy must be byte-identical")


def is_page_builder(p):
    return p.name == "build_page.py" and p.parent.name == "page" and p.parent.parent.parent == SKILLS


def git_files(*flags):
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", *flags, "--exclude-standard", "--", str(PLUGIN)],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    return {ROOT / f for f in out}


def plugin_files():
    """Plugin-folder files a commit would hold, and the tracked files that .gitignore matches."""
    try:
        tracked_ignored = git_files("-ci")
        files = git_files("-co")
    except (OSError, subprocess.CalledProcessError):
        tracked_ignored, files = set(), set(PLUGIN.rglob("*"))
    return sorted(p for p in files if p.is_file() and "results" not in p.parts), sorted(tracked_ignored)


def readme_word_count():
    text = (PLUGIN / "README.md").read_text() if (PLUGIN / "README.md").exists() else ""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return len(text.split())


def check_icon(path):
    if not path.exists():
        fail(path, "missing; the directory reads the listing icon from here")
        return
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        fail(path, "must be a PNG")
        return
    width, height = struct.unpack(">II", head[16:24])
    if width != height or not 512 <= width <= 2048:
        fail(path, f"{width}x{height}; must be square, 512 to 2048 px")
    if path.stat().st_size >= 2 * 1024 * 1024:
        fail(path, "must be under 2 MB")


def dig(data, *keys):
    for key in keys:
        data = data.get(key) if isinstance(data, dict) else None
    return data


def check_keys(path, data, allowed, label):
    unknown = set(data) - allowed if isinstance(data, dict) else set()
    if unknown:
        fail(path, f"unknown {label} keys: {sorted(unknown)}")


def normalize_prompt(text):
    return " ".join(unicodedata.normalize("NFKC", text).split())


def check_no_credentials(path, data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower() in CREDENTIAL_KEYS:
                fail(path, f"{key!r} key; MCP configs must not carry credentials, client IDs or headers")
            check_no_credentials(path, value)
    elif isinstance(data, list):
        for value in data:
            check_no_credentials(path, value)


def check_openai_interface(path, iface):
    for key, limit in OPENAI_TEXT_LIMITS.items():
        value = iface.get(key)
        if not isinstance(value, str) or not value:
            fail(path, f"interface.{key} missing")
        elif len(value) > limit:
            fail(path, f"interface.{key} is {len(value)} chars (max {limit})")
    for key in OPENAI_ONE_LINE_KEYS:
        if LINE_BREAK.search(str(iface.get(key, ""))):
            fail(path, f"interface.{key} must be one line")
    if re.search(r"plugin|mcp", str(iface.get("displayName", "")), re.I):
        fail(path, "interface.displayName must not contain 'plugin' or 'MCP'")
    if iface.get("category") not in OPENAI_CATEGORIES:
        fail(path, f"interface.category must be one of {sorted(OPENAI_CATEGORIES)}")
    for key in OPENAI_URL_KEYS:
        value = str(iface.get(key, ""))
        if not value.startswith("https://") or len(value) > 1024:
            fail(path, f"interface.{key} must be an https URL of at most 1024 chars")
    for key in OPENAI_ICON_KEYS:
        value = str(iface.get(key, ""))
        target = (PLUGIN / value).resolve()
        if (not value.startswith("./") or ".." in pathlib.PurePosixPath(value).parts
                or PLUGIN not in target.parents):
            fail(path, f"interface.{key} must be a ./ path without .. to a file inside greenhouse/")
        else:
            check_icon(target)
    prompts = iface.get("defaultPrompt", [])
    if (not isinstance(prompts, list) or len(prompts) > 3
            or any(not isinstance(p, str) or len(p) > 128 or LINE_BREAK.search(p) for p in prompts)
            or len({normalize_prompt(p) for p in prompts}) != len(prompts)):
        fail(path, "interface.defaultPrompt must be at most 3 unique one-line strings of at most 128 chars")


def check_openai_plugin(claude_pj):
    path = PLUGIN / "plugin.json"
    if not path.exists():
        fail(path, "missing; OpenAI reads the plugin manifest from here")
        return
    pj = json.loads(path.read_text())
    if pj.get("$schema") != OPENAI_PLUGIN_SCHEMA:
        fail(path, f"$schema must be {OPENAI_PLUGIN_SCHEMA}")
    check_keys(path, pj, OPENAI_PLUGIN_KEYS, "top-level")
    name = str(pj.get("name", ""))
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        fail(path, "name must be kebab-case, at most 64 chars")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", str(pj.get("version", ""))):
        fail(path, "version must be semver X.Y.Z")
    if len(str(pj.get("description", ""))) > 1024:
        fail(path, "description is over 1024 chars")
    iface = dig(pj, "extensions", "com.openai", "interface")
    if not isinstance(iface, dict):
        fail(path, "extensions.com.openai.interface missing")
        iface = {}
    check_openai_interface(path, iface)
    for claude_key, openai_key in MANIFEST_SYNC:
        scope, _, key = openai_key.rpartition(".")
        actual, expected = (iface if scope else pj).get(key), claude_pj.get(claude_key)
        if actual != expected:
            fail(path, f"{openai_key} is {actual!r}; must equal .claude-plugin/plugin.json {claude_key} ({expected!r})")


def check_openai_mcp():
    path = PLUGIN / "mcp.json"
    if not path.exists():
        fail(path, "missing; OpenAI reads the MCP server config from here")
        return
    mcp = json.loads(path.read_text())
    check_no_credentials(path, mcp)
    check_keys(path, mcp, OPENAI_MCP_KEYS, "top-level")
    if mcp.get("$schema") != OPENAI_MCP_SCHEMA:
        fail(path, f"$schema must be {OPENAI_MCP_SCHEMA}")
    server = dig(mcp, "mcpServers", "greenhouse")
    if list(mcp.get("mcpServers") or {}) != ["greenhouse"] or not isinstance(server, dict):
        fail(path, "expected exactly one server 'greenhouse' under mcpServers")
        return
    check_keys(path, server, OPENAI_SERVER_KEYS, "server")
    check_keys(path, server.get("extensions"), OPENAI_SERVER_EXTENSION_KEYS, "server extensions")
    check_keys(path, dig(server, "extensions", "com.openai"), OPENAI_SERVER_VENDOR_KEYS, "extensions.com.openai")
    if server.get("type") != "streamable-http":
        fail(path, "server type must be streamable-http")
    if server.get("url") != MCP_URL:
        fail(path, f"server url is {server.get('url')!r}; must be {MCP_URL}")
    if dig(server, "extensions", "com.openai", "auth") != OPENAI_AUTH:
        fail(path, f"extensions.com.openai.auth must be {json.dumps(OPENAI_AUTH)}")


def check_plugin():
    pj = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    changelog = (ROOT / "CHANGELOG.md").read_text() if (ROOT / "CHANGELOG.md").exists() else ""
    first = re.search(r"^## \[?v?([0-9]+\.[0-9]+\.[0-9]+)", changelog, re.M)
    if not first or first.group(1) != pj.get("version"):
        fail(ROOT / "CHANGELOG.md", f"first heading version must equal plugin.json version {pj.get('version')}")
    for key in ("hooks", "agents", "commands", "mcpServers", "lspServers", "outputStyles", "workflows"):
        if key in pj:
            fail(PLUGIN / ".claude-plugin" / "plugin.json", f"{key} key; the plugin ships skills and one remote .mcp.json server only")
    for key in ("homepage", "documentationUrl", "supportUrl", "termsOfServiceUrl"):
        if key in pj and not str(pj[key]).startswith("https://"):
            fail(PLUGIN / ".claude-plugin" / "plugin.json", f"{key} must be an https URL")
    # Without it the directory takes the first privacy link in the README, which is Google Fonts'.
    if pj.get("privacyPolicyUrl") != PRIVACY_URL:
        fail(PLUGIN / ".claude-plugin" / "plugin.json", f"privacyPolicyUrl must be {PRIVACY_URL}")
    check_icon(PLUGIN / ".claude-plugin" / "icon.png")
    for f in ("LICENSE",):
        if not (ROOT / f).exists() or not (PLUGIN / f).exists():
            fail(ROOT / f, "must exist at the repo root and in greenhouse/")
    if readme_word_count() < 40:
        fail(PLUGIN / "README.md", "needs at least 40 words outside code blocks")
    mcp = json.loads((PLUGIN / ".mcp.json").read_text())
    servers = mcp.get("mcpServers", mcp)
    if list(servers) != ["greenhouse"] or servers["greenhouse"].get("url") != MCP_URL:
        fail(PLUGIN / ".mcp.json", f"expected exactly one server 'greenhouse' at {MCP_URL}")
    if servers.get("greenhouse", {}).get("type") not in {"http", "sse", "ws"}:
        fail(PLUGIN / ".mcp.json", "remote server needs type http, sse or ws")
    check_keys(PLUGIN / ".mcp.json", servers.get("greenhouse"), CLAUDE_SERVER_KEYS, "server")
    check_no_credentials(PLUGIN / ".mcp.json", mcp)
    check_openai_mcp()
    check_openai_plugin(pj)
    files, tracked_ignored = plugin_files()
    if tracked_ignored:
        fail(PLUGIN, f"{len(tracked_ignored)} tracked files match .gitignore, e.g. "
                     f"{tracked_ignored[0].relative_to(ROOT)}; remove them from the index with git rm --cached")
    if len(files) > MAX_PLUGIN_FILES:
        fail(PLUGIN, f"{len(files)} files (max {MAX_PLUGIN_FILES})")
    for p in files:
        if p.suffix.lower() not in SIZE_EXEMPT_SUFFIXES and p.stat().st_size > MAX_FILE_BYTES:
            fail(p, f"{p.stat().st_size // 1024} KiB (max {MAX_FILE_BYTES // 1024} KiB for a file that is not an image or font)")
        if (p.suffix.lower() in CODE_SUFFIXES and not is_page_builder(p)) or p.name == "hooks.json":
            fail(p, "executable or hook file in the plugin")
    for p in PLUGIN.rglob("*"):
        if "evals" in p.relative_to(PLUGIN).parts:
            continue
        if p.name in JUNK_NAMES:
            fail(p, "OS junk file")
        if p.is_symlink():
            fail(p, "symlink; commit a regular file")
        if WINDOWS_BAD.search(p.name):
            fail(p, "name is not valid on Windows")
    lowered = {}
    for p in PLUGIN.rglob("*"):
        if "evals" in p.relative_to(PLUGIN).parts:
            continue
        other = lowered.setdefault(str(p).lower(), p)
        if other is not p:
            fail(p, f"name differs only by case from {other.relative_to(ROOT)}")
    for sub in ("bin", "hooks", "agents", "commands", "scripts"):
        if (PLUGIN / sub).exists():
            fail(PLUGIN / sub, "the plugin ships skills only")
    if (PLUGIN / "CLAUDE.md").exists():
        fail(PLUGIN / "CLAUDE.md", "not loaded as context; move into a skill")


def main():
    for p in sorted(SKILLS.iterdir()):
        if p.is_dir():
            check_skill(p)
        else:
            fail(p, "only skill directories belong under skills/")
    check_plugin()
    check_shared_page_files()
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print(f"lint ok: {sum(1 for p in SKILLS.iterdir() if p.is_dir())} skills")


if __name__ == "__main__":
    main()
