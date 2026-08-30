---
name: plain-language
description: Switches the assistant's communication style to Plain Language — everyday words, active voice, short sentences, main point first. Use when you want clear, jargon-free writing for a general or professional audience, in replies and in artefacts, or when the user says "plain language", "plain English", "write this in plain language", "use plain language", "no jargon", "make this clearer", or asks for jargon-free or plainly worded output.
argument-hint: "[audit] [path]"
---

Read `plain-language.md` in this skill's directory and adopt the writing style it defines, ignoring its frontmatter. Stay in Plain Language until the user explicitly asks to stop — for example, "stop plain language" or "back to normal".

## The linter

`scripts/lint.py` catches the mechanical half of the style: formal words with plainer equivalents, hidden verbs, filler, corporate jargon, AI phrase structures, long sentences, dense paragraphs, and likely passive voice. Run it with any runner that supports PEP 723 inline dependencies (default `uv`). Run it from the project directory, not this skill's directory. Target paths and project overrides both resolve from the working directory.

```bash
uv run scripts/lint.py [PATH ...] [--fix [--dry-run]] [--json] [--strict] [--errors-only] [--disable-rule IDS]
```

A path is a file or a directory. The linter walks a directory for `.md`, `.markdown`, `.mdx`, `.txt`, and `.rst` files. With no path it reads stdin. Findings come in two tiers:

- **Errors** — dictionary hits. Either a single replacement (`utilise → use`) or a set of candidates (`leverage → use | build on`). High confidence; resolve every one.
- **Warnings** — pattern heuristics. Passive voice, sentence length, paragraph density, and the AI structures. These misfire on writing that is already good, so judge each one rather than obeying it.

`--fix` applies the single-replacement swaps in place and leaves everything else alone. Add `--dry-run` to see those swaps as a list and write nothing — same file, line, and column as a finding, plus the replacement. It exits 1 when swaps are pending, so it works as a check. With `--json` it emits `{ "fixes": [...], "findings": [...] }` rather than a bare findings array. `--dry-run` on its own is a usage error. `--strict` reports warnings as errors, `--errors-only` hides them, `--disable-rule triad,em-dash-pivot` switches named rules off, and `--json` emits findings as an array. Exit code 1 means the linter reported findings, not that the run failed.

## Suppressing a finding

Three levers, narrowest first:

| Lever | Effect |
|---|---|
| `<!-- plain-language-ignore -->` | Skips the next non-blank line |
| `<!-- plain-language-ignore-file -->` | Skips the whole file |
| `--disable-rule IDS` | Switches named rules off for the run |

Reach for a suppression comment when a specific line is right as written. Reach for `--disable-rule` only when a rule is wrong for the whole document.

## Self-check

After writing any prose artefact to disk — a doc, email, report, or spec — run the linter over it before saying the work is done. Source code, config, and data files are out of scope, even when they contain prose in comments.

1. Run `--fix` on the file to clear the unambiguous swaps.
2. Re-read the remaining findings and rewrite where the change genuinely improves the sentence. Leave a finding alone when the flagged wording is the clearest option.
3. Tell the user in one line what changed, naming anything deliberately left as-is.

Done after resolving or deliberately keeping every error, and reading every warning to either act on it or dismiss it. This applies to files written, never to replies in conversation — the style already governs those.

## Audit

When the user hands over text and asks what is wrong with it, run the linter without `--fix`, then read the text yourself for what patterns cannot see. Report both together, most damaging first, and offer a rewrite of the worst passages.

## What the linter cannot judge

Patterns see words, not arguments. Judge these directly on every audit and self-check:

- **Main point first** — whether the answer, decision, or recommendation leads, or sits buried under background.
- **The right technical term** — the style keeps precise terms and defines them once. A word the linter flags may be exactly right for the audience.
- **Structure** — whether content with real structure is set out as a list, heading, or table rather than as prose.
- **What is missing** — detail the reader needs that the draft never supplies.

## Gotchas

