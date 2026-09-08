---
name: prefer-skills
description: Installs a short standing rule in your global agent instructions so the agent checks for a relevant skill and invokes it before working from training — or removes that rule again. Use when skill invocations keep getting skipped in favour of guesswork and rework.
argument-hint: "[--mode install|remove] [--scope global|project]"
disable-model-invocation: true
---

A skill only helps when it is invoked, and an agent left alone reaches for what it already knows. The fix is not another skill competing for activation — it is three lines in the instructions file that loads on every turn. This skill puts them there, and takes them out again.

## Route

Mode: **install**, unless the request is to take the rule out, drop it, or undo it — that is **remove**. An explicit `--mode` wins outright.

Scope: **global** by default — the instructions file that applies to every project. `--scope project` writes to the current repository's instructions file *instead*: it never also writes global, and never removes a global copy already there.

## The rule

Insert exactly this, adapting only the heading depth to the target file:

```markdown
## Skills

Scan available skills before each task and invoke what fits — a skill beats
working from memory. Re-scan when the task shifts or you are about to guess.
Say which skill you used, or that none fit.
```

Every word is paid for on every turn, so the text is fixed. Do not expand it with examples, rationale, or a list of installed skills: a longer rule is not obeyed harder.

## Install

1. **Read before proposing.** Locate the instructions files in the resolved scope and read each in full — global scope may hold more than one when several agent harnesses are installed (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, and their equivalents). A blind append lands the rule under a heading that changes its meaning. When the scope holds no instructions file at all, propose creating one.
2. **Hunt the rule already there, however worded.** A line telling the agent to check for skills, prefer a skill, or look at its skills before acting is this rule wearing different words. Revise that line into the canonical text rather than adding a second — two copies of one instruction compete, and the weaker wording wins as often as the stronger.
3. **Place it among the standing rules**, not appended at the end under project detail it has nothing to do with. Match the file's existing heading depth and register.
4. **Propose, then wait.** Show each file path and the exact insertion in context — the surrounding lines, the rule, and whatever it replaces. Apply nothing until the user approves. Where several files are in scope, list them all so the user can pare the set back.

Done when every file the user approved carries the rule exactly once, and the user has seen the final wording of each edit.

## Remove

Locate the rule in the resolved scope, show each file path with the exact lines to be deleted, and get an explicit yes before touching anything. Report a scope that carries no such rule plainly, rather than removing the nearest line that happens to mention skills. Delete only within the scope asked for — a removal at project scope leaves a global copy standing, and the reverse. Take the surrounding heading with the rule only where the rule was its whole content.

## Gotchas

- A project instructions file is usually committed, so a project-scope rule governs everyone working in that repository. Say so before writing, and steer to global scope when the intent is the user's own habit rather than a team convention.
- The rule cannot force the invocation. The instructions file loads every turn, but the agent still decides; the rule's job is to make skipping an applicable skill read as a deviation. When it demonstrably stops working, the answer is a mechanism that fires mechanically — a hook, or a check — never a longer rule.
