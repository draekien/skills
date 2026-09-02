# Context Management

Skills for building and managing agent context: the documentation and reference indexes an agent reads before it touches the code.

- [extract-llms-txt](extract-llms-txt/SKILL.md) — Produces an llms.txt-format index of a library, framework, SDK, or documentation site, for the agent to consult before touching that area of the codebase.
- [init-agent-docs](init-agent-docs/SKILL.md) — Sets up a repository's agent documentation: AGENTS.md and CLAUDE.md at the root and under docs/, plus adr, references, explorations, and plans directories with the conventions agents need to use them.
- [maintain-agent-docs](maintain-agent-docs/SKILL.md) — Audits a repository's existing agent docs for drift against the code and for wrong shape, then repairs what the user accepts.
