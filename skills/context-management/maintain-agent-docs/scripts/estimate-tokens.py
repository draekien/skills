#!/usr/bin/env python3
# /// script
# dependencies = ["tiktoken>=0.7"]
# ///
"""
Report the token cost of a set of agent documents.

Usage:
    uv run estimate-tokens.py <path> [<path> ...] [--json]

Each path is a file or a directory; directories are walked for *.md
recursively. Counts come from a real BPE tokenizer (o200k_base), not the
harness's own, so treat them as accurate to a few percent — enough for read
order and before-and-after deltas, which is all this skill uses them for.

--json prints [{path, tokens, lines}] plus a total on stdout and nothing
else; without it, a table is printed instead.

Exit codes:
    0  counted
    1  a path did not exist or could not be read
    2  usage error
"""

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import tiktoken
except ImportError:
    print("tiktoken is required: run via `uv run`", file=sys.stderr)
    sys.exit(2)


def collect(paths):
    files, missing = [], []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.is_file():
            files.append(path)
        else:
            missing.append(raw)
    seen, unique = set(), []
    for path in files:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique, missing


def main(argv):
    as_json = "--json" in argv
    paths = [arg for arg in argv if arg != "--json"]
    if not paths:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    files, missing = collect(paths)
    for raw in missing:
        print(f"no such path: {raw}", file=sys.stderr)

    encoding = tiktoken.get_encoding("o200k_base")
    rows = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            print(f"cannot read {path}: {error}", file=sys.stderr)
            missing.append(str(path))
            continue
        rows.append(
            {
                "path": path.as_posix(),
                "tokens": len(encoding.encode(text)),
                "lines": text.count("\n") + (0 if text.endswith("\n") else 1),
            }
        )

    total = sum(row["tokens"] for row in rows)
    if as_json:
        print(json.dumps({"files": rows, "total": total}, indent=2))
    else:
        width = max((len(row["path"]) for row in rows), default=4)
        for row in sorted(rows, key=lambda row: -row["tokens"]):
            print(f"{row['path']:<{width}}  {row['tokens']:>6}  {row['lines']:>5} ln")
        print(f"{'total':<{width}}  {total:>6}")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
