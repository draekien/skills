#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Validate an agent skill against the Agent Skills open standard.

Usage:
    uv run validate.py <skill-dir> [--json]
    uv run validate.py <skill-dir>/SKILL.md [--json]

--json prints the check results as a JSON array of {rule, level, detail}
objects on stdout (no other stdout output); without it, a human-readable
report is printed on stderr instead, keeping stdout free for data output.

Exit codes:
    0  all checks passed (warnings, if any, do not fail the run)
    1  one or more checks failed
    2  usage or parse error
"""

import io
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pyyaml not available — run with: uv run validate.py", file=sys.stderr)
    sys.exit(2)

# Fields defined by the Agent Skills open standard (agentskills.io/specification).
# Portable across every conformant harness.
_STANDARD_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}

# Harness-specific extensions to the open standard, grouped by the harness that
# defines them. These fields are valid for that harness but are NOT portable —
# a skill using them may be ignored or rejected by other harnesses. Using one is
# a warning, never an error.
#
# Claude Code is currently the only Agent Skills harness that documents SKILL.md
# frontmatter beyond the open standard. The others (GitHub Copilot, Cursor,
# Windsurf, Cline, Amp, Gemini CLI) read SKILL.md but document only the
# open-standard fields, so they contribute no extension set here. Add a new
# `_<HARNESS>_HARNESS_FIELDS` set and register it below when that changes.
# Source of truth (keep in sync): https://code.claude.com/docs/en/skills.md
_CLAUDE_HARNESS_FIELDS = {
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "hooks",
    "paths",
    "shell",
}

# Map each harness-specific field to the harness that defines it, so warnings can
# name the harness. Extend with `**{f: "<Harness>" for f in _<HARNESS>_FIELDS}`.
_HARNESS_FIELD_OWNER = {f: "Claude Code" for f in _CLAUDE_HARNESS_FIELDS}

_KNOWN_FIELDS = _STANDARD_FIELDS | set(_HARNESS_FIELD_OWNER)

# Model-specific terms that indicate non-portable instructions
_MODEL_TERMS = [
    "claude",
    "gpt-4",
    "gpt-3",
    "gpt-3.5",
    "gemini",
    "anthropic",
    "openai",
    "mistral",
    "llama",
    "cohere",
    "titan",
]

# Regex matching Python network library imports (more precise than string search)
_PY_NETWORK_IMPORT_RE = re.compile(
    r"^\s*(import|from)\s+(requests|httpx|aiohttp|urllib\.request|socket|http\.client|urllib3)\b",
    re.MULTILINE,
)


def _parse_skill_md(skill_md: Path):
    """Return (frontmatter_dict, body_str, raw_fm_str) or raise ValueError."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("SKILL.md does not begin with YAML frontmatter (---).")
    close = text.find("\n---", 3)
    if close == -1:
        raise ValueError("SKILL.md frontmatter is never closed by a second --- line.")
    raw_fm = text[3:close]
    fm = yaml.safe_load(raw_fm.strip()) or {}
    body = text[close + 4 :].strip()
    return fm, body, raw_fm


def _strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code spans from markdown."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", "", text)
    return text


def _local_links(text: str) -> list[str]:
    """Extract local file paths from markdown [label](path) links (ignores code spans)."""
    return [
        m.group(1)
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", _strip_code(text))
        if not re.match(r"https?://|#|mailto:", m.group(1))
    ]


# ---------------------------------------------------------------------------
# Check helpers
# ---------------------------------------------------------------------------


