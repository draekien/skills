# Avoid Hasty Abstractions (AHA)

Duplication is cheaper than the wrong abstraction. Do not unify two pieces of code until the pattern they share is fully understood — a premature abstraction is harder to undo than duplicated code.

```
// prefer — duplicate until the right seam is clear
function renderAdminButton(label):
  return Button(label, style: "admin")

function renderGuestButton(label):
  return Button(label, style: "guest")

// avoid — unified too early around the wrong axis
function renderButton(label, role, size, variant, iconPosition, ...):
  // every new caller warps the interface further
```

The sunk-cost of an existing abstraction makes it feel wrong to break it apart. Recognise this pressure and override it: if an abstraction must grow a new parameter or flag to accommodate the next use case, the abstraction has the wrong shape and should be reconsidered.
