# Script Design Rules

Design rules, dependency approaches, and referencing patterns for commands and scripts bundled with skills.

## When a script earns its place

Script the deterministic floor of a task, never its decisions:

- **Script when variation is a bug** — the operation has one right answer (parsing, validation, conversion, scaffolding) and reliability demands every run take it. The signals surface in real execution traces: the agent re-derives the same logic each run, fumbles a long incantation, or produces inconsistent results across runs.
- **Keep judgment in prose** — where multiple approaches are valid, reasoning-carrying prose beats frozen code: a script cannot adapt when its assumptions don't hold, and the agent cannot see inside it to know why it did what it did. Encoding a whole workflow's sequence as a script is the workflow-scripting anti-pattern wearing an executable coat.

## Command or script

Execution warranted, there are two ways a skill puts it in the agent's hands:

- **One-off command** — an existing package already does the job: invoke it directly from the body via a runner that resolves dependencies at invocation time (`uvx`, `npx`, or the ecosystem's equivalent). Right for a tool plus a few flags.
- **Bundled script** — the logic is reusable, or the command is complex enough to be hard to get right on the first attempt: ship it tested in `scripts/`. The author debugs it once so no run pays that cost again.

## Design rules (non-negotiable for agent compatibility)

The agent reads a script's output to decide its next action — every rule below exists to make that decision reliable.

- **No interactive prompts** — agents run in non-interactive shells; a TTY prompt hangs the run indefinitely. Accept all input via flags, environment variables, or stdin.
- **Structured stdout, diagnostics to stderr** — data the agent parses goes to stdout as JSON, CSV, or TSV (unambiguous field boundaries, composable with standard pipeline tools); progress and warnings go to stderr so they never contaminate the parseable stream.
- **Actionable error messages** — the message directly shapes the agent's next attempt: say what went wrong, what was expected, and what to try. An opaque "invalid input" wastes a turn.
- **`--help` is the interface contract** — a brief description, the flags, an example or two, and what each exit code means. It is how the agent learns the script; keep it short, because the output lands in the agent's context window.
- **Reject ambiguous input** — a closed set of accepted values plus a clear error beats guessing what the caller meant.
- **Idempotent** — agents retry: "create if not exists" beats "create and fail on duplicate".
- **Dry-run flag for destructive operations** — and weigh whether the risk warrants an explicit confirmation flag rather than acting by default.
- **Meaningful exit codes** — 0 for success, distinct non-zero codes per failure type.
- **Output size guards** — harnesses truncate large tool output, silently losing the tail. Default to a summary or a bounded limit, with a pagination flag to request more; for output too large to page, take an `--output <file>` argument instead of streaming to stdout.

## Dependencies

In order of preference:

1. One-off invocation with pinned version: `uvx some-tool@1.2.3` or `npx tool@version`
2. Self-contained script with PEP 723 inline deps (Python): `# dependencies = ["httpx==0.27.0"]`
3. Full documented dependency list if the above are insufficient

Always pin versions — an unpinned tool drifts under the skill. State any prerequisite the runner itself needs ("requires Node 18+") in the body rather than assuming the environment provides it; where the harness supports a compatibility field in frontmatter, set it to match.

## Referencing scripts

When a skill ships any bundled scripts, declare them all in an "Available scripts" listing in the body before first use, so the agent knows they exist without stumbling on them. Use relative paths from the skill directory root, both in listings and in code block invocations.

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
