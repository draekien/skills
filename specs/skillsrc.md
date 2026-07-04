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

- Use the skill's own `scripts/skillsrc.py --skill <skill-name> get <key>` to read config values (see [Script convention](#script-convention) below).
- If the file or the skill's block is absent, the script falls back to the skill's documented defaults — do not error.

**Writing:**

- Use the skill's own `scripts/skillsrc.py --skill <skill-name> set <key> <value>` to write config values.
- Always confirm any write with the user before executing the script.
- If `.draekien/` does not exist, follow the directory creation protocol in [specs/draekien.md](draekien.md) before running the script.

**Key naming:**

- Use `camelCase` keys.
- Document every key the skill reads or writes in the skill's own reference file. Do not rely on undocumented keys.

## Script Convention

`scripts/skillsrc.py` is implemented once, at [specs/skillsrc.py](skillsrc.py), and every skill that reads or writes `.skillsrc` bundles it as a symlink at `scripts/skillsrc.py` inside its own skill directory — not a copy. The script is generic: it takes the skill name and key as arguments rather than hardcoding them, so one file serves every skill.

**Interface:**

```
uv run scripts/skillsrc.py --config <path-to-.skillsrc> --skill <skill-name> get <key> [--default <value>]
uv run scripts/skillsrc.py --config <path-to-.skillsrc> --skill <skill-name> set <key> <value>
```

**Implementation rules (in [specs/skillsrc.py](skillsrc.py)):**

- `get`: read the named skill's block, print the key's value; print `--default` (or `""` if omitted) if the file or key is absent; exit 0.
- `set`: parse existing JSON → merge only the named skill's block → rewrite the file; exit 0.
- `dependencies = []` — stdlib only (`json`, `pathlib`, `argparse`).
- Exit codes: 0 success, 2 usage error, 3 config file unreadable or not valid JSON.

**Adding a new skill:**

1. Symlink the script: from the skill's `scripts/` directory, create `skillsrc.py` as a relative symlink to `specs/skillsrc.py`.
2. Requires `core.symlinks=true` in the git config (`git config core.symlinks true` — needed once per clone on Windows, otherwise git checks the symlink out as a plain text file containing the path).
3. Invoke with `--skill <skill-name>` and the key documented in [Registered Keys](#registered-keys) below.

See `skills/engineering/module-design/scripts/skillsrc.py` and `skills/engineering/with-ubiquitous-language/scripts/skillsrc.py` as reference symlinks.

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
| `with-ubiquitous-language` | `dictionaryPath` | string | `.draekien/ubiquitous-language.yaml` | Path (relative to repo root) to the ubiquitous language YAML dictionary |
| `break-down-prd` | `outputDir` | string | `.draekien/break-down-prd` | Directory (relative to repo root) where PRD breakdowns are written; the skill appends `/<prd-slug>/` per breakdown |
| `skill-evals` | `outputDir` | string | `.draekien/skill-evals` | Directory (relative to repo root) where eval state is written; the skill appends `/<skill-name>/` per evaluated skill |
| `transcribe-video` | `whisperModel` | string | `base` | Preferred Whisper model size (`tiny`, `base`, `small`, `medium`, `large`) |
