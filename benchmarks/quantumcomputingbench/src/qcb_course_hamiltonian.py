"""Source and receipt bindings for the Hamiltonian training companions."""
from qcb_core import digest, read_json
from qcb_course_batch import bind_review_input, qualify_candidate_batch
from qcb_graph_course_pilot import B, R, load_candidates
from qcb_integrity import text_sha

FIXTURE = B / "tracks/lean/fixtures/graph-course-hamiltonian-v1.json"
PLAN = B / "tracks/lean/curriculum/course-v5.json"
EVIDENCE = B / "reports/lean-course-hamiltonian-v1"
EXPECTED = {"qcb-core-be-011", "qcb-core-la-019"}
PROFILE = {"batch_wall_seconds": 3600, "session_wall_seconds": 600,
           "check_seconds": 120, "control_wall_seconds": 180}
PATHS = {
    *(B / "src" / name for name in (
        "qcb_course_hamiltonian.py", "qcb_course_batch.py", "qcb_graph_course_pilot.py",
        "qcb_authored_session.py", "qcb_reference_receipt.py", "qcb_proof_session.py",
        "qcb_core.py", "qcb_curriculum.py", "qcb_textbook_policy.py", "qcb_lean.py",
        "qcb_integrity.py", "qcb_evaluation_registry.py", "qcb_lean_course.py",
    )),
    B / "scripts/lean_course.py", B / "scripts/lean_course_v5.py", R / "website/scripts/proof_inputs.py",
    FIXTURE, PLAN,
    *(EVIDENCE / name for name in ("hamiltonian-decoder-input.json", "hamiltonian-decoder.json",
                                  "comparison-input.json", "comparison.json")),
}


def pipeline_identity():
    return {path.relative_to(R).as_posix(): text_sha(path) for path in sorted(PATHS)}


def candidates():
    cases, identity, catalog, graph = load_candidates(fixture=FIXTURE, evidence_dir=EVIDENCE,
                                                       expected_cores=EXPECTED)
    bind_review_input(FIXTURE, EVIDENCE, cases, require_sanitized=True)
    if any(case["task"]["split"] != "train" for case in cases):
        raise ValueError("Hamiltonian supervision requires existing train cores")
    return cases, identity, catalog, graph


def qualified():
    cases, identity, catalog, graph = candidates()
    views, status = qualify_candidate_batch(cases, identity, EVIDENCE / "reference-checks.json",
                                            PROFILE, set(pipeline_identity()))
    for case in cases:
        views[case["view_id"]]["formal_scope"] = case["semantic_coverage"]
    return views, status, catalog, graph


def reference_records():
    """Project only the exact standalone constructed control for each train core."""
    records = {}
    for case in read_json(FIXTURE)["cases"]:
        task = case["task"]
        root = next(node for node in task["nodes"] if node["id"] == task["root_id"])
        records[task["core_id"]] = {
            "proof": case["controls"]["constructed_whole_root"],
            "route": "constructed_whole_root",
            "method_disclosure": case["shortcut_disclosure"],
            "target": root["target"],
            "imports": task["imports"],
            "source": FIXTURE.relative_to(B).as_posix(),
            "source_digest": digest(case),
            "task_digest": digest(task),
        }
    return records
