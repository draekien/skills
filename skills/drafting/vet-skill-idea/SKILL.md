---
name: vet-skill-idea
description: Evaluates whether an idea should become an agent skill, checking it against worthiness criteria and routing it to build, split, redirect, or drop. Use when about to write a new skill, to avoid adding one that is not worth the ongoing context cost.
argument-hint: [skill idea]
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
disable-model-invocation: true
---

Every skill's description loads into context for every session in its scope. An unworthy skill is permanent tax that also dilutes activation for the skills that earn their place — so the default answer is no. The job here is to find the reason *not* to build a skill; only an idea that survives every gate below deserves one.

## The gates

An idea warrants a skill only by clearing all four. Each gate carries the test that discriminates a pass from a failure, and where a failure routes instead.

If the idea description is too vague to test against a gate, ask one focused question to clarify it before proceeding — do not evaluate an idea you cannot fairly test.

### Net-new capability

A skill is worth its context only if the agent does the task materially worse without it. Test against the base model: would a competent agent with no skill produce a worse result? If it already does the job well, the skill teaches nothing it doesn't already know — drop it. Restating knowledge the agent carries from training is the most common way this gate fails.

### Sound goal, not a gamed metric

A skill should instill an idea that moves the work toward the real outcome every time it runs — not chase a metric for its own sake. Test: can the skill be satisfied while missing the outcome? If success is box-ticking rather than the outcome landing, the skill optimises the metric and forgets the outcome. Reframe it around the outcome so that using it *causes* the outcome, or drop it.

### Single responsibility

One unified job. Test: state the purpose in one sentence without "and", and write a description that fires on one clear class of situations. An idea that needs several unrelated triggers is several skills wearing one name — split it into those pieces and run each back through the gates.

### Right home

A skill is one vehicle among several, and often the wrong one. A durable fact belongs in memory — it doesn't need re-teaching each session. An always-on project convention belongs in the project's rules or instructions file — it should apply without being invoked. An automated, deterministic behaviour — "after every X, do Y" — belongs in a hook, which the harness runs reliably; an agent reading a skill cannot guarantee it fires. A recurring one-keystroke invocation is a slash command — no judgment is needed to decide when it fires. If another vehicle fits better, name it and route there.

## Verdict

Evaluate all four gates before concluding — do not stop at the first failure. Then route by the earliest gate (in the order above) that failed, and name every gate that failed so the decision is legible:

- Net-new capability fails → drop.
- Sound goal fails → drop.
- Single responsibility fails → split into single-responsibility skills.
- Right home fails → redirect to the named vehicle.
- Clears all four → worth building.

If multiple gates fail, name all of them in the verdict — the person needs the full picture to reframe or drop the idea.

Once an idea passes, recommend the user run `/skill-writing` to author it — it is not model-invocable, so it must be invoked directly. If that skill is not installed, recommend the user add it with `npx skills add draekien/skills --skill "skill-writing"` first.
