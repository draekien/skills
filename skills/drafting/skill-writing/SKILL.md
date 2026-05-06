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

## Writing Standards

Apply these rules whenever writing or rewriting any `SKILL.md` content:

- Third-person imperative: "Extract the text..." not "I will..." or "You should..."
- One term per concept — never vary
- No comments explaining what was removed or changed
- Omit what the agent already knows (common tool usage, language syntax)

See [references/structure.md](references/structure.md) for progressive disclosure rules (what belongs in body vs `references/` vs `assets/`) and supporting file design rules.

## Post-Write Validation

Run after completing any create, update, or refine workflow:

```
uv run scripts/validate.py <skill-dir>
```

Fix failures before confirming to user. Script checks all `[AUTO]` rules in [references/spec-rules.md](references/spec-rules.md) — frontmatter structure, file references, body length, script safety, model-specific term heuristics.

Then manually review `[LLM]` rules in [references/spec-rules.md](references/spec-rules.md): description quality, instruction style, content placement, script robustness, security.
