## Rule: Single Responsibility

Each React component does one thing. Renders UI, manages state, or coordinates — not combinations.

**Do:**

- Split when you need "and" to describe it
- Extract fetching, formatting, event handling into separate hooks or components
- Keep files under ~150 lines

**Don't:**

- Mix `fetch`/`useEffect` data loading with render logic
- Put unrelated `useEffect` calls in same component
- Add conditional branches requiring different prop shapes

**Example:**

```tsx
// bad
function UserCard({ userId }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  return <div>{user?.name}</div>;
}

// good
function useUser(userId) {
  /* fetch logic */
}
function UserCard({ userId }) {
  const user = useUser(userId);
  return <div>{user?.name}</div>;
}
```
