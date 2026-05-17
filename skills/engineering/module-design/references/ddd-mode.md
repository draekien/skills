# DDD Mode

Activated when `UBIQUITOUS_LANGUAGE.md` exists at the project root. Integrates bounded context awareness and term tracking into the design session.

## On Activation

Load all scoped `UBIQUITOUS_LANGUAGE.md` files found in the project. Infer the bounded context map from the root index. Confirm the map with the user if ambiguous.

## During Interview

After every user response:

**Term Capture** — when a noun is judged domain-specific and not yet defined in any loaded file:
1. Propose a definition. Wait for confirmation.
2. Search the codebase for the term. Read surrounding context.
3. If a semantic contradiction is found: hard interrupt, surface the conflict, wait for resolution.
4. Determine the bounded context. If ambiguous, ask.
5. Before first write to any context file, confirm the target path.
6. Write immediately — no batching.
7. Update root `UBIQUITOUS_LANGUAGE.md` if a new scoped file is created.

**Conflict Detection** — check every response against all loaded definitions:
- **Definition conflict** — user uses a defined term contradicting its stored meaning: hard interrupt, surface both meanings, ask which is canonical.
- **Cross-context collision** — same term defined differently in two contexts: surface explicitly, ask if intentional. Both stand if deliberate.
- **Vague language** — user word matches 2+ defined terms: hard interrupt, list matching terms with definition summaries, wait for disambiguation.

## In the Spec

Include a **Bounded Context** section naming the confirmed context and listing any terms defined or referenced from its `UBIQUITOUS_LANGUAGE.md`.
