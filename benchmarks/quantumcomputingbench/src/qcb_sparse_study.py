"""Validate the owner-only sparse-access study against its public commitments."""
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

from qcb_assessment_protocol import _index
from qcb_assessment_v3 import _committed, study_contract
from qcb_core import digest, read_json
from qcb_curriculum import load_catalog
from qcb_integrity import text_sha
from qcb_learning_reference import REFERENCE_PROFILE, validate_reference_results
from qcb_learning_validity import B, R, challenge_task

SEAL = B / "tracks/lean/assessment-sparse-v1/seal.json"
QUALIFICATION = B / "reports/assessment-sparse-v1/qualification.json"
FILES = frozenset({"cohort.json", "neutral-questions.json", "authored-reference-private.json",
                   "reasoning-routes-private.json", "question-first-input.json",
                   "question-first-review.json", "decoder-input.json", "decoder.json",
                   "source-review.json", "exposure-audit.json"})
CHECKS = {"positive": 8, "fresh_final_roots": 4, "expected_rejections": 2, "total": 10}
GROUP = "banded_sparse_address_semantics"


def pipeline_identity():
    paths = [SEAL, B / "scripts/sparse_assessment.py", R / "website/scripts/proof_inputs.py"]
    paths.extend(B / "src" / name for name in (
        "qcb_sparse_study.py", "qcb_sparse_study_reference.py", "qcb_learning_reference.py",
        "qcb_assessment_v3.py", "qcb_learning_validity.py", "qcb_assessment_protocol.py",
        "qcb_authored_session.py", "qcb_proof_session.py", "qcb_lean.py",
        "qcb_core.py", "qcb_integrity.py", "qcb_curriculum.py",
    ))
    return {path.relative_to(R).as_posix(): text_sha(path) for path in paths}


def load_seal():
    seal = read_json(SEAL)
    if (set(seal) != {"schema_version", "cohort_digest", "private_files_sha256",
                      "probe_count", "contrast_count", "source_group", "formal_scope",
                      "public_source_exposure", "canonical_admissions_changed"}
            or seal["schema_version"] != "qcb.sparse_assessment_seal.v1"
            or seal["probe_count"] != 4 or seal["contrast_count"] != 2
            or seal["source_group"] != GROUP or seal["formal_scope"] != "decision_polarity_only"
            or seal["public_source_exposure"] != "available; pretraining_exposure_unknown"
            or seal["canonical_admissions_changed"] is not False
            or set(seal["private_files_sha256"]) != FILES
            or not all(re.fullmatch("[0-9a-f]{64}", s) for s in
                       [seal["cohort_digest"], *seal["private_files_sha256"].values()])):
        raise ValueError("expected fixed metadata-only sparse assessment seal")
    return seal


def validate_qualification(seal=None):
    seal = load_seal() if seal is None else seal
    q = read_json(QUALIFICATION)
    if (set(q) != {"schema_version", "seal_digest", "private_receipt_digest", "source_commit",
                   "checks", "execution_class", "isolated", "model_calls"}
            or q["schema_version"] != "qcb.sparse_assessment_qualification.v1"
            or q["seal_digest"] != digest(seal) or q["checks"] != CHECKS
            or q["execution_class"] != "trusted_local_authored_reference"
            or q["isolated"] is not False or q["model_calls"] != 0
            or not re.fullmatch("[0-9a-f]{64}", q["private_receipt_digest"])):
        raise ValueError("missing or stale sparse assessment qualification")
    _committed(pipeline_identity(), q["source_commit"])
    return q


def _documents(directory, files):
    result = {}
    for name, expected in files.items():
        path = directory / name
        if path.resolve().parent != directory or path.stat().st_size > 32_000_000:
            raise ValueError("unsafe private assessment artifact")
        raw = path.read_bytes()
        if sha256(raw).hexdigest() != expected:
            raise ValueError("private assessment artifact changed: " + name)
        result[name] = json.loads(raw)
    return result


