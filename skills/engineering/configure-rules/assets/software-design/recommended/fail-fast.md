# Fail Fast

Detect invalid conditions at the earliest possible point and surface them with specific, actionable messages. The cost of finding a bug grows with every step it travels from its origin.

```
// prefer — caught immediately at the boundary
function divide(a, b):
  if b == 0: raise ArgumentError("divisor cannot be zero")
  return a / b

// avoid — silent wrong result defers the problem to an unknown caller
function divide(a, b):
  if b == 0: return 0
  return a / b
```

Validate at system boundaries (user input, external APIs, configuration). Trust internal invariants that have already been enforced; don't re-validate everywhere.
