## Rule: Avoid Prop Drilling — Composition over Configuration

Do not pass props through intermediate components that don't use them. Restructure the component tree so data lives closest to where it's consumed. Reach for composition first, Context second, external state last.

**Do:**
- Use the `children` prop to let the parent compose already-configured subtrees, skipping intermediaries
- Use Context for genuinely shared, low-churn data (theme, locale, auth state)
- Colocate state with the component that owns it

**Don't:**
- Pass the same prop through 3+ component layers when intermediaries don't use it
- Use Context for high-frequency updates (form input values, mouse position)
- Reach for global state management when restructuring the component tree solves it

**Example:**
```tsx
// bad — Layout and Sidebar don't use theme but must pass it
function App() { return <Layout theme="dark" /> }
function Layout({ theme }) { return <Sidebar theme={theme} /> }
function Sidebar({ theme }) { return <Widget theme={theme} /> }

// good — App composes directly, no drilling
function App() {
  return (
    <Layout>
      <Sidebar>
        <Widget theme="dark" />
      </Sidebar>
    </Layout>
  )
}
```
