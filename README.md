# Skills

Agent skills organised into buckets by domain.

## Quickstart

### Claude Code — plugin marketplace

```bash
/plugin marketplace add draekien/skills
```

Then install everything at once:

```bash
/plugin install everything@draekien-skills
```

Or install individual bucket plugins:

```bash
/plugin install engineering-skills@draekien-skills
```

### Cross-agent — npx skills

Works with Claude Code, GitHub Copilot, Cursor, Cline, and 40+ other agents.

```bash
npx skills add draekien/skills
```

### Manual — Claude Code

Copy skill directories into:

- `~/.claude/skills/` — personal scope (all projects)
- `.claude/skills/` — project scope (current project only)

## Planning

Skills for turning an idea into a spec, and a spec into work an agent or a person can pick up.

**2 skills →** [browse the planning bucket](skills/planning/README.md)

## Software Design

Skills for designing code and the vocabulary it is built on, from a single method to an entire architectural layer.

**2 skills →** [browse the software-design bucket](skills/software-design/README.md)

## Quality

Skills for making work hold up: stress-testing a change before it ships, and testing it so the tests would actually fail.

**2 skills →** [browse the quality bucket](skills/quality/README.md)

## Technical Writing

Skills for developer-facing writing: the documentation that ships alongside the code.

**1 skill →** [browse the technical-writing bucket](skills/technical-writing/README.md)

## Version Control

Skills for git hygiene and repository workflow.

**1 skill →** [browse the version-control bucket](skills/version-control/README.md)

## Context Management

Skills for building and managing agent context: the documentation and reference indexes an agent reads before it touches the code.

**3 skills →** [browse the context-management bucket](skills/context-management/README.md)

## Productivity

Skills for general workplace productivity: summarisation, research, meeting prep, and task management.

**7 skills →** [browse the productivity bucket](skills/productivity/README.md)

## Problem Solving

Skills for working through a hard problem or decision: reasoning from fundamentals, or debating between competing options.

**2 skills →** [browse the problem-solving bucket](skills/problem-solving/README.md)

## Roles

Skills that adopt a fixed persona or stance to sharpen thinking: an advocate, a listener, a critic.

**3 skills →** [browse the roles bucket](skills/roles/README.md)

## UI/UX

Skills for user interface and experience design: dashboards, visual design, and usability.

**2 skills →** [browse the ui-ux bucket](skills/ui-ux/README.md)

## Output Styles

Skills that shift Claude's communication tone and voice.

**5 skills →** [browse the output-styles bucket](skills/output-styles/README.md)

## Teaching

Skills for explanation and comprehension: making an idea land, and repairing it when it does not.

**1 skill →** [browse the teaching bucket](skills/teaching/README.md)

## Meta

Meta-skills: skills about authoring, vetting, and evaluating skills themselves.

**2 skills →** [browse the meta bucket](skills/meta/README.md)

## Engineering (retired)

Split into the planning, software-design, quality, technical-writing, version-control, and context-management buckets. The bucket ships redirect stubs only, so an existing `engineering-skills` install keeps pointing at the right place.

**0 skills →** [see where each one went](skills/engineering/README.md)
