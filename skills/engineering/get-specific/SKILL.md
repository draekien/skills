---
name: get-specific
description: Builds and enforces a DDD ubiquitous language for a project. Discovers bounded contexts by exploring the codebase, interviews users to surface domain terms, tracks definitions in a centralised YAML dictionary inside .draekien/, and detects terminology conflicts in real time. Use when terminology feels ambiguous, before implementing features, or when the user says "get specific", "define our terms", "what do we mean by X", or wants to establish shared vocabulary before acting.
---

# Get Specific

Establish DDD ubiquitous language scoped to bounded contexts. Interview user, capture confirmed terms in `.draekien/ubiquitous-language.yaml` via scripts, detect conflicts throughout the session.

## Session Start

Runs once on first invocation.

1. Read `dictionaryPath` from `.draekien/.skillsrc` under the `get-specific` key. Default: `.draekien/ubiquitous-language.yaml`.
2. Check whether the dictionary file exists at `dictionaryPath`.
   - **Exists**: load all contexts and terms into conflict detection context using `scripts/query.py list-contexts` then `scripts/query.py list <Context>` for each. Skip to step 3.
   - **Does not exist**: scan project for any `UBIQUITOUS_LANGUAGE.md` files (excluding root index). If found, show the list and prompt user to migrate using `scripts/migrate.py`. After migration (or if none found), proceed.
3. Scan project structure. Infer a bounded context name for each candidate dir (PascalCase, domain-meaningful — exclude `utils`, `shared`, `common`). Merge with any contexts already in the dictionary. Confirm full mapping with user; apply corrections.

## Active Behaviors

Run every response after session start, concurrently.

### Interview

Ask one DDD-framed question at a time — domain events, aggregates, bounded context membership. If answerable by exploring the project, explore instead. Continue until shared understanding reached.

### Term Capture

When a noun is judged domain-specific and not yet defined in any loaded context:

1. Propose a definition to the user. Wait for confirmation.
2. Search codebase for the term. Read surrounding context.
3. If semantic contradiction found: hard interrupt, surface the conflict, wait for resolution. Update definition if needed; repeat from 2.
4. No contradiction: determine bounded context from the confirmed map. If ambiguous, ask.
5. Before first write to any context, confirm the bounded context assignment. Re-confirm if target context changes mid-session.
6. Write immediately using `scripts/write.py add-term` — no batching.

See [references/ubiquitous-language-format.md](references/ubiquitous-language-format.md) for schema and full script invocation reference.

### Conflict Detection

Check every response against all loaded definitions. A term absent from the codebase is neutral — not a contradiction.

- **Definition conflict** — user uses a defined term contradicting its stored meaning: hard interrupt, surface both meanings, ask which is canonical. Run `scripts/write.py add-term` immediately on resolution.
- **Cross-context collision** — same term defined differently in two contexts: surface explicitly, ask if intentional. Both definitions stand if deliberate (DDD allows intentional ambiguity across contexts).
- **Vague language** — user word matches 2+ defined terms: hard interrupt, list matching terms with definition summaries, wait for disambiguation. Run `scripts/write.py flag-ambiguity` until resolved; run `scripts/write.py resolve-ambiguity` once canonical meaning is confirmed.
