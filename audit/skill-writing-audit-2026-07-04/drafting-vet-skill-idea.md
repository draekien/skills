# vet-skill-idea

## Terminology drift: "idea" (name/description) vs "concept" (body)

**Gap**: The skill's name (`vet-skill-idea`) and its frontmatter description call the input an "idea," but the body almost exclusively calls the same referent a "concept" (lines 8, 12, 14, 26, and the Verdict section), with a single reversion to "idea" at the very end ("reframe or drop the idea"). This violates the one-term-per-concept writing standard.

**Why it's a tradeoff, not a clear-cut fix**: "Concept" is the established leading term used throughout the body (5+ occurrences across every gate). Swapping it for "idea" means touching wording in every gate section, not a single isolated line, and risks colliding with the *other* meaning of "concept" used in the Sound-goal gate (see next item) — the two problems are entangled. This is exactly the kind of "renaming an established leading term" change that needs a deliberate pass rather than a mechanical find-replace, since related phrasing (e.g. "A concept warrants a skill only by clearing all four") would need to read naturally after the swap.

**Recommendation**: Standardize the body on "idea" (matches the skill's own name and its description, and is the word a user will naturally use when describing what they want vetted). Replace "concept" with "idea" at lines 8, 12, 14, 26, and in the Verdict section's "Once a concept passes" sentence.

**Alternative**: Standardize on "concept" instead and rename the description's "idea" to "concept" — keeps the body untouched but requires renaming the skill's own name/description, which is a bigger surface change.

## Sound-goal gate: inconsistent synonyms and a third, colliding meaning of "concept"

**Gap**: The "Sound goal, not a gamed metric" section names its two core referents with a different word almost every sentence — the true outcome is called "the real outcome" / "the point" / "the idea landing" / "the target" / "the outcome"; the gamed proxy is called "a gamed metric" (title) / "a number" / "the proxy." It also uses "concept" for a third, distinct referent (the insight the skill instills) that collides with "concept" used elsewhere in the file for the candidate pitch.

**Why it's a tradeoff, not a clear-cut fix**: Fixing this requires picking a single leading word for two (arguably three, given the "concept" collision above) different referents and rewriting the section's sentences around those choices. That's a phrasing/structure decision with several reasonable options (e.g. "outcome" vs. "goal" for the true target; "metric" vs. "proxy" for the gamed number), not a single unambiguous substitution — and it's entangled with the idea/concept decision above, since resolving one affects the vocabulary available for the other.

**Recommendation**: Use "outcome" for the true goal and "metric" for the gamed proxy (matching the section title "Sound goal, not a gamed metric"), and use "idea" (not "concept") for what the skill instills once the idea/concept rename above is applied, e.g.: "A skill should instill an idea that moves the work toward the real outcome every time it runs — not chase a metric for its own sake. Test: can the skill be satisfied while missing the outcome? If success is box-ticking rather than the outcome landing, the skill optimises the metric and forgets the outcome. Reframe it around the outcome so that using it causes the outcome, or drop it."

**Alternative**: Keep "goal" as the leading word for the true target (matching the section's own title "Sound goal") instead of "outcome," and use "score" instead of "metric" for the gamed proxy if that reads more naturally alongside "gamed."
