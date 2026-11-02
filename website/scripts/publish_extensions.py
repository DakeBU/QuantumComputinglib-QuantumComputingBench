#!/usr/bin/env python3
"""Publish the Papers hub and additional state-preparation cases.

The base site builder remains the single renderer for normal case pages.  This
post-build extension deliberately reuses that renderer rather than maintaining
a second state-preparation template.  It also moves the Robin paper reproduction
under a first-class Papers navigation group while retaining the historical URL
as a hidden compatibility route.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path, PureWindowsPath

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from website import case_assets  # noqa: E402
from website.scripts import build_site  # noqa: E402
from website.scripts import enrich_casebook as casebook  # noqa: E402
from website.scripts import polish_casebook  # noqa: E402

EXTENSION_PATH = ROOT / "website" / "state-prep-cases.json"
HERMITE_PATH = ROOT / "website" / "hermite-case.json"
PAPERS_PATH = ROOT / "website" / "papers.json"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_extension_payload() -> dict[str, object]:
    """Both committed catalogs are mandatory, including their case assets."""
    payload = load_json(EXTENSION_PATH)
    hermite = load_json(HERMITE_PATH)
    payload["cases"] = list(payload["cases"]) + list(hermite["cases"])
    for key in ("teaching", "circuits"):
        overlap = set(payload[key]) & set(hermite[key])
        if overlap:
            raise RuntimeError(f"duplicate {key} records: {sorted(overlap)}")
        payload[key] = {**payload[key], **hermite[key]}
    return payload


def publish_case_assets(root: Path, case: dict[str, object]) -> str:
    """Copy source packets and figures with repository-relative provenance."""
    items = []
    slug = str(case["slug"])
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise RuntimeError("invalid case asset slug")
    for asset in case.get("supplementaryAssets", []):
        name = str(asset["path"])
        relative = Path(name)
        source = ROOT / relative
        if (relative.is_absolute() or PureWindowsPath(name).is_absolute()
                or "\\" in name or not source.resolve().is_relative_to(ROOT.resolve())):
            raise RuntimeError(f"case asset is outside the repository: {slug}")
        if not source.is_file() or source.stat().st_size == 0:
            raise RuntimeError(f"required case asset missing: {slug}: {relative.as_posix()}")
        destination = root / "downloads" / slug / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        url = "../../" + destination.relative_to(root).as_posix()
        label = html.escape(str(asset["label"]))
        if asset.get("kind") == "figure":
            items.append(f'<figure><img src="{url}" alt="{label}" style="width:100%;height:auto"><figcaption>{label}</figcaption></figure>')
        else:
            items.append(f'<p><a href="{url}" download>{label}</a></p>')
        if asset.get("copy"):
            items.append(build_site.render_copyable_source(
                str(asset["label"]), source.read_text(encoding="utf-8"),
                str(asset.get("language", relative.suffix.lstrip("."))),
            ))
    if not items:
        return ""
    return '<section class="content-section" id="complete-source-packet"><h2>Diagrams and complete source packet</h2>' + "".join(items) + '</section>'


def declarations_from_site(root: Path) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    inventory = load_json(root / "library" / "declarations.json")
    declarations = [dict(item) for item in inventory["declarations"]]
    return declarations, {str(item["fullName"]): item for item in declarations}


def validate_extension(
    payload: dict[str, object], declarations: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    if payload.get("schemaVersion") != 1:
        raise RuntimeError("state-prep extension schema changed")
    cases = [dict(case) for case in payload.get("cases", [])]
    teaching = dict(payload.get("teaching", {}))
    circuits = dict(payload.get("circuits", {}))
    if len(cases) < 4:
        raise RuntimeError("representative state-preparation extension lost cases")
    seen: set[str] = set()
    for case in cases:
        slug = str(case["slug"])
        if slug in seen:
            raise RuntimeError(f"duplicate state-preparation extension slug: {slug}")
        seen.add(slug)
        if case.get("kind") != "statePreparation" or case.get("status") != "certified":
            raise RuntimeError(f"extension case must be certified state preparation: {slug}")
        roots = list(case.get("leanAnchors", []))
        if not roots:
            raise RuntimeError(f"extension case has no Lean roots: {slug}")
        for root_name in roots:
            if root_name not in declarations:
                raise RuntimeError(f"unknown extension Lean root: {slug}: {root_name}")
        stages = list(dict(case["evolution"])["stages"])
        if not stages:
            raise RuntimeError(f"extension case has no evolution stages: {slug}")
        for stage in stages:
            anchor = str(stage["leanAnchor"])
            if anchor not in roots:
                raise RuntimeError(f"stage root not listed by case: {slug}: {anchor}")
            score = stage.get("score")
            if not isinstance(score, list) or len(score) != 4:
                raise RuntimeError(f"extension stage lost four-coordinate score: {slug}")
            if str(stage.get("status", "")).startswith("Strictly better") and "betterThan" not in anchor:
                raise RuntimeError(f"strict state-preparation claim lacks betterThan root: {slug}")
            if str(stage["name"]) not in dict(circuits.get(slug, {})):
                raise RuntimeError(f"extension case lacks quantikz: {slug}: {stage['name']}")
        qiskit = ROOT / str(dict(case["qiskit"])["path"])
        if not qiskit.is_file():
            raise RuntimeError(f"extension case lacks Qiskit artifact: {slug}: {qiskit}")
        record = dict(teaching.get(slug, {}))
        for key in ("readerGoal", "whyThisCase", "algorithmContext", "circuitReading", "theorems"):
            if not record.get(key):
                raise RuntimeError(f"extension teaching record lacks {key}: {slug}")
        for theorem in record["theorems"]:
            for root_name in theorem.get("leanRoots", []):
                if root_name not in declarations:
                    raise RuntimeError(f"unknown tutorial theorem root: {slug}: {root_name}")
        for root_name in dict(record.get("improvement") or {}).get("leanRoots", []):
            if root_name not in declarations:
                raise RuntimeError(f"unknown tutorial improvement root: {slug}: {root_name}")
    return cases


def register_circuits(payload: dict[str, object]) -> None:
    for slug, stages in dict(payload["circuits"]).items():
        case_assets.STAGE_CIRCUITS[str(slug)] = {
            str(name): str(tex) for name, tex in dict(stages).items()
        }


def render_extra_cases(
    root: Path,
    extra_cases: list[dict[str, object]],
    teaching: dict[str, object],
    declarations: dict[str, dict[str, object]],
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> list[dict[str, object]]:
    base_data = load_json(root / "data" / "example-cases.json")
    base_cases = [dict(case) for case in base_data["cases"]]
    combined = base_cases + extra_cases
    build_site.EXAMPLE_CASE_NAV = [
        (str(case["shortTitle"]), str(case["slug"])) for case in combined
    ]
    build_site.write_page(
        root,
        "example-cases",
        build_site.render_example_case_index(combined, coverage, gate, context),
    )
    for case in extra_cases:
        slug = str(case["slug"])
        build_site.write_page(
            root,
            f"example-cases/{slug}",
            build_site.render_example_case(case, declarations, coverage, gate, context),
        )
        path = root / "example-cases" / slug / "index.html"
        text = path.read_text(encoding="utf-8")
        text = casebook.ensure_css(text, "../../static/casebook.css")
        text = casebook.inject_after_hero(
            text,
            casebook.render_case_tutorial(slug, dict(teaching[slug]), declarations),
        )
        assets = publish_case_assets(root, case)
        text = text.replace('<section class="content-section case-problem"', assets + '<section class="content-section case-problem"', 1)
        path.write_text(text, encoding="utf-8")
    polish_casebook.polish_example_pages(root)
    (root / "data" / "example-cases.json").write_text(
        json.dumps(
            {
                "schemaVersion": 2,
                "scoreOrder": ["gate count", "parallel depth", "auxiliary qubits", "oracle calls"],
                "cases": combined,
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    return combined


def inject_state_preparation_case_map(root: Path, cases: list[dict[str, object]]) -> None:
    path = root / "state-preparation" / "index.html"
    text = path.read_text(encoding="utf-8")
    if 'id="representative-state-preparation-cases"' in text:
        return
    state_cases = [case for case in cases if case.get("kind") == "statePreparation"]
    cards = "".join(
        f"""<article class="case-card">
  <p class="eyebrow">{html.escape(str(case['semanticTier']))}</p>
  <h3><a href="../example-cases/{html.escape(str(case['slug']))}/index.html">{html.escape(str(case['title']))}</a></h3>
  <p>{html.escape(str(case['summary']))}</p>
  <p>{build_site.badge('Lean certified')}</p>