def _review_binding(docs, probes):
    neutral = docs["neutral-questions.json"]
    authored = docs["authored-reference-private.json"]
    question_input = docs["question-first-input.json"]
    question_review = docs["question-first-review.json"]
    decoder_input, decoder = docs["decoder-input.json"], docs["decoder.json"]
    source_review = docs["source-review.json"]
    neutral_rows = neutral["probes"]
    roles = {authored["author_identity"], decoder["decoder_identity"],
             question_review["reviewer_identity"], source_review["reviewer_identity"]}
    if (len(roles) != 4 or not all(isinstance(role, str) and role.strip() for role in roles)
            or decoder["source_blind"] is not True or decoder["packet_digest"] != digest(decoder_input)
            or source_review["source_blind"] is not False
            or source_review["neutral_digest"] != digest(neutral)
            or source_review["authored_digest"] != digest(authored)
            or source_review["decoder_digest"] != digest(decoder)
            or decoder_input["views"] != [
                {"anonymous_id": f"N{i}", "formal_context": row["formal_context"]}
                for i, row in enumerate(neutral_rows, 1)]
            or [row["anonymous_id"] for row in decoder["views"]] != [
                row["anonymous_id"] for row in decoder_input["views"]]):
        raise ValueError("review roles or exact neutral contexts changed")
    projected = {row["probe_id"]: row for row in question_input}
    first = {row["probe_id"]: row for row in question_review["items"]}
    reviewed = source_review["rows"]
    if (len(question_input) != len(probes) or len(first) != len(question_review["items"])
            or set(projected) != set(probes) or set(first) != set(probes) or set(reviewed) != set(probes)):
        raise ValueError("each sparse question must have one independent review")
    for row in neutral_rows:
        probe_id = row["probe_id"]
        probe = probes[probe_id]
        if (any(probe[key] != row[key] for key in ("question", "assumptions", "conventions", "formal_context",
                                                   "source_nodes", "pair_id"))
                or any(projected[probe_id][key] != row[key] for key in ("question", "assumptions", "conventions"))
                or first[probe_id]["decision"] != probe["gold"]["decision"]
                or reviewed[probe_id]["verdict"] != "accept"
                or any(not isinstance(reviewed[probe_id][key], str) or not reviewed[probe_id][key].strip()
                       for key in ("reasoning", "rubric_review", "route_review"))):
            raise ValueError("sparse question, formal target, or independent verdict differs")


def load_private_bank(directory, *, require_qualified=True):
    directory = Path(directory).resolve()
    if directory.is_relative_to(R):
        raise ValueError("private assessment must stay outside the public checkout")
    seal = load_seal()
    docs = _documents(directory, seal["private_files_sha256"])
    packet, authored = docs["cohort.json"], docs["authored-reference-private.json"]
    probes = _index(packet)
    source = packet["source_bindings"]
    if (packet["schema_version"] != "qcb.sparse_assessment_cohort.v1"
            or digest(packet) != seal["cohort_digest"] or len(probes) != seal["probe_count"]
            or packet["probes"] != authored["probes"] or source != authored["source_bindings"]
            or packet["study_cores"] != authored["study_core_index"]
            or packet["snapshot_id"] != authored["snapshot_id"]
            or packet["library_revision"] != authored["library_revision"]
            or len({tuple(p["formal_context"]["imports"]) for p in probes.values()}) != 1
            or len({p["pair_id"] for p in probes.values()}) != seal["contrast_count"]):
        raise ValueError("private cohort does not match the frozen sparse study")
    _committed({row["path"]: row["sha256_lf"] for row in source}, authored["source_commit"])
    catalog, _, graph = load_catalog()
    if packet["snapshot_id"] != catalog["snapshot_id"]:
        raise ValueError("sparse assessment requires its exact graph snapshot")
    source_paths = {row["path"] for row in source}
    for probe in probes.values():
        parent = "candidate:" + probe["probe_id"]
        if (probe["split"] != "test_public" or probe["cluster_id"] != GROUP
                or probe["parent_core_ids"] != [parent]
                or probe["parent_contracts"] != {parent: digest(study_contract(probe, source))}
                or any(graph[node]["inventory_status"] != "Compiled" or graph[node]["open_obligation"]
                       or graph[node]["source"] not in source_paths for node in probe["source_nodes"])):
            raise ValueError("sparse probe lost its private core or compiled source binding")
        for belief in ("holds", "refuted"):
            challenge_task(probe, belief, snapshot_id=packet["snapshot_id"], library_revision=packet["library_revision"])
    _review_binding(docs, probes)
    if (authored["neutral_packet_sha256_raw"] != seal["private_files_sha256"]["neutral-questions.json"]
            or docs["question-first-review.json"]["input_sha256_raw"]
            != seal["private_files_sha256"]["question-first-input.json"]):
        raise ValueError("reviewed input bytes changed")
    if require_qualified:
        q = validate_qualification(seal)
        receipt = read_json(directory / "reference-checks.json")
        if (digest(receipt) != q["private_receipt_digest"] or receipt["seal_digest"] != digest(seal)
                or receipt["tested_code_commit"] != q["source_commit"]
                or receipt["pipeline_source_hashes_lf"] != pipeline_identity()
                or receipt["profile"] != REFERENCE_PROFILE or receipt["passed"] is not True):
            raise ValueError("sparse reference receipt is stale")
        validate_reference_results(packet, receipt["results"])
    return packet, seal


def current_commit():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip()
