---
description: "Regenerate the wiki docs from docgen source files"
argument-hint: "Use when docs under docs/codebase/namespaces need regeneration or prose updates"
agent: "agent"
---
Regenerate the wiki documentation from the source of truth under [tools](../tools).

Use this prompt when the generated pages under [docs/codebase/namespaces](../docs/codebase/namespaces) need to be refreshed, or when the wording should be improved.

- Inspect the relevant docgen inputs first.
- Prefer updating [tools/overrides.toml](../tools/overrides.toml) for prose changes instead of editing generated markdown directly.
- Use GenAI to draft or refine override text when the change is editorial.
- Keep structural or generator fixes in [tools/docgen](../tools/docgen) only if the generator itself is the problem.
- After making source-of-truth changes, run doc generation and confirm the output matches the intended update.