</article>"""
        for case in state_cases
    )
    section = f"""<section class="content-section" id="representative-state-preparation-cases">
  <div class="section-heading">
    <p class="eyebrow">Representative certified cases</p>
    <h2>From basis states to entanglement, dense loading, structured distributions, and sparsity</h2>
    <p>Every card uses the same case renderer and certificate discipline as the operator/block-encoding examples. Paper-derived finite benchmarks state their scope explicitly rather than inheriting the paper-wide asymptotic claim.</p>
  </div>
  <div class="case-grid">{cards}</div>
  <p><a class="button secondary" href="../papers/index.html#reproduction-queue">See the state-preparation paper reproduction queue</a></p>
</section>"""
    marker = '<section class="content-section" id="state-reading">'
    if marker not in text:
        raise RuntimeError("state-preparation landing page lost state-reading marker")
    path.write_text(text.replace(marker, section + "\n" + marker, 1), encoding="utf-8")


def status_label(status: str) -> str:
    return {
        "reproduced-fixed-benchmark": "Reproduced fixed benchmark",
        "finite-benchmark-formalized": "Finite benchmark formalized",
        "structured-benchmark-formalized": "Structured benchmark formalized",
        "finite-sparse-benchmark-formalized": "Finite sparse benchmark formalized",
        "resource-lemma-formalized": "Resource lemma formalized",
        "queued": "Queued",
    }.get(status, status)


def render_papers_index(
    papers: dict[str, object], coverage: dict[str, object], gate: dict[str, object], context: dict[str, object]
) -> str:
    featured = "".join(
        f"""<article class="case-card">
  <p class="eyebrow">{html.escape(status_label(str(item['status'])))}</p>
  <h2><a href="{html.escape(str(item['slug']))}/index.html">{html.escape(str(item['title']))}</a></h2>
  <p>{html.escape(str(item['authors']))} · {int(item['year'])}</p>
  <p>{html.escape(str(item['summary']))}</p>
  <div class="link-row"><a class="button" href="{html.escape(str(item['slug']))}/index.html">Read reproduction</a><a class="text-link" href="{html.escape(str(item['url']))}">Source paper ↗</a></div>
