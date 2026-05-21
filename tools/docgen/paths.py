"""Path mapping between C++ include/ headers and docs/codebase/namespaces/ docs."""

import os
from pathlib import Path


def include_to_doc_path(
    header_path: Path,
    include_root: Path,
    docs_root: Path,
) -> Path:
    """Convert an include/ header path to the corresponding docs/ .md path."""
    rel = header_path.relative_to(include_root)
    doc_rel = Path(*rel.parts).with_suffix('.md')
    return docs_root / doc_rel


def display_include_path(
    header_path: Path,
    include_root: Path,
) -> str:
    """Return the include path string used in `#include "..."` directives."""
    rel = header_path.relative_to(include_root)
    return str(rel).replace('\\', '/')


def relative_link(from_doc: Path, to_doc: Path) -> str:
    """Return the relative path from from_doc to to_doc (for markdown links)."""
    rel = os.path.relpath(str(to_doc), str(from_doc.parent))
    return rel.replace('\\', '/')


def build_doc_index(
    headers: list[Path],
    include_root: Path,
    docs_root: Path,
) -> dict[str, Path]:
    """Build a mapping of class/namespace name → doc file path.

    Keys are the bare class or namespace name (last component, e.g. 'i_component').
    """
    index: dict[str, Path] = {}
    for h in headers:
        doc = include_to_doc_path(h, include_root, docs_root)
        stem = h.stem  # e.g. 'i_component', 'floor_plane_math'
        index[stem] = doc
    return index
