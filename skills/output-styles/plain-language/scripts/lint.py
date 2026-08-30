#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Plain Language linter. Finds wordy, formal, and AI-flavoured writing and suggests
plainer alternatives.

Usage:
  uv run scripts/lint.py [PATH ...] [options]
  cat draft.md | uv run scripts/lint.py

A PATH may be a file or a directory; directories are walked for prose files.

Options:
  --fix               Apply the unambiguous swaps in place (stdin prints to stdout)
  --dry-run           With --fix, list the swaps it would make and write nothing
  --json              Emit findings as JSON instead of text
  --strict            Report warnings as errors
  --errors-only       Hide warnings
  --disable-rule IDS  Comma-separated rule or boundary ids to switch off
  --overrides PATH    Extra dictionary merged over the built-in one
  --config PATH       .skillsrc to read overridesPath from (default .draekien/.skillsrc)

Suppression comments:
  <!-- plain-language-ignore -->        skips the next non-blank line
  <!-- plain-language-ignore-file -->   skips the whole file

Exit codes:
  0  no findings
  1  findings reported
  2  usage error
  3  dictionary, overrides, or input unusable
"""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
BUILTIN_DICTIONARY = SCRIPT_DIR / "dictionary.json"
SKILL_NAME = "plain-language"
DEFAULT_OVERRIDES = ".draekien/plain-language.json"

LONG_SENTENCE_WORDS = 30
DENSE_PARAGRAPH_SENTENCES = 5
DENSE_PARAGRAPH_WORDS = 120

IRREGULAR = {
    "have": ("has", "had", "having"),
    "get": ("gets", "got", "getting"),
    "buy": ("buys", "bought", "buying"),
    "give": ("gives", "gave", "giving"),
    "tell": ("tells", "told", "telling"),
    "keep": ("keeps", "kept", "keeping"),
    "let": ("lets", "let", "letting"),
    "go": ("goes", "went", "going"),
    "make": ("makes", "made", "making"),
    "take": ("takes", "took", "taking"),
    "hold": ("holds", "held", "holding"),
    "come": ("comes", "came", "coming"),
    "do": ("does", "did", "doing"),
    "pay": ("pays", "paid", "paying"),
    "say": ("says", "said", "saying"),
    "find": ("finds", "found", "finding"),
    "send": ("sends", "sent", "sending"),
    "speed": ("speeds", "sped", "speeding"),
    "run": ("runs", "ran", "running"),
    "be": ("is", "was", "being"),
}

BE_COMPLEMENTS = {
    "interested", "involved", "related", "based", "located", "limited",
    "tired", "excited", "pleased", "concerned", "committed", "dedicated",
    "detailed", "mixed", "aged", "supposed", "used", "known", "given",
    "open", "closed", "unchanged", "unaffected", "often", "golden",
    "sudden", "wooden",
}

ADVERBS = (
    r"\w+ly|often|always|never|sometimes|seldom|rarely|still|already|"
    r"now|then|also|just|even|only|not|no longer|therefore|thus"
)

PASSIVE = re.compile(
    rf"\b(?:am|is|are|was|were|be|been|being)\s+(?:(?:{ADVERBS})\s+)*(\w+(?:ed|en))\b",
    re.IGNORECASE,
)

TABLE_PLACEHOLDER = re.compile(r"(?<=\|)\s*[—–]\s*(?=\||$)", re.MULTILINE)

ENTRY_OPTIONS = {"replacement", "inflect", "notPrecededBy", "notFollowedBy"}

NEGATORS = {"not", "n't", "never", "hardly", "scarcely", "barely", "no", "nor", "without"}

PROSE_SUFFIXES = {".md", ".markdown", ".txt", ".mdx", ".rst"}
SKIP_DIRS = {"node_modules", ".git", ".venv", "__pycache__", "dist", "build"}

IGNORE_LINE = re.compile(r"<!--\s*plain-language-ignore\s*-->")
IGNORE_FILE = re.compile(r"<!--\s*plain-language-ignore-file\s*-->")

PROTECTED_PATTERNS = (
    re.compile(r"\A---\n.*?\n---\n", re.DOTALL),
    re.compile(r"^(```|~~~).*?^\1", re.DOTALL | re.MULTILINE),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"https?://\S+"),
    re.compile(r"\]\([^)]*\)"),
)


def die(message: str, code: int = 3) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(code)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as e:
        die(f"could not read {path}: {e}")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON: {e}")
    return {}


def merge_dictionary(base: dict, extra: dict) -> dict:
    merged = json.loads(json.dumps(base))
    for section in ("swaps", "candidates"):
        for category, entries in extra.get(section, {}).items():
            merged.setdefault(section, {}).setdefault(category, {}).update(entries)
    merged.setdefault("structures", []).extend(extra.get("structures", []))
    merged.setdefault("sentenceBoundaries", []).extend(extra.get("sentenceBoundaries", []))
    merged.setdefault("allow", []).extend(extra.get("allow", []))
    merged.setdefault("disable", []).extend(extra.get("disable", []))
    return merged


def overrides_path(config_path: Path) -> Path | None:
    if not config_path.exists():
        candidate = Path(DEFAULT_OVERRIDES)
        return candidate if candidate.exists() else None
    data = read_json(config_path)
    configured = data.get(SKILL_NAME, {}).get("overridesPath")
    if configured:
        candidate = Path(configured)
        if not candidate.exists():
            die(f"overridesPath in {config_path} points at a missing file: {candidate}")
        return candidate
    candidate = Path(DEFAULT_OVERRIDES)
    return candidate if candidate.exists() else None


def us_variants(term: str) -> list[str]:
    out = []
    for suffix, replacement in (("isation", "ization"), ("ise", "ize"), ("yse", "yze"), ("our", "or")):
        if term.endswith(suffix):
            out.append(term[: -len(suffix)] + replacement)
            break
    return out


def inflect(word: str, form: str) -> str:
    if word in IRREGULAR:
        return IRREGULAR[word][{"s": 0, "ed": 1, "ing": 2}[form]]
    if form == "s":
        if re.search(r"(s|x|z|ch|sh)$", word):
            return word + "es"
        if re.search(r"[^aeiou]y$", word):
            return word[:-1] + "ies"
        return word + "s"
    if form == "ed":
        if word.endswith("e"):
            return word + "d"
        if re.search(r"[^aeiou]y$", word):
            return word[:-1] + "ied"
        return word + "ed"
    if word.endswith("e"):
        return word[:-1] + "ing"
    return word + "ing"


def inflect_phrase(phrase: str, form: str) -> str:
    if not phrase:
        return phrase
    head, _, tail = phrase.partition(" ")
    inflected = inflect(head, form)
    return f"{inflected} {tail}".strip() if tail else inflected


def compile_guard(term: str, option: str, pattern: str | None, before: bool):
    """A guard pattern anchored to the text immediately beside a match."""
    if not pattern:
        return None
    if pattern.startswith("^") or pattern.endswith("$"):
        die(f"{term}: {option} must be unanchored; the linter anchors it beside the match")
    anchored = rf"(?:{pattern})\W*$" if before else rf"^\W*(?:{pattern})"
    try:
        return re.compile(anchored, re.IGNORECASE)
    except re.error as e:
        die(f"{term}: invalid {option} pattern {pattern!r}: {e}")
    return None


def parse_entry(term: str, value) -> tuple[object, bool, dict]:
    """An entry is a replacement string, a candidate list, or an object with options."""
    if not isinstance(value, dict):
        return value, True, {"not_preceded": None, "not_followed": None}
    unknown = set(value) - ENTRY_OPTIONS
    if unknown:
        die(f"{term}: unknown entry option(s) {', '.join(sorted(unknown))}; expected {', '.join(sorted(ENTRY_OPTIONS))}")
    guards = {
        "not_preceded": compile_guard(term, "notPrecededBy", value.get("notPrecededBy"), before=True),
        "not_followed": compile_guard(term, "notFollowedBy", value.get("notFollowedBy"), before=False),
    }
    return value.get("replacement", ""), value.get("inflect", True), guards


def surface_forms(term: str, replacement, inflect_forms: bool = True) -> list[tuple[str, object]]:
    """Every string that should match this entry, paired with its replacement."""
    spellings = [term] + us_variants(term)
    forms: list[tuple[str, object]] = []
    for spelling in spellings:
        forms.append((spelling, replacement))
        if not inflect_forms or " " in spelling or "-" in spelling:
            continue
        for form in ("s", "ed", "ing"):
            variant = inflect(spelling, form)
            if variant == spelling:
                continue
            if isinstance(replacement, list):
                inflected = [inflect_phrase(option, form) for option in replacement]
            elif replacement:
                inflected = inflect_phrase(replacement, form)
            else:
                inflected = replacement
            forms.append((variant, inflected))
    return forms


class Matcher:
    def __init__(self, dictionary: dict):
        self.allow = {term.lower() for term in dictionary.get("allow", [])}
        self.disabled = {rule.lower() for rule in dictionary.get("disable", [])}
        self.entries: dict[str, dict] = {}
        for kind, section in (("swap", "swaps"), ("candidate", "candidates")):
            for category, terms in dictionary.get(section, {}).items():
                for term, value in terms.items():
                    replacement, inflect_forms, guards = parse_entry(term, value)
                    for surface, resolved in surface_forms(term, replacement, inflect_forms):
                        key = surface.lower()
                        if key in self.entries:
                            continue
                        self.entries[key] = {
                            "kind": kind,
                            "category": category,
                            "term": term,
                            "replacement": resolved,
                            **guards,
                        }
        ordered = sorted(self.entries, key=len, reverse=True)
        alternation = "|".join(re.escape(term).replace(r"\ ", r"\s+") for term in ordered)
        self.regex = re.compile(rf"\b(?:{alternation})\b", re.IGNORECASE) if ordered else None
        self.structures = [
            (rule["id"], re.compile(rule["pattern"]), rule["message"])
            for rule in dictionary.get("structures", [])
        ]
        self.boundaries = []
        for boundary in dictionary.get("sentenceBoundaries", []):
            if not isinstance(boundary, dict) or "id" not in boundary or "pattern" not in boundary:
                die(f"sentenceBoundaries entries need an id and a pattern: {boundary!r}")
            if boundary["id"].lower() in self.disabled:
                continue
            try:
                self.boundaries.append(re.compile(boundary["pattern"]))
            except re.error as e:
                die(f"invalid sentenceBoundaries pattern {boundary['pattern']!r}: {e}")

    def terms(self, text: str, protected):
        if not self.regex:
            return
        for match in self.regex.finditer(text):
            if is_protected(match.start(), match.end(), protected):
                continue
            key = re.sub(r"\s+", " ", match.group(0).lower())
            entry = self.entries.get(key)
            if entry is None or key in self.allow or entry["term"].lower() in self.allow:
                continue
            before = text[max(0, match.start() - 40) : match.start()]
            after = text[match.end() : match.end() + 40]
            if entry["not_preceded"] and entry["not_preceded"].search(before):
                continue
            if entry["not_followed"] and entry["not_followed"].search(after):
                continue
            yield match, entry


def is_protected(start: int, end: int, protected) -> bool:
    return any(p_start <= start and end <= p_end for p_start, p_end in protected)


def protected_spans(text: str) -> list[tuple[int, int]]:
    spans = []
    for pattern in PROTECTED_PATTERNS:
        spans.extend((m.start(), m.end()) for m in pattern.finditer(text))
    return spans


def prose_view(text: str, protected) -> str:
    """Text with code, links, headings, and tables blanked out, offsets preserved."""
    chars = list(text)
    for start, end in protected:
        for i in range(start, min(end, len(chars))):
            if chars[i] != "\n":
                chars[i] = " "
    blanked = "".join(chars)
    lines = blanked.split("\n")
    for index, line in enumerate(lines):
        if line.lstrip().startswith(("#", "|", "```", "~~~")):
            lines[index] = " " * len(line)
    return "\n".join(lines)


def negated(text: str, start: int) -> bool:
    """True when a negator sits immediately before this offset, so deleting flips sense."""
    preceding = text[max(0, start - 40) : start]
    words = re.findall(r"[\w']+", preceding.lower())
    return bool(words) and (words[-1] in NEGATORS or words[-1].endswith("n't"))


def suppressions(text: str) -> tuple[bool, set[int]]:
    """Whole-file skip flag, and the line numbers an ignore comment covers."""
    if IGNORE_FILE.search(text):
        return True, set()
    lines = text.split("\n")
    covered = set()
    for index, line in enumerate(lines):
        if not IGNORE_LINE.search(line):
            continue
        for offset in range(index + 1, len(lines)):
            if lines[offset].strip():
                covered.add(offset + 1)
                break
    return False, covered


def line_col(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    col = offset - (text.rfind("\n", 0, offset) + 1) + 1
    return line, col


def match_case(source: str, replacement: str) -> str:
    if not replacement:
        return replacement
    if source.isupper() and len(source) > 1:
        return replacement.upper()
    if source[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def describe(entry: dict) -> str:
    replacement = entry["replacement"]
    if isinstance(replacement, list):
        return " | ".join(replacement)
    return replacement if replacement else "(delete)"


def sentences(text: str):
    start = 0
    for match in re.finditer(r"[.!?](?=\s|$)", text):
        yield start, text[start : match.end()]
        start = match.end() + 1
    if start < len(text):
        yield start, text[start:]


def segments(text: str, boundaries) -> list[tuple[int, str]]:
    """Prose split at block boundaries, so a sentence never spans two blocks."""
    found: list[tuple[int, str]] = []
    start = 0
    lines: list[str] = []
    offset = 0
    for line in text.split("\n"):
        hits = [match for match in (pattern.match(line) for pattern in boundaries) if match]
        markup = any(match.end() >= len(line.rstrip()) for match in hits)
        if hits or not line.strip():
            if lines:
                found.append((start, "\n".join(lines)))
                lines = []
            if hits and not markup:
                start = offset
                lines = [line]
        else:
            if not lines:
                start = offset
            lines.append(line)
        offset += len(line) + 1
    if lines:
        found.append((start, "\n".join(lines)))
    return found


def paragraphs(text: str):
    pos = 0
    for separator in re.finditer(r"\n\s*\n", text):
        yield pos, text[pos : separator.start()]
        pos = separator.end()
    if pos < len(text):
        yield pos, text[pos:]


def analyse(text: str, matcher: Matcher, path: str) -> list[dict]:
    protected = protected_spans(text)
    prose = prose_view(text, protected)
    skip_file, ignored_lines = suppressions(prose)
    if skip_file:
        return []
    findings = []

    def add(offset, span, rule, severity, category, message, suggestion):
        if rule in matcher.disabled:
            return
        line, col = line_col(text, offset)
        if line in ignored_lines:
            return
        findings.append({
            "file": path,
            "line": line,
            "column": col,
            "rule": rule,
            "severity": severity,
            "category": category,
            "text": span,
            "suggestion": suggestion,
            "message": message,
        })

    for match, entry in matcher.terms(text, protected):
        if not entry["replacement"] and negated(text, match.start()):
            continue
        add(
            match.start(),
            match.group(0),
            entry["kind"],
            "error",
            entry["category"],
            "Auto-fixable swap." if entry["kind"] == "swap" else "Pick the option that fits.",
            describe(entry),
        )

    structural = TABLE_PLACEHOLDER.sub(lambda m: " " * len(m.group(0)), text)
    for rule_id, regex, message in matcher.structures:
        for match in regex.finditer(structural):
            if is_protected(match.start(), match.end(), protected):
                continue
            add(match.start(), match.group(0).strip(), rule_id, "warning", "structure", message, None)

    for base, block in segments(prose, matcher.boundaries):
        for offset, sentence in sentences(block):
            offset += base
            stripped = sentence.strip()
            if not stripped:
                continue
            offset += len(sentence) - len(sentence.lstrip())
            words = re.findall(r"\b[\w'-]+\b", stripped)
            if len(words) > LONG_SENTENCE_WORDS:
                add(
                    offset, stripped[:60], "long-sentence", "warning", "readability",
                    f"{len(words)} words. Split it so each sentence carries one idea.", None,
                )
            for match in PASSIVE.finditer(stripped):
                if match.group(1).lower() in BE_COMPLEMENTS:
                    continue
                add(
                    offset + match.start(), match.group(0), "passive-voice", "warning", "voice",
                    "Likely passive. Name who acts.", None,
                )

    for offset, block in paragraphs(prose):
        stripped = block.strip()
        if not stripped or stripped.startswith(("-", "*", "|", "#", ">")):
            continue
        count = len(list(sentences(stripped)))
        words = len(re.findall(r"\b[\w'-]+\b", stripped))
        if count > DENSE_PARAGRAPH_SENTENCES and words > DENSE_PARAGRAPH_WORDS:
            add(
                offset, stripped[:60], "dense-paragraph", "warning", "readability",
                f"{count} sentences, {words} words. Break it up or use a list.", None,
            )

    findings.sort(key=lambda f: (f["line"], f["column"]))
    return findings


def plan_fixes(text: str, matcher: Matcher, path: str) -> list[dict]:
    """Every swap --fix would apply, in document order."""
    protected = protected_spans(text)
    skip_file, ignored_lines = suppressions(prose_view(text, protected))
    if skip_file:
        return []
    planned = []
    for match, entry in matcher.terms(text, protected):
        if entry["kind"] != "swap":
            continue
        if not entry["replacement"] and negated(text, match.start()):
            continue
        line, col = line_col(text, match.start())
        if line in ignored_lines:
            continue
        planned.append({
            "file": path,
            "line": line,
            "column": col,
            "start": match.start(),
            "end": match.end(),
            "text": match.group(0),
            "replacement": entry["replacement"],
        })
    return planned


def apply_fixes(text: str, planned: list[dict]) -> str:
    result = text
    for edit in sorted(planned, key=lambda e: e["start"], reverse=True):
        start, end, original, replacement = edit["start"], edit["end"], edit["text"], edit["replacement"]
        if replacement:
            result = result[:start] + match_case(original, replacement) + result[end:]
        else:
            tail = result[end:].lstrip(" ")
            if tail[:1] in (",", ";", ":"):
                tail = tail[1:].lstrip(" ")
            if original[0].isupper() and tail[:1].isalpha():
                tail = tail[0].upper() + tail[1:]
            result = result[:start] + tail
    return result


def report_fixes(planned: list[dict]) -> None:
    for edit in planned:
        replacement = match_case(edit["text"], edit["replacement"]) if edit["replacement"] else "(delete)"
        print(f'{edit["file"]}:{edit["line"]}:{edit["column"]}  fix  "{edit["text"]}" → {replacement}')
    files = len({edit["file"] for edit in planned})
    print(f"\n{len(planned)} fix(es) would be applied across {files} file(s)")


def report_text(findings: list[dict], strict: bool) -> None:
    for finding in findings:
        severity = "error" if strict else finding["severity"]
        location = f"{finding['file']}:{finding['line']}:{finding['column']}"
        suggestion = f' → {finding["suggestion"]}' if finding["suggestion"] else ""
        print(f'{location}  {severity}  {finding["rule"]}  "{finding["text"]}"{suggestion}')
        print(f"    {finding['message']}")
    errors = sum(1 for f in findings if f["severity"] == "error" or strict)
    warnings = len(findings) - errors
    files = len({f["file"] for f in findings})
    print(f"\n{errors} error(s), {warnings} warning(s) across {files} file(s)")


def gather_inputs(paths: list[str]) -> list[tuple[str, str, str]]:
    """Each input as (path, text normalised to \\n, the file's own line ending)."""
    if not paths or paths == ["-"]:
        return [("<stdin>", sys.stdin.read(), "\n")]
    inputs = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            targets = sorted(
                child
                for child in path.rglob("*")
                if child.suffix.lower() in PROSE_SUFFIXES
                and child.is_file()
                and not any(part in SKIP_DIRS or part.startswith(".") for part in child.parts)
            )
        elif path.is_file():
            targets = [path]
        else:
            die(f"no such file or directory: {raw}")
            targets = []
        for target in targets:
            with target.open("r", encoding="utf-8", newline="") as handle:
                content = handle.read()
            ending = "\r\n" if "\r\n" in content else "\n"
            inputs.append((target.as_posix(), content.replace("\r\n", "\n"), ending))
    return inputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Plain Language linter")
    parser.add_argument("paths", nargs="*", help="Files or directories; omit or use - for stdin")
    parser.add_argument("--fix", action="store_true", help="Apply unambiguous swaps in place")
    parser.add_argument("--dry-run", action="store_true", help="With --fix, list the swaps instead of writing them")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON")
    parser.add_argument("--strict", action="store_true", help="Report warnings as errors")
    parser.add_argument("--errors-only", action="store_true", help="Hide warnings")
    parser.add_argument("--disable-rule", default="", help="Comma-separated rule or boundary ids to switch off")
    parser.add_argument("--overrides", help="Extra dictionary merged over the built-in one")
    parser.add_argument("--config", default=".draekien/.skillsrc", help="Path to .skillsrc")
    args = parser.parse_args()

    if args.dry_run and not args.fix:
        parser.error("--dry-run only means something with --fix")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    dictionary = read_json(BUILTIN_DICTIONARY)
    extra = Path(args.overrides) if args.overrides else overrides_path(Path(args.config))
    if extra:
        if not extra.is_file():
            die(f"overrides not found: {extra}")
        dictionary = merge_dictionary(dictionary, read_json(extra))

    if args.disable_rule:
        dictionary.setdefault("disable", []).extend(
            rule.strip() for rule in args.disable_rule.split(",") if rule.strip()
        )

    matcher = Matcher(dictionary)
    inputs = gather_inputs(args.paths)

    findings = []
    planned = []
    for path, text, ending in inputs:
        if args.fix:
            edits = plan_fixes(text, matcher, path)
            planned.extend(edits)
            text = apply_fixes(text, edits)
            if not args.dry_run:
                if path == "<stdin>":
                    sys.stdout.write(text)
                else:
                    with Path(path).open("w", encoding="utf-8", newline="") as handle:
                        handle.write(text.replace("\n", ending))
        findings.extend(analyse(text, matcher, path))

    if args.errors_only:
        findings = [f for f in findings if f["severity"] == "error"]

    if args.json and args.dry_run:
        print(json.dumps({"fixes": planned, "findings": findings}, indent=2))
    elif args.json:
        print(json.dumps(findings, indent=2))
    else:
        if args.dry_run:
            report_fixes(planned)
        if not (args.fix and not args.dry_run and inputs[0][0] == "<stdin>"):
            report_text(findings, args.strict)

    return 1 if findings or (args.dry_run and planned) else 0


if __name__ == "__main__":
    sys.exit(main())
