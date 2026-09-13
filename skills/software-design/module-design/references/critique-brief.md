# Critique Brief

One subagent per round. The rubric is supplied and the pass is bounded, so this does not need the strongest model on hand — a mid-tier one clears it. It proposes; it never commits.

Brief it to:

- Read the draft: the spec at the resolved path under `design` and `refine`, the violations report plus the code it covers under `review`. Where no file exists yet, the draft text comes in the brief.
- Check the design the draft describes against every recommended rule in `design-principles.md` under the Recommended Rules heading, where the full rule definitions live.
- For each violation: quote the offending text, name the rule, and supply the concrete replacement text — the text itself, not a description of the change.
- Under `review`, a finding is a violation the report missed, or a suggested fix that would not hold.
- Report clean if nothing violates.
- Never edit the draft or write any file.

Judge each round fresh. A draft that came back clean in an earlier round has since changed, so carry no verdict forward.
