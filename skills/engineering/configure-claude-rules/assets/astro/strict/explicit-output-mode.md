# Explicit Output Mode

Explicitly declare `output` in `astro.config.mjs`. Relying on the default silently changes behaviour when the Astro version changes or an adapter is added.

```ts
// prefer
export default defineConfig({
  output: 'static', // or 'server' / 'hybrid'
});

// avoid — output mode is implicit
export default defineConfig({
  integrations: [react()],
});
```

Use `'static'` for fully pre-rendered sites, `'server'` for fully SSR sites, and `'hybrid'` when mixing both with per-route `export const prerender` overrides.
