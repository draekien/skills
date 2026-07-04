---
name: with-ubiquitous-language
description: Builds and enforces a shared project vocabulary (a DDD ubiquitous language). Discovers bounded contexts by exploring the codebase, interviews you to surface domain terms, and tracks definitions in a project dictionary, flagging conflicts as they arise. Use when terminology feels ambiguous, or before implementing a feature that needs a shared vocabulary.
disable-model-invocation: true
---

# With Ubiquitous Language

Establish DDD ubiquitous language scoped to bounded contexts. Interview user, capture confirmed terms in `.draekien/ubiquitous-language.yaml` via scripts, detect conflicts throughout the session.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes `with-ubiquitous-language` config from `.draekien/.skillsrc`.
- **`scripts/query.py`** — Queries the ubiquitous language dictionary (`list-contexts`, `list`, `lookup`).
- **`scripts/write.py`** — Writes terms and flags/resolves ambiguities in the dictionary.
- **`scripts/migrate.py`** — Migrates legacy `UBIQUITOUS_LANGUAGE.md` files to the YAML dictionary.

## Session Start

Runs once on first invocation.

1. If the user wants the dictionary stored somewhere other than the default, confirm the path with them, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill with-ubiquitous-language set dictionaryPath <path>` before continuing. Otherwise skip straight to the next step.
2. Run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill with-ubiquitous-language get dictionaryPath --default .draekien/ubiquitous-language.yaml` to read the configured dictionary path. If `.draekien/.skillsrc` is absent the script prints the default `.draekien/ubiquitous-language.yaml`. If the script exits non-zero, fall back to the default path `.draekien/ubiquitous-language.yaml` and tell the user the config could not be read and the default path is being used.
3. Check whether the dictionary file exists at `dictionaryPath`.
   - **Exists**: load all contexts and terms into conflict detection context using `scripts/query.py list-contexts` then `scripts/query.py list <Context>` for each. If `query.py` exits non-zero or the dictionary fails to parse, tell the user the dictionary could not be read and is being treated as empty, then proceed as if no contexts were loaded. Skip to step 4.
   - **Does not exist**: scan project for any `UBIQUITOUS_LANGUAGE.md` files, excluding a top-level `UBIQUITOUS_LANGUAGE.md` at the project root (that file is a table-of-contents index, not a per-context glossary). If found, show the list and prompt user to migrate using `scripts/migrate.py`. After migration (or if none found), confirm with the user that a new dictionary will be created at `dictionaryPath`, then proceed.
4. Scan project structure. Infer a bounded context name for each candidate dir (PascalCase, domain-meaningful — exclude `utils`, `shared`, `common`). Merge with any contexts already in the dictionary. Confirm full mapping with user; apply corrections.

## Active Behaviors

Run every response after session start, concurrently.

### Interview

Ask one DDD-framed question at a time — domain events, aggregates, bounded context membership. If the question concerns project structure, naming conventions, or existing terminology (facts observable in the codebase), explore and present findings rather than asking. If it concerns intent, ownership, or business meaning, always ask the user. Continue until the user explicitly confirms they are done, or until all candidate terms surfaced during the session have confirmed definitions in the dictionary.

### Term Capture

A candidate term is a word or phrase surfaced during the Interview that has not yet been captured in the dictionary. When a candidate term is judged domain-specific — unique to this domain, not a general programming concept — and not yet defined in any loaded context:

1. Propose a definition to the user. When proposing a definition, also propose a one-sentence usage example (the `--usage` argument). Confirm both before writing. If no other terms are yet defined in the dictionary, the usage note may not reference other domain terms — write with whatever context is available. Once any other term is defined, the usage note must reference at least one defined term where the relationship is meaningful.
2. Search codebase for the term. Read surrounding context.
3. If semantic contradiction found: hard interrupt, surface the conflict, wait for resolution. If the user updates the definition, replace the proposed definition with the new one and proceed to step 4 (do not repeat step 2). If the user confirms the definition is correct, note the code divergence and proceed to step 4.
4. No contradiction: determine bounded context from the confirmed map. If ambiguous, ask.
5. Before first write to any context, confirm the bounded context assignment. If the bounded context the agent would now assign to a term differs from the bounded context it proposed during definition confirmation, re-confirm the bounded context assignment before writing.
6. Write immediately using `scripts/write.py add-term` — no batching.

See [references/ubiquitous-language-format.md](references/ubiquitous-language-format.md) for schema and full script invocation reference.

### Conflict Detection

Check every response against all loaded definitions. A term absent from the codebase is neutral — not a contradiction.

If more than one hard interrupt fires in the same response, surface only the highest-priority one and re-evaluate the rest on the next response, in this order: Definition conflict (a term already has a canonical definition being contradicted — the most authoritative signal), then Cross-context collision, then Vague language, then Term Capture's semantic contradiction.

- **Definition conflict** — user uses a defined term contradicting its stored definition: hard interrupt, surface both definitions, ask which is canonical. Run `scripts/write.py add-term` immediately on resolution.
- **Cross-context collision** — same term defined differently in two contexts: surface explicitly, ask if intentional. Both definitions stand if deliberate (DDD allows intentional ambiguity across contexts). Mark the collision as intentional in the loaded conflict-detection context so it is not re-surfaced on subsequent responses. Run `scripts/write.py flag-ambiguity` on both contexts with a note recording the intentional divergence. If not intentional, treat as a Definition conflict: ask which definition is canonical, update the incorrect context with the corrected definition, and flag the other pending review.
- **Vague language** — user word matches 2+ defined terms: hard interrupt, list matching terms with definition summaries, wait for disambiguation. Run `scripts/write.py flag-ambiguity` until resolved; run `scripts/write.py resolve-ambiguity` once canonical meaning is confirmed.
