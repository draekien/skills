# Import Type

Use `import type` for imports that are used only as types. This makes intent explicit, allows bundlers and transpilers to elide the import entirely, and prevents accidental circular dependencies caused by importing a module solely for its types.

```typescript
// prefer — type-only import, fully elided at runtime
import type { User, UserRole } from './user';
import type { ApiResponse } from '../types';

// mixed import — value and type from the same module
import { createUser, type CreateUserInput } from './user';

// avoid — runtime import when only the type is needed
import { User } from './user';
```

Use inline `import type { Foo }` within a regular import when only some of a module's exports are type-only:

```typescript
import { createUser, type User } from './user';
```
