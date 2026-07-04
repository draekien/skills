# draft-a-prd

## Phase 1 (interview) sits directly above Phase 2 (draft) in the same file

**Gap:** Phase 1 — Alignment (the interview step) is immediately followed in the same file by Phase 2 — Draft. This matches the "shortchanged legwork" anti-pattern described in `skills/drafting/skill-writing/SKILL.md`, where an interview/gathering step is at risk of being rushed or skipped because the drafting goal is visible right below it in the same document.

**Why it's a tradeoff, not a clear-cut fix:** Splitting Phase 1 into a separate skill (e.g. `gather-prd-requirements`) is a structural, invocation-affecting change — it would alter how the skill is composed and invoked (two skills instead of one, a hand-off between them, possibly different `disable-model-invocation` semantics per skill). The skill-writing guidance itself frames this anti-pattern as something to watch for empirically, not something to preemptively refactor: the fix is only warranted if live runs actually show the interview being rushed or skipped in favor of jumping straight to drafting. There's no evidence yet of that failure mode occurring, so restructuring now would be speculative.

**Recommendation:** No change for now. Keep the single-file, three-phase structure as-is.

**Alternative:** If future evals or real usage show the agent skipping/shortchanging Phase 1 in practice, split the interview step out into its own skill (e.g. `gather-prd-requirements`) that `draft-a-prd` invokes or depends on, per the skill-writing anti-pattern's suggested remedy.
