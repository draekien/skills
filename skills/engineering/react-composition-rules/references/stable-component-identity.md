## Rule: Stable Component Identity — No Component Definitions Inside Render

Never define React component (function returning JSX) inside another component's render or inside hooks (`useMemo`, `useCallback`). React tracks component types by function reference — new reference each render = subtree unmount+remount, all state destroyed.

**Do:**

- Define components at module scope
- Pass data as props instead of closing over parent scope
- Use `React.memo` at module scope if memoisation needed

**Don't:**

- Define component with `function` or `const` inside another component's body
- Define components inside `useMemo`, `useCallback`, or `useEffect`
- Close over parent variables instead of passing as props

**Example:**

```tsx
// bad — Row is re-created every render, state inside Row is destroyed
function List({ items }) {
  const Row = ({ item }) => <li>{item}</li>; //  new reference every render
  return (
    <ul>
      {items.map((item) => (
        <Row key={item} item={item} />
      ))}
    </ul>
  );
}

// good — Row has a stable reference at module scope
function Row({ item }) {
  return <li>{item}</li>;
}
function List({ items }) {
  return (
    <ul>
      {items.map((item) => (
        <Row key={item} item={item} />
      ))}
    </ul>
  );
}
```
