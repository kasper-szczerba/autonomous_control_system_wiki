"""Renders parsed headers into markdown documentation using Jinja2 templates.

Flow:
  1. Load all parsed headers → build a class-name → doc-path index
  2. Load overrides.toml for custom overviews / method descriptions
  3. For each header, build a render context and fill it with:
       - Structural info from ParsedHeader (100% deterministic)
       - Descriptions from conventions.py (naming conventions)
       - Overrides from overrides.toml (manual prose when needed)
  4. Render via the appropriate Jinja2 template
"""

import re
import textwrap
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import jinja2

from . import conventions as conv
from .models import Method, ParsedClass, ParsedHeader, ParsedNamespaceHelper
from .paths import relative_link

# ---------------------------------------------------------------------------
# Render context dataclasses
# ---------------------------------------------------------------------------


@dataclass
class ParamCtx:
    name: str
    description: str


@dataclass
class MethodCtx:
    name: str
    heading: str
    anchor: str
    signature: str
    description: str
    params: list[ParamCtx]
    is_pure_virtual: bool


@dataclass
class IfaceImplCtx:
    name: str  # e.g. 'i_obstacle_detector'
    link: str  # relative .md path
    methods: list  # list of {name, anchor}


@dataclass
class StructCtx:
    heading: str
    signature: str
    description: str
    fields: list  # list of {name, type, description}


@dataclass
class RelatedClassCtx:
    name: str
    display_name: str
    link: str


@dataclass
class NamespaceLinkCtx:
    name: str
    link: str


@dataclass
class NamespacePageCtx:
    display_name: str
    namespace: str
    overview: str
    interfaces: list[NamespaceLinkCtx] = field(default_factory=list)
    implementations: list[NamespaceLinkCtx] = field(default_factory=list)
    graph_md: str = ""


@dataclass
class DocCtx:
    kind: str
    display_name: str
    class_name: str
    namespace: str
    include_path: str
    overview: str
    inheritance_bases_diagram_md: str = ""
    inheritance_derived_diagram_md: str = ""
    inheritance_bases: list[RelatedClassCtx] = field(default_factory=list)
    inheritance_derived: list[RelatedClassCtx] = field(default_factory=list)
    inheritance_bases_md: str = ""
    inheritance_derived_md: str = ""
    constructors: list[MethodCtx] = field(default_factory=list)
    interface_impls: list[IfaceImplCtx] = field(default_factory=list)
    own_public_methods: list[MethodCtx] = field(default_factory=list)
    protected_methods: list[MethodCtx] = field(default_factory=list)
    # namespace helpers only:
    structs: list[StructCtx] = field(default_factory=list)
    functions: list[MethodCtx] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Overrides loading
# ---------------------------------------------------------------------------


def load_overrides(overrides_path: Path) -> dict:
    """Load overrides.toml. Returns empty dict if file doesn't exist."""
    if not overrides_path.exists():
        return {}
    with open(overrides_path, "rb") as f:
        return tomllib.load(f)


def _override_key(header_path: Path, include_root: Path) -> str:
    """Return the override lookup key for a header, e.g. 'vision/implementation/detection/obstacle_detector'."""
    rel = header_path.relative_to(include_root)
    return str(rel.with_suffix("")).replace("\\", "/")


# ---------------------------------------------------------------------------
# Jinja2 environment
# ---------------------------------------------------------------------------


def _make_jinja_env(templates_dir: Path) -> jinja2.Environment:
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=False,
    )


# ---------------------------------------------------------------------------
# Context builders
# ---------------------------------------------------------------------------


def _method_ctx(
    method: Method,
    override_key: str,  # e.g. 'vision/.../obstacle_detector'
    method_overrides: dict,  # overrides sub-dict for this header
) -> MethodCtx:
    heading = conv.method_heading(method.name)
    anchor = conv.method_anchor(method.name)

    # Description: override → convention → empty
    desc_key = method.name
    description = method_overrides.get(desc_key, "") or conv.describe_method(
        method.name
    )

    params = []
    for p in method.params:
        pdesc = method_overrides.get(
            f"{method.name}.{p.name}", ""
        ) or conv.describe_param(p.name, p.type)
        params.append(ParamCtx(name=p.name, description=pdesc))

    return MethodCtx(
        name=method.name,
        heading=heading,
        anchor=anchor,
        signature=method.signature,
        description=description,
        params=params,
        is_pure_virtual=method.is_pure_virtual,
    )


