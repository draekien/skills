# {{team-name}}

Use for: {{the kind of task this team completes}}. Not for: {{nearby tasks that need a different team, or no team}}.

## Roster

| Role | Count | Owns | Work | Access |
| --- | --- | --- | --- | --- |
| leader | 1 | the task graph, every shared interface, the final verification | Orchestrate | write |
| {{role}} | {{n or n–m}} | {{paths, question, or deliverable no other member owns}} | {{Build, Review, Write, or Search}} | {{read-only or write}} |

### {{role}}

{{What this member is for, what it owns, the standard its output is held to, and what it must not touch. The leader builds each spawn prompt from this.}}

## Task graph

1. {{task}} — {{role}} — blocked by: none
2. {{task}} — {{role}} — blocked by: 1

## Messaging

- {{role}} → {{role}}: {{what is sent, and when}}
- every member → leader: {{blockers, interface change requests, the done signal}}

## Review

{{Who checks what, against which standard, with which command or criterion. A member never reviews its own output.}}

## Stop

{{The checkable condition that ends the team, including the condition that ends it without success.}}
