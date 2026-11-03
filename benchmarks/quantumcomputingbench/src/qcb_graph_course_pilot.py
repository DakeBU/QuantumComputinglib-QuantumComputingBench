"""Source/review-bound graph-course candidates and authored reference qualification."""
import sys
from copy import deepcopy
from pathlib import Path

from qcb_core import digest, read_json
from qcb_curriculum import load_catalog
from qcb_evaluation_registry import _source_lineage
from qcb_integrity import text_sha
from qcb_proof_session import validate_task
from qcb_reference_receipt import validate_course_receipt
from qcb_textbook_policy import check_source_bindings

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
FIXTURE = B / "tracks/lean/fixtures/graph-course-v1.json"
EVIDENCE = B / "reports/lean-course-v1"
RECEIPT = EVIDENCE / "reference-checks.json"
EXPECTED = {"qcb-core-be-105", "qcb-core-be-107", "qcb-core-be-109", "qcb-core-sp-114", "qcb-core-sp-009"}
PREFIX = "benchmarks/quantumcomputingbench/"
# Version-1 execution inputs, not the later qualification reader. These exact
# paths retain their recorded Git revisions after reader-only hardening.
REFERENCE_PIPELINE_PATHS = {PREFIX + name for name in (
    "scripts/lean_course.py", "tracks/lean/fixtures/graph-course-v1.json", "tracks/lean/curriculum/course-v1.json",
    *("src/" + n for n in ("qcb_graph_course_pilot.py", "qcb_lean_course.py", "qcb_proof_session.py", "qcb_authored_session.py",
                            "qcb_core.py", "qcb_curriculum.py", "qcb_lean.py", "qcb_integrity.py")),
    *("reports/lean-course-v1/" + n for n in ("comparison.json", "be-decoder-input.json", "rank-decoder-input.json",
                                            "be-decoder.json", "rank-decoder.json", "context-extensions.json")))}
sys.path.insert(0, str(R / "website/scripts"))
from proof_inputs import proof_input_digest


def load_candidates(*, require_semantics=True):
    packet = read_json(FIXTURE)
    catalog, items, graph = load_catalog()
    if (packet["schema_version"] != "qcb.graph_course_candidates.v1" or packet["catalog_hash"] != catalog["catalog_hash"]
            or packet["proof_inputs_sha256"] != proof_input_digest(R)
            or packet["lean_toolchain"] != (R / "lean-toolchain").read_text().strip()
            or packet["new_mathematical_cores"] != 0 or packet["new_canonical_formal_admissions"] != 0
            or packet["model_predictions_executed"] is not False or packet["isolated"] is not False):
        raise ValueError("graph-course fixture source or evidence class drift")
    candidates = packet["cases"]
    if len(candidates) != len(EXPECTED) or {c["task"]["core_id"] for c in candidates} != EXPECTED:
        raise ValueError("preserve the exact five shared-core companion views")
    cores = {c["core_id"]: c for c in catalog["cores"]}
    cases = []
    for candidate in candidates:
        task = validate_task(candidate["task"])
        core, item = cores[task["core_id"]], items[task["core_id"]]
        check_source_bindings(candidate["source_bindings"])
        if (any(task[k] != core[k] for k in ("contract_hash", "family", "split", "snapshot_id"))
                or any(task[k] != item[k] for k in ("question", "assumptions", "conventions"))
                or candidate["source_item_digest"] != core["item_digest"] or digest(item) != core["item_digest"]
                or task["library_revision"] != packet["library_revision"] or candidate["assumptions_added"]
                or not candidate["semantic_coverage"] or not candidate["shortcut_disclosure"]):
            raise ValueError("course companion changed canonical mathematics or assumptions")
        if (not candidate["source_node_ids"] or set(candidate["source_node_ids"]) - set(core["target_nodes"] + core["supporting_nodes"])
                or any(n not in graph for n in candidate["source_node_ids"])):
            raise ValueError("course companion needs frozen core graph anchors")
        if candidate["view_id"] != "qcb-course-" + task["core_id"].removeprefix("qcb-core-") + "-v1":
            raise ValueError("unexpected course view identity")
        refs, controls, negatives = [deepcopy(candidate[k]) for k in ("references", "controls", "negative_controls")]
        if (set(refs) != {n["id"] for n in task["nodes"]} or "library_control" not in controls
                or set(controls) - {"library_control", "constructed_whole_root"}
                or set(negatives) != {"wrong_target", "sorry_axiom"}):
            raise ValueError("complete exact reference/control coverage required")
        proofs = [*refs.values(), *controls.values(), *negatives.values()]
        if any(not isinstance(p, str) or not p.startswith("by") or len(p) > 16000 for p in proofs):
            raise ValueError("authored proof blocks must be complete and bounded")
        allowed = {key: [proof] for key, proof in refs.items()}
        allowed[task["root_id"]].extend([*controls.values(), *negatives.values()])
        cases.append({**deepcopy(candidate), "task": task, "allowed_proofs": allowed})
    if require_semantics:
        check_semantics(packet, cases, cores)
    identity = {k: packet[k] for k in ("catalog_hash", "library_revision", "lean_toolchain", "proof_inputs_sha256")}
    identity.update(fixture_digest=digest(packet), fixture_sha256_lf=text_sha(FIXTURE))
    return cases, identity, catalog, graph


