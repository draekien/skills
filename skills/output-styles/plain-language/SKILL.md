---
name: plain-language
description: Switches the assistant's communication style to Plain Language — everyday words, active voice, short sentences, main point first. Use when you want clear, jargon-free writing for a general or professional audience, in replies and in artefacts, or when the user says "plain language", "plain English", "write this in plain language", "use plain language", "no jargon", "make this clearer", or asks for jargon-free or plainly worded output.
argument-hint: "[audit] [path]"
---

Read `plain-language.md` in this skill's directory and adopt the writing style it defines, ignoring its frontmatter. Stay in Plain Language until the user explicitly asks to stop — for example, "stop plain language" or "back to normal".

## The linter

`scripts/lint.py` catches the mechanical half of the style: formal words with plainer equivalents, hidden verbs, filler, corporate jargon, AI phrase structures, long sentences, dense paragraphs, and likely passive voice. Run it with any runner that supports PEP 723 inline dependencies (default `uv`). Run it from the project directory, not this skill's directory — target paths and project overrides both resolve from the working directory:

```bash
uv run scripts/lint.py [PATH ...] [--fix] [--json] [--strict] [--errors-only]
```

With no path it reads stdin. Findings come in two tiers:

- **Errors** — dictionary hits. Either a single replacement (`utilise → use`) or a set of candidates (`leverage → use | build on`). High confidence; resolve every one.
- **Warnings** — pattern heuristics. Passive voice, sentence length, paragraph density, and the AI structures. These misfire on writing that is already good, so judge each one rather than obeying it.

`--fix` applies the single-replacement swaps in place and leaves everything else alone. `--strict` reports warnings as errors, `--errors-only` hides them, `--json` emits findings as an array. Exit code 1 means the linter reported findings, not that the run failed.

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

- `--fix` rewrites files in place with no backup. Run it only on a file the user has asked to change, and only when that file is committed or otherwise recoverable, so the rewrite stays reviewable.
- `--fix` reading stdin prints the rewritten text to stdout and reports nothing. Pass a file path to get findings as well.
- The triad and em-dash rules produce the most false positives. Dismiss them freely; never contort a sentence to satisfy a heuristic.
- The linter skips fenced code, inline code, link targets, URLs, and YAML frontmatter, so linting a document full of examples is safe.
- The dictionary uses Australian spelling, and the matcher also accepts the American forms and the common word endings. Adding `utilise` covers `utilises`, `utilised`, `utilising`, and `utilized`.

## Project overrides

A project can extend the built-in dictionary with its own terms. The extra file uses the same schema as `scripts/dictionary.json` — `swaps`, `candidates`, and `allow`, where `allow` lists terms the linter must never flag:

```json
{
  "swaps": { "house": { "conveyance": "transfer" } },
  "allow": ["utilise"]
}
```

`allow` suppresses dictionary entries only, whether built-in or project-added. It has no effect on the warning-tier rules.

The linter looks for `.draekien/plain-language.json` by default, and `--overrides PATH` points it elsewhere for one run. Either way, a path that does not exist stops the run with exit code 3 rather than falling back to the built-in dictionary. To move the file permanently, read or write the `overridesPath` key:

```bash
uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill plain-language get overridesPath
```

Confirm with the user before writing to `.skillsrc`.
