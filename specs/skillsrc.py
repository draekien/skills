#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Generic reader/writer for a single skill's section of .draekien/.skillsrc.

Symlinked into each consuming skill's scripts/ directory as skillsrc.py —
see specs/skillsrc.md for the convention this implements.

Usage:
  uv run scripts/skillsrc.py --config <path> --skill <skill-name> get <key> [--default <value>]
  uv run scripts/skillsrc.py --config <path> --skill <skill-name> set <key> <value>

get  — prints the key's value, or --default (or "" if omitted) if absent
set  — merges the key into the file, preserving all other skills' keys

Exit codes:
  0  success
  2  usage error
  3  config file unreadable or not valid JSON
"""

import argparse
import json
import sys
from pathlib import Path


def load(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: could not read {config_path}: {e}", file=sys.stderr)
        sys.exit(3)
    except json.JSONDecodeError:
        print(
            f"error: {config_path} is not valid JSON — fix or delete it",
            file=sys.stderr,
        )
        sys.exit(3)


def cmd_get(config_path: Path, skill: str, key: str, default: str) -> int:
    data = load(config_path)
    print(data.get(skill, {}).get(key, default))
    return 0


def cmd_set(config_path: Path, skill: str, key: str, value: str) -> int:
    data = load(config_path)
    data.setdefault(skill, {})[key] = value
    config_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage a skill's config in .skillsrc")
    parser.add_argument("--config", required=True, help="Path to .draekien/.skillsrc")
    parser.add_argument("--skill", required=True, help="Skill name (top-level key)")
    subparsers = parser.add_subparsers(dest="command")

    get_p = subparsers.add_parser("get", help="Print a config value")
    get_p.add_argument("key", help="Config key to read")
    get_p.add_argument("--default", default="", help="Value to print if the key is absent")

    set_p = subparsers.add_parser("set", help="Set a config value")
    set_p.add_argument("key", help="Config key to write")
    set_p.add_argument("value", help="New value for the key")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 2

    config_path = Path(args.config)

    if args.command == "get":
        return cmd_get(config_path, args.skill, args.key, args.default)
    if args.command == "set":
        return cmd_set(config_path, args.skill, args.key, args.value)

    return 2


if __name__ == "__main__":
    sys.exit(main())