def _constructor_ctx(
    method: Method,
    class_name: str,
    method_overrides: dict,
) -> MethodCtx:
    heading = conv.constructor_heading(method.params)
    anchor = conv.heading_to_anchor(heading)
    description = method_overrides.get(
        "__constructor__", ""
    ) or conv.constructor_description(class_name, method.params)
    params = []
    for p in method.params:
        pdesc = method_overrides.get(
            f"__constructor__.{p.name}", ""
        ) or conv.describe_param(p.name, p.type)
        params.append(ParamCtx(name=p.name, description=pdesc))

    return MethodCtx(
        name=class_name,
        heading=heading,
        anchor=anchor,
        signature=method.signature,
        description=description,
        params=params,
        is_pure_virtual=False,
    )


def _build_interface_impls(
    entity: ParsedClass,
    doc_path: Path,
    doc_index: dict[str, Path],  # class_name → doc_path
    parsed_index: dict[str, ParsedHeader],  # class_name → ParsedHeader
) -> list[IfaceImplCtx]:
    """Build the 'Implementations' list for an impl class."""
    impls: list[IfaceImplCtx] = []

    for base in entity.bases:
        # Only include i_* bases (direct interface bases)
        base_name = base.split("::")[-1]  # strip namespace prefix
        if not base_name.startswith("i_"):
            continue
        if base_name not in doc_index:
            continue

        iface_doc = doc_index[base_name]
        link = relative_link(doc_path, iface_doc)

        # Collect method names from the parsed interface
        method_entries = []
        if base_name in parsed_index:
            iface_parsed = parsed_index[base_name].entity
            if isinstance(iface_parsed, ParsedClass):
                for m in iface_parsed.public_methods:
                    method_entries.append(
                        {
                            "name": m.name,
                            "anchor": conv.method_anchor(m.name),
                        }
                    )
        else:
            # Fallback: use the impl's own public methods as a proxy
            for m in entity.public_methods:
                method_entries.append(
                    {
                        "name": m.name,
                        "anchor": conv.method_anchor(m.name),
                    }
                )

        impls.append(
            IfaceImplCtx(
                name=_symbol_link_label(base_name), link=link, methods=method_entries
            )
        )

    return impls


def _class_display_name(class_name: str) -> str:
    return _symbol_link_label(class_name)


def _inheritance_label(class_name: str) -> str:
    return _symbol_link_label(class_name)


def _snake_to_lower_camel(name: str) -> str:
    return name


def _symbol_link_label(symbol_name: str) -> str:
    """Render class/interface symbol names in project-style snake_case for links/diagrams."""
    return symbol_name


