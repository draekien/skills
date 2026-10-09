---
name: prompting
description: Drafts or revises a prompt for the specific Claude model that will run it — a system prompt, subagent brief, project instruction, single CLAUDE.md rule, or chat message — with model-specific tuning. Use when writing a prompt for a named model, when a prompt behaves worse after a model change, or when the user says "write a system prompt for", "tune this for opus", "why does this prompt behave worse on sonnet". Not for model-agnostic prompt scoring, authoring a skill's SKILL.md, or documenting a repository for agents.
argument-hint: "[draft|revise] [--model <model-id>] [request-or-file]"
---

# Prompting

Prompting advice is **model-specific**: a line one model needs is a line the next model's guidance says to delete. Every line of a prompt is a claim the guidance set must support, and the guidance set is chosen by the target model.

The deliverable is text the model reads. How a request is sent or a product is configured — model settings, request parameters, environment variables, harness code — is out of scope; leave it out even when the target model's docs cover it.

When a step below says to ask and no one can answer — a delegated or scheduled run — take the stated fallback, and list each assumption under **Assumptions** in the record.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes the `prompting` output directory in `.draekien/.skillsrc`.

## Resolve the output directory

Each prompt the skill produces is saved in the output directory as a **saved prompt**: a directory holding the prompt file and its record, so a later run can revise it. Read it with `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill prompting get outputDir --default .draekien/prompting`; when the script cannot run, read `prompting.outputDir` from `.draekien/.skillsrc` as JSON, defaulting to `.draekien/prompting`. Do not create the directory yet.

When no file system is available, there is no output directory: the deliverable goes in the reply only, and the reply says it was not saved.

## Choose the mode

An explicit subcommand wins. Otherwise the mode is **revise** when the request supplies an existing prompt — a saved prompt in the output directory, a file path, pasted text, or a prompt named in the codebase — or complains about how one behaves; it is **draft** when it asks for a new one. The positional is the request in draft and the prompt in revise. When the prompt text is not supplied, or a named file cannot be read or is empty, say so and ask for the prompt; never draft in its place. Fallback: stop and report that there is nothing to revise.

## Resolve the target model

The **target model** is the model that will run the prompt. It is often not the model running this session: a subagent brief runs on the model its definition names, and a system prompt runs on the model the application calls. Go down the list and stop at the first source that names a model:

1. `--model`, or a model the user names in the request or in the code the prompt is written for. When `--model` disagrees with a model the request or code names, ask. Fallback: `--model`.
2. The model ID in your own system prompt — only when the prompt will run in this session, or in a subagent whose definition names no model.
3. Configuration: the model the session is configured to start on, read in the priority order `https://code.claude.com/docs/en/model-config.md` gives, across the settings scopes in the precedence order `https://code.claude.com/docs/en/settings.md` gives. A variable set in a settings file's `env` block counts as environment. When either page cannot be fetched, skip this source.
4. Ask the user. Fallback: the target is unresolved; use the general-only guidance set.

An alias such as `opus`, from any source, names a tier, not a version. Resolve it to a version with the alias table and the alias-override variables on the model-config page, for the provider the session runs on. When the page cannot be fetched, the provider is unknown, or the alias names no tier (such as `default`), ask. Fallback: the target is unresolved. When the request names several models as targets, run the rest of the skill once for each and label each result.

In a saved prompt, the record's frontmatter `target` is the model the prompt was last written for. When the request names no other model, it states the target, like source 1; when it does, the new model is the target and the prompt is being moved between models. The record's frontmatter `kind` likewise states the prompt kind.

Sources 1 and 2 state the target. Source 3 and any alias resolved through the table are **inferences**, because a session switch, a launch flag, or a resumed session can override configuration and an override variable can repoint an alias. Ask the user to confirm an inference before loading references. Fallback: proceed on it, marked unconfirmed.

Done when the target model is named with its source, and an inference is confirmed or marked unconfirmed.

## Classify the prompt kind

The **prompt kind** decides which reference files make up the guidance set. Classify by how the text reaches the model:

- **API prompt** — text an application places in a request it builds through the Messages API: a system prompt, tool description, a message the application injects mid-run, or a brief or instruction file the application sends in its own request.
- **Product prompt** — text a person types or saves in a chat or coding product built on the model, which the product loads itself: a chat message, project instructions, a `CLAUDE.md` or `AGENTS.md` rule, a subagent definition, or the brief a coding product passes to a subagent it dispatches.

In the references, "the application" is what an API prompt's author builds, and "product" always means the product-prompt kind. When the prompt kind is unclear, ask. Fallback: classify by where the text will be saved or sent.

Done when the prompt kind is stated.

## Load the guidance set

The skill supports the latest model of each tier. Match the target by tier and version, ignoring a provider prefix such as `anthropic.`, a date suffix, and a context-window suffix such as `[1m]`:

| Tier | Supported model | Tier references |
| --- | --- | --- |
| Fable | Fable 5.1 (`claude-fable-5-1`), and Mythos 5.1, which shares its guidance | [fable.md](references/fable.md), [fable-api.md](references/fable-api.md) |
| Opus | Opus 5.5 (`claude-opus-5-5`) | [opus.md](references/opus.md), [opus-api.md](references/opus-api.md), [opus-product.md](references/opus-product.md) |
| Sonnet | Sonnet 5.5 (`claude-sonnet-5-5`) | [sonnet.md](references/sonnet.md), [sonnet-api.md](references/sonnet-api.md), [sonnet-product.md](references/sonnet-product.md) |
| Haiku | Haiku 5.5 (`claude-haiku-5-5`) | [haiku.md](references/haiku.md), [haiku-api.md](references/haiku-api.md) |

Each set of references is split by prompt kind: `<name>.md` holds the entries for both kinds, `<name>-api.md` the entries for API prompts only, and `<name>-product.md` the entries for product prompts only. The **guidance set** is the both-kinds file and the prompt kind's file, from the general references — [general.md](references/general.md), [general-api.md](references/general-api.md), [general-product.md](references/general-product.md) — always, and from the tier references when the target is a supported model. Never load the other kind's files. Read every file in the guidance set in full before drafting or revising.

- **The tier references win.** When a tier entry contradicts a general entry, or supplies its own block for the same behaviour — scope, subagents, verification, thinking — use the tier entry only.
- **Measured entries are scoped.** A general entry marked `Measured on <model>` applies to another target only when the prompt shows the behaviour it corrects; cite it with that label.
- **Context engineering is 5-generation only.** The general references' "Context engineering" sections apply to Fable, Opus, and Sonnet targets and to Haiku 5.5.

When the target is any other model — an earlier version in a tier, a version newer than this table, or unresolved — the guidance set is the general references alone. Say so in the record's header, naming the supported model of the target's tier. Never apply a tier reference to a model it was not written for: neighbouring versions often need opposite instructions.

Done when the guidance set is read, and an unsupported target is stated as such.

## Align on the task

A prompt can only carry what its author knows about the job. The **task brief** is complete when the request, the conversation, a saved prompt's record, or the project answers each of:

- what the model is asked to do, and the inputs it receives;
- what "done" looks like: the output, its format, and who reads it;
- the constraints: what the model must not do, and when it must stop and ask;
- in revise mode, why the prompt is being revised: a behaviour to fix, a move to another model, or a general review.

Answer every item the project can answer — the code the prompt is written for, the files it reads, the tools it is given — before asking about it. When any item is still open, tell the user the task brief is not complete and use the `get-aligned` skill to interview them about the open items. If that skill is not installed, ask the user to add it — `/plugin install productivity-skills@draekien-skills` in a harness with plugin support, or `npx skills add draekien/skills --skill "get-aligned"` anywhere else. When the user asks to proceed with items still open, or no one can answer, take the most literal reading of the request and list each open item under **Assumptions**.

Done when every item of the task brief is answered or listed under **Assumptions**.

## Draft

- **Every line changes behaviour.** A line asking for something the guidance set says the target model already does is a no-op at best, and overcorrects at worst.
- **Keep measured wording.** Text in a code block in the references is a sample prompt measured as written: keep it verbatim, filling only bracketed placeholders and dropping only the parts its entry says may be dropped. Text quoted inline may be adapted to the task.
- **State placement.** Where an entry says where a line belongs, the record says so.

