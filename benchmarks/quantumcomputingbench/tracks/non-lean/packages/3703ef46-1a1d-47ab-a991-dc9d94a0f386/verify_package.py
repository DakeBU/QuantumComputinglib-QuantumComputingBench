#!/usr/bin/env python3
"""Read-only integrity checks for this contribution package, never math approval."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from uuid import UUID

P = Path(__file__).resolve().parent
R = P.parents[5]
B = R / "benchmarks/quantumcomputingbench"
sys.path.insert(0, str(B / "src"))
from qcb_core import digest
from qcb_textbook_policy import CONTRACT_FIELDS, check_source_bindings


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rooted(name):
    path = (R / name).resolve()
    assert path.is_relative_to(R), ("path escapes repository", name)
    return path


def main():
    manifest = read(P / "manifest.json")
    baseline = read(P / "evidence/baseline.json")
    assert manifest["base_commit"] == baseline["base_commit"]
    files = manifest["files"]
    names = [x["path"] for x in files]
    assert len(names) == len(set(names))
    for entry in files:
        path = rooted(entry["path"])
        assert path.is_file() and not path.is_symlink(), entry["path"]
        assert sha(path) == entry["sha256"], ("changed bytes", entry["path"])
        assert path.stat().st_size == entry["bytes"], entry["path"]
    actual_package = {
        str(x.relative_to(R)) for x in P.rglob("*")
        if x.is_file() and x.name != "manifest.json" and "__pycache__" not in x.parts
    }
    assert actual_package == {x for x in names if x.startswith(str(P.relative_to(R)) + "/")}
    graph = rooted(baseline["graph"]["path"])
    assert sha(graph) == baseline["graph"]["sha256"]
    nodes = {x["id"] for x in read(graph)["nodes"]}
    for old in baseline["previous_cohort"]["verified_files"]:
        assert sha(rooted(old["path"])) == old["sha256"], ("historical change", old["path"])
    for source in read(P / "source-index.json")["source_files"]:
        assert sha(rooted(source["path"])) == source["sha256_raw"]
    for source in baseline["protocol_bindings"]:
        assert sha(rooted(source["path"])) == source["sha256"]

    # Phase-1 seals remain valid even if a reviewed payload subsequently changes.
    for prefix in "GPE":
        auth = read(P / "evidence" / (prefix + "-phase2-authorization.json"))
        assert auth["phase1_observed_before_phase2_authorization"] is True
        for name, expected in auth["bound_files"].items():
            if name.startswith("reviews/"):
                assert sha(P / name) == expected, ("changed phase-1 seal", name)

    questions = [json.loads(x) for x in (P / "questions-only.jsonl").read_text().splitlines()]
    references = [json.loads(x) for x in (P / "references-rubrics.jsonl").read_text().splitlines()]
    assert len(questions) == len(references) == len(manifest["contributions"]) == 6
    question_by_slot = {x["slot"]: x for x in questions}
    reference_by_slot = {x["slot"]: x for x in references}
    proposal_paths = set()
    for row in manifest["contributions"]:
        q = read(rooted(row["payload_path"]))
        slot = q["slot"]
        UUID(q["proposal_id"])
        assert q["core_id"] == "candidate:" + q["proposal_id"]
        assert q["admission"] == "candidate_not_counted" and q["dedup_review_required"] is True
        assert q["split"] == "unassigned_pending_reconciliation"
        assert q["snapshot_id"] == baseline["graph"]["snapshot_id"]
        assert set(q["target_nodes"] + q["supporting_nodes"]) <= nodes
        assert abs(sum(x["weight"] for x in q["rubric"]) - 10) < 1e-12
        assert all(x["weight"] > 0 and x["criterion"] for x in q["rubric"])
        frozen = read(P / "questions" / (slot + ".json"))
        for field in ["core_id", "question", "assumptions", "conventions"]:
            assert frozen[field] == q[field], ("question drift", slot, field)
        projection = question_by_slot[slot]
        assert set(projection) == {"slot", "core_id", "title", "question", "assumptions", "conventions"}
        assert all(projection[k] == q[k] for k in projection)
        reference = reference_by_slot[slot]
        assert reference["item_digest"] == digest(q)
        for field in ["reference_answer", "rubric", "boundary_cases", "common_errors", "reasoning_map"]:
            assert reference[field] == q[field]
        # This checks declared topology and bindings, not sufficiency of premises.
        reasoning = q["reasoning_map"]
        available = {x["id"] for x in reasoning["inputs"]}
        for step in reasoning["steps"]:
            assert step["id"] not in available
            assert set(step["required_inputs"]) <= available, (slot, step["id"], "dangling/forward dependency")
            assert step["claim"] and step["conclusion"]
            available.add(step["id"])
        report_path = P / "reviews" / (slot[0] + "-review.json")
        report = read(report_path)
        assert report["reviewer"] != q["author"]
        items = [x for x in report["items"] if x["core_id"] == q["core_id"]]
        assert len(items) == 1
        review = items[0]
        assert review["item_digest"] == digest(q) and review["payload_sha256_raw"] == sha(rooted(row["payload_path"]))
        assert review["reasoning"] and review["source_checks"]
        check_source_bindings(review["source_checks"])
        assert row["review"]["report_sha256"] == sha(report_path)
        proposal_path = rooted(row["proposal_path"])
        proposal_paths.add(str(proposal_path.relative_to(R)))
        proposal = read(proposal_path)
        contract = {k: q[k] for k in CONTRACT_FIELDS}
        assert proposal["proposed_contract"] == contract
        assert proposal["contract_hash"] == digest(contract)
        assert proposal["item_digest"] == digest(q)
        assert proposal["payload_sha256"] == sha(rooted(row["payload_path"]))
        assert proposal["core_id"] == q["core_id"] and proposal["admission"] == "candidate_not_counted"
    assert set(names) == actual_package | proposal_paths
    # A source checkout is required; repository files outside this package and its
    # six proposals must remain identical to the recorded base in tracked diffs.
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", baseline["base_commit"], "--"], cwd=R, text=True
    ).splitlines()
    permitted = set(names) | {str((P / "manifest.json").relative_to(R))}
    assert set(changed) <= permitted, ("outside-scope tracked changes", sorted(set(changed) - permitted))
    print(json.dumps({
        "status": "pass", "candidate_packets": 6, "admitted_cores": 0,
        "historical_files_preserved": len(baseline["previous_cohort"]["verified_files"]),
        "checks": ["manifest closure and raw hashes", "question/reference separation", "frozen questions",
                   "review payload digests and phase-1 seals", "proposed contracts", "source and graph identities",
                   "reasoning-map identifier topology", "historical preservation", "tracked-diff scope"],
        "limit": "Integrity and compatibility checks only; no mathematical truth, reviewer independence, admission or Lean certification."
    }, indent=2))


if __name__ == "__main__":
    main()
