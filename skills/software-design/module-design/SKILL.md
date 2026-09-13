---
name: module-design
description: Applies software design principles to modules — from a single method to an entire architectural layer — over rounds of critique and refinement. Use when designing new code, refining an existing design spec, or auditing existing code for design problems, or when the user says "design this", "refine this design", "audit this", "what's wrong with this", "plan this component".
argument-hint: "[--mode design|refine|review] [--effort low|medium|high] [--runner inline|subagent] [module-or-file]"
---

# Module Design

Apply software design principles to whatever the user brings. A first pass is rarely a good design, so the payload is the rounds, not the draft. Explore the project before asking; let the principles drive the analysis.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes `module-design` config from `.draekien/.skillsrc`.

## Session Start

Run once on first invocation in this order:

1. **Load config** — run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill module-design get specsDir --default docs/designs` to read the spec output directory. If the script is unavailable, parse `.draekien/.skillsrc` as JSON directly and read `module-design.specsDir`; default to `docs/designs` if absent.
2. **Settle the run** — take mode, effort, and runner from the flags. Unflagged, infer the mode: an existing spec to improve is `refine`, existing code to assess is `review`, anything else is `design`. Effort defaults to `medium`, runner to `subagent`.
3. **Open question** — if the module, spec, or code in scope isn't already clear from the conversation, ask what to look at before proceeding.

## Modes

| Mode     | Input                                                 | Draft under refinement |
| -------- | ----------------------------------------------------- | ---------------------- |
| `design` | the module to build, understood by interview          | a new spec             |
| `refine` | an existing spec, or the design written this session  | that spec              |
| `review` | existing code                                         | a violations report    |

`refine` resolves its input in that order: if the positional names a spec that exists under the resolved specs directory, read it; otherwise continue the design already in this conversation. If neither is available, ask which.

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

## Rounds

Every mode produces an initial draft, then loops over it before anything reaches the user or the disk.

`--effort` sets the round budget:

| Effort             | Rounds |
| ------------------ | ------ |
| `low`              | 1      |
| `medium` (default) | 3      |
| `high`             | 5      |

`--runner` decides where a round executes. `subagent` (the default) dispatches it to a fresh context — fresh eyes catch what the draft's own author cannot see. `inline` runs it here, keeping the reasoning visible and costing no dispatch.

Each round is critique-and-refine over the current draft:

1. **Critique** — check the draft against every recommended rule in [references/design-principles.md](references/design-principles.md). For each violation, quote the offending text and name the rule.
2. **Refine** — write the concrete replacement text for each finding. Nothing lands in the draft at this step.
3. **Adjudicate** — take each finding on its merits: apply it, or reject it with a reason. Apply the accepted changes before the next round starts.

Under `--runner subagent`, steps 1 and 2 belong to the subagent and step 3 is always yours — the subagent proposes, it never commits. Dispatch brief: [references/critique-brief.md](references/critique-brief.md). Under `--runner inline`, do all three yourself.

A finding that names a strict rule is applied, never rejected.

Rounds run without stopping for the user — the user's gate is the finished draft, not each round. Record every finding as it is adjudicated; the record ships with the draft.

Stop early when a round returns no findings, or when every finding in a round is rejected: the budget is a ceiling, not a quota.

Rounds are done when the budget is spent or a round stops it early, and every finding from every round sits in the record as applied, or rejected with its reason.

## Output

**`design` and `refine`** — the spec. Adapt depth to scope; see [references/spec-format.md](references/spec-format.md) for section rules by scope. Present the refined draft, including its refinement record, to the user and apply any corrections before writing to disk.

**`review`** — a violations report, ending in the same refinement record. For each violation that survives the rounds, quote the offending code, name the rule, and suggest a concrete fix. If none survive, state that explicitly. Offer to write a redesign spec either way.

Spec output path:

- Use `module-design.specsDir` from `.skillsrc` if set, otherwise `docs/designs`.
- Filename: `<module-name>.md` (kebab-case).
- **Exists** — write directly, no confirmation needed. (Config writes still require confirmation per [references/skillsrc-format.md](references/skillsrc-format.md).)
- **Does not exist** — confirm the full path with the user before creating it.

If the user provides a custom path that differs from the default, confirm with the user, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill module-design set specsDir <path>` to persist it. The script merges only the `module-design` block and preserves all other skills' config.

Once a spec exists at the resolved path, offer `--mode refine` to put it through further rounds.
