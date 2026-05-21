---
description: "Regenerate the wiki docs from docgen source files"
argument-hint: "Use when docs under docs/codebase/namespaces need regeneration or prose updates"
agent: "agent"
---
Regenerate the wiki documentation from the source of truth under [tools](../../tools).

Use this prompt when the generated pages under [docs/codebase/namespaces](../../docs/codebase/namespaces) need to be refreshed, or when wording should be improved.

Required workflow:

1. Inspect the current source-of-truth files first:
	- [tools/overrides.toml](../../tools/overrides.toml)
	- [tools/config.toml](../../tools/config.toml)
	- [tools/docgen](../../tools/docgen)
2. Audit override coverage before regeneration:
	- Determine expected override keys from parsed headers (`namespace/kind/name` without extension).
	- Compare against keys present in [tools/overrides.toml](../../tools/overrides.toml).
	- Detect missing namespace entries under `[__namespaces__]`.
3. If missing entries are found, update [tools/overrides.toml](../../tools/overrides.toml) in the same run:
	- Add missing section stubs or drafted prose for new headers.
	- Add missing `[__namespaces__]` overview entries for new namespaces.
	- Keep existing manual text intact unless explicitly asked to rewrite it.
4. Prefer editing overrides for editorial/prose changes, not generated markdown files.
5. Only edit [tools/docgen](../../tools/docgen) when generator logic itself is incorrect.
6. Run generation and validate:
	- `python -m tools.docgen`
	- Confirm generated output reflects the updated overrides.

Expected behavior when this prompt is used:

- It should check [tools/overrides.toml](../../tools/overrides.toml) for missing coverage.
- It should add/update missing override content when needed.
- It should regenerate docs after source-of-truth updates.