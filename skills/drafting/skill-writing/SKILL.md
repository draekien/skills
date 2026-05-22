---
name: skill-writing
description: Creates, updates, and refines agent skills following the Agent Skills open standard (agentskills.io). Three modes — create (new skill from scratch), update (revise existing skill for new requirements), refine (audit and rewrite for health and token efficiency). Use when building/scaffolding a skill, or when the user says "create a skill", "make a skill", "new skill", "scaffold a skill", "update this skill", "modify this skill", "revise this skill", "refine this skill", "audit this skill", "compress this skill", "optimize this skill", "skill is too verbose", "clean up this skill".
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
---

# Skill Writing

Creates, updates, and refines agent skills per the [Agent Skills open standard](https://agentskills.io/specification). Three modes, each with its own workflow.

## Mode Detection

Determine mode from trigger keywords first. If no keywords, check the filesystem.

| Priority     | Signal                                                                                 | Mode       |
| ------------ | -------------------------------------------------------------------------------------- | ---------- |
| 1            | "create", "new skill", "make a skill", "scaffold"                                      | **create** |
| 2            | "refine", "audit", "compress skill", "optimize skill", "too verbose", "clean up skill" | **refine** |
| 3            | "update", "modify", "revise", "change this skill"                                      | **update** |
| 4 (fallback) | Target path provided, `SKILL.md` exists at path                                        | **update** |
| 5 (fallback) | Target path provided, no `SKILL.md` at path                                            | **create** |

Once mode is determined, read the corresponding reference file and follow it:

- **Create:** [references/create.md](references/create.md)
- **Update:** [references/update.md](references/update.md)
- **Refine:** [references/refine.md](references/refine.md)

## Writing Standards

Apply these whenever writing or rewriting any `SKILL.md` content:

- Third-person imperative: "Extract the text..." not "I will..." or "You should..."
- One term per concept — never vary
- No comments explaining what was removed or changed
- **No tool names** — never reference specific agent tools (e.g. WebSearch, Grep, SendMessage) or MCP tool names; describe capabilities instead ("search the web", "read local files", "send a direct message") so the skill works across agents with different toolsets
- **Activation lives in the description** — never write a "When to use this skill" section in the body
- **No narrative or session-dated examples** — content like "In session 2025-10-03 we found..." is too specific and decays into noise; replace with the abstract rule; generic illustrative examples (good vs poor pair) are fine

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

### Test against your target models

Skills augment models; effectiveness depends on the host model.

- Smaller/faster models: does the skill provide enough scaffolding?
- Mid-tier models: is it clear and efficient?
- Largest models: does it avoid over-explaining?

If the skill runs across model tiers, aim for instructions that work for all of them.

## Content Placement

Place content at the level where it is first needed.

| Level         | Location        | What belongs here                                                                                  |
| ------------- | --------------- | -------------------------------------------------------------------------------------------------- |
| Always loaded | `SKILL.md` body | Complete workflow steps, decision logic, all info needed on first activation                       |
| On demand     | `references/`   | API schemas, data formats, lookup tables, verbose technical docs unlikely needed every run         |
| Template      | `assets/`       | Output templates the agent copies rather than invents, static config files, example inputs/outputs |

Link reference files from the body using relative paths. One level deep only — never reference a reference from a reference. Target body under 500 lines; when content exceeds this, split into `references/`.

### Supporting files

**`scripts/`** — use when the task is deterministic (variation = bug), the agent would re-derive complex logic each run, or the operation benefits from idempotency.

Script design rules (non-negotiable for agent compatibility):

- No interactive prompts — must run fully unattended
- Structured stdout (data output) vs stderr (diagnostic logs)
- Actionable error messages — tell agent how to self-correct
- Idempotent — safe to run twice
- Dry-run flag for destructive operations
- Meaningful exit codes (0 = success, non-zero = specific failure)
- Output size guards to avoid harness truncation

Dependency approaches (in order of preference):

1. One-off invocation with pinned version: `uvx some-tool@1.2.3` or `npx tool@version`
2. Self-contained script with PEP 723 inline deps (Python): `# dependencies = ["httpx==0.27.0"]`
3. Full documented dependency list if above insufficient

**`references/`** — use when docs are verbose but not needed every activation, content is stable reference material (schemas, cheatsheets, domain specs), or loading every time wastes context.

**`assets/`** — use when the agent needs a concrete template to copy (not invent), or static config/example files are needed.

## Post-Write Validation

Run after completing any create, update, or refine workflow:

```
uv run scripts/validate.py <skill-dir>
```

Fix failures before confirming to user.
Script checks all `[AUTO]` rules in [references/spec-rules.md](references/spec-rules.md).
You must manually review `[LLM]` rules in [references/llm-rules.md](references/spec-rules.md)
