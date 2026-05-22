---
name: steelman
description: Builds the strongest possible case for any perspective, idea, or decision by delegating to a focused subagent. Use when stress-testing a position, pressure-testing a decision, or making sure the best version of an argument has been heard — or when the user says "steelman this", "steelman my idea", "make the best case for", "strongest argument for".
---

## Identify the Target

Determine what to steelman from the current session. If the topic is not clear, prompt the user to specify the topic.

## Brief the Subagent

Spawn a single subagent with the target position and any relevant session context (domain constraints, prior objections raised, known alternatives). Include the steelman mandate below as the operating instruction.

Do not give the subagent hedging instructions or ask it to balance the argument — its only job is to be a genuine advocate.

## Steelman Mandate

A steelman is the strongest internally consistent version of a position — not a neutral summary, not devil's advocacy, but the best case a thoughtful proponent would actually make. The difference matters: a devil's advocate finds problems; a steelman finds the best possible answers to them. The subagent should:

- Reason as if the position is correct and build outward from that foundation
- Surface the strongest evidence, logic, and values that support it
- Anticipate the most compelling objections and resolve them from within the position's own logic
- Carry only its strongest material — weak or easily dismissed arguments dilute the steelman

## Present the Result

Return the subagent's steelman directly to the user. No preamble — just the argument. One to three paragraphs unless the topic demands more depth.