class Results:
    def __init__(self):
        self._items: list[dict] = []

    def ok(self, rule: str):
        self._items.append({"level": "pass", "rule": rule, "detail": ""})

    def fail(self, rule: str, detail: str):
        self._items.append({"level": "fail", "rule": rule, "detail": detail})

    def warn(self, rule: str, detail: str):
        """A non-blocking advisory — surfaced to the user but does not fail the run."""
        self._items.append({"level": "warn", "rule": rule, "detail": detail})

    def check(self, cond: bool, rule: str, detail: str):
        if cond:
            self.ok(rule)
        else:
            self.fail(rule, detail)

    @property
    def items(self):
        return self._items

    @property
    def failed(self):
        return [r for r in self._items if r["level"] == "fail"]

    @property
    def warnings(self):
        return [r for r in self._items if r["level"] == "warn"]


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def check_frontmatter_formatting(raw_fm: str, fm: dict, r: Results):
    unknown = [k for k in fm if k not in _KNOWN_FIELDS]
    r.check(
        not unknown,
        "frontmatter: no unknown fields",
        f"Unknown fields: {unknown} — check for typos",
    )

    # Harness-specific fields are valid but non-portable — warn, don't block.
    by_owner: dict[str, list[str]] = {}
    for k in fm:
        owner = _HARNESS_FIELD_OWNER.get(k)
        if owner:
            by_owner.setdefault(owner, []).append(k)
    for owner, fields in sorted(by_owner.items()):
        r.warn(
            f"frontmatter: {owner}-specific field(s) in use",
            f"{sorted(fields)} are {owner} extensions, not part of the Agent Skills "
            f"open standard — skills using them may not be portable to other harnesses",
        )

    for field in ("name", "description"):
        val = fm.get(field)
        if val is not None:
            r.check(
                isinstance(val, str),
                f"frontmatter: {field} is a plain string",
                f"{field} parsed as {type(val).__name__} — wrap value in quotes",
            )

    lines = raw_fm.splitlines()
    trailing = [i + 1 for i, line in enumerate(lines) if line != line.rstrip()]
    r.check(
        not trailing,
        "frontmatter: no trailing whitespace",
        f"Lines with trailing whitespace: {trailing}",
    )

    has_block_scalar = bool(re.search(r":\s*[|>]", raw_fm))
    r.check(
        not has_block_scalar,
        "frontmatter: no block scalar notation",
        "Block scalars (| or >) found — use inline strings for frontmatter values",
    )


def check_name(fm: dict, skill_dir: Path, r: Results):
    name = fm.get("name")
    r.check(bool(name), "name: present and non-empty", "name field is missing or empty")
    if not name:
        return

    r.check(
        1 <= len(name) <= 64,
        "name: 1–64 characters",
        f"name is {len(name)} characters — must be 1–64",
    )
    r.check(
        bool(re.match(r"^[a-z0-9-]+$", name)),
        "name: lowercase alphanumeric and hyphens only",
        f"'{name}' contains characters outside [a-z0-9-]",
    )
    r.check(
        not name.startswith("-"),
        "name: does not start with a hyphen",
        f"'{name}' starts with a hyphen",
    )
    r.check(
        not name.endswith("-"),
        "name: does not end with a hyphen",
        f"'{name}' ends with a hyphen",
    )
    r.check(
        "--" not in name,
        "name: no consecutive hyphens",
        f"'{name}' contains '--'",
    )
    dir_name = skill_dir.name
    r.check(
        name == dir_name,
        "name matches parent directory name",
        f"name is '{name}' but directory is '{dir_name}' — they must match exactly",
    )


def check_description(fm: dict, r: Results):
    desc = fm.get("description")
    r.check(
        bool(desc),
        "description: present and non-empty",
        "description field is missing or empty",
    )
    if desc:
        r.check(
            1 <= len(desc) <= 1024,
            "description: 1–1024 characters",
            f"description is {len(desc)} characters — must be 1–1024",
        )


