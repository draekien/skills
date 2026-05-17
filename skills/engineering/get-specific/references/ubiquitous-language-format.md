# Ubiquitous Language Format Reference

## Dictionary File

Stored at the path specified by `dictionaryPath` in `.draekien/.skillsrc` (default: `.draekien/ubiquitous-language.yaml`).

Single file for the whole project. Bounded contexts are top-level keys under `contexts`.

```yaml
contexts:
  Orders:
    terms:
      Order:
        aliases:
          - PurchaseOrder
        definition: "Intent from a customer to acquire one or more products. Exists before payment is confirmed. Mutable until submitted."
        usage: "When a customer adds items to their cart and clicks 'Buy', that creates an Order."
        related:
          - term: OrderLine
            relationship: contains
          - term: Invoice
            relationship: precedes
          - term: Customer
            relationship: owned by
    ambiguities:
      LineItem:
        note: "Used to mean both OrderLine and Invoice line — resolution pending."
```

## Schema

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `contexts` | map | yes | Top-level key. Each entry is a bounded context. |
| `contexts.<Name>.terms` | map | yes | Term definitions keyed by PascalCase name. |
| `contexts.<Name>.terms.<Term>.definition` | string | yes | 50 words max. What it IS. No impl detail. |
| `contexts.<Name>.terms.<Term>.aliases` | list\<string\> | no | Alternative names to actively avoid. |
| `contexts.<Name>.terms.<Term>.usage` | string | yes | One sentence using the term in a domain conversation. |
| `contexts.<Name>.terms.<Term>.related` | list\<{term, relationship}\> | no | Only terms already defined. |
| `contexts.<Name>.ambiguities` | map | no | Terms flagged as conflicting. Remove on resolution. |
| `contexts.<Name>.ambiguities.<Term>.note` | string | yes | Describes the conflict. |

## Script Invocation

All scripts use `uv run` from the skill's base directory. `<dict>` is the resolved `dictionaryPath`.

**Query (read-only):**
```
uv run scripts/query.py --dict <dict> list-contexts
uv run scripts/query.py --dict <dict> lookup <TermName> [--context <Context>]
uv run scripts/query.py --dict <dict> list <Context> [--page N] [--page-size N]
```

**Write:**
```
uv run scripts/write.py --dict <dict> add-term \
  --context <Context> --term <TermName> --definition "<text>" \
  [--aliases Alias1 Alias2] [--usage "<text>"] \
  [--related "TermName:relationship" ...]

uv run scripts/write.py --dict <dict> flag-ambiguity \
  --context <Context> --term <TermName> --note "<text>"

uv run scripts/write.py --dict <dict> resolve-ambiguity \
  --context <Context> --term <TermName>
```

**Migrate (one-time):**
```
uv run scripts/migrate.py --project-root <root> --dict <dict> [--dry-run]
```

## Term Rules

- **PascalCase** term names to distinguish from prose.
- **50 words max per definition.** Define what it IS. No impl detail. Aliases, usage, and related live outside this budget.
- **Be opinionated.** When multiple words exist for the same concept, pick one canonical term; list alternatives as `aliases` to actively avoid.
- **Project-specific only.** Before adding a term, ask: unique to this domain, or a general programming concept? General concepts don't belong.
- **Usage note required.** Must use at least one other defined term where possible.
- **Related terms required when applicable.** List only already-defined terms. Use a relationship label.

## Relationship Labels

| Label | Meaning |
|-------|---------|
| `contains` | this term owns one or more of the related term |
| `part of` | this term is a component of the related term |
| `produced by` | this term results from the related term |
| `precedes` | this term comes before the related term in a process |
| `triggers` | this term causes the related term to occur |
| `owned by` | this term's lifecycle is controlled by the related term |
| `synonym of` | same concept, different name — one should be aliased |
