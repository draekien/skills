## Rule: Explicit Controlled vs Uncontrolled Awareness

Every component with internal state must be explicit about whether it is controlled (parent drives state via `value` + `onChange`) or uncontrolled (component owns state, parent reads via ref). Never silently mix both modes.

**Do:**
- Accept `value` + `onChange` for controlled mode
- Accept `defaultValue` for uncontrolled initial state
- Use `useControllableState` (or equivalent) when a reusable component must support both modes
- Never switch between controlled and uncontrolled after mount

**Don't:**
- Accept both `value` and internal `useState` without explicit mode detection
- Ignore the `onChange` prop when `value` is provided
- Use a ref to read state from a controlled component

**Example:**
```tsx
// bad — conflates both modes
function Input({ value }) {
  const [internal, setInternal] = useState(value) // stale after first render
  return <input value={internal} onChange={e => setInternal(e.target.value)} />
}

// good — explicit controlled component
function Input({ value, onChange }) {
  return <input value={value} onChange={e => onChange(e.target.value)} />
}
```
