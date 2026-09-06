# Description Triggering

A description can satisfy every rule in the body's description section and still never fire. This covers why, and how to find out before shipping.

## The mechanism

Only `name` and `description` are loaded at startup, for every installed skill at once, and the agent selects from that list alone. A trigger rule written in the body cannot help the agent decide to load the body. Everything below follows from that.

✗ `description: Helps with database work.`

✓ `description: Writes and reviews Postgres migrations. Use when adding or altering a table, when a migration fails to apply, or when the user says "add a column", "backfill", "schema change".`

The second names an operation, its object, the situations, and the words a user actually types. The first names a domain and leaves the agent to guess the rest.

One nuance shapes what to aim for: an agent reaches for a skill on work that needs capability beyond what it already has. A simple one-step request can fail to trigger a perfectly matched description, because the agent just does the task. That is not a wording defect — a skill whose whole job the agent already performs failed the worthiness gate, and no description will rescue it.

## Failure modes

- **Too narrow** — requests that should trigger slide past, because the description names only the vocabulary the author happened to use. Cure: name the *situation*, not just the domain word, and claim the cases where the user would not say the domain word at all.
- **Too broad** — the skill fires on adjacent work it does not handle. Cure: state the boundary against the nearest neighbouring capability. Where two skills share vocabulary, each description says what it is not for; broadening both is how a set of skills becomes untriggerable.
- **Implementation-facing** — the description explains the skill's internals, while the agent matches against what the user asked for. Cure: write it in terms of the user's intent and the result they get.
- **First or second person** — the description is injected into a system prompt, where an inconsistent point of view degrades selection. Third person, always.

## The optimisation loop

Intuition does not settle whether a description fires; running it does.

1. **Write the query set** — around twenty realistic prompts, split evenly between should-trigger and should-not-trigger, each labelled. Vary phrasing (formal, casual, abbreviated, mistyped), explicitness (some naming the domain, some describing only the need), length, and how deeply the relevant task sits inside a larger request. The valuable positives are those where the skill helps but the connection is not obvious from the wording; a query asking for exactly what the skill does tests nothing.
2. **Make the negatives near-misses** — prompts sharing the skill's vocabulary that genuinely need something else. An obviously unrelated prompt measures nothing.
3. **Split the set** — hold back roughly 40% as a validation set and never read those results while revising, or the description ends up fitted to the queries rather than to the class of situations behind them.
4. **Run each query several times and score a trigger rate**, not a yes or no: selection is nondeterministic, and a single run cannot tell a description that fires half the time from one that fires reliably. Three runs is a workable floor; a positive passes above a rate of 0.5 and a negative below it.
5. **Revise against the training failures only, one change per round.** Two edits at once hide which one moved the result. Generalise each failure instead of importing its exact words — the fix for a missed query is the category it belongs to, not its keywords.
6. **Choose by validation rate, not recency** — a later iteration is often an overfitted one. When several rounds produce no improvement, restructure the description rather than continuing to tune it, and suspect the query set: queries that are too easy, too hard, or mislabelled cannot be fixed by better wording.

Watch the character budget throughout — descriptions grow under optimisation, and the spec's ceiling is easy to cross without noticing.

Done when every training query passes or has stopped improving, and the description carried forward is the one with the best validation rate observed.
