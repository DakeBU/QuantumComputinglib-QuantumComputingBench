"""Fixed third cohort: permutations, Taylor jets and concrete workspace action."""
import qcb_course_expansion as preceding
from qcb_core import read_json
from qcb_course_batch import bind_review_input, qualify_candidate_batch
from qcb_course_expansion import PIPELINE_PATHS as PREVIOUS_PATHS
from qcb_graph_course_pilot import B, R, check_semantics, load_candidates
from qcb_integrity import text_sha

FIXTURE = B / "tracks/lean/fixtures/graph-course-v3.json"
EVIDENCE = B / "reports/lean-course-v3"
PLAN = B / "tracks/lean/curriculum/course-v3.json"
EXPECTED = frozenset({"qcb-core-be-110", "qcb-core-be-111", "qcb-core-be-102", "qcb-core-sp-101", "qcb-core-sp-104"})
AUTHORS = ("/root/course_permutation_third", "/root/course_jet_uniqueness_third", "/root/course_dirty_oracle_third")
PROFILE = {"batch_wall_seconds": 2700, "session_wall_seconds": 600,
           "check_seconds": 120, "control_wall_seconds": 180}
PREFIX = "benchmarks/quantumcomputingbench/"
# Keep all imported local Python files, not prior-cohort data never read in
# this reference command. Old receipt source maps retain their original set.
PIPELINE_PATHS = frozenset(p for p in PREVIOUS_PATHS if p.endswith(".py")) | frozenset(PREFIX + p for p in (
    "scripts/lean_course_v3.py", "src/qcb_course_batch.py", "src/qcb_course_third.py",
    "tracks/lean/fixtures/graph-course-v3.json", "tracks/lean/curriculum/course-v3.json",
    *("reports/lean-course-v3/" + n for n in ("comparison.json", "comparison-input.json", "permutation-decoder-input.json",
        "permutation-decoder.json", "jet-decoder-input.json", "jet-decoder.json", "oracle-decoder-input.json", "oracle-decoder.json")),
    "tracks/lean/fixtures/graph-course-v2.json",
    *("reports/lean-course-v3/legacy-v2/" + n for n in ("comparison.json", "comparison-input.json", "lcu-decoder-input.json",
                                                      "lcu-decoder.json", "conditioning-decoder-input.json", "conditioning-decoder.json"))))


def pipeline_identity():
    return {p: text_sha(R / p) for p in sorted(PIPELINE_PATHS)}


def candidates():
    loaded = load_candidates(fixture=FIXTURE, evidence_dir=EVIDENCE, expected_cores=EXPECTED, excluded_authors=AUTHORS)
    bind_review_input(FIXTURE, EVIDENCE, loaded[0], require_sanitized=True)
    return loaded


def qualified():
    cases, identity, catalog, graph = candidates()
    views, status = qualify_candidate_batch(cases, identity, EVIDENCE / "reference-checks.json", PROFILE, PIPELINE_PATHS)
    return views, status, catalog, graph


def check_preceding_alignment():
    """Fresh sanitized review of unchanged v2 roots; not another Lean replay."""
    cases, _, catalog, _ = preceding.candidates()
    evidence = EVIDENCE / "legacy-v2"
    check_semantics(read_json(preceding.FIXTURE), cases, {c["core_id"]: c for c in catalog["cores"]},
                    evidence_dir=evidence, excluded_authors=preceding.AUTHORS)
    bind_review_input(preceding.FIXTURE, evidence, cases, require_sanitized=True)
