## Rule: Single Responsibility

Each React component must do exactly one thing. A component either renders UI, manages state, or coordinates interactions — not combinations of these.

**Do:**
- Split a component when you need "and" to describe it
- Extract data fetching, formatting, and event handling into separate hooks or components
- Keep component files under ~150 lines as a rough heuristic

**Don't:**
- Mix `fetch`/`useEffect` data loading with render logic in the same component
- Put unrelated `useEffect` calls in the same component
- Add conditional rendering branches that require completely different prop shapes

**Example:**
```tsx
// bad
function UserCard({ userId }) {
  const [user, setUser] = useState(null)
  useEffect(() => { fetchUser(userId).then(setUser) }, [userId])
  return <div>{user?.name}</div>
}

// good
function useUser(userId) { /* fetch logic */ }
function UserCard({ userId }) {
  const user = useUser(userId)
  return <div>{user?.name}</div>
}
```
