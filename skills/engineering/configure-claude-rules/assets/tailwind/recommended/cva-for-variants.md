---
paths:
  - "**/*.{ts,tsx}"
---

# Use CVA for Component Variants

Use `cva` from `class-variance-authority` when a component has two or more mutually exclusive visual states. CVA keeps variant definitions typed, centralised, and composable.

```tsx
// prefer
import { cva, type VariantProps } from "class-variance-authority";

const button = cva("inline-flex items-center rounded font-medium", {
  variants: {
    intent: {
      primary: "bg-blue-600 text-white hover:bg-blue-700",
      ghost: "bg-transparent text-gray-900 hover:bg-gray-100",
    },
    size: { sm: "px-3 py-1 text-sm", md: "px-4 py-2 text-base" },
  },
  defaultVariants: { intent: "primary", size: "md" },
});

// avoid — ternary chains don't scale and lose type safety
const cls = `inline-flex items-center rounded font-medium ${
  intent === "primary" ? "bg-blue-600 text-white" : "bg-transparent text-gray-900"
} ${size === "sm" ? "px-3 py-1 text-sm" : "px-4 py-2 text-base"}`;
```

Pair `cva` with `cn` when spreading the result into a component that also accepts a `className` prop: `cn(button({ intent, size }), className)`.
