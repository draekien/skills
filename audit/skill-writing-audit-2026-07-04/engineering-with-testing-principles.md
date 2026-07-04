# with-testing-principles

## Name the Arrange-Act-Assert pattern explicitly

**Gap:** SKILL.md:49 describes the standard Arrange-Act-Assert test structure in bespoke phrasing ("Arrange the preconditions, act once on the code under test, assert the outcome") without naming the pattern.

**Why it's a tradeoff:** Anchoring on the established term would let the skill lead with a strongly-primed piece of jargon, which can shorten the instruction and leverage the model's prior knowledge of the pattern. But the skill's current voice consistently favors plain-language description of *why* each move matters (e.g. "keeping these phases distinct keeps the test legible and its failure diagnostic") over naming conventions, and this is a deliberate style choice, not an oversight. Inserting the term also risks the model pattern-matching to a shallow AAA checklist rather than internalizing the diagnostic reasoning the sentence is built to convey. This is a voice/emphasis decision, not a correctness fix.

**Recommendation:** Leave as-is, since the surrounding prose already states the substance of AAA and the skill's style elsewhere avoids naming conventions as a crutch.

**Alternative:** Rewrite the sentence to lead with the term, e.g. "Structure each test as **Arrange-Act-Assert**: set up preconditions, act once on the code under test, assert the outcome — keeping the phases distinct and named keeps the test legible and its failure diagnostic," trading a small voice shift for faster recognition by readers already familiar with the term.

## Possible duplication between the "coverage theatre" framing and the closing coverage aphorism

**Gap:** SKILL.md:29 opens the Edge-case enumeration section with "High line coverage on the happy path while every boundary goes untested is coverage theatre," and SKILL.md:39 closes the same section with "Coverage of lines is a weak proxy; coverage of behaviours is the target."

**Why it's a tradeoff:** Both sentences make the same underlying claim (line coverage ≠ real coverage), but they serve different structural roles: line 29 frames why enumeration matters before the list of input classes, and line 39 is a closing aphorism that pivots into the audit-time instruction ("enumerate the same input classes and flag every class the suite never tests as a coverage gap"). Cutting the aphorism removes the bookending rhetorical structure the section uses elsewhere (open with the failure mode, close with the operational takeaway), and the "weak proxy" phrasing is punchier and more quotable than the opening sentence. Whether this is sediment or intentional restatement-for-retention is a judgment call, not a clear duplicate to delete.

**Recommendation:** Leave as-is; the two sentences are close in meaning but distinct in function (framing vs. closing takeaway), and removing one weakens the section's structure more than it tightens the prose.

**Alternative:** Cut the standalone claim and keep only the operational half of line 39 ("At audit time, enumerate the same input classes and flag every class the suite never tests as a coverage gap."), relying on line 29 alone to carry the "coverage theatre" point.
