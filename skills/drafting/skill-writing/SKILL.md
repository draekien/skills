---
name: skill-writing
description: Writes and improves agent skills to meet the Agent Skills open standard (agentskills.io). Use when creating a new skill from scratch, revising an existing one for new requirements, or auditing a skill for quality.
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
disable-model-invocation: true
---

A skill is a teaching document for a future LLM instance — it transfers intent and judgment so the agent can achieve a goal without the author present.

## Workflow

1. **Gather context** — understand purpose, scope, trigger phrases, and supporting file needs from session before asking anything. When building from scratch and the user has not already validated the concept (no prior research, no vet-skill-idea output in session, and no clear existing use-case driving the request), ask the user to run `/vet-skill-idea` first — it is not model-invocable, so it must be invoked directly; if that skill is not installed, recommend the user add it with `npx skills add draekien/skills --skill "vet-skill-idea"`; if the verdict is to not proceed, surface the reasons to the user and stop — do not continue to the remaining workflow steps
2. **Plan structure** — characterise the skill on both axes — knowledge↔procedural (see [Knowledge or Procedural](#knowledge-or-procedural)) and stateful↔stateless (see [Stateful or Stateless](#stateful-or-stateless)) — then decide what belongs in the body versus references, scripts, or assets (see [Content Placement](#content-placement))
3. **Write** — let the task's fragility and the agent's existing knowledge determine how much structure to impose; apply Writing Standards throughout
4. **Run the [Quality Gate](#quality-gate)**

## Skill Anatomy

See [references/specification.md](references/specification.md) for the full format specification — frontmatter fields, name/description constraints, directory structure, and progressive disclosure model.

**Name** — verb-noun form preferred when name contains a verb (`transcribe-video`, `review-code`).

**Argument hint** — if the skill takes arguments, add an `argument-hint` frontmatter field with a free-text usage cue, e.g. `[issue-number]` or `[filename] [format]`. This is a harness-specific extension, not part of the open standard, but it's the one worth adding by default: it's supported under that exact name on more than one harness, and a harness that doesn't recognize it just ignores the field — there's no working structure to fall back to for expected arguments otherwise, so the cost of including it is zero and the upside is real. Don't invent a structured argument schema beyond this hint; that capability exists on at most one harness today and isn't worth designing a skill around.

**Description** — the sole activation signal; write as an API contract:

```
<verb> <what it does>. Use when <conditions>, or when the user says "<phrase 1>", "<phrase 2>".
```

Imperative, embeds trigger phrases verbatim.

## Context First, Then Interview

Exhaust what the session already provides before asking anything. If purpose, scope, trigger phrases, and supporting file needs are clear from context, proceed directly. When genuine gaps remain, surface them one at a time — give a recommendation and the key tradeoff, and resolve interdependent decisions before moving on. Context informs your choices, but only timeless principles belong in the skill body.

## Writing Standards

These standards ensure the skill transfers cleanly — the agent reading it cold should receive the author's intent without noise or ambiguity:

- Third-person imperative: "Extract the text..." not "I will..." or "You should..."
- One term per concept — never vary
- No comments explaining what was removed or changed
- **No tool names** — describe capabilities instead ("search the web", "read local files") so the skill works across agents with different toolsets
- **Activation lives in the description** — never write a "When to use this skill" section in the body
- **No narrative or session-dated examples** — generic illustrative examples (good vs poor pair) are fine
- **Encode timeless principles, not the current state of the world** — never write facts about the mutable environment the skill runs against (corpus contents, file counts, "all existing X do Y"). Such facts rot as the skill is used — most sharply when the skill exists to change that very state. Abstract any session or codebase observation into the durable rule before it enters the body.
- **Never drop process logic from an existing skill without explicit confirmation** — the future agent will lack that judgment without knowing it's missing

### Match freedom to fragility

Calibrate specificity to how variable and fragile the task is:

- **High freedom** — reasoning-carrying prose. Use when multiple approaches are valid and judgment determines the path.

  ```
  Understand the current state of the codebase before suggesting changes — look for shallow
  modules, tight coupling, and untested seams. The goal is to surface friction, not apply a checklist.
  ```

- **Medium freedom** — pseudocode or parameterised templates. Use when a preferred pattern exists but some variation is acceptable.

  ```
  def generate_report(data, format="markdown", include_charts=True): ...
  ```

- **Low freedom** — exact scripts, few or no parameters. Use when operations are fragile, consistency is critical, or a specific sequence must hold.

  ```
  Run exactly: python scripts/migrate.py --verify --backup
  ```

Analogy: narrow bridge with cliffs → low freedom. Open field → high freedom. Choose by terrain.

If the judgment required is *whether* to follow a process at all — not just how to execute it — encoding the process is wrong regardless of terrain (see the Workflow scripting [anti-pattern](#anti-patterns)).

### Trust the agent's intelligence

Every token spent on knowledge the agent already carries is noise that buries the intent that actually needs to transfer. Challenge every paragraph against:

- Does the agent really need this explanation?
- Can this be assumed as common knowledge?
- Does this content justify its token cost?

Those questions find what to cut. The inverse finds what to keep: a skill's highest-value content is the *delta from the agent's defaults* — what it would not do on its own, most sharply an instruction that countermands a strong reflex (to help, to solve, to elaborate). When a skill defines a role or behaviour the agent could already approximate, that delta is the whole payload; describing the role is not. Ask what is non-obvious to the agent, and write that.

Run the **deletion test** on anything you're unsure about: delete the paragraph and check whether the agent's output would actually change. If it wouldn't, the paragraph was dead weight — cut it, unless it's process logic from an existing skill, which the rule above requires confirming before removing regardless of what the deletion test says. Bloat traces back to one of three causes:

- **Duplication** — the same rule stated in more than one place; give each concept a single source of truth and cross-reference it, never restate it
- **Sediment** — older instructions nobody revisited as the skill evolved, now superseded or irrelevant; delete rather than layering a correction on top
- **No-ops** — instructions that read as if they change behaviour but don't, because the agent already does them by default; the deletion test catches these directly

### Carry the why, not just the what

This is the technique for writing the high-freedom prose [Match freedom to fragility](#match-freedom-to-fragility) calls for: instructions should explain what good looks like and why — not just issue a command. An agent that understands the goal can adapt when exact steps don't fit. An agent with only commands cannot.

- Weak: "Run `git status` to see uncommitted changes."
- Strong: "Understand the working tree state before deciding what to stage — distinguish between intentional changes, generated artefacts, and files that might be sensitive."

Reserve bare imperative commands for deterministic operations where variation is a bug.

### Steer with leading words

A leading word is a domain term, deliberately chosen and repeated, that compresses an instruction into something the agent's training already has strong priors about — so it self-reinforces, surfacing unprompted in the agent's own reasoning and output rather than needing to be re-issued. Anchoring on an existing term beats inventing bespoke phrasing for the same idea.

- Weak, bespoke phrasing: "Don't build the whole thing layer by layer — get something small working first."
- Strong, leading word: "Build a **vertical slice** first" — then keep using "vertical slice" wherever the skill returns to that idea, instead of re-describing it each time.

Pick the term deliberately, then hold it constant everywhere the skill touches that idea (this is also [one term per concept](#writing-standards)). This can only be verified by running the skill against a live agent and checking whether the term reappears unprompted in its reasoning trace or output — a Quality Gate read-through cannot confirm it; if a live run shows the term didn't take hold, it either wasn't leading enough or wasn't repeated enough.

### Body patterns

Choose structures that best surface the judgment the agent needs — the right pattern depends on what kind of knowledge needs to transfer:

- **Gotchas section** — for known pitfalls the agent would otherwise fall into
- **Output template in `assets/`** — for outputs the agent should copy rather than invent
- **Checklist** — when order matters but steps are independent
- **Validation loop** — "if output doesn't satisfy X, retry with Y" for fragile generations
- **Philosophy section** — opens with the core principle and explains *why* it matters before any workflow; use when task judgment matters more than step adherence
- **Anti-pattern section** — names the common wrong approach, explains the mechanism by which it fails, contrasts with correct behaviour; "don't do X" gives the agent no way to recognise X in the wild
- **Concept-named phases** — name phases by what the agent is doing conceptually rather than by sequence; names that encode the mental model survive when steps are skipped or reordered

## Anti-patterns

**Workflow scripting** — encoding a fixed sequence of steps when the task requires judgment about whether to follow a process at all. A skill that prescribes "interview the user, then write the spec" fails when the codebase already answers the interview questions and the spec is an artefact nobody needs. Encode the principles and the goal instead; let the agent determine the path. Recognise it by this tell: if removing every step header leaves nothing of substance, the steps were carrying the skill — not the intent.

**Shortchanged legwork** — an early step gets rushed because the agent's attention is already pulled toward a later step's goal visible in the same file (classically: "ask clarifying questions" gets skipped or token-boxed because "write the plan" is sitting right below it). Encoding the step more forcefully in the same skill rarely fixes this — the pull toward the visible next goal remains. Split the shortchanged step into its own skill instead, so the agent doing that step cannot see the later phase at all and gives it full attention. Reach for this only after the same step is observed being skipped or rushed across multiple real runs (a skill eval or repeated live use, not a single authoring pass) — not preemptively for every multi-step skill.

## Knowledge or Procedural

Every skill sits on a spectrum between two purposes, and most carry some of
both. **Knowledge** skills seed information the agent would otherwise lack — a
team's coding standards, a person's preferences, how a technology works,
principles to follow; the payload is the information. **Procedural** skills
change how the agent works — a workflow, an output style, an SOP, a process to
follow; the payload is the behaviour. Name where the skill sits before writing,
because each end stresses different standards and suggests a different
invocation default:

- **Toward knowledge** — the value is the *delta from what the agent already
  knows* (see [Trust the agent's intelligence](#trust-the-agents-intelligence));
  state only what is non-obvious, keep facts durable (no mutable-state
  references), and let the bulk live in `references/` with the body as a thin
  router. Consider making it not user-invocable so it surfaces by automatic
  relevance rather than as a manual command.
- **Toward procedural** — calibrate [freedom to fragility](#match-freedom-to-fragility),
  [carry the why](#carry-the-why-not-just-the-what), and avoid
  [workflow scripting](#anti-patterns); the judgment lives in the body. Consider
  making it not model-invocable so the user turns the process on deliberately
  rather than the agent auto-firing it onto unrelated tasks.

These invocation controls (`user-invocable`, `disable-model-invocation`) are
harness-specific frontmatter, not part of the open standard — recommendations to
weigh where supported, not defaults to apply blindly.

## Stateful or Stateless

A skill is stateless by default — each run starts fresh and derives what it needs from the session. Make a skill stateful only when it must remember something across sessions that cannot be re-derived. State comes in two kinds: **config** — per-project settings that change how the skill behaves (an output directory, a dictionary path) — and **working artefacts** — data the skill builds up and maintains across runs (a glossary, a set of specs). If the information is cheap to rediscover each session, it is not state; persisting it just creates a second source of truth that drifts.

When the skill is stateful, apply every rule in [references/stateful-skills.md](references/stateful-skills.md) — each guards a distinct failure mode.

## Content Placement

Before placing content, identify the skill's **branches** — the distinct ways it gets used (a `domain-modeling` skill might branch into "update a glossary" or "write an ADR"). Material only one branch needs — its template, its reference doc, its edge cases — moves to `references/` or `assets/` as a context pointer the agent reads only when that branch is taken. Material every branch needs is a candidate for the body, but yields to the [Knowledge or Procedural](#knowledge-or-procedural) default first — a knowledge-leaning skill still pushes shared bulk to `references/` behind a thin router even when every branch needs it.

| Level         | Location        | What belongs here                                                                                  |
| ------------- | --------------- | -------------------------------------------------------------------------------------------------- |
| Always loaded | `SKILL.md` body | Intent, judgment, and workflow — everything the agent needs to act without the author present      |
| On demand     | `references/`   | API schemas, data formats, lookup tables, verbose technical docs unlikely needed every run         |
| Template      | `assets/`       | Output templates the agent copies rather than invents, static config files, example inputs/outputs |
| Executable    | `scripts/`      | Deterministic operations too fragile or complex to re-derive each run; benefits from idempotency  |

Link reference files from the body using relative paths. One level deep only — never reference a reference from a reference. Target body under 500 lines; when content exceeds this, split into `references/`.

When the skill bundles scripts, see [references/script-design.md](references/script-design.md) for design rules, dependency approaches, and the listing/invocation patterns for referencing scripts from the body.

## Available scripts

- **`scripts/validate.py`** — Checks all `[AUTO]` spec rules; exits non-zero on failure. Harness-specific frontmatter fields pass with a non-blocking portability warning; a non-portable form of a shared open-standard field (e.g. an `allowed-tools` YAML list) fails.

## Quality Gate

1. Spawn three LLM-judge subagents in parallel — give each the skill path and a single specialised remit so it audits deeply rather than spreading thin. Each reads the skill and reports every gap in its remit as a flat list:

   | Judge | What to read | What to check |
   | --- | --- | --- |
   | **Spec & structure** | Skill Anatomy; all `[LLM]` rules in [references/spec-rules.md](references/spec-rules.md); [references/stateful-skills.md](references/stateful-skills.md) when stateful; [references/script-design.md](references/script-design.md) when the skill bundles scripts | Name and description constraints; every `[LLM]` rule; Content Placement (right level for each piece, 500-line body limit); state only where it cannot be re-derived, and stateful skills satisfy every stateful-skills.md rule; bundled scripts satisfy every script-design.md rule |
   | **Writing-standards** | all quality criteria in [references/quality-criteria.md](references/quality-criteria.md) | Voice, terminology consistency, no tool names, freedom calibration, trust the agent's intelligence, deletion-test failures (duplication, sediment, no-ops), leading-word consistency, a shortchanged step that should be split into its own skill, carry the why, durability (no mutable-state references), body pattern choices, branch material misplaced in the body |
   | **Prompt-analysis** | [references/prompt-analysis.md](references/prompt-analysis.md) | The body as a prompt: contradictions, ambiguity, persona/voice consistency, cognitive load, semantic coverage, composition conflicts with linked files — applying the findings discipline |

2. Merge the three judges' findings, then review — fix unambiguous gaps without asking; for gaps with meaningful tradeoffs, ask one question before fixing
3. Run `uv run scripts/validate.py <skill-dir>` — fix any `[AUTO]` failures before confirming (if uv is unavailable, check `[AUTO]` rules manually against [references/spec-rules.md](references/spec-rules.md) before confirming)
4. If the skill contains Python scripts, run `uv tool run ruff check <skill-dir>/scripts/` — fix any reported issues before confirming
5. Verify all relative file links in the body resolve
