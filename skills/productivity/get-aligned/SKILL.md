---
name: get-aligned
description: Aligns understanding between human and AI before acting. Use when the task has ambiguity, multiple valid approaches, unstated constraints, or non-trivial scope — including when the human says "help me think through", "let's figure out", "work with me on", or asks for a plan or design without full requirements.
---

Map every decision branch that could change the approach before acting. Walk down each branch one-by-one, resolving dependencies between decisions. For each question, provide your recommended answer. Include pros/cons for each decision you have made and why you have made the recommendation.

Ask questions one at a time, highest-impact first. After each answer, revisit the tree: prune resolved branches, surface any new ones. Repeat until every branch is resolved, then hand control back to the user.

If a question can be answered by exploring the project, explore the project instead.
