# .skillsrc Specification

## Location

`.draekien/.skillsrc` at the repository root. See [specs/draekien.md](draekien.md) for the directory convention.

## Format

JSON object. Top-level keys are skill names (matching each skill's `name` frontmatter field exactly). Values are objects of skill-defined key-value pairs.

```json
{
  "<skill-name>": {
    "<key>": "<value>"
  }
}
```

## Rules for Skills

**Reading:**
- Parse `.draekien/.skillsrc` as JSON.
- Read only the block matching the skill's own `name`. Never read or interpret another skill's block.
- If the file or the skill's block is absent, fall back to the skill's documented defaults — do not error.

**Writing:**
- Never overwrite the entire file. Always: parse existing JSON → merge the skill's block → rewrite.
- Preserve all other skills' blocks exactly.
- Confirm any write to `.skillsrc` with the user before executing.
- If `.draekien/` does not exist, follow the directory creation protocol in [specs/draekien.md](draekien.md) before writing.

**Key naming:**
- Use `camelCase` keys.
- Document every key the skill reads or writes in the skill's own reference file. Do not rely on undocumented keys.

## Example

```json
{
  "module-design": {
    "specsDir": "architecture/designs"
  },
  "another-skill": {
    "outputFormat": "markdown"
  }
}
```

## Registered Keys

Skills that use `.skillsrc` must register their keys here.

| Skill | Key | Type | Default | Description |
|-------|-----|------|---------|-------------|
| `module-design` | `specsDir` | string | `docs/designs` | Directory (relative to repo root) where design specs are written |
