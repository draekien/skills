# steelman

## Terminology drift for the output artifact ("case" / "argument" / "the steelman")

The body uses three different words for what is produced — "the strongest possible case" (line 7), "a genuine advocate case" (line 9), "balance the argument" and "Reason as if the target is correct" context (line 11), and "Return the steelman directly ... just the argument ... each additional paragraph carries a distinct argument" (line 13).

**Why this is a tradeoff, not a clear-cut fix:** "argument" is doing two distinct jobs in the current text, not one. In "Return the steelman directly ... just the argument" it means the whole output (synonymous with "case"/"the steelman"). In "each additional paragraph carries a distinct argument" it means an individual claim or line of reasoning *within* the output — a part, not the whole. A mechanical find-and-replace to a single term (e.g. "the steelman" everywhere, as the raw finding suggested, swapping the second usage to "point") would need to introduce a *new* term ("point") to cover the part/whole distinction that "argument" was already quietly carrying. That's a real terminology decision, not a typo fix, and it affects how the subagent parses "one steelman, made of multiple arguments" versus flattening everything to "steelman."

**Recommendation:** Keep "the steelman" (or "case" — pick one) for the whole output, and introduce one distinct, deliberately-chosen term for the sub-unit (e.g. "argument" or "point") rather than reusing "argument" for both. Concretely: reserve "case" or "the steelman" for the whole deliverable, and use "argument" only for an individual line of reasoning within it (as line 13's second usage already does) — then fix line 11's "balance the argument" to "balance the case" (or "the steelman") since that instance means the whole, not a part.

**Alternative:** Accept the current dual meaning of "argument" as acceptable natural-language overloading (whole vs. part is a common English pattern, e.g. "the report" vs. "a point in the report") and leave it unchanged, only tightening the line 9 vs line 7 "case" wording for consistency.
