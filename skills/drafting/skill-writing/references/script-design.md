# Script Design Rules

Design rules and dependency approaches for scripts bundled with skills.

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
