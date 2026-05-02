---
name: creating-react-components
description: "Creates React components following composition best practices: single responsibility, compound components, custom hooks, headless patterns, inversion of control, forwardRef, render props, stable component identity, controlled/uncontrolled awareness, and more. Use when creating a new React component, building a reusable UI primitive, authoring a design system component, or when the user says 'create a component', 'build a React component', 'make a [name] component', 'write a [name] hook', or asks for a component following composition patterns. Also use when the user asks to refactor an existing component to follow composition best practices."
---

# React Composition Component Author

Creates spec-compliant React components following 11 composition patterns. Reads the relevant rule files before writing code so every pattern is applied correctly.

## Step 1 — Understand the request

Infer the following from context:
- Component name (PascalCase)
- Output file path (follow existing project conventions; default to `src/components/<ComponentName>.tsx`)
- Purpose: what does this component render or orchestrate?
- Whether it wraps a native element, groups related sub-components, or encapsulates behaviour

If any of these is genuinely ambiguous, ask one question. Otherwise proceed.

## Step 2 — Select applicable patterns and plan

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

## Step 3 — Read the rule files for applicable patterns

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

## Step 4 — Create the component

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

## Step 5 — Verify

For each pattern applied in Step 4, re-read its rule file and confirm:
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

## Gotchas

- A function that returns JSX is a **component**, not a hook — name it in PascalCase and use it as JSX, even if it feels small
- Compound component sub-components must throw a clear error when used outside their parent context — always add the guard
- `useImperativeHandle` without `forwardRef` is a no-op — always pair them
- Controlled and uncontrolled modes must never be switched after mount — detect which mode is in use on the first render and stay in it
- State reducer defaults must be exported alongside the hook so consumers can call them as fallbacks
