---
name: with-testing-principles
description: Applies established testing principles to write tests that catch real bugs, and to audit existing tests for the failure modes that pass review yet verify nothing. Language- and framework-agnostic; covers unit through end-to-end. Use when writing tests, adding coverage, or reviewing a test suite's quality — or when the user says "write tests", "add tests", "add test coverage", "review these tests", "are these tests any good", "test this".
---

A test earns its place only if it can fail when the code is wrong. Most tests that pass review fail this bar silently: they execute the code, raise coverage, and assert nothing that would break if the behaviour regressed. The job is not to produce tests that pass — it is to produce tests that would fail for the right reason. This discipline holds identically whether writing new tests or judging existing ones; auditing is just applying the same pillars to code already on the page.

The pillars below are independent. Each defends against a distinct failure, and no pillar covers for another — a test can satisfy one and still be worthless under the rest. Hold every test against all of them.

## Falsifiability

A test that cannot fail is not a test. Before trusting any assertion, establish that it bites: that some realistic defect in the code under test would turn it red.

- **At write time**, prove falsifiability through the test, never by editing the code under test. Either write the test before the implementation exists so red comes for free, or flip the expected value in the assertion, confirm the test fails, then restore it. Flipping a literal in the test is trivially reversible and touches nothing else; mutating source code to prove a point risks leaving the codebase broken and is never necessary here.
- **At audit time**, the code already exists, so falsifiability is checked by mutation: imagine a plausible bug — an off-by-one, a flipped comparison, a dropped branch, a swapped operand — and ask whether any test would catch it. A mutation that survives every test exposes a gap, not a passing suite. Where a mutation-testing tool is available, this reasoning can be made empirical; where it is not, reason through the mutations by hand.

Never leave source code mutated. Any change made to provoke a failure is restored before moving on.

## Independent derivation

Expected values come from the specification, the requirements, or first-principles reasoning about what the code *should* do — never from observing what the code currently returns. Reading the output off a running implementation and pasting it into the assertion produces a test that passes by construction and blesses whatever the code does, bugs included. Such a test is fully falsifiable — break the code and it goes red — yet it locks in incorrect behaviour, because the expectation was copied from the defect.

This is the trap to watch most closely when tests are written against code that already exists: the path of least resistance is to run it, capture the output, and assert equality. Derive the expectation independently instead. When the independently-derived value disagrees with the code's actual output, that disagreement is a finding — surface it as a possible bug rather than quietly adopting the code's answer.

## Edge-case enumeration

Falsifiability and independent derivation interrogate the tests that exist; neither says anything about the cases never written. High line coverage on the happy path while every boundary goes untested is coverage theatre — impressive numbers over exposed logic.

Enumerate the input space *before* writing assertions, and write a case for each class that the code must handle:

- Empty and null inputs; zero, one, and many.
- Boundaries and just past them — minimum, maximum, off-by-one neighbours.
- Error and failure paths — invalid input, exceptions, rejected operations.
- Concurrency, ordering, and timing where the code is exposed to them.
- The documented contract's stated guarantees, each asserted explicitly.

Coverage of lines is a weak proxy; coverage of behaviours is the target. A branch executed without its outcome asserted is not covered in any sense that matters. At audit time, enumerate the same input classes and flag every class the suite never tests as a coverage gap.

## Behaviour over implementation

Assert observable outcomes and contracts, not the internal mechanics by which they are produced. Tests bound to private structure, call order, or incidental detail break on every refactor while catching no real defect, and they quietly invert into tests of the test's own setup.

The sharpest form of this failure: configuring a mock to return a value, then asserting the code returns that value. That verifies the mock, not the code. Mock only what crosses a genuine boundary — external services, the clock, the network, the filesystem — and assert the behaviour the code exhibits given that boundary, not the boundary's scripted output. Prefer real collaborators wherever they are cheap and deterministic; every mock is an assumption about how the dependency behaves, and a wrong assumption yields a green test over broken integration.

## One reason to fail

Each test pins one behaviour, structured so a failure names its cause. Arrange the preconditions, act once on the code under test, assert the outcome — keeping these phases distinct keeps the test legible and its failure diagnostic.

- One behaviour per test. A test asserting many unrelated things — assertion roulette — reports only which line tripped, not which behaviour broke.
- Name the test for the behaviour and condition it pins, so a failing test communicates what regressed without reading its body.
- No unexplained literals. A bare expected value with no derivation reads as a magic number; make its origin clear so a later reader can tell a correct expectation from a stale one.
- Determinism is non-negotiable. A test that depends on wall-clock time, ambient state, network reachability, or execution order flakes, and a flaky test trains everyone to ignore failures — the opposite of the point.

## Anti-patterns

These are the failure modes that pass casual review while verifying nothing. Name them on sight, both when writing tests and when auditing:

- **The tautology** — an assertion that restates the implementation under test. Green by construction; can never fail meaningfully.
- **The no-op** — a test that invokes the code and asserts nothing, or only that no exception was thrown. Buys coverage, proves almost nothing.
- **Bug-blessing** — expectations copied from the code's current output, freezing today's behaviour, defects and all, as the spec.
- **Coverage theatre** — input classes never given a test; boundaries and error paths absent from the suite entirely, however high the line percentage.
- **The mock mirror** — asserting that a function returns exactly what its mocked dependency was told to return.
- **The flake** — non-deterministic dependence on time, order, or environment, surfacing as intermittent failures that erode trust in the whole suite.

When auditing, report each finding as the specific anti-pattern it instantiates, with the mutation or missing case that exposes it — so the fix is unambiguous.
