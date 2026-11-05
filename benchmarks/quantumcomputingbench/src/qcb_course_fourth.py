"""Fourth authored cohort: interval restriction and phase-aware loading.

Qualification reads exact evidence. It never executes a submitted proof or
changes the canonical mathematical registry or formal admission frontier.
"""
import hashlib

from qcb_core import digest, read_json
from qcb_course_batch import bind_review_input, qualify_candidate_batch
from qcb_course_third import PIPELINE_PATHS as PREVIOUS_PATHS
from qcb_graph_course_pilot import B, R, load_candidates
from qcb_integrity import text_sha

FIXTURE = B / "tracks/lean/fixtures/graph-course-v4.json"
EVIDENCE = B / "reports/lean-course-v4"
PLAN = B / "tracks/lean/curriculum/course-v4.json"
EXPECTED = frozenset({"qcb-core-sp-110", "qcb-core-be-101", "qcb-core-be-104"})
AUTHORS = ("/root/lean_course_analytic_fourth", "/root/lean_course_oracle_fourth", "/root")
PROFILE = {"batch_wall_seconds": 3600, "session_wall_seconds": 600,
           "check_seconds": 120, "control_wall_seconds": 180}
PREFIX = "benchmarks/quantumcomputingbench/"
PIPELINE_PATHS = frozenset(p for p in PREVIOUS_PATHS if p.endswith(".py")) | frozenset(PREFIX + p for p in (
    "scripts/lean_course_v4.py", "src/qcb_course_fourth.py",
    "tracks/lean/fixtures/graph-course-v4.json", "tracks/lean/curriculum/course-v4.json",
    *("reports/lean-course-v4/" + n for n in (
        "comparison.json", "comparison-input.json", "analytic-decoder-input.json",
        "analytic-decoder.json", "oracle-decoder-input.json", "oracle-decoder.json",
        "diagnostics/oracle-full-decoder-input.json", "diagnostics/oracle-full-decoder.json",
        "diagnostics/analytic-full-decoder-input.json", "diagnostics/analytic-full-decoder.json",
        "diagnostics/four-view-comparison-input.json", "diagnostics/four-view-comparison.json",
        "diagnostics/four-candidate-fixture.json"))))


def pipeline_identity():
    return {p: text_sha(R / p) for p in sorted(PIPELINE_PATHS)}


def candidates():
    check_decoder_projection("analytic")
    check_decoder_projection("oracle")
    check_review_projection()
    loaded = load_candidates(fixture=FIXTURE, evidence_dir=EVIDENCE,
                             expected_cores=EXPECTED, excluded_authors=AUTHORS)
    bind_review_input(FIXTURE, EVIDENCE, loaded[0], require_sanitized=True)
    return loaded


def _archive_binding(projection, full_input, full_output, original, decoded):
    for key, path, value in (("full_input", full_input, original), ("full_output", full_output, decoded)):
        binding = projection.get(key, {})
        if (binding.get("path") != path.relative_to(R).as_posix()
                or binding.get("canonical_sha256") != digest(value)
                or binding.get("raw_sha256") != hashlib.sha256(path.read_bytes()).hexdigest()):
            raise ValueError("diagnostic archive differs from its sealed bytes")


def check_decoder_projection(group):
    """Excluded reconstructions are preserved without gaining course admission."""
    selected, excluded = {"analytic": (["A1"], ["A2"]), "oracle": (["O4A", "O4B"], ["O4C"])}[group]
    context = read_json(EVIDENCE / (group + "-decoder-input.json"))
    decoder = read_json(EVIDENCE / (group + "-decoder.json"))
    full_input = EVIDENCE / ("diagnostics/" + group + "-full-decoder-input.json")
    full_output = EVIDENCE / ("diagnostics/" + group + "-full-decoder.json")
    original, decoded = read_json(full_input), read_json(full_output)
    projection = context.get("projection", {})
    if (projection.get("kind") != "selected_projection_of_same_formal_only_reconstruction"
            or projection.get("new_blind_review") is not False or projection.get("compiler_evidence") is not False
            or projection.get("selected_anonymous_ids") != selected
            or projection.get("excluded_anonymous_ids") != excluded
            or decoder.get("projection") != projection
            or decoded.get("packet_digest") != digest(original)
            or decoder.get("packet_digest") != digest(context)
            or decoder.get("decoder_identity") != decoded.get("decoder_identity")
            or context.get("views") != [v for v in original["views"] if v["anonymous_id"] in selected]
            or decoder.get("views") != [v for v in decoded["views"] if v["anonymous_id"] in selected]):
        raise ValueError("selection must preserve exact full reconstruction and diagnostic boundary")
    _archive_binding(projection, full_input, full_output, original, decoded)


def check_review_projection():
    """Retain the real rejected alignment and all unchanged accepted verdicts."""
    inputs = read_json(EVIDENCE / "comparison-input.json")
    report = read_json(EVIDENCE / "comparison.json")
    full_input = EVIDENCE / "diagnostics/four-view-comparison-input.json"
    full_output = EVIDENCE / "diagnostics/four-view-comparison.json"
    original, reviewed = read_json(full_input), read_json(full_output)
    previous_fixture = read_json(EVIDENCE / "diagnostics/four-candidate-fixture.json")
    fixture = read_json(FIXTURE)
    projection = report.get("prior_review_projection", {})
    selected = ["qcb-core-sp-110", "qcb-core-be-101", "qcb-core-be-104"]
    if (projection.get("kind") != "selected_projection_of_same_source_aware_review"
            or projection.get("new_mathematical_review") is not False
            or projection.get("row_adapter") != "reasoning_is_paragraph_join_of_original_substantive_reasoning"
            or projection.get("selected_core_ids") != selected
            or projection.get("excluded_core_ids") != ["qcb-core-sp-116"]
            or reviewed.get("comparison_input_digest") != digest(original)
            or reviewed.get("candidate_batch_digest") != digest(previous_fixture)
            or report.get("comparison_input_digest") != digest(inputs)
            or report.get("candidate_batch_digest") != digest(fixture)
            or report.get("reviewer") != reviewed.get("reviewer")
            or report.get("views") != [{**v, "reasoning": "\n\n".join(v["substantive_reasoning"])}
                                      for v in reviewed["views"] if v["core_id"] in selected]
            or not any(v["core_id"] == "qcb-core-sp-116" and v["verdict"] == "reject" for v in reviewed["views"])
            or fixture != {**previous_fixture, "cases": [c for c in previous_fixture["cases"] if c["task"]["core_id"] in selected]}):
        raise ValueError("selected review must preserve the full rejected/accepted source history")
    before = {v["core_id"]: v for v in original["views"]}
    if len(inputs["views"]) != len(selected) or {v["core_id"] for v in inputs["views"]} != set(selected):
        raise ValueError("source review projection changed selected core coverage")
    for row in inputs["views"]:
        # Only the decoder wrapper records the admission-only selection.
        if {k: v for k, v in row.items() if k != "ambient_context"} != {k: v for k, v in before[row["core_id"]].items() if k != "ambient_context"}:
            raise ValueError("source review projection altered a mathematical row")
    _archive_binding(projection, full_input, full_output, original, reviewed)


def qualified():
    cases, identity, catalog, graph = candidates()
    views, status = qualify_candidate_batch(cases, identity, EVIDENCE / "reference-checks.json",
                                            PROFILE, PIPELINE_PATHS)
    for case in cases:
        views[case["view_id"]]["formal_scope"] = case["semantic_coverage"]
    return views, status, catalog, graph
