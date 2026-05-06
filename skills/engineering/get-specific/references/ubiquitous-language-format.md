# UBIQUITOUS_LANGUAGE.md Format Reference

## Scoped File

Saved at `<bounded-context-dir>/UBIQUITOUS_LANGUAGE.md`. Term defs for that bounded context only.

```markdown
# Ubiquitous Language — <Bounded Context Name>

## Terms

### TermName
aliases: Alias1, Alias2
Definition in 50 words max. What it IS, not what it does. No impl detail.
usage: One sentence showing the term used naturally in a domain conversation.
related:
  - OtherTerm (relationship label)
  - AnotherTerm (relationship label)

### AnotherTerm
Definition.
usage: Usage note.
```

## Root File

Saved at project root `UBIQUITOUS_LANGUAGE.md`. Index + bounded context map only — no term defs.

```markdown
# Ubiquitous Language Index

<!-- Last validated: <ISO date> -->

## Bounded Contexts
- [path/to/UBIQUITOUS_LANGUAGE.md](path/to/UBIQUITOUS_LANGUAGE.md) — <Bounded Context Name>

## Unmapped Directories
- `path/to/dir/` — no bounded context assigned yet
```

## Rules

- Root file updated every session start (revalidation timestamp) + when new scoped file created.
- Scoped file updated immediately on term confirm — no batching.
- Term names PascalCase to distinguish from prose.
- **50 words max per definition.** Define what it IS. No impl detail. Aliases, usage note, and related terms live outside this budget.
- **Be opinionated.** When multiple words exist for same concept, pick canonical term, list alternatives as `aliases:` to actively avoid.
- **Project-specific only.** Before adding term, ask: unique to this context, or general programming concept? General concepts (timeouts, error types, utility patterns) don't belong even if project uses them heavily.
- **Usage note required.** One sentence showing the term used in a realistic domain conversation. Must use at least one other defined term where possible.
- **Related terms required when applicable.** List only terms already defined. Use a relationship label that describes directionality.

### Relationship Labels

| Label | Meaning |
|---|---|
| `contains` | this term owns one or more of the related term |
| `part of` | this term is a component of the related term |
| `produced by` | this term results from the related term |
| `precedes` | this term comes before the related term in a process |
| `triggers` | this term causes the related term to occur |
| `owned by` | this term's lifecycle is controlled by the related term |
| `synonym of` | same concept, different name — one should be aliased |

## Flagged Ambiguities

Use when term used in conflicting ways not yet resolved.

```markdown
## Flagged Ambiguities

### TermName
Used to mean both X and Y. Resolution pending.
```

Remove entry once resolved and canonical def written under Terms.

## Full Scoped File Example

```markdown
# Ubiquitous Language — Orders

## Terms

### Order
aliases: PurchaseOrder
Intent from a customer to acquire one or more products. Exists before payment is confirmed. Mutable until submitted.
usage: "When a customer adds items to their cart and clicks 'Buy', that creates an Order."
related:
  - OrderLine (contains)
  - Invoice (precedes)
  - Customer (owned by)

### OrderLine
A single product-quantity pair within an Order. Quantity, price, and product reference captured at order time.
usage: "Each product in an Order is represented as an OrderLine with its price locked at submission."
related:
  - Order (part of)
  - Product (references)

### Invoice
aliases: Bill
Formal record of what was charged for a fulfilled Order. Immutable once issued.
usage: "Once payment is confirmed, an Invoice is generated from the Order's OrderLines."
related:
  - Order (produced by)
  - Payment (triggers)

## Flagged Ambiguities

### LineItem
Used to mean both OrderLine and Invoice line — resolution pending.
```
