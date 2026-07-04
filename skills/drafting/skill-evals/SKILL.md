---
name: skill-evals
description: Builds and runs an empirical eval suite for an existing skill, measuring whether its description activates correctly and whether it actually improves the agent's output. The suite and every run are persisted, so a skill's scores can be tracked across edits. Use when you want to test a skill's quality or track it over time.
argument-hint: [skill-name-or-path]
disable-model-invocation: true
---

A skill makes two empirical claims, and the author's intuition cannot settle either. The `description` claims *I am the right tool for this class of situation* — an activation claim. The body claims *loading me makes the work better* — an impact claim. An eval measures whether each claim holds against evidence the author has not seen yet. The discipline is to commit to what a passing result looks like *before* running anything, then run an agent under controlled conditions and report the gap between claim and reality.

The eval is driven by an orchestrator that never performs the work it is measuring. It delegates every generation, every eval run, and every LLM judgement to a separate subagent with isolated context — because an agent that has already seen the skill, the labels, and the result the author is hoping for cannot produce an uncontaminated scenario, run, or verdict. Isolation is the mechanism that keeps each step honest. And the final word on whether the agent did a good job stays with the human author: the machinery narrows the question down to the cases worth looking at, it does not answer it.

Both eval modes ride one spine. Only what is held fixed and what is judged differ between them.

## The spine

Every eval, of either mode, is the same four moves. Skip one and the result stops meaning anything.

1. **Commit ground truth first.** Have an isolated subagent generate the candidate scenarios — corpus prompts (activation) or tasks (impact) — so they are shaped by the skill's purpose rather than by its exact wording or the result the author wants. Then the orchestrator commits their labels (activation) or success criteria (impact) — with the author approving them before any eval run — derived from the skill's intent, never from outputs already seen. A criterion authored after the output exists describes the output, not the goal, and the eval can no longer fail. Committing is literal: the approved suite is written to disk as a hash-keyed version (`v1`, `v2`…) and frozen. A re-run reuses the existing frozen suite — that reuse is what makes the eval repeatable — and mints the next version only when the suite's content genuinely changes. Seeing the outputs can legitimately reveal that a label was wrong or a criterion ill-formed; that is a real change to the test set, so encode it by minting a new version, never by loosening the standard in place to fit what was just observed. The first is learning; the second is drift wearing its costume. Regenerating the suite from scratch on every run is the bug, not the feature: it swaps the test set out from under the trend, so no two runs are comparable.
2. **Run each scenario in its own isolated subagent.** Hold everything fixed except the one variable under test — the prompt (activation) or the presence of the skill (impact). One subagent per run, its context limited to that scenario and carrying nothing about the eval's purpose, the other runs, or the outcome anyone expects. Shared or carried-over context bleeds the answer from one run into the next; isolation is what makes "controlled" more than a label.
3. **Judge blind as a first pass, then validate with the author.** A judge subagent scores each result against the committed standard without being told which run the author hopes will win — blindness stops it from scoring the hope instead of the work. But an LLM judge shares the blind spots of the agents it judges and is swayed by the same plausible-but-wrong output, so its verdict is triage, not truth: it narrows the set the author has to inspect. The author makes the final call on whether the agent did a good job. Where scoring is mechanical — comparing a fire/no-fire decision against a label — no judge subagent is needed, and the author instead reviews the misfires that scoring surfaces.
4. **Append the run; read the gap from the history.** A single number ("80%") tells the author nothing they can act on, and a single run tells them nothing about whether the skill is moving. Each run appends a record — precision and recall, or the judge's per-task verdicts — to a persisted log, and a frozen HTML report (copied into the output directory once, never regenerated) reads the whole history back. It plots each metric's trend *segmented by suite version* — so scores measured against different test sets never join into one misleading line — and surfaces the latest run's specific misfires: *this* prompt that should have fired and didn't, *this* part of the output the skill failed to improve. For the activation eval, it shows precision and recall alongside the two named lists: the should-fire prompts it missed and the should-stay-silent prompts it fired on. For the impact eval, it pairs each task with the judge's first-pass verdict and the committed criteria each delta served or missed, marks any run the author has not yet validated, and leaves the author's final call as the last step. Because the report fetches the run and suite files, view it over a local server (see *Persisted state and run history*), not by opening the file directly. The history is the deliverable; the grade is not.

The point of the eval is to find where the skill falls short, not to confirm it works. An eval that cannot produce a failing result is theatre. Treat a clean pass with suspicion and check the corpus and criteria were demanding enough to bite.

## Activation eval — does the description fire when it should, and stay silent when it shouldn't

A model-invocable skill is selected on its `description` alone. This mode measures the quality of that selection signal as a classifier: across realistic prompts, how often does the right call get made.

