#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Copies rule files to a target directory.

Usage:
  uv run scripts/write-rules.py --target <rules-dir> <source-file> [source-file ...]

Output (stdout): JSON array — one entry per file copied:
  [{"name": "no-any", "source": "...", "target": "..."}]

Exit codes:
  0  All files copied successfully
  1  One or more source files not found
  2  Usage error
"""

import sys
import json
import shutil
from pathlib import Path


def main() -> int:
    args = sys.argv[1:]

    if "--target" not in args or len(args) < 3:
        print(
            "Usage: write-rules.py --target <rules-dir> <source-file> [...]",
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

    target_dir.mkdir(parents=True, exist_ok=True)

    results = []
    failed = False

    for src in source_paths:
        if not src.exists():
            print(f"Source not found: {src}", file=sys.stderr)
            failed = True
            continue

        target = target_dir / src.name
        shutil.copy2(src, target)
        results.append({"name": src.stem, "source": str(src), "target": str(target)})

    print(json.dumps(results, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
