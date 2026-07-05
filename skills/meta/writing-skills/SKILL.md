---
name: writing-skills
description: Knowledge for writing agent skills — the tenets, design axes, and craft of a SKILL.md, plus a spec validator. Reach for it before creating a new skill or revising an existing one.
argument-hint: "[skill-name-or-path]"
disable-model-invocation: true
---

A skill is a teaching document for a future agent: it transfers intent and judgment so that agent can achieve a goal without the author present. A skill exists to wrangle determinism out of a stochastic system — **predictability**, the agent taking the same *process* every run (not producing the same output; a brainstorming skill predictably diverges), is the root virtue. Every tenet, axis, and craft rule below is a lever on it.

Everything here governs the whole skill, not just its body: a reference is body content deferred, not a different kind of document, and `assets/` prose and script docs are held to the same bar.

## Tenets

When a writing decision is not covered elsewhere in this document, resolve it against the tenets directly.

A skill MUST:

- **Teach the class of problems** — how to approach the class, never what to produce for a specific instance.
- **Be grounded in real expertise** — extracted from hands-on task execution or synthesized from real project artefacts (runbooks, schemas, review comments, failure cases). A skill generated from generic training knowledge yields vague procedures ("handle errors appropriately") and adds no delta.
- **Target the agent, not the user** — if the information is not necessary for the agent to perform its task, cut it.
- **Carry activation entirely in the description** — the body is never read until after activation, so the description is the sole activation signal. Never write a "when to use this skill" section in the body.
- **Encode timeless principles** — moderated by the Knowledge ↔ Procedure axis: principles are the default payload and a procedure skill may encode steps instead, but even steps must stay free of state-of-the-world.
- **Never encode the current state of the world** — corpus contents, file counts, "all existing X do Y". Such facts rot as the skill is used, most sharply when the skill exists to change that very state. Where current state is required, instruct the agent to explore.

A skill SHOULD:

- **Carry the why, not just the what** — an agent that understands the goal adapts when exact steps don't fit; an agent with only commands cannot.
- **Omit what the agent already knows** — the highest-value content is the delta from the agent's defaults: what it would not do on its own, most sharply an instruction that countermands a strong reflex. Aim for moderate detail; most edge cases are better handled by the agent's own judgment than enumerated.
- **Cover a coherent unit of work** — scoped like a well-designed function: too narrow forces many skills to load for one task; too broad cannot activate precisely.
- **Name tools at the right specificity** — for the agent's harness capabilities, describe the capability ("search the web", "read local files"), never name a harness tool: toolsets vary and belong to the current state of the world. For domain tools a task requires (a library, a runner, a CLI), provide a default, not a menu: name one and mention the escape hatch briefly. A skill's own bundled scripts are exempt — invoking them prescriptively is what they exist for.
- **Be refined against real execution** — run the draft on real tasks and read the agent's traces, not just final outputs. Wasted steps expose vague instructions, inapplicable instructions, or a missing default; a correction the user had to make becomes a gotcha. Behavioural disputes (is this line a no-op? did the leading word take hold?) are settled by running the skill, not by debate.

## Axes

Position the skill on each axis before writing — each end pulls the writing in a different direction.

### Knowledge ↔ Procedure

**Knowledge** is context that guides the agent into acting a specific way — principles, standards, domain understanding; the payload is the information. **Procedure** is a specific set of steps to execute a workflow or task; the payload is the behaviour. Most skills carry some of both — name where the skill sits, because each end stresses different craft: knowledge skills live or die on the delta from the agent's defaults; procedure skills live or die on freedom calibration and completion criteria.

### Stateful ↔ Stateless

A skill is **stateless** by default — each run starts fresh and derives what it needs from the session. **Stateful** covers both resumability within a task (knowing where it is up to mid-execution) and persistence across sessions (config, working artefacts the skill builds up). The key judgement in both cases: if the information is cheap to re-derive, it is not state — persisting it creates a second source of truth that drifts.

### Prescriptive ↔ Flexible

A sub-axis of the Procedure end — knowledge skills are inherently flexible. Calibrate each part of a skill independently by terrain: a narrow bridge with cliffs demands prescription; an open field demands freedom.

