# Opus 5.5 — product prompts

Snapshot: 2026-10-07. Model: Opus 5.5 (`claude-opus-5-5`). Predecessor: Opus 5 — "the patterns in Prompting Claude Opus 5 remain a reasonable starting point"; entries taken from it are marked `(predecessor: Opus 5)`, and an Opus 5.5 entry wins where they disagree. Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| O55 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5` |
| PB | `https://claude.dev/blog/getting-the-most-out-of-opus-5-5/` |

## Add when the behaviour matters

- **Settled answers in a chat project.** "Once you have answered something, treat that answer as done. Focus on what I'm asking now, and don't go back over an earlier answer unless I ask about it or point out a problem with it." Leave it out where a later step can expose an earlier mistake; it may make the model less likely to point out an earlier mistake on its own. — PB § In a project, say when answers are settled; O55 § Thinking instructions in chat system prompts
- **Early stops, in a coding product.** "When a step doesn't need my input, keep going. Put status notes in the same message as your next action. Stop and ask only when you can't continue without me, or before anything destructive: deleting data, force-pushing, or changing anything outside this repository." For pair programming, ask instead for a one-line plan first and a short recap at the end. — PB § Tell it which stops you want
