#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
Validate a generated HTML visualisation for structure, self-containment, and typography.

Usage:
    uv run scripts/validate.py <path-to-html-file>

Exit codes:
    0  all checks passed
    1  one or more checks failed
    2  usage or file error
"""

import io
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_CDN_HOSTS = {
    "cdn.tailwindcss.com",
    "cdnjs.cloudflare.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "cdn.jsdelivr.net",
    "unpkg.com",
    "d3js.org",
    "cdn.plot.ly",
    "code.highcharts.com",
}


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


class _HTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags_seen: set[str] = set()
        self.external_resources: list[tuple[str, str, int]] = []  # (url, tag, line)
        self.style_blocks: list[tuple[str, int]] = []  # (content, start_line)
        self._in_style = False
        self._style_buf: list[str] = []
        self._style_start = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag_lower = tag.lower()
        self.tags_seen.add(tag_lower)
        attrs_dict = dict(attrs)

        if tag_lower == "style":
            self._in_style = True
            self._style_buf = []
            self._style_start = self.getpos()[0]
            return

        url: str | None = None
        if tag_lower in ("script", "img", "source", "audio", "video", "embed", "iframe"):
            url = attrs_dict.get("src")
        elif tag_lower == "link":
            url = attrs_dict.get("href")

        if url:
            normalised = url if "://" in url else ("https:" + url if url.startswith("//") else None)
            if normalised and (normalised.startswith("http://") or normalised.startswith("https://")):
                host = urlparse(normalised).netloc
                if host not in ALLOWED_CDN_HOSTS:
                    self.external_resources.append((url, tag_lower, self.getpos()[0]))

    def handle_data(self, data: str):
        if self._in_style:
            self._style_buf.append(data)

    def handle_endtag(self, tag: str):
        if tag.lower() == "style":
            self._in_style = False
            self.style_blocks.append(("".join(self._style_buf), self._style_start))


def _check_font_sizes(style_content: str, style_start_line: int, r: Results):
    for i, line in enumerate(style_content.splitlines()):
        m = re.search(r"font-size\s*:\s*(\d+(?:\.\d+)?)(px|rem|em)", line, re.IGNORECASE)
        if not m:
            continue
        size, unit = float(m.group(1)), m.group(2).lower()
        too_small = (unit == "px" and size < 16) or (unit in ("rem", "em") and size < 1)
        if too_small:
            abs_line = style_start_line + i
            r.fail(
                f"typography: font-size {m.group(1)}{unit} on line ~{abs_line}",
                f"Body text minimum is 1rem (16px) — change to font-size: 1rem or larger",
            )


def validate(html_path: Path) -> Results:
    r = Results()
    content = html_path.read_text(encoding="utf-8")

    # Structure
    r.check(
        bool(re.search(r"<!DOCTYPE\s+html", content, re.IGNORECASE)),
        "structure: <!DOCTYPE html> present",
        "Missing <!DOCTYPE html> — add it as the first line of the file",
    )

    parser = _HTMLParser()
    parser.feed(content)

    for tag in ("html", "head", "body"):
        r.check(
            tag in parser.tags_seen,
            f"structure: <{tag}> tag present",
            f"Missing <{tag}> — add the required <{tag}>...</{tag}> wrapper",
        )

    # Self-containment
    if not parser.external_resources:
        r.ok("self-contained: no non-CDN external resources")
    else:
        for url, tag, line in parser.external_resources:
            host = urlparse("https:" + url if url.startswith("//") else url).netloc
            r.fail(
                f"self-contained: <{tag}> on line {line} loads from {host}",
                f"URL {url!r} is not an approved CDN — embed the resource inline or swap to "
                f"an approved CDN ({', '.join(sorted(ALLOWED_CDN_HOSTS))})",
            )

    # Typography — font-size in <style> blocks
    failures_before = len(r.failed)
    for style_content, style_line in parser.style_blocks:
        _check_font_sizes(style_content, style_line, r)
    if len(r.failed) == failures_before:
        r.ok("typography: no sub-1rem font-size in <style> blocks")

    return r


def main() -> int:
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) != 2:
        print("Usage: uv run scripts/validate.py <path-to-html-file>", file=sys.stderr)
        return 2

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"File not found: {html_path}", file=sys.stderr)
        return 2
    if html_path.suffix.lower() not in (".html", ".htm"):
        print(f"Expected an .html file, got: {html_path.suffix}", file=sys.stderr)
        return 2

    results = validate(html_path)
    items = results.items
    failed = results.failed

    width = 60
    print("\nVisualise Validator")
    print(f"File: {html_path}")
    print("-" * width)
    for item in items:
        icon = "pass" if item["passed"] else "FAIL"
        print(f"  [{icon}]  {item['rule']}")
        if item["detail"]:
            print(f"           {item['detail']}")
    print("-" * width)
    print(f"  {len(items) - len(failed)} passed, {len(failed)} failed\n")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
