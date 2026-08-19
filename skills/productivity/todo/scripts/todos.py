#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Reads and writes todos in the markdown backend, in either layout.

Usage:
  uv run scripts/todos.py --path <path> --layout <layout> add --title <t> [--body <b> | --body-file <f>] [--needs-expansion]
  uv run scripts/todos.py --path <path> --layout <layout> list [--status open|done|all] [--limit <n>]
  uv run scripts/todos.py --path <path> --layout <layout> update <id> [--title <t>] [--body <b> | --body-file <f>] [--clear-flag]

--layout is file-per-todo (--path is a directory) or single-file (--path is a file).
--body-file accepts - to read the body from stdin, which keeps line breaks intact.

add     — writes the todo and prints its JSON record; re-adding an identical
          title and body is a no-op rather than a duplicate
list    — prints {"todos": [...], "total": n, "returned": n, "skipped": [...]}
update  — replaces the named fields of an existing todo, leaving the rest as-is

Exit codes:
  0  success
  2  usage error
  3  path unreadable, or its layout does not match --layout
  4  no todo found with the given id
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

STATUSES = ("open", "done")
LAYOUTS = ("file-per-todo", "single-file")
DEFAULT_LIMIT = 50
ITEM = re.compile(r"^- \[(?P<box>[ xX])\] (?P<rest>.*)$")
CREATED = re.compile(r"<!-- created: (?P<created>[^>]*?) -->")
FLAG = "<!-- needs-expansion -->"


def fail(message: str, code: int) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(code)


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60].strip("-") or "todo"


def read_body(body: str | None, body_file: str | None) -> str | None:
    if body is not None and body_file is not None:
        fail("pass --body or --body-file, not both", 2)
    if body is not None:
        return body
    if body_file is None:
        return None
    if body_file == "-":
        return sys.stdin.read().strip()
    path = Path(body_file)
    if not path.exists():
        fail(f"--body-file {body_file} does not exist", 3)
    return path.read_text(encoding="utf-8").strip()


def unique_id(taken: set[str], base: str) -> str:
    if base not in taken:
        return base
    n = 2
    while f"{base}-{n}" in taken:
        n += 1
    return f"{base}-{n}"


class FilePerTodo:
    """One markdown file per todo, metadata in YAML frontmatter."""

    def __init__(self, path: Path):
        if path.exists() and not path.is_dir():
            fail(f"{path} is a file; --layout file-per-todo needs a directory", 3)
        self.dir = path

    def _parse(self, path: Path) -> dict | None:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return None
        _, _, rest = text.partition("---")
        front, sep, body = rest.partition("\n---")
        if not sep:
            return None
        fields = {}
        for line in front.strip().splitlines():
            key, _, value = line.partition(":")
            value = value.strip()
            if value.startswith('"'):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    value = value.strip('"')
            fields[key.strip()] = value
        if "title" not in fields:
            return None
        return {
            "id": path.stem,
            "title": fields["title"],
            "created": fields.get("created", ""),
            "status": fields.get("status", "open"),
            "needsExpansion": fields.get("needsExpansion", "false") == "true",
            "location": str(path).replace("\\", "/"),
            "body": body.lstrip("\n"),
        }

    def load(self) -> tuple[list[dict], list[str]]:
        if not self.dir.exists():
            return [], []
        todos, skipped = [], []
        for path in sorted(self.dir.glob("*.md")):
            try:
                todo = self._parse(path)
            except OSError as e:
                fail(f"could not read {path}: {e}", 3)
            if todo is None:
                skipped.append(str(path).replace("\\", "/"))
            else:
                todos.append(todo)
        return todos, skipped

    def _write(self, todo: dict) -> None:
        front = "\n".join(
            [
                "---",
                f"title: {json.dumps(todo['title'])}",
                f"created: {todo['created']}",
                f"status: {todo['status']}",
                f"needsExpansion: {'true' if todo['needsExpansion'] else 'false'}",
                "---",
            ]
        )
        body = todo["body"].strip()
        text = front + "\n\n" + (body + "\n" if body else "")
        Path(todo["location"]).write_text(text, encoding="utf-8")

    def add(self, title: str, body: str, flag: bool) -> dict:
        existing, _ = self.load()
        for todo in existing:
            if todo["title"] == title and todo["body"].strip() == body.strip():
                return todo
        self.dir.mkdir(parents=True, exist_ok=True)
        todo_id = unique_id({t["id"] for t in existing}, slugify(title))
        todo = {
            "id": todo_id,
            "title": title,
            "created": date.today().isoformat(),
            "status": "open",
            "needsExpansion": flag,
            "location": str(self.dir / f"{todo_id}.md").replace("\\", "/"),
            "body": body,
        }
        self._write(todo)
        return todo

    def update(self, todo_id: str, title, body, clear_flag: bool) -> dict:
        todos, _ = self.load()
        match = next((t for t in todos if t["id"] == todo_id), None)
        if match is None:
            fail(f"no todo with id {todo_id}; ids: {', '.join(t['id'] for t in todos) or 'none'}", 4)
        if title is not None:
            match["title"] = title
        if body is not None:
            match["body"] = body
        if clear_flag:
            match["needsExpansion"] = False
        self._write(match)
        return match