**Build a labelled corpus with both classes.** Positives are prompts where the skill genuinely ought to fire. Negatives are prompts where it ought to stay silent — and negatives are not optional. A corpus of positives only measures recall and silently calls it accuracy; it cannot detect a description so broad it fires on everything. The negatives that matter are the *near misses*: prompts in the same topic neighbourhood that a slightly-too-broad description would wrongly fire on. Easy negatives from unrelated domains pass trivially and prove nothing. Spend the effort on the hard ones at the boundary. Size each class so the rates are stable rather than swung by a single prompt — on the order of fifteen to twenty per class; a handful makes precision and recall too noisy to act on.

**Derive positives that test generalisation, not string-matching.** Give the generating subagent the skill's *purpose* but not its body, so the positives reflect how people phrase the need rather than echoing the description's own wording. Seed from the situations the skill is meant to serve, then paraphrase away from any literal trigger phrase — different vocabulary, implied rather than stated need, the request buried mid-sentence. A description that only fires on its own trigger phrases quoted verbatim is brittle in exactly the way this catches. If every positive is lifted word-for-word from the description, the eval tests the corpus, not the skill.

**Run the selection decision in isolation.** Present the skill's name and description to a subagent acting as the selector, alongside the competing skill descriptions committed into the frozen suite — sourced from the skills available at commit time, because in production the choice is never the skill against nothing. Freezing the competitor set alongside the prompts and labels is what lets a re-run against the same suite version select against an identical field; an unfrozen, live-resampled set would make two runs against one suite version incomparable. The selector sees only the prompt and the competing descriptions, never the corpus label for that prompt; showing it the label leaks the answer and the run measures nothing. For each corpus prompt, record the binary: fire or no-fire.

**Score precision and recall separately, then read the misfires.** Recall is, of the prompts that should fire, how many did. Precision is, of the prompts where it fired, how many should have. They fail in opposite directions and demand opposite fixes, so a blended score hides the diagnosis. The actionable output is the two lists: false negatives (should-fire prompts it missed → the description is too narrow or its triggers too literal, broaden or add phrasings) and false positives (should-stay-silent prompts it fired on → the description is too broad, tighten the scope). Each named misfire points at the words to change.

## Impact eval — does loading the skill make the output better

This mode tests the body's claim that the skill changes the work for the better. The method is a controlled comparison: same task, same conditions, the skill present or absent as the only difference.

**Define task-specific success criteria from the skill's intent.** Ask what a great output does that a default one would not — the specific moves, omissions avoided, judgments made that the skill exists to instil. Generic quality ("is it good") rewards verbosity and cannot isolate the skill's contribution. Write these criteria down before any output exists.

**Choose representative tasks, more than one.** A single task declared representative is a guess, and agent outputs vary run to run. Use several tasks — on the order of three to five — spanning the skill's intended range, and where variance is a concern, repeat a task across a few fresh subagents so a lucky or unlucky single draw is not mistaken for the skill's effect.

**A/B with the skill as the only variable.** For each task, run two subagents with isolated context on the identical prompt: one with the skill's instructions in context, one without. Same task, same model, same everything else. The difference in their outputs is the skill's effect, isolated. Capture each arm's token count and wall-clock from its completion notification as the run finishes — they are recorded nowhere else — so the run carries what the skill *cost*, not only what it changed. A skill is paid for in context on every invocation; an eval that measures the quality delta but not the token premium that bought it is reporting half the trade.

**Judge the pair blind, then hand the author the call.** A judge subagent scores both outputs against the criteria without being told which arm had the skill — blindness is what stops it from rewarding the output it was told to prefer. Score each criterion as a binary met / not-met rather than a sliding rating: the gap between a 0.5 and a 0.6 is not something an author can act on, and a clean pass/fail is what the report and the trend can read. Require the judge to quote the specific span of output that earns a *met* — a section carrying the right label but no substance behind it is a miss, not a pass granted on the benefit of the doubt. Run the judge on a smaller, cheaper model than the one under test; scoring against fixed criteria does not need the strongest model, and a cheap judge is affordable to attach to every pair. Treat the score as a first pass regardless: an LLM judge can be convinced by the same polished-but-wrong output that would convince the agent it is judging, so the author validates the verdict rather than trusting it. The finding is the delta: where the skill changed the output and whether that change served the criteria. A skill that produces no delta — or buys its delta with a token premium the quality gain does not justify — is not earning its context cost. A skill that produces a delta the criteria do not value is teaching something, but not the thing it claims — and that gap is the most useful thing the eval can surface.

## Closing the loop

