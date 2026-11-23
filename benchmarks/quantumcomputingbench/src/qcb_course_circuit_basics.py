"""Source and review bindings for the circuit-foundations course cohort."""
from qcb_core import digest, read_json
from qcb_course_batch import bind_review_input, qualify_candidate_batch
from qcb_graph_course_pilot import B, R, load_candidates
from qcb_integrity import text_sha
from website.scripts.proof_inputs import lean_module_targets, proof_input_digest

FIXTURE = B / "tracks/lean/fixtures/graph-course-circuit-basics-v1.json"
PLAN = B / "tracks/lean/curriculum/course-v7.json"
EVIDENCE = B / "reports/lean-course-circuit-basics-v1"
EXPECTED_SPLITS = {"qcb-core-la-004": "test_public", "qcb-core-la-007": "dev",
                   "qcb-core-la-017": "train", "qcb-core-la-018": "train"}
AUTHORS = {"register_linearity": "/root/foundations_register_linearity_author",
           "reversible": "/root/foundations_reversible_author"}
GROUPS = {"qcb-core-la-004": "register_linearity", "qcb-core-la-007": "register_linearity",
          "qcb-core-la-017": "reversible", "qcb-core-la-018": "reversible"}
EXPECTED = set(EXPECTED_SPLITS)
PROFILE = {"batch_wall_seconds": 3600, "session_wall_seconds": 600,
           "check_seconds": 120, "control_wall_seconds": 180}
PATHS = {
    *(B / "src" / name for name in (
        "qcb_course_circuit_basics.py", "qcb_course_batch.py", "qcb_graph_course_pilot.py",
        "qcb_authored_session.py", "qcb_reference_receipt.py", "qcb_proof_session.py",
        "qcb_core.py", "qcb_curriculum.py", "qcb_textbook_policy.py", "qcb_lean.py",
        "qcb_integrity.py", "qcb_evaluation_registry.py", "qcb_lean_course.py",
    )),
    B / "scripts/lean_course.py", B / "scripts/lean_course_v7.py", R / "website/scripts/proof_inputs.py",
    FIXTURE, PLAN,
    *(EVIDENCE / (group + suffix) for group in AUTHORS for suffix in ("-decoder-input.json", "-decoder.json")),
    *(EVIDENCE / name for name in ("comparison-input.json", "comparison.json",
                                  "source-and-exposure-review.json", "library-gate.json")),
}


def pipeline_identity():
    return {path.relative_to(R).as_posix(): text_sha(path) for path in sorted(PATHS)}


def _validate_cases(cases):
    if len(cases) != len(EXPECTED) or {case["task"]["core_id"] for case in cases} != EXPECTED:
        raise ValueError("circuit foundations require exactly the four existing selected cores")
    for case in cases:
        task = case["task"]
        core = task["core_id"]
        if (task["split"] != EXPECTED_SPLITS[core]
                or case["semantic_evidence"]["group"] != GROUPS[core]
                or case["author_identity"] != AUTHORS[GROUPS[core]]):
            raise ValueError("circuit foundations changed the source split or author/group identity")


def candidates():
    cases, identity, catalog, graph = load_candidates(fixture=FIXTURE, evidence_dir=EVIDENCE,
                                                       expected_cores=EXPECTED, excluded_authors=tuple(AUTHORS.values()))
    _validate_cases(cases)
    gate = read_json(EVIDENCE / "library-gate.json")
    modules = lean_module_targets(R)
    expected_commands = [["lake", "build"], ["lake", "build", "Tests"]]
    expected_commands += [["lake", "build", *modules[i:i+40]] for i in range(0, len(modules), 40)]
    if (gate.get("passed") is not True or gate.get("commit") != identity["library_revision"]
            or gate.get("proofInputsSha256") != proof_input_digest(R) or gate.get("compiledModules") != modules
            or [result["argv"] for result in gate["executionResults"]] != expected_commands
            or any(result["exit_code"] != 0 for result in gate["executionResults"])):
        raise ValueError("circuit foundations require the exact passed pinned library build/test gate")
    review = read_json(EVIDENCE / "source-and-exposure-review.json")
    if (review.get("schema_version") != "qcb.independent_source_and_public_exposure_review.v1"
            or review.get("reviewer_identity") != "foundations_question_and_exposure_review"
            or review["source_identity"]["catalog_hash"] != catalog["catalog_hash"]
            or review["exposure_and_evidence_boundary"]["new_author_drafts_seen"] is not False
            or review["exposure_and_evidence_boundary"]["unseen_family_independence_demonstrated"] is not False):
        raise ValueError("circuit foundations require the exact independent public-source review scope")
    reviewed = {row["core_id"]: row for row in review["items"]}
    if len(review["items"]) != len(EXPECTED) or set(reviewed) != EXPECTED:
        raise ValueError("source review must cover the exact cohort")
    for case in cases:
        task = case["task"]
        row = reviewed[task["core_id"]]
        if (row["item_digest"] != case["source_item_digest"]
                or row["contract_hash"] != task["contract_hash"]
                or row["source_split"] != task["split"]):
            raise ValueError("independent source review refers to changed core mathematics")
    bind_review_input(FIXTURE, EVIDENCE, cases, require_sanitized=True)
    return cases, identity, catalog, graph


def qualified():
    cases, identity, catalog, graph = candidates()
    views, status = qualify_candidate_batch(cases, identity, EVIDENCE / "reference-checks.json",
                                            PROFILE, set(pipeline_identity()))
    for case in cases:
        views[case["view_id"]]["formal_scope"] = case["semantic_coverage"]
    return views, status, catalog, graph


def reference_records():
    """Project only existing train-core reference bodies, never dev/test bodies."""
    cases = read_json(FIXTURE)["cases"]
    _validate_cases(cases)
    records = {}
    for case in cases:
        task = case["task"]
        if task["split"] != "train":
            continue
        root = next(node for node in task["nodes"] if node["id"] == task["root_id"])
        proof = case["controls"]["constructed_whole_root"]
        if not isinstance(proof, str) or not proof.startswith("by"):
            raise ValueError("training requires a standalone constructed whole-root reference")
        records[task["core_id"]] = {
            "proof": proof, "route": "constructed_whole_root",
            "method_disclosure": case["shortcut_disclosure"],
            "target": root["target"], "imports": task["imports"],
            "source": FIXTURE.relative_to(B).as_posix(),
            "source_digest": digest(case), "task_digest": digest(task),
        }
    return records
