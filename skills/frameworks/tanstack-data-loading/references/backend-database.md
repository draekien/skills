# Backend: database

Rules for server functions whose handlers query a database client directly.

## Server functions

- One server function per query key. Each call already pays a fixed request and middleware cost, so a function that serves one key keeps that cost tied to one query-cache entry.
- Merge two server functions only where they compute the same expensive work (the same lookup, the same aggregate), and read each part with `select`.
- A list that runs one query per row becomes one server function returning every row's values, read by one query keyed as a list.
- A multi-step write is one server function that runs every step.
- Resolve the session's scope (tenant, plan, permissions) in one statement per call. A cookie or in-memory cache of it serves stale permissions after they change.

## Writes

- A read that guards a write (a limit check, a uniqueness check) runs in the same transaction as the write and locks the rows it read: `SELECT ... FOR UPDATE`, or the query builder's equivalent such as Drizzle `.for("update")`. Without the lock, two concurrent requests both pass the check.
- A guard that counts rows that do not exist yet has no rows to lock. Take a transaction-scoped advisory lock keyed on the parent instead: `pg_advisory_xact_lock` in Postgres, or the database's equivalent.
- Prove the race before adding the lock: a test that fires several creates in parallel against the unlocked code and gets more rows than the limit. The same test passing after the lock is the evidence the lock works.