- **Prescriptive** — operations are fragile, consistency matters, or a specific sequence must be followed: exact commands, few or no parameters, "do not modify or add flags".
- **Flexible** — multiple approaches are valid: reasoning-carrying prose that explains what good looks like and why, letting the agent determine the path. Flexible prose leans hardest on the carry-the-why tenet:

  > Weak: "Run the status command to see uncommitted changes."
  >
  > Strong: "Understand the working tree state before deciding what to stage — distinguish intentional changes, generated artefacts, and files that might be sensitive."

### Model-triggered ↔ User-triggered

Two ways a skill is reached, trading different costs:

- **Model-triggered** — the skill surfaces by relevance when the agent matches the description against the task. Knowledge skills lean this way: the agent should benefit without being told. Pays **context load** — the description sits in the agent's window every turn.
- **User-triggered** — the human turns the skill on deliberately. Procedure skills lean this way: a process should not auto-fire onto unrelated tasks. Pays **cognitive load** — the human is the index that must remember the skill exists. Not a cost to minimise: it is the price of human agency; spend it where human judgement matters. When user-triggered skills multiply past memory, a **router skill** — one user-triggered skill naming the others and when to reach for each — cures the pile-up.

Where a harness supports invocation controls in frontmatter, set them to match; they are extensions, not part of the open standard.

## The description

The mechanics of the sole-activation-signal tenet. Which form to write follows from the Model-triggered ↔ User-triggered axis:

- **Model-triggered** — an API contract the agent matches against a request: imperative, dense with domain keywords and trigger phrases embedded verbatim.

  ```text
  <verb> <what it does>. Use when <conditions>, or when the user says "<phrase 1>", "<phrase 2>".
  ```

- **User-triggered** — a menu line for a human scanning a command list: say what it produces and when someone would reach for it, the way a CLI help one-liner does. Trigger-phrase density makes a poor menu label.

If both invocation paths are open, write the model-triggered form — it still reads fine to a human.

Every description word pays context load, so prune it harder than the body: **front-load the leading word** (the description is where it does its invocation work), keep **one trigger per branch** (synonym triggers restating a single branch are duplication), and **cut identity the body already carries**.

## The argument hint

A quoted, free-text usage cue in frontmatter — the only place that signals which capabilities a skill exposes and what to supply. A progressive enhancement: harnesses that don't recognise the field ignore it, so it costs nothing to include.

- **Single input** — `"[issue-number]"` or `"[filename] [format]"`.
- **Fixed modes** — name them pipe-separated, even for two: `"[write|audit] [target]"`, not a descriptive phrase.
- **Always quote** — an unquoted `[issue-number]` parses as a YAML list, not the string every harness expects.

Don't push it toward a structured, typed argument schema — that isn't broadly supported or worth designing around.

## Content placement

Rank content by how immediately the agent needs it, and place it accordingly:

| Level         | Location        | What belongs here                                                                       |
| ------------- | --------------- | ---------------------------------------------------------------------------------------- |
| Always loaded | `SKILL.md` body | Steps and judgment every activation needs — the primary tier                             |
| On demand     | `references/`   | Material only some branches need — schemas, lookup tables, deep documentation            |
| Template      | `assets/`       | Outputs the agent copies rather than invents; static config; example files               |
| Executable    | `scripts/`      | Deterministic operations where variation is a bug — bundle one when execution traces show the agent reinventing the same logic each run |

**Branching is the cleanest placement test**: each distinct way the skill gets used is a branch — inline what every branch needs, defer what only some branches reach. Push too little down and the body bloats, burying the steps; push too much down and material the agent actually needs hides behind a pointer. Keep the body under 500 lines; link supporting files with relative paths, one level deep only — never reference a reference.

**A context pointer's wording, not its target, decides when the agent loads deferred material** — and how reliably. "Read `references/api-errors.md` if the API returns a non-200 status" beats "see references/ for details". A weak pointer on must-have material is a variance bug: sharpen the wording first; inline the material only if sharpening fails.

**Co-locate what is read together**: a concept's definition, rules, and caveats under one heading, not scattered across the file. The test is that the skill reads like documentation written for the agent — grouped material reads that way, scattered material does not.

When bundling scripts, apply [references/script-design.md](references/script-design.md).

## Craft

