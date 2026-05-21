"""Text-based C++ header parser.

Parses consistently clang-formatted C++ headers into structured data models.
No binary dependencies — uses regex and a character-level state machine.
"""

import re
import textwrap
from pathlib import Path
from typing import Optional

from .models import (
    Field,
    Method,
    Param,
    ParsedClass,
    ParsedHeader,
    ParsedNamespaceHelper,
    Struct,
)

# ---------------------------------------------------------------------------
# Comment stripping
# ---------------------------------------------------------------------------


def _strip_comments(source: str) -> str:
    """Remove // and /* */ comments, preserving line structure."""
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    source = re.sub(r"//[^\n]*", "", source)
    return source


# ---------------------------------------------------------------------------
# Bracket-balanced extraction
# ---------------------------------------------------------------------------


def _find_matching_brace(text: str, open_pos: int) -> int:
    """Return the index of the closing } that matches the { at open_pos."""
    assert text[open_pos] == "{"
    depth = 1
    i = open_pos + 1
    while i < len(text) and depth > 0:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    return i - 1  # position of closing }


# ---------------------------------------------------------------------------
# Namespace extraction
# ---------------------------------------------------------------------------


def _find_namespace(source: str) -> tuple[Optional[str], Optional[str]]:
    """Return (namespace_name, body_text) for the top-level namespace."""
    m = re.search(r"\bnamespace\s+([\w:]+)\s*\{", source)
    if not m:
        return None, None
    namespace = m.group(1)
    open_pos = source.index("{", m.start())
    close_pos = _find_matching_brace(source, open_pos)
    body = source[open_pos + 1 : close_pos]
    return namespace, body


# ---------------------------------------------------------------------------
# Class declaration parsing
# ---------------------------------------------------------------------------

_CLASS_RE = re.compile(
    r"\bclass\s+"
    r"(\w+)"  # group 1: class name
    r"(?:\s+final\b)?"  # optional 'final'
    r"(?:\s*:\s*([^{]+?))?"  # group 2: optional base list
    r"\s*\{",
    re.DOTALL,
)

_STRUCT_RE = re.compile(
    r"\bstruct\s+"
    r"(\w+)"  # group 1: struct name
    r"\s*\{",
)


def _parse_bases(base_str: Optional[str]) -> list[str]:
    """Parse 'public A, public virtual B' → ['A', 'B']."""
    if not base_str:
        return []
    bases = []
    for part in base_str.split(","):
        part = re.sub(r"\bstd::enable_shared_from_this\s*<[^>]+>", "", part)
        for kw in ["public", "protected", "private", "virtual"]:
            part = re.sub(r"\b" + kw + r"\b", "", part)
        name = part.strip()
        if name:
            bases.append(name)
    return bases


# ---------------------------------------------------------------------------
# Class body splitting → declarations
# ---------------------------------------------------------------------------


def _split_class_body(body: str) -> list[tuple[str, str, str]]:
    """Split a class body into (access, raw_decl, normalized_decl) tuples.

    - access:     'public' | 'protected' | 'private'
    - raw_decl:   original source lines joined with \\n (for display)
    - normalized: single-line whitespace-normalised text (for parsing)
    """
    results: list[tuple[str, str, str]] = []
    current_access = "private"  # C++ default

    ACCESS_RE = re.compile(r"^\s*(public|protected|private)\s*:\s*$")

    buf: list[str] = []
    paren_depth = 0

    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped:
            if buf:
                buf.append(line)
            continue

        # Access specifier line
        m = ACCESS_RE.match(stripped)
        if m and paren_depth == 0:
            if buf:
                raw = "\n".join(buf)
                norm = " ".join(raw.split())
                if norm:
                    results.append((current_access, raw, norm))
                buf = []
                paren_depth = 0
            current_access = m.group(1)
            continue

        # Track parenthesis depth for multiline signatures
        paren_depth += stripped.count("(") - stripped.count(")")
        buf.append(line)

        # A declaration is complete when we hit ';' at depth 0
        if ";" in stripped and paren_depth == 0:
            raw = "\n".join(buf)
            last_semi = raw.rfind(";")
            raw = raw[: last_semi + 1]
            normalized = " ".join(raw[: raw.rfind(";")].split())
            if normalized:
                results.append((current_access, raw, normalized))
            buf = []

    return results


# ---------------------------------------------------------------------------
# Individual method declaration parsing
# ---------------------------------------------------------------------------

_SKIP_PREFIXES = ("using ", "friend ", "typedef ", "static_assert")


