"""Task-bound Lean curriculum; course order is not a model-difficulty score.

Coverage counts reviewed task anchors in a frozen inventory. Provided proof
obligations, source construction and actual Lean proof-term dependencies remain
different graphs. This module never executes Lean or publishes an admission.
"""
from collections import Counter
from copy import deepcopy

from qcb_core import digest
from qcb_proof_session import ProofSession, validate_task

BANDS = {
    "D1": "Statement, assumptions and disclosed library application",
    "D2": "Local symbolic construction and finite entry/sum reasoning",
    "D3": "Composition across mathematical interfaces with all AND premises",
    "D4": "Parametric induction or representation/factorization argument",
}
SKILLS = {"statement_understanding", "premise_selection", "library_application", "finite_sum_algebra",
          "matrix_entry_algebra", "unitary_closure", "tensor_lift", "induction", "representation_bridge",
          "rank_factorization", "diagnostic_repair"}
SPLIT_ORDER = {"train": 0, "dev": 1, "test_public": 2}


def topology(task):
    """Only the supplied AND-obligation graph; no inferred semantic proof depth."""
    task = validate_task(task)
    nodes = {n["id"]: n for n in task["nodes"]}
    children = {key: set() for key in nodes}
    for key, node in nodes.items():
        for parent in node["depends_on"]:
            children[parent].add(key)
    depths, pending = {}, set(nodes)
    while pending:
        for key in list(pending):
            parents = nodes[key]["depends_on"]
            if all(p in depths for p in parents):
                depths[key] = 1 + max((depths[p] for p in parents), default=0)
                pending.remove(key)
    ancestors = {}
    for key in sorted(nodes, key=depths.get):
        ancestors[key] = {key}.union(*(ancestors[p] for p in nodes[key]["depends_on"]))
    reconvergent = any(ancestors[a] & ancestors[b] and a not in ancestors[b] and b not in ancestors[a] for node in nodes.values()
                       for i, a in enumerate(node["depends_on"]) for b in node["depends_on"][i+1:])
    tags = []
    if len(nodes) == 1:
        tags.append("single_root")
    else:
        if all(len(n["depends_on"]) <= 1 and len(children[k]) <= 1 for k, n in nodes.items()):
            tags.append("chain")
        if any(len(n["depends_on"]) > 1 for n in nodes.values()):
            tags.append("and_fan_in")
        if any(len(c) > 1 for c in children.values()):
            tags.append("shared_prerequisite")
        if reconvergent:
            tags.append("reconvergent_diamond")
    return {"evidence_class": "evaluator_supplied_AND_obligation_graph", "tags": tags,
            "obligation_nodes": len(nodes), "obligation_edges": sum(len(n["depends_on"]) for n in nodes.values()),
            "longest_obligation_chain_nodes": depths[task["root_id"]],
            "is_lean_proof_term_dependency_graph": False, "is_semantic_reasoning_depth": False}


