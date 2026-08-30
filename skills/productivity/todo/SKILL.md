---
name: todo
description: Parks an idea as a todo in this project's tracker — markdown files, GitHub issues, or Linear — or lists what is already parked. Use it when an idea surfaces mid-task and you do not want to act on it yet.
argument-hint: "[idea]"
disable-model-invocation: true
---

Captures an idea without derailing the work in progress. Where the todos live is a per-project choice, asked once and persisted; everything after that is delegated, so the capture costs the current session almost nothing.

## Available scripts

- **`scripts/skillsrc.py`** — Reads and writes `todo` config from `.draekien/.skillsrc`.
- **`scripts/todos.py`** — Adds, lists, and updates todos in the markdown backend, in either layout. Owns that file format; never hand-write markdown todos.

## Config

Read the backend first, every invocation:

```bash
uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill todo get backend
```

An empty line means this project has never been configured — run **Setup**. Otherwise read the remaining keys for that backend, then **Route**.

| Key | Backend | Default | Meaning |
|---|---|---|---|
| `backend` | all | none — asked at Setup | `markdown`, `github`, or `linear` |
| `markdownPath` | markdown | `docs/todos` | Directory under `file-per-todo`; file path under `single-file` |
| `markdownLayout` | markdown | `file-per-todo` | `file-per-todo` or `single-file` |
| `githubLabels` | github | `todo` | Comma-separated labels applied to every captured issue |
| `linearTeamId` | linear | none — asked at Setup | Team the issues belong to |
| `linearProjectId` | linear | empty | Optional project to file issues under |

### Setup

Setup stays with you and the user — a delegate cannot ask anything. Ask which backend, then only that backend's follow-up questions: path and layout for markdown, labels for GitHub, team and optional project for Linear. Offer the defaults above as the accept-and-move-on answer.

Confirm the choices, create `.draekien/` if it is absent (confirming that too), then persist each key:

```bash
uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill todo set <key> <value>
```

Carry the answers straight into **Route** — do not make the user re-state the idea they came in with.

## Route

An idea goes to **Capture** when the user supplies it as an argument or proposes it in the message that invoked the skill. Earlier discussion is context for enriching that idea, never the idea itself. A bare invocation with no idea in it means the user wants to see what is already parked — go to **List**.

## Capture

Fork your own session: a delegate that inherits this conversation, so it can enrich the idea from context you have already paid for, and its backend writes never re-enter your window. Do not draft the todo yourself — drafting in your own context is the exact cost the fork exists to avoid.

Brief the fork with the idea as the user put it, the resolved config values, and the instruction to follow the Capture rules in [references/backends.md](references/backends.md).

Fire and forget. Confirm the hand-off in one line, resume the work in progress, and relay the fork's result — the file path or issue URL, or a backend failure — when its notification arrives.

## List

Dispatch to a fresh, fast, low-cost delegate. Listing needs no conversation history, so its prompt must be self-contained: the resolved config values, this skill's directory — the script paths in the rules resolve relative to it — the absolute path to `references/backends.md`, and the instruction to follow the List rules there.

Wait for it, since the user asked for the list, and relay what it returns. If any todo comes back flagged `needs-expansion`, offer to **Expand** those now.

## Expand

An idea captured with no surrounding context holds a title and nothing that makes it actionable weeks later. Expanding fills that gap: ask the user one or two questions — what it covers, what triggered it, roughly how big — then hand the rewrite to a fork, which follows the same Capture rules but updates the existing todo in place and clears the flag.

The interview stays with you, for the same reason Setup does.

## Gotchas

- A missing `backend` value is not markdown. Guessing a default skips the one question the skill exists to ask once, and the user's real tracker never sees the todo — run Setup.
- `markdownPath` reverses meaning between layouts: a directory under `file-per-todo`, a single file under `single-file`. Read it against `markdownLayout` before writing, or the todo lands somewhere List will never look.
- A backend that is not usable right now — GitHub CLI missing or unauthenticated, Linear connection absent — stops the run. Write nothing, change no config, and report what to fix. Quietly falling back to a markdown file splits the todo list across two places.
- `skillsrc.py get` prints an empty line and exits 0 for a key that is not set. Absence is the normal first-run state, not an error to report.
- Config writes need the user's confirmation before the `set` runs. The todo write itself does not — that is the whole point.
