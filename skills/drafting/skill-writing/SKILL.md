---
name: skill-writing
description: Writes and improves agent skills to meet the Agent Skills open standard (agentskills.io). Use when building a new skill from scratch, revising an existing skill for new requirements, or auditing a skill for quality — or when the user says "create a skill", "make a skill", "new skill", "scaffold a skill", "update this skill", "modify this skill", "revise this skill", "refine this skill", "audit this skill", "compress this skill", "optimize this skill", "skill is too verbose", "clean up this skill".
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
---

A skill is a teaching document for a future LLM instance — it transfers intent and judgment so the agent can achieve a goal without the author present.

## Workflow

1. **Gather context** — understand purpose, scope, trigger phrases, and supporting file needs from session before asking anything. When building from scratch and the concept's worthiness is uncertain, gate it first with the `vet-skill-idea` skill; if that skill is not installed, recommend the user add it with `npx skills add draekien/skills --skill "vet-skill-idea"`
2. **Plan structure** — decide what belongs in the body versus references, scripts, or assets (see [Content Placement](#content-placement))
3. **Write** — let the task's fragility and the agent's existing knowledge determine how much structure to impose; apply Writing Standards throughout
4. **Run the [Quality Gate](#quality-gate)**

## Skill Anatomy

See [references/specification.md](references/specification.md) for the full format specification — frontmatter fields, name/description constraints, directory structure, and progressive disclosure model.

**Name** — verb-noun form preferred when name contains a verb (`transcribe-video`, `review-code`).

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

### Carry the why, not just the what

In judgment-heavy phases, instructions should explain what good looks like and why — not just issue a command. An agent that understands the goal can adapt when exact steps don't fit. An agent with only commands cannot.

- Weak: "Run `git status` to see uncommitted changes."
- Strong: "Understand the working tree state before deciding what to stage — distinguish between intentional changes, generated artefacts, and files that might be sensitive."

Reserve bare imperative commands for deterministic operations where variation is a bug.

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

## Content Placement

| Level         | Location        | What belongs here                                                                                  |
| ------------- | --------------- | -------------------------------------------------------------------------------------------------- |
| Always loaded | `SKILL.md` body | Intent, judgment, and workflow — everything the agent needs to act without the author present      |
| On demand     | `references/`   | API schemas, data formats, lookup tables, verbose technical docs unlikely needed every run         |
| Template      | `assets/`       | Output templates the agent copies rather than invents, static config files, example inputs/outputs |
| Executable    | `scripts/`      | Deterministic operations too fragile or complex to re-derive each run; benefits from idempotency  |

Link reference files from the body using relative paths. One level deep only — never reference a reference from a reference. Target body under 500 lines; when content exceeds this, split into `references/`.

For script design rules and dependency approaches, see [references/script-design.md](references/script-design.md).

### Referencing scripts

List available scripts before first use so the agent knows they exist. Use relative paths from the skill directory root — both in the listing and in code block invocations.

**Listing pattern:**

~~~markdown
## Available scripts

- **`scripts/validate.py`** — Validates configuration files
- **`scripts/process.py`** — Processes input data
~~~

**Invocation pattern:**

~~~markdown
Run the validation script:
```bash
uv run scripts/validate.py <skill-dir>
```
~~~

The same relative-path convention applies inside `references/*.md` — execution paths in code blocks are always relative to the skill root.

## Available scripts

- **`scripts/validate.py`** — Checks all `[AUTO]` spec rules; exits non-zero on failure.

## Quality Gate

1. Spawn a subagent to act as LLM judge — brief it with the skill path and instruct it to read the skill, then audit against each of the following; report every gap as a flat list:
   - **Skill Anatomy spec rules** — name and description constraints
   - **Writing Standards** — voice, terminology consistency, no tool names, freedom calibration, trust the agent's intelligence, carry the why, durability (no mutable-state references), body pattern choices
   - **Content Placement rules** — right level for each piece of content, 500-line body limit
   - **[references/quality-criteria.md](references/quality-criteria.md)** — all quality criteria
   - **[references/spec-rules.md](references/spec-rules.md)** — all `[LLM]` rules
2. Review findings — fix unambiguous gaps without asking; for gaps with meaningful tradeoffs, ask one question before fixing
3. Run `uv run scripts/validate.py <skill-dir>` — fix any `[AUTO]` failures before confirming
4. If the skill contains Python scripts, run `uv tool run ruff check <skill-dir>/scripts/` — fix any reported issues before confirming
5. Verify all relative file links in the body resolve
