---
name: extract-llms-txt
description: Produces an llms.txt-format index of a library, framework, SDK, or documentation site, for the agent to consult before touching that area of the codebase. Searches for an official llms.txt or llms-full.txt first and adapts it if found; otherwise crawls the docs site and compiles an index from scratch. Use when the user says "extract llms.txt", "index the docs for X", "make an llms.txt for X", "create a docs index for X", or asks to summarise a documentation site into a reference file.
argument-hint: "[docs-url-or-topic] [output-path]"
---

# Extract an llms.txt index

Produce a concise, link-based index of a documentation site in the [llms.txt](https://llmstxt.org/#proposal) format, so a future agent can scan it in one read and pull only the pages a task needs — instead of crawling the site cold every time.

## Resolve scope before fetching anything

Pin down three things:

- **The docs root** — a URL the user gave, or the official docs site for the named library/framework/SDK.
- **The boundary** — the whole site, or one section of it (e.g. "just the Agent SDK pages," not the entire product's docs). A narrower boundary produces a tighter, more useful index; when the user names a subsection, hold to it even if a wider official index exists.
- **The output path** — where the project keeps these indexes. Check for an existing convention first: a `docs/llms/` directory, a reference doc pointing at prior indexes, or a mention in the project's standing agent-instructions file. Match that convention (directory, filename style) rather than inventing a new one; if none exists, `docs/llms/<slug>.txt` is a reasonable default.

Call this combination of docs root + boundary the **resolved boundary** for the rest of this skill — every later step (searching, crawling, writing) operates against it.

If the docs root can't be fetched at all — blocked, JS-only render, auth-gated — stop and tell the user rather than fabricating an index from memory.

## Search for an official index first

Before crawling by hand, check whether the site already publishes one:

1. Try `<root>/llms.txt` and `<root>/llms-full.txt` directly.
2. If the docs root has a deeper path (e.g. `example.com/docs/en/product/overview`), also try it at the site root (`example.com/llms.txt`) and at the nearest parent path (`example.com/docs/llms.txt`) — official indexes are usually published once per site or per docs root, not per page.
3. Read the first fetched page itself: docs sites sometimes point to their own index inline (a note, a footer link, a `<link>` tag) rather than at a predictable path.

If an official index exists, prefer adapting it over crawling by hand — it's already curated and its descriptions come from the source. Fetch it and filter its entries down to the resolved boundary: keep only the lines whose URL falls under the section the user asked for, in the same format found. If it covers the whole site and the boundary is narrower, extract the matching subset rather than passing through the whole file — an index padded with out-of-scope entries costs the reading agent more than it saves.

If no official index exists at any of the above, crawl the boundary by hand.

## Crawl the boundary by hand

When no official index is available:

1. Fetch the root/overview page of the resolved boundary. Read it for two things: an overall one-paragraph description of what the product/library/section *is*, and any on-page navigation, sidebar, or "next steps" links into the rest of the boundary.
2. If the boundary's page count is not obvious from the overview page's links alone, fetch a sitemap or table-of-contents page if the site has one, to get the full page list. If neither exists, proceed with only the links reachable by following on-page navigation from the overview page, and flag in the review that coverage may be partial.
3. For every page inside the boundary, capture: its title, its canonical URL, and a one-line description. Prefer the description already given by the site (a subtitle, a meta description, a card blurb) over writing a new one — it's the source's own framing, not a paraphrase that can drift from it.
4. Prefer the plain-markdown form of each URL when the site serves one (many docs platforms serve raw markdown at the same path with a `.md` suffix) — it's cheaper for a future agent to fetch than the rendered HTML page.

## Write the index

Follow the llms.txt structure exactly:

```markdown
# Title

> One-sentence blockquote summary of what this is and why it matters for this project.

- [Page title](url): one-line description of the page's content.
- [Page title](url): one-line description of the page's content.

## Optional

- [Rarely-needed page title](url): one-line description.
```

- The H1 title and blockquote summary describe the *whole index* — the product/library/section, not any one page. If the index feeds a specific project, the summary should say why this doc set matters to that project (what it's used for, which ADR or decision references it), the same way an existing convention in the project does.
- Group entries under `##` section headings that mirror the source site's own grouping (by topic, by lifecycle stage) rather than an arbitrary alphabetical or crawl-order list — a reader scanning headings should recognise the site's own shape. If a section would otherwise become one long flat list, split it into finer subheadings that mirror the site's own deeper navigation rather than leaving it unbroken.
- Reserve an `## Optional` section, per the llms.txt convention, for pages that are unlikely to matter for the resolved boundary's purpose (deprecated/removed features, edge-case references) — pages worth listing for completeness but safe to skip on a normal read.
- One entry per page, each as `- [title](url): description` — no nested bullets, no additional prose between entries.

## Wire it into the project

If the project has an existing convention for referencing these indexes (commonly a line in its standing agent-instructions file pointing at each `docs/llms/*.txt` file, telling the agent when to consult it), add a matching entry for the new index — same phrasing style, same trigger condition pattern ("consult before making changes to X"). If no such convention exists yet, ask the user whether they want one added rather than inventing a new documentation-reference pattern unprompted.

## Completion criteria

Every page inside the resolved boundary appears exactly once, with a title and description sourced from the docs (not invented), and every link resolves to a real page. The file passes as a drop-in replacement for crawling the site cold: a future agent reading only this index, with no further fetches, can tell which single page to open for a given sub-task.
