# C# Project Alignment

Expected `.csproj` and `Directory.Build.props` settings per preset.

## Recommended

```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
</PropertyGroup>
```

Check `.csproj` or any `Directory.Build.props` in the directory chain.

## Strict

All recommended settings, plus:

```xml
<PropertyGroup>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  <AnalysisLevel>latest-recommended</AnalysisLevel>
</PropertyGroup>
```

- `TreatWarningsAsErrors` — promotes nullable and style warnings to errors.
- `EnforceCodeStyleInBuild` — applies `.editorconfig` rules during `dotnet build`, not just in IDE.
- `AnalysisLevel` — enables latest Roslyn analysers; `latest-recommended` is a safe default.

## .editorconfig patterns

For rules with `.editorconfig` equivalents:

```ini
[*.cs]
# file-scoped-namespaces.md
csharp_style_namespace_declarations = file_scoped:warning

# sealed-classes.md
dotnet_diagnostic.CA1852.severity = warning

# no-null-forgiving.md
dotnet_diagnostic.CS8601.severity = warning
dotnet_diagnostic.CS8602.severity = warning
dotnet_diagnostic.CS8603.severity = warning

# explicit-access-modifiers.md
dotnet_diagnostic.IDE0036.severity = suggestion
```

## Language version

Some strict rules depend on a minimum C# language version. Check `<LangVersion>` before recommending:

- `required` keyword → C# 11
- File-scoped namespaces → C# 10
- `init` properties → C# 9
