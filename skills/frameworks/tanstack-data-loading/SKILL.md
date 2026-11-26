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

Every mode starts with Discovery. The rules branch on what it records: if you guess the backend shape, you apply the wrong server function rules and the wrong write rules; if you write an API name from memory, you write one the installed version renamed, deprecated or never had.

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
| 0 | Fresh discovery entry printed | Use it. If `versionNotes` lacks an entry for any [API lookup](#api-lookups), resolve the missing ones and `write` the completed entry. In `refresh`, discover and write anyway. |
| 4 | No discovery entry | Discover and write. |
| 5 | Older than the script's maximum age, or an installed `@tanstack` version changed | Discover and write. |
| 3 | Cache file or an installed package manifest unreadable | Read stderr. For the cache file, tell the user and delete it only after they agree, since it holds every app's discovery entry. For a manifest, ask the user to reinstall dependencies. |
| 2 | Usage error | Read stderr, correct the call, rerun. |

**Discover.** Find each field from the code:

| Field | Values | How to find it |
| --- | --- | --- |
| `backend` | `database`, `service`, `both` | Read the server function handlers. `database`: they query a database client directly. `service`: they call another service over HTTP. `both`: some do each. |
| `pendingUi` | `route-level`, `per-section` | Resolve the **pending options** lookup first. `route-level` when the router file sets the default pending component it names. Otherwise ask the user whether they want a route-level pending component or Suspense sections only; with no user available, record `per-section` and say so. |
| `verify` | list of commands | The repo's lint, typecheck and test commands from `package.json` `scripts`. |
| `versionNotes` | list of strings | Run `uv run scripts/discovery.py versions --app <app-root> --repo <repo-root>`, then resolve every [API lookup](#api-lookups) against those versions by reading [references/versions.md](references/versions.md). Record one string per lookup, `<lookup>: <installed API and behaviour>`. If `versions` prints `{}`, ask the user to install dependencies before continuing. |

**Write.** The script adds `discoveredAt` and the installed `versions`, and rejects unknown values:

```bash
uv run scripts/discovery.py write --app apps/web --repo <repo-root> <<'EOF'
{"backend": "database", "pendingUi": "per-section", "verify": ["pnpm check", "pnpm typecheck", "pnpm test"], "versionNotes": ["awaited fetch: ...", "background prefetch: ..."]}
EOF
```

**First write in a repo.** Exit 6 means `.draekien/` is missing: ask the user before creating it. When `.draekien/tanstack-data-loading/discovery.json` does not exist yet, ask whether to add `.draekien/tanstack-data-loading/` to `.gitignore`; the discovery entries hold one developer's local discovery. If the user declines `.draekien/`, keep the discovered fields for this task only and say the discovery cache was not written.

Discovery is done when all of these hold: every field is known; `versionNotes` has one entry for every API lookup; and either `read` or `write` exited 0 for the app, or the user declined the cache.

**Backend rules.** Before writing or auditing any server function, mutation or write path, read the reference for `backend`:

- `database` — [references/backend-database.md](references/backend-database.md).
- `service` — [references/backend-service.md](references/backend-service.md).
- `both` — read both. Apply each to the server functions whose handlers match it; a handler that does both applies each reference to its own part.

## API lookups

The rules below name these concepts in bold instead of an API, because the API for each changes between releases. Discovery resolves each one for the installed versions and records it in `versionNotes`; write the API that entry names. Only the bold terms in this table are lookups; **critical**, **unawaited** and **Suspense section** are terms the rules define.

| Lookup | What to resolve |
| --- | --- |
| **awaited fetch** | The `QueryClient` method a loader awaits: returns cached data when fresh, otherwise fetches, and resolves with the data. Its infinite-query counterpart. |
| **background prefetch** | How a loader starts the same read without awaiting it, whether that promise resolves with the data (a chained read needs it to), and how to attach a no-op rejection handler (a library export, or `.catch(() => {})`). |
| **deprecated reads** | Every `QueryClient` read method the installed docs mark deprecated, and its documented replacement. For a replacement of a method that returned cached data without refetching: the `staleTime` value that keeps that behaviour, and the value that still refetches after invalidation. |
| **SSR query integration** | The call in the router file that connects the router to the query client for server rendering and streaming, and its package. |
| **data-only SSR** | The route option that runs loaders on the server and renders the component only on the client. |
| **section boundary** | The router's error boundary component that resets on a key, and Query's error reset boundary. |
| **pending options** | The router options that set a default pending component, the delay before it renders, and the minimum time it stays, with their defaults. |
| **mutation scope** | The `useMutation` option that runs mutations sharing an id one at a time, in call order. |
| **input validator** | The server function builder method that validates input. |
| **server-only files** | The file-name convention for server function exports and for server-only helpers, and whether import protection blocks client imports of server-only files. |
| **suspense batch** | Whether `useSuspenseQueries` accepts infinite queries. |

## Loaders

Scope: the `loader` option of every file route under the app root.

A read is **critical** when the route must not render without it or must render something else when it fails: the main content, existence (404), authorization (403), a redirect, a limit gate, form defaults. Every other read is **unawaited**.

- Critical read: `await` the **awaited fetch** with the read's `queryOptions`. Awaiting it in the loader sends a 404 or 403 to `notFoundComponent` or `errorComponent` before render; let the error reach them, or throw `notFound()`.
- Unawaited read, including hidden variants such as a toggle's second period: the **background prefetch** with a no-op rejection handler. Without the handler the rejection is unhandled on the server; the component's `useSuspenseQuery` still rethrows the error to its boundary.
- Start every unawaited read before the first `await`. A read started after an `await` is a waterfall.
- Independent critical reads: one `await Promise.all([...])`.

  ```ts
  ✗ const order = await awaitedFetch(orderQueryOptions(id))
    const customer = await awaitedFetch(customerQueryOptions(customerId))

  ✓ const [order, customer] = await Promise.all([
      awaitedFetch(orderQueryOptions(id)),
      awaitedFetch(customerQueryOptions(customerId)),
    ])
  ```

  `awaitedFetch` stands for the **awaited fetch** recorded in `versionNotes`.

- A read `b` that needs read `a`'s result is a waterfall that cannot be removed:

  | `a` | `b` | Loader |
  | --- | --- | --- |
  | critical | critical | Await `a`, then await `b` with `a`'s result. |
  | critical | unawaited | Await `a`, then start `b` as a background prefetch: the one unawaited read started after an `await`. |
  | unawaited | unawaited | Before the first `await`, call the **awaited fetch** for `a` without awaiting it, chain `b`'s awaited fetch onto its result with `.then`, and end the chain with one no-op rejection handler. A background prefetch that resolves without data cannot start this chain. |

- The loader and the component use the same `queryOptions` object. A different key in the component fetches the data a second time.
- A route a signed-out visitor can open starts reads that require a session only in its signed-in branch. Otherwise every signed-out visit fires calls that throw.
- Replace each of the **deprecated reads** with its replacement. A replacement that returns cached data without refetching has a trap: if a mutation invalidates the key, a later loader run still returns the invalidated data, so the route decides its branch, redirect or gate from old data. For a key a mutation invalidates, use the `staleTime` the **deprecated reads** entry records as still refetching after invalidation, not the one that keeps the old behaviour. A `staleTime` passed to one loader call does not stay on the query: whether invalidation refetches a mounted page depends on the component's `useSuspenseQuery` `staleTime`.
- Do not defer reads to scroll or interaction, and do not add hover prefetching beyond the router's intent preloading. An unawaited read already streams without blocking the page; deferring it adds a request after render, and no TanStack doc defines how deferral behaves with `useSuspenseQuery`.

## Streaming and SSR

Scope: the router file and every route's SSR option.

- The rules here hold only when the router file sets up the **SSR query integration**. If it does not, report that as the first finding.
- An unawaited read runs on the server and streams to the client without blocking the server response. A critical read blocks the response until it resolves.
- `useSuspenseQuery` and loader reads run on the server. `useQuery` does not; its data loads after hydration, so a route component that reads with `useQuery` is a waterfall.
- Do not rely on unawaited reads streaming under **data-only SSR**, and do not recommend it as a fix; no official doc states the behaviour. Check it in the running app when the task depends on it.
- Do not configure route code splitting: Start enables it, and the loader stays in the main chunk.
- Where a rule here says no official doc states a behaviour, search the installed docs for it first. If they now state it, record it in `versionNotes` and follow the docs.

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

- An infinite query that the **suspense batch** does not accept still starts after the others resolve; start it in the loader.
- A child that suspends on a query its route could know about: start that read in the route loader. Otherwise the child's request starts only after the parent renders.
- Each unawaited read renders inside its own **Suspense section**: the **section boundary** around `<React.Suspense fallback={...}>`, inside Query's error reset boundary where the error UI offers a retry. The rest of the page renders while the section streams, and its error stays inside it. A critical read needs no Suspense section.
- A query key that changes on the same route (search param, tab, page, period): make the change inside `React.startTransition`. `useSuspenseQuery` has no `placeholderData`; without the transition, React replaces the content with the fallback.
- `pendingUi: route-level`: the router sets a default pending component, rendered inside the app's shell layout; read its delay and minimum display time from the **pending options**. `pendingUi: per-section`: add no default pending component; if the user chose this while the router sets one, leave it until they ask for its removal.

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

- Saves to one entity that can overlap (autosave, rapid toggles): set the **mutation scope** to a string naming the entity, such as `` `order-${orderId}` ``. A refetch after each save does not fix ordering: the responses can still arrive out of order. Where the installed version has no mutation scope, disable the trigger while `isPending`.
- A mutation that changes which data the user may see (switching account or workspace) awaits its invalidation, so the next screen never renders with the previous account's data. Every other mutation follows the rule above.

## Server functions

Scope: every `createServerFn`.

- Put server function exports and server-only helpers in the files the **server-only files** convention names. Client code may import server function exports; the build replaces each handler with a request stub. Where import protection does not block client imports of server-only files, the convention is naming only: search for each server-only file's importers, and report any importer client code reaches (a route component, a hook, or any module a route component imports).
- Validate input with the **input validator**.
- Each call from the client is one HTTP request with a fixed cost: the request, plus every middleware it runs. Start neither batches nor deduplicates calls: `Promise.all` over three server functions sends three concurrent requests, and two identical calls send two. Deduplicate identical reads through the query cache by calling the server function only from a `queryFn`.
- Do not merge every read on a page into one server function. The page then waits for its slowest part, Suspense sections stop streaming separately, and every mutation refetches all of it.
- Middleware runs on every call to every server function that uses it. Shared middleware computes only what every one of those functions reads; a value only some read goes in its own middleware.
- Statements sent on one database connection, including every statement in one transaction, run one at a time. `Promise.all` over them saves no time; reduce the number of statements instead.
- Apply the backend reference named under Discovery, "Backend rules", to every server function.

## Gotchas

- After converting to `useSuspenseQueries`, every test mock of `@tanstack/react-query` must export `useSuspenseQueries`.
- `toBe` on cached rows fails: structural sharing returns an equal copy, not the same object. Use `toEqual`.
- Once a loader awaits a read, a 404 from it right after a write (a backend that updates its read model asynchronously) shows the route's error component instead of an error inside a Suspense section.
