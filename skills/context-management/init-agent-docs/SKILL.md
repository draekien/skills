---
name: init-agent-docs
description: Sets up a repository's agent documentation — AGENTS.md and CLAUDE.md at the root and under docs/, plus adr, references, explorations, and plans directories with the conventions agents need to use them. Use on a repo with no agent docs, or one whose docs have drifted.
disable-model-invocation: true
---

# Init agent docs

Produce documentation a future agent can act on. Two things make it worthless: placeholders, which look authoritative and say nothing, and **restated discoverables** — stack, commands, and directory layout that any agent finds in thirty seconds by reading the package manifest and listing the tree. Restated discoverables cost context on every turn, and they rot the moment the repo moves. `AGENTS.md` carries only what exploration cannot reach: intent, enforced convention, external constraint, and the specific traps of this repo.

## Phase 1 — Survey

Read the repository before writing a word about it — not to transcribe it, but to know what to leave out and what to ask.

- **Discoverables** — stack, package manifests, task-runner scripts, CI workflows, directory layout. Learn them so you can recognise and exclude them, and so your questions are informed.
- **Contradictions** — where a documented rule and the actual code disagree. Each one is an interview question: which is true?
- **Existing prose** — README, CONTRIBUTING, any current `AGENTS.md`, `CLAUDE.md`, or `docs/`. Note what is authoritative and what has rotted.
- **Collisions** — every *file* this skill would create that already exists. Note existing directories separately; they are not collisions.

Done when you can describe the repo's shape and build surface in one paragraph without writing any of it into a document, and can list every contradiction and every colliding file.

## Phase 2 — Interview

Ask only what the repository cannot tell you, and keep asking until nothing is left open. Surface one question at a time, highest impact first, using each answer to shape the next. Do not stop after the first answer, and do not settle for the questions listed below if the survey raised others.

Worth asking in an established repo:

- What is this project for, who uses it, and what does it deliberately not do?
- What do agents repeatedly get wrong here?
- Which conventions are enforced rather than merely common — and which would a competent engineer guess wrong?
- Constraints invisible in the code: compliance limits, performance contracts, deployment targets that cannot change.
- For each contradiction found in Phase 1: which side is true?
- For each rotted doc found in Phase 1: rewrite it, fold what is still true into `AGENTS.md`, or leave it untouched?

**An empty or near-empty repository has nothing to discover, so the interview carries the whole document.** Interview the user about the project itself: what it is meant to achieve and for whom, what it will deliberately not do, the constraints already known, and the conventions they intend to enforce. Record only what the user actually decides — an intention stated as fact becomes a lie the moment the code disagrees. Where they have not decided yet, leave it out and say so in Phase 5. Stack and layout still stay out of the document even here: the moment code exists, they become discoverable, and a written copy only drifts from it.

Not worth asking: anything Phase 1 already discovered, and general software advice the agent applies by default. A convention the agent would follow anyway earns no line in `AGENTS.md`.

If the user asks to proceed before every question is resolved, list the remaining ones, state the assumptions you will write under, and continue.

## Phase 3 — Scaffold

Create this structure. Never overwrite.

```text
AGENTS.md
CLAUDE.md
docs/
  AGENTS.md
  CLAUDE.md
  adr/
    AGENTS.md
  references/
  explorations/
  plans/
```

Templates, and how each is used:

| Target | Template | Treatment |
| --- | --- | --- |
| `AGENTS.md` | [assets/agents-md-root.md](assets/agents-md-root.md) | Fill from Phase 2 answers only |
| `CLAUDE.md`, `docs/CLAUDE.md` | [assets/import-agents-md.md](assets/import-agents-md.md) | Copy verbatim to both locations |
| `docs/AGENTS.md` | [assets/agents-md-docs.md](assets/agents-md-docs.md) | Copy verbatim; change only paths that differ in this repo |
| `docs/adr/AGENTS.md` | [assets/agents-md-adr.md](assets/agents-md-adr.md) | Copy verbatim; change only paths that differ in this repo |

Each copied template carries the format for the documents in its directory, so the repo needs no separate template files.

`CLAUDE.md` holds the import line and nothing else — `AGENTS.md` is the single source of truth, and duplicated guidance drifts apart within weeks.

Braced text in `agents-md-root.md` is instruction to you, not content — some braces mark a slot to fill, others tell you what to include or drop. No `{` survives into the written file.

For `AGENTS.md`, cut every section the interview did not fill; an empty heading invites a future agent to invent content for it. **Documentation** is the exception: it is a convention, not a finding, and always stays. Before writing the file, check each remaining line against the discoverable test — if an agent could learn it by reading the package manifest, listing the tree, or opening two source files, delete it.

Git ignores empty directories, so give `docs/references`, `docs/explorations`, and `docs/plans` a `.gitkeep` unless they already hold files.

For each colliding file, do not touch it. Show the user the exact additions you propose — as a diff against the current file — and apply only what they approve.

## Phase 4 — Seed ADRs

The survey often surfaces decisions already made and nowhere recorded. Offer to capture them, applying the bar in [assets/agents-md-adr.md](assets/agents-md-adr.md) without softening it: all three of hard to reverse, surprising without context, and the result of a real trade-off.

Offer a short list and let the user choose, then write each chosen record from the `## Template` section of that same file, without its code fence. Do not write an ADR they did not pick, and do not invent the rationale — if the user cannot say why the alternative was rejected, there is no ADR to write. Zero seeded ADRs is a correct outcome.

## Phase 5 — Report

Close with a table of every path: created, amended (additions the user approved), skipped (already present, left untouched), or proposed-and-declined. Then name what remains unknown — contradictions left unresolved, conventions the user deferred on — so the gaps are visible rather than silently absent from the docs.

## Gotchas

- **`@AGENTS.md` resolves relative to the importing file**, so `docs/CLAUDE.md` imports `docs/AGENTS.md` with that exact line. Do not write a rooted path.
- **A nested `AGENTS.md` does not replace the root one**; both apply. Keep `docs/AGENTS.md` scoped to working with documentation and never restate root conventions in it.
- **A command table in `AGENTS.md` is the most common form of restated discoverable, and the fastest to rot.** If a command genuinely cannot be found — an undocumented flag, a step with no script behind it — that is a gotcha, not a reference table.
- **Existing agent docs are usually stale, not wrong.** Treat them as interview material rather than as a source to copy forward.
