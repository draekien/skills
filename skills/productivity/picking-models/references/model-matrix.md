# Model matrix

Scores are 1-10, higher is better. Read them against the dimension definitions in `SKILL.md`.

## Selectable aliases

Dispatch takes an alias, not a version. These four are the candidate set:

| Alias | Speed | Taste | Intelligence | Cost |
| --- | --- | --- | --- | --- |
| `fable` | 2 | 10 | 10 | 2 |
| `opus` | 4 | 9 | 9 | 4 |
| `sonnet` | 5 | 7 | 8 | 7 |
| `haiku` | 10 | 2 | 2 | 10 |

An alias resolves to whichever generation the harness currently ships. Score the alias, pass the alias.

## Escalation ladder

Ordered by Intelligence, which is the axis escalation climbs:

`haiku` → `sonnet` → `opus` → `fable`

`fable` is the ceiling and is gated — see the Fable gate in `SKILL.md`.

## Full model IDs

Some places take a full model ID instead of an alias: agent-definition frontmatter, the API, and SDK calls. There, name the generation explicitly.

| Model | Speed | Taste | Intelligence | Cost |
| --- | --- | --- | --- | --- |
| Fable 5 | 2 | 10 | 10 | 2 |
| Opus 5 | 4 | 9 | 9 | 4 |
| Opus 4.8 | 4 | 9 | 9 | 5 |
| Sonnet 5 | 5 | 7 | 8 | 7 |
| Sonnet 4.6 | 6 | 6 | 6 | 7 |
| Haiku 4.5 | 10 | 2 | 2 | 10 |

Confirm the exact ID string before using one — IDs are versioned and change per release.

## Scoring an unlisted model

A model absent from both tables is not a fallback to a listed one. Score it on the four dimensions first, using the listed models as anchors: `haiku` sets the floor for Intelligence and the ceiling for Speed and Cost; `fable` sets the ceiling for Taste and Intelligence. Then resolve normally. A model that cannot be scored — no published benchmarks, no session experience with it — is not a candidate.
