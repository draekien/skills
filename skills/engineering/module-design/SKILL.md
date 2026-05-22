---
name: module-design
description: Designs a new piece of code — from a single method to an entire architectural layer — through structured interview, enforces software-design principles as hard constraints in real time, and produces an adaptive Markdown spec. Use when designing a new module, class, function, or architectural layer, or when the user says "design this", "help me design", "design a module", "design a class", "let's design", "plan this component".
---

# Module Design

Guide the user through designing a new piece of code. Interview one question at a time; explore the project before asking. Enforce strict design principles as hard constraints during the interview. Produce an adaptive spec document, then spawn an independent subagent to audit it against the recommended rules.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes `module-design` config from `.draekien/.skillsrc`.

## Session Start

Run once on first invocation in this order:

1. **Load config** — run `uv run scripts/skillsrc.py --config .draekien/.skillsrc get` to read the configured spec output directory. If `.draekien/.skillsrc` is absent the script prints the default `docs/designs`.
2. **DDD mode** — check for `.draekien/ubiquitous-language.yaml` at the project root. If found, activate DDD mode: run `uv run scripts/query.py --dict .draekien/ubiquitous-language.yaml list-contexts`, then for each context run `uv run scripts/query.py --dict .draekien/ubiquitous-language.yaml list <Context>` to load all terms into conflict-detection context. See [references/ddd-mode.md](references/ddd-mode.md). If the dictionary is absent but a `UBIQUITOUS_LANGUAGE.md` exists at the project root, inform the user that migration is needed and recommend running the `get-specific` skill first. If neither exists, skip DDD mode entirely.
3. **Open question** — ask "What are you designing?" Wait for the answer before proceeding.

## Interview

Ask one question at a time. If the answer can be determined by exploring the project (existing interfaces, call sites, data types), explore first rather than asking.

Work through these in order, skipping any the user has already answered:

1. **Scope** — is this a method, class, module, or layer? This governs spec depth.
2. **Responsibility** — what is its single job? If the answer involves "and", surface that as a potential scope issue.
3. **Callers** — who uses it and what do they care about? What must they not need to know?
4. **Data contract** — what goes in, what comes out? What shape should errors take?
5. **Side effects** — does it mutate state, perform I/O, or emit events? Which are intentional?
6. **DDD placement** *(DDD mode only)* — which bounded context does this belong to?

During DDD mode, run term capture and conflict detection after every response — see [references/ddd-mode.md](references/ddd-mode.md).

## Strict Constraint Enforcement

These five rules are non-negotiable. Check each design decision against them as it is made. If a decision violates a strict rule, **block immediately**: name the rule, explain the specific violation, and ask the user to revise before continuing.

| Rule | Hard constraint |
|------|----------------|
| **Information Hiding** | Callers must not depend on how a result is achieved — only what the module provides. Flag any interface that exposes implementation details. |
| **Law of Demeter** | Only communicate with immediate neighbours. Flag any interface that requires callers to navigate through another object's internals. |
| **Define Errors Out of Existence** | Invalid states must be unrepresentable in the data model. Flag any design where invalid inputs can reach internal logic. |
| **Avoid Temporal Decomposition** | Modules must be structured around the information they own, not the order operations execute. Flag any decomposition that splits by execution step rather than by knowledge boundary. |
| **Strategic Programming** | Interfaces must be shaped around the concept, not around the first caller's immediate needs. Flag any interface with caller-specific parameters or flags. |

Full rule definitions: [references/design-principles.md](references/design-principles.md).

## Spec Draft

Once the interview is complete, draft the spec. Adapt depth to scope — see [references/spec-format.md](references/spec-format.md) for section rules by scope.

Present the draft to the user and apply any corrections before writing to disk.

## Output

1. Determine the output path:
   - Use `module-design.specsDir` from `.skillsrc` if set, otherwise `docs/designs`.
   - Filename: `<module-name>.md` (kebab-case).
2. Check whether the directory exists.
   - **Exists** — write directly, no confirmation needed.
   - **Does not exist** — confirm the full path with the user before creating it.
3. If the user provides a custom path that differs from the default, confirm with the user, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc set <path>` to persist it. The script merges only the `module-design` block and preserves all other skills' config.

## Recommended Rules Audit

After writing the spec, spawn an independent subagent to audit it. Brief it to:

- Read the spec at the resolved path.
- Check each of the eight recommended principles: Minimize Complexity, Deep Modules, Avoid Hasty Abstractions, Command-Query Separation, Fail Fast, Names as Documentation, Principle of Least Astonishment, Single Abstraction Level.
- For each violation: quote the offending spec text, name the rule, and suggest a concrete fix.
- Report clean if no violations found. Do not rewrite the spec — findings only.
- Full rule definitions are in `skills/engineering/module-design/references/design-principles.md`.

Report the subagent's findings to the user as a numbered list of violations (or a confirmation of none). The user decides which findings to apply; update the spec only on explicit instruction.
