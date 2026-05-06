---
name: get-specific
description: Builds and enforces a DDD ubiquitous language for a project. Discovers bounded contexts by exploring the codebase, interviews users to surface domain terms, tracks definitions in scoped UBIQUITOUS_LANGUAGE.md files, and detects terminology conflicts in real time. Use when terminology feels ambiguous, before implementing features, or when the user says "get specific", "define our terms", "what do we mean by X", or wants to establish shared vocabulary before acting.
---

# Get Specific

Establish + enforce DDD ubiquitous language scoped to bounded contexts. Discover contexts by exploring project, interview user, detect domain terms, validate against codebase, write definitions to scoped `UBIQUITOUS_LANGUAGE.md` files.

## Step 0 — Preflight Migration

Before any other step, scan for legacy `ALIGNMENT.md` files (root and all subdirs).

If any found:

> "I found legacy `ALIGNMENT.md` files from a previous version of this skill:
> - `<path>/ALIGNMENT.md`
> - ...
>
> These need to be migrated to `UBIQUITOUS_LANGUAGE.md` before we continue. Migrate now?"

If user confirms, follow [references/migration.md](references/migration.md). Complete all migrations before proceeding to Step 1.

If user declines, proceed — treat legacy files as absent for this session.

## Step 1 — Session Initialization

On first invocation each session:

1. Scan project structure. Find candidate bounded context dirs (e.g. `src/`, `apps/`, `packages/`, `features/`, named subdirs with domain meaning). Infer a bounded context name for each (PascalCase, domain-meaningful — not technical names like `utils`, `shared`, `common`).
2. Read root `UBIQUITOUS_LANGUAGE.md` if exists. Extract known bounded context map + file index. Load all scoped `UBIQUITOUS_LANGUAGE.md` files into conflict detection context.
3. Merge scan with existing map. Present full inferred mapping to user for one-shot confirmation:

   > "I've mapped these bounded contexts:
   > - `src/orders/` → **Orders**
   > - `src/billing/` → **Billing**
   > - `src/inventory/` → **Inventory**
   >
   > Correct? Any to rename, merge, or add?"

   Wait for user confirmation or corrections before continuing.

4. Write confirmed map to root `UBIQUITOUS_LANGUAGE.md` (create if absent). Authoritative bounded context map for session.

## Step 2 — Interview Phase

Interview relentlessly on every domain aspect until shared understanding reached. Walk each design branch, resolve dependencies one by one. Per question: pros/cons + recommendation.

One question at a time. If answerable by exploring project, explore instead.

Frame questions in DDD terms naturally — ask about domain events ("what triggers X?"), aggregates ("what owns the lifecycle of X?"), and bounded context membership ("does this concept mean the same thing in Billing as it does in Orders?").

Continue until domain sufficiently mapped.

## Step 3 — Term Detection

During + after interview, monitor for candidate terms.

Noun = **candidate term** if both hold:

- Appears 2+ times in session without prior definition in any loaded `UBIQUITOUS_LANGUAGE.md`
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

1. Determine which bounded context the term belongs to using confirmed map from root `UBIQUITOUS_LANGUAGE.md`.
2. Best-effort guess for most relevant bounded context. If ambiguous, ask:

   > "Does `<Term>` belong to **Orders** or **Billing**?"

3. Before first write to any bounded context file, confirm:

   > "Writing to `<path>/UBIQUITOUS_LANGUAGE.md` (**Orders** context) — correct?"

4. Re-confirm if target context changes mid-session.
5. Write term immediately. No batching.
6. Update root `UBIQUITOUS_LANGUAGE.md` to include new scoped file if not already listed.

See [references/ubiquitous-language-format.md](references/ubiquitous-language-format.md) for full file structure and rules.

## Step 6 — Conflict Detection

Every response: check user language against all terms in all loaded `UBIQUITOUS_LANGUAGE.md` files.

**Definition conflict** — user uses defined term contradicting stored meaning. Hard interrupt:

> "Previous definition of '`<Term>`' is `<X>`, but you seem to mean `<Y>` — which is it?"

Stop. Wait for resolution. If definition changes, update `UBIQUITOUS_LANGUAGE.md` immediately.

**Cross-context collision** — same term defined differently across two bounded contexts. Surface explicitly:

> "`<Term>` means `<X>` in **Orders** but `<Y>` in **Billing** — is this intentional? If so, both definitions stand. If not, which is canonical?"

**Vague language** — user uses word matching 2+ defined terms. Hard interrupt:

> "You said '`<vague word>`' — did you mean `<Term A>` (`<definition summary A>`) or `<Term B>` (`<definition summary B>`)?"

Stop. Wait for clarification before continuing.

## Gotchas

- `UBIQUITOUS_LANGUAGE.md` must never contain implementation detail: no file paths, function names, method signatures, variable names, data structures.
- Never write term not explicitly confirmed by user.
- No deferred writes — update `UBIQUITOUS_LANGUAGE.md` moment term resolved.
- Root `UBIQUITOUS_LANGUAGE.md` = index only. No term definitions there.
- Term absent from codebase = neutral, not contradiction.
- Cross-context collision ≠ error by default — same word can mean different things in different bounded contexts (DDD intentional ambiguity). Surface it; don't force resolution.
- Bounded context map in root = cache — always re-scan + rewrite at session start to catch structural changes.
