# skillsrc — ddd-modular-monolith Keys

Configuration is stored in `.draekien/.skillsrc`, a JSON file shared across skills — each skill owns only its own top-level block.

## Keys Used by This Skill

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `architectureDir` | string | `docs/architecture` | Directory (relative to repo root) holding `module-map.md` and the per-module specs |
| `subagentModel` | string | empty | Model every `--runner subagent` round is dispatched to — any model name or alias the harness accepts, such as `sonnet`. Empty leaves the choice to the critique brief |

## Reading

Parse `.draekien/.skillsrc` as JSON. Read the `ddd-modular-monolith` block only. If the file, block or key is absent, use the defaults above.

## Writing

When the user provides a custom output path: parse the file, merge `{ "ddd-modular-monolith": { "architectureDir": "<path>" } }`, and rewrite. If `.draekien/` does not yet exist, confirm its creation with the user before proceeding, then create it. Confirm any write with the user before executing. Never overwrite other skills' blocks.

When the user names a default model for subagent rounds: merge `{ "ddd-modular-monolith": { "subagentModel": "<model>" } }` the same way, with the same confirmation.
