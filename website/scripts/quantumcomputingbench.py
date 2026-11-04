#!/usr/bin/env python3
"""Publish one hierarchical reader over the evidence-qualified shared QA cores."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sys
import tempfile
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "benchmarks/quantumcomputingbench"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(B / "src"))
from qcb_core import digest, read_json, write_json
from qcb_curriculum import load_catalog, reader_source_digest, stable_readiness
from qcb_integrity import text_sha
from qcb_textbook_policy import public_reader_item

HUB = "quantumcomputingbench/"
REPO = "https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench"
SOURCE_COMMIT = "86b9e677566498da04faebcf4e5ed57f177c6bb1"
TRACKS = ("non-lean", "lean")


def esc(value):
    return html.escape(str(value), quote=True)


def prose(value):
    """Render source-bound mathematics without changing the underlying QA record."""
    from website.scripts.qcb_math import render_prose
    return render_prose(value)


def title_of(topic):
    return topic.removeprefix("planned_").replace("_", " ").title()


def section(title, content, anchor):
    return f'<section class="qcb-section" id="{esc(anchor)}"><h2>{esc(title)}</h2>{content}</section>'


def disclosure(title, content, anchor):
    return (f'<details class="qcb-disclosure" id="{esc(anchor)}"><summary>{esc(title)}</summary>'
            '<div class="qcb-details-content tex2jax_ignore" data-qcb-math-deferred>' + content + '</div></details>')


def reader_sources():
    return reader_source_digest()


def presentation_contract():
    paths = ("website/scripts/qcb_math.py", "website/static/qcb-math.css",
             "website/scripts/qcb_expert.py", "website/static/qcb-expert.css", "website/static/qcb-expert.js",
             "website/scripts/qcb_benchmark_center.py", "benchmarks/quantumcomputingbench/src/qcb_bench_runtime.py",
             "website/scripts/qcb_workbook_reader.py", "benchmarks/quantumcomputingbench/src/qcb_nonlean_workbook.py",
             "benchmarks/quantumcomputingbench/reports/nonlean-intake-20261104/reader-comparison.json",
             "website/scripts/qcb_ecosystem_browser.py",
             "benchmarks/quantumcomputingbench/scripts/bench.py",
             "benchmarks/quantumcomputingbench/reports/ecosystem-v1/math-notation-review.json")
    sources = {p: text_sha(ROOT / p) for p in paths}
    return {"schema_version": "qcb.reader_presentation.v1", "sources_lf": sources, "digest": digest(sources)}


def math_notation_contract(catalog_hash):
    from website.scripts.qcb_math import _QUESTION_COMPANIONS, notation_source_bindings
    review = read_json(B / "reports/ecosystem-v1/math-notation-review.json")
    bindings = notation_source_bindings()
    rows = review.get("per_item_review", [])
    if (review.get("schema_version") != "qcb.math_notation_semantic_review.v1"
            or review.get("catalog_hash") != catalog_hash
            or review.get("notation_source_bindings") != bindings
            or review.get("notation_source_bindings_digest") != digest(bindings)
            or review.get("notation_annotations_digest") != digest(_QUESTION_COMPANIONS)
            or len(rows) != len(bindings) or {r["record_id"] for r in rows} != set(bindings)
            or any(r["verdict"] != "accepted_notation_excerpt"
                   or r["extra_assumptions_introduced"] is not False
                   or r["source_claim_replaced"] is not False
                   or r["gold_verdict_counterexample_or_repair_inserted"] is not False for r in rows)):
        raise ValueError("question notation changed without its bound mathematical review")
    return {"review_digest": digest(review), "annotations_digest": digest(_QUESTION_COMPANIONS),
            "reviewed_notation_excerpts": len(rows), "human_expert_approval": review["human_expert_approval"]}


def environment_record(registry):
    source = ROOT / "_out/qcb-container-smoke/public-summary.json"
    if not source.exists():
        return {"schema_version": "qcb.portable_environment_smoke.v1", "execution_status": "not_run", "passed": None,
                "registry_hash": registry["registry_hash"], "source_commit": registry["source_commit"],
                "model_performance_measured": False}
    record = read_json(source)
    if (record.get("schema_version") != "qcb.portable_environment_smoke.v1" or record.get("passed") is not True
            or record.get("execution_status") != "passed" or record.get("registry_hash") != registry["registry_hash"]
            or record.get("source_commit") != registry["source_commit"]
            or record.get("student_workspace_verified") is not True or record.get("oracle_decision_accuracy") != 1
            or record.get("wrong_decision_accuracy") != 0 or record.get("not_run_decision_accuracy") != 0
            or record.get("tampered_task_rejected") is not True or record.get("model_performance_measured") is not False):
        raise ValueError("portable environment evidence does not match the actual registry or controls")
    return record


COURSE_LABELS = {
    "sp-009": "From real core rows to complex isometries",
    "be-105": "Normalization and a planar rotation",
    "be-107": "Unitary operators with controlled blocks",
    "be-109": "Tensor lifts across three registers",
    "la-102": "Row rotations and determinants",
    "sp-005": "Norms under a last-bit marginal",
    "sp-007": "Sequential amplitudes and transfer contractions",
    "sp-008": "Probability along a sequential preparation",
    "sp-114": "Polynomial arrays and rank factorization",
    "be-106": "Amplitude readout and its domain",
    "be-112": "LCU composition and inverse requirements",
    "sp-113": "A conditioning anchor and the normalizer",
    "sp-120": "A cutoff search and its exact-real cost",
    "be-110": "Controlled permutations and their inverses",
    "be-111": "Permutation matrices and circuit chronology",
    "sp-104": "Two-point polynomial interpolation",
    "sp-101": "Taylor data and prescribed derivatives",
    "be-102": "Reversible arithmetic with clean and dirty work",
}
COURSE_BANDS = {
    "D0": ("Read the contract", "Identify the objects, dimensions, register order and assumptions before proving anything. This is a knowledge facet of the same questions, not another set of questions."),
    "D1": ("Understand and apply", "Translate a mathematical statement faithfully and select a disclosed library interface."),
    "D2": ("Construct locally", "Work through matrix entries, finite sums, polynomial coefficients or a concrete reversible action."),
    "D3": ("Connect interfaces", "Combine several mathematical ingredients, preserving every required assumption at the join."),
    "D4": ("Control a whole family", "Use induction, invariants or a global degree argument to handle a parameterized family."),
}


@lru_cache(maxsize=1)
def course_reader():
    """A separate, qualified sidecar; never mutate canonical formal admissions."""
    sys.path.insert(0, str(B / "scripts"))
    from lean_course_v3 import load_course
    plan, views, _, _, report = load_course()
    return plan, views, report


DIAGNOSTIC_CLUSTERS = {
    "state_core_isometry_and_mass": (
        "Core orientation, mass and isometry",
        "Track the input bond and the output registers through statements about mass, normalization and matrix orientation.",
        "ᵀ denotes transpose, † denotes conjugate transpose, and I_l is the identity on l coordinates. Old bond, physical bit and new bond name distinct index registers.",
        ("Mass and normalization", "Changing output order", "Operators on the output space")),
    "state_marginal_norm_and_linearity": (
        "Marginal amplitudes and linearity",
        "Compare an amplitude table with its last-bit marginal, checking both the norm statement and the proposed linear action.",
        "An n-bit prefix b records all but the last wire; (b,v) appends the bit v. The square root is the nonnegative real square root.",
        ("A last-bit marginal",)),
    "controlled_permutation_semantics": (
        "Controlled permutations and register order",
        "Follow the selector and coefficient through basis relabeling, inverse maps and chronological composition.",
        "For k=(x,(c,s)), k.1=x, k.2.1=c and k.2.2=s. A matrix entry uses an output row and an input column. The stated column-vector convention fixes how matrix products act.",
        ("Relabeling a controlled register", "A selector and its inverse", "Chronological composition")),
    "hermite_endpoint_multiplicity": (
        "Endpoint jets and the degree boundary",
        "Compare matching endpoint derivative data under two different degree budgets.",
        "Derivative order zero means the polynomial itself. Higher orders are ordinary repeated derivatives. Each degree bound applies separately to p and q.",
        ("Two degree budgets",)),
}


def diagnostic_reader():
    """Requalify the actual public cohort on every publication/check, without cache."""
    from qcb_learning_reference import qualify
    from qcb_learning_validity import load_cohort
    packet, _ = load_cohort()
    qualification = qualify(packet)
    if (qualification.get("status") != "PUBLIC_SEMANTIC_REFERENCE_PILOT_QUALIFIED"
            or qualification.get("cohort_digest") != digest(packet)
            or qualification.get("formal_coverage") != "decision_polarity_only"
            or qualification.get("actual_model_performance_measured") is not False
            or qualification.get("learning_gain") is not None or qualification.get("hidden_holdout") is not False
            or qualification.get("canonical_admissions_changed") is not False):
        raise ValueError("diagnostic reader requires the actual content-bound reference qualification")
    if {p["cluster_id"] for p in packet["probes"]} != set(DIAGNOSTIC_CLUSTERS):
        raise ValueError("diagnostic reader cluster coverage needs an explicit editorial update")
    return packet, qualification


def diagnostic_source_link(path, publication_commit, label=None):
    """Only the publication context supplies source revisions; never use main."""
    relative = PurePosixPath(path)
    if (relative.is_absolute() or ".." in relative.parts or "\\" in path or ":" in path):
        raise ValueError("diagnostic source links must be repository-relative paths")
    label = label or path
    if not isinstance(publication_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", publication_commit):
        return '<span>' + esc(label) + ' (publication source link unavailable)</span>'
    url = REPO + '/blob/' + publication_commit + '/' + quote(path, safe='/')
    return '<a href="' + esc(url) + '">' + esc(label) + '</a>'


def diagnostic_manifest(packet, qualification, publication_commit):
    return {"schema_version": "qcb.public_semantic_diagnostics.v1", "cohort_id": packet["cohort_id"],
            "cohort_digest": digest(packet), "reference_receipt_digest": qualification["reference_receipt_digest"],
            "qualification": qualification["status"], "source_commit": publication_commit,
            "reader_renderer_sha256_lf": text_sha(Path(__file__)),
            "diagnostic_candidates": len(packet["probes"]),
            "contrast_pairs": len({p["pair_id"] for p in packet["probes"]}),
            "clusters": dict(Counter(p["cluster_id"] for p in packet["probes"])),
            "reference_replay_count": qualification["reference_replay_count"],
            "formal_coverage": "decision_polarity_only", "admission": "candidate_not_counted",
            "new_canonical_core_ids": 0, "new_canonical_lean_admissions": 0, "new_course_companions": 0,
            "hidden_holdout": False, "model_performance_measured": False, "learning_gain": None,
            "routes": [HUB + "diagnostics/index.html"] + [HUB + "diagnostics/" + key + "/index.html" for key in DIAGNOSTIC_CLUSTERS]}


def diagnostic_evidence(packet, qualification, publication_commit):
    base = 'benchmarks/quantumcomputingbench/'
    paths = ((base + 'tracks/lean/learning-validity/v1/cohort.json', 'Exact candidate questions, answers and rubrics'),
             (base + 'reports/learning-validity-v1/decoder.json', 'Independent formal-statement reconstruction'),
             (base + 'reports/learning-validity-v1/source-comparison.json', 'Distinct source-aware semantic comparison'),
             (base + 'reports/learning-validity-v1/answer-review.json', 'Independent explanation and rubric review'),
             (base + 'reports/learning-validity-v1/reference-checks.json', 'Actual authored Lean reference receipt'))
    body = '<p>The authored Lean reference batch checks the decision target P or ¬P, including fresh final-root replays. It covers the decision polarity only. The explanatory answer and rubric have separate content-bound mathematical review; a compiled root does not certify every explanatory sentence or proposed repair.</p>'
    body += '<p>Authoring and review are AI-assisted. Recorded distinct reviewers and exact hashes establish provenance; they do not authenticate real-world independence or imply human expert approval. No model evaluation is needed to read this public reference pilot.</p><ul>'
    body += ''.join('<li>' + diagnostic_source_link(path, publication_commit, label) + '</li>' for path, label in paths) + '</ul>'
    body += '<p>Cohort SHA-256: <code>' + esc(digest(packet)) + '</code><br>Reference receipt SHA-256: <code>' + esc(qualification["reference_receipt_digest"]) + '</code><br>Actual reference checks: ' + esc(qualification["reference_replay_count"]) + '.</p>'
    body += '<h3>Bound library sources</h3><ul>' + ''.join('<li>' + diagnostic_source_link(s["path"], publication_commit) + '<br><small>Source SHA-256 (LF): <code>' + esc(s["sha256_lf"]) + '</code></small></li>' for s in packet["source_bindings"]) + '</ul>'
    return disclosure("Sources, independent review and actual reference evidence", body, "diagnostic-evidence")


def diagnostic_probe_body(probe, number, packet, expert_index=None):
    from qcb_learning_validity import challenge_task

    from website.scripts.qcb_math import question_equations
    anchor = 'probe-' + probe["probe_id"]
    body = '<article class="qcb-part" id="' + esc(anchor) + '" data-qcb-diagnostic="' + esc(probe["probe_id"]) + '"><h3>Question ' + str(number) + '</h3>'
    body += '<p class="qcb-meta">Candidate diagnostic · provisional ' + esc(probe["difficulty"]["band"]) + ' · ' + esc(probe["reasoning_kind"].replace('_', ' ')) + ' · inherited split: ' + esc(probe["split"]) + '</p>'
    for field in ("assumptions", "conventions"):
        body += '<h4>' + field.title() + '</h4><ul data-qcb-diagnostic-' + field + '>' + ''.join('<li>' + prose(value) + '</li>' for value in probe[field]) + '</ul>'
        if not probe[field]:
            body += '<p class="qcb-meta">None listed separately; all premises stated in the question still apply.</p>'
    body += '<div data-qcb-diagnostic-question>' + prose(probe["question"]) + '</div>'
    body += question_equations(probe["probe_id"], probe["question"])
    body += disclosure("Reference decision and mathematical explanation", '<p><strong>Reference decision: ' + esc(probe["gold"]["decision"]) + '</strong></p>' + prose(probe["gold"]["answer"]), 'answer-' + probe["probe_id"])
    rubric = '<ol>' + ''.join('<li>' + prose(row["criterion"]) + ' <small>(weight ' + esc(row["weight"]) + ')</small></li>' for row in probe["gold"]["rubric"]) + '</ol>'
    body += disclosure("Assessment rubric", rubric, 'rubric-' + probe["probe_id"])
    # The same evaluator-owned construction used by reference qualification.
    task = challenge_task(probe, probe["gold"]["decision"], snapshot_id=packet["snapshot_id"], library_revision=packet["library_revision"])
    formal = '<p>Optional Lean syntax. The exact checked target is P or ¬P according to the reference decision. This certificate covers polarity, not the complete explanation, witness, repair or physical/resource interpretation.</p><p>Imports: <code>' + esc(', '.join(task["imports"])) + '</code>.</p>'
    formal += '<pre><code data-qcb-diagnostic-target>' + esc(task["nodes"][0]["target"]) + '</code></pre>'
    formal += disclosure("Fixed authored reference proof", '<pre><code>' + esc(probe["gold"]["reference_proof"]) + '</code></pre>', 'proof-' + probe["probe_id"])
    body += disclosure("Optional Lean target and polarity certificate", formal, 'formal-' + probe["probe_id"])
    provenance = '<p>Separate candidate contract; no new canonical core or Lean admission is created. Parent contract bindings:</p><ul>'
    for core in probe["parent_core_ids"]:
        provenance += '<li><a href="../../cores/' + esc(core) + '/index.html">' + esc(core) + '</a> · <code>' + esc(probe["parent_contracts"][core]) + '</code></li>'
    provenance += '</ul><p>Exact source declaration anchors:</p><ul>' + ''.join('<li><code>' + esc(node) + '</code></li>' for node in probe["source_nodes"]) + '</ul>'
    provenance += '<p>Provisional construction-band rationale: ' + esc(probe["difficulty"]["rationale"]) + ' This is not measured model difficulty.</p>'
    body += disclosure("Parent contracts and source anchors", provenance, 'parents-' + probe["probe_id"])
    if expert_index is not None:
        from website.scripts.qcb_expert import diagnostic_panel
        body += diagnostic_panel(probe["probe_id"], expert_index)
    return body + '</article>'


def diagnostic_cluster_body(packet, cluster, expert_index=None):
    rows = [p for p in packet["probes"] if p["cluster_id"] == cluster]
    pair_ids = list(dict.fromkeys(p["pair_id"] for p in rows))
    labels = DIAGNOSTIC_CLUSTERS[cluster][3]
    if len(pair_ids) != len(labels):
        raise ValueError("diagnostic contrast hierarchy needs an explicit editorial update")
    body = '<p class="qcb-status-line">Public diagnostic questions · provisional construction levels · answers and formal companions folded.</p>'
    body += section("Reading the notation", prose(DIAGNOSTIC_CLUSTERS[cluster][2]), "notation")
    number = 0
    for pair, label in zip(pair_ids, labels):
        content = ''
        for probe in rows:
            if probe["pair_id"] == pair:
                number += 1
                content += diagnostic_probe_body(probe, number, packet, expert_index)
        body += section(label, content, 'contrast-' + pair)
    return body


def publish_diagnostics(write, intro, packet, qualification, publication_commit, expert_index=None):
    manifest = diagnostic_manifest(packet, qualification, publication_commit)
    body = intro("Reason about quantum contracts", "Read each proposition, decide whether it follows from exactly the supplied assumptions, then explain your reasoning or give a precise counterexample. The mathematics is readable without Lean.")
    body += '<p><a href="../index.html">Exercise book</a> / Semantic diagnostics · <a href="../non-lean/index.html">Mathematical path</a> · <a href="../lean/index.html">Lean path</a></p>'
    body += '<p class="qcb-status-line">' + str(manifest["diagnostic_candidates"]) + ' public candidate propositions · ' + str(manifest["contrast_pairs"]) + ' contrasts · reference mathematics and optional Lean evidence.</p>'
    body += section("Attempt the question before inspecting evidence", '<ol><li>Read every assumption and convention, including dimensions and empty cases.</li><li>Decide whether the exact proposition holds. An invalid statement needs a precise witness; distinguish any repaired claim from the original.</li><li>Open the folded mathematical reference and rubric to compare the argument.</li><li>Inspect the optional Lean target to see exactly which polarity is certified.</li></ol><p>D1–D4 describe provisional construction routes, not measured model difficulty. Existing train/dev/public-test source splits stay visible. Contrasted statements are not interchangeable fresh pre/post forms.</p>', "reading")
    cards = '<div class="qcb-grid">'
    for key, (title, description, _, _) in DIAGNOSTIC_CLUSTERS.items():
        cards += '<article class="qcb-card"><h3><a href="' + key + '/index.html">' + esc(title) + '</a></h3>' + prose(description) + '<p>' + str(manifest["clusters"][key]) + ' candidate propositions</p></article>'
    body += section("Four mathematical themes", cards + '</div>', "themes")
    body += diagnostic_evidence(packet, qualification, publication_commit)
    write(HUB + "diagnostics/", "Public quantum-semantic diagnostics", body + '</div>', "Public candidate propositions about quantum assumptions, representation, composition and boundary cases; separate reference evidence, no new canonical admissions.")
    for key, (title, description, _, _) in DIAGNOSTIC_CLUSTERS.items():
        body = intro(title, description)
        body += '<p><a href="../index.html">All diagnostic themes</a> · <a href="../../non-lean/index.html">Mathematical path</a> · <a href="../../lean/index.html">Lean path</a></p>'
        body += diagnostic_cluster_body(packet, key, expert_index) + diagnostic_evidence(packet, qualification, publication_commit)
        write(HUB + "diagnostics/" + key + "/", title + " · public diagnostics", body + '</div>', description + " Public candidate questions; reference answers and exact polarity certificates are folded.")
    return manifest


def check_diagnostic_pages(root, packet, qualification, manifest, expert_index=None):
    if manifest.get("public_semantic_diagnostics") != diagnostic_manifest(packet, qualification, manifest["source_commit"]):
        raise ValueError("diagnostic projection has stale cohort, receipt, source or counting bindings")
    index = (root / HUB / "diagnostics/index.html").read_text(encoding="utf-8")
    if (diagnostic_evidence(packet, qualification, manifest["source_commit"]) not in index
            or any('href="' + key + '/index.html"' not in index for key in DIAGNOSTIC_CLUSTERS)):
        raise ValueError("diagnostic index lost its evidence binding or theme hierarchy")
    for key in DIAGNOSTIC_CLUSTERS:
        page = (root / HUB / "diagnostics" / key / "index.html").read_text(encoding="utf-8")
        if diagnostic_cluster_body(packet, key, expert_index) not in page:
            raise ValueError("diagnostic question, premises, closed answer or exact formal projection changed")
        if diagnostic_evidence(packet, qualification, manifest["source_commit"]) not in page:
            raise ValueError("diagnostic source/evidence projection changed")


def course_label(core_id):
    return COURSE_LABELS[core_id.removeprefix("qcb-core-")]


def course_cards(entries, prefix, views):
    cards = []
    for entry in entries:
        core_id = entry["core_id"]
        band = entry["difficulty"]["construction_band"]
        cards.append('<article class="qcb-card"><p class="eyebrow">' + esc(band + ' · ' + core_id.removeprefix('qcb-core-').upper()) + '</p><h3><a href="' + prefix + HUB + 'cores/' + core_id + '/index.html">' + esc(course_label(core_id)) + '</a></h3><p>' + esc(entry["difficulty"]["rationale"]) + '</p><p class="qcb-meta">' + esc(entry["split"]) + ' · ' + str(entry["topology"]["obligation_nodes"]) + ' supplied obligations</p><a href="' + prefix + HUB + 'cores/' + core_id + '/index.html#course">Inspect the course companion</a></article>')
    return '<div class="qcb-grid">' + ''.join(cards) + '</div>'


def course_panel(core, prefix, publication_commit=None):
    plan, views, _ = course_reader()
    entry = next((e for e in plan["entries"] if e["core_id"] == core["core_id"]), None)
    if not entry:
        return ""
    task = views[entry["view_id"]]["task"]
    body = '<p>This experimental companion studies the same mathematical core. Its fixed roots and authored references have been checked; it does not add a canonical Lean admission or certify the whole explanation.</p>'
    body += '<p><strong>' + esc(entry["difficulty"]["construction_band"] + ': ' + COURSE_BANDS[entry["difficulty"]["construction_band"]][0]) + '</strong>. ' + esc(entry["difficulty"]["rationale"]) + '</p>'
    body += '<p><a href="' + prefix + HUB + 'course/index.html">Follow the difficulty course</a> · <a href="' + prefix + HUB + 'reasoning/index.html">Understand these graph connections</a></p>'
    body += '<p><strong>Library shortcut:</strong> ' + esc(entry["difficulty"]["imported_shortcut"]) + '</p>'
    parents = entry["prerequisite_core_ids"]
    if parents:
        body += '<p>Suggested reading, not required theorem dependencies: ' + ', '.join('<a href="' + prefix + HUB + 'cores/' + p + '/index.html">' + esc(course_label(p)) + '</a>' for p in parents) + '.</p>'
    body += '<h3>Exact supplied obligation map</h3><p>Each row is a formal subgoal. An arrow supplies a previously established result to a later subgoal; all listed inputs are available together. This is an evaluator-supplied graph, not extracted Lean proof-term dependencies.</p><ol class="qcb-obligations">'
    for node in task["nodes"]:
        body += '<li><code>' + esc(node["id"]) + '</code><p class="qcb-meta">' + ('Inputs: ' + esc(', '.join(node['depends_on'])) if node['depends_on'] else 'No preceding supplied obligation') + (' · final root' if node['id'] == task['root_id'] else '') + '</p><pre><code>' + esc(node["target"]) + '</code></pre></li>'
    body += '</ol><p>Imports: <code>' + esc(', '.join(task['imports'])) + '</code>. The supplied route is visible in both root-only and incremental protocols. Only intermediate checking and reuse differ.</p>'
    body += '<p>Construction levels are provisional. A callable exact theorem or finite decision procedure can make an apparently deep route easy. Model difficulty, a calibrated process reward and faithful internal reasoning are not established by this graph.</p>'
    if publication_commit and re.fullmatch(r'[0-9a-f]{40}', publication_commit):
        base = REPO + '/tree/' + publication_commit + '/benchmarks/quantumcomputingbench/'
        body += '<p>Inspect the <a href="' + base + 'tracks/lean/curriculum/course-v3.json">course manifest</a> and the <a href="' + base + 'reports/lean-course-v1">first</a>, <a href="' + base + 'reports/lean-course-v2">second</a> and <a href="' + base + 'reports/lean-course-v3">third cohort evidence</a>. Receipts preserve their actual execution commits and scope; publishing this page does not rerun those proofs.</p>'
    return disclosure("Guided course and optional Lean obligations", body, "course")


def public_catalog(catalog):
    """Display agent identities as identities, never as apparent host paths.

    The catalog hash still binds the unmodified internal registry. This explicit,
    reversible display projection does not change the identities used by the
    independent-review checks, and does not exempt paths from the leak scanner.
    """
    projected = deepcopy(catalog)
    for collection in ("cores", "withheld_cores"):
        for core in projected.get(collection, []):
            identity = core.get("author_identity")
            if isinstance(identity, str) and re.fullmatch(r"/root(?:/[a-z0-9_]+)*", identity):
                core["author_identity"] = "agent-task:" + identity[1:]
    projected["public_projection"] = {
        "schema_version": "qcb.public_catalog_projection.v1",
        "catalog_hash_binds": "unmodified_internal_registry",
        "author_identity_encoding": "agent-task:root[/task...] represents /root[/task...]; other identities are unchanged",
    }
    return projected


def formal_warmups():
    """Bind semantic review to exact fixed references, without admitting new cores."""
    review = read_json(B / "reports/textbook-v1/formal-view-review.json")
    for binding in review["file_bindings"]:
        if text_sha(ROOT / binding["path"]) != binding["sha256_lf"]:
            raise ValueError("formal view review is stale: " + binding["path"])
    raw = read_json(B / "data/authored/repairs-v3.json")
    records = raw if isinstance(raw, list) else raw["items"]
    by_key = {r["key"]: r for r in records}
    selected = []
    for row in review["reviews"]:
        item = by_key[row["key"]]
        if digest(item) != row["raw_record_digest"] or row["verdict"] != "accept":
            raise ValueError("formal warmup review does not match the exact record")
        selected.append((item, row))
    return selected


def graph_link(node, prefix, graph, live_ids):
    if node in live_ids:
        href = prefix + "lean-graph/index.html?focus=" + quote(node, safe="")
        return '<a data-qcb-graph href="' + esc(href) + '">' + esc(graph[node].get("label", node)) + '</a>'
    # A frozen planned/curated identity may not be a live declaration identity.
    return '<span>' + esc(graph[node].get("label", node)) + ' <small>(frozen curriculum anchor; see graph registry)</small></span>'


def source_list(item):
    rows = []
    for source in item.get("source_refs", []):
        path = source.get("path", "")
        relative = PurePosixPath(path)
        if path and not relative.is_absolute() and ".." not in relative.parts and "\\" not in path:
            href = REPO + "/blob/" + SOURCE_COMMIT + "/" + quote(path, safe="/")
            label = '<a href="' + esc(href) + '">' + esc(path) + '</a>'
        else:
            label = esc(path or "Source record")
        rows.append('<li>' + label + prose(source.get("anchor", "")) +
                    '<small>Source SHA-256: <code>' + esc(source.get("sha256", "not recorded")) +
                    '</code> · ' + esc(source.get("license", "license not recorded")) + '</small></li>')
    for source in item.get("primary_sources", []):
        url = source.get("url", "")
        label = source.get("title", source.get("id", "Primary source"))
        if urlsplit(url).scheme in {"http", "https"}:
            label = '<a href="' + esc(url) + '">' + esc(label) + '</a>'
        else:
            label = esc(label)
        rows.append('<li>' + label + prose(source.get("anchor", source.get("section", ""))) + '</li>')
    return '<ul class="qcb-sources">' + "".join(rows) + '</ul>'


def core_body(core, item, catalog, graph, live_ids, prefix, publication_commit=None, expert_index=None):
    from website.scripts.qcb_math import question_equations
    part = next(p for p in catalog["parts"] if p["id"] == core["part"])
    parent = prefix + HUB + "non-lean/" + part["id"] + "/" + core["topic"] + "/index.html"
    body = '<article class="qcb-reader"><p class="qcb-breadcrumb"><a href="' + esc(parent) + '">' + esc(part["title"]) + ' / ' + esc(title_of(core["topic"])) + '</a></p>'
    body += '<p class="eyebrow">' + esc(title_of(core["topic"])) + '</p><h1>Exercise ' + esc(core["core_id"].removeprefix("qcb-core-").upper()) + '</h1>'
    body += '<p class="qcb-meta">' + esc(item["difficulty"]["level"]) + ' · ' + esc(item["task_kind"]) + ' · ' + esc(core["split"]) + '</p>'
    if core["core_id"].removeprefix("qcb-core-") in COURSE_LABELS:
        body += '<p class="qcb-deck">' + esc(course_label(core["core_id"])) + '</p><p class="qcb-meta"><a href="' + prefix + HUB + 'course/index.html">Guided course</a> · <a href="#course">Optional course companion</a></p>'
    review_status = ('Explicit question version ' + str(core["question_version"]) + ' with distinct contract-change review; the predecessor question is not equivalent current gold. Core, family and split are retained.' if core.get("question_successor") else
                    'Additive answer successor with distinct content-bound review; historical rejected answer retained only for audit.' if core.get("textbook_successor") else
                    'Current content-bound mathematical second pass accepted.' if core.get("editorial_second_pass") == "content_bound_review_accepted" else
                    'Inherited reviews only; a current content-bound mathematical second pass remains pending.')
    body += '<p class="qcb-meta">Source relation: ' + esc(core["evidence_relation"].replace("_", " ")) + '. Review details are folded under Sources and provenance.</p>'
    premises = ''.join('<ul data-qcb-active-' + field + '>' + ''.join(
        '<li>' + prose(s) + '</li>' for s in item[field]) + '</ul>'
        for field in ('assumptions', 'conventions'))
    body += section("Assumptions and conventions", premises, "assumptions")
    if core.get("question_successor"):
        body += '<p class="qcb-boundary" data-qcb-question-version="' + esc(core["question_version"]) + '">This question explicitly revises its historical contract. A Lean companion must bind the current contract hash, not the predecessor hash. This is one reserved core, not two exercises.</p>'
        if "conventions" in core["question_successor"]["changed_contract_fields"]:
            body += '<p class="qcb-boundary" data-qcb-convention-revision="2">The conventions above are the current premises. The superseded convention list is retained in the revision audit below, not as active assumptions. A question may quote a historical claim to assess or refute it.</p>'
        if "assumptions" in core["question_successor"]["changed_contract_fields"]:
            body += '<p class="qcb-boundary" data-qcb-assumption-revision="2">The assumptions above are the current premises. The superseded assumptions are retained in the folded historical audit, not as current premises. This is an explicit correction, not an equivalent restatement.</p>'
    body += section("Question", prose(item["question"]) + question_equations(core["core_id"], item["question"]), "question")
    roadmap = '<ol>' + "".join('<li>' + prose(s["claim"]) + '</li>' for s in item["semantic_steps"]) + '</ol>'
    body += disclosure("Hint: mathematical route", prose(core["title"]) + roadmap, "hint")
    body += disclosure("Reference solution", prose(item["reference_answer"]), "solution")
    rubric = '<ol>' + "".join('<li>' + prose(r["criterion"]) + ' <small>(' + esc(r["weight"]) + ' weight)</small></li>' for r in item["rubric"]) + '</ol>'
    body += disclosure("Assessment rubric", rubric, "rubric")
    body += course_panel(core, prefix, publication_commit)
    if expert_index is not None:
        from website.scripts.qcb_expert import expert_panel, graph_summary
        body += section("Location in the Lean graph", graph_summary(core["core_id"], expert_index, prefix), "graph")
        body += expert_panel(core["core_id"], expert_index, prefix)
    else:
        body += section("Graph-grounded prerequisites", '<p>Support/source anchors:</p><ul>' + "".join('<li>' + graph_link(n, prefix, graph, live_ids) + '</li>' for n in dict.fromkeys(core["target_nodes"] + core["supporting_nodes"])) + '</ul>', "graph")
    formal = core["views"].get("lean")
    if formal:
        formal_body = '<p class="qcb-boundary">Exact formal conclusion: independently decoded and compared with this question, then checked with the fixed reference in Lean. This is a library-lemma application, not a deep proof-search result. The kernel does not certify every sentence of the natural-language explanation.</p>'
        formal_body += '<pre><code>' + esc(json.dumps(formal["formal_context"], ensure_ascii=False, indent=2)) + '</code></pre>'
        formal_body += disclosure("Fixed reference proof", '<pre><code>' + esc(formal["reference_proof"]) + '</code></pre>', "lean-reference")
        formal_body += prose(formal["boundary"]) + '<p>Execution class: trusted local reference; not isolated model-output evaluation. The same core, family and split apply to both views.</p>'
        if publication_commit and re.fullmatch(r'[0-9a-f]{40}', publication_commit):
            formal_body += '<p>Source-blind reconstruction, distinct comparison and actual reference receipts: <a href="' + REPO + '/tree/' + publication_commit + '/benchmarks/quantumcomputingbench/' + esc(formal["evidence_directory"]) + '">inspect the evidence records</a>.</p>'
    else:
        formal_body = '<p>No aligned Lean view has been admitted for this native core in this textbook checkpoint. This is not a claim that the underlying mathematics lacks a formal proof. Contributions must preserve this exact target contract and split.</p>'
    formal_body += '<p><a href="' + prefix + HUB + 'lean/index.html">Read the Lean track and existing diagnostic warmups</a></p>'
    body += disclosure("Lean view and evidence boundary", formal_body, "lean")
    body += disclosure("Sources and provenance", '<p>' + esc(review_status) + ' No new Lean verification is claimed for this NL view.</p>' + source_list(item) + '<p>Contract: <code>' + esc(core["contract_hash"]) + '</code></p><p>Item digest: <code>' + esc(core["item_digest"]) + '</code></p><p>Graph snapshot: <code>' + esc(core["snapshot_id"]) + '</code></p><p>Authored support steps: ' + str(core["semantic_steps"]) + '. This is not measured graph distance or model difficulty.</p>', "sources")
    if core.get("textbook_successor"):
        body += disclosure("Answer revision lineage", prose(json.dumps(core["textbook_successor"], indent=2)), "revision")
    if core.get("question_successor"):
        lineage = core["question_successor"]
        revision_body = ""
        if "conventions" in lineage["changed_contract_fields"]:
            for title, key in (("Historical conventions (audit only)", "original_conventions"),
                               ("Current conventions", "current_conventions")):
                revision_body += '<h3>' + title + '</h3><ul data-qcb-' + key + '>' + ''.join(
                    '<li>' + prose(s) + '</li>' for s in lineage[key]) + '</ul>'
        if "assumptions" in lineage["changed_contract_fields"]:
            for title, key in (("Historical assumptions (audit only)", "original_assumptions"),
                               ("Current assumptions", "current_assumptions")):
                revision_body += '<h3>' + title + '</h3><ul data-qcb-' + key + '>' + ''.join(
                    '<li>' + prose(s) + '</li>' for s in lineage[key]) + '</ul>'
        body += disclosure("Question revision lineage", revision_body + prose(json.dumps(lineage, indent=2)), "revision")
    return body + '</article>'


def exercise_cards(cores, prefix, items, track="non-lean"):
    content = '<div class="qcb-grid">'
    for c in cores:
        href = prefix + HUB + "cores/" + c["core_id"] + "/index.html"
        if track == "lean":
            href += "#lean"
        question = items[c["core_id"]]["question"]
        preview = question if len(question) <= 220 else question[:220] + "…"
        label = (' · aligned Lean reference checked' if "lean" in c["views"] else ' · formal view pending') if track == "lean" else ''
        content += '<article class="qcb-card" data-qcb-card data-qcb-search="' + esc(c["core_id"] + ' ' + c["topic"] + ' ' + c["evidence_relation"] + ' ' + question) + '"><p class="qcb-meta">' + esc(c["split"]) + ' · ' + esc(items[c["core_id"]]["task_kind"]) + esc(label) + '</p><h3><a href="' + esc(href) + '">Exercise ' + esc(c["core_id"].removeprefix("qcb-core-").upper()) + '</a></h3>' + prose(preview) + '<p>' + esc(c["evidence_relation"].replace("_", " ")) + '</p></article>'
    return content + '</div>'


def filters():
    return '<div class="qcb-filter" data-qcb-controls hidden><label for="qcb-query">Find an exercise (questions and topics, not solutions)</label><input id="qcb-query" data-qcb-query type="search" autocomplete="off"><p data-qcb-count role="status" aria-live="polite"></p></div>'


def publish_course(write, intro, plan, views, report):
    """Project the checked course without creating new question identities."""
    body = intro("A course in connected quantum reasoning", "Start with mathematical contracts, then build local derivations, combine interfaces and tackle whole parameterized families. You can follow every question and solution without reading Lean syntax.")
    body += '<p><a href="../index.html">Exercise book</a> / Guided course · <a href="../reasoning/index.html">How reasoning graphs work</a></p>'
    body += '<p>This course provides ' + str(report["distinct_shared_cores"]) + ' experimental companions to existing questions. Each question has one core ID, one family and one split across its natural-language and formal views. The course does not increase the question count or change canonical Lean admissions.</p>'
    body += '<ol class="qcb-ladder">' + ''.join('<li><a href="' + b.lower() + '/index.html"><span class="qcb-level">' + b + '</span><strong>' + esc(label) + '</strong></a><p>' + esc(description) + '</p></li>' for b, (label, description) in COURSE_BANDS.items()) + '</ol>'
    body += section("How to use a level", '<ol><li>Read the assumptions and conventions, then attempt the mathematical question.</li><li>Open the hint only when needed. Compare your reasoning with the folded solution and rubric.</li><li>Inspect the optional course companion to see the exact supplied subgoals and their inputs.</li><li>Keep the source relation and shortcut disclosure in view: calling an existing theorem tests a different skill from constructing its proof.</li></ol><p>D1–D4 are provisional assessments of the disclosed construction route, not measured model difficulty. D0 is a reading facet of these same cores. We do not assign course levels to unannotated questions elsewhere in the book.</p>', "method")
    for band in list(COURSE_BANDS)[1:]:
        entries = [e for e in plan["entries"] if e["difficulty"]["construction_band"] == band]
        body += section(band + ' · ' + COURSE_BANDS[band][0], '<p>' + str(len(entries)) + ' existing shared cores</p>' + course_cards(entries, '../../', views), band.lower())
    body += '<p class="qcb-boundary">Public authored reference tasks: exact formal roots have bounded reference evidence; whole-question exposition and required proof methods have only partial formal coverage. No model baseline, calibrated process reward or isolated generated-proof execution is claimed. <a href="../evidence/index.html">Read the release boundaries</a>.</p>'
    write(HUB + "course/", "Guided reasoning course", body + '</div>', "A provisional D0–D4 reading and construction course over existing shared quantum-computing questions.")
    for band, (label, description) in COURSE_BANDS.items():
        entries = plan["entries"] if band == "D0" else [e for e in plan["entries"] if e["difficulty"]["construction_band"] == band]
        body = intro(band + ' · ' + label, description)
        body += '<p><a href="../index.html">All course levels</a> · <a href="../../reasoning/index.html">Reasoning graph guide</a></p>'
        if band == "D0":
            body += section("Before opening any solution", '<ol><li>State what the objects represent: amplitudes, operators, polynomials or classical basis labels.</li><li>List the dimensions, register order, normalization and clean-work assumptions.</li><li>Separate the requested conclusion from stronger claims: unitarity, a projected block and auxiliary cleanup are different properties.</li><li>Find the linked source anchors. Identify what is compiled, what is source-backed and what is still planned.</li></ol><p>Apply these questions to any core below. These are knowledge and statement-understanding facets, not independently admitted benchmark items.</p>', "reading-checklist")
        else:
            body += '<p>Suggested entry points grouped by the reference construction route. Every card opens the original mathematical question; solutions and formal details remain folded.</p>'
        body += course_cards(entries, '../../../', views)
        body += '<p class="qcb-meta">Levels are not graph-distance scores. Imported theorems, supplied subgoals, model strength and execution budgets can change solving difficulty. Existing splits remain fixed.</p>'
        write(HUB + 'course/' + band.lower() + '/', band + ' · ' + label, body + '</div>', description)

    body = intro("How a connection becomes a reasoning question", "A library graph helps us choose related mathematical ingredients. A question then specifies what must be understood or proved, under explicit assumptions. You do not need Lean to follow these examples.")
    body += '<p><a href="../index.html">Exercise book</a> / Reasoning guide · <a href="../course/index.html">Follow the guided course</a></p>'
    body += section("Read the edge before counting it", '<dl class="qcb-legend"><dt>Library node</dt><dd>A definition, theorem or documented interface. Its evidence says whether it is compiled, source-backed or planned.</dd><dt>Pedagogical prerequisite</dt><dd>Suggested earlier reading, not a claim of theorem dependency.</dd><dt>Supplied obligation arrow</dt><dd>An earlier subgoal is available to a later subgoal in a specific task. At an AND join, all listed inputs are supplied together.</dd><dt>Import or conceptual relationship</dt><dd>A module import gives availability. An upper-level Functor Hypergraph relationship records a conceptual or compositional interface. Neither alone proves the requested conclusion.</dd></dl><p>The examples below describe supplied course obligations and their mathematical routes, not extracted Lean proof-term dependencies. More nodes or edges need not mean harder reasoning.</p>', "legend")
    examples = [
        ("single-root", "One root: understand the interface", "SP009", "A real core has orthonormal rows. Reinterpret its entries as complex numbers and orient them as output rows and input columns. The task asks for the corresponding isometry condition. A single formal root can test a subtle representation convention.", '<div class="qcb-flow-step">Real row condition and stated orientation → complex isometry target</div>'),
        ("chain", "A chain: justify the next transformation", "BE111", "A permutation matrix selects one surviving term in a matrix-product sum. Use that row-action identity to determine which order of matrix multiplication implements a chronological pair of permutations. This tests a link between finite-sum algebra and circuit composition, rather than two unrelated facts.", '<div class="qcb-flow-step">Surviving finite-sum term</div><div class="qcb-flow-arrow" aria-hidden="true">↓</div><div class="qcb-flow-step">Matrix action and chronological composition</div>'),
        ("and-join", "An AND join: retain both ingredients", "BE106", "A real rotation is unitary for every angle. Separately, a cosine entry can represent a requested real amplitude only in [−1,1]. With an angle function satisfying the stipulated inverse-cosine relation on that interval, combine unitarity and the readout-range fact. Unitarity alone does not establish the requested readout.", '<div class="qcb-flow-row"><div class="qcb-flow-step">Rotation unitarity</div><div class="qcb-flow-step">Readout range</div></div><div class="qcb-flow-arrow" aria-hidden="true">↓ both inputs</div><div class="qcb-flow-step">Combined unitarity and exact readout-domain conclusion</div>'),
    ]
    equations = {
        'SP009': r'\(C_{(b,r),a}=A_{a,(b,r)}\), with \(AA^{\mathsf T}=I\) giving \(C^\dagger C=I\) for real entries.',
        'BE111': r'\(\sum_k P(e)_{r,k}O_{k,c}=O_{e^{-1}(r),c}\), hence \(P(\mathrm{second})P(\mathrm{first})=P(\mathrm{second}\circ\mathrm{first})\).',
        'BE106': r'\(R(\theta)=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}\), with \(R(\theta)^\dagger R(\theta)=I\); exact clean-entry readout is a separate condition.',
    }
    for anchor, title, short_id, explanation, diagram in examples:
        core_id = 'qcb-core-' + short_id[:2].lower() + '-' + short_id[2:]
        body += section(title, '<p>' + esc(explanation) + '</p>' + prose(equations[short_id]) + '<figure class="qcb-flow">' + diagram + '<figcaption>Mathematical reading of the supplied task. Ambient assumptions still apply.</figcaption></figure><p><a href="../cores/' + core_id + '/index.html">Try ' + short_id + ': ' + esc(course_label(core_id)) + '</a></p>', anchor)
    body += section("A shared provider and a reconvergent diamond", '<p>In SP104, two polynomials have degree at most 2k+1 and matching derivatives through order k at −1 and 0. A generic result connects matching derivatives at a point a with divisibility of their difference by (X−a)^(k+1). Reuse it at both endpoints. The branches join with a separate coprimality fact; a separate degree argument completes the proof.</p><p>For \\(d=p-q\\), the product \\((X+1)^{k+1}X^{k+1}\\) has degree \\(2k+2\\), while the difference has degree at most \\(2k+1\\). Product divisibility therefore forces \\(d=0\\).</p><figure class="qcb-flow"><div class="qcb-flow-step">Shared provider: derivatives at a ↔ divisibility by (X−a)^(k+1)</div><div class="qcb-flow-arrow" aria-hidden="true">↓ reused independently</div><div class="qcb-flow-row"><div class="qcb-flow-step">Left endpoint: (X+1)^(k+1) divides p−q</div><div class="qcb-flow-step">Right endpoint: X^(k+1) divides p−q</div><div class="qcb-flow-step">Separate input: endpoint factors are coprime</div></div><div class="qcb-flow-arrow" aria-hidden="true">↓ all three inputs</div><div class="qcb-flow-step">Their product divides p−q</div><div class="qcb-flow-row"><div class="qcb-flow-step">Separate input: product degree is 2k+2 → a divisible difference of degree ≤2k+1 must vanish</div></div><div class="qcb-flow-arrow" aria-hidden="true">↓ combine divisibility and the vanishing argument</div><div class="qcb-flow-step">Final root: p = q, using both endpoint data and both degree bounds</div><figcaption>The endpoint branches share a provider and reconverge. Coprimality, product degree and the degree-to-vanishing argument are retained as side inputs. The exact eight-obligation map is available in the optional course panel.</figcaption></figure><p>This tests reuse, separate endpoint reasoning, premise selection and a global degree budget. Every graph combination is not automatically a meaningful new question.</p><p><a href="../cores/qcb-core-sp-104/index.html">Try SP104: two-point polynomial interpolation</a> · <a href="../cores/qcb-core-sp-104/index.html#course">Inspect every supplied obligation</a></p>', "diamond")
    body += section("From coverage map to useful evaluation", '<p>We aim to sample knowledge, local derivations, counterexamples, compositions and parameterized arguments across the library. Shared core identities prevent natural-language and Lean variants from being counted twice; shared contracts preserve assumptions and splits. Reusable interfaces make deeper checks practical without rebuilding lower-level mathematics for every task.</p><p>The course does not yet cover the entire library. Source-only and planned nodes guide future work but are not verified gold. A passed Lean root certifies its exact proposition under permitted assumptions; it does not grade every explanatory sentence or establish that an intermediate step helped a model.</p><p><a href="../non-lean/index.html">Browse by subject</a> · <a href="../course/index.html">Browse by construction level</a> · <a href="../evidence/index.html">Inspect current evidence</a></p>', "coverage")
    write(HUB + "reasoning/", "How reasoning graphs work", body + '</div>', "A mathematical guide to single nodes, chains, AND joins and shared-provider reasoning, with exact evidence boundaries.")


def publish(root):
    from qcb_bench_runtime import build_registry, write_downloads
    from qcb_nonlean_workbook import check_publication_sources, load_workbook
    from qcb_nonlean_workbook import write_downloads as write_workbook_downloads

    from website.scripts import build_site as site
    from website.scripts.qcb_benchmark_center import publish_center
    from website.scripts.qcb_expert import build_expert_index, publish_expert
    from website.scripts.qcb_workbook_reader import publish_workbook
    from website.scripts.research_atlas import patch_navigation
    root = root.resolve()
    catalog, items, graph = load_catalog()
    native_lean_count = sum("lean" in c["views"] for c in catalog["cores"])
    course_plan, course_views, course_report = course_reader()
    # Fail before any output mutation if the actual new reference receipt is
    # absent or stale. Historical course evidence cannot qualify these probes.
    diagnostic_packet, diagnostic_qualification = diagnostic_reader()
    notation_contract = math_notation_contract(catalog["catalog_hash"])
    report = read_json(root / "build-report.json")
    context = site.git_context()
    if not report["leanGate"].get("passed") or report["leanGate"].get("commit") != context["commit"]:
        raise ValueError("textbook publication requires the current passed repository Lean gate")
    graph_path = root / "data/lean-graph.json"
    graph_hash = hashlib.sha256(graph_path.read_bytes()).hexdigest()
    live_ids = {n["id"] for n in read_json(graph_path)["nodes"]}
    data_dir = root / "data/quantumcomputingbench"
    registry = build_registry()
    workbook = load_workbook()
    check_publication_sources(workbook, context['commit'])
    write_workbook_downloads(data_dir / 'nonlean-workbook', workbook)
    runtime_environment = environment_record(registry)
    write_json(data_dir / "environment-smoke.json", runtime_environment)
    publication_commit = context["commit"] if re.fullmatch(r'[0-9a-f]{40}', context["commit"]) else None
    expert_index = build_expert_index(catalog, items, graph, live_ids, publication_commit,
        snapshot=read_json(B / "manifests/release-v3/snapshot.json"),
        course_plan=course_plan, course_views=course_views, diagnostics=diagnostic_packet)
    write_json(data_dir / "expert-index.json", expert_index)
    # The export command preserves user artifacts; the site publisher materializes
    # its deterministic outputs through a fresh staging directory for idempotence.
    with tempfile.TemporaryDirectory(prefix="qcb-reader-downloads-") as staging:
        staged_downloads = Path(staging) / "downloads"
        write_downloads(staged_downloads, registry=registry)
        runtime_dir = data_dir / "runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        for exported in staged_downloads.iterdir():
            if not exported.is_file():
                raise ValueError("unexpected runtime download directory")
            shutil.copyfile(exported, runtime_dir / exported.name)
    write_json(data_dir / "cores.json", public_catalog(catalog))
    write_json(data_dir / "reader-items.json", {"schema_version": "qcb.current_reader_export.v1", "stable": False,
        "catalog_hash": catalog["catalog_hash"], "use": "Open reader views; not a stable training/scoring release.", "items": [public_reader_item(i) for i in items.values()]})
    for name in ("quantumcomputingbench.css", "quantumcomputingbench.js", "qcb-math.css", "qcb-expert.css", "qcb-expert.js"):
        shutil.copyfile(ROOT / "website/static" / name, root / "static" / name)
    entries, routes = [], []

    def write(route, title, body, description, searchable=True):
        site.write_page(root, route, site.page_template(
            title=title, route=route, current=route, body=body,
            coverage=report["coverage"], gate=report["leanGate"], context=context,
            description=description, extra_styles=("static/quantumcomputingbench.css", "static/qcb-math.css", "static/qcb-expert.css"),
            extra_scripts=("static/quantumcomputingbench.js", "static/qcb-expert.js")))
        routes.append(route + "index.html")
        if searchable:
            entries.append({"type": "page", "kind": "quantumcomputingbench", "title": title,
                            "summary": description, "url": route + "index.html"})

    def intro(title, subtitle):
        return '<div class="qcb-reader"><p class="eyebrow">QuantumComputingBench · graph-grounded exercise book</p><h1>' + esc(title) + '</h1>' + prose(subtitle)

    body = intro("QuantumComputingBench", "Study quantum mathematics, prepare training and evaluation tasks, and inspect the Lean graph behind every question.")
    body += '<div class="qcb-grid qcb-role-paths"><article class="qcb-card"><p class="eyebrow">For readers</p><h2><a href="non-lean/index.html">Read and solve</a></h2><p>Follow the subject hierarchy or difficulty course. Read compiled mathematics and open solutions when ready.</p></article><article class="qcb-card"><p class="eyebrow">For model builders</p><h2><a href="run/index.html">Train and evaluate</a></h2><p>Get task-bound inputs, train-only supervision, portable environments and scoring tools.</p></article><article class="qcb-card"><p class="eyebrow">For domain experts</p><h2><a href="expert/index.html">Review the graph</a></h2><p>Locate targets and prerequisites, inspect source versions, and review question and proof evidence.</p></article></div>'
    body += '<nav class="qcb-jump" aria-label="Exercise book contents"><a href="#start">Start reading</a><a href="#library">Why a library graph?</a><a href="#progression">Choose a level</a><a href="#parts">Browse subjects</a></nav>'
    body += '<div class="qcb-stats" aria-label="Distinct inventories"><div><strong>' + str(len(catalog["cores"])) + '</strong><span>shared mathematical core IDs</span></div><div><strong>' + str(native_lean_count) + '</strong><span>canonical native Lean views</span></div><div><strong>' + str(course_report["distinct_shared_cores"]) + '</strong><span>experimental course companions</span></div></div>'
    body += '<p class="qcb-meta">The course reuses existing cores, including the canonical formal cores. Natural-language and Lean versions are views of the same question, not extra questions.</p>'
    body += section("Choose your reading path", '<div class="qcb-grid"><article class="qcb-card"><p class="eyebrow">No Lean needed</p><h3><a href="non-lean/index.html">Explore the mathematics</a></h3><p>Read definitions, attempt a question, then open its hint, solution and rubric. Browse by subject and follow the source anchors.</p></article><article class="qcb-card"><p class="eyebrow">A guided progression</p><h3><a href="course/index.html">Build your reasoning skills</a></h3><p>Move from assumptions and local calculations to interface composition, induction and global arguments.</p></article><article class="qcb-card"><p class="eyebrow">Optional formal companion</p><h3><a href="lean/index.html">Inspect precise proof tasks</a></h3><p>Compare exact formal conclusions and supplied subgoals. Read the mathematics first; no installation is needed to inspect a task.</p></article></div>', "start")
    body += section("Test the exact assumptions", '<p><a href="diagnostics/index.html">Explore ' + str(len(diagnostic_packet["probes"])) + ' public semantic candidate diagnostics</a> organized by mass and isometry, marginal amplitudes, controlled permutations and endpoint derivatives. Read the ordinary mathematics first; reference answers, rubrics and optional Lean certificates are folded. This separate public reference pilot adds no canonical core, native Lean admission or course companion.</p>', "diagnostics")
    body += section('Connect the mathematical ingredients', '<p><a href="non-lean/workbook/index.html">Open the supplementary mathematics workbook</a>: twelve reviewed expositions and candidate problems about normalization, coherent implementations, tensor structure and polynomial sampling, organized by subject and D2–D4 routes. Existing-core expositions and unassigned targets remain distinct from canonical counts and scored splits.</p>', 'workbook')
    body += section("A library makes the questions connect", '<p>QuantumComputinglib supplies shared definitions, reusable lemmas and explicit mathematical interfaces. A state-preparation question and a block-encoding question can therefore use the same conventions for norms, registers, matrices and composition. We can ask about an individual fact, a derivation between facts, or a construction combining several ingredients.</p><div class="qcb-grid"><article class="qcb-card"><h3>Breadth: what do you know?</h3><p>Objects and definitions, assumptions, boundary cases, representations and the meaning of a quantum construction.</p></article><article class="qcb-card"><h3>Depth: what can you connect?</h3><p>Local algebra, dependencies between lemmas, reuse of a common result, and conclusions requiring several premises together.</p></article><article class="qcb-card"><h3>Precision: what is actually checked?</h3><p>Linked sources expose the contract. A qualified Lean root checks one exact proposition; explanatory prose and resource claims still need their own review.</p></article></div><p><a href="reasoning/index.html">See how a graph connection becomes a reasoning question →</a></p><p class="qcb-meta">A graph is a coverage map, not a guarantee of exhaustive questions. Planned nodes are a roadmap; source-backed material and compiled declarations carry different evidence.</p>', "library")
    body += section("From understanding to construction", '<p>Choose a provisional construction level. These levels describe the guided course route, not measured model performance or the number of graph nodes.</p><ol class="qcb-ladder">' + ''.join('<li><a href="course/' + band.lower() + '/index.html"><span class="qcb-level">' + band + '</span><strong>' + esc(label) + '</strong></a><p>' + esc(description) + '</p></li>' for band, (label, description) in COURSE_BANDS.items()) + '</ol>', "progression")
    body += section("Shared foundations and four subject areas", "".join('<article class="qcb-part"><p class="eyebrow">' + ('Shared foundations' if p['id'] == 'foundations' else 'Subject area') + '</p><h3><a href="non-lean/' + p["id"] + '/index.html">' + esc(p["title"]) + '</a></h3>' + prose(p["summary"]) + '<p>' + str(sum(c["part"] == p["id"] for c in catalog["cores"])) + ' shared cores · ' + str(len(p["topics"])) + ' topics' + (' · source-backed / planned formal frontier' if p['id'] in ('quantum-information', 'scientific-computing') else '') + '</p></article>' for p in catalog["parts"]), "parts")
    body += '<p class="qcb-boundary">Open textbook edition in progress, not a stable benchmark release. Global semantic deduplication and fresh editorial review remain incomplete. Public solutions support learning and diagnostics; they are not a hidden evaluation set. <a href="evidence/index.html">Inspect the evidence boundaries</a>.</p>'
    body += section("Read, solve, then inspect", '<ol><li>Choose a part and topic. Check dimensions, normalization, phase and resource conventions first.</li><li>Attempt the question before opening the hint or solution.</li><li>Follow exact graph/source anchors. Source-backed and planned material are visibly different evidence classes.</li><li>Use the Lean path to contribute a matching formal view, not another copy of the same question.</li></ol><p><a href="contribute/index.html">Contributor tracks and compatibility contract</a> · <a href="evidence/index.html">Release boundaries and current acceptance gates</a></p>', "reading")
    write(HUB, "QuantumComputingBench exercise book", body + '</div>', "Five-part graph-grounded quantum-computing exercise book with non-Lean and Lean companion paths.")
    publish_course(write, intro, course_plan, course_views, course_report)
    diagnostic_report = publish_diagnostics(write, intro, diagnostic_packet, diagnostic_qualification, context["commit"], expert_index)
    expert_report = publish_expert(write, intro, expert_index)
    benchmark_center = publish_center(write, intro, catalog, registry, context["commit"], runtime_environment)
    workbook_start = len(routes)
    workbook_report = publish_workbook(write, intro, workbook, graph, live_ids, context['commit'])
    workbook_report['routes'] = routes[workbook_start:]
    for track in TRACKS:
        prefix = "../../"
        is_lean = track == "lean"
        body = intro("Lean companion" if is_lean else "Mathematical exercise book", "The same five-part curriculum, with no duplicate mathematical core counting. " + ("A source-supported NL answer is not automatically a verified formal view. Admitted views and remaining formalization work are labeled separately." if is_lean else "Read and solve substantial quantum-computing problems without learning Lean syntax."))
        if is_lean:
            body += '<p class="qcb-boundary">' + str(native_lean_count) + ' admitted native Lean views in this checkpoint. These check exact conclusions by library-lemma application, not deep proof synthesis or the full NL explanation. The three corrected-v3 reference warmups are separate legacy diagnostics, not additions to the native count. Trusted local checking does not establish isolated model-output evaluation.</p><p><a href="warmups/index.html">Open the three semantic-audited API warmups</a></p>'
            body += '<p><a href="../course/index.html">Explore the ' + str(course_report["distinct_shared_cores"]) + ' experimental course companions</a> for supplied proof-obligation graphs, construction levels and shortcut disclosures. These overlap existing cores and remain separate from canonical formal admission.</p>'
            admitted = [c for c in catalog["cores"] if "lean" in c["views"]]
            if admitted:
                body += section("Aligned native formal views", exercise_cards(admitted, prefix, items, track), "native-views")
        body += '<p><a href="../course/index.html">Choose a difficulty level</a> · <a href="../reasoning/index.html">Read the reasoning-graph guide</a></p>'
        if not is_lean:
            body += '<p><a href="workbook/index.html">Supplementary mathematics workbook</a> · normalization, coherence, tensor structure and polynomial samples; twelve additional expositions/candidates with separate counting and split boundaries.</p>'
        body += '<p><a href="../diagnostics/index.html">Try the public semantic reference pilot</a>: ' + str(len(diagnostic_packet["probes"])) + ' candidate propositions with folded answers and polarity-only Lean evidence; separate from canonical admissions and course views.</p>'
        body += '<div class="qcb-grid">' + "".join('<article class="qcb-card"><h2><a href="' + p["id"] + '/index.html">' + esc(p["title"]) + '</a></h2>' + prose(p["summary"]) + '</article>' for p in catalog["parts"]) + '</div>'
        write(HUB + track + "/", "Lean companion" if is_lean else "Non-Lean exercise book", body + '</div>', "Shared curriculum and exact evidence boundaries for the " + track + " track.")
        for part in catalog["parts"]:
            body = intro(part["title"], part["summary"])
            body += '<p><a href="../index.html">Back to the ' + track + ' reader path</a></p><ol class="qcb-topic-list">' + "".join('<li><a href="' + topic + '/index.html">' + esc(title_of(topic)) + '</a> <small>(' + str(sum(c["topic"] == topic for c in catalog["cores"])) + ' shared cores' + (', ' + str(sum(c["topic"] == topic and "lean" in c["views"] for c in catalog["cores"])) + ' aligned Lean views' if is_lean else '') + ')</small></li>' for topic in part["topics"]) + '</ol>'
            write(HUB + track + "/" + part["id"] + "/", part["title"] + " · " + track, body + '</div>', part["summary"])
            for topic in part["topics"]:
                rows = [c for c in catalog["cores"] if c["topic"] == topic]
                body = intro(title_of(topic), part["summary"])
                if topic.startswith("planned_"):
                    body += '<p class="qcb-boundary">Source-backed / planned formal frontier. These questions do not establish compiled Lean closure for this topic.</p>'
                body += '<p><a href="../index.html">Back to ' + esc(part["title"]) + '</a></p>'
                if is_lean:
                    body += '<p class="qcb-boundary">These links open the shared core\'s formal companion panel. Each card distinguishes admitted fixed-reference views from pending formalization. Preserve the exact core contract and split; a formal view is not another core.</p>'
                body += filters() + exercise_cards(rows, "../../../../", items, track)
                write(HUB + track + "/" + part["id"] + "/" + topic + "/", title_of(topic) + " · " + track, body + '</div>', "Graph-grounded " + title_of(topic) + " questions; shared targets for both reader paths.")
    for core in catalog["cores"]:
        title = title_of(core["topic"]) + " · Exercise " + core["core_id"].removeprefix("qcb-core-").upper()
        content = core_body(core, items[core["core_id"]], catalog, graph, live_ids, "../../../", context["commit"], expert_index)
        extras = [e for e in workbook['entries'] if e['packet']['contribution_type'] == 'existing_core_view' and e['packet']['core_id'] == core['core_id']]
        if extras:
            more = section('Additional mathematical exposition', '<ul>' + ''.join('<li><a href="../../non-lean/workbook/' + e['slot'].lower() + '/index.html">' + esc(e['packet']['title']) + '</a> · same core and split</li>' for e in extras) + '</ul>', 'supplementary')
            content = content.removesuffix('</article>') + more + '</article>'
        write(HUB + "cores/" + core["core_id"] + "/", title, content, items[core["core_id"]]["question"])
    withheld_routes = []
    decisions = {d["core_id"]: d for d in catalog["reader_decisions"]}
    for core in catalog.get("withheld_cores", []):
        route = HUB + "cores/" + core["core_id"] + "/"
        decision = decisions[core["core_id"]]
        body = intro("Exercise withheld pending correction", "This historical core remains reserved, but its rejected or ambiguous content is excluded from current exercise listings, reader downloads and scoring. No approved replacement is implied by this notice.")
        body += '<p class="qcb-boundary" data-qcb-withheld>' + esc(core["core_id"]) + ': ' + esc(decision["reason"]) + '</p>'
        body += '<p>The frozen preview and original review records remain available for audit. Withdrawal does not close this core\'s stable-release obligation and does not authorize a different split or duplicate core ID.</p>'
        body += '<p><a href="../../../' + HUB + 'evidence/index.html#answer-decisions">Inspect the current reader decisions</a> · <a href="../../../' + HUB + 'contribute/index.html">Contribute a separately reviewed correction</a></p>'
        write(route, "Withheld exercise · " + core["core_id"], body + '</div>', "Historical content withheld pending mathematical correction.", searchable=False)
        withheld_routes.append(route + "index.html")
    body = intro("Three reference warmups", "Small API applications, not deep proof synthesis. A distinct semantic review checked exact definitions, angle conventions and assumptions; inherited fixed-reference elaboration is separate from this review. The review is not a strictly source-blind decoder certificate.")
    for i, (item, review) in enumerate(formal_warmups(), 1):
        formal = item["formal"]
        content = prose(item["question"]) + '<pre><code>' + esc(json.dumps({k: formal[k] for k in ("imports", "target")}, ensure_ascii=False, indent=2)) + '</code></pre>'
        content += disclosure("Reference proof and semantic reconstruction", '<pre><code>' + esc(formal["reference_proof"]) + '</code></pre>' + prose(review["independent_reconstruction"]["meaning"]) + prose(review["independent_reconstruction"]["proof"]), "warmup-proof-" + str(i))
        content += '<p>Historical same-core alias: ' + esc(", ".join(review["suggested_core_aliases"])) + '. Not added to the native core count.</p>'
        body += section(item["key"], content, "warmup-" + str(i))
    write(HUB + "lean/warmups/", "Lean reference warmups", body + '</div>', "Three exact-target, semantic-audited diagnostic warmups with inherited trusted reference checks.")
    body = intro("Contribute without conflicting datasets", "Two contribution folders, one merge-time semantic contract. Existing mathematical targets keep their core identity, family and split across natural-language, Lean and mixed views.")
    for track in TRACKS:
        body += section(track.title() + " contributor goal", '<p><a href="' + REPO + '/blob/main/benchmarks/quantumcomputingbench/tracks/' + track + '/AGENT_GOAL.md">Open the copyable English agent goal</a></p>', track)
    body += prose((B / "shared/CONTRACT.md").read_text(encoding="utf-8"))
    write(HUB + "contribute/", "Contribution contract", body + '</div>', "Shared core IDs, UUID proposals, exact contracts, compatible views and split-safe collaboration.")
    body = intro("Evidence and release readiness", "An inspectable textbook is not automatically a fully validated benchmark. These are the current acceptance boundaries, not claimed completions.")
    body += '<pre><code>' + esc(json.dumps(stable_readiness(catalog), indent=2)) + '</code></pre>'
    body += '<p>A bounded historical cross-cohort review is available as <a href="' + REPO + '/blob/' + context["commit"] + '/benchmarks/quantumcomputingbench/reports/textbook-v1/cohort-reconciliation/review-at-8533b9b.json">an exact snapshot audit</a>. It identifies an equivalent target and cross-split mechanism overlap, not exhaustive global deduplication. Its inventory predates current withdrawals and later answer repairs; it does not authorize pooling.</p>'
    body += '<p>Historical integration quarantines, current rejected/ambiguous records and inherited provisional material are excluded from the normal reader. Historical releases and all source/review records are retained in the repository. Existing AI reviews are fallible, content-bound provenance, not newly invented expert approval. No model baseline or isolated arbitrary-Lean prediction evaluation is claimed.</p><p>The frozen benchmark graph is not the current whole-library inventory. Exact live node links are offered only when identities exist; planned/source-only anchors remain graph metadata. An import edge is not theorem entailment and a curated AND hyperedge is not a completed proof.</p>'
    body += section("Versioned reader decisions", '<pre><code>' + esc(json.dumps(catalog["reader_decisions"], indent=2)) + '</code></pre><p>The frozen preview contains historical predecessor questions and answers. Do not treat their bytes as current gold after a withdrawal. Answer-only repairs preserve the question contract. Explicit question successors bind both old and new contract hashes and require a distinct contract-change review; old acceptance and Lean views do not transfer. Neither kind creates another mathematical core.</p><p><a href="../../data/quantumcomputingbench/reader-items.json">Download current open reader views (not a stable training release)</a></p>', "answer-decisions")
    write(HUB + "evidence/", "Evidence and release readiness", body + '</div>', "Current second-pass review, split/dedup, formal-view, isolation and publication boundaries.")
    home = root / "index.html"
    text = home.read_text(encoding="utf-8")
    text = re.sub(r'<!-- qcb-textbook:start -->.*?<!-- qcb-textbook:end -->', '', text, flags=re.DOTALL)
    panel = '<!-- qcb-textbook:start --><section class="qcb-home" id="quantumcomputingbench"><p class="eyebrow">QuantumComputingBench · open exercise book</p><h2><a href="quantumcomputingbench/index.html">A graph-grounded quantum-computing exercise book</a></h2><p>Five parts. ' + str(len(catalog["cores"])) + ' retained native core IDs. Read substantial mathematics without Lean, then inspect the formal companion and exact evidence boundaries.</p><p><a href="quantumcomputingbench/non-lean/index.html">Read the mathematical exercises</a> · <a href="quantumcomputingbench/course/index.html">Follow the difficulty course</a> · <a href="quantumcomputingbench/reasoning/index.html">Understand reasoning graphs</a> · <a href="quantumcomputingbench/lean/index.html">Explore the Lean companion</a></p><p><small>Textbook edition in progress; semantic review and formal-view expansion remain explicit gates.</small></p></section><!-- qcb-textbook:end -->'
    text = text.replace('<main id="main-content">', '<main id="main-content">' + panel, 1)
    if 'static/quantumcomputingbench.css' not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="./static/quantumcomputingbench.css"></head>', 1)
    home.write_text(text, encoding="utf-8")
    patch_navigation(root)
    search_path = root / "search-index.json"
    search = read_json(search_path)
    search["entries"] = [e for e in search["entries"] if e.get("kind") != "quantumcomputingbench"] + entries
    search["entryCount"] = len(search["entries"])
    search["pageEntryCount"] = sum(e.get("type") == "page" for e in search["entries"])
    write_json(search_path, search)
    manifest = {"schema_version": 1, "catalog_hash": catalog["catalog_hash"],
                "reader_source_digest": reader_sources(), "routes": routes,
                "native_core_ids": len(catalog["cores"]), "admitted_native_lean_views": native_lean_count,
                "experimental_course": {"course_id": course_plan["course_id"], "course_digest": course_report["course_digest"], "distinct_shared_cores": course_report["distinct_shared_cores"], "new_mathematical_cores": 0, "canonical_admissions_changed": False, "by_construction_band": course_report["by_construction_band"]},
                "public_semantic_diagnostics": diagnostic_report,
                "expert_atlas": expert_report,
                "benchmark_center": benchmark_center,
                "supplementary_workbook": workbook_report,
                "runtime_registry_hash": registry["registry_hash"],
                "presentation": presentation_contract(),
                "math_notation": notation_contract,
                "benchmark_environment": runtime_environment,
                "withheld_routes": withheld_routes, "historical_native_core_count": catalog["historical_native_core_count"],
                "legacy_reference_warmups": 3, "stable": False,
                "leanGraphSha256": graph_hash, "source_commit": context["commit"]}
    write_json(data_dir / "reader.json", manifest)
    for filename in ("site-metadata.json", "build-report.json"):
        value = read_json(root / filename)
        value["searchEntryCount"] = search["entryCount"]
        value["quantumComputingBench"] = manifest
        write_json(root / filename, value)
    if hashlib.sha256(graph_path.read_bytes()).hexdigest() != graph_hash:
        raise ValueError("textbook publisher mutated the authoritative Lean graph")
    return {"pages": len(routes), "native_core_ids": len(catalog["cores"]), "stable": False}


def check_site(root):
    from qcb_nonlean_workbook import load_workbook
    from qcb_nonlean_workbook import verify_downloads as verify_workbook_downloads
    manifest = read_json(root / "data/quantumcomputingbench/reader.json")
    catalog, items, graph = load_catalog()
    workbook = load_workbook()
    verify_workbook_downloads(root / 'data/quantumcomputingbench/nonlean-workbook', workbook)
    if manifest.get('supplementary_workbook', {}).get('workbook_digest') != workbook['workbook_digest']:
        raise ValueError('supplementary workbook projection is stale')
    plan, views, course_report = course_reader()
    diagnostic_packet, diagnostic_qualification = diagnostic_reader()
    if manifest.get("presentation") != presentation_contract():
        raise ValueError("math, expert atlas or runtime presentation sources changed")
    if manifest.get("math_notation") != math_notation_contract(catalog["catalog_hash"]):
        raise ValueError("notation review does not match the displayed mathematical source")
    from qcb_bench_runtime import build_registry, verify_downloads

    from website.scripts.qcb_expert import build_expert_index
    registry = build_registry()
    if manifest.get("runtime_registry_hash") != registry["registry_hash"]:
        raise ValueError("runtime registry is stale")
    verify_downloads(root / "data/quantumcomputingbench/runtime", registry)
    if (manifest.get("benchmark_environment") != environment_record(registry)
            or read_json(root / "data/quantumcomputingbench/environment-smoke.json") != environment_record(registry)):
        raise ValueError("published environment report lost its execution/source binding")
    expert_index = read_json(root / "data/quantumcomputingbench/expert-index.json")
    live_ids = {n["id"] for n in read_json(root / "data/lean-graph.json")["nodes"]}
    source_commit = manifest["source_commit"]
    publication_commit = source_commit if re.fullmatch(r'[0-9a-f]{40}', source_commit) else None
    expected_expert = build_expert_index(catalog, items, graph, live_ids, publication_commit,
        snapshot=read_json(B / "manifests/release-v3/snapshot.json"), course_plan=plan,
        course_views=views, diagnostics=diagnostic_packet)
    if expert_index != expected_expert:
        raise ValueError("expert graph/source projection differs from the exact current registry")
    check_diagnostic_pages(root, diagnostic_packet, diagnostic_qualification, manifest, expert_index)
    if (manifest.get("experimental_course", {}).get("course_digest") != course_report["course_digest"]
            or manifest["experimental_course"]["distinct_shared_cores"] != course_report["distinct_shared_cores"]
            or manifest["experimental_course"]["new_mathematical_cores"] != 0
            or manifest["experimental_course"]["canonical_admissions_changed"] is not False):
        raise ValueError("course projection changed its qualified scope or core counting")
    for entry in plan["entries"]:
        page = (root / HUB / "cores" / entry["core_id"] / "index.html").read_text(encoding="utf-8")
        task = views[entry["view_id"]]["task"]
        if ('id="course"' not in page or any(esc(n["target"]) not in page for n in task["nodes"])):
            raise ValueError("missing or incomplete supplied course obligation map")
    if manifest["catalog_hash"] != catalog["catalog_hash"] or manifest["reader_source_digest"] != reader_sources():
        raise ValueError("textbook projection is stale")
    if read_json(root / "data/quantumcomputingbench/cores.json") != public_catalog(catalog):
        raise ValueError("public catalog differs from its declared identity display projection")
    if manifest["leanGraphSha256"] != hashlib.sha256((root / "data/lean-graph.json").read_bytes()).hexdigest():
        raise ValueError("textbook graph binding differs")
    current_routes = {HUB + "cores/" + c["core_id"] + "/index.html": items[c["core_id"]] for c in catalog["cores"]}
    for route in manifest["routes"]:
        page = (root / route).read_text(encoding="utf-8")
        if '<html lang="en"' not in page or 'class="qcb-reader"' not in page:
            raise ValueError("missing shared English reader shell: " + route)
        if route in current_routes:
            item = current_routes[route]
            if prose(item["question"]) not in page or prose(item["reference_answer"]) not in page or 'id="solution"' not in page:
                raise ValueError("page changed the exact reviewed question or answer: " + route)
    entries = [e for e in read_json(root / "search-index.json")["entries"] if e.get("kind") == "quantumcomputingbench"]
    expected = {HUB + "cores/" + c["core_id"] + "/index.html": items[c["core_id"]]["question"] for c in catalog["cores"]}
    actual = {e["url"]: e["summary"] for e in entries if e["url"] in expected}
    withheld = set(manifest.get("withheld_routes", []))
    expected_withheld = {HUB + "cores/" + c["core_id"] + "/index.html" for c in catalog.get("withheld_cores", [])}
    if withheld != expected_withheld or any(e["url"] in withheld for e in entries):
        raise ValueError("quarantined content entered ordinary question search")
    exported = read_json(root / "data/quantumcomputingbench/reader-items.json")
    expected_items = {key: public_reader_item(item) for key, item in items.items()}
    if (exported.get("catalog_hash") != catalog["catalog_hash"] or exported.get("stable") is not False
            or len(exported["items"]) != len(expected_items)
            or {i["core_id"]: i for i in exported["items"]} != expected_items):
        raise ValueError("current reader export differs from exact reviewed content or includes quarantined content")
    for route in withheld:
        page = (root / route).read_text(encoding="utf-8")
        if 'data-qcb-withheld' not in page or 'id="solution"' in page or 'id="hint"' in page or 'id="rubric"' in page:
            raise ValueError("quarantine notice exposed an unapproved answer")
    if actual != expected or len(entries) != len(manifest["routes"]) - len(withheld):
        raise ValueError("question-only search or route coverage changed")
    return {"pages": len(manifest["routes"]), "question_only_search": True, "graph_unchanged": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("publish", "check-site"))
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(publish(args.root) if args.command == "publish" else check_site(args.root), indent=2))