- `--fix` rewrites files in place with no backup. Run it only on a file the user has asked to change, and only when that file is committed or otherwise recoverable, so the rewrite stays reviewable. On a file that is not recoverable, run `--fix --dry-run` first and read the list.
- `--fix` reading stdin prints the rewritten text to stdout and reports nothing. Pass a file path to get findings as well.
- The triad and em-dash rules produce the most false positives. Dismiss them freely; never contort a sentence to satisfy a heuristic.
- The linter skips fenced code, inline code, link targets, URLs, and YAML frontmatter, so linting a document full of examples is safe.
- The dictionary uses Australian spelling, and the matcher also accepts the American forms and the common word endings. Adding `utilise` covers `utilises`, `utilised`, `utilising`, and `utilized`.
- The matcher generates word endings by rule, so an irregular verb in a replacement produces a wrong form. Set `"inflect": false` on the entry and add the forms you need as separate entries.
- A few dictionary terms carry a second, technical sense the matcher cannot see: `implement` (an interface or trait), `component` (a tuple or UI component), and `additional` (`AdditionalFiles` and similar identifiers). In a software docs repo, start the project overrides with `"allow": ["implement", "component", "additional"]` rather than dismissing each hit by hand.
- A term whose two senses are spelled the same belongs in `candidates`, not `swaps`, however confident the replacement looks. `underscores` sits there because `--fix` would otherwise turn "use underscores between words" into "use stresses between words".
- Filler is never deleted after a negator, because `not very good` and `not good` mean different things. The linter stays silent there rather than reporting a fix it cannot safely make.

## Project overrides

A project can extend the built-in dictionary with its own terms. The extra file uses the same schema as `scripts/dictionary.json`: `swaps`, `candidates`, `structures`, `sentenceBoundaries`, `allow`, and `disable`.

```json
{
  "swaps": {
    "house": {
      "conveyance": "transfer",
      "seek": { "replacement": "look for", "inflect": false },
      "settle": { "replacement": "complete", "notFollowedBy": "\\b(?:date|statement)" }
    }
  },
  "sentenceBoundaries": [{ "id": "docusaurus-container", "pattern": "^\\s*:::" }],
  "allow": ["utilise"],
  "disable": ["triad", "em-dash-pivot", "boundary-jsx"]
}
```

An entry written as an object takes exactly four keys: `replacement`, `inflect`, `notPrecededBy`, and `notFollowedBy`. Any other key stops the run with exit code 3, so a typo fails loudly instead of silently doing nothing. The last two are guards: a regex tested against the text immediately before or after the match, where a hit drops the finding. Use a guard when a term has two senses and the neighbouring word tells them apart — the built-in `very` entry skips `the very X`, and `the user` skips `the user does not exist`. **Write a guard unanchored.** The linter adds the anchor that binds it to the match; a pattern starting with `^` or ending with `$` is rejected rather than quietly never firing.

`sentenceBoundaries` is a list of `{ "id", "pattern" }` objects, each pattern matched against the start of each line. They control where the `long-sentence` and `passive-voice` rules stop reading, so hard-wrapped prose still joins into one sentence while markup does not. A pattern that matches the whole line — `{% ... %}` block tags, HTML comments, JSX tags — drops that line from the prose. A pattern that matches only a prefix — a list marker, a blockquote `>` — starts a new sentence at that line. Project patterns add to the built-in list; to switch a built-in off, put its id in `disable` alongside the rule ids. The built-ins are `boundary-block-tag`, `boundary-comment`, `boundary-jsx`, `boundary-list-item`, and `boundary-blockquote`. Headings, table rows, and fenced code are already excluded before boundaries run, so they need no pattern.

The two switches cover different things. `allow` takes terms and suppresses dictionary entries, built-in or project-added. `disable` takes rule ids — the warning-tier rules, such as `triad`, `passive-voice`, `long-sentence`, `dense-paragraph`, `ai-phrase`, and every structure id the `--json` output names. Re-using a built-in term as a key replaces its replacement rather than adding a second entry.

The linter looks for `.draekien/plain-language.json` by default, and `--overrides PATH` points it elsewhere for one run. Either way, a path that does not exist stops the run with exit code 3 rather than falling back to the built-in dictionary. To move the file permanently, read or write the `overridesPath` key:

```bash
uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill plain-language get overridesPath
```

Confirm with the user before writing to `.skillsrc`.
