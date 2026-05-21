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

- [draft-a-prd](skills/drafting/draft-a-prd/SKILL.md) — Aligns with the user on scope and requirements, then produces a structured PRD document.
- [skill-writing](skills/drafting/skill-writing/SKILL.md) — Creates, updates, and refines agent skills following the Agent Skills open standard.

## Engineering

Skills for software development tasks: code review, debugging, architecture, and technical workflows.

- [react-composition-rules](skills/engineering/react-composition-rules/SKILL.md) — Applies React composition rules to create new components, analyse a codebase for violations, or decompose monolithic components into composable pieces.
- [get-specific](skills/engineering/get-specific/SKILL.md) — Builds and enforces a DDD ubiquitous language scoped to bounded contexts through structured interview and real-time conflict detection.
- [configure-claude-rules](skills/engineering/configure-claude-rules/SKILL.md) — Writes AI behaviour rules into a repository's `.claude/rules/` directory from a curated, topic-organised rule library.
- [module-design](skills/engineering/module-design/SKILL.md) — Designs a new piece of code through structured interview, enforces software-design principles as hard constraints, and produces an adaptive Markdown spec.

## Productivity

Skills for general workplace productivity: summarisation, research, meeting prep, and task management.

- [get-aligned](skills/productivity/get-aligned/SKILL.md) — Maps every decision branch before acting, resolving unknowns through exploration and targeted questions.
- [round-table](skills/productivity/round-table/SKILL.md) — Assembles a debate-style agent team with one champion per option and a fence sitter judge to deliver a structured verdict and recommendation.
- [deep-research](skills/productivity/deep-research/SKILL.md) — Conducts structured multi-source research through a scoping interview, parallel agent researchers with adaptive source selection, and a synthesizer report.
- [transcribe-video](skills/productivity/transcribe-video/SKILL.md) — Transcribes video or audio from a local file or URL to plain text using OpenAI Whisper.
- [visualise](skills/productivity/visualise/SKILL.md) — Takes user-supplied input and produces a self-contained HTML visualisation opened in the browser.

## Output Styles

Skills that shift Claude's communication tone and voice.

- [cte-mode](skills/output-styles/cte-mode/SKILL.md) — Adapts Claude's communication style for someone with CTE: short sentences, plain language, structured output, and patient tone.
