# Skill Structure Rules

## Progressive Disclosure

Place content at the level where it is first needed, not where it is most convenient.

| Level | Location | What belongs here |
|-------|----------|-------------------|
| L2 (always loaded) | `SKILL.md` body | Complete workflow steps, decision logic, all info needed on first activation |
| L3 (loaded on demand) | `references/` | API schemas, data formats, lookup tables, verbose technical docs, domain-specific reference material unlikely needed every run |
| Template | `assets/` | Output templates the agent copies rather than invents, static config files, example inputs/outputs |

Link reference files from the body using relative paths:

```
See [references/schema.md](references/schema.md) for the full schema.
```

One level deep only — never reference a reference from a reference.

Target body under 500 lines. When content exceeds this, split into `references/`.

## Supporting Files

### `scripts/` — use when

- Task is deterministic; variation = bug
- Agent would re-derive complex logic each run
- Operation benefits from idempotency

**Script design rules (non-negotiable for agent compatibility):**

- No interactive prompts — must run fully unattended
- Structured stdout (data output) vs. stderr (diagnostic logs)
- Actionable error messages — tell agent how to self-correct
- Idempotent — safe to run twice
- Dry-run flag for destructive operations
- Meaningful exit codes (0 = success, non-zero = specific failure)
- Output size guards to avoid harness truncation

**Dependency approaches (in order of preference):**

1. One-off invocation with pinned version: `uvx some-tool@1.2.3` or `npx tool@version`
2. Self-contained script with PEP 723 inline deps (Python):
   ```python
   # /// script
   # dependencies = ["httpx==0.27.0", "rich==13.7.0"]
   # ///
   ```
3. Full documented dependency list if above insufficient

### `references/` — use when

- Docs verbose but not needed every activation
- Content is stable reference material (schemas, cheatsheets, domain specs)
- Loading every time wastes context

### `assets/` — use when

- Agent needs a concrete template to copy (not invent)
- Static config or example files are needed
