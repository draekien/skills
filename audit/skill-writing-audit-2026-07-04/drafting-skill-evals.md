# skill-evals

## Anti-patterns section largely restates content already explained earlier

The `## Anti-patterns` section (naming Recall theatre, Verbatim-trigger corpus, Criteria drift, Verdict leakage, Context bleed, Judge as authority, Single-sample certainty, The unfailable eval, Trend drift) reuses phrasing and mechanisms already fully taught in "The spine," "Activation eval," and "Impact eval" — e.g. "drift wearing its costume" (spine) versus "wearing the costume of a test" (Criteria drift), and "shares the blind spots of the agents it judges" (spine) repeated near-verbatim in "Judge as authority."

**Why it's a tradeoff, not a clear fix:** `skill-writing/SKILL.md` explicitly lists "Anti-pattern section" as an endorsed body pattern precisely for naming failure modes the agent should recognize on sight — collapsing it to a one-line index (as the raw finding suggests) trades that recognition value for compactness, and there's a real judgment call about how much restatement is acceptable "as a named index" versus how much is pure duplication. Deleting the section outright would also drop a naming device the "Closing the loop" step could reference when a skill fails an eval for one of these reasons.

**Recommendation:** Compress each bullet to name + one-line pointer back to where the mechanism is explained (e.g. "Criteria drift — see 'Commit ground truth first' above"), keeping the section as a lookup index rather than a re-explanation. This keeps the recognized-on-sight value while eliminating the duplicated mechanism prose.

**Alternative:** Leave the section as-is if the author judges the redundancy an intentional reinforcement device (repetition at the point of highest recall value, i.e., right before the agent runs an eval) rather than bloat — in which case no change is needed.

## Activation eval and Impact eval sections are single-branch material sitting in the always-loaded body

Every real invocation of this skill takes exactly one branch — activation or impact — yet both mode's full instructions (corpus construction, positive/negative derivation, judging, scoring) sit directly in the body, and the "Persisted state" section already treats them as fully separate subtrees (`activation/` vs `impact/`).

**Why it's a tradeoff, not a clear fix:** The body is currently well under the 500-line cap, and the two modes are tightly cross-referenced through "The spine" (both modes are explained as instances of the same four-move discipline). Splitting them into `references/activation-eval.md` and `references/impact-eval.md` would reduce context loaded per run, but risks fragmenting a currently cohesive explanation of the shared spine, and the orchestrator commonly runs both modes for the same skill in one session anyway (so the token savings from lazy-loading one branch may not materialize in practice).

**Recommendation:** Leave the two sections in the body as-is unless the body later grows past the line budget or an eval shows the orchestrator wastes context re-reading both branches when the author only asked for one. Splitting is a defensible future move, not a current defect.

**Alternative:** Split now — move each mode's construction/derivation/judging instructions into its own reference file, leaving a one-line summary + link per mode in the body, consistent with the "distinct branches → references/" rule in `skill-writing`'s Content Placement section.

## Competing skill descriptions used by the activation eval's selector are not frozen into the suite

The Activation eval section says to present the skill's description "alongside a realistic set of competing skill descriptions" to the selector subagent, but never specifies where that competitor set comes from or whether it is committed into the frozen suite alongside the prompts and labels. Without freezing it, two runs against the same suite version could select against different competitor sets — an uncontrolled variable of exactly the kind the eval otherwise guards against (Isolation, Versioning).

**Why it's a tradeoff, not a clear fix:** Freezing the competitor set changes the suite's schema (it would need a new field, e.g. `competingDescriptions`) and its versioning semantics (does changing only the competitor set, with prompts/labels unchanged, warrant a new suite version?) — both are design decisions with real alternatives, not a wording fix. There's also a question of *source*: freezing the competitor set at suite-commit time locks in whatever other skills existed then, which itself can drift as skills are added/removed from the environment — arguably a second, harder-to-solve version of the same staleness problem the fix is meant to close.

**Recommendation:** Add the competing descriptions as a field on the committed suite object (sourced from the skills actually available to the selector at commit time), so a re-run against the same suite version selects against an identical competitor set. Treat a competitor-set change as suite content for hashing/versioning purposes, same as a prompt or label change.

**Alternative:** Leave the competitor set unfrozen and re-sampled live each run, accepting that activation runs are only comparable in aggregate trend, not in a strict apples-to-apples per-run sense — cheaper to implement, but weakens the "same frozen suite version" comparability guarantee the rest of the skill relies on.
