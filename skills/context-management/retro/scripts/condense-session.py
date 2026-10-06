#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Condense a Claude Code session transcript into the evidence a retro needs.

Usage:
    uv run condense-session.py --list [--project <dir>] [--limit N]
    uv run condense-session.py <session-id | path.jsonl> [--output <file>] [--text-limit N]

--list prints the most recent sessions for a project directory (default: the
current directory) as JSON: [{id, path, modified, first_prompt}].

Given a session id or a transcript path, prints JSON on stdout:
    summary   tool call counts, error count, token usage, largest results,
              repeated calls, subagent rollups
    timeline  user prompts, tool calls (name, input, result size, error flag),
              and assistant text, in order

Long text is truncated to --text-limit characters (default 400). Pass
--output to write the JSON to a file instead of stdout; the timeline of a long
session will not fit in a tool result.

Exit codes:
    0  condensed or listed
    1  session not found, or the transcript could not be read
    2  usage error
    3  the transcript holds no records in the format this script parses
"""

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECTS = Path.home() / ".claude" / "projects"
LARGEST = 10


def project_slug(directory):
    return "".join(c if c.isalnum() else "-" for c in str(Path(directory).resolve()))


def clip(text, limit):
    text = text.strip()
    return text if len(text) <= limit else text[:limit] + f"… [+{len(text) - limit} chars]"


def result_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(part.get("text", "") for part in content if isinstance(part, dict))
    return ""


def read_records(path):
    records = []
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"skipped malformed line {number} in {path}", file=sys.stderr)
    return records


def first_prompt(path, limit):
    for record in read_records(path):
        if record.get("type") != "user" or record.get("isMeta"):
            continue
        content = (record.get("message") or {}).get("content")
        if isinstance(content, str):
            return clip(content, limit)
        if isinstance(content, list) and content and content[0].get("type") == "text":
            return clip(content[0].get("text", ""), limit)
    return ""


def condense(path, limit):
    timeline, calls, usage, counted = [], {}, Counter(), set()
    for record in read_records(path):
        kind = record.get("type")
        message = record.get("message") or {}
        content = message.get("content")
        stamp = record.get("timestamp")
        if kind == "assistant" and message.get("id") not in counted:
            counted.add(message.get("id"))
            for key in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
                usage[key] += (message.get("usage") or {}).get(key) or 0
        if kind == "user" and not record.get("isMeta"):
            if isinstance(content, str):
                timeline.append({"at": stamp, "event": "prompt", "text": clip(content, limit)})
                continue
        if not isinstance(content, list):
            continue
        for block in content:
            block_type = block.get("type")
            if kind == "user" and block_type == "text" and not record.get("isMeta"):
                timeline.append({"at": stamp, "event": "prompt", "text": clip(block.get("text", ""), limit)})
            elif kind == "assistant" and block_type == "text":
                timeline.append({"at": stamp, "event": "reply", "text": clip(block.get("text", ""), limit)})
            elif kind == "assistant" and block_type == "tool_use":
                entry = {
                    "at": stamp,
                    "event": "call",
                    "tool": block.get("name"),
                    "input": clip(json.dumps(block.get("input"), ensure_ascii=False), limit),
                    "key": json.dumps([block.get("name"), block.get("input")], sort_keys=True),
                }
                calls[block.get("id")] = entry
                timeline.append(entry)
            elif kind == "user" and block_type == "tool_result":
                entry = calls.get(block.get("tool_use_id"))
                text = result_text(block.get("content"))
                if entry is None:
                    continue
                entry["result_chars"] = len(text)
                if block.get("is_error"):
                    entry["error"] = clip(text, limit)

    tool_calls = [e for e in timeline if e["event"] == "call"]
    repeats = Counter(e["key"] for e in tool_calls)
    for entry in tool_calls:
        entry.pop("key")
    largest = sorted(tool_calls, key=lambda e: e.get("result_chars", 0), reverse=True)[:LARGEST]
    summary = {
        "transcript": str(path),
        "tool_calls": dict(Counter(e["tool"] for e in tool_calls).most_common()),
        "errors": sum(1 for e in tool_calls if "error" in e),
        "usage": dict(usage),
        "largest_results": [{k: e.get(k) for k in ("at", "tool", "input", "result_chars")} for e in largest],
        "repeated_calls": [{"call": clip(k, limit), "times": n} for k, n in repeats.items() if n > 1],
    }
    return summary, timeline


def resolve(target):
    path = Path(target)
    if path.suffix == ".jsonl" and path.is_file():
        return path
    matches = sorted(PROJECTS.glob(f"*/{target}.jsonl"))
    return matches[0] if matches else None


def list_sessions(project, count, limit):
    directory = PROJECTS / project_slug(project)
    if not directory.is_dir():
        print(f"no sessions for {project}: expected {directory}", file=sys.stderr)
        return 1
    files = sorted(directory.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)[:count]
    sessions = [
        {
            "id": f.stem,
            "path": str(f),
            "modified": datetime.fromtimestamp(f.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
            "first_prompt": first_prompt(f, limit),
        }
        for f in files
    ]
    print(json.dumps(sessions, indent=2, ensure_ascii=False))
    return 0


def option(argv, name, default):
    if name not in argv:
        return default
    index = argv.index(name)
    if index + 1 >= len(argv):
        raise ValueError(f"{name} needs a value")
    value = argv.pop(index + 1)
    argv.pop(index)
    return value


def main(argv):
    if not argv or "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0 if argv else 2
    try:
        limit = int(option(argv, "--text-limit", "400"))
        count = int(option(argv, "--limit", "10"))
        project = option(argv, "--project", ".")
        output = option(argv, "--output", None)
    except ValueError as error:
        print(f"{error}; see --help", file=sys.stderr)
        return 2

    if "--list" in argv:
        return list_sessions(project, count, limit)
    if len(argv) != 1 or argv[0].startswith("--"):
        print(f"expected one session id or .jsonl path, got {argv}; see --help", file=sys.stderr)
        return 2

    path = resolve(argv[0])
    if path is None:
        print(f"no transcript for {argv[0]!r}: pass a .jsonl path, or run --list for ids", file=sys.stderr)
        return 1
    try:
        summary, timeline = condense(path, limit)
        subagents = []
        for sub in sorted((path.parent / path.stem / "subagents").glob("agent-*.jsonl")):
            sub_summary, _ = condense(sub, limit)
            subagents.append(sub_summary)
    except (OSError, UnicodeDecodeError) as error:
        print(f"could not read {path}: {error}", file=sys.stderr)
        return 1
    if not timeline:
        print(f"no recognised records in {path}: read the transcript directly instead", file=sys.stderr)
        return 3
    summary["subagents"] = subagents
    document = json.dumps({"summary": summary, "timeline": timeline}, indent=2, ensure_ascii=False)
    if output:
        Path(output).write_text(document, encoding="utf-8")
        print(f"wrote {len(timeline)} timeline events to {output}", file=sys.stderr)
    else:
        print(document)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
