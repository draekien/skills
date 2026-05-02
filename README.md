# Skills

Agent skills organised into buckets by domain.

## Quickstart

### Claude Code — plugin marketplace

```bash
/plugin marketplace add draekien/skills
```

Then install individual bucket plugins:

```bash
/plugin install drafting-skills@draekien-skills
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

## Drafting

Skills for writing and editing content: emails, documents, reports, and other written output.

- [skill-writing](skills/drafting/skill-writing/SKILL.md) — Creates a new agent skill following the Agent Skills open standard.

## Engineering

Skills for software development tasks: code review, debugging, architecture, and technical workflows.

_No skills yet._

## Productivity

Skills for general workplace productivity: summarisation, research, meeting prep, and task management.

_No skills yet._
