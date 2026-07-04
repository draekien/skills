---
name: round-table
description: Assembles an adversarial agent team to compare competing options, approaches, or technologies. Champions debate each other directly, then a synthesizer subagent analyses the debate and delivers a recommendation. Use when comparing options and you want a rigorously debated comparison rather than a single opinion.
argument-hint: "[topic] [option1] [option2] ..."
compatibility: Requires Claude Code with agent teams enabled.
disable-model-invocation: true
---

Runs an adversarial debate: N champion teammates argue and challenge each other via direct messaging, then a synthesizer subagent analyses the settled debate and delivers a recommendation.

## Step 1 — Establish options

Build the option list from user input, inference, or a combination:

- **User-specified:** use exactly as provided
- **Propose:** generate 3–5 candidate options for the topic; present and let the user confirm, add, or remove
- **Hybrid:** merge user-supplied options with agent-proposed additions; present the merged list

Always display the final option list and ask for confirmation before spawning any agents.

Guard the option count: fewer than 2 options → tell the user a round-table needs at least 2 options and stop. Exactly 2 options → note this is a direct comparison and omit "consensus" framing from the synthesizer prompt.

## Step 2 — Spawn champion team

Create an agent team with one champion teammate per confirmed option. Run champions on a fast mid-tier model — the debate needs breadth and speed, not peak reasoning per turn.

Each champion receives:

- The debate topic
- Their assigned option
- The names of all other champions
- Instructions, in order:
  1. Research their option if needed (skip if sufficient context already exists).
  2. Build the strongest possible case for their assigned option.
  3. Send challenges to other champions via direct messaging whenever they find evidence that weakens a competing option, and respond to challenges directed at them.
  4. Treat this as a live scientific debate, not a one-shot argument — expect multiple rounds of challenge and rebuttal.
  5. Send a "done" message to the lead only after (1) they have sent all challenges they intend to send, and (2) they have received and responded to any challenges directed at them. Do not send "done" while awaiting a reply to an outstanding challenge. Exception: if the challenged champion has already sent "done" to the lead, treat the non-reply as a concession and proceed to send your own "done".
  6. If the lead sends a "wrap up — send your done signal" message, send "done" to the lead immediately, even if still awaiting a reply to an outstanding challenge.

**Anti-pattern — shallow debate:** a champion states its case once, finds no real weakness to attack, and sends "done" without ever testing a competing option. The synthesizer then has no rebuttals to weigh and defaults to whichever argument read best in isolation. Counter this by holding champions to instruction 3 — a champion that never attempts a challenge hasn't debated, it's only presented — and by having the synthesizer explicitly discount arguments that were never tested.

## Step 3 — Wait for close signals

Wait until all champions send their "done" message to the lead. If a champion has not sent "done" after the debate has visibly stalled — no new challenges or rebuttals in several exchanges (one challenge plus one reply counts as one exchange) between any given pair — the lead sends that champion a "wrap up — send your done signal" message. The threshold is a judgment call: err toward patience in high-stakes comparisons, sooner when options are straightforward. Proceed once all done messages are received or the wrap-up has been sent to all remaining champions. Collect the full debate transcript: all champion arguments and inter-champion messages exchanged.

## Step 4 — Spawn synthesizer

Spawn a single subagent, on the highest-capability model available, with the topic and the debate transcript. Format the transcript grouped by champion (labelled with their option), separating the arguments they made, the challenges they sent, and the challenges they received with their rebuttals.

Synthesizer instructions: analyse the debate — which arguments held up, which were successfully challenged, and (when more than 2 options were compared) where consensus emerged; for exactly 2 options, omit consensus framing and instead note which side's case held up better — then deliver a recommendation. The recommendation may be conditional ("use X if Y, use Z if W").

## Step 5 — Present report

Return the synthesizer's report to the user as-is; the synthesizer chooses how to structure and label its sections.
