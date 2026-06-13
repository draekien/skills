# Agent Skills Specification

> Source: https://agentskills.io/specification

## Directory structure

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

## `SKILL.md` format

The `SKILL.md` file must contain YAML frontmatter followed by Markdown content.

### Frontmatter

| Field           | Required | Constraints                                                                                                       |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen.             |
| `description`   | Yes      | Max 1024 characters. Non-empty. Describes what the skill does and when to use it.                                 |
| `license`       | No       | License name or reference to a bundled license file.                                                              |
| `compatibility` | No       | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                                              |
| `allowed-tools` | No       | Space-separated string of pre-approved tools the skill may use. (Experimental)                                    |

#### `name` field

- Must be 1–64 characters
- May only contain lowercase alphanumeric characters (`a-z`, `0-9`) and hyphens (`-`)
- Must not start or end with a hyphen
- Must not contain consecutive hyphens (`--`)
- Must match the parent directory name

#### `description` field

- Must be 1–1024 characters
- Should describe both what the skill does and when to use it
- Should include specific keywords that help agents identify relevant tasks

#### `license` field

- Specifies the license applied to the skill

#### `compatibility` field

- Must be 1–500 characters if provided
- Should only be included if the skill has specific environment requirements
- Can indicate intended product, required system packages, network access needs, etc.
- Most skills do not need this field

#### `metadata` field

- A map from string keys to string values
- Use reasonably unique key names to avoid conflicts

#### `allowed-tools` field

- A space-separated string of tools pre-approved to run
- Experimental — support varies between agent implementations

### Body content

The Markdown body after the frontmatter contains the skill instructions. There are no format restrictions. Write whatever helps agents perform the task effectively.

Recommended sections: step-by-step instructions, examples of inputs and outputs, common edge cases.

The agent loads the entire file once a skill is activated. Split longer content into referenced files.

## Optional directories

### `scripts/`

Contains executable code that agents can run. Scripts should be self-contained or clearly document dependencies, include helpful error messages, and handle edge cases gracefully.

### `references/`

Contains additional documentation agents can read on demand. Keep individual files focused — smaller files mean less context use.

### `assets/`

Contains static resources: templates, images, data files, lookup tables, schemas.

## Progressive disclosure

Agents load skills progressively:

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup for all skills
2. **Instructions** (< 5000 tokens recommended): full `SKILL.md` body loaded on activation
3. **Resources** (as needed): files in `scripts/`, `references/`, or `assets/` loaded only when required

Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files.

## File references

Use relative paths from the skill root. Keep references one level deep from `SKILL.md` — never reference a file from within a referenced file.
