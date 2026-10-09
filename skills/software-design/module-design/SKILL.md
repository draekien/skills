---
name: module-design
description: Applies software design principles to modules — from a single method to an entire architectural layer — over rounds of critique and refinement. Use when designing new code, refining an existing design spec, or auditing existing code for design problems, or when the user says "design this", "refine this design", "audit this", "what's wrong with this", "plan this component".
argument-hint: "[design|refine|review] [--effort low|medium|high] [--runner inline|subagent] [module-or-file]"
---

# Module Design

Apply software design principles to whatever the user brings. A first pass is rarely a good design, so the payload is the rounds, not the draft. Explore the project before asking; let the principles drive the analysis.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes `module-design` config from `.draekien/.skillsrc`.

## Session Start

Run once on first invocation in this order:

1. **Load config** — read the `module-design` block of `.draekien/.skillsrc` as JSON: `specsDir` (default `docs/designs`) and `subagentModel` (default empty). If the file, block, or key is absent, use the defaults.
2. **Settle the run** — take the mode from the subcommand, and effort and runner from the flags. With no subcommand, infer the mode: an existing spec to improve is `refine`, existing code to assess is `review`, anything else is `design`. Unflagged effort comes from a project rule that sets one, otherwise `medium`; runner defaults to `subagent`.
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

Put each open decision to the user one at a time, with its options, their trade-offs, any precedent behind them, and your recommendation — a batch of bare questions gets rejected. Use the `get-aligned` skill for this. If it is not installed, ask the user to add it: `/plugin install productivity-skills@draekien-skills`, or `npx skills add draekien/skills --skill "get-aligned"`.

## Strict Constraint Enforcement

These five rules are non-negotiable. Check each design decision against them as it is made during the interview. If a decision violates a strict rule, **block immediately**: name the rule, explain the specific violation, and ask the user to revise before continuing. A strict-rule finding raised in a round follows the Rounds rule instead.

| Rule                               | Hard constraint                                                                                                                                                                       |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Information Hiding**             | Callers must not depend on how a result is achieved — only what the module provides. Flag any interface that exposes implementation details.                                          |
| **Law of Demeter**                 | Only communicate with immediate neighbours. Flag any interface that requires callers to navigate through another object's internals.                                                  |
| **Define Errors Out of Existence** | Invalid states must be unrepresentable in the data model. Flag any design where invalid inputs can reach internal logic.                                                              |
| **Avoid Temporal Decomposition**   | Modules must be structured around the information they own, not the order operations execute. Flag any decomposition that splits by execution step rather than by knowledge boundary. |
| **Strategic Programming**          | Interfaces must be shaped around the concept, not around the first caller's immediate needs. Flag any interface with caller-specific parameters or flags.                             |

Full rule definitions: [references/design-principles.md](references/design-principles.md).

## Rounds

Every mode writes an initial draft to a temp file outside the repo — under `refine`, a copy of the existing spec — then loops over it. Nothing is written to the repo, and no implementation starts, until the rounds are done and the user has replied at the gate in Output.

`--effort` sets the round budget:

| Effort             | Rounds |
| ------------------ | ------ |
| `low`              | 1      |
| `medium` (default) | 3      |
| `high`             | 5      |

`--runner` decides where a round executes. `subagent` (the default) dispatches it to a fresh context — fresh eyes catch what the draft's own author cannot see. `inline` runs it here, keeping the reasoning visible and costing no dispatch.

Each round is critique-and-refine over the current draft:

1. **Critique** — check the draft through the three lenses in [references/critique-brief.md](references/critique-brief.md): correctness, the project's rules, and every strict and recommended rule in [references/design-principles.md](references/design-principles.md). For each finding, quote the offending text, name the lens or rule, and tag it `blocker`, `major`, or `minor`. Under `--runner inline`, apply the lenses and tags exactly as the brief defines them.
2. **Refine** — write the concrete replacement text for each finding. Nothing lands in the draft at this step.
3. **Adjudicate** — check each finding's claim against the code or docs before deciding, then apply it or reject it with a reason. Apply the accepted changes before the next round starts.

Under `--runner subagent`, steps 1 and 2 belong to the subagent and step 3 is always yours — the subagent proposes, it never commits. Dispatch brief: [references/critique-brief.md](references/critique-brief.md). Dispatch every round to `subagentModel` when it is set; when it is empty, choose the model as the brief directs. If the user names a model to use by default from now on, confirm it, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill module-design set subagentModel <model>`. Under `--runner inline`, do all three yourself and write every finding in your reply — a round held only in your reasoning leaves no record.

A finding that names a strict rule is applied, unless a constraint outside the draft's control forbids it — a stated requirement of the module, a rule in the project's rules files, or a limit of the language or toolchain. Cite that constraint and record the finding as escalated, for the user to settle at the gate.

Rounds run without stopping for the user — the user's gate is the finished draft, not each round. Record every finding as it is adjudicated; the record ships with the draft. If the user tells you to stop, discard any round still running and go to the gate.

Stop early when a round leaves no `blocker` or `major` finding standing — none raised, or every one rejected or escalated. Apply that round's accepted `minor` findings and end: the budget is a ceiling, not a quota.

Rounds are done when the budget is spent or a round stops it early, and every finding from every round sits in the record as applied, rejected with its reason, or escalated with its constraint.

## Output

**`design` and `refine`** — the spec. Adapt depth to scope; see [references/spec-format.md](references/spec-format.md) for section rules by scope. At the gate — the point where the finished draft is shown to the user — present the refined draft in chat with its Refinement Record and every escalated finding, and apply the user's corrections before writing to the repo. At method or class scope the spec stays in chat and no file is written, unless the user asks for one.

**`review`** — a violations report, ending in the same refinement record. For each violation that survives the rounds, quote the offending code, name the rule, and suggest a concrete fix. If none survive, state that explicitly. Offer to write a redesign spec either way.

Spec output path:

- Use `module-design.specsDir` from `.skillsrc` if set, otherwise `docs/designs`.
- Filename: `<module-name>.md` (kebab-case).
- **Exists** — write after the gate with no path confirmation. (Config writes still require confirmation per [references/skillsrc-format.md](references/skillsrc-format.md).)
- **Does not exist** — create it only after the user's reply at the gate confirms the full path.

If the user provides a custom path that differs from the default, confirm with the user, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill module-design set specsDir <path>` to persist it. The script merges only the `module-design` block and preserves all other skills' config.

Once a spec exists at the resolved path, offer `refine` to put it through further rounds.
