---
name: round-table
description: 'Assembles an adversarial agent team to compare competing options, approaches, or technologies. Champions debate via direct messaging — each builds a case and actively challenges the others — then a synthesizer subagent analyses the debate and delivers a recommendation. Use when comparing options or approaches, or when the user says "round-table X vs Y", "run a round-table on...", "round-table these options: A, B, C".'
compatibility: Requires Claude Code with agent teams enabled. Champions run on a fast mid-tier model (e.g. claude-sonnet-4-6); the synthesizer subagent runs on the highest-capability model available (e.g. claude-opus-4-7).
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

Create an agent team with one champion teammate per confirmed option.

Each champion receives:

- The debate topic
- Their assigned option
- The names of all other champions
- Instructions, in order:
  1. Research their option if needed (skip if sufficient context already exists).
  2. Build the strongest possible case for their assigned option.
  3. Send challenges via SendMessage to other champions whenever they find evidence that weakens a competing option, and respond to challenges directed at them.
  4. Treat this as a live scientific debate, not a one-shot argument — expect multiple rounds of challenge and rebuttal.
  5. Send a "done" message to the lead only after (1) they have sent all challenges they intend to send, and (2) they have received and responded to any challenges directed at them. Do not send "done" while awaiting a reply to an outstanding challenge.

## Step 3 — Wait for close signals

Wait until all champions send their "done" message to the lead. If a champion has not sent "done" within N rounds of inter-champion messaging (default 3 per pair), the lead sends a "wrap up — send your done signal" message; proceed once all done signals are received or the wrap-up has been sent to all remaining champions. Collect the full debate transcript: all champion arguments and inter-champion messages exchanged.

## Step 4 — Spawn synthesizer

Spawn a single subagent with the topic and the debate transcript. Format the transcript grouped by champion (labelled with their option), separating the arguments they made, the challenges they sent, and the challenges they received with their rebuttals.

Synthesizer instructions: analyse the debate — what arguments held up, what was successfully challenged, where consensus emerged — then deliver a recommendation. The recommendation may be conditional ("use X if Y, use Z if W").

## Step 5 — Present verdict

Return the synthesizer's report:

**Analysis:** what the debate revealed — which arguments held, which were undermined, and where consensus emerged.

**Recommendation:** clear conclusion, conditional if warranted.
