"""Human-review graph locations over the checked QA catalog.

The exported relation graph is a frozen inventory, not an extracted proof-term
graph. Supplied course obligations are carried in a separate field. No source
identity, contract or split is changed by this presentation module.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from copy import deepcopy
from pathlib import PurePosixPath
from urllib.parse import quote

REPO = "https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench"
HUB = "quantumcomputingbench/"
ROUTES = [HUB + "expert/index.html", HUB + "expert/nodes/index.html", HUB + "expert/node/index.html"]
EDGE_LABELS = {
    "module-declares-leaf": "Module owns declaration",
    "module-supports-importer": "Module import availability",
    "track-contains-module": "Inventory grouping",
    "curated-chapter-module": "Curated chapter placement",
    "curriculum-navigation": "Curriculum navigation",
    "external-adapter-curriculum-plan": "Planned adapter placement",
    "research-route-obligation": "Recorded research obligation",
}


def _hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def _e(value):
    return html.escape(str(value), quote=True)


def _revision(value):
    if value is not None and (not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value)):
        raise ValueError("expert source links require an exact commit, or an explicit unavailable value")
    return value


def _relative(path):
    if (not isinstance(path, str) or not path or PurePosixPath(path).is_absolute()
            or ".." in PurePosixPath(path).parts or any(c in path for c in "\\:\r\n\x00")):
        raise ValueError("expert source path must be repository-relative")
    return path


def _url(path, revision, line=None):
    path = _relative(path)
    if revision is None:
        return None
    _revision(revision)
    if line is not None and (type(line) is not int or line < 1):
        raise ValueError("expert source line must be a positive integer")
    return REPO + "/blob/" + revision + "/" + quote(path, safe="/") + ("#L" + str(line) if line else "")


def _key(node):
    return "node-" + hashlib.sha256(node.encode()).hexdigest()[:20]


def _core_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"qcb-core-[a-z0-9-]+", value):
        raise ValueError("invalid core identity in expert map")
    return value


def _node_record(record, live_ids, frozen_commit):
    node_id = record["id"]
    source = record.get("source")
    line = record.get("line")
    if source:
        _relative(source)
    module = ""
    if source and source.startswith("QuantumBlockEncoding/") and source.endswith(".lean"):
        module = str(PurePosixPath(source).with_suffix("")).replace("/", ".")
    kind = record.get("kind", "unclassified")
    inventory = record.get("inventory_status")
    evidence = ("compiled_inventory" if inventory == "Compiled" else
                "partial_or_experimental_inventory" if inventory in {"Partial route", "Experimental"} else
                "curated_concept" if kind == "concept" else "structural_or_planned_inventory")
    return {"id": node_id, "anchor": _key(node_id), "label": record.get("label", node_id),
            "kind": kind, "module": module, "topic": record.get("topic", "Unclassified"),
            "inventory_status": inventory, "status": record.get("status", "unrecorded"),
            "open_obligation": record.get("open_obligation"), "evidence_class": evidence,
            "live_identity": "present_by_exact_id" if node_id in live_ids else "frozen_only",
            "source_path": source, "source_line": line,
            "frozen_source_url": _url(source, frozen_commit, line) if source else None,
            "source_location_scope": "frozen_snapshot_source"}


def build_expert_index(catalog, items, graph, live_ids, publication_commit, *, snapshot=None,
                       course_plan=None, course_views=None, diagnostics=None):
    """Build a lossless anchor/reverse map from already validated upstream inputs.

    This function checks joins; callers still perform the catalog/course/probe
    qualification gates. Passing an arbitrary dictionary cannot certify a proof.
    """
    _revision(publication_commit)
    frozen_commit = _revision(catalog["graph_source_commit"])
    if snapshot is not None:
        if snapshot["snapshot_id"] != catalog["snapshot_id"] or snapshot["commit"] != frozen_commit:
            raise ValueError("expert map snapshot differs from the checked catalog")
        snapshot_nodes = {n["id"]: n for n in snapshot["nodes"]}
        if snapshot_nodes != graph:
            raise ValueError("expert map nodes differ from the frozen graph")
    cores, reverse, anchors, course = {}, {}, set(), {}

    def attach(node_id, reference):
        if node_id not in graph:
            raise ValueError("unmapped exact expert anchor: " + str(node_id))
        anchors.add(node_id)
        bucket = reverse.setdefault(node_id, [])
        if reference not in bucket:
            bucket.append(reference)

    for raw in catalog["cores"]:
        core_id = _core_id(raw["core_id"])
        if core_id in cores or core_id not in items:
            raise ValueError("expert core identity duplicated or has no current item")
        item = items[core_id]
        if item["core_id"] != core_id or item["split"] != raw["split"]:
            raise ValueError("expert core/item identity or split changed")
        if item["target_nodes"] != raw["target_nodes"] or item["supporting_nodes"] != raw["supporting_nodes"]:
            raise ValueError("expert core anchor roles differ from the actual question")
        record = {k: deepcopy(raw[k]) for k in ("core_id", "title", "contract_hash", "part", "topic", "family",
                                      "split", "target_nodes", "supporting_nodes", "evidence_relation")}
        record["href"] = HUB + "cores/" + core_id + "/index.html"
        record["source_url"] = _url("benchmarks/quantumcomputingbench/" + raw["question_source_record"], publication_commit)
        record["evidence_url"] = _url("benchmarks/quantumcomputingbench/" + raw["answer_source_record"], publication_commit)
        record["editorial_status"] = raw.get("editorial_second_pass", "unrecorded")
        record["formal_admission"] = raw.get("views", {}).get("lean", {}).get("status", "not_admitted")
        record["rubric_criteria"] = len(item.get("rubric", []))
        cores[core_id] = record
        for field, role in (("target_nodes", "target"), ("supporting_nodes", "support")):
            for node in raw[field]:
                attach(node, {"kind": "core", "id": core_id, "role": role, "title": raw["title"],
                              "part": raw["part"], "split": raw["split"], "href": record["href"] + "#expert"})

    if (course_plan is None) != (course_views is None):
        raise ValueError("supply both course manifest and actual task views")
    for entry in (course_plan or {}).get("entries", []):
        core_id = entry["core_id"]
        if (core_id not in cores or entry["contract_hash"] != cores[core_id]["contract_hash"]
                or entry["split"] != cores[core_id]["split"] or entry["view_id"] not in course_views):
            raise ValueError("expert supplied-course identity/contract/split mismatch")
        task = course_views[entry["view_id"]]["task"]
        if (task["core_id"] != core_id or task["contract_hash"] != entry["contract_hash"]
                or task["split"] != entry["split"] or _hash(task) != entry["task_hash"]):
            raise ValueError("expert supplied graph differs from the actual qualified task")
        ids = [n["id"] for n in task["nodes"]]
        if len(set(ids)) != len(ids) or task["root_id"] not in ids:
            raise ValueError("expert supplied graph has duplicate nodes or a missing root")
        seen = set()
        for node in task["nodes"]:
            if any(dep not in seen for dep in node["depends_on"]):
                raise ValueError("supplied obligations must retain their actual acyclic order")
            seen.add(node["id"])
        course[core_id] = {"view_id": entry["view_id"], "root_id": task["root_id"],
                           "nodes": [{k: deepcopy(n[k]) for k in ("id", "target", "depends_on")} for n in task["nodes"]],
                           "band": entry["difficulty"]["construction_band"], "task_hash": entry["task_hash"],
                           "evidence_class": "evaluator_supplied_obligations_not_extracted_proof_dependencies"}
        for node in entry["source_node_ids"]:
            attach(node, {"kind": "course_view", "id": entry["view_id"], "role": "course_source",
                          "title": cores[core_id]["title"], "part": cores[core_id]["part"], "split": entry["split"],
                          "href": cores[core_id]["href"] + "#course"})

    probes = {}
    if diagnostics is not None and diagnostics["snapshot_id"] != catalog["snapshot_id"]:
        raise ValueError("diagnostic source graph differs from the canonical snapshot")
    for probe in (diagnostics or {}).get("probes", []):
        identity = probe["probe_id"]
        if not re.fullmatch(r"[0-9a-f-]{36}", identity) or not re.fullmatch(r"[a-z0-9_]+", probe["cluster_id"]):
            raise ValueError("invalid diagnostic identity or cluster path")
        if identity in probes:
            raise ValueError("duplicate diagnostic expert reference")
        for core_id in probe["parent_core_ids"]:
            if (core_id not in cores or probe["parent_contracts"][core_id] != cores[core_id]["contract_hash"]
                    or probe["split"] != cores[core_id]["split"]):
                raise ValueError("diagnostic expert parent/contract/split mismatch")
        probes[identity] = {"probe_id": identity, "cluster_id": probe["cluster_id"],
                            "split": probe["split"], "parent_core_ids": list(probe["parent_core_ids"]),
                            "source_nodes": list(probe["source_nodes"]), "admission": "candidate_not_counted",
                            "href": HUB + "diagnostics/" + probe["cluster_id"] + "/index.html#probe-" + identity}
        for node in probe["source_nodes"]:
            attach(node, {"kind": "diagnostic_candidate", "id": identity, "role": "diagnostic_source",
                          "title": probe["cluster_id"].replace("_", " "), "part": cores[probe["parent_core_ids"][0]]["part"],
                          "split": probe["split"], "href": probes[identity]["href"]})

    selected = set(anchors)
    raw_edges = (snapshot or {}).get("edges", [])
    owners = {e["source"] for e in raw_edges if e["type"] == "module-declares-leaf" and e["target"] in anchors}
    selected.update(owners)
    for edge in raw_edges:
        if edge["type"] == "module-supports-importer" and (edge["source"] in owners or edge["target"] in owners):
            selected.update((edge["source"], edge["target"]))
    if any(n not in graph for n in selected):
        raise ValueError("recorded structural neighborhood refers to an absent graph node")
    edges = {}
    duplicate_edges = 0
    for edge in raw_edges:
        if edge["source"] in selected and edge["target"] in selected:
            identity = (edge["source"], edge["target"], edge["type"])
            if identity in edges:
                duplicate_edges += 1
                continue
            edges[identity] = {"source": identity[0], "target": identity[1], "type": identity[2],
                               "label": EDGE_LABELS.get(identity[2], identity[2].replace("-", " ")),
                               "evidence_class": "recorded_structural_relation_not_proof_entailment"}
    hyperedges = []
    for edge in (snapshot or {}).get("hyperedges", []):
        endpoints = edge["tails"] + edge["heads"]
        if not anchors.intersection(endpoints):
            continue
        row = {key: deepcopy(edge[key]) for key in ("id", "label", "tails", "heads", "status")}
        for key in ("mechanism", "hypothesis_map", "conclusion_map", "failure_boundary", "review", "lean_refs"):
            if key in edge:
                row[key] = deepcopy(edge[key])
        row["unmapped_endpoint_ids"] = [n for n in endpoints if n not in graph]
        row["evidence_class"] = "curated_hyperedge_not_lean_entailment"
        hyperedges.append(row)
    nodes = {node: _node_record(graph[node], live_ids, frozen_commit) for node in sorted(selected)}
    for bucket in reverse.values():
        bucket.sort(key=lambda r: (r["kind"], r["id"], r["role"]))
    result = {"schema_version": "qcb.expert_graph_index.v1", "catalog_hash": catalog["catalog_hash"],
              "snapshot_id": catalog["snapshot_id"], "frozen_source_commit": frozen_commit,
              "publication_commit": publication_commit, "cores": cores, "diagnostics": probes,
              "anchor_node_ids": sorted(anchors), "nodes": nodes, "reverse_index": reverse,
              "structural_edges": sorted(edges.values(), key=lambda e: (e["source"], e["target"], e["type"])),
              "curated_hyperedges": hyperedges, "supplied_courses": course,
              "counts": {"shared_cores": len(cores), "diagnostic_candidates": len(probes),
                         "supplied_course_views": len(course), "distinct_cited_anchors": len(anchors),
                         "context_nodes": len(nodes) - len(anchors),
                         "live_anchor_identity_matches": sum(n in live_ids for n in anchors),
                         "frozen_only_anchors": sum(n not in live_ids for n in anchors)},
              "edge_policy": "Only recorded snapshot ownership/import/curated edges; no inferred theorem-proof dependencies.",
              "source_policy": "Frozen source links bind frozen lines; exact live identity does not certify source equality.",
              "coverage_policy": "Anchor citations locate questions; citation counts are neither whole-graph question coverage nor mathematical proof depth.",
              "duplicate_snapshot_edge_records_collapsed": duplicate_edges,
              "new_mathematical_cores": 0, "canonical_admissions_changed": False}
    result["index_digest"] = _hash(result)
    return result


def _link(url, label, **attrs):
    if not url:
        return '<span>' + _e(label) + ' <small>(source link unavailable)</small></span>'
    attributes = ''.join(' ' + _e(k.replace('_', '-')) + '="' + _e(v) + '"' for k, v in attrs.items())
    return '<a' + attributes + ' href="' + _e(url) + '">' + _e(label) + '</a>'


def _graph_link(node, prefix):
    if node["live_identity"] == "present_by_exact_id":
        return _link(prefix + 'lean-graph/index.html?focus=' + quote(node["id"], safe=''), node["label"], data_qcb_graph='')
    return _link(prefix + HUB + 'expert/node/index.html?node=' + quote(node["id"], safe=''), node["label"] + ' · frozen anchor')


def graph_summary(core_id, index, prefix='../../../'):
    """Visible concise location, before the closed expert dossier."""
    core = index["cores"][core_id]
    targets = [index["nodes"][n] for n in core["target_nodes"]]
    modules = sorted({n["module"].removeprefix('QuantumBlockEncoding.') for n in targets if n["module"]})
    return ('<div class="qcb-graph-location" data-qcb-graph-location><p class="eyebrow">Library location</p><p>'
            + _e(core["part"].replace('-', ' ').title())
            + (' <span aria-hidden="true">›</span> ' + _e(', '.join(modules)) if modules else '')
            + '</p><p>' + ' · '.join(_graph_link(n, prefix) for n in targets)
            + '</p><p><a href="#expert">Inspect assumptions, graph roles and evidence</a> · '
            + _link(prefix + HUB + 'expert/index.html', 'Expert review map') + '</p></div>')


def _node_rows(core, index, prefix):
    rows = ''
    for field, role in (("target_nodes", "Target statement"), ("supporting_nodes", "Supporting anchor")):
        for node_id in core[field]:
            n = index["nodes"][node_id]
            rows += ('<tr><td>' + _e(role) + '</td><td>' + _graph_link(n, prefix)
                     + '<small>' + _e(n["module"].removeprefix('QuantumBlockEncoding.') or n["kind"]) + '</small></td><td>'
                     + _e(n["inventory_status"] or n["evidence_class"].replace('_', ' ')) + '</td><td>'
                     + _link(n["frozen_source_url"], 'Frozen source' + (':' + str(n['source_line']) if n['source_line'] else ''))
                     + ' · ' + _link(prefix + HUB + 'expert/node/index.html?node=' + quote(node_id, safe=''), 'Neighborhood') + '</td></tr>')
    return '<div class="qcb-expert-scroll"><table class="qcb-expert-table"><thead><tr><th>Question role</th><th>Library statement</th><th>Frozen inventory</th><th>Inspect</th></tr></thead><tbody>' + rows + '</tbody></table></div>'


def expert_panel(core_id, index, prefix='../../../'):
    core = index["cores"][core_id]
    body = '<p>These targets and supporting anchors are the actual bindings of this question. A supporting citation alone does not establish the target.</p>'
    body += _node_rows(core, index, prefix)
    body += '<p><strong>Question evidence:</strong> ' + _e(core['evidence_relation'].replace('_', ' '))
    body += '. Editorial status: ' + _e(core['editorial_status'].replace('_', ' ')) + '. Formal admission: ' + _e(core['formal_admission'].replace('_', ' ')) + '.</p>'
    body += '<p>' + _link(core['source_url'], 'Current question source') + ' · ' + _link(core['evidence_url'], 'Current answer and rubric source') + ' · ' + _link(prefix + HUB + 'expert/nodes/index.html', 'Find every question citing a node') + '</p>'
    body += '<p>' + _link('#solution', 'Read the mathematical reference answer') + ' · ' + _link('#rubric', 'Inspect the scoring criteria') + '</p>'
    if core_id in index['supplied_courses']:
        course = index['supplied_courses'][core_id]
        body += '<h3>Supplied reasoning route</h3><p>The following task inputs describe the evaluator-supplied obligation graph. They are separate from library ownership/import relations and extracted Lean proof dependencies.</p><ol class="qcb-expert-obligations">'
        for n in course['nodes']:
            body += '<li><strong>' + _e(n['id'].replace('_', ' ')) + (' · final root' if n['id'] == course['root_id'] else '') + '</strong><span>'
            body += ('All inputs: ' + _e(', '.join(n['depends_on'])) if n['depends_on'] else 'No preceding supplied input') + '</span></li>'
        body += '</ol><p>' + _link('#course', 'Inspect the exact formal subgoals and their supplied inputs') + '</p>'
    exact = {k: core[k] for k in ('core_id', 'contract_hash', 'family', 'split', 'target_nodes', 'supporting_nodes')}
    exact.update(snapshot_id=index['snapshot_id'], frozen_source_commit=index['frozen_source_commit'], publication_commit=index['publication_commit'])
    body += '<details class="qcb-disclosure"><summary>Exact identities and source versions</summary><pre><code>' + _e(json.dumps(exact, indent=2)) + '</code></pre><p>' + _e(index['source_policy']) + '</p></details>'
    return '<details class="qcb-disclosure qcb-expert-panel" id="expert"><summary>Expert review: graph location and evidence</summary>' + body + '</details>'


def diagnostic_panel(probe_id, index, prefix='../../../'):
    """Source context of a candidate is not a claim it is a named library root."""
    probe = index['diagnostics'][probe_id]
    parents = [_link(prefix + index['cores'][core]['href'] + '#expert', core.removeprefix('qcb-core-').upper())
               for core in probe['parent_core_ids']]
    body = '<p><strong>Library context:</strong> ' + ' · '.join(parents) + '</p>'
    body += '<p>The diagnostic proposition and its polarity certificate are separate from the named source declarations below. These declarations locate the mathematical context; a source citation alone does not prove this candidate conclusion.</p><ul>'
    for node_id in probe['source_nodes']:
        node = index['nodes'][node_id]
        body += '<li>' + _graph_link(node, prefix) + ' · ' + _link(node['frozen_source_url'], 'Frozen source') + ' · '
        body += _link(prefix + HUB + 'expert/node/index.html?node=' + quote(node_id, safe=''), 'Related questions') + '</li>'
    body += '</ul><p>Inherited split: ' + _e(probe['split']) + '. Candidate remains outside canonical admission.</p>'
    body += '<p>' + _link(_url('benchmarks/quantumcomputingbench/reports/learning-validity-v1/reference-checks.json', index['publication_commit']), 'Actual candidate polarity receipts') + ' · '
    body += _link(_url('benchmarks/quantumcomputingbench/reports/learning-validity-v1/answer-review.json', index['publication_commit']), 'Mathematical explanation and rubric review') + '</p>'
    return '<details class="qcb-disclosure qcb-expert-panel" id="expert-' + _e(probe_id) + '"><summary>Locate this diagnostic in the library graph</summary>' + body + '</details>'


def _legend():
    return ('<section class="qcb-section"><h2>Read the relation before drawing a conclusion</h2><dl class="qcb-legend">'
            '<dt>Target / support</dt><dd>How the question cites a library anchor. This is not itself a proof edge.</dd>'
            '<dt>Ownership / import</dt><dd>Recorded library structure and availability of declarations.</dd>'
            '<dt>Supplied obligation inputs</dt><dd>Subgoals made available together by a particular evaluator task.</dd>'
            '<dt>Curated hyperedge / planned anchor</dt><dd>A documented conceptual or compositional relationship with its own status. Inspect its assumptions and unproved boundaries.</dd></dl></section>')


def publish_expert(write, intro, index):
    """Publish three bounded routes; caller separately writes the JSON and assets."""
    counts = index['counts']
    body = intro('Expert review map', 'Locate a question in the library, inspect the exact statement and source version, and see which other questions reuse its anchors.')
    body += '<p>' + _link('../index.html', 'Exercise book') + ' / Expert map · ' + _link('nodes/index.html', 'Browse cited nodes') + ' · ' + _link('node/index.html', 'Open a focused neighborhood') + '</p>'
    body += '<div class="qcb-grid">' + ''.join('<article class="qcb-card"><strong>' + str(counts[key]) + '</strong><p>' + label + '</p></article>' for key, label in
            (('shared_cores', 'Shared mathematical cores'), ('distinct_cited_anchors', 'Distinct cited graph anchors'), ('supplied_course_views', 'Existing supplied course views'), ('diagnostic_candidates', 'Separate diagnostic candidates'))) + '</div>'
    body += '<p>' + _e(index['coverage_policy']) + '</p>' + _legend()
    body += '<section class="qcb-section"><h2>Review questions by mathematical area</h2>'
    for part in sorted({c['part'] for c in index['cores'].values()}):
        entries = [c for c in index['cores'].values() if c['part'] == part]
        body += '<details class="qcb-disclosure"><summary>' + _e(part.replace('-', ' ').title()) + ' · ' + str(len(entries)) + ' shared cores</summary><ul>'
        for core in entries:
            body += '<li>' + _link('../../' + core['href'] + '#expert', core['core_id'].removeprefix('qcb-core-').upper() + ' · ' + core['title']) + '<small>' + _e(core['split']) + ' · ' + str(len(core['target_nodes'])) + ' targets / ' + str(len(core['supporting_nodes'])) + ' supporting anchors</small></li>'
        body += '</ul></details>'
    body += '</section><p>' + _link('../../data/quantumcomputingbench/expert-index.json', 'Download the versioned anchor and reverse-index data') + '</p>'
    write(HUB + 'expert/', 'Expert review map', body + '</div>', 'Exact graph location, source versions and evidence roles for quantum-computing QA.')

    body = intro('Which questions use this library node?', 'Search the exact anchor label, module or question title. Targets, supporting anchors, course sources and diagnostic sources retain different roles.')
    body += '<p>' + _link('../index.html', 'Expert review map') + ' / Cited-node index</p>'
    body += '<div class="qcb-filter" data-qcb-expert-filter><label for="qcb-expert-search">Search nodes and associated questions</label><input id="qcb-expert-search" type="search" autocomplete="off"><p role="status" data-qcb-expert-count></p></div>'
    body += '<div class="qcb-expert-node-list">'
    for node_id in index['anchor_node_ids']:
        node, references = index['nodes'][node_id], index['reverse_index'][node_id]
        search = ' '.join([node_id, node['label'], node['module']] + [r['title'] + ' ' + r['id'] + ' ' + r['role'] for r in references])
        body += '<article class="qcb-part" id="' + node['anchor'] + '" data-qcb-expert-row data-search="' + _e(search.casefold()) + '"><h2>' + _graph_link(node, '../../../') + '</h2><p>' + _e(node['module'] or node['kind']) + ' · ' + _e(node['inventory_status'] or node['evidence_class'].replace('_', ' ')) + '</p><p>'
        body += _link('../node/index.html?node=' + quote(node_id, safe=''), 'View this neighborhood') + ' · ' + _link(node['frozen_source_url'], 'Inspect frozen source') + '</p>'
        body += '<details class="qcb-disclosure"><summary>Questions and views citing this anchor (' + str(len(references)) + ' role bindings)</summary><ul>'
        for ref in references:
            body += '<li>' + _link('../../../' + ref['href'], ref['title']) + '<small>' + _e(ref['kind'].replace('_', ' ') + ' · ' + ref['role'].replace('_', ' ') + ' · ' + ref['split']) + '</small></li>'
        body += '</ul><code>' + _e(node_id) + '</code></details></article>'
    body += '</div>'
    write(HUB + 'expert/nodes/', 'Node-to-question review index', body + '</div>', 'An exact reverse index of graph anchors cited by current questions and their distinct views.')

    body = intro('Focused library neighborhood', 'Select a cited declaration or module to inspect its recorded graph relations and the questions that use it.')
    body += '<p>' + _link('../index.html', 'Expert review map') + ' · ' + _link('../nodes/index.html', 'Static node-to-question index') + '</p>'
    body += '<div data-qcb-expert-viewer data-url="../../../data/quantumcomputingbench/expert-index.json" data-site-prefix="../../../"><form data-qcb-expert-select><label for="qcb-expert-node">Library node</label><input id="qcb-expert-node" name="node" list="qcb-expert-choices" autocomplete="off"><datalist id="qcb-expert-choices"></datalist><button type="submit">Inspect node</button></form><p role="status" data-qcb-expert-status>Choose a node above, or use the static index.</p><div data-qcb-expert-result></div></div>'
    body += _legend()
    body += '<noscript><p>JavaScript is disabled. The static node-to-question index includes every cited anchor, frozen source and associated question.</p></noscript>'
    write(HUB + 'expert/node/', 'Focused library neighborhood', body + '</div>', 'Inspect exact library ownership/import neighbors, frozen source and associated QA roles.')
    return {"index_digest": index['index_digest'], "counts": index['counts'], "routes": ROUTES,
            "publication_commit": index['publication_commit'], "new_mathematical_cores": 0,
            "canonical_admissions_changed": False}
