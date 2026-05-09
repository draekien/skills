---
name: react-composition-rules
description: "Applies 11 React composition rules in 3 modes: CREATE (new component from scratch), ANALYSE (scan codebase for violations), DECOMPOSE (break monolithic component into composable pieces). Trigger: 'create a component', 'build a React component', 'make a [name] component', 'write a [name] hook', 'analyse my components', 'audit my React components', 'find components that violate', 'check for composition rule violations', 'scan for bad components', 'decompose this component', 'break this component apart', 'split this component', 'refactor into composable pieces'."
---

# React Composition Rules

11 React composition rules, three modes: create new components, analyse existing for violations, decompose monoliths into composable pieces.

## Rule files

Authoritative Do/Don't/Example content for each pattern. Read the relevant ones before writing or judging code — never rely on memory.

- [references/stable-component-identity.md](references/stable-component-identity.md)
- [references/single-responsibility.md](references/single-responsibility.md)
- [references/custom-hooks.md](references/custom-hooks.md)
- [references/avoid-prop-drilling.md](references/avoid-prop-drilling.md)
- [references/compound-components.md](references/compound-components.md)
- [references/forward-ref.md](references/forward-ref.md)
- [references/controlled-vs-uncontrolled.md](references/controlled-vs-uncontrolled.md)
- [references/inversion-of-control.md](references/inversion-of-control.md)
- [references/headless-components.md](references/headless-components.md)
- [references/render-props.md](references/render-props.md)
- [references/avoid-hocs.md](references/avoid-hocs.md)

## Step 1 — Determine mode

Infer mode from request:

- **CREATE** — user wants new component from scratch
- **ANALYSE** — user wants scan for composition violations
- **DECOMPOSE** — user wants existing component broken into smaller pieces

Ambiguous? Ask one question. Else proceed.

---

## Mode: Create

### Step C1 — Understand the request

Infer from context:

- Component name (PascalCase)
- Output file path (follow project conventions; default `src/components/<ComponentName>.tsx`)
- Purpose: what does it render or orchestrate?
- Whether it wraps native element, groups sub-components, or encapsulates behaviour

Genuinely ambiguous? Ask one question at a time. Else proceed.

### Step C2 — Select applicable patterns

Mark each pattern **applies** or **skip** based on purpose. Simple display component may use 2–3; library primitive may use most.

| #   | Pattern                    | Apply when                                                       |
| --- | -------------------------- | ---------------------------------------------------------------- |
| 1   | Stable component identity  | Always                                                           |
| 2   | Single responsibility      | Always                                                           |
| 3   | Custom hooks               | Component has stateful logic                                     |
| 4   | Avoid prop drilling        | Data passes through components that don't use it                 |
| 5   | Compound components        | Multiple related sub-components share state                      |
| 6   | forwardRef                 | Wraps native element or needs imperative handle                  |
| 7   | Controlled vs uncontrolled | Component has internal state                                     |
| 8   | Inversion of control       | Complex state transitions; consumers need to customise behaviour |
| 9   | Headless components        | Behaviour must work with any UI / design system                  |
| 10  | Render props               | Flexible rendering across different UI shapes                    |
| 11  | Avoid HOCs                 | Cross-cutting logic that would otherwise be a HOC                |

Present plan: component name, output path, applicable patterns (numbered), sub-components needed. Proceed immediately unless scope ambiguous.

### Step C3 — Read applicable rule files

Read the rule file for each pattern marked **applies** (see top of skill). Don't write code yet.

### Step C4 — Create the component

Apply the patterns marked **applies** in this order (skip non-applicable):

1. Stable identity
2. Single responsibility
3. Custom hooks
4. Compound components
5. forwardRef
6. Controlled vs uncontrolled
7. Inversion of control (state reducer)
8. Headless / render props
9. Avoid HOCs
10. Avoid prop drilling

The rule files specify *how* to apply each pattern. Write the complete component file.

### Step C5 — Verify

For each pattern applied, confirm Do items satisfied and Don't items avoided. Report as checklist:

```
✓ Stable component identity — all components defined at module scope
✓ Custom hooks — logic extracted into useXxx hook
✗ forwardRef — not applied (no native element wrapper)
```

Flag any rule relevant but not fully satisfied with brief explanation.

---

## Mode: Analyse

### Step A1 — Identify scope

Determine files to scan from request. Named directory or pattern — use it. Scope ambiguous — ask one question. Default `src/components/**/*.{tsx,jsx}` if no scope given and project structure suggests it.

### Step A2 — Read all 11 rule files

See list at top of skill. Read every one before scanning.

### Step A3 — Scan each file

For each component file in scope:

1. Read file
2. Check against all 11 rules
3. Record each violation: rule name + one-line explanation of what code does wrong

Skip inapplicable rules (e.g. skip forwardRef for component rendering no native element).

### Step A4 — Report violations

Group by file. Clean files: single ✓. Files with violations, list each as ✗:

```
src/components/UserCard.tsx
  ✗ Single responsibility — fetches data and renders in the same component body
  ✗ Custom hooks — useState + useEffect are inline, not extracted

src/components/Button.tsx
  ✓ No violations
```

Summarise: total files scanned, total violations found.

### Step A5 — Offer next steps

After report, ask if user wants to decompose flagged components. If yes, transition to Decompose mode for each selected file.

---

## Mode: Decompose

### Step D1 — Identify the component

Identify file from request or prior Analyse run. Read file.

### Step D2 — Identify violated rules

Check component against all 11 rules (read relevant reference files). List each violation with brief explanation.

### Step D3 — Plan the decomposition

For each violation, determine minimal extraction needed:

| Violation                             | Extraction                                         |
| ------------------------------------- | -------------------------------------------------- |
| Stateful logic in component body      | Extract into `useXxx` hook                         |
| Multiple unrelated responsibilities   | Split into separate components                     |
| Nested component definitions          | Move to module scope                               |
| Prop drilling through intermediaries  | Introduce `children` composition or scoped Context |
| HOC wrapper                           | Convert to hook consumed directly                  |
| Multiple sub-components sharing state | Refactor to compound component with Context        |

Present plan as numbered list (what to extract, where it goes, name). Wait for confirmation before changes.

### Step D4 — Execute the refactor

Apply plan. Write or edit all affected files. Follow same ordering as Step C4.

### Step D5 — Verify

Same checklist check as Step C5 across all modified files. Report result. Flag any rule not fully satisfied.

---

## Gotchas

- Compound component sub-components must throw clear error outside parent context — always add guard
- `useImperativeHandle` without `forwardRef` = no-op — always pair them
- Controlled/uncontrolled modes must never switch after mount — detect mode on first render, stay in it
- State reducer defaults must be exported alongside hook so consumers can call them as fallbacks
