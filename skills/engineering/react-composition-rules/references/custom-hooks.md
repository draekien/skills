## Rule: Extract Logic into Custom Hooks

All stateful logic — `useState`, `useEffect`, `useRef`, `useReducer`, derived state, event handlers — must be extracted into a custom hook when it would otherwise make a component hard to read or test, or when the logic is reusable.

**Do:**
- Name hooks with the `use` prefix
- Keep hooks focused on a single concern; compose multiple hooks in a component
- Return only what the component needs — don't leak internal implementation details

**Don't:**
- Return JSX from a hook (that's a component — name and use it as one)
- Put business logic directly in component bodies when it can be extracted
- Duplicate stateful logic across multiple components instead of sharing a hook

**Example:**
```tsx
// bad
function SearchBox({ query }) {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  useEffect(() => {
    setLoading(true)
    search(query).then(setResults).finally(() => setLoading(false))
  }, [query])
  return loading ? <Spinner /> : <ResultList results={results} />
}

// good
function useSearch(query) {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  useEffect(() => {
    setLoading(true)
    search(query).then(setResults).finally(() => setLoading(false))
  }, [query])
  return { results, loading }
}
function SearchBox({ query }) {
  const { results, loading } = useSearch(query)
  return loading ? <Spinner /> : <ResultList results={results} />
}
```
