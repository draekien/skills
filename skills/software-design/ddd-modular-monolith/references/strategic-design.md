# Strategic Design

Carving the monolith. Everything here decides what the modules *are* before any code exists.

## Module equals bounded context

Treat this as a structural rule, not an analogy.

```
Module  ==  Bounded Context
              owns 1..N Aggregates
              organised internally as packages (domain, application, infrastructure, contracts)
```

A package is code organisation *inside* one context. `meetings.domain` and `meetings.application` are not two contexts.

The same word carries different models in different contexts, and that is the point:

```
Order in Fulfilment  { pickList, warehouseLocation, shippingLabel }
Order in Billing     { invoiceLines, paymentTerms, taxTreatment }
```

Forcing one shared `Order` used verbatim by both is under-bounding — the model then serves neither. Record both definitions in the project's ubiquitous language rather than collapsing them.

## Classify the subdomain first

| Type | Test | Investment |
|------|------|------------|
| Core | Differentiates the business; rules are argued about | Rich model, strongest engineers, full tactical patterns |
| Supporting | Business-specific but simple rules | CRUD or transaction script |
| Generic | Could be bought off the shelf without losing advantage | Conformist wrapper over the vendor's model — or buy it |

```
Meetings      core        rich aggregates, invariants in the domain model
Administration supporting  CRUD over a few tables
Payments      generic     conformist wrapper; do not grow a competing model
UserAccess    generic     conformist wrapper
```

The failure specific to monoliths: no deployment boundary hurts, so every module gets equal ceremony. A generic module that grows its own `User` aggregate competing with the identity provider's is the signature.

## Find the boundaries

Four techniques, used together. No single one is reliable.

**The change test** — the strongest single heuristic. A typical business change should touch exactly one module.

```
Change: "add coupon codes to checkout"
  touches Ordering only            → boundary holds
  touches Ordering AND Catalog     → boundary is wrong
```

**Business capability grouping** — list what the business does (place order, manage catalogue, handle payments, ship orders, generate invoices, handle refunds), then group by what changes together. Capabilities, never entities.

**Linguistic boundary** — where sales, logistics and accounting use different words for what appears to be the same thing, a context ends. Domain experts disagreeing about what an event means is itself the signal.

**Volatility and coupling** — two candidate modules that always change for the *same business reason* are one context. Things that must co-change belong close together; things that change for different reasons belong apart.

Triangulate these against existing team ownership and data ownership. A boundary that cuts across a team is a boundary that will erode.

## Boundary smells

| Smell | Signature |
|-------|-----------|
| Entity-per-module | `OrderModule`, `CustomerModule`, `ProductModule` — "place an order" now needs synchronised calls across three modules |
| Process-stage modules | `Lead`, `Quote`, `Order`, `Invoice` as four contexts — changing how discounts work cuts across every one |
| Layer-shaped modules | `ApiModule`, `ServicesModule`, `DataAccessModule` — technical rather than business capability |
| Shared dumping ground | `Common`, `Shared`, `Core` holding business concepts every module imports |
| Anaemic module | The module is a facade proxying calls elsewhere; the logic lives outside it |
| Under-bounding | One `Customer` table used verbatim by Sales, Support and Shipping |
| God module | Almost everything depends on one type; it can never change or move |

The shared dumping ground deserves special suspicion in a monolith: nothing physically stops it growing. Justify a shared module only when several teams get real reuse from a genuine capability. Duplicating a small value object in two modules is usually cheaper than a shared kernel that accumulates business meaning.

## Relationship patterns between modules

| Pattern | Verdict inside one deployable |
|---------|-------------------------------|
| Open host service | The normal case — the module's public contract |
| Published language | The shared event and DTO schema used for integration |
| Customer/supplier | Normal between a core module and a supporting one |
| Conformist | Correct default for a generic-subdomain module |
| Anticorruption layer | Needed at the seam between a core module and any generic or legacy module, even in-process |
| Partnership | Often redundant — one release train already forces coordination |
| Shared kernel | Highest-risk pattern here. Restrict to zero-business-logic plumbing |
| Separate ways | Legitimate but rare — if truly unrelated, ask why it ships in the same deployable |
| Big ball of mud | The default failure mode, not an option |

A service boundary is enforced by the network. A module boundary is enforced only by what the build, the compiler, or a test refuses to allow — which is why every pattern above has to be backed by a check `enforce` mode can emit.

## Sizing

Merge two modules when the dependencies between them are *numerous*, *strong* and *unstable* — all three together mean the split is wrong. Split a module when it bundles capabilities that do not co-change, or when it has grown past roughly fifteen to twenty entities.

| Direction | Cost |
|-----------|------|
| Too many modules | Inter-module chatter explodes; a cross-module saga replaces what should be one local transaction — the coordination cost of microservices with none of the independent deployability |
| Too few modules | Monoliths within the monolith; the autonomy that justified modularising is gone |

Start from capabilities, not from a target count. A system with four well-owned modules beats one with twelve that all call each other.

## What to be honest about

Boundary discipline is harder to sustain than most writing implies. The common claim is that a well-modularised monolith keeps later extraction cheap; the honest counter-position is that boundaries erode in practice and the easy split rarely happens. Design as if extraction will never happen and the boundaries must pay for themselves today — in comprehension, ownership and blast radius. Extraction, if it comes, is a bonus.
