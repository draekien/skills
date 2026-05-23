---
name: module-design
description: Applies software design principles to modules — from a single method to an entire architectural layer. Use when designing new code, auditing existing code for design problems, or when the user says "design this", "help me design", "audit this", "find design problems in", "what's wrong with this", "let's design", "plan this component".
---

# Module Design

Apply software design principles to whatever the user brings. Explore the project before asking; let the principles drive the analysis. Produce a spec for new designs or a violations report for existing ones.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes `module-design` config from `.draekien/.skillsrc`.

## Session Start

Run once on first invocation in this order:

1. **Load config** — run `uv run scripts/skillsrc.py --config .draekien/.skillsrc get` to read the configured spec output directory. If `.draekien/.skillsrc` is absent the script prints the default `docs/designs`.
2. **Open question** — ask "What are we looking at?" Wait for the answer before proceeding.

## Understanding the module

Explore the project before asking questions. What matters is understanding scope, responsibility, callers, data contract, side effects, and boundaries — whether by reading existing code or by interviewing the user. If the module exists, the codebase already answers most of these.

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

## Output

For existing modules: produce a violations report. For each violation, quote the offending code, name the rule, and suggest a concrete fix. Offer to draft a redesign spec if the user wants one.

For new modules: draft the spec once the design is understood. Adapt depth to scope — see [references/spec-format.md](references/spec-format.md) for section rules by scope. Present the draft to the user and apply any corrections before writing to disk.

Spec output path:
- Use `module-design.specsDir` from `.skillsrc` if set, otherwise `docs/designs`.
- Filename: `<module-name>.md` (kebab-case).
- **Exists** — write directly, no confirmation needed.
- **Does not exist** — confirm the full path with the user before creating it.

If the user provides a custom path that differs from the default, confirm with the user, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc set <path>` to persist it. The script merges only the `module-design` block and preserves all other skills' config.

## Recommended Rules Audit

After writing the spec, spawn an independent subagent to audit it. Brief it to:

- Read the spec at the resolved path.
- Check each of the eight recommended principles: Minimize Complexity, Deep Modules, Avoid Hasty Abstractions, Command-Query Separation, Fail Fast, Names as Documentation, Principle of Least Astonishment, Single Abstraction Level.
- For each violation: quote the offending spec text, name the rule, and suggest a concrete fix.
- Report clean if no violations found. Do not rewrite the spec — findings only.
- Full rule definitions are in `skills/engineering/module-design/references/design-principles.md`.

Report the subagent's findings to the user as a numbered list of violations (or a confirmation of none). The user decides which findings to apply; update the spec only on explicit instruction.
