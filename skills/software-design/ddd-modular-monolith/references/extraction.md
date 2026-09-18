# Extraction

Pulling a module out into its own deployable, and the reverse problem — modularising a codebase that never had boundaries.

## Should it be extracted at all

Extraction buys independent deployment and independent failure, and pays for it in latency, partial failure and versioned contracts. The trade is worth making only for a reason that survives being written down.

| Legitimate | Illegitimate |
|------------|--------------|
| Load profile diverges sharply from the rest of the system | Perceived coupling that is actually a bad module boundary |
| Deploy cadence differs by an order of magnitude | Microservices as the modern default |
| A team is blocked waiting on another team's release | Resume-driven architecture |
| Compliance or availability requirements differ materially | "It will scale better" with no measured limit |
| A real workload needs a different runtime or storage engine | |

The first illegitimate reason is the one experienced engineers get wrong most often. Coupling that hurts inside one process will hurt more across a network — extraction adds a boundary, it does not fix a badly placed one. Fix the module first; then ask whether extraction still has a reason.

Teams have consolidated services back into a single deployable and improved on every measure that mattered to them — deploy time, test duration, defect rate, infrastructure cost — while accepting weaker fault isolation in exchange. Extraction is a case-by-case call about one module's workload, never a direction of travel.

## Readiness

Every row must pass. A single failing row means the answer is "not yet", and names the work.

| Signal | Not ready | Ready |
|--------|-----------|-------|
| Call direction | Calls run both ways in one request path | One direction only |
| Call granularity | Called many times per request, or per row | Coarse-grained: roughly one call per request, or asynchronous |
| Shared tables | A query joins across the boundary, or a foreign key crosses it | Every table has one owning module; no foreign key crosses |
| Transactions | One transaction commits writes on both sides | Each side commits its own; cross-boundary consistency is already eventual |
| Shared kernel | Both sides import and write the same mutable model | Anything shared is small, stable, and effectively read-only |
| Contract stability | The interface changed in most recent release cycles | Unchanged across several cycles; call sites are few and enumerated |
| Ownership | Several teams routinely edit the module | One team owns every read and write |

The foreign key row is the sharpest gate. If it is not yet clear which side would own the referenced table, the module is not ready and no amount of interface work changes that.

## Sequence

Order matters more than any individual step.

```
1. Data        give the module exclusive ownership of its tables
               remove cross-boundary foreign keys and joins
               a transitional view or replication feed is a bridge, not a destination

2. Contract    introduce the interface the service will expose — still in-process
               route every internal caller through it
               build the new implementation behind the abstraction, delete the old
               → at this point the module is extractable and nothing has moved

3. Network     stand the module up as its own deployable
               route calls to it, run both in parallel, compare outputs, cut over
               decommission the in-process implementation
```

Doing it in the reverse order is the classic failure. Cut the network boundary before the data is untangled and a distributed transaction appears on day one, with production traffic live and no clear answer to which side owns which row. Cut it before the contract has proven stable in-process and every contract change becomes a cross-deployment coordination problem instead of a single-repository refactor.

## What changes at the network boundary

Each of these must be designed before cutover, not discovered after.

| Was | Becomes |
|-----|---------|
| A call always returns | It can time out, half-complete, or return stale data — retries need idempotency, or a retried charge double-charges |
| Microsecond call cost | Millisecond cost with a long tail; per-row call patterns that were invisible become the dominant cost |
| One transaction across both sides | Eventual consistency, an outbox, and compensating actions instead of rollback |
| One process to debug | A request spanning processes — correlation and tracing become mandatory, not nice to have |
| Interface changes recompile atomically | Two independently deployed sides; the contract needs versioning and backward compatibility |
| Tests exercise both sides in one process | Contract tests, test doubles, and a parallel run against real traffic before trusting the new side |

## Modularising an existing mess

The mirror problem: no boundaries exist, and a rewrite is not an option.

**Get visibility before perfecting anything.** Assign every existing file or type to exactly one intended module, in one pass, accepting that almost no module has a clean boundary yet. A complete rough map beats one immaculate module and an unmapped remainder — it is what makes the next cut arguable.

**Cut for leverage, not purity.** The first module should be one where ownership is clear and the pain is measurable. Perfect boundaries in a quiet corner teach nothing and change nothing.

**Find the seams.** A seam is a place where behaviour can be altered without editing in that place — an injection point, an overridable method, an existing interface. Seams are where an abstraction can be inserted without a large rewrite.

**Characterise before refactoring.** Legacy code has no spec. Write tests that record what it actually does, bugs included; their job is to protect existing behaviour against unintended change, not to assert correctness.

**Never a long-lived branch.** Every step ships on its own. The alternative is the multi-month restructure that never lands and is eventually abandoned with the codebase in a third state, worse than either.

**Stop the mess growing while you work** — baseline the current violations and fail only on new ones, the way `enforce` mode does. New code obeys the boundary from the first day; old code is cleaned module by module.

Adoption is the constraint, not tooling. Rules imposed over the momentum of everyone else's work get switched off; rules that solve a pain those people already feel survive.
