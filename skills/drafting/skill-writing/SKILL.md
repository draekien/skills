---
name: skill-writing
description: Creates, updates, and refines agent skills following the Agent Skills open standard (agentskills.io). Three modes — create (new skill from scratch), update (revise existing skill for new requirements), refine (audit and rewrite for health and token efficiency). Use when building/scaffolding a skill, or when the user says "create a skill", "make a skill", "new skill", "scaffold a skill", "update this skill", "modify this skill", "revise this skill", "refine this skill", "audit this skill", "compress this skill", "optimize this skill", "skill is too verbose", "clean up this skill".
compatibility: Designed for Claude Code (or similar products with Agent Skills support)
---

# Skill Writing

Creates, updates, and refines agent skills per the [Agent Skills open standard](https://agentskills.io/specification). Three modes, each with its own workflow.

## Mode Detection

Determine mode from trigger keywords first. If no keywords, check the filesystem.

| Priority | Signal | Mode |
|----------|--------|------|
| 1 | "create", "new skill", "make a skill", "scaffold" | **create** |
| 2 | "refine", "audit", "compress skill", "optimize skill", "too verbose", "clean up skill" | **refine** |
| 3 | "update", "modify", "revise", "change this skill" | **update** |
| 4 (fallback) | Target path provided, `SKILL.md` exists at path | **update** |
| 5 (fallback) | Target path provided, no `SKILL.md` at path | **create** |

Once mode is determined, read the corresponding reference file and follow it:

- **Create:** [references/create.md](references/create.md)
- **Update:** [references/update.md](references/update.md)
- **Refine:** [references/refine.md](references/refine.md)

Always read [references/principles.md](references/principles.md) and [references/structure.md](references/structure.md) alongside the mode file — every mode applies them.

## Writing Standards

Apply these whenever writing or rewriting any `SKILL.md` content:

- Third-person imperative: "Extract the text..." not "I will..." or "You should..."
- One term per concept — never vary
- No comments explaining what was removed or changed
- **No tool names** — never reference specific agent tools (e.g. WebSearch, Grep, SendMessage) or MCP tool names; describe capabilities instead ("search the web", "read local files", "send a direct message") so the skill works across agents with different toolsets
- **Match freedom to task fragility** — see [references/principles.md](references/principles.md) for the high/medium/low rubric
- **Trust the agent's intelligence** — omit context it already has; challenge each paragraph against "would the agent already know this?"
- **No narrative or session-dated examples** — abstract rules only; sessions/incidents go in PR descriptions, not skills
- **Activation lives in the description** — never write a "When to use this skill" section in the body

See [references/structure.md](references/structure.md) for content placement rules (body vs `references/` vs `assets/`).

## Post-Write Validation

Run after completing any create, update, or refine workflow:

```
uv run scripts/validate.py <skill-dir>
```

Fix failures before confirming to user. Script checks all `[AUTO]` rules in [references/spec-rules.md](references/spec-rules.md). Then manually review `[LLM]` rules there.
