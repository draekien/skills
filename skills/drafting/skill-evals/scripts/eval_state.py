#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Deterministic state for the skill-evals suite: hash suites, mint versions,
append run records, scaffold an output directory. Keeps the suite frozen so
runs stay comparable, and versions it the moment its content changes so a
trend never silently spans two different test sets.

The orchestrator owns generation and judgement; this script owns the file
mechanics that must be exact and repeatable.

Output layout (per evaluated skill):
  <dir>/
    report.html                 copied from assets, never regenerated
    README.md                   copied from assets
    activation/suite/v1.json …  frozen corpus + labels, hash-keyed
    activation/runs.jsonl       one run record per line
    impact/suite/v1.json …      frozen tasks + criteria
    impact/runs.jsonl

Usage:
  uv run scripts/eval_state.py init-output --dir <dir>
  uv run scripts/eval_state.py hash-suite --file <draft.json>
  uv run scripts/eval_state.py commit-suite --dir <dir> --mode <activation|impact> --file <draft.json>
  uv run scripts/eval_state.py append-run  --dir <dir> --mode <activation|impact> --file <run.json>

Exit codes: 0 success, 2 usage / validation error.
"""

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

MODES = ("activation", "impact")
# Fields stamped by this script — excluded from the content hash so re-hashing
# an already-committed suite reproduces the same digest.
VOLATILE = ("version", "hash", "createdTs")
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def content_hash(suite: dict) -> str:
    """Stable digest of everything that defines the test set."""
    content = {k: v for k, v in suite.items() if k not in VOLATILE}
    blob = json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()


def suite_dir(root: Path, mode: str) -> Path:
    return root / mode / "suite"


def existing_versions(root: Path, mode: str) -> list[int]:
    d = suite_dir(root, mode)
    if not d.exists():
        return []
    out = []
    for f in d.glob("v*.json"):
        try:
            out.append(int(f.stem[1:]))
        except ValueError:
            continue
    return sorted(out)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(msg: str) -> int:
    print(f"error: {msg}", file=sys.stderr)
    return 2


# ---- commands -----------------------------------------------------------

def cmd_init_output(root: Path) -> int:
    for mode in MODES:
        suite_dir(root, mode).mkdir(parents=True, exist_ok=True)
        runs = root / mode / "runs.jsonl"
        if not runs.exists():
            runs.write_text("", encoding="utf-8")

    report_src = ASSETS / "report-template.html"
    readme_src = ASSETS / "output-README.md"
    if not report_src.exists():
        return fail(f"missing bundled asset: {report_src}")
    shutil.copyfile(report_src, root / "report.html")
    if readme_src.exists():
        shutil.copyfile(readme_src, root / "README.md")

    print(str(root))
    return 0


def cmd_hash_suite(draft: Path) -> int:
    print(content_hash(load_json(draft)))
    return 0


def cmd_commit_suite(root: Path, mode: str, draft_path: Path) -> int:
    if mode not in MODES:
        return fail(f"mode must be one of {MODES}")
    draft = load_json(draft_path)
    new_hash = content_hash(draft)

    versions = existing_versions(root, mode)
    if versions:
        latest = versions[-1]
        latest_file = suite_dir(root, mode) / f"v{latest}.json"
        if load_json(latest_file).get("hash") == new_hash:
            # Identical test set — reuse the frozen version, do not mint.
            print(json.dumps({"version": latest, "hash": new_hash, "minted": False}))
            return 0
        version = latest + 1
    else:
        version = 1

    suite_dir(root, mode).mkdir(parents=True, exist_ok=True)
    draft["mode"] = mode
    draft["version"] = version
    draft["hash"] = new_hash
    draft["createdTs"] = now_iso()
    out = suite_dir(root, mode) / f"v{version}.json"
    out.write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"version": version, "hash": new_hash, "minted": True}))
    return 0


def cmd_append_run(root: Path, mode: str, run_path: Path) -> int:
    if mode not in MODES:
        return fail(f"mode must be one of {MODES}")
    run = load_json(run_path)

    version = run.get("suiteVersion")
    if version is None:
        return fail("run record must carry suiteVersion")
    suite_file = suite_dir(root, mode) / f"v{version}.json"
    if not suite_file.exists():
        return fail(f"run references suite v{version}, which does not exist - commit the suite first")

    suite_hash = load_json(suite_file).get("hash")
    if run.get("suiteHash") and run["suiteHash"] != suite_hash:
        return fail("run suiteHash does not match the committed suite — the suite changed under this run")
    run["suiteHash"] = suite_hash
    run["mode"] = mode
    run.setdefault("ts", now_iso())

    runs = root / mode / "runs.jsonl"
    runs.parent.mkdir(parents=True, exist_ok=True)
    with runs.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(run, ensure_ascii=False) + "\n")
    print(json.dumps({"appended": True, "ts": run["ts"], "suiteVersion": version}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen-suite state for skill-evals")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init-output", help="Scaffold the output dir and copy the report + README")
    p_init.add_argument("--dir", required=True)

    p_hash = sub.add_parser("hash-suite", help="Print the content hash of a draft suite")
    p_hash.add_argument("--file", required=True)

    p_commit = sub.add_parser("commit-suite", help="Reuse the frozen suite if unchanged, else mint the next version")
    p_commit.add_argument("--dir", required=True)
    p_commit.add_argument("--mode", required=True)
    p_commit.add_argument("--file", required=True)

    p_run = sub.add_parser("append-run", help="Append a run record to runs.jsonl")
    p_run.add_argument("--dir", required=True)
    p_run.add_argument("--mode", required=True)
    p_run.add_argument("--file", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 2

    if args.command == "init-output":
        return cmd_init_output(Path(args.dir))
    if args.command == "hash-suite":
        return cmd_hash_suite(Path(args.file))
    if args.command == "commit-suite":
        return cmd_commit_suite(Path(args.dir), args.mode, Path(args.file))
    if args.command == "append-run":
        return cmd_append_run(Path(args.dir), args.mode, Path(args.file))
    return 2


if __name__ == "__main__":
    sys.exit(main())
