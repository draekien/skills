---
paths:
  - "**/*.{ts,astro}"
---

# Content Collection Schemas

Define a Zod schema for every content collection. Unschema'd collections type all frontmatter as `any`, losing the type-safety that Content Collections exist to provide.

```ts
// prefer — typed schema in src/content.config.ts
import { defineCollection, z } from 'astro:content';

export const collections = {
  blog: defineCollection({
    schema: z.object({
      title: z.string(),
      pubDate: z.date(),
      tags: z.array(z.string()).optional(),
    }),
  }),
};

// avoid — no schema, all frontmatter is `any`
export const collections = {
  blog: defineCollection({}),
};
```
