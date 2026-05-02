---
name: react-composition-rules
description: "Applies React composition rules across three modes: (1) CREATE — creates a new React component following 11 composition patterns (single responsibility, compound components, custom hooks, headless patterns, inversion of control, forwardRef, render props, stable component identity, controlled/uncontrolled awareness, and more); (2) ANALYSE — scans a codebase or directory for components that violate composition rules and reports violations per file; (3) DECOMPOSE — breaks apart an existing monolithic component into smaller, composable pieces. Use when the user says 'create a component', 'build a React component', 'make a [name] component', 'write a [name] hook', 'analyse my components', 'audit my React components', 'find components that violate', 'check for composition rule violations', 'scan for bad components', 'decompose this component', 'break this component apart', 'split this component', or 'refactor into composable pieces'."
---

# React Composition Rules

Applies 11 React composition rules in three modes: creating new components, analysing existing ones for violations, or decomposing monolithic components into composable pieces.

## Step 1 — Determine mode

Infer the mode from the user's request:

- **CREATE** — user wants a new component written from scratch
- **ANALYSE** — user wants to scan files for composition rule violations
- **DECOMPOSE** — user wants an existing component broken into smaller, composable pieces

If the mode is genuinely ambiguous, ask one question. Otherwise proceed to the matching section.

---

## Mode: Create

### Step C1 — Understand the request

Infer from context:
- Component name (PascalCase)
- Output file path (follow existing project conventions; default to `src/components/<ComponentName>.tsx`)
- Purpose: what does this component render or orchestrate?
- Whether it wraps a native element, groups related sub-components, or encapsulates behaviour

If any of these is genuinely ambiguous, ask one question. Otherwise proceed.

### Step C2 — Select applicable patterns and plan

Review the 11 patterns below. Mark each as **applies** or **skip** based on the component's purpose. A simple display component may only use 2–3; a library primitive may use most.

| # | Pattern | Apply when |
|---|---|---|
| 1 | Stable component identity | Always |
| 2 | Single responsibility | Always |
| 3 | Custom hooks | Component has stateful logic |
| 4 | Avoid prop drilling | Data passes through components that don't use it |
| 5 | Compound components | Multiple related sub-components share state |
| 6 | forwardRef | Wraps a native element or needs imperative handle |
| 7 | Controlled vs uncontrolled | Component has internal state |
| 8 | Inversion of control | Complex state transitions; consumers need to customise behaviour |
| 9 | Headless components | Behaviour must work with any UI / design system |
| 10 | Render props | Flexible rendering across different UI shapes |
| 11 | Avoid HOCs | Cross-cutting logic that would otherwise be a HOC |

Present the plan:
- Component name and output path
- Applicable patterns (numbered list)
- Sub-components needed, if any

Proceed immediately without waiting unless the component scope is ambiguous.

### Step C3 — Read the rule files for applicable patterns

Before writing code, read each rule file for the patterns marked **applies**. Rule files are in `references/` relative to this skill.

File names map directly to pattern names:
- [references/single-responsibility.md](references/single-responsibility.md)
- [references/compound-components.md](references/compound-components.md)
- [references/custom-hooks.md](references/custom-hooks.md)
- [references/avoid-prop-drilling.md](references/avoid-prop-drilling.md)
- [references/controlled-vs-uncontrolled.md](references/controlled-vs-uncontrolled.md)
- [references/avoid-hocs.md](references/avoid-hocs.md)
- [references/render-props.md](references/render-props.md)
- [references/forward-ref.md](references/forward-ref.md)
- [references/headless-components.md](references/headless-components.md)
- [references/inversion-of-control.md](references/inversion-of-control.md)
- [references/stable-component-identity.md](references/stable-component-identity.md)

Read all applicable rule files before writing any code. Do not rely on memory — the rule files contain the authoritative Do/Don't/Example content.

### Step C4 — Create the component

Apply patterns in this fixed order (skip non-applicable ones):

1. **Stable identity** — define all components at module scope, never inside another component's render function or inside hooks
2. **Single responsibility** — each component does one thing; extract data-fetching, formatting, and event logic into separate hooks or components
3. **Custom hooks** — extract all `useState`, `useEffect`, `useReducer`, and derived state into a `use`-prefixed hook; the component body renders only
4. **Compound components** — if multiple sub-components share state, create a Context, add a provider to the parent, and expose sub-components as named properties on the parent (`Parent.Child`)
5. **forwardRef** — wrap any component that renders a single native element in `forwardRef`; add `useImperativeHandle` if the component exposes a non-trivial imperative API
6. **Controlled vs uncontrolled** — explicitly decide which mode the component supports; never conflate both without a `useControllableState` pattern
7. **State reducer** — if complex state transitions need consumer customisation, expose a `reducer` prop that defaults to the built-in reducer
8. **Headless / render props** — if the component's behaviour must work with arbitrary markup, return prop-getters from the hook and let the consumer own all rendering
9. **Avoid HOCs** — implement any cross-cutting concerns (auth, permissions, theming) as hooks consumed directly by the component, not as HOC wrappers
10. **Avoid prop drilling** — restructure with `children` composition or a scoped Context if props pass through uninvolved intermediaries

