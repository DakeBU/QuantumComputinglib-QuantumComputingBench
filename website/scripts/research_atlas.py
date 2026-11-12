#!/usr/bin/env python3
"""One source for mathematical mechanism browsing, research routes and agent retrieval.

The existing Lean inventory/graph remains authoritative. This module publishes
curated views over it; no conceptual incidence is inserted into the import graph,
and no route is promoted because a prerequisite happens to compile.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "website/research"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FILES = {"sources": "sources.json", "atlas": "atlas.json", "wiki": "state-preparation-wiki.json"}
VIEWS = (("Mathematical methods", "mathematical-methods/"),
         ("Functor Hypergraph", "functor-hypergraph/"),
         ("StatePreparationWiki", "state-preparation-wiki/"),
         ("Current Progress", "progress/"))
ID = re.compile(r"[a-z][a-z0-9-]*:[a-z0-9][a-z0-9-]*$|[a-z][a-z0-9-]*$")
SOURCE_STATES = {"primary-metadata-checked", "primary-text-checked", "primary-source-unavailable"}
TECHNICAL_STATES = {"paper-cited", "classic-unformalized", "contract-only", "obligation", "formalized"}
# Exact source/field pairs, not a general host-path or task-name rewrite rule.
_PUBLIC_SOURCE_AUTHOR_DISPLAY = {
    "aspbe-local-exact-primitives-controlled-rotations-finite-cubic": (
        "Retrospective natural source /root; metadata /root/primitive_compiler_metadata_c31; historical formalizer UNKNOWN",
        "Retrospective natural source agent-task:root; metadata agent-task:root/primitive_compiler_metadata_c31; historical formalizer UNKNOWN",
    ),
    "aspbe-local-stored-rectangular-elimination-v1": (
        "Retrospective implementation-informed source /root/stored_givens_source_author_c38; historical formalizer UNKNOWN",
        "Retrospective implementation-informed source agent-task:root/stored_givens_source_author_c38; historical formalizer UNKNOWN",
    ),
    "aspbe-local-retrospective-sequential-primitive-assembly-c48": (
        "/root/sequential_assembly_c48_source_author; LOCAL retrospective mathematical contract",
        "agent-task:root/sequential_assembly_c48_source_author; LOCAL retrospective mathematical contract",
    ),
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_catalog(directory: Path = DATA) -> dict[str, Any]:
    return {name: read_json(directory / filename) for name, filename in FILES.items()}


def public_catalog(catalog: dict[str, Any]) -> dict[str, Any]:
    """Derive lossless author-identity display metadata from validated originals.

    Only three exact source-ID/author-field pairs are encoded. Unrecognized
    authors, actual paths, nested fields and all scientific metadata are left
    untouched for the ordinary publication checks, including the path scanner.
    Canonical source bytes, source digests and review bindings never change.
    """
    validate_catalog(catalog)
    if "public_projection" in catalog["sources"]:
        raise ValueError("canonical sources must not contain derived public projection metadata")
    projected = deepcopy(catalog)
    for source in projected["sources"]["sources"]:
        pair = _PUBLIC_SOURCE_AUTHOR_DISPLAY.get(source["id"])
        if pair is not None and source.get("authors") == pair[0]:
            source["authors"] = pair[1]
    projected["sources"]["public_projection"] = {
        "schema_version": "research.sources_author_identity_display.v1",
        "canonical_source": "website/research/sources.json",
        "source_digest_binds": "unmodified_canonical_catalog_files",
        "author_identity_encoding": (
            "Only exact allowlisted source-ID/author-field pairs are encoded. "
            "Decode each agent-task:root[/task] token by replacing agent-task: "
            "with a leading slash; other metadata is unchanged."
        ),
        "review_boundary": "Display-only derived metadata; no new source, mathematical or formalization review.",
    }
    return projected


def require_fields(item: dict[str, Any], fields: tuple[str, ...], kind: str) -> None:
    missing = [key for key in fields if key not in item or item[key] in (None, "")]
    if missing:
        raise ValueError(f"{kind} {item.get('id', '?')}: missing {', '.join(missing)}")


def unique(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in items:
        identifier = item.get("id", "")
        if not isinstance(identifier, str) or not ID.fullmatch(identifier):
            raise ValueError(f"invalid {label} id: {identifier!r}")
        if identifier in out:
            raise ValueError(f"duplicate {label} id: {identifier}")
        out[identifier] = item
    return out


def validate_catalog(catalog: dict[str, Any], declarations: dict[str, Any] | None = None) -> None:
    for name in FILES:
        if catalog[name].get("schema_version") != 1:
            raise ValueError(f"unsupported {name} schema")
    atlas, wiki = catalog["atlas"], catalog["wiki"]
    sources = unique(catalog["sources"]["sources"], "source")
    domains = unique(atlas["domains"], "domain")
    families = unique(atlas["families"], "family")
    nodes = {**domains, **families}
    if len(nodes) != len(domains) + len(families):
        raise ValueError("domain/family identity collision")
    edges = unique(atlas["hyperedges"], "hyperedge")
    contributions = unique(atlas["contributions"], "contribution")
    routes = unique(wiki["routes"], "route")
    cards = []
    for item in sources.values():
        require_fields(item, ("title", "url", "status", "anchor", "scope", "formal_status"), "source")
        if item["status"] not in SOURCE_STATES or not item["url"].startswith("https://"):
            raise ValueError(f"invalid source verification/url: {item['id']}")
    for item in families.values():
        require_fields(item, ("label", "question", "formula", "mechanism", "assumptions", "proof_steps", "boundary"), "family")
        if not item["assumptions"] or not item["proof_steps"]:
            raise ValueError(f"empty mathematical lesson: {item['id']}")
        if any(domain not in domains for domain in item["domains"]):
            raise ValueError(f"unknown family domain: {item['id']}")
        if "technical_card" in item:
            card = item["technical_card"]
            if not isinstance(card, dict):
                raise ValueError(f"technical card must be an object: {item['id']}")
            require_fields(card, ("id", "source_ids", "statement", "lean_decl", "lean_status", "used_by", "dependencies", "next_action", "tags", "failure_modes"), "technical card")
            for field in ("statement", "lean_status", "next_action"):
                if not isinstance(card[field], str) or not card[field].strip():
                    raise ValueError(f"invalid technical card {field}: {card['id']}")
            for field in ("source_ids", "lean_decl", "used_by", "dependencies", "tags", "failure_modes"):
                values = card[field]
                if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values):
                    raise ValueError(f"invalid technical card {field}: {card['id']}")
                if len(values) != len(set(values)):
                    raise ValueError(f"duplicate technical card {field}: {card['id']}")
                if field in {"source_ids", "used_by", "tags", "failure_modes"} and not values:
                    raise ValueError(f"empty technical card {field}: {card['id']}")
            if card["lean_status"] not in TECHNICAL_STATES:
                raise ValueError(f"invalid technical card lean_status: {card['id']}")
            if card["lean_status"] != "formalized" and card["lean_decl"]:
                raise ValueError(f"uncertified technical card cannot claim a local certificate: {card['id']}")
            if card["lean_status"] == "formalized" and not card["lean_decl"]:
                raise ValueError(f"formalized technical card requires a local declaration: {card['id']}")
            for field, targets in (("source_ids", sources), ("used_by", routes), ("dependencies", families)):
                if any(value not in targets for value in card[field]):
                    raise ValueError(f"unknown technical card {field} reference: {card['id']}")
            for ref in card["lean_decl"]:
                if declarations is not None:
                    if ref not in declarations:
                        raise ValueError(f"unknown generated Lean declaration in technical card: {ref}")
                    if declarations[ref].get("openProof") or declarations[ref].get("experimental"):
                        raise ValueError(f"non-certified technical card declaration: {ref}")
            cards.append(card)
    unique(cards, "technical card")
    for item in edges.values():
        require_fields(item, ("label", "tails", "heads", "formula", "mechanism", "hypothesis_map", "conclusion_map", "failure_boundary", "status", "review"), "hyperedge")
        if not item["tails"] or not item["heads"]:
            raise ValueError(f"hyperedge lost its AND input/output set: {item['id']}")
        if len(set(item["tails"])) != len(item["tails"]):
            raise ValueError(f"duplicate hyperedge tail: {item['id']}")
        if any(node not in nodes for node in item["tails"] + item["heads"]):
            raise ValueError(f"unknown hyperedge endpoint: {item['id']}")
        if item["status"] not in {"proposal", "curated-transport"}:
            raise ValueError("conceptual transport is not a certified Lean functor")
    for item in contributions.values():
        require_fields(item, ("baseline", "head", "classes", "before", "after", "invariant", "novelty_boundary", "review"), "contribution")
        if any(kind not in {"add-node", "shortcut", "reorganisation", "bridge"} for kind in item["classes"]):
            raise ValueError("unrecognized contribution class")
        if not all(re.fullmatch(r"[0-9a-f]{40}", item[key]) for key in ("baseline", "head")):
            raise ValueError("contribution endpoints must be pinned commits")
    for item in routes.values():
        require_fields(item, ("title", "setting_id", "formula", "goal", "input_model", "assumptions", "target_bound", "known_boundary", "steps", "next", "lower_bound"), "route")
        if "reading_layers" in item:
            if not isinstance(item["reading_layers"], list) or not item["reading_layers"]:
                raise ValueError("reading layers must be a nonempty list")
            for layer in item["reading_layers"]:
                require_fields(layer, ("title", "summary", "items"), "reading layer")
                if any(not isinstance(layer[key], str) or not layer[key].strip() for key in ("title", "summary")):
                    raise ValueError("reading layer headings must be nonempty text")
                if not isinstance(layer["items"], list) or not layer["items"] or any(not isinstance(text, str) or not text.strip() for text in layer["items"]):
                    raise ValueError("reading layer items must be nonempty text")
        if item["status"] != "research-target":
            raise ValueError("research agenda status cannot imply a proved result")
        if item["lower_bound"]["comparison_key"] != item["setting_id"]:
            raise ValueError(f"lower-bound comparison changes model: {item['id']}")
        if not item["steps"]:
            raise ValueError("research route needs bounded acceptance steps")
        unique(item["steps"], "route step")
        for step in item["steps"]:
            require_fields(step, ("target", "acceptance"), "step")
        if any(family not in families for family in item["families"]):
            raise ValueError(f"unknown route family: {item['id']}")
    for item in list(families.values()) + list(edges.values()) + list(contributions.values()) + list(routes.values()):
        if any(source not in sources for source in item.get("source_ids", [])):
            raise ValueError(f"unknown source reference: {item['id']}")
        for ref in item.get("lean_refs", []):
            if declarations is not None:
                if ref not in declarations:
                    raise ValueError(f"unknown generated Lean declaration: {ref}")
                if declarations[ref].get("openProof") or declarations[ref].get("experimental"):
                    raise ValueError(f"non-certified substrate needs explicit frontier treatment: {ref}")


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def slug(identifier: str) -> str:
    return identifier.split(":", 1)[-1]


def tex(value: str) -> str:
    # Historic input used a Unicode dagger; retain a valid TeX superscript.
    return value.replace(r"\u2020", r"\dagger").replace("†", r"\dagger")


def math(value: str) -> str:
    from website.scripts.build_site import render_math_tex
    return render_math_tex(tex(value))


def paragraphs(items: list[str], ordered: bool = False) -> str:
    tag = "ol" if ordered else "ul"
    return f'<{tag} class="ra-list">' + "".join(f"<li>{esc(item)}</li>" for item in items) + f"</{tag}>"


def section(title: str, body: str, identifier: str = "") -> str:
    anchor = f' id="{esc(identifier)}"' if identifier else ""
    return f'<section class="ra-section"{anchor}><h2>{esc(title)}</h2>{body}</section>'


def source_list(ids: list[str], sources: dict[str, Any]) -> str:
    if not ids:
        return '<p class="ra-boundary">No external source is attached to this local mechanism note. It remains authored exposition, not a literature-priority claim.</p>'
    return '<div class="ra-sources">' + "".join(
        f'<article><a href="{esc(sources[i]["url"])}">{esc(sources[i]["title"])}</a>'
        f'<p><span class="ra-tag">{esc(sources[i]["status"])}</span> {esc(sources[i]["anchor"])}</p>'
        f'<p>{esc(sources[i]["scope"])}</p></article>' for i in ids) + '</div>'


def node_url(identifier: str, prefix: str) -> str:
    if identifier.startswith("family:"):
        return prefix + "mathematical-methods/" + slug(identifier) + "/index.html"
    return prefix + "mathematical-methods/index.html#" + slug(identifier)


def family_links(ids: list[str], families: dict[str, Any], prefix: str) -> str:
    return '<div class="ra-tags">' + "".join(f'<a class="ra-tag" href="{node_url(i, prefix)}">{esc(families[i]["label"])}</a>' for i in ids) + '</div>'


def lean_links(refs: list[str], declarations: dict[str, Any], prefix: str, full_source: bool = False) -> str:
    if not refs:
        return '<p class="ra-boundary">No local transport theorem is bound to this record. Do not infer formal truth from its position in the atlas.</p>'
    from website.scripts import build_site as site
    content = '<p class="ra-boundary">Named Lean substrates below have their own exact signatures. They do not certify every sentence or proposed generalization on this page.</p>'
    modules: set[str] = set()
    for name in refs:
        item = declarations[name]
        content += f'<p><a href="{site.module_url(prefix, item)}"><code>{esc(name)}</code></a></p>'
        focus = quote("declaration:" + name, safe="")
        content += f'<p class="ra-boundary"><a href="{prefix}lean-graph/index.html?focus={focus}">Locate the same declaration in the Lean graph</a></p>'
        source = str(item["source"])
        if full_source and source not in modules:
            modules.add(source)
            path = ROOT / source
            if not path.resolve().is_relative_to(ROOT.resolve()) or not path.is_file():
                raise ValueError(f"invalid Lean source path: {source}")
            content += '<details class="ra-code"><summary>Exact owning Lean module: ' + esc(source) + '</summary>'
            content += '<p>Whole module, including imports and scoped assumptions. The declaration link above focuses the generated statement.</p>'
            content += '<pre><code class="language-lean">' + esc(path.read_text(encoding="utf-8")) + '</code></pre></details>'
    return content


def family_latex(item: dict[str, Any]) -> str:
    def prose(value: str) -> str:
        mapping = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
        return "".join(mapping.get(char, char) for char in value)
    lines = ["% Authored mechanism lesson; not a new theorem certificate.",
             r"\section*{" + prose(item["label"]) + "}", prose(item["question"]),
             r"\[", tex(item["formula"]), r"\]", prose(item["mechanism"]),
             r"\paragraph{Hypotheses and contracts.}", r"\begin{enumerate}"]
    lines += [r"\item " + prose(value) for value in item["assumptions"]]
    lines += [r"\end{enumerate}", r"\paragraph{Mathematical proof mechanism.}",
              "This is a reusable derivation guide; exact certified scope is given by the linked Lean signatures.", r"\begin{enumerate}"]
    lines += [r"\item " + prose(value) for value in item["proof_steps"]]
    lines += [r"\end{enumerate}", r"\paragraph{Boundary.} " + prose(item["boundary"])]
    return "\n".join(lines) + "\n"


def render_technical_card(card: dict[str, Any], families: dict[str, Any], routes: dict[str, Any], sources: dict[str, Any], declarations: dict[str, Any], prefix: str) -> str:
    boundary = ("Local declaration references certify only their exact checked statements, not the surrounding research route."
                if card["lean_status"] == "formalized" else
                "Planned / uncertified technical lemma. This card is a retrieval obligation, not a local Lean certificate or a completed source route.")
    body = '<p><code>' + esc(card["id"]) + '</code> <span class="ra-tag">' + esc(card["lean_status"]) + '</span></p>'
    body += '<p class="ra-warning">' + boundary + '</p><p>' + esc(card["statement"]) + '</p>'
    body += '<h3>Exact card declarations</h3>' + lean_links(card["lean_decl"], declarations, prefix)
    body += '<h3>Planned consumers (not verified reuse)</h3><ul>' + "".join(
        f'<li><a href="{prefix}state-preparation-wiki/{identifier}/index.html">{esc(routes[identifier]["title"])}</a></li>' for identifier in card["used_by"]) + '</ul>'
    body += '<h3>Required mechanisms</h3>' + (family_links(card["dependencies"], families, prefix) if card["dependencies"] else '<p>No additional family dependencies recorded.</p>')
    body += '<h3>Failure modes</h3>' + paragraphs(card["failure_modes"])
    body += '<p><strong>Next bounded action:</strong> ' + esc(card["next_action"]) + '</p>'
    body += '<div class="ra-tags">' + "".join('<span class="ra-tag">' + esc(tag) + '</span>' for tag in card["tags"]) + '</div>'
    body += '<h3>Card source ledger</h3>' + source_list(card["source_ids"], sources)
    return section("Reusable technical lemma card", body, "technical-card")


def context_packet(catalog: dict[str, Any], query: str = "", route_id: str | None = None, limit: int = 5) -> dict[str, Any]:
    validate_catalog(catalog)
    limit = max(1, min(limit, 6))
    families = catalog["atlas"]["families"]
    routes = catalog["wiki"]["routes"]
    requested = next((r for r in routes if r["id"] == route_id), None)
    if route_id and requested is None:
        raise ValueError(f"unknown route {route_id}")
    terms = re.findall(r"[\w-]+", query.lower())
    def score(item: dict[str, Any]) -> int:
        haystack = json.dumps(item, ensure_ascii=False).lower()
        return sum(haystack.count(term) for term in terms)
    if requested:
        by_id = {f["id"]: f for f in families}
        chosen = [by_id[identifier] for identifier in requested["families"]][:limit]
        selected_routes = [requested]
    else:
        chosen = sorted(families, key=lambda x: (-score(x), x["id"]))
        chosen = [f for f in chosen if not terms or score(f)][:limit]
        selected_routes = [r for r in sorted(routes, key=lambda x: (-score(x), x["priority"])) if not terms or score(r)][:2]
    ids = {f["id"] for f in chosen}
    direct_ids = set(requested["families"]) if requested else ids
    edges = [e for e in catalog["atlas"]["hyperedges"] if ids.intersection(e["tails"] + e["heads"])]
    edges.sort(key=lambda e: (-len(direct_ids.intersection(e["tails"] + e["heads"])), -score(e), e["id"]))
    edges = edges[:4]  # Bound the number of complete hyperedges, never their AND inputs.
    records = chosen + selected_routes + edges + [f["technical_card"] for f in chosen if "technical_card" in f]
    source_ids = {source for record in records for source in record.get("source_ids", [])}
    sources = [source for source in catalog["sources"]["sources"] if source["id"] in source_ids]
    return {"schema_version": 1, "query": query, "route_id": route_id,
            "truth_boundary": "Curated retrieval packet, not an execution result or Lean implication. Hyperedge tails are conjunctive. Check exact source, input/oracle/phase/norm/resource contracts before reuse.",
            "families": chosen, "routes": selected_routes, "hyperedges": edges, "sources": sources,
            "required_handoff": ["frozen target and access model", "exact reused declarations", "bounded mathematical delta", "assumption differences", "independent round-trip evidence", "graph contribution and residual boundary"]}


def progress_payload(catalog: dict[str, Any], declarations: dict[str, Any], commit: str) -> dict[str, Any]:
    from website.content import CHAPTERS, IMPLEMENTATION_MAP, ROADMAP
    chapters = []
    for chapter in CHAPTERS:
        results = []
        for result in chapter.get("results", []):
            name = result["declaration"]
            if name not in declarations:
                raise ValueError(f"chapter declaration is missing: {name}")
            results.append({key: result.get(key) for key in ("declaration", "title", "math", "local_status", "route_status", "missing", "dependencies", "route_closures")})
        chapters.append({"id": chapter["slug"], "title": chapter["title"], "track": chapter["track"], "summary": chapter["summary"], "results": results})
    return {"schema_version": 1, "commit": commit,
            "policy": "Projected from existing chapter/result and implementation metadata, not a newly scored source-coverage percentage. A compiled prerequisite does not close a route.",
            "chapters": chapters, "paper_frontier": read_json(ROOT / "website/papers.json"), "implementation_frontier": IMPLEMENTATION_MAP,
            "historical_roadmap": [{"title": title, "status": status} for title, status in ROADMAP],
            "research_routes": catalog["wiki"]["routes"]}


def git_text(*args: str) -> str | None:
    run = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    return run.stdout if run.returncode == 0 else None


def contribution_delta(item: dict[str, Any]) -> dict[str, Any]:
    def modules_at(commit: str) -> dict[str, str] | None:
        listing = git_text("ls-tree", "-r", "--name-only", commit, "QuantumBlockEncoding")
        if listing is None:
            return None
        return {path: "module:" + path.removesuffix(".lean").replace("/", ".")
                for path in listing.splitlines() if path.endswith(".lean")}
    before, after = modules_at(item["baseline"]), modules_at(item["head"])
    out = {"contribution_id": item["id"], "baseline": item["baseline"], "head": item["head"],
           "layer": "git-module-import-delta", "classification": "curated, not inferred",
           "classes": item["classes"], "boundary": item["novelty_boundary"]}
    if before is None or after is None:
        return {**out, "status": "history-unavailable", "added_modules": [], "removed_modules": [], "added_imports": [], "removed_imports": []}
    def edges(commit: str, modules: dict[str, str]) -> set[tuple[str, str]]:
        result: set[tuple[str, str]] = set()
        for path, node in modules.items():
            text = git_text("show", f"{commit}:{path}")
            if text is None:
                raise ValueError("commit object disappeared during graph delta")
            text = re.sub(r"/-.*?-/", "", text, flags=re.S)
            for module in re.findall(r"^\s*(?:(?:public|private|meta)\s+)*import\s+(QuantumBlockEncoding(?:\.[\w]+)+)", text, re.M):
                result.add(("module:" + module, node))
        return result
    old_edges, new_edges = edges(item["baseline"], before), edges(item["head"], after)
    return {**out, "status": "computed", "added_modules": sorted(set(after.values()) - set(before.values())),
            "removed_modules": sorted(set(before.values()) - set(after.values())),
            "added_imports": sorted(new_edges - old_edges), "removed_imports": sorted(old_edges - new_edges)}


def patch_navigation(root: Path) -> None:
    from website.scripts.sidebar_navigation import replace_navigation
    cases = read_json(root / "data/example-cases.json")["cases"]
    papers = read_json(root / "data/papers.json")
    for path in root.rglob("*.html"):
        if "blueprint" in path.relative_to(root).parts:
            continue
        text = path.read_text(encoding="utf-8")
        prefix = "../" * len(path.parent.relative_to(root).parts) or "./"
        current = path.relative_to(root).as_posix()
        text = replace_navigation(text, prefix, current, papers, cases)
        path.write_text(text, encoding="utf-8")


def publish(root: Path) -> dict[str, Any]:
    from website.scripts import build_site as site
    root = root.resolve()
    catalog = load_catalog()
    inventory = read_json(root / "library/declarations.json")
    declarations = {d["fullName"]: d for d in inventory["declarations"]}
    validate_catalog(catalog, declarations)
    report = read_json(root / "build-report.json")
    coverage, gate = report["coverage"], report["leanGate"]
    context = site.git_context()
    if not gate.get("passed") or gate.get("commit") != context["commit"]:
        raise ValueError("research publication requires the current passed Lean gate")
    graph_path = root / "data/lean-graph.json"
    graph_digest = hashlib.sha256(graph_path.read_bytes()).hexdigest()
    graph = read_json(graph_path)
    graph_ids = {node["id"] for node in graph["nodes"]}
    all_refs = {ref for name in ("families", "hyperedges", "contributions") for item in catalog["atlas"][name] for ref in item.get("lean_refs", [])}
    all_refs |= {ref for item in catalog["wiki"]["routes"] for ref in item.get("lean_refs", [])}
    all_refs |= {ref for item in catalog["atlas"]["families"] for ref in item.get("technical_card", {}).get("lean_decl", [])}
    for name in all_refs:
        if "declaration:" + name not in graph_ids:
            raise ValueError(f"shared declaration missing from Lean graph: {name}")
    atlas, wiki = catalog["atlas"], catalog["wiki"]
    families = {x["id"]: x for x in atlas["families"]}
    nodes = {x["id"]: x for x in atlas["domains"] + atlas["families"]}
    sources = {x["id"]: x for x in catalog["sources"]["sources"]}
    data_dir = root / "data/research"
    data_dir.mkdir(parents=True, exist_ok=True)
    displayed_catalog = public_catalog(catalog)
    for name, filename in FILES.items():
        (data_dir / filename).write_text(json.dumps(displayed_catalog[name], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for filename in ("research-atlas.css", "research-atlas.js", "research-focus.js", "research-delta.js"):
        shutil.copyfile(ROOT / "website/static" / filename, root / "static" / filename)
    additions: list[dict[str, Any]] = []
    def write(route: str, title: str, body: str, toc: list[tuple[str, str]] | None = None) -> None:
        prefix = site.prefix_for(route)
        breadcrumbs = '<nav class="ra-breadcrumb" aria-label="Research views">' + "".join(f'<a href="{prefix}{path}index.html">{esc(label)}</a>' for label, path in VIEWS) + '</nav>'
        page = site.page_template(title=title, route=route, current=route,
            body='<div class="ra-book">' + breadcrumbs + body + '</div>', coverage=coverage, gate=gate, context=context, toc=toc,
            extra_styles=("static/research-atlas.css",), extra_scripts=("static/research-atlas.js", "static/research-delta.js"))
        site.write_page(root, route, page)
        additions.append({"type": "page", "kind": "research", "title": title, "summary": re.sub("<[^>]+>", " ", body)[:500], "url": route + "index.html"})
    hero = lambda title, body: '<header class="ra-hero"><p class="eyebrow">Structure before circuit tricks</p><h1>' + esc(title) + '</h1><p class="lede">' + esc(body) + '</p></header>'
    intro = hero("Mathematical methods", "Search by problem structure, then inspect the hypotheses, mathematical mechanism, exact Lean substrates and unresolved boundaries. One declaration has one identity across every view.")
    intro += '<div class="ra-warning">Overview = curated organization. Lean graph = generated imports and declaration ownership. Hypergraph = conditional conceptual transport. None of these is an automatic novelty or theorem-implication oracle.</div>'
    intro += '<div class="ra-filter"><label for="method-query">Search structure or technique</label><input id="method-query" data-ra-search placeholder="e.g. polynomial, envelope, QSVT, norm, phase"><p data-ra-count aria-live="polite"></p></div>'
    for domain in atlas["domains"]:
        cards = []
        for f in atlas["families"]:
            if domain["id"] not in f["domains"]:
                continue
            haystack = " ".join([f["label"], f["question"], *f["tags"]])
            cards.append(f'<article class="ra-card" data-ra-item="{esc(haystack)}"><p class="eyebrow">Mechanism family</p><h3><a href="{slug(f["id"])}/index.html">{esc(f["label"])}</a></h3><p>{esc(f["question"])}</p><p class="ra-boundary">{esc(f["boundary"])}</p></article>')
        intro += section(domain["label"], '<p>' + esc(domain["question"]) + '</p><div class="ra-grid">' + "".join(cards) + '</div>', slug(domain["id"]))
    intro += section("Agent retrieval without graph dumps", '<p>The same authored records produce a bounded packet. It contains assumptions and failure boundaries, not only similar keywords.</p><pre><code>python3 website/scripts/research_atlas.py context --query "localized function envelope"\npython3 website/scripts/research_atlas.py context --route spw-envelope</code></pre><p><a href="../data/research/atlas.json">Download mechanism metadata</a></p>', "agent-retrieval")
    write("mathematical-methods/", "Mathematical methods", intro)
    for f in atlas["families"]:
        prefix = "../../"
        body = hero(f["label"], f["question"]) + math(f["formula"])
        body += section("What this technique preserves", '<p>' + esc(f["mechanism"]) + '</p>', "mechanism")
        body += section("Hypotheses and hidden contracts", paragraphs(f["assumptions"]), "hypotheses")
        body += section("Mathematical proof mechanism", '<p>This is an authored reusable derivation guide, not a claim that the full family has been source-assimilated.</p>' + paragraphs(f["proof_steps"], True), "proof")
        body += section("Exact Lean substrates", lean_links(f["lean_refs"], declarations, prefix, True), "lean")
        body += section("Do not cross this boundary", '<p class="ra-warning">' + esc(f["boundary"]) + '</p>', "boundary")
        if "technical_card" in f:
            card = f["technical_card"]
            body += render_technical_card(card, families, {r["id"]: r for r in wiki["routes"]}, sources, declarations, prefix)
            filename = slug(f["id"]) + "-technical-card.json"
            (data_dir / filename).write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            body += f'<p><a download href="{prefix}data/research/{filename}">Download technical card JSON</a></p>'
        connected = [e for e in atlas["hyperedges"] if f["id"] in e["tails"] + e["heads"]]
        body += section("Related transports", "".join(f'<p><a href="../../functor-hypergraph/index.html#{slug(e["id"])}">{esc(e["label"])}</a> — {esc(e["status"])}</p>' for e in connected))
        body += section("Source and prior-art ledger", source_list(f["source_ids"], sources), "sources")
        latex = family_latex(f)
        (data_dir / (slug(f["id"]) + ".tex")).write_text(latex, encoding="utf-8")
        body += '<details class="ra-code"><summary>Copy mathematical mechanism as LaTeX</summary><button type="button" data-ra-copy>Copy LaTeX</button><pre><code>' + esc(latex) + '</code></pre></details>'
        body += f'<p><a download href="../../data/research/{slug(f["id"])}.tex">Download LaTeX</a></p>'
        write("mathematical-methods/" + slug(f["id"]) + "/", f["label"], body, [("mechanism", "Mechanism"), ("hypotheses", "Hypotheses"), ("proof", "Proof guide"), ("lean", "Lean"), ("boundary", "Boundary"), ("sources", "Sources")])
    hyper = hero("Functor Hypergraph", "Follow mathematical mechanisms across fields without confusing an analogy, a conditional construction and a formal implication.")
    hyper += '<div class="ra-warning">All tails of a hyperedge are required together (AND). Incidence lines are not separate implications. Every transport here is curated or proposed; no Lean-certified categorical functor is asserted.</div>'
    hyper += '<div class="ra-graph-app" data-ra-hypergraph data-url="../data/research/atlas.json"><label for="transport-select">Choose a complete transport</label><select id="transport-select" data-ra-edge>' + "".join(f'<option value="{esc(e["id"])}">{esc(e["label"])}</option>' for e in atlas["hyperedges"]) + '</select><div class="ra-graph-stage"><svg data-ra-svg role="img" aria-label="Conjunctive mathematical transport" viewBox="0 0 1000 360"></svg></div><p class="ra-legend">Dashed paths: curated/proposed incidence. AND junction: all listed hypotheses and tail mechanisms. Solid proof dependencies remain in the separate generated Lean graph.</p><button type="button" data-ra-download-svg>Download this diagram as SVG</button><p data-ra-graph-status aria-live="polite"></p></div>'
    for e in atlas["hyperedges"]:
        tails = "".join(f'<li><a href="{node_url(i, "../")}">{esc(nodes[i]["label"])}</a></li>' for i in e["tails"])
        heads = "".join(f'<li><a href="{node_url(i, "../")}">{esc(nodes[i]["label"])}</a></li>' for i in e["heads"])
        body = f'<p><span class="ra-tag">{esc(e["status"])}</span> {esc(e["review"])}</p>' + math(e["formula"])
        body += '<div class="ra-transport"><div><h3>All inputs required</h3><ul>' + tails + '</ul></div><strong class="ra-and">AND</strong><div><h3>Conditional outputs</h3><ul>' + heads + '</ul></div></div>'
        body += '<dl class="ra-contract">' + "".join(f'<dt>{label}</dt><dd>{esc(e[key])}</dd>' for key, label in (("mechanism", "Mechanism"), ("hypothesis_map", "Hypothesis map"), ("conclusion_map", "Conclusion map"), ("failure_boundary", "Failure boundary"))) + '</dl>'
        body += lean_links(e["lean_refs"], declarations, "../") + source_list(e["source_ids"], sources)
        hyper += section(e["label"], body, slug(e["id"]))
    deltas = [contribution_delta(item) for item in atlas["contributions"]]
    for c, delta in zip(atlas["contributions"], deltas):
        body = '<div class="ra-tags">' + "".join(f'<span class="ra-tag">{esc(kind)}</span>' for kind in c["classes"]) + '</div>'
        body += '<div class="ra-comparison"><article><h3>Before</h3><p>' + esc(c["before"]) + '</p></article><article><h3>After</h3><p>' + esc(c["after"]) + '</p></article></div>' + math(c["formula"])
        body += '<p><strong>Preserved contract:</strong> ' + esc(c["invariant"]) + '</p><p class="ra-warning">' + esc(c["novelty_boundary"]) + '</p>'
        body += '<p><strong>Actual Git module/import delta:</strong> ' + esc(delta["status"]) + '. This is not an elaborated proof-term delta.</p>'
        body += f'<div class="ra-graph-app" data-ra-delta="{esc(c["id"])}"><label>Inspect changed import edges around a module <select data-ra-delta-select aria-label="Module in contribution delta"></select></label><div class="ra-graph-stage" style="max-height:620px"><svg data-ra-delta-svg role="img" aria-label="Pinned module import contribution delta"></svg></div><p data-ra-delta-status aria-live="polite">Loading the computed Git delta; complete source data is linked below.</p><p class="ra-legend">Solid lines: added imports. Dashed lines: removed imports. This is the changed module-import neighborhood, not a theorem proof graph or an automatically inferred novelty classification.</p></div>'
        body += '<details><summary>Added modules at the pinned contribution</summary>' + paragraphs(delta["added_modules"]) + '</details>'
        body += '<p><a download href="../data/research/contributions.json">Download baseline/head and exact module-import delta</a></p>'
        hyper += section(c["label"], body, slug(c["id"]))
    write("functor-hypergraph/", "Functor Hypergraph", hyper)
    agenda = hero("StatePreparationWiki", "Research targets with explicit access models, acceptance tests and model-matched lower-bound obligations. A candidate route is not a proved open-problem classification.")
    agenda += '<div class="ra-warning">' + esc(wiki["baseline"]["statement"]) + ' ' + esc(wiki["baseline"]["prohibition"]) + '</div>'
    agenda += section("The resource contract", paragraphs(wiki["resource_contract"]), "resources")
    agenda += '<div class="ra-filter"><label for="wiki-query">Search application, obstacle or technique</label><input id="wiki-query" data-ra-search placeholder="e.g. PDE, envelope, phase, Gibbs"><p data-ra-count aria-live="polite"></p></div><div class="ra-grid">'
    for r in sorted(wiki["routes"], key=lambda item: (item["priority"], item["id"])):
        agenda += f'<article class="ra-card" data-ra-item="{esc(json.dumps(r, ensure_ascii=False))}"><p class="eyebrow">Priority {r["priority"]} · research target</p><h2><a href="{r["id"]}/index.html">{esc(r["title"])}</a></h2><p>{esc(r["goal"])}</p><p class="ra-boundary">{esc(r["known_boundary"])}</p></article>'
    agenda += '</div>' + section("Audited baselines and candidate references", source_list(list(sources), sources), "sources")
    write("state-preparation-wiki/", "StatePreparationWiki", agenda)
    for r in wiki["routes"]:
        body = hero(r["title"], r["motivation"]) + '<p><span class="ra-tag">research target</span> <code>' + esc(r["setting_id"]) + '</code></p>' + math(r["formula"])
        if r.get("reading_layers"):
            layers = ''.join('<details class="ra-code" data-reading-layer><summary>' + esc(layer["title"]) + '</summary><p>' + esc(layer["summary"]) + '</p>' + paragraphs(layer["items"]) + '</details>' for layer in r["reading_layers"])
            body += section("Choose your reading depth", '<p>Question → mechanism → mathematical suppliers → evidence. Open only the level you need; the contract and unproved boundaries remain visible below.</p>' + layers, "reading-depth")
        body += section("Frozen target and input model", '<p>' + esc(r["goal"]) + '</p><p><strong>Access model:</strong> ' + esc(r["input_model"]) + '</p>' + paragraphs(r["assumptions"]), "contract")
        body += section("Desired result, not an achieved bound", '<p>' + esc(r["target_bound"]) + '</p><p class="ra-warning">' + esc(r["known_boundary"]) + '</p>', "boundary")
        body += section("Dependency-ready execution route", '<div class="ra-steps">' + "".join(f'<article><span class="ra-step-number">{i+1:02d}</span><h3>{esc(s["target"])}</h3><p><strong>Acceptance:</strong> {esc(s["acceptance"])}</p><p class="ra-tag">planned; no claimed closure</p></article>' for i, s in enumerate(r["steps"])) + '</div><p><strong>Next bounded advance:</strong> ' + esc(r["next"]) + '</p>', "route")
        body += section("Reusable mathematics", family_links(r["families"], families, "../../") + lean_links(r["lean_refs"], declarations, "../../"), "reuse")
        body += section("Lower-bound comparison contract", '<p><span class="ra-tag">' + esc(r["lower_bound"]["status"]) + '</span></p><p>' + esc(r["lower_bound"]["task"]) + '</p><p><strong>Same-model key:</strong> <code>' + esc(r["lower_bound"]["comparison_key"]) + '</code></p>', "lower-bound")
        body += section("Diagnostic examples, not proofs", paragraphs(r["benchmarks"]), "examples")
        body += section("Primary-source ledger", source_list(r["source_ids"], sources), "sources")
        packet = context_packet(catalog, route_id=r["id"])
        (data_dir / (r["id"] + "-packet.json")).write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        body += '<p><a download href="../../data/research/' + r["id"] + '-packet.json">Download bounded agent / contributor packet</a></p>'
        body += '<pre><code>python3 website/scripts/research_atlas.py context --route ' + r["id"] + '</code></pre>'
        write("state-preparation-wiki/" + r["id"] + "/", r["title"], body, [("contract", "Contract"), ("route", "Execution route"), ("reuse", "Reuse"), ("lower-bound", "Lower bound"), ("sources", "Sources")])
    progress = progress_payload(catalog, declarations, str(context["commit"]))
    body = hero("Current Progress", "One generated projection of the existing textbook and implementation frontier, alongside the new research contracts. No manual chapter-completion percentages and no credit transfer from prerequisites.")
    body += '<p class="ra-warning">Compiled local results, source-complete theorems, reusable interfaces, rejected routes and research targets are different evidence classes. The counts below count records, not mathematical importance.</p>'
    body += '<div class="ra-metrics"><article><strong>' + str(len(progress["chapters"])) + '</strong><span>existing chapter records</span></article><article><strong>' + str(len(wiki["routes"])) + '</strong><span>research-target contracts</span></article></div>'
    body += section("Textbook routes and their exact residual boundaries", "".join(render_chapter_progress(c, declarations) for c in progress["chapters"]), "textbook")
    paper_cards = []
    for paper in progress["paper_frontier"].get("featured", []) + progress["paper_frontier"].get("queue", []):
        title = esc(paper["title"])
        route = paper.get("route")
        heading = f'<a href="../{esc(route)}index.html">{title}</a>' if route else title
        roots = paper.get("leanRoots", [])
        residual = paper.get("remaining", paper.get("summary", "Exact source scope must be inspected."))
        paper_cards.append('<article class="ra-card"><h3>' + heading + '</h3><p class="ra-tag">' + esc(paper["status"]) + '</p><p><strong>Source anchors:</strong> ' + esc(", ".join(paper.get("sourceAnchors", []))) + '</p><p><strong>Current scope:</strong> ' + esc(paper.get("formalized", paper.get("summary", "Queued; no paper-wide closure claimed."))) + '</p><p><strong>Residual / next acceptance boundary:</strong> ' + esc(residual) + '</p>' + lean_links(roots, declarations, "../") + '</article>')
    body += section("Existing source-paper routes", '<div class="ra-grid">' + "".join(paper_cards) + '</div>', "paper-frontier")
    frontier = []
    for i, record in enumerate(progress["implementation_frontier"]):
        name = record["declaration"]
        if name not in declarations:
            raise ValueError(f"implementation frontier lost root: {name}")
        frontier.append('<article class="ra-card"><h3>' + esc(record["goal"]) + '</h3>' + math(record["contract"]) + '<p><span class="ra-tag">' + esc(record["status"]) + '</span></p><p><strong>Obligation:</strong> ' + esc(record["obligation"]) + '</p><p><strong>Existing parents:</strong> ' + esc(record["dependencies"]) + '</p><p><strong>Residual / next boundary:</strong> ' + esc(record["missing"]) + '</p>' + lean_links([name], declarations, "../") + '</article>')
    body += section("Existing implementation frontier — preserved, not overwritten", '<div class="ra-grid">' + "".join(frontier) + '</div>', "implementation")
    remaining = [r for r in progress["historical_roadmap"] if r["status"] != "Compiled"]
    body += section("Previously pending work", '<p>These are the existing roadmap entries, not newly invented completions. Each resumes by fixing the source target and checking which compiled interfaces genuinely discharge it.</p>' + "".join('<article class="ra-card"><h3>' + esc(r["title"]) + '</h3><p class="ra-tag">' + esc(r["status"]) + '</p><p>Next: freeze an arbitrary-width/source contract; connect current semantic leaves to the actual primitive compiler; prove the resource theorem; then pass independent source fidelity and publication gates.</p></article>' for r in remaining), "pending")
    body += section("StatePreparationWiki execution queue", '<div class="ra-grid">' + "".join(f'<article class="ra-card"><p class="eyebrow">Priority {r["priority"]} · research target</p><h3><a href="../state-preparation-wiki/{r["id"]}/index.html">{esc(r["title"])}</a></h3><p>{esc(r["next"])}</p><p><strong>First acceptance test:</strong> {esc(r["steps"][0]["acceptance"])}</p></article>' for r in sorted(wiki["routes"], key=lambda x: (x["priority"], x["id"]))) + '</div>', "wiki")
    body += section("Contribution admission", '<p>Source statement → exact Lean statement → source-blind reconstruction → independent comparison → separately reviewed repairs. Authors do not self-certify a review. A graph delta records add-node, shortcut, reorganisation or bridge, while global novelty remains a separate literature judgement.</p><p><a href="../research-protocol/index.html">Read the adapted ASPBE publication protocol</a> · <a download href="../data/research/progress.json">Download this generated progress snapshot</a></p>', "admission")
    write("progress/", "Current Progress", body, [("textbook", "Textbook"), ("paper-frontier", "Paper routes"), ("implementation", "Implementation"), ("pending", "Pending work"), ("wiki", "Research queue"), ("admission", "Admission")])
    protocol = ROOT / "docs/theorem-publication-protocol.md"
    if not protocol.is_file():
        raise ValueError("ASPBE publication protocol is required")
    body = hero("ASPBE publication and graph protocol", "Mathematics is authored once; reader, agent and graph views reuse the same declarations and contracts.")
    body += section("Source, semantics, evidence and presentation", '<p>This adaptation credits Samplinglib, but keeps quantum register, phase, norm, oracle, ancilla and finite-precision contracts explicit. No new independent review has been fabricated by this website change.</p>' + source_list(["samplinglib-protocol"], sources))
    body += '<pre class="ra-protocol"><code>' + esc(protocol.read_text(encoding="utf-8")) + '</code></pre>'
    write("research-protocol/", "ASPBE publication and graph protocol", body)
    # Preserve the existing Lean graph and all its audited assertions.
    graph_page = root / "lean-graph/index.html"
    text = graph_page.read_text(encoding="utf-8")
    text = re.sub(r"<!-- research-lens:start -->.*?<!-- research-lens:end -->", "", text, flags=re.S)
    lens = '<!-- research-lens:start --><section class="ra-section" id="mathematical-structure-lens"><p class="eyebrow">Three views, one set of Lean identities</p><h2>From dependencies to mathematical ideas</h2><div class="ra-grid">' + "".join(f'<article class="ra-card"><h3><a href="../{route}index.html">{esc(title)}</a></h3><p>' + desc + '</p></article>' for (title, route), desc in zip(VIEWS, ("Search reusable mechanisms by structural assumptions.", "Inspect typed AND transports and hypothesis/failure maps.", "Freeze research targets and compare bounds in the same model.", "See exact textbook residuals and the next acceptance target."))) + '</div><p class="ra-warning">The graph below still records generated module imports and declaration ownership, not elaborated theorem dependencies. The new atlas is a curated lens, not a replacement proof graph.</p></section><!-- research-lens:end -->'
    text = text.replace('<main id="main-content">', '<main id="main-content">' + lens, 1)
    if "research-atlas.css" not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="../static/research-atlas.css"></head>', 1)
    if "research-focus.js" not in text:
        text = text.replace("</body>", '<script src="../static/research-focus.js" defer></script></body>', 1)
    graph_page.write_text(text, encoding="utf-8")
    patch_navigation(root)
    for name, value in (("progress.json", progress), ("contributions.json", {"schema_version": 1, "contributions": deltas})):
        (data_dir / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    search_path = root / "search-index.json"
    search = read_json(search_path)
    search["entries"] = [entry for entry in search["entries"] if entry.get("kind") != "research"] + additions
    search["entryCount"] = len(search["entries"])
    search["pageEntryCount"] = sum(entry.get("type") == "page" for entry in search["entries"])
    search_path.write_text(json.dumps(search, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for filename in ("site-metadata.json", "build-report.json"):
        path = root / filename
        value = read_json(path)
        value["searchEntryCount"] = search["entryCount"]
        value["researchAtlas"] = {"schema_version": 1, "sourceDigest": source_digest(), "familyCount": len(families), "routeCount": len(wiki["routes"]), "hyperedgeCount": len(atlas["hyperedges"]), "truthLayer": "curated-overlay", "leanGraphSha256": graph_digest}
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if hashlib.sha256(graph_path.read_bytes()).hexdigest() != graph_digest:
        raise ValueError("research overlay must not mutate the authoritative Lean graph")
    return {"pages": len(additions), "families": len(families), "routes": len(wiki["routes"]), "hyperedges": len(atlas["hyperedges"]), "leanGraphUnchanged": True}


def render_chapter_progress(chapter: dict[str, Any], declarations: dict[str, Any]) -> str:
    from website.scripts import build_site as site
    content = f'<details class="ra-chapter"><summary><span>{esc(chapter["track"])}</span> {esc(chapter["title"])} <small>{len(chapter["results"])} mapped result records</small></summary><p>{esc(chapter["summary"])}</p><p><a href="../chapters/{chapter["id"]}/index.html">Open the existing chapter</a></p>'
    for result in chapter["results"]:
        content += '<article class="ra-result"><h3>' + esc(result["title"]) + '</h3>' + math(result["math"])
        content += '<p><strong>Local:</strong> ' + esc(result["local_status"]) + ' · <strong>Route:</strong> ' + esc(result["route_status"]) + '</p><p><strong>Residual:</strong> ' + esc(result["missing"]) + '</p>'
        content += '<p><a href="' + site.module_url("../", declarations[result["declaration"]]) + '"><code>' + esc(result["declaration"]) + '</code></a></p>'
        content += '<details><summary>Mapped parents and route-closure names</summary>' + paragraphs(list(result["dependencies"] or []) + list(result["route_closures"] or [])) + '</details></article>'
    return content + '</details>'


def source_digest() -> str:
    digest = hashlib.sha256()
    for filename in sorted(FILES.values()):
        digest.update(filename.encode())
        digest.update((DATA / filename).read_bytes())
    return digest.hexdigest()


def check_published(root: Path) -> None:
    catalog = load_catalog()
    expected = public_catalog(catalog)
    for name, filename in FILES.items():
        if read_json(root / "data/research" / filename) != expected[name]:
            raise ValueError("published research catalog differs from its declared display projection: " + filename)
    for _, route in VIEWS:
        path = root / route / "index.html"
        if not path.is_file() or not all(marker in path.read_text(encoding="utf-8") for marker in ('class="site-sidebar"', 'data-taxonomy-nav="papers"', 'data-taxonomy-nav="example-cases"')):
            raise ValueError(f"missing reader route: {route}")
    metadata = read_json(root / "build-report.json")["researchAtlas"]
    if metadata["sourceDigest"] != source_digest():
        raise ValueError("published research metadata is stale")
    if metadata["leanGraphSha256"] != hashlib.sha256((root / "data/lean-graph.json").read_bytes()).hexdigest():
        raise ValueError("published graph provenance changed")
    hyper = (root / "functor-hypergraph/index.html").read_text(encoding="utf-8")
    for marker in ("All inputs required", "AND", "Failure boundary", "no Lean-certified", "data-ra-hypergraph"):
        if marker not in hyper:
            raise ValueError(f"hypergraph lost truth contract: {marker}")
    for route in catalog["wiki"]["routes"]:
        path = root / "state-preparation-wiki" / route["id"] / "index.html"
        text = path.read_text(encoding="utf-8")
        for marker in ("Same-model key", "Acceptance:", "research target", route["setting_id"]):
            if marker not in text:
                raise ValueError(f"wiki route lost {marker}: {route['id']}")
    print("research publication contract passed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "publish", "check-site", "context"))
    parser.add_argument("--root", type=Path, default=ROOT / "_site")
    parser.add_argument("--query", default="")
    parser.add_argument("--route")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.command == "context":
        print(json.dumps(context_packet(load_catalog(), args.query, args.route, args.limit), ensure_ascii=False, indent=2))
    elif args.command == "check":
        validate_catalog(load_catalog())
        print("research source contracts passed (no Lean promotion)")
    elif args.command == "publish":
        print(json.dumps(publish(args.root), indent=2))
    else:
        check_published(args.root)


if __name__ == "__main__":
    main()
