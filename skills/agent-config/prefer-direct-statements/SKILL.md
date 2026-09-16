---
name: prefer-direct-statements
description: Installs a standing rule against mannered prose — in your agent instructions files, or as a prompt-submission hook where the harness has one — so the agent states things directly instead of reaching for metaphor, and takes the rule back out again. Use when replies and documents keep arriving full of metaphor and flourish.
argument-hint: "[--mode install|remove] [--via instructions|hook] [--scope user|project]"
disable-model-invocation: true
---

An agent asked to write well reaches for figurative language, because most of what it was trained on treats flourish as a mark of quality. A skill cannot correct that: a skill has to be invoked, and by then the sentence is already written. The correction has to be standing text the agent reads every turn. This skill puts that text in place and takes it out again.

It installs a rule; it does not edit prose. Rewriting a document that is already mannered is `writing-for-humans` (`/plugin install technical-writing-skills@draekien-skills`, or `npx skills add draekien/skills --skill "writing-for-humans"`). Ask the user to install it rather than doing that work here.

## Route

Mode: **install**, unless the request is to take the rule out, drop it, or undo it — that is **remove**. An explicit `--mode` wins outright.

Channel: **instructions** by default — the rule lives in the instructions file. `--via hook` registers a hook that contributes the same rule as context each time a prompt is submitted, so the rule arrives with the prompt rather than relying on what was loaded at session start.

Scope: **user** by default — the configuration that applies to every project. `--scope project` writes to the current repository's configuration *instead*: it never also writes user scope, and never removes a user-scope copy already there.

## The rule

Insert exactly this, adapting only the heading depth to the target file:

```markdown
## Prose

Mannered prose substitutes metaphor and flourish for direct statement. Instead of
"a parameter worth varying," the mannered writer produces "a dial worth turning."
Instead of "this point still matters," they write "this point earns its keep." The
phrases exist to display the writer, not to convey the idea, and readers can tell.
That is why mannered prose irritates: it makes the reader work harder so the writer
can perform. It is also imprecise. Metaphors drag in connotations the writer did not
choose and cannot control. The fix is to say what you mean. When a literal phrase is
available, use it.
```

The text is fixed, and both channels carry it identically. The worked examples are what makes the rule usable — they give the agent a pattern to match against rather than a label to interpret — so do not compress the rule to its last two sentences, and do not add examples of your own. Do not adapt the examples to the user's domain either: a domain-specific pair narrows what the agent recognises as mannered.

## Available scripts

- **`scripts/discover-instructions.py`** — finds agent instruction files and candidate config directories in either scope, without a list of harness names

## Install

### Instructions

1. **Find the targets, then read them.** Run the script for the resolved scope and read every file it reports, in full:

   ```bash
   uv run scripts/discover-instructions.py --scope user --grep "mannered|metaphor|flourish|figurative|plain language|literal"
   ```

   `files` is what exists. `config_dirs` is directories that look like agent configuration but hold no instruction file — a harness installed with nothing written for it yet. A blind append lands the rule under a heading that changes its meaning, so read before proposing. `config_dirs` entries are candidates in their own right, not a fallback for an empty `files` list — propose creating an instruction file in each one, whether or not other harnesses in the scope already have theirs.

2. **Hunt the rule already there, however worded.** The `matches` array is the first pass, not the answer — a line telling the agent to write plainly, avoid metaphor, or drop the marketing voice is this rule under different wording, and may use none of the searched terms. Read for it. Revise that line into the canonical text rather than adding a second: two copies of one instruction compete, and the weaker wording wins as often as the stronger.

3. **Place it among the standing rules**, not appended at the end under project detail it has nothing to do with. Match the file's existing heading depth and register.

4. **Propose, then wait.** Show each file path and the exact insertion in context — the surrounding lines, the rule, and whatever it replaces. Apply nothing until the user approves. Where several files are in scope, list them all so the user can pare the set back.

Done when every file the user approved carries the rule exactly once, and the user has seen the final wording of each edit.

### Hook

1. **Establish the hook point from the harness itself.** Read the harness's own hook documentation and its existing configuration to find the event that fires when the user submits a prompt and whose output is added to that prompt's context. Never assume a config shape, a file location, or an event name. Where the harness offers no such event, say so plainly and offer the instructions channel instead — a hook bolted onto a different event fires at the wrong time and is worse than none.
2. **Make the payload a literal print of the rule.** Nothing generated, nothing conditional. The rule runs to several lines, so put the text in a file beside the hook configuration and have the hook print that file rather than quoting it inside a command; an unescaped quotation mark in the examples will otherwise break the hook, and a hook that errors is noise on every prompt.
3. **Register at the resolved scope**, in the configuration the harness reads for hooks at that scope — not the instructions file.
4. **Propose, then wait.** Show the configuration path, the exact addition, and the command the hook will run. Apply nothing until the user approves.
5. **Prove it fires.** Have the user submit one prompt, then confirm the rule text actually reached the context through whatever the harness exposes — hook output, a debug view, or asking the agent in that session to quote the rule. A misregistered hook fails silently, so a clean write is not evidence.

Done when the hook is registered at the resolved scope and the rule text has been observed arriving with a real prompt.

## Remove

Locate the rule first, then propose. What to read differs by channel:

- **Instructions** — run the script with the same `--grep` over the resolved scope. The `matches` array is a first pass, not the answer: a rule the user has since reworded no longer matches the pattern, so read each file the script reports before concluding the rule is absent. Take the surrounding heading with the rule only where the rule was its whole content.
- **Hook** — the script does not reach this channel, because the payload sits beside the hook configuration under a name it does not glob for. A clean run of the script is not evidence the rule is gone. Read the harness's hook configuration for the registered entry and the file it prints; deregister the entry, and delete that payload file if it has no other reader.

Show each file path with the exact lines to be deleted, and get an explicit yes before touching anything. Report a scope that genuinely carries no such rule plainly, rather than removing the nearest line that happens to mention writing style. Delete only within the scope and channel asked for — a removal at project scope leaves a user-scope copy standing, and the reverse; a removal `--via hook` leaves the instructions copy standing.

## Gotchas

- A project configuration file is usually committed, so a project-scope rule or hook governs everyone working in that repository. Say so before writing, and steer to user scope when the intent is how the user wants the agent to write for them rather than a team convention.
- Running both channels at once puts two copies of one rule in front of the agent every turn — the same competition the instructions channel hunts within a file. Pick one, and when the hook goes in, offer to take the instructions copy out.
- The rule governs the agent's own writing, not the user's codebase. It will not stop the agent from quoting mannered prose it was asked to review, and it should not: the user asking "what is wrong with this paragraph" needs the paragraph.
- The script matches filenames, not harnesses, so a harness that keeps its instructions under some other name is invisible to it. When the user names a file the script did not report, take them at their word and treat it as a target.
- The rule cannot force literal writing. It arrives every turn, but the agent still decides; the rule's job is to make a metaphor read as a deviation. When it demonstrably stops working, move it onto a mechanism that fires mechanically — `--via hook` where the harness has one — rather than lengthening the rule.
