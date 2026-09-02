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

Two outcomes, and the line decides which:

- **The work it describes is real and ongoing** — the content belongs in a plan, where status discipline gives it an expiry. Move it there, and leave behind only the durable rule it implies, if there is one.
- **The work is done, abandoned, or the state has passed** — remove the line. The document is better with the gap, because an absent rule sends an agent to read the code while a stale one sends it somewhere wrong.

A transient line sometimes wraps a durable rule worth keeping. "Use the v2 client, the old one is being retired" carries one of each: keep the preference if it stands on its own merits, drop the retirement.

## Evidence standard

Quote the line and name which outcome applies and why. Where the outcome depends on whether the described work has landed, that is not this class — it is a history-rot finding, and it goes to interview.
