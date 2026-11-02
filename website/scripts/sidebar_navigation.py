"""One concise final sidebar, rendered from the existing textbook/case catalogs."""
from __future__ import annotations

import html
import re


TOOLS = (
    ("Lean library", "library/"),
    ("Underlying Lean Graph of Libraries", "lean-graph/"),
    ("Implementation map", "implementation-map/"),
    ("Live workspace", "ide/"),
    ("Run with your API", "task-builder/"),
    ("ASPBE harness", "workflow/"),
    ("Verso Blueprint", "blueprint/"),
)
PROJECT = (
    ("Our place in Math 2.0", "math-2-0/"),
    ("Quantum ecosystem", "ecosystem/"),
    ("Contribute", "community/"),
    ("Contributors", "contributors/"),
    ("Organizers", "organizers/"),
    ("Licenses and reuse", "licensing/"),
)
NAV = re.compile(r'<nav class="book-nav"(?:\s[^>]*)?>.*?</nav>', re.S)


def render_navigation(prefix: str, current: str, papers: dict, cases: list[dict]) -> str:
    from website.scripts import build_site
    from website.scripts.finalize_taxonomy_navigation import (
        render_examples_navigation, render_papers_navigation,
    )
    from website.scripts.research_atlas import VIEWS

    route = current.removesuffix("index.html")

    def link(label: str, target: str) -> str:
        active = ' aria-current="page"' if route == target else ""
        return f'<a href="{html.escape(build_site.page_url(prefix, target))}"{active}>{html.escape(label)}</a>'

    def section(key: str, title: str, content: str, selected: bool) -> str:
        opened = " open" if selected else ""
        return (f'<details class="sidebar-section" data-nav-section="{key}"{opened}>'
                f'<summary>{html.escape(title)}</summary>'
                f'<div class="sidebar-section-links">{content}</div></details>')

    def links_section(key: str, title: str, items) -> str:
        return section(key, title, "".join(link(label, target) for label, target in items),
                       any(route.startswith(target) for _, target in items))

    # Keep the existing SP/BE hierarchies and every paper/case, but expose them
    # only on demand. Their old group headings become the disclosure summaries.
    def collection(key: str, title: str, content: str, target: str) -> str:
        heading = f'<strong class="nav-group-label">{title}</strong>'
        if not content.startswith(heading):
            raise ValueError(f"missing canonical {title} navigation heading")
        return section(key, title, content[len(heading):], route.startswith(target))

    research = links_section("research", "Structure & research", VIEWS)
    bench = links_section("quantumcomputingbench", "QuantumComputingBench", (
        ("Exercise book", "quantumcomputingbench/"),
        ("Mathematical exercises", "quantumcomputingbench/non-lean/"),
        ("Lean companion", "quantumcomputingbench/lean/"),
        ("Contribution contract", "quantumcomputingbench/contribute/"),
        ("Evidence and release gates", "quantumcomputingbench/evidence/"),
    ))
    return (
        '<nav class="book-nav" data-compact-navigation="1">'
        '<strong class="nav-group-label">Explore</strong>'
        + link("Home", "") + link("Book map", "learning/")
        + '<strong class="nav-group-label">Textbooks</strong>'
        + build_site.render_book_navigation(prefix, route)
        + bench
        + '<!-- research-nav:start -->' + research + '<!-- research-nav:end -->'
        + collection("papers", "Papers", render_papers_navigation(prefix, current, papers), "papers/")
        + collection("examples", "Example Cases", render_examples_navigation(prefix, current, cases), "example-cases/")
        + links_section("tools", "Library & tools", TOOLS)
        + links_section("project", "About & community", PROJECT)
        + '</nav>'
    )


def replace_navigation(text: str, prefix: str, current: str, papers: dict, cases: list[dict]) -> str:
    """Replace, never append; missing/ambiguous navigation fails closed."""
    if len(NAV.findall(text)) != 1:
        raise ValueError(f"expected one common sidebar navigation: {current}")
    text = NAV.sub(lambda _: render_navigation(prefix, current, papers, cases), text, count=1)
    # Keep the frozen base renderer intact; the final navigation pass adds a
    # native, no-JavaScript footer entry at the correct page-relative depth.
    footer = re.compile(r'(<footer class="site-footer">.*?<nav aria-label="Footer">)(.*?)(</nav>)', re.S)
    def add_license_link(match):
        if 'data-license-link="1"' in match[2]:
            return match[0]
        link = f'<a data-license-link="1" href="{html.escape(prefix)}licensing/index.html">Licenses and reuse</a>'
        return match[1] + match[2] + link + match[3]
    return footer.sub(add_license_link, text)
