---
name: skill-refining
description: Audits and rewrites an existing SKILL.md for health and token efficiency. Reads the target skill, diagnoses structural problems and token waste, aligns with the user on decisions, then rewrites. Use when a skill feels too verbose, has structural problems, or when the user says "refine this skill", "this skill is too thick", "compress this skill", "skill is too verbose", "audit this skill", "clean up this skill", or "optimize this skill".
---

# Skill Refining

Read an existing SKILL.md, diagnose problems across four categories, align with the user on decisions, then rewrite.

## Step 1 — Read

Read the target `SKILL.md` and all files in its `references/` directory (if any).

If no target path provided, ask the user which skill to refine before continuing.

## Step 2 — Diagnose

Identify problems across four categories:

**Token waste**
- Verbatim LLM response templates — `> "..."` blocks specifying exact phrasing. Rule: describe behavior, not words.
- Prose describing what the LLM will say rather than rules the LLM must follow.
- Repeated explanations of the same rule across multiple steps.
- Examples in the body that belong in `references/` or `assets/`.

**Structural mismatch**
- Sequential numbered steps for behaviors that are concurrent or trigger-based (e.g. ongoing monitors, event-driven sub-flows).
- One-time setup actions mixed with recurring behaviors — these need separate sections.
- Steps that are sub-flows of other steps presented as peers.

**Content placement**
- Format specs, schemas, lookup tables, or relationship taxonomies in the body that belong in `references/`.
- Output templates described in prose that belong in `assets/`.
- Body over 80 lines when reference files could absorb the excess.

**Outdated content**
- Migration steps for already-completed migrations.
- References to deprecated file names or patterns.
- Steps that duplicate behavior the LLM already knows from training (e.g. "use the Read tool to read a file").

## Step 3 — Present Diagnostic Report

List every found problem: category, description, and recommended fix. Present as a flat list — one problem per line. Do not rewrite anything yet.

## Step 4 — Align

For each fix with meaningful tradeoffs, ask the user one question at a time before touching anything. Examples of decisions requiring alignment:

- Drop verbatim templates entirely vs. move to `references/` for occasional lookup
- Restructure sequential steps into Session Start + Active Behaviors vs. keep numbered with inline annotations
- Move content to `references/` (requires reading a new file on activation) vs. keep in body (always loaded)

Proceed with unambiguous fixes (e.g. removing duplicate rule explanations) without asking.

## Step 5 — Rewrite

Apply all confirmed decisions. Rewrite the `SKILL.md` in place. Do not touch `references/` files unless content is being moved into or out of them.

Instruction style rules:
- Third-person imperative: "Search the codebase..." not "I will search..."
- One term per concept — never vary
- No comments explaining what was removed or changed

## Step 6 — Verify

After rewriting:
1. Confirm line count is lower than original.
2. Confirm no verbatim `> "..."` quote blocks remain.
3. Confirm all relative file links in the body still resolve.
4. Confirm all original process logic is preserved — nothing dropped without user confirmation.

Report line count before and after.

## Gotchas

- Never drop process logic without explicit user confirmation — even if it looks redundant.
- "Outdated" is a judgment call — surface it, don't silently delete it.
- Moving content to `references/` trades token weight at activation for an extra file read per run. Surface this tradeoff before moving.
- Structural mismatch problems often require more user alignment than token waste problems — the user knows the intended execution model.
