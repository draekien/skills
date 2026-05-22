---
name: devils-advocate
description: Challenges any topic, idea, plan, or position by surfacing the strongest objections, weakest assumptions, and most compelling counterarguments. Use when stress-testing a decision before committing, exposing blind spots in a proposal, or pressure-testing reasoning — or when the user says "play devil's advocate", "devil's advocate this", "argue against this", "poke holes in this", "what's wrong with this", "challenge my thinking".
---

## Identify the Target

Determine what to challenge from the current session. If the topic is not clear, ask the user to specify what they want challenged.

## Brief the Subagent

Spawn a single subagent with the target and any relevant session context (domain constraints, known assumptions, prior objections already raised). Include the adversarial mandate below as the operating instruction.

Do not give the subagent instructions to be balanced or fair — its only job is to find what's wrong, weak, or risky.

## Adversarial Mandate

Devil's advocacy is not steelmanning the opposition and not a balanced critique — it is the strongest possible case *against* a position. The difference: a steelman finds the best version of an argument; a devil's advocate finds the strongest reasons it fails. The subagent should:

- Identify the weakest assumptions the position depends on and show what breaks if they don't hold
- Surface the strongest objections a well-informed critic would raise
- Name unintended consequences, edge cases, and second-order effects that undermine the position
- Present the most plausible alternative framings that make the position look less compelling or necessary
- Carry only its sharpest material — mild or easily answered objections dilute the challenge

## Present the Result

Return the subagent's challenge directly. No preamble, no softening, no "to be fair" caveats. One to three paragraphs unless the topic demands more depth.
