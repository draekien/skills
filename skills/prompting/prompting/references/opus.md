# Opus 5.5

Snapshot: 2026-10-07. Model: Opus 5.5 (`claude-opus-5-5`). Predecessor: Opus 5 — "the patterns in Prompting Claude Opus 5 remain a reasonable starting point"; entries taken from it are marked `(predecessor: Opus 5)`, and an Opus 5.5 entry wins where they disagree. Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| O55 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5` |
| O5 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5` |
| BP | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` |
| PB | `https://claude.dev/blog/getting-the-most-out-of-opus-5-5/` |

## Defaults

- Thinking is always on and the model decides how much. — O55 § Prompts written for thinking disabled; BP § Leverage thinking & interleaved thinking capabilities
- Strongest on multistep agentic coding and code review, knowledge work with large inputs, and charts, diagrams, and screenshots without extra tooling. Its progress reports and summaries say plainly what it did, found, and needs. — O55 § Capabilities relevant to prompting
- Gets to work quickly on loosely specified tasks. — O55 § Explore context in multi-app workflows

## Remove from older prompts

- "Think carefully", "think step by step", and similar lines. The model already thinks before every reply; removing such a line in a chat product made replies start sooner with no clear quality loss. For a quick answer, say "Answer directly." — O55 § Thinking instructions in chat system prompts; PB § Stop telling it to "think hard"
- Instructions to write out reasoning in the response. They invite `reasoning_extraction` declines. Ask for a short explanation instead — "Explain why you chose this approach in three sentences.". — O55 § Safeguard refusals; PB § Don't ask it to show its reasoning in the reply
- "Avoid a generic AI look" for design work: it swaps one default style for another. Replace with named patterns (next section). — O55 § Frontend design defaults
- Verification instructions ("include a final verification step", "use a subagent to verify") and re-check instructions ("double-check your answer") cause over-verification. (predecessor: Opus 5) — O5 § Task scope and over-verification; O5 § Self-correction
- Review filters such as "only report high-severity issues" or "be conservative" in a finding stage that feeds a separate filter: they are followed literally and cut recall; ask for everything and filter in the later pass. (predecessor: Opus 5) For a single-pass review that gates a merge, state the bar concretely instead: "List only problems you'd block the merge for. For each one, give the file and line, why it's wrong, and how to show it fails." — O5 § Capability improvements; PB § Ask it to review the code

## Add when the behaviour matters

- **Finish line.** Give the whole task in one message, name what "done" means, and say when to stop and ask: "Done means: every endpoint uses the new client, the old client is deleted, and the test suite passes. Stop and ask me only if a test fails for a reason you can't explain." — PB § Say what "done" looks like, then let it run
- **Progress at set points.** A system-prompt line asking for a one-line statement of intent before the first tool call and a short recap at the end; most useful with a human in the loop. — O55 § User-facing progress updates
- **Multi-app context.** "Before taking any action, explore broadly with tool calls: list and open the emails, documents, spreadsheet tabs and records across the available apps that could be relevant to this task, including ones the task does not explicitly mention, and use what you find." Keep untrusted content out of the searched records. — O55 § Explore context in multi-app workflows
- **Design.** Name the patterns to avoid: "Do not use a cream or off-white background, italic accent words in headlines, numbered "01/02/03" section labels, monospace labels, or pill-shaped buttons." Extend the list with whatever the next result defaults to. — O55 § Frontend design defaults; PB § For design work, name the styles you don't want
- **Large work.** "Give each service to its own subagent. When a subagent reports back, check its evidence before you accept it." and a task list kept in a file the model ticks off. — PB § Ask it to split big work across subagents; PB § Keep the task list in a file
- **Unconfirmed claims.** "Mark anything you couldn't confirm, and say where you looked." — PB § Ask it to mark what it couldn't confirm
- **Response length.** Effort changes thinking, not visible length; prompt for length. "Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested." In a long system prompt, add `<tone_preference>Keep outputs reasonably concise.</tone_preference>` near the end. (predecessor: Opus 5) — O5 § Response length and verbosity
- **Document length.** "Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate." (predecessor: Opus 5) — O5 § Written deliverable length
- **Scope.** For narrow tasks: "Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked." (predecessor: Opus 5) — O5 § Task scope and over-verification
- **Subagent spawning.** "Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low." (predecessor: Opus 5) — O5 § Controlling subagent spawning
- **Correction narration.** "Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it." (predecessor: Opus 5) — O5 § Self-correction
