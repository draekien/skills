---
name: maintain-agent-docs
description: Audits a repository's existing agent docs and reports what would mislead an agent or waste its context — guidance gone stale against the code, placed where the wrong agents read it, or padded past what it needs to teach. Repairs findings with --fix.
argument-hint: "[--effort low|mid|high|xhigh|max] [--scope drift|shape|distill] [--target path] [--fix safe|unsafe] [--interview one|batch]"
disable-model-invocation: true
---

# Maintain agent docs

Agent docs fail three ways, and the three need separating all the way through to the report because they resolve differently.

**Drift** — the document is no longer true. An agent that reads it and acts does the wrong thing.

**Shape** — every line is true, but the document is built so an agent reads the wrong thing first: guidance for one directory sitting in the always-loaded root file, this quarter's migration written as a permanent rule, a convention stated as prose that a linter would enforce for free.

**Distill** — every line is true and correctly placed, and the document still costs more than it teaches: a line the package manifest already states, a rule wrapped in two sentences of preamble, a behaviour written as an image the agent must translate before it can act. Context spent here is spent on every turn, on every task, including the ones the line has nothing to do with. Most of that cost is tokens; the figurative-language class is the exception, where the cost is the interpretation the line forces and the two readings it allows.

The bar for all three is **the contract** — the conventions this repository committed to, recorded in its own convention docs. Not the conventions a well-run repository usually has. That distinction carries the whole skill; see [Anti-patterns](#anti-patterns).

This audit needs a user. Interview findings resolve only by asking, so a run with nobody to answer reports them unresolved and writes nothing for them — no mode presumes an answer, and no flag makes this an unattended tool. Where the invocation is automated, say so in the report and treat every interview finding as open.

## Establish the contract

First identify **the root document** — the file at the repository root that an agent actually reads for standing guidance. It may be `AGENTS.md`, `CLAUDE.md`, or an equivalent another tool reads. What decides is content, not filename: a file holding nothing but an import line is a pointer, and the file it points at is the root document.

- **One file holds the guidance** — that file is the root document, whichever name it carries. Audit it in place. Do not propose renaming it or migrating to a different convention; a repository that keeps its guidance in `CLAUDE.md` has made a choice, and reshaping the doc set to a preferred layout is scaffolding, not maintenance.
- **One holds guidance, another imports it** — the imported file is the root document, and the import-only file is checked against the import discipline.
- **Two or more hold guidance independently** — every one is a root document. Audit against all of them and say in the report that the guidance is split; never pick one and proceed, because the rules in the file not chosen then go unread with nothing recording it. Where they disagree, the disagreement is a cross-document finding and the user says which should own the guidance. Where they agree, report the duplication as a divergence risk and leave the arrangement alone: a repository hand-syncing two root files has an unusual convention, not a contradiction.
- **A root file exists but holds nothing** — an empty file, or one whose content carries no guidance, is itself a finding. Every session loads it and learns nothing, and its emptiness reads as an audited pass unless the report names it. Report it and continue with whatever else holds guidance.
- **None exist** — stop. Report that there is nothing to maintain and point at `init-agent-docs` — and if the user does not have it, at how to install it: `/plugin install context-management-skills@draekien-skills` in a harness with plugin support, or `npx skills add draekien/skills --skill "init-agent-docs"` anywhere else. This skill corrects an existing doc set; it never creates one. This is a normal outcome, not a failure of the run.

Then find and read the repository's own convention docs, before forming any finding. They define the frontmatter form, the status discipline, the ADR bar, and the directory purposes this audit measures against — including where this repository deliberately diverged from convention. Locate them by searching the doc set for the documents that govern the doc set, not by expecting a fixed path: a repository that keeps them one directory name from convention still has a contract, and treating it as contractless discards the very rules the audit measures against.

Where a root document exists but the convention docs do not, audit against what the docs claim about themselves and about the code, and state in the report that the contract was unavailable, so the user can see the findings rest on a narrower basis. With no contract, structural-invariant checks reduce to internal consistency and link integrity: raise no finding about frontmatter form or status vocabulary, and apply no invariant mechanically. General convention is not a substitute for the contract.

The distill classes survive a missing contract, because their evidence sits outside the doc set: a line restating the package manifest is waste whether or not the repository ever wrote down that it should be. Where the contract records no convention about how agent docs are written, that absence is itself the axis's first finding.

## Scope the pass

`--target` bounds the doc set: a directory, or a single document. Absent, the doc set is every agent-facing document — the root document, every nested `AGENTS.md` or `CLAUDE.md`, the import-only files that point at them, and everything under `docs/`. A nested document is resolved the same way as the root one: content decides which file governs that subtree.

The root document and the convention docs are read whatever `--target` says, because a nested document cannot be judged without the rules it inherits. The bound governs which documents can carry a finding, not which are read.

Where `--target` selects no documents, report that: name the target and the documents that exist outside it. Never widen the scope unasked — a silent widening produces findings about documents the user excluded on purpose.

The doc set stops at what this repository owns. A submodule, a vendored tree, or an installed dependency carries its own agent docs governed by someone else's contract: exclude them. Editing them writes into a tree the parent repository does not track, so the change is invisible to review and disappears on the next update, and the same finding returns on every run.

Measure the doc set before reading it: `uv run scripts/estimate-tokens.py <paths>` — the script path relative to this skill's directory, the arguments relative to the audited repository — reports each document's cost and the total, using any runner that supports PEP 723 inline dependencies. The numbers set read order for the distill axis and give the report its before-and-after. They never make a finding on their own — a document is not too long, and a long document of lines that all earn their tokens is correct.

Read each document in scope in full, and open code only to verify a specific claim a document makes. Agent docs are usually few and short, which is what keeps cost proportional to the doc set rather than the repository — but that is an observation, not a guarantee. Where the doc set is too large to read in full, or a single document is, say so and ask for a narrower `--target` rather than proceeding on a premise the pass has already broken. A document reported as unaudited is honest; a document skimmed and reported as checked is not.

## Route by effort

`--effort` selects which finding classes are in play. Levels are cumulative — each includes every class below it. Absent, the level is `mid`.

`--scope` restricts the pass to one axis — `drift`, `shape`, or `distill`. Absent, all three run. The two flags compose: a class is active only when its level is reached and its axis is in scope, so `--effort xhigh --scope shape` runs transient state, scoping, and guardrails, and no drift or distill class at all.

Read a class's reference before hunting for that class, and read no others. A scoped-out axis loads none of its references.

| Level | Adds | Reference |
| --- | --- | --- |
| `low` | Structural invariants | [references/drift-invariants.md](references/drift-invariants.md) |
| | Transient state | [references/shape-transient.md](references/shape-transient.md) |
| | Restated discoverables | [references/distill-discoverables.md](references/distill-discoverables.md) |
| | Figurative language | [references/distill-literal.md](references/distill-literal.md) |
| `mid` | Claim verification | [references/drift-claims.md](references/drift-claims.md) |
| `high` | Cross-document contradictions | [references/drift-cross-doc.md](references/drift-cross-doc.md) |
| | Scoping and progressive disclosure | [references/shape-scoping.md](references/shape-scoping.md) |
| | Prose density | [references/distill-density.md](references/distill-density.md) |
| `xhigh` | History rot and unrecorded decisions | [references/drift-history.md](references/drift-history.md) |
| | Guardrail candidates | [references/shape-guardrails.md](references/shape-guardrails.md) |
| `max` | No new classes. The confidence bar drops, so findings that are probable rather than proven surface, alongside claims that resist falsification — each marked as such | |

Three rules hold across the routing:

- **A probable finding is never applied**, in any `--fix` mode. Marking it probable and then writing it anyway defeats the mark.
- **A class that hands a finding to a class this run has not activated still reports it**, as an unresolved finding of the receiving class, named as out of level or out of scope. Never resolve it under the sending class's resolution — that is how a line gets deleted mechanically on the strength of a check the pass never ran.
- **A finding belonging to no listed class resolves as interview**, never as mechanical. A class the routing table names but the resolution table does not is an unfinished class, and inheriting the resolution of whichever row sits nearest is how a finding meant to be a question becomes an unattended write.

## Resolve by class

Each class resolves one of four ways. The class decides, not the finding's severity.

| Resolution | Classes | Behaviour |
| --- | --- | --- |
| **Mechanical** | Structural invariants, transient state, restated discoverables, figurative language, prose density | Apply it. One correct answer exists for the first two; the distill classes hold their licence differently, below. |
| **Approval** | Scoping and progressive disclosure, the missing writing convention | Propose it in full — for a move, the lines, the destination, and the evidence for that scope; for the convention, the exact text. Apply only what the user accepts. |
| **Interview** | Claim verification, cross-document contradictions, history rot | The audit knows two things disagree, not which is the mistake. Ask. |
| **Recommendation** | Guardrail candidates | Name the mechanism and what the prose becomes. Never build it. |

The distill classes resolve mechanically on a different licence from the other two. No single correct rewrite of a padded rule exists, so what makes the edit safe unattended is not certainty but reversibility: no writing pass runs without a clean tree, which leaves the whole pass as one reviewable diff that `git checkout -- .` undoes. That licence buys nothing without the evidence bar in [Anti-patterns](#anti-patterns) — reversible is not the same as harmless, and a rewrite that quietly drops an exception reads clean in the diff.

An interview finding is never resolved by presuming the code is right. A document line can be a real rule the code violates — that is a code defect, and rewriting the document to match deletes the rule that exposes it. Surface both sides with the evidence for each and let the user say which is true.

`--interview` sets how those questions arrive. Absent, the mode is `one`.

- **`one`** — one finding at a time, each answer informing what to ask next. The right default: a user deciding whether a rule or the code is wrong needs room to think about that pair alone.
- **`batch`** — findings sharing a root cause are grouped and answered together. Worth reaching for on a wide doc set, where the same underlying divergence surfaces across a dozen documents and answering it a dozen times teaches nobody anything.

Batching groups by root cause, never by document or by count. Each finding in a group still carries its own two sides and its own evidence, and a finding that shares no root cause with another is asked alone whatever the mode — a group assembled to shorten the queue asks the user to answer a question nobody posed.

## Write only when asked

**A writing pass requires a clean tree.** Check before the first edit whenever the run could write — any `--fix`, and the disposition's action-now route. Where the tree is dirty, or the repository is not under version control, run read-only and say so at the top of the report, naming the paths that blocked it: these edits are only cheap to undo while the diff holds nothing but them, and that is the whole basis on which the distill classes are allowed to write unattended.

Leave the edits uncommitted. The gate has already made the working tree a clean review surface, and the commit message is the user's to write.

| Invocation | Applies |
| --- | --- |
| no `--fix` | Nothing during the pass. Every finding goes to the disposition, and what the user accepts there is written. |
| `--fix`, `--fix safe` | Mechanical classes, during the pass. Approval and recommendation classes still go to the disposition. |
| `--fix unsafe` | Mechanical classes, plus approval-class findings without asking — moves, reorderings, and the writing convention. Guardrail findings are filed as plans. |

Interview findings are asked in every mode, `--fix unsafe` included. An interview answer authorises the write for that finding alone — and authorises nothing at all for a finding marked probable. A probable finding is asked so the user learns what the pass suspects, not so an answer can convert a guess into an edit; the answer is recorded in the report and the document is left alone.

`--fix unsafe` does not apply a move whose blast radius rests on judgement rather than on paths verified in the code. Report those as proposals instead: a rule moved too far down goes quiet rather than visibly wrong, so it is the one approval-class finding an unattended run must not guess at.

Repairs follow the audited repository's own status discipline, so no document is deleted: a shipped plan is marked done, a replaced decision is superseded, a document that has outlived its purpose is reported rather than removed. Lines within a document are a different matter — the distill classes delete them, and that is the axis's whole point.

## Report

**Open the report with what this run covered**: the classes that ran, the classes that did not, and the documents in scope. A reader forms a verdict from the first thing they see, so coverage stated only at the end arrives after they have already read few findings as a healthy doc set. Say plainly that a narrow pass is not a clean one — the most expensive failure this skill can produce is a partial audit mistaken for a clean bill of health.

Rank findings by one test: **would an agent reading this document today do the wrong thing?** A rule that contradicts working code outranks a stale date, which outranks a line that is merely expensive. Give each axis its own section — a reader deciding what to accept needs to know whether a document is wrong, badly placed, or just costly.

For each finding: the document and lines, the class, the evidence, and the resolution taken or proposed. Findings already applied under `--fix` are listed as done, not as pending.

Where a distill class ran, quote the doc set's cost before and after, per document and in total. The saving is that axis's whole justification, so a distill report without it asks the user to accept a rewrite on the audit's word. Figurative-language findings are excluded from that arithmetic and reported without a token figure — their saving is usually zero, and quoting it invites the user to reject a correct finding on the wrong measure.

Report each class as it finishes rather than holding everything to the end. A pass can run out of room or be interrupted, and findings established but never stated are worth nothing — a run that ends early must still have said what it found. Where a pass cannot complete, name the classes that finished, the classes that did not, and anything already written.

Close with what was left and why — interview findings the user deferred, guardrail recommendations not taken, and the classes this run did not cover, naming whether each was out of level or out of scope.

## Disposition

Where findings remain open, offer three routes. They compose, and where the user files or actions, they choose which findings go that way rather than accepting all of them.

- **Save the report** — a dated document under the repository's explorations directory, since an audit is evidence gathered. Accept any path the user names instead, inside or outside the repository. Where no explorations directory exists, ask for a path rather than creating one.
- **File plans** — one dated plan per accepted finding group, in the format the repository's own documentation conventions define.
- **Action now** — apply the accepted findings in this session. Accepting a finding here is the authorisation `--fix` would have carried, so this route writes even on a run invoked without it.

## Anti-patterns

**Auditing against the agent's own taste.** This one is dangerous because the output looks like good work: a convention gets flagged because a different repository would do it differently, and the user accepts a rewrite that erases a deliberate local decision. A rule the audit would not have chosen is still the rule. The only grounds for a finding are that a document contradicts the code, contradicts another document, has rotted, is shaped so an agent reads the wrong thing first, or spends tokens on nothing — never that a convention is unusual.

The distill axis rewrites prose, so it stands closest to that line and carries the bar that keeps it clear: **every distill finding names the specific waste it removes** — the artifact the line restates, the document it duplicates, the padding wrapped around the rule, the device standing in for a statement of behaviour — and **no distill finding changes what a line requires**. Wording the audit would have chosen differently is not waste, and a shorter rule that demands something narrower is not a distillation.

**Splitting by size.** Length is not the trigger for a split; blast radius is. A long document of genuinely repository-wide rules stays whole, and a short one holding directory-specific rules gets scoped.

**Auditing the code.** Verifying a claim surfaces real defects in passing. They are not findings of this pass — mention them once in the report's closing and leave them there.

## Gotchas

- **An import line resolves relative to the file that holds it.** Where the repository uses pointer files, a nested document created by a scoping move needs its own sibling pointer, holding that relative line and nothing else. Never write a rooted path. Where the repository does not use pointer files, a scoping move creates the nested document alone — inventing a pointer imposes a convention the repository never adopted.
- **A nested document does not replace the root one** — both apply, so a nested document is judged against the root rules it inherits rather than on its own.
- **A stale document marked active is worse than a missing one**, because an agent will act on it. Status drift outranks most prose problems even though it looks like housekeeping.
- **Drift marks the moment a document stopped tracking the code.** Look for what changed at that moment. Finding the change explains the divergence; it does not settle which side is now correct, and the document is as likely to be a rule the code broke as a description the code outgrew.