def _build_inheritance_maps(
    parsed_index: dict[str, ParsedHeader],
    doc_index: dict[str, Path],
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    bases_map: dict[str, list[str]] = {}
    derived_map: dict[str, list[str]] = {}

    for class_name, parsed in parsed_index.items():
        if not isinstance(parsed.entity, ParsedClass):
            continue
        direct_bases: list[str] = []
        for base in parsed.entity.bases:
            base_name = base.split("::")[-1]
            if base_name in doc_index:
                direct_bases.append(base_name)
                derived_map.setdefault(base_name, []).append(class_name)
        if direct_bases:
            bases_map[class_name] = direct_bases

    return bases_map, derived_map


def _render_inheritance_tree(
    root_name: str,
    relation_map: dict[str, list[str]],
    doc_path: Path,
    doc_index: dict[str, Path],
    indent: int = 0,
    visited: set[str] | None = None,
) -> str:
    if visited is None:
        visited = set()
    if root_name not in doc_index or root_name in visited:
        return ""

    visited = set(visited)
    visited.add(root_name)

    lines: list[str] = []
    indent_str = "  " * indent
    link = relative_link(doc_path, doc_index[root_name])
    lines.append(f"{indent_str}- [`{_inheritance_label(root_name)}`]({link})")

    for child_name in sorted(relation_map.get(root_name, [])):
        child_text = _render_inheritance_tree(
            child_name,
            relation_map,
            doc_path,
            doc_index,
            indent + 1,
            visited,
        )
        if child_text:
            lines.append(child_text)

    return "\n".join(lines)


def _build_inheritance_graph(
    parsed_index: dict[str, ParsedHeader],
    doc_index: dict[str, Path],
) -> str:
    edges: set[tuple[str, str, str, str]] = set()

    for class_name, parsed in parsed_index.items():
        if not isinstance(parsed.entity, ParsedClass) or class_name not in doc_index:
            continue
        child_id = class_name.replace("::", "_")
        child_label = _inheritance_label(class_name)
        for base in parsed.entity.bases:
            base_name = base.split("::")[-1]
            if base_name not in doc_index:
                continue
            base_id = base_name.replace("::", "_")
            base_label = _inheritance_label(base_name)
            edges.add((base_id, base_label, child_id, child_label))

    lines = ["```mermaid", "graph TD"]
    for base_id, base_label, child_id, child_label in sorted(edges):
        lines.append(f'    {base_id}["{base_label}"] --> {child_id}["{child_label}"]')
    lines.append("```")
    return "\n".join(lines)


def _doc_display_name(parsed: ParsedHeader) -> str:
    entity = parsed.entity
    if parsed.kind in ("interface", "class") and isinstance(entity, ParsedClass):
        if entity.is_interface:
            return entity.name
        return conv.snake_to_title(entity.name)
    if parsed.kind == "namespace_helper" and isinstance(entity, ParsedNamespaceHelper):
        last_segment = entity.namespace.split("::")[-1]
        display_name = conv.snake_to_title(last_segment) + " Helpers"
        if last_segment.endswith("_helpers") or last_segment.endswith("helper"):
            display_name = conv.snake_to_title(last_segment)
        return display_name
    return parsed.path.stem


def _namespace_link_label(parsed: ParsedHeader) -> str:
    entity = parsed.entity
    if parsed.kind == "interface" and isinstance(entity, ParsedClass):
        return _symbol_link_label(entity.name)
    if parsed.kind == "class" and isinstance(entity, ParsedClass):
        return _symbol_link_label(entity.name)
    if parsed.kind == "namespace_helper" and isinstance(entity, ParsedNamespaceHelper):
        return _doc_display_name(parsed)
    return parsed.path.stem


def _doc_title(kind: str, entity: ParsedClass | ParsedNamespaceHelper) -> str:
    if isinstance(entity, ParsedClass):
        base_name = entity.name
        if (kind == "interface" or entity.is_interface) and entity.name.startswith(
            "i_"
        ):
            base_name = entity.name[2:]
        base = conv.snake_to_title(base_name)
        if kind == "interface" or entity.is_interface:
            return f"{base} Interface"
        return base
    if isinstance(entity, ParsedNamespaceHelper):
        return conv.snake_to_title(entity.namespace.split("::")[-1])
    return ""


def _namespace_overview(overrides: dict, namespace_name: str) -> str:
    section = overrides.get("__namespaces__", {})
    if isinstance(section, dict):
        text = section.get(namespace_name, "")
        if isinstance(text, str):
            return text
    return ""


def _build_namespace_graph(
    namespace_name: str,
    parsed_headers: list[ParsedHeader],
    doc_index: dict[str, Path],
) -> str:
    nodes: dict[str, str] = {}
    edges: set[tuple[str, str]] = set()

    def node_id_for(name: str, doc_path: Path) -> str:
        raw = str(doc_path.with_suffix(""))
        return re.sub(r"[^0-9A-Za-z_]", "_", raw)

    def add_node(name: str, doc_path: Path, label: str) -> str:
        node_id = node_id_for(name, doc_path)
        nodes[node_id] = label
        return node_id

    for parsed in parsed_headers:
        entity = parsed.entity
        if not isinstance(entity, ParsedClass):
            continue
        parts = entity.namespace.split("::")
        if len(parts) < 2 or parts[0] != "acs" or parts[1] != namespace_name:
            continue

        child_doc = doc_index.get(entity.name)
        if child_doc is None:
            continue
        child_id = add_node(entity.name, child_doc, _symbol_link_label(entity.name))

        for base in entity.bases:
            base_name = base.split("::")[-1]
            base_doc = doc_index.get(base_name)
            if base_doc is None:
                continue
            base_parsed = next(
                (
                    p
                    for p in parsed_headers
                    if p.entity
                    and hasattr(p.entity, "name")
                    and getattr(p.entity, "name") == base_name
                ),
                None,
            )
            if base_parsed and isinstance(base_parsed.entity, ParsedClass):
                base_label = _symbol_link_label(base_name)
            else:
                base_label = conv.snake_to_title(base_name)
            base_id = add_node(base_name, base_doc, base_label)
            edges.add((base_id, child_id))

    lines = ["```mermaid", "graph TD"]
    for node_id, label in sorted(nodes.items()):
        lines.append(f'    {node_id}["{label}"]')
    for base_id, child_id in sorted(edges):
        lines.append(f"    {base_id} --> {child_id}")
    lines.append("```")
    return "\n".join(lines)


def render_namespace_index_pages(
    parsed_headers: list[ParsedHeader],
    docs_root: Path,
    doc_index: dict[str, Path],
    overrides: dict,
    env: jinja2.Environment,
) -> list[tuple[Path, str]]:
    """Render docs/codebase/namespaces/<namespace>/index.md pages."""
    pages: list[tuple[Path, str]] = []
    namespace_names: list[str] = []
    seen: set[str] = set()

    for parsed in parsed_headers:
        entity = parsed.entity
        if not isinstance(entity, (ParsedClass, ParsedNamespaceHelper)):
            continue
        parts = entity.namespace.split("::")
        if len(parts) < 2 or parts[0] != "acs":
            continue
        ns = parts[1]
        if ns in seen:
            continue
        seen.add(ns)
        namespace_names.append(ns)

    for ns in namespace_names:
        interface_docs: list[NamespaceLinkCtx] = []
        implementation_docs: list[NamespaceLinkCtx] = []
        for parsed in parsed_headers:
            entity = parsed.entity
            if entity is None or not hasattr(entity, "namespace"):
                continue
            parts = getattr(entity, "namespace").split("::")
            if len(parts) < 2 or parts[0] != "acs" or parts[1] != ns:
                continue
            doc_path = doc_index.get(getattr(entity, "name", parsed.path.stem))
            if doc_path is None:
                continue
            label = _namespace_link_label(parsed)
            link_ctx = NamespaceLinkCtx(
                name=label,
                link=relative_link(docs_root / ns / "index.md", doc_path),
            )
            if parsed.kind == "interface":
                interface_docs.append(link_ctx)
            elif parsed.kind == "class":
                implementation_docs.append(link_ctx)

        interface_docs.sort(key=lambda p: p.name.lower())
        implementation_docs.sort(key=lambda p: p.name.lower())
        ctx = NamespacePageCtx(
            display_name=conv.snake_to_title(ns),
            namespace=f"acs::{ns}",
            overview=_namespace_overview(overrides, ns),
            interfaces=interface_docs,
            implementations=implementation_docs,
            graph_md=_build_namespace_graph(ns, parsed_headers, doc_index),
        )
        template = env.get_template("namespace_index.md.j2")
        rendered = template.render(**ctx.__dict__)
        rendered = re.sub(r"\n{3,}", "\n\n", rendered).strip() + "\n"
        pages.append((docs_root / ns / "index.md", rendered))

    return pages


def _render_inheritance_diagram(
    root_name: str,
    relation_map: dict[str, list[str]],
    doc_index: dict[str, Path],
) -> str:
    """Render a Mermaid graph for the inheritance tree rooted at root_name."""
    edges: set[tuple[str, str, str, str]] = set()

    def walk(node_name: str, visited: set[str]) -> None:
        if node_name in visited or node_name not in doc_index:
            return
        visited.add(node_name)
        node_id = node_name.replace("::", "_")
        node_label = _inheritance_label(node_name)
        for child_name in sorted(relation_map.get(node_name, [])):
            if child_name not in doc_index:
                continue
            child_id = child_name.replace("::", "_")
            child_label = _inheritance_label(child_name)
            edges.add((node_id, node_label, child_id, child_label))
            walk(child_name, visited)

    walk(root_name, set())

    lines = ["```mermaid", "graph TD"]
    if root_name in doc_index:
        root_id = root_name.replace("::", "_")
        root_label = _inheritance_label(root_name)
        lines.append(f'    {root_id}["{root_label}"]')
    for base_id, base_label, child_id, child_label in sorted(edges):
        lines.append(f'    {base_id}["{base_label}"] --> {child_id}["{child_label}"]')
    lines.append("```")
    return "\n".join(lines)


def _build_inheritance_relations(
    entity: ParsedClass,
    doc_path: Path,
    doc_index: dict[str, Path],
    parsed_index: dict[str, ParsedHeader],
) -> tuple[list[RelatedClassCtx], list[RelatedClassCtx]]:
    """Return direct base classes and direct derived classes for a class."""
    bases: list[RelatedClassCtx] = []
    seen_bases: set[str] = set()

    for base in entity.bases:
        base_name = base.split("::")[-1]
        if base_name in seen_bases or base_name not in doc_index:
            continue
        seen_bases.add(base_name)
        bases.append(
            RelatedClassCtx(
                name=base_name,
                display_name=_class_display_name(base_name),
                link=relative_link(doc_path, doc_index[base_name]),
            )
        )

    derived: list[RelatedClassCtx] = []
    seen_derived: set[str] = set()
    for child_name, child_parsed in parsed_index.items():
        if child_name == entity.name or not isinstance(
            child_parsed.entity, ParsedClass
        ):
            continue
        child_entity = child_parsed.entity
        if not any(base.split("::")[-1] == entity.name for base in child_entity.bases):
            continue
        if child_name in seen_derived or child_name not in doc_index:
            continue
        seen_derived.add(child_name)
        derived.append(
            RelatedClassCtx(
                name=child_name,
                display_name=_class_display_name(child_name),
                link=relative_link(doc_path, doc_index[child_name]),
            )
        )

    return bases, derived


def _default_overview(kind: str, entity: ParsedClass | ParsedNamespaceHelper) -> str:
    """Generate a minimal placeholder overview."""
    if kind == "interface" and isinstance(entity, ParsedClass):
        display = conv.snake_to_title(entity.name.lstrip("i_"))
        return f"Interface for {display.lower()}."
    if kind == "class" and isinstance(entity, ParsedClass):
        i_bases = [
            b.split("::")[-1]
            for b in entity.bases
            if b.split("::")[-1].startswith("i_")
        ]
        if i_bases:
            return f"Concrete implementation of `{i_bases[0]}`."
        return f"{conv.snake_to_title(entity.name)}."
    if kind == "namespace_helper" and isinstance(entity, ParsedNamespaceHelper):
        last_segment = entity.namespace.split("::")[-1]
        return f"Helper utilities for {conv.snake_to_title(last_segment).lower()}."
    return ""


# ---------------------------------------------------------------------------
# Main render function
# ---------------------------------------------------------------------------


def render_header(
    parsed: ParsedHeader,
    include_root: Path,
    docs_root: Path,
    doc_index: dict[str, Path],
    parsed_index: dict[str, ParsedHeader],
    overrides: dict,
    env: jinja2.Environment,
) -> tuple[Path, str]:
    """Build a DocCtx from a ParsedHeader and render it.

    Returns (output_doc_path, rendered_markdown_text).
    """
    from .paths import include_to_doc_path, display_include_path

    doc_path = include_to_doc_path(parsed.path, include_root, docs_root)
    include_path_str = display_include_path(parsed.path, include_root)
    override_key = _override_key(parsed.path, include_root)
    hdr_overrides: dict = overrides.get(override_key, {})

    bases_map, derived_map = _build_inheritance_maps(parsed_index, doc_index)

    entity = parsed.entity

    # ------------------------------------------------------------------ #
    # Interface / class
    # ------------------------------------------------------------------ #
    if parsed.kind in ("interface", "class") and isinstance(entity, ParsedClass):
        display_name = _doc_title(parsed.kind, entity)

        overview = hdr_overrides.get("__overview__", "") or _default_overview(
            parsed.kind, entity
        )
        inheritance_bases, inheritance_derived = _build_inheritance_relations(
            entity, doc_path, doc_index, parsed_index
        )
        inheritance_bases_diagram_md = _render_inheritance_diagram(
            entity.name, bases_map, doc_index
        )
        inheritance_derived_diagram_md = _render_inheritance_diagram(
            entity.name, derived_map, doc_index
        )
        inheritance_bases_md = _render_inheritance_tree(
            entity.name, bases_map, doc_path, doc_index
        )
        inheritance_derived_md = _render_inheritance_tree(
            entity.name, derived_map, doc_path, doc_index
        )

        constructors = [
            _constructor_ctx(c, entity.name, hdr_overrides) for c in entity.constructors
        ]

        if entity.is_interface:
            public_methods = [
                _method_ctx(m, override_key, hdr_overrides)
                for m in entity.public_methods
            ]
            ctx = DocCtx(
                kind=parsed.kind,
                display_name=display_name,
                class_name=entity.name,
                namespace=entity.namespace,
                include_path=include_path_str,
                overview=overview,
                inheritance_bases_diagram_md=inheritance_bases_diagram_md,
                inheritance_derived_diagram_md=inheritance_derived_diagram_md,
                inheritance_bases=inheritance_bases,
                inheritance_derived=inheritance_derived,
                inheritance_bases_md=inheritance_bases_md,
                inheritance_derived_md=inheritance_derived_md,
                constructors=constructors,
                own_public_methods=public_methods,
            )
            template = env.get_template("interface.md.j2")

        else:
            # Determine whether to show "Implementations" or individual methods
            has_i_bases = any(b.split("::")[-1].startswith("i_") for b in entity.bases)
            if has_i_bases:
                interface_impls = _build_interface_impls(
                    entity, doc_path, doc_index, parsed_index
                )
                own_public = []
            else:
                interface_impls = []
                own_public = [
                    _method_ctx(m, override_key, hdr_overrides)
                    for m in entity.public_methods
                ]

            protected = [
                _method_ctx(m, override_key, hdr_overrides)
                for m in entity.protected_methods
            ]

            ctx = DocCtx(
                kind=parsed.kind,
                display_name=display_name,
                class_name=entity.name,
                namespace=entity.namespace,
                include_path=include_path_str,
                overview=overview,
                inheritance_bases_diagram_md=inheritance_bases_diagram_md,
                inheritance_derived_diagram_md=inheritance_derived_diagram_md,
                inheritance_bases=inheritance_bases,
                inheritance_derived=inheritance_derived,
                inheritance_bases_md=inheritance_bases_md,
                inheritance_derived_md=inheritance_derived_md,
                constructors=constructors,
                interface_impls=interface_impls,
                own_public_methods=own_public,
                protected_methods=protected,
            )
            template = env.get_template("impl.md.j2")

    # ------------------------------------------------------------------ #
    # Namespace helper
    # ------------------------------------------------------------------ #
    elif parsed.kind == "namespace_helper" and isinstance(
        entity, ParsedNamespaceHelper
    ):
        display_name = _doc_title(parsed.kind, entity)

        overview = hdr_overrides.get("__overview__", "") or _default_overview(
            parsed.kind, entity
        )

        structs = []
        for s in entity.structs:
            s_overrides = hdr_overrides.get(s.name, {})
            s_desc = (
                s_overrides.get("__description__", "")
                if isinstance(s_overrides, dict)
                else ""
            )
            fields = []
            for f in s.fields:
                fdesc = (
                    s_overrides.get(f.name, "") if isinstance(s_overrides, dict) else ""
                ) or conv.describe_param(f.name, f.type)
                fields.append({"name": f.name, "type": f.type, "description": fdesc})
            structs.append(
                StructCtx(
                    heading=conv.snake_to_title(s.name),
                    signature=s.signature,
                    description=s_desc,
                    fields=fields,
                )
            )

        functions = [
            _method_ctx(f, override_key, hdr_overrides) for f in entity.functions
        ]

        ctx = DocCtx(
            kind="namespace_helper",
            display_name=display_name,
            class_name="",
            namespace=entity.namespace,
            include_path=include_path_str,
            overview=overview,
            structs=structs,
            functions=functions,
        )
        template = env.get_template("namespace.md.j2")

    else:
        raise ValueError(f"Unknown kind {parsed.kind!r} for {parsed.path}")

    rendered = template.render(**ctx.__dict__)

    # Clean up excessive blank lines (Jinja2 trimming can still leave some)
    rendered = re.sub(r"\n{3,}", "\n\n", rendered).strip() + "\n"

    return doc_path, rendered


def render_namespaces_index(
    parsed_headers: list[ParsedHeader],
    include_root: Path,
    docs_root: Path,
    doc_index: dict[str, Path],
    parsed_index: dict[str, ParsedHeader],
    env: jinja2.Environment,
) -> tuple[Path, str]:
    """Render docs/codebase/namespaces/index.md."""
    index_path = docs_root / "index.md"
    namespace_names: list[str] = []
    seen: set[str] = set()

    for parsed in parsed_headers:
        if parsed.entity is None or not hasattr(parsed.entity, "namespace"):
            continue
        parts = getattr(parsed.entity, "namespace").split("::")
        if len(parts) < 2 or parts[0] != "acs":
            continue
        namespace = parts[1]
        if namespace in seen:
            continue
        seen.add(namespace)
        namespace_names.append(namespace)

    namespace_links = [
        NamespaceLinkCtx(
            name=conv.snake_to_title(ns),
            link=f"{ns}/index.md",
        )
        for ns in namespace_names
    ]

    ctx = {
        "inheritance_graph": _build_inheritance_graph(parsed_index, doc_index),
        "namespace_links": namespace_links,
    }
    template = env.get_template("namespaces_index.md.j2")
    rendered = template.render(**ctx)
    rendered = re.sub(r"\n{3,}", "\n\n", rendered).strip() + "\n"
    return index_path, rendered
