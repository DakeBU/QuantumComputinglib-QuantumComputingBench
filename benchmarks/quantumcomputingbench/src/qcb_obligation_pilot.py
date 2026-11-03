"""Fixed authored engineering cohort; not a new admission or a hidden test.

The loader owns the only fixture path. No candidate can choose a JSON file,
write a reference allowlist, change a split, or provide verifier receipts.
"""
from __future__ import annotations

import hashlib
import sys
from copy import deepcopy
from pathlib import Path

from qcb_core import digest, read_json
from qcb_curriculum import core_contract, load_catalog
from qcb_proof_session import TASK_SCHEMA, ProofSession, validate_task

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
FIXTURE = B / "tracks/lean/fixtures/obligation-pilot-v1.json"
EXPECTED_CORES = {"qcb-core-sp-005", "qcb-core-la-102"}
sys.path.insert(0, str(R / "website/scripts"))
from proof_inputs import proof_input_digest


def _lf_sha(path):
    return hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest()


def bind_cases(packet, catalog, items, *, source_root=R):
    """Bind authored fixture roots to the current independently reviewed catalog.

    This checks identity/source/shape, not semantic approval of new obligations.
    Callers must review changed fixture code before trusted local execution.
    """
    if (packet.get("schema_version") != "qcb.evaluator_owned_proof_dag_pilot.v1"
            or packet["catalog_hash"] != catalog["catalog_hash"]
            or packet["isolated"] is not False or packet["model_performance_measured"] is not False
            or packet["new_cores"] != 0 or packet["new_formal_views_admitted"] != 0):
        raise ValueError("pilot identity/evidence policy changed; review required")
    if (packet["proof_inputs_sha256"] != proof_input_digest(source_root)
            or packet["lean_toolchain"] != (source_root / "lean-toolchain").read_text().strip()):
        raise ValueError("pilot production input/toolchain identity drift")
    if {c["core_id"] for c in packet["cases"]} != EXPECTED_CORES or len(packet["cases"]) != len(EXPECTED_CORES):
        raise ValueError("fixed pilot cohort must preserve both existing roots")
    core_map = {c["core_id"]: c for c in catalog["cores"]}
    bound, seen = [], set()
    for case in packet["cases"]:
        key = case["core_id"]
        if key in seen or key not in core_map:
            raise ValueError("duplicate or unadmitted pilot core")
        seen.add(key)
        core, item = core_map[key], items[key]
        if (digest(item) != core["item_digest"] or digest(core_contract(item)) != core["contract_hash"]
                or any(case["binding"][k] != core[k]
                       for k in ("contract_hash", "item_digest", "family", "split", "snapshot_id"))):
            raise ValueError("pilot binding differs from canonical item, contract or split")
        view = core.get("views", {}).get("lean", {})
        if (view.get("status") != "reference_and_alignment_checked"
                or view.get("view_id") != case["native_formal_view_id"]
                or view.get("formal_context", {}).get("imports") != case["imports"]):
            raise ValueError("pilot imports/root must retain an admitted native view")
        nodes = [{k: deepcopy(n[k]) for k in ("id", "target", "depends_on")} for n in case["nodes"]]
        roots = [n for n in nodes if n["id"] == case["root_id"]]
        if len(roots) != 1 or roots[0]["target"] != view["formal_context"]["target"]:
            raise ValueError("pilot may not change the admitted root target")
        for source in case["source_bindings"]:
            path = (source_root / source["path"]).resolve()
            if not path.is_relative_to(source_root.resolve()) or _lf_sha(path) != source["sha256_lf"]:
                raise ValueError("pilot production source binding drift")
        if packet["preamble"] != "open scoped BigOperators" or case["preamble"] != packet["preamble"]:
            raise ValueError("unreviewed proof preamble")
        task = validate_task({"schema_version": TASK_SCHEMA, "core_id": key,
                              "contract_hash": core["contract_hash"], "family": core["family"],
                              "split": core["split"], "snapshot_id": core["snapshot_id"],
                              "library_revision": packet["source_commit"], "imports": case["imports"],
                              "question": item["question"], "assumptions": item["assumptions"],
                              "conventions": item["conventions"], "root_id": case["root_id"], "nodes": nodes,
                              "interfaces": case["interfaces"],
                              "alignment_status": "existing_root_reviewed; provided_obligation_decomposition_experimental"})
        # Names in the inspected authoring packet are rewritten deterministically
        # into the protocol namespace; these exact transformed bodies are replayed.
        renames = {n["helper_name"]: "qcb_step_" + n["id"] for n in case["nodes"]}

        def rewrite(proof, names=renames):
            if not isinstance(proof, str) or not proof.startswith("by\n") and not proof.startswith("by "):
                raise ValueError("expected a complete inspected authored proof body")
            for old, new in sorted(names.items(), key=lambda pair: -len(pair[0])):
                proof = proof.replace(old, new)
            if "QuantumComputingBench.PilotMath." in proof:
                raise ValueError("unresolved authored helper name")
            return proof

        if set(case["references"]) != {n["id"] for n in nodes}:
            raise ValueError("each obligation needs exactly one authored reference")
        references = {k: rewrite(v) for k, v in case["references"].items()}
        wrong = deepcopy(case["wrong_reference"])
        wrong["proof"] = rewrite(wrong["proof"])
        if wrong["node_id"] not in references or rewrite(wrong["repair_proof"]) != references[wrong["node_id"]]:
            raise ValueError("repair must return to the same fixed obligation")
        if next(n for n in nodes if n["id"] == wrong["node_id"])["depends_on"]:
            raise ValueError("this pilot's authored negative control must be a leaf")
        controls = {"library_application": rewrite(case["baseline_control"]["proof"]),
                    "constructed_whole_root": rewrite(case["independent_root_reference"])}
        allowed = {k: [v] for k, v in references.items()}
        allowed[wrong["node_id"]].append(wrong["proof"])
        allowed[task["root_id"]].extend(controls.values())
        bound.append({"task": task, "references": references, "wrong_reference": wrong,
                      "controls": controls, "allowed_proofs": allowed,
                      "operator_metadata": deepcopy(case)})
    return bound


