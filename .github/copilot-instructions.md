# Copilot Instructions

## First-time setup

`tools/docgen/` is a git submodule. After cloning, copy the example files and configure your paths:

```powershell
git submodule update --init
cp tools/docgen/config.toml.example  tools/config.toml
cp tools/docgen/overrides.toml.example tools/overrides.toml
# Edit tools/config.toml → set include_root and docs_root for this project
```

`tools/config.toml` and `tools/overrides.toml` are gitignored — never commit them.

## Doc generation

The wiki docs under `docs/codebase/namespaces/` are auto-generated from the C++ headers in the sibling repo. The generator lives in `tools/docgen/`.

### Regenerate all docs

```powershell
# From the wiki root
.venv\Scripts\activate
python -m tools.docgen
```

### Dry-run (no writes)

```powershell
python -m tools.docgen --dry-run
```

### Regenerate specific headers

```powershell
python -m tools.docgen path/to/header.h
```

## Customising generated output

- **Overviews, method descriptions, param descriptions**: edit `tools/overrides.toml`.
  - Key format: `["namespace/kind/class_name"]`, then `__overview__`, method name, or `"method.param"`.
- **Naming conventions** (auto-descriptions, title expansions): edit `tools/docgen/conventions.py`.
- **Document structure**: edit the Jinja2 templates in `tools/docgen/templates/`.

> **Warning**: running the generator **overwrites** existing `.md` files. Never hand-edit generated docs — put custom prose in `tools/overrides.toml` instead.
