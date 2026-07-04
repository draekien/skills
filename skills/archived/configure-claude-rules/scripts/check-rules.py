#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Compares rule source files against an installed target directory.

Usage:
  uv run scripts/check-rules.py --target <rules-dir> <source-file> [source-file ...]

Output (stdout): JSON array — one entry per source file:
  [{"name": "no-any", "status": "new|identical|modified", "source": "...", "target": "..."}]

Exit codes:
  0  All files identical (nothing to copy)
  1  One or more files are new or modified
  2  Usage or file error
"""

import sys
import json
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    args = sys.argv[1:]

    if "--target" not in args or len(args) < 3:
        print(
            "Usage: check-rules.py --target <rules-dir> <source-file> [...]",
            file=sys.stderr,
        )
        return 2

    target_idx = args.index("--target")
    target_dir = Path(args[target_idx + 1])
    source_paths = [
        Path(a) for i, a in enumerate(args) if i not in (target_idx, target_idx + 1)
    ]

    if not source_paths:
        print("No source files provided.", file=sys.stderr)
        return 2

    results = []
    has_changes = False

    for src in source_paths:
        if not src.exists():
            print(f"Source not found: {src}", file=sys.stderr)
            return 2

        target = target_dir / src.name

        if not target.exists():
            status = "new"
            has_changes = True
        elif sha256(src) == sha256(target):
            status = "identical"
        else:
            status = "modified"
            has_changes = True

        results.append(
            {
                "name": src.stem,
                "status": status,
                "source": str(src),
                "target": str(target),
            }
        )

    print(json.dumps(results, indent=2))
    return 1 if has_changes else 0


if __name__ == "__main__":
    sys.exit(main())
