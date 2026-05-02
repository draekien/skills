# ALIGNMENT.md Format Reference

## Scoped File

Saved at `<feature-dir>/ALIGNMENT.md`. Term defs for that scope only.

```markdown
# Ubiquitous Language — <scope>

## Terms

### TermName
One or two sentence definition. No implementation detail.

### AnotherTerm
Definition.
```

## Root File

Saved at project root `ALIGNMENT.md`. Index + candidate map only — no term defs.

```markdown
# Alignment Map

<!-- Last validated: <ISO date> -->

## Alignment Files
- [path/to/ALIGNMENT.md](path/to/ALIGNMENT.md) — <scope description>

## Candidate Directories
- `path/to/dir/` — no ALIGNMENT.md yet
```

## Rules

- Root file updated every session start (revalidation timestamp) + when new scoped file created.
- Scoped file updated immediately on term confirm — no batching.
- Term names PascalCase to distinguish from prose.
- **One sentence max.** Define what it IS, not what it does. No impl detail.
- **Be opinionated.** When multiple words exist for same concept, pick canonical term, list alternatives as `aliases:` to actively avoid.
- **Project-specific only.** Before adding term, ask: unique to this context, or general programming concept? General concepts (timeouts, error types, utility patterns) don't belong even if project uses them heavily.
- **Show relationships.** Use bold term names inline, express cardinality where obvious (e.g. "An **Order** contains one or more **LineItems**").
- **Group naturally.** Use subheadings when clusters emerge. If all terms belong to one cohesive area, flat list fine.

## Flagged Ambiguities

Use when term used in conflicting ways not yet resolved.

```markdown
## Flagged Ambiguities

### TermName
Used to mean both X and Y. Resolution pending.
```

Remove entry once resolved and canonical def written under Terms.

## Scoped File — Extended Format

```markdown
# Ubiquitous Language — <scope>

## <Group Name>

### TermName
aliases: OtherWord, AlternativeName
What it IS in one sentence.

### RelatedTerm
A **TermName** that [relationship].

## Flagged Ambiguities

### AmbiguousTerm
Used to mean both X and Y. Resolution pending.
```

## Example Dialogue

Each scoped `ALIGNMENT.md` include example dialogue between dev and domain expert — shows terms interacting naturally, clarifies boundaries between related concepts.

```markdown
## Example Dialogue

**Dev:** So when a customer places an order, does that immediately create an Invoice?
**Expert:** No — an Order is just intent. An Invoice only exists once we've confirmed payment details.
**Dev:** And a LineItem — is that on the Order or the Invoice?
**Expert:** Both. The Order's LineItems are what was requested; the Invoice's LineItems are what was billed. They usually match, but not always.
```

Dialogue must:
- Use defined terms naturally (bolded on first use)
- Expose at least one boundary or distinction between related terms
- Ground in realistic workflow, not contrived example