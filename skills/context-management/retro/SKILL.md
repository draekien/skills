---
name: retro
description: Reviews a coding session's transcript and recommends changes to the agent's environment — navigation pointers, automated checks, review rules, tool economy, information access — so the next session avoids the same mistakes. Applies them with --fix.
argument-hint: "[--fix safe|unsafe]"
disable-model-invocation: true
---

# Retro

A retro changes the **environment** the next agent works in, never the code this session produced. A mistake fixed in the code is fixed once; the same mistake fixed in the environment — a check that fails on it, a pointer to the file the agent could not find — is fixed for every later session.

Every finding is **evidence-led**: it cites the moment in the transcript that shows the problem — a failed call, a retry, a long search, a correction the user had to make. A recommendation with no evidence in the session is a general repo audit, which is a different job. Three **absence findings** are exempt, because their evidence is something missing rather than a moment: a repo with no **guardrail**, a repo with no review stage, and a root steering file missing the `REVIEW.md` pointer.

## Available scripts

- **`scripts/condense-session.py`** — condenses a JSONL transcript from `~/.claude/projects` into a summary (tool-call counts, errors, token usage, largest results, repeated calls, subagent rollups) and a timeline. `--list` prints recent sessions for the current directory.

## Read the session

- **No argument** — the session is the current one, already in context. If the context has been summarised, the early turns are gone from it: run `--list` and condense the entry whose `first_prompt` matches this conversation's opening. If none matches, or more than one does, ask the user for the id.
- **A session id or a `.jsonl` path** — condense it:

  ```bash
  uv run scripts/condense-session.py <session-id-or-path> --output <tmp-file>
  ```

  Always pass `--output`; a long timeline overflows a tool result. Read the `summary` object first, then the `timeline` in ranges of at most 200 lines, never the whole file at once. A summary with zero tool calls and an empty timeline means the file is not in the format the script parses.
- **Any other transcript** — read it directly in ranges of at most 200 lines, and say in the report that no summary was computed.

The script records each result's size, not its content. Judge a large result from its call and its size; re-run the call only when the size alone cannot settle whether it was wasted.

Done when every error, every repeated call, every user correction, and the call behind each of the largest results is either tied to a finding or judged harmless.

## Check what exists first

Before proposing any check, read what the repo already runs: its package or build manifest's `lint`/`check`/`test` scripts, its CI workflows, its pre-commit configuration, its `REVIEW.md`. A check that exists but is unwired, or wired and silently passing on the session's mistake, is the finding — wiring it is cheaper and safer than building a second one. Run the existing check against the session's mistake to see whether it fails; the transcript shows what the agent did, not why a check did not catch it. Where the mistake has since been fixed, reproduce it in a scratch copy; where it cannot be reproduced, mark the finding unverified and say why.

## Categories

Read each category against the evidence; skip a category the session gave no evidence for.

- **Navigation** — the agent took many calls to find a file, read the wrong file first, or missed a dependency between files. The fix is a **navigation pointer**: one line in the root steering file naming the file and when to read it. The root steering file is the `CLAUDE.md` or `AGENTS.md` that holds the repo's guidance; where one only imports the other, it is the imported one. Pointers are the only content that file should gain, because every agent in the repo loads it on every turn.
- **Automated checks** — the agent made a mistake a linter, type checker, test, or filesystem check could have caught. A repo with no guardrail — no pre-commit hook and no CI job running its lint, type check, or tests — is a finding on its own, whether or not the session hit it.
- **Coding standards** — the agent broke a convention and nothing caught it. Classify the violation before choosing the fix:
  - **Mechanical** — a fixed syntactic pattern, a banned API, an import shape, a file-location rule. It gets a deterministic check: a custom rule in the repo's own linter, a pre-commit hook, or a CI job, whichever the repo's existing guardrail makes cheapest. Never a prose rule.
  - **Judgement call** — consistency across files, matching the surrounding style, anything no program can decide. It gets a rule in `REVIEW.md`, for the reviewer.
- **Tool economy** — a call returned far more than the agent used, the same call ran repeatedly, or a custom CLI or MCP server is token-heavy. Propose the narrower call or the tooling change.
- **Information access** — a fact the agent needed was not reachable: dev server logs, a third-party service's state, a schema. Propose the access, read-only by default.

Steering-file problems — a rule in `CLAUDE.md`/`AGENTS.md` the agent ignored, a rule that changes nothing, a file too large for what it teaches — are not audited here, and `maintain-agent-docs` is not invoked from here either. Report the evidence with the command for the user to run: `/maintain-agent-docs --scope prune` for lines that should come out, `/maintain-agent-docs --scope contexts` for rules in the wrong file. It ships in this plugin; if it is missing, install it with `/plugin install context-management-skills@draekien-skills`, or `npx skills add draekien/skills --skill "maintain-agent-docs"`.

### Why rules go to the reviewer

Work passes through two stages. The implementing agent carries the most context: it explores, writes, and debugs. The reviewing agent receives a diff and needs no exploration. A rule placed where the implementer reads it costs context on every task; placed where only the reviewer reads it, it costs context only at review. So judgement-call rules go to `REVIEW.md`, and the root steering file gains one pointer line so a local reviewer reaches them:

```markdown
When reviewing a change, read `REVIEW.md` and apply its rules.
```

Before writing the pointer, check which files each reviewer reads, on `https://code.claude.com/docs/en/code-review.md`, section "What the review reads and edits". The pointer exists for a reviewer that reads the root steering file but not `REVIEW.md`; if every reviewer the repo uses reads `REVIEW.md` directly, skip it. A root steering file that needs the pointer and lacks it is an absence finding. A repo with no review stage at all — no `/code-review` use, no reviewer agent, no review workflow in CI — gets a finding of its own, because a judgement-call rule then has no reader.

## Rank and report

Rank by what the problem costs if it recurs:

1. A mistake that reached a commit, or that only the user caught.
2. A mistake the agent caught itself, after rework.
3. Wasted calls or tokens with no mistake.

Within a tier, a problem seen more than once in the session ranks higher. Absence findings rank after all three tiers.

Load `writing-for-agents` before writing any line an agent will read — a pointer, a `REVIEW.md` rule, a check's error message. It ships in the `technical-writing-skills` plugin: `/plugin install technical-writing-skills@draekien-skills`, or `npx skills add draekien/skills --skill "writing-for-agents"`.

Report each finding in rank order:

```markdown
### 1. <category>: <one-line problem>

- **Evidence:** <timestamp> — <the call, error, or correction>, or "absence"
- **Recommendation:** <the exact line, rule, or check to add>
- **Action:** <this finding's cell in the --fix table for the flag this run used>
```

A run with no findings says so and names the categories it checked.

## Apply with --fix

| Finding | no flag | `--fix safe` | `--fix unsafe` |
| --- | --- | --- | --- |
| Navigation pointer | report | apply | apply |
| Judgement rule to `REVIEW.md`, plus its pointer | report | apply | apply |
| New check for a mechanical violation | report | proposal | build and prove |
| Existing check unwired or broken | report | proposal | wire and prove |
| Tool economy | report | proposal | proposal |
| Information access | report | proposal | proposal |
| Steering-file problem | hand-off | hand-off | hand-off |

**Prove** a check before keeping it: run it against the session's mistake and confirm it fails, then against the corrected code and confirm it passes. A check that passes on the mistake matches nothing, and is removed rather than committed. Information access is never applied, in any mode, because it touches credentials and external services. Applied fixes are left uncommitted for the user to review.

Done when every finding is reported, every applied fix is listed with the file it changed, and every built check has both proof runs shown.
