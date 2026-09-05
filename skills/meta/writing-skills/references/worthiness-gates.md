# Worthiness Gates

A skill is the most expensive mechanism available for changing an agent's behaviour and the least reliable: its description competes for activation in every session it is installed, and even once activated, the agent can still deviate from it. Every other mechanism costs less and deviates less. So the gate does not ask whether an idea is a *good* skill — it asks **whether the work needs judgment at all**, and routes everything that does not to the mechanism that does the job deterministically.

Two scopes. The **whole-idea gate** runs before authoring and can end the work outright. The **part gate** runs inside a skill that survived, over each unit of work its body describes.

## The whole-idea gate

Read top down and take the first row that fits — the cheaper mechanisms come first on purpose, so a match high in the list settles it.

- **The agent already does it unprompted** → nothing. Test: run a representative task with no skill loaded and read the result. If it is already right, the skill teaches nothing and its description dilutes activation for every skill that does earn its place.
- **One right answer, decidable by a machine** → a script, a lint rule, or a check in the build. Test: could a program return pass or fail without reading intent? Parsing, validation, formatting, conversion, scaffolding, naming rules, and required-field checks all answer yes. Prose asking an agent to be careful about a decidable property is a check that fails silently.
- **Must happen every time, with no decision about when** → a hook. Test: is the trigger a mechanical event — a file changed, a command finished, a session began — rather than a judgement about relevance? A skill fires only when the agent recognises it is relevant, so "always, after X" is a guarantee it cannot make.
- **A durable fact about the user, the project, or a past decision** → memory. Test: does it need teaching each session, or only recalling? A fact restated as an instruction is a fact with extra steps.
- **An always-on convention for one repository** → that project's instructions file. Test: should it govern work in this codebase whether or not anyone invokes it? A convention that must never be optional cannot depend on activation.
- **A keystroke whose only variable is when the human wants it** → a command the user invokes, with the behaviour fixed.
- **Judgment that varies by case, applied when the case arises** → a skill. This is the residue: work where the right move depends on context the author cannot enumerate, and where the agent left alone would pick a worse one.

### Verdict

Evaluate every row before concluding — an idea often matches more than one, and the split is the useful finding. Report the routing, not just the yes or no:

- **Routes away entirely** — name the mechanism and stop. Do not author a skill alongside it; a skill shadowing a deterministic mechanism lets the less reliable of the two win by being the one that loads.
- **Splits** — the decidable part goes to its mechanism and the remainder is a smaller skill. State both halves so neither is lost.
- **Stays a skill** — carry forward what the gate found: the parts that came close to deciding deterministically are the first candidates for the part gate.

## The part gate

The same question scoped to a step rather than a whole idea. Run it over each unit of work in the skill.

- **Script the deterministic floor** — a step with one right answer belongs in `scripts/`, invoked by the body. The signals surface in real execution traces: the agent re-derives the same logic every run, fumbles a long incantation, or produces different results across runs from identical input.
- **Keep judgment in prose** — where several approaches are valid, reasoning-carrying prose beats frozen code: a script cannot adapt when its assumptions do not hold, and the agent cannot see inside it to know why it did what it did. Encoding a whole workflow's sequence as a script is workflow scripting wearing an executable coat.
- **A checklist a program could run is a check, not a checklist** — the sharpest form this takes when reviewing an existing skill. Prose asking the agent to confirm a set of properties, every one of them mechanically decidable, is a validator nobody wrote.

Done when every unit of work in the skill sits on one side or the other, and each scripted one names its script.
