# Critique Brief

One subagent per round. The lenses are supplied and the pass is bounded, so this does not need the strongest model on hand — a mid-tier one clears it. It proposes; it never commits.

Give it the files the draft depends on and the project's rules files — `AGENTS.md`, `CLAUDE.md`, and the contract docs they point to — so it reads those rather than rediscovering them.

Brief it to:

- Read the draft at its temp path: the spec under `design` and `refine`, the violations report plus the code it covers under `review`.
- Check the draft through three lenses, in this order:
  1. **Correctness** — every claim about existing code, libraries, protocols, or analyzers is checked against its source and cited, or marked `unverified`.
  2. **Project rules** — the rules files and contract docs supplied in the brief.
  3. **Design principles** — every strict and recommended rule in `design-principles.md`, where the full rule definitions live.
- For each finding: quote the offending text, name the lens or rule, tag it, and supply the concrete replacement text — the text itself, not a description of the change.
- Tag `blocker` when the design would not build, run, or behave as stated, or breaks a strict rule; `major` when it breaks a project rule or a recommended rule in a way a caller would notice; `minor` for wording, naming, and consistency.
- Under `review`, a finding is a violation the report missed, or a suggested fix that would not hold.
- Read the draft's Refinement Record. Re-raise a rejected or escalated finding only with evidence its recorded reason did not consider.
- Report clean if nothing violates.
- Never edit the draft or write any file.

Judge each round fresh. A draft that came back clean in an earlier round has since changed, so carry no clean verdict forward.
