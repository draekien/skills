# Sonnet 5.5 — API prompts

Snapshot: 2026-10-07. Model: Sonnet 5.5 (`claude-sonnet-5-5`). Predecessor: Sonnet 5 — "the patterns in Prompting Claude Sonnet 5 remain a reasonable starting point"; entries taken from it are marked `(predecessor: Sonnet 5)`, and a Sonnet 5.5 entry wins where they disagree. Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| S55 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5` |
| PB | `https://claude.dev/blog/building-with-claude-sonnet-5-5/` |

## Remove from older prompts

- Token or budget countdowns appended after tool results in interactive sessions: they make the model treat real user messages as injections. — S55 § Mid-turn user messages

## Add when the behaviour matters

- **When to use a tool**, for a tool the application used to force: the model can now answer without calling it, so say in the system prompt when to use it. — PB § 2. Replace forced tool_choice with auto plus strict tools
- **Quiet-turn reminder**, appended after the latest tool results as a system message when several tool-calling steps in a row go quiet: "The user hasn't heard from you in a while — say in a few words what you're doing, then continue." — S55 § User-facing progress updates
- **Mid-turn messages.** Put user input that arrives mid-turn as text after the last tool result, not inside one, and keep application notices in a separate system message after the user's words. — S55 § Mid-turn user messages
- **Reasoning with JSON output.** End the system prompt with "Think the problem through before you answer." — S55 § Reasoning tasks with JSON output
