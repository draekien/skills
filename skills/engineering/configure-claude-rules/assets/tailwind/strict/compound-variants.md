---
paths:
  - "**/*.{ts,tsx}"
---

# Use `compoundVariants` for Multi-Variant Combinations

Use `compoundVariants` when a style applies only for a specific combination of two or more variants. Duplicating classes across individual variant branches causes drift when one branch is updated.

```tsx
// prefer
const button = cva("inline-flex items-center rounded font-medium", {
  variants: {
    intent: { primary: "bg-blue-600 text-white", ghost: "bg-transparent" },
    size: { sm: "px-3 py-1", lg: "px-6 py-3" },
  },
  compoundVariants: [
    { intent: "primary", size: "lg", className: "shadow-lg tracking-wide" },
  ],
});

// avoid — the combination class is duplicated in each variant branch
const cls = cn(
  intent === "primary" && size === "lg" && "shadow-lg tracking-wide",
  intent === "primary" && "bg-blue-600 text-white",
);
```
