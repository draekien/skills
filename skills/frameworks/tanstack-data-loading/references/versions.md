# Resolving API lookups for the installed versions

Resolve every API lookup in SKILL.md from the installed version's own documentation, never from memory, and record each as one `versionNotes` string: `<lookup>: <installed API and behaviour>`. Where the installed version has nothing for a lookup, record that (`mutation scope: none in 5.20.0`) so the rule's fallback applies. Where you can dispatch work to a fresh context, give the reading to a subagent with the lookup table and the installed versions.

## Router and Start

Router and Start publish skills inside their packages (`@tanstack/router-core`, `@tanstack/start-client-core`, `@tanstack/react-start`). The TanStack Intent CLI reads them from `node_modules`, so they match the installed version. Requires Node.js and network access to fetch the CLI.

```bash
npx @tanstack/intent@0.5.5 list --json
npx @tanstack/intent@0.5.5 load @tanstack/router-core#router-core/data-loading
```

Run both from the app root. From `list`, load every skill covering data loading, SSR, server functions, the execution model and middleware. `list` and `load` write nothing. Never run `intent install`: it edits `package.json` and `AGENTS.md`.

If `list` returns no skills for these packages, or a lookup is not answered by them, read the docs index pages below. If `npx` fails (offline, no registry access), the CLI is unavailable; read the docs index pages instead.

## Docs at the installed version

Read docs from the repository at the git tag for the installed version: `@tanstack/<package>@<version>` (`@tanstack/react-query@<version>` in `TanStack/query`; `@tanstack/react-router@<version>` or `@tanstack/react-start@<version>` in `TanStack/router`). Older releases are tagged `v<version>`; use whichever tag exists. If neither exists or the docs cannot be read, record the lookup as `unverified for <version>` and tell the user.

## Docs index

| Lookup | Repository | Path |
| --- | --- | --- |
| awaited fetch, background prefetch, deprecated reads | `TanStack/query` | `docs/framework/react/guides/prefetching.md`, `docs/framework/react/reference/classes/QueryClient.md`, `docs/framework/react/guides/caching.md` |
| awaited fetch, background prefetch (router side) | `TanStack/router` | `docs/router/guide/external-data-loading.md`, `docs/router/integrations/query.md` |
| SSR query integration | `TanStack/router` | `docs/router/integrations/query.md`, `docs/start/framework/react/guide/tanstack-query.md` |
| data-only SSR | `TanStack/router` | `docs/start/framework/react/guide/selective-ssr.md` |
| section boundary | `TanStack/router` | `docs/start/framework/react/guide/error-boundaries.md`, `docs/router/guide/data-loading.md` |
| section boundary (Query side), suspense batch | `TanStack/query` | `docs/framework/react/guides/suspense.md`, `docs/framework/react/reference/functions/useSuspenseQueries.md` |
| pending options | `TanStack/router` | `docs/router/guide/data-loading.md`, `docs/router/api/router/RouterOptionsType.md` |
| mutation scope | `TanStack/query` | `docs/framework/react/guides/mutations.md`, `docs/framework/react/reference/type-aliases/MutationScope.md` |
| input validator | `TanStack/router` | `docs/start/framework/react/guide/server-functions.md` |
| server-only files | `TanStack/router` | `docs/start/framework/react/guide/server-functions.md`, `docs/start/framework/react/guide/import-protection.md`, `docs/start/framework/react/guide/execution-model.md` |

Where a path no longer exists at the installed tag, list the `docs/` tree at that tag and read the page whose title covers the lookup.

Done when every API lookup in SKILL.md has a `versionNotes` entry naming the installed API, stating the installed version has none, or marked `unverified for <version>`.
