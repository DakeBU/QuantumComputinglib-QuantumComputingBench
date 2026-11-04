#!/usr/bin/env python3
"""Check this unadmitted contribution package; never judge its mathematics."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def main():
    package = Path(__file__).resolve().parent
    root = next((p for p in package.parents
                 if (p / "benchmarks/quantumcomputingbench/src/qcb_curriculum.py").is_file()), None)
    if root is None:
        raise ValueError("Apply the contribution files to the documented repository baseline first.")
    manifest = read(package / "manifest.json")
    for entry in manifest["files"]:
        path = root / entry["path"]
        if not path.is_file() or sha(path) != entry["sha256"]:
            raise ValueError("Package file mismatch: " + entry["path"])
    sys.path.insert(0, str(root / "benchmarks/quantumcomputingbench/src"))
    from qcb_curriculum import load_catalog, core_contract, validate_proposals
    from qcb_textbook_policy import check_source_bindings
    catalog, originals, graph = load_catalog()
    if catalog["catalog_hash"] != manifest["catalog_hash"]:
        raise ValueError("Current catalog differs: rebase and re-review instead of transferring approval.")
    proposals = []
    payloads = {}
    for contribution in manifest["contributions"]:
        payload = read(root / contribution["payload_path"])
        proposal = read(root / contribution["proposal_path"])
        payloads[payload["slot"]] = payload
        if canonical(payload) != contribution["item_digest"]:
            raise ValueError("Content digest mismatch: " + payload["slot"])
        if proposal["item_digest"] != contribution["item_digest"]:
            raise ValueError("Proposal binding mismatch: " + payload["slot"])
        required = ["mathematical_target", "question", "reference_answer", "rubric",
                    "common_errors", "boundary_cases", "difficulty", "reasoning_map",
                    "source_refs", "unverified", "provenance"]
        if any(not payload.get(k) for k in required):
            raise ValueError("Incomplete payload: " + payload["slot"])
        if sum(row["weight"] for row in payload["rubric"]) != 10:
            raise ValueError("Rubric weights must sum to ten: " + payload["slot"])
        for node in payload["target_nodes"] + payload["supporting_nodes"]:
            if node not in graph:
                raise ValueError("Unknown frozen graph node: " + node)
        if payload["contribution_type"] == "existing_core_view":
            if core_contract(payload) != core_contract(originals[payload["core_id"]]):
                raise ValueError("Existing mathematical contract changed: " + payload["slot"])
        else:
            if payload["split"] != "unassigned_pending_reconciliation":
                raise ValueError("Candidate split assigned without reconciliation.")
        for ref in payload["source_refs"]:
            if sha(root / ref["path"]) != ref["sha256"]:
                raise ValueError("Source bytes changed: " + ref["path"])
        reasoning = payload["reasoning_map"]
        if reasoning.get("not_extracted_lean_dependencies") is not True:
            raise ValueError("Reasoning provenance must be explicit.")
        seen = {entry["id"] for entry in reasoning["inputs"]}
        for step in reasoning["steps"]:
            if step["id"] in seen or any(x not in seen for x in step["required_inputs"]):
                raise ValueError("Unknown, forward or duplicate reasoning input in " + payload["slot"])
            if not all(step.get(k) for k in ("claim", "conclusion", "justification")):
                raise ValueError("Incomplete reasoning step in " + payload["slot"])
            seen.add(step["id"])
        proposals.append(proposal)
    result = validate_proposals(catalog, proposals)
    reviewed_slots = set()
    for report_path in manifest["review_reports"]:
        report = read(root / report_path)
        if report["method"] != "independent-mathematical-reader-review":
            raise ValueError("Unexpected review method.")
        phase1_path = root / report["provenance"]["phase1_path"]
        phase1 = read(phase1_path)
        if report["reviewer"] != phase1["reviewer"]:
            raise ValueError("Phase-one reviewer identity differs.")
        phase1_hash = report["provenance"].get("phase1_sha256_raw", report["provenance"].get("phase1_raw_sha256"))
        if not phase1_hash or sha(phase1_path) != phase1_hash:
            raise ValueError("Independent derivation bytes changed.")
        phase1_digest = report["provenance"].get("phase1_digest", report["provenance"].get("phase1_canonical_digest"))
        if not phase1_digest or canonical(phase1) != phase1_digest:
            raise ValueError("Independent derivation content binding changed.")
        for item in report["items"]:
            payload = payloads[item["slot"]]
            if item["slot"] in reviewed_slots:
                raise ValueError("Duplicate current review binding.")
            reviewed_slots.add(item["slot"])
            if item["item_digest"] != canonical(payload):
                raise ValueError("Stale review: " + item["slot"])
            if report["reviewer"] == payload["author"]:
                raise ValueError("Self-review cannot be independent.")
            if not item.get("reasoning") or not item.get("source_checks"):
                raise ValueError("Missing review evidence.")
            check_source_bindings(item["source_checks"])
            blind = read(package / "blind" / (item["slot"] + ".json"))
            for key in ("core_id", "question", "assumptions", "conventions", "graph_version",
                        "target_nodes", "supporting_nodes", "source_refs"):
                if blind[key] != payload[key]:
                    raise ValueError("Question/source context changed since independent derivation.")
    if reviewed_slots != set(payloads):
        raise ValueError("Some payloads lack an exact current comparison report.")
    print(json.dumps({"package_integrity": "pass", "proposal_compatibility": result,
                      "mathematical_approval": "not_established_by_this_script",
                      "benchmark_admission": False, "new_lean_execution": False}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, StopIteration) as error:
        print("ERROR:", error, file=sys.stderr)
        raise SystemExit(1)
