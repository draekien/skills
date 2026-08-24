---
name: picking-models
description: Picks which model runs a subagent, workflow step, or agent team member by classifying the task's role, then taking the cheapest model that clears that role's bar. Use when dispatching a subagent, staffing an agent team, choosing a model for a workflow step, or when a delegated task keeps coming back wrong — or when the user says "which model", "what model should I use", "pick a model", "model selection".
argument-hint: "[task description]"
---

Every dispatch names a model. Omitting the field is not a neutral default — it silently runs the subagent on the parent's model, so a fan-out of file reads burns orchestrator-grade spend and a security review runs on whatever happened to be driving the session.

The goal is never the best model. It is the **cheapest model that clears the bar** — the least capable model that still finishes the task in one pass. Overshooting wastes spend on every dispatch; undershooting costs more than it saves, because a model that loops three times and still needs correcting is more expensive than one pass on the tier above.

Selection runs on four dimensions, scored 1-10, higher is better:

- **Speed** — latency and throughput.
- **Taste** — output craft: prose, coding, UI/UX, restraint.
- **Intelligence** — reasoning depth, long-horizon reliability, tool use, completion rate.
- **Cost** — efficiency of total spend to finish the task, not price per token.

## Classify

Match the task to a role. The role fixes a **leading dimension** and a **bar** — the minimum score on that dimension the task demands. Classify on what the task actually demands, not on what it is called.

| Role | Tasks | Leading dimension | Bar |
| --- | --- | --- | --- |
| Orchestrator | plan, decompose, delegate, synthesise | Intelligence | 9 |
| Heavy worker | complex implementation, deep analysis, long-horizon | Intelligence | 9 |
| Reviewer | code review, verification, security, QA | Intelligence | 9 |
| Editor | final pass, polish, voice, anything shipping to an audience | Taste | 9 |
| Worker | bounded implementation, known patterns, targeted investigation | Intelligence | 7 |
| Writer | first drafts, bulk prose, docs from a spec, routine copy | Taste | 7 |
| Scout | search, extract, classify, file reads, fan-out | Intelligence | 2 |

Two tests separate the worker tiers, and they decide most classifications:

- **Can the acceptance criteria be written before the agent starts?** Yes and the steps are independent → scout. Yes but the work is a single bounded pass → worker. No, the output has to be read to judge it → heavy worker.
- **Who supplies the rubric?** A scout follows one it is given. A worker applies a known pattern. A heavy worker builds its own as it goes.

Search with judgment is not scouting. "Find every file importing X" is a scout task — checkable against the repo. "Find where the auth logic lives" is a worker task, because the agent decides what counts as auth logic.

A task that splits across roles is two tasks — dispatch it as two subagents on two models rather than averaging into one compromise.

## Resolve

Read [references/model-matrix.md](references/model-matrix.md) for the scores. Do this on every selection: the lineup shifts between releases, and the matrix carries the rule for scoring a model it does not list.

Dispatch takes an **alias** — `haiku`, `sonnet`, `opus`, `fable` — not a version string. Selection resolves to an alias; the harness picks the generation. Full model IDs apply only where one is accepted: agent-definition frontmatter, the API, the SDK.

Against the aliases this harness offers:

1. Drop `fable` from the candidates — it is gated, see below.
2. Keep every alias scoring at or above the role's bar on its leading dimension.
3. Take the cheapest one that remains.
4. On a cost tie, take the higher score on the leading dimension; still tied, the newer generation.

Resolution is mechanical once the role is fixed. Do not override the result on a hunch about the specific task — if the pick feels wrong, the role was misclassified. Reclassify and resolve again.

## Escalate

The trigger is two failures of the same task — wrong, incomplete, or looping. One failure is noise; re-running after a single miss spends more than it saves.

On the second failure, re-run on the next model up the **Intelligence** ladder, whatever the role's leading dimension was. Repeat failure means the task exceeded the model's reasoning, not its taste or speed.

Escalation is sticky within the session: once a class of task has escalated, start similar tasks on the escalated model rather than paying the two failures again.

## The Fable gate

`fable` is never an autonomous starting model. It is reachable two ways only: as the ceiling of an escalation chain, or because a human named it.

It carries safety classifiers and can refuse partway through a task. A classifier refusal is not a capability failure — stop escalating, do not retry, and surface it to the human. There is nothing above `fable` to escalate to, and a retry buys another refusal.

## Gotchas

- **A fork inherits the parent model.** Dispatching a fork to save spend does nothing; a model override on a fork is ignored. Use a fresh subagent when the point is to run cheaper.
- **Cheap-but-looping is not cheap.** Cost scores efficiency of total spend to finish, not price per token. A scout that needs three passes and a correction was a worker task all along.
- **The bar is a floor, not a target.** Clearing it by a wide margin is overspend, not safety. Take the cheapest alias above the line, not the strongest.
- **Cost never overrides the bar.** A reviewer bar exists so that saving spend cannot quietly downgrade a security review.
- **The matrix scores models, not agent definitions.** A named agent type may pin its own model; when it does, that pin wins and this skill has nothing to decide.

Selection is done when every dispatch in the plan names a model, each traceable to a role, a bar, and the cheapest alias that clears it.
