---
name: draft-a-prd
description: Creates a structured product requirements document, first aligning with you on scope and requirements before writing it. Use when defining a new feature or product and you need a complete PRD.
argument-hint: "[feature or product description]"
disable-model-invocation: true
---

# Draft a PRD

## Phase 1 — Alignment

If the opening message or prior conversation supplies — without guessing — enough information to populate every required section of the template (Problem Statement, Goals, User Stories, Out of Scope, Testing Decisions; Additional Notes is optional and does not affect this check), skip directly to Phase 2.

Otherwise, tell the user that scope isn't resolved yet and ask them to run `/get-aligned` to work through the open decisions — it is not model-invocable, so it must be invoked directly. Once they confirm alignment, or ask to proceed early, record every remaining unresolved decision and stated assumption in the Open Questions section and continue to Phase 2.

## Phase 2 — Draft

Write the PRD following the template in [assets/prd-template.md](assets/prd-template.md).

Enforce these rules without exception:

- **Goals** — each must be measurable and verifiable (a number, threshold, or observable outcome); reject vague goals like "improve the experience"
- **User stories** — numbered sequentially, format: "As a [role], I want [action] so that [outcome]"
- **Out of scope** — list specific exclusions, not general deferrals; "future work" is not a valid exclusion
- **No implementation details** — no file paths, architecture decisions, or library and framework names; describe *what*, not *how*
- **Testing decisions** — state the testing methodology (e.g. automated, manual, exploratory) and any constraints (e.g. no production data, specific environments); do not enumerate individual test cases or assign ownership
- **Problem statement** — state who experiences the problem and why it matters; no solution language
- **Open questions** — omit the section entirely if none

## Phase 3 — Review

Present the draft and invite feedback. Revise until the user explicitly confirms the PRD is complete. On confirmation, output the final PRD in full as the closing response.
