# debugging

Use for: a bug whose cause is unknown and has several plausible explanations. Not for: a bug whose cause is already evident (fix it directly), or choosing between design options — that is the `round-table` skill (`/plugin install problem-solving-skills@draekien-skills`, or `npx skills add draekien/skills --skill "round-table"`).

## Roster

| Role | Count | Owns | Work | Access |
| --- | --- | --- | --- | --- |
| leader | 1 | the reproduction, the hypothesis list, applying experiments | Orchestrate | write |
| investigator | 3–5 | one hypothesis each | Review | read-only until task 5; may run commands |

Investigators do not edit tracked files until the leader grants write access for task 5: several experiments applied to one tree at once make every result uninterpretable. An experiment that needs a code change goes to the leader as a proposed patch, and the leader applies one experiment at a time and reverts it after.

### investigator

Owns one hypothesis. Gathers evidence for and against it — logs, history, code paths, commands that run the reproduction under different conditions — then attacks the other investigators' hypotheses. Concedes its own hypothesis as soon as the evidence disproves it; holding a disproved hypothesis to stay in the argument wastes every other member's time.

## Task graph

1. Establish a reproduction command that shows the bug, and write every plausible hypothesis, one per investigator — leader — blocked by: none
2. Gather evidence on the owned hypothesis — investigator — blocked by: 1
3. Challenge the other hypotheses — investigator — blocked by: every task 2
4. Run one experiment per surviving hypothesis, one at a time; an experiment whose prediction fails disproves its hypothesis — leader — blocked by: every task 3
5. Write the fix — the investigator whose hypothesis was confirmed — blocked by: 4

Fewer than three plausible hypotheses means one agent can investigate: say so and stop rather than spawning an investigator for an invented cause.

The investigator whose hypothesis was confirmed writes the fix because it holds the context the fix needs. Before assigning task 5, message it that it now has write access to the paths the fix touches; every other investigator stays read-only, so nothing collides. The fix is Build work on a model picked for Review: if it is more than a few lines, ask the user, then spawn an implementer with the investigator's findings instead.

## Messaging

- investigator → investigator: evidence against the other's hypothesis, with the command and output that show it. The recipient rebuts with evidence or concedes.
- investigator → leader: a proposed experiment as a patch plus the result it predicts; a concession; the done signal.
- leader → every investigator: each experiment's outcome, so all hypotheses are judged on the same evidence.

## Review

A hypothesis is confirmed only by a prediction a command verifies: apply the change and the reproduction passes, revert it and the reproduction fails again. Investigators agreeing is not confirmation.

## Stop

Done when the reproduction passes with the fix and fails without it, and every other hypothesis has a disproof on record. Stop without success when every hypothesis is disproved; report the evidence gathered and a new hypothesis list instead of a fix, rather than starting another round unasked. Stop without success, too, when more than one hypothesis survives every experiment; report the survivors with their evidence and the experiment that would separate them.
