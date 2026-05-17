# Spec Format

The spec adapts its depth to the scope of the module being designed. All scopes share a core set of sections; larger scopes add more.

## Scope Determination

| Scope | Description |
|-------|-------------|
| **Method** | A single function or method on an existing type |
| **Class** | A single class or struct with its methods |
| **Module** | A cohesive group of types and functions (a package, namespace, or file) |
| **Layer** | A horizontal architectural slice (e.g. persistence layer, API layer) |

When in doubt, ask the user to confirm the scope before drafting.

## Core Sections (all scopes)

### Name and Purpose

One sentence. States what the module is and its single responsibility.

```
## PaymentGateway

Processes payment authorisation requests and returns a typed result — never throws.
```

### Interface

Public API surface: function/method signatures, parameter types, return types, and error contracts. Language-agnostic pseudocode is fine if the target language is not yet determined.

```
## Interface

authorise(request: PaymentRequest): Result<AuthorisationToken, PaymentError>
refund(token: AuthorisationToken, amount: Money): Result<void, PaymentError>
```

### Design Rationale

One paragraph per major decision. Each paragraph names the decision and explains *why* — not what the code does. Link to violated or upheld design principles where relevant.

```
## Design Rationale

**Result type over exceptions** — callers must handle both success and failure paths explicitly. Exceptions would allow callers to ignore the error case, violating Fail Fast at the boundary.

**Single `authorise` entry point** — rather than separate methods per payment provider, the gateway hides the provider selection internally (Information Hiding). Adding a provider does not change the interface.
```

## Extended Sections (class scope and above)

### Key Data Structures

Types that cross the module boundary. Include fields, constraints, and invariants. Omit internal-only types.

```
## Key Data Structures

PaymentRequest { amount: Money, currency: CurrencyCode, card: CardToken }
PaymentError   { code: ErrorCode, message: string }  // code is exhaustive enum — no stringly-typed errors
```

### Bounded Context *(DDD mode only)*

The bounded context this module belongs to, confirmed against the root `UBIQUITOUS_LANGUAGE.md` index. List any terms defined or referenced from the context's `UBIQUITOUS_LANGUAGE.md`.

## Extended Sections (module and layer scope only)

### Internal Decomposition

Sub-modules or internal layers, named and described in one sentence each. Organised around knowledge ownership, not execution order.

```
## Internal Decomposition

- **ProviderRouter** — selects the payment provider for a given currency and card type
- **AuthorisationClient** — speaks the provider's wire protocol; one implementation per provider
- **ResultMapper** — translates provider-specific responses into `PaymentError` codes
```

### Rejected Alternatives

Alternatives considered and the reason each was rejected. Prevents revisiting settled decisions.

```
## Rejected Alternatives

**Per-provider public methods** (`authoriseWithStripe`, `authoriseWithAdyen`) — rejected: leaks provider selection to callers, violates Information Hiding. Provider choice is an internal decision.

**Exception-based error handling** — rejected: callers can silently swallow exceptions; Result type makes the error path impossible to ignore.
```
