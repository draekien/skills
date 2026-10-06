# Haiku 4.5

Snapshot: 2026-10-07. Model: Haiku 4.5 (`claude-haiku-4-5-20251001`, alias `claude-haiku-4-5`). The docs publish no prompting page for this model; these entries are the passages of the best-practices page and the migration guide that apply to it. Entries marked "inferred" are not stated for Haiku 4.5 by name. Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| BP | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` |
| HM | `https://platform.claude.com/docs/en/models/haiku-4-5/migration-guide` |

## Defaults

- Communicates in the more concise, direct style of the 4-generation models. — HM § Breaking changes
- Has context awareness: it tracks its remaining context window during a conversation. — BP § Context awareness and multiwindow workflows

## Remove from older prompts

- Prompts tuned for Haiku 3.x: review them against the best practices for the more concise 4-generation style. — HM § Breaking changes

## Add when the behaviour matters

- **Context limits**, when the harness compacts context or lets the model save state to files — otherwise it may wrap up early as the limit nears: "Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully, even if the end of your budget is approaching. Never artificially stop any task early regardless of the context remaining." — BP § Context awareness and multiwindow workflows
