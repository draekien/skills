---
name: get-specific
description: Builds and enforces a DDD ubiquitous language for a project. Discovers bounded contexts by exploring the codebase, interviews users to surface domain terms, tracks definitions in scoped UBIQUITOUS_LANGUAGE.md files, and detects terminology conflicts in real time. Use when terminology feels ambiguous, before implementing features, or when the user says "get specific", "define our terms", "what do we mean by X", or wants to establish shared vocabulary before acting.
---

# Get Specific

Establish DDD ubiquitous language scoped to bounded contexts. Interview user, capture confirmed terms in scoped `UBIQUITOUS_LANGUAGE.md` files, detect conflicts throughout the session.

## Session Start

Runs once on first invocation.

1. Scan project structure. Infer a bounded context name for each candidate dir (PascalCase, domain-meaningful — exclude `utils`, `shared`, `common`). Merge with any existing root `UBIQUITOUS_LANGUAGE.md` index. Confirm full mapping with user; apply corrections.
2. Write confirmed map to root `UBIQUITOUS_LANGUAGE.md` (create if absent). Index only — no term definitions.
3. Load all scoped `UBIQUITOUS_LANGUAGE.md` files into conflict detection context.

## Active Behaviors

Run every response after session start, concurrently.

### Interview

Ask one DDD-framed question at a time — domain events, aggregates, bounded context membership. If answerable by exploring project, explore instead. Continue until shared understanding reached.

### Term Capture

When a noun is judged domain-specific and not yet defined in any loaded file:

1. Propose a definition to the user. Wait for confirmation.
2. Search codebase for the term. Read surrounding context.
3. If semantic contradiction found: hard interrupt, surface the conflict, wait for resolution. Update definition if needed; repeat from 2.
4. No contradiction: determine bounded context from root index. If ambiguous, ask.
5. Before first write to any context file, confirm the target path. Re-confirm if target context changes mid-session.
6. Write immediately — no batching.
7. Update root `UBIQUITOUS_LANGUAGE.md` if new scoped file created.

See [references/ubiquitous-language-format.md](references/ubiquitous-language-format.md) for file structure and rules.

### Conflict Detection

Check every response against all loaded definitions. A term absent from the codebase is neutral — not a contradiction.

- **Definition conflict** — user uses defined term contradicting stored meaning: hard interrupt, surface both meanings, ask which is canonical. Update file immediately on resolution.
- **Cross-context collision** — same term defined differently in two contexts: surface explicitly, ask if intentional. Both definitions stand if deliberate (DDD allows intentional ambiguity across contexts).
- **Vague language** — user word matches 2+ defined terms: hard interrupt, list matching terms with definition summaries, wait for disambiguation.
