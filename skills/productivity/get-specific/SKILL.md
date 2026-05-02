---
name: get-specific
description: Builds and enforces shared ubiquitous language for a project. Interviews users to surface domain terms, tracks definitions in scoped ALIGNMENT.md files, and detects terminology conflicts in real time. Use when terminology feels ambiguous, before implementing features, or when the user says "get specific", "define our terms", "what do we mean by X", or wants to establish shared vocabulary before acting.
---

# Get Specific

Establish + enforce shared vocab. Interview user, detect domain terms, validate against codebase, write definitions to scoped `ALIGNMENT.md` files.

## Step 1 — Session Initialization

On first invocation each session:

1. Scan project structure. Find candidate feature/app dirs (e.g. `src/`, `apps/`, `packages/`, `features/`, named subdirs with domain meaning).
2. Read root `ALIGNMENT.md` if exists. Extract candidate dir map + alignment file index. Load all scoped `ALIGNMENT.md` files into conflict detection context.
3. Merge scan with existing candidate map. Write updated map to root `ALIGNMENT.md` (create if absent). Authoritative candidate map for session.
4. No user prompt about init.

## Step 2 — Interview Phase

Interview relentlessly on every domain aspect until shared understanding reached. Walk each design branch, resolve dependencies one by one. Per question: pros/cons + recommendation.

One question at a time. If answerable by exploring project, explore instead.

Continue until domain sufficiently mapped.

## Step 3 — Term Detection

During + after interview, monitor for candidate terms.

Noun = **candidate term** if both hold:

- Appears 2+ times in session without prior definition in any loaded `ALIGNMENT.md`
- Domain-specific — not generic like "user", "request", "file"

On candidate detected, propose definition:

> "I'm hearing you use `<Term>` repeatedly. Does this definition capture it?
> **`<Term>`**: `<proposed definition based on conversation context>`"

Wait for user confirmation before Step 4.

## Step 4 — Code Validation

Before writing confirmed definition:

1. Search codebase for term.
2. If found, read surrounding context. Check for semantic contradictions.
3. If contradiction exists, hard interrupt:

   > "Your code does `<A → B → C>`, but you said `<D>` — which is it?"

   Wait for resolution. Update proposed definition if needed, repeat from step 2.

4. If term absent, proceed — may be new concept.

## Step 5 — Writing Definitions

On user confirmation after code validation:

1. Check candidate map from root `ALIGNMENT.md` for save location.
2. Best-effort guess for most relevant scoped dir. If no candidates, target project root.
3. Before first write to any location, confirm:

   > "Writing to `<path>/ALIGNMENT.md` — correct?"

4. Re-confirm if target location changes mid-session.
5. Write term immediately. No batching.
6. Update root `ALIGNMENT.md` to include new scoped file if not already listed.

See [references/alignment-format.md](references/alignment-format.md) for full file structure and rules.

## Step 6 — Conflict Detection

Every response: check user language against all terms in all loaded `ALIGNMENT.md` files.

**Definition conflict** — user uses defined term contradicting stored meaning. Hard interrupt:

> "Previous definition of '`<Term>`' is `<X>`, but you seem to mean `<Y>` — which is it?"

Stop. Wait for resolution. If definition changes, update `ALIGNMENT.md` immediately.

**Vague language** — user uses word matching 2+ defined terms. Hard interrupt:

> "You said '`<vague word>`' — did you mean `<Term A>` (`<definition summary A>`) or `<Term B>` (`<definition summary B>`)?"

Stop. Wait for clarification before continuing.

## Gotchas

- `ALIGNMENT.md` must never contain implementation detail: no file paths, function names, method signatures, variable names, data structures.
- Never write term not explicitly confirmed by user.
- No deferred writes — update `ALIGNMENT.md` moment term resolved.
- Root `ALIGNMENT.md` = index only. No term definitions there.
- Term absent from codebase = neutral, not contradiction.
- Candidate map in root `ALIGNMENT.md` = cache — always re-scan + rewrite at session start to catch structural changes.