# Guardrail candidates

Prose asks an agent to remember a rule on every turn and hopes it complies. A guardrail makes the rule impossible to break quietly. Where a rule can be enforced mechanically, the prose is a weaker copy of a check that does not exist yet.

## What qualifies

A rule is a candidate when all three hold:

1. **Mechanically decidable** — compliance can be determined from the code, not from intent. "Name exported functions in camel case" qualifies; "keep modules cohesive" does not.
2. **Worth catching every time** — the rule is violated by accident rather than by exception, and a violation costs something.
3. **Currently enforced only by asking** — nothing in the repository already fails when it is broken. A rule with an existing check does not need prose at all; that is a restated discoverable.

Rules that fail the first test are the majority, and they are exactly what prose is for. Do not stretch a judgement rule into a mechanical one to produce a finding.

## Choosing the mechanism

| Mechanism | Fits when | Cost |
| --- | --- | --- |
| **Formatter or linter rule** | The rule is a property of source text or syntax — naming, imports, forbidden constructs, required annotations | Lowest. Runs locally and in review, output points at the line |
| **Type or schema constraint** | The rule can be made unrepresentable rather than checked — a required field, a closed set of values, an illegal state | Highest leverage where it fits, since violation stops being possible |
| **Test** | The rule is about behaviour or structure at runtime — a boundary not crossed, a contract upheld, a migration applied | Runs with the suite, and expresses rules no linter can |
| **Static analysis or architecture check** | The rule is about dependency direction or reach across module boundaries | Needs configuration and a place in the pipeline |
| **Pipeline or hook check** | The rule concerns artefacts rather than code — commit format, generated files not hand-edited, a file that must accompany a change | Cheap, but only fires where it is installed |
| **A skill** | The rule needs judgement applied consistently rather than a pass or fail verdict | Not enforcement. The right answer when the rule is a process, not a property |

Prefer the mechanism closest to the moment the rule is broken. A rule caught by a type is better than one caught by a test, which is better than one caught in a pipeline, because the feedback reaches whoever broke it while they are still holding the context.

## What the prose becomes

Once a rule is enforced, the prose line is deleted. It is then a discoverable — the check states the rule, and the failure message teaches it at the moment it matters. Keep a line only where the check cannot explain itself: if the failure would leave a reader unable to tell what to do instead, the guidance that survives is the remedy, not the rule.

## The recommendation

Name the rule, the mechanism, where the check would live, and what happens to the prose. Stop there. Building the guardrail is a change to the repository's tooling with its own review, and smuggling it into a documentation audit hides it from the people who would want to see it.

A plan is the furthest this class goes. Writing one records the recommendation where the repository's own conventions expect proposed work to sit, and leaves the decision and the build to whoever picks it up — so an unattended run files plans rather than prompting, and still builds nothing.
