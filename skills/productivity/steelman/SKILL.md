---
name: steelman
description: Builds the strongest possible case for a perspective, idea, or decision, using a dedicated subagent. Use when you want to see the best version of an argument before deciding whether to act on it.
disable-model-invocation: true
---

Spawn a subagent to build the strongest possible case *for* the target. Determine the target from the user's most recent message; if absent, scan earlier turns for the most recently discussed position or idea. If it is unclear, ask what to steelman.

If the target position is harmful, illegal, or calls for violence or discrimination, do not steelman it — tell the user you cannot build a genuine advocate case for that position and ask if there is a different angle to explore.

The reflex to hedge is the enemy. Never instruct the subagent to balance the argument, caveat, or note weaknesses — its only job is to be a genuine advocate. This is neither a neutral summary nor devil's advocacy: a devil's advocate finds problems; a steelman finds the best possible answers to them. Reason as if the position is correct and build outward — marshal the strongest evidence, logic, and values behind it, and resolve the most compelling objections from within its own logic. Carry only the strongest material — weak, easily dismissed arguments dilute the steelman.

Return the steelman directly: no preamble, just the argument. Two to four paragraphs as a default; go longer only when each additional paragraph carries a distinct argument.
