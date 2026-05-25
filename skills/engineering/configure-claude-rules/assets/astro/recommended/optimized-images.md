---
paths:
  - "**/*.astro"
---

# Optimized Images

Use `<Image />` or `<Picture />` from `astro:assets` instead of raw `<img>` tags. Astro's image components apply automatic compression, resizing, and modern format conversion at build time.

```astro
---
// prefer
import { Image } from 'astro:assets';
import hero from '../assets/hero.jpg';
---

<Image src={hero} alt="Hero banner" width={800} height={400} />

<!-- avoid — bypasses optimization pipeline -->
<img src="/assets/hero.jpg" alt="Hero banner" />
```

Remote images require an explicit `width` and `height`. Local images infer dimensions automatically but benefit from an explicit `width` to cap output size.
