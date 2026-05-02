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

- [react-composition-rules](skills/engineering/react-composition-rules/SKILL.md) — Applies React composition rules to create new components, analyse a codebase for violations, or decompose monolithic components into composable pieces.

## Productivity

Skills for general workplace productivity: summarisation, research, meeting prep, and task management.

- [get-aligned](skills/productivity/get-aligned/SKILL.md) — Maps every decision branch before acting, resolving unknowns through exploration and targeted questions.
- [get-specific](skills/productivity/get-specific/SKILL.md) — Builds and enforces shared ubiquitous language for a project through structured interview and real-time conflict detection.
