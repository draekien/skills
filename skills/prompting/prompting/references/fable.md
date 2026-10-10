# Fable 5.1

Snapshot: 2026-10-07. Model: Fable 5.1 (`claude-fable-5-1`); Mythos 5.1 shares this guidance. Predecessor: Fable 5 — "Your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes"; entries taken from its page are marked `(predecessor: Fable 5)`, and a Fable 5.1 entry wins where they disagree. Each entry ends with its source key and heading.

| Key | Source |
| --- | --- |
| F51 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1` |
| F5 | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5` |
| BP | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` |
| HR | Repository convention, not Anthropic guidance |

## Defaults

- Thinking is always on; adaptive is the only mode. — BP § Leverage thinking & interleaved thinking capabilities
- Executes very long tasks without much guidance on methodology, especially when the goal is clear. — F51 § Finish the whole task
- Completes multiday, goal-directed runs with strong instruction retention. (predecessor: Fable 5) — F5 § Capability improvements
- Teams seeing the best outcomes apply it to their hardest unsolved problems. (predecessor: Fable 5) — F5 (introduction)
- Writes fewer user-facing updates during long tool-calling turns than Fable 5, more so at higher effort. — F51 § Ask for user-facing progress updates
- Formats less than earlier models: less bold, fewer headers, lists, and quotation marks. Its prose has few stock phrases but can run dense, with long sentences and few paragraph breaks. — F51 § Formatting in chat; F51 § Writing density
- Instruction following is strong enough that one brief instruction steers a behaviour; there is no need to enumerate each case. (predecessor: Fable 5) — F5 § Strong instruction following
- Performs better when told why: "I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request]." (predecessor: Fable 5) — F5 § Give the reason, not only the request
- Dispatches parallel subagents more readily than prior models, and sustains them and long-running peer agents dependably. (predecessor: Fable 5) — F5 § Capability improvements; F5 § Parallel subagents
- As a lead agent it often stops to wait for a subagent's result even when the harness lets it keep working. — F51 § Let the lead agent keep working while subagents run

## Remove from older prompts

- Anti-formatting blocks written to suppress bullets and bold; they now suppress structure the content needs. Replace with the formatting rule below. — F51 § Formatting in chat; BP § Control the format of responses
- Lines that suppress narration, such as "hold all findings for the final response". — F51 § Ask for user-facing progress updates
- Instructions to write out thinking or reasoning — in prompts, skills, and tool descriptions — which invite `reasoning_extraction` declines. Ask for a short explanation or a summary of actions instead. — F51 (introduction)
- Prescriptive skills and step lists written for earlier models; they can degrade output. Review and remove where default behaviour is better. (predecessor: Fable 5) — F5 § Recommended scaffolding changes

## Add when the behaviour matters

- **Progress updates**, for human-in-the-loop work: "Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture." — F51 § Ask for user-facing progress updates
- **Dense prose.** In a user message (preferred) or the system prompt — the long form, or "Please remove all mannered prose." — F51 § Writing density

  ```text
  Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
  ```

- **Formatting rule**: "Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose." — F51 § Formatting in chat
- **Quoting sources.** When summaries reproduce source wording unmarked, add one complete correct example to the system prompt — request, response, and a `<rationale>` saying why it is correct — with the tool-call lines written in the application's own tool name. The source's example compares two outlets' coverage in the assistant's own words with one short marked quote. — F51 § Quoting retrieved sources
- **Finish the whole task**, for autonomous work. Use both blocks; under a length limit, the first alone keeps most of the effect. Keep the first block's opening sentence as written; if the model must stop for specific confirmations, add a sentence after it listing them. The first block can make the model ask less about ambiguous requests; check that trade-off on real tasks. — F51 § Finish the whole task

  ```text
  You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not.

  Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.

  Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide.

  Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
  ```

  ```text
  # Delivering work
  The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it. Read ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. If you see a real problem with the task as specified, say so in a sentence or two and keep building under stated assumptions; if the user hears the concern and reaffirms, that is their decision, so deliver the full request.

  If a question comes up partway, first do everything that doesn't depend on the answer; then state the assumption you made, or — when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a turn that also delivers that progress. If one part turns out to be blocked, complete every other part in full and say exactly what you left out and why — the whole task is the deliverable, and scaling it down is the user's call, not yours. A step you have decided on is something to run, not to announce: describing the next step and ending the turn leaves it undone until the user replies.

  Keep changes to what the request needs. Something else you notice worth doing — cleanup or documentation the task didn't call for, a change to a file the task didn't require — is a suggestion to make at the end, not a change to make; actions clearly beyond what the ask implies, and risky or destructive ones, still need the user's go-ahead.
  ```

- **Scope and tests**, on open-ended features: "If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well. Verify your work however you like; scratch scripts and quick checks need not be kept. Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files. This is about extras only: implement every behavior the task asks for, completely." — F51 § Keep changes and tests to what the task asks for
- **Search at low effort**: "When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. This holds even when you have some background on it — partial background is exactly what makes an out-of-date answer sound authoritative, so familiarity is not a reason to skip the search." — F51 § Search triggering at low effort
- **Targeted edits**, when whole files are rewritten for small changes: "The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing." — F51 § Prefer targeted edits over whole-file rewrites
- **Act, don't survey**, when it overplans on ambiguous tasks: "When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks." (predecessor: Fable 5) — F5 § Longer turns by default
- **Brevity**: "Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more. The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon." (predecessor: Fable 5) — F5 § Strong instruction following
- **Checkpoints**: "Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise." (predecessor: Fable 5) — F5 § Strong instruction following
- **Grounded progress claims** on long runs: "Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging." (predecessor: Fable 5) — F5 § Ground progress claims during long runs
- **Readable final summaries** after long agentic work: tell it that working shorthand is fine between tool calls but the final message is a re-grounding for a reader who saw none of it — outcome first, complete sentences, terms spelled out, no arrow chains or invented labels, clear over short. (predecessor: Fable 5) — F5 § Readability when communicating with the user
- **Subagents**: use them frequently, say when delegation is appropriate, and prefer asynchronous communication over blocking until each subagent returns — "Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context." (predecessor: Fable 5) — F5 § Parallel subagents
- **Verifier interval**, on long runs; fresh-context verifier subagents tend to outperform self-critique: "Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification." (predecessor: Fable 5) — F5 § Recommended scaffolding changes
- **Memory**: give a place to write lessons — "Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong." (predecessor: Fable 5) — F5 § Construct a memory system

## House rules

Entries here are this repository's conventions. No Anthropic page states them; cite them as `HR`, never as Anthropic guidance.

- **Orchestrator first**, in every prompt where the model leads agentic work and can dispatch subagents. Put it with the **Subagents** entry, which supplies the delegation mechanics: "You are the orchestrator. Split the task into subtasks and delegate their execution to subagents. Keep for yourself the work only the lead can do: planning, briefing each subagent with the context it needs, integrating results, and checking each result's evidence before accepting it. Do a step directly only when it takes a handful of tool calls, or when briefing a subagent would cost more than doing it." — HR § Orchestrator first
- **No scripted subagent briefs**, in every prompt with the **Orchestrator first** line. The orchestrator writes the subagents' briefs, so leave out how to split the task, which subagents to dispatch, and what to tell each one: their prompts, wording, roles, and step lists. Give the orchestrator what only the prompt's author knows — the goal, inputs, constraints, and what done looks like — and state a constraint every subagent must follow once, as a constraint on the task. In revise mode, remove lines that script a subagent's brief. Prescriptive step lists can degrade Fable's output, and it carries out long tasks without guidance on method. — HR § No scripted subagent briefs; F5 § Recommended scaffolding changes (predecessor: Fable 5); F51 § Finish the whole task

## Refusals

- Phrasing that raises false-positive safety declines: compile-check phrasing (ask "Are there any bugs in this program?" instead of "Does this program compile without errors?"), lesser-known languages (supply their documentation), and base64 in tool output (remove it). — F51 § Reduce safeguard false positives