def load_pilot():
    packet = read_json(FIXTURE)
    catalog, items, _ = load_catalog()
    cases = bind_cases(packet, catalog, items)
    return cases, {"fixture_sha256_lf": _lf_sha(FIXTURE), "fixture_digest": digest(packet),
                   "catalog_hash": catalog["catalog_hash"], "proof_inputs_sha256": packet["proof_inputs_sha256"],
                   "library_revision": packet["source_commit"], "lean_toolchain": packet["lean_toolchain"]}


def pipeline_identity():
    paths = [B / "src" / name for name in ("qcb_proof_session.py", "qcb_authored_session.py",
                                          "qcb_obligation_pilot.py", "qcb_lean.py", "qcb_core.py",
                                          "qcb_curriculum.py")]
    paths += [B / "scripts/proof_session.py", R / "website/scripts/proof_inputs.py", FIXTURE]
    return {path.relative_to(R).as_posix(): _lf_sha(path) for path in paths}


def export_pilot(cases, identity):
    return {"schema_version": "qcb.proof_obligation_export.v1", **identity,
            "tasks": [ProofSession(c["task"]).agent_input() for c in cases],
            "distinct_mathematical_cores": len(cases), "new_mathematical_cores": 0,
            "blind_test": False, "model_performance_measured": False,
            "candidate_execution": "blocked; reference smoke is a separate authored-only command",
            "boundaries": ["Public authored engineering cohort, not hidden evaluation.",
                           "Provided obligation DAG does not assess autonomous decomposition.",
                           "Existing imported root lemmas remain callable in every condition.",
                           "Kernel checks do not grade natural-language explanations."]}