- **Leading words** — compress an instruction into a domain term the agent's training already has strong priors about ("build a **vertical slice** first"), then reuse that exact term — as a token, never re-explained as a sentence — everywhere the skill touches the idea. A pretrained word recruits priors for free; a coined word pays in definition tokens what a pretrained word gives free. Grade a leading word with the no-op test: "be thorough" too weak to beat the default means a stronger word ("relentless"), not a different technique.
- **Completion criteria** — end each unit of work on the condition that tells the agent it is done. Make it *checkable* (the agent can tell done from not-done) and *demanding* ("every modified model accounted for", not "produce a change list"). Demand drives legwork — the digging the agent does within the work — and binds flat reference just as it binds steps: "every rule applied" is a completion criterion too.
- **Prune relentlessly** — give each meaning a single source of truth and check every line for relevance. Hunt the named failure modes: **duplication** (same meaning in two places — inflates its prominence past its real rank), **sediment** (stale layers that settle because adding feels safe and removing feels risky — the default fate of any skill without a pruning discipline), **no-ops** (lines the agent already obeys by default — test per sentence, and delete the whole sentence rather than trim words), and **sprawl** (length itself, even when every line is live — cured by placement, not editing).
- **One term per concept** — a synonym reads as a second concept; never vary terminology.
- **Third-person imperative** — "Extract the text...", not "I will..." or "You should...". The skill is documentation the agent executes, not a dialogue with it.
- **Generic examples only** — a good/poor pair illustrates a principle; a narrative or session-dated example encodes state-of-the-world.
- **No authoring changelog** — never explain what was removed or changed; the reading agent needs the correct current instruction, not the history of how it got there.
- **Never silently drop process logic** when revising an existing skill — the future agent will lack that judgment without knowing it is missing; confirm removals with the skill's owner.

### Structural patterns

Reusable shapes for body content — use the ones that fit the task:

- **Gotchas section** — often the highest-value content: concrete corrections to mistakes the agent will otherwise make ("the health endpoint returns 200 even when the database is down — check the readiness endpoint instead"), not general advice. Keep gotchas in the body, where the agent reads them before encountering the situation — behind a pointer, it may not recognise the trigger. Every correction the user makes during real runs is a gotcha candidate.
- **Output template** — when output must follow a format, provide a template to copy: agents pattern-match against concrete structure more reliably than against prose descriptions. Short templates inline; long or branch-specific ones in `assets/`.
- **Checklist** — for multi-step workflows with dependencies or validation gates; an explicit checklist lets the agent track progress and not skip steps.
- **Validation loop** — do the work, run a validator (a script, a reference checklist, or a self-check), fix what it reports, and repeat until it passes. Only proceed on a pass.
- **Plan-validate-execute** — for batch or destructive operations: produce an intermediate plan in a structured format, validate the plan against a source of truth — with errors informative enough for self-correction ("field X not found; available fields: ...") — and only then execute.

## Anti-patterns

- **Workflow scripting** — encoding a fixed sequence when the task requires judgment about whether to follow a process at all. Encode the principles and the goal; let the agent determine the path. The tell: if removing every step header leaves nothing of substance, the steps were carrying the skill, not the intent.
- **Premature completion** — the agent ends a step before it is genuinely done because visible later steps pull its attention to *being done* (classically, "ask clarifying questions" collapses because "write the plan" sits right below it). Defend in order: **sharpen the completion criterion first** — it is local and cheap, and a checkable bar resists the pull no matter how many later steps are visible. Only when the criterion is irreducibly fuzzy *and* the rush is observed across real runs, hide the later steps by splitting the sequence — and only across a real context boundary (a separate skill or a sub-task dispatch); an inline call leaves the later steps in context and clears nothing.

## Validation

Run the bundled validator against the finished skill, using any runner that supports PEP 723 inline dependencies (default: `uv`):

```bash
uv run scripts/validate.py <skill-dir>
```

The script path is relative to this skill's directory; `<skill-dir>` is the skill being validated. It enforces the invariant rules in [references/spec-rules.md](references/spec-rules.md) and exits non-zero on failure — fix failures before shipping. Warnings flag portability tradeoffs to weigh, not defects; read that reference when a result needs interpreting.

The invariants are the stable subset of the [Agent Skills open standard](https://agentskills.io/specification). For anything beyond them — optional fields, packaging, evolving harness support — fetch the live specification.
