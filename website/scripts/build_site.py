#!/usr/bin/env python3
"""Build QuantumComputinglib from the ASPBE Lean inventory and teaching content."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import quote

try:
    from proof_inputs import lean_module_targets, proof_input_digest
except ModuleNotFoundError:
    from website.scripts.proof_inputs import lean_module_targets, proof_input_digest


ROOT = Path(__file__).resolve().parents[2]
WEBSITE_ROOT = ROOT / "website"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(WEBSITE_ROOT))

from content import (  # noqa: E402
    CHAPTERS,
    IMPLEMENTATION_MAP,
    LESSONS,
    ROADMAP,
    STATUS_ORDER,
    WORKFLOW_STAGES,
)
from website.case_assets import STAGE_CIRCUITS, stage_circuit_latex  # noqa: E402
from lean_graph import build_lean_graph_payload, render_lean_graph_body  # noqa: E402


NAVIGATION = [
    ("Home", ""),
    ("Our place in Math 2.0", "math-2-0/"),
    ("Book map", "learning/"),
    ("Part I · State Preparation", "state-preparation/"),
    ("Part II · Block Encoding", "block-encoding/"),
    ("Part III · QIT & Representation", "quantum-information/"),
    ("Part IV · Scientific Computing", "quantum-scientific-computing/"),
    ("Lean library", "library/"),
    ("Underlying Lean Graph of Libraries", "lean-graph/"),
    ("Implementation map", "implementation-map/"),
    ("Robin paper map", "case-studies/robin/"),
    ("Live workspace", "ide/"),
    ("Run with your API", "task-builder/"),
    ("Quantum ecosystem", "ecosystem/"),
    ("Progress", "roadmap/"),
    ("Contribute", "community/"),
    ("Contributors", "contributors/"),
    ("Organizers", "organizers/"),
]

PROJECT_REPOSITORY = "DakeBU/QuantumComputinglib-QuantumComputingBench"
PROJECT_REPOSITORY_URL = f"https://github.com/{PROJECT_REPOSITORY}"
ORGANIZERS = (
    ("Dake Bu", "City University of Hong Kong · A*STAR"),
    ("Xiajie Huang", "Shanghai Jiao Tong University"),
    ("Outongyi Lv", "Shanghai Jiao Tong University"),
    ("Nana Liu", "Shanghai Jiao Tong University"),
    ("Atsushi Nitanda", "A*STAR · Nanyang Technological University"),
    ("Hau-san Wong", "City University of Hong Kong"),
    ("Qingfu Zhang", "City University of Hong Kong"),
)

EXAMPLE_CASE_NAV: list[tuple[str, str]] = []
DOUBLE_TEX_COMMAND = re.compile(r"\\\\(?=[A-Za-z])")


def render_math_tex(tex: str) -> str:
    """Render canonical TeX after rejecting corrupt or pre-escaped input."""
    if "\x00" in tex:
        raise ValueError("MathJax source contains NUL")
    normalized = unicodedata.normalize("NFC", tex)
    if "\ufffd" in normalized:
        raise ValueError("MathJax source contains U+FFFD")
    if DOUBLE_TEX_COMMAND.search(normalized):
        raise ValueError(f"MathJax source contains doubled TeX command: {tex!r}")
    return f'<div class="math-block">\\[{html.escape(normalized, quote=False)}\\]</div>'


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def github_repository(remote: str) -> str | None:
    patterns = [
        r"^https://github\.com/(?P<repo>[^/]+/[^/]+?)(?:\.git)?$",
        r"^git@github\.com:(?P<repo>[^/]+/[^/]+?)(?:\.git)?$",
        r"^ssh://git@github\.com/(?P<repo>[^/]+/[^/]+?)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.match(pattern, remote)
        if match:
            return match.group("repo")
    return None


def git_context() -> dict[str, object]:
    commit = run_git("rev-parse", "HEAD")
    short_commit = run_git("rev-parse", "--short=12", "HEAD")
    branch = run_git("branch", "--show-current") or os.getenv("GITHUB_REF_NAME", "detached")
    remote = run_git("remote", "get-url", "origin")
    repository = github_repository(remote)
    remote_branches = run_git("branch", "-r", "--contains", commit).splitlines()
    github_sha = os.getenv("GITHUB_SHA", "")
    published = bool(
        commit
        and repository
        and (
            any(line.strip().startswith("origin/") for line in remote_branches)
            or github_sha == commit
        )
    )
    return {
        "commit": commit,
        "shortCommit": short_commit,
        "branch": branch,
        "remote": remote,
        "repository": repository,
        "publishedRef": published,
    }


def path_is_clean(path: str) -> bool:
    return not run_git("status", "--porcelain", "--", path)


def path_exists_at_head(path: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    return result.returncode == 0


def external_source_url(
    source: str, line: int, context: dict[str, object]
) -> str | None:
    repository = context["repository"]
    commit = context["commit"]
    if (
        not context["publishedRef"]
        or not repository
        or not commit
        or not path_is_clean(source)
        or not path_exists_at_head(source)
    ):
        return None
    return f"https://github.com/{repository}/blob/{commit}/{quote(source)}#L{line}"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def module_slug(source: str) -> str:
    return slug(source.removeprefix("QuantumBlockEncoding/").removesuffix(".lean"))


def declaration_anchor(full_name: str) -> str:
    return f"decl-{slug(full_name)}"


def status_class(status: str) -> str:
    return f"status status-{slug(status)}"


def badge(status: str) -> str:
    return f'<span class="{status_class(status)}">{html.escape(status)}</span>'


def prefix_for(route: str) -> str:
    depth = len([part for part in route.strip("/").split("/") if part])
    return "../" * depth if depth else "./"


def page_url(prefix: str, route: str) -> str:
    return f"{prefix}{route}index.html" if route else f"{prefix}index.html"


def module_url(prefix: str, declaration: dict[str, object]) -> str:
    source = str(declaration["source"])
    return (
        f"{prefix}library/modules/{module_slug(source)}/"
        f"index.html#{declaration_anchor(str(declaration['fullName']))}"
    )


def blueprint_url(prefix: str, declaration: dict[str, object]) -> str:
    target = str(declaration["blueprintUrl"]).removeprefix("../")
    return f"{prefix}{target}"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_curriculum_catalog(
    curriculum: dict[str, object],
    sources: dict[str, object],
    oai_intake: dict[str, object],
) -> list[dict[str, object]]:
    """Validate planned textbook placement without promoting it to Lean truth."""
    parts = curriculum.get("parts")
    if not isinstance(parts, list) or len(parts) != 4:
        raise SystemExit("Curriculum catalog must contain exactly four peer parts.")
    source_ids = {str(item["id"]) for item in sources.get("sources", [])}
    cluster_ids = {str(item["id"]) for item in oai_intake.get("clusters", [])}
    seen_parts: set[str] = set()
    seen_routes: set[str] = set()
    seen_chapters: set[str] = set()
    for part in parts:
        part_id = str(part.get("id", ""))
        route = str(part.get("route", ""))
        status = str(part.get("status", ""))
        if not part_id or part_id in seen_parts:
            raise SystemExit(f"Duplicate or empty curriculum part id: {part_id!r}")
        if not route or route in seen_routes or route.startswith(('/', '\\')) or ':' in route:
            raise SystemExit(f"Unsafe or duplicate curriculum route: {route!r}")
        if status not in STATUS_ORDER:
            raise SystemExit(f"Unknown curriculum status: {status!r}")
        seen_parts.add(part_id)
        seen_routes.add(route)
        unknown_sources = set(map(str, part.get("sourceIds", []))) - source_ids
        if unknown_sources:
            raise SystemExit(f"{part_id}: unknown source ids: {sorted(unknown_sources)}")
        for chapter in part.get("chapters", []):
            chapter_id = str(chapter.get("id", ""))
            chapter_status = str(chapter.get("status", ""))
            if not chapter_id or chapter_id in seen_chapters:
                raise SystemExit(f"Duplicate or empty curriculum chapter id: {chapter_id!r}")
            if chapter_status not in STATUS_ORDER:
                raise SystemExit(f"{chapter_id}: unknown status {chapter_status!r}")
            seen_chapters.add(chapter_id)
            unknown_clusters = set(map(str, chapter.get("oaiClusters", []))) - cluster_ids
            if unknown_clusters:
                raise SystemExit(f"{chapter_id}: unknown OpenAI Math clusters: {sorted(unknown_clusters)}")
            href = str(chapter.get("href", ""))
            if href and (href.startswith(('/', '\\')) or ':' in href or '\\' in href):
                raise SystemExit(f"{chapter_id}: unsafe local href {href!r}")
    if seen_parts != {
        "part-i-state-preparation", "part-ii-block-encoding",
        "part-iii-quantum-information", "part-iv-quantum-scientific-computing",
    }:
        raise SystemExit("Curriculum catalog must name the four canonical peer parts.")
    placements = {
        f'{part["id"]}:{chapter["id"]}': set(chapter.get("oaiClusters", []))
        for part in parts for chapter in part["chapters"]
    }
    for cluster in oai_intake.get("clusters", []):
        for target in cluster.get("curriculum", []):
            if cluster["id"] not in placements.get(target, set()):
                raise SystemExit(f"Missing audited upstream placement: {cluster['id']} -> {target}")
    upstream = oai_intake.get("upstream", {})
    local = oai_intake.get("local_boundary", {})
    if upstream.get("lean_toolchain") != "leanprover/lean4:v4.34.1":
        raise SystemExit("OpenAI Math pinned toolchain boundary is missing or changed.")
    if local.get("lean_toolchain") != "leanprover/lean4:v4.33.0":
        raise SystemExit("Local curriculum toolchain must remain Lean 4.33.0.")
    if local.get("direct_package_dependency_allowed") is not False:
        raise SystemExit("Toolchain-mismatched OpenAI Math must not be a direct dependency.")
    return parts


def parse_literature_registry() -> list[dict[str, str]]:
    source = (ROOT / "QuantumBlockEncoding" / "Literature.lean").read_text(
        encoding="utf-8"
    )
    entries: list[dict[str, str]] = []
    for block in re.findall(r"\{\s*key := .*?\n\s*\}", source, flags=re.S):
        item: dict[str, str] = {}
        for field in ("key", "title", "authors", "targetFile", "url", "note"):
            match = re.search(field + r' := "([^"]*)"', block)
            if match:
                item[field] = match.group(1)
        for field, pattern in (
            ("year", r"year := ([0-9]+)"),
            ("role", r"role := PaperRole\.([A-Za-z]+)"),
            ("status", r"status := ImplementationStatus\.([A-Za-z]+)"),
        ):
            match = re.search(pattern, block)
            if match:
                item[field] = match.group(1)
        if "key" in item:
            entries.append(item)
    return entries


def load_gate_report(path: Path, context: dict[str, object]) -> dict[str, object]:
    if not path.exists():
        raise SystemExit(
            f"Lean gate report is missing: {path}. Run the Lean gate before publishing."
        )
    report = load_json(path)
    if report.get("commit") != context["commit"] or report.get("passed") is not True:
        raise SystemExit("Lean gate report does not certify the current checkout.")
    if report.get("proofInputsSha256") != proof_input_digest(ROOT):
        raise SystemExit("Lean gate proof inputs differ from the current files; rebuild before publishing.")
    if report.get("compiledModules") != lean_module_targets(ROOT):
        raise SystemExit("Lean gate does not cover every current module; rerun the complete gate.")
    return report


def source_statement(preview: str) -> str:
    lines = preview.splitlines()
    kept: list[str] = []
    for line in lines:
        kept.append(line)
        if ":= by" in line or line.rstrip().endswith(":= by"):
            break
        if line.strip() in {"sorry", "by"}:
            break
        if len(kept) >= 11:
            break
    return "\n".join(kept)


def render_book_navigation(prefix: str, current: str) -> str:
    """Use the same four-part catalog in every sidebar, without proof promotion."""
    parts = load_json(WEBSITE_ROOT / "curriculum-parts.json")["parts"]
    by_number = {int(chapter["number"]): chapter for chapter in CHAPTERS}
    groups = []
    for index, part in enumerate(parts):
        route = str(part["route"])
        guided = [by_number[number] for number in BOOK_PARTS[index][1]] if index < 2 else []
        selected = current == route or any(
            current == f"chapters/{chapter['slug']}/" for chapter in guided
        )
        opened = " open" if selected else ""
        active = ' aria-current="page"' if current == route else ""
        links = [f'<a class="book-part-overview" href="{page_url(prefix, route)}"{active}>Part overview →</a>']
        for chapter in guided:
            chapter_route = f"chapters/{chapter['slug']}/"
            active = ' aria-current="page"' if current == chapter_route else ""
            links.append(
                f'<a href="{page_url(prefix, chapter_route)}"{active}>'
                f'<span class="book-chapter-number">{int(chapter["number"]):02d}</span>'
                f'<span>{html.escape(str(chapter["title"]))}</span></a>'
            )
        for chapter in part["chapters"]:
            if index < 2 and chapter["status"] == "Compiled":
                continue  # Already reached through the overview and guided chapters.
            # A shared technique can belong to multiple books. Link its owned
            # chapter card here; the card retains the common source/route link.
            target = f'{page_url(prefix, route)}#{chapter["id"]}'
            links.append(
                f'<a class="book-curriculum-link" href="{html.escape(target)}">'
                f'<span>{html.escape(str(chapter["title"]))}</span>'
                f'<small class="book-chapter-status">{html.escape(str(chapter["status"]))}</small></a>'
            )
        groups.append(
            f'<details class="book-part-nav" data-book-part="{part["id"]}"{opened}>'
            f'<summary><span class="book-part-label">{part["label"]}</span>'
            f'<span>{html.escape(str(part["title"]))}</span></summary>'
            f'<div class="book-part-links">{"".join(links)}</div></details>'
        )
    return '<div class="book-part-navigation" aria-label="Chapters by textbook">' + "".join(groups) + '</div>'


def site_header(prefix: str, current: str) -> str:
    links: list[str] = []
    for label, route in NAVIGATION:
        current_attr = ' aria-current="page"' if current == route else ""
        links.append(
            f'<a href="{page_url(prefix, route)}"{current_attr}>{html.escape(label)}</a>'
        )
    example_links = []
    for index, (label, case_slug) in enumerate(EXAMPLE_CASE_NAV, start=1):
        route = f"example-cases/{case_slug}/"
        current_attr = ' aria-current="page"' if current == route else ""
        example_links.append(
            f'<a href="{page_url(prefix, route)}"{current_attr}>'
            f'<span>{index:02d}</span>'
            f'<span>{html.escape(label)}</span></a>'
        )
    return f"""
<a class="skip-link" href="#main-content">Skip to content</a>
<header class="mobile-header">
    <a class="brand" href="{page_url(prefix, '')}">
      <span class="brand-word">QuantumComputinglib</span>
      <span class="brand-subtitle">learn · inspect · formalize</span>
    </a>
    <button class="icon-button mobile-menu" type="button" data-menu-button
            aria-label="Open book navigation" aria-expanded="false">&#9776;</button>
</header>
<aside class="site-sidebar" data-main-nav aria-label="QuantumComputinglib book navigation">
  <div class="sidebar-head">
    <a class="brand" href="{page_url(prefix, '')}">
      <span class="brand-word">QuantumComputinglib</span>
      <span class="brand-subtitle">A formal quantum computing textbook</span>
    </a>
    <p><strong>ASPBE</strong><br>Automatic State Preparation and Block Encoding for Quantum Computing</p>
  </div>
  <div class="sidebar-search search-shell">
    <label class="visually-hidden" for="global-search">Search declarations and chapters</label>
    <input id="global-search" class="global-search" type="search"
           placeholder="Search QuantumComputinglib" data-global-search>
    <div class="search-results" data-search-results hidden></div>
  </div>
  <nav class="book-nav">
    <strong class="nav-group-label">Explore</strong>
    {''.join(links)}
    <strong class="nav-group-label">Chapters</strong>
    {render_book_navigation(prefix, current)}
    <strong class="nav-group-label">Example Cases</strong>
    <a href="{page_url(prefix, 'example-cases/')}">All examples</a>
    <div class="example-nav">{''.join(example_links)}</div>
    <strong class="nav-group-label">Reference</strong>
    <a href="{page_url(prefix, 'workflow/')}">ASPBE harness</a>
    <a href="{page_url(prefix, 'blueprint/')}">Verso Blueprint</a>
  </nav>
  <div class="sidebar-footer">
    <div class="theme-switcher" aria-label="Reading style">
      <button type="button" data-theme-choice="blueprint" aria-pressed="true">Book</button>
      <button type="button" data-theme-choice="modern" aria-pressed="false">Sans</button>
      <button type="button" data-theme-choice="bold" aria-pressed="false">High contrast</button>
    </div>
  </div>
</aside>"""


def verification_strip(
    prefix: str,
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    return f"""
<div class="verification-strip">
  <div class="verification-inner">
    <strong>Checked on this commit</strong>
    <span>{int(coverage['publicDeclarationCount']):,} public declarations</span>
    <span>commit <code>{html.escape(str(context['shortCommit']))}</code></span>
    <a href="{prefix}build-report.json">Build record</a>
  </div>
</div>"""


def page_template(
    *,
    title: str,
    route: str,
    current: str,
    body: str,
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
    toc: list[tuple[str, str]] | None = None,
    description: str = "QuantumComputinglib: a formal quantum computing textbook and the ASPBE Lean library",
    extra_scripts: tuple[str, ...] = (),
    extra_styles: tuple[str, ...] = (),
) -> str:
    prefix = prefix_for(route)
    toc_html = ""
    shell_class = "page-shell"
    if toc:
        toc_html = (
            '<aside class="toc" aria-label="On this page"><strong>On this page</strong>'
            + "".join(
                f'<a href="#{html.escape(anchor)}">{html.escape(label)}</a>'
                for anchor, label in toc
            )
            + "</aside>"
        )
    else:
        shell_class += " no-toc"
    extra_script_html = "".join(
        f'<script src="{prefix}{html.escape(path)}"></script>' for path in extra_scripts
    )
    extra_style_html = "".join(
        f'<link rel="stylesheet" href="{prefix}{html.escape(path)}">'
        for path in extra_styles
    )
    return f"""<!doctype html>
