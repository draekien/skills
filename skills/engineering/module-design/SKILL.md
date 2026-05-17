---
name: module-design
description: Designs a new piece of code — from a single method to an entire architectural layer — through structured interview, enforces software-design principles as hard constraints in real time, and produces an adaptive Markdown spec. Use when designing a new module, class, function, or architectural layer, or when the user says "design this", "help me design", "design a module", "design a class", "let's design", "plan this component".
---

# Module Design

Guide the user through designing a new piece of code. Interview one question at a time; explore the project before asking. Enforce strict design principles as hard constraints during the interview. Produce an adaptive spec document, then spawn an independent subagent to audit it against the recommended rules.

## Session Start

Run once on first invocation in this order:

1. **Load config** — read `.draekien/.skillsrc` at the project root. If present and `module-design.specsDir` is set, use that as the spec output directory. Otherwise default to `docs/designs`.
2. **DDD mode** — check for `UBIQUITOUS_LANGUAGE.md` at the project root. If found, load it and activate DDD mode (bounded context mapping, term capture, conflict detection — see [references/ddd-mode.md](references/ddd-mode.md)). If absent, skip DDD mode entirely.
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
3. If the user provides a custom path that differs from the default, write it to `.draekien/.skillsrc` under `module-design.specsDir`. See [references/skillsrc-format.md](references/skillsrc-format.md) for keys and write rules.

## Recommended Rules Audit

After writing the spec, spawn an independent subagent with this exact brief:

> You are a software design auditor. Read the spec at `<resolved-path>`. Check it against each of the following eight recommended design principles. For each violation found, quote the relevant spec text, name the rule, and suggest a concrete fix. If no violations, say so. Do not rewrite the spec — findings only.
>
> Principles to check: Minimize Complexity, Deep Modules, Avoid Hasty Abstractions, Command-Query Separation, Fail Fast, Names as Documentation, Principle of Least Astonishment, Single Abstraction Level.
>
> Full rule definitions are in `skills/engineering/module-design/references/design-principles.md`.

Report the subagent's findings to the user as a numbered list of violations (or a confirmation of none). The user decides which findings to apply; update the spec only on explicit instruction.
