# Migration: ALIGNMENT.md → UBIQUITOUS_LANGUAGE.md

Loaded only when legacy `ALIGNMENT.md` files are detected. Covers root and scoped file migration.

## Process

Migrate one file at a time. For each legacy file:

1. Read the full contents.
2. Determine migration type (root or scoped — see below).
3. Perform conversion.
4. Confirm target path with user before writing:

   > "Migrating `<old-path>/ALIGNMENT.md` → `<new-path>/UBIQUITOUS_LANGUAGE.md`. Proceed?"

5. Write the migrated file.
6. Delete the old `ALIGNMENT.md`.

If a `UBIQUITOUS_LANGUAGE.md` already exists at the target path, merge — do not overwrite. Append migrated terms under `## Terms`. Flag duplicates:

> "`<Term>` already exists in `UBIQUITOUS_LANGUAGE.md`. Skip or overwrite?"

---

## Root File Migration

Old root `ALIGNMENT.md` contains an index + candidate directory map. Convert to root `UBIQUITOUS_LANGUAGE.md` format.

**Old format:**
```markdown
# Alignment Map

<!-- Last validated: <ISO date> -->

## Alignment Files
- [path/to/ALIGNMENT.md](path/to/ALIGNMENT.md) — <scope description>

## Candidate Directories
- `path/to/dir/` — no ALIGNMENT.md yet
```

**New format:**
```markdown
# Ubiquitous Language Index

<!-- Last validated: <ISO date> -->

## Bounded Contexts
- [path/to/UBIQUITOUS_LANGUAGE.md](path/to/UBIQUITOUS_LANGUAGE.md) — <scope description>

## Unmapped Directories
- `path/to/dir/` — no bounded context assigned yet
```

Mapping rules:
- `## Alignment Files` → `## Bounded Contexts`
- Each `ALIGNMENT.md` path → same path with `UBIQUITOUS_LANGUAGE.md`
- `## Candidate Directories` → `## Unmapped Directories`
- Preserve ISO date, update to today's date.

---

## Scoped File Migration

Old scoped `ALIGNMENT.md` contains term definitions. Convert each term to new format.

**Old format:**
```markdown
### TermName
aliases: Alias1
One or two sentence definition.
```

**New format:**
```markdown
### TermName
aliases: Alias1
Definition trimmed to 50 words max.
usage: <generated — see below>
related:
  - <inferred from definition text — see below>
```

### Trimming definitions

If old definition exceeds 50 words: trim to the most essential clause. Preserve what it IS; drop what it does or how it works. If trimming would lose meaning, ask user to confirm the shortened version before writing.

### Generating usage notes

Infer a usage note from the definition text. Model: one sentence showing the term in a realistic domain conversation, using at least one other term from the same file where possible.

If unable to infer confidently, leave a placeholder and flag:

```markdown
usage: <!-- TODO: add usage note -->
```

### Inferring related terms

Scan definition text for bold term names (e.g. `**OrderLine**`) or explicit cardinality phrases (e.g. "contains one or more", "belongs to", "produced by"). Convert to related entries with appropriate labels.

If no relationships are detectable, omit the `related:` block — do not fabricate.

### Handling Flagged Ambiguities

Preserve `## Flagged Ambiguities` sections as-is. They require no format change.

### Handling Example Dialogue

Discard `## Example Dialogue` sections. They are not part of the new format.

---

## Post-Migration

After all files migrated:

- Confirm root `UBIQUITOUS_LANGUAGE.md` index is up to date.
- Load all migrated scoped files into conflict detection context.
- Resume normal session flow from Step 1.
