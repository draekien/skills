# Define Errors Out of Existence

Design data structures and APIs so that invalid states are unrepresentable. When the wrong thing cannot be expressed, an entire class of bugs becomes impossible rather than merely detected.

```
// prefer — the type prevents the invalid state
type NonEmptyList<T> = { head: T, tail: T[] }
function process(items: NonEmptyList<T>): ...   // no empty-list check needed

// avoid — valid type admits invalid state; callers must remember to guard
type List<T> = T[]
function process(items: List<T>):
  if items.length == 0: raise Error("list must not be empty")
  ...
```

When a runtime check is unavoidable, push it to the system boundary where untrusted data enters. Once data is inside the system and has passed that boundary, trust the type.
