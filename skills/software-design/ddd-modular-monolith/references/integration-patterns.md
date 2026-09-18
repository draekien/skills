# Integration Patterns

How one module talks to another. Every rule here exists to stop a monolith acquiring the coordination cost of distributed services while keeping none of the benefits.

## Choosing the mechanism

Take the cheapest option that satisfies the actual requirement.

| Mechanism | Use when | Cost |
|-----------|----------|------|
| Direct call to the public contract | The caller cannot proceed without the answer — validating stock before confirming an order | Temporal coupling: the callee's failure becomes the caller's failure |
| Event, dispatched in the same transaction | A side effect must happen in the same unit of work and needs no answer | Still couples lifetimes; a failing handler can fail the caller |
| Event, dispatched asynchronously | The side effect can lag and the caller needs no result — emailing a receipt | Eventual consistency; handlers must tolerate duplicates and reordering |
| Module-owned read model | A cross-module view is needed for reads only | Staleness, and a projection to keep current |
| Anticorruption layer | The other side's model does not fit yours, or it is external or legacy | Translation code to own |

The decision rule, in order:

```
Can the caller proceed without an answer?
  yes → asynchronous event
  no  → does the callee's own model already say what you need, unmodified?
          yes → direct call to its public contract
          no  → anticorruption layer over that call
```

Never reach for a shared table because both modules happen to use one database.

## The contract surface

```
✗ published: Order              — the aggregate itself: internal status enum,
                                  child collections, persistence annotations
✓ published: OrderSummary { orderId, status, total }   — a hand-written DTO
```

| May cross | Must never cross |
|-----------|------------------|
| Commands, queries, integration events | Aggregates and entities |
| DTOs written specifically for the contract | Repositories and query builders |
| Opaque identifiers | Internal enums and status codes |
| | Persistence or ORM types |

Keep the surface as small as it can be: every published field is a promise. A contract may add optional fields indefinitely; it may never repurpose or remove a field a consumer might read.

```
✗ OrderPlaced { orderId, customerId, lines[], shippingAddress, paymentMethod, ... }
   — forty fields because each new consumer asked for one more; every change
     now renegotiates with every subscriber

✓ OrderPlaced { orderId, placedAt }
   — subscribers needing more call the owning module back
```

A shared package holding every module's DTOs, imported by all of them, recreates the coupling the boundary was for. Each module publishes its own contract.

## Events

**Naming** — past tense, business language, never a command in disguise.

```
✗ OrderUpdated          what changed, and why would anyone care?
✗ UpdateShippingStatus  imperative — this is a command
✓ OrderCancelled
✓ ShipmentDispatched
```

**Payload** — the trade is explicit, so make it deliberately.

```
Thin:  ShipmentDispatched { shipmentId }
       Subscribers call back for detail. Low coupling; the business flow is
       invisible in code — it can only be seen by watching the system run.

Fat:   ShipmentDispatched { shipmentId, carrier, trackingNumber, estimatedDelivery }
       Subscribers never call back: faster, and resilient to the publisher being
       down. Costs duplicated data and a wider contract to keep stable.
```

Default to thin, and go fat only where a subscriber's resilience to the publisher genuinely matters.

**Idempotency** — a handler must tolerate the same event twice and events out of order, unless strict ordering has been paid for.

```
handle(event):
  if consumed.contains(event.id): return
  apply(event)
  consumed.insert(event.id)      — same transaction as apply()
```

**Choreography or orchestration** — choreography suits two or three steps. Past that, no single place knows where a given order is in its lifecycle, and orchestration by an explicit process manager wins.

```
Choreography:  OrderPlaced → Billing charges → PaymentCaptured
               → Shipping creates shipment → ShipmentCreated → Notifications emails

Orchestration: OrderFulfilment commands each step and knows the current state
```

## Consistency

```
✗ transaction {
     orders.save(order)        — Orders' table
     billing.save(invoice)     — Billing's table, same physical database
  }
  Compiles. Passes tests. Orders' code now knows Billing's schema, and the
  day the databases split, it breaks.
```

Transactional consistency is allowed *within* one module's aggregate boundary. Anything crossing a module boundary is eventually consistent, even when both tables sit in the same database instance. Co-location is a deployment fact the code must never assume.

**The outbox** earns its place in a monolith, not only across a network: it makes "commit my own change" and "hand off the event" atomic, so a crash between the two neither loses the event nor fires it twice.

```
transaction {
  update orders set status = 'placed' where id = ...
  insert into outbox (type, payload) values ('OrderPlaced', ...)
}
— a separate relay publishes from the outbox and marks each row dispatched
```

Outbox delivery order follows commit order, and parallel transactions commit out of order. Consumers must not assume delivery order equals business order.

A multi-module workflow needs a process manager with **compensating actions** the moment any step can fail after an earlier step committed. Rollback across modules does not exist; refunding does.

## Queries across modules

```
✗ SELECT o.id, o.total, i.status
    FROM orders.order o JOIN billing.invoice i ON i.order_id = o.id
   Works today. Billing renames a column tomorrow and Orders breaks at
   runtime with nothing to catch it at build time.
```

A cross-module join makes the *schema* the contract instead of the module's API. Three alternatives, against an "orders with invoice status" screen:

| Approach | Shape | Trade-off |
|----------|-------|-----------|
| Composition in the caller | Orders fetches summaries, then asks Billing for statuses by id, joins in memory | Simple; degrades as the result set grows |
| Module-owned projection | Orders handles `InvoiceStatusChanged` and keeps its own denormalised column | Fast reads; briefly stale |
| Reporting module | A module owning cross-cutting read models, fed by events | Right for analytics; wrong for live transactional screens |

## Anticorruption layers

Between two modules you own, an ACL earns its place when one module's vocabulary would otherwise contaminate the other's — Orders' *payment* is not Billing's *invoice*, related though they are. Against an external or legacy system it is close to mandatory, so that a vendor change touches one translation file instead of every call site.

```
✓ BillingTranslator.toPaymentState(legacyCode):
      0    → Unpaid
      1, 2 → Paid
      3    → Refunded
      else → Unknown
```

## Failure modes

| Failure | Signature |
|---------|-----------|
| Chatty synchronous chain | `Orders.Place` calls Billing calls Inventory calls Shipping, all synchronous — one request now carries the combined latency and failure rate of four modules |
| Event as disguised RPC | `InvoiceOverdue` published because the publisher wants the subscriber to halt a shipment — a command wearing past tense; the payload carries nothing the subscriber needs to decide |
| Transaction spanning modules | One commit covering two modules' tables because they share a database |
| Subscribing to another module's domain events | A subscriber handling an event meant for the publisher's own aggregates; any internal refactor breaks it |
| Shared DTO package | One contracts package every module imports — a single change recompiles and redeploys everything in lockstep |
| Payload bloat | An event grown from two fields to forty, one consumer request at a time |

Each of these looks identical to its correct form until one question is asked: is the thing crossing the boundary a deliberate, versioned public contract, or an internal detail that leaked? When in doubt, return to the contract surface and make it smaller.
