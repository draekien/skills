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
| `ubiquitous-language.yaml` | DDD ubiquitous language dictionary (bounded contexts + terms) | managed by `ubiquitous-language` skill |
| `prompting/` | Saved prompts, one `<prompt-slug>/` directory per prompt: `prompt.md` holds the raw prompt, `record.md` its target model, assumptions, and sources | managed by `prompting` skill; location set by its `outputDir` key |
| `tanstack-data-loading/discovery.json` | Discovery cache keyed by app root: backend shape, pending UI choice, verify commands, version notes, installed `@tanstack` versions. Stale after 1 day or a version change; gitignored on the user's confirmation, an explicit exception to [Version Control](#version-control) | managed by `tanstack-data-loading` skill via its `scripts/discovery.py` |
| `using-teams/` | Team files, one `<team-name>.md` per team, each with a `Use for` line and Roster, Task graph, Messaging, Review and Stop sections; a file overrides the built-in team of the same name | managed by the `using-teams` skill's `new` subcommand |
| `skill-customizations/` | Per-skill customization files, one directory per customized skill | managed by the `customize-skill` skill — see [skills/meta/customize-skill/SKILL.md](../skills/meta/customize-skill/SKILL.md) |

Future files added by new skills must be documented here and in their own spec.

## Version Control

Commit `.draekien/` and its contents by default. Shared configuration (such as a team-agreed specs directory) should be version-controlled so all contributors use the same settings. Skills must not add `.draekien/` to `.gitignore` unless the user explicitly requests it.

## Naming Rationale

The `.draekien` name is vendor-namespaced (matching the marketplace owner `draekien`), making collision with any other tool's dotfile or dotfolder effectively impossible.
