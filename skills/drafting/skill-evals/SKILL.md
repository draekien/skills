---
name: skill-evals
description: Builds and runs an empirical eval suite against an existing skill — measures whether its description activates correctly (precision and recall over a labelled prompt corpus) and whether loading it improves agent output (blind A/B against pre-committed criteria). Use when evaluating, testing, or measuring a skill's quality, validating a skill's triggers, or when the user says "eval this skill", "test this skill", "run a skill eval", "measure the impact of this skill", "check the description hit rate", "is this skill's description firing".
---

A skill makes two empirical claims, and the author's intuition cannot settle either. The `description` claims *I am the right tool for this class of situation* — an activation claim. The body claims *loading me makes the work better* — an impact claim. An eval measures whether each claim holds against evidence the author has not seen yet. The discipline is to commit to what a passing result looks like *before* running anything, then run an agent under controlled conditions and report the gap between claim and reality.

The eval is driven by an orchestrator that never performs the work it is measuring. It delegates every generation, every eval run, and every LLM judgement to a separate subagent with isolated context — because an agent that has already seen the skill, the labels, and the result the author is hoping for cannot produce an uncontaminated scenario, run, or verdict. Isolation is the mechanism that keeps each step honest. And the final word on whether the agent did a good job stays with the human author: the machinery narrows the question down to the cases worth looking at, it does not answer it.

Both eval modes ride one spine. Only what is held fixed and what is judged differ between them.

## The spine

Every eval, of either mode, is the same four moves. Skip one and the result stops meaning anything.

1. **Commit ground truth first.** Have an isolated subagent generate the candidate scenarios — corpus prompts (activation) or tasks (impact) — so they are shaped by the skill's purpose rather than by its exact wording or the result the author wants. Then the orchestrator commits their labels (activation) or success criteria (impact) — with the human author approving them before any eval run — derived from the skill's intent, never from outputs already seen. A criterion authored after the output exists describes the output, not the goal, and the eval can no longer fail.
2. **Run each scenario in its own isolated subagent.** Hold everything fixed except the one variable under test — the prompt (activation) or the presence of the skill (impact). One subagent per run, its context limited to that scenario and carrying nothing about the eval's purpose, the other runs, or the outcome anyone expects. Shared or carried-over context bleeds the answer from one run into the next; isolation is what makes "controlled" more than a label.
3. **Judge blind as a first pass, then validate with the human.** A judge subagent scores each result against the committed standard without being told which run the author hopes will win — blindness stops it from scoring the hope instead of the work. But an LLM judge shares the blind spots of the agents it judges and is swayed by the same plausible-but-wrong output, so its verdict is triage, not truth: it narrows the set the author has to inspect. The human author makes the final call on whether the agent did a good job. Where scoring is mechanical — comparing a fire/no-fire decision against a label — no judge subagent is needed, and the human instead reviews the misfires that scoring surfaces.
4. **Report the gap as a self-contained HTML artefact.** A single number ("80%") tells the author nothing they can act on. Render the specific misfires — *this* prompt that should have fired and didn't, *this* part of the output the skill failed to improve — into a self-contained HTML file (styles and scripts inlined, no external dependencies, opens offline) that lays the findings out visually so the author can take in the result at a glance and run the final validation quickly. For the activation eval, show precision and recall alongside the two named lists: the should-fire prompts it missed and the should-stay-silent prompts it fired on. For the impact eval, pair each task's two outputs with the judge's first-pass verdict and the committed criteria each delta served or missed, leaving the author's final call as the last step. The artefact is the deliverable; the grade is not.

The point of the eval is to find where the skill falls short, not to confirm it works. An eval that cannot produce a failing result is theatre. Treat a clean pass with suspicion and check the corpus and criteria were demanding enough to bite.

## Activation eval — does the description fire when it should, and stay silent when it shouldn't

A model-invocable skill is selected on its `description` alone. This mode measures the quality of that selection signal as a classifier: across realistic prompts, how often does the right call get made.

**Build a labelled corpus with both classes.** Positives are prompts where the skill genuinely ought to fire. Negatives are prompts where it ought to stay silent — and negatives are not optional. A corpus of positives only measures recall and silently calls it accuracy; it cannot detect a description so broad it fires on everything. The negatives that matter are the *near misses*: prompts in the same topic neighbourhood that a slightly-too-broad description would wrongly fire on. Easy negatives from unrelated domains pass trivially and prove nothing. Spend the effort on the hard ones at the boundary. Size each class so the rates are stable rather than swung by a single prompt — on the order of fifteen to twenty per class; a handful makes precision and recall too noisy to act on.

