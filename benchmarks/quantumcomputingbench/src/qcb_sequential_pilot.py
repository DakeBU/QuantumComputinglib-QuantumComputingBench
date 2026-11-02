"""Reviewed prospective proof-construction views over existing SP core IDs.

This sidecar does not alter the canonical catalog or promote a stable release.
The exact root conclusion has a blinded reconstruction and distinct comparison;
whole-question prose/method grading remains separate.
"""
from __future__ import annotations

import hashlib
import sys
from copy import deepcopy

from qcb_core import digest, read_json
from qcb_curriculum import core_contract, load_catalog
from qcb_integrity import text_sha
from qcb_obligation_pilot import B, R
from qcb_proof_session import UNIVERSE_TASK_SCHEMA, ProofSession, validate_task
from qcb_textbook_policy import check_source_bindings

FIXTURE = B / "tracks/lean/fixtures/sequential-pilot-v1.json"
EVIDENCE = B / "reports/lean-agentic-sequential-v1"
EXPECTED_CORES = {"qcb-core-sp-007", "qcb-core-sp-008"}
sys.path.insert(0, str(R / "website/scripts"))
from proof_inputs import proof_input_digest


def load_sequential_pilot():
    packet = read_json(FIXTURE)
    context, decoder, comparison, seal, audit = [read_json(EVIDENCE / (n + ".json"))
                                               for n in ("decoder-input", "decoder", "comparison", "statement-seal", "source-context-audit")]
    catalog, items, graph = load_catalog()
    if (packet["schema_version"] != "qcb.sequential_prospective_formal_views.v1"
            or packet["execution_class"] != "trusted_local_reference"
            or packet["catalog_hash"] != catalog["catalog_hash"] or comparison["catalog_hash"] != catalog["catalog_hash"]
            or packet["proof_inputs_sha256"] != proof_input_digest(R)
            or packet["lean_toolchain"] != (R / "lean-toolchain").read_text().strip()
            or packet["new_cores"] != 0 or packet["new_formal_views_admitted"] != 0
            or packet["isolated"] is not False or packet["model_predictions_executed"] is not False):
        raise ValueError("sequential fixture source/evidence policy drift")
    if (decoder["source_blind"] is not True or decoder["packet_digest"] != digest(context)
            or comparison["batch_digest"] != digest(packet) or comparison["decoder_digest"] != digest(decoder)
            or comparison["packet_digest"] != digest(context) or comparison["statement_seal_digest"] != digest(seal)
            or comparison["source_context_audit_digest"] != digest(audit)
            or len({packet["author"], decoder["decoder_identity"], comparison["reviewer"]}) != 3
            or comparison["source_blind"] is not False):
        raise ValueError("sequential semantic reviews do not bind distinct actual roles and exact context")
    candidates = packet["cases"]
    if len(candidates) != len(EXPECTED_CORES) or {c["core_id"] for c in candidates} != EXPECTED_CORES:
        raise ValueError("preserve both sealed sequential candidates")
    anonymous = {c["anonymous_id"]: c for c in context["views"]}
    reconstructed = {c["anonymous_id"]: c for c in decoder["views"]}
    decisions = {c["core_id"]: c for c in comparison["views"]}
    if len(anonymous) != 2 or len(reconstructed) != 2 or len(decisions) != 2:
        raise ValueError("sequential comparison coverage incomplete")
    core_map = {c["core_id"]: c for c in catalog["cores"]}
    cases = []
    for candidate in candidates:
        key = candidate["core_id"]
        item, core, decision = items[key], core_map[key], decisions[key]
        check_source_bindings([candidate["source_binding"]])
        if (candidate["assumptions_added"] or candidate["new_core_count"] != 0
                or candidate["formal_context"]["preamble"] != "universe u\nopen scoped BigOperators"
                or candidate["imports"] != candidate["formal_context"]["imports"]
                or any(candidate["binding"][k] != core[k]
                       for k in ("contract_hash", "item_digest", "family", "split", "snapshot_id"))
                or digest(core_contract(item)) != core["contract_hash"]
                or digest(item) != core["item_digest"]):
            raise ValueError("sequential candidate changed canonical assumptions, target context or split")
        node_ids = candidate["source_node_ids"] + candidate["source_supporting_node_ids"]
        if any(n not in graph for n in node_ids):
            raise ValueError("sequential candidate uses an unadmitted graph identity")
        formal = candidate["formal_context"]
        if (decision["verdict"] != "accept" or decision["question_contract_hash"] != core["contract_hash"]
                or decision["source_item_digest"] != core["item_digest"]
                or decision["formal_context_digest"] != digest(formal)
                or anonymous[decision["anonymous_id"]]["formal_context"] != formal
                or not reconstructed[decision["anonymous_id"]]["reconstructed_statement"]
                or hashlib.sha256(formal["target"].encode()).hexdigest() != candidate["signature_sha256"]):
            raise ValueError("exact sequential root is not covered by the semantic comparison")
        nodes = [{k: deepcopy(n[k]) for k in ("id", "target", "depends_on")} for n in candidate["nodes"]]
        root = next(n for n in nodes if n["id"] == candidate["root_id"])
        if root["target"] != formal["target"]:
            raise ValueError("sequential obligation root differs from the reviewed type")
        task = validate_task({"schema_version": UNIVERSE_TASK_SCHEMA, "universe_parameters": ["u"],
                              "core_id": key, "contract_hash": core["contract_hash"], "family": core["family"],
                              "split": core["split"], "snapshot_id": core["snapshot_id"],
                              "library_revision": packet["library_commit"], "imports": formal["imports"],
                              "question": item["question"], "assumptions": item["assumptions"],
                              "conventions": item["conventions"], "root_id": root["id"], "nodes": nodes,
                              "interfaces": candidate["interfaces"],
                              "alignment_status": "exact_root_semantic_alignment_reviewed; experimental_sidecar_not_canonical_formal_admission; whole_question_coverage_partial"})
        renames = {n["helper_name"]: "qcb_step_" + n["id"] for n in candidate["nodes"]}

        def rewrite(proof, names=renames):
            if not isinstance(proof, str) or not proof.startswith("by"):
                raise ValueError("expected a complete inspected authored proof body")
            for old, new in sorted(names.items(), key=lambda pair: -len(pair[0])):
                proof = proof.replace(old, new)
            if "QuantumComputingBench.SequentialMath." in proof:
                raise ValueError("unresolved sequential helper name")
            return proof

        references = {k: rewrite(p) for k, p in candidate["references"].items()}
        if set(references) != {n["id"] for n in nodes}:
            raise ValueError("each sequential node needs one exact authored reference")
        controls = {"library_control": rewrite(candidate["baseline_control"]["proof"]),
                    "constructed_whole_root": rewrite(candidate["independent_root_reference"])}
        wrong = deepcopy(candidate["wrong_reference"])
        wrong["proof"] = rewrite(wrong["proof"])
        if wrong["node_id"] != root["id"]:
            raise ValueError("this sequential repair probe is bound to the unchanged root")
        allowed = {k: [p] for k, p in references.items()}
        allowed[root["id"]].extend([*controls.values(), wrong["proof"]])
        cases.append({"task": task, "references": references, "controls": controls,
                      "wrong_reference": wrong, "allowed_proofs": allowed,
                      "library_control_one_call": candidate["baseline_control"]["one_call"],
                      "semantic_coverage": decision["whole_canonical_question_formal_coverage"]})
    return cases, {"catalog_hash": catalog["catalog_hash"], "fixture_digest": digest(packet),
                   "decoder_input_digest": digest(context), "decoder_digest": digest(decoder),
                   "comparison_digest": digest(comparison), "source_context_audit_digest": digest(audit),
                   "fixture_sha256_lf": text_sha(FIXTURE), "proof_inputs_sha256": packet["proof_inputs_sha256"],
                   "library_revision": packet["library_commit"], "lean_toolchain": packet["lean_toolchain"]}


def export_sequential(cases, identity):
    return {"schema_version": "qcb.sequential_proof_export.v1", **identity,
            "tasks": [ProofSession(c["task"]).agent_input() for c in cases],
            "distinct_mathematical_cores": len(cases), "new_mathematical_cores": 0,
            "new_canonical_formal_admissions": 0, "model_performance_measured": False, "blind_test": False,
            "candidate_execution": "blocked; use separately accepted isolation for untrusted outputs",
            "limitations": ["Experimental sidecar with exact-root semantic review; original references are public.",
                            "Whole-question proof-method and prose grading remains separate.",
                            "Normalized decoder displays are not byte-literal or executable verbatim; the display-only universe-v caveat is retained.",
                            "Provided DAG is not autonomous decomposition or measured proof-term depth."]}
