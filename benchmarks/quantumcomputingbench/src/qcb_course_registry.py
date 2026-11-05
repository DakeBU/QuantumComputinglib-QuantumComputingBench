"""Expose qualified course companions to the existing bounded agent loop.

The pilot remains a separate frozen suite. A course registration qualifies its
recorded reference, never a model answer or an isolated execution backend.
"""
import sys
from copy import deepcopy

from qcb_core import digest
from qcb_graph_course_pilot import B, R
from qcb_integrity import text_sha
from qcb_lean_course import validate_course


def _load_current_course():
    sys.path.insert(0, str(B / "scripts"))
    from lean_course_v4 import load_course
    return load_course()


def load_course_registry():
    plan, source_views, catalog, graph, report = _load_current_course()
    validate_course(plan, source_views, catalog, graph)
    if (report["course_digest"] != digest(plan)
            or report["distinct_shared_cores"] != len(plan["entries"])
            or "reference_qualification" not in report):
        raise ValueError("course registry requires the complete qualified course")
    # Pin the selection adapter as well as the exact already-qualified tasks.
    paths = [B / "src/qcb_course_registry.py", B / "scripts/evaluate_agentic.py"]
    sources = {p.relative_to(R).as_posix(): text_sha(p) for p in paths}
    identity = {"course_digest": digest(plan), "qualification_digest": digest(report["reference_qualification"]),
                "task_hashes": {k: v["entry"]["task_hash"] for k, v in sorted(source_views.items())},
                "selection_sources_sha256_lf": sources}
    registry_digest = digest(identity)
    views = deepcopy(source_views)
    for entry in plan["entries"]:
        view = views[entry["view_id"]]
        view["entry"]["registration_scope"] = (
            "reference_qualified_experimental_course; supplied_plan; explanations_separately_graded")
        view["entry"]["construction_band"] = entry["difficulty"]["construction_band"]
        view["registry_digest"] = registry_digest
    return views, {"schema_version": "qcb.course_registry_qualification.v1", "suite_id": plan["course_id"],
                   "registry_digest": registry_digest, "catalog_hash": catalog["catalog_hash"], **identity,
                   "qualified_views": len(views), "distinct_shared_core_ids": len(plan["entries"]),
                   "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0,
                   "live_formal_certificates_issued": 0, "validation_performed_lean_replay": False,
                   "blind_test": False, "model_performance_measured": False,
                   "isolated_model_evaluation": "ENV_BLOCKED",
                   "qualification_scope": "Recorded authored evidence; no live model result or stable-release claim"}
