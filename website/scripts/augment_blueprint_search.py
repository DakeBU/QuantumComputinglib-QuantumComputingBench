#!/usr/bin/env python3
"""Register compiled Blueprint declarations through Verso's DomainMapper API.

The pinned renderer emits informal cross-reference domains but only registers
the standard Manual domains for quick-jump search. This deterministic adapter
uses the existing LeanCodePreview target, page and anchor; it neither changes
the search implementation nor adds HTML or proof/certification metadata.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote

DOMAIN = "«Informal.LeanCodePreview»"
PREFIX = "Informal.LeanCodePreview."
ADAPTER = "blueprint-declarations.js"
BEGIN = "// BEGIN ASPBE BLUEPRINT DECLARATION SEARCH"
END = "// END ASPBE BLUEPRINT DECLARATION SEARCH"
SEARCH_IMPORT = 'import { domainMappers } from "./domain-mappers.js";'
SEARCH_IMPORT_433 = 'import { domainMappers, searchPriorities } from "./domain-mappers.js";'
REQUIRED_DECLARATIONS = {"QuantumBlockEncoding.HermiteStatePreparation.hermiteStatePreparation_complete"}


class SearchContractError(ValueError):
    """Required emitted search structure is absent or inconsistent."""


def required_text(root: Path, relative: str) -> str:
    file = root / relative
    if not file.is_file() or not file.stat().st_size:
        raise SearchContractError(f"Missing nonempty Blueprint asset: {relative}")
    try:
        file.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise SearchContractError("Blueprint asset escapes the output tree") from error
    return file.read_text(encoding="utf-8")


def original_registry(source: str) -> str:
    """Remove only our complete trailing block; reject an upstream shape change."""
    if BEGIN in source or END in source:
        if source.count(BEGIN) != 1 or source.count(END) != 1:
            raise SearchContractError("Malformed Blueprint search adapter markers")
        start = source.index(BEGIN)
        end = source.index(END)
        if end < start or source[end + len(END):].strip():
            raise SearchContractError("Blueprint search adapter must be the trailing block")
        source = source[:start]
    if len(re.findall(r"export\s+const\s+domainMappers\s*=\s*\{", source)) != 1:
        raise SearchContractError("Unsupported Verso domain mapper export")
    if DOMAIN in source:
        raise SearchContractError("Renderer already registers Blueprint declarations; review adapter")
    if not source.rstrip().endswith("};"):
        raise SearchContractError("Unsupported Verso domain mapper terminator")
    return source.rstrip() + "\n"


def validate_search_initialization(source: str) -> None:
    """Accept only the two inspected Verso call shapes, preserving priorities."""
    compact = re.sub(r"\s+", "", source)
    contracts = (
        (SEARCH_IMPORT, "registerSearch({searchWrapper,data,domainMappers})"),
        (SEARCH_IMPORT_433,
         "registerSearch({searchWrapper,data,domainMappers,searchPriorities,"
         "docPriorities,searchPagePath,})"),
    )
    imports = re.findall(
        r'import\s*\{[^}]+\}\s*from\s*"\./domain-mappers\.js";', source
    )
    if len(imports) != 1 or compact.count("registerSearch({") != 1:
        raise SearchContractError("Unsupported Verso search initialization contract")
    if not any(source.count(statement) == 1 and compact.count(call) == 1
               for statement, call in contracts):
        raise SearchContractError("Unsupported Verso search initialization contract")


def declaration_entries(root: Path, xref: object) -> list[dict[str, str]]:
    if not isinstance(xref, dict) or not isinstance(xref.get(DOMAIN), dict):
        raise SearchContractError("Missing Blueprint LeanCodePreview domain")
    contents = xref[DOMAIN].get("contents")
    if not isinstance(contents, dict) or not contents:
        raise SearchContractError("Empty or malformed Blueprint declaration domain")
    pages: dict[str, str] = {}
    entries: dict[str, dict[str, str]] = {}
    for key, values in sorted(contents.items()):
        if not isinstance(key, str) or not key.startswith(PREFIX) or not isinstance(values, list) or not values:
            raise SearchContractError("Malformed Blueprint declaration entry")
        for value in values:
            if not isinstance(value, dict) or not isinstance(value.get("data"), dict):
                raise SearchContractError("Missing Blueprint declaration data")
            name = value["data"].get("target")
            address, anchor = value.get("address"), value.get("id")
            if not isinstance(name, str) or not name or key != PREFIX + name:
                raise SearchContractError("Blueprint declaration target disagrees with its key")
            if any(ord(char) < 32 for char in name) or any(char in name for char in "/\\:"):
                raise SearchContractError("Unsafe Blueprint declaration name")
            if not isinstance(address, str) or not address.startswith("/") or address.startswith("//"):
                raise SearchContractError("Blueprint declaration address must be book-relative")
            decoded = unquote(address)
            if any(char in decoded for char in "\\:#?\x00") or ".." in decoded.split("/"):
                raise SearchContractError("Unsafe Blueprint declaration address")
            relative = str(PurePosixPath(decoded.lstrip("/")))
            if not relative.endswith(".html"):
                relative = relative.rstrip("/") + "/index.html"
            if not isinstance(anchor, str) or not anchor or any(ord(char) < 32 for char in anchor):
                raise SearchContractError("Missing or unsafe Blueprint declaration anchor")
            if relative not in pages:
                pages[relative] = required_text(root, relative)
            escaped = html.escape(anchor, quote=True)
            if f'id="{escaped}"' not in pages[relative] and f"id='{escaped}'" not in pages[relative]:
                raise SearchContractError("Blueprint declaration anchor is absent from its page")
            entry = {"searchKey": name, "address": address + "#" + anchor, "domainId": DOMAIN, "ref": name}
            # The same declaration can be rendered repeatedly; choose a stable
            # canonical destination, and do not also register its preview domains.
            if name not in entries or entry["address"] < entries[name]["address"]:
                entries[name] = entry
    return [entries[name] for name in sorted(entries)]


def expected_assets(root: Path) -> tuple[dict[str, str], int]:
    try:
        xref = json.loads(required_text(root, "xref.json"))
    except json.JSONDecodeError as error:
        raise SearchContractError("Malformed Blueprint cross-reference JSON") from error
    entries = declaration_entries(root, xref)
    if not REQUIRED_DECLARATIONS.issubset({entry["searchKey"] for entry in entries}):
        raise SearchContractError("Required Hermite root is missing from Blueprint search entries")
    registry = original_registry(required_text(root, "-verso-search/domain-mappers.js"))
    init = required_text(root, "-verso-search/search-init.js")
    validate_search_initialization(init)
    search_box = required_text(root, "-verso-search/search-box.js")
    if "domainMappers[key].dataToSearchables(value)" not in search_box:
        raise SearchContractError("Unsupported Verso DomainMapper consumer")
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    adapter = (
        "// Generated from verified local Blueprint xref entries; do not edit.\n"
        "// Uses the public Verso Search DomainMapper contract, not an HTML injection.\n"
        f"const entries = {payload};\n"
        "export const blueprintDeclarationMapper = {\n"
        '  displayName: "Lean declaration",\n'
        '  className: "doc-domain",\n'
        "  dataToSearchables: (_domainData) => entries,\n"
        "};\n"
    )
    registry += (
        "\n" + BEGIN + "\n"
        f'import {{ blueprintDeclarationMapper }} from "./{ADAPTER}";\n'
        f"domainMappers[{json.dumps(DOMAIN, ensure_ascii=False)}] = blueprintDeclarationMapper;\n"
        + END + "\n"
    )
    return {"-verso-search/" + ADAPTER: adapter, "-verso-search/domain-mappers.js": registry}, len(entries)


def augment(root: Path, *, check: bool = False) -> int:
    assets, count = expected_assets(root)
    # Validate every input and destination before changing any generated file.
    for relative in assets:
        target = root / relative
        if target.is_symlink() or not target.parent.is_dir():
            raise SearchContractError("Unsafe Blueprint search output destination")
        try:
            target.parent.resolve().relative_to(root.resolve())
        except ValueError as error:
            raise SearchContractError("Blueprint search output parent escapes the output tree") from error
    if check:
        for relative, expected in assets.items():
            if required_text(root, relative) != expected:
                raise SearchContractError(f"Stale Blueprint search adapter: {relative}")
    else:
        for relative, expected in assets.items():
            (root / relative).write_text(expected, encoding="utf-8", newline="\n")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Generated Blueprint html-multi directory")
    parser.add_argument("--check", action="store_true", help="Reject absent, stale or changed search adapters")
    args = parser.parse_args()
    try:
        count = augment(args.root, check=args.check)
    except (OSError, SearchContractError) as error:
        # Filesystem exceptions can contain private paths: expose only the class.
        reason = str(error) if isinstance(error, SearchContractError) else type(error).__name__
        print(f"Blueprint declaration search: FAIL ({reason})")
        return 1
    print(f"Blueprint declaration search: PASS ({count} unique declarations; {'checked' if args.check else 'generated'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
