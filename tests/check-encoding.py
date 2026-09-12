#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Validates that every Python script normalises its text I/O to UTF-8.

Usage:
  uv run tests/check-encoding.py

Run from the repo root. No arguments.

Python decodes files, stdout and subprocess output with the locale encoding unless
told otherwise. On Windows that is cp1252, which cannot encode characters these
scripts print routinely — a bare `print(f"{src} → {dst}")` raises
UnicodeEncodeError and kills the run. Scripts ship to users on every platform, so
they normalise encoding in-process rather than relying on the console codepage.

Checks every tracked *.py file:
  1. Reconfigures sys.stdout and sys.stderr to UTF-8 at import time
  2. Passes encoding= to every open() and Path.read_text/write_text call
  3. Passes encoding= to every subprocess call that decodes output with text=True

Exit codes:
  0  all scripts normalise their I/O
  1  gaps found
  2  file error
"""

import ast
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).parent.parent
DECODING_CALLS = {"run", "check_output", "Popen"}
ENCODED_READS = {"read_text", "write_text"}


def tracked_scripts() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return [REPO_ROOT / line for line in result.stdout.split()]


def call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


def is_subprocess_call(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and isinstance(func.value, ast.Name)
        and func.value.id == "subprocess"
        and func.attr in DECODING_CALLS
    )


def kwargs_of(node: ast.Call) -> set[str]:
    return {kw.arg for kw in node.keywords if kw.arg}


def normalises_streams(tree: ast.Module) -> bool:
    """True when the module reconfigures both stdout and stderr at import time."""
    streams = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or call_name(node) != "reconfigure":
            continue
        target = node.func.value
        if (
            isinstance(target, ast.Attribute)
            and isinstance(target.value, ast.Name)
            and target.value.id == "sys"
        ):
            streams.add(target.attr)
    return {"stdout", "stderr"} <= streams


def check(script: Path) -> list[str]:
    rel = script.relative_to(REPO_ROOT).as_posix()
    tree = ast.parse(script.read_text(encoding="utf-8"))
    issues = []

    if not normalises_streams(tree):
        issues.append(
            f"UNNORMALISED {rel} does not reconfigure sys.stdout and sys.stderr to UTF-8"
        )

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = call_name(node)
        keywords = kwargs_of(node)

        if name == "open" and "encoding" not in keywords and "b" not in _mode(node):
            issues.append(f"UNENCODED {rel}:{node.lineno} open() without encoding=")
        elif name in ENCODED_READS and "encoding" not in keywords:
            issues.append(f"UNENCODED {rel}:{node.lineno} {name}() without encoding=")
        elif (
            is_subprocess_call(node)
            and {"text", "universal_newlines"} & keywords
            and "encoding" not in keywords
        ):
            issues.append(
                f"UNENCODED {rel}:{node.lineno} subprocess.{name}(text=True) "
                f"without encoding="
            )

    return issues


def _mode(node: ast.Call) -> str:
    """The literal mode string of an open() call, or '' when it is not a literal."""
    for kw in node.keywords:
        if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
            return str(kw.value.value)
    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
        return str(node.args[1].value)
    return ""


def main() -> int:
    try:
        scripts = tracked_scripts()
    except (subprocess.CalledProcessError, FileNotFoundError) as err:
        print(f"Could not list tracked scripts: {err}")
        return 2

    issues = []
    for script in scripts:
        try:
            issues.extend(check(script))
        except (OSError, SyntaxError) as err:
            print(f"Could not parse {script}: {err}")
            return 2

    if issues:
        print("Encoding issues found:\n")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n{len(issues)} issue(s) found.")
        return 1

    print(f"OK — {len(scripts)} scripts normalise their I/O to UTF-8.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
