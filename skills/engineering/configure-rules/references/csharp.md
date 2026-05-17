# C# Project Alignment

Expected `.csproj`, `Directory.Build.props`, and `.editorconfig` settings per preset. Use this during discrepancy detection to compare the target repo's configuration against the chosen preset.

## Recommended

```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
</PropertyGroup>
```

`<Nullable>enable</Nullable>` enables nullable reference type annotations and warnings project-wide. Check for this in `.csproj` **or** in `Directory.Build.props` (which applies to all projects in its directory tree).

## Strict

All recommended settings, plus:

```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  <AnalysisLevel>latest-recommended</AnalysisLevel>
</PropertyGroup>
```

| Flag | What it does |
|------|-------------|
| `TreatWarningsAsErrors` | Turns all compiler warnings into errors — forces nullable and style issues to be resolved |
| `EnforceCodeStyleInBuild` | Applies `.editorconfig` style rules during `dotnet build`, not just in the IDE |
| `AnalysisLevel` | Enables the latest set of Roslyn code-quality analysers; `latest-recommended` is a safe default |

## .editorconfig patterns for style rules

Rules that correspond to `.editorconfig` settings for reference:

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

## Checking a `Directory.Build.props` chain

If `.csproj` does not set `<Nullable>`, check for `Directory.Build.props` in the project directory and each parent directory up to the repo root. A flag set in any ancestor counts as set. Report which file sets each flag when surfacing discrepancies.

## Language version

Strict rules depend on C# language features:
- `required` keyword → C# 11 (`<LangVersion>11</LangVersion>` or higher, or `latest`)
- File-scoped namespaces → C# 10
- `init` properties → C# 9

Check `<LangVersion>` in `.csproj` when recommending strict rules that require a minimum language version.
