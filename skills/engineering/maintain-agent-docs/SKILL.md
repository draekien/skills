---
name: maintain-agent-docs
description: Audits a repository's existing agent docs and reports what would mislead an agent — guidance gone stale against the code, or placed where the wrong agents read it. Repairs findings with --fix.
argument-hint: "[--effort low|mid|high|xhigh|max] [--scope drift|shape] [--target path] [--fix safe|unsafe]"
disable-model-invocation: true
---

# Maintain agent docs

Agent docs fail two ways, and the two need separating all the way through to the report because they resolve differently.

**Drift** — the document is no longer true. An agent that reads it and acts does the wrong thing.

**Shape** — every line is true, but the document is built so an agent reads the wrong thing first: guidance for one directory sitting in the always-loaded root file, this quarter's migration written as a permanent rule, a convention stated as prose that a linter would enforce for free.

The bar for both is **the contract** — the conventions this repository committed to, recorded in its own convention docs, typically `docs/AGENTS.md` and `docs/adr/AGENTS.md` or wherever this repository keeps them. Not the conventions a well-run repository usually has. That distinction carries the whole skill; see [Anti-patterns](#anti-patterns).

## Establish the contract

First identify **the root document** — the file at the repository root that an agent actually reads for standing guidance. It may be `AGENTS.md`, `CLAUDE.md`, or an equivalent another tool reads. What decides is content, not filename: a file holding nothing but an import line is a pointer, and the file it points at is the root document.

- **One file holds the guidance** — that file is the root document, whichever name it carries. Audit it in place. Do not propose renaming it or migrating to a different convention; a repository that keeps its guidance in `CLAUDE.md` has made a choice, and reshaping the doc set to a preferred layout is scaffolding, not maintenance.
- **One holds guidance, another imports it** — the imported file is the root document, and the import-only file is checked against the import discipline.
- **Two or more hold guidance independently** — every one is a root document, and the split is itself a finding: an agent reads whichever it finds first, so the two will diverge. Report it as a cross-document finding and let the user say which should own the guidance.
- **None exist** — stop. Report that there is nothing to maintain and point at `init-agent-docs`. This skill corrects existing docs; it never scaffolds.

Then read the repository's own convention docs, before forming any finding. They define the frontmatter form, the status discipline, the ADR bar, and the directory purposes this audit measures against — including where this repository deliberately diverged from convention.

Where a root document exists but the convention docs do not, audit against what the docs claim about themselves and about the code, and state in the report that the contract was unavailable, so the user can see the findings rest on a narrower basis. With no contract, structural-invariant checks reduce to internal consistency and link integrity: raise no finding about frontmatter form or status vocabulary, and apply nothing mechanically. General convention is not a substitute for the contract.

## Scope the pass

`--target` bounds the doc set: a directory, or a single document. Absent, the doc set is every agent-facing document — the root document, every nested `AGENTS.md` or `CLAUDE.md`, the import-only files that point at them, and everything under `docs/`. A nested document is resolved the same way as the root one: content decides which file governs that subtree.

The root document and the convention docs are read whatever `--target` says, because a nested document cannot be judged without the rules it inherits. The bound governs which documents can carry a finding, not which are read.

Where `--target` selects no documents, report that: name the target and the documents that exist outside it. Never widen the scope unasked — a silent widening produces findings about documents the user excluded on purpose.

Read each document in scope in full; they are few and short. Open code only to verify a specific claim a document makes, so cost scales with the doc set rather than with the repository.

## Route by effort

`--effort` selects which finding classes are in play. Levels are cumulative — each includes every class below it. Absent, the level is `mid`.

`--scope drift` or `--scope shape` restricts the pass to one axis. Absent, both run. The two flags compose: a class is active only when its level is reached and its axis is in scope, so `--effort xhigh --scope shape` runs transient state, scoping, and guardrails, and no drift class at all.

Read a class's reference before hunting for that class, and read no others. A scoped-out axis loads none of its references.

| Level | Adds | Reference |
| --- | --- | --- |
| `low` | Structural invariants | [references/drift-invariants.md](references/drift-invariants.md) |
| | Transient state | [references/shape-transient.md](references/shape-transient.md) |
| `mid` | Claim verification | [references/drift-claims.md](references/drift-claims.md) |
| `high` | Cross-document contradictions | [references/drift-cross-doc.md](references/drift-cross-doc.md) |
| | Scoping and progressive disclosure | [references/shape-scoping.md](references/shape-scoping.md) |
| `xhigh` | History rot and unrecorded decisions | [references/drift-history.md](references/drift-history.md) |
| | Guardrail candidates | [references/shape-guardrails.md](references/shape-guardrails.md) |
| `max` | No new classes. The confidence bar drops, so findings that are probable rather than proven surface, alongside claims that resist falsification — each marked as such | |

Two rules hold across the routing:

- **A probable finding is never applied**, in any `--fix` mode. Marking it probable and then writing it anyway defeats the mark.
- **A class that hands a finding to a class this run has not activated still reports it**, as an unresolved finding of the receiving class, named as out of level or out of scope. Never resolve it under the sending class's resolution — that is how a line gets deleted mechanically on the strength of a check the pass never ran.

## Resolve by class

Each class resolves one of four ways. The class decides, not the finding's severity.

| Resolution | Classes | Behaviour |
| --- | --- | --- |
| **Mechanical** | Structural invariants, transient state | One correct answer exists. Apply it. |
| **Approval** | Scoping and progressive disclosure | Propose the move: the lines, the destination, and the evidence for that scope. Apply only what the user accepts. |
| **Interview** | Claim verification, cross-document contradictions, history rot | The audit knows two things disagree, not which is the mistake. Ask. |
| **Recommendation** | Guardrail candidates | Name the mechanism and what the prose becomes. Never build it. |

An interview finding is never resolved by presuming the code is right. A document line can be a real rule the code violates — that is a code defect, and rewriting the document to match deletes the rule that exposes it. Surface both sides with the evidence for each, one finding at a time, and let the user say which is true.

## Write only when asked

| Invocation | Applies |
| --- | --- |
| no `--fix` | Nothing during the pass. Every finding goes to the disposition, and what the user accepts there is written. |
| `--fix`, `--fix safe` | Mechanical classes, during the pass. Approval and recommendation classes still go to the disposition. |
| `--fix unsafe` | Mechanical classes, plus approval-class moves without asking. Guardrail findings are filed as plans. |

Interview findings are asked in every mode, `--fix unsafe` included. An interview answer authorises the write for that finding alone.

`--fix unsafe` does not apply a move whose blast radius rests on judgement rather than on paths verified in the code. Report those as proposals instead: a rule moved too far down goes quiet rather than visibly wrong, so it is the one approval-class finding an unattended run must not guess at.

Repairs follow the audited repository's own status discipline, so nothing is deleted: a shipped plan is marked done, a replaced decision is superseded, a document that has outlived its purpose is reported rather than removed.

## Report

Rank findings by one test: **would an agent reading this document today do the wrong thing?** A rule that contradicts working code outranks a stale date. Keep drift and shape in separate sections — a reader deciding what to accept needs to know whether a document is wrong or merely badly placed.

For each finding: the document and lines, the class, the evidence, and the resolution taken or proposed. Findings already applied under `--fix` are listed as done, not as pending.

Close with what was left and why — interview findings the user deferred, guardrail recommendations not taken, and the classes this run did not cover, naming whether each was out of level or out of scope. A scoped run reports one axis and says the other went unexamined; a reader must never mistake a narrow pass for a clean one.

## Disposition

Where findings remain open, offer three routes. They compose, and where the user files or actions, they choose which findings go that way rather than accepting all of them.

- **Save the report** — a dated document under the repository's explorations directory, since an audit is evidence gathered. Accept any path the user names instead, inside or outside the repository. Where no explorations directory exists, ask for a path rather than creating one.
- **File plans** — one dated plan per accepted finding group, in the format the repository's own documentation conventions define.
- **Action now** — apply the accepted findings in this session. Accepting a finding here is the authorisation `--fix` would have carried, so this route writes even on a run invoked without it.

## Anti-patterns

**Auditing against the agent's own taste.** This one is dangerous because the output looks like good work: a convention gets flagged because a different repository would do it differently, and the user accepts a rewrite that erases a deliberate local decision. A rule the audit would not have chosen is still the rule. The only grounds for a finding are that a document contradicts the code, contradicts another document, has rotted, or is shaped so an agent reads the wrong thing first — never that a convention is unusual.

**Splitting by size.** Length is not the trigger for a split; blast radius is. A long document of genuinely repository-wide rules stays whole, and a short one holding directory-specific rules gets scoped.

**Auditing the code.** Verifying a claim surfaces real defects in passing. They are not findings of this pass — mention them once in the report's closing and leave them there.

## Gotchas

- **An import line resolves relative to the file that holds it.** Where the repository uses pointer files, a nested document created by a scoping move needs its own sibling pointer, holding that relative line and nothing else. Never write a rooted path. Where the repository does not use pointer files, a scoping move creates the nested document alone — inventing a pointer imposes a convention the repository never adopted.
- **A nested document does not replace the root one** — both apply, so a nested document is judged against the root rules it inherits rather than on its own.
- **A stale document marked active is worse than a missing one**, because an agent will act on it. Status drift outranks most prose problems even though it looks like housekeeping.
- **Drift marks the moment a document stopped tracking the code.** Look for what changed at that moment. Finding the change explains the divergence; it does not settle which side is now correct, and the document is as likely to be a rule the code broke as a description the code outgrew.
