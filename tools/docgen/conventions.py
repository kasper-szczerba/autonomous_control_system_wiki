"""Naming convention rules for auto-generating descriptions from identifiers."""

import re

# Words that get special Title-Case treatment in headings
_TITLE_EXPANSIONS: dict[str, str] = {
    'ptr':   'Pointer',
    'ref':   'Reference',
    'fps':   'FPS',
    'toml':  'TOML',
    'gpu':   'GPU',
    'cpu':   'CPU',
    'id':    'ID',
    'url':   'URL',
    'api':   'API',
    'ui':    'UI',
    'zed':   'ZED',
    'sl':    'SL',
    'cv':    'CV',
}

# Same expansions for noun-phrase descriptions (lowercase unless acronym)
_PHRASE_EXPANSIONS: dict[str, str] = {
    k: (v if v == v.upper() or v[0].isupper() and v[1:].isupper() else v.lower())
    for k, v in _TITLE_EXPANSIONS.items()
}
_PHRASE_EXPANSIONS.update({
    'fps': 'FPS', 'toml': 'TOML', 'gpu': 'GPU', 'cpu': 'CPU',
    'id': 'ID', 'url': 'URL', 'api': 'API', 'ui': 'UI',
    'zed': 'ZED', 'ptr': 'pointer', 'ref': 'reference',
})


def snake_to_title(name: str) -> str:
    """Convert a snake_case identifier to a Title Case heading string."""
    parts = name.lstrip('~').split('_')
    result = []
    for part in parts:
        if not part:
            continue
        expanded = _TITLE_EXPANSIONS.get(part.lower())
        result.append(expanded if expanded else part.capitalize())
    return ' '.join(result)


def heading_to_anchor(heading: str) -> str:
    """Convert a markdown heading to its MkDocs anchor (lowercase, hyphens)."""
    anchor = heading.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor.strip())
    return anchor


def method_heading(method_name: str) -> str:
    return snake_to_title(method_name)


def method_anchor(method_name: str) -> str:
    return heading_to_anchor(method_heading(method_name))


# ---------------------------------------------------------------------------
# Method description generation
# ---------------------------------------------------------------------------

_KNOWN_METHODS: dict[str, str] = {
    'setup':                   'Initializes the component.',
    'teardown':                'Cleans up the component before destruction.',
    'update':                  'Performs one update cycle.',
    'on_setup':                'Called during the setup phase.',
    'on_teardown':             'Called during the teardown phase.',
    'on_update':               'Performs the update logic.',
    'begin':                   'Starts the component thread.',
    'end':                     'Stops the component thread and waits for it to finish.',
    'cancel_begin':            'Cancels a pending begin operation.',
    'parse':                   'Parses the configuration file.',
    'free':                    'Releases the parsed configuration data.',
    'on_initialize':           'Called during initialization.',
    'on_shutdown':             'Called during shutdown.',
    # get_is_* — these are phrased as bool predicates
    'get_is_setup_completed':  'Returns whether the setup process has been completed.',
    'get_is_running':          'Returns whether the component is running.',
    'get_is_opened':           'Returns whether the camera is opened.',
    'get_is_floor_detected':   'Returns whether a floor has been detected.',
    'get_is_begin_canceled':   'Returns whether a pending begin has been cancelled.',
}


def describe_method(name: str) -> str:
    """Return an auto-generated description for a method, or '' if unknown."""
    if name in _KNOWN_METHODS:
        return _KNOWN_METHODS[name]

    if name.startswith('get_'):
        return f'Returns {_noun_phrase(name[4:])}.'

    if name.startswith('set_'):
        return f'Sets {_noun_phrase(name[4:])}.'

    return ''


def _noun_phrase(name: str) -> str:
    """'obstacle_min_range_meters' → 'the obstacle min range meters'"""
    parts = name.split('_')
    expanded = [_PHRASE_EXPANSIONS.get(p.lower(), p) for p in parts if p]
    return 'the ' + ' '.join(expanded)


# ---------------------------------------------------------------------------
# Parameter description generation
# ---------------------------------------------------------------------------

_KNOWN_PARAMS: dict[str, str] = {
    'name':           'The name of the component.',
    'toml_reader_ptr':'A shared pointer to a TOML reader for configuration.',
}


def describe_param(param_name: str, param_type: str) -> str:
    """Return an auto-generated description for a parameter, or '' if unknown."""
    if param_name in _KNOWN_PARAMS:
        return _KNOWN_PARAMS[param_name]

    # shared_ptr<i_X> or shared_ptr<X> → "Shared pointer to the X."
    m = re.search(r'shared_ptr\s*<\s*([\w:]+)\s*>', param_type)
    if m:
        inner = m.group(1).split('::')[-1]         # strip namespace prefix
        display = inner.lstrip('i_') if inner.startswith('i_') else inner
        display = snake_to_title(display).lower()
        return f'Shared pointer to the {display}.'

    # Generic fallback: "The update rate." from param name "update_rate"
    words = [_PHRASE_EXPANSIONS.get(p.lower(), p) for p in param_name.split('_') if p]
    if words:
        return 'The ' + ' '.join(words) + '.'

    return ''


# ---------------------------------------------------------------------------
# Constructor description / heading
# ---------------------------------------------------------------------------

def constructor_heading(params: list) -> str:
    return 'Default Constructor' if not params else 'Constructor'


def _article(word: str) -> str:
    """Return 'an' before vowel sounds, otherwise 'a'."""
    return 'an' if word and word[0].lower() in 'aeiou' else 'a'


def constructor_description(class_name: str, params: list) -> str:
    display = snake_to_title(class_name).lower()
    art = _article(display)
    if not params:
        return f'Creates {art} {display} with its default configuration.'
    return f'Creates {art} {display} with the specified name.'