</article>"""
        for item in papers.get("featured", [])
    )
    queue_rows = "".join(
        f"""<article class="result">
  <div class="result-header"><div><p class="eyebrow">{html.escape(status_label(str(item['status'])))}</p><h3>{html.escape(str(item['title']))}</h3><p>{html.escape(str(item['authors']))} · {int(item['year'])}</p></div></div>
  <p><strong>Formalized now.</strong> {html.escape(str(item['formalized']))}</p>
  <p><strong>Still required for paper reproduction.</strong> {html.escape(str(item['remaining']))}</p>
  <p><a href="{html.escape(str(item['url']))}">Open source paper ↗</a></p>
</article>"""
        for item in papers.get("queue", [])
    )
    body = f"""<section class="hero" id="papers">
  <p class="eyebrow">Source papers · theorem → proof → Lean scope</p>
  <h1>Papers</h1>
  <p class="lede">Paper reproductions are a first-class reading track, parallel to Chapters and Example Cases. A paper page starts from the source theorem and proof, states the exact formalization boundary, and only then shows the Lean evidence or ASPBE improvement.</p>
</section>
<section class="content-section" id="published-reproductions">
  <div class="section-heading"><p class="eyebrow">Published reproductions</p><h2>Read source-facing formalizations</h2><p>Robin/GHL is the first full paper-map surface. More papers move here only when their public source-to-Lean contract is ready.</p></div>
  <div class="case-grid">{featured}</div>
</section>
<section class="content-section" id="reproduction-queue">
  <div class="section-heading"><p class="eyebrow">Paper reproduction queue</p><h2>What has a finite theorem today, and what still needs the paper-wide proof</h2><p>A fixed benchmark, a resource-formula lemma, and a complete paper reproduction are different statuses. This queue makes that boundary public.</p></div>
  <div class="result-list">{queue_rows}</div>