class SingleFile:
    """One checklist file, body lines indented two spaces under each item."""

    def __init__(self, path: Path):
        if path.is_dir():
            fail(f"{path} is a directory; --layout single-file needs a file path", 3)
        self.file = path

    def load(self) -> tuple[list[dict], list[str]]:
        if not self.file.exists():
            return [], []
        try:
            lines = self.file.read_text(encoding="utf-8").splitlines()
        except OSError as e:
            fail(f"could not read {self.file}: {e}", 3)
        todos, taken, current = [], set(), None
        for line in lines:
            item = ITEM.match(line)
            if item:
                rest = item.group("rest")
                created = CREATED.search(rest)
                title = CREATED.sub("", rest).replace(FLAG, "").strip()
                todo_id = unique_id(taken, slugify(title))
                taken.add(todo_id)
                current = {
                    "id": todo_id,
                    "title": title,
                    "created": created.group("created").strip() if created else "",
                    "status": "open" if item.group("box") == " " else "done",
                    "needsExpansion": FLAG in rest,
                    "location": str(self.file).replace("\\", "/"),
                    "body": "",
                }
                todos.append(current)
            elif current is not None and line.startswith("  ") and line.strip():
                current["body"] = (current["body"] + "\n" + line[2:]).strip("\n")
            elif not line.strip():
                current = None
        return todos, []

    def _render(self, todo: dict) -> list[str]:
        head = f"- [{' ' if todo['status'] == 'open' else 'x'}] {todo['title']}"
        if todo["created"]:
            head += f" <!-- created: {todo['created']} -->"
        if todo["needsExpansion"]:
            head += f" {FLAG}"
        lines = [head]
        lines += [f"  {line}" for line in todo["body"].splitlines() if line.strip()]
        return lines

    def _rewrite(self, todos: list[dict]) -> None:
        out = ["# Todos", ""]
        for todo in todos:
            out += self._render(todo) + [""]
        self.file.parent.mkdir(parents=True, exist_ok=True)
        self.file.write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8")

    def add(self, title: str, body: str, flag: bool) -> dict:
        todos, _ = self.load()
        for todo in todos:
            if todo["title"] == title and todo["body"].strip() == body.strip():
                return todo
        todo = {
            "id": unique_id({t["id"] for t in todos}, slugify(title)),
            "title": title,
            "created": date.today().isoformat(),
            "status": "open",
            "needsExpansion": flag,
            "location": str(self.file).replace("\\", "/"),
            "body": body,
        }
        self._rewrite([todo] + todos)
        return todo

    def update(self, todo_id: str, title, body, clear_flag: bool) -> dict:
        todos, _ = self.load()
        match = next((t for t in todos if t["id"] == todo_id), None)
        if match is None:
            fail(f"no todo with id {todo_id}; ids: {', '.join(t['id'] for t in todos) or 'none'}", 4)
        if title is not None:
            match["title"] = title
        if body is not None:
            match["body"] = body
        if clear_flag:
            match["needsExpansion"] = False
        self._rewrite(todos)
        return match


def backend(path: str, layout: str):
    return FilePerTodo(Path(path)) if layout == "file-per-todo" else SingleFile(Path(path))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manage todos in the markdown backend",
        epilog=(
            "example:\n"
            "  uv run scripts/todos.py --path docs/todos --layout file-per-todo add \\\n"
            "      --title 'Cache the parser output' --body-file -\n\n"
            "exit codes:\n"
            "  0 success\n"
            "  2 usage error\n"
            "  3 path unreadable, or its layout does not match --layout\n"
            "  4 no todo found with the given id\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--path", required=True, help="Directory (file-per-todo) or file (single-file)")
    parser.add_argument("--layout", required=True, choices=LAYOUTS)
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Write a new todo")
    add_p.add_argument("--title", required=True)
    add_p.add_argument("--body", default=None)
    add_p.add_argument("--body-file", default=None, help="File to read the body from, or - for stdin")
    add_p.add_argument("--needs-expansion", action="store_true", help="Flag the todo as needing expansion")

    list_p = subparsers.add_parser("list", help="Print todos as JSON")
    list_p.add_argument("--status", default="open", choices=(*STATUSES, "all"))
    list_p.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Max todos to return (default {DEFAULT_LIMIT})")

    update_p = subparsers.add_parser("update", help="Replace fields of an existing todo")
    update_p.add_argument("id")
    update_p.add_argument("--title", default=None)
    update_p.add_argument("--body", default=None)
    update_p.add_argument("--body-file", default=None, help="File to read the body from, or - for stdin")
    update_p.add_argument("--clear-flag", action="store_true", help="Clear the needs-expansion flag")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 2

    store = backend(args.path, args.layout)

    if args.command == "add":
        body = read_body(args.body, args.body_file) or ""
        print(json.dumps(store.add(args.title, body, args.needs_expansion), indent=2))
        return 0

    if args.command == "list":
        if args.limit < 1:
            fail("--limit must be 1 or more", 2)
        todos, skipped = store.load()
        if args.status != "all":
            todos = [t for t in todos if t["status"] == args.status]
        todos.sort(key=lambda t: (t["created"], t["id"]), reverse=True)
        for todo in todos:
            todo.pop("body", None)
        if skipped:
            print(f"warning: skipped {len(skipped)} file(s) without valid frontmatter", file=sys.stderr)
        print(
            json.dumps(
                {
                    "todos": todos[: args.limit],
                    "total": len(todos),
                    "returned": min(len(todos), args.limit),
                    "skipped": skipped,
                },
                indent=2,
            )
        )
        return 0

    if args.command == "update":
        body = read_body(args.body, args.body_file)
        if body is None and args.title is None and not args.clear_flag:
            fail("update needs at least one of --title, --body, --body-file, --clear-flag", 2)
        print(json.dumps(store.update(args.id, args.title, body, args.clear_flag), indent=2))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