def check_optional_fields(fm: dict, r: Results):
    compat = fm.get("compatibility")
    if compat is not None:
        r.check(
            1 <= len(str(compat)) <= 500,
            "compatibility: 1–500 characters",
            f"compatibility is {len(str(compat))} characters — must be 1–500",
        )

    metadata = fm.get("metadata")
    if metadata is not None:
        if isinstance(metadata, dict):
            bad = [k for k, v in metadata.items() if not isinstance(v, str)]
            r.check(
                not bad,
                "metadata: all values are strings",
                f"Non-string values for keys: {bad}",
            )
        else:
            r.fail(
                "metadata: must be a YAML key-value mapping",
                f"Got {type(metadata).__name__}",
            )

    allowed_tools = fm.get("allowed-tools")
    if allowed_tools is not None:
        # allowed-tools is a shared open-standard field — other harnesses honour
        # it only as a space-separated string. A YAML list works in Claude Code
        # but breaks that contract elsewhere, so it fails (not a warning). This is
        # the line between fail and warn: harness-only *fields* warn (others ignore
        # them); a non-portable form of a *shared* field fails.
        r.check(
            isinstance(allowed_tools, str),
            "allowed-tools: must be a space-separated string (not a YAML list)",
            f'Got {type(allowed_tools).__name__} — other harnesses honour this '
            f'shared field only as a string like "Bash Read Write"; the list form '
            f"works only in Claude Code",
        )

    argument_hint = fm.get("argument-hint")
    if argument_hint is not None:
        # An unquoted `[source]` parses as a YAML list, not the free-text string
        # every harness expects. Quoting it (`"[source]"`) keeps it a string and
        # is the only form that renders correctly across harnesses.
        r.check(
            isinstance(argument_hint, str),
            "argument-hint: must be a quoted string (not a YAML list)",
            f'Got {type(argument_hint).__name__} — wrap the value in quotes, e.g. '
            f'argument-hint: "[source]", not argument-hint: [source]',
        )


def check_body(body: str, skill_dir: Path, r: Results):
    lines = body.splitlines()
    r.check(
        len(lines) <= 500,
        "body: under 500 lines",
        f"Body is {len(lines)} lines — move verbose content to references/",
    )

    links = _local_links(body)

    absolute = [link for link in links if link.startswith("/")]
    r.check(
        not absolute,
        "body: file references use relative paths",
        f"Absolute paths found: {absolute}",
    )

    missing = [link for link in links if not (skill_dir / link).exists()]
    r.check(
        not missing,
        "body: all linked files exist",
        f"Missing: {missing}",
    )

    # Model-specific term heuristic — skip code blocks and inline code.
    # Word-boundary match so e.g. "coherent" does not trip on "cohere".
    body_prose = _strip_code(body).lower()
    found = [
        t for t in _MODEL_TERMS if re.search(rf"\b{re.escape(t)}\b", body_prose)
    ]
    r.check(
        not found,
        "body: no model-specific terms (LLM-agnostic)",
        f"Found: {found} — move platform-specific notes to compatibility:",
    )


def check_references(skill_dir: Path, r: Results):
    refs_dir = skill_dir / "references"
    if not refs_dir.exists():
        return
    chained = []
    for ref in refs_dir.glob("*.md"):
        local_links = _local_links(ref.read_text(encoding="utf-8"))
        if local_links:
            chained.append(f"{ref.name} → {local_links}")
    r.check(
        not chained,
        "references: no chained file links (one level deep only)",
        f"References link to other files: {chained}",
    )


def check_python_script(script: Path, compat: str | None, r: Results):
    src = script.read_text(encoding="utf-8")
    name = f"scripts/{script.name}"

    # Match actual input() calls; skip occurrences inside string literals or comments
    has_input = bool(re.search(r'(?m)^[^#"\']*\binput\s*\(', src))
    r.check(
        not has_input,
        f"{name}: no interactive input() calls",
        "input() call found — scripts must run fully unattended",
    )

    # PEP 723 dependency pinning
    m = re.search(r"# dependencies\s*=\s*\[([^\]]*)\]", src, re.DOTALL)
    if m:
        raw_deps = re.findall(r'"([^"]+)"|\'([^\']+)\'', m.group(1))
        deps = [a or b for a, b in raw_deps]
        unpinned = [d for d in deps if not re.search(r"[><=!~@]", d)]
        r.check(
            not unpinned,
            f"{name}: all PEP 723 dependencies are pinned",
            f"Unpinned: {unpinned} — add version specifiers like ==1.2.3",
        )

    has_network = bool(_PY_NETWORK_IMPORT_RE.search(src))
    if has_network:
        compat_declares = bool(compat) and any(
            w in compat.lower() for w in ("network", "internet", "http")
        )
        r.check(
            compat_declares,
            f"{name}: network access declared in compatibility:",
            "Makes network calls but compatibility: does not mention network/internet/http",
        )


