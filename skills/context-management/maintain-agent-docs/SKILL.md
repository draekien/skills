---
name: maintain-agent-docs
description: Audits a repository's existing agent docs and reports what would mislead an agent — guidance gone stale against the code, or placed where the wrong agents read it. Repairs findings with --fix.
argument-hint: "[--effort low|mid|high|xhigh|max] [--scope drift|shape] [--target path] [--fix safe|unsafe] [--interview one|batch]"
disable-model-invocation: true
---

# Maintain agent docs

Agent docs fail two ways, and the two need separating all the way through to the report because they resolve differently.

**Drift** — the document is no longer true. An agent that reads it and acts does the wrong thing.

**Shape** — every line is true, but the document is built so an agent reads the wrong thing first: guidance for one directory sitting in the always-loaded root file, this quarter's migration written as a permanent rule, a convention stated as prose that a linter would enforce for free.

The bar for both is **the contract** — the conventions this repository committed to, recorded in its own convention docs. Not the conventions a well-run repository usually has. That distinction carries the whole skill; see [Anti-patterns](#anti-patterns).

This audit needs a user. Interview findings resolve only by asking, so a run with nobody to answer reports them unresolved and writes nothing for them — no mode presumes an answer, and no flag makes this an unattended tool. Where the invocation is automated, say so in the report and treat every interview finding as open.

## Establish the contract

First identify **the root document** — the file at the repository root that an agent actually reads for standing guidance. It may be `AGENTS.md`, `CLAUDE.md`, or an equivalent another tool reads. What decides is content, not filename: a file holding nothing but an import line is a pointer, and the file it points at is the root document.

- **One file holds the guidance** — that file is the root document, whichever name it carries. Audit it in place. Do not propose renaming it or migrating to a different convention; a repository that keeps its guidance in `CLAUDE.md` has made a choice, and reshaping the doc set to a preferred layout is scaffolding, not maintenance.
- **One holds guidance, another imports it** — the imported file is the root document, and the import-only file is checked against the import discipline.
- **Two or more hold guidance independently** — every one is a root document. Audit against all of them and say in the report that the guidance is split; never pick one and proceed, because the rules in the file not chosen then go unread with nothing recording it. Where they disagree, the disagreement is a cross-document finding and the user says which should own the guidance. Where they agree, report the duplication as a divergence risk and leave the arrangement alone: a repository hand-syncing two root files has an unusual convention, not a contradiction.
- **A root file exists but holds nothing** — an empty file, or one whose content carries no guidance, is itself a finding. Every session loads it and learns nothing, and its emptiness reads as an audited pass unless the report names it. Report it and continue with whatever else holds guidance.
- **None exist** — stop. Report that there is nothing to maintain and point at `init-agent-docs` — and if the user does not have it, at how to install it: `/plugin install context-management-skills@draekien-skills` in a harness with plugin support, or `npx skills add draekien/skills --skill "init-agent-docs"` anywhere else. This skill corrects existing docs; it never scaffolds. This is a normal outcome, not a failure of the run.

Then find and read the repository's own convention docs, before forming any finding. They define the frontmatter form, the status discipline, the ADR bar, and the directory purposes this audit measures against — including where this repository deliberately diverged from convention. Locate them by searching the doc set for the documents that govern the doc set, not by expecting a fixed path: a repository that keeps them one directory name from convention still has a contract, and treating it as contractless discards the very rules the audit measures against.

Where a root document exists but the convention docs do not, audit against what the docs claim about themselves and about the code, and state in the report that the contract was unavailable, so the user can see the findings rest on a narrower basis. With no contract, structural-invariant checks reduce to internal consistency and link integrity: raise no finding about frontmatter form or status vocabulary, and apply nothing mechanically. General convention is not a substitute for the contract.

## Scope the pass

`--target` bounds the doc set: a directory, or a single document. Absent, the doc set is every agent-facing document — the root document, every nested `AGENTS.md` or `CLAUDE.md`, the import-only files that point at them, and everything under `docs/`. A nested document is resolved the same way as the root one: content decides which file governs that subtree.

The root document and the convention docs are read whatever `--target` says, because a nested document cannot be judged without the rules it inherits. The bound governs which documents can carry a finding, not which are read.

Where `--target` selects no documents, report that: name the target and the documents that exist outside it. Never widen the scope unasked — a silent widening produces findings about documents the user excluded on purpose.

The doc set stops at what this repository owns. A submodule, a vendored tree, or an installed dependency carries its own agent docs governed by someone else's contract: exclude them. Editing them writes into a tree the parent repository does not track, so the change is invisible to review and disappears on the next update, and the same finding returns on every run.

Read each document in scope in full, and open code only to verify a specific claim a document makes. Agent docs are usually few and short, which is what keeps cost proportional to the doc set rather than the repository — but that is an observation, not a guarantee. Where the doc set is too large to read in full, or a single document is, say so and ask for a narrower `--target` rather than proceeding on a premise the pass has already broken. A document reported as unaudited is honest; a document skimmed and reported as checked is not.

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
- **A finding belonging to no listed class resolves as interview**, never as mechanical. A class the routing table names but the resolution table does not is an unfinished class, and inheriting the resolution of whichever row sits nearest is how a finding meant to be a question becomes an unattended write.

## Resolve by class

Each class resolves one of four ways. The class decides, not the finding's severity.

| Resolution | Classes | Behaviour |
| --- | --- | --- |
| **Mechanical** | Structural invariants, transient state | One correct answer exists. Apply it. |
| **Approval** | Scoping and progressive disclosure | Propose the move: the lines, the destination, and the evidence for that scope. Apply only what the user accepts. |
| **Interview** | Claim verification, cross-document contradictions, history rot | The audit knows two things disagree, not which is the mistake. Ask. |
| **Recommendation** | Guardrail candidates | Name the mechanism and what the prose becomes. Never build it. |

An interview finding is never resolved by presuming the code is right. A document line can be a real rule the code violates — that is a code defect, and rewriting the document to match deletes the rule that exposes it. Surface both sides with the evidence for each and let the user say which is true.

`--interview` sets how those questions arrive. Absent, the mode is `one`.

- **`one`** — one finding at a time, each answer informing what to ask next. The right default: a user deciding whether a rule or the code is wrong needs room to think about that pair alone.
- **`batch`** — findings sharing a root cause are grouped and answered together. Worth reaching for on a wide doc set, where the same underlying divergence surfaces across a dozen documents and answering it a dozen times teaches nobody anything.

Batching groups by root cause, never by document or by count. Each finding in a group still carries its own two sides and its own evidence, and a finding that shares no root cause with another is asked alone whatever the mode — a group assembled to shorten the queue asks the user to answer a question nobody posed.

## Write only when asked

| Invocation | Applies |
| --- | --- |
| no `--fix` | Nothing during the pass. Every finding goes to the disposition, and what the user accepts there is written. |
| `--fix`, `--fix safe` | Mechanical classes, during the pass. Approval and recommendation classes still go to the disposition. |
| `--fix unsafe` | Mechanical classes, plus approval-class moves without asking. Guardrail findings are filed as plans. |

Interview findings are asked in every mode, `--fix unsafe` included. An interview answer authorises the write for that finding alone — and authorises nothing at all for a finding marked probable. A probable finding is asked so the user learns what the pass suspects, not so an answer can convert a guess into an edit; the answer is recorded in the report and the document is left alone.

`--fix unsafe` does not apply a move whose blast radius rests on judgement rather than on paths verified in the code. Report those as proposals instead: a rule moved too far down goes quiet rather than visibly wrong, so it is the one approval-class finding an unattended run must not guess at.

Repairs follow the audited repository's own status discipline, so nothing is deleted: a shipped plan is marked done, a replaced decision is superseded, a document that has outlived its purpose is reported rather than removed.

## Report

**Open the report with what this run covered**: the classes that ran, the classes that did not, and the documents in scope. A reader forms a verdict from the first thing they see, so coverage stated only at the end arrives after they have already read few findings as a healthy doc set. Say plainly that a narrow pass is not a clean one — the most expensive failure this skill can produce is a partial audit mistaken for a clean bill of health.

Rank findings by one test: **would an agent reading this document today do the wrong thing?** A rule that contradicts working code outranks a stale date. Keep drift and shape in separate sections — a reader deciding what to accept needs to know whether a document is wrong or merely badly placed.

For each finding: the document and lines, the class, the evidence, and the resolution taken or proposed. Findings already applied under `--fix` are listed as done, not as pending.

Report each class as it finishes rather than holding everything to the end. A pass can run out of room or be interrupted, and findings established but never stated are worth nothing — a run that ends early must still have said what it found. Where a pass cannot complete, name the classes that finished, the classes that did not, and anything already written.

Close with what was left and why — interview findings the user deferred, guardrail recommendations not taken, and the classes this run did not cover, naming whether each was out of level or out of scope.

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