def validate_course(plan, views, catalog, graph):
    if (plan.get("schema_version") != "qcb.lean_course.v1" or plan.get("catalog_hash") != catalog["catalog_hash"]
            or plan.get("snapshot_id") != catalog["snapshot_id"] or plan.get("difficulty_status") != "provisional_author_mathematical_assessment"
            or plan.get("measured_model_difficulty") is not None or plan.get("blind_test") is not False
            or plan.get("prerequisite_edge_kind") != "pedagogical_not_theorem_dependency"
            or plan.get("new_mathematical_cores") != 0 or plan.get("canonical_formal_admissions_changed") is not False):
        raise ValueError("course source/difficulty/admission policy drift")
    entries = plan.get("entries")
    if (not isinstance(entries, list) or not entries or {e.get("view_id") for e in entries} != set(views)
            or len(entries) != len(views) or len({e.get("core_id") for e in entries}) != len(entries)):
        raise ValueError("course must cover each registered view exactly once with unique shared cores")
    cores = {c["core_id"]: c for c in catalog["cores"]}
    by_core = {e["core_id"]: e for e in entries}
    for entry in entries:
        task = validate_task(views[entry["view_id"]]["task"])
        core = cores[entry["core_id"]]
        if (any(entry[k] != core[k] or task[k] != core[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id"))
                or entry["task_hash"] != digest(task) or entry["source_item_digest"] != core["item_digest"]):
            raise ValueError("course entry changed its mathematical identity or split")
        difficulty = entry["difficulty"]
        if (set(difficulty) != {"construction_band", "rationale", "imported_shortcut", "measured_model_difficulty"}
                or difficulty["construction_band"] not in BANDS or not isinstance(difficulty["rationale"], str)
                or not difficulty["rationale"].strip() or not isinstance(difficulty["imported_shortcut"], str)
                or not difficulty["imported_shortcut"].strip() or difficulty["measured_model_difficulty"] is not None):
            raise ValueError("difficulty needs a substantive provisional rationale and shortcut disclosure")
        if (not isinstance(entry["skills"], list) or not entry["skills"] or len(set(entry["skills"])) != len(entry["skills"])
                or set(entry["skills"]) - SKILLS or entry["topology"] != topology(task)):
            raise ValueError("course skill or supplied-topology metadata drift")
        anchors = entry["source_node_ids"]
        if (not isinstance(anchors, list) or not anchors or len(set(anchors)) != len(anchors)
                or set(anchors) - set(core["target_nodes"] + core["supporting_nodes"])):
            raise ValueError("course anchors must belong to its frozen shared core")
        for key in anchors:
            node = graph[key]
            if (node.get("kind") != "declaration" or node.get("open_obligation") is not False
                    or node.get("inventory_status") != "Compiled"):
                raise ValueError("planned or uncompiled inventory nodes cannot become verified task anchors")
        parents = entry["prerequisite_core_ids"]
        if (not isinstance(parents, list) or len(set(parents)) != len(parents)
                or entry["core_id"] in parents or set(parents) - by_core.keys()):
            raise ValueError("unknown, duplicate or self prerequisite")
        for parent in parents:
            prior = by_core[parent]
            if (SPLIT_ORDER[prior["split"]] > SPLIT_ORDER[entry["split"]]
                    or prior["difficulty"]["construction_band"] > difficulty["construction_band"]):
                raise ValueError("course prerequisite leaks a later split or reverses the declared curriculum band")
    done, pending = set(), set(by_core)
    while pending:
        ready = {k for k in pending if set(by_core[k]["prerequisite_core_ids"]) <= done}
        if not ready:
            raise ValueError("course prerequisite cycle")
        done |= ready
        pending -= ready
    return deepcopy(plan)


def coverage(plan, views, catalog, graph):
    plan = validate_course(plan, views, catalog, graph)
    entries = plan["entries"]
    targets = {node for e in entries for node in e["source_node_ids"]}
    modules = {graph[node]["source"] for node in targets}
    return {"schema_version": "qcb.lean_course_coverage.v1", "course_digest": digest(plan),
            "catalog_hash": catalog["catalog_hash"], "snapshot_id": catalog["snapshot_id"],
            "distinct_shared_cores": len(entries), "registered_views": len(views), "new_mathematical_cores": 0,
            "by_construction_band": dict(Counter(e["difficulty"]["construction_band"] for e in entries)),
            "by_split": dict(Counter(e["split"] for e in entries)),
            "by_part": dict(Counter(next(c["part"] for c in catalog["cores"] if c["core_id"] == e["core_id"]) for e in entries)),
            "by_skill": dict(Counter(s for e in entries for s in e["skills"])),
            "by_supplied_topology_tag": dict(Counter(t for e in entries for t in e["topology"]["tags"])),
            "task_anchor_node_ids": sorted(targets), "task_anchor_node_count": len(targets),
            "task_anchor_source_files": sorted(modules), "task_anchor_source_file_count": len(modules),
            "snapshot_declaration_inventory_count": sum(n.get("kind") == "declaration" for n in graph.values()),
            "inventory_denominator_is_verified_question_capacity": False,
            "node_wide_source_semantic_debt_cleared": False, "model_performance_measured": False,
            "difficulty_empirically_calibrated": False, "global_semantic_dedup_complete": False,
            "isolated_candidate_execution": "ENV_BLOCKED"}


def export_course(plan, views, catalog, graph, *, split=None, band=None, mode="proof_dag", exposure="approved_interface"):
    plan = validate_course(plan, views, catalog, graph)
    if split not in {None, *SPLIT_ORDER} or band not in {None, *BANDS}:
        raise ValueError("unknown course split or band")
    selected = [e for e in plan["entries"] if (split is None or e["split"] == split)
                and (band is None or e["difficulty"]["construction_band"] == band)]
    if not selected:
        raise ValueError("course selection contains no qualified task")
    pending = {e["core_id"]: e for e in selected}
    selected_ids, selected, done = set(pending), [], set()
    while pending:
        ready = [e for e in pending.values() if set(e["prerequisite_core_ids"]) & selected_ids <= done]
        first = min(ready, key=lambda e: (e["difficulty"]["construction_band"], e["core_id"]))
        selected.append(first)
        done.add(first["core_id"])
        del pending[first["core_id"]]
    tasks = [{"view_id": e["view_id"], "construction_band": e["difficulty"]["construction_band"],
              "prerequisite_core_ids": list(e["prerequisite_core_ids"]),
              "prerequisites_outside_selection": sorted(set(e["prerequisite_core_ids"]) - selected_ids),
              "input": ProofSession(views[e["view_id"]]["task"], mode=mode, exposure=exposure).agent_input()}
             for e in selected]
    return {"schema_version": "qcb.lean_course_export.v1", "course_digest": digest(plan), "tasks": tasks,
            "distinct_shared_cores": len(tasks), "new_mathematical_cores": 0, "reference_answers_projected": False,
            "difficulty_empirically_calibrated": False, "blind_test": False, "model_performance_measured": False,
            "candidate_execution": "disabled; accepted isolation required"}
