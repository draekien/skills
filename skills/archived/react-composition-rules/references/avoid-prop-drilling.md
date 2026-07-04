## Rule: Avoid Prop Drilling — Composition over Configuration

No props through intermediaries that don't use them. Move data closest to consumer. Composition first, Context second, external state last.

**Do:**

- Use `children` prop — parent composes configured subtrees, skips intermediaries
- Use Context for genuinely shared, low-churn data (theme, locale, auth state)
- Colocate state with owning component

**Don't:**

- Pass same prop through 3+ layers when intermediaries don't use it
- Use Context for high-frequency updates (form input values, mouse position)
- Reach for global state when restructuring tree solves it

**Example:**

```tsx
// bad — Layout and Sidebar don't use theme but must pass it
function App() {
  return <Layout theme="dark" />;
}
function Layout({ theme }) {
  return <Sidebar theme={theme} />;
}
function Sidebar({ theme }) {
  return <Widget theme={theme} />;
}

// good — App composes directly, no drilling
function App() {
  return (
    <Layout>
      <Sidebar>
        <Widget theme="dark" />
      </Sidebar>
    </Layout>
  );
}
```
