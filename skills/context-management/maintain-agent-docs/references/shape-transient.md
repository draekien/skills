# Transient state

Guidance that was true for a season, written in a document that is read as permanent. It is not drift — the line may still be accurate today — but its shape guarantees it will mislead later, and nothing in the document tells a future reader when to stop believing it.

## The tell

Durable guidance states what holds. Transient state states where things currently stand. The distinguishing question: **if this line goes unread for two quarters, does it become a lie on its own?** A rule about naming does not. A note that the new client is behind a flag does.

Recognisable forms:

- **In-flight work described as fact** — a migration under way, a rewrite half-landed, a package being split, two systems running side by side "for now".
- **Temporal deixis** — currently, at the moment, for now, until, still, soon, this quarter, the new X, the old X, we are in the process of. "The old X" is the strongest signal: it names a state, and it dates the document to the moment that state existed.
- **Ordering by circumstance rather than rule** — "prefer the v2 client" where the reason is that v1 is being retired, not that v2 is better. Once v1 is gone the line is noise; while it stands the reason is invisible.
- **Counts and inventories that move** — how many services exist, which modules have been converted, what remains to do. A conversion checklist inside a conventions document is a plan wearing the wrong clothes.
- **Named people and in-flight decisions** — who is working on something, what is awaiting a decision, what a discussion concluded last month.

## What the repair is

Three outcomes, and the line decides which:

- **The work it describes is real and ongoing** — the content belongs in a plan, where status discipline gives it an expiry. Move it there, and leave behind only the durable rule it implies, if there is one.
- **The state is still moving and an agent acts on its current value** — replace the snapshot with the lookup, below. The document keeps the instruction that finds the answer; the answer stays where it is generated.
- **The work is done, abandoned, or the state has passed** — remove the line. The document is better with the gap, because an absent rule sends an agent to read the code while a stale one sends it somewhere wrong.

A transient line sometimes wraps a durable rule worth keeping. "Use the v2 client, the old one is being retired" carries one of each: keep the preference if it stands on its own merits, drop the retirement.

## Writing the lookup

```text
✗ Twelve services use the v2 client. Auth, billing and search are still on v1.
✓ For the services still on v1, grep for `V1Client` under `services/`.
```

The replacement is one instruction that returns what the deleted lines held — a command, a path, a generated file, a document something regenerates. It is not a shorter summary of the state, and not a hint about where to start looking.

**Run it before writing it.** A lookup that returns nothing, returns something other than the information, or names a path that has since moved costs the agent a round trip and then leaves it with less than the stale line gave it. Where nothing returns the information, the line takes one of the other two outcomes — never a pointer written on the assumption that something will answer it.

The conversion saves no tokens and is not meant to. What it buys is a line that cannot rot: a snapshot is wrong the next time anything moves, and the instruction holds until the code that answers it moves.

Only state an agent acts on earns a lookup. Where the answer would change nothing an agent does, the outcome is removal — a pointer to information nobody needs is the same waste in fewer tokens.

## Evidence standard

Quote the line and name which outcome applies and why. For a lookup, give the instruction and what running it returned. Where the outcome depends on whether the described work has landed, that is not this class — it is a history-rot finding, and it goes to interview.
