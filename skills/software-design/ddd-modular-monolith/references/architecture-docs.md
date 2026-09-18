# Architecture Docs

Two documents under the resolved architecture directory. The module map is the shared state every mode reads; a module spec covers one module in depth.

```
docs/architecture/
  module-map.md      the system: modules, dependencies, data ownership, contracts
  ordering.md        one module: subdomain type, aggregates, contract, decisions
  shipping.md
```

Write only the sections the scope has content for. An empty section invites the next agent to invent something to fill it.

## module-map.md

### Modules

One row per module. The subdomain type drives how much modelling the module deserves.

```markdown
| Module | Bounded context | Subdomain | Owns |
|--------|-----------------|-----------|------|
| Ordering | Ordering | core | Placing and cancelling orders, order lifecycle |
| Shipping | Fulfilment | supporting | Dispatch, carrier booking, tracking |
| Payments | Payments | generic | Charging and refunding via the provider |
```

### Dependencies

Every allowed edge, with its direction and mechanism. An edge absent from this table is forbidden.

```markdown
| From | To | Via | Reason |
|------|----|-----|--------|
| Shipping | Ordering.contracts | `OrderPlaced` event | Creates a shipment once an order is placed |
| Ordering | Payments.contracts | direct call | Cannot confirm an order without an authorisation result |
| Payments | — | — | Leaf; depends on no module |
```

### Data ownership

```markdown
| Schema or table group | Owner | Notes |
|-----------------------|-------|-------|
| `ordering.*` | Ordering | No foreign key leaves this schema |
| `shipping.*` | Shipping | `customer_name` denormalised from `CustomerRenamed` |
| `reporting.*` | Reporting | Projection only; never written by another module |
```

### Contracts

Each module's published contract, listed so a reader can tell contract from internals without opening the code.

```markdown
**Ordering**
- Commands: `PlaceOrder`, `CancelOrder`
- Queries: `GetOrderSummary`
- Events: `OrderPlaced { orderId, placedAt }`, `OrderCancelled { orderId, reason }`
```

### Layout and enforcement

The physical arrangement and what currently refuses a violation — including what it does not catch.

```markdown
Build unit per module under `src/modules/`; host in `src/host/`.

Enforced: reference and direction rules, in the existing test suite.
Not enforced: cross-schema queries in hand-written reports — reviewed manually.
```

### Refinement record

Every finding from every round, applied or rejected with a reason. Stops a later round, or a later session, re-raising a settled point.

```markdown
**Applied**
- *Data ownership* — `shipping` read `ordering.orders` directly; replaced with a denormalised column fed by `OrderPlaced`.

**Rejected**
- *Sizing* — splitting Ordering into Ordering and Pricing. Rejected: pricing rules change for the same business reasons as ordering rules, so the split would violate the change test.
```

## A module spec

```markdown
# Ordering

Core subdomain. Owns the lifecycle of an order from placement to completion.

## Aggregates

**Order** — consistency boundary for "an order's lines must total its recorded amount".
Holds `OrderLine` children. References `CustomerId` and `PaymentId` by identity only.

## Contract

Commands: `PlaceOrder(customerId, lines) -> OrderId`
Queries:  `GetOrderSummary(orderId) -> OrderSummary`
Events:   `OrderPlaced { orderId, placedAt }`

## Dependencies

- `Payments.contracts` — direct call, authorisation must resolve before an order is confirmed.

## Data

Owns `ordering.*`. Denormalises `customer_name` from `CustomerRenamed`.

## Decisions

**Eventual consistency with Billing** — invoice creation reacts to `OrderPlaced` in its own transaction rather than sharing Ordering's. A failure to invoice must not fail order placement.

## Rejected alternatives

**Order and Invoice in one aggregate** — rejected: no invariant requires them to be consistent in the same instant, and it would put two teams' changes in one lock.

## Refinement record

**Applied**
- *Aggregate sizing* — `Order` held the shipment schedule; moved to Shipping, referenced by id.
```

The **Decisions** and **Rejected alternatives** sections carry the reasoning. Without them the next reader sees only the outcome and re-opens every settled question — most damagingly the subdomain type, which is what licenses a supporting module to stay CRUD.
