# Audit

Scope: the path given after `audit`, default the app root. Without `--fix`, report and stop; change code only when `--fix` is given or the user asked for fixes.

## Sweep

Search with ripgrep regular expressions. Rows marked multi-line need multi-line search or a read of each file. Read every hit.

| Search | Rule |
| --- | --- |
| `ensureQueryData\|prefetchQuery\|fetchQuery\|prefetchInfiniteQuery\|ensureInfiniteQueryData\|fetchInfiniteQuery` | Deprecated `QueryClient` method, when the installed version has `query` |
| multi-line: `void [^;]*\.(query\|infiniteQuery)\(` whose chain has no `.catch(` | Unhandled rejection |
| multi-line: `loader:` followed by two `await` lines | Waterfall between independent critical reads |
| multi-line: two `useSuspenseQuery\(` in one function | Waterfall between suspense queries |
| `useQuery\(` in a route component | Not run on the server |
| `(await\|return) [^;]*invalidateQueries` inside `onSuccess` or `onSettled` | Pending until refetch |
| `setQueryData\(` and `invalidateQueries\(` on the same key | Refetch of written data |
| `useSuspenseQuery\(` in a component rendered inside `.map(` | One request per row |
| `createServerFn` in a file not named `*.functions.ts` | File naming |
| `backend: database` only: read each writing server function for a count or existence check followed by an insert | Check-then-write race |

The `\|` in the table is markdown escaping: the pattern is `|`, for example `ensureQueryData|prefetchQuery|fetchQuery`.

Then read every loader, every component that renders a query read, every `useMutation` and every `createServerFn` under the scope against the SKILL.md rules and the backend reference. The table finds the patterns a search can find; it does not decide which reads are critical, whether Suspense sections exist, or whether server functions are sized to the backend.

## Report

One finding per broken rule: `file:line`, the rule, and the change. Group by route. State requests saved per page load from reading the code, for example "3 sequential requests → 1 parallel batch". Report a latency change only if it was measured before and after; otherwise say it was not measured.

## Apply

Only with `--fix` or an explicit request. Run every `verify` command first and record which already fail. Make the changes, then run `verify` again, and fix new failures against the SKILL.md Gotchas until every command that passed before passes again.

Done when every loader in scope has each read classified as critical or unawaited, every component, mutation and server function in scope has been checked, every search hit is reported or ruled out, and, with `--fix`, every `verify` command that passed before the changes passes after them.
