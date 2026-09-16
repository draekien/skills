---
name: prefer-skills
description: Installs a short standing rule — in your agent instructions file, or as a prompt-submission hook where the harness has one — so the agent checks for a relevant skill and invokes it before working from training, and takes either back out. Use when skill invocations keep getting skipped in favour of guesswork and rework.
argument-hint: "[--mode install|remove] [--via instructions|hook] [--scope user|project]"
disable-model-invocation: true
---

A skill only helps when it is invoked, and an agent left alone reaches for what it already knows. The fix is not another skill competing for activation — it is three lines the agent reads every turn, written into the instructions file or fed in as each prompt is submitted. This skill puts them there, and takes them out again.

## Route

Mode: **install**, unless the request is to take the rule out, drop it, or undo it — that is **remove**. An explicit `--mode` wins outright.

Channel: **instructions** by default — the rule lives in the instructions file. `--via hook` registers a hook that contributes the same rule as context each time a prompt is submitted, so the rule arrives with the prompt rather than relying on what was loaded at session start.

Scope: **user** by default — the configuration that applies to every project. `--scope project` writes to the current repository's configuration *instead*: it never also writes user scope, and never removes a user-scope copy already there.

## The rule

Insert exactly this, adapting only the heading depth to the target file:

```markdown
## Skills

Scan available skills before each task and invoke what fits — a skill beats
working from memory. Re-scan when the task shifts or you are about to guess.
Say which skill you used, or that none fit.
```

Every word is paid for on every turn, so the text is fixed. Do not expand it with examples, rationale, or a list of installed skills: a longer rule is not obeyed harder. Both channels carry this exact text.

## Available scripts

- **`scripts/discover-instructions.py`** — finds agent instruction files and candidate config directories in either scope, without a list of harness names

## Install

### Instructions

1. **Find the targets, then read them.** Run the script for the resolved scope and read every file it reports, in full:

   ```bash
   uv run scripts/discover-instructions.py --scope user --grep "skill"
   ```

   `files` is what exists — user scope usually holds more than one, because each installed harness keeps its own. `config_dirs` is directories that look like agent configuration but hold no instruction file, which is a harness installed with nothing written for it yet. A blind append lands the rule under a heading that changes its meaning, so read before proposing. `config_dirs` entries are candidates in their own right, not a fallback for an empty `files` list — propose creating an instruction file in each one, whether or not other harnesses in the scope already have theirs.
2. **Hunt the rule already there, however worded.** The `matches` array is the first pass, not the answer — a line telling the agent to check for skills, prefer a skill, or look at its skills before acting is this rule wearing different words, and the grep is deliberately broad enough to be noisy. Read for it. Revise that line into the canonical text rather than adding a second — two copies of one instruction compete, and the weaker wording wins as often as the stronger.
3. **Place it among the standing rules**, not appended at the end under project detail it has nothing to do with. Match the file's existing heading depth and register.
4. **Propose, then wait.** Show each file path and the exact insertion in context — the surrounding lines, the rule, and whatever it replaces. Apply nothing until the user approves. Where several files are in scope, list them all so the user can pare the set back.

Done when every file the user approved carries the rule exactly once, and the user has seen the final wording of each edit.

### Hook

1. **Establish the hook point from the harness itself.** Read the harness's own hook documentation and its existing configuration to find the event that fires when the user submits a prompt and whose output is added to that prompt's context. Never assume a config shape, a file location, or an event name. Where the harness offers no such event, say so plainly and offer the instructions channel instead — a hook bolted onto a different event fires at the wrong time and is worse than none.
2. **Make the payload a literal print of the rule.** Nothing generated, nothing conditional, no enumeration of installed skills. Where quoting three lines inside a command gets awkward, put the text in a file beside the hook configuration and have the hook print that file. A hook that errors is noise on every prompt.
3. **Register at the resolved scope**, in the configuration the harness reads for hooks at that scope — not the instructions file.
4. **Propose, then wait.** Show the configuration path, the exact addition, and the command the hook will run. Apply nothing until the user approves.
5. **Prove it fires.** Have the user submit one prompt, then confirm the rule text actually reached the context through whatever the harness exposes — hook output, a debug view, or asking the agent in that session to quote the rule. A misregistered hook fails silently, so a clean write is not evidence.

Done when the hook is registered at the resolved scope and the rule text has been observed arriving with a real prompt.

## Remove

Locate the rule first, then propose. What to read differs by channel:

- **Instructions** — run the script with the same `--grep` over the resolved scope. The `matches` array is a first pass, not the answer: a rule the user has since reworded no longer matches the pattern, so read each file the script reports before concluding the rule is absent. Take the surrounding heading with the rule only where the rule was its whole content.
- **Hook** — the script does not reach this channel, because the payload sits beside the hook configuration under a name it does not glob for. A clean run of the script is not evidence the rule is gone. Read the harness's hook configuration for the registered entry and the file it prints; deregister the entry, and delete that payload file if it has no other reader.

Show each file path with the exact lines to be deleted, and get an explicit yes before touching anything. Report a scope that genuinely carries no such rule plainly, rather than removing the nearest line that happens to mention skills. Delete only within the scope and channel asked for — a removal at project scope leaves a user-scope copy standing, and the reverse; a removal `--via hook` leaves the instructions copy standing.

## Gotchas

- A project configuration file is usually committed, so a project-scope rule or hook governs everyone working in that repository. Say so before writing, and steer to user scope when the intent is the user's own habit rather than a team convention.
- Running both channels at once puts two copies of one rule in front of the agent every turn — the same competition the instructions channel hunts within a file. Pick one, and when the hook goes in, offer to take the instructions copy out.
- The script matches filenames, not harnesses, so a harness that keeps its instructions under some other name is invisible to it. When the user names a file the script did not report, take them at their word and treat it as a target.
- The rule cannot force the invocation. It arrives every turn, but the agent still decides; the rule's job is to make skipping an applicable skill read as a deviation. When it demonstrably stops working, the answer is to move it onto a mechanism that fires mechanically — `--via hook` where the harness has one — never a longer rule.