Done when every line of the draft cites the entry that supports it or is task content — what the model must know about this job that only the user's request supplies: its subject, inputs, audience, and constraints.

## Revise

Give every line of the existing prompt one verdict — keep, remove, rewrite, or add — against the guidance set.

The main finding is the **carried-over line**: an instruction written for an earlier model that the guidance set says to remove or soften. The tier references list the known ones under "Remove from older prompts"; look for them by meaning, not wording, and keep a line the guidance set endorses. With the general-only guidance set there is no such list: flag only lines a general entry contradicts. Task content is kept unchanged, never rewritten for style.

Done when every line of the existing prompt has a verdict, and every remove, rewrite, or add cites an entry.

## Deliverable

The deliverable is two parts, kept apart so the prompt can be copied or loaded as it is:

- **Prompt file** — the prompt text and nothing else: no frontmatter, header, fences, or commentary. Its first line is the prompt's first line.
- **Record** — the data around the prompt: target, kind, guidance, assumptions, placement, task content, and sources. It quotes single lines of the prompt only to cite them, never the prompt as a whole.

Cite each entry by expanding its source key to the URL in that reference's table, followed by the heading; write "introduction" in place of a heading the entry gives as "(introduction)", separate several sources with semicolons, and never construct an anchor. Carry an entry's `(predecessor: <model>)` or `Measured on <model>` label into its source line.

A draft's record:

```markdown
---
target: <model-id, or "unresolved">
kind: <api | product>
guidance: <tier references' snapshot date, or "general only">
---

**Target:** <model-id> (<source, or "inferred from <source>, confirmed|unconfirmed">) · **Kind:** <API prompt | product prompt> · **Guidance:** <tier references' snapshot date, or "general only, snapshot <date>: <target> is not supported; the supported <tier> model is <model>">
**Assumptions:** <each fallback taken, or "none">
**Placement:** <where each line goes, where an entry states it; "not stated" otherwise>
**Task content:** <lines that are task content, or "none">

**Sources**
- "<line>" — <URL> § <heading>; <URL> § <heading> (predecessor: <model>, when applicable)
```

A revision's record replaces the body after the header line and **Assumptions** with:

````markdown
```diff
- <removed line>
+ <added or rewritten line>
```

- `-` "<removed line>" — <reason> — <URL> § <heading>
- `+` "<added or rewritten line>" — <reason> — <URL> § <heading>

**Placement:** <where each added or rewritten line goes>
**Kept:** <each unchanged line with "task content" or its source; above 40 kept lines, a count instead — removed, rewritten, and added lines are always listed>
````

The prompt file of a revision holds the revised prompt in full.

## Save the deliverable

With a file system available, write both parts to `<outputDir>/<prompt-slug>/`, where `<prompt-slug>` is the kebab-cased name of what the prompt is for, such as `release-notes-agent`:

```text
<outputDir>/release-notes-agent/
  prompt.md      the prompt file
  record.md      the record
```

With several target models, write one directory per model, suffixing the slug with the model ID.

- **Revising a saved prompt overwrites both files.** `prompt.md` always holds the current prompt and `record.md` the latest draft or revision; version control keeps earlier versions.
- **Revising a prompt from elsewhere** — a repository file, pasted text — creates a new directory. Never edit the prompt's own file; the reply names that file as where the revised prompt goes.
- **A new draft never overwrites.** When the slug is taken by a different prompt, ask for another name. Fallback: append `-2`, `-3`, and so on.

If the output directory is under `.draekien/` and `.draekien/` does not exist, confirm its creation with the user before the first write. If the user declines or names another directory, persist the choice with `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill prompting set outputDir <path>` and write nothing until a confirmed directory exists. Fallback: deliver in the reply only and say it was not saved.

In the reply, give the prompt file in a fenced block, then the record. Without a file system, the reply is the whole deliverable and says it was not saved.

Done when both files are written and the reply gives their paths, or the reply says why nothing was saved.

## Gotchas

- **The snapshot can trail the docs.** Each reference records its snapshot date. When the user reports behaviour the guidance set contradicts, or names guidance it lacks, say the snapshot may be out of date rather than arguing from it.
