---
name: customize-skill
description: Records standing customizations for an installed skill, injected automatically every time that skill runs, and reviews or removes them. Use when a skill needs to behave differently without editing the skill itself, or when the user says "customise the X skill so that", "remember this for next time I use X", "what customisations do I have", "remove my customisations for X".
argument-hint: "--mode record|review|remove|setup [skill-name]"
---

Turns a one-off correction into a standing instruction. A customization is a markdown file the user owns; a hook that fires when a skill is invoked reads the files for that skill and injects them, so the customization applies without anyone remembering it exists. Installed skills stay untouched — an upgrade or reinstall never clobbers a customization.

## Route

Settle the mode from the invocation before anything else. An explicit `--mode <name>` wins outright — honour it even when the surrounding prose reads like another branch. With no flag, infer from the request: an instruction about how a skill should behave is **record**; a question about what is on file is **review**; a request to forget, drop, or undo is **remove**; a report that customizations never take effect is **setup**. Any remaining argument names the target skill.

Where two readings are genuinely live — "change my customisation for X" could revise one file or replace the set — ask which, because an unwanted file and a deleted wanted one cost the same to undo.

## Storage

One directory per customized skill, one file per concern. The handler reads exactly these two locations:

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

The hook ships with this skill and registers itself wherever the harness loads hooks declared by an installed plugin — no setup needed there. Run setup only for a standalone install (`npx skills`), or when injection demonstrably never fires.

1. **Establish the hook point from the harness itself.** Read the harness's own hook documentation and its existing configuration to find the event that fires once a skill has been invoked and whose output is added to that session's context. Never assume a config shape, a file location, or an event name. Where the harness has no such event, say so plainly and stop — customizations can still be recorded and read back, but nothing will inject them, and a hook bolted onto a different event fires at the wrong time.
2. **Check what is already registered before proposing anything.** An entry pointing at `inject-customizations.sh` means the hook is installed; a second registration injects every customization twice. Merge into whatever collection the harness keeps rather than replacing it.
3. **Resolve the handler's absolute path and write it out.** The command is `bash "<this skill's directory>/hooks/inject-customizations.sh"`. A path variable the harness defines only for hooks a plugin declared expands to nothing in a hand-written configuration, so the literal path is the only safe form here.
4. **Narrow the trigger as far as the harness allows.** The handler exits 0 silently when the payload is not a skill invocation or the skill has no customizations, so a broad trigger is harmless but spends a process on every tool call.
5. **Confirm the payload shape matches the handler.** It reads JSON on stdin and takes the skill name from `tool_input.skill`. Where the harness sends something else, the fix is a shim that rewrites the payload — never an edit to the handler, which the next update overwrites.
6. **Propose, then wait.** Show the configuration path, the exact addition, and the command the hook will run. Apply nothing until the user approves.
7. **Prove it fires.** A clean write is not evidence: a misregistered hook fails silently. Invoke a skill that has a customization on file and confirm the text actually reached the context.

Verify the handler on its own at any point, by piping a payload through it from this skill's directory:

```bash
echo '{"tool_name":"Skill","tool_input":{"skill":"<skill-name>"}}' | bash hooks/inject-customizations.sh
```

A skill with customizations on file prints one JSON object; a skill without prints nothing and exits 0. Done when a real customization round-trips through that command.

## Gotchas

- The hook fires **after** the skill has been invoked, so a customization steers what the agent does with a skill it has already loaded. It cannot stop a skill from activating, change its description, or gate its invocation — an instruction of that shape belongs in the agent instructions file, not here.
- Customizations are injected verbatim, so they compete with the skill's own instructions on equal footing. Keep each one narrow and about behaviour the skill actually reaches; a file that restates half the skill destabilises it.
- The hook resolves project scope from the current git repository root, so a customization written in a worktree applies in that worktree only. Prefer user scope for anything that should follow the user across checkouts.
