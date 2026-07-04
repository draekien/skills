---
paths:
  - "**/*.{ts,tsx}"
---

# Use `cn` for Class Merging

Use `cn()` whenever conditionally combining classes or accepting a `className` prop override. `cn` wraps `clsx` (conditional logic) and `tailwind-merge` (conflict resolution) so that later classes correctly override earlier ones.

```tsx
// prefer
function Button({ variant, className, ...props }: ButtonProps) {
  return (
    <button className={cn("px-4 py-2 rounded", variant === "ghost" && "bg-transparent", className)} {...props} />
  );
}

// avoid — tailwind-merge absent, so className="p-8" won't override "px-4 py-2"
function Button({ className, ...props }: ButtonProps) {
  return <button className={`px-4 py-2 rounded ${className}`} {...props} />;
}
```

Every component that accepts a `className` prop must pass it through `cn` as the last argument.
