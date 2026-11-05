#!/usr/bin/env python3
"""Apply the bounded search-asset fix for the pinned Windows Verso checkout.

The patch is deliberately not a general dependency editor. Only the pinned
revision, fixed source path, and exact original/already-patched blocks below
are accepted. Linux/macOS builds are unchanged. Re-running after ``lake update``
is safe; an unfamiliar revision or source layout requires a fresh review.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import sys


ROOT = Path(__file__).absolute().parents[1]
VERSO_REV = "36664a0ebe032ef3f9e72a8ed0d7be9b14af17d2"
VERSO_URL = "https://github.com/leanprover/verso"
TARGET = Path(".lake/packages/verso/src/verso-search/VersoSearch/DomainSearch.lean")
ORIGINAL = r'''public def searchBoxCode : Array (String × ByteArray) :=
  (include_bin_dir "../../../static-web/search").filterMap fun (name, contents) =>
    if name.endsWith "domain-mappers.js" then none
    else some (name.dropPrefix "../../../static-web/search/" |>.copy, contents)'''
PATCHED = r'''public def searchBoxCode : Array (String × ByteArray) :=
  (include_bin_dir "../../../static-web/search").filterMap fun (name, contents) =>
    let name := name.replace "\\" "/"
    if name.endsWith "domain-mappers.js" then none
    else some (name.dropPrefix "../../../static-web/search/" |>.copy, contents)'''


class CompatibilityError(RuntimeError):
    """An unknown or unsafe dependency layout; no patch is applied."""


def _plain_path(path: Path) -> None:
    """Reject symlinks and all Windows reparse-point types along a path."""
    for component in reversed((path, *path.parents)):
        try:
            metadata = component.lstat()
        except OSError as exc:
            raise CompatibilityError("Required repository/dependency path is missing.") from exc
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if stat.S_ISLNK(metadata.st_mode) or (
            getattr(metadata, "st_file_attributes", 0) & reparse_flag
        ):
            raise CompatibilityError("Refusing a symlink or reparse-point path.")


def _checked_file(root: Path, relative: Path) -> Path:
    if relative.is_absolute() or ".." in relative.parts:
        raise CompatibilityError("Only fixed repository-relative paths are allowed.")
    candidate = root / relative
    _plain_path(candidate)
    try:
        candidate.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise CompatibilityError("Dependency path escapes the repository.") from exc
    if not candidate.is_file():
        raise CompatibilityError("Expected a regular repository/dependency file.")
    return candidate


def _check_pin(root: Path) -> None:
    manifest = _checked_file(root, Path("lake-manifest.json"))
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        packages = [p for p in data["packages"] if p["name"] == "verso"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise CompatibilityError("Cannot validate the pinned Verso manifest.") from exc
    if (
        data.get("packagesDir") != ".lake/packages"
        or len(packages) != 1
        or packages[0].get("rev") != VERSO_REV
        or packages[0].get("url") != VERSO_URL
        or packages[0].get("type") != "git"
        or packages[0].get("subDir") is not None
    ):
        raise CompatibilityError("Unsupported Verso pin or package location; review required.")


def apply_compat(repo_root: Path, *, platform: str | None = None) -> str:
    """Return ``applied``, ``already-applied``, or ``not-windows``.

    ``platform`` is an in-process test seam, not a CLI override. A normal build
    can only apply this compatibility change on Windows.
    """
    if (sys.platform if platform is None else platform) != "win32":
        return "not-windows"
    root = Path(os.path.abspath(repo_root))
    _plain_path(root)
    if not root.is_dir():
        raise CompatibilityError("Repository root is not a directory.")
    _check_pin(root)
    target = _checked_file(root, TARGET)
    try:
        before = target.read_bytes()
        source = before.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise CompatibilityError("Cannot read the pinned Verso source.") from exc
    newline = "\r\n" if "\r\n" in source else "\n"
    normalized = source.replace("\r\n", "\n")
    if normalized.count("public def searchBoxCode :") != 1:
        raise CompatibilityError("Unknown or ambiguous searchBoxCode declaration.")
    if normalized.count(PATCHED) == 1 and ORIGINAL not in normalized:
        return "already-applied"
    if normalized.count(ORIGINAL) != 1 or PATCHED in normalized:
        raise CompatibilityError("Unknown searchBoxCode pattern; review required.")
    original_block = ORIGINAL.replace("\n", newline)
    if source.count(original_block) != 1:
        raise CompatibilityError("Unknown searchBoxCode line endings; review required.")
    replacement = source.replace(original_block, PATCHED.replace("\n", newline), 1)
    # Recheck immediately before the only write. Do not follow a newly linked
    # dependency directory or overwrite a concurrently edited source file.
    _checked_file(root, TARGET)
    if target.read_bytes() != before:
        raise CompatibilityError("Verso source changed during compatibility validation.")
    target.write_bytes(replacement.encode("utf-8"))
    return "applied"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        outcome = apply_compat(args.repo_root)
    except (CompatibilityError, OSError) as exc:
        # Never print a local absolute path (including OS exception text).
        message = str(exc) if isinstance(exc, CompatibilityError) else "Compatibility file operation failed."
        print(f"Verso Windows compatibility: FAIL: {message}", file=sys.stderr)
        return 1
    print(f"Verso Windows compatibility: {outcome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
