---
name: customize-skill
description: Records standing customizations for an installed skill, injected automatically every time that skill runs, and reviews or removes them. Use when a skill needs to behave differently without editing the skill itself, or when the user says "customise the X skill so that", "remember this for next time I use X", "what customisations do I have", "remove my customisations for X".
argument-hint: "--mode [record|review|remove|setup] [skill-name]"
---

Turns a one-off correction into a standing instruction. A customization is a markdown file the user owns; a `PostToolUse` hook on the `Skill` tool reads the files for whichever skill was just invoked and injects them, so the customization applies without anyone remembering it exists. Installed skills stay untouched — an upgrade or reinstall never clobbers a customization.

## Route

Settle the mode from the invocation before anything else. An explicit `--mode <name>` wins outright — honour it even when the surrounding prose reads like another branch. With no flag, infer from the request: an instruction about how a skill should behave is **record**; a question about what is on file is **review**; a request to forget, drop, or undo is **remove**; a report that customizations never take effect is **setup**. Any remaining argument names the target skill.

Where two readings are genuinely live — "change my customisation for X" could revise one file or replace the set — ask which, because an unwanted file and a deleted wanted one cost the same to undo.

## Storage

One directory per customized skill, one file per concern:

```
~/.claude/skill-customizations/<skill-name>/<slug>.md          user scope — every project
<repo-root>/.draekien/skill-customizations/<skill-name>/<slug>.md   project scope — this repo only
```

Name the directory after the skill's **bare name** (`revise-claude-md`), not the plugin-qualified form (`claude-md-management:revise-claude-md`) — bare applies however the skill is installed. The hook reads both and injects project scope last, so project customizations override user ones.

Each file carries a one-line `description` in frontmatter and the instruction as its body:

```markdown
---
description: Always log CI changes under a Pipelines heading
---

When recording session learnings, file anything about CI or pipeline behaviour under a
`## Pipelines` heading, creating it if absent — this project's CLAUDE.md keeps that
material separate from build instructions.
```

## Record

1. **Pin the target** — resolve the skill the user named against the skills actually installed. A customization filed under a misspelt name is silently dead. If no installed skill matches, say so and confirm the name before writing.
2. **Pin the scope** — project scope when the instruction depends on this codebase's conventions, layout, or tooling; user scope when it is how the user always wants that skill to work. Ask when it is genuinely either.
3. **Slug the concern** — one file per concern, named for that concern (`pipelines-heading.md`), never a dated or numbered file. A new instruction about a concern already on file revises that file rather than adding a second.
4. **Write it as an instruction to the executing agent** — the user speaks in first person about themselves ("I want it to always..."); the file must read as third-person imperative addressed to the agent running that skill, and must carry the *why*, so the agent adapts when the exact case does not fit. Rewrite, do not transcribe.
5. **Confirm and write** — show the file path and the body, then create it. Before the first write into a project, create `.draekien/` if absent, confirming that per [specs/draekien.md](../../../specs/draekien.md).

Done when the file exists at the resolved path and the user has seen its final wording.

## Review

Read both scopes' directories for the named skill, or every directory when no skill is named, and report skill, scope, file, and the frontmatter `description` for each. Report an empty result plainly rather than inferring what might be customized.

## Remove

Deleting is the user's data. List exactly what will be deleted — paths and descriptions — and get an explicit yes before removing anything. "Remove all my customisations for X" means both scopes for that skill; confirm that reach is intended. Remove an emptied `<skill-name>/` directory too, but never `skill-customizations/` itself.

## Setup

The hook ships with this skill and loads automatically when the skill came from the plugin marketplace — no setup needed. Run setup only for a standalone install (`npx skills`), or when injection demonstrably never fires.

Merge this `PostToolUse` entry into `~/.claude/settings.json`, substituting this skill's absolute directory for `${CLAUDE_PLUGIN_ROOT}/skills/meta/customize-skill`; that variable is defined only for plugin-provided hooks and expands to nothing in a settings file. Merge into any existing `PostToolUse` array rather than replacing it, and skip the write entirely if an entry pointing at `inject-customizations.sh` is already there — two registrations inject everything twice.

```json
{
  "PostToolUse": [
    {
      "matcher": "Skill",
      "hooks": [
        {
          "type": "command",
          "command": "bash \"${CLAUDE_PLUGIN_ROOT}/skills/meta/customize-skill/hooks/inject-customizations.sh\"",
          "timeout": 10
        }
      ]
    }
  ]
}
```

Verify by piping a payload through the handler directly, from this skill's directory:

```bash
echo '{"tool_name":"Skill","tool_input":{"skill":"<skill-name>"}}' | bash hooks/inject-customizations.sh
```

A skill with customizations on file prints one JSON object; a skill without prints nothing and exits 0. Done when a real customization round-trips through that command.

## Gotchas

- The hook fires **after** the `Skill` tool returns, so a customization steers what the agent does with a skill it has already loaded. It cannot stop a skill from activating, change its description, or gate its invocation — an instruction of that shape belongs in `CLAUDE.md`, not here.
- Customizations are injected verbatim, so they compete with the skill's own instructions on equal footing. Keep each one narrow and about behaviour the skill actually reaches; a file that restates half the skill destabilises it.
- The hook resolves project scope from the current git repository root, so a customization written in a worktree applies in that worktree only. Prefer user scope for anything that should follow the user across checkouts.
