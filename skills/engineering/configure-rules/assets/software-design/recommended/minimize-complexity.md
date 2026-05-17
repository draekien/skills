# Minimize Complexity

Complexity is the primary cost driver in software. Every module, parameter, layer of indirection, and abstraction adds cognitive overhead — introduce them only when they demonstrably reduce net system complexity.

```
// prefer — direct
function formatName(first, last):
  return first + " " + last

// avoid — indirection adds overhead with no benefit
class NameFormatter:
  constructor(strategy = DefaultNameStrategy())
  function format(name: NameRecord): string
```

The question to ask before adding any abstraction: does this make the system as a whole simpler, or does it just move complexity somewhere less visible? Moving complexity is not the same as eliminating it.
