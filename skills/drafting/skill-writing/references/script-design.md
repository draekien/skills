# Script Design Rules

Design rules, referencing conventions, and dependency approaches for scripts bundled with skills.

## Referencing scripts from SKILL.md

List available scripts before first use so the agent knows they exist. Use relative paths from the skill directory root — both in the listing and in code block invocations.

**Listing pattern:**

~~~markdown
## Available scripts

- **`scripts/validate.py`** — Validates configuration files
- **`scripts/process.py`** — Processes input data
~~~

**Invocation pattern:**

~~~markdown
Run the validation script:
```bash
uv run scripts/validate.py <skill-dir>
```
~~~

The same relative-path convention applies inside `references/*.md` — execution paths in code blocks are always relative to the skill root.

## Design rules (non-negotiable for agent compatibility)

- No interactive prompts — must run fully unattended
- Structured stdout (data output) vs stderr (diagnostic logs)
- Prefer JSON, CSV, or TSV output over free-form text — composable with standard tools and pipelines
- Actionable error messages — tell agent how to self-correct
- Idempotent — safe to run twice
- Dry-run flag for destructive operations
- Meaningful exit codes (0 = success, non-zero = specific failure)
- Output size guards to avoid harness truncation

## Dependency approaches (in order of preference)

1. One-off invocation with pinned version: `uvx some-tool@1.2.3` or `npx tool@version`
2. Self-contained script with PEP 723 inline deps (Python): `# dependencies = ["httpx==0.27.0"]`
3. Full documented dependency list if above insufficient
