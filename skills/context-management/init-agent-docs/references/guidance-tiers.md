# Guidance tiers

Every convention the interview surfaces has a place it belongs, and the root document is the last of them. A rule written down is a rule an agent is asked to remember on every turn. A rule enforced is a rule that cannot be broken quietly. Place each convention before writing it, because a line that should have been a check is not improved by being worded well.

## The descent

Take the convention as the user stated it and work down the tiers. The first one it clears is where it belongs.

| Tier | The convention belongs here when |
| --- | --- |
| **Make it unrepresentable** | The state the rule forbids can be designed out, so breaking it stops being expressible |
| **Fail at authoring time** | Compliance is decidable from source text alone — naming, imports, forbidden constructs, required annotations |
| **Fail across boundaries** | The rule is about dependency direction or reach between modules |
| **Fail in the suite** | The rule is about behaviour or structure once the code runs |
| **Fail on the change** | The rule concerns the artefacts accompanying a change rather than the code — commit form, generated files, a file that must travel with another |
| **A skill** | The rule is a process needing judgement applied consistently, not a property with a pass or a fail |
| **Prose, loaded on demand** | The rule needs judgement, and the tasks that need it can be named |
| **Prose, always loaded** | The rule needs judgement, and every task needs it |

The order is proximity to the moment the rule is broken. Feedback that reaches whoever broke it while they still hold the context is worth more than feedback that arrives later, which is why a rule caught by a type beats one caught by a test, which beats one caught in a pipeline.

Most conventions a user names fail the first six tests and land in prose. That is what prose is for. Do not stretch a judgement rule into a mechanical one to move it up the tiers — a check that cannot actually decide the question produces noise the repository learns to ignore, which is worse than the line it replaced.

## Above prose, recommend and write nothing

A convention landing on any of the top six tiers is reported, not implemented and not written into the documentation. Say which tier it reached and what the check would decide. Building it is a change to the repository's tooling with its own review, and installing it during a documentation setup hides it from the people who would want to see it.

Describe the mechanism by what it decides, never as a named product. Which linter, which runner, which pipeline is a decision this repository has already made or will make on its own terms, and a recommendation that names one is guessing at a stack.

## A tier the repository does not have

Recommend the check, say it does not exist yet, and place the rule in prose meanwhile. An unenforced rule nobody has written down is held by nothing at all, and the descent is about where a rule is best kept rather than about refusing to keep it.

Say both in the report, so the prose line arrives with the reason it is provisional. A line written as the permanent answer to a rule that should fail mechanically is what this descent exists to keep out.

## Between the two prose tiers

Name the tasks that need the rule. If they can be enumerated, the rule is a context document and the root document gets a pointer naming those tasks. If they cannot, every task needs it and it stays in the root document.

The enumeration is the test, not the length of the rule. A rule too short to be worth its own document still stays in the root document when every task reads it, and a long one whose tasks are nameable still moves.

## What the repository keeps

The repository records the commitment, not this descent. A few lines in its own documentation conventions say how guidance is placed there; the tiers and their reasoning stay in the skill. A repository that copies the whole descent into its docs pays for it on every turn and then has to maintain it.
