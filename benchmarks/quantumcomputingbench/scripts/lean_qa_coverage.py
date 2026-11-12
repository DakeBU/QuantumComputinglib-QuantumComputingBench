#!/usr/bin/env python3
"""Audit Lean QA citations against the frozen graph and current reader catalog."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
sys.path.insert(0, str(B / "src"))

from qcb_assessment_v3 import public_status
from qcb_core import read_json, write_json
from qcb_curriculum import load_catalog
from qcb_integrity import text_sha
from qcb_nonlean_workbook import load_workbook

SNAPSHOT = B / "manifests/release-v3/snapshot.json"
COURSE = B / "tracks/lean/curriculum/course-v4.json"
NATIVE = B / "tracks/lean/views/native-v1.json"
PUBLIC_PROBES = B / "tracks/lean/learning-validity/v1/cohort.json"


def audit():
    catalog, _, graph = load_catalog()
    cores = {row["core_id"]: row for row in catalog["cores"]}
    course = read_json(COURSE)
    native = read_json(NATIVE)["views"]
    public_probes = read_json(PUBLIC_PROBES)["probes"]
    sealed = public_status()
    workbook = load_workbook()
    snapshot = read_json(SNAPSHOT)
    if (snapshot["snapshot_id"] != catalog["snapshot_id"]
            or course["catalog_hash"] != catalog["catalog_hash"]
            or course["snapshot_id"] != catalog["snapshot_id"]
            or workbook["catalog_hash"] != catalog["catalog_hash"]):
        raise ValueError("Coverage inputs do not share the current catalog and frozen graph")

    course_cores = {row["core_id"] for row in course["entries"]}
    native_cores = {row["core_id"] for row in native}
    if (not (course_cores | native_cores) <= cores.keys()
            or len(course_cores) != len(course["entries"]) or len(native_cores) != len(native)):
        raise ValueError("A formal view has an unknown or duplicate core")
    for row in course["entries"] + native:
        core = cores[row["core_id"]]
        if any(row[field] != core[field] for field in ("split", "contract_hash", "family", "snapshot_id")):
            raise ValueError("Formal view differs from the current shared core contract")

    sealed_probes = sealed["seal"]["probe_index"]
    citations = {
        "course": {node for row in course["entries"] for node in row["source_node_ids"]},
        "public_diagnostics": {node for row in public_probes for node in row["source_nodes"]},
        "sealed_assessment": {node for row in sealed_probes for node in row["source_nodes"]},
        "workbook": {node for row in workbook["entries"] for node in
                     row["packet"]["target_nodes"] + row["packet"]["supporting_nodes"]},
    }
    if any(not nodes <= graph.keys() for nodes in citations.values()):
        raise ValueError("A suite cites a node absent from the frozen graph")
    declarations = {node: value for node, value in graph.items() if value.get("kind") == "declaration"}
    closed = {node for node, value in declarations.items()
              if value.get("inventory_status") == "Compiled" and value.get("open_obligation") is False}
    if any(not citations[suite] <= closed for suite in ("course", "public_diagnostics", "sealed_assessment")):
        raise ValueError("A formal suite cites a declaration outside the closed compiled inventory")

    modules = defaultdict(set)
    for node, value in declarations.items():
        if value.get("source"):
            modules[value["source"]].add(node)
    canonical_citations = defaultdict(set)
    for core in cores.values():
        for node in core["target_nodes"] + core["supporting_nodes"]:
            canonical_citations[node].add(core["core_id"])

    course_and_assessment = citations["course"] | citations["public_diagnostics"] | citations["sealed_assessment"]
    module_rows = []
    for path, nodes in sorted(modules.items()):
        module_rows.append({
            "path": path,
            "declarations": len(nodes),
            "closed_compiled_declarations": len(nodes & closed),
            "closed_compiled_outside_course_and_assessment_citations": len((nodes & closed) - course_and_assessment),
            "citation_counts": {suite: len(nodes & ids) for suite, ids in citations.items()},
            "canonical_nl_cores": sorted({core_id for node in nodes for core_id in canonical_citations[node]}),
        })
    return {
        "schema_version": "qcb.lean_qa_coverage_audit.v1",
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip(),
        "catalog_hash": catalog["catalog_hash"],
        "snapshot_id": snapshot["snapshot_id"],
        "graph_source_commit": snapshot["commit"],
        "graph_relationship_inventory": {
            "ordinary_edges": dict(sorted(Counter(edge["type"] for edge in snapshot["edges"]).items())),
            "hyperedges": dict(sorted(Counter(edge["status"] for edge in snapshot["hyperedges"]).items())),
        },
        "input_sha256_lf": {p.relative_to(R).as_posix(): text_sha(p) for p in (SNAPSHOT, COURSE, NATIVE, PUBLIC_PROBES)},
        "workbook_digest": workbook["workbook_digest"],
        "assessment_seal_digests": {
            "v2": sealed["base_v2_seal_digest"],
            "v3": sealed["seal"]["extension_seal_digest"],
        },
        "canonical_cores_by_part": dict(sorted(Counter(row["part"] for row in cores.values()).items())),
        "public_lean_cores_by_part": dict(sorted(Counter(cores[key]["part"] for key in course_cores | native_cores).items())),
        "course_cores": len(course_cores),
        "native_formal_cores": len(native_cores),
        "public_lean_distinct_cores": len(course_cores | native_cores),
        "course_topology_tags": dict(sorted(Counter(
            tag for row in course["entries"] for tag in row["topology"]["tags"]).items())),
        "public_diagnostic_propositions": len(public_probes),
        "sealed_propositions": len(sealed_probes),
        "workbook_entries": len(workbook["entries"]),
        "declarations": len(declarations),
        "closed_compiled_declarations": len(closed),
        "citation_counts": {suite: len(nodes) for suite, nodes in citations.items()},
        "closed_compiled_outside_course_and_assessment_citations": len(closed - course_and_assessment),
        "modules": module_rows,
        "scope": "Counts describe exact citations and supplied routes. Public formal-view counts deduplicate shared core IDs. "
                 "Per-module counts use the suites that provide explicit graph citations. "
                 "Graph edges and cited declarations do not measure theorem-proof dependencies or model mastery.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a new output path to preserve the existing audit.")
    report = audit()
    write_json(args.output, report, immutable=True)
    print(json.dumps({key: report[key] for key in ("catalog_hash", "public_lean_distinct_cores",
                                                    "closed_compiled_declarations", "citation_counts")}))


if __name__ == "__main__":
    main()
