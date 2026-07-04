---
name: steelman
description: Steelmans a perspective, idea, or decision by building the strongest possible case for it, using a dedicated subagent. Use when you want to see the best version of an argument before deciding whether to act on it, or when the user says "steelman this".
argument-hint: "[target]"
disable-model-invocation: true
---

Spawn a subagent to build the strongest possible steelman *for* the target. Determine the target from the user's most recent message; if absent, scan earlier turns for the most recently discussed target. If it is unclear, ask what to steelman.

If the target is harmful, illegal, or calls for violence or discrimination, do not steelman it — tell the user you cannot build a genuine advocate steelman for that target and ask if there is a different angle to explore.

The reflex to hedge is the enemy. Never instruct the subagent to balance the steelman, caveat, or note weaknesses — its only job is to be a genuine advocate. This is neither a neutral summary nor devil's advocacy: a devil's advocate finds problems; a steelman finds the best possible answers to them. Reason as if the target is correct and build outward — marshal the strongest evidence, logic, and values behind it, and resolve the most compelling objections from within its own logic. Carry only the strongest material — weak, easily dismissed arguments dilute the steelman.

Return the steelman directly: no preamble. Two to four paragraphs as a default; go longer only when each additional paragraph carries a distinct argument.
