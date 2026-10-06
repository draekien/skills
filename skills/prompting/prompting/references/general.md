# General guidance

Snapshot: 2026-10-07. Each entry ends with its source key and heading. `Measured on <model>` marks an entry the source states for that model only.

| Key | Source |
| --- | --- |
| BP | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` |
| CE | `https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/` |

## Clarity and context

- Be explicit about the output, its format, and its constraints. Ask for "above and beyond" behaviour outright instead of expecting it to be inferred. Test: a colleague with no context could follow the prompt. — BP § Be clear and direct
- Use numbered steps when order or completeness matters. — BP § Be clear and direct
- Give the reason behind a constraint; the model generalises from the reason. "Your response will be read aloud by a text-to-speech engine, so never use ellipses" beats "NEVER use ellipses". — BP § Add context to improve performance
- A one-sentence role in the system prompt focuses behaviour and tone. — BP § Give Claude a role

## Structure

- Wrap each kind of content — instructions, context, examples, inputs — in its own consistently named XML tag; nest tags for hierarchy, such as `<document index="n">` inside `<documents>`. — BP § Structure prompts with XML tags
- Examples: 3–5, relevant to the real use case, diverse enough to avoid unintended patterns, wrapped in `<example>` tags inside `<examples>`. — BP § Use examples effectively
- Long inputs (20k+ tokens): put documents at the top and the query, instructions, and examples after them; queries at the end can improve quality by up to 30 percent in tests, most with complex, multidocument inputs. Wrap each document in `<document>` tags with `<document_content>` and `<source>` subtags. — BP § Long context prompting
- For long-document tasks, ask for the relevant quotes first, in `<quotes>` tags, then the task over those quotes. — BP § Long context prompting

## Output and formatting

- Say what to do, not what not to do: "Your response should be composed of smoothly flowing prose paragraphs" over "Do not use markdown". — BP § Control the format of responses
- XML format indicators steer format: "Write the prose sections of your response in `<smoothly_flowing_prose_paragraphs>` tags." — BP § Control the format of responses
- The prompt's own style leaks into the output: removing markdown from the prompt reduces markdown in the response. — BP § Control the format of responses
- Plain-text math needs an explicit instruction; the default is LaTeX. — BP § LaTeX output
- The default style is concise and may skip summaries after tool calls. To get one: "After completing a task that involves tool use, provide a quick summary of the work you've done." — BP § Communication style and verbosity

## Tool use

- Name the action to get the action: "Change this function to improve its performance", not "Can you suggest some changes". — BP § Tool usage
- To act by default, or to hold back by default — BP § Tool usage:

  ```text
  <default_to_action>
  By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed, using tools to discover any missing details instead of guessing. Try to infer the user's intent about whether a tool call (e.g., file edit or read) is intended or not, and act accordingly.
  </default_to_action>
  ```

  ```text
  <do_not_act_before_instructions>
  Do not jump into implementation or change files unless clearly instructed to make changes. When the user's intent is ambiguous, default to providing information, doing research, and providing recommendations rather than taking action. Only proceed with edits, modifications, or implementations when the user explicitly requests them.
  </do_not_act_before_instructions>
  ```

- Write tool instructions at normal strength. Prompts written to fix undertriggering overtrigger on models more responsive to the system prompt: "CRITICAL: You MUST use this tool when..." becomes "Use this tool when...", and "If in doubt, use [tool]" lines come out. Measured on Opus 4.5 and Opus 4.6. — BP § Tool usage; BP § Overthinking and excessive thoroughness
- Parallel calls happen without prompting; this raises the rate to near 100 percent — BP § Optimize parallel tool calling:

  ```text
  <use_parallel_tool_calls>
  If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
  </use_parallel_tool_calls>
  ```

## Thinking

- Prefer a general instruction ("think thoroughly") over a hand-written step-by-step plan for the model's reasoning. — BP § Leverage thinking & interleaved thinking capabilities
- Worked examples shape how the model reasons: present each as problem, method, answer. — BP § Leverage thinking & interleaved thinking capabilities
- When adaptive thinking triggers more than wanted — not Haiku 4.5, which uses manual extended thinking: "Thinking adds latency and should only be used when it will meaningfully improve answer quality - typically for problems that require multistep reasoning. When in doubt, respond directly." — BP § Leverage thinking & interleaved thinking capabilities
- Self-check: append something like "Before you finish, verify your answer against [test criteria]."; it catches errors in coding and math. — BP § Leverage thinking & interleaved thinking capabilities
- To stop the model reopening decisions: "When you're deciding how to approach a problem, choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning. If you're weighing two approaches, pick one and see it through. You can always course-correct later if the chosen approach fails." Measured on Opus 4.6. — BP § Overthinking and excessive thoroughness

## Agentic work

- Risky actions. Measured on Opus 4.6. — BP § Balancing autonomy and safety:

  ```text
  Consider the reversibility and potential impact of your actions. You are encouraged to take local, reversible actions like editing files or running tests, but for actions that are hard to reverse, affect shared systems, or could be destructive, ask the user before proceeding.

  Examples of actions that warrant confirmation:
  - Destructive operations: deleting files or branches, dropping database tables, rm -rf
  - Hard to reverse operations: git push --force, git reset --hard, amending published commits
  - Operations visible to others: pushing code, commenting on PRs/issues, sending messages, modifying shared infrastructure

  When encountering obstacles, do not use destructive actions as a shortcut. For example, don't bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be in-progress work.
  ```

- Research: define what a successful answer is, ask for verification across sources, and for complex research ask for competing hypotheses with tracked confidence. — BP § Research and information gathering
- Subagent use: "Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state. For simple tasks, sequential operations, single-file edits, or tasks where you need to maintain context across steps, work directly rather than delegating." Measured on Opus 4.6, which overuses subagents. — BP § Subagent orchestration
- Multi-context-window work: a distinct first-window prompt that sets up tests and scripts; tests tracked in a structured file such as `tests.json`; setup scripts such as `init.sh`; a fresh window told what to read ("Review progress.txt, tests.json, and the git logs."). — BP § Workflows across multiple context windows
- State: structured formats such as JSON for status, free text for progress notes, git for checkpoints. — BP § State management best practices
- Scratch files: "If you create any temporary new files, scripts, or helper files for iteration, clean up these files by removing them at the end of the task." — BP § Reduce file creation in agentic coding
- Overengineering. Measured on Opus 4.5 and Opus 4.6. — BP § Overeagerness:

  ```text
  Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused:

  - Scope: Don't add features, refactor code, or make "improvements" beyond what was asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.
  - Documentation: Don't add docstrings, comments, or type annotations to code you didn't change. Only add comments where the logic isn't self-evident.
  - Defensive coding: Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).
  - Abstractions: Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task.
  ```

- Test-fitting — BP § Avoid focusing on passing tests and hardcoding:

  ```text
  Please write a high-quality, general-purpose solution using the standard tools available. Do not create helper scripts or workarounds to accomplish the task more efficiently. Implement a solution that works correctly for all valid inputs, not just the test cases. Do not hard-code values or create solutions that only work for specific test inputs. Instead, implement the actual logic that solves the problem generally.

  Focus on understanding the problem requirements and implementing the correct algorithm. Tests are there to verify correctness, not to define the solution. Provide a principled implementation that follows best practices and software design principles.

  If the task is unreasonable or infeasible, or if any of the tests are incorrect, please inform me rather than working around them. The solution should be robust, maintainable, and extendable.
  ```

- Grounding in code — BP § Minimizing hallucinations in agentic coding:

  ```text
  <investigate_before_answering>
  Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer - give grounded and hallucination-free answers.
  </investigate_before_answering>
  ```

## Context engineering

Applies to instructions that persist across requests: system prompts, `CLAUDE.md`, skills, tool descriptions. The source addresses 5-generation models; its measurements were on Opus 5 and Fable 5.

- Give judgment, not rules. Strong guardrails written for earlier models are wrong for part of the prompts they cover and conflict with other instructions in the same context. "Write code that reads like the surrounding code: match its comment density, naming, and idiom." replaced a block of comment rules. — CE § Then: Give Claude rules
- For tools, design the interface instead of giving usage examples: tool-usage examples narrow exploration. Examples of output format and tone still work. A tool with a status enum and one rule replaced a 9,100-character tool description of lists and examples. — CE § Then: Give Claude examples
- Use progressive disclosure: move material needed only sometimes into skills or files loaded when needed, instead of putting it all up front. — CE § Then: Put it all upfront
- Put tool instructions in the tool description once; don't repeat them in the system prompt. — CE § Then: Repeat yourself
- Prefer references in code — a test suite, an HTML mockup — over prose descriptions. — CE § References
