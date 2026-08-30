#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Classifies every local branch by whether its work is provably in the base branch.

Usage:
  uv run scripts/classify.py [--base BRANCH] [--json]

Verdicts:
  ancestor     every commit is already in the base branch — safe to delete
  pr-merged    a merged pull request carried the work in — safe to delete
  pr-open      an open pull request still needs the branch — keep
  pr-closed    a pull request was closed without merging — keep
  unresolved   no evidence either way — keep, and decide by hand

Output is TSV on stdout: branch, sha, verdict, evidence. Diagnostics go to stderr.
The sha column is the recovery record: restore a branch with
`git branch <branch> <sha>`.

Exit codes:
  0  classification printed
  2  usage error
  3  not a git repository, or the base branch does not exist
"""

import argparse
import json
import subprocess
import sys


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def require_repo() -> None:
    if git("rev-parse", "--git-dir").returncode != 0:
        print("error: not a git repository", file=sys.stderr)
        sys.exit(3)


def resolve_base(requested: str | None) -> str:
    if requested:
        if git("rev-parse", "--verify", requested).returncode != 0:
            print(f"error: base branch not found: {requested}", file=sys.stderr)
            sys.exit(3)
        return requested
    for candidate in ("main", "master"):
        if git("rev-parse", "--verify", candidate).returncode == 0:
            return candidate
    print("error: no main or master branch; pass --base", file=sys.stderr)
    sys.exit(3)


def local_branches() -> list[tuple[str, str]]:
    result = git("for-each-ref", "--format=%(refname:short)\t%(objectname)", "refs/heads/")
    rows = []
    for line in result.stdout.splitlines():
        if "\t" in line:
            name, sha = line.split("\t", 1)
            rows.append((name, sha))
    return rows


def pull_requests() -> dict[str, list[dict]]:
    """Head branch -> its pull requests. Empty when the GitHub CLI cannot answer."""
    try:
        result = subprocess.run(
            ["gh", "pr", "list", "--state", "all", "--limit", "500",
             "--json", "headRefName,state,number"],
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        print("warning: gh not found — squash-merged branches will read as unresolved", file=sys.stderr)
        return {}
    if result.returncode != 0:
        print(f"warning: gh pr list failed — {result.stderr.strip()}", file=sys.stderr)
        return {}
    by_head: dict[str, list[dict]] = {}
    for pr in json.loads(result.stdout):
        by_head.setdefault(pr["headRefName"], []).append(pr)
    return by_head


def classify(name: str, sha: str, base: str, prs: dict[str, list[dict]]) -> tuple[str, str]:
    if git("merge-base", "--is-ancestor", sha, base).returncode == 0:
        return "ancestor", f"in {base}"
    candidates = prs.get(name, [])
    for pr in candidates:
        if pr["state"] == "MERGED":
            return "pr-merged", f"PR #{pr['number']} merged"
    for pr in candidates:
        if pr["state"] == "OPEN":
            return "pr-open", f"PR #{pr['number']} open"
    for pr in candidates:
        if pr["state"] == "CLOSED":
            return "pr-closed", f"PR #{pr['number']} closed unmerged"
    return "unresolved", "no merged PR and not in base"


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify local branches for pruning")
    parser.add_argument("--base", help="Base branch to test against (default main, then master)")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of TSV")
    args = parser.parse_args()

    require_repo()
    base = resolve_base(args.base)
    current = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    prs = pull_requests()

    rows = []
    for name, sha in local_branches():
        if name == base:
            continue
        verdict, evidence = classify(name, sha, base, prs)
        rows.append({
            "branch": name,
            "sha": sha,
            "verdict": verdict,
            "evidence": evidence,
            "checkedOut": name == current,
        })

    if args.json:
        print(json.dumps({"base": base, "branches": rows}, indent=2))
    else:
        print("branch\tsha\tverdict\tevidence")
        for row in rows:
            print(f"{row['branch']}\t{row['sha']}\t{row['verdict']}\t{row['evidence']}")

    safe = sum(1 for row in rows if row["verdict"] in ("ancestor", "pr-merged"))
    print(f"{len(rows)} branches, {safe} safe to delete, base {base}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
