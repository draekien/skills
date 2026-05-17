# Stable Query Client

Create `QueryClient` outside component render — or inside `useState` / `useRef` — so the instance is stable across renders. Creating it inline discards the entire cache on every re-render.

```typescript
// prefer — module-level singleton (non-React entrypoints, SSR, tests)
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router />
    </QueryClientProvider>
  );
}

// prefer — useState for frameworks where module-level state is undesirable
function App() {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <Router />
    </QueryClientProvider>
  );
}

// avoid — new QueryClient() on every render empties the cache each time
function App() {
  return (
    <QueryClientProvider client={new QueryClient()}> {/* recreated every render */}
      <Router />
    </QueryClientProvider>
  );
}
```

For Next.js App Router, create the client with `useState` inside a client component to avoid sharing state between requests on the server.
