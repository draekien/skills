# Enforcement

A module boundary exists only to the extent something refuses to compile, refuses to lint, or fails a test. Conventions erode; the module map's dependency graph is worth exactly what enforces it.

## Rule shapes

Six shapes cover nearly every boundary rule. Each is stated as a rule the project's own tooling can express.

| Shape | Rule | Catches |
|-------|------|---------|
| Reference | No type outside `ordering` may reference a type in `ordering/domain` or `ordering/infrastructure` | Reaching past the contract |
| Direction | `shipping` may reference `ordering/contracts`; `ordering` may not reference `shipping` at all | Reverse edges that create cycles |
| Cycle | The module graph is acyclic | The graph rotting one edge at a time |
| Surface | Only types under `ordering/contracts` are publicly visible from `ordering` | The contract widening by accident |
| Data | No query, migration or mapping in `shipping` names a table owned by `ordering` | Cross-module joins and foreign keys |
| Leaf | `shared-kernel` references no module | A second core forming |

The Data shape is the one most projects skip and the one that most often makes a boundary fictional. Express it however the stack allows — a test asserting no migration names a foreign schema, a grep over SQL and mapping files, a check on which connection a module may open.

The Surface, Data and container rules matter most, because the failures they catch — a widened contract, a cross-schema join, a shared registration — do not appear in the import graph at all. A project whose only enforcement walks imports is blind to all three.

## Emitting the rules

Detect what the project already uses before writing anything: read the build files to identify the ecosystem, then find the existing test or lint setup and match it — the same runner, the same directory, the same naming. Boundary rules belong beside the project's other tests, not in a new parallel system.

Each rule is emitted with the module map's own names, so a failure reads as a boundary violation rather than a type error:

```
✗ test name: Test_Dependencies_1
✓ test name: shipping_must_not_reference_ordering_internals
```

Wire them in as an ordinary build step that exits non-zero. A boundary check that produces a report nobody reads is not enforcement.

## No test infrastructure

Do not make a test framework a prerequisite. Reach for the cheapest thing that fails closed, in this order:

1. **What the language enforces for free.** Many toolchains already refuse a cross-boundary reference given the right layout — an internal-only package convention the compiler honours, separate build units with no declared reference between siblings, module visibility declarations. Restructuring to use one of these costs an afternoon and needs no tooling at all.
2. **A grep-based build step.** Crude and prone to false negatives, but it catches raw cross-module reaches immediately: fail the build when a file under `shipping/` names `ordering.domain`. Worth writing while the real check is still hypothetical.
3. **Ownership gating.** A per-module owners file, so any change touching another module's directory requires that module's owners to approve. Process standing in for tooling.

State plainly which of these the project is on, and what it does not catch. An honest grep plus an owners file beats an architecture-test suite that was never written.

When the project has no test setup and would benefit from one, name the architecture-rule tooling that fits its ecosystem and let the user decide — do not install anything unasked. Tooling categories by ecosystem, for that recommendation:

| Ecosystem | Category | Examples |
|-----------|----------|----------|
| JVM | Fluent architecture-rule tests | ArchUnit; module verification APIs in the framework |
| .NET | Fluent architecture-rule tests, plus project references | NetArchTest, ArchUnitNET |
| TypeScript, JavaScript | Import-graph analysis at lint time | dependency-cruiser, eslint import-boundary rules, monorepo tag rules |
| Python | Import contracts declared in project config | import-linter, tach |
| Go | Compiler-enforced visibility, plus a linter | the `internal/` package convention, go-arch-lint |
| Ruby | Static constant-reference analysis | Packwerk |

Verify the tool still exists and fits before recommending it; this table is a starting point, not a guarantee.

## Retrofitting onto an existing mess

Turning every rule on at once against a codebase with hundreds of violations produces a red build that gets switched off within a week.

Ratchet instead:

```
1. Run the rules, write every current violation to a checked-in baseline
2. CI fails only on violations absent from the baseline
3. The baseline may shrink; it may never grow
4. Enable the strict rules on one module at a time, starting where ownership is clearest
```

Partial coverage teams actually adopt beats a strict gate imposed over everyone's work. A baseline that has not shrunk in months is a signal the modularisation stalled — report it rather than quietly regenerating the baseline.