def check_bash_script(script: Path, compat: str | None, r: Results):
    src = script.read_text(encoding="utf-8")
    name = f"scripts/{script.name}"

    # Interactive read: `read VAR` but not `read -r` (which is fine in loops reading files)
    interactive_read = re.search(r"(?<!\w)read\s+[A-Za-z_]", src)
    r.check(
        not interactive_read,
        f"{name}: no interactive read commands",
        "'read VAR' found — scripts must run fully unattended",
    )

    has_network = bool(re.search(r"\bcurl\b|\bwget\b", src))
    if has_network:
        compat_declares = bool(compat) and any(
            w in compat.lower() for w in ("network", "internet", "http")
        )
        r.check(
            compat_declares,
            f"{name}: network access declared in compatibility:",
            "Uses curl/wget but compatibility: does not mention network/internet/http",
        )


def check_scripts(skill_dir: Path, compat: str | None, r: Results):
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return
    for script in sorted(scripts_dir.iterdir()):
        if script.suffix == ".py":
            check_python_script(script, compat, r)
        elif script.suffix == ".sh":
            check_bash_script(script, compat, r)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def validate(skill_path: Path) -> Results:
    skill_md = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
    skill_dir = skill_md.parent
    r = Results()

    r.check(
        skill_md.exists(), "SKILL.md exists at skill root", f"Not found: {skill_md}"
    )
    if not skill_md.exists():
        return r

    try:
        fm, body, raw_fm = _parse_skill_md(skill_md)
    except (ValueError, yaml.YAMLError) as e:
        r.fail("SKILL.md frontmatter is valid YAML", str(e))
        return r

    check_frontmatter_formatting(raw_fm, fm, r)
    check_name(fm, skill_dir, r)
    check_description(fm, r)
    check_optional_fields(fm, r)
    check_body(body, skill_dir, r)
    check_references(skill_dir, r)
    check_scripts(skill_dir, fm.get("compatibility"), r)
    return r


def main():
    # Force UTF-8 output on Windows (avoids cp1252 encoding errors)
    if (
        isinstance(sys.stdout, io.TextIOWrapper)
        and sys.stdout.encoding.lower() != "utf-8"
    ):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__.strip())
        sys.exit(0)

    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv[1:]
    if len(args) != 1:
        print("Usage: uv run validate.py <skill-dir> [--json]", file=sys.stderr)
        sys.exit(2)

    skill_path = Path(args[0])
    if not skill_path.exists():
        print(f"Path does not exist: {skill_path}", file=sys.stderr)
        sys.exit(2)

    results = validate(skill_path)
    items = results.items
    failed = results.failed
    warnings = results.warnings

    if as_json:
        print(json.dumps(items))
    else:
        icons = {"pass": "pass", "fail": "FAIL", "warn": "warn"}
        width = 52
        print("\nAgent Skills Validator", file=sys.stderr)
        print(f"Skill: {skill_path}", file=sys.stderr)
        print("-" * width, file=sys.stderr)
        for item in items:
            print(f"  [{icons[item['level']]}]  {item['rule']}", file=sys.stderr)
            if item["detail"]:
                print(f"           {item['detail']}", file=sys.stderr)
        print("-" * width, file=sys.stderr)
        passed = len(items) - len(failed) - len(warnings)
        print(
            f"  {passed} passed, {len(failed)} failed, {len(warnings)} warnings\n",
            file=sys.stderr,
        )

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
