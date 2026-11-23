#!/usr/bin/env python3
"""Check the assembled static site, internal links, fragments, and indexes."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[2]


def check_hermite_publication(site: Path, repository: Path = ROOT) -> list[str]:
    """Check final assembled output, not merely successful source rendering."""
    errors: list[str] = []
    site = site.resolve()
    payload = json.loads((repository / "website/hermite-case.json").read_text(encoding="utf-8"))
    slug = "hermite-smooth-state-preparation"
    cases = [case for case in payload["cases"] if case["slug"] == slug]
    if len(cases) != 1:
        return ["Hermite publication must have exactly one mandatory case"]
    page = site / "example-cases" / slug / "index.html"
    if not page.is_file() or page.stat().st_size == 0:
        errors.append("Hermite case page is absent or empty")
    for asset in cases[0]["supplementaryAssets"]:
        name = str(asset["path"])
        relative = PurePosixPath(name)
        if (relative.is_absolute() or PureWindowsPath(name).is_absolute()
                or ".." in relative.parts or "\\" in name):
            errors.append("Hermite download has a non-portable path")
            continue
        source = repository / relative
        target = site / "downloads" / slug / relative
        if (not target.is_file() or not target.resolve().is_relative_to(site)
                or target.stat().st_size == 0):
            errors.append(f"Hermite download absent or empty: {name}")
        elif not source.is_file() or target.read_bytes() != source.read_bytes():
            errors.append(f"Hermite download differs from the current source: {name}")
    return errors


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.base_href: str | None = None

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        identifier = values.get("id") or values.get("name")
        if identifier:
            self.ids.add(identifier)
        if tag == "base" and values.get("href") and self.base_href is None:
            self.base_href = values["href"]
        if tag in {"a", "link"} and values.get("href"):
            self.references.append(("href", values["href"]))
        if tag in {"script", "img", "source"} and values.get("src"):
            self.references.append(("src", values["src"]))


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def relative_url(path: Path, site: Path) -> str:
    return path.relative_to(site).as_posix()


def target_file(
    site: Path, current: Path, raw_url: str, base_href: str | None
) -> tuple[Path, str]:
    parsed = urlsplit(raw_url)
    current_url = relative_url(current, site)
    base_url = urljoin(current_url, base_href) if base_href else current_url
    joined = urlsplit(urljoin(base_url, parsed.path))
    relative = unquote(joined.path).lstrip("/")
    target = site / relative
    if not parsed.path:
        target = site / unquote(urlsplit(base_url).path).lstrip("/")
        if target.is_dir() or str(base_url).endswith("/"):
            target /= "index.html"
    elif parsed.path.endswith("/"):
        target /= "index.html"
    elif target.is_dir():
        target /= "index.html"
    return target, unquote(parsed.fragment)


def check_links(site: Path) -> list[str]:
    errors: list[str] = []
    page_cache: dict[Path, PageParser] = {}

    def cached_page(path: Path) -> PageParser:
        if path not in page_cache:
            page_cache[path] = parse_page(path)
        return page_cache[path]

    pages = sorted(site.rglob("*.html"))
    for page in pages:
        parser = cached_page(page)
        for attribute, url in parser.references:
            parsed = urlsplit(url)
            if parsed.scheme in {"http", "https", "mailto", "data", "javascript"}:
                continue
            if url.startswith("//"):
                continue
            target, fragment = target_file(site, page, url, parser.base_href)
            if not target.exists():
                errors.append(
                    f"{relative_url(page, site)}: missing {attribute} target {url}"
                )
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = cached_page(target)
                if fragment not in target_parser.ids:
                    errors.append(
                        f"{relative_url(page, site)}: missing fragment {url}"
                    )
    return errors


def require(path: Path, errors: list[str]) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        errors.append(f"missing or empty required artifact: {path}")


def check_ordered_markers(text: str, markers: tuple[str, ...], label: str) -> list[str]:
    positions = [text.find(marker) for marker in markers]
    if any(position < 0 for position in positions):
        missing = [marker for marker, position in zip(markers, positions) if position < 0]
        return [f"{label}: missing ordered marker(s): {missing}"]
    if positions != sorted(positions):
        return [f"{label}: markers are not in required newest-to-oldest order"]
    return []


MOJIBAKE_MARKERS = ("\ufffd", "ï¿½", "Ã", "Â", "â€", "ðŸ")


def check_encoding(site: Path) -> list[str]:
    errors: list[str] = []
    # Restrict this check to the MathJax container itself. Case pages embed
    # JSON later in the document, where valid JSON escaping spells `\frac`
    # as `\\frac`; a cross-element regex would report that as corrupt TeX.
    doubled_tex = re.compile(
        r'<div class="math-block">(?:(?!</div>).)*?\\\\[A-Za-z]',
        re.S,
    )
    for path in sorted(site.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".json", ".js", ".css", ".tex", ".md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"{relative_url(path, site)}: invalid UTF-8: {error}")
            continue
        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                errors.append(f"{relative_url(path, site)}: mojibake marker {marker!r}")
        if any(0x80 <= ord(character) <= 0x9F for character in text):
            errors.append(f"{relative_url(path, site)}: C1 control character")
        if path.suffix == ".html" and doubled_tex.search(text):
            errors.append(f"{relative_url(path, site)}: doubled TeX command in MathJax container")
    return errors


def check_case_teaching(case_page: str, slug: str) -> list[str]:
    """Require reader-facing replay evidence without claiming a full Operator check."""
    errors: list[str] = []
    for marker in (
        "The equation being studied",
        "Circuit anatomy",
        "Candidate and proof progression",
        "Named Lean certificates",
    ):
        if marker not in case_page:
            errors.append(f"example case lacks teaching marker {marker!r}: {slug}")
    # Check the actual evidence section: embedded source downloads or unrelated
    # prose must not hide a missing backend row or a missing trust boundary.
    evidence = re.search(
        r'<section\b[^>]*\bid=[\"\']executable-evidence[\"\'][^>]*>(.*?)</section>',
        case_page, re.S,
    )
    if evidence is None:
        errors.append(f"example case lacks executable evidence section: {slug}")
        return errors
    for marker in (
        "Executable verification and exports",
        "Checking and artifact selection are independent",
        "<th>Qiskit replay</th>",
        "Gate-by-gate numerical screening",
        "OpenQASM 3 round-trip",
        "Fast executable checks may reject, rank, or queue a route for formalization",
        "Floating-point tolerances do not replace the exact Lean roots above",
    ):
        if marker not in evidence.group(1):
            errors.append(f"example case lacks executable teaching marker {marker!r}: {slug}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT / "_site")
    parser.add_argument("--require-blueprint", action="store_true")
    args = parser.parse_args()
    site = args.root.resolve()
    errors: list[str] = []

    required = [
        "index.html",
        "state-preparation/index.html",
        "block-encoding/index.html",
        "quantum-information/index.html",
        "quantum-scientific-computing/index.html",
        "data/curriculum-parts.json",
        "implementation-map/index.html",
        "learning/index.html",
        "library/index.html",
        "roadmap/index.html",
        "workflow/index.html",
        "ide/index.html",
        "ide-data.json",
        "ecosystem/index.html",
        "community/index.html",
        "contributors/index.html",
        "CONTRIBUTING.md",
        "community/contribution.schema.json",
        "community/translation-response.schema.json",
        "organizers/index.html",
        "attribution/index.html",
        "blueprint/index.html",
        "task-builder/index.html",
        "example-cases/index.html",
        "data/example-cases.json",
        "search-index.json",
        "library/declarations.json",
        "site-metadata.json",
        "build-report.json",
        "case-studies/robin/index.html",
        "sources/ghl2025-robin-excerpts.tex",
        "data/public-case-replay.json",
        "static/site.css",
        "static/site.js",
        "static/curriculum.js",
        "static/task-builder.js",
        "static/case-memory.js",
        "static/workspace.js",
        "static/favicon.svg",
    ]
    for item in required:
        require(site / item, errors)
    errors.extend(check_hermite_publication(site))

    home = (site / "index.html").read_text(encoding="utf-8")
    errors.extend(
        check_ordered_markers(
            home,
            (
                'datetime="2026-11-24"',
                'datetime="2026-10-21"',
                'datetime="2026-09-10"',
                'datetime="2026-08-14"',
            ),
            "homepage News",
        )
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    errors.extend(
        check_ordered_markers(
            readme,
            (
                "- **24 November 2026.**",
                "- **21 October 2026.**",
                "- **10 September 2026.**",
                "- **14 August 2026.**",
            ),
            "README News",
        )
    )
    archive = (ROOT / "PROJECT_GUIDE.md").read_text(encoding="utf-8")
    errors.extend(check_ordered_markers(archive, (
        "- **17 May 2026.**", "- **May 2026.**", "- **April 2026.**"), "Project history"))
    learning = (site / "learning" / "index.html").read_text(encoding="utf-8")
    for marker in (
        "Part I · State Preparation",
        "Part II · Block Encoding",
        "Planned Part III",
        "Planned Part IV",
        "quantum-domain-roadmap",
        'id="textbook-explorer"',
        "data-curriculum-query",
        "data-curriculum-card",
        "Not local admission",
    ):
        if marker not in learning:
            errors.append(f"learning page lacks curriculum marker {marker!r}")

    roadmap = (site / "roadmap" / "index.html").read_text(encoding="utf-8")
    for marker in (
        'id="long-term-quantum-curriculum"',
        "Representation-theoretic methods in quantum information theory",
        "Quantum Algorithms for Scientific Computation",
        'id="vandaele-frontier"',
        "literal Figure 4 gates",
    ):
        if marker not in roadmap:
            errors.append(f"roadmap page lacks formalization-plan marker {marker!r}")

    if args.require_blueprint:
        require(site / "blueprint" / "html-multi" / "index.html", errors)

    if errors:
        print("\n".join(errors))
        return 1

    inventory = json.loads(
        (site / "library" / "declarations.json").read_text(encoding="utf-8")
    )
    search = json.loads((site / "search-index.json").read_text(encoding="utf-8"))
    metadata = json.loads((site / "site-metadata.json").read_text(encoding="utf-8"))
    replay = json.loads(
        (site / "data" / "public-case-replay.json").read_text(encoding="utf-8")
    )
    declaration_count = int(inventory["publicDeclarationCount"])
    if search["declarationEntryCount"] != declaration_count:
        errors.append("search declarationEntryCount differs from inventory")
    declaration_entries = sum(
        entry.get("type") == "declaration" for entry in search["entries"]
    )
    if declaration_entries != declaration_count:
        errors.append("search declaration entries differ from inventory")
    if search["entryCount"] != len(search["entries"]):
        errors.append("search entryCount differs from entries length")
    if metadata["declarationCount"] != declaration_count:
        errors.append("site metadata declarationCount differs from inventory")
    if replay.get("cold_start_claim") is not False:
        errors.append("public-case replay incorrectly claims cold-start discovery")
    if metadata.get("publicCaseReplay", {}).get("sourceDigest") != replay.get(
        "source_digest"
    ):
        errors.append("site metadata public-case replay digest differs from report")

    diagrams = sorted((site / "diagrams").glob("*.mmd"))
    if len(diagrams) < 7:
        errors.append(f"expected at least 7 editable diagrams, found {len(diagrams)}")
    unified_pages = [
        site / "index.html",
        site / "implementation-map" / "index.html",
        site / "learning" / "index.html",
        site / "library" / "index.html",
        site / "roadmap" / "index.html",
        site / "workflow" / "index.html",
        site / "ide" / "index.html",
        site / "community" / "index.html",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in unified_pages)
    for marker in (
        "mathjax@3",
        "mermaid@11",
        'data-theme-choice="blueprint"',
        'data-theme-choice="modern"',
        'data-theme-choice="bold"',
        'name="viewport"',
        'class="site-sidebar"',
        "QuantumComputinglib",
        "ASPBE",
        "DakeBU/QuantumComputinglib-QuantumComputingBench",
        "Dake Bu, Xiajie Huang, Outongyi Lv, Nana Liu, Atsushi Nitanda, Hau-san Wong, Qingfu Zhang",
        "<span>01</span>",
    ):
        if marker not in combined:
            errors.append(f"missing frontend marker: {marker}")
    css = (site / "static" / "site.css").read_text(encoding="utf-8")
    for marker in (
        ':root[data-theme="modern"]',
        ':root[data-theme="bold"]',
        "@media (max-width: 760px)",
        "@media (prefers-reduced-motion: reduce)",
        ".site-sidebar",
        ".workspace-grid",
    ):
        if marker not in css:
            errors.append(f"missing CSS marker: {marker}")
    task_builder = (site / "task-builder" / "index.html").read_text(encoding="utf-8")
    task_script = (site / "static" / "task-builder.js").read_text(encoding="utf-8")
    for marker in ("Run with my API", 'id="runnerEndpoint"', 'class="site-sidebar"', "Example Cases"):
        if marker not in task_builder:
            errors.append(f"missing user API task-builder marker: {marker}")
    for marker in ("Authorization", "runWithApi"):
        if marker not in task_script:
            errors.append(f"missing user API runner client marker: {marker}")
    if "/api/run-task" not in task_builder:
        errors.append("missing default user API runner endpoint")
    for forbidden in ("topbar", "Testing preview", "aspbe-harness-flow.svg", "abeis-library-map.svg", "redactApiKey"):
        if forbidden in task_builder or forbidden in task_script:
            errors.append(f"forbidden standalone task-builder marker: {forbidden}")
    memory_script = (site / "static" / "case-memory.js").read_text(encoding="utf-8")
    for marker in ("indexedDB", "pendingReview", "verified", "rejected", "apiKey"):
        if marker not in memory_script:
            errors.append(f"missing private case-memory marker: {marker}")
    generated_pages = [
        path for path in site.rglob("*.html")
        if "blueprint/html" not in path.relative_to(site).as_posix()
    ]
    for page in generated_pages:
        page_text = page.read_text(encoding="utf-8")
        if 'class="site-sidebar"' not in page_text or "Example Cases" not in page_text:
            errors.append(f"{relative_url(page, site)}: common navigation is incomplete")
    cases = json.loads((site / "data" / "example-cases.json").read_text(encoding="utf-8"))["cases"]
    if metadata.get("exampleCaseCount") != len(cases):
        errors.append("site metadata exampleCaseCount differs from generated cases")
    for case in cases:
        route = site / "example-cases" / case["slug"] / "index.html"
        if not route.exists():
            errors.append(f"missing example case route: {case['slug']}")
            continue
        case_page = route.read_text(encoding="utf-8")
        if f"?case={case['slug']}" not in case_page:
            errors.append(f"example case lacks task-builder preset link: {case['slug']}")
        errors.extend(check_case_teaching(case_page, str(case["slug"])))
    if re.search(r"(?:file://|/home/|[A-Za-z]:\\\\Users\\\\)", combined):
        errors.append("local filesystem path leaked into unified HTML")

    errors.extend(check_encoding(site))
    errors.extend(check_links(site))
    if errors:
        print("Site checks failed:")
        for error in errors:
            print(f"  {error}")
        return 1
    print(
        f"site checks passed: {len(list(site.rglob('*.html')))} HTML pages, "
        f"{declaration_count} declaration search entries, {len(diagrams)} diagrams"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
