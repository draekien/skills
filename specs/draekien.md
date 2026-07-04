# .draekien Directory Convention

## Purpose

`.draekien/` is a project-level configuration directory created at the repository root by any skill that requires persistent, per-project settings. It provides a single, vendor-namespaced location for all draekien skill configuration, preventing collision with other tooling dotfiles and dotfolders.

## Location

Always at the repository root:

```
<project-root>/
  .draekien/
    .skillsrc       skill configuration (see specs/skillsrc.md)
```

## Creating the Directory

Skills must not assume `.draekien/` exists. Before writing any file inside it:

1. Check whether `.draekien/` exists at the project root.
2. If it does not exist, confirm the creation with the user before proceeding.
3. Create the directory, then write the target file.

Once created in a session, treat it as present for the remainder — do not re-confirm on subsequent writes.

## Contents

| File | Purpose | Spec |
|------|---------|------|
| `.skillsrc` | Per-skill configuration keyed by skill name | [specs/skillsrc.md](skillsrc.md) |
| `ubiquitous-language.yaml` | DDD ubiquitous language dictionary (bounded contexts + terms) | managed by `get-specific` skill |
| `skill-evals/` | Per-evaluated-skill eval state (frozen suites, run history, report) | managed by `skill-evals` skill — see [skills/drafting/skill-evals/SKILL.md](../skills/drafting/skill-evals/SKILL.md) |

Future files added by new skills must be documented here and in their own spec.

## Version Control

Commit `.draekien/` and its contents by default. Shared configuration (such as a team-agreed specs directory) should be version-controlled so all contributors use the same settings. Skills must not add `.draekien/` to `.gitignore` unless the user explicitly requests it.

## Naming Rationale

The `.draekien` name is vendor-namespaced (matching the marketplace owner `draekien`), making collision with any other tool's dotfile or dotfolder effectively impossible.
