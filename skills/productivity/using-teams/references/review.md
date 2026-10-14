# review

Use for: reviewing a diff, pull request, or module from several independent angles at once. Not for: fixing what the review finds — the team reports, and the leader or the user decides what to fix.

## Roster

| Role | Count | Owns | Work | Access |
| --- | --- | --- | --- | --- |
| leader | 1 | the review target, the lens assignments, the final report | Orchestrate | read-only |
| reviewer | 2–4 | one lens each | Review | read-only |

The default lenses are security, performance, and correctness with test coverage. Swap or add a lens the target calls for — accessibility for UI, compatibility for a public API, migration safety for a schema change. Two reviewers never share a lens; a shared lens produces the same findings twice.

### reviewer

Reviews the whole target through its lens only. Every finding states `file:line`, severity (blocking or non-blocking), and a failure scenario: the concrete input or state and the wrong result it produces. A suspicion without a failure scenario is a question, not a finding.

## Task graph

1. Fix the target (diff range, pull request, or paths) and assign one lens per reviewer — leader — blocked by: none
2. Review through the lens, one task per reviewer — reviewer — blocked by: 1
3. Cross-check the other reviewers' blocking findings — reviewer — blocked by: every task 2
4. Verify, deduplicate and rank the findings — leader — blocked by: every task 3

## Messaging

- reviewer → every reviewer: its blocking findings, with `file:line` and failure scenario, as soon as its task 2 completes.
- reviewer → reviewer: an issue that falls in the other's lens, sent to that lens's owner instead of reported twice.
- reviewer → reviewer: during the cross-check, a dispute of a blocking finding, with the evidence that contradicts its failure scenario. The finder replies by confirming with more evidence or withdrawing.
- reviewer → leader: a dispute not settled after one exchange, with both sides' evidence. The leader opens the location and rules; the ruling settles the dispute.
- every member → leader: the full findings list in the message, and the done signal once every dispute it raised or received is settled.

## Review

The cross-check is the review of the reviewers: a blocking finding stands only after the others have had the chance to dispute it. The leader then opens each surviving blocking finding at its `file:line` and confirms the failure scenario before reporting it.

## Stop

Done when every reviewer has sent its findings and its done signal, every dispute is settled as confirmed, withdrawn, or ruled on by the leader, and every blocking finding in the leader's report has been confirmed at its location. Stop without success on a dispute the leader cannot settle at its location; report it as unresolved, with both sides' evidence.
