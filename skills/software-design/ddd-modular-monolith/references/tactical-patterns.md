# Tactical Patterns

The inside of one module. Everything here is scoped by the first decision: a module's subdomain type decides how much modelling it deserves.

## Match the modelling style to the subdomain

| Subdomain | Modelling style | Test |
|-----------|-----------------|------|
| Core | Rich domain model — aggregates, value objects, domain events | Rules branch and interact, and change often |
| Supporting | Transaction script or active record | Rules are field validation and a few conditionals |
| Generic | Buy, or the thinnest possible CRUD | Nobody in the business would argue about the rules |

```
✗ CountryCode aggregate + CountryRepository + CountryRenamed event + CountryFactory
  — a lookup table of 195 rows nobody edits

✓ LoanUnderwriting gets the full treatment: eligibility rules, rate tiers and
  collateral checks genuinely interact
  Countries gets a table and a read query
```

Applying one style uniformly across every module is the failure this table exists to prevent. Decide per module, and record the choice in the module spec — the next agent will otherwise "improve" the CRUD module into an aggregate.

## Aggregates

### The boundary is the true invariant

An aggregate exists to hold a rule that must be true *atomically* — not eventually. Hunt invariants, not relationships: ask what must never be observed in an inconsistent state by anyone, right now.

```
Invariant: a delivery stop cannot arrive before the pickup stop has departed.

✓ Shipment aggregate { PickupStop, DeliveryStop }
    Shipment.Arrive(stopId, at)   — checks both stops, one method, one boundary

✗ PickupStop and DeliveryStop as separate aggregates with separate repositories
    — the rule now lives in every application service that touches a stop,
      or in none of them
```

"These things are related" is not an invariant. `Order` and `Invoice` are related; nothing breaks if the invoice is written a second later.

### Four rules

1. **Model true invariants in consistency boundaries** — one aggregate per rule that must hold atomically.
2. **Design small aggregates** — default to the smallest aggregate that holds its invariant. Grow it only when a *second* true invariant cannot be enforced any other way. Never grow it for query convenience.
3. **Reference other aggregates by identity only** — `Delivery.droneId: DroneId`, never `Delivery.drone: Drone`. This rule is what lets a module boundary later become a service boundary without remodelling.
4. **One aggregate per transaction; eventual consistency between aggregates** — when a rule spans two aggregates, raise a domain event and let a handler update the other in its own transaction. Do not widen the transaction.

```
✗ DeliveryService.Complete(id):
      delivery.Complete()
      account.AddCharge(delivery.Fee)     — second aggregate, same transaction
      commit()

✓ DeliveryService.Complete(id):
      delivery.Complete()                 — raises DeliveryCompleted
      commit()
   BillingHandler.On(DeliveryCompleted):
      account.AddCharge(...)              — its own transaction
```

### Sizing failures, both directions

| Direction | Symptom | Signature in code |
|-----------|---------|-------------------|
| Too large | Lock contention, slow loads, unrelated updates competing | One aggregate root loading every child row of a table on every write; two users editing unrelated fields conflicting |
| Too small | The invariant is enforced nowhere, or copy-pasted | The same guard clause appearing in three application services before they call the same method |

The too-large case is usually survivable and measurable. The too-small case is silent: the rule is simply not enforced, and nothing fails until data is already wrong. When uncertain, prefer the smaller aggregate only if the invariant genuinely has one owner.

### When to break the rules

- **Batch creation** — creating many instances in one transaction is fine when it is semantically identical to creating them one at a time.
- **No asynchronous infrastructure** — with no message dispatch, no background worker and no timer, eventual consistency cannot actually be implemented. Accept a multi-aggregate transaction and keep the set of touched aggregates minimal, rather than pretending.
- **A legacy transaction already spanning everything** — minimise what is touched inside it; do not model around it.

Record any break and its reason in the module spec. An unexplained multi-aggregate transaction reads as a bug to every later reader.

## Entity or value object

One test: **if two instances have different attribute values but the same identity, are they still the same thing?**

