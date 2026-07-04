## Rule: Explicit Controlled vs Uncontrolled Awareness

Component with internal state: must be explicit. Controlled = parent drives via `value` + `onChange`. Uncontrolled = component owns state, parent reads via ref. Never silently mix.

**Do:**

- Accept `value` + `onChange` for controlled mode
- Accept `defaultValue` for uncontrolled initial state
- Use `useControllableState` (or equivalent) when reusable component must support both modes
- Never switch between controlled and uncontrolled after mount

**Don't:**

- Accept both `value` and internal `useState` without explicit mode detection
- Ignore `onChange` when `value` provided
- Use ref to read state from controlled component

**Example:**

```tsx
// bad — conflates both modes
function Input({ value }) {
  const [internal, setInternal] = useState(value); // stale after first render
  return (
    <input value={internal} onChange={(e) => setInternal(e.target.value)} />
  );
}

// good — explicit controlled component
function Input({ value, onChange }) {
  return <input value={value} onChange={(e) => onChange(e.target.value)} />;
}
```