The run history is not a scoreboard; it is the input to the next edit. A finished eval surfaces the specific places the skill fell short — the false negatives and false positives by name (activation), the criteria a delta missed and the transcripts of how the agent reached its output (impact). Feed those signals, together with the current `SKILL.md`, to a subagent and have it propose edits: generalise each fix to the class of prompt it represents rather than patching the single corpus case, give an instruction its reason rather than adding another bare directive, and cut the instructions the transcripts show were wasted rather than only ever adding more. Apply the edit, then re-run against the *same frozen suite version* — the new run lands as the next point on the trend, and the segment reads directly whether the edit moved the metric or only moved the words. That before-and-after on one held-fixed test set is the whole reason the suite is frozen and the history persisted; an eval run once and filed away has skipped the step where it pays for itself.

## Persisted state and run history

**Available scripts**

- `scripts/skillsrc.py` — reads and writes the `skill-evals.outputDir` config key in `.draekien/.skillsrc`
- `scripts/eval_state.py` — owns the output directory's file mechanics: scaffolding, suite freezing/versioning, and run-record writes

```bash
uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill skill-evals get outputDir --default .draekien/skill-evals
```

Repeatability is a property of state, not of intent: an eval that cannot be re-run against identical inputs cannot detect a regression. Everything the eval commits lives under one directory per evaluated skill — `<outputDir>/<skill-name>/`, where `outputDir` defaults to `.draekien/skill-evals` and is read via `scripts/skillsrc.py` using the key `skill-evals.outputDir`; if the key is absent or the file does not exist, fall back to the default without error:

```text
<skill-name>/
  report.html             frozen renderer, copied once from assets
  README.md               how to view it
  activation/
    suite/v1.json …       frozen corpus + labels + competing descriptions, one file per version
    runs.jsonl            one run record per line
  impact/
    suite/v1.json …       frozen tasks + criteria, one file per version
    runs.jsonl
```

`scripts/eval_state.py` owns the file mechanics so they stay exact and repeatable: `init-output` scaffolds the directory and copies the report; `commit-suite` reuses the frozen suite when its content hash is unchanged and mints the next version when it is not; `append-run` validates a run against its suite version, stamps it, and appends it. The orchestrator generates and judges; the script does the deterministic writes. Before the first write, check whether the `.draekien/` directory exists at the project root; if it is absent, confirm its creation with the user, then create it along with an empty `.draekien/.skillsrc` JSON file (`{}`) — once created in the session, do not re-confirm on later writes. Then scaffold the output directory:

```bash
uv run scripts/eval_state.py init-output --dir <outputDir>/<skill-name>
```

Each appended run record must use exactly the keys `report.html` reads back, or the report renders that field blank with no error: activation — `suiteVersion`, `ts`, `recall`, `precision`, `misfires: { falseNegatives: [...promptIds], falsePositives: [...promptIds] }`; impact — `suiteVersion`, `ts`, `judge: { winRate, perTask: [{ taskId, winner, criteriaMet: [...], criteriaMissed: [...] }] }`, `humanVerdict: { winner, note } | null`, `cost: { withSkill: { tokens, durationMs }, baseline: { tokens, durationMs } }`.

**Versioning is the honesty mechanism.** A suite is frozen on approval and reused on every later run — that is what holds the inputs fixed. When the suite is deliberately improved (a hard negative added, a mislabel fixed, a task added, the competing-description set changed), its content hash changes and the next run records the new version; the report draws each version as its own band, so pre-change and post-change scores are never silently compared on one line. Reusing the frozen suite is the default; minting a version is a deliberate act.

**Impact runs carry the judge's score, the per-arm token and wall-clock cost, and, where given, the author's verdict.** The blind first-pass judge score is logged on every run as the cheap trend signal; the author's validated verdict supersedes it and is what the trend treats as truth. A run left unvalidated is marked as such rather than counted as settled — the judge triages, the author decides. The cost the run captured (with-skill versus baseline) rides alongside the verdict so the readout shows the token premium next to the quality it bought.

**Viewing the report.** Because `report.html` fetches the run and suite files, it needs a server — `file://` blocks the reads. Start one as a background task, hand the author the URL, then stop it when they are done:

```sh
python -m http.server 8787 --directory <outputDir>/<skill-name>
```

Point the author at `http://localhost:8787/report.html`.

## Anti-patterns

Each of these produces a number that looks like a result and means nothing. Name them on sight.

- **Recall theatre** — see "Build a labelled corpus with both classes" above.
- **Verbatim-trigger corpus** — see "Derive positives that test generalisation, not string-matching" above.
- **Criteria drift** — see "Commit ground truth first" above.
- **Verdict leakage** — see "Run the selection decision in isolation" and "Judge blind as a first pass, then validate with the author" above.
- **Context bleed** — see "Run each scenario in its own isolated subagent" above.
- **Judge as authority** — see "Judge blind as a first pass, then validate with the author" above.
- **Single-sample certainty** — see "Choose representative tasks, more than one" above.
- **The unfailable eval** — see "The point of the eval is to find where the skill falls short, not to confirm it works" above.
- **Trend drift** — see "Append the run; read the gap from the history" and "Versioning is the honesty mechanism" above.