def _format_signature(raw: str) -> str:
    """Dedent and normalise raw source text for a code block."""
    # Dedent BEFORE stripping so the relative indentation of continuation
    # lines (e.g. aligned constructor params) is preserved correctly.
    return textwrap.dedent(raw).strip()


def _find_matching_paren(text: str, start: int) -> int:
    """Return index of ) matching the ( at start."""
    depth = 1
    i = start + 1
    while i < len(text) and depth > 0:
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
        i += 1
    return i - 1


def _parse_method(normalized: str, raw: str, class_name: str) -> Optional[Method]:
    """Parse a normalised single-line C++ declaration into a Method."""
    if any(normalized.startswith(p) for p in _SKIP_PREFIXES):
        return None
    if "~" in normalized:
        return None  # destructors are not documented
    if "(" not in normalized:
        return None  # field, not a method

    is_nodiscard = "[[nodiscard]]" in normalized
    is_virtual = bool(re.search(r"\bvirtual\b", normalized))
    is_pure_virtual = bool(re.search(r"=\s*0\s*$", normalized))
    is_override = bool(re.search(r"\boverride\b", normalized))
    is_const = bool(re.search(r"\)\s*const\b", normalized))
    is_noexcept = bool(re.search(r"\bnoexcept\b", normalized))
    is_explicit = bool(re.search(r"\bexplicit\b", normalized))
    is_static = bool(re.search(r"\bstatic\b", normalized))

    # Strip qualifiers for structural parsing
    clean = normalized
    for kw_re in [r"\[\[nodiscard\]\]", r"\[\[.*?\]\]"]:
        clean = re.sub(kw_re, "", clean)
    for kw in [
        "virtual",
        "override",
        "explicit",
        "static",
        "inline",
        "constexpr",
        "consteval",
        "constinit",
    ]:
        clean = re.sub(r"\b" + kw + r"\b", "", clean)
    clean = re.sub(r"=\s*0\s*$", "", clean)
    clean = re.sub(r"=\s*default\s*$", "", clean)
    clean = re.sub(r"=\s*delete\s*$", "", clean)
    clean = " ".join(clean.split())

    paren_start = clean.find("(")
    if paren_start == -1:
        return None

    paren_end = _find_matching_paren(clean, paren_start)
    before_params = clean[:paren_start].strip()
    params_text = clean[paren_start + 1 : paren_end].strip()

    # Method name = last identifier before '('
    name_match = re.search(r"(\w+)\s*$", before_params)
    if not name_match:
        return None
    method_name = name_match.group(1)
    return_type = before_params[: name_match.start()].strip()

    is_constructor = method_name == class_name and not return_type

    params = _parse_params(params_text)
    signature = _format_signature(raw)

    return Method(
        name=method_name,
        return_type=return_type,
        params=params,
        is_virtual=is_virtual,
        is_pure_virtual=is_pure_virtual,
        is_override=is_override,
        is_const=is_const,
        is_noexcept=is_noexcept,
        is_nodiscard=is_nodiscard,
        is_explicit=is_explicit,
        is_static=is_static,
        is_constructor=is_constructor,
        signature=signature,
    )


# ---------------------------------------------------------------------------
# Parameter list parsing
# ---------------------------------------------------------------------------


def _split_params(params_text: str) -> list[str]:
    """Split 'a, b<c, d>, e' on commas respecting nested <> and ()."""
    if not params_text.strip():
        return []
    result: list[str] = []
    depth = 0
    current: list[str] = []
    for ch in params_text:
        if ch in "(<":
            depth += 1
            current.append(ch)
        elif ch in ")>":
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch == "," and depth == 0:
            p = "".join(current).strip()
            if p:
                result.append(p)
            current = []
        else:
            current.append(ch)
    last = "".join(current).strip()
    if last:
        result.append(last)
    return result


def _parse_params(params_text: str) -> list[Param]:
    """Parse a parameter list string into Param objects."""
    params: list[Param] = []
    for p in _split_params(params_text):
        p = p.strip()
        if not p or p == "void":
            continue
        # Strip default value (find '=' at depth 0)
        depth = 0
        eq_pos = -1
        for i, ch in enumerate(p):
            if ch in "(<":
                depth += 1
            elif ch in ")>":
                depth = max(0, depth - 1)
            elif ch == "=" and depth == 0:
                eq_pos = i
                break
        if eq_pos != -1:
            p = p[:eq_pos].strip()
        # Parameter name = last identifier
        name_match = re.search(r"(\w+)\s*$", p)
        if not name_match:
            continue
        name = name_match.group(1)
        type_str = p[: name_match.start()].strip()
        if "..." in type_str or name == "...":
            continue
        params.append(Param(type=type_str, name=name))
    return params


