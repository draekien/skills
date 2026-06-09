# Agent Skills Spec — Validation Rules

Full checklist for validating skill against [Agent Skills open standard](https://agentskills.io/specification).

`[AUTO]` rules checked by `scripts/validate.py`. `[LLM]` rules need human judgment.

Run automated checks first:

```
uv run scripts/validate.py <skill-dir>
```

Then work through `[LLM]` rules below.

---

## Frontmatter

### `name` field

- `[AUTO]` Present and non-empty
- `[AUTO]` 1–64 characters
- `[AUTO]` Lowercase letters, numbers, hyphens only (`a-z`, `0-9`, `-`)
- `[AUTO]` No leading hyphen
- `[AUTO]` No trailing hyphen
- `[AUTO]` No consecutive hyphens (`--`)
- `[AUTO]` Matches parent directory name exactly

### `description` field

- `[AUTO]` Present and non-empty
- `[AUTO]` 1–1024 characters
- `[LLM]` States what skill does (not just what it is)
- `[LLM]` States when to use it (trigger conditions)
- `[LLM]` Imperative phrasing ("Extracts...", not "A skill that...")
- `[LLM]` Domain-specific keywords matching natural trigger phrases

### `compatibility` field (if present)

- `[AUTO]` 1–500 characters
- `[LLM]` Only included when skill has specific environment requirements

### `metadata` field (if present)

- `[AUTO]` All values are strings
- `[LLM]` Key names reasonably unique to avoid conflicts

### `allowed-tools` field (if present)

- `[AUTO]` Space-separated string (not YAML list)
- `[LLM]` Tools listed valid and no broader than skill's stated purpose

### Frontmatter formatting

- `[AUTO]` No unknown or misspelled field names
- `[AUTO]` `name` and `description` plain strings (not YAML integers or booleans)
- `[AUTO]` No trailing whitespace on any frontmatter line
- `[AUTO]` No block scalar notation (`|` or `>`) in frontmatter values

## Directory structure

- `[AUTO]` `SKILL.md` present at skill root
- `[AUTO]` `name` matches parent directory name exactly
- `[AUTO]` All file references in body use relative paths (not `/` or `http`)
- `[AUTO]` All linked files referenced in body exist
- `[AUTO]` Reference files in `references/` don't link to other files (one level deep only)

## Body content

- `[AUTO]` Body under 500 lines
- `[AUTO]` Body contains no model-specific terms (`claude`, `gpt-4`, `openai`, etc.)
- `[LLM]` Workflow steps numbered sequentially
- `[LLM]` Decision trees mapped explicitly (no ambiguous branching)
- `[LLM]` Consistent terminology — one term per concept throughout
- `[LLM]` No info agent already knows (language syntax, common tools)
- `[LLM]` Verbose reference material moved to `references/`
- `[LLM]` Output templates moved to `assets/`
- `[LLM]` Specificity matches task fragility
- `[LLM]` No "When to use this skill" section in body — activation belongs in description
- `[LLM]` No narrative or session-dated examples
- `[LLM]` No references to mutable environment state that will drift as the skill is used

## Scripts (if present)

- `[AUTO]` Python: no `input()` calls (scripts must run unattended)
- `[AUTO]` Bash: no interactive `read VAR` commands
- `[AUTO]` Python PEP 723 dependencies all version-pinned
- `[AUTO]` Network calls (`requests`, `httpx`, `curl`, etc.) declared in `compatibility:`
- `[LLM]` Scripts self-contained or clearly document all dependencies
- `[LLM]` Stdout carries data output; stderr carries diagnostic logs
- `[LLM]` Error messages tell agent how to self-correct
- `[LLM]` Scripts idempotent (safe to run twice)
- `[LLM]` Destructive operations have `--dry-run` flag
- `[LLM]` Exit codes meaningful (0 = success, non-zero = specific failure)

## Security

- `[LLM]` No instructions overridable by malicious user input (prompt injection)
- `[LLM]` No instructions causing agent to send file contents to external endpoints (data exfiltration)
- `[LLM]` `allowed-tools` scope no broader than skill's stated purpose (no privilege escalation)
- `[LLM]` Script dependencies from trusted, verifiable sources (supply chain)

## LLM-agnostic portability

- `[AUTO]` Body contains no model-specific terms (same check as body section above)
- `[LLM]` Platform-specific extensions documented in `compatibility:` or separate note, not in core instructions
- `[LLM]` Description trigger behaviour tested against example queries
