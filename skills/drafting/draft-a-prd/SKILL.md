---
name: draft-a-prd
description: Creates a structured PRD by first aligning with the user on scope and requirements, then producing a complete product requirements document. Use when defining a new feature or product, or when the user says "create a PRD", "write a PRD", "draft a PRD", "I need a PRD", "product requirements document".
---

# Draft a PRD

Creates a structured PRD by interviewing the user, aligning on scope, then writing a complete document.

## Phase 1 — Alignment

If the current session already provides sufficient context to write an accurate PRD, skip directly to Phase 2.

Otherwise, interview relentlessly about every aspect of the request until shared understanding is reached. Walk down each branch of the design tree, resolving dependencies between decisions one by one. For each question, provide pros/cons of each choice and explain the recommendation.

Ask questions one at a time. If a question is answerable by exploring the project, explore the project instead.

## Phase 2 — Draft

Write the PRD following the template in [assets/prd-template.md](assets/prd-template.md).

Enforce these rules without exception:

- **Goals** — each must be measurable and verifiable (a number, threshold, or observable outcome); reject vague goals like "improve the experience"
- **User stories** — numbered sequentially, format: "As a [role], I want [action] so that [outcome]"
- **Out of scope** — list specific exclusions, not general deferrals; "future work" is not a valid exclusion
- **No implementation details** — no file paths, architecture decisions, or library and framework names; describe *what*, not *how*
- **Testing decisions** — state the testing approach and constraints, not individual test cases

## Phase 3 — Review

Present the draft and invite feedback. Revise until the user confirms.
