"""Import the reviewed public geometry exercise packets into the workbook."""
from hashlib import sha256
import json
import re
import subprocess

from qcb_core import digest, read_json
from qcb_curriculum import core_contract

PACKAGE_ID = "b3a8eb51-c162-46a4-a117-021b837fe5c1"
CHAPTERS = {
    "rotation": ("local-rotations", "Local rotations and state preparation"),
    "cycles": ("phase-cycles", "Phases, permutations and cycle traces"),
}
SLOTS = {"G1s": "rotation", "G2s": "rotation", "G3s": "rotation",
         "C1s": "cycles", "C2s": "cycles", "C3s": "cycles"}
QUESTION_FIELDS = ("slot", "title", "question", "assumptions", "conventions")
GRADER_FIELDS = ("rubric", "reasoning_map", "common_errors", "boundary_cases",
                 "valid_alternatives", "difficulty")


def _by_slot(rows, expected=SLOTS.keys()):
    by_slot = {row["slot"]: row for row in rows}
    if len(by_slot) != len(rows) or set(by_slot) != expected:
        raise ValueError("geometry packet inventory differs")
    return by_slot


def _check_route(packet):
    anchors = set(packet["target_nodes"] + packet["supporting_nodes"])
    route = packet["reasoning_map"]
    seen = {}
    for node in route["nodes"]:
        if (node["id"] in seen or not node["claim"] or node["kind"] not in {"given", "derive"}
                or not set(node["requires"]) <= seen.keys() or not set(node["anchors"]) <= anchors):
            raise ValueError("geometry reasoning route has an invalid node or prerequisite")
        seen[node["id"]] = set(node["requires"])
    for join in route["joins"]:
        inputs = set(join["necessary_inputs"])
        if len(inputs) < 2 or not join["why_each"] or not inputs <= seen.get(join["node"], set()):
            raise ValueError("geometry reasoning join has invalid required inputs")


