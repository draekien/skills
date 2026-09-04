# skillsrc — module-design Keys

Configuration is stored in `.draekien/.skillsrc`, a JSON file shared across skills — each skill owns only its own top-level block.

## Keys Used by This Skill

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `specsDir` | string | `docs/designs` | Directory (relative to repo root) where design specs are written |

## Reading

Parse `.draekien/.skillsrc` as JSON. Read the `module-design` block only. If the file or block is absent, use the default above.

## Writing

When the user provides a custom output path: parse the file, merge `{ "module-design": { "specsDir": "<path>" } }`, and rewrite. If `.draekien/` does not yet exist, confirm its creation with the user before proceeding, then create it. Confirm any write with the user before executing. Never overwrite other skills' blocks.
