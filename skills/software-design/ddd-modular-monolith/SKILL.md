---
name: ddd-modular-monolith
description: Applies domain-driven design to a modular monolith — carving bounded contexts into modules, modelling a module's aggregates, wiring cross-module contracts, enforcing boundaries in the build, auditing an existing codebase, and judging extraction readiness. Use when deciding what the modules are, designing inside one, reviewing whether boundaries hold, or when the user says "modular monolith", "module boundaries", "bounded contexts", "how should this module call that one", "enforce module boundaries", "should we split this into a service".
argument-hint: "[--mode shape|model|integrate|enforce|critique|extract] [--effort low|medium|high] [--runner inline|subagent] [module]"
---

# DDD Modular Monolith

A module boundary is enforced by nothing. A service boundary is enforced by the network; a module boundary holds only while something in the build refuses to allow a violation, and erodes the moment nothing does. Every mode here exists to make a boundary real rather than aspirational.

Explore the project before asking. The codebase already answers most questions about what the modules are.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes `ddd-modular-monolith` config from `.draekien/.skillsrc`.

## Session Start

Run once on first invocation, in this order:

1. **Load config** — run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill ddd-modular-monolith get architectureDir --default docs/architecture` to read the architecture directory. If the script is unavailable, parse `.draekien/.skillsrc` as JSON directly and read `ddd-modular-monolith.architectureDir`; default to `docs/architecture` if absent.
2. **Load the module map** — read `<architectureDir>/module-map.md` if it exists. It is the shared state every mode reads: the module list, dependency rules, data ownership and contracts. Where it is absent and the mode needs it, derive what is needed from the codebase and offer to write it.
3. **Settle the run** — take mode, effort and runner from the flags. Effort defaults to `medium`, runner to `subagent`. Unflagged, infer the mode from the request against the table below.
4. **Open question** — if the module, domain or code in scope is not already clear from the conversation, ask before proceeding.

## Modes

| Mode | Input | Rules to apply | Produces |
|------|-------|----------------|----------|
| `shape` | A domain, or a codebase with no module boundaries | [references/strategic-design.md](references/strategic-design.md) and [references/module-structure.md](references/module-structure.md) | The module map |
| `model` | One module | [references/tactical-patterns.md](references/tactical-patterns.md) | That module's spec |
| `integrate` | Two or more modules that must interact | [references/integration-patterns.md](references/integration-patterns.md) | Contracts and the dependency rows they add to the map |
| `enforce` | An existing module map | [references/enforcement.md](references/enforcement.md) | Boundary rules as checks in the project's own build |
| `critique` | Existing code | Every reference above | A violations report |
| `extract` | One module, to be split out | [references/extraction.md](references/extraction.md) | A readiness verdict and the work it names |

Inferring the mode when unflagged: no modules yet is `shape`; a named module to design inside is `model`; existing code to assess is `critique`; a question about splitting something out is `extract`. A request to "review the architecture" is `critique`, not `shape` — do not redesign what was only meant to be assessed.

Read the reference a mode names before drafting. These files carry the rules the mode is applying, and working from memory instead produces generic advice the user could have written themselves.

## Strict Constraint Enforcement

These five rules are non-negotiable. Check each decision against them as it is made. If a decision violates a strict rule, **block immediately**: name the rule, explain the specific violation, and ask the user to revise before continuing.

| Rule | Hard constraint |
|------|-----------------|
| **Module Owns Its Data** | Every table has exactly one owning module. No query, foreign key or migration crosses a module boundary — including hand-written reports and ORM navigation. |
| **Contract-Only Coupling** | Only a module's published contract crosses its boundary. Aggregates, entities, repositories, internal enums, persistence types and domain events stay inside. |
| **No Cross-Module Transaction** | One commit never spans two modules. Cross-module consistency is eventual, even when both modules share one database instance. |
| **Acyclic Dependencies** | The module graph has no cycle, and every allowed edge has a stated direction recorded in the module map. |
| **Invariant-Bounded Aggregates** | An aggregate boundary is a true invariant — a rule that must hold atomically — and one transaction modifies one aggregate. |

Blocking applies to decisions made outside the rounds loop. Inside a round, a strict-rule violation is a finding: Adjudicate applies it and the round continues without stopping for the user.

The first three all have the same disguise: they look correct because they work today. A cross-schema join runs, a two-module transaction commits, a leaked entity compiles. Each becomes a rewrite the day the boundary is tested.

## Rounds

Every mode produces an initial draft, then loops over it before anything reaches the user or the disk.

`--effort` sets the round budget:

| Effort | Rounds |
|--------|--------|
| `low` | 1 |
| `medium` (default) | 3 |
| `high` | 5 |

`--runner` decides where a round executes. `subagent` (the default) dispatches it to a fresh context — fresh eyes catch what the draft's own author cannot see. `inline` runs it here, keeping the reasoning visible and costing no dispatch.

Each round is critique-and-refine over the current draft:

1. **Critique** — check the draft against every rule in the reference the mode names, and against the five strict rules. For each violation, quote the offending text and name the rule.
2. **Refine** — write the concrete replacement text for each finding. Nothing lands in the draft at this step.
3. **Adjudicate** — take each finding on its merits: apply it, or reject it with a reason. Apply the accepted changes before the next round starts.

Under `--runner subagent`, steps 1 and 2 belong to the subagent and step 3 is always yours — the subagent proposes, it never commits. Dispatch brief: [references/critique-brief.md](references/critique-brief.md). Under `--runner inline`, do all three yourself.

A finding that names a strict rule is applied, never rejected.

Rounds run without stopping for the user — the user's gate is the finished draft, not each round. Record every finding as it is adjudicated; the record ships with the draft.

Stop early when a round returns no findings, or when every finding in a round is rejected: the budget is a ceiling, not a quota.

Rounds are done when the budget is spent or a round stops it early, and every finding from every round sits in the record as applied, or rejected with its reason.

## Mode specifics

**`shape`** — classify every module's subdomain before designing any of it; the type decides how much modelling the module earns, and skipping it produces four core modules where one was warranted. Apply the change test to each proposed boundary: a typical business change should touch exactly one module. Done when every module has a subdomain type, every dependency edge has a direction and a mechanism, every table group has an owner, and the layout names what will refuse a violation.

**`model`** — the module's subdomain type governs. A supporting or generic module gets a transaction script and a table; building aggregates there is the most common over-application of this skill. Done when every aggregate's boundary is stated as the invariant it holds, and every cross-aggregate rule is either inside one boundary or handled by an event.

**`integrate`** — pick the mechanism per interaction, cheapest that satisfies the requirement, and add the resulting edge to the module map. Done when each interaction names its mechanism, its contract, and its consistency expectation.

**`enforce`** — detect what the project already uses before writing anything: read its build files, find the existing test or lint setup, and match it. Where no test infrastructure exists, do not make one a prerequisite — take the cheapest rung of the ladder in the reference, say which rung the project is on, and name what it does not catch. Recommend tooling rather than installing it. Done when every dependency row in the module map has a check, or an explicit note saying why it has none.

**`critique`** — report, do not redesign. For each violation, quote the offending code with its file path, name the rule, and give a concrete fix. If none survive the rounds, say so explicitly. Offer to write the module map or a redesign spec either way. Done when every violation surviving the rounds is reported with a concrete fix, or the report states explicitly that none survived, and the offer to write a module map or redesign spec has been made.

**`extract`** — work the readiness table row by row; every row must pass. A single failing row means "not yet" and names the work. Challenge the reason for extracting before assessing readiness: coupling that hurts in one process hurts more across a network, and extraction adds a boundary rather than fixing a misplaced one. Done when the verdict is stated, every failing row has the work it implies, and the sequence for that work is data first, then contract, then network.

## Output

Resolve the output path from `architectureDir`, defaulting to `docs/architecture`.

| Mode | File |
|------|------|
| `shape` | `module-map.md` |
| `model`, `integrate` | `<module-name>.md`, kebab-case |
| `enforce` | Test or lint files in the project's existing location, plus the enforcement note in `module-map.md` |
| `critique`, `extract` | Presented in conversation; written only if the user asks |

Before writing `module-map.md` or any module spec, read [references/architecture-docs.md](references/architecture-docs.md) for the section layout each one uses. Free-form output here is what the next reader has to reverse-engineer.

Present the refined draft, including its refinement record, and apply any corrections before writing to disk. Where the target file exists, write directly. Where the directory does not exist, confirm the full path first. If the user provides a custom path, confirm it, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill ddd-modular-monolith set architectureDir <path>` to persist it — the script merges only the `ddd-modular-monolith` block and preserves all other skills' config. Config writes require confirmation per [references/skillsrc-format.md](references/skillsrc-format.md).

