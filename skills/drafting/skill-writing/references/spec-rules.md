# Agent Skills Spec — Validation Rules

Full checklist for validating a skill against the [Agent Skills open standard](https://agentskills.io/specification).

Rules marked `[AUTO]` are checked by `scripts/validate.py`. Rules marked `[LLM]` require judgment and must be reviewed manually.

Run automated checks first:
```
uv run scripts/validate.py <skill-dir>
```

Then work through the `[LLM]` rules below.

---

## Frontmatter

### `name` field
- `[AUTO]` Present and non-empty
- `[AUTO]` 1–64 characters
- `[AUTO]` Lowercase letters, numbers, and hyphens only (`a-z`, `0-9`, `-`)
- `[AUTO]` Does not start with a hyphen
- `[AUTO]` Does not end with a hyphen
- `[AUTO]` Does not contain consecutive hyphens (`--`)
- `[AUTO]` Matches the parent directory name exactly

### `description` field
- `[AUTO]` Present and non-empty
- `[AUTO]` 1–1024 characters
- `[LLM]` States what the skill does (not just what it is)
- `[LLM]` States when to use it (trigger conditions)
- `[LLM]` Uses imperative phrasing ("Extracts...", not "A skill that...")
- `[LLM]` Includes domain-specific keywords that match natural trigger phrases

### `compatibility` field (if present)
- `[AUTO]` 1–500 characters
- `[LLM]` Only included when the skill has specific environment requirements

### `metadata` field (if present)
- `[AUTO]` All values are strings
- `[LLM]` Key names are reasonably unique to avoid conflicts

### `allowed-tools` field (if present)
- `[AUTO]` Is a space-separated string (not a YAML list)
- `[LLM]` Tools listed are valid and no broader than the skill's stated purpose

## Directory structure

- `[AUTO]` `SKILL.md` is present at the skill root
- `[AUTO]` `name` matches parent directory name exactly
- `[AUTO]` All file references in the body use relative paths (not `/` or `http`)
- `[AUTO]` All linked files referenced in the body actually exist
- `[AUTO]` Reference files in `references/` do not link to other files (one level deep only)

## Body content

- `[AUTO]` Body is under 500 lines
- `[AUTO]` Body contains no model-specific terms (`claude`, `gpt-4`, `openai`, etc.)
- `[LLM]` Workflow steps are numbered sequentially
- `[LLM]` Decision trees are mapped explicitly (no ambiguous branching)
- `[LLM]` Consistent terminology — one term per concept throughout
- `[LLM]` Does not contain information the agent already knows (language syntax, common tools)
- `[LLM]` Verbose reference material has been moved to `references/`
- `[LLM]` Output templates have been moved to `assets/`

## Scripts (if present)

- `[AUTO]` Python: no `input()` calls (scripts must run unattended)
- `[AUTO]` Bash: no interactive `read VAR` commands
- `[AUTO]` Python PEP 723 dependencies are all version-pinned
- `[AUTO]` Network calls (`requests`, `httpx`, `curl`, etc.) are declared in `compatibility:`
- `[LLM]` Scripts are self-contained or clearly document all dependencies
- `[LLM]` Stdout carries data output; stderr carries diagnostic logs
- `[LLM]` Error messages tell the agent how to self-correct
- `[LLM]` Scripts are idempotent (safe to run twice)
- `[LLM]` Destructive operations have a `--dry-run` flag
- `[LLM]` Exit codes are meaningful (0 = success, non-zero = specific failure)

## Security

- `[LLM]` No instructions that could be overridden by malicious user input (prompt injection)
- `[LLM]` No instructions that cause the agent to send file contents to external endpoints (data exfiltration)
- `[LLM]` `allowed-tools` scope is no broader than the skill's stated purpose (no privilege escalation)
- `[LLM]` Script dependencies are from trusted, verifiable sources (supply chain)

## LLM-agnostic portability

- `[AUTO]` Body contains no model-specific terms (same check as body section above)
- `[LLM]` Platform-specific extensions are documented in `compatibility:` or a separate note, not in core instructions
- `[LLM]` Description trigger behaviour has been tested against example queries
