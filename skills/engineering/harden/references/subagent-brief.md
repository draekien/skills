# Subagent brief

Dispatch one subagent per lens. Each returns field reports only — no ranking, no recommendations.

Use a cheap exploration-grade model; these agents read and imagine rather than synthesise. Never leave the model unset.

## Brief template

Give each subagent:

- **The target** — paste the diff, file paths, spec text, or description in full. A subagent that has to hunt for the target wastes its context and returns vaguer reports.
- **The surrounding context** — callers, adjacent modules, conventions, and anything learned during Brief. State the project, team size, and release cadence if known.
- **Its lens and only its lens** — the lens name and its forcing question. Independence is the point of this mode; a subagent given all seven lenses converges on the same three obvious failures every other one found.
- **The horizon** — today's date plus six months, stated as an absolute month.
- **The output contract** — below.

## Output contract to give each subagent

> Write field reports from six months in the future, in the past tense, as things that already happened.
>
> For each incident: the month it occurred, what triggered it, what broke, how far the damage spread, and the root cause traced to a specific property of the target as it exists today — quote the line, decision, or omission.
>
> For each success: what worked, who benefited, and the specific property of the target that caused it.
>
> Produce at least three incidents, or state plainly that this lens produced fewer and why. Do not invent incidents you cannot trace to the target; a short honest report beats a padded one. Do not propose changes.

## Merging

Deduplicate by root cause, not by symptom — two lenses reporting the same underlying property found one incident, not two. Keep the telling with the most concrete trigger and blast radius, and note that two lenses independently reached it: that convergence raises the confidence score at Rank.

Discard any incident whose root cause is not traceable to the target, however vivid it reads.
