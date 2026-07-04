---
name: break-down-prd
description: Decomposes a PRD into tracer-bullet-style tasks, classified autonomous (AFK) versus human-in-the-loop (HIL), with per-bullet dependency trees that maximise parallel execution. Use after drafting a PRD, to turn it into an actionable task list.
disable-model-invocation: true
---

# Break Down a PRD

Turn a PRD into an ordered set of tracer bullets — thin, end-to-end, always-demoable increments — where each bullet is a self-contained artefact whose tasks are classified AFK (an agent can complete it unsupervised) or HIL (a human must be in the loop), wired into a dependency tree that runs as much in parallel as the work allows. This skill plans the work; it does not execute the tasks.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes the `break-down-prd` output directory in `.draekien/.skillsrc`.

## Session start

Resolve the output directory: run the skillsrc helper script to read the output directory from `.draekien/.skillsrc` (default: `.draekien/break-down-prd`). Write the breakdown to `<outputDir>/<prd-slug>/`, where `<prd-slug>` is the kebab-cased feature name.

## Get the PRD

Work from a PRD in the draft-a-prd format — Problem Statement, Goals / Success Criteria, User Stories, Testing Decisions, Out of Scope, Additional Notes, Open Questions. Use a file path if the user gives one; otherwise use the PRD already in the conversation; otherwise ask where it is. If the PRD does not use this format, map its content onto these sections and note any absent ones; missing Open Questions and missing measurable Goals must both be surfaced as gaps in the overview coverage table before proceeding.

## Structure as tracer bullets

A tracer bullet is a thin slice that runs end-to-end in the real system — lean but complete, with real structure and error handling, not a throwaway prototype. The breakdown is an ordered sequence of bullets:

- **Bullet 1 is the walking skeleton** — the thinnest slice that connects the riskiest part of the PRD to at least one real entry point and one real persistence/output boundary. It need not touch every component; it must touch those the skeleton's risk depends on. Find that risk in the Open Questions, in anything novel or unproven, and in the Testing Decisions' constraints, and attack it first. That is where the plan is most likely wrong, so the earliest feedback is worth the most.
- **Each later bullet adds one capability**, also end-to-end, so the system stays demoable after every bullet. A reviewer can judge how close each increment is to the target.

Bullets run in sequence. Within a bullet, two tasks are parallel unless a dependency forces an order between them — so order tasks by genuine dependency, never by guesswork, and let the dependency tree expose the maximum that can run at once.

## Classify every task: AFK or HIL

Tag each task:

- **AFK** — an agent can complete it unsupervised, end to end.
- **HIL** — a human must be in the loop.

A task is HIL only when it is *irreducibly* so — when one of these holds and cannot be designed away:

1. it needs subjective human judgment or taste (is this copy on-brand, does this layout feel right);
2. it needs a real-world action or credential the agent cannot hold (provisioning access, signing off, configuring a third-party account);
3. it is blocked on information that does not yet exist (an external team's answer, a not-yet-run experiment);
4. it carries irreversible or high-blast-radius risk that warrants human approval (destructive migration, production deletion).

Everything else is AFK.

When a task is HIL, **decompose it**. Split it into finer-grained tasks within the same bullet (or across bullets if the scope warrants) and peel the AFK parts away — the setup, the scaffolding, the reversible preparation — until only the smallest kernel still carries the HIL reason. A "deploy to production" task is mostly AFK (build, stage, dry-run, prepare rollback) wrapped around one HIL kernel (approve the cutover). Isolate that kernel and tag only it HIL.

### Honest classification is the whole point

The breakdown exists so a human can trust it: the AFK tasks are genuinely safe to run unsupervised, and every place a human is actually needed is flagged. A breakdown that *looks* autonomous because HIL work was mislabelled AFK is worse than useless — it sends an agent to make subjective calls or take irreversible actions with no human present.

So never optimise for a high AFK count. "Mostly AFK" is what a well-decomposed PRD looks like *after* honest classification and HIL-kernel isolation — it is a consequence, never a target. If a task meets a HIL criterion and cannot be decomposed further, it stays HIL. Trading classification accuracy for a better-looking ratio defeats the skill.

## Write the breakdown

Create one file per bullet plus an overview, in `<outputDir>/<prd-slug>/`:

- `00-overview.md` — from [assets/overview-template.md](assets/overview-template.md)
- `01-<slug>.md`, `02-<slug>.md`, … — one self-contained file per bullet, from [assets/bullet-template.md](assets/bullet-template.md)

A bullet file is self-contained: an executor needs nothing beyond it — the goal, the PRD items it serves (quoted), the task checklist with `[AFK]`/`[HIL]` tags, the Mermaid dependency tree, and the HIL callouts naming the human decision each HIL task needs and the HIL criterion that makes it irreducible (judgment / credential / blocked-on-info / high-risk approval).

Every task cites the PRD user story or measurable goal it serves. The inline `serves:` field is authoritative; the header block is a derived summary — keep it in sync when tasks change. The overview's coverage table maps each PRD user story and each measurable goal to the task(s) covering it, and flags any that no task covers — an uncovered requirement is a gap to surface, not to ship.

If `<outputDir>` is under `.draekien/` and that directory does not yet exist, confirm its creation with the user before the first write. If the user declines, ask for an alternative path, persist it with the `set` command, and write nothing until a confirmed output directory exists. If the user chooses a custom output directory, confirm it, then persist it using the skillsrc helper script's `set` command.

## Review

Once the files are written (including any required confirmations already obtained), present a summary — bullet order, AFK versus HIL counts, the front-loaded risks, and any coverage gaps — and invite feedback. On each revision cycle, re-audit every bullet file: for each task's `serves:` field, confirm the referenced PRD item still exists and is still required. Then rebuild the overview table from those audited mappings, flag any PRD user story or measurable goal no task covers, and update the overview file before presenting the revised summary. Complete when the user explicitly approves.
