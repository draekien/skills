---
name: get-specific
description: Builds and enforces a DDD ubiquitous language for a project. Discovers bounded contexts by exploring the codebase, interviews users to surface domain terms, tracks definitions in a centralised YAML dictionary inside .draekien/, and detects terminology conflicts in real time. Use when terminology feels ambiguous, before implementing features, or when the user says "get specific", "define our terms", "what do we mean by X", or wants to establish shared vocabulary before acting.
---

# Get Specific

Establish DDD ubiquitous language scoped to bounded contexts. Interview user, capture confirmed terms in `.draekien/ubiquitous-language.yaml` via scripts, detect conflicts throughout the session.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes `get-specific` config from `.draekien/.skillsrc`.
- **`scripts/query.py`** — Queries the ubiquitous language dictionary (`list-contexts`, `list`, `lookup`).
- **`scripts/write.py`** — Writes terms and flags/resolves ambiguities in the dictionary.
- **`scripts/migrate.py`** — Migrates legacy `UBIQUITOUS_LANGUAGE.md` files to the YAML dictionary.

## Session Start

Runs once on first invocation.

1. Run `uv run scripts/skillsrc.py --config .draekien/.skillsrc get` to read the configured dictionary path. If `.draekien/.skillsrc` is absent the script prints the default `.draekien/ubiquitous-language.yaml`. If the script exits non-zero, fall back to the default path `.draekien/ubiquitous-language.yaml` and inform the user: "Could not read config; using default dictionary path."
2. Check whether the dictionary file exists at `dictionaryPath`.
   - **Exists**: load all contexts and terms into conflict detection context using `scripts/query.py list-contexts` then `scripts/query.py list <Context>` for each. Skip to step 3.
   - **Does not exist**: scan project for any `UBIQUITOUS_LANGUAGE.md` files (excluding root index). If found, show the list and prompt user to migrate using `scripts/migrate.py`. After migration (or if none found), proceed.
3. Scan project structure. Infer a bounded context name for each candidate dir (PascalCase, domain-meaningful — exclude `utils`, `shared`, `common`). Merge with any contexts already in the dictionary. Confirm full mapping with user; apply corrections.

## Active Behaviors

Run every response after session start, concurrently.

### Interview

Ask one DDD-framed question at a time — domain events, aggregates, bounded context membership. If the question concerns project structure, naming conventions, or existing terminology (facts observable in the codebase), explore and present findings rather than asking. If it concerns intent, ownership, or business meaning, always ask the user. Continue until the user explicitly confirms they are done, or until all domain nouns surfaced during the session have confirmed definitions in the dictionary.

### Term Capture

When a noun is judged domain-specific and not yet defined in any loaded context:

1. Propose a definition to the user. When proposing a definition, also propose a one-sentence usage example (the `--usage` argument). Confirm both before writing. If no other terms are yet defined in the dictionary, the usage note may not reference other domain terms — write with whatever context is available. Once any other term is defined, the usage note must reference at least one defined term where the relationship is meaningful.
2. Search codebase for the term. Read surrounding context.
3. If semantic contradiction found: hard interrupt, surface the conflict, wait for resolution. If the user updates the definition, replace the proposed definition with the new one and proceed to step 4 (do not repeat step 2). If the user confirms the definition is correct, note the code divergence and proceed to step 4.
4. No contradiction: determine bounded context from the confirmed map. If ambiguous, ask.
5. Before first write to any context, confirm the bounded context assignment. If the bounded context the agent would now assign to a term differs from the bounded context it proposed during definition confirmation, re-confirm the bounded context assignment before writing.
6. Write immediately using `scripts/write.py add-term` — no batching.

See [references/ubiquitous-language-format.md](references/ubiquitous-language-format.md) for schema and full script invocation reference.

### Conflict Detection

Check every response against all loaded definitions. A term absent from the codebase is neutral — not a contradiction.

- **Definition conflict** — user uses a defined term contradicting its stored meaning: hard interrupt, surface both meanings, ask which is canonical. Run `scripts/write.py add-term` immediately on resolution.
- **Cross-context collision** — same term defined differently in two contexts: surface explicitly, ask if intentional. Both definitions stand if deliberate (DDD allows intentional ambiguity across contexts). Mark the collision as intentional in the loaded conflict-detection context so it is not re-surfaced on subsequent responses. Run `scripts/write.py flag-ambiguity` on both contexts with a note recording the intentional divergence. If not intentional, treat as a Definition conflict: ask which definition is canonical, update the incorrect context with the corrected definition, and flag the other pending review.
- **Vague language** — user word matches 2+ defined terms: hard interrupt, list matching terms with definition summaries, wait for disambiguation. Run `scripts/write.py flag-ambiguity` until resolved; run `scripts/write.py resolve-ambiguity` once canonical meaning is confirmed.
