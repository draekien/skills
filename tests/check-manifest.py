#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Validates that marketplace.json and bucket READMEs are consistent with actual skill directories.

Usage:
  uv run tests/check-manifest.py

Run from the repo root. No arguments.

Checks (personal and archived buckets are excluded):
  1. Every non-personal, non-archived SKILL.md has a path entry in marketplace.json "everything.skills"
  2. Every non-personal, non-archived SKILL.md has an entry in its bucket README.md
  3. Every path in marketplace.json "everything.skills" resolves to a real SKILL.md

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
SKILLS_ROOT = REPO_ROOT / "skills"
PERSONAL_BUCKET = "personal"
ARCHIVED_BUCKET = "archived"


def parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    return yaml.safe_load(text[3:end]) or {}


def skill_path_entry(skill_dir: Path) -> str:
    rel = skill_dir.relative_to(REPO_ROOT)
    return "./" + rel.as_posix()


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    everything_plugin = next(
        (p for p in manifest.get("plugins", []) if p["name"] == "everything"), None
    )
    if not everything_plugin:
        print('No "everything" plugin entry found in marketplace.json', file=sys.stderr)
        return 2

    everything_skills = set(everything_plugin.get("skills", []))

    # Collect all SKILL.md files, excluding personal and archived buckets
    skill_mds = [
        p
        for p in SKILLS_ROOT.rglob("SKILL.md")
        if PERSONAL_BUCKET not in p.parts and ARCHIVED_BUCKET not in p.parts
    ]

    issues: list[str] = []

    # Check 1 & 2: each skill is in manifest and README
    for skill_md in skill_mds:
        skill_dir = skill_md.parent
        bucket = skill_dir.parent.name
        entry = skill_path_entry(skill_dir)

        if entry not in everything_skills:
            fm = parse_frontmatter(skill_md)
            name = fm.get("name", skill_dir.name)
            issues.append(
                f"MISSING from marketplace.json everything.skills: {entry}  (name: {name})"
            )

        bucket_readme = SKILLS_ROOT / bucket / "README.md"
        if bucket_readme.exists():
            readme_text = bucket_readme.read_text(encoding="utf-8")
            skill_name = skill_dir.name
            if skill_name not in readme_text:
                issues.append(f"MISSING from {bucket}/README.md: {skill_name}")
        else:
            issues.append(f"MISSING bucket README: skills/{bucket}/README.md")

    # Check 3: every manifest entry resolves to a real SKILL.md
    for entry in everything_skills:
        skill_md = REPO_ROOT / entry.lstrip("./") / "SKILL.md"
        if not skill_md.exists():
            issues.append(f"STALE entry in marketplace.json (no SKILL.md): {entry}")

    if issues:
        print("Manifest consistency issues found:\n")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n{len(issues)} issue(s) found.")
        return 1

    print(f"OK — {len(skill_mds)} skills, all consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
