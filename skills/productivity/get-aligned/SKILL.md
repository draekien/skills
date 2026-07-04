---
name: get-aligned
description: Aligns you and the assistant before acting, by surfacing open decisions one at a time in order of impact. Use when a request is ambiguous, has multiple valid approaches, or has not been fully scoped yet.
disable-model-invocation: true
---

Drive toward shared understanding by identifying all open decisions in the request, then surfacing them one at a time in order of impact. Ask about the highest-impact unknown first, use the answer to surface the next dependent decision, and keep probing — do not stop after the first answer — until no material unknowns remain. For contested or consequential decisions, briefly state the trade-offs and your recommendation. For clear or low-stakes questions, ask directly without analysis.

Ask questions one at a time.

If question answerable by exploring project, explore project instead.

If the human asks you to proceed before all open questions are resolved, list any remaining unknowns briefly, state the assumptions you will use, and begin.
