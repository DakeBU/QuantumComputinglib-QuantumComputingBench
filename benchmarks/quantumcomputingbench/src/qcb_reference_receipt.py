"""Strict recorded-authored-reference structure; no certificate authentication.

These checks reject contradictory policy and freshness metadata. Actual Lean
execution and source-aware review remain external evidence, not consequences of
a valid JSON object or identity string.
"""
import re
from copy import deepcopy

from qcb_core import digest
from qcb_lean import APPROVED_AXIOMS
from qcb_proof_session import proof_sha


def validate_course_receipt(report, cases, identity, expected_pipeline_paths):
    try:
        _validate(report, cases, identity, expected_pipeline_paths)
    except (KeyError, TypeError, AttributeError, IndexError) as error:
        raise ValueError("malformed authored-reference receipt") from error
    return report


def _validate(report, cases, identity, expected_pipeline_paths):
    payload = deepcopy(report)
    claimed = payload.pop("receipt_digest", None)
    if (report.get("schema_version") != "qcb.graph_course_reference_replay.v1" or digest(payload) != claimed
            or report.get("passed") is not True or report.get("execution_class") != "trusted_local_authored_reference"
            or any(report.get(k) is not False for k in ("isolated", "model_performance_measured", "blind_test", "standalone_controls_are_completed_protocol_sessions"))
            or any(type(report.get(k)) is not int or report[k] != 0 for k in ("model_calls", "new_mathematical_cores", "new_canonical_formal_admissions"))
            or any(report.get(k) != value for k, value in identity.items())):
        raise ValueError("authored-reference receipt policy, content or identity drift")
    if not isinstance(report.get("tested_code_commit"), str) or not re.fullmatch(r"[0-9a-f]{40}", report["tested_code_commit"]):
        raise ValueError("recorded source commit required")
    sources = report.get("pipeline_source_hashes_lf")
    if (not isinstance(sources, dict) or set(sources) != set(expected_pipeline_paths)
            or any(not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v) for v in sources.values())):
        raise ValueError("the complete versioned reference pipeline map is required")
    rows = report.get("results")
    expected = {c["task"]["core_id"]: c for c in cases}
    if (not isinstance(rows, list) or len(rows) != len(expected)
            or {r["core_id"] for r in rows} != set(expected)):
        raise ValueError("exact course reference coverage required")
    execution_ids, request_hashes = set(), set()

    def check_evidence(value, proof, *, positive, sorry_control=False, node=False):
        fields = {"status", "failure_class", "request_hash", "proof_sha256", "execution_id", "kernel_checked", "axioms"}
        if node:
            fields.add("node_id")
        if not isinstance(value, dict) or set(value) != fields:
            raise ValueError("complete bounded reference evidence fields required")
        axioms = value["axioms"]
        if (not isinstance(axioms, list) or len(axioms) > 64 or any(not isinstance(a, str) for a in axioms)
                or len(set(axioms)) != len(axioms)):
            raise ValueError("axioms must be an actual bounded list of distinct names")
        if (value["proof_sha256"] != proof_sha(proof)
                or not isinstance(value["request_hash"], str) or not re.fullmatch(r"[0-9a-f]{64}", value["request_hash"])
                or not isinstance(value["execution_id"], str) or not re.fullmatch(r"[0-9a-f]{32}", value["execution_id"])):
            raise ValueError("reference request/proof/execution binding is malformed")
        if value["request_hash"] in request_hashes or value["execution_id"] in execution_ids:
            raise ValueError("each actual check and final replay requires distinct execution/request identities")
        request_hashes.add(value["request_hash"]);execution_ids.add(value["execution_id"])
        if positive:
            if (value["status"] != "verified" or value["failure_class"] is not None
                    or value["kernel_checked"] is not True or set(axioms) - APPROVED_AXIOMS):
                raise ValueError("positive reference lacks policy-qualified kernel evidence")
        elif (value["status"] != "compile_error" or value["failure_class"] != "IMPLEMENTATION_FAILED"
              or value["kernel_checked"] is not False
              or sorry_control and ("sorryAx" not in axioms or set(axioms) - APPROVED_AXIOMS - {"sorryAx"})
              or not sorry_control and axioms):
            raise ValueError("negative type/axiom control cannot claim a positive kernel result")

    for row in rows:
        case = expected[row["core_id"]];task = case["task"]
        if row.get("passed") is not True or row.get("task_hash") != digest(task):
            raise ValueError("root reference has wrong task binding or failed status")
        positives = row["positive_obligations"]
        if (not isinstance(positives, list) or len(positives) != len(case["references"])
                or {p["node_id"] for p in positives} != set(case["references"])):
            raise ValueError("all and only provided obligations must be checked")
        for evidence in positives:
            check_evidence(evidence, case["references"][evidence["node_id"]], positive=True, node=True)
        for field, proofs in (("controls", case["controls"]), ("negative_controls", case["negative_controls"])):
            if not isinstance(row[field], dict) or set(row[field]) != set(proofs):
                raise ValueError("exact standalone and negative control coverage required")
            for key, proof in proofs.items():
                check_evidence(row[field][key], proof, positive=field == "controls", sorry_control=key == "sorry_axiom")
        check_evidence(row["final_replay"], case["references"][task["root_id"]], positive=True)
