---
name: get-aligned
description: Aligns you and the assistant before acting, by surfacing open decisions one at a time in order of impact. Use when a request is ambiguous, has multiple valid approaches, or has not been fully scoped yet.
disable-model-invocation: true
---

Drive toward shared understanding by identifying all open decisions in the request, then surfacing them one at a time in order of impact. Ask about the highest-impact open decision first, use the answer to surface the next dependent decision, and keep probing — do not stop after the first answer — until no open decisions remain. For contested or consequential decisions, briefly state the trade-offs and your recommendation. For clear or low-stakes decisions, ask directly without analysis.

If an open decision is answerable by exploring the project, explore the project instead of asking — don't spend the human's attention on something discoverable without them.

If the human asks you to proceed before all open decisions are resolved, list the remaining ones briefly, state the assumptions you will use, and begin.
