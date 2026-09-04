---
name: picking-models
description: Picks which model runs a subagent, workflow step, or agent team member by classifying what the work is and how much judgment it takes, then taking the cheapest model that clears the bar. Use when dispatching a subagent, staffing an agent team, choosing a model for a workflow step, or when a delegated task keeps coming back wrong — or when the user says "which model", "what model should I use", "pick a model", "model selection".
argument-hint: "[task description] [--fable]"
---

Every dispatch names a model. Omitting the field is not a neutral default — it silently runs the subagent on the parent's model, so a fan-out of file reads burns orchestrator-grade spend and a security review runs on whatever happened to be driving the session.

The goal is never the best model. It is the **cheapest model that clears the bar** — the least capable model that still finishes the task in one pass. Overshooting wastes spend on every dispatch; undershooting costs more than it saves, because a model that loops three times and still needs correcting is more expensive than one pass on the tier above.

Selection runs on four dimensions, scored 1-10, higher is better:

- **Speed** — latency and throughput.
- **Taste** — output craft: prose, coding, UI/UX, restraint.
- **Intelligence** — reasoning depth, long-horizon reliability, tool use, completion rate.
- **Cost** — efficiency of total spend to finish the task, not price per token.

## Classify

Two lookups, not one. **What the work is** fixes the leading dimension. **How much judgment it takes** fixes the bar — the minimum score on that dimension the task demands. Classify on what the task actually demands, not on what it is called.

### What the work is

| Work | Leading dimension |
| --- | --- |
| Orchestrate — plan, decompose, delegate, synthesise | Intelligence |
| Build — implement, refactor, fix | Intelligence |
| Review — verify, audit, QA | Intelligence |
| Write — draft, edit, polish | Taste |
| Search — find, extract, classify | Intelligence |

### How much judgment it takes

One test decides it: **can the acceptance criteria be written before the agent starts?**

| Judgment | Test | Bar |
| --- | --- | --- |
| Mechanical | Yes, and the steps are independent — output is checkable against a source | 2 |
| Bounded | Yes, but it needs one bounded pass of judgment against a known pattern or a supplied rubric | 7 |
| Open | No — the agent builds its own criteria, and the output has to be read to be judged | 9 |

Worked examples across the grid:

| Work | Mechanical | Bounded | Open |
| --- | --- | --- | --- |
| Orchestrate | run a written dispatch list | fan out an existing plan, collate results | plan from scratch, decompose something unscoped |
| Build | renames, codemods, mechanical edits | bounded implementation on known patterns | complex implementation, deep analysis, long-horizon work |
| Review | presence checks, lint-style rules | a diff against a stated convention | security, correctness, unfamiliar code |
| Write | fill a template, mechanical copy | first drafts, docs from a spec | final pass, voice, anything shipping to an audience |
| Search | "every file importing X" | "where does the auth logic live" | open-ended research and synthesis |

Two floors override the test:

- **Review of security or correctness never drops below Bounded**, however mechanical the check looks. Cost cannot quietly downgrade a security review.
- **A task that splits across two cells is two tasks.** Dispatch it as two subagents on two models rather than averaging into one compromise.

## Resolve

Read [references/model-matrix.md](references/model-matrix.md) for the scores. Do this on every selection: the lineup shifts between releases, and the matrix carries the rule for scoring a model it does not list.

Dispatch takes an **alias** — `haiku`, `sonnet`, `opus`, `fable` — not a version string. Selection resolves to an alias; the harness picks the generation. Full model IDs apply only where one is accepted: agent-definition frontmatter, the API, the SDK.

Against the aliases this harness offers:

1. Drop `fable` from the candidates — it is gated, see below.
2. Keep every alias scoring at or above the bar on the leading dimension.
3. Take the cheapest one that remains.
4. On a cost tie, take the higher score on the leading dimension; still tied, the newer generation.

Resolution is mechanical once both lookups are fixed. Do not override the result on a hunch about the specific task — if the pick feels wrong, one of the two lookups is wrong. Reclassify and resolve again.

## Escalate

The trigger is two failures of the same task — wrong, incomplete, or looping. One failure is noise; re-running after a single miss spends more than it saves.

On the second failure, re-run on the next model up the **Intelligence** ladder, whatever the leading dimension was. Repeat failure means the task exceeded the model's reasoning, not its taste or speed.

Escalation is sticky within the session: once a class of task has escalated, start similar tasks on the escalated model rather than paying the two failures again.

## The Fable gate

`fable` is never an autonomous starting model. It is reachable two ways only: as the ceiling of an escalation chain, or because a human named it.

**`--fable` is the human naming it.** The flag skips resolution rather than joining it — `fable` scores worst on Cost, so re-adding it as a candidate would only see it dropped again at step 3. Passing the flag means the human has decided; take `fable` and stop.

The flag applies per dispatch, not per session. On a plan of several dispatches, apply it to the one the human was pointing at and resolve the rest normally — a whole fan-out on `fable` is almost never what the flag was for. If the plan has more than one plausible target, ask which.

It carries safety classifiers and can refuse partway through a task. A classifier refusal is not a capability failure — stop escalating, do not retry, and surface it to the human. There is nothing above `fable` to escalate to, and a retry buys another refusal.

## Gotchas

- **Work that arrives scoped is Bounded.** Once an orchestrator has written the plan, the dispatches it fans out already have criteria — they are Bounded, not Open. Running them on the planner's own model pays a second time for thinking already done.
- **A fork inherits the parent model.** Dispatching a fork to save spend does nothing; a model override on a fork is ignored. Use a fresh subagent when the point is to run cheaper.
- **Cheap-but-looping is not cheap.** Cost scores efficiency of total spend to finish, not price per token. A Mechanical dispatch that needs three passes and a correction was Bounded all along.
- **The bar is a floor, not a target.** Clearing it by a wide margin is overspend, not safety. Take the cheapest alias above the line, not the strongest.
- **Search with judgment is not Mechanical.** "Find every file importing X" is checkable against the repo. "Find where the auth logic lives" is Bounded, because the agent decides what counts as auth logic.
- **The matrix scores models, not agent definitions.** A named agent type may pin its own model; when it does, that pin wins and this skill has nothing to decide.

Selection is done when every dispatch in the plan names a model, each traceable to a cell in the grid, a bar, and the cheapest alias that clears it.
