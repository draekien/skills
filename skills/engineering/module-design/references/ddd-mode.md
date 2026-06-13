# DDD Mode

Activated when `.draekien/ubiquitous-language.yaml` exists at the project root. Integrates bounded context awareness and term tracking into the design session.

## On Activation

All contexts and terms are loaded during Session Start via `scripts/query.py`. No additional loading step is needed here.

## During Interview

After every user response, run term capture and conflict detection concurrently.

**Term Capture** — when a noun is judged domain-specific and not yet defined in any loaded context:

1. Propose a definition. Wait for confirmation.
2. Search the codebase for the term. Read surrounding context.
3. If a semantic contradiction is found: hard interrupt, surface the conflict, wait for resolution. Update definition if needed; repeat from step 2.
4. Determine the bounded context from the confirmed map. If ambiguous, ask.
5. Before first write to any context, confirm the bounded context assignment.
6. Write immediately using:

   ```
   uv run scripts/write.py --dict .draekien/ubiquitous-language.yaml add-term \
     --context <Context> --term <TermName> --definition "<text>" \
     [--aliases Alias1 Alias2] [--usage "<text>"] \
     [--related "TermName:relationship" ...]
   ```

**Conflict Detection** — check every response against all loaded definitions:

- **Definition conflict** — user uses a defined term contradicting its stored meaning: hard interrupt, surface both meanings, ask which is canonical. Run `add-term` on resolution.
- **Cross-context collision** — same term defined differently in two contexts: surface explicitly, ask if intentional. Both stand if deliberate (DDD allows intentional ambiguity across contexts).
- **Vague language** — user word matches 2+ defined terms: hard interrupt, list matching terms with definition summaries, wait for disambiguation. Run `flag-ambiguity` until resolved; run `resolve-ambiguity` once canonical meaning is confirmed:

  ```
  uv run scripts/write.py --dict .draekien/ubiquitous-language.yaml flag-ambiguity \
    --context <Context> --term <TermName> --note "<text>"

  uv run scripts/write.py --dict .draekien/ubiquitous-language.yaml resolve-ambiguity \
    --context <Context> --term <TermName>
  ```

## In the Spec

Include a **Bounded Context** section naming the confirmed context and listing any terms defined or referenced from `.draekien/ubiquitous-language.yaml` during this session.