# ---------------------------------------------------------------------------
# Struct parsing (for namespace helpers)
# ---------------------------------------------------------------------------


def _parse_struct_body(struct_name: str, body_text: str, raw_text: str) -> Struct:
    """Parse a struct body into a Struct object."""
    fields: list[Field] = []
    for line in body_text.split("\n"):
        line = line.strip()
        if not line or ":" in line:
            continue
        m = re.match(r"(.+?)\s+(\w+)\s*;", line)
        if m:
            fields.append(Field(type=m.group(1).strip(), name=m.group(2)))
    return Struct(name=struct_name, fields=fields, signature=raw_text.strip())


# ---------------------------------------------------------------------------
# Class body → ParsedClass
# ---------------------------------------------------------------------------


def _parse_class_entity(
    class_name: str,
    namespace: str,
    is_interface: bool,
    is_final: bool,
    bases: list[str],
    class_body: str,
) -> ParsedClass:
    decls = _split_class_body(class_body)

    constructors: list[Method] = []
    public_methods: list[Method] = []
    protected_methods: list[Method] = []

    for access, raw, normalized in decls:
        method = _parse_method(normalized, raw, class_name)
        if method is None:
            continue
        if method.is_constructor:
            constructors.append(method)
        elif access == "public":
            public_methods.append(method)
        elif access == "protected":
            protected_methods.append(method)

    return ParsedClass(
        name=class_name,
        namespace=namespace,
        is_interface=is_interface,
        is_final=is_final,
        bases=bases,
        constructors=constructors,
        public_methods=public_methods,
        protected_methods=protected_methods,
    )


# ---------------------------------------------------------------------------
# Namespace helper body → ParsedNamespaceHelper
# ---------------------------------------------------------------------------


def _parse_namespace_helper_entity(namespace: str, body: str) -> ParsedNamespaceHelper:
    structs: list[Struct] = []
    functions: list[Method] = []

    # Extract and parse structs
    for m in _STRUCT_RE.finditer(body):
        struct_name = m.group(1)
        open_pos = body.index("{", m.start())
        close_pos = _find_matching_brace(body, open_pos)
        struct_body = body[open_pos + 1 : close_pos]
        raw_text = body[m.start() : close_pos + 1]
        structs.append(_parse_struct_body(struct_name, struct_body, raw_text))

    # Remove struct bodies before scanning for free functions
    body_clean = _STRUCT_RE.sub("", body)
    body_clean = re.sub(
        r"\{[^{}]*\}", "", body_clean
    )  # remove any remaining inline bodies

    # Parse free function declarations
    buf: list[str] = []
    paren_depth = 0
    for line in body_clean.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        paren_depth += stripped.count("(") - stripped.count(")")
        buf.append(line)
        if ";" in stripped and paren_depth == 0:
            raw = "\n".join(buf)
            last_semi = raw.rfind(";")
            raw = raw[: last_semi + 1]
            normalized = " ".join(raw[: raw.rfind(";")].split())
            if normalized and "(" in normalized:
                method = _parse_method(normalized, raw, "")
                if method and not method.is_constructor:
                    functions.append(method)
            buf = []

    return ParsedNamespaceHelper(
        namespace=namespace, structs=structs, functions=functions
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_header(path: Path) -> Optional[ParsedHeader]:
    """Parse a C++ header file. Returns None if the file cannot be parsed."""
    try:
        source = path.read_text(encoding="utf-8")
    except Exception:
        return None

    source = _strip_comments(source)
    namespace, body = _find_namespace(source)
    if namespace is None:
        return None

    class_match = _CLASS_RE.search(body)
    if class_match:
        class_name = class_match.group(1)
        base_str = class_match.group(2)
        is_final = "final" in class_match.group(0)
        bases = _parse_bases(base_str)
        is_interface = class_name.startswith("i_") or "interfaces" in str(path).replace(
            "\\", "/"
        )

        open_pos = body.index("{", class_match.start())
        close_pos = _find_matching_brace(body, open_pos)
        class_body = body[open_pos + 1 : close_pos]

        entity = _parse_class_entity(
            class_name=class_name,
            namespace=namespace,
            is_interface=is_interface,
            is_final=is_final,
            bases=bases,
            class_body=class_body,
        )
        kind = "interface" if is_interface else "class"
        return ParsedHeader(path=path, kind=kind, entity=entity)

    else:
        entity = _parse_namespace_helper_entity(namespace, body)
        return ParsedHeader(path=path, kind="namespace_helper", entity=entity)
