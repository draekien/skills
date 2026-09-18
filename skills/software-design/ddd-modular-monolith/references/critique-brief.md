# Critique Brief

One subagent per round. The rubric is supplied and the pass is bounded, so this does not need the strongest model available — a mid-tier one clears it. It proposes; it never commits.

Brief it to:

- Read the draft — the module map, the module spec, the rule set, or the violations report, whichever the current mode produces. Where nothing is on disk yet, the draft text comes in the brief.
- Read every reference file the mode names — one for most modes, all of them under `critique` — and check the draft against every rule in each. Name the full set in the brief; do not make the subagent guess which applies.
- Check the draft against the five strict rules, quoted into the brief in full.
- For each violation: quote the offending text, name the rule, and supply the concrete replacement text — the text itself, not a description of the change.
- Under `critique`, a finding is a violation the report missed, or a suggested fix that would not hold once applied.
- Report clean if nothing violates.
- Never edit the draft or write any file.

Two failure modes to name explicitly in the brief, because a critic reading only the draft will otherwise miss both:

- A boundary that looks clean in the module map while the code underneath joins across it. Where code is available, check the claim.
- A module given more ceremony than its subdomain type justifies. Over-modelling is a finding, not a virtue.

Judge each round fresh. A draft that came back clean in an earlier round has since changed, so carry no verdict forward.