<html lang="en" data-theme="blueprint">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description)}">
  <title>{html.escape(title)} | QuantumComputinglib</title>
  <link rel="icon" href="{prefix}static/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}static/site.css">
  {extra_style_html}
  <script>
    window.MathJax = {{
      tex: {{inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']]}},
      options: {{skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']}}
    }};
  </script>
  <script src="{prefix}static/math-reader.js?v=20261021-2"></script>
  <script defer src="{prefix}static/vendor/mathjax@3.2.2/tex-mml-chtml.js"></script>
</head>
<body data-site-root="{prefix}">
  {site_header(prefix, current)}
  {verification_strip(prefix, coverage, gate, context)}
  <div class="{shell_class}">
    <main id="main-content">{body}</main>
    {toc_html}
  </div>
  <footer class="site-footer">
    <div class="footer-provenance">
      <div><strong>QuantumComputinglib</strong> is generated from the ASPBE Lean inventory in
        <a href="{PROJECT_REPOSITORY_URL}"><code>{PROJECT_REPOSITORY}</code></a>.</div>
      <div><strong>Organizers:</strong> {html.escape(', '.join(name for name, _ in ORGANIZERS))}.</div>
    </div>
    <nav aria-label="Footer">
      <a href="{page_url(prefix, 'organizers/')}">Organizers</a>
      <a href="{page_url(prefix, 'implementation-map/')}">Implementation map</a>
      <a href="{page_url(prefix, 'workflow/')}">ASPBE harness</a>
      <a href="{page_url(prefix, 'blueprint/')}">Verso Blueprint</a>
      <a href="{page_url(prefix, 'attribution/')}">License, reuse and attribution</a>
    </nav>
  </footer>
  <script src="{prefix}static/site.js"></script>
  {extra_script_html}
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
    if (window.matchMedia("(max-width: 760px)").matches) {{
      document.querySelectorAll(".mermaid").forEach((node) => {{
        node.textContent = node.textContent.replace(/^flowchart LR/m, "flowchart TB");
      }});
    }}
    mermaid.initialize({{
      startOnLoad: true,
      securityLevel: "strict",
      theme: "base",
      flowchart: {{curve: "linear", htmlLabels: true}},
      themeVariables: {{
        primaryColor: "#eaf1f2",
        primaryTextColor: "#1e2c36",
        primaryBorderColor: "#007e84",
        lineColor: "#71868e",
        secondaryColor: "#ffffff",
        tertiaryColor: "#f4f7f8",
        fontFamily: "system-ui, sans-serif"
      }}
    }});
  </script>
</body>
</html>
"""


def diagram(prefix: str, name: str, title: str) -> str:
    source = (WEBSITE_ROOT / "diagrams" / f"{name}.mmd").read_text(encoding="utf-8")
    return f"""
<figure class="diagram-panel" id="diagram-{html.escape(name)}">
  <figcaption class="diagram-toolbar">
    <strong>{html.escape(title)}</strong>
    <a href="{prefix}diagrams/{html.escape(name)}.mmd">editable Mermaid source</a>
  </figcaption>
  <pre class="mermaid">{html.escape(source)}</pre>
</figure>"""


TRACK_ORDER = (
    "Shared foundations",
    "State preparation",
    "Block encoding",
    "System and evidence",
)

BOOK_PARTS = (
    (
        "Part I · State Preparation",
        (1, 2, 3, 4),
        "Chapters 1–2 are shared foundations authored once and reused by Block Encoding; Chapters 3–4 specialize them to preparation certificates.",
    ),
    (
        "Part II · Block Encoding",
        (5, 6, 7, 8, 9),
        "Block Encoding reuses the same finite-matrix and circuit nodes, then adds projected-block, composition, resource and proof-gated construction obligations.",
    ),
)


def _chapter_link(link_prefix: str, chapter: dict[str, object]) -> str:
    return f"""
<a class="chapter-link" href="{link_prefix}chapters/{chapter['slug']}/index.html">
  <span class="chapter-number">{int(chapter['number']):02d}</span>
  <span class="chapter-copy">
    <strong>{html.escape(str(chapter['title']))}</strong>
    <span>{html.escape(str(chapter['summary']))}</span>
  </span>
  <span class="chapter-arrow" aria-hidden="true">&#8594;</span>
</a>"""


def render_chapter_groups(
    link_prefix: str, tracks: tuple[str, ...] | None = None
) -> str:
    groups: list[str] = []
    if tracks is None:
        by_number = {
            int(chapter["number"]): chapter
            for chapter in CHAPTERS
        }
        for label, numbers, note in BOOK_PARTS:
            chapters = [by_number[number] for number in numbers]
            links = "".join(_chapter_link(link_prefix, chapter) for chapter in chapters)
            groups.append(
                f'<section class="reading-track book-part"><h3>{html.escape(label)}</h3>'
                f'<p>{html.escape(note)}</p>'
                f'<div class="chapter-list">{links}</div></section>'
            )
        # Planned peer textbooks belong in the same book map, not a second tier.
        # Their chapter links lead to source-anchored plans, never invented roots.
        for part in load_json(WEBSITE_ROOT / "curriculum-parts.json")["parts"][2:]:
            target = page_url(link_prefix, str(part["route"]))
            links = "".join(
                f'<a class="chapter-link" href="{target}#{html.escape(str(chapter["id"]))}">'
                '<span class="chapter-number">Plan</span>'
                f'<span class="chapter-copy"><strong>{html.escape(str(chapter["title"]))}</strong>'
                f'<span>{html.escape(str(chapter["summary"]))}</span></span>'
                '<span class="chapter-arrow" aria-hidden="true">&#8594;</span></a>'
                for chapter in part["chapters"]
            )
            groups.append(
                f'<section class="reading-track book-part" data-curriculum-part="{part["id"]}">'
                f'<h3>{html.escape(str(part["label"]))} · {html.escape(str(part["title"]))}</h3>'
                f'{badge(str(part["status"]))}<p>{html.escape(str(part["summary"]))}</p>'
                f'<details><summary>Explore planned chapters (not local certificates)</summary>'
                f'<div class="chapter-list">{links}</div></details></section>'
            )
    else:
        for track in tracks:
            chapters = sorted(
                (chapter for chapter in CHAPTERS if chapter["track"] == track),
                key=lambda item: int(item["number"]),
            )
            links = "".join(_chapter_link(link_prefix, chapter) for chapter in chapters)
            groups.append(
                f'<section class="reading-track"><h3>{html.escape(track)}</h3>'
                f'<div class="chapter-list">{links}</div></section>'
            )
    return '<div class="reading-tracks">' + "".join(groups) + "</div>"

def render_math_2_0(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    body = """
<section class="hero math2-hero">
  <p class="eyebrow">QuantumComputinglib × Math 2.0</p>
  <h1>Proofs that grow human understanding</h1>
  <p class="lede">A living knowledge network and a quality Lean library support
  our core mission: explain quantum constructions clearly and teach their reusable ideas.</p>
  <p>ASPBE is the construction system; QuantumComputinglib is the library and
  teaching surface. State preparation and block encoding are the current focus.</p>
  <div class="hero-actions"><a class="button" href="../example-cases/index.html">Read a worked case</a>
  <a class="button secondary" href="../lean-graph/index.html">Explore the graph</a></div>
</section>
<section class="content-section" id="framing">
  <h2>Our original aims and the report</h2>
  <p>In <a href="https://teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf">Terence Tao's
  <em>Math 2.0</em> talk (Caltech, 2026)</a>, slides 18–21 put human understanding
  at the center of sustainable AI-assisted mathematics. Slides 22, 25 and 26 give
  nine examples of useful work. The map below is our interpretation of those
  examples, not an official nine-goal framework or an endorsement.</p>
  <p>Our original goals of connected knowledge, reusable Lean proofs and clearer quantum teaching predate and resonate with this report. We invite collaborators in quantum algorithms, formalization, education and mathematical AI to improve the teaching and test what proof maps can reveal.</p>
  <p><strong>Foundations (2, 3) → understanding (1, 8) → research agenda (4, 5, 6, 7, 9).</strong>
  Existing infrastructure gives us a starting point; each next step still needs its own evidence.</p>
</section>
<section class="content-section" id="foundations">
  <p class="eyebrow">Foundations</p><h2>Keep the knowledge connected and checkable</h2>
  <div class="math2-grid">
    <article class="math2-card" id="direction-2"><p class="path-label">02 · Living knowledge networks</p>
      <h3>Connect papers through reusable quantum mechanisms</h3>
      <p><strong>Existing:</strong> source-anchored paper maps, implementation records,
      a mechanism atlas and the shared Lean graph connect constructions and their obligations.</p>
      <p><strong>Next:</strong> update source and dependency records together so a changed
      assumption exposes every affected route.</p>
      <a href="../implementation-map/index.html">Inspect the implementation map →</a></article>
    <article class="math2-card" id="direction-3"><p class="path-label">03 · Quality formal libraries</p>
      <h3>Reuse one set of quantum foundations</h3>
      <p><strong>Existing:</strong> shared finite-matrix, circuit, state-preparation
      and block-encoding interfaces have a generated declaration inventory and publication gates.</p>
      <p><strong>Next:</strong> close missing semantic adapters and proof obligations;
      extend the library through reviewed reusable declarations.</p>
      <a href="../library/index.html">Browse the Lean library →</a></article>
  </div>
</section>
<section class="content-section" id="understanding">
  <p class="eyebrow">Core value</p><h2>Turn certificates into explanations people can use</h2>
  <div class="math2-grid">
    <article class="math2-card" id="direction-1"><p class="path-label">01 · Open exposition problems</p>
      <h3>Explain why a construction works</h3>
      <p><strong>Existing:</strong> proof-digestion records and theorem-linked
      figures expose the registers, normalization, projection and resource model behind a circuit.</p>
      <p><strong>Next:</strong> compress repetitive bookkeeping into reusable conceptual
      moves, with lossless links back to assumptions and Lean. The Functor Hypergraph
      is a navigation lens; categorical correctness requires separate certificates.</p>
      <a href="../case-studies/robin/index.html">Read the Robin construction map →</a></article>
    <article class="math2-card" id="direction-8"><p class="path-label">08 · Interactive texts and presentations</p>
      <h3>Read the idea, statement and proof together</h3>
      <p><strong>Existing:</strong> the book map, worked cases, natural-language/Lean
      views and graph navigation offer several routes into the same mathematics.</p>
      <p><strong>Next:</strong> improve motivated reading paths and reader evaluation.
      Parts III–IV are source-anchored curricula with local certificates still pending.</p>
      <a href="../learning/index.html">Start with the reading guide →</a></article>
  </div>
</section>
<section class="content-section" id="research-agenda">
  <p class="eyebrow">Research agenda</p><h2>Use the graph to ask better questions</h2>
  <div class="math2-grid">
    <article class="math2-card" id="direction-4"><p class="path-label">04 · Principles, methods and insights</p>
      <h3>Make mathematical cross-pollination visible</h3>
      <p><strong>Existing:</strong> the Hermite–Bernstein/tensor-train case and shared
      preparation/block-encoding graph expose structural connections.</p>
      <p><strong>Next:</strong> test whether a shared mechanism transfers to a new
      construction. A graph shortcut suggests a question; a checked bridge supplies evidence.</p>
      <a href="../example-cases/hermite-smooth-state-preparation/index.html">Explore the structured-state case →</a></article>
    <article class="math2-card" id="direction-5"><p class="path-label">05 · Theorem-level ablation studies</p>
      <h3>Ask which proof tools are actually needed</h3>
      <p><strong>Existing:</strong> source-blind encoder–denoiser review reconstructs
      meaning from Lean and audits hidden hypotheses. This is infrastructure for ablations.</p>
      <p><strong>Next:</strong> fix the same conclusion, remove a named theory or proof
      input, then supply another proof or a precise obstruction. Harness-route ablations
      measure a different question and do not establish this result.</p>
      <a href="../workflow/index.html">Inspect the review workflow →</a></article>
    <article class="math2-card" id="direction-6"><p class="path-label">06 · Theorem neighborhoods</p>
      <h3>Vary a condition and track what survives</h3>
      <p><strong>Existing:</strong> exact/approximate contracts and explicit oracle,
      register, ancilla and normalization boundaries identify what may be varied.</p>
      <p><strong>Next:</strong> weaken a condition, trace affected graph edges, and
      check a generalization or a counterexample under a new sealed statement.</p>
      <a href="../block-encoding/index.html">Explore the block-encoding contracts →</a></article>
    <article class="math2-card" id="direction-7"><p class="path-label">07 · Interpretable open math models</p>
      <h3>Provide auditable mathematical task material</h3>
      <p><strong>Existing:</strong> concise Lean interfaces, natural-language counterparts,
      source links and typed failed routes can support explainable mathematical tools.</p>
      <p><strong>Next:</strong> curate training/evaluation packets from our own or
      appropriately licensed exposition/proof pairs and test semantic fidelity.
      External references are not automatically eligible model data.
      We do not claim a trained model or certified safety;
      visible explanations do not expose a model's private internal reasoning.</p>
      <a href="../community/index.html">See the contribution packet →</a></article>
    <article class="math2-card" id="direction-9"><p class="path-label">09 · Model failure and misalignment</p>
      <h3>Show where a certificate stops applying</h3>
      <p><strong>Existing:</strong> the library separates ideal circuits, exact-real
      resource models, finite diagnostics, finite-bit synthesis and external application assumptions.</p>
      <p><strong>Next:</strong> expose boundary violations, misleading oracle costs
      and model hallucinations through explicit failure cases. A model-level counterexample
      or Lean proof alone does not certify real hardware reliability.</p>
      <a href="../example-cases/hermite-smooth-state-preparation/index.html">Read an explicit finite-bit boundary →</a></article>
  </div>
</section>
"""
    return page_template(
        title="Our place in Math 2.0", route="math-2-0/", current="math-2-0/",
        body=body, coverage=coverage, gate=gate, context=context,
        toc=[("framing", "The report"), ("foundations", "Foundations · 2, 3"),
             ("understanding", "Core value · 1, 8"), ("research-agenda", "Research agenda")],
        description="QuantumComputinglib's Math 2.0 mission: connected Lean knowledge, clearer quantum proofs, interactive teaching and explicit model boundaries.",
    )


def render_gate_examples() -> str:
    return r"""
<div class="gate-example-grid" aria-label="One-qubit state-preparation examples">
  <article class="gate-example state-example">
    <div class="wire" aria-hidden="true"><span>|0&gt;</span><b>H</b><span>|+&gt;</span></div>
    <h3>Hadamard prepares a superposition</h3>
    <div class="example-math">\(H|0\rangle=(|0\rangle+|1\rangle)/\sqrt{2}\)</div>
    <p>The two computational-basis amplitudes have equal magnitude.</p>
  </article>
  <article class="gate-example x-example">
    <div class="wire" aria-hidden="true"><span>|0&gt;</span><b>X</b><span>|1&gt;</span></div>
    <h3>Pauli X swaps the basis states</h3>
    <div class="example-math">\(X|0\rangle=|1\rangle,\quad X|1\rangle=|0\rangle\)</div>
    <p>This is a basis-state preparation, not an arbitrary superposition.</p>
  </article>
</div>"""


def render_home(
    inventory: dict[str, object],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    prefix = "./"
    declarations = inventory["declarations"]
    experimental = sum(bool(item["experimental"]) for item in declarations)
    open_proofs = sum(bool(item.get("openProof")) for item in declarations)
    body = rf"""
<section class="hero home-hero">
  <p class="eyebrow">Human-understanding infrastructure for Math 2.0</p>
  <h1>QuantumComputinglib</h1>
  <p class="lede">Understand a quantum construction. Read its proof beside Lean.
  Follow the shared ideas and see exactly which assumptions it needs.</p>
  <p class="hero-scope"><strong>ASPBE</strong> constructs and certifies state preparation
  and block encoding. The library connects those certificates to readable
  mathematics, circuit figures and reusable proof graphs.</p>
  <div class="hero-actions">
    <a class="button state-button" href="learning/index.html">Start reading</a>
    <a class="button secondary" href="example-cases/index.html">Explore a worked case</a>
    <a class="text-link" href="lean-graph/index.html">Inspect the Lean graph &#8594;</a>
  </div>
  <div class="home-book-links" aria-label="Four textbook parts">
    <a href="state-preparation/index.html">Part I · State Preparation</a>
    <a href="block-encoding/index.html">Part II · Block Encoding</a>
    <a href="quantum-information/index.html">Part III · QIT &amp; Representation</a>
    <a href="quantum-scientific-computing/index.html">Part IV · Scientific Computing</a>
  </div>
  <p class="evidence-note">Parts I–II: core certificates and open routes. Parts III–IV:
  source-anchored curricula; local Lean certificates pending.</p>
</section>
<section class="content-section math2-intro" id="math-2-0">
  <p class="eyebrow">From checked results to shared understanding</p>
  <h2>Our place in Math 2.0</h2>
  <p>Terence Tao's <a href="https://teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf"><em>Math 2.0</em> talk</a>
  echoes our original aim: a living quantum textbook with inspectable proofs,
  reusable mechanisms and explicit model boundaries. We invite collaborators to
  improve the teaching and explore the potential of proof maps.</p>
  <p><strong>Foundations:</strong> a living knowledge network and a quality Lean library.
  <strong>Core value:</strong> clearer explanations and better interactive teaching.
  <strong>Research agenda:</strong> shared principles, ablations, theorem neighborhoods,
  auditable AI tools and model-failure analysis.</p>
  <a class="text-link" href="math-2-0/index.html">Nine contribution directions: what exists and what comes next &#8594;</a>
</section>
<section class="content-section" id="applications">
  <div class="section-heading">
    <p class="eyebrow">Choose the problem first</p>
    <h2>Four textbook parts, one shared Lean graph</h2>
    <p>Four peer parts share the same foundations. Within Parts I and II, the main construction relation is State Preparation → Block Encoding:
    PREPARE is a reusable subproblem inside many block-encoding routes. A
    block-to-state consumer path also exists, but it is not the inclusion relation
    and it needs extra branch, normalization and amplification hypotheses. Shared
    foundations are authored once rather than duplicated.</p>
  </div>
  <div class="application-paths">
    <article class="application-path state-path">
      <p class="path-label">Part I</p>
      <h3>State preparation</h3>
      <div class="contract-equation">\[U|0^n\rangle=|\psi\rangle\]</div>
      <p>Fix a normalized target state, construct a unitary, and prove that its
      action on the all-zero state gives exactly those amplitudes.</p>
      <a href="state-preparation/index.html">Read the state-preparation route &#8594;</a>
    </article>
    <article class="application-path block-path">
      <p class="path-label">Part II</p>
      <h3>Block encoding</h3>
      <div class="contract-equation">\[\Pi U\Pi^\dagger=A/\alpha\]</div>
      <p>Fix an operator, normalization, ancilla convention, and register order;
      then prove that the projected block of a larger unitary has the requested value.</p>
      <a href="block-encoding/index.html">Read the block-encoding route &#8594;</a>
    </article>
    <article class="application-path">
      <p class="path-label">Part III · Planned</p>
      <h3>Quantum Information and Representation Theory</h3>
      <p>States, channels and measurements lead to symmetry, Schur–Weyl duality
      and information-theoretic applications. Leditzky's notes anchor the
      curriculum; named local Lean roots are still required.</p>
      <a href="quantum-information/index.html">Explore the representation-theoretic QIT curriculum &#8594;</a>
    </article>
    <article class="application-path">
      <p class="path-label">Part IV · Planned</p>
      <h3>Quantum Algorithms for Scientific Computation</h3>
      <p>Lin–Wiebe's scientific algorithms reuse the shared Block Encoding part,
      then add transforms, simulation, estimation and application contracts.</p>
      <a href="quantum-scientific-computing/index.html">Explore scientific quantum algorithms &#8594;</a>
    </article>
  </div>
  {diagram(prefix, "quantum-domain-roadmap", "Four peer textbooks and their shared foundations — a curriculum map, not new Lean implications")}
</section>
<section class="content-section process-section state-section" id="state-process">
  <div class="section-heading">
    <p class="eyebrow">State-preparation workflow</p>
    <h2>From a target vector to a preparation certificate</h2>
    <p>Normalization, unitarity, and state action are separate obligations. The
    first-column identity is the matrix form of the same state-action equation.</p>
  </div>
  {diagram(prefix, "state-preparation-flow", "State-preparation proof and export flow")}
</section>
<section class="content-section process-section block-section" id="block-process">
  <div class="section-heading">
    <p class="eyebrow">Block-encoding workflow</p>
    <h2>From an operator contract to a clean-block certificate</h2>
    <p>This route introduces choices that state preparation does not need: ancilla
    count, a clean projector, register layout, normalization \(\alpha\), and an
    exact or approximate block norm.</p>
  </div>
  {diagram(prefix, "block-encoding-flow", "Block-encoding proof and export flow")}
</section>
<section class="content-section" id="evidence">
  <div class="section-heading">
    <p class="eyebrow">Current checkout</p>
    <h2>What this build actually certifies</h2>
  </div>
  <div class="metric-strip">
    <div class="metric"><strong>{int(coverage['publicDeclarationCount']):,}</strong><span>explicit public declarations</span></div>
    <div class="metric"><strong>{int(coverage['sourceDocstringCount']):,}</strong><span>source docstrings</span></div>
    <div class="metric"><strong>{experimental:,}</strong><span>experimental declarations</span></div>
    <div class="metric"><strong>{open_proofs:,}</strong><span>explicit incomplete proofs</span></div>
    <div class="metric"><strong>{len(CHAPTERS)}</strong><span>guided learning chapters</span></div>
  </div>
  <p class="evidence-note"><strong>Compiled</strong> means the Lean and test gates
  passed on commit <code>{html.escape(str(context['shortCommit']))}</code>. A contract
  record may compile even when a concrete construction route is still partial; the
  site shows those two statuses separately.</p>
</section>
<section class="content-section" id="pipeline">
  <div class="section-heading">
    <p class="eyebrow">Shared evidence discipline</p>
    <h2>What happens after either contract is fixed</h2>
    <p>ASPBE explores candidates, records why routes fail, and lets Lean decide
    formal promotion. A Qiskit check is useful finite evidence after certification;
    it does not prove a symbolic family.</p>
  </div>
  {diagram(prefix, "certificate-pipeline", "Shared certification and feedback loop")}
</section>
<section class="content-section" id="use">
  <div class="section-heading">
    <p class="eyebrow">Use the project</p>
    <h2>Read, formalize, or submit a construction</h2>
    <p>The public site is not only a declaration catalog. It keeps the original
    user-facing task builder, the local-compilation workspace, and the reviewed
    contribution route beside the textbook.</p>
  </div>
  <div class="use-paths">
    <article><span>Read</span><h3>Learn from a checked chapter</h3><p>Follow a formula from its physical meaning to the exact Lean declaration.</p><a href="learning/index.html">Open the book map &#8594;</a></article>
    <article><span>Formalize</span><h3>Compare LaTeX and Lean</h3><p>Edit a theorem, inspect dependencies, and compile temporary code with the local companion.</p><a href="ide/index.html">Open the workspace &#8594;</a></article>
    <article><span>Run</span><h3>Build an ASPBE task packet</h3><p>Describe a target state or operator, choose a harness, and export a reproducible task packet.</p><a href="task-builder/index.html">Open the task builder &#8594;</a></article>
  </div>
</section>
<section class="content-section" id="news">
  <div class="section-heading">
    <p class="eyebrow">Project record</p>
    <h2>News and auditable priority</h2>
    <p>The dates below are repository milestones. They do not replace the
    generated proof-status pages.</p>
  </div>
  <ol class="milestone-list">
    <li><time datetime="2026-10-21">21 October 2026</time><div><strong>QuantumComputingBench starts.</strong><p>We are launching <a href="{PROJECT_REPOSITORY_URL}/tree/main/benchmarks/quantumcomputingbench">QuantumComputingBench</a> to build graph-grounded QA for training and evaluating specialized quantum-computing models across knowledge, mathematical reasoning and Lean skills, with planned topics clearly separated from verified library evidence.</p></div></li>
    <li><time datetime="2026-10-18">18 October 2026</time><div><strong>Priority: digesting discovered reversible circuits.</strong><p>We have opened a source-first formalization route for <a href="https://arxiv.org/abs/2610.22367v1">Gu, Kemeny, Yelin and Lukin</a>, explicitly crediting the author Lean proofs and separating their adaptation from circuit, error and resource closure. <a href="state-preparation-wiki/spw-uncompute/index.html">Read the layered Uncompute plan →</a>. Work in progress; no paper-wide or new local certificate is claimed.</p></div></li>
    <li><time datetime="2026-10-10">10 October 2026</time><div><strong>Four textbooks you can browse, not just a roadmap.</strong><p>All four peer textbooks have homepage actions, a shared curriculum diagram and chapter-map entries. The <a href="learning/index.html#textbook-explorer">textbook explorer</a> filters chapters by book, technique and evidence status, with reading sources and expandable commit-pinned OpenAI Math memory. Parts III and IV remain source-anchored plans, not newly certified Lean books. The first curriculum release was merged in <a href="https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/pull/87">PR #87</a>; rendering and deployed-reader checks were repaired in <a href="https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/pull/88">#88</a> and <a href="https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/pull/89">#89</a>.</p></div></li>
    <li><time datetime="2026-10-09">9 October 2026</time><div><strong>Four peer textbook parts and explicit formalization plans.</strong><p>State Preparation and Block Encoding are joined by Quantum Information and Representation Theory, and Quantum Algorithms for Scientific Computation. Walsh-series and diagonal-operator papers have source-linked plans and reusable technical cards. New parts and upstream OpenAI Math placements are planned curriculum, not new local theorem certificates.</p></div></li>
    <li><time datetime="2026-10-06">6 October 2026</time><div><strong>Statement Seal, evidence memory, and proof digestion.</strong><p>QuantumComputinglib now freezes source-facing quantum contracts before proof search, types and salvages failed routes before cleanup, keeps environment/API failures separate from mathematical refutation, defaults routine coordination to deterministic/low-token control in light of local route-ablation evidence, requires distinct uncertainty for parallel Workers, and seals PURIFIED reader explanations against the source and Lean graphs.</p></div></li>
    <li><time datetime="2026-09-10">10 September 2026</time><div><strong>Schrödingerisation smooth auxiliary-state preparation: a structured logical resource bound.</strong><p>The smooth auxiliary \(p\)-register state required by <a href="https://arxiv.org/abs/2403.19123v3">Jin–Liu–Ma’s PDE Schrödingerisation construction</a>, viewed alongside the smooth-function state-preparation route of <a href="https://arxiv.org/abs/2005.04351">Holmes–Matsuura</a>, has exact Hermite–Bernstein/tensor-train structure. The logical bound is \(G\le48n_p(2k+6)^3\), hence \(O(n_p)\) for fixed \(k\), with \(O(\log k)\) workspace under the stated exact-real contracts. This is not a complete finite-bit algorithm certificate: classical core generation, arithmetic and gate synthesis for <code>SP-HERMITE-POLY-002</code> still need separate certification. <a href="example-cases/hermite-smooth-state-preparation/index.html">Read the worked case and its scope →</a></p></div></li>
    <li><time datetime="2026-08-14">14 August 2026</time><div><strong>Robin boundary block encoding: a smaller certified primitive.</strong><p>For the selected \(n=3\) Robin boundary instance in <a href="https://arxiv.org/abs/2406.18072">Guseynov–Huang–Liu, <em>Block encoding by signal processing</em></a>, ASPBE reduced the audited \(T^{{\dagger 3}}\) branch from 49 to 30 \(T^{{\dagger 3}}\) gates and from 52 to 32 CNOTs, with the same five qubits and zero ancillas under the fixed primitive model.</p></div></li>
    <li><time datetime="2026-08-10">10 August 2026</time><div><strong>ASPBE and QuantumComputinglib.</strong><p>The two application tracks, local workspace, task builder, and contributor review path are presented in one site.</p></div></li>
    <li><time datetime="2026-07">July 2026</time><div><strong>Blueprint and Library Explorer.</strong><p>One generated inventory now drives the checked Blueprint catalog and searchable declaration browser.</p></div></li>
    <li><time datetime="2026-06">June 2026</time><div><strong>Public testing preview.</strong><p>The site exposed separate State Preparation and Block Encoding directions and the user task builder.</p></div></li>
    <li><time datetime="2026-05-17">17 May 2026</time><div><strong>Earliest repository record.</strong><p>The <a href="https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/commit/af59b03c58c2cedec52b14a80b4d909031d62521">initial commit</a> and <a href="https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/af59b03c58c2cedec52b14a80b4d909031d62521/MANIFEST.md">timestamped manifest</a> begin the public, auditable project history. No earlier date is asserted without evidence.</p></div></li>
  </ol>
</section>
<section class="content-section" id="chapters">
  <div class="section-heading">
    <p class="eyebrow">Reading guide</p>
    <h2>Browse all four textbook chapter maps</h2>
    <p><a class="button secondary" href="learning/index.html#textbook-explorer">Search by textbook, technique or proof status &#8594;</a></p>
  </div>
  {render_chapter_groups('')}
</section>
<section class="content-section" id="navigation">
  <div class="section-heading">
    <p class="eyebrow">Audit the source</p>
    <h2>Explanation, inventory, and checked Blueprint</h2>
    <p>The chapters teach selected results. The Library Explorer inventories every
    explicit public declaration. The Verso Blueprint resolves its Lean references
    during the build.</p>
  </div>
  <div class="link-row">
    <a class="button secondary" href="implementation-map/index.html">Implementation map</a>
    <a class="button secondary" href="library/index.html">Library Explorer</a>
    <a class="button secondary" href="blueprint/html-multi/index.html">Verso Blueprint</a>
    <a class="text-link" href="task-builder/index.html">Task builder &#8594;</a>
  </div>
</section>"""
    toc = [
        ("math-2-0", "Our place in Math 2.0"),
        ("applications", "Four textbook parts"),
        ("state-process", "State preparation"),
        ("block-process", "Block encoding"),
        ("evidence", "Build evidence"),
        ("pipeline", "Shared verification"),
        ("use", "Use the project"),
        ("news", "News"),
        ("chapters", "Learning chapters"),
        ("navigation", "Source views"),
    ]
    return page_template(
        title="Overview",
        route="",
        current="",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=toc,
    )


def curriculum_part(part_id: str) -> dict[str, object]:
    catalog = load_json(WEBSITE_ROOT / "curriculum-parts.json")
    return next(part for part in catalog["parts"] if part["id"] == part_id)


def render_curriculum_chapters(part: dict[str, object], prefix: str) -> str:
    cards: list[str] = []
    for chapter in part["chapters"]:
        href = str(chapter.get("href", ""))
        title = html.escape(str(chapter["title"]))
        if href:
            title_html = f'<a href="{page_url(prefix, href)}">{title}</a>'
        else:
            title_html = title
        cluster_html = render_curriculum_intake(chapter)
        cards.append(
            f'''<article class="application-path" id="{html.escape(str(chapter["id"]))}">
  <p class="path-label">{html.escape(str(chapter["id"]))}</p>
  <h3>{title_html}</h3>
  <p>{html.escape(str(chapter["summary"]))}</p>
  {badge(str(chapter["status"]))}
  {cluster_html}
</article>'''
        )
    return '<div class="application-paths">' + "".join(cards) + "</div>"


def render_curriculum_intake(chapter: dict[str, object]) -> str:
    """Expose the pinned intake, never infer local theorem admission from it."""
    ids = chapter.get("oaiClusters", [])
    if not ids:
        return ""
    intake = load_json(ROOT / "research-wiki/openai-math-2026-intake.json")
    commit = str(intake["upstream"]["commit"])
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Curriculum upstream links require an exact commit")
    clusters = {item["id"]: item for item in intake["clusters"]}
    rows = []
    for cluster_id in ids:
        cluster = clusters[cluster_id]
        paths = ([cluster["path"]] if "path" in cluster
                 else [item["path"] for item in cluster["paths"]])
        links = []
        for path in paths:
            if (not str(path).startswith(("lean/OAI/", "preprints/"))
                    or ".." in str(path).split("/") or "\\" in str(path)):
                raise ValueError("Unsafe upstream curriculum path")
            url = f"https://github.com/openai/math/tree/{commit}/{quote(str(path), safe='/')}"
            links.append(f'<a href="{url}">{html.escape(str(path).removeprefix("lean/OAI/"))}</a>')
        verification = cluster["upstream_verification"]
        action = cluster.get("next_action", "A local semantic adapter and independent publication review are still required.")
        rows.append(f'''<li><strong>{html.escape(str(cluster_id))}</strong>
  <p>{' · '.join(links)}</p>
  <p>{html.escape(str(cluster.get('local_role', 'Candidate circuit-model and resource adapter.')))}</p>
  <p class="hint">Upstream evidence: {html.escape(str(verification['status']))}. {html.escape(str(cluster['class']))}. Not local admission.</p>
  <p><strong>Next boundary:</strong> {html.escape(str(action))}</p></li>''')
    return f'''<details class="curriculum-intake"><summary>Inspect pinned upstream memory ({len(rows)} routes)</summary>
  <p>OpenAI Math snapshot <code>{commit[:12]}</code> · upstream Lean 4.34.1 · local migration target 4.33.0.
  Source placement does not certify an adapter, the whole chapter, or an SP/BE construction.</p>
  <ul>{''.join(rows)}</ul></details>'''


def render_curriculum_explorer(prefix: str) -> str:
    """One searchable view of the canonical catalog; all cards work without JS."""
    catalog = load_json(WEBSITE_ROOT / "curriculum-parts.json")
    sources = {item["id"]: item for item in load_json(WEBSITE_ROOT / "research/sources.json")["sources"]}
    cards = []
    options = []
    for part in catalog["parts"]:
        options.append(f'<option value="{part["id"]}">{html.escape(str(part["label"]))} · {html.escape(str(part["title"]))}</option>')
        source_links = ' · '.join(
            f'<a href="{html.escape(str(sources[source_id]["url"]))}">{html.escape(str(sources[source_id]["title"]))}</a>'
            for source_id in part["sourceIds"]
        )
        for chapter in part["chapters"]:
            # Keep the landing anchor: a planned chapter is not a fabricated lesson.
            href = f'{prefix}{part["route"]}index.html#{chapter["id"]}'
            if chapter.get("href"):
                href = page_url(prefix, str(chapter["href"]))
            search = ' '.join(str(value) for value in (
                part["title"], chapter["title"], chapter["summary"],
                *chapter.get("oaiClusters", []),
                *(sources[source_id]["title"] for source_id in part["sourceIds"]),
            ))
            cards.append(f'''<article class="curriculum-card" data-curriculum-card
  data-part="{part['id']}" data-status="{chapter['status']}" data-search="{html.escape(search, quote=True)}">
  <p class="path-label">{html.escape(str(part['label']))} · {html.escape(str(part['title']))}</p>
  <h3><a href="{html.escape(href)}">{html.escape(str(chapter['title']))}</a></h3>
  {badge(str(chapter['status']))}
  <p>{html.escape(str(chapter['summary']))}</p>
  <details class="curriculum-sources"><summary>Textbook / paper sources</summary><p>{source_links}</p>
    <p class="hint">These are reading anchors, not a claim that every source theorem is formalized.</p></details>
  {render_curriculum_intake(chapter)}
</article>''')
    return f'''<section class="content-section" id="textbook-explorer" data-curriculum-explorer>
  <div class="section-heading"><p class="eyebrow">Choose what to learn</p>
    <h2>Search all four textbooks</h2><p>Find a chapter, its reading source and the exact upstream memory assigned to it.
    Compiled means the listed local core, not a completed source book; Partial route and Planned keep their open boundaries.</p></div>
  <div class="curriculum-controls" data-curriculum-controls hidden>
    <label>Chapter or technique<input type="search" data-curriculum-query placeholder="Walsh, Schur, channels, Fourier…"></label>
    <label>Textbook<select data-curriculum-part><option value="">All four parts</option>{''.join(options)}</select></label>
    <label>Evidence status<select data-curriculum-status><option value="">All statuses</option>
      <option>Compiled</option><option>Partial route</option><option>Planned</option></select></label>
    <button class="button secondary" type="button" data-curriculum-reset>Reset filters</button>
  </div>
  <p class="hint" data-curriculum-count role="status" aria-live="polite">{len(cards)} chapter entries. All visible without JavaScript.</p>
  <p data-curriculum-empty hidden>No matching chapter. Try a broader term or reset the filters.</p>
  <div class="curriculum-grid">{''.join(cards)}</div>
</section>'''


def render_curriculum_part(
    part: dict[str, object],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    source_url = str(part.get("sourceUrl", ""))
    source_link = (
        f'<a class="text-link" href="{html.escape(source_url)}">Read the curriculum anchor &#8594;</a>'
        if source_url else ""
    )
    body = f'''
<section class="hero curriculum-hero">
  <p class="eyebrow">{html.escape(str(part["label"]))} · {badge(str(part["status"]))}</p>
  <h1>{html.escape(str(part["title"]))}</h1>
  <p class="lede">{html.escape(str(part["summary"]))}</p>
  {source_link}
</section>
<section class="content-section" id="truth-boundary">
  <div class="section-heading"><p class="eyebrow">Truth boundary</p><h2>Placement is not proof</h2></div>
  <p>{html.escape(str(load_json(WEBSITE_ROOT / "curriculum-parts.json")["truthBoundary"]))}</p>
  <div class="callout"><strong>OpenAI Math boundary.</strong> Audited clusters are pinned source or adapter inputs. Their upstream Lean 4.34.1 results are not local Lean 4.33.0 declarations until separately ported and compiled. Lean 4.33.0 is the migration target; this reader release preserves the published proof tree and records its actual version in the build evidence.</div>
</section>
<section class="content-section" id="chapter-map">
  <div class="section-heading"><p class="eyebrow">Graph-driven chapter map</p><h2>Shared foundations first, source-specific consumers later</h2></div>
  {render_curriculum_chapters(part, '../')}
  <p><a class="button secondary" href="../learning/index.html#textbook-explorer">Search across all four textbooks &#8594;</a></p>
</section>'''
    return page_template(
        title=str(part["title"]), route=str(part["route"]), current=str(part["route"]),
        body=body, coverage=coverage, gate=gate, context=context,
        toc=[("truth-boundary", "Truth boundary"), ("chapter-map", "Chapter map")],
        description=str(part["summary"]),
    )


def render_state_preparation(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    body = rf"""
<section class="hero application-hero state-hero">
  <p class="eyebrow">Part I · nested preparation layer</p>
  <h1>State preparation</h1>
  <p class="lede">Given a normalized target \(|\psi\rangle\), construct a unitary
  \(U\) that sends the all-zero state to it. ASPBE treats this as its own synthesis
  and proof problem, with its own exact and approximate acceptance predicates.</p>
  <div class="hero-contract">\[U|0^n\rangle=|\psi\rangle\]</div>
</section>
<section class="content-section" id="first-example">
  <div class="section-heading">
    <p class="eyebrow">One qubit is enough to see the contract</p>
    <h2>Two familiar gates, two concrete targets</h2>
    <p>The Hadamard statement is correct: it prepares the equal superposition from
    \(|0\rangle\). Pauli \(X\) exchanges \(|0\rangle\) and \(|1\rangle\).</p>
  </div>
  {render_gate_examples()}
</section>
<section class="content-section" id="preparation-flow">
  <div class="section-heading">
    <p class="eyebrow">Standalone certificate inside the broader toolchain</p>
    <h2>What ASPBE has to establish</h2>
    <p>The target must be normalized. The proposed matrix must be unitary. Finally,
    its action on the zero ket, equivalently its first column, must match every
    target amplitude.</p>
  </div>
  {diagram('../', 'state-preparation-flow', 'State-preparation proof and export flow')}
</section>
<section class="content-section" id="certificate-anatomy">
  <div class="section-heading">
    <p class="eyebrow">Certificate anatomy</p>
    <h2>Three facts travel together</h2>
  </div>
  <dl class="concept-list">
    <div><dt>Normalized target</dt><dd>The requested amplitude vector has unit norm.</dd></div>
    <div><dt>Unitary candidate</dt><dd>The circuit matrix preserves inner products, not merely the first column.</dd></div>
    <div><dt>State action</dt><dd>Applying the candidate to \(|0^n\rangle\) returns the requested vector.</dd></div>
  </dl>
  <p>A preparation circuit may later become a PREPARE component in an LCU or
  purification construction. That downstream block-encoding theorem remains a
  separate proof obligation.</p>
</section>
<section class="content-section" id="state-reading">
  <div class="section-heading">
    <p class="eyebrow">Continue reading</p>
    <h2>State-preparation chapters</h2>
  </div>
  {render_chapter_groups('../', ('State preparation',))}
</section>
<section class="content-section" id="state-frontiers">
  <div class="section-heading">
    <p class="eyebrow">Source-audited additions · not yet compiled roots</p>
    <h2>Walsh series and diagonal-filter suppliers</h2>
  </div>
  {render_curriculum_chapters(curriculum_part('part-i-state-preparation'), '../')}
</section>"""
    return page_template(
        title="State preparation",
        route="state-preparation/",
        current="state-preparation/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[
            ("first-example", "One-qubit examples"),
            ("preparation-flow", "Proof route"),
            ("certificate-anatomy", "Certificate anatomy"),
            ("state-reading", "Chapters"),
            ("state-frontiers", "Planned frontiers"),
        ],
    )


def render_block_encoding(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    body = rf"""
<section class="hero application-hero block-hero">
  <p class="eyebrow">Part II · encompassing block-encoding layer</p>
  <h1>Block encoding</h1>
  <p class="lede">Given an operator \(A\), place the scaled operator inside a
  larger unitary. The contract says exactly which ancilla block is selected and
  how normalization and approximation are interpreted.</p>
  <div class="hero-contract">\[\left\|A-\alpha\Pi U\Pi^\dagger\right\|\le\varepsilon\]</div>
</section>
<section class="content-section" id="block-contract">
  <div class="section-heading">
    <p class="eyebrow">Read the notation before the circuit</p>
    <h2>Four choices determine the contract</h2>
  </div>
  <dl class="concept-list block-concepts">
    <div><dt>Ancillas</dt><dd>Extra qubits make room for the larger unitary and are projected onto a declared clean state.</dd></div>
    <div><dt>Register order</dt><dd>The index convention identifies which matrix rows and columns form the signal block.</dd></div>
    <div><dt>Normalization \(\alpha\)</dt><dd>The selected block represents \(A/\alpha\), so the scale is part of correctness.</dd></div>
    <div><dt>Error \(\varepsilon\)</dt><dd>Exact encoding has zero error; approximate routes must name both a norm and a tolerance.</dd></div>
  </dl>
</section>
<section class="content-section" id="encoding-flow">
  <div class="section-heading">
    <p class="eyebrow">Encompassing construction certificate</p>
    <h2>What ASPBE has to establish</h2>
    <p>A candidate is not accepted because one small matrix looks right. The layout,
    unitarity, projected block, scale, and declared resource record are checked as
    separate obligations.</p>
  </div>
  {diagram('../', 'block-encoding-flow', 'Block-encoding proof and export flow')}
</section>
<section class="content-section" id="block-frontiers">
  <div class="section-heading">
    <p class="eyebrow">Source-audited additions · not yet compiled roots</p>
    <h2>Diagonal operators and structured Fourier suppliers</h2>
  </div>
  {render_curriculum_chapters(curriculum_part('part-ii-block-encoding'), '../')}
</section>
<section class="content-section" id="connection">
  <div class="section-heading">
    <p class="eyebrow">The main inclusion-like connection</p>
    <h2>State Preparation supplies a nested PREPARE subproblem</h2>
  </div>
  <p>A certified state-preparation circuit can supply a PREPARE oracle for an LCU,
  Gram, or purification-based construction. Its first-column theorem becomes a
  dependency; it does not by itself prove the clean-block identity.</p>
  <div class="link-row">
    <a class="button block-button" href="../chapters/block-encoding/index.html">Read the block contract</a>
    <a class="button secondary" href="../chapters/classic-routes/index.html">Compare construction routes</a>
    <a class="text-link" href="../chapters/certified-cases/index.html">See certified cases &#8594;</a>
  </div>
</section>"""
    return page_template(
        title="Block encoding",
        route="block-encoding/",
        current="block-encoding/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[
            ("block-contract", "Contract terms"),
            ("encoding-flow", "Proof route"),
            ("block-frontiers", "Planned frontiers"),
            ("connection", "Prepared-state inputs"),
        ],
    )


def result_card(
    result: dict[str, object],
    declaration: dict[str, object],
    declarations: dict[str, dict[str, object]],
    prefix: str,
) -> str:
    dependencies = []
    for dependency in result["dependencies"]:
        dependencies.append(f"<code>{html.escape(str(dependency))}</code>")
    steps = "".join(
        "<tr>"
        f"<td>{html.escape(natural)}</td>"
        f"<td><code>{html.escape(lean)}</code></td>"
        "</tr>"
        for natural, lean in result["correspondence"]
    )
    external = declaration.get("sourceUrl")
    source_links = (
        f'<a href="{html.escape(str(external))}">commit-pinned GitHub source</a>'
        if external
        else "<span class=\"muted\">No external source link: this file is not publishable at the detected ref.</span>"
    )
    route_closures = "".join(
        f'<li><a href="{module_url(prefix, declarations[str(root)])}">'
        f'<code>{html.escape(str(root))}</code></a></li>'
        for root in result["route_closures"]
    )
    return f"""
<article class="result" id="{declaration_anchor(str(result['declaration']))}">
  <div class="result-header">
    <div>
      <p class="eyebrow">Lean result</p>
      <h3>{html.escape(str(result['title']))}</h3>
      <code class="declaration-name">{html.escape(str(result['declaration']))}</code>
    </div>
    <div class="status-pair">
      <span><small>Declaration</small>{badge(str(result['local_status']))}</span>
      <span><small>Full route</small>{badge(str(result['route_status']))}</span>
    </div>
  </div>
  <div class="math-block">\\[{html.escape(str(result['math']))}\\]</div>
  <div class="result-story">
    <section>
      <h4>What it says</h4>
      <p>{html.escape(str(result['plain']))}</p>
    </section>
    <section>
      <h4>Why it matters</h4>
      <p>{html.escape(str(result['intuition']))} {html.escape(str(result['why']))}</p>
    </section>
    <section>
      <h4>How the proof goes</h4>
      <p>{html.escape(str(result['proof_idea']))}</p>
    </section>
  </div>
  <dl class="result-notes">
    <div><dt>Uses</dt><dd>{'; '.join(dependencies)}</dd></div>
    <div><dt>Still outside this result</dt><dd>{html.escape(str(result['missing']))}</dd></div>
  </dl>
  <h4 class="proof-heading">Route closure</h4>
  <ul class="declaration-list">{route_closures}</ul>
  <h4 class="proof-heading">Natural-language steps and Lean objects</h4>
  <table class="proof-steps">
    <thead><tr><th>Mathematical step</th><th>Lean object or step</th></tr></thead>
    <tbody>{steps}</tbody>
  </table>
  <details class="source-panel">
    <summary>Open the Lean statement and source links</summary>
    <pre><code>{html.escape(source_statement(str(declaration['sourcePreview'])))}</code></pre>
    <p>
      <a href="{module_url(prefix, declaration)}">Local declaration</a> ·
      <a href="{blueprint_url(prefix, declaration)}">Verso Blueprint</a> ·
      {source_links}
    </p>
  </details>
</article>"""


def load_robin_paper_map(
    declarations: dict[str, dict[str, object]],
) -> dict[str, object]:
    data = load_json(WEBSITE_ROOT / "robin-paper-map.json")
    missing: list[str] = []
    for row in data["rows"]:
        for status_key in ("localStatus", "routeStatus"):
            if row[status_key] not in STATUS_ORDER:
                raise SystemExit(
                    f"Unknown Robin paper-map status: {row[status_key]}"
                )
        for name in row["declarations"]:
            if name not in declarations:
                missing.append(str(name))
    if missing:
        raise SystemExit(
            "Robin paper map names declarations absent from inventory:\n  "
            + "\n  ".join(sorted(set(missing)))
        )
    return data


def render_robin_paper_map(
    data: dict[str, object],
    declarations: dict[str, dict[str, object]],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    route = "case-studies/robin/"
    prefix = prefix_for(route)
    paper = data["paper"]
    robin_matrix_tex = render_math_tex(
        r"A=\frac1{12}\begin{pmatrix}-30&32&-2&0&0&0&0&0\\16&-31&16&-1&0&0&0&0\\-1&16&-30&16&-1&0&0&0\\0&-1&16&-30&16&-1&0&0\\0&0&-1&16&-30&16&-1&0\\0&0&0&-1&16&-30&16&-1\\0&0&0&0&-1&16&-31&16\\0&0&0&0&0&-2&32&-30\end{pmatrix},\qquad \Pi U\Pi^\dagger=\frac{A}{56/3}=\frac{M}{224}."
    )
    robin_tiers = (
        ("Candidate exact primitive certificate", "QuantumBlockEncoding.Robin.warmRobinXorFourSlotPrimitiveVerifiedBlockEncoding"),
        ("True source sparse-slot decomposition", "QuantumBlockEncoding.Robin.warmRobinSourceSevenSparseDecomposition"),
        ("Paper-seven exact primitive normal form", "QuantumBlockEncoding.Robin.warmRobinPaperSevenPrimitiveVerifiedBlockEncoding"),
        ("Figure-4 fixed-N8 exact primitive realization", "QuantumBlockEncoding.Robin.warmRobinFigure4PrimitiveVerifiedBlockEncoding"),
        ("Candidate better than paper-seven", "QuantumBlockEncoding.Robin.warmRobinFourSlotT3Cost_betterThan_paperSeven"),
        ("Candidate better than Figure 4", "QuantumBlockEncoding.Robin.warmRobinFourSlotT3Cost_betterThan_figure4"),
        ("Frozen benchmark winner", "QuantumBlockEncoding.Robin.warmRobinBestVerified"),
        ("Fixed publication state is consistent", "QuantumBlockEncoding.Robin.warmRobinPublicationState_consistent"),
    )
    tier_rows = []
    for label, root in robin_tiers:
        declaration = declarations.get(root)
        if declaration:
            evidence = f'<a href="{module_url(prefix, declaration)}"><code>{html.escape(root)}</code></a>'
            state = badge("Compiled")
        else:
            evidence = f'<code>{html.escape(root)}</code>'
            state = badge("Open")
        tier_rows.append(
            f"<tr><th>{html.escape(label)}</th><td>{state}</td><td>{evidence}</td></tr>"
        )
    rows: list[str] = []
    toc = [
        ("paper-contract", "Paper contract"),
        ("fixed-benchmark", "Fixed benchmark"),
        ("how-to-read", "How to read the map"),
        ("source-interpretation", "Source decisions"),
        ("structural-candidates", "Primitive evolution"),
    ]
    for row in data["rows"]:
        row_id = str(row["id"])
        toc.append((row_id, str(row["paperAnchor"])))
        declaration_links: list[str] = []
        statement_panels: list[str] = []
        for name in row["declarations"]:
            declaration = declarations[str(name)]
            declaration_links.append(
                f'<li><a href="{module_url(prefix, declaration)}">'
                f'<code>{html.escape(str(name))}</code></a></li>'
            )
            statement_panels.append(
                f"""<details class="source-panel">
  <summary>{html.escape(str(name))}</summary>
  <pre><code>{html.escape(source_statement(str(declaration['sourcePreview'])))}</code></pre>
  <p><a href="{module_url(prefix, declaration)}">Open local declaration</a> ·
  <a href="{blueprint_url(prefix, declaration)}">Open in the Verso Blueprint</a></p>
</details>"""
            )
        rows.append(
            f"""<article class="result paper-correspondence" id="{html.escape(row_id)}">
  <div class="result-header">
    <div>
      <p class="eyebrow">{html.escape(str(row['paperAnchor']))}</p>
      <h3>{html.escape(str(row['plain']))}</h3>
    </div>
    <div class="status-pair">
      <span><small>Local declarations</small>{badge(str(row['localStatus']))}</span>
      <span><small>Paper-wide route</small>{badge(str(row['routeStatus']))}</span>
    </div>
  </div>
  {render_math_tex(str(row['latex']))}
  <div class="paper-reading">
    <h4>What Lean currently establishes</h4>
    <p>{html.escape(str(row['reading']))}</p>
  </div>
  <h4>Corresponding declarations</h4>
  <ul class="declaration-list">{''.join(declaration_links)}</ul>
  <details class="source-panel paper-latex">
    <summary>Show the paper-side LaTeX</summary>
    <pre><code>{html.escape(str(row['latex']))}</code></pre>
  </details>
  {''.join(statement_panels)}
</article>"""
        )
    body = rf"""
<section class="hero" id="paper-contract">
  <p class="eyebrow">Paper reproduction · source-to-Lean reading map</p>
  <h1>Robin boundary block encoding</h1>
  <p class="lede">The source paper proposes a general circuit family for
  differential operators with Robin boundaries. ASPBE separates that general
  route from a fixed \(N=8\) benchmark, where three exact primitive block
  encodings and their same-tier resource comparison now compile.</p>
  <div class="link-row">
    <a class="button" href="{html.escape(str(paper['url']))}">Open the source paper</a>
    <a class="button secondary" href="{prefix}sources/ghl2025-robin-excerpts.tex">Download the LaTeX excerpts</a>
    <a class="text-link" href="{prefix}example-cases/robin-ghl-one-term/index.html">See the circuit and evolution trace &#8594;</a>
  </div>
</section>
<section class="content-section" id="fixed-benchmark">
  <div class="section-heading"><p class="eyebrow">The concrete case</p>
  <h2>What matrix is being encoded?</h2>
  <p>The benchmark fixes the homogeneous-Robin fourth-derivative matrix. Keeping
  \(M=12A\) integral makes every decomposition identity exact in Lean.</p></div>
  {robin_matrix_tex}
  <p>The clean projector fixes selector and coefficient registers to zero. The
  remaining three-qubit register indexes the rows and columns of \(A\).</p>
</section>
<section class="content-section" id="how-to-read">
  <div class="section-heading">
    <p class="eyebrow">Status discipline</p>
    <h2>A compiled declaration is not automatically the paper theorem</h2>
  </div>
  <p>The left badge says that the named Lean object compiles in this checkout.
  The right badge says whether the entire paper route is closed. Contract
  records, transcript equalities, finite diagnostics, and counterexamples are
  valuable formal results, but they do not replace the final projected-block
  theorem.</p>
  <div class="callout warning">
    <strong>Current conclusion.</strong>
    The arbitrary-size paper theorem remains partial. The fixed \(N=8\),
    homogeneous \(f=1\) benchmark is closed separately: Lean certifies
    paper-seven, the standard-RY-corrected Figure-4 realization, and the XOR
    four-slot candidate in the exact <code>{{X, RY, RZ, CX}}</code> basis. It
    proves the candidate strictly better than both source realizations under
    the frozen compiler and lexicographic score. This is not a global
    optimality theorem.
  </div>
  <table class="proof-steps"><thead><tr><th>Verification layer</th><th>Status in this build</th><th>Required root</th></tr></thead><tbody>{''.join(tier_rows)}</tbody></table>
</section>
<section class="content-section" id="source-interpretation">
  <div class="section-heading"><p class="eyebrow">Source audit</p>
  <h2>Source interpretation decisions</h2><p>The fixed circuit is explicit
  about choices that cannot safely remain hidden in a transcription.</p></div>
  <ol class="reading-steps">{''.join(f'<li>{html.escape(str(item))}</li>' for item in data.get('sourceInterpretation', []))}</ol>
</section>
<section class="content-section" id="structural-candidates">
  <div class="section-heading"><p class="eyebrow">Fixed N=8 evolution</p>
  <h2>Three comparable primitive circuits</h2><p>Every tuple is ordered as
  gates, depth, auxiliary qubits, and oracle calls.</p></div>
  {render_math_tex(r"A/(56/3)=M/224")}
  <div class="case-grid">
    <article class="case-card"><p class="eyebrow">Source Figure 4 · (881,674,6,0)</p><h3>Fixed-N8 circuit</h3><p>Indicator,
    bulk and boundary loaders, two distinct sparse transports, register swap,
    and clean uncomputation follow the corrected source order.</p></article>
    <article class="case-card"><p class="eyebrow">Source normal form · (312,266,5,0)</p><h3>Paper seven</h3><p>A true padded-seven
    sparse table compiles directly through PREPARE, amplitude loading, modular
    SELECT, and unprepare.</p></article>
    <article class="case-card"><p class="eyebrow">Certified winner · (106,96,3,0)</p><h3>XOR four slot</h3><p>Robin centrosymmetry
    reduces the selector and turns SELECT into two CX gates. Lean proves both
    strict same-tier comparisons.</p></article>
  </div>
  <p><a class="button" href="{prefix}example-cases/robin-ghl-one-term/index.html">Open the theorem-linked evolution visualization</a></p>
  <div class="callout"><strong>Executable replicas.</strong> Canonical IR,
  gate-by-gate Qiskit, and strict OpenQASM 3 files are generated separately for
  all three circuits. Their numerical checks are debugging evidence; the Lean
  refinement and projected-block declarations above are the proof authority.</div>
</section>
<section class="content-section paper-map" id="correspondence">
  <div class="section-heading">
    <p class="eyebrow">{html.escape(str(paper['shortName']))}</p>
    <h2>Paper statement to Lean structure</h2>
    <p>Expand a row to compare the source LaTeX, the exact Lean statement, and
    its location in the Library Explorer and Blueprint.</p>
  </div>
  {''.join(rows)}
</section>"""
    return page_template(
        title="Robin paper map",
        route=route,
        current=route,
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=toc,
        description=(
            "Guseynov-Huang-Liu Robin block-encoding statements mapped to "
            "compiled ASPBE Lean declarations and open paper-route obligations."
        ),
    )


def render_textbook_lesson(slug: str) -> str:
    lesson = LESSONS[slug]
    objectives = "".join(
        f"<li>{html.escape(str(item))}</li>" for item in lesson["objectives"]
    )
    sections = "".join(
        f"""<article class="lesson-step">
  <h3>{html.escape(str(title))}</h3>
  <div class="lesson-equation">\\[{html.escape(str(math))}\\]</div>
  <p>{html.escape(str(explanation))}</p>
</article>"""
        for title, math, explanation in lesson["sections"]
    )
    return f"""
<section class="content-section textbook-lesson" id="lesson">
  <div class="lesson-opening">
    <div>
      <p class="eyebrow">Textbook lesson</p>
      <h2>Build the idea before opening the proof</h2>
      <p class="lesson-lead">{html.escape(str(lesson['lead']))}</p>
    </div>
    <aside class="lesson-objectives" aria-label="Learning objectives">
      <h3>By the end</h3>
      <ul>{objectives}</ul>
    </aside>
  </div>
  <div class="lesson-steps">{sections}</div>
  <div class="lesson-checkpoint">
    <strong>Check your understanding</strong>
    <p>{html.escape(str(lesson['checkpoint']))}</p>
  </div>
  <p class="source-note">Mathematical order and conventions adapted from Lin,
  <a href="https://arxiv.org/abs/2201.08309">Lecture Notes on Quantum Algorithms for Scientific Computation</a>.
  The formal checkpoints and ASPBE status distinctions are specific to this library.</p>
</section>"""


def render_chapter(
    chapter: dict[str, object],
    declarations: dict[str, dict[str, object]],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    route = f"chapters/{chapter['slug']}/"
    prefix = prefix_for(route)
    result_html = []
    toc = [
        ("orientation", "Orientation"),
        ("lesson", "Textbook lesson"),
        ("dependency-view", "Route at a glance"),
    ]
    for item in chapter["results"]:
        declaration = declarations[str(item["declaration"])]
        result_html.append(result_card(item, declaration, declarations, prefix))
        toc.append((declaration_anchor(str(item["declaration"])), str(item["title"])))
    modules = "".join(f"<li><code>{html.escape(module)}</code></li>" for module in chapter["modules"])
    body = f"""
<section class="hero" id="orientation">
  <p class="eyebrow">{html.escape(str(chapter['track']))} · Chapter {chapter['number']} of {len(CHAPTERS)}</p>
  <h1>{html.escape(str(chapter['title']))}</h1>
  <p class="lede">{html.escape(str(chapter['summary']))}</p>
  <details class="module-list">
    <summary>Lean modules used in this chapter</summary>
    <ul>{modules}</ul>
  </details>
</section>
{render_textbook_lesson(str(chapter['slug']))}
<section class="content-section" id="dependency-view">
  <div class="section-heading">
    <p class="eyebrow">Route at a glance</p>
    <h2>Where these results sit</h2>
  </div>
  {diagram(prefix, str(chapter['diagram']), f"{chapter['track']}: {chapter['title']}")}
</section>
<section class="content-section" id="important-results">
  <div class="section-heading">
    <p class="eyebrow">Selected declarations</p>
    <h2>Read the mathematics beside the Lean statement</h2>
    <p>A compiled route means that the reusable theorem or constructor and at
    least one finite witness compile. Hardware- and problem-specific downstream
    instantiations are out of scope, not universal claims made by these cards.</p>
  </div>
  {''.join(result_html)}
</section>"""
    return page_template(
        title=str(chapter["title"]),
        route=route,
        current=route,
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=toc,
        description=str(chapter["summary"]),
    )


def render_learning(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    catalog = load_json(WEBSITE_ROOT / "curriculum-parts.json")
    parts = catalog["parts"]
    part_cards = "".join(
        f'''<article class="application-path">
  <p class="path-label">{html.escape(str(part["label"]))} · {badge(str(part["status"]))}</p>
  <h3><a href="../{html.escape(str(part["route"]))}index.html">{html.escape(str(part["title"]))}</a></h3>
  <p>{html.escape(str(part["summary"]))}</p>
</article>'''
        for part in parts
    )
    body = f"""
<section class="hero">
  <p class="eyebrow">Guided reading</p>
  <h1>Four peer textbook parts, one shared Lean graph</h1>
  <p class="lede">State Preparation and Block Encoding are the two currently
  compiled cores. Quantum Information and Representation Theory, and Quantum
  Algorithms for Scientific Computation, are source-audited peer parts with
  honest planned status. They reuse shared foundations instead of defining a
  second state, channel, circuit or block-encoding API.</p>
  <div class="hero-actions">
    <a class="button state-button" href="../state-preparation/index.html">Part I · State Preparation</a>
    <a class="button block-button" href="../block-encoding/index.html">Part II · Block Encoding</a>
    <a class="button secondary" href="../quantum-information/index.html">Part III · QIT &amp; Representation</a>
    <a class="button secondary" href="../quantum-scientific-computing/index.html">Part IV · Scientific Computing</a>
  </div>
</section>
<section class="content-section" id="reading-map">
  <div class="section-heading">
    <p class="eyebrow">Reading map</p>
    <h2>Nested preparation layer, explicit transport hypotheses</h2>
    <p>The graph makes State Preparation a reusable subproblem of the broader
    Block Encoding toolchain without identifying their certificate types. Reverse
    block-to-state consumption remains a separately typed path.</p>
  </div>
  {diagram("../", "learning-path", "Shared foundations and typed SP/BE bridges")}
</section>
<section class="content-section" id="chapter-list">
  <div class="section-heading">
    <p class="eyebrow">One book map · explicit proof status</p>
    <h2>Four peer parts: compiled chapters and source-anchored plans</h2>
  </div>
  {render_chapter_groups('../')}
</section>
{render_curriculum_explorer('../')}
<section class="content-section" id="future-curriculum">
  <div class="section-heading">
    <p class="eyebrow">One navigation level · distinct proof status</p>
    <h2>The four-part curriculum</h2>
    <p>{html.escape(str(catalog["truthBoundary"]))}</p>
  </div>
  {diagram("../", "quantum-domain-roadmap", "Conceptual curriculum roadmap; dashed transports are not Lean implications")}
  <div class="application-paths">{part_cards}</div>
  <div class="callout"><strong>Source policy.</strong> The 29 April Lin–Wiebe
  edition supplied to the project is publicly hosted by the authors, so the
  repository records the public source rather than vendoring a large PDF. A
  genuinely non-public appendix may be stored later only with provenance and
  reuse/license review.</div>
</section>"""
    return page_template(
        title="Guided learning",
        route="learning/",
        current="learning/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[
            ("reading-map", "Reading map"),
            ("chapter-list", "All four chapter maps"),
            ("textbook-explorer", "Search textbooks"),
            ("future-curriculum", "Four-part curriculum"),
        ],
        extra_scripts=("static/curriculum.js",),
    )

def render_implementation_map(
    declarations: dict[str, dict[str, object]],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    prefix = "../"
    chapter_tracks = {
        str(chapter["slug"]): str(chapter["track"]) for chapter in CHAPTERS
    }
    grouped_rows: dict[str, list[str]] = {track: [] for track in TRACK_ORDER}
    for item in IMPLEMENTATION_MAP:
        declaration = declarations[str(item["declaration"])]
        track = chapter_tracks[str(item["chapter"])]
        grouped_rows[track].append(
            f"""<tr>
  <td>{html.escape(str(item['goal']))}</td>
  <td>\\({html.escape(str(item['contract']))}\\)</td>
  <td>{html.escape(str(item['obligation']))}</td>
  <td><a href="{module_url(prefix, declaration)}"><code>{html.escape(str(item['declaration']))}</code></a></td>
  <td><code>{html.escape(str(declaration['source']))}:{int(declaration['line'])}</code></td>
  <td>{html.escape(str(item['dependencies']))}</td>
  <td>{badge(str(item['status']))}</td>
  <td>{html.escape(str(item['missing']))}</td>
  <td><a href="../chapters/{html.escape(str(item['chapter']))}/index.html">chapter</a> ·
      <a href="{blueprint_url(prefix, declaration)}">Blueprint</a></td>
</tr>"""
        )
    tables = []
    for track in TRACK_ORDER:
        if not grouped_rows[track]:
            continue
        tables.append(
            f"""
<section class="map-group">
  <h2>{html.escape(track)}</h2>
  <div class="table-wrap">
    <table class="data-table">
      <thead><tr>
        <th>Mathematical goal</th><th>Contract</th><th>Proof obligation</th>
        <th>Lean declaration</th><th>Module / line</th><th>Dependencies</th>
        <th>Status</th><th>Missing step</th><th>Reader links</th>
      </tr></thead>
      <tbody>{''.join(grouped_rows[track])}</tbody>
    </table>
  </div>
</section>"""
        )
    body = f"""
<section class="hero">
  <p class="eyebrow">Generated links · Curated route status</p>
  <h1>Implementation Map</h1>
  <p class="lede">Trace a mathematical statement to the exact Lean declaration,
  source line, dependencies, current status, and work that remains. The map is
  grouped by the same learning tracks used throughout the site.</p>
</section>
<section class="content-section map-groups">
  {''.join(tables)}
</section>"""
    return page_template(
        title="Implementation Map",
        route="implementation-map/",
        current="implementation-map/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
    )


def declaration_status(declaration: dict[str, object]) -> str:
    return str(declaration["localStatus"])


def render_library(
    inventory: dict[str, object],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    declarations = inventory["declarations"]
    kinds = sorted({str(item["kind"]) for item in declarations})
    catalogs = sorted({str(item["catalog"]) for item in declarations})
    statuses = [status for status in STATUS_ORDER if any(declaration_status(item) == status for item in declarations)]
    options = lambda values: "".join(
        f'<option value="{html.escape(value)}">{html.escape(value)}</option>'
        for value in values
    )
    rows = []
    for declaration in declarations:
        search = " ".join(
            str(declaration.get(field, ""))
            for field in ("fullName", "readerLabel", "plainEnglish", "source", "catalog")
        ).lower()
        rows.append(
            f"""
<article class="declaration-row" data-declaration-row
  data-search="{html.escape(search, quote=True)}"
  data-kind="{html.escape(str(declaration['kind']), quote=True)}"
  data-catalog="{html.escape(str(declaration['catalog']), quote=True)}"
  data-status="{html.escape(declaration_status(declaration), quote=True)}">
  <div>
    <h3><a href="{module_url('../', declaration)}"><code>{html.escape(str(declaration['fullName']))}</code></a></h3>
    <p>{html.escape(str(declaration['plainEnglish']))}</p>
  </div>
  <div class="status-pair">{badge(declaration_status(declaration))}{badge(str(declaration['routeStatus']))}</div>
</article>"""
        )
    body = f"""
<section class="hero">
  <p class="eyebrow">Lean Declaration Catalog / Library Explorer</p>
  <h1>Search every explicit public declaration</h1>
  <p class="lede">The inventory is generated from <code>QuantumBlockEncoding/</code>.
  Private declarations follow the repository's existing exclusion rule and are
  counted in the build report, not displayed as public API.</p>
</section>
<section class="content-section" data-library>
  <div class="filter-bar">
    <label><span class="visually-hidden">Search library</span>
      <input type="search" placeholder="Name, source, docstring, catalog" data-library-query>
    </label>
    <label><span class="visually-hidden">Declaration kind</span>
      <select data-library-kind><option value="">All kinds</option>{options(kinds)}</select>
    </label>
    <label><span class="visually-hidden">Catalog</span>
      <select data-library-catalog><option value="">All catalogs</option>{options(catalogs)}</select>
    </label>
    <label><span class="visually-hidden">Local status</span>
      <select data-library-status><option value="">All local statuses</option>{options(statuses)}</select>
    </label>
  </div>
  <p class="muted" data-library-count>{len(declarations):,} declarations shown</p>
  <div class="declaration-list">{''.join(rows)}</div>
</section>"""
    return page_template(
        title="Lean Library Explorer",
        route="library/",
        current="library/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
    )


def render_module_page(
    source: str,
    declarations: list[dict[str, object]],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    route = f"library/modules/{module_slug(source)}/"
    prefix = prefix_for(route)
    entries = []
    for declaration in declarations:
        external = declaration.get("sourceUrl")
        external_html = (
            f'<a href="{html.escape(str(external))}">commit-pinned source</a>'
            if external
            else '<span class="muted">No publishable external source link</span>'
        )
        entries.append(
            f"""
<article class="module-declaration" id="{declaration_anchor(str(declaration['fullName']))}">
  <div class="result-header">
    <div>
      <p class="eyebrow">{html.escape(str(declaration['kind']))} · line {int(declaration['line'])}</p>
      <h3><code>{html.escape(str(declaration['fullName']))}</code></h3>
    </div>
    <div class="status-pair">
      {badge(declaration_status(declaration))}
      {badge(str(declaration['routeStatus']))}
    </div>
  </div>
  <p>{html.escape(str(declaration['plainEnglish']))}</p>
  <pre><code>{html.escape(source_statement(str(declaration['sourcePreview'])))}</code></pre>
  <p>{external_html} · <a href="{blueprint_url(prefix, declaration)}">Verso Blueprint panel</a></p>
</article>"""
        )
    body = f"""
<section class="hero">
  <p class="eyebrow">Lean source module</p>
  <h1><code>{html.escape(source)}</code></h1>
  <p class="lede">{len(declarations):,} explicit public declarations in source order.</p>
  <a class="button secondary" href="{prefix}library/index.html">Back to Library Explorer</a>
</section>
<section class="content-section">
  {''.join(entries)}
</section>"""
    return page_template(
        title=source,
        route=route,
        current="library/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
    )


def render_roadmap(
    inventory: dict[str, object],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    route_counts = Counter(str(item["routeStatus"]) for item in inventory["declarations"])
    rows = "".join(
        f"<tr><td>{html.escape(label)}</td><td>{badge(status)}</td></tr>"
        for label, status in ROADMAP
    )
    stats = "".join(
        f'<div class="metric"><strong>{route_counts.get(status, 0):,}</strong><span>{html.escape(status)} route labels</span></div>'
        for status in STATUS_ORDER
    )
    literature_status = {
        "formalized": "Compiled",
        "skeleton": "Partial route",
        "planned": "Planned",
    }
    literature_rows = "".join(
        f"""<tr>
  <td>{badge(literature_status.get(item.get('status', ''), 'Experimental'))}</td>
  <td><a href="{html.escape(item.get('url', ''), quote=True)}">{html.escape(item.get('title', 'Untitled'))}</a><br><span class="muted">{html.escape(item.get('authors', ''))} ({html.escape(item.get('year', ''))})</span></td>
  <td><code>{html.escape(item.get('role', ''))}</code></td>
  <td><code>{html.escape(item.get('targetFile', ''))}</code><br>{html.escape(item.get('note', ''))}</td>
</tr>"""
        for item in parse_literature_registry()
    )
    body = f"""
<section class="hero">
  <p class="eyebrow">Progress and Roadmap</p>
  <h1>Local proof completion is not route completion</h1>
  <p class="lede">Counts below are generated from the declaration inventory.
  Milestones are curated against the actual modules and openly name partial,
  experimental, planned, and blocked work.</p>
</section>
<section class="content-section">
  <div class="metric-grid">{stats}</div>
  {diagram("../", "roadmap", "Milestone status and open routes")}
  <div class="table-wrap">
    <table class="data-table">
      <thead><tr><th>Milestone</th><th>Broader route status</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</section>
<section class="content-section" id="paper-reproduction-queue">
  <div class="section-heading">
    <p class="eyebrow">Paper reproduction queue</p>
    <h2>What has been reproduced, and what has not</h2>
    <p>This table is generated from the Lean-compiled literature registry. A
    compiled local lemma does not promote a paper-wide route unless its circuit,
    oracle, projection, normalization, and resource obligations are all closed.</p>
  </div>
  <div class="table-wrap">
    <table class="data-table">
      <thead><tr><th>Status</th><th>Paper</th><th>Role</th><th>Target and next step</th></tr></thead>
      <tbody>{literature_rows}</tbody>
    </table>
  </div>
</section>
<section class="content-section" id="long-term-quantum-curriculum">
  <div class="section-heading">
    <p class="eyebrow">Planned textbook expansion · source anchors only</p>
    <h2>One shared graph beyond State Preparation and Block Encoding</h2>
    <p>The next domains are not separate libraries with duplicated foundations.
    Quantum Information and Quantum Scientific Computing will reuse the same
    density-operator, tensor-system, channel, distance, circuit, query and
    resource nodes whenever their semantics agree.</p>
  </div>
  {diagram("../", "quantum-domain-roadmap", "Long-term QuantumComputinglib curriculum and shared-node plan")}
  <div class="table-wrap">
    <table class="data-table">
      <thead><tr><th>Status</th><th>Future part / source anchor</th><th>Reuse policy</th></tr></thead>
      <tbody>
        <tr><td>{badge("Planned")}</td><td><strong>Part III · Quantum Information and symmetry</strong><br><a href="https://www.felixleditzky.info/teaching/FT25/math595-repth-qit.pdf">Felix Leditzky, Representation-theoretic methods in quantum information theory</a></td><td>Build on shared states/density operators, subsystem operations, channels and distances; representation-theoretic nodes live above that layer.</td></tr>
        <tr><td>{badge("Planned")}</td><td><strong>Part IV · Quantum Algorithms for Scientific Computation</strong><br><a href="https://math.berkeley.edu/~linlin/qasc/live_notes_0429.pdf">Lin Lin and Nathan Wiebe, 29 April 2026 live notes</a></td><td>Reuse the existing Block Encoding part for source Chapter 9, then add qubitization, QSP/QSVT, simulation, QPE and application layers without a second BE API.</td></tr>
      </tbody>
    </table>
  </div>
  <p>External quantum Lean projects on the ecosystem page are reference/adapter
  candidates only. A future chapter enters positive proof memory only after the
  source, semantic, Lean, integration, exposition and independent-review gates
  are satisfied.</p>
</section>
<section class="content-section" id="vandaele-frontier">
  <div class="section-heading">
    <p class="eyebrow">Source-faithful formalization frontier</p>
    <h2>Vandaele comparator / incrementer route</h2>
    <p>The current route is deliberately <strong>partial</strong>. ASPBE already
    certifies reusable controlled-conjugation and dirty-flag/involution identities;
    it does not yet certify the paper's complete comparator, incrementer, or
    optimality claims.</p>
  </div>
  <div class="callout"><strong>Next root chain.</strong>
    literal Figure 4 gates → named U₁,…,U₈ slice semantics →
    arbitrary-width adder including carry → literal X–ADD–X Figure 5 semantics →
    Eq. (17) comparison predicate and operand orientation → recursive
    V₂^(n) resource theorem → lower-bound bridge before the word
    <em>optimal</em> is promoted.</div>
  <p>The finite Figure 4/5 witnesses are convention discriminators, not
  arbitrary-width closure. If the literal circuit and advertised comparison
  orientation disagree under the pinned register convention, the source
  equation, literal-circuit theorem, counterexample, and any repair proposal
  remain separate reviewed objects.</p>
  <p><a href="https://arxiv.org/abs/2603.12917">Primary source: Vandaele 2026</a>.
  The repository plan also separates controlled/classical–quantum comparators,
  incrementers, the classical–quantum adder, and the downstream Shor consequence
  into later integration stages rather than inferring them from local lemmas.</p>
</section>
<section class="content-section" id="memory-transfer-protocol">
  <div class="section-heading">
    <p class="eyebrow">Planned longitudinal experiment</p>
    <h2>Does a larger certified memory actually help?</h2>
  </div>
  <p>Each newly reproduced paper adds memory cards only after its named Lean
  roots compile. Earlier cold and warm benchmarks are then replayed in fresh,
  isolated worktrees with the same model, prompt budget, target, tolerance
  ladder, and acceptance gates. We compare solve rate, accepted-cycle count,
  token proxy, wall time, and invalid-route count. Historical run artifacts are
  never injected into the cold arm.</p>
</section>"""
    return page_template(
        title="Progress and Roadmap",
        route="roadmap/",
        current="roadmap/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
    )


def render_workflow(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    steps = "".join(
        f'<article class="workflow-step"><h3>{html.escape(title)}</h3><p>{html.escape(text)}</p></article>'
        for title, text in WORKFLOW_STAGES
    )
    body = f"""
<section class="hero">
  <p class="eyebrow">ASPBE harness</p>
  <h1>Search, prove, validate, and retain evidence</h1>
  <p class="lede">The upper layer controls decomposition and budget; the middle
  layer maintains a diverse population and feedback; focused workers discharge
  bounded obligations. Tolerance is relaxed by an explicit schedule, not silently.</p>
</section>
<section class="content-section">
  {diagram("../", "candidate-lifecycle", "Candidate generation, scoring, verification, and acceptance")}
  <div class="workflow-list">{steps}</div>
  <div class="callout"><strong>Evidence boundary.</strong> Harness declarations
  formalize controller data and acceptance policy. They do not prove that an
  external agent run was efficient. Run logs, token accounting, and Qiskit outputs
  remain engineering evidence attached after the Lean gate.</div>
</section>"""
    return page_template(
        title="ASPBE harness",
        route="workflow/",
        current="workflow/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
    )


def render_organizers(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    cards = "".join(
        f'<article class="person-row"><h3>{html.escape(name)}</h3>'
        f'<p>{html.escape(affiliation)}</p></article>'
        for name, affiliation in ORGANIZERS
    )
    body = f"""
<section class="hero" id="organizers">
  <p class="eyebrow">People</p>
  <h1>Organizers</h1>
  <p class="lede">QuantumComputinglib is maintained with ASPBE by the current project
  authors. Contributor credit is recorded separately and follows each accepted
  lemma or teaching contribution.</p>
</section>
<section class="content-section" id="team">
  <div class="people-list">{cards}</div>
</section>
<section class="content-section" id="credits">
  <h2>Contributor credit</h2>
  <p>New contributors choose a preferred public credit line in their lemma
  packet. Integration keeps the mathematical source, compiler evidence, and
  contributor attribution together.</p>
  <a class="button secondary" href="../community/index.html">Submit a contribution</a>
</section>"""
    return page_template(
        title="Organizers",
        route="organizers/",
        current="organizers/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[("organizers", "Organizers"), ("team", "Current authors"), ("credits", "Contributor credit")],
    )


def render_ecosystem(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    body = """
<section class="hero" id="ecosystem">
  <p class="eyebrow">Quantum Lean ecosystem</p>
  <h1>One reading map, honest dependency boundaries</h1>
  <p class="lede">QuantumComputinglib brings ASPBE declarations, selected external
  quantum-formalization references, and textbook explanations into one map.
  “Indexed” does not mean “imported”: every row states how the source is used.</p>
</section>
<section class="content-section" id="catalog">
  <h2>Libraries represented in QuantumComputinglib</h2>
  <div class="ecosystem-list">
    <article><div><h3>ASPBE</h3><p>State preparation, block encoding, finite circuit semantics, construction routes, resource records, automation, and certified cases.</p></div><span class="status status-compiled">Built here</span></article>
    <article><div><h3>Mathlib</h3><p>Finite types, matrices, algebra, norms, finite sums, and proof infrastructure used by the local Lean package.</p></div><span class="status status-compiled">Imported</span></article>
    <article><div><h3><a href="https://github.com/duckki/quantum-computing-lean">quantum-computing-lean</a></h3><p>Named states, gates, projectors, gate actions, decompositions, and compact finite-dimensional module organization.</p></div><span class="status status-partial-route">Reference atlas</span></article>
    <article><div><h3><a href="https://github.com/Timeroot/Lean-QuantumInfo">Lean-QuantumInfo</a></h3><p>Finite-dimensional quantum and classical information, channels, distributions, entropy, and capacity.</p></div><span class="status status-partial-route">Reference atlas</span></article>
    <article><div><h3><a href="https://github.com/Hayata-Yamasaki-Group/lean-quantum">lean-quantum</a></h3><p>Quantum states, channels, qudits, operator conventions, and higher-level quantum-information semantics.</p></div><span class="status status-partial-route">Reference atlas</span></article>
    <article><div><h3><a href="https://github.com/QudeLeap/Lean-QuantumAlg-Bench">Lean-QuantumAlg-Bench</a></h3><p>Pinned quantum-algorithm benchmark statements. They are useful formalization targets but unresolved statements are excluded from proof memory.</p></div><span class="status status-planned">Benchmark reference</span></article>
    <article><div><h3><a href="https://github.com/QuAIR/Lean-QIT-Bench">Lean-QIT-Bench</a></h3><p>Pinned quantum-information benchmark statements for future QIT coverage; statement presence is not a local theorem certificate.</p></div><span class="status status-planned">Benchmark reference</span></article>
    <article><div><h3><a href="https://rammalahmad.github.io/atlas/">ATLAS v1</a></h3><p>A pinned external memory over broad textbook mathematics. ASPBE preserves upstream compilation and quality distinctions, then admits only narrow locally compiled adapters.</p></div><span class="status status-partial-route">External memory</span></article>
  </div>
</section>
<section class="content-section" id="policy">
  <h2>How an external result enters the library</h2>
  <ol class="numbered-reading">
    <li><strong>Reference.</strong> Record the upstream repository, license, module, and exact declaration.</li>
    <li><strong>Adapter.</strong> State the narrow ASPBE bridge without copying incompatible APIs.</li>
    <li><strong>Compile.</strong> Import or prove the adapter under the pinned toolchain.</li>
    <li><strong>Teach.</strong> Add the formula, plain-language reading, assumptions, and source link.</li>
  </ol>
  <p>This prevents a survey entry, benchmark statement, or upstream theorem card
  from appearing as a locally compiled result. Before adding foundational QIT
  objects, search these sources and prefer one reviewed adapter/shared node to
  a parallel local definition.</p>
</section>"""
    return page_template(
        title="Quantum Lean ecosystem",
        route="ecosystem/",
        current="ecosystem/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[("ecosystem", "Ecosystem"), ("catalog", "Libraries"), ("policy", "Import policy")],
    )


def render_community(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    repository = context.get("repository") or "DakeBU/QuantumComputinglib-QuantumComputingBench"
    issue_url = f"https://github.com/{repository}/issues/new?template=lemma-contribution.yml"
    pull_url = f"https://github.com/{repository}/compare"
    body = f"""
<section class="hero" id="contribute">
  <p class="eyebrow">Contribute to QuantumComputinglib</p>
  <h1>Bring one sourced statement to one checked Lean declaration</h1>
  <p class="lede">Submit teaching corrections, external-library mappings, or
  new state-preparation and block-encoding lemmas. Large changes begin with a
  proposal so assumptions and module ownership are agreed before proof work.</p>
  <div class="hero-actions">
    <a class="button state-button" href="../ide/index.html">Draft in the live workspace</a>
    <a class="button secondary" href="{html.escape(issue_url)}">Open a lemma proposal</a>
    <a class="text-link" href="{html.escape(pull_url)}">Prepare a pull request &#8594;</a>
  </div>
</section>
<section class="content-section" id="before">
  <h2>Before writing Lean</h2>
  <p>A small correction or isolated lemma can go directly to a pull request.
  Start with a proposal when the work adds a module, dependency, public API,
  mathematical contract, or substantial construction route.</p>
  <div class="contribution-paths">
    <article><span>01</span><h3>Fix the scope</h3><p>Record the source, exact statement, conventions, owning module, and whether the wider route is complete.</p></article>
    <article><span>02</span><h3>Reuse before adding</h3><p>Search the declaration catalog and external atlas. Prefer a narrow adapter to a duplicate API.</p></article>
    <article><span>03</span><h3>Choose the evidence class</h3><p>Separate a Lean certificate, finite executable check, imported contract, and exploratory argument.</p></article>
  </div>
</section>
<section class="content-section" id="steps">
  <h2>Four steps from idea to an indexed contribution</h2>
  <ol class="contributor-steps">
    <li><span>1</span><div><h3>Scope</h3><p>Agree on the mathematical boundary, source, conventions, owner module, and public API.</p></div></li>
    <li><span>2</span><div><h3>Develop</h3><p>Add the smallest focused declaration. Do not use <code>sorry</code>, <code>admit</code>, a new <code>axiom</code>, or a weakened placeholder proposition.</p></div></li>
    <li><span>3</span><div><h3>Verify</h3><pre><code>lake build
lake build ABEISTests
python3 tools/qbe.py check
bash scripts/build-all.sh</code></pre><p>Report a gate you could not run; do not mark it passed.</p></div></li>
    <li><span>4</span><div><h3>Submit and receive credit</h3><p>Open a focused PR with source, API choices, local and route status, exact gate results, and preferred public credit.</p></div></li>
  </ol>
  <p>Read the repository-wide <a href="../CONTRIBUTING.md">contribution policy</a>
  and <a href="../contributors/index.html">integrated contributor record</a>.</p>
</section>
<section class="content-section" id="packet">
  <h2>Workspace packet and pull request serve different stages</h2>
  <p>The workspace exports a versioned JSON packet for discussion and review.
  A pull request carries the implementation. Neither marks itself integrated:
  maintainers check mathematical equivalence, assumptions, API fit, provenance,
  license, and the complete ASPBE gate.</p>
  <p><a href="contribution.schema.json">Machine-readable packet schema</a> ·
  <a href="{html.escape(issue_url)}">Open a proposal</a> ·
  <a href="{html.escape(pull_url)}">Open a pull request</a></p>
</section>
<section class="content-section" id="status">
  <h2>Status words are not interchangeable</h2>
  <div class="status-key">
    <p><span class="status status-planned">Proposed</span> statement or code awaits review.</p>
    <p><span class="status status-partial-route">Lean checked</span> the submitted snippet compiled locally.</p>
    <p><span class="status status-compiled">Integrated</span> the declaration passed the repository gate and entered the generated inventory.</p>
  </div>
</section>"""
    return page_template(
        title="Contribute",
        route="community/",
        current="community/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[("contribute", "Contribute"), ("before", "Before you begin"), ("steps", "Four steps"), ("packet", "Packet and PR"), ("status", "Statuses")],
    )


def render_contributors(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    data = load_json(WEBSITE_ROOT / "community" / "contributors.json")
    contributors = data.get("contributors", [])
    records = []
    for contributor in contributors:
        items = "".join(
            f"<li>{html.escape(str(item))}</li>"
            for item in contributor.get("contributions", [])
        )
        records.append(
            '<article class="contributor-record">'
            f'<h3>{html.escape(str(contributor["name"]))}</h3>'
            f'<p>{html.escape(str(contributor.get("credit", "")))}</p>'
            f'<ul>{items}</ul></article>'
        )
    if not records:
        records.append(
            '<article class="contributor-record contributor-invitation">'
            '<p class="eyebrow">Your name here</p>'
            '<h3>The first external integrated contribution is open</h3>'
            '<p>Accepted theorem, adapter, chapter, validation, and tooling work '
            'will be listed with a precise contribution summary and preferred credit.</p>'
            '<a href="../community/index.html">Read the contribution process &#8594;</a>'
            '</article>'
        )
    body = f"""
<section class="hero" id="contributors">
  <p class="eyebrow">People whose work has entered the repository</p>
  <h1>Contributors</h1>
  <p class="lede">This page lists integrated external contributions, not open
  proposals or locally compiling drafts. Organizers are listed separately.</p>
</section>
<section class="content-section" id="accepted-work">
  <h2>Integrated work</h2>
  <div class="contributor-list">{''.join(records)}</div>
</section>
<section class="content-section" id="recognition">
  <h2>How credit is recorded</h2>
  <p>Each accepted entry names the contributor and the concrete theorem,
  chapter, adapter, executable check, or tool improvement that entered the
  repository. Commit authorship and co-authorship are preserved in Git.</p>
  <a class="button secondary" href="../community/index.html">Become a contributor</a>
</section>"""
    return page_template(
        title="Contributors",
        route="contributors/",
        current="contributors/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[("contributors", "Contributors"), ("accepted-work", "Integrated work"), ("recognition", "Credit")],
    )


def workspace_items(
    declarations: dict[str, dict[str, object]],
) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for chapter in CHAPTERS:
        for result in chapter["results"]:
            declaration = declarations[str(result["declaration"])]
            dependencies = []
            for name in result["dependencies"]:
                dependency = declarations.get(str(name))
                dependencies.append(
                    {
                        "name": str(name),
                        "url": module_url("../", dependency) if dependency else "",
                    }
                )
            local_url = module_url("../", declaration)
            items.append(
                {
                    "name": str(declaration["fullName"]),
                    "chapter": str(chapter["title"]),
                    "plain": str(result["plain"]),
                    "latex": rf"\[{result['math']}\]",
                    "statement": source_statement(str(declaration["sourcePreview"])),
                    "module": str(declaration["source"])
                    .removesuffix(".lean")
                    .replace("/", "."),
                    "url": local_url,
                    "source_url": declaration.get("sourceUrl") or local_url,
                    "dependencies": dependencies,
                    "compile_source": (
                        "import QuantumBlockEncoding\n\n"
                        "-- Ask Lean for the reviewed declaration's exact type.\n"
                        f"#check {declaration['fullName']}\n"
                    ),
                }
            )
    return items



def render_lean_graph(
    payload: dict[str, object],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    route = "lean-graph/"
    return page_template(
        title="Underlying Lean Graph of Libraries",
        route=route,
        current=route,
        body=render_lean_graph_body(payload),
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[
            ("graph-purpose", "Purpose"),
            ("graph-methodology", "Methodology"),
            ("interactive-graph", "Interactive graph"),
            ("graph-compression", "Proof-graph compression"),
        ],
        description=(
            "Interactive QuantumComputinglib Lean module and declaration graph, "
            "with textbook, paper, example-case, and proof-compression context."
        ),
        extra_scripts=("static/lean-graph.js",),
        extra_styles=("static/lean-graph.css",),
    )


def render_ide(
    declarations: dict[str, dict[str, object]],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    body = """
<section class="hero" id="formalization-workspace">
  <p class="eyebrow">Live formalization workspace</p>
  <h1>Read the formula, inspect the Lean statement, then compile</h1>
  <p class="lede">Load a reviewed QuantumComputinglib mapping or edit your own snippet.
  Formula rendering and declaration navigation work on the static site. Real
  compilation is available only through the loopback companion server.</p>
</section>
<section class="content-section" id="execution-boundary">
  <div class="workspace-mode" data-ide-mode>
    <span class="mode-dot" aria-hidden="true"></span>
    <div><strong data-ide-mode-title>Checking the local Lean service</strong>
    <p data-ide-mode-detail>The teaching workspace remains available without code execution.</p></div>
  </div>
  <p class="security-note"><strong>Execution boundary.</strong> GitHub Pages never
  runs submitted code. <code>ide_server.py</code> binds only to loopback, compiles
  temporary files under the pinned ASPBE toolchain, and never edits project source.</p>
</section>
<section class="content-section" id="workspace">
  <div class="workspace-toolbar">
    <label>Reviewed mapping<select data-ide-declaration><option>Loading declarations</option></select></label>
    <label>Translation direction<select data-ide-direction><option value="latex-to-lean">LaTeX to Lean</option><option value="lean-to-latex">Lean to LaTeX</option></select></label>
    <button class="button secondary" type="button" data-ide-load>Reload mapping</button>
    <button class="button secondary" type="button" data-ide-translate>Translate with local agent</button>
    <button class="button secondary" type="button" data-ide-scaffold>Start an honest draft</button>
    <label class="auto-check"><input type="checkbox" data-ide-auto> Compile after edits</label>
  </div>
  <div class="workspace-grid" data-ide-app data-ide-data="../ide-data.json">
    <article class="workspace-pane math-pane">
      <header><span>01</span><h2>Mathematical statement</h2><button class="button secondary compact-button" type="button" data-copy-editor="latex">Copy</button><b data-translation-status>Reviewed mapping</b></header>
      <label for="ide-latex">LaTeX</label>
      <textarea id="ide-latex" data-ide-latex spellcheck="false"></textarea>
      <h3>Rendered statement</h3>
      <div class="math-preview" data-ide-math-preview></div>
      <p data-ide-plain></p>
    </article>
    <article class="workspace-pane lean-pane">
      <header><span>02</span><h2>Lean source</h2><button class="button secondary compact-button" type="button" data-copy-editor="lean">Copy</button><button class="button state-button" type="button" data-ide-compile>Compile</button></header>
      <label for="ide-lean">Editable snippet</label>
      <textarea id="ide-lean" data-ide-lean spellcheck="false"></textarea>
      <p class="source-actions"><a data-ide-declaration-link href="#">Declaration page</a> · <a data-ide-source-link href="#">Source</a></p>
    </article>
  </div>
  <div class="workspace-output">
    <article class="workspace-pane"><header><span>03</span><h2>Lean diagnostics</h2><b data-ide-duration></b></header><pre data-ide-diagnostics aria-live="polite">Local compiler not contacted.</pre></article>
    <article class="workspace-pane"><header><span>04</span><h2>Dependencies</h2><b data-ide-tree-summary></b></header><div class="dependency-tree" data-ide-tree></div></article>
  </div>
</section>
<section class="content-section" id="submit">
  <h2>Request review without overstating the result</h2>
  <div class="submit-fields">
    <label>Name<input type="text" data-contributor-name placeholder="Required for submission"></label>
    <label>Preferred credit<input type="text" data-contributor-credit placeholder="How QuantumComputinglib should credit you"></label>
    <label>Source or citation<input type="text" data-contributor-source placeholder="URL, DOI, book, or original result"></label>
  </div>
  <div class="hero-actions">
    <button class="button secondary" type="button" data-ide-export>Download lemma packet</button>
    <button class="button block-button" type="button" data-ide-submit>Request submission on GitHub</button>
  </div>
  <p class="submission-note" data-ide-export-note>Only the exact Lean text most
  recently accepted by the local compiler is labeled Lean checked. Editing it
  invalidates that status.</p>
</section>"""
    return page_template(
        title="Live formalization workspace",
        route="ide/",
        current="ide/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[
            ("formalization-workspace", "Workspace"),
            ("execution-boundary", "Execution boundary"),
            ("workspace", "Editors"),
            ("submit", "Submit"),
        ],
        extra_scripts=("static/workspace.js",),
    )


def render_attribution(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    license_sections = []
    for paragraph in (ROOT / "LICENSE_SCOPE.md").read_text(encoding="utf-8").strip().split("\n\n"):
        if paragraph.startswith("# "):
            continue
        tag = "h3" if paragraph.startswith("## ") else "p"
        license_sections.append(f"<{tag}>{html.escape(paragraph.removeprefix('## '))}</{tag}>")
    license_body = '<section id="license"><h2>License and reuse</h2><p><a href="../LICENSE">Apache 2.0 full text</a> · <a href="../LICENSE_SCOPE.md">Reuse scope</a> · <a href="../NOTICE">NOTICE</a> · <a href="../LICENSE-MIT">Earlier MIT text</a></p>' + "".join(license_sections) + '</section>'
    body = """
<section class="hero">
  <p class="eyebrow">Attribution</p>
  <h1>Tools, libraries, and project boundaries</h1>
  <p class="lede">QuantumComputinglib is generated from this repository's ASPBE Lean
  source and curated quantum-computing explanations.</p>
</section>
<section class="content-section">
  <h2>Formalization stack</h2>
  <ul>
    <li><a href="https://lean-lang.org/">Lean</a> and
        <a href="https://github.com/leanprover-community/mathlib4">Mathlib</a>
        provide the proof language and mathematical library.</li>
    <li><a href="https://github.com/leanprover/verso">Verso</a> and
        <a href="https://github.com/leanprover/verso-blueprint">Verso Blueprint</a>
        build the checked Blueprint pages.</li>
    <li><a href="https://mermaid.js.org/">Mermaid</a> renders editable dependency
        diagrams; <a href="https://www.mathjax.org/">MathJax</a> renders mathematics.</li>
    <li><a href="https://www.ibm.com/quantum/qiskit">Qiskit</a> is used only where
        an executable validation route requests it; it is not a substitute for Lean.</li>
  </ul>
  <h2>Content boundary</h2>
  <p>This site is tailored to ASPBE state preparation, block encoding, circuit
  semantics, resource evaluation, and automation records. It does not import
  unrelated application terminology or status data from reference documentation.</p>
  <h2>External textbook memory</h2>
  <p><a href="https://github.com/facebookresearch/atlas-lean">ATLAS v1</a>, by
  Ahmad Rammal, Niket Patel, Fabian Gloeckle, Amaury Hayat, Julia Kempe, Remi
  Munos, Charles Arnal, and Vivien Cabannes, is indexed locally as a pinned
  external theorem-retrieval surface. Its source and generated theorem text
  remain under its CC BY-NC 4.0 and no-training terms; they are not copied into
  project-owned Apache-2.0 distribution. Upstream compilation or evaluation does not replace an
  ASPBE adapter and Lean gate.</p>
  <h2>Interface inspiration</h2>
  <p><a href="https://statsmllib.github.io/">StatsMLlib</a> demonstrates a useful
  textbook organization: a persistent book map, selected formulas, natural-language
  readings, source locations, organizers, and a visible contribution path.
  QuantumComputinglib uses independently written templates, CSS, JavaScript, diagrams, and
  quantum-computing content.</p>
  <p>The local-compiler boundary and reviewed LaTeX-to-Lean workspace follow the
  proven design used by
  <a href="https://github.com/DakeBU/Auto-Bandit-RL-Proof-In-Sleep">Auto-Bandit-RL-Proof-In-Sleep</a>:
  the public site is static, while a loopback-only companion server may invoke the
  pinned Lean toolchain on temporary snippets. No bandit chapters, declarations,
  statuses, or theorem data are copied into QuantumComputinglib.</p>
</section>"""
    body += license_body
    return page_template(
        title="Attribution",
        route="attribution/",
        current="",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
    )


def render_blueprint_entry(
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> str:
    body = """
<section class="hero">
  <p class="eyebrow">Stable Blueprint entry</p>
  <h1>ASPBE Verso Blueprint</h1>
  <p class="lede">The Blueprint resolves Lean declaration references during its
  own build. The unified site adds guided chapters and implementation status while
  retaining the existing multi-page Blueprint URL.</p>
  <div class="hero-actions">
    <a class="button" href="html-multi/index.html">Open multi-page Blueprint</a>
    <a class="button secondary" href="../library/index.html">Open Library Explorer</a>
  </div>
</section>"""
    return page_template(
        title="Verso Blueprint",
        route="blueprint/",
        current="",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
    )


def replay_record(
    replay: dict[str, object], selector: dict[str, str]
) -> dict[str, object] | None:
    for group in replay.get("cases", []):
        if group.get("case") != selector.get("case"):
            continue
        name = selector.get("name")
        if name is None:
            return group
        for case in group.get("cases", []):
            if case.get("name") == name:
                return {**case, "semantic_tier": group.get("semantic_tier")}
        acceptance = group.get("acceptance", {})
        for route in acceptance.get("routes", []):
            if route.get("name") == name:
                return {**route, "semantic_tier": acceptance.get("semantic_tier")}
    return None


def load_example_cases(
    declarations: dict[str, dict[str, object]], replay: dict[str, object]
) -> list[dict[str, object]]:
    data = load_json(WEBSITE_ROOT / "example-cases.json")
    if data.get("schemaVersion") != 2 or not isinstance(data.get("cases"), list):
        raise SystemExit("website/example-cases.json has an unsupported schema")
    seen: set[str] = set()
    cases: list[dict[str, object]] = []
    for case in data["cases"]:
        case_slug = str(case.get("slug", ""))
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", case_slug):
            raise SystemExit(f"Invalid example-case slug: {case_slug!r}")
        if case_slug in seen:
            raise SystemExit(f"Duplicate example-case slug: {case_slug}")
        seen.add(case_slug)
        required = (
            "title", "shortTitle", "kind", "status", "semanticTier", "problem",
            "formula", "contract", "symbols", "circuit", "evolution", "qiskit",
            "preset", "summary", "source", "contributor", "limitations",
        )
        absent = [field for field in required if not case.get(field)]
        if absent:
            raise SystemExit(f"Example case {case_slug} lacks fields: {absent}")
        anchors = case.get("leanAnchors", [])
        if case.get("status") == "certified" and not anchors:
            raise SystemExit(f"Certified example {case_slug} has no Lean roots")
        missing = [name for name in anchors if name not in declarations]
        if missing:
            raise SystemExit(
                f"Example case {case_slug} names declarations absent from inventory: {missing}"
            )
        stages = case["evolution"].get("stages", [])
        if not stages:
            raise SystemExit(f"Example case {case_slug} has no evolution stages")
        for stage in stages:
            stage_anchor = stage.get("leanAnchor")
            if stage_anchor not in anchors:
                raise SystemExit(
                    f"Example case {case_slug} evolution root is not listed in leanAnchors: "
                    f"{stage_anchor}"
                )
            score = stage.get("score")
            if score is not None and (
                not isinstance(score, list)
                or len(score) != 4
                or any(not isinstance(value, int) or value < 0 for value in score)
            ):
                raise SystemExit(f"Example case {case_slug} has an invalid score: {score}")
            if str(stage.get("status", "")).startswith("Strictly better") and (
                "betterThan" not in str(stage_anchor)
            ):
                raise SystemExit(
                    f"Example case {case_slug} advertises strict improvement without "
                    "a named Lean betterThan theorem"
                )
            try:
                stage_circuit_latex(case_slug, str(stage.get("name", "")))
            except KeyError as error:
                raise SystemExit(
                    f"Example case {case_slug} has no editable circuit LaTeX for "
                    f"stage {stage.get('name')!r}"
                ) from error
        export_path = ROOT / str(case["qiskit"].get("path", ""))
        if not export_path.is_file() or ROOT not in export_path.resolve().parents:
            raise SystemExit(
                f"Example case {case_slug} has no repository Qiskit export: {export_path}"
            )
        evidence = None
        selector = case.get("replaySelector")
        if selector:
            evidence = replay_record(replay, selector)
        if case.get("status") == "certified":
            if not case.get("semanticTier") or not case.get("source"):
                raise SystemExit(f"Certified example {case_slug} lacks tier or provenance")
            # The site itself is built only after `load_gate_report` has accepted
            # the current commit.  Executable replay is deliberately not a proof
            # gate for an individual mathematical claim.
        cases.append({**case, "executionEvidence": evidence})
    return cases


def compact_json(value: object) -> str:
    return html.escape(json.dumps(value, ensure_ascii=False, separators=(",", ":")))


def case_kind_label(kind: object) -> str:
    return {
        "statePreparation": "State preparation",
        "operatorBlockEncoding": "Block encoding",
    }.get(str(kind), str(kind))


def render_case_score(stage: dict[str, object]) -> str:
    score = stage.get("score")
    if score is None:
        return '<span class="score-unranked">not ranked at this tier</span>'
    values = list(score)  # type: ignore[arg-type]
    labels = ("gates", "depth", "aux", "oracles")
    cells = "".join(
        f'<span><strong>{int(value)}</strong><small>{label}</small></span>'
        for value, label in zip(values, labels, strict=True)
    )
    breakdown = stage.get("gateBreakdown")
    breakdown_html = ""
    if isinstance(breakdown, dict):
        breakdown_html = (
            '<p class="score-breakdown"><strong>Primitive split</strong>'
            f'<span>{int(breakdown["singleQubit"])} single-qubit</span>'
            f'<span>{int(breakdown["cx"])} CX</span></p>'
        )
    tier = str(stage.get("instructionTier", ""))
    tier_html = f'<p class="score-tier">{html.escape(tier)}</p>' if tier else ""
    return f'<div class="score-panel"><div class="score-tuple" aria-label="resource score">{cells}</div>{breakdown_html}{tier_html}</div>'


def render_copyable_source(title: str, source: str, language: str) -> str:
    return f"""<details class="copy-source-panel">
  <summary>{html.escape(title)}</summary>
  <div class="copy-source-actions"><button type="button" data-copy-source>Copy</button></div>
  <pre><code class="language-{html.escape(language)}">{html.escape(source)}</code></pre>
</details>"""


def extract_tex_argument(source: str, command: str) -> str | None:
    """Extract one balanced braced argument from a small reviewed TeX command."""
    start = source.find(command)
    if start < 0:
        return None
    brace = source.find("{", start + len(command))
    if brace < 0:
        return None
    depth = 0
    for index in range(brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[brace + 1:index]
    return None


def circuit_plain_label(source: str) -> str:
    """Produce a compact readable label for the reviewed quantikz subset."""
    label = source.replace("$", "")
    label = re.sub(r"\\ket\{([^{}]*)\}", r"|\1>", label)
    label = re.sub(r"\\(?:mathrm|textrm|rm)\s*\{([^{}]*)\}", r"\1", label)
    replacements = {
        r"\dagger": "†",
        r"\perp": "perp",
        r"\alpha": "alpha",
        r"\theta": "theta",
        r"\arccos": "arccos",
        r"\mathrm": "",
        r"\rm": "",
        r"\!": "",
        r"\,": " ",
        r"\;": " ",
    }
    for old, new in replacements.items():
        label = label.replace(old, new)
    label = label.replace("{", "").replace("}", "")
    label = label.replace("\\", "")
    return re.sub(r"\s+", " ", label).strip()


def quantikz_rows(source: str) -> list[list[str]]:
    body = re.sub(r"\\begin\{quantikz\}(?:\[[^\]]*\])?", "", source)
    body = body.replace(r"\end{quantikz}", "")
    rows = re.split(r"\\\\\s*(?:\n|$)", body.strip())
    return [[cell.strip() for cell in row.split("&")] for row in rows if row.strip()]


def render_quantikz_svg(source: str, title: str) -> str:
    """Render the repository's reviewed grouped-register quantikz subset as SVG."""
    rows = quantikz_rows(source)
    row_gap = 62
    col_gap = 132
    left = 118
    top = 38
    columns = max((len(row) for row in rows), default=1)
    width = max(430, left + max(1, columns - 1) * col_gap + 116)
    height = max(104, top * 2 + max(0, len(rows) - 1) * row_gap)
    parts = [
        f'<svg class="quantikz-preview" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{html.escape(title)}"><title>{html.escape(title)}</title>'
    ]
    for row_index, row in enumerate(rows):
        y = top + row_index * row_gap
        parts.append(f'<line class="qc-wire" x1="92" y1="{y}" x2="{width - 34}" y2="{y}"/>')
        for col_index, cell in enumerate(row):
            x = left + col_index * col_gap
            left_label = extract_tex_argument(cell, r"\lstick")
            right_label = extract_tex_argument(cell, r"\rstick")
            gate_label = extract_tex_argument(cell, r"\gate")
            if left_label is not None:
                parts.append(
                    f'<text class="qc-register" x="8" y="{y + 5}">'
                    f'{html.escape(circuit_plain_label(left_label))}</text>'
                )
            if gate_label is not None:
                wires_match = re.search(r"\\gate\[wires=(\d+)\]", cell)
                wires = int(wires_match.group(1)) if wires_match else 1
                gate_height = 38 + (wires - 1) * row_gap
                gate_y = y - 19
                parts.append(
                    f'<rect class="qc-gate" x="{x - 48}" y="{gate_y}" width="96" '
                    f'height="{gate_height}" rx="4"/>'
                )
                parts.append(
                    f'<text class="qc-gate-label" x="{x}" y="{gate_y + gate_height / 2 + 4}" '
                    f'text-anchor="middle">{html.escape(circuit_plain_label(gate_label))}</text>'
                )
            ctrl = re.search(r"\\ctrl\{(-?\d+)\}", cell)
            if ctrl:
                target_y = y + int(ctrl.group(1)) * row_gap
                parts.append(f'<line class="qc-control" x1="{x}" y1="{y}" x2="{x}" y2="{target_y}"/>')
                parts.append(f'<circle class="qc-control-dot" cx="{x}" cy="{y}" r="5"/>')
            if r"\targ" in cell:
                parts.append(f'<circle class="qc-target" cx="{x}" cy="{y}" r="12"/>')
                parts.append(f'<line class="qc-target" x1="{x - 8}" y1="{y}" x2="{x + 8}" y2="{y}"/>')
                parts.append(f'<line class="qc-target" x1="{x}" y1="{y - 8}" x2="{x}" y2="{y + 8}"/>')
            if r"\meter" in cell:
                parts.append(f'<path class="qc-meter" d="M{x - 15},{y + 10} A15,15 0 0 1 {x + 15},{y + 10}"/>')
                parts.append(f'<line class="qc-meter" x1="{x}" y1="{y + 8}" x2="{x + 9}" y2="{y - 8}"/>')
            if right_label is not None:
                parts.append(
                    f'<text class="qc-output" x="{min(width - 190, x - 20)}" y="{y - 12}">'
                    f'{html.escape(circuit_plain_label(right_label))}</text>'
                )
    parts.append("</svg>")
    return "".join(parts)


def case_stage_gate_labels(case: dict[str, object], stage: dict[str, object]) -> list[str]:
    stage_name = str(stage.get("name", "")).lower()
    if "audit" in str(stage.get("iteration", "")).lower():
        return ["address audit", "padded-seven source"]
    circuit_stages = list(case["circuit"]["stages"])
    for circuit_stage in circuit_stages:
        label = str(circuit_stage.get("label", "")).lower()
        if any(word in stage_name for word in re.findall(r"[a-z0-9]+", label) if len(word) > 3):
            return [str(gate) for gate in circuit_stage.get("gates", [])]
    stage_index = list(case["evolution"]["stages"]).index(stage)
    selected = circuit_stages[min(stage_index, len(circuit_stages) - 1)]
    return [str(gate) for gate in selected.get("gates", [])]


def render_stage_circuit_visual(case: dict[str, object], stage: dict[str, object]) -> str:
    gates = "".join(
        f'<span class="stage-circuit-gate">{html.escape(label)}</span>'
        for label in case_stage_gate_labels(case, stage)
    )
    return f"""<div class="stage-circuit-visual" aria-label="logical circuit stage">
  <span class="stage-circuit-input">clean input</span><span class="stage-circuit-wire"></span>
  {gates}<span class="stage-circuit-wire"></span><span class="stage-circuit-output">certified branch</span>
</div>"""


def render_case_circuit(case: dict[str, object]) -> str:
    circuit = case["circuit"]
    stages: list[str] = []
    for index, stage in enumerate(circuit["stages"], start=1):
        gates = "".join(
            f'<span class="gate-chip">{html.escape(str(gate))}</span>'
            for gate in stage.get("gates", [])
        )
        stages.append(f"""<article class="circuit-stage">
  <span class="stage-index">{index:02d}</span>
  <h3>{html.escape(str(stage['label']))}</h3>
  <p>{html.escape(str(stage['detail']))}</p>
  <div class="gate-row">{gates}</div>
</article>""")
    return f"""<div class="circuit-registers"><strong>Register order</strong><span>{html.escape(str(circuit['registers']))}</span></div>
<div class="circuit-flow">{''.join(stages)}</div>"""


def render_executable_evidence(case: dict[str, object], prefix: str) -> str:
    qiskit = case["qiskit"]
    artifact = str(qiskit["path"])
    manifest_path = ROOT / Path(artifact).parents[1] / "manifest.json"
    manifest = load_json(manifest_path) if manifest_path.is_file() else {}
    checks = manifest.get("checkBackends", {}) if isinstance(manifest, dict) else {}
    checks = checks if isinstance(checks, dict) else {}

    def check_status(name: str, fallback: str) -> str:
        value = checks.get(name, {})
        return str(value.get("status", fallback)) if isinstance(value, dict) else fallback

    lean_status = "passed" if case.get("status") == "certified" else "open"
    rows = [
        ("Internal canonical evaluator", "Reference semantics for primitive canonical IR", check_status("internalCanonicalEvaluator", "open"), "metrics manifest"),
        ("Qiskit replay", "Gate-by-gate numerical screening", check_status("qiskitOperator", "artifact available"), artifact),
        ("OpenQASM 3 round-trip", "Strict serialization, import, and semantic replay", check_status("openqasm3RoundTrip", "not recorded"), "QASM and report when generated"),
        ("Lean certificate", "Exact proof authority at the page's stated semantic tier", lean_status, f"{len(case.get('leanAnchors', []))} named root(s)"),
    ]
    legacy = checks.get("legacyDenseDiagnostic")
    if isinstance(legacy, dict):
        rows.insert(1, (
            "Legacy dense diagnostic", "Historical numerical composition; explicitly non-primitive and not T3",
            str(legacy.get("status", "recorded")), "numericUnitary + numericCleanBlock",
        ))
    rendered = "".join(
        f"<tr><th>{html.escape(name)}</th><td>{html.escape(role)}</td><td>{badge(status)}</td><td><code>{html.escape(evidence)}</code></td></tr>"
        for name, role, status, evidence in rows
    )
    return f'<table class="proof-steps"><thead><tr><th>Backend / artifact</th><th>Role</th><th>Status</th><th>Evidence</th></tr></thead><tbody>{rendered}</tbody></table>'


def render_case_evolution(
    case: dict[str, object], declarations: dict[str, dict[str, object]], prefix: str
) -> str:
    points: list[str] = []
    for stage in case["evolution"]["stages"]:
        anchor = str(stage["leanAnchor"])
        circuit_latex = stage_circuit_latex(str(case["slug"]), str(stage["name"]))
        points.append(f"""<article class="evolution-point">
  <div class="iteration-mark"><span>iteration</span><strong>{html.escape(str(stage['iteration']))}</strong></div>
  <div class="evolution-copy">
    <div class="evolution-heading"><h3>{html.escape(str(stage['name']))}</h3><span>{html.escape(str(stage['status']))}</span></div>
    <p>{html.escape(str(stage['description']))}</p>
    <figure class="stage-circuit-render"><div class="stage-circuit-canvas">{render_quantikz_svg(circuit_latex, str(stage['name']))}</div><figcaption>Grouped-register circuit. Open the source or workbench to adapt notation.</figcaption></figure>
    <a class="theorem-root" href="{module_url(prefix, declarations[anchor])}"><span>Lean root</span><code>{html.escape(anchor)}</code></a>
    <a class="text-link stage-edit-link" href="#case-workbench" data-edit-circuit="{html.escape(str(stage['name']))}">Edit and preview this stage &#8594;</a>
    {render_copyable_source('Copy this stage as quantikz', circuit_latex, 'latex')}
  </div>
  {render_case_score(stage)}
</article>""")
    audit = str(case["evolution"].get("scoreAudit", ""))
    audit_html = f'<aside class="case-score-audit"><strong>Cost audit</strong><p>{html.escape(audit)}</p></aside>' if audit else ""
    return f"""<p class="figure-caption">{html.escape(str(case['evolution']['caption']))}</p>{audit_html}
<div class="evolution-track">{''.join(points)}</div>"""


def render_case_copy_packet(case: dict[str, object]) -> str:
    stage_sources = "\n\n".join(
        "% " + str(stage["name"]) + "\n" +
        stage_circuit_latex(str(case["slug"]), str(stage["name"]))
        for stage in case["evolution"]["stages"]
    )
    construction = (
        "% Requires: \\usepackage{quantikz}\n"
        "\\paragraph{Construction.}\n"
        "\\[\n" + str(case["formula"]) + "\n\\]\n\n" + stage_sources
    )
    proof_steps = "\n".join(
        f"  \\item {str(stage['description'])}"
        for stage in case["evolution"]["stages"]
    )
    proof = (
        "\\paragraph{Proof.}\n"
        + str(case["contract"]) + "\n"
        "\\begin{enumerate}\n" + proof_steps + "\n\\end{enumerate}\n"
        "Each advertised certificate is the named Lean declaration linked on this page."
    )
    lean = "import QuantumBlockEncoding\n\n" + "\n".join(
        f"#check {anchor}" for anchor in case["leanAnchors"]
    )
    editor_data = {
        "formula": str(case["formula"]),
        "proofSteps": [str(stage["description"]) for stage in case["evolution"]["stages"]],
        "circuits": {
            str(stage["name"]): stage_circuit_latex(str(case["slug"]), str(stage["name"]))
            for stage in case["evolution"]["stages"]
        },
    }
    encoded_editor_data = (
        json.dumps(editor_data, ensure_ascii=True)
        .replace("&", r"\u0026")
        .replace("<", r"\u003c")
        .replace(">", r"\u003e")
    )
    options = "".join(
        f'<option value="{html.escape(name)}">{html.escape(name)}</option>'
        for name in editor_data["circuits"]
    )
    return f"""<section class="content-section case-workbench" id="case-workbench" data-case-workbench>
<div class="section-heading"><p class="eyebrow">Reader workbench</p><h2>Edit, preview, then copy</h2><p>Change symbols, language, proof steps, or the grouped-register circuit locally in your browser. The preview is explanatory; the linked Lean declaration remains the certificate.</p></div>
<script type="application/json" data-case-editor-data>{encoded_editor_data}</script>
<div class="case-editor-grid">
  <section class="case-editor-panel"><div class="editor-panel-heading"><h3>Mathematical construction</h3><button type="button" data-copy-editor="formula">Copy</button></div><textarea data-case-formula spellcheck="false" aria-label="Editable construction LaTeX"></textarea><div class="case-live-preview math-preview" data-case-formula-preview aria-live="polite"></div></section>
  <section class="case-editor-panel"><div class="editor-panel-heading"><h3>Proof steps</h3><button type="button" data-copy-editor="proof">Copy as LaTeX</button></div><p class="field-note">One step per line. Natural language and inline mathematics are both accepted.</p><textarea data-case-proof spellcheck="true" aria-label="Editable proof steps"></textarea><ol class="case-live-preview proof-preview" data-case-proof-preview></ol></section>
  <section class="case-editor-panel circuit-editor-panel"><div class="editor-panel-heading"><h3>Quantum circuit</h3><button type="button" data-copy-editor="circuit">Copy quantikz</button></div><label class="field-label">Stage<select data-case-circuit-select>{options}</select></label><textarea data-case-circuit spellcheck="false" aria-label="Editable quantikz circuit"></textarea><div class="case-live-preview circuit-live-preview" data-case-circuit-preview></div><p class="field-note" data-case-circuit-diagnostic></p></section>
</div>
</section>
<section class="content-section" id="copy-construction">
<div class="section-heading"><p class="eyebrow">Complete packet</p><h2>Copy the reviewed construction and proof</h2><p>The packet below is generated from the reviewed case record. The exact primitive authority is the linked Lean source and executable artifact.</p></div>
<div class="copy-packet-grid">
{render_copyable_source('Construction and circuit LaTeX', construction, 'latex')}
{render_copyable_source('English proof LaTeX', proof, 'latex')}
{render_copyable_source('Lean declaration retrieval block', lean, 'lean')}
</div></section>"""


def render_case_verification_status(
    case: dict[str, object], declarations: dict[str, dict[str, object]], prefix: str
) -> str:
    rows = case.get("verificationStatus", [])
    if not rows:
        return ""
    rendered = []
    for label, status, root in rows:
        declaration = declarations[str(root)]
        rendered.append(
            f"<tr><th>{html.escape(str(label))}</th><td>{badge(str(status))}</td>"
            f'<td><a href="{module_url(prefix, declaration)}"><code>{html.escape(str(root))}</code></a></td></tr>'
        )
    return f"""<section class="content-section" id="verification-status">
<div class="section-heading"><p class="eyebrow">Machine-checked status</p><h2>What is closed in this checkout</h2></div>
<table class="proof-steps"><thead><tr><th>Obligation</th><th>Status</th><th>Lean authority</th></tr></thead><tbody>{''.join(rendered)}</tbody></table>
</section>"""


def render_source_interpretation(case: dict[str, object]) -> str:
    decisions = case.get("sourceInterpretation", [])
    if not decisions:
        return ""
    items = "".join(f"<li>{html.escape(str(item))}</li>" for item in decisions)
    return f"""<section class="content-section" id="source-interpretation">
<div class="section-heading"><p class="eyebrow">Source audit</p><h2>Source interpretation decisions</h2><p>These choices are part of the formal benchmark contract, not silent implementation details.</p></div>
<ol class="reading-steps">{items}</ol>
</section>"""


def render_example_case_index(
    cases: list[dict[str, object]], coverage: dict[str, object],
    gate: dict[str, object], context: dict[str, object]
) -> str:
    cards = []
    for case in cases:
        cards.append(f"""<article class="case-card">
  <p class="eyebrow">{html.escape(case_kind_label(case['kind']))}</p>
  <h2><a href="{html.escape(str(case['slug']))}/index.html">{html.escape(str(case['title']))}</a></h2>
  <p>{html.escape(str(case['summary']))}</p>
  <div class="case-formula">{render_math_tex(str(case['formula']))}</div>
  <div class="case-meta">{badge('Lean certified' if case['status'] == 'certified' else 'Partial route')}<span>{html.escape(str(case['semanticTier']))}</span></div>
</article>""")
    body = f"""<section class="hero"><p class="eyebrow">Reproducible reading paths</p>
<h1>Case studies, from equation to circuit</h1><p class="lede">Each case begins with the operator or target state, fixes the acceptance contract, and then shows the circuit and resource trace. “Certified” means a named Lean root compiled in this checkout. Qiskit and other fast backends may screen and prioritize routes; a floating-point match alone is not the final exact proof.</p></section>
<section class="content-section case-reading-key"><h2>How to read a score</h2><p>The tuple is ordered lexicographically as <strong>(gate count, parallel depth, auxiliary qubits, oracle calls)</strong>. A page says “strictly better” only when it links the corresponding Lean <code>betterThan</code> theorem. Routes at different semantic tiers are not compared.</p></section>
<section class="content-section"><div class="case-grid">{''.join(cards)}</div></section>
<section class="content-section contribution-callout"><h2>Contribute a checked variant</h2><p>Generated drafts are welcome. Public retrieval begins only after review, a repository declaration, and the advertised gates pass.</p><div class="link-row"><a class="button" href="../task-builder/index.html">Share a State Preparation example</a><a class="button secondary" href="../community/index.html">Share a Block Encoding example</a></div></section>"""
    return page_template(title="Example cases", route="example-cases/", current="example-cases/", body=body, coverage=coverage, gate=gate, context=context)


def render_example_case(
    case: dict[str, object], declarations: dict[str, dict[str, object]],
    coverage: dict[str, object], gate: dict[str, object], context: dict[str, object]
) -> str:
    route = f"example-cases/{case['slug']}/"
    prefix = prefix_for(route)
    anchors = "".join(
        f'<li><a href="{module_url(prefix, declarations[name])}"><code>{html.escape(name)}</code></a>'
        f'<span>{html.escape(str(declarations[name]["source"]))}:{int(declarations[name]["line"])}</span></li>'
        for name in case["leanAnchors"]
    )
    symbols = "".join(
        f'<div><dt><code>{html.escape(str(symbol))}</code></dt><dd>{html.escape(str(reading))}</dd></div>'
        for symbol, reading in case["symbols"]
    )
    qiskit = case["qiskit"]
    preset = compact_json(case["preset"])
    body = f"""<article class="case-detail">
<header class="hero case-hero"><p class="eyebrow">{html.escape(case_kind_label(case['kind']))} · {html.escape(str(case['semanticTier']))}</p><h1>{html.escape(str(case['title']))}</h1><p class="lede">{html.escape(str(case['problem']))}</p><div class="case-status-line">{badge('Lean certified' if case['status'] == 'certified' else 'Partial route')}<span>{html.escape(str(case['summary']))}</span></div></header>
<section class="content-section case-problem" id="mathematical-target"><div class="section-heading"><p class="eyebrow">Mathematical target</p><h2>The equation being studied</h2></div>{render_math_tex(str(case['formula']))}<p class="contract-reading">{html.escape(str(case['contract']))}</p><dl class="symbol-key">{symbols}</dl></section>
<section class="content-section" id="circuit"><div class="section-heading"><p class="eyebrow">Circuit anatomy</p><h2>How the candidate acts</h2><p>These blocks show logical stages and register responsibilities. They do not pretend an unresolved logical oracle is already a primitive hardware gate.</p></div>{render_case_circuit(case)}</section>
<section class="content-section" id="evolution"><div class="section-heading"><p class="eyebrow">Auditable evolution</p><h2>Candidate and proof progression</h2></div>{render_case_evolution(case, declarations, prefix)}</section>
{render_case_copy_packet(case)}
{render_case_verification_status(case, declarations, prefix)}
{render_source_interpretation(case)}
<section class="content-section" id="lean-certificate"><div class="section-heading"><p class="eyebrow">Proof authority</p><h2>Named Lean certificates</h2><p>These declarations, compiled by the current Lean gate, support the mathematical and resource claims above.</p></div><ul class="case-declaration-list">{anchors}</ul></section>
<section class="content-section export-section" id="executable-evidence"><div class="section-heading"><p class="eyebrow">Optional executable checks and outputs</p><h2>Executable verification and exports</h2><p>Checking and artifact selection are independent. A user may screen with Qiskit, OpenQASM round-trip, both, or neither, then request a different set of output files.</p></div>{render_executable_evidence(case, prefix)}<p>{html.escape(str(qiskit['role']))}</p><dl class="definition-list"><dt>Current runnable artifact</dt><dd><code>{html.escape(str(qiskit['path']))}</code></dd><dt>Command</dt><dd><pre><code>{html.escape(str(qiskit['command']))}</code></pre></dd></dl><div class="callout warning"><strong>Trust boundary.</strong> Fast executable checks may reject, rank, or queue a route for formalization. Floating-point tolerances do not replace the exact Lean roots above; an external exact certificate contributes only after a Lean checker verifies it.</div></section>
<section class="content-section"><dl class="definition-list"><dt>Source</dt><dd>{html.escape(str(case['source']))}</dd><dt>Contributor</dt><dd>{html.escape(str(case['contributor']))}</dd><dt>Current boundary</dt><dd>{html.escape(str(case['limitations']))}</dd></dl><div class="link-row"><a class="button" href="{prefix}task-builder/index.html?case={html.escape(str(case['slug']))}">Load in task builder</a><a class="button secondary" href="{prefix}community/index.html?case={html.escape(str(case['slug']))}">Contribute a variant</a></div></section>
<script type="application/json" data-example-preset>{preset}</script></article>"""
    toc = [("mathematical-target", "Mathematical target"), ("circuit", "Circuit anatomy"), ("evolution", "Evolution"), ("copy-construction", "Copy construction")]
    if case.get("verificationStatus"):
        toc.append(("verification-status", "Verification status"))
    if case.get("sourceInterpretation"):
        toc.append(("source-interpretation", "Source decisions"))
    toc.extend([("lean-certificate", "Lean certificates"), ("executable-evidence", "Executable evidence")])
    return page_template(title=str(case["title"]), route=route, current=route, body=body, coverage=coverage, gate=gate, context=context, toc=toc, extra_scripts=("static/case-workbench.js",))


def render_task_builder(
    coverage: dict[str, object], gate: dict[str, object], context: dict[str, object]
) -> str:
    body = """<section class="hero task-builder-intro"><p class="eyebrow">User-owned execution</p>
<h1>Build an ASPBE task</h1><p class="lede">Describe a state or operator, choose fast executable screening independently from final artifacts, and send the packet only to a runner you control. Exact certification still enters through Lean.</p></section>
<div class="task-builder" data-task-builder>
<section class="builder-panel"><h2>Target and acceptance contract</h2>
<label>Example preset<select id="benchmarkPreset"><option value="custom">Custom task</option></select></label>
<label>Task name<input id="taskName" value="state-preparation-task" autocomplete="off"></label>
<div class="form-grid"><label>Application<select id="mode"><option value="statePreparation">State Preparation</option><option value="operatorBlockEncoding">Block Encoding</option><option value="paperBenchmark">Paper reproduction</option><option value="exploratoryConstruction">Certified improvement</option></select></label><label>Harness<select id="harnessMode"><option value="hierarchical">Hierarchical</option><option value="game">Game</option><option value="parallel">Compare both</option></select></label></div>
<label>Target state, operator, or oracle<textarea id="oracleDescription">Prepare (|0> + |1>) / sqrt(2) from |0></textarea></label>
<div class="form-grid"><label>Normalizer alpha / state norm<input id="normalizer" value="1"></label><label>Initial or clean state<input id="projector" value="|0^n>"></label></div>
<label>Constraints<textarea id="constraints" placeholder="Register order, exact or approximate tolerance, allowed gates, and non-goals."></textarea></label>
<fieldset class="executable-policy"><legend>Executable verification</legend>
<div class="section-heading"><p>Choose an intermediate checker independently from the files you want to keep.</p></div>
<div class="backend-options" role="radiogroup" aria-label="Intermediate executable checker">
<label class="option-row"><input name="intermediateBackend" type="radio" value="none"><span><strong>None</strong><small>Skip intermediate executable screening.</small></span></label>
<label class="option-row"><input name="intermediateBackend" type="radio" value="qiskitOperator"><span><strong>Qiskit Operator check</strong><small>Builds the circuit gate by gate and numerically checks unitarity and the clean block.</small></span></label>
<label class="option-row"><input name="intermediateBackend" type="radio" value="openqasm3RoundTrip"><span><strong>OpenQASM 3 strict round-trip</strong><small>Writes canonical IR, parses the supported subset, reconstructs the IR, and checks its semantics.</small></span></label>
<label class="option-row"><input name="intermediateBackend" type="radio" value="both" checked><span><strong>Both</strong><small>Recommended. Both independent checks must pass when required.</small></span></label>
</div>
<div class="form-grid"><label class="check-row"><input id="checkRequired" type="checkbox" checked> Treat selected checker as required</label><label class="check-row"><input id="requireCanonicalRoundTrip" type="checkbox" checked> Require canonical QASM round-trip</label><label>Unitarity tolerance<input id="unitarityTolerance" type="number" value="1e-10" min="0" step="any"></label><label>Clean-block tolerance<input id="cleanBlockTolerance" type="number" value="1e-10" min="0" step="any"></label></div>
<p class="hint">Neither numerical backend replaces Lean. A passing check may screen and prioritize a candidate; exact proof authority requires a Lean root.</p>
<h3>Export artifacts</h3><div class="artifact-options"><label class="check-row"><input id="exportCanonicalIr" type="checkbox" checked> Canonical circuit IR</label><label class="check-row"><input id="exportQiskitPython" type="checkbox" checked> Qiskit Python</label><label class="check-row"><input id="exportOpenQasm3" type="checkbox" checked> OpenQASM 3</label><label class="check-row"><input id="exportMetricsJson" type="checkbox" checked> Verification metrics</label><label class="check-row"><input id="exportCircuitText" type="checkbox"> Circuit text</label></div>
</fieldset>
<fieldset><legend>API ownership</legend><div class="form-grid"><label>Run location<select id="runLocation"><option value="localCli">Local CLI</option><option value="selfHostedRunner">My self-hosted runner</option><option value="browserPacketOnly">Packet only</option></select></label><label>Provider<select id="apiProvider"><option value="openai">OpenAI</option><option value="anthropic">Anthropic</option><option value="gemini">Gemini</option><option value="custom">Custom endpoint</option></select></label><label>Model<input id="defaultModel" value="use profile default"></label><label>Runner endpoint<input id="runnerEndpoint" value="/api/run-task"></label></div><label>Session-only API key<input id="apiKey" type="password" autocomplete="off" data-never-persist></label><p class="hint">The key is never stored, exported, logged, or placed in a contribution URL.</p></fieldset>
<details><summary>Advanced search fields</summary><label>Known baseline<textarea id="baseline"></textarea></label><label>User insight<textarea id="userInsight"></textarea></label><label>Proposed construction or proof<textarea id="proposedProof"></textarea></label></details>
<div class="builder-actions"><button id="buildPacket" type="button">Build task packet</button><button id="runWithApi" type="button">Run with my API</button><button id="copyPacket" class="secondary" type="button">Copy</button><button id="downloadPacket" class="secondary" type="button">Download</button></div><p id="runnerStatus" aria-live="polite"></p></section>
<section class="builder-panel"><h2>Generated packet</h2><pre id="packet" class="packet" tabindex="0"></pre><div class="memory-actions"><button id="savePrivateCase" type="button">Save privately</button><button id="forgetPrivateCase" class="secondary" type="button">Forget</button><button id="exportPrivateCases" class="secondary" type="button">Export JSON</button><label class="file-button">Import JSON<input id="importPrivateCases" type="file" accept="application/json"></label><button id="submitCase" class="secondary" type="button">Submit for review</button></div><p id="memoryStatus" aria-live="polite"></p><details><summary>Runner dashboard JSON</summary><textarea id="dashboardJson"></textarea><button id="renderDashboard" type="button">Render JSON</button><div id="dashboardView"></div></details></section></div>"""
    return page_template(title="Task builder", route="task-builder/", current="task-builder/", body=body, coverage=coverage, gate=gate, context=context, extra_scripts=("static/case-memory.js", "static/task-builder.js"))


def write_page(output: Path, route: str, content: str) -> None:
    destination = output / route / "index.html" if route else output / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8", newline="\n")


def build_search_index(
    output: Path,
    declarations: list[dict[str, object]],
    cases: list[dict[str, object]],
) -> dict[str, object]:
    entries: list[dict[str, str]] = []
    for declaration in declarations:
        entries.append(
            {
                "type": "declaration",
                "kind": str(declaration["kind"]),
                "title": str(declaration["fullName"]),
                "summary": str(declaration["plainEnglish"]),
                "url": (
                    f"library/modules/{module_slug(str(declaration['source']))}/"
                    f"index.html#{declaration_anchor(str(declaration['fullName']))}"
                ),
            }
        )
    for case in cases:
        entries.append(
            {
                "type": "exampleCase",
                "kind": str(case["kind"]),
                "title": str(case["title"]),
                "summary": str(case["summary"]),
                "url": f"example-cases/{case['slug']}/index.html",
            }
        )
    page_entries = [
        ("QuantumComputinglib", "Formal quantum computing chapters, declarations, and tools", "index.html"),
        ("Our place in Math 2.0", "Nine contribution directions: foundations, understanding and research agenda", "math-2-0/index.html"),
        ("State preparation", "Prepare a normalized target state from the all-zero basis state", "state-preparation/index.html"),
        ("Block encoding", "Encode a scaled operator in the clean block of a larger unitary", "block-encoding/index.html"),
        ("Implementation Map", "Mathematical goals connected to exact Lean declarations", "implementation-map/index.html"),
        ("Robin paper map", "Original Robin construction statements mapped to compiled Lean structures and open obligations", "case-studies/robin/index.html"),
        ("Lean Library Explorer", "Search the complete public declaration inventory", "library/index.html"),
        ("Underlying Lean Graph of Libraries", "Explore generated Lean import topology and declaration branches", "lean-graph/index.html"),
        ("Progress and Roadmap", "Compiled, partial, experimental, planned, and blocked routes", "roadmap/index.html"),
        ("ASPBE harness", "Candidate generation, resource scoring, proof, and validation", "workflow/index.html"),
        ("Live formalization workspace", "Compare LaTeX with Lean and compile through the local companion server", "ide/index.html"),
        ("Quantum Lean ecosystem", "ASPBE and selected external formalization libraries", "ecosystem/index.html"),
        ("Contribute", "Develop and submit a sourced teaching, theorem, adapter, or validation contribution", "community/index.html"),
        ("Contributors", "Integrated external contributions and public credit", "contributors/index.html"),
        ("Organizers", "Current ASPBE authors and contributor credit policy", "organizers/index.html"),
    ]
    page_entries.extend(
        (
            str(chapter["title"]),
            str(chapter["summary"]),
            f"chapters/{chapter['slug']}/index.html",
        )
        for chapter in CHAPTERS
    )
    page_entries.extend(
        (
            str(part["title"]),
            str(part["summary"]),
            f"{part['route']}index.html",
        )
        for part in load_json(WEBSITE_ROOT / "curriculum-parts.json")["parts"]
        if part["id"] in {
            "part-iii-quantum-information",
            "part-iv-quantum-scientific-computing",
        }
    )
    entries.extend(
        {"type": "page", "kind": "page", "title": title, "summary": summary, "url": url}
        for title, summary, url in page_entries
    )
    payload = {
        "schemaVersion": 1,
        "declarationEntryCount": len(declarations),
        "pageEntryCount": len(page_entries),
        "entryCount": len(entries),
        "entries": entries,
    }
    (output / "search-index.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return payload


def validate_curated_declarations(
    declaration_map: dict[str, dict[str, object]]
) -> None:
    missing: list[str] = []
    for chapter in CHAPTERS:
        for item in chapter["results"]:
            if item["declaration"] not in declaration_map:
                missing.append(str(item["declaration"]))
            if item["local_status"] not in STATUS_ORDER:
                raise SystemExit(f"Unknown local status: {item['local_status']}")
            if item["route_status"] not in STATUS_ORDER:
                raise SystemExit(f"Unknown route status: {item['route_status']}")
            for root in item["route_closures"]:
                if root not in declaration_map:
                    missing.append(str(root))
    for item in IMPLEMENTATION_MAP:
        if item["declaration"] not in declaration_map:
            missing.append(str(item["declaration"]))
    if missing:
        raise SystemExit(
            "Curated website content names declarations absent from inventory:\n  "
            + "\n  ".join(sorted(set(missing)))
        )


def enrich_inventory(
    inventory: dict[str, object],
    context: dict[str, object],
) -> list[dict[str, object]]:
    enriched: list[dict[str, object]] = []
    # Eligibility is module-wide in this inventory snapshot. Do not retain
    # this cache across builds: a later dirty checkout must be checked anew.
    source_links: dict[str, str | None] = {}
    for raw in inventory["declarations"]:
        declaration = dict(raw)
        source = str(declaration["source"])
        if source not in source_links:
            source_links[source] = external_source_url(source, 1, context)
        link = source_links[source]
        declaration["sourceUrl"] = (
            f"{link.partition('#')[0]}#L{int(declaration['line'])}" if link else None
        )
        enriched.append(declaration)
    inventory["declarations"] = enriched
    return enriched


def build(args: argparse.Namespace) -> None:
    inventory = load_json(args.inventory)
    coverage = load_json(args.coverage)
    if inventory["publicDeclarationCount"] != coverage["publicDeclarationCount"]:
        raise SystemExit("Inventory and coverage declaration counts differ.")
    context = git_context()
    gate = load_gate_report(args.lean_gate_report, context)
    declarations = enrich_inventory(inventory, context)
    declaration_map = {str(item["fullName"]): item for item in declarations}
    validate_curated_declarations(declaration_map)
    curriculum_catalog = load_json(WEBSITE_ROOT / "curriculum-parts.json")
    curriculum_parts = validate_curriculum_catalog(
        curriculum_catalog,
        load_json(WEBSITE_ROOT / "research" / "sources.json"),
        load_json(ROOT / "research-wiki" / "openai-math-2026-intake.json"),
    )
    robin_paper_map = load_robin_paper_map(declaration_map)
    replay_report = load_json(
        ROOT / "reports" / "public-case-replay" / "latest.json"
    )
    if replay_report.get("cold_start_claim") is not False:
        raise SystemExit("Public-case replay must not be labeled as cold-start search.")
    example_cases = load_example_cases(declaration_map, replay_report)
    global EXAMPLE_CASE_NAV
    EXAMPLE_CASE_NAV = [
        (str(case["shortTitle"]), str(case["slug"])) for case in example_cases
    ]
    lean_graph_payload = build_lean_graph_payload(
        ROOT, declarations, CHAPTERS, example_cases
    )

    output: Path = args.output
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(WEBSITE_ROOT / "static", output / "static")
    shutil.copytree(WEBSITE_ROOT / "diagrams", output / "diagrams")
    for license_file in ("LICENSE", "LICENSE-MIT", "LICENSE_SCOPE.md", "NOTICE", "NOTICE.md"):
        shutil.copy2(ROOT / license_file, output / license_file)
    shutil.copy2(ROOT / "CONTRIBUTING.md", output / "CONTRIBUTING.md")
    sources = output / "sources"
    sources.mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        ROOT / "paper-notes" / "GHL2025" / "source-excerpts.tex",
        sources / "ghl2025-robin-excerpts.tex",
    )
    data = output / "data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "lean-graph.json").write_text(
        json.dumps(lean_graph_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (data / "public-case-replay.json").write_text(
        json.dumps(replay_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (data / "curriculum-parts.json").write_text(
        json.dumps(curriculum_catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if (WEBSITE_ROOT / "community").exists():
        shutil.copytree(WEBSITE_ROOT / "community", output / "community")

    write_page(output, "", render_home(inventory, coverage, gate, context))
    write_page(output, "math-2-0", render_math_2_0(coverage, gate, context))
    write_page(
        output,
        "state-preparation",
        render_state_preparation(coverage, gate, context),
    )
    write_page(
        output, "example-cases",
        render_example_case_index(example_cases, coverage, gate, context),
    )
    for case in example_cases:
        write_page(
            output, f"example-cases/{case['slug']}",
            render_example_case(case, declaration_map, coverage, gate, context),
        )
    write_page(
        output,
        "block-encoding",
        render_block_encoding(coverage, gate, context),
    )
    write_page(
        output,
        "implementation-map",
        render_implementation_map(declaration_map, coverage, gate, context),
    )
    write_page(
        output,
        "case-studies/robin",
        render_robin_paper_map(
            robin_paper_map, declaration_map, coverage, gate, context
        ),
    )
    write_page(output, "learning", render_learning(coverage, gate, context))
    for part in curriculum_parts:
        if part["id"] in {
            "part-iii-quantum-information",
            "part-iv-quantum-scientific-computing",
        }:
            write_page(
                output,
                str(part["route"]).rstrip("/"),
                render_curriculum_part(part, coverage, gate, context),
            )
    for chapter in CHAPTERS:
        write_page(
            output,
            f"chapters/{chapter['slug']}",
            render_chapter(chapter, declaration_map, coverage, gate, context),
        )
    write_page(output, "library", render_library(inventory, coverage, gate, context))
    write_page(
        output, "lean-graph",
        render_lean_graph(lean_graph_payload, coverage, gate, context),
    )
    by_source: dict[str, list[dict[str, object]]] = {}
    for declaration in declarations:
        by_source.setdefault(str(declaration["source"]), []).append(declaration)
    for source, source_declarations in sorted(by_source.items()):
        write_page(
            output,
            f"library/modules/{module_slug(source)}",
            render_module_page(
                source, source_declarations, coverage, gate, context
            ),
        )
    write_page(output, "roadmap", render_roadmap(inventory, coverage, gate, context))
    write_page(output, "workflow", render_workflow(coverage, gate, context))
    write_page(output, "ecosystem", render_ecosystem(coverage, gate, context))
    write_page(output, "community", render_community(coverage, gate, context))
    write_page(output, "contributors", render_contributors(coverage, gate, context))
    write_page(output, "organizers", render_organizers(coverage, gate, context))
    write_page(
        output,
        "ide",
        render_ide(declaration_map, coverage, gate, context),
    )
    (output / "ide-data.json").write_text(
        json.dumps(
            {"schemaVersion": 1, "items": workspace_items(declaration_map)},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_page(output, "attribution", render_attribution(coverage, gate, context))
    write_page(
        output,
        "blueprint",
        render_blueprint_entry(coverage, gate, context),
    )
    write_page(
        output, "task-builder",
        render_task_builder(coverage, gate, context),
    )
    (output / "data" / "example-cases.json").write_text(
        json.dumps(
            {"schemaVersion": 2, "scoreOrder": [
                "gate count", "parallel depth", "auxiliary qubits", "oracle calls"
            ], "cases": [
                {key: value for key, value in case.items() if key != "executionEvidence"}
                for case in example_cases
            ]},
            ensure_ascii=False, indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    search = build_search_index(output, declarations, example_cases)
    inventory_path = output / "library" / "declarations.json"
    inventory_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    status_counts = Counter(declaration_status(item) for item in declarations)
    route_counts = Counter(str(item["routeStatus"]) for item in declarations)
    source_link_count = sum(bool(item.get("sourceUrl")) for item in declarations)
    metadata = {
        "schemaVersion": 1,
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "commit": context["commit"],
        "shortCommit": context["shortCommit"],
        "branch": context["branch"],
        "publishedRef": context["publishedRef"],
        "declarationCount": len(declarations),
        "chapterCount": len(CHAPTERS),
        "curriculumPartCount": len(curriculum_parts),
        "exampleCaseCount": len(example_cases),
        "diagramCount": len(list((WEBSITE_ROOT / "diagrams").glob("*.mmd"))),
        "leanGraphModuleCount": lean_graph_payload["stats"]["moduleCount"],
        "leanGraphDeclarationCount": lean_graph_payload["stats"]["declarationCount"],
        "leanGraphImportEdgeCount": lean_graph_payload["stats"]["importEdgeCount"],
        "modulePageCount": len(by_source),
        "sourceLinkCount": source_link_count,
        "localStatusCounts": dict(sorted(status_counts.items())),
        "routeStatusCounts": dict(sorted(route_counts.items())),
        "searchEntryCount": search["entryCount"],
        "leanGate": gate,
        "publicCaseReplay": {
            "passed": replay_report["passed"],
            "role": "executable diagnostics only; not a Lean certification gate",
            "scope": replay_report["replay_scope"],
            "coldStartClaim": replay_report["cold_start_claim"],
            "sourceDigest": replay_report["source_digest"],
        },
    }
    (output / "site-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output / "build-report.json").write_text(
        json.dumps(
            {
                **metadata,
                "coverage": coverage,
                "sourceLinkPolicy": (
                    "External source links use the detected GitHub repository and "
                    "current commit SHA only when that commit is present on origin "
                    "and the source file is clean and exists in the commit."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"built {output}: {len(declarations)} declarations, "
        f"{len(CHAPTERS)} chapters, {len(by_source)} module pages, "
        f"{source_link_count} commit-pinned source links"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "web" / "library" / "declarations.json",
    )
    parser.add_argument(
        "--coverage",
        type=Path,
        default=ROOT / "docs" / "blueprint-coverage.json",
    )
    parser.add_argument(
        "--lean-gate-report",
        type=Path,
        default=ROOT / "_out" / "lean-gate.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "_out" / "site",
    )
    build(parser.parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
