# Avoid Temporal Decomposition

Do not structure modules around the order operations execute. Structure them around the information each module owns and hides. Execution-order decomposition produces shallow, tightly coupled pipelines where each step exposes its internals to the next.

```
// prefer — one module owns the whole concept and hides its steps
config = Config.load(path)   // reads, parses, validates, and normalises internally

// avoid — split by execution order into separate shallow modules
raw       = ConfigReader.read(path)
parsed    = ConfigParser.parse(raw)
validated = ConfigValidator.validate(parsed)
normalised = ConfigNormaliser.normalise(validated)
```

Ask: "what knowledge does this module own?" not "what does it do first?" If two steps always appear together and share knowledge, they belong in the same module.
