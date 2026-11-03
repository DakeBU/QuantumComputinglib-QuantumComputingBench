"""Evaluator-owned second cohort; frozen version-1 evidence stays unchanged."""
from copy import deepcopy

from qcb_core import digest, read_json
from qcb_evaluation_registry import _source_lineage
from qcb_graph_course_pilot import B, R, load_candidates
from qcb_integrity import text_sha
from qcb_reference_receipt import validate_course_receipt

FIXTURE = B / "tracks/lean/fixtures/graph-course-v2.json"
EVIDENCE = B / "reports/lean-course-v2"
PLAN = B / "tracks/lean/curriculum/course-v2.json"
EXPECTED = frozenset({"qcb-core-be-106", "qcb-core-be-112", "qcb-core-sp-113", "qcb-core-sp-120"})
AUTHORS = ("/root/course_lcu_next", "/root/course_conditioning_next")
PROFILE = {"batch_wall_seconds": 2100, "session_wall_seconds": 450,
           "check_seconds": 120, "control_wall_seconds": 180}
PREFIX = "benchmarks/quantumcomputingbench/"
# The receipt cannot choose a smaller cohort, source map, or runtime profile.
PIPELINE_PATHS = frozenset(PREFIX + p for p in (
    *("scripts/" + n for n in ("lean_course.py", "lean_course_v2.py", "check_references.py", "nl_qa.py", "qcb.py", "release.py")),
    "tracks/lean/fixtures/graph-course-v2.json", "tracks/lean/curriculum/course-v2.json",
    *("src/" + n for n in ("qcb_course_expansion.py", "qcb_graph_course_pilot.py", "qcb_lean_course.py",
                            "qcb_proof_session.py", "qcb_authored_session.py", "qcb_core.py", "qcb_curriculum.py",
                            "qcb_lean.py", "qcb_integrity.py", "qcb_reference_receipt.py", "qcb_textbook_policy.py",
                            "qcb_evaluation_registry.py", "qcb_formal_views.py", "qcb_migration.py", "qcb_model_loop.py",
                            "qcb_nl.py", "qcb_nl_release_policy.py", "qcb_obligation_pilot.py", "qcb_runner.py",
                            "qcb_sequential_pilot.py", "qcb_snapshot.py")),
    *("reports/lean-course-v2/" + n for n in ("comparison.json", "comparison-input.json", "lcu-decoder-input.json",
                                           "conditioning-decoder-input.json", "lcu-decoder.json", "conditioning-decoder.json")))) | {"website/scripts/proof_inputs.py"}


def pipeline_identity():
    return {p: text_sha(R / p) for p in sorted(PIPELINE_PATHS)}


def candidates():
    comparison = read_json(EVIDENCE / "comparison.json")
    inputs = read_json(EVIDENCE / "comparison-input.json")
    if (inputs.get("schema_version") != "qcb.course_semantic_comparison_input.v1"
            or comparison.get("comparison_input_digest") != digest(inputs)
            or inputs.get("candidate_batch_digest") != digest(read_json(FIXTURE))
            or any(inputs.get(k) != comparison.get(k) for k in ("candidate_batch_digest", "packet_digests", "decoder_digests"))):
        raise ValueError("second-cohort source-aware review must bind its actual bounded comparison input")
    return load_candidates(fixture=FIXTURE, evidence_dir=EVIDENCE, expected_cores=EXPECTED, excluded_authors=AUTHORS)


def qualified():
    cases, identity, catalog, graph = candidates()
    report = read_json(EVIDENCE / "reference-checks.json")
    validate_course_receipt(report, cases, identity, PIPELINE_PATHS)
    if report.get("authored_reference_profile") != PROFILE:
        raise ValueError("second cohort requires its exact disclosed authored-only runtime profile")
    lineage = _source_lineage(report["tested_code_commit"], report["pipeline_source_hashes_lf"])
    views = {}
    for case in cases:
        task = case["task"]
        entry = {"view_id": case["view_id"], "task_hash": digest(task),
                 "allowed_modes": ["root_only", "proof_dag"], "allowed_exposures": ["closed_book", "approved_interface"],
                 **{k: task[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")}}
        views[case["view_id"]] = {"entry": entry, "task": task, "registry_digest": identity["fixture_digest"], "reference_lineage": lineage}
    return views, {"qualified_course_companions": len(views), "new_mathematical_cores": 0,
                   "new_canonical_formal_admissions": 0, "model_performance_measured": False,
                   "authored_reference_profile": deepcopy(PROFILE), "reference_lineage": lineage}, catalog, graph
