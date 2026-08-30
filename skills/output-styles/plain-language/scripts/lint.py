#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Plain Language linter. Finds wordy, formal, and AI-flavoured writing and suggests
plainer alternatives.

Usage:
  uv run scripts/lint.py [FILE ...] [options]
  cat draft.md | uv run scripts/lint.py

Options:
  --fix             Apply the unambiguous swaps in place (stdin prints to stdout)
  --json            Emit findings as JSON instead of text
  --strict          Report warnings as errors
  --errors-only     Hide warnings
  --overrides PATH  Extra dictionary merged over the built-in one
  --config PATH     .skillsrc to read overridesPath from (default .draekien/.skillsrc)

Exit codes:
  0  no findings
  1  findings reported
  2  usage error
  3  dictionary or input unreadable
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

COPULAR_PARTICIPLES = {
    "interested", "involved", "related", "based", "located", "limited",
    "tired", "excited", "pleased", "concerned", "committed", "dedicated",
    "detailed", "mixed", "aged", "supposed", "used", "known", "given",
}

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
    merged.setdefault("allow", []).extend(extra.get("allow", []))
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


def surface_forms(term: str, replacement) -> list[tuple[str, object]]:
    """Every string that should match this entry, paired with its replacement."""
    spellings = [term] + us_variants(term)
    forms: list[tuple[str, object]] = []
    for spelling in spellings:
        forms.append((spelling, replacement))
        if " " in spelling or "-" in spelling:
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
        self.entries: dict[str, dict] = {}
        for kind, section in (("swap", "swaps"), ("candidate", "candidates")):
            for category, terms in dictionary.get(section, {}).items():
                for term, replacement in terms.items():
                    for surface, resolved in surface_forms(term, replacement):
                        key = surface.lower()
                        if key in self.entries:
                            continue
                        self.entries[key] = {
                            "kind": kind,
                            "category": category,
                            "term": term,
                            "replacement": resolved,
                        }
        ordered = sorted(self.entries, key=len, reverse=True)
        alternation = "|".join(re.escape(term).replace(r"\ ", r"\s+") for term in ordered)
        self.regex = re.compile(rf"\b(?:{alternation})\b", re.IGNORECASE) if ordered else None
        self.structures = [
            (rule["id"], re.compile(rule["pattern"]), rule["message"])
            for rule in dictionary.get("structures", [])
        ]

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


def paragraphs(text: str):
    pos = 0
    for separator in re.finditer(r"\n\s*\n", text):
        yield pos, text[pos : separator.start()]
        pos = separator.end()
    if pos < len(text):
        yield pos, text[pos:]


def analyse(text: str, matcher: Matcher, path: str) -> list[dict]:
    protected = protected_spans(text)
    findings = []

    def add(offset, span, rule, severity, category, message, suggestion):
        line, col = line_col(text, offset)
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
        add(
            match.start(),
            match.group(0),
            entry["kind"],
            "error",
            entry["category"],
            "Auto-fixable swap." if entry["kind"] == "swap" else "Pick the option that fits.",
            describe(entry),
        )

    for rule_id, regex, message in matcher.structures:
        for match in regex.finditer(text):
            if is_protected(match.start(), match.end(), protected):
                continue
            add(match.start(), match.group(0).strip(), rule_id, "warning", "structure", message, None)

    prose = prose_view(text, protected)

    for offset, sentence in sentences(prose):
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
        for match in re.finditer(
            r"\b(?:am|is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(\w+(?:ed|en))\b", stripped, re.IGNORECASE
        ):
            if match.group(1).lower() in COPULAR_PARTICIPLES:
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


def apply_fixes(text: str, matcher: Matcher) -> tuple[str, int]:
    protected = protected_spans(text)
    edits = []
    for match, entry in matcher.terms(text, protected):
        if entry["kind"] != "swap":
            continue
        edits.append((match.start(), match.end(), match.group(0), entry["replacement"]))

    applied = 0
    result = text
    for start, end, original, replacement in sorted(edits, reverse=True):
        if replacement:
            result = result[:start] + match_case(original, replacement) + result[end:]
        else:
            tail = result[end:].lstrip(" ")
            if tail[:1] in (",", ";", ":"):
                tail = tail[1:].lstrip(" ")
            if original[0].isupper() and tail[:1].isalpha():
                tail = tail[0].upper() + tail[1:]
            result = result[:start] + tail
        applied += 1
    return result, applied


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
        if not path.is_file():
            die(f"not a file: {raw}")
        with path.open("r", encoding="utf-8", newline="") as handle:
            content = handle.read()
        ending = "\r\n" if "\r\n" in content else "\n"
        inputs.append((path.as_posix(), content.replace("\r\n", "\n"), ending))
    return inputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Plain Language linter")
    parser.add_argument("paths", nargs="*", help="Files to lint; omit or use - for stdin")
    parser.add_argument("--fix", action="store_true", help="Apply unambiguous swaps in place")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON")
    parser.add_argument("--strict", action="store_true", help="Report warnings as errors")
    parser.add_argument("--errors-only", action="store_true", help="Hide warnings")
    parser.add_argument("--overrides", help="Extra dictionary merged over the built-in one")
    parser.add_argument("--config", default=".draekien/.skillsrc", help="Path to .skillsrc")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    dictionary = read_json(BUILTIN_DICTIONARY)
    extra = Path(args.overrides) if args.overrides else overrides_path(Path(args.config))
    if extra:
        if not extra.is_file():
            die(f"overrides not found: {extra}")
        dictionary = merge_dictionary(dictionary, read_json(extra))

    matcher = Matcher(dictionary)
    inputs = gather_inputs(args.paths)

    findings = []
    for path, text, ending in inputs:
        if args.fix:
            text, _ = apply_fixes(text, matcher)
            if path == "<stdin>":
                sys.stdout.write(text)
            else:
                with Path(path).open("w", encoding="utf-8", newline="") as handle:
                    handle.write(text.replace("\n", ending))
        findings.extend(analyse(text, matcher, path))

    if args.errors_only:
        findings = [f for f in findings if f["severity"] == "error"]

    if args.json:
        print(json.dumps(findings, indent=2))
    elif not (args.fix and inputs[0][0] == "<stdin>"):
        report_text(findings, args.strict)

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
