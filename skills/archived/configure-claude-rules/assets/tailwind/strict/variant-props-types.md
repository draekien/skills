---
paths:
  - "**/*.{ts,tsx}"
---

# Export `VariantProps` from CVA Definitions

Export the `VariantProps<typeof variantFn>` type alongside every CVA definition. Without it, consumers must duplicate variant values manually and lose autocomplete for valid options.

```tsx
// prefer
import { cva, type VariantProps } from "class-variance-authority";

const badge = cva("inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium", {
  variants: {
    status: { success: "bg-green-100 text-green-800", error: "bg-red-100 text-red-800" },
  },
});

export type BadgeVariants = VariantProps<typeof badge>;

// avoid — consumers must guess valid values; prop types drift from the CVA definition
interface BadgeProps {
  status: "success" | "error"; // manually duplicated; can go out of sync
}
```
