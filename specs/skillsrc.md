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

- Use the skill's own `scripts/skillsrc.py get` to read config values (see [Script convention](#script-convention) below).
- If the file or the skill's block is absent, the script falls back to the skill's documented defaults — do not error.

**Writing:**

- Use the skill's own `scripts/skillsrc.py set <value>` to write config values.
- Always confirm any write with the user before executing the script.
- If `.draekien/` does not exist, follow the directory creation protocol in [specs/draekien.md](draekien.md) before running the script.

**Key naming:**

- Use `camelCase` keys.
- Document every key the skill reads or writes in the skill's own reference file. Do not rely on undocumented keys.

## Script Convention

Every skill that reads or writes `.skillsrc` must bundle `scripts/skillsrc.py` in its own `scripts/` directory. Each script is hardcoded to its own skill's section only — it never reads or writes another skill's block.

**Interface:**

```
uv run scripts/skillsrc.py --config <path-to-.skillsrc> get
uv run scripts/skillsrc.py --config <path-to-.skillsrc> set <value>
```

**Implementation rules:**

- `get`: read the skill's block, print the value; print the default if the file or key is absent; exit 0.
- `set`: parse existing JSON → merge only the skill's block → rewrite the file; exit 0.
- `dependencies = []` — stdlib only (`json`, `pathlib`, `argparse`).
- Exit codes: 0 success, 2 usage error.
- If the skill has more than one key, add one subcommand per key (e.g. `get specsDir`, `get outputFormat`).

See `skills/engineering/module-design/scripts/skillsrc.py` and `skills/engineering/get-specific/scripts/skillsrc.py` as reference implementations.

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
| `get-specific` | `dictionaryPath` | string | `.draekien/ubiquitous-language.yaml` | Path (relative to repo root) to the ubiquitous language YAML dictionary |
| `break-down-prd` | `outputDir` | string | `.draekien/break-down-prd` | Directory (relative to repo root) where PRD breakdowns are written; the skill appends `/<prd-slug>/` per breakdown |
| `skill-evals` | `outputDir` | string | `.draekien/skill-evals` | Directory (relative to repo root) where eval state is written; the skill appends `/<skill-name>/` per evaluated skill |
