# Names as Documentation

Names should communicate intent so completely that a comment explaining *what* becomes redundant. If a name needs explanation, it needs changing.

```
// prefer — intent readable without context
function calculateMonthlyInterest(principal, annualRate)
daysUntilExpiry = expiryDate - today

// avoid — reader must decode intent from surrounding code
function calc(p, r)
d = e - t
```

A name that is hard to choose is a signal that the underlying concept is unclear or conflated. Difficulty naming is a design smell, not a language problem.
