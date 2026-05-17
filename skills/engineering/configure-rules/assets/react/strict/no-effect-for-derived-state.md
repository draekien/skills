---
paths:
  - "**/*.{tsx,jsx}"
---

# No useEffect for Derived State

Never use `useEffect` + `setState` to synchronise state derived from other state or props. Compute the derived value during render with `useMemo` or a plain expression.

```tsx
// prefer — derived inline, no extra state
function UserProfile({ firstName, lastName }: Props) {
  const fullName = `${firstName} ${lastName}`;
  return <h1>{fullName}</h1>;
}

// prefer — expensive derivation memoized
function FilteredList({ items, query }: Props) {
  const filtered = useMemo(
    () => items.filter((item) => item.name.includes(query)),
    [items, query],
  );
  return <List items={filtered} />;
}

// avoid — effect + extra state for a value that is always derivable
function UserProfile({ firstName, lastName }: Props) {
  const [fullName, setFullName] = useState('');

  useEffect(() => {
    setFullName(`${firstName} ${lastName}`); // extra render cycle every time deps change
  }, [firstName, lastName]);

  return <h1>{fullName}</h1>;
}
```

Effect-synced state always causes an extra render cycle: one with the stale value, then another after the effect fires and sets state. Every such pattern is replaceable with a derivation.
