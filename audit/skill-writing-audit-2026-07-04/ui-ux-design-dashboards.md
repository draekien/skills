# design-dashboards

## Residual "screen" vs "dashboard" terminology overlap

**Gap:** The body uses both "dashboard" and "screen" to refer to the same artifact throughout (e.g. line 7 "single-screen answer", line 17 "one screen", line 62 "data-dense screens", line 64 "one screen, no scrolling", vs. "dashboard" as the title term used everywhere else including the skill name itself). The narrower "view" synonym (lines 58, 64) has already been folded into "screen" as a mechanical fix, but the deeper question — whether "screen" should itself be retired in favor of "dashboard" everywhere, or kept as the deliberate physical-viewport term while "dashboard" stays the conceptual/artifact term — was not resolved.

**Why it's a tradeoff:** This is an established leading-term decision, not a typo fix. "Screen" and "dashboard" arguably carry different shades of meaning in this skill: "screen" emphasizes the physical viewport constraint (no scrolling, F-pattern scanning), while "dashboard" emphasizes the artifact/deliverable as a whole. Collapsing them into one term could either clarify or flatten a useful distinction, and doing so touches many lines across multiple sections (Layout, the opening commitments, and the classification intro).

**Recommendation:** Leave "dashboard" as the primary/title term and "screen" as a deliberate secondary term scoped specifically to physical-viewport statements (scanning patterns, scrolling, one-screen constraint) — i.e., treat the current mixed usage as intentional rather than drift, since each instance of "screen" in the file already refers specifically to viewport/scanning behavior rather than the dashboard as a concept.

**Alternative:** Do a full pass replacing every standalone "screen" with "dashboard" for strict one-term-per-concept compliance, accepting the loss of the viewport-specific nuance.

## Buried prerequisite step (audience/decision/speed brief)

**Gap:** The instruction to establish who reads the dashboard, what decision it serves, and how fast they need an answer (line 7) is a subordinate clause in the opening paragraph with no heading, immediately followed by the prominent "## Classify the dashboard first" heading and table. The visually compelling classification table may pull attention away from actually pinning down the brief first.

**Why it's a tradeoff:** Fixing this well requires either (a) restructuring the body to add a new "## Establish the brief" heading ahead of classification — a structural change to the skill's phase model — or (b) leaving it as-is on the grounds that "Classify the dashboard first" already embeds audience and question as table columns, so the brief is not actually skippable in practice. Per skill-writing's own evidentiary bar, splitting or promoting a step into a heading should be backed by evidence that agents actually skip it, which hasn't been established here. This is a structural/judgment call, not a mechanical fix.

**Recommendation:** Leave as-is for now; the classification table's "Question" and "Audience" columns already force the same information to surface. Revisit only if live runs show the brief step being skipped or rushed.

**Alternative:** Add a short "## Establish the brief" subsection (who reads this / what decision / how fast) before "Classify the dashboard first" to give it equal structural weight immediately, without waiting for failure evidence.
