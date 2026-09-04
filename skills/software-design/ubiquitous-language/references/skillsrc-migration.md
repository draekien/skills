# Migrating the `with-ubiquitous-language` config block

This skill was renamed from `with-ubiquitous-language` to `ubiquitous-language` when it moved
into the `software-design` bucket. `.skillsrc` is keyed by skill name, so a project configured
before the rename still holds its `dictionaryPath` under the old key. Left alone, the skill reads
nothing, falls back to the default path, and starts a second dictionary beside the real one.

Read this file only when Session Start finds a `with-ubiquitous-language` block in
`.draekien/.skillsrc`.

## Migrate

`scripts/skillsrc.py` has only `get` and `set`, so it cannot remove the stale block. Edit the JSON
directly.

1. Parse `.draekien/.skillsrc` and read `with-ubiquitous-language.dictionaryPath`.
2. Tell the user what you found and what you propose: the old key's value moves to
   `ubiquitous-language.dictionaryPath`, and the `with-ubiquitous-language` block is removed.
3. On confirmation, rewrite the file with the block renamed. Preserve every other skill's block
   and every other key inside the migrated block. If the user declines, use the old key's value
   for this session and do not ask again.
4. Continue Session Start from step 3 with the migrated `dictionaryPath`.

## Edge cases

- **Both keys present** — the new key wins. Report both values to the user, and delete the old
  block only once they confirm the new value is the one they want.
- **Old block holds no `dictionaryPath`** — delete it on confirmation and use the default path.
- **File is not valid JSON** — do not rewrite it. Tell the user, use the default path, and stop
  the migration.
