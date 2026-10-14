# Reading guidance for the installed versions

Read the installed version's own guidance, record each rule it changes as one string in the discovery entry's `versionNotes` (or `checked: no changes`), and apply the changed rule in place of the SKILL.md one. Where you can dispatch work to a fresh context, give the reading to a subagent with the rule list and the installed versions.

## Router and Start

Router and Start publish skills inside their packages (`@tanstack/router-core`, `@tanstack/start-client-core`, `@tanstack/react-start`). The TanStack Intent CLI reads them from `node_modules`, so they match the installed version. Requires Node.js and network access to fetch the CLI.

```bash
npx @tanstack/intent@0.5.5 list --json
npx @tanstack/intent@0.5.5 load @tanstack/router-core#router-core/data-loading
```

Run both from the app root. From `list`, load every skill covering data loading, SSR, server functions, the execution model and middleware. `list` and `load` write nothing. Never run `intent install`: it edits `package.json` and `AGENTS.md`.

If `list` returns no skills for these packages, the installed versions predate them; if `npx` fails (offline, no registry access), the CLI is unavailable. Read the docs instead, as for Query below, from `docs/router/` and `docs/start/` in `TanStack/router`.

## Query

Query ships no Intent skills. Read `docs/framework/react/guides/` in `TanStack/query` at the installed version's git tag: `@tanstack/react-query@<version>` for recent releases, `v<version>` for older ones. Use whichever tag exists. If neither exists or the docs cannot be read, record the affected rules as `unverified for <version>` in `versionNotes` and tell the user.

Done when every rule in SKILL.md that uses a changed API has a `versionNotes` entry or is confirmed unchanged.
