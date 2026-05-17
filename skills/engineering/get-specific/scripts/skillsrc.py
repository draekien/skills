#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Reads and writes the get-specific section of .draekien/.skillsrc.

Usage:
  uv run scripts/skillsrc.py --config <path> get
  uv run scripts/skillsrc.py --config <path> set <value>

get  — prints dictionaryPath value (or default if absent)
set  — merges dictionaryPath into the file, preserving all other skills' keys

Exit codes:
  0  success
  2  usage error
"""

import argparse
import json
import sys
from pathlib import Path

SKILL_NAME = "get-specific"
KEY = "dictionaryPath"
DEFAULT = ".draekien/ubiquitous-language.yaml"


def load(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def cmd_get(config_path: Path) -> int:
    data = load(config_path)
    print(data.get(SKILL_NAME, {}).get(KEY, DEFAULT))
    return 0


def cmd_set(config_path: Path, value: str) -> int:
    data = load(config_path)
    data.setdefault(SKILL_NAME, {})[KEY] = value
    config_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Manage {SKILL_NAME} config in .skillsrc"
    )
    parser.add_argument("--config", required=True, help="Path to .draekien/.skillsrc")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("get", help=f"Print {KEY} (default: {DEFAULT!r})")

    set_p = subparsers.add_parser("set", help=f"Set {KEY}")
    set_p.add_argument("value", help="New value for dictionaryPath")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 2

    config_path = Path(args.config)

    if args.command == "get":
        return cmd_get(config_path)
    if args.command == "set":
        return cmd_set(config_path, args.value)

    return 2


if __name__ == "__main__":
    sys.exit(main())
