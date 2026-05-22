# Refine Mode

Audit an existing skill for health and token efficiency. Diagnose, align with the user, then rewrite.

## Phase 1 — Read

Read the target `SKILL.md` and every file under its `references/`. Ask which skill to refine if no path was given.

## Phase 2 — Diagnose

Identify problems across these categories. The writing principles define many of these — apply them as audit criteria.

**Token waste**
- Verbatim LLM response templates (`> "..."` blocks dictating exact phrasing). Describe behaviour, not words.
- Prose describing what the agent will say rather than rules it must follow.
- Repeated explanations of the same rule across multiple sections.
- Examples in the body that belong in `references/` or `assets/`.

**Mis-calibrated freedom**
- Low-freedom step-by-step instructions where the task is variable and heuristic-driven.
- High-freedom heuristics where the task is fragile or sequence-critical.

**Reasoning-absent instructions**
- Imperative commands in judgment-heavy phases that carry no reasoning ("do X" with no "so that Y" or "because Z").
- Phase names that are generic sequence numbers when a concept name would encode the mental model.
- Missing philosophy section in a skill where the agent needs to understand the goal before executing.
- Missing anti-pattern section where a predictable wrong approach exists.

**Trust violations**
- Content the agent already knows from training (language syntax, common tool usage).
- Paragraphs that don't justify their token cost.

**Body bloat**
- "When to use this skill" sections (activation belongs in the description, not the body).
- Narrative or session-dated examples ("In session 2025-10-03 we found...") that aren't reusable.

**Structural mismatch**
- Sequential numbered steps for behaviours that are concurrent or trigger-based.
- One-time setup mixed with recurring behaviours.
- Sub-flows presented as peers of their parent steps.

**Content placement**
- Format specs, schemas, lookup tables in the body that belong in `references/`.
- Output templates described in prose that belong in `assets/`.
- Body over 80 lines when references could absorb the excess.

**Outdated content**
- Migration steps for already-completed migrations.
- References to deprecated names or patterns.

## Phase 3 — Present

List every problem as a flat list — category, description, recommended fix. One per line. Don't rewrite yet.

## Phase 4 — Align

For each fix with meaningful tradeoffs, ask one question at a time before touching anything. Examples: drop verbatim templates entirely vs. move to `references/`; restructure sequential steps vs. keep numbered with annotations; move body content to `references/` (extra read per run) vs. keep inline (always loaded). Proceed with unambiguous fixes (duplicate rule explanations, etc.) without asking.

## Phase 5 — Rewrite

Apply confirmed decisions in place. Apply writing standards from main `SKILL.md`. Don't touch `references/` files unless content is moving into or out of them.

## Phase 6 — Verify

Before running the validator, confirm:

1. Line count is lower than original.
2. No verbatim `> "..."` quote blocks remain.
3. Every relative file link still resolves.
4. No process logic was dropped without user confirmation.

Report line count before and after, then run `scripts/validate.py` per main `SKILL.md`.

## Gotchas

- Never drop process logic without explicit confirmation, even when redundant.
- "Outdated" is a judgement call — surface it, don't silently delete.
- Moving content to `references/` trades token weight for an extra read per run. Surface the tradeoff before moving.
