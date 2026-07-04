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
- `[LLM]` If model-invocable (default, or `disable-model-invocation` absent/false): domain-specific keywords matching natural trigger phrases, dense enough for activation matching
- `[LLM]` If user-invocable only (`disable-model-invocation: true`): plain, scannable language for a human choosing from a command list, not trigger-phrase density — reads like a CLI `--help` one-liner

### `compatibility` field (if present)

- `[AUTO]` 1–500 characters
- `[LLM]` Only included when skill has specific environment requirements

### `metadata` field (if present)

- `[AUTO]` All values are strings
- `[LLM]` Key names reasonably unique to avoid conflicts

### `allowed-tools` field (if present)

- `[AUTO]` Must be a space-separated string, not a YAML list. `allowed-tools` is a shared open-standard field other harnesses honour only as a string, so the list form (valid in Claude Code) fails rather than warns
- `[LLM]` Tools listed valid and no broader than skill's stated purpose

### `argument-hint` field

- `[LLM]` Present whenever the skill body expects the invoker to supply arguments — this harness-specific extension warns rather than fails on harnesses that don't define it, so it costs nothing to include. Most valuable when the body branches on what's supplied (a term looked up versus a command run versus no argument at all); the hint is the only place telling the invoker which input forms exist and what each triggers
- `[AUTO]` Must be a quoted string, e.g. `argument-hint: "[issue-number]"` — the unquoted form (`argument-hint: [issue-number]`) parses as a YAML list, not the free-text string every harness expects
- `[LLM]` Free text only (e.g. `"[issue-number]"`, or `"[write|audit] [target]"` / `"[cmdA|cmdB · cmdC|cmdD] [target]"` for a skill with a fixed set of named modes or sub-commands — even just two); not used to encode a structured/typed argument schema — that capability isn't broadly supported and isn't worth designing a skill around
- `[LLM]` When the skill branches on a fixed set of modes, the hint names them pipe-separated rather than spelling the branch out as a descriptive phrase — `"[write|audit] [target]"`, not `"[code to write tests for, or existing tests to audit]"`

### Frontmatter formatting

- `[AUTO]` No unknown or misspelled field names. Open-standard fields (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) pass silently. Harness-specific extensions pass with a non-blocking portability warning rather than failing — a skill using one still validates, but authors should confirm which harnesses recognize the field before relying on it. Anything else fails as a likely typo.
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
- `[LLM]` Scripts satisfy every design rule in script-design.md (self-contained or documented dependencies, structured stdout/stderr, actionable errors, idempotent, dry-run flag on destructive operations, meaningful exit codes)

## Security

- `[LLM]` No instructions overridable by malicious user input (prompt injection)
- `[LLM]` No instructions causing agent to send file contents to external endpoints (data exfiltration)
- `[LLM]` `allowed-tools` scope no broader than skill's stated purpose (no privilege escalation)
- `[LLM]` Script dependencies from trusted, verifiable sources (supply chain)

## LLM-agnostic portability

- `[LLM]` Platform-specific extensions documented in `compatibility:` or separate note, not in core instructions
- `[LLM]` Description trigger behaviour tested against example queries
