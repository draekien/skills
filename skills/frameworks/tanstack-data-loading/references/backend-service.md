# Backend: service

Rules for server functions whose handlers call another service over HTTP.

## Server functions

- One generic passthrough server function for a single backend call. It follows the same error rule as a composed function below.
- One named composed server function for any action or critical read that needs more than one backend call. Run the independent backend calls inside it in parallel. Several client calls would each pay the request and middleware cost; one composed call pays it once.
- A composed function returns the first non-2xx response instead of throwing. A thrown error crosses the Start serializer with only its `message`, losing the status and body.
- The client wrapper that calls a composed function checks the returned response and throws for non-2xx: `notFound()` for 404, an `Error` carrying the status otherwise. Loaders, Suspense sections and `onSuccess` then see a rejection, never an error body written into the query cache.
- Measure the session lookup's cost before caching it. A session cookie cache keeps a revoked session valid until the cache expires.

## Writes

- A write that spans two services has no transaction. The client generates one `Idempotency-Key` per user action, outside `mutationFn` (in the mutation variables or form state), and reuses it for every attempt and every backend call the write makes. A key generated inside `mutationFn` changes on retry and applies the write twice.
- Check that each service honours `Idempotency-Key` before relying on it; if one does not, report that instead of adding the key. A retry with the same keys then completes the action.
- An orphaned first write (the second call failed and was never retried) is accepted. Do not add compensating deletes; the retry path is what completes the action.
