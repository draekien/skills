---
name: get-specific
description: Builds and enforces a DDD ubiquitous language for a project. Discovers bounded contexts by exploring the codebase, interviews users to surface domain terms, tracks definitions in scoped UBIQUITOUS_LANGUAGE.md files, and detects terminology conflicts in real time. Use when terminology feels ambiguous, before implementing features, or when the user says "get specific", "define our terms", "what do we mean by X", or wants to establish shared vocabulary before acting.
---

# Get Specific

Establish DDD ubiquitous language scoped to bounded contexts. Interview user, capture confirmed terms in scoped `UBIQUITOUS_LANGUAGE.md` files, detect conflicts throughout the session.

## Session Start

Runs once on first invocation.

1. Scan for legacy `ALIGNMENT.md` files (root + all subdirs). If found, offer migration before continuing. Follow [references/migration.md](references/migration.md) if user confirms; otherwise treat as absent.
2. Scan project structure. Infer a bounded context name for each candidate dir (PascalCase, domain-meaningful — exclude `utils`, `shared`, `common`). Merge with any existing root `UBIQUITOUS_LANGUAGE.md` index. Confirm full mapping with user; apply corrections.
3. Write confirmed map to root `UBIQUITOUS_LANGUAGE.md` (create if absent). Index only — no term definitions.
4. Load all scoped `UBIQUITOUS_LANGUAGE.md` files into conflict detection context.

## Active Behaviors

Run every response after session start, concurrently.

### Interview

Ask one DDD-framed question at a time — domain events ("what triggers X?"), aggregates ("what owns the lifecycle of X?"), bounded context membership ("does this mean the same thing in both contexts?"). If answerable by exploring project, explore instead. Continue until shared understanding reached.

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

Check every response against all loaded definitions.

- **Definition conflict** — user uses defined term contradicting stored meaning: hard interrupt, surface both meanings, ask which is canonical. Update file immediately on resolution.
- **Cross-context collision** — same term defined differently in two contexts: surface explicitly, ask if intentional. Both definitions stand if deliberate.
- **Vague language** — user word matches 2+ defined terms: hard interrupt, list matching terms with definition summaries, wait for disambiguation.

## Gotchas

- No impl detail in definitions — no file paths, function names, method signatures, data structures.
- Never write a term not confirmed by user.
- Root `UBIQUITOUS_LANGUAGE.md` = index only. No term definitions.
- Term absent from codebase = neutral, not contradiction.
- Cross-context collision ≠ error — DDD allows intentional ambiguity across contexts. Surface it; don't force resolution.
- Bounded context map in root = cache — always re-scan + rewrite at session start.
