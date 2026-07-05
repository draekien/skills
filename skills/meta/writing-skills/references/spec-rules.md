# Invariant Spec Rules

The stable subset of the [Agent Skills open standard](https://agentskills.io/specification)
that `scripts/validate.py` enforces. Every rule here is machine-checked; run
the validator rather than checking by hand. For anything not listed — optional
fields, packaging, evolving harness support — fetch the live specification.

## `name`

- Present, non-empty, a plain string
- 1–64 characters
- Lowercase letters, numbers, hyphens only (`a-z`, `0-9`, `-`)
- No leading, trailing, or consecutive hyphens
- Matches the parent directory name exactly

## `description`

- Present, non-empty, a plain string
- 1–1024 characters

## Optional fields

- `compatibility`: 1–500 characters
- `metadata`: a YAML mapping with string values only
- `allowed-tools`: a space-separated string, never a YAML list — this is a
  shared open-standard field other harnesses honour only as a string, so the
  list form fails rather than warns
- `argument-hint`: a quoted string, never a YAML list — the unquoted
  `[issue-number]` form parses as a list, not the free-text string every
  harness expects

## Frontmatter formatting

- Only open-standard fields pass silently (`name`, `description`, `license`,
  `compatibility`, `metadata`, `allowed-tools`)
- Known harness-specific extensions pass with a non-blocking portability
  warning; anything else fails as a likely typo. The validator's list of known
  extensions is a maintained snapshot — the one piece of state-of-the-world
  this skill carries, because a script cannot explore. If a field fails that a
  harness genuinely documents, update the list in `scripts/validate.py` rather
  than renaming the field
- No trailing whitespace on any frontmatter line
- No block scalar notation (`|` or `>`) in frontmatter values

## Structure and body

- `SKILL.md` present at the skill root
- Body under 500 lines
- All file references in the body use relative paths and resolve to files
  that exist
- Files in `references/` do not link to other files (one level deep only)
- Body prose contains no model-specific terms (LLM-agnostic)

## Scripts

- Python: no interactive `input()` calls; PEP 723 dependencies all
  version-pinned
- Bash: no interactive `read VAR` commands
- Network access (`requests`, `httpx`, `curl`, ...) declared in
  `compatibility:`
