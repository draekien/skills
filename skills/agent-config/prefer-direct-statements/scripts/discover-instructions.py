#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Finds agent instruction files without knowing which harnesses exist.

Usage:
  uv run scripts/discover-instructions.py
  uv run scripts/discover-instructions.py --scope user
  uv run scripts/discover-instructions.py --scope project --root /path/to/repo
  uv run scripts/discover-instructions.py --grep "skills?"

Flags:
  --scope user|project|all   Where to look. Default: all
  --root DIR                 Starting directory for project scope. Default: cwd
  --grep PATTERN             Case-insensitive regex; report matching lines per file

Globs for AGENTS.md, CLAUDE.md and their .local.md variants in the places agent
harnesses put them. No registry of harness names, so a harness released tomorrow is
found on the same rules as one released last year:

  user scope     ~/<name>.md, ~/.*/<name>.md, ~/.config/*/<name>.md,
                 $XDG_CONFIG_HOME/*/<name>.md, and any directory named by an
                 environment variable ending in _HOME or _CONFIG_DIR
  project scope  <name>.md and .*/<name>.md at --root, then at each ancestor up to
                 and including the git repository root

Prints one JSON object on stdout. "files" lists what exists; "config_dirs" lists
directories that look like agent configuration (they hold a skills/, commands/,
agents/, prompts/ or hooks/ subdirectory) but carry no instruction file, which are
the candidates when one has to be created. Diagnostics go to stderr.

Exit codes:
  0  scan completed (an empty "files" list is a result, not a failure)
  2  bad usage
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

NAMES = ("AGENTS.md", "CLAUDE.md", "AGENTS.local.md", "CLAUDE.local.md")
CONFIG_MARKERS = ("skills", "commands", "agents", "prompts", "hooks")
CONFIG_VIA = ("home-dotdir", "config-dir", "env-dir", "project-dotdir")
NEVER_CONFIG = (".git",)
ANCESTOR_LIMIT = 12


def instruction_files_in(directory: Path) -> list[Path]:
    return [directory / name for name in NAMES if (directory / name).is_file()]


def looks_like_config_dir(directory: Path, found_via: str) -> bool:
    if found_via not in CONFIG_VIA or directory.name in NEVER_CONFIG:
        return False
    return any((directory / marker).is_dir() for marker in CONFIG_MARKERS)


def subdirs(directory: Path, pattern: str) -> list[Path]:
    if not directory.is_dir():
        return []
    try:
        return sorted(p for p in directory.glob(pattern) if p.is_dir())
    except OSError:
        return []


def env_dirs() -> list[Path]:
    found = []
    for key, value in os.environ.items():
        if not (key.endswith("_HOME") or key.endswith("_CONFIG_DIR")):
            continue
        if not value:
            continue
        try:
            path = Path(value)
        except (OSError, ValueError):
            continue
        if path.is_dir():
            found.append(path)
    return found


def user_candidates() -> list[tuple[Path, str]]:
    home = Path.home()
    candidates: list[tuple[Path, str]] = [(home, "home")]
    candidates += [(d, "home-dotdir") for d in subdirs(home, ".*")]

    xdg = os.environ.get("XDG_CONFIG_HOME")
    config_roots = [home / ".config"]
    if xdg:
        config_roots.append(Path(xdg))
    for root in config_roots:
        candidates += [(d, "config-dir") for d in subdirs(root, "*")]

    candidates += [(d, "env-dir") for d in env_dirs()]
    return candidates


def repo_root(start: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def project_candidates(root: Path) -> list[tuple[Path, str]]:
    top = repo_root(root)
    levels = [root]
    current = root
    while top is not None and current != top and current != current.parent:
        if len(levels) >= ANCESTOR_LIMIT:
            break
        current = current.parent
        levels.append(current)

    candidates: list[tuple[Path, str]] = []
    for level in levels:
        candidates.append((level, "project"))
        candidates += [(d, "project-dotdir") for d in subdirs(level, ".*")]
    return candidates


def grep(path: Path, pattern: re.Pattern[str]) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
        return []
    return [
        {"line": number, "text": line.strip()}
        for number, line in enumerate(text.splitlines(), start=1)
        if pattern.search(line)
    ]


def scan(candidates: list[tuple[Path, str]], scope: str, pattern: re.Pattern[str] | None):
    files: list[dict] = []
    config_dirs: list[dict] = []
    seen_files: set[str] = set()
    seen_dirs: set[str] = set()

    for directory, found_via in candidates:
        resolved = str(directory.resolve()) if directory.exists() else str(directory)
        present = instruction_files_in(directory)
        for path in present:
            key = str(path.resolve())
            if key in seen_files:
                continue
            seen_files.add(key)
            entry = {
                "path": path.as_posix(),
                "scope": scope,
                "name": path.name,
                "found_via": found_via,
                "bytes": path.stat().st_size,
            }
            if pattern is not None:
                entry["matches"] = grep(path, pattern)
            files.append(entry)
        if not present and looks_like_config_dir(directory, found_via) and resolved not in seen_dirs:
            seen_dirs.add(resolved)
            config_dirs.append(
                {"path": directory.as_posix(), "scope": scope, "found_via": found_via}
            )

    return files, config_dirs


def main() -> int:
    parser = argparse.ArgumentParser(add_help=True, description=__doc__)
    parser.add_argument("--scope", choices=("user", "project", "all"), default="all")
    parser.add_argument("--root", default=".")
    parser.add_argument("--grep", default=None)
    args = parser.parse_args()

    pattern = None
    if args.grep is not None:
        try:
            pattern = re.compile(args.grep, re.IGNORECASE)
        except re.error as exc:
            print(f"error: --grep is not a valid regex: {exc}", file=sys.stderr)
            return 2

    root = Path(args.root).resolve()
    if args.scope in ("project", "all") and not root.is_dir():
        print(f"error: --root is not a directory: {root}", file=sys.stderr)
        return 2

    files: list[dict] = []
    config_dirs: list[dict] = []

    if args.scope in ("user", "all"):
        found, dirs = scan(user_candidates(), "user", pattern)
        files += found
        config_dirs += dirs

    if args.scope in ("project", "all"):
        found, dirs = scan(project_candidates(root), "project", pattern)
        files += found
        config_dirs += dirs

    json.dump(
        {"scope": args.scope, "root": root.as_posix(), "files": files, "config_dirs": config_dirs},
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
