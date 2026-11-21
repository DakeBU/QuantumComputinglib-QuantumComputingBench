#!/usr/bin/env python3
"""Guard the concise README and detailed guide's figure and formula surfaces.

The public README is deliberately figure-first and uses conservative GitHub math
syntax. This check prevents regressions to fragile TeX, broken harness assets,
UI/sans typography, or glossy dashboard-style SVG decoration.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PROJECT_GUIDE = ROOT / "PROJECT_GUIDE.md"
SITE_JS = ROOT / "website" / "static" / "site.js"
DIAGRAM_DIR = ROOT / "website" / "diagrams"
MPL_RC = ROOT / "matplotlibrc"
CURRENT_HARNESS_WEBP = ROOT / "docs" / "assets" / "aspbe_current_harness.webp"
# The current reader-facing Harness is a high-resolution generated comic rather
# than the earlier compact diagram. Keep a bounded guard, but match the asset
# intentionally committed on main instead of the obsolete 120 KB ceiling.
CURRENT_HARNESS_WEBP_MIN_BYTES = 10_000
CURRENT_HARNESS_WEBP_MAX_BYTES = 1_500_000

MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\((docs/assets/[^)]+\.svg)\)")
HTML_SVG_RE = re.compile(r"<img\s+[^>]*src=[\"'](docs/assets/[^\"']+\.svg)[\"']", re.I)
FORBIDDEN_FONTS = (
    "Arial",
    "DejaVu Sans",
    "system-ui",
    "ui-sans-serif",
    "sans-serif",
)
FORBIDDEN_DECORATION = (
    "linearGradient",
    "radialGradient",
    "drop-shadow",
    "filter=",
)
ASCII_MATH_TOKENS = re.compile(
    r"(?i)(?:\|psi>|<psi\||\bpsi\b|\balpha\b|\bepsilon\b|\btensor\b|\bdagger\b|\bPi\b|\|0\^[a-z0-9]+>)"
)
FORBIDDEN_README_TOKENS = (
    "$$",
    r"\operatorname",
    r"\begin{cases}",
    r"\dfrac",
    r"\mathrm{diag}",
    'src="docs/assets/aspbe_hierarchical_harness_v4.webp"',
    'src="docs/assets/aspbe_hierarchical_harness.png"',
    'src="docs/assets/aspbe_hierarchical_harness_display.jpg"',
)


def fail(message: str) -> None:
    print(f"figure-style check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def readme_svg_refs(readme: str) -> list[str]:
    refs = set(MARKDOWN_IMAGE_RE.findall(readme))
    refs.update(HTML_SVG_RE.findall(readme))
    return sorted(refs)


def check_frontier_asset(readme: str) -> None:
    reference = 'src="docs/assets/aspbe_current_harness.webp"'
    if reference not in readme:
        fail("README must use the generated current ASPBE Harness comic")
    if "aspbe_master_worker_frontier.svg" in readme:
        fail("README still references the superseded Harness SVG")
    if not CURRENT_HARNESS_WEBP.is_file():
        fail("missing generated current ASPBE Harness WebP")
    payload = CURRENT_HARNESS_WEBP.read_bytes()
    if not (payload.startswith(b"RIFF") and payload[8:12] == b"WEBP"):
        fail("current ASPBE Harness asset is not a valid WebP container")
    if not (
        CURRENT_HARNESS_WEBP_MIN_BYTES
        <= len(payload)
        <= CURRENT_HARNESS_WEBP_MAX_BYTES
    ):
        fail(f"current ASPBE Harness WebP has unexpected size: {len(payload)} bytes")


def check_readme_math_surface(readme: str, *, technical_guide: bool = False) -> None:
    for token in FORBIDDEN_README_TOKENS:
        if token in readme:
            fail(f"README contains renderer-fragile token {token!r}")

    if readme.count("```math") < (6 if technical_guide else 1):
        fail("Public display equations should use fenced `math` blocks")

    for line_number, line in enumerate(readme.splitlines(), start=1):
        stripped = line.lstrip()
        if re.match(r"^#{1,6}\s", stripped) and "$" in stripped:
            fail(f"README line {line_number} puts inline math in a heading")
        if stripped.startswith("|") and "$" in stripped:
            fail(
                f"README line {line_number} puts TeX inside a Markdown table; "
                "ket/bra bars can be parsed as column separators"
            )

    if "Upper/Middle/Lower" in readme or "original fixed Upper" in readme:
        fail("README should not explain historical Harness role stacks; link the workflow page instead")

    if technical_guide:
        order = (
            readme.find("ASPBE is designed for a quantum-computing researcher"),
            readme.find("## ASPBE harness — proof-gated synthesis"),
            readme.find("## Route I — State Preparation"),
            readme.find("## Route II — Block Encoding"),
            readme.find("## Certified block-encoding cases"),
        )
        if any(position < 0 for position in order) or list(order) != sorted(order):
            fail("Technical guide reader order must be intro → Harness → SP → BE → cases")
        check_frontier_asset(readme)
    else:
        required = ("## Explore", "## See what we do", "## QuantumComputingBench", "## News",
                    "PROJECT_GUIDE.md", "/library/", "/lean-graph/", "/functor-hypergraph/", "/quantumcomputingbench/")
        for marker in required:
            if marker not in readme:
                fail(f"README missing reader entry {marker!r}")
        news = readme.split("## News", 1)[1].split("\n## ", 1)[0]
        if news.count("- **") > 4:
            fail("Keep only four concise news items in the README; archive the rest")
        if len(readme.split()) > 600:
            fail("README is too dense for the project landing page; move technical detail to the guide")


def check_readme_svgs(readme: str, *, minimum: int = 1) -> None:
    refs = readme_svg_refs(readme)
    if len(refs) < minimum:
        fail(f"Reader surface should contain at least {minimum} SVG figures; found {len(refs)}")

    for ref in refs:
        path = ROOT / ref
        source = read(path)
        try:
            ET.fromstring(source)
        except ET.ParseError as exc:
            fail(f"invalid SVG XML in {ref}: {exc}")

        if "Times New Roman" not in source:
            fail(f"{ref} does not declare Times New Roman")
        for font in FORBIDDEN_FONTS:
            if font in source:
                fail(f"{ref} contains forbidden UI font {font!r}")
        for token in FORBIDDEN_DECORATION:
            if token in source:
                fail(f"{ref} contains dashboard-style SVG decoration {token!r}")
        if ASCII_MATH_TOKENS.search(source):
            fail(f"{ref} contains ASCII pseudo-mathematics; use Unicode symbols")


def check_mermaid_math_labels() -> None:
    diagrams = sorted(DIAGRAM_DIR.glob("*.mmd"))
    if not diagrams:
        fail("website/diagrams contains no Mermaid sources")
    for path in diagrams:
        source = read(path)
        match = ASCII_MATH_TOKENS.search(source)
        if match:
            fail(
                f"{path.relative_to(ROOT)} contains ASCII pseudo-math {match.group(0)!r}; "
                "use Unicode mathematical labels"
            )


def check_website_runtime_figures() -> None:
    source = read(SITE_JS)
    required = (
        '"Times New Roman"',
        ".diagram-panel .mermaid",
        ".quantikz-preview text",
        "box-shadow: none",
        '.replace(/\\balpha\\b/g, "α")',
        '.replace(/\\btheta\\b/g, "θ")',
        '.replace(/\\bperp\\b/g, "⊥")',
        '"|$1⟩"',
        'replace(/\\\\operatorname\\{([^{}]+)\\}/g, "\\\\mathrm{$1}")',
        "normalizeFragileMath",
        "MutationObserver",
    )
    for needle in required:
        if needle not in source:
            fail(f"website figure/math override is missing {needle!r}")


def check_matplotlib_defaults() -> None:
    source = read(MPL_RC)
    required = (
        "font.family: serif",
        "Times New Roman",
        "mathtext.fontset: stix",
        "svg.fonttype: none",
    )
    for needle in required:
        if needle not in source:
            fail(f"matplotlibrc is missing {needle!r}")


def main() -> None:
    readme = read(README)
    check_readme_math_surface(readme)
    check_readme_svgs(readme)
    guide = read(PROJECT_GUIDE)
    check_readme_math_surface(guide, technical_guide=True)
    check_readme_svgs(guide, minimum=5)
    check_mermaid_math_labels()
    check_website_runtime_figures()
    check_matplotlib_defaults()
    print("public README typography/formula/layout checks passed")


if __name__ == "__main__":
    main()
