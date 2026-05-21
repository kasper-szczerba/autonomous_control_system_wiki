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
- **Namespace index overviews**: edit `[__namespaces__]` in `tools/overrides.toml`.
- **Title/acronym expansions** (e.g. `toml` → `TOML` or `Toml`): edit `[naming.title_expansions]` in `tools/config.toml`.
- **Generated prose wording** (e.g. `ptr` → `pointer`): edit `[naming.phrase_expansions]` in `tools/config.toml`.
- **Generated fallback phrase templates** (getter/setter, constructor text, generic parameter text): edit `[phrases]` in `tools/config.toml`.
- **Default method/parameter descriptions**: edit `[descriptions.methods]` and `[descriptions.params]` in `tools/config.toml`.
- **Shared fallback naming logic**: edit `tools/docgen/conventions.py` (logic only, no project prose).
- **Document structure**: edit the Jinja2 templates in `tools/docgen/templates/`.

For repeated cross-project updates, prefer changing TOML sections first so an LLM can maintain style and prose without editing Python source.

## Submodule Reuse Rules

- Keep project-specific paths and naming style in `tools/config.toml`.
- Keep project-specific prose in `tools/overrides.toml`.
- Keep shared logic in `tools/docgen/` generic and reusable across repositories.
- When changing generator behavior, update both:
  - `tools/docgen/config.toml.example`
  - `tools/docgen/overrides.toml.example`

> **Warning**: running the generator **overwrites** existing `.md` files. Never hand-edit generated docs — put custom prose in `tools/overrides.toml` instead.
