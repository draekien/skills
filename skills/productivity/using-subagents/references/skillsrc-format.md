# skillsrc — using-subagents Keys

Configuration is stored in `.draekien/.skillsrc`, a JSON file shared across skills — each skill owns only its own top-level block.

## Keys Used by This Skill

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `maxConcurrentAgents` | string | `4` | Positive integer: the most agents running at once on leaves whose reports are judged one by one. Mechanical fan-out is not capped by it |

## Reading

```bash
uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill using-subagents get maxConcurrentAgents --default 4
```

If the script cannot run, read `using-subagents.maxConcurrentAgents` from `.draekien/.skillsrc` as JSON. Use `4` when the file, block or key is absent, or when the value is not a positive integer.

## Writing

A limit the user names for one task applies to that task only; do not write it. When the user asks to change the standing limit: confirm with the user, then run `uv run scripts/skillsrc.py --config .draekien/.skillsrc --skill using-subagents set maxConcurrentAgents <n>`. If `.draekien/` does not yet exist, confirm its creation with the user before proceeding, then create it. The script merges only the `using-subagents` block.