def load(catalog, graph):
    from qcb_nonlean_workbook import B, R, FROZEN, band, question_sha, repository_path, sha

    package = B / "tracks/non-lean/packages" / PACKAGE_ID
    review_path = B / "reports/nonlean-intake-20261114/intake.json"
    manifest = read_json(package / "manifest.json")
    intake = read_json(review_path)
    snapshot = manifest["snapshot"]
    if (manifest["schema_version"] != "qcb.nonlean_intake_manifest.v1"
            or manifest["visibility"] != "public_study" or manifest["package_id"] != PACKAGE_ID
            or manifest["package_path"] != package.relative_to(R).as_posix()
            or manifest["catalog_hash"] != catalog["catalog_hash"]
            or snapshot["id"] != catalog["snapshot_id"] or snapshot["source_commit"] != FROZEN
            or sha(repository_path(snapshot["path"])) != snapshot["sha256"]
            or manifest["new_cores_admitted"] != 0 or manifest["existing_contract_views"] != 0
            or manifest["distinct_packet_count"] != len(SLOTS)
            or any(manifest[k] is not False for k in ("human_approval", "new_Lean_execution", "model_responses_collected"))
            or intake["manifest_sha256"] != sha(package / "manifest.json")
            or intake["schema_version"] != "qcb.nl_geometry_intake.v1"
            or intake["visibility"] != "public_study_only" or intake["official_splits_assigned"] != 0
            or intake["canonical_cores_added"] != 0
            or set(intake["items"]) != SLOTS.keys()):
        raise ValueError("geometry package, graph or public-study scope changed")

    files = {}
    for row in manifest["files"]:
        path = repository_path(row["path"])
        if path in files or path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
            raise ValueError("geometry contribution bytes changed: " + row["path"])
        files[path] = row["sha256"]
    inventory = {p for p in package.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    inventory.update(repository_path(row["proposal_path"]) for row in manifest["packets"])
    if set(files) != inventory - {package / "manifest.json"}:
        raise ValueError("geometry manifest inventory differs")

    questions, references, grader = (
        _by_slot([json.loads(line) for line in (package / name).read_text(encoding="utf-8").splitlines()])
        for name in ("questions-only.jsonl", "references.jsonl", "grader-metadata.jsonl"))
    review_index = _by_slot(read_json(package / "review-index.json")["items"])
    frozen_sources = {}
    entries, proposals = [], []
    for slot, row in _by_slot(manifest["packets"]).items():
        payload = package / "qa" / (slot + ".json")
        question_path = package / "questions" / (slot + ".json")
        packet, frozen = read_json(payload), read_json(question_path)
        core, item = packet["core_id"], digest(packet)
        common = {"slot": slot, "core_id": core, "item_digest": item}
        review = row["review"]
        early_path = repository_path(review["phase1_path"])
        late_path = repository_path(review["report_path"])
        early, late = read_json(early_path), read_json(late_path)
        siblings = {key for key in SLOTS if key[0] == slot[0]}
        paired = _by_slot(early["items"], siblings)[slot]
        final = _by_slot(late["items"], siblings)[slot]
        seal_path = late_path.parent / "phase1-seal.json"
        seal = read_json(seal_path)
        authorized = any(
            auth["payloads"].get(slot) == files[payload]
            and auth["phase1_sha256"] == files[early_path]
            and auth["phase1_seal_sha256"] == files[seal_path]
            for auth in map(read_json, late_path.parent.glob("phase2-authorization*.json")))
        annotation = intake["items"][slot]
        use = packet["proposed_use"]
        if (repository_path(row["payload_path"]) != payload or repository_path(row["frozen_question_path"]) != question_path
                or set(frozen) != set(QUESTION_FIELDS) or any(packet[k] != frozen[k] for k in QUESTION_FIELDS)
                or packet["slot"] != slot or row["core_id"] != core or row["item_digest"] != item
                or row["question_sha256"] != files[question_path] or row["payload_sha256"] != files[payload]
                or packet["split"] != "unassigned_pending_reconciliation" or packet["admission"] != "candidate_not_counted"
                or packet["contribution_type"] != "new_candidate" or packet["dedup_review_required"] is not True
                or use["status"] != "public_study_only" or use["empirical_calibration"] is not False
                or packet["snapshot_id"] != catalog["snapshot_id"]
                or core != "candidate:" + packet["proposal_id"] or questions[slot] != {**frozen, "core_id": core}
                or references[slot] != {**common, "question_file_sha256": files[question_path],
                                         "reference_answer": packet["reference_answer"]}
                or grader[slot] != {**common, **{k: packet[k] for k in GRADER_FIELDS}}):
            raise ValueError("geometry original, split or exact exports differ: " + slot)
        if (review != review_index[slot] or review["payload_sha256"] != files[payload]
                or review["item_digest"] != item or review["question_sha256"] != files[question_path]
                or review["phase1_sha256"] != files[early_path] or review["report_sha256"] != files[late_path]
                or late["phase1_sha256"] != files[early_path]
                or seal["phase1_sha256"] != files[early_path] or seal["question_hashes"][slot] != files[question_path]
                or not authorized
                or not early["reviewer"] == late["reviewer"] == review["reviewer"]
                or late["reviewer"] == packet["author"] or late["human_approval"] is not False
                or paired["question_sha256"] != files[question_path] or not paired["derivation"]
                or final["verdict"] != "accept" or final["payload_sha256_raw"] != files[payload]
                or final["item_digest"] != item or not final["reasoning"] or not final["rubric_assessment"]
                or annotation["verdict"] != "accept" or annotation["question_sha256"] != files[question_path]
                or annotation["payload_sha256"] != files[payload] or not annotation["reasoning"]
                or not annotation["limitations"] or annotation["reviewer"] in {packet["author"], late["reviewer"]}):
            raise ValueError("geometry mathematical review differs: " + slot)
        anchors = set(packet["target_nodes"] + packet["supporting_nodes"])
        covered = set()
        for ref in packet["source_refs"]:
            path = ref["path"]
            if ref["source_commit"] != FROZEN or not re.fullmatch(r"QuantumBlockEncoding/(?:\w+/)*\w+\.lean", path):
                raise ValueError("invalid geometry source binding")
            if path not in frozen_sources:
                raw = subprocess.check_output(["git", "show", FROZEN + ":" + path], cwd=R)
                frozen_sources[path] = raw.replace(b"\r\n", b"\n")
            blob = frozen_sources[path]
            if sha256(blob).hexdigest() != ref["sha256_lf"]:
                raise ValueError("pinned geometry source changed: " + path)
            lines = blob.splitlines(keepends=True)
            for span in ref["declaration_spans"]:
                node = graph[span["node_id"]]
                first, last = span["start"], span["end"]
                if (node["source"] != path or node["line"] != first
                        or not 1 <= first <= last <= len(lines)
                        or sha256(b"".join(lines[first - 1:last])).hexdigest() != span["sha256_lf"]):
                    raise ValueError("geometry graph and source span differ")
                covered.add(span["node_id"])
        if not packet["target_nodes"] or covered != anchors:
            raise ValueError("geometry graph anchors lack exact declaration spans")
        rubric = packet["rubric"]
        if (sum(r["weight"] for r in rubric) != 10 or len({r["id"] for r in rubric}) != len(rubric)
                or any(r["weight"] <= 0 or not r["criterion"] or not r["partial"] for r in rubric)):
            raise ValueError("geometry rubric must provide weighted partial credit")
        _check_route(packet)
        proposal_path = repository_path(row["proposal_path"])
        proposal = read_json(proposal_path)
        contract = core_contract(packet)
        if (proposal["proposed_contract"] != contract or proposal["core_id"] != core
                or proposal["item_digest"] != item or proposal["contract_hash"] != digest(contract)
                or proposal["source_nodes"] != packet["target_nodes"] + packet["supporting_nodes"]
                or row["contract_hash"] != digest(contract) or proposal["split"] != packet["split"]):
            raise ValueError("geometry proposal differs from the reviewed mathematical core")
        proposals.append(proposal)
        entries.append({"slot": slot, "chapter": SLOTS[slot], "view_id": f"qcb-supplementary-{slot.lower()}-b3a8eb51",
                        "band": band(packet), "packet": packet, "payload_path": row["payload_path"],
                        "payload_sha256": files[payload], "question_sha256": question_sha(packet),
                        "review": {"report_path": review_path.relative_to(R).as_posix(),
                                   "limitations": annotation["limitations"]},
                        "notation": {"equations": []}, "clarifications": annotation,
                        "display_reasoning_map": packet["reasoning_map"], "display_rubric": rubric})
    return entries, proposals
