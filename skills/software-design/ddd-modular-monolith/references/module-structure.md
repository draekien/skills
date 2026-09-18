# Module Structure

What a module is made of, where its code sits, and what it owns. Boundaries chosen while shaping the system become real here or not at all.

## Anatomy

A module has exactly two surfaces: the contract, which other modules may reach, and everything else, which must be physically unreachable rather than conventionally private.

```
Ordering/
  contracts/        public    commands, queries, integration events, DTOs, IDs
  domain/           internal  aggregates, value objects, domain events
  application/      internal  use case handlers, transaction control
  infrastructure/   internal  persistence, external clients, migrations
```

```
✗ Shipping calls Ordering.infrastructure.OrderRepository.get(id)
✓ Shipping handles Ordering.contracts.OrderPlaced
```

### Addressing another module

| Mechanism | Shape | Trade-off |
|-----------|-------|-----------|
| Facade on the contract | `ordering.PlaceOrder(command)` | Simplest; creates a hard call-graph edge that can cycle |
| In-process message bus | `bus.Send(PlaceOrder{...})` | Same edge, but the caller never names the callee's type |
| Integration event | `OrderPlaced` published via outbox | Decouples the call graph entirely; costs eventual consistency |

Pick per interaction, not per project; `integrate` mode carries the decision rule.

## Layout

Layout decides what *stops* a violation, which matters more than tidiness.

| Layout | Separate build unit per module | What refuses a violation |
|--------|-------------------------------|--------------------------|
| Build unit per module | Yes | The build itself — no declared reference means no access, before any test runs |
| Directory per module, one build unit | No | Static analysis in CI |
| Namespace only | No | Nothing, until a rule is written |

Prefer a build unit per module when the toolchain offers it: it is the only option where the boundary fails closed.

```
src/
  modules/
    ordering/           each module owns its own layers internally
    shipping/
    billing/
  shared-kernel/        below every module in the graph, never beside them
  host/                 composition root — the only place that knows all modules
```

The host is always its own top-level unit. It is the one place allowed to reference every module, which is exactly why it must not be inside one.

### Layering inside a module

Four internal layers is a cost paid for behavioural complexity, not a badge every module wears. A module with no aggregate holding a real invariant and a handful of use cases gets one unit and a contracts folder. Splitting it into four is ceremony that later readers will imitate.

## Data ownership

Every table has exactly one owning module. This is the rule that decides whether the boundary is real.

```
✗ SELECT o.total, c.name
    FROM ordering.orders o JOIN identity.customers c ON o.customer_id = c.id

✓ ordering.orders stores customer_id and a denormalised customer_name,
  kept current by handling identity's CustomerRenamed event
```

- **No foreign key crosses a module boundary.** An FK is a hard commitment that both tables live in one database forever.
- **No query joins across module boundaries** — including hand-written reports and ORM navigation properties. This is the most common failure because it is invisible in review: the schemas look separate while a single join quietly welds them.
- **Migrations are owned per module.** No module's migration touches another module's tables.
- **One physical database is fine.** Schema-per-module inside it is the normal arrangement. Co-location is a deployment detail the code must not assume.

Cross-module reporting gets its own read model, populated by handling each module's integration events — never a live join across owning schemas.

## Dependency rules

The module graph must be acyclic, and every allowed edge must have a stated direction.

| Module | May depend on | May not depend on |
|--------|---------------|-------------------|
| Shipping | `ordering/contracts`, `shared-kernel` | `ordering/domain`, `ordering/infrastructure`, `billing/*` |
| Ordering | `shared-kernel` | `shipping/*`, `billing/*` |
| Shared kernel | nothing | any module |

"Shipping may use Ordering's contract" is not enough on its own. Without a stated direction, Ordering's owners will eventually add a reverse dependency on Shipping's contract to solve one problem, and the pair cycles. Write the direction down in the module map; a cycle that exists is nearly impossible to remove later.

**Shared kernel discipline**: cross-cutting plumbing only — a base entity type, an integration-event marker, a clock. No business logic, no persistence. A shared kernel that absorbs genuinely shared business concepts becomes a second core that every module depends on. Duplicating a small value object in two modules is usually cheaper than that.

## Anti-patterns with their signatures

| Anti-pattern | Signature |
|--------------|-----------|
| Distributed monolith in one process | One business change touches three modules in lockstep through chained synchronous calls — all the coordination cost of services, none of the deployability |
| Cross-module repository access | A module constructs another module's repository directly instead of calling its contract |
| Static back-channel | A static context, cache or registry written by one module and read by another. Invisible to every import-graph analyser, because a static is not a declared dependency |
| Container as bypass | One shared composition root lets any module resolve any other module's internal service. Give each module its own registration, composed by the host |
| Shared dumping ground | `Common`, `Shared`, `Core` holding business types every module imports and which import business types back |
| God type | Almost everything depends on one type; it can neither change nor move |

The last three are the ones that survive a review of the import graph, because none of them show up as an import. Check for them by name.
