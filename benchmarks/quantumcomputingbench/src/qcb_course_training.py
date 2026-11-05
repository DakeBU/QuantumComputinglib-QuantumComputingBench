"""Train-only formal supervision from qualified public authored references.

These examples teach the disclosed routes under full imports. They are not
private holdouts, internal model thoughts, or inferred positive PRM labels.
"""
from copy import deepcopy

from qcb_core import digest, read_json
from qcb_graph_course_pilot import B
from qcb_obligation_pilot import load_pilot
from qcb_proof_session import ProofSession, proof_sha
from qcb_sequential_pilot import load_sequential_pilot

FIXTURES = (
    "obligation-pilot-v1.json", "sequential-pilot-v1.json", "graph-course-v1.json",
    "graph-course-v2.json", "graph-course-v3.json", "graph-course-v4.json",
)


def reference_records():
    """Evaluator-owned fixed paths, never a caller-selected reference corpus."""
    rows = {}
    for name in FIXTURES:
        path = B / "tracks/lean/fixtures" / name
        packet = read_json(path)
        raw_cases = packet["cases"]
        raw_by_core = {c.get("task", c)["core_id"]: c for c in raw_cases}
        if len(raw_by_core) != len(raw_cases):
            raise ValueError("duplicate authored root in training source corpus")
        if name in {"obligation-pilot-v1.json", "sequential-pilot-v1.json"}:
            # Legacy qualification reconstructs canonical tasks and rewrites
            # authored helper names before its recorded proof checks. Export
            # those exact bound controls, never the raw pre-normalization text.
            loader = load_pilot if name == "obligation-pilot-v1.json" else load_sequential_pilot
            cases, identity = loader()
            if (identity["fixture_digest"] != digest(packet) or len(cases) != len(raw_cases)
                    or {c["task"]["core_id"] for c in cases} != set(raw_by_core)):
                raise ValueError("bound training references differ from their exact source corpus")
        else:
            cases = raw_cases
        for case in cases:
            task = case["task"]
            core = task["core_id"]
            if core in rows:
                raise ValueError("duplicate authored root in training source corpus")
            nodes = task["nodes"]
            root = task["root_id"]
            controls = case["controls"]
            constructed = controls.get("constructed_whole_root")
            library = controls.get("library_control", controls.get("library_application"))
            proof = constructed if constructed is not None else library
            if not isinstance(proof, str) or not proof.startswith("by"):
                raise ValueError("training needs a standalone checked whole-root reference")
            rows[core] = {"proof": proof, "route": "constructed_whole_root" if constructed is not None else "library_application",
                          "method_disclosure": case.get("shortcut_disclosure", "A standalone control packages the proof; it does not enforce a proof method. Imported facts and root shortcuts remain callable."),
                          "target": next(n["target"] for n in nodes if n["id"] == root),
                          "imports": task["imports"], "source": path.relative_to(B).as_posix(),
                          "source_digest": digest(raw_by_core[core]), "task_digest": digest(task)}
    return rows


def export_training(views, qualification, records):
    """No split override: dev/public-test proofs cannot enter this projection."""
    examples = []
    for key, view in sorted(views.items()):
        task = view["task"]
        if task["split"] != "train":
            continue
        source = records[task["core_id"]]
        target = next(n["target"] for n in task["nodes"] if n["id"] == task["root_id"])
        if (view["entry"]["task_hash"] != digest(task) or source["target"] != target
                or source["imports"] != task["imports"]
                or source["task_digest"] != digest(task)):
            raise ValueError("training reference is not the qualified task's exact root")
        examples.append({"schema_version": "qcb.lean_training_example.v1", "view_id": key,
                         **{k: task[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")},
                         "task_hash": digest(task), "registry_digest": qualification["registry_digest"],
                         "input": ProofSession(task, mode="root_only", exposure="approved_interface").agent_input(),
                         "target": {"node_id": task["root_id"], "proof": source["proof"],
                                    "proof_sha256": proof_sha(source["proof"]), "route": source["route"],
                                    "method_disclosure": source["method_disclosure"]},
                         "provenance": {"source": source["source"], "source_digest": source["source_digest"],
                                        "recorded_reference_lineage": deepcopy(view["reference_lineage"])},
                         "reference_public": True, "whole_question_prose_kernel_certified": False,
                         "process_reward_labels": None, "model_performance_measured": False})
    if not examples or len({e["core_id"] for e in examples}) != len(examples):
        raise ValueError("expected unique existing train cores")
    return {"schema_version": "qcb.lean_training_export.v1", "suite_id": qualification["suite_id"],
            "registry_digest": qualification["registry_digest"], "split": "train", "examples": examples,
            "distinct_shared_cores": len(examples), "new_mathematical_cores": 0,
            "dev_and_test_references_projected": False, "training_launched": False,
            "difficulty_empirically_calibrated": False, "blind_test": False}
