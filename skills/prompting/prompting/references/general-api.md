# General guidance — API prompts

Snapshot: 2026-10-07. Each entry ends with its source key and heading. `Measured on <model>` marks an entry the source states for that model only.

| Key | Source |
| --- | --- |
| BP | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` |

## Clarity and context

- For model identity in an app: `The assistant is Claude, created by Anthropic. The current model is <name>.` For model strings: name the default model and its exact ID. — BP § Model self-knowledge

## Output and formatting

- Replacing prefill: for preambles, "Respond directly without preamble"; for a continuation, move it into the user turn with the interrupted text quoted. — BP § Migrating away from prefilled responses
