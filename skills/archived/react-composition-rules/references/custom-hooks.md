## Rule: Extract Logic into Custom Hooks

Stateful logic — `useState`, `useEffect`, `useRef`, `useReducer`, derived state, event handlers — extract into custom hook when component gets hard to read/test, or logic reusable.

**Do:**

- Name hooks with `use` prefix
- One concern per hook; compose in component
- Return only what component needs — don't leak internals

**Don't:**

- Return JSX from hook (that's component — treat as one)
- Put business logic in component body when extractable
- Duplicate stateful logic across components instead of sharing hook

**Example:**

```tsx
// bad
function SearchBox({ query }) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    setLoading(true);
    search(query)
      .then(setResults)
      .finally(() => setLoading(false));
  }, [query]);
  return loading ? <Spinner /> : <ResultList results={results} />;
}

// good
function useSearch(query) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    setLoading(true);
    search(query)
      .then(setResults)
      .finally(() => setLoading(false));
  }, [query]);
  return { results, loading };
}
function SearchBox({ query }) {
  const { results, loading } = useSearch(query);
  return loading ? <Spinner /> : <ResultList results={results} />;
}
```