## Gotchas

- **Equal ceremony for every module is the monolith-specific failure.** No deployment boundary hurts, so nothing pushes back on a generic module growing its own aggregates to compete with a vendor's model. Classify first, then model.
- **A tidy module map proves nothing.** The map says `shipping` does not read `ordering`'s tables; a hand-written report joins them anyway. Where code is available, verify the claim rather than restating it.
- **"It is all one database, so a transaction is fine" is the trap that works.** It commits, it passes tests, and it welds two modules together permanently.
- **Organising modules by entity looks like domain modelling and is not.** `OrderModule`, `CustomerModule`, `ProductModule` means "place an order" now needs three modules in lockstep. Modules are business capabilities.
- **Extraction is not the goal and not a grade.** Design the boundaries to pay for themselves today — in comprehension, ownership and blast radius. Boundaries erode more often than they graduate into services.
- **Do not define domain terms here.** Term definitions and bounded-context vocabulary belong to the `ubiquitous-language` skill, which tracks them in a project dictionary and detects conflicts. Install it with `/plugin install software-design-skills@draekien-skills`, or `npx skills add draekien/skills --skill "ubiquitous-language"`, and ask the user to run it. Never duplicate its dictionary.
- **Do not design a class here.** Design of a single method, class or layer against general software-design principles belongs to the `module-design` skill, installed the same way or with `npx skills add draekien/skills --skill "module-design"`. This skill stops at the module's contract and its aggregates.
