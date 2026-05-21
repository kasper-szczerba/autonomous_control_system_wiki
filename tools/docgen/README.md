# docgen Submodule Guide

This generator is designed to be reusable as a git submodule across similar projects.

## Project-level files (local, not committed)

Create these in the parent `tools/` folder of each consuming project:

- `tools/config.toml`
- `tools/overrides.toml`

Use the examples from this submodule:

```powershell
cp tools/docgen/config.toml.example tools/config.toml
cp tools/docgen/overrides.toml.example tools/overrides.toml
```

## What belongs where

- `tools/config.toml`
: Project paths and naming style
  - `[paths]` for `include_root` and `docs_root`
  - `[naming.title_expansions]` for acronym/title style overrides

- `tools/overrides.toml`
: Project prose and descriptions
  - `__overview__`, method and parameter descriptions
  - `[__namespaces__]` for namespace index overviews

- `tools/docgen/` source code
: Shared generic behavior used by all projects

## Run

From the consuming project root:

```powershell
python -m tools.docgen
```

Dry-run:

```powershell
python -m tools.docgen --dry-run
```

## Maintenance rule

When shared generator behavior changes, update these files in the submodule too:

- `tools/docgen/config.toml.example`
- `tools/docgen/overrides.toml.example`
- `tools/docgen/README.md`
