# Fable 5.1 — API prompts

Snapshot: 2026-10-07. Model: Fable 5.1 (`claude-fable-5-1`); Mythos 5.1 shares this guidance. Predecessor: Fable 5 — "Your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes"; entries taken from its page are marked `(predecessor: Fable 5)`, and a Fable 5.1 entry wins where they disagree. Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| F51 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1` |
| F5 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5` |

## Remove from older prompts

- Remaining-token countdowns shown to the model; they trigger suggestions to start a new session or trim work. If a countdown must stay: "You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work." (predecessor: Fable 5) — F5 § Rare cases of context-budget concern

## Add when the behaviour matters

- **Hidden tool output.** When the application collapses tool output, tell the model, as a turn-scoped system message: "Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply." — F51 § Ask for user-facing progress updates
- **Batching.** In coding and computer-use loops it may issue implied independent calls one per turn. Append "First privately list what you need next; then request every item that doesn't depend on another's result in this one response." after each round of tool results, as a system message; leave earlier copies in place. — F51 § Batch independent tool calls in agent loops
- **Compaction summaries.** For client-side compaction — F51 § Tell the model what to preserve in compaction summaries:

  ```text
  Summarize the transcript inside <summary></summary> tags. Include relevant information in the summary such that this conversation will be continued by a new context window without needing to redo work or be reprovided with relevant constraints or context. Be sure to preserve: (1) any difficulties or problems that came up, and how they were handled or resolved; (2) any possibilities, options, or approaches that were raised, tried, or set aside, and why; (3) anything that was asked for, decided, agreed, ruled out, or established as a preference, constraint, or boundary — stated exactly; (4) exactly where things stand now — what has been covered, settled, or completed so far; (5) anything still open, unresolved, promised, or expected to happen next; (6) specific details that would be hard to reconstruct — names, numbers, dates, exact wording, links or references — kept exactly. Be complete on these even at the cost of length; keep everything else concise. Weight the two voices differently: keep what the user said, asked for, shared, or established carefully and close to their own words; your own explanations and reasoning can be condensed much further, to what they concluded or produced — as long as nothing in the six items above is dropped.
  ```

- **Send-to-user tool.** For long asynchronous agents, a `send_to_user` tool whose input is displayed verbatim, paired with: "Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning." Without the instruction it is rarely called. (predecessor: Fable 5) — F5 § Create a send-to-user tool

- **Long outputs**, when the model drafts a long deliverable in full in thinking and then writes it again (seen at `xhigh` and `max` effort): append this to the user message, with the request's real output limit in place of `[max_tokens]`. — F51 § Leave room for long outputs at xhigh and max effort

  ```text
  Everything produced in one reply, including any reasoning or drafting done before the reply, counts toward a single limit of about [max_tokens] tokens. If that limit is reached before the reply is finished, the person receives a cut-off response and has to start over. Composing an entire output or deliverable in full as reasoning and then again as a reply would double the length of the turn without improving the result, so don't do that.

  Instead, when the person has asked for a long or effort-intensive deliverable such as a multi-section document, a large table or dataset, or a complete code file, spend extra effort on understanding the request, checking the inputs the answer depends on, settling the structure and other difficult decisions, and otherwise using the reasoning space to reason and the output space to write an output. Usually it is not needed to draft an output multiple times.
  ```