**Derive positives that test generalisation, not string-matching.** Give the generating subagent the skill's *purpose* but not its body, so the positives reflect how people phrase the need rather than echoing the description's own wording. Seed from the situations the skill is meant to serve, then paraphrase away from any literal trigger phrase — different vocabulary, implied rather than stated need, the request buried mid-sentence. A description that only fires on its own trigger phrases quoted verbatim is brittle in exactly the way this catches. If every positive is lifted word-for-word from the description, the eval tests the corpus, not the skill.

**Run the selection decision in isolation.** Present the skill's name and description to a subagent acting as the selector — alongside a realistic set of competing skill descriptions, because in production the choice is never the skill against nothing. The selector sees only the prompt and the competing descriptions, never the corpus label for that prompt; showing it the label leaks the answer and the run measures nothing. For each corpus prompt, record the binary: fire or no-fire.

**Score precision and recall separately, then read the misfires.** Recall is, of the prompts that should fire, how many did. Precision is, of the prompts where it fired, how many should have. They fail in opposite directions and demand opposite fixes, so a blended score hides the diagnosis. The actionable output is the two lists: false negatives (should-fire prompts it missed → the description is too narrow or its triggers too literal, broaden or add phrasings) and false positives (should-stay-silent prompts it fired on → the description is too broad, tighten the scope). Each named misfire points at the words to change.

## Impact eval — does loading the skill make the output better

This mode tests the body's claim that the skill changes the work for the better. The method is a controlled comparison: same task, same conditions, the skill present or absent as the only difference.

**Define task-specific success criteria from the skill's intent.** Ask what a great output does that a default one would not — the specific moves, omissions avoided, judgments made that the skill exists to instil. Generic quality ("is it good") rewards verbosity and cannot isolate the skill's contribution. Write these criteria down before any output exists.

**Choose representative tasks, more than one.** A single task declared representative is a guess, and agent outputs vary run to run. Use several tasks — on the order of three to five — spanning the skill's intended range, and where variance is a concern, repeat a task across a few fresh subagents so a lucky or unlucky single draw is not mistaken for the skill's effect.

**A/B with the skill as the only variable.** For each task, run two subagents with isolated context on the identical prompt: one with the skill's instructions in context, one without. Same task, same model, same everything else. The difference in their outputs is the skill's effect, isolated.

**Judge the pair blind, then hand the author the call.** A judge subagent scores both outputs against the criteria without being told which arm had the skill — blindness is what stops it from rewarding the output it was told to prefer. Treat that score as a first pass: an LLM judge can be convinced by the same polished-but-wrong output that would convince the agent it is judging, so the author validates the verdict rather than trusting it. The finding is the delta: where the skill changed the output and whether that change served the criteria. A skill that produces no delta is not earning its context cost. A skill that produces a delta the criteria do not value is teaching something, but not the thing it claims — and that gap is the most useful thing the eval can surface.

## Anti-patterns

Each of these produces a number that looks like a result and means nothing. Name them on sight.

- **Recall theatre** — a positives-only corpus reporting a high hit rate. Says nothing about over-firing; a description that fires on everything scores perfectly. Hard negatives are the cure.
- **Verbatim-trigger corpus** — positives copied word-for-word from the description, so the eval confirms string-matching rather than whether the skill generalises to how people actually phrase the need.
- **Criteria drift** — writing or loosening success criteria after seeing the outputs until the skill passes. The criteria must predate the outputs, or the eval is a post-hoc justification wearing the costume of a test.
- **Verdict leakage** — the judge knows which output came from the skill. It then scores the label, not the work, and every result tilts toward the expected answer.
- **Context bleed** — generation, the eval runs, or judging share or reuse context, so the skill's wording, the committed labels, or one run's output seeps into the next. The numbers look controlled; nothing was. A separate isolated subagent per step is the cure.
- **Judge as authority** — taking the LLM judge's verdict as the verdict. It shares the blind spots of the agent it judges, so a plausible-but-wrong output sails past both. The judge triages; the human decides.
- **Single-sample certainty** — one task, one run, treated as proof. Output variance alone can swing a single comparison either way; the conclusion is noise dressed as signal.
- **The unfailable eval** — a corpus and criteria so undemanding that no realistic skill could fail them. A pass carries no information. If nothing in the suite could ever come back red, it is measuring nothing.
