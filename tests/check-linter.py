#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""Fixture tests for the plain-language linter's matching rules.

Usage:
  uv run tests/check-linter.py

Exit codes:
  0  every case matched
  1  a case produced unexpected findings
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LINT = REPO / "skills" / "output-styles" / "plain-language" / "scripts" / "lint.py"

CASES = [
    (
        "block tags do not join prose into one sentence",
        "{% hint style=\"info\" %}\n"
        "A read taken after the write, and before the next call, will observe the\n"
        "value the writer stored, so long as nothing has reset it in between now.\n"
        "{% endhint %}\n",
        [],
    ),
    (
        "trailing whitespace does not turn markup into prose",
        "{% hint style=\"info\" %}   \n"
        "A read taken after the write, and before the next call, will observe the\n"
        "value the writer stored, so long as nothing has reset it in between now.\n",
        [],
    ),
    (
        "hard-wrapped prose still joins into one sentence",
        "The team reviewed every single file in the repository during the audit, and\n"
        "then they wrote a long report about it that nobody read, which wasted the\n"
        "whole week for everyone involved in the project.\n",
        [("long-sentence", "warning")],
    ),
    (
        "list items are measured on their own",
        "- A list item that runs on and on and on and on and on and on and on and on\n"
        "  and on and on and on and on and on and on and on until it is far too long.\n",
        [("long-sentence", "warning")],
    ),
    (
        "be plus adjective is not passive",
        "The parameters and the return type are unchanged. The type is closed.\n"
        "Positional calls are unaffected.\n",
        [],
    ),
    (
        "an adverb does not hide the participle",
        "This behaviour is often described as a fold.\n",
        [("passive-voice", "warning")],
    ),
    (
        "real passive voice still reports",
        "The report was written by the team.\n",
        [("passive-voice", "warning")],
    ),
    (
        "placeholder dashes in table cells are not pivots",
        "| Rule | Quick fix | Notes |\n| --- | --- | --- |\n| WM001 | — | — |\n| WM002 | — | — |\n",
        [],
    ),
    (
        "a real em-dash pivot still reports",
        "The plan — the one we agreed — is done.\n",
        [("em-dash-pivot", "warning")],
    ),
    (
        "an em-dash pivot never spans two lines",
        "The plan — the one we agreed\nis done — for now.\n",
        [],
    ),
    (
        "notPrecededBy skips attributive very",
        "The change allocates the very Task it avoids.\n",
        [],
    ),
    (
        "adverbial very still reports",
        "This is a very good example.\n",
        [("candidate", "error")],
    ),
    (
        "the underscore character is not the verb",
        "The underscore character is reserved.\n",
        [("passive-voice", "warning")],
    ),
    (
        "the verb form still reports, and never auto-fixes",
        "This underscores the need for care.\n",
        [("candidate", "error")],
    ),
    (
        "code cast as a speaker reports",
        "The name tells you nothing. The signature says the contract out loud.\n"
        "Only one of them tells you what it is doing.\n",
        [("anthropomorphism", "warning"), ("anthropomorphism", "warning"),
         ("anthropomorphism", "warning")],
    ),
    (
        "a plain report of what something says does not report",
        "The log tells you which branch ran.\n",
        [],
    ),
    (
        "nothing as a clause subject does not report",
        "The dashboard tells you nothing is wrong.\n",
        [],
    ),
    (
        "code described as growing reports",
        "You will meet it in code that grew one method at a time.\n",
        [("candidate", "error"), ("anthropomorphism", "warning")],
    ),
    (
        "a thing that really grows does not report",
        "The town grew one house at a time.\n",
        [],
    ),
    (
        "gives plus a type name reports",
        "The parser gives Option<string> when the key is missing.\n",
        [("gives-type", "warning")],
    ),
    (
        "gives plus an ordinary noun does not report",
        "The report gives Australia as the jurisdiction.\n",
        [],
    ),
    (
        "gives plus a possessive brand does not report",
        "The service gives McDonald's a discount.\n",
        [],
    ),
    (
        "notFollowedBy skips the user as a data record",
        "If the user does not exist, return an error.\n",
        [],
    ),
    (
        "the user as the reader still reports",
        "The user should read this page.\n",
        [("candidate", "error")],
    ),
]

FIX_CASES = [
    ("underscores is never applied by --fix", "Use underscores between words.\n"),
    ("reach for is never applied by --fix", "Do not reach for the top shelf.\n"),
    ("you will meet is never applied by --fix",
     "The survey asks how many people you will meet each week.\n"),
]

DRY_RUN_BODY = "We will utilise the process and commence work.\n"

DRY_RUN_CHECKS = 4

REJECTED = [
    ("an anchored guard", {"swaps": {"x": {"a": {"replacement": "b", "notFollowedBy": "^y"}}}}),
    ("an unknown entry option", {"swaps": {"x": {"a": {"replacment": "b"}}}}),
    ("a boundary without an id", {"sentenceBoundaries": ["^:::"]}),
]


def run(workdir: Path, target: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LINT), str(target), *flags],
        capture_output=True, text=True, cwd=workdir, encoding="utf-8",
    )


def total() -> int:
    return len(CASES) + len(FIX_CASES) + len(REJECTED) + DRY_RUN_CHECKS


def main() -> int:
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        target = workdir / "case.md"

        for name, body, expected in CASES:
            target.write_text(body, encoding="utf-8")
            result = run(workdir, target, "--json")
            if result.returncode not in (0, 1):
                failures.append(f"{name}: linter exited {result.returncode}\n{result.stderr}")
                continue
            actual = [(f["rule"], f["severity"]) for f in json.loads(result.stdout)]
            if sorted(actual) != sorted(expected):
                failures.append(f"{name}: expected {sorted(expected)}, got {sorted(actual)}")

        for name, body in FIX_CASES:
            target.write_text(body, encoding="utf-8")
            run(workdir, target, "--fix")
            if target.read_text(encoding="utf-8") != body:
                failures.append(f"{name}: --fix rewrote the text")

        target.write_text(DRY_RUN_BODY, encoding="utf-8")
        result = run(workdir, target, "--fix", "--dry-run", "--json")
        payload = json.loads(result.stdout)
        planned = [(f["text"], f["replacement"]) for f in payload["fixes"]]
        if planned != [("utilise", "use"), ("commence", "start")]:
            failures.append(f"--dry-run listed {planned}")
        if target.read_text(encoding="utf-8") != DRY_RUN_BODY:
            failures.append("--dry-run rewrote the file")
        if result.returncode != 1:
            failures.append(f"--dry-run with pending fixes exited {result.returncode}, expected 1")

        if run(workdir, target, "--dry-run").returncode != 2:
            failures.append("--dry-run without --fix did not exit 2")

        overrides = workdir / "overrides.json"
        for name, payload in REJECTED:
            target.write_text("hello\n", encoding="utf-8")
            overrides.write_text(json.dumps(payload), encoding="utf-8")
            result = run(workdir, target, "--overrides", str(overrides))
            if result.returncode != 3:
                failures.append(f"{name}: expected exit 3, got {result.returncode}")

    if failures:
        for failure in failures:
            print(f"FAIL  {failure}")
        print(f"\n{len(failures)} failure(s) across {total()} case(s)")
        return 1
    print(f"OK - {total()} linter cases, all matched.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
