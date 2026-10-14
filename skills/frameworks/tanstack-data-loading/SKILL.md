---
name: tanstack-data-loading
description: Writes and audits data loading in a TanStack Start and TanStack Query app, removing request waterfalls and wasted requests from route loaders, suspense queries, mutations and server functions. Use when writing or reviewing a loader, useSuspenseQuery, useMutation or createServerFn, when a TanStack route loads slowly, fetches the same data twice or a save stays pending, or when the user says "audit data loading", "find waterfalls". Not for bundle size, HTTP caching, or apps without TanStack Query.
argument-hint: "[audit|refresh] [--fix] [path]"
---

# TanStack data loading

The first argument selects the mode. With no mode argument, infer it: a request to audit, find waterfalls or review existing code is `audit`; a request to rediscover or bust the cache is `refresh`; anything else is writing.

- `audit [--fix] [path]` — read [references/audit.md](references/audit.md) before starting, and run it over `path`.
- `refresh [path]` — rerun [Discovery](#discovery) for the app containing `path`, write the result, and stop.
- Writing — apply the rules below to the code being written or reviewed, within `path` if given.

Every mode starts with Discovery. The rules branch on what it records: if you guess the backend shape, you apply the wrong server function rules and the wrong write rules.

## Available scripts

- **`scripts/discovery.py`** — `read` and `write` the discovery cache at `<repo-root>/.draekien/tanstack-data-loading/discovery.json`, one discovery entry per app root; `versions` prints the installed `@tanstack` versions. `--help` lists the exit codes.

## Discovery

**App root.** The nearest ancestor of `path` (or of the current directory) whose `package.json` depends on `@tanstack/react-start`. If none matches, or the task spans several apps, ask the user which app.

**Read.** Run the script from this skill's directory, passing the app root relative to the repo root (`.` for a single-package repo):

```bash
uv run scripts/discovery.py read --app apps/web --repo <repo-root>
```

| Exit | Meaning | Next |
| --- | --- | --- |
| 0 | Fresh discovery entry printed | Use it, and apply its `versionNotes` in place of the rules they name. In `refresh`, discover and write anyway. |
| 4 | No discovery entry | Discover and write. |
| 5 | Older than the script's maximum age, or an installed `@tanstack` version changed | Discover and write. |
| 3 | Cache file or an installed package manifest unreadable | Read stderr. For the cache file, tell the user and delete it only after they agree, since it holds every app's discovery entry. For a manifest, ask the user to reinstall dependencies. |
| 2 | Usage error | Read stderr, correct the call, rerun. |

**Discover.** Find each field from the code:

| Field | Values | How to find it |
| --- | --- | --- |
| `backend` | `database`, `service`, `both` | Read the `createServerFn` handlers. `database`: they query a database client directly. `service`: they call another service over HTTP. `both`: some do each. |
| `pendingUi` | `route-level`, `per-section` | `route-level` when the router sets `defaultPendingComponent`. Otherwise ask the user whether they want a route-level pending component or Suspense sections only; with no user available, record `per-section` and say so. |
| `verify` | list of commands | The repo's lint, typecheck and test commands from `package.json` `scripts`. |
| `versionNotes` | list of strings | Run `uv run scripts/discovery.py versions --app <app-root> --repo <repo-root>` and compare against [Versions](#versions). When it sends you to [references/versions.md](references/versions.md), record its findings, or `checked: no changes` when there are none. Otherwise empty. If `versions` prints `{}`, ask the user to install dependencies before continuing. |

**Write.** The script adds `discoveredAt` and the installed `versions`, and rejects unknown values:

```bash
uv run scripts/discovery.py write --app apps/web --repo <repo-root> <<'EOF'
{"backend": "database", "pendingUi": "per-section", "verify": ["pnpm check", "pnpm typecheck", "pnpm test"], "versionNotes": []}
EOF
```

**First write in a repo.** Exit 6 means `.draekien/` is missing: ask the user before creating it. When `.draekien/tanstack-data-loading/discovery.json` does not exist yet, ask whether to add `.draekien/tanstack-data-loading/` to `.gitignore`; the discovery entries hold one developer's local discovery. If the user declines `.draekien/`, keep the discovered fields for this task only and say the discovery cache was not written.

Discovery is done when `read` or `write` exits 0 for the app, or when the user declined the cache and every field is known.

**Backend rules.** Before writing or auditing any server function, mutation or write path, read the reference for `backend`:

- `database` — [references/backend-database.md](references/backend-database.md).
- `service` — [references/backend-service.md](references/backend-service.md).
- `both` — read both. Apply each to the server functions whose handlers match it; a handler that does both applies each reference to its own part.

## Versions

Rules were checked against `@tanstack/react-query` 5.104.2, `@tanstack/react-router` 1.170.44 and `@tanstack/react-start` 1.169.1. Before applying a rule that uses an API below, compare the installed versions (the discovery entry's `versions`, or the `versions` command) to the minimum and use the substitute when the installed version is lower:

| Rule uses | Needs | Below the minimum |
| --- | --- | --- |
| `queryClient.query`, `queryClient.infiniteQuery` | `@tanstack/react-query` 5.102.0 | `fetchQuery`, `prefetchQuery`, `ensureQueryData` and their infinite variants, which are not deprecated there |
| `staleTime: "static"` | `@tanstack/react-query` 5.79.0 | `staleTime: Infinity` |
| `import { noop } from "@tanstack/react-query"` | `@tanstack/react-query` 5.76.0 | `.catch(() => {})` |
| mutation `scope: { id }` | `@tanstack/react-query` 5.32.0 | disable the trigger while `isPending` |
| `createServerFn().validator(...)` | `@tanstack/react-start` 1.168.25 | `.inputValidator(...)`; versions from 1.169.0 accept only `.validator(...)` |
| `*.server.ts` blocked from client imports | `@tanstack/react-start` 1.166.8 | the suffix is a naming convention; nothing blocks the import |

When an installed major version is newer than the checked one, or an API a rule uses is missing from the installed types, and the discovery entry has no `versionNotes`, read [references/versions.md](references/versions.md) before applying any rule.

## Loaders

Scope: the `loader` option of every file route under the app root.

A read is **critical** when the route must not render without it or must render something else when it fails: the main content, existence (404), authorization (403), a redirect, a limit gate, form defaults. Every other read is **unawaited**.

- Critical read: `await context.queryClient.query(options)`. Awaiting it in the loader sends a 404 or 403 to `notFoundComponent` or `errorComponent` before render; let the error reach them, or throw `notFound()`.
- Unawaited read, including hidden variants such as a toggle's second period: `void context.queryClient.query(options).catch(noop)`. Without `.catch(noop)` the rejection is unhandled on the server; the component's `useSuspenseQuery` still rethrows the error to its boundary.
- Start every unawaited read before the first `await`. A read started after an `await` is a waterfall.
- Independent critical reads: one `await Promise.all([...])`.

  ```ts
  ✗ await context.queryClient.query(orderQueryOptions(id))
    await context.queryClient.query(customerQueryOptions(customerId))

  ✓ await Promise.all([
      context.queryClient.query(orderQueryOptions(id)),
      context.queryClient.query(customerQueryOptions(customerId)),
    ])
  ```

- A read `b` that needs read `a`'s result is a waterfall that cannot be removed:

  | `a` | `b` | Loader |
  | --- | --- | --- |
  | critical | critical | `const x = await query(a)`, then `await query(b(x))` |
  | critical | unawaited | `const x = await query(a)`, then `void query(b(x)).catch(noop)`: the one unawaited read started after an `await` |
  | unawaited | unawaited | `void query(a).then((x) => query(b(x))).catch(noop)`, started before the first `await` |

- The loader and the component use the same `queryOptions` object. A different key in the component fetches the data a second time.
- A route a signed-out visitor can open starts reads that require a session only in its signed-in branch. Otherwise every signed-out visit fires calls that throw.
- Replace deprecated `QueryClient` methods:

  | Deprecated | Replacement |
  | --- | --- |
  | `fetchQuery(options)` | `query(options)` |
  | `prefetchQuery(options)` | `void query(options).catch(noop)` |
  | `ensureQueryData(options)` | `query({ ...options, staleTime: "static" })`; if a mutation invalidates the key, `staleTime: Infinity` instead, because `invalidateQueries` never refetches a `"static"` query |
  | `fetchInfiniteQuery(options)` | `infiniteQuery(options)` |
  | `prefetchInfiniteQuery(options)` | `void infiniteQuery(options).catch(noop)` |
  | `ensureInfiniteQueryData(options)` | `infiniteQuery(...)` with the same `staleTime` choice as `ensureQueryData` |

- Do not defer reads to scroll or interaction, and do not add hover prefetching beyond the router's `defaultPreload: "intent"`. An unawaited read already streams without blocking the page; deferring it adds a request after render, and no TanStack doc defines how deferral behaves with `useSuspenseQuery`.

## Streaming and SSR

Scope: the router file and every route's `ssr` option.

- The rules here hold only when the router file calls `setupRouterSsrQueryIntegration` from `@tanstack/react-router-ssr-query`. If it does not, report that as the first finding.
- An unawaited read runs on the server and streams to the client without blocking the server response. A critical read blocks the response until it resolves.
- `useSuspenseQuery` and loader reads run on the server. `useQuery` does not; its data loads after hydration, so a route component that reads with `useQuery` is a waterfall.
- `ssr: "data-only"` runs `beforeLoad` and `loader` on the server and renders the component only on the client. Do not rely on unawaited reads streaming under `ssr: "data-only"`, and do not recommend it as a fix; no official doc states the behaviour. Check it in the running app when the task depends on it.
- Do not configure route code splitting: Start always enables it, and the loader stays in the main chunk.

## Components

Scope: components that read query data with suspense.

- Two or more suspense queries in one component: one `useSuspenseQueries` call. Separate `useSuspenseQuery` calls in one component are a waterfall: the second starts after the first resolves.

  ```tsx
  ✗ const { data: order } = useSuspenseQuery(orderQueryOptions(id))
    const { data: notes } = useSuspenseQuery(notesQueryOptions(id))

  ✓ const [{ data: order }, { data: notes }] = useSuspenseQueries({
      queries: [orderQueryOptions(id), notesQueryOptions(id)],
    })
  ```

- A child that suspends on a query its route could know about: start that read in the route loader. Otherwise the child's request starts only after the parent renders.
- Each unawaited read renders inside its own **Suspense section**: `<CatchBoundary getResetKey={...} errorComponent={...}>` from `@tanstack/react-router` around `<React.Suspense fallback={...}>`, inside `QueryErrorResetBoundary` where the error UI offers a retry. The rest of the page renders while the section streams, and its error stays inside it. A critical read needs no Suspense section.
- A query key that changes on the same route (search param, tab, page, period): make the change inside `React.startTransition`. `useSuspenseQuery` has no `placeholderData`; without the transition, React replaces the content with the fallback.
- `pendingUi: route-level`: the router sets `defaultPendingComponent`, rendered inside the app's shell layout. It renders after `defaultPendingMs` (default 1000) and stays at least `defaultPendingMinMs` (default 500). `pendingUi: per-section`: add no `defaultPendingComponent`; if the user chose this while the router sets one, leave it until they ask for its removal.

## Mutations

Scope: every `useMutation`.

- The server function returns the saved entity. `onSuccess` writes it with `queryClient.setQueryData(key, saved)`.
- `onSuccess` invalidates only keys derived from the change (lists, counts, totals) and does not await the invalidation. A promise returned or awaited in `onSuccess` keeps `isPending` true until every invalidated query has refetched.

  ```ts
  ✗ onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: orderKeys.all })
    }

  ✓ onSuccess: (saved) => {
      queryClient.setQueryData(orderKeys.detail(saved.id), saved)
      void queryClient.invalidateQueries({ queryKey: orderKeys.lists() })
    }
  ```

- Never invalidate the key just written; invalidation refetches it. To invalidate a prefix that contains it, skip the written key with a `predicate`:

  ```ts
  void queryClient.invalidateQueries({
    queryKey: orderKeys.all,
    predicate: (query) =>
      query.queryKey.length !== written.length ||
      query.queryKey.some((part, index) => part !== written[index]),
  })
  ```

- Saves to one entity that can overlap (autosave, rapid toggles): set `scope: { id }` to a string naming the entity, such as `` `order-${orderId}` ``. Mutations with the same `scope.id` run one at a time in call order. A refetch after each save does not fix ordering: the responses can still arrive out of order.
- A mutation that changes which data the user may see (switching account or workspace) awaits its invalidation, so the next screen never renders with the previous account's data. Every other mutation follows the rule above.

## Server functions

Scope: every `createServerFn`.

- Put `createServerFn` exports in `*.functions.ts`. Client code may import them; the build replaces each handler with a request stub. Server-only helpers go in `*.server.ts`, which import protection blocks from client code.
- Validate input: `.validator(z.object({ ... }))`.
- Each call from the client is one HTTP request with a fixed cost: the request, plus every middleware it runs. Start neither batches nor deduplicates calls: `Promise.all` over three server functions sends three concurrent requests, and two identical calls send two. Deduplicate identical reads through the query cache by calling the server function only from a `queryFn`.
- Do not merge every read on a page into one server function. The page then waits for its slowest part, Suspense sections stop streaming separately, and every mutation refetches all of it.
- Middleware runs on every call to every server function that uses it. Shared middleware computes only what every one of those functions reads; a value only some read goes in its own middleware.
- Statements sent on one database connection, including every statement in one transaction, run one at a time. `Promise.all` over them saves no time; reduce the number of statements instead.
- Apply the backend reference named under Discovery, "Backend rules", to every server function.

## Gotchas

- `useSuspenseQueries` does not accept infinite queries. An infinite query in the same component still starts after the others resolve; start it in the loader.
- After converting to `useSuspenseQueries`, every test mock of `@tanstack/react-query` must export `useSuspenseQueries`.
- `toBe` on cached rows fails: structural sharing returns an equal copy, not the same object. Use `toEqual`.
- Once a loader awaits a read, a 404 from it right after a write (a backend that updates its read model asynchronously) shows the route's error component instead of an error inside a Suspense section.
