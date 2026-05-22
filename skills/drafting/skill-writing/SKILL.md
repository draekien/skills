---
name: skill-writing
description: Writes and improves agent skills to meet the Agent Skills open standard (agentskills.io). Use when building a new skill from scratch, revising an existing skill for new requirements, or auditing a skill for quality — or when the user says "create a skill", "make a skill", "new skill", "scaffold a skill", "update this skill", "modify this skill", "revise this skill", "refine this skill", "audit this skill", "compress this skill", "optimize this skill", "skill is too verbose", "clean up this skill".
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
---

A skill is a teaching document for a future LLM instance — it transfers intent and judgment so the agent can achieve a goal without the author present.

## Skill Anatomy

Every skill has:

- **Frontmatter** — `name`, `description`, optional `compatibility`
- **Body** — workflow steps, decision logic, and any information the agent needs on first activation
- **Supporting files** — `scripts/`, `references/`, `assets/` as needed (see Content Placement)

**Name** — 1–64 characters, `[a-z0-9-]` only, no leading/trailing/consecutive hyphens, matches parent directory name exactly. Verb-noun form preferred when name contains a verb (`transcribe-video`, `review-code`).

**Description** — the sole activation signal; write as an API contract:
```
<verb> <what it does>. Use when <conditions>, or when the user says "<phrase 1>", "<phrase 2>".
```
1–1024 characters, imperative, embeds trigger phrases verbatim.

## Context First, Then Interview

When the request is clear and session context provides sufficient detail, proceed directly. When ambiguity remains:

1. Extract what the session already provides — purpose, scope, trigger phrases, supporting file needs — before asking anything
2. For each remaining unknown, ask one targeted question; give your recommendation and the key tradeoff
3. Resolve dependencies between decisions before moving on

## Writing Standards

Apply these whenever writing or rewriting any `SKILL.md` content:

- Third-person imperative: "Extract the text..." not "I will..." or "You should..."
- One term per concept — never vary
- No comments explaining what was removed or changed
- **No tool names** — describe capabilities instead ("search the web", "read local files") so the skill works across agents with different toolsets
- **Activation lives in the description** — never write a "When to use this skill" section in the body
- **No narrative or session-dated examples** — replace with the abstract rule; generic illustrative examples (good vs poor pair) are fine
- **Never drop process logic from an existing skill without explicit confirmation** — silent removal is the hardest regression to catch

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

### Trust the agent's intelligence

Default to omitting context the agent already has. Challenge every paragraph against:

- Does the agent really need this explanation?
- Can this be assumed as common knowledge?
- Does this content justify its token cost?

If the answer is no, drop it.

### Carry the why, not just the what

In judgment-heavy phases, instructions should explain what good looks like and why — not just issue a command. An agent that understands the goal can adapt when exact steps don't fit. An agent with only commands cannot.

- Weak: "Run `git status` to see uncommitted changes."
- Strong: "Understand the working tree state before deciding what to stage — distinguish between intentional changes, generated artefacts, and files that might be sensitive."

Reserve bare imperative commands for deterministic operations where variation is a bug.

### Body patterns

Pick patterns that fit the task — don't force a template. Common shapes:

- **Gotchas section** — for known pitfalls the agent would otherwise fall into
- **Output template in `assets/`** — for outputs the agent should copy rather than invent
- **Checklist** — when order matters but steps are independent
- **Validation loop** — "if output doesn't satisfy X, retry with Y" for fragile generations
- **Philosophy section** — opens with the core principle and explains *why* it matters before any workflow; use when task judgment matters more than step adherence
- **Anti-pattern section** — names the common wrong approach, explains the mechanism by which it fails, contrasts with correct behaviour; "don't do X" gives the agent no way to recognise X in the wild
- **Concept-named phases** — name phases by what the agent is doing conceptually rather than by sequence; names that encode the mental model survive when steps are skipped or reordered

## Content Placement

Place content at the level where it is first needed.

| Level         | Location        | What belongs here                                                                                  |
| ------------- | --------------- | -------------------------------------------------------------------------------------------------- |
| Always loaded | `SKILL.md` body | Complete workflow steps, decision logic, all info needed on first activation                       |
| On demand     | `references/`   | API schemas, data formats, lookup tables, verbose technical docs unlikely needed every run         |
| Template      | `assets/`       | Output templates the agent copies rather than invents, static config files, example inputs/outputs |
| Executable    | `scripts/`      | Deterministic operations too fragile or complex to re-derive each run; benefits from idempotency  |

Link reference files from the body using relative paths. One level deep only — never reference a reference from a reference. Target body under 500 lines; when content exceeds this, split into `references/`.

For script design rules and dependency approaches, see [references/script-design.md](references/script-design.md).

## Available scripts

- **`scripts/validate.py`** — Checks all `[AUTO]` spec rules; exits non-zero on failure.

## After producing or improving a skill

1. Spawn a subagent to act as LLM judge — brief it with the skill path and instruct it to read the skill, audit against [references/quality-criteria.md](references/quality-criteria.md), and check all `[LLM]` rules in [references/spec-rules.md](references/spec-rules.md); report every gap as a flat list
2. Review findings — fix unambiguous gaps without asking; for gaps with meaningful tradeoffs, ask one question before fixing
3. Run `uv run scripts/validate.py <skill-dir>` — fix any `[AUTO]` failures before confirming
4. Verify all relative file links in the body resolve
