#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Scans a target repository and outputs detected configure-claude-rules topics as JSON.

Usage:
  uv run scripts/detect-topics.py <target-dir>

Output (stdout): JSON array of detected topics with their signals, e.g.:
  [
    {"topic": "typescript", "signals": ["tsconfig.json found"]},
    {"topic": "software-design", "signals": ["always applicable"]}
  ]

Exit codes:
  0  success
  2  usage error
"""

import json
import re
import sys
from pathlib import Path


def load_package_json(root: Path) -> dict:
    pkg = root / "package.json"
    if not pkg.exists():
        return {}
    try:
        return json.loads(pkg.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def all_deps(pkg: dict) -> set:
    deps = set(pkg.get("dependencies", {}).keys())
    deps |= set(pkg.get("devDependencies", {}).keys())
    return deps


def detect(root: Path) -> list:
    results = []
    pkg = load_package_json(root)
    deps = all_deps(pkg)

    # typescript
    ts_signals = []
    if (root / "tsconfig.json").exists():
        ts_signals.append("tsconfig.json found")
    if not ts_signals and any(root.rglob("*.ts")) or any(root.rglob("*.tsx")):
        ts_signals.append(".ts/.tsx files found")
    if ts_signals:
        results.append({"topic": "typescript", "signals": ts_signals})

    # csharp
    cs_signals = []
    for pattern in ("*.csproj", "*.sln", "global.json", "*.cs"):
        if any(root.rglob(pattern)):
            cs_signals.append(f"{pattern} found")
            break
    if cs_signals:
        results.append({"topic": "csharp", "signals": cs_signals})

    # react
    if "react" in deps:
        results.append({"topic": "react", "signals": ["react in package.json dependencies"]})

    # tanstack-query
    tq_signals = [p for p in ("@tanstack/react-query", "@tanstack/query-core") if p in deps]
    if tq_signals:
        results.append({"topic": "tanstack-query", "signals": [f"{s} in package.json" for s in tq_signals]})

    # tanstack-router
    tr_signals = [p for p in ("@tanstack/react-router", "@tanstack/router") if p in deps]
    if tr_signals:
        results.append({"topic": "tanstack-router", "signals": [f"{s} in package.json" for s in tr_signals]})

    # tailwind
    tw_signals = []
    if "tailwindcss" in deps:
        tw_signals.append("tailwindcss in package.json dependencies")
    if not tw_signals:
        for css_file in root.rglob("*.css"):
            try:
                if re.search(r'@import\s+["\']tailwindcss["\']', css_file.read_text(encoding="utf-8", errors="ignore")):
                    tw_signals.append(f'@import "tailwindcss" in {css_file.name}')
                    break
            except OSError:
                continue
    if tw_signals:
        results.append({"topic": "tailwind", "signals": tw_signals})

    # software-design — always applicable
    results.append({"topic": "software-design", "signals": ["always applicable"]})

    return results


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: detect-topics.py <target-dir>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2

    print(json.dumps(detect(root), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
