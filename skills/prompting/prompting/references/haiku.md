# Haiku 5.5

Snapshot: 2026-10-09. Model: Haiku 5.5 (`claude-haiku-5-5`). Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| H55 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5` |

## Defaults

- Prompts written for Haiku 4.5 perform well without changes. — H55 (introduction)
- Thinking is on by default (adaptive). Effort sets how much it thinks: a prompt line telling it to answer directly did not stop it thinking. — H55 § Use effort to control thinking
- At `low` effort in long agent prompts it is more likely to skip a search, stop early, or skip a check. — H55 § Use effort to control thinking
- With a short system prompt it rarely stops before the work is done; with a long coding-agent system prompt at `low` effort it sometimes stops early and hands the task back. — H55 § Prevent early stopping in long agent prompts
- At `low` and `medium` effort it sometimes reports a code change as done without running a check. — H55 § Tell coding agents to verify their changes
- It sometimes writes reasoning-like text in the reply users see, more often with thinking off or at `low` effort. The source fixes this with adaptive thinking and `medium` effort, not with prompt text. — H55 § Keep reasoning out of user-facing text

## Remove from older prompts

- Lines telling the model to answer directly or think less: they do not reduce thinking. — H55 § Use effort to control thinking
- Blanket search rules such as "search for any present-day factual question, regardless of how confident you are": the model then searched on half the prompts that needed no search, with no gain in correct answers. — H55 § Accurate search results

## Add when the behaviour matters

- **Today's date**, whenever the model has a search tool, in the system prompt or the search tool's description. — H55 § Accurate search results

  ```text
  The current date is {{current_date}}.
  ```

- **Which facts to search for**, directly after the date, when the model skips searches — most often at `low` effort and with long system prompts. With a short system prompt at `medium` effort the date alone was enough. — H55 § Accurate search results

  ```text
  Your training data ends well before today's date. Records, office holders, prices, versions, rules and anything "latest" may have changed since then, so search for those before you answer, even when you feel sure. Facts that can't change need no search. When the answer depends on where the user is, put the user's country or region in the search query.
  ```

- **Carry work through and limit scope**, when an agent with a long system prompt stops early. Raising effort also reduces early stopping, at a higher cost. — H55 § Prevent early stopping in long agent prompts

  ```text
  Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.
  When the work the user asked for is done and checked, stop and report. Don't add new features, docs, or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.
  ```

- **Real checks**, when a coding agent reports results without checking its work. Costs more tokens. — H55 § Tell coding agents to verify their changes

  ```text
  When you change code that can be run, built, or type-checked, run a real check that exercises the change before reporting it done: the project's tests, type-checker, or build, or the changed command itself. A syntax-only check, or a check command that failed to start, does not count; if all that is missing is the project's declared dependencies, install them with its own package manager and lockfile (e.g. npm install, pip install -r requirements.txt), never via sudo or the system package manager, unless told not to. Only if no real check can run here, say which one you did not run and why instead of reporting the change as done.
  ```
