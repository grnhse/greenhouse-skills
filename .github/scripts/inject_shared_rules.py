#!/usr/bin/env python3
"""Copy docs/shared-rules.md into every data skill's SKILL.md between the rules markers.

Usage: inject_shared_rules.py [--check]
--check exits 1 when any skill's block differs from the source instead of rewriting it.
A skill whose frontmatter declares `kind: style` carries no rules block and is skipped.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "shared-rules.md"
SKILLS = ROOT / "greenhouse" / "skills"
START = "<!-- greenhouse-rules v8 -->"
END = "<!-- /greenhouse-rules -->"
STYLE_KIND = re.compile(r"^\s+kind:\s*style\s*$", re.M)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def splice(text, block):
    start = text.find(START)
    end = text.find(END)
    if start == -1 or end == -1 or end < start:
        return None
    end += len(END)
    return text[:start] + block.rstrip("\n") + text[end:]


def main():
    check = "--check" in sys.argv
    block = SOURCE.read_text()
    if not (block.startswith(START) and block.rstrip("\n").endswith(END)):
        sys.exit(f"{SOURCE} must start with {START} and end with {END}")
    drift = []
    broken = []
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        text = skill_md.read_text()
        if STYLE_KIND.search(frontmatter(text)):
            if START in text or END in text:
                broken.append(f"{skill_md}: style skill must not carry the rules block")
            continue
        updated = splice(text, block)
        if updated is None:
            broken.append(f"{skill_md}: rules markers missing")
            continue
        if updated != text:
            drift.append(f"{skill_md}: rules block differs from docs/shared-rules.md")
            if not check:
                skill_md.write_text(updated)
    if drift or broken:
        verb = "Drift found" if check else "Rewrote"
        print(verb + ":\n  " + "\n  ".join(drift + broken))
        sys.exit(1 if (check or broken) else 0)
    print("Rules block identical in every data skill")


if __name__ == "__main__":
    main()
