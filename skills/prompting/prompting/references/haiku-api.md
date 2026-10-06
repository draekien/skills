# Haiku 4.5 — API prompts

Snapshot: 2026-10-07. Model: Haiku 4.5 (`claude-haiku-4-5-20251001`, alias `claude-haiku-4-5`). The docs publish no prompting page for this model; these entries are the passages of the best-practices page and the migration guide that apply to it. Entries marked "inferred" are not stated for Haiku 4.5 by name. Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| BP | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` |

## Add when the behaviour matters

- **Reasoning with thinking off.** Ask it to think through the problem before answering and to put the final answer in `<answer>` tags for extraction. — BP § Leverage thinking & interleaved thinking capabilities
