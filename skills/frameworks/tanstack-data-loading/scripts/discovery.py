#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Reads and writes the tanstack-data-loading discovery cache, one entry per app root.

Usage:
  uv run scripts/discovery.py read --app <app-root> [--repo <repo-root>] [--max-age-hours 24]
  uv run scripts/discovery.py write --app <app-root> [--repo <repo-root>] < entry.json
  uv run scripts/discovery.py versions --app <app-root> [--repo <repo-root>]

--app is the app root relative to the repo root, such as apps/web or . for a
single-package repo. --repo defaults to the current directory.

The cache is <repo-root>/.draekien/tanstack-data-loading/discovery.json.

read      prints the cached entry for --app as JSON when it is fresh. An entry is
          stale when it is older than --max-age-hours or when any recorded
          @tanstack version differs from the installed one.
write     reads one entry as a JSON object on stdin, sets discoveredAt and the
          installed versions, and stores it under --app. Other apps' entries
          are kept. Creates the cache file but not .draekien/ itself.
          Fields: backend (database|service|both), pendingUi
          (route-level|per-section), verify (list of strings), versionNotes
          (list of strings).
versions  prints the installed @tanstack package versions for --app, resolved
          from node_modules, searching from the app root up to the repo root.

Exit codes:
  0  success
  2  usage error, or stdin is not a JSON object
  3  cache file unreadable or not valid JSON
  4  no cache entry for --app
  5  cache entry stale; stderr says why
  6  .draekien/ does not exist at the repo root
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PACKAGES = (
    "@tanstack/react-query",
    "@tanstack/react-router",
    "@tanstack/react-start",
    "@tanstack/react-router-ssr-query",
)
CACHE = Path(".draekien") / "tanstack-data-loading" / "discovery.json"
CHOICES = {"backend": ("database", "service", "both"), "pendingUi": ("route-level", "per-section")}
LISTS = ("verify", "versionNotes")


def fail(message: str, code: int) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(code)


def installed_versions(repo: Path, app: str) -> dict[str, str]:
    app_dir = (repo / app).resolve()
    if not app_dir.is_dir():
        fail(f"app root {app_dir} is not a directory; pass --app relative to the repo root", 2)
    search = [app_dir, *[p for p in app_dir.parents if p.is_relative_to(repo.resolve())]]
    versions: dict[str, str] = {}
    for package in PACKAGES:
        for directory in search:
            manifest = directory / "node_modules" / package / "package.json"
            if manifest.is_file():
                try:
                    versions[package] = json.loads(manifest.read_text(encoding="utf-8"))["version"]
                except (OSError, json.JSONDecodeError, KeyError) as error:
                    fail(f"cannot read the version from {manifest}: {error}; reinstall dependencies", 3)
                break
    return versions


def load_cache(path: Path) -> dict:
    if not path.is_file():
        return {"apps": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read {path}: {error}; delete the file and run discovery again", 3)
    if not isinstance(data, dict) or not isinstance(data.get("apps"), dict):
        fail(f"{path} has no 'apps' object; delete the file and run discovery again", 3)
    return data


def read(repo: Path, app: str, max_age_hours: float) -> int:
    entry = load_cache(repo / CACHE)["apps"].get(app)
    if entry is None:
        print(f"no cache entry for {app}", file=sys.stderr)
        return 4
    try:
        discovered_at = datetime.fromisoformat(entry["discoveredAt"])
        recorded = dict(entry["versions"])
    except (KeyError, TypeError, ValueError):
        print(f"stale: entry for {app} lacks a valid discoveredAt or versions", file=sys.stderr)
        return 5
    age = datetime.now(timezone.utc) - discovered_at
    if age > timedelta(hours=max_age_hours):
        print(f"stale: discovered {age.total_seconds() / 3600:.1f} hours ago", file=sys.stderr)
        return 5
    current = installed_versions(repo, app)
    changed = {
        package: f"{recorded.get(package)} -> {current.get(package)}"
        for package in set(current) | set(recorded)
        if current.get(package) != recorded.get(package)
    }
    if changed:
        print(f"stale: installed versions changed {json.dumps(changed)}", file=sys.stderr)
        return 5
    print(json.dumps(entry, indent=2))
    return 0


def write(repo: Path, app: str) -> int:
    if not (repo / ".draekien").is_dir():
        fail(f"{repo / '.draekien'} does not exist; confirm with the user, create it, then retry", 6)
    try:
        entry = json.loads(sys.stdin.read())
    except json.JSONDecodeError as error:
        fail(f"stdin is not valid JSON: {error}", 2)
    if not isinstance(entry, dict):
        fail("stdin must be one JSON object", 2)
    for field, allowed in CHOICES.items():
        if entry.get(field) not in allowed:
            fail(f"{field} must be one of {', '.join(allowed)}; got {entry.get(field)!r}", 2)
    for field in LISTS:
        value = entry.setdefault(field, [])
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            fail(f"{field} must be a list of strings; got {value!r}", 2)
    unknown = set(entry) - set(CHOICES) - set(LISTS)
    if unknown:
        fail(f"unknown fields {sorted(unknown)}; allowed: {sorted([*CHOICES, *LISTS])}", 2)
    entry["discoveredAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entry["versions"] = installed_versions(repo, app)
    path = repo / CACHE
    data = load_cache(path)
    data["apps"][app] = entry
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(entry, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("read", "write", "versions"))
    parser.add_argument("--app", required=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--max-age-hours", type=float, default=24)
    args = parser.parse_args()
    repo = Path(args.repo)
    app = Path(args.app).as_posix()
    if args.command == "read":
        return read(repo, app, args.max_age_hours)
    if args.command == "write":
        return write(repo, app)
    print(json.dumps(installed_versions(repo, app), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