Write the complete component file.

### Step C5 — Verify

For each pattern applied in Step C4, re-read its rule file and confirm:
- The Do items are satisfied
- The Don't items are avoided

Report the result as a checklist:
```
✓ Stable component identity — all components defined at module scope
✓ Custom hooks — logic extracted into useXxx hook
✗ forwardRef — not applied (no native element wrapper)
...
```

Flag any rule that was relevant but could not be fully satisfied, with a brief explanation.

---

## Mode: Analyse

### Step A1 — Identify scope

Determine which files to scan from the request. If the user named a directory or pattern, use it. If the scope is ambiguous, ask one question. Default to `src/components/**/*.{tsx,jsx}` if no scope is given and the project structure suggests it.

### Step A2 — Read all 11 rule files

Read every reference file before scanning. This establishes the full set of rules to check against.

- [references/single-responsibility.md](references/single-responsibility.md)
- [references/compound-components.md](references/compound-components.md)
- [references/custom-hooks.md](references/custom-hooks.md)
- [references/avoid-prop-drilling.md](references/avoid-prop-drilling.md)
- [references/controlled-vs-uncontrolled.md](references/controlled-vs-uncontrolled.md)
- [references/avoid-hocs.md](references/avoid-hocs.md)
- [references/render-props.md](references/render-props.md)
- [references/forward-ref.md](references/forward-ref.md)
- [references/headless-components.md](references/headless-components.md)
- [references/inversion-of-control.md](references/inversion-of-control.md)
- [references/stable-component-identity.md](references/stable-component-identity.md)

### Step A3 — Scan each file

For each component file in scope:
1. Read the file
2. Check it against all 11 rules
3. Record each violation: rule name + one-line explanation of what the code does wrong

Skip rule checks that are not applicable to the file (e.g. skip forwardRef for a component that renders no native element).

### Step A4 — Report violations

Group results by file. For clean files, show a single ✓. For files with violations, list each as ✗:

```
src/components/UserCard.tsx
  ✗ Single responsibility — fetches data and renders in the same component body
  ✗ Custom hooks — useState + useEffect are inline, not extracted

src/components/Button.tsx
  ✓ No violations
```

Summarise at the end: total files scanned, total violations found.

### Step A5 — Offer next steps

After the report, ask whether the user wants to decompose any of the flagged components. If yes, transition to Decompose mode for each selected file.

---

## Mode: Decompose

### Step D1 — Identify the component

Identify the file to refactor from the request or from a prior Analyse run. Read the file.

### Step D2 — Identify violated rules

Check the component against all 11 rules (read the relevant reference files). List each violation with a brief explanation.

### Step D3 — Plan the decomposition

For each violation, determine the minimal extraction needed:

| Violation | Extraction |
|---|---|
| Stateful logic in component body | Extract into a `useXxx` hook |
| Multiple unrelated responsibilities | Split into separate components |
| Nested component definitions | Move to module scope |
| Prop drilling through intermediaries | Introduce `children` composition or a scoped Context |
| HOC wrapper | Convert to a hook consumed directly |
| Multiple sub-components sharing state | Refactor to compound component with Context |

Present the plan as a numbered list of steps (what to extract, where it goes, what it will be named). Wait for confirmation before making changes.

### Step D4 — Execute the refactor

Apply the plan. Write or edit all affected files. Follow the same ordering as Step C4 (stable identity first, then single responsibility, etc.).

### Step D5 — Verify

Run the same checklist check as Step C5 across all modified files. Report the result. Flag any rule that could not be fully satisfied.

---

## Gotchas

- A function that returns JSX is a **component**, not a hook — name it in PascalCase and use it as JSX, even if it feels small
- Compound component sub-components must throw a clear error when used outside their parent context — always add the guard
- `useImperativeHandle` without `forwardRef` is a no-op — always pair them
- Controlled and uncontrolled modes must never be switched after mount — detect which mode is in use on the first render and stay in it
- State reducer defaults must be exported alongside the hook so consumers can call them as fallbacks