def check_semantics(packet, cases, cores):
    comparison = read_json(EVIDENCE / "comparison.json")
    if (comparison["schema_version"] != "qcb.course_semantic_comparison.v1"
            or comparison["candidate_batch_digest"] != digest(packet) or comparison["source_blind"] is not False
            or not isinstance(comparison["reviewer"], str) or not comparison["reviewer"].strip()
            or comparison["reviewer"] in {packet["author"], "/root/curriculum_be_routes", "/root/curriculum_rank_route"}):
        raise ValueError("source-aware comparison must bind the current batch and distinct roles")
    decoded = {}
    for group in ("be", "rank"):
        context = read_json(EVIDENCE / (group + "-decoder-input.json"))
        decoder = read_json(EVIDENCE / (group + "-decoder.json"))
        if (decoder["source_blind"] is not True or decoder["packet_digest"] != digest(context)
                or decoder["decoder_identity"] in {packet["author"], comparison["reviewer"], "/root/curriculum_be_routes", "/root/curriculum_rank_route"}
                or comparison["decoder_digests"][group] != digest(decoder)
                or comparison["packet_digests"][group] != digest(context)):
            raise ValueError("course decoder or comparison context is stale")
        contexts = context.get("views", [context])
        rows = decoder.get("views", [decoder])
        decoded[group] = ({r["anonymous_id"]: r for r in contexts}, {r["anonymous_id"]: r for r in rows})
    decisions = {v["core_id"]: v for v in comparison["views"]}
    new = {c["task"]["core_id"] for c in cases if c["semantic_evidence"]["kind"] == "new_roundtrip"}
    if set(decisions) != new or len(comparison["views"]) != len(new):
        raise ValueError("comparison must cover each new mathematical root exactly once")
    for case in cases:
        task, evidence = case["task"], case["semantic_evidence"]
        root = next(n["target"] for n in task["nodes"] if n["id"] == task["root_id"])
        if evidence["kind"] == "reuse_canonical_native":
            native = cores[task["core_id"]]["views"]["lean"]
            if (native["status"] != "reference_and_alignment_checked" or native["formal_context"]["target"] != root
                    or native["formal_context"]["imports"] != task["imports"]
                    or evidence["formal_context_digest"] != digest(native["formal_context"])
                    or any(evidence[k] != native[k] for k in ("view_id", "batch_digest", "decoder_digest", "comparison_digest"))):
                raise ValueError("native calibration changed its independently reviewed context")
            continue
        context, decodes = decoded[evidence["group"]]
        formal = context[evidence["anonymous_id"]]["formal_context"]
        decision = decisions[task["core_id"]]
        universe_line = "universe " + " ".join(task.get("universe_parameters", []))
        preamble = formal.get("preamble", "").splitlines()
        if (formal["target"] != root or formal["imports"] != task["imports"]
                or not preamble or preamble[0] != universe_line
                or any(line not in {"open scoped BigOperators", "open scoped BigOperators Kronecker"} for line in preamble[1:])
                or "universe_parameters" in formal and formal["universe_parameters"] != task.get("universe_parameters", [])
                or decision["task_hash"] != digest(task) or decision["formal_context_digest"] != digest(formal)
                or decision["source_item_digest"] != case["source_item_digest"] or decision["verdict"] != "accept"
                or not decision["reasoning"] or not decision["whole_question_coverage"]
                or not decodes[evidence["anonymous_id"]]["reconstructed_statement"]):
            raise ValueError("exact mathematical root lacks accepted source/semantic review")


def load_qualified():
    cases, identity, catalog, graph = load_candidates()
    report = read_json(RECEIPT)
    validate_course_receipt(report, cases, identity, REFERENCE_PIPELINE_PATHS)
    lineage = _source_lineage(report["tested_code_commit"], report["pipeline_source_hashes_lf"])
    views = {}
    for case in cases:
        task = case["task"]
        entry = {"view_id": case["view_id"], "task_hash": digest(task),
                 "allowed_modes": ["root_only", "proof_dag"], "allowed_exposures": ["closed_book", "approved_interface"],
                 **{k: task[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")}}
        views[case["view_id"]] = {"entry": entry, "task": task, "registry_digest": identity["fixture_digest"], "reference_lineage": lineage}
    return views, {"qualified_course_companions": len(views), "new_mathematical_cores": 0,
                   "new_canonical_formal_admissions": 0, "model_performance_measured": False, "reference_lineage": lineage}, catalog, graph
