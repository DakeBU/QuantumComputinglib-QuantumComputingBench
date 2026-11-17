#!/usr/bin/env python3
"""Normalize Blueprint source locations before publishing the generated site."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


TEXT_OUTPUT_SUFFIXES = {".css", ".html", ".js", ".json", ".map", ".svg"}
ABSOLUTE_PATH_RE = re.compile(
    r"(?i)"
    r"(?:file:///[^\s\"'<>]+"
    # Require two path components after a drive letter.  A single ``x:\foo``
    # shape also occurs naturally in rendered mathematics such as
    # ``x:\mathcal V(x)`` and must not be mistaken for a filesystem path.
    r"|(?<![A-Za-z0-9_])[A-Z]:[\\/][^\\/\s\"'<>]+[\\/][^\s\"'<>]+"
    r"|(?<![A-Za-z0-9_])/(?:home|Users|root)/[^\s\"'<>]+)"
)
WEB_URL_RE = re.compile(r"https?://[^\s\"'<>]+", flags=re.IGNORECASE)
MATHJAX_REGION_RE = re.compile(
    r"\\\[(?:.|\n)*?\\\]|\\\((?:.|\n)*?\\\)",
)
PORTABLE_PATH_RE = re.compile(
    r"[A-Za-z0-9_. -]+(?:[\\/][A-Za-z0-9_. -]+)+"
    r"(?:(?:#|\?)[^\s\"'<>]*)?"
)
# Pinned Verso's `xref`/`emitFindHtml` embeds xref.json immediately before
# static-web/find.js. Match that exact boundary, not arbitrary JavaScript.
FIND_XREF_ASSIGNMENT_RE = re.compile(r"<script>\s*window\.xref = ")
FIND_XREF_DRIVER_PREFIX = (
    ";\n/**\n"
    " * Copyright (c) 2024 Lean FRO LLC. All rights reserved.\n"
    " * Released under Apache 2.0 license as described in the file LICENSE.\n"
    " * Author: David Thrane Christiansen\n"
    " */\n\n// Enable typescript\n// @ts-check\n"
)


def _is_absolute(path: str) -> bool:
    return PurePosixPath(path).is_absolute() or PureWindowsPath(path).is_absolute()


def _relative_source_path(source_path: str, repo_root: Path) -> str:
    """Return a portable repository-relative source path.

    Verso records the source file supplied by Lean.  On some platforms that is
    an absolute path, so strip the current repository root without ever baking
    that root into a tracked file.  Absolute paths outside the repository are
    rejected rather than published.
    """

    normalized = source_path.replace("\\", "/")
    normalized_root = str(repo_root).replace("\\", "/").rstrip("/")

    # Windows drive paths are case-insensitive.  Using casefold for the prefix
    # comparison is harmless for the repository root on the other platforms.
    prefix = normalized_root + "/"
    if normalized.casefold().startswith(prefix.casefold()):
        relative = normalized[len(prefix) :]
    elif normalized.casefold() == normalized_root.casefold():
        raise ValueError("a Blueprint source path resolves to the repository root")
    elif _is_absolute(normalized) or normalized.startswith("file://"):
        raise ValueError("a Blueprint source path points outside the repository")
    else:
        relative = normalized

    portable = PurePosixPath(relative)
    if portable.is_absolute() or ".." in portable.parts:
        raise ValueError("a Blueprint source path is not repository-relative")
    return portable.as_posix()


def _normalize_source_paths(value: Any, repo_root: Path) -> tuple[Any, int, int]:
    """Normalize every structured ``sourcePath`` field in a JSON value."""

    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        changed = 0
        seen = 0
        for key, child in value.items():
            if key == "sourcePath":
                if not isinstance(child, str):
                    raise TypeError("Blueprint sourcePath must be a string")
                replacement = _relative_source_path(child, repo_root)
                normalized[key] = replacement
                changed += int(replacement != child)
                seen += 1
            else:
                replacement, child_changed, child_seen = _normalize_source_paths(
                    child, repo_root
                )
                normalized[key] = replacement
                changed += child_changed
                seen += child_seen
        return normalized, changed, seen

    if isinstance(value, list):
        normalized_items: list[Any] = []
        changed = 0
        seen = 0
        for child in value:
            replacement, child_changed, child_seen = _normalize_source_paths(
                child, repo_root
            )
            normalized_items.append(replacement)
            changed += child_changed
            seen += child_seen
        return normalized_items, changed, seen

    return value, 0, 0


def _scrub_local_paths_from_text(
    text: str, repo_root: Path
) -> tuple[str, int]:
    """Make embedded local paths portable without exposing their values."""

    scrubbed = text
    changed = 0
    roots = {
        str(repo_root).replace("\\", "/").rstrip("/"),
        str(repo_root).replace("/", "\\").rstrip("\\"),
    }
    for root in roots:
        if not root:
            continue
        with_separator = re.compile(
            re.escape(root) + r"[\\/]", flags=re.IGNORECASE
        )
        scrubbed, replacements = with_separator.subn("", scrubbed)
        changed += replacements
        exact_root = re.compile(re.escape(root), flags=re.IGNORECASE)
        scrubbed, replacements = exact_root.subn(
            "repository-root", scrubbed
        )
        changed += replacements

    scrubbed, replacements = ABSOLUTE_PATH_RE.subn(
        "external-source", scrubbed
    )
    changed += replacements

    # Verso can append Lean's Windows source spelling to an otherwise valid
    # GitHub blob URL.  After removing the repository root, canonicalize only
    # URL/path-shaped values; do not rewrite backslashes in rendered Lean code.
    url_separator_replacements = 0

    def normalize_web_url(match: re.Match[str]) -> str:
        nonlocal url_separator_replacements
        value = match.group(0)
        url_separator_replacements += value.count("\\")
        return value.replace("\\", "/")

    scrubbed = WEB_URL_RE.sub(normalize_web_url, scrubbed)
    changed += url_separator_replacements
    if PORTABLE_PATH_RE.fullmatch(scrubbed):
        separator_replacements = scrubbed.count("\\")
        scrubbed = scrubbed.replace("\\", "/")
        changed += separator_replacements
    return scrubbed, changed


def _scrub_json_strings(value: Any, repo_root: Path) -> tuple[Any, int]:
    """Scrub local paths inside every JSON string, including cached HTML."""

    if isinstance(value, dict):
        scrubbed: dict[str, Any] = {}
        changed = 0
        for key, child in value.items():
            replacement, child_changed = _scrub_json_strings(
                child, repo_root
            )
            scrubbed[key] = replacement
            changed += child_changed
        return scrubbed, changed
    if isinstance(value, list):
        scrubbed_items: list[Any] = []
        changed = 0
        for child in value:
            replacement, child_changed = _scrub_json_strings(
                child, repo_root
            )
            scrubbed_items.append(replacement)
            changed += child_changed
        return scrubbed_items, changed
    if isinstance(value, str):
        return _scrub_local_paths_from_text(value, repo_root)
    return value, 0


def _script_safe_json(value: Any) -> str:
    """Serialize data without allowing cached HTML to terminate its script."""

    serialized = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    for character, escaped in (
        ("<", r"\u003c"), (">", r"\u003e"), ("&", r"\u0026"),
        ("\u2028", r"\u2028"), ("\u2029", r"\u2029"),
    ):
        serialized = serialized.replace(character, escaped)
    return serialized


def _rewrite_find_xref(
    find_path: Path, normalized_xref: Any, repo_root: Path
) -> tuple[int, int]:
    """Restore the inline copy from the same build's canonical xref.json.

    A text regex must never scrub serialized JSON: JSON-escaped Windows
    separators differ from source paths, and a trailing `\\` can be the escape
    of an HTML attribute quote. The previous text pass both missed the root
    and damaged that quote in find/index.html. Re-embedding the complete,
    structured, normalized xref retains every entry, cached HTML field, and
    source anchor; it also repairs output already touched by that old pass.

    Unknown or ambiguous script layouts fail closed. Only the exact generated
    assignment is replaced; the page shell and find.js driver are preserved.
    """

    if not find_path.is_file():
        raise FileNotFoundError("generated Blueprint find/index.html was not found")
    text = find_path.read_text(encoding="utf-8")
    starts = list(FIND_XREF_ASSIGNMENT_RE.finditer(text))
    if len(starts) != 1 or text.count(FIND_XREF_DRIVER_PREFIX) != 1:
        raise ValueError("unknown or ambiguous Blueprint inline xref layout")
    start = starts[0].end()
    end = text.index(FIND_XREF_DRIVER_PREFIX)
    if end <= start:
        raise ValueError("invalid Blueprint inline xref boundaries")
    prefix, prefix_changed = _scrub_local_paths_from_text(text[:start], repo_root)
    suffix, suffix_changed = _scrub_local_paths_from_text(text[end:], repo_root)
    replacement = prefix + _script_safe_json(normalized_xref) + suffix
    changed = int(replacement != text)
    if changed:
        find_path.write_text(replacement, encoding="utf-8", newline="\n")
    return changed, changed + prefix_changed + suffix_changed


def _scrub_output_text_files(
    output_root: Path, repo_root: Path, skipped: set[Path]
) -> tuple[int, int]:
    files_changed = 0
    replacements = 0
    skipped_resolved = {path.resolve() for path in skipped}
    for path in output_root.rglob("*"):
        if (
            not path.is_file()
            or path.suffix.lower() not in TEXT_OUTPUT_SUFFIXES
            or path.resolve() in skipped_resolved
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        scrubbed, changed = _scrub_local_paths_from_text(text, repo_root)
        if changed:
            path.write_text(
                scrubbed, encoding="utf-8", errors="strict", newline="\n"
            )
            files_changed += 1
            replacements += changed
    return files_changed, replacements


def _assert_no_local_paths(output_root: Path, repo_root: Path) -> int:
    """Reject local filesystem paths without printing the sensitive values."""

    repo_spellings = {
        str(repo_root).replace("\\", "/").casefold(),
        str(repo_root).replace("/", "\\").casefold(),
    }
    checked = 0
    leaking_files = 0
    for path in output_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_OUTPUT_SUFFIXES:
            continue
        checked += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        folded = text.casefold()
        if any(spelling and spelling in folded for spelling in repo_spellings):
            leaking_files += 1
            continue
        # TeX such as ``I:\quad\mathrm{toggle}`` resembles a Windows drive
        # path. Repository-root checks above still inspect the complete file;
        # only the generic path heuristic skips rendered mathematics.
        non_math_text = MATHJAX_REGION_RE.sub("", text)
        if ABSOLUTE_PATH_RE.search(non_math_text):
            leaking_files += 1

    if leaking_files:
        raise ValueError(
            "generated Blueprint output contains local filesystem paths "
            f"in {leaking_files} text files"
        )
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Make generated Blueprint source locations repository-relative."
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="_out/blueprint",
        help="Blueprint output directory (default: _out/blueprint)",
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="scan an assembled static site without requiring Blueprint xref.json",
    )
    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    changed = 0
    seen = 0
    embedded_changed = 0
    find_files_changed = 0
    skipped: set[Path] = set()
    if not args.scan_only:
        xref_path = Path(args.output) / "html-multi" / "xref.json"
        if not xref_path.is_file():
            raise FileNotFoundError("generated Blueprint xref.json was not found")

        data = json.loads(xref_path.read_text(encoding="utf-8"))
        normalized, changed, seen = _normalize_source_paths(data, repo_root)
        normalized, embedded_changed = _scrub_json_strings(
            normalized, repo_root
        )

        xref_path.write_text(
            json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        skipped.add(xref_path)
        find_path = xref_path.parent / "find" / "index.html"
        find_files_changed, find_replacements = _rewrite_find_xref(
            find_path, normalized, repo_root
        )
        embedded_changed += find_replacements
        # Its JSON has already been sanitized structurally. A later text pass
        # would corrupt escaped quotes even when every source URL is portable.
        skipped.add(find_path)
    files_changed = 0
    text_replacements = 0
    if not args.scan_only:
        files_changed, text_replacements = _scrub_output_text_files(
            Path(args.output), repo_root, skipped
        )
        files_changed += find_files_changed
    checked = _assert_no_local_paths(Path(args.output), repo_root)
    if args.scan_only:
        print(
            f"Checked {checked} publication text files for local-path leakage."
        )
    else:
        print(
            f"Normalized {changed} of {seen} Blueprint source paths; "
            f"scrubbed {embedded_changed + text_replacements} embedded paths "
            f"across {files_changed} text files; checked {checked} generated "
            "text files for local-path leakage."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
