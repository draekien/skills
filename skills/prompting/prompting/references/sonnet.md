# Sonnet 5.5

Snapshot: 2026-10-07. Model: Sonnet 5.5 (`claude-sonnet-5-5`). Predecessor: Sonnet 5 — "the patterns in Prompting Claude Sonnet 5 remain a reasonable starting point"; entries taken from it are marked `(predecessor: Sonnet 5)`, and a Sonnet 5.5 entry wins where they disagree. Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| S55 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5` |
| S5 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5` |
| PB | `https://claude.dev/blog/building-with-claude-sonnet-5-5/` |

## Defaults

- Fits well-scoped work with a clear spec and a way to check the result; for the hardest long-horizon work, an Opus model is the better choice. — S55 (introduction); PB § Choosing between Sonnet 5.5 and Opus 5.5
- Thinking is on by default (adaptive). — PB § 1. Turn off upfront thinking with between_tools
- At `low` and `medium` on long agentic tasks it checks in before finishing more often; at every effort it tends to add tests, docs, and small supporting files that fit the repository, more at higher effort. — S55 § Steer initiative and scope
- Follows instructions literally, especially at lower effort: it does not generalise an instruction from one item to another or infer unrequested work. State scope explicitly: "Apply this formatting to every section, not just the first one." (predecessor: Sonnet 5) — S5 § More literal instruction following

## Remove from older prompts

- Sonnet 5 workarounds — refusal steering, tool-call retry shims, "do not be lazy" — then re-run evals before tuning anything else. — PB § Remove Sonnet 5 workarounds
- Language that discourages tools — "only use tools when strictly necessary", "minimize tool calls". — S55 § Tool use in chat and knowledge work
- "Hold all findings for the final response" and similar lines that suppress progress notes. — S55 § User-facing progress updates
- Instructions to write out reasoning in the response; they invite `reasoning_extraction` declines. Ask for a short explanation or a summary of actions instead. — S55 § Safeguard refusals
- "Think less" instructions: asking for less thinking in the system prompt doesn't reliably reduce it. — S55 § Calibrate effort
- Any instruction telling the model not to think: it makes it more likely that the model writes internal XML tags in its visible output. — S55 § Running without up-front thinking
- Scaffolding that forces interim status messages ("After every 3 tool calls, summarize progress"). (predecessor: Sonnet 5) — S5 § User-facing progress updates
- Review filters such as "only report high-severity issues", "be conservative", "don't nitpick": followed faithfully, they cut recall. (predecessor: Sonnet 5) — S5 § Code review harnesses

## Add when the behaviour matters

- **Carry work through** at `low` and `medium` effort, and **limit scope** at any effort. Use both paragraphs, or only the second to limit additions. Sessions at low effort then run longer and cost more; keep separate rules for risky actions. — S55 § Steer initiative and scope

  ```text
  Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.

  When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.
  ```

- **Self-started review** at `xhigh` and `max`: cut session cost by about a third at `max` with no quality change. — S55 § Steer initiative and scope

  ```text
  When the work the user asked for is done and its checks pass, stop and report. Don't start extra rounds of review or hardening on your own, and don't launch reviewer sub-agents unless the user asked for a review. If you think a deeper review is worth doing, say so at the end.
  ```

- **Ideas, not builds**, on open-ended requests: "When the user asks for ideas, options or a plan, give them that and stop. Don't start building or changing anything until they say to go ahead." — S55 § Steer initiative and scope
- **Progress at set points.** A system-prompt line asking for a line on what it is about to do before the first tool call and a short recap at the end; most useful with a human in the loop. — S55 § User-facing progress updates
- **Search for current details**, when the application has a search tool: "Use the search tool to check specifics that may have changed since your training, such as what is allowed, required or charged, even when you feel confident. For researched work such as a report or a comparison, gather current sources rather than writing from your training knowledge." — S55 § Tool use in chat and knowledge work
- **Real checks** when changes are reported done without test or build output, mainly at `low` effort. — S55 § Verification on coding tasks

  ```text
  When you change code that can be run, built, or type-checked, run a real check that exercises the change before reporting it done: the project's tests, type-checker, or build, or the changed command itself. A syntax-only check, or a check command that failed to start, does not count; if all that is missing is the project's declared dependencies, install them with its own package manager and lockfile (e.g. npm install, pip install -r requirements.txt), never via sudo or the system package manager, unless told not to. Only if no real check can run here, say which one you did not run and why instead of reporting the change as done.
  ```

- **Length.** "Provide concise, focused responses. Skip non-essential context, and keep examples minimal." Positive examples of the wanted concision work better than prohibitions. (predecessor: Sonnet 5) — S5 § Response length and verbosity
- **Warmer voice.** "Use a warm, collaborative tone. Acknowledge the user's framing before answering." (predecessor: Sonnet 5) — S5 § Tone and writing style
- **Design.** Generic instructions swap one default palette for another. Either specify a concrete direction (palette hexes, type, radius, layout, motion), or: "Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction." Optionally add a short `<frontend_aesthetics>` block naming generic fonts, cliched palettes, and cookie-cutter layouts to avoid. (predecessor: Sonnet 5) — S5 § Design and frontend defaults
- **Review coverage.** For a finding stage: "Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them." For a single pass, state the bar concretely instead of "important". (predecessor: Sonnet 5) — S5 § Code review harnesses
