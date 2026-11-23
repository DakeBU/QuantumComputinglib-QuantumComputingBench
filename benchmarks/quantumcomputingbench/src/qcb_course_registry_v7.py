"""Fixed v7 selection; preserve historical evaluation fingerprints."""
import sys
from copy import deepcopy

from qcb_core import digest
from qcb_graph_course_pilot import B, R
from qcb_integrity import text_sha
from qcb_lean_course import validate_course

SUITE_ID = "qcb-lean-graph-course-v7"
CORE_COUNT = 29


def _load_current_course():
    sys.path.insert(0, str(B / "scripts"))
    from lean_course_v7 import load_course
    return load_course()


def load_course_registry():
    return _registry_from_qualified_course(_load_current_course())


def _registry_from_qualified_course(source):
    """Internal reuse of an already qualified course in the same publication."""
    plan, source_views, catalog, graph, report = source
    validate_course(plan, source_views, catalog, graph)
    if (plan["course_id"] != SUITE_ID or len(plan["entries"]) != CORE_COUNT
            or report["course_digest"] != digest(plan)
            or report["distinct_shared_cores"] != CORE_COUNT
            or "reference_qualification" not in report):
        raise ValueError("v7 registry requires the complete qualified 29-core v7 course")
    for key, view in source_views.items():
        entry, task = view["entry"], view["task"]
        if (entry["view_id"] != key or entry["task_hash"] != digest(task)
                or any(entry[k] != task[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id"))):
            raise ValueError("v7 registry entry differs from its qualified task")
    paths = (B / "src/qcb_course_registry_v7.py", B / "scripts/evaluate_course_v7.py",
             B / "scripts/lean_course_v7.py", B / "scripts/lean_training_v7.py", B / "scripts/course_task_v7.py")
    sources = {path.relative_to(R).as_posix(): text_sha(path) for path in paths}
    identity = {"course_digest": digest(plan), "qualification_digest": digest(report["reference_qualification"]),
                "task_hashes": {key: view["entry"]["task_hash"] for key, view in sorted(source_views.items())},
                "selection_sources_sha256_lf": sources}
    registry_digest = digest(identity)
    views = deepcopy(source_views)
    for entry in plan["entries"]:
        view = views[entry["view_id"]]
        view["entry"]["registration_scope"] = "reference_qualified_experimental_course; supplied_plan; explanations_separately_graded"
        view["entry"]["construction_band"] = entry["difficulty"]["construction_band"]
        view["registry_digest"] = registry_digest
    return views, {"schema_version": "qcb.course_registry_qualification.v1", "suite_id": SUITE_ID,
                   "registry_digest": registry_digest, "catalog_hash": catalog["catalog_hash"], **identity,
                   "qualified_views": len(views), "distinct_shared_core_ids": CORE_COUNT,
                   "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0,
                   "live_formal_certificates_issued": 0, "validation_performed_lean_replay": False,
                   "blind_test": False, "model_performance_measured": False,
                   "isolated_model_evaluation": "ENV_BLOCKED",
                   "qualification_scope": "Recorded authored evidence; no live model result or stable-release claim"}
