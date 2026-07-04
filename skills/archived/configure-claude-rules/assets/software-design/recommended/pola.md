# Principle of Least Astonishment (POLA)

Software should behave exactly as a knowledgeable reader would predict from its name and context. Surprising behaviour is a design problem — the fix is a better interface, not a warning in the documentation.

```
// prefer — name matches behaviour precisely
function getUser(id): return user or null

// avoid — name implies a read, behaviour silently mutates
function getUser(id):
  user = db.find(id)
  db.updateLastAccessed(id)    // caller had no reason to expect this
  return user
```

If you feel the urge to add a "note: also does X" to a function's comment, stop. Separate the surprising behaviour into its own explicitly named function and let callers opt in.
