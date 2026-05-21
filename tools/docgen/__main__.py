"""docgen — C++ header → MkDocs markdown generator.

Usage (from the wiki project root):

    # Regenerate ALL docs:
    python -m tools.docgen

    # Regenerate one or more specific headers:
    python -m tools.docgen path/to/include/foo.h path/to/include/bar.h

    # Preview without writing (dry-run):
    python -m tools.docgen --dry-run

    # Use a custom config file:
    python -m tools.docgen --config tools/config.toml
"""

import argparse
import sys
import tomllib
from pathlib import Path

import jinja2

from . import conventions as conv
from .parser import parse_header
from .paths import build_doc_index, include_to_doc_path
from .renderer import (
    load_overrides,
    render_header,
    render_namespace_index_pages,
    render_namespaces_index,
    _make_jinja_env,
)

# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------


def _load_config(config_path: Path) -> tuple[Path, Path, dict]:
    with open(config_path, "rb") as f:
        cfg = tomllib.load(f)

    root = Path.cwd()  # always run from the wiki project root
    include_root = (root / cfg["paths"]["include_root"]).resolve()
    docs_root = (root / cfg["paths"]["docs_root"]).resolve()
    return include_root, docs_root, cfg


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m tools.docgen",
        description="Generate MkDocs markdown from C++ header files.",
    )
    parser.add_argument(
        "headers",
        nargs="*",
        help="Specific header files to process. Omit to process all headers.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated docs to stdout instead of writing files.",
    )
    parser.add_argument(
        "--config",
        default="tools/config.toml",
        help="Path to config.toml (default: tools/config.toml)",
    )
    parser.add_argument(
        "--overrides",
        default="tools/overrides.toml",
        help="Path to overrides.toml (default: tools/overrides.toml)",
        # Copy tools/docgen/overrides.toml.example → tools/overrides.toml to get started.
    )
    args = parser.parse_args(argv)

    config_path = Path(args.config)
    try:
        include_root, docs_root, cfg = _load_config(config_path)
    except Exception as e:
        print(f"ERROR loading config: {e}", file=sys.stderr)
        return 1

    if not include_root.exists():
        print(f"ERROR: include_root not found: {include_root}", file=sys.stderr)
        print("       Check [paths].include_root in config.toml", file=sys.stderr)
        return 1

    naming_cfg = cfg.get("naming", {}) if isinstance(cfg, dict) else {}
    title_expansions = (
        naming_cfg.get("title_expansions", {}) if isinstance(naming_cfg, dict) else {}
    )
    phrase_expansions = (
        naming_cfg.get("phrase_expansions", {}) if isinstance(naming_cfg, dict) else {}
    )
    conv.configure_title_expansions(title_expansions, phrase_expansions)

    descriptions_cfg = cfg.get("descriptions", {}) if isinstance(cfg, dict) else {}
    phrases_cfg = cfg.get("phrases", {}) if isinstance(cfg, dict) else {}
    method_descriptions = (
        descriptions_cfg.get("methods", {})
        if isinstance(descriptions_cfg, dict)
        else {}
    )
    param_descriptions = (
        descriptions_cfg.get("params", {})
        if isinstance(descriptions_cfg, dict)
        else {}
    )
    conv.configure_default_descriptions(
        method_descriptions,
        param_descriptions,
        phrases_cfg if isinstance(phrases_cfg, dict) else {},
    )

    overrides = load_overrides(Path(args.overrides))

    templates_dir = Path(__file__).parent / "templates"
    env = _make_jinja_env(templates_dir)

    # Collect headers to process
    if args.headers:
        header_files = [Path(h).resolve() for h in args.headers]
    else:
        header_files = sorted(include_root.rglob("*.h"))

    if not header_files:
        print("No header files found.", file=sys.stderr)
        return 1

    # Phase 1: parse all headers to build cross-reference index
    parsed_index: dict[str, object] = {}  # class_name → ParsedHeader
    all_parsed = []
    for h in header_files:
        result = parse_header(h)
        if result is None:
            print(f"  SKIP  {h.name}  (could not parse)", file=sys.stderr)
            continue
        all_parsed.append(result)
        if result.entity and hasattr(result.entity, "name"):
            parsed_index[result.entity.name] = result

    doc_index = build_doc_index(
        [p.path for p in all_parsed],
        include_root=include_root,
        docs_root=docs_root,
    )

    index_doc_path, index_content = render_namespaces_index(
        parsed_headers=all_parsed,
        include_root=include_root,
        docs_root=docs_root,
        doc_index=doc_index,
        parsed_index=parsed_index,
        env=env,
    )
    namespace_index_pages = render_namespace_index_pages(
        parsed_headers=all_parsed,
        docs_root=docs_root,
        doc_index=doc_index,
        overrides=overrides,
        env=env,
    )

    expected_output_paths: set[Path] = {
        include_to_doc_path(p.path, include_root, docs_root) for p in all_parsed
    }
    expected_output_paths.add(index_doc_path)
    expected_output_paths.update(page_path for page_path, _ in namespace_index_pages)

    # Phase 2: render and write (or print)
    written = 0
    errors = 0
    for parsed in all_parsed:
        try:
            doc_path, content = render_header(
                parsed=parsed,
                include_root=include_root,
                docs_root=docs_root,
                doc_index=doc_index,
                parsed_index=parsed_index,
                overrides=overrides,
                env=env,
            )
        except Exception as e:
            print(f"  ERROR {parsed.path.name}: {e}", file=sys.stderr)
            errors += 1
            continue

        if args.dry_run:
            print(f'\n{"=" * 72}')
            print(f"# {doc_path}")
            print("=" * 72)
            print(content)
        else:
            doc_path.parent.mkdir(parents=True, exist_ok=True)
            doc_path.write_text(content, encoding="utf-8")
            print(f"  WROTE {doc_path.relative_to(docs_root)}")
            written += 1

    if args.dry_run:
        print(f'\n{"=" * 72}')
        print(f"# {index_doc_path}")
        print("=" * 72)
        print(index_content)
        for page_path, page_content in namespace_index_pages:
            print(f'\n{"=" * 72}')
            print(f"# {page_path}")
            print("=" * 72)
            print(page_content)
    else:
        # Full regeneration mode is authoritative: remove stale generated markdown files first.
        if not args.headers:
            expected_resolved = {x.resolve() for x in expected_output_paths}
            stale_files = [
                p
                for p in docs_root.rglob("*.md")
                if p.resolve() not in expected_resolved
            ]
            for stale in stale_files:
                stale.unlink()
                print(f"  DELETED {stale.relative_to(docs_root)}")

        index_doc_path.parent.mkdir(parents=True, exist_ok=True)
        index_doc_path.write_text(index_content, encoding="utf-8")
        print(f"  WROTE {index_doc_path.relative_to(docs_root)}")
        written += 1

        for page_path, page_content in namespace_index_pages:
            page_path.parent.mkdir(parents=True, exist_ok=True)
            page_path.write_text(page_content, encoding="utf-8")
            print(f"  WROTE {page_path.relative_to(docs_root)}")
            written += 1

    if not args.dry_run:
        print(f"\nDone: {written} file(s) written, {errors} error(s).")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
