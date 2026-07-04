---
name: draft-a-prd
description: Creates a structured product requirements document, first aligning with you on scope and requirements before writing it. Use when defining a new feature or product and you need a complete PRD.
disable-model-invocation: true
---

# Draft a PRD

Creates a structured PRD by interviewing the user, aligning on scope, then writing a complete document.

## Phase 1 — Alignment

If the opening message or prior conversation supplies enough information to populate every required section of the template (Problem Statement, Goals, User Stories, Out of Scope, Testing Decisions) — Additional Notes is optional and does not affect this check without guessing, skip directly to Phase 2.

Otherwise, interview relentlessly about every aspect of the request until shared understanding is reached. Walk down each branch of the design tree, resolving dependencies between decisions one by one. For high-stakes decisions where the choice materially changes scope or architecture, briefly note the key trade-off and your recommendation. For low-stakes clarifications, just ask.

Ask questions one at a time. If a question is answerable by exploring the project, explore the project instead.

If the user cannot answer a question, make a reasonable stated assumption and continue. Record every unresolved decision in the Open Questions section.

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

Present the draft and invite feedback. Revise until the user explicitly confirms the document is complete. On confirmation, output the final PRD in full as the closing response.