</section>"""
    return build_site.page_template(
        title="Papers",
        route="papers/",
        current="papers/",
        body=body,
        coverage=coverage,
        gate=gate,
        context=context,
        toc=[("papers", "Papers"), ("published-reproductions", "Published reproductions"), ("reproduction-queue", "Reproduction queue")],
    )


def publish_papers(
    root: Path,
    coverage: dict[str, object],
    gate: dict[str, object],
    context: dict[str, object],
) -> dict[str, object]:
    papers = load_json(PAPERS_PATH)
    if papers.get("schemaVersion") != 1 or not papers.get("featured") or not papers.get("queue"):
        raise RuntimeError("Papers catalog lost featured reproduction or queue")
    source = root / "case-studies" / "robin" / "index.html"
    target = root / "papers" / "ghl2025-robin" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    build_site.write_page(root, "papers", render_papers_index(papers, coverage, gate, context))
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "papers.json").write_text(
        json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return papers


def relative_prefix(root: Path, page: Path) -> str:
    depth = len(page.parent.relative_to(root).parts)
    return "../" * depth if depth else "./"


def rewrite_navigation(root: Path) -> None:
    old_robin = re.compile(r'<a href="[^"]*case-studies/robin/index\.html"[^>]*>Robin paper map</a>')
    marker = '<strong class="nav-group-label">Example Cases</strong>'
    for path in root.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        text = old_robin.sub("", text)
        if '<strong class="nav-group-label">Papers</strong>' not in text and marker in text:
            prefix = relative_prefix(root, path)
            current = path.relative_to(root).as_posix()
            all_current = ' aria-current="page"' if current == "papers/index.html" else ""
            robin_current = ' aria-current="page"' if current == "papers/ghl2025-robin/index.html" else ""
            papers_nav = (
                '<strong class="nav-group-label">Papers</strong>'
                f'<a href="{prefix}papers/index.html"{all_current}>All papers</a>'
                '<div class="chapter-nav paper-nav">'
                f'<a href="{prefix}papers/ghl2025-robin/index.html"{robin_current}><span>01</span><span>GHL Robin PDE</span></a>'
                f'<a href="{prefix}papers/index.html#reproduction-queue"><span>→</span><span>Paper reproduction queue</span></a>'
                '</div>'
            )
            text = text.replace(marker, papers_nav + marker, 1)
        path.write_text(text, encoding="utf-8")


def rebuild_search_and_metadata(
    root: Path,
    declarations: list[dict[str, object]],
    cases: list[dict[str, object]],
) -> None:
    search = build_site.build_search_index(root, declarations, cases)
    search_path = root / "search-index.json"
    payload = load_json(search_path)
    for entry in payload["entries"]:
        if entry.get("title") == "Robin paper map":
            entry["title"] = "GHL Robin PDE paper reproduction"
            entry["summary"] = "GHL Robin source theorems, proof story, formalization scope, and ASPBE fixed-benchmark improvement"
            entry["url"] = "papers/ghl2025-robin/index.html"
    payload["entries"].extend([
        {"type": "page", "kind": "paper", "title": "Papers", "summary": "Source-facing paper reproductions and their exact Lean scope", "url": "papers/index.html"},
        {"type": "page", "kind": "paperQueue", "title": "Paper reproduction queue", "summary": "Finite benchmarks, resource lemmas, reproduced papers, and remaining proof obligations", "url": "papers/index.html#reproduction-queue"},
        {"type": "page", "kind": "licensing", "title": "Licenses and reuse", "summary": "Project MIT scope, third-party Apache 2.0 text, notices and attribution", "url": "licensing/index.html"},
    ])
    payload["entryCount"] = len(payload["entries"])
    payload["pageEntryCount"] = int(payload["pageEntryCount"]) + 3
    search_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("site-metadata.json", "build-report.json"):
        path = root / name
        data = load_json(path)
        data["exampleCaseCount"] = len(cases)
        data["searchEntryCount"] = payload["entryCount"]
        data["paperTrack"] = {"route": "papers/", "featuredCount": 1, "queueCount": len(load_json(PAPERS_PATH)["queue"])}
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_published(root: Path, extra_cases: list[dict[str, object]]) -> None:
    papers = (root / "papers" / "index.html").read_text(encoding="utf-8")
    robin = (root / "papers" / "ghl2025-robin" / "index.html").read_text(encoding="utf-8")
    if "Paper reproduction queue" not in papers or "GHL Theorem 3" not in robin or "GHL Theorem 4" not in robin:
        raise RuntimeError("Papers track lost queue or Robin source theorems")
    sample = (root / "index.html").read_text(encoding="utf-8")
    if '>Robin paper map</a>' in sample:
        raise RuntimeError("Robin still appears as a standalone Explore navigation item")
    if '<strong class="nav-group-label">Papers</strong>' not in sample:
        raise RuntimeError("Papers is not a peer navigation group")
    state_landing = (root / "state-preparation" / "index.html").read_text(encoding="utf-8")
    if 'id="representative-state-preparation-cases"' not in state_landing:
        raise RuntimeError("state-preparation landing page lost representative cases")
    for case in extra_cases:
        page = root / "example-cases" / str(case["slug"]) / "index.html"
        text = page.read_text(encoding="utf-8")
        for token in ('id="case-tutorial"', "Proof story", "Show the Lean proof checkpoints"):
            if token not in text:
                raise RuntimeError(f"state-preparation case lost theorem-first treatment: {case['slug']}: {token}")


def publish(root: Path) -> None:
    payload = load_extension_payload()
    declarations_list, declarations = declarations_from_site(root)
    extra_cases = validate_extension(payload, declarations)
    register_circuits(payload)
    report = load_json(root / "build-report.json")
    coverage = dict(report["coverage"])
    gate = dict(report["leanGate"])
    context = build_site.git_context()
    combined = render_extra_cases(
        root, extra_cases, dict(payload["teaching"]), declarations,
        coverage, gate, context,
    )
    inject_state_preparation_case_map(root, combined)
    publish_papers(root, coverage, gate, context)
    from website.scripts import publish_licensing
    publish_licensing.publish(root, coverage, gate, context)
    rebuild_search_and_metadata(root, declarations_list, combined)
    rewrite_navigation(root)
    validate_published(root, extra_cases)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    publish(args.root)
