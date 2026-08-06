#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Validates the output style convention.

Usage:
  uv run tests/check-output-styles.py

Run from the repo root. No arguments.

Every skill in skills/output-styles/ ships two files: <skill-name>.md holds the
instructions as a native Claude Code output style, and SKILL.md is a thin wrapper
that points at it.

Checks:
  1. Every output-style skill has a sibling <skill-name>.md
  2. SKILL.md references that sibling by filename
  3. The native file's frontmatter has name matching the directory, keep-coding-instructions
     set, and a description matching the skill's
  4. Every native file is listed in marketplace.json "outputStyles" for both the
     "output-styles" and "everything" entries, and every listed path resolves

Exit codes:
  0  all consistent
  1  gaps found
  2  file error
"""

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
STYLES_ROOT = REPO_ROOT / "skills" / "output-styles"
MANIFEST_ENTRIES = ("output-styles", "everything")


def split_frontmatter(md: Path) -> tuple[dict, str]:
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    end = text.index("---", 3)
    return yaml.safe_load(text[3:end]) or {}, text[end + 3 :]


def path_entry(md: Path) -> str:
    return "./" + md.relative_to(REPO_ROOT).as_posix()


def main() -> int:
    if not STYLES_ROOT.is_dir():
        print(f"Output styles bucket not found: {STYLES_ROOT}", file=sys.stderr)
        return 2
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    plugins = {p["name"]: p for p in manifest.get("plugins", [])}

    issues: list[str] = []
    expected_entries: set[str] = set()

    skill_mds = sorted(STYLES_ROOT.glob("*/SKILL.md"))
    if not skill_mds:
        print(f"No skills found under {STYLES_ROOT}", file=sys.stderr)
        return 2

    for skill_md in skill_mds:
        skill_dir = skill_md.parent
        name = skill_dir.name
        native = skill_dir / f"{name}.md"

        if not native.exists():
            issues.append(f"MISSING native output style: {path_entry(native)}")
            continue

        expected_entries.add(path_entry(native))

        skill_fm, skill_body = split_frontmatter(skill_md)
        if native.name not in skill_body:
            issues.append(
                f"NO REFERENCE to {native.name} in {path_entry(skill_md)}"
            )

        native_fm = split_frontmatter(native)[0]
        if native_fm.get("name") != name:
            issues.append(
                f"BAD frontmatter name in {path_entry(native)}: "
                f"expected {name!r}, got {native_fm.get('name')!r}"
            )
        if not native_fm.get("description"):
            issues.append(f"MISSING frontmatter description in {path_entry(native)}")
        elif native_fm.get("description") != skill_fm.get("description"):
            issues.append(
                f"DRIFT in description between {path_entry(skill_md)} "
                f"and {path_entry(native)}"
            )
        if "keep-coding-instructions" not in native_fm:
            issues.append(
                f"MISSING frontmatter keep-coding-instructions in {path_entry(native)}"
            )

    for entry_name in MANIFEST_ENTRIES:
        plugin = plugins.get(entry_name)
        if plugin is None:
            issues.append(f'MISSING marketplace.json entry: "{entry_name}"')
            continue

        listed = set(plugin.get("outputStyles", []))
        for missing in sorted(expected_entries - listed):
            issues.append(
                f"MISSING from marketplace.json {entry_name}.outputStyles: {missing}"
            )
        for stale in sorted(listed):
            if not (REPO_ROOT / stale.lstrip("./")).exists():
                issues.append(
                    f"STALE entry in marketplace.json {entry_name}.outputStyles: {stale}"
                )

    if issues:
        print("Output style consistency issues found:\n")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n{len(issues)} issue(s) found.")
        return 1

    print(f"OK — {len(skill_mds)} output styles, all consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
