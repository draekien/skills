---
name: vet-skill-idea
description: Evaluates whether an idea should become an agent skill, checking it against worthiness criteria and routing it to build, split, redirect, or drop. Run this before writing a new skill, to avoid adding one that is not worth the ongoing context cost.
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
disable-model-invocation: true
---

Every skill's description loads into context for every session in its scope. An unworthy skill is permanent tax that also dilutes activation for the skills that earn their place — so the default answer is no. The job here is to find the reason *not* to build a skill; only a concept that survives every gate below deserves one.

## The gates

A concept warrants a skill only by clearing all four. Each gate carries the test that discriminates a pass from a failure, and where a failure routes instead.

If the concept description is too vague to test against a gate, ask one focused question to clarify it before proceeding — do not evaluate a concept you cannot fairly test.

### Net-new capability

A skill is worth its context only if the agent does the task materially worse without it. Test against the base model: would a competent agent with no skill produce a worse result? If it already does the job well, the skill teaches nothing it doesn't already know — drop it. Restating knowledge the agent carries from training is the most common way this gate fails.

### Sound goal, not a gamed metric

A skill should instill a concept that moves the work toward the real outcome every time it runs — not chase a number for its own sake. Test: can the skill be satisfied while missing the point? If success is box-ticking rather than the idea landing, the skill optimises the proxy and rots the target. Reframe it around the underlying concept so that using it *causes* the outcome, or drop it.

### Single responsibility

One unified job. Test: state the purpose in one sentence without "and", and write a description that fires on one clear class of situations. A concept that needs several unrelated triggers is several skills wearing one name — split it into those pieces and run each back through the gates.

### Right home

A skill is one vehicle among several, and often the wrong one. A durable fact belongs in memory. An always-on project convention belongs in the project's rules or instructions file. An automated, deterministic behaviour — "after every X, do Y" — belongs in a hook, which the harness runs reliably; an agent reading a skill cannot guarantee it fires. A recurring one-keystroke invocation is a slash command. If another vehicle fits better, name it and route there.

## Verdict

Route by the first gate that fails, and name the gate so the decision is legible:

- Net-new capability fails → drop.
- Sound goal fails → drop.
- Single responsibility fails → split into single-responsibility skills.
- Right home fails → redirect to the named vehicle.
- Clears all four → worth building.

If multiple gates fail, name all of them in the verdict — the person needs the full picture to reframe or drop the idea.

Once a concept passes, hand off to the `skill-writing` skill to author it. If that skill is not installed, recommend the user add it with `npx skills add draekien/skills --skill "skill-writing"` before authoring.
