#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Validates that vendored copies of shared scripts match their canonical source.

Usage:
  uv run tests/check-shared-scripts.py
  uv run tests/check-shared-scripts.py --fix

Run from the repo root.

A script that more than one skill needs lives canonically in specs/. Each consuming
skill ships a real byte-identical copy at skills/<bucket>/<skill>/scripts/<name>,
never a symlink — Git does not materialize symlinks on Windows without Developer
Mode, so a symlinked script reaches the client as a short text file holding its own
target path, and every skill that runs it fails.

A file under skills/**/scripts/ counts as a copy when its name matches a file in
specs/. No registry to maintain: copy the script in and it is checked from then on.

Checks:
  1. No symlink is tracked anywhere in the repository
  2. Every copy is byte-identical to its canonical source in specs/

--fix re-copies drifted copies from specs/. It never creates a copy that does not
already exist, and never touches the canonical source.

Exit codes:
  0  all copies in sync (or repaired with --fix)
  1  drift or symlinks found
  2  file error
"""

import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).parent.parent
SPECS_ROOT = REPO_ROOT / "specs"
SKILLS_ROOT = REPO_ROOT / "skills"


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def tracked_symlinks() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-s"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return [
        line.split("\t", 1)[1]
        for line in result.stdout.splitlines()
        if line.startswith("120000 ")
    ]


def main() -> int:
    argv = sys.argv[1:]
    if argv not in ([], ["--fix"]):
        print(f"Usage: {Path(__file__).name} [--fix]")
        return 2
    fix = argv == ["--fix"]

    canonical = {p.name: p for p in SPECS_ROOT.glob("*.py")}
    if not canonical:
        print("No shared scripts in specs/ — nothing to check.")
        return 0

    issues: list[str] = []

    try:
        symlinks = tracked_symlinks()
    except (subprocess.CalledProcessError, FileNotFoundError) as err:
        print(f"Could not read the git index: {err}")
        return 2

    for link in symlinks:
        issues.append(
            f"SYMLINK {link} is tracked as a symlink (git mode 120000) — "
            f"ship a real copy instead"
        )

    copies = sorted(
        p for p in SKILLS_ROOT.glob("*/*/scripts/*") if p.name in canonical
    )
    repaired = 0
    for copy in copies:
        source = canonical[copy.name]
        if copy.read_bytes() == source.read_bytes():
            continue
        if fix:
            copy.write_bytes(source.read_bytes())
            print(f"SYNCED {rel(copy)}")
            repaired += 1
        else:
            issues.append(f"DRIFT {rel(copy)} differs from {rel(source)}")

    if issues:
        print("Shared script issues found:\n")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n{len(issues)} issue(s) found.")
        if any(i.startswith("DRIFT") for i in issues):
            print("Run with --fix to re-copy from specs/.")
        return 1

    suffix = f", {repaired} repaired" if repaired else ""
    print(f"OK — {len(copies)} copies of {len(canonical)} shared script(s){suffix}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
