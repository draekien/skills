# Command-Query Separation (CQS)

A function either changes state (command) or returns data (query) — never both. Mixing the two makes each concern impossible to reason about independently and turns call sites into implicit side-effect chains.

```
// prefer — separated
function currentCount(): return counter        // query: no side effects
function resetCounter(): counter = 0           // command: no return value

// avoid — caller cannot observe state without triggering a mutation
function consumeAndGetNext():
  value = counter
  counter = 0
  return value
```

Exceptions: building a stack's `pop` or a channel's `receive` — where atomicity is the point — are acceptable. Outside those cases, the question "what does this return?" and "what does this change?" should have one answer each.
