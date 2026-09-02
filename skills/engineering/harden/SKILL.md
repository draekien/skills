---
name: harden
description: Simulates six months of a change, spec, design, or skill being used and misused, then reports the RICE-ranked changes worth making before it ships.
argument-hint: "[--mode inline|subagents] [target]"
disable-model-invocation: true
---

# Harden

Travel six months forward, live with the target as its future users will, record what went wrong and what went right, then return to the present and rank the changes that would have prevented the incidents without killing the successes.

The target is whatever the user brings: a git diff, a source module, a spec or PRD, an API surface, a document, a skill, or an idea described only in this session. Adapt the simulation to what the target actually is — a diff has callers and edge cases, a spec has readers and ambiguities, a skill has invoking agents and misfires.

## Brief

Establish two things before simulating: **what the target is** and **who touches it downstream**.

Explore the surrounding project for what the supplied context does not say — callers, adjacent modules, existing conventions the target must live beside. If the target is an idea with nothing in the project to explore yet, skip that exploration and ask the user directly about intended users, reach, and dependents. If the supplied context and the project together answer who uses this, how it is reached, and what depends on it, go straight to Timeshift. Ask only about the gaps that remain, and ask them in one batch.

Do not ask the user to predict the future. That is the skill's job.

Choose the simulation mode from the invocation: `--mode subagents` dispatches an independent subagent per lens, anything else runs inline. Default inline. Subagents cost more but stop one agent's blind spots from flattening all seven lenses into the same three obvious failures — use them on consequential or unusually broad targets.

## Timeshift

Move to six months from today and write **field reports** — incidents and successes recorded as they happened, in the past tense, dated by month offset.

Run every lens below. Each lens must yield at least one field report — three under `--mode subagents`, where an independent context has room to dig — or an explicit statement that it produced nothing, with the reason. A lens skipped in silence is a hole in the simulation.

| Lens          | The question it forces                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Adopters**  | Who chose this that it was never designed for, and what did they assume it did?                            |
| **Mutation**  | Where was it copied, forked, half-applied, or extended past its shape — and what broke in the copy?               |
| **Load**      | What changed in volume, frequency, concurrency, or size, and where did the design stop holding?                   |
| **Drift**     | The target stayed still while the world moved: dependencies, schemas, adjacent code, team turnover. What snapped? |
| **Edge**      | Which boundary input or state — empty, maximal, malformed, concurrent, partially failed — was hit in anger?       |
| **Handoff**   | A stranger owned it after the author left. What did they misread, and what did they break fixing something else? |
| **Success**   | What worked so well that people built on it, and what property made that possible?                               |

Under `--mode subagents`, dispatch one subagent per lens using [references/subagent-brief.md](references/subagent-brief.md), then merge their field reports as that brief directs.

Write each incident with: the month it happened, what triggered it, what broke, how far the damage spread, and the **root cause traced back to a specific property of the target as it exists today**. Write each success with the property that caused it.

## Return

Come back to the present. For each incident, name the change to the target that would have prevented it — concrete enough to act on: a signature, a guard, a renamed concept, a section the spec is missing, a constraint the skill never stated.

Then run every proposed change against the success list. A change that would have destroyed a recorded success is a regression, not a change worth keeping — say so and either reshape it or drop it. Note the ones that survived only after reshaping.

## Rank

Score each surviving change with RICE, using these fixed anchors so scores stay comparable between runs.

| Factor         | Anchor                                                                                  |
| -------------- | ----------------------------------------------------------------------------------------- |
| **Reach**      | How many future users, callers, or runs hit this incident over the six months (a count) |
| **Impact**     | Severity when hit: 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal                   |
| **Confidence** | How sure the prediction is: 100% seen before, 80% plausible, 50% speculative, 20% needs several unlikely things to align            |
| **Effort**     | Work to make the change today, in half-days (minimum 0.5)                               |

Score = Reach × Impact × Confidence ÷ Effort. Rank descending.

An incident needing several unlikely things to line up scores 20%, not exclusion — a rare catastrophe can still outrank a common annoyance.

## Report

Present the findings in chat, in this order:

1. **Verdict** — one paragraph: how the target held up, and the single most dangerous thing about it today.
2. **Field reports** — incidents grouped by lens, each with its month, trigger, blast radius, and present-day root cause. Successes listed separately, with the property to protect.
3. **Ranked changes** — a table of every surviving change: change, the incidents it prevents, R, I, C, E, score. Highest score first.
4. **Do not touch** — properties that caused the successes, and any change rejected for threatening them.
5. **Open risks** — incidents with no proportionate change, stated plainly rather than padded with a change nobody should make.

Stop at the report. Do not modify the target unless the user asks.

## Gotchas

- **An incident you cannot trace to a real property of the target is fiction.** Every field report must point at a line, a decision, or a specific omission that exists today. Generic misfortune — "the API was slow", "requirements changed" — teaches nothing and inflates the report.
- **A predicted incident is not a licence to generalise.** The most common damage this skill can do is overbuilding a simple target into a speculative framework. Prefer a guard, a name, or a stated constraint over a new abstraction layer, and reject any change whose only justification is a future that has not been simulated.
- **Simulate misuse, not malice.** The failures that matter come from reasonable people holding the target wrong, not from an attacker. Security failures belong in the report only when a lens actually produced one.
- **Do not rewrite the target's purpose.** Incidents caused by someone wanting a different thing entirely are out of scope; record them as adopter confusion — a naming or documentation problem — not as missing features.
- **Six months means six months.** Resist drifting to a horizon where anything can happen. Constrain predictions to changes plausible within two quarters for this project, this team, this codebase.
