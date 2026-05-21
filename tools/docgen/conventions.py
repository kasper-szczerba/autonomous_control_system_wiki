"""Naming convention rules for auto-generating descriptions from identifiers."""

import re

_TITLE_EXPANSIONS: dict[str, str] = {}
_PHRASE_EXPANSIONS: dict[str, str] = {}
_KNOWN_METHODS: dict[str, str] = {}
_KNOWN_PARAMS: dict[str, str] = {}
_PHRASES: dict[str, str] = {}


def configure_title_expansions(
    custom_expansions: dict | None,
    custom_phrase_expansions: dict | None = None,
) -> None:
    """Apply optional title/phrase expansion overrides from config.toml."""
    global _TITLE_EXPANSIONS, _PHRASE_EXPANSIONS

    expansions: dict[str, str] = {}
    if isinstance(custom_expansions, dict):
        for key, value in custom_expansions.items():
            if not isinstance(key, str) or not isinstance(value, str):
                continue
            k = key.strip().lower()
            v = value.strip()
            if not k or not v:
                continue
            expansions[k] = v

    _TITLE_EXPANSIONS = expansions
    phrase_expansions = {
        k: (v if v == v.upper() or v[0].isupper() and v[1:].isupper() else v.lower())
        for k, v in _TITLE_EXPANSIONS.items()
    }

    if isinstance(custom_phrase_expansions, dict):
        for key, value in custom_phrase_expansions.items():
            if not isinstance(key, str) or not isinstance(value, str):
                continue
            k = key.strip().lower()
            v = value.strip()
            if not k or not v:
                continue
            phrase_expansions[k] = v

    _PHRASE_EXPANSIONS = phrase_expansions


def configure_default_descriptions(
    custom_method_descriptions: dict | None,
    custom_param_descriptions: dict | None = None,
    custom_phrases: dict | None = None,
) -> None:
    """Apply optional method/parameter description overrides from config.toml."""
    global _KNOWN_METHODS, _KNOWN_PARAMS, _PHRASES

    method_descriptions: dict[str, str] = {}
    if isinstance(custom_method_descriptions, dict):
        for key, value in custom_method_descriptions.items():
            if not isinstance(key, str) or not isinstance(value, str):
                continue
            k = key.strip()
            v = value.strip()
            if not k or not v:
                continue
            method_descriptions[k] = v

    param_descriptions: dict[str, str] = {}
    if isinstance(custom_param_descriptions, dict):
        for key, value in custom_param_descriptions.items():
            if not isinstance(key, str) or not isinstance(value, str):
                continue
            k = key.strip()
            v = value.strip()
            if not k or not v:
                continue
            param_descriptions[k] = v

    _KNOWN_METHODS = method_descriptions
    _KNOWN_PARAMS = param_descriptions

    phrase_texts: dict[str, str] = {}
    if isinstance(custom_phrases, dict):
        for key, value in custom_phrases.items():
            if not isinstance(key, str) or not isinstance(value, str):
                continue
            k = key.strip()
            v = value.strip()
            if not k or not v:
                continue
            phrase_texts[k] = v
    _PHRASES = phrase_texts


def snake_to_title(name: str) -> str:
    """Convert a snake_case identifier to a Title Case heading string."""
    parts = name.lstrip("~").split("_")
    result = []
    for part in parts:
        if not part:
            continue
        expanded = _TITLE_EXPANSIONS.get(part.lower())
        result.append(expanded if expanded else part.capitalize())
    return " ".join(result)


def heading_to_anchor(heading: str) -> str:
    """Convert a markdown heading to its MkDocs anchor (lowercase, hyphens)."""
    anchor = heading.lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor.strip())
    return anchor


def method_heading(method_name: str) -> str:
    return snake_to_title(method_name)


def method_anchor(method_name: str) -> str:
    return heading_to_anchor(method_heading(method_name))


# ---------------------------------------------------------------------------
# Method description generation
# ---------------------------------------------------------------------------


def describe_method(name: str) -> str:
    """Return an auto-generated description for a method, or '' if unknown."""
    if name in _KNOWN_METHODS:
        return _KNOWN_METHODS[name]

    if name.startswith("get_"):
        template = _PHRASES.get("getter")
        noun_phrase = _noun_phrase(name[4:])
        if template and noun_phrase:
            return template.format(noun_phrase=noun_phrase)

    if name.startswith("set_"):
        template = _PHRASES.get("setter")
        noun_phrase = _noun_phrase(name[4:])
        if template and noun_phrase:
            return template.format(noun_phrase=noun_phrase)

    return ""


def _noun_phrase(name: str) -> str:
    """'obstacle_min_range_meters' → 'the obstacle min range meters'"""
    parts = name.split("_")
    expanded = [_PHRASE_EXPANSIONS.get(p.lower(), p) for p in parts if p]
    if not expanded:
        return ""

    base = " ".join(expanded)
    prefix = _PHRASES.get("noun_phrase_prefix", "")
    if not prefix:
        return base
    return f"{prefix} {base}".strip()


# ---------------------------------------------------------------------------
# Parameter description generation
# ---------------------------------------------------------------------------


def describe_param(param_name: str, param_type: str) -> str:
    """Return an auto-generated description for a parameter, or '' if unknown."""
    if param_name in _KNOWN_PARAMS:
        return _KNOWN_PARAMS[param_name]

    # shared_ptr<i_X> or shared_ptr<X> → "Shared pointer to the X."
    m = re.search(r"shared_ptr\s*<\s*([\w:]+)\s*>", param_type)
    if m:
        inner = m.group(1).split("::")[-1]  # strip namespace prefix
        display = inner.lstrip("i_") if inner.startswith("i_") else inner
        display = snake_to_title(display).lower()
        template = _PHRASES.get("shared_ptr_param")
        if template:
            return template.format(type=display)

    # Generic fallback: "The update rate." from param name "update_rate"
    words = [_PHRASE_EXPANSIONS.get(p.lower(), p) for p in param_name.split("_") if p]
    if words:
        template = _PHRASES.get("generic_param")
        if template:
            return template.format(words=" ".join(words), param=param_name)

    return ""


# ---------------------------------------------------------------------------
# Constructor description / heading
# ---------------------------------------------------------------------------


def constructor_heading(params: list) -> str:
    if not params:
        return _PHRASES.get("constructor_heading_default", "")
    return _PHRASES.get("constructor_heading", "")


def _article(word: str) -> str:
    """Return the configured article form for vowel/consonant leading words."""
    if not word:
        return ""
    vowel = _PHRASES.get("article_vowel", "")
    consonant = _PHRASES.get("article_consonant", "")
    return vowel if word[0].lower() in "aeiou" else consonant


def constructor_description(class_name: str, params: list) -> str:
    display = snake_to_title(class_name).lower()
    art = _article(display)
    template_key = (
        "constructor_description_default"
        if not params
        else "constructor_description_with_params"
    )
    template = _PHRASES.get(template_key)
    if not template:
        return ""
    if not params:
        return template.format(article=art, display=display)
    return template.format(article=art, display=display)
