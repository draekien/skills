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

1. **Load config** — run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill module-design get specsDir --default docs/designs` to read the spec output directory. If the script is unavailable, parse `.draekien/.skillsrc` as JSON directly and read `module-design.specsDir`; default to `docs/designs` if absent.
2. **Open question** — if the module or system in scope isn't already clear from the conversation, ask what to look at before proceeding.

## Understanding the module

After the user answers the opening question from Session Start, explore the project, then ask further targeted questions. What matters is understanding scope, responsibility, callers, data contract, side effects, and boundaries — whether by reading existing code or by interviewing the user. If the module exists, the codebase already answers most of these.

## Strict Constraint Enforcement

These five rules are non-negotiable. Check each design decision against them as it is made. If a decision violates a strict rule, **block immediately**: name the rule, explain the specific violation, and ask the user to revise before continuing.

| Rule                               | Hard constraint                                                                                                                                                                       |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Information Hiding**             | Callers must not depend on how a result is achieved — only what the module provides. Flag any interface that exposes implementation details.                                          |
| **Law of Demeter**                 | Only communicate with immediate neighbours. Flag any interface that requires callers to navigate through another object's internals.                                                  |
| **Define Errors Out of Existence** | Invalid states must be unrepresentable in the data model. Flag any design where invalid inputs can reach internal logic.                                                              |
| **Avoid Temporal Decomposition**   | Modules must be structured around the information they own, not the order operations execute. Flag any decomposition that splits by execution step rather than by knowledge boundary. |
| **Strategic Programming**          | Interfaces must be shaped around the concept, not around the first caller's immediate needs. Flag any interface with caller-specific parameters or flags.                             |

Full rule definitions: [references/design-principles.md](references/design-principles.md).

## Output

For existing modules: produce a violations report. For each violation, quote the offending code, name the rule, and suggest a concrete fix. Offer to draft a redesign spec if the user wants one. If no violations are found, state that explicitly and offer to draft a redesign spec. Once a spec exists at the resolved path (drafted now or from an earlier session), also offer to run the recommended-rules audit against it.

For new modules: draft the spec once the design is understood. Adapt depth to scope — see [references/spec-format.md](references/spec-format.md) for section rules by scope. Present the draft to the user and apply any corrections before writing to disk.

Spec output path:

- Use `module-design.specsDir` from `.skillsrc` if set, otherwise `docs/designs`.
- Filename: `<module-name>.md` (kebab-case).
- **Exists** — write directly, no confirmation needed. (Config writes still require confirmation per [references/skillsrc-format.md](references/skillsrc-format.md).)
- **Does not exist** — confirm the full path with the user before creating it.

If the user provides a custom path that differs from the default, confirm with the user, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill module-design set specsDir <path>` to persist it. The script merges only the `module-design` block and preserves all other skills' config.

## Recommended Rules Audit

After writing the spec, run the recommended-rules audit — see [references/recommended-rules-audit.md](references/recommended-rules-audit.md) for the subagent brief.

Report the subagent's findings to the user as a numbered list of violations (or a confirmation of none). The user decides which findings to apply; update the spec only on explicit instruction.
