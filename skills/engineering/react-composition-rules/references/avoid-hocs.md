## Rule: Avoid HOCs — Use Hooks Instead

No new HOCs for cross-cutting concerns (auth, permissions, theming, feature flags, logging). Use custom hooks. `React.memo` and `React.forwardRef` are not HOCs — `React.forwardRef` is required when wrapping a native element (see forward-ref rule).

**Do:**

- Replace new HOC with custom hook, component calls directly
- Migrate existing HOCs to hooks when touching that code
- Use `React.memo` for memoisation, `React.forwardRef` for ref forwarding

**Don't:**

- Create `withAuth(Component)`, `withTheme(Component)`, `withFeatureFlag(Component)` wrappers
- Chain HOCs — prop origin untraceable, breaks TypeScript inference
- Use HOCs to inject props hook could provide directly

**Example:**

```tsx
// bad
function withAuth(Component) {
  return function WithAuth(props) {
    const user = useAuthStore((s) => s.user);
    return <Component {...props} user={user} />;
  };
}
export default withAuth(Dashboard);

// good
function Dashboard() {
  const user = useAuth();
  return <div>Hello {user.name}</div>;
}
```