```
✓ Person is an entity      — two people named "Bob Smith" born the same day
                             are different individuals
✓ Money is a value object  — Money(100, "AUD") is interchangeable with any
                             other Money(100, "AUD")
✗ Money with a MoneyId     — surrogate identity on an interchangeable value
                             is pure ceremony
```

**Value object is the default.** Promote to entity only when identity must be tracked over time. `Address` is a value object — until the domain must answer "which address did we ship to on the third, even though the customer's address has changed since", at which point the shipped-to address needs its own identity.

Value objects are immutable: a change returns a new instance.

```
✗ money.Add(other)        — mutates in place
✓ money.Plus(other) -> Money
```

The counter-failure is real: not every immutable-shaped bag of fields is a value object. The test is whether a domain expert names the concept, not whether the data happens to be immutable.

## Where logic lives

Try in order; stop at the first that fits.

1. **On the entity or value object** — logic needing only that object's own state.
2. **In a domain service** — logic spanning several aggregates that belongs to none of them, and is still domain logic (scheduling, pricing across catalogues, routing).
3. **In an application service** — orchestration only: load, call, save, publish. No business rules.

```
✗ DeliveryAppService.Cancel(id):
      d = repo.Get(id)
      if d.Status == InTransit: throw CannotCancel()   — domain rule, wrong layer
      d.Status = Cancelled
      repo.Save(d)

✓ DeliveryAppService.Cancel(id):
      d = repo.Get(id)
      d.Cancel()                                       — the rule lives in Cancel()
      repo.Save(d)
```

An anaemic model — entities of getters and setters, all behaviour in services — is a procedural design wearing object syntax. It is the correct design for a supporting subdomain and the wrong one for a core subdomain; the subdomain table above settles which.

## Repositories

**One repository per aggregate root.** Child entities have none — they are reachable only by loading the root.

```
✓ ShipmentRepository { get, save, findScheduledBefore }
✗ PickupStopRepository            — child entity, not a root
```

What a repository must not expose:

```
✗ FindAll() -> QueryBuilder<Shipment>    — callers compose arbitrary queries;
                                           the contract promises nothing
✗ Repository<T> { GetById, Save, Delete } as the public type for every aggregate
✓ ShipmentRepository {
      get(id: ShipmentId) -> Shipment
      save(shipment: Shipment)
      findOverdue(asOf: Instant) -> List<Shipment>
  }
```

Every method takes or returns whole aggregates, and method names are domain vocabulary rather than CRUD verbs. A generic base type is acceptable as a private implementation detail; it is never the published contract.

`save` stages; it does not commit. The transaction is owned by the application service, which is also where "one aggregate per transaction" becomes structurally checkable.

## Domain events and integration events

| | Domain event | Integration event |
|---|---|---|
| Raised by | An aggregate, inside its transaction | A handler, after that transaction commits |
| Audience | Handlers inside the same module | Other modules |
| Named in | The module's internal language | The published language |
| Changes when | The aggregate's internals change | Never, without versioning |

The two are different objects even when one triggers the other. Publishing a domain event across a module boundary is the leak: every internal change then has to be renegotiated with every consumer.

```
✓ ShoppingCart aggregate raises        CartConfirmed            (internal)
  handler loads what else it needs and publishes
                                        OrderPlaced             (public contract)

✗ handler publishes CartConfirmed directly to other modules
```

**Collection and dispatch**: aggregate methods append events to an internal list rather than dispatching inline; the application service drains that list only after a successful commit. Dispatching inline publishes events for changes that then roll back.

Cross-module publication needs the outbox, which `integrate` mode covers.

## Factories and specifications

Both earn their place or get deleted.

```
✗ ShipmentFactory.Create(a, b) { return new Shipment(a, b) }     — ceremony
✓ Order.CreateExpedited(...) / Order.CreateStandard(...)
  — valid construction branches into two different initial states, and a
    constructor cannot express the choice safely

✗ class OverdueSpecification { isSatisfiedBy(d) { return d.dueDate < now } }
  used in exactly one place
✓ the same specification used to filter a repository query AND to re-check a
  single loaded aggregate before escalating — one rule, two call sites
```

A specification also earns its place when the business names the rule, or when rules must combine.
