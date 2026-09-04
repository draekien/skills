# Design Principles

## Strict Rules

Enforced as hard constraints during the interview. A design decision that violates a strict rule must be blocked and revised before proceeding.

### Information Hiding

Implementation decisions stay private inside the module that makes them. Callers must not depend on *how* a result is achieved — only *what* the module provides. When an internal change forces caller changes, information has leaked.

```
// prefer — interface exposes the concept, not the mechanism
cache.get(key)
cache.set(key, value, ttl)

// avoid — storage technology leaks through the interface
cache.redisClient.hget("cache_ns", key)
cache.redisClient.expire("cache_ns:" + key, ttl)
```

### Law of Demeter

Only communicate with immediate neighbours. A module should call methods on objects it owns, objects passed to it, or objects it created — not objects retrieved by navigating through another object's internals.

```
// prefer — ask the neighbour to do the work
total = order.calculateTotal()

// avoid — reach through order → customer → address → country
taxRate = order.customer.address.country.taxRate
```

Each dot in a chain that crosses an ownership boundary is a hidden dependency on an intermediate's internal structure.

### Define Errors Out of Existence

Design data structures and APIs so that invalid states are unrepresentable. When the wrong thing cannot be expressed, an entire class of bugs becomes impossible rather than merely detected.

```
// prefer — the type prevents the invalid state
type NonEmptyList<T> = { head: T, tail: T[] }
function process(items: NonEmptyList<T>): ...

// avoid — valid type admits invalid state; callers must remember to guard
type List<T> = T[]
function process(items: List<T>):
  if items.length == 0: raise Error("list must not be empty")
```

When a runtime check is unavoidable, push it to the system boundary where untrusted data enters.

### Avoid Temporal Decomposition

Do not structure modules around the order operations execute. Structure them around the information each module owns and hides. Execution-order decomposition produces shallow, tightly coupled pipelines.

```
// prefer — one module owns the whole concept
config = Config.load(path)   // reads, parses, validates, normalises internally

// avoid — split by execution order
raw       = ConfigReader.read(path)
parsed    = ConfigParser.parse(raw)
validated = ConfigValidator.validate(parsed)
normalised = ConfigNormaliser.normalise(validated)
```

Ask: "what knowledge does this module own?" not "what does it do first?"

### Strategic Programming

Every change is an opportunity to improve the design. Interfaces must be shaped around the concept, not around one caller's immediate needs.

```
// prefer — interface designed around the concept
function parseDate(input): Date

// avoid — interface shaped around one caller's needs
function parseDateForCheckoutFlow(rawInput, userTimezone, localeOverride, legacyFormat):
```

Budget roughly 10–20% of implementation time on design quality: naming, module boundaries, eliminating special cases.

---

## Recommended Rules

Applied by the audit subagent after the spec is complete. Findings are suggestions — the user decides which to apply.

### Minimize Complexity

Complexity is the primary cost driver in software. Every module, parameter, layer of indirection, and abstraction adds cognitive overhead — introduce them only when they demonstrably reduce net system complexity.

```
// prefer — direct
function formatName(first, last): return first + " " + last

// avoid — indirection adds overhead with no benefit
class NameFormatter:
  constructor(strategy = DefaultNameStrategy())
  function format(name: NameRecord): string
```

Ask before adding any abstraction: does this make the system as a whole simpler, or does it just move complexity somewhere less visible?

### Deep Modules

A module's value is its power-to-interface ratio. Prefer a few rich abstractions that hide substantial complexity behind a narrow surface over many thin wrappers that expose every internal step.

```
// prefer — one call, all complexity hidden
store.save(record)

// avoid — caller orchestrates internal steps
store.beginTransaction()
store.validate(record)
store.writeRow(record)
store.commitTransaction()
```

A module whose interface is nearly as complex as its implementation (a shallow module) adds cognitive overhead without returning value.

### Avoid Hasty Abstractions (AHA)

Duplication is cheaper than the wrong abstraction. Do not unify two pieces of code until the pattern they share is fully understood.

```
// prefer — duplicate until the right seam is clear
function renderAdminButton(label): return Button(label, style: "admin")
function renderGuestButton(label): return Button(label, style: "guest")

// avoid — unified too early around the wrong axis
function renderButton(label, role, size, variant, iconPosition, ...):
  // every new caller warps the interface further
```

If an abstraction must grow a new parameter or flag to accommodate the next use case, it has the wrong shape.

### Command-Query Separation (CQS)

A function either changes state (command) or returns data (query) — never both.

```
// prefer — separated
function currentCount(): return counter    // query: no side effects
function resetCounter(): counter = 0       // command: no return value

// avoid — caller cannot observe state without triggering a mutation
function consumeAndGetNext():
  value = counter; counter = 0; return value
```

Exceptions: stack `pop`, channel `receive` — where atomicity is the point — are acceptable.

### Fail Fast

Detect invalid conditions at the earliest possible point and surface them with specific, actionable messages.

```
// prefer — caught immediately at the boundary
function divide(a, b):
  if b == 0: raise ArgumentError("divisor cannot be zero")
  return a / b

// avoid — silent wrong result defers the problem
function divide(a, b):
  if b == 0: return 0
  return a / b
```

Validate at system boundaries. Trust internal invariants that have already been enforced.

### Names as Documentation

Names should communicate intent so completely that a comment explaining *what* becomes redundant. If a name needs explanation, it needs changing.

```
// prefer — intent readable without context
function calculateMonthlyInterest(principal, annualRate)
daysUntilExpiry = expiryDate - today

// avoid — reader must decode intent
function calc(p, r)
d = e - t
```

Difficulty naming is a design smell — it signals that the underlying concept is unclear or conflated.

### Principle of Least Astonishment (POLA)

Software should behave exactly as a knowledgeable reader would predict from its name and context. Surprising behaviour is a design problem — fix with a better interface, not a warning in the documentation.

```
// prefer — name matches behaviour precisely
function getUser(id): return user or null

// avoid — name implies a read, behaviour silently mutates
function getUser(id):
  user = db.find(id)
  db.updateLastAccessed(id)    // caller had no reason to expect this
  return user
```

### Single Abstraction Level

Each function or module should operate at one conceptual level. Business intent and implementation mechanics must not share a function body.

```
// prefer — each function stays at its own level
function processOrder(order):
  validateOrder(order)
  chargePayment(order)
  fulfilOrder(order)

// avoid — business intent mixed with raw mechanics
function processOrder(order):
  if order.items.length == 0: raise Error("order is empty")
  db.execute("INSERT INTO charges VALUES (?)", order.total)
  smtp.send(order.customer.email, "Your order is confirmed")
```

When a function reads as a mix of high-level policy and low-level detail, extract the details into named helpers.
