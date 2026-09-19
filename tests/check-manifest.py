#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Validates that marketplace.json, bucket plugin manifests and bucket READMEs are
consistent with actual skill directories.

Usage:
  uv run tests/check-manifest.py

Run from the repo root. No arguments.

Each bucket under skills/ is its own plugin: skills/<bucket>/.claude-plugin/plugin.json
is the plugin manifest, and marketplace.json points an entry at ./skills/<bucket>.

Checks:
  1. Every bucket holding at least one skill has a plugin.json declaring
     "skills": ["./"], and a name, version and description (empty buckets are
     skipped, and archived/ is never a plugin)
  2. Every bucket has a marketplace.json entry whose source is ./skills/<bucket> and
     whose name matches the plugin.json name
  3. Every marketplace.json entry resolves to a bucket that exists
  4. Every non-personal, non-archived SKILL.md has an entry in its bucket README.md

Exit codes:
  0  all consistent
  1  gaps found
  2  file error
"""

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
SKILLS_ROOT = REPO_ROOT / "skills"
PERSONAL_BUCKET = "personal"
ARCHIVED_BUCKET = "archived"


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"Manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries_by_source = {p.get("source"): p for p in manifest.get("plugins", [])}

    buckets = sorted(
        d
        for d in SKILLS_ROOT.iterdir()
        if d.is_dir() and d.name != ARCHIVED_BUCKET and any(d.rglob("SKILL.md"))
    )

    archived = SKILLS_ROOT / ARCHIVED_BUCKET
    if (archived / ".claude-plugin" / "plugin.json").exists():
        issues_archived = f"ARCHIVED bucket must not be a plugin: {archived}/.claude-plugin"
    else:
        issues_archived = None
    issues: list[str] = []

    for bucket in buckets:
        source = f"./skills/{bucket.name}"
        plugin_json = bucket / ".claude-plugin" / "plugin.json"

        if not plugin_json.exists():
            issues.append(f"MISSING plugin manifest: {source}/.claude-plugin/plugin.json")
            plugin = {}
        else:
            plugin = json.loads(plugin_json.read_text(encoding="utf-8"))
            if plugin.get("skills") != ["./"]:
                issues.append(
                    f'BAD skills field in {source}/.claude-plugin/plugin.json: '
                    f'expected ["./"], got {plugin.get("skills")!r}'
                )
            for field in ("name", "version", "description"):
                if not plugin.get(field):
                    issues.append(
                        f"MISSING {field} in {source}/.claude-plugin/plugin.json"
                    )

        entry = entries_by_source.pop(source, None)
        if entry is None:
            issues.append(f"MISSING from marketplace.json: an entry with source {source}")
        elif plugin.get("name") and entry.get("name") != plugin["name"]:
            issues.append(
                f"NAME MISMATCH for {source}: marketplace.json says "
                f"{entry.get('name')!r}, plugin.json says {plugin['name']!r}"
            )

    for source, entry in entries_by_source.items():
        issues.append(
            f"STALE entry in marketplace.json (no such bucket): "
            f"{entry.get('name')!r} → {source}"
        )

    if issues_archived:
        issues.append(issues_archived)

    skill_mds = [
        p
        for p in SKILLS_ROOT.rglob("SKILL.md")
        if PERSONAL_BUCKET not in p.parts and ARCHIVED_BUCKET not in p.parts
    ]

    for skill_md in skill_mds:
        skill_dir = skill_md.parent
        bucket_readme = SKILLS_ROOT / skill_dir.parent.name / "README.md"
        if not bucket_readme.exists():
            issues.append(f"MISSING bucket README: skills/{skill_dir.parent.name}/README.md")
        elif skill_dir.name not in bucket_readme.read_text(encoding="utf-8"):
            issues.append(f"MISSING from {skill_dir.parent.name}/README.md: {skill_dir.name}")

    if issues:
        print("Manifest consistency issues found:\n")
        for issue in sorted(set(issues)):
            print(f"  {issue}")
        print(f"\n{len(set(issues))} issue(s) found.")
        return 1

    print(f"OK — {len(buckets)} plugins, {len(skill_mds)} public skills, all consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
