"""Data models for parsed C++ headers."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Param:
    type: str
    name: str


@dataclass
class Method:
    name: str
    return_type: str  # empty string for constructors
    params: list["Param"] = field(default_factory=list)
    is_virtual: bool = False
    is_pure_virtual: bool = False
    is_override: bool = False
    is_const: bool = False
    is_noexcept: bool = False
    is_nodiscard: bool = False
    is_explicit: bool = False
    is_static: bool = False
    is_constructor: bool = False
    signature: str = ""  # formatted source text for display in code blocks


@dataclass
class Field:
    type: str
    name: str


@dataclass
class Struct:
    name: str
    fields: list["Field"] = field(default_factory=list)
    signature: str = ""  # full struct source text for display


@dataclass
class ParsedClass:
    name: str
    namespace: str
    is_interface: bool
    is_final: bool
    bases: list[str]  # base class names as written in source
    constructors: list[Method] = field(default_factory=list)
    public_methods: list[Method] = field(default_factory=list)
    protected_methods: list[Method] = field(default_factory=list)
    # private methods are intentionally excluded from docs


@dataclass
class ParsedNamespaceHelper:
    namespace: str  # e.g. acs::vision::floor_plane_math
    structs: list[Struct] = field(default_factory=list)
    functions: list[Method] = field(default_factory=list)


@dataclass
class ParsedHeader:
    path: Path
    kind: str  # "class" | "interface" | "namespace_helper"
    entity: "Optional[ParsedClass | ParsedNamespaceHelper]" = None
