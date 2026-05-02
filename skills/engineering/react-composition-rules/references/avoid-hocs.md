## Rule: Avoid HOCs — Use Hooks Instead

Do not create new Higher-Order Components for cross-cutting concerns (auth, permissions, theming, feature flags, logging). Implement these as custom hooks instead. `React.memo` and `React.forwardRef` are acceptable HOC usage.

**Do:**
- Replace any new HOC with a custom hook that the component calls directly
- Migrate existing HOCs to hooks when touching that code
- Use `React.memo` for memoisation and `React.forwardRef` for ref forwarding (these are standard)

**Don't:**
- Create `withAuth(Component)`, `withTheme(Component)`, `withFeatureFlag(Component)` wrappers
- Chain multiple HOCs — this makes prop origin untraceable and breaks TypeScript inference
- Use HOCs to inject props that a hook could provide directly

**Example:**
```tsx
// bad
function withAuth(Component) {
  return function WithAuth(props) {
    const user = useAuthStore(s => s.user)
    return <Component {...props} user={user} />
  }
}
export default withAuth(Dashboard)

// good
function Dashboard() {
  const user = useAuth()
  return <div>Hello {user.name}</div>
}
```
