#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Validate an agent skill against the Agent Skills open standard.

Usage:
    uv run validate.py <skill-dir>
    uv run validate.py <skill-dir>/SKILL.md

Exit codes:
    0  all checks passed
    1  one or more checks failed
    2  usage or parse error
"""

import io
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pyyaml not available — run with: uv run validate.py", file=sys.stderr)
    sys.exit(2)

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
    """Return (frontmatter_dict, body_str) or raise ValueError."""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("SKILL.md does not begin with YAML frontmatter (---).")
    close = text.find("\n---", 3)
    if close == -1:
        raise ValueError("SKILL.md frontmatter is never closed by a second --- line.")
    fm = yaml.safe_load(text[3:close].strip()) or {}
    body = text[close + 4 :].strip()
    return fm, body


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
        self._items.append({"passed": True, "rule": rule, "detail": ""})

    def fail(self, rule: str, detail: str):
        self._items.append({"passed": False, "rule": rule, "detail": detail})

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
        return [r for r in self._items if not r["passed"]]


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


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
        r.check(
            isinstance(allowed_tools, str),
            "allowed-tools: must be a space-separated string (not a list)",
            f'Got {type(allowed_tools).__name__} — use a quoted string like "Bash Read Write"',
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

    # Model-specific term heuristic — skip code blocks and inline code
    body_prose = _strip_code(body).lower()
    found = [t for t in _MODEL_TERMS if t in body_prose]
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
        fm, body = _parse_skill_md(skill_md)
    except (ValueError, yaml.YAMLError) as e:
        r.fail("SKILL.md frontmatter is valid YAML", str(e))
        return r

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

    if len(sys.argv) != 2:
        print("Usage: uv run validate.py <skill-dir>", file=sys.stderr)
        sys.exit(2)

    skill_path = Path(sys.argv[1])
    if not skill_path.exists():
        print(f"Path does not exist: {skill_path}", file=sys.stderr)
        sys.exit(2)

    results = validate(skill_path)
    items = results.items
    failed = results.failed

    width = 52
    print("\nAgent Skills Validator")
    print(f"Skill: {skill_path}")
    print("-" * width)
    for item in items:
        icon = "pass" if item["passed"] else "FAIL"
        print(f"  [{icon}]  {item['rule']}")
        if item["detail"]:
            print(f"           {item['detail']}")
    print("-" * width)
    print(f"  {len(items) - len(failed)} passed, {len(failed)} failed\n")

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
