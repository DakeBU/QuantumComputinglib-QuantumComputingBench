"""Portable task, training, response and review interfaces; no model/Lean execution.

The registry joins existing qualified views without rewriting their source
pipelines. Public index, student inputs and reference records are distinct
projections. Imported responses/reviews are observations, not authenticated runs.
"""
from __future__ import annotations

import hashlib
import json
import re
import secrets
import shutil
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from qcb_core import digest, read_json


def _source_roots(module_path):
    """Repo layout or shallow standalone grader; scoring needs no repository."""
    base = module_path.parents[1] if len(module_path.parents) > 1 else module_path.parent
    return base, base.parents[1] if len(base.parents) > 1 else base


B, R = _source_roots(Path(__file__).resolve())
SPLITS = {"train", "dev", "test_public"}
TRACKS = {"nonlean", "semantic", "lean"}
STATUSES = {"answered", "abstained", "env_blocked", "not_run", "budget_exhausted"}
RESPONSE_FIELDS = {"schema_version", "run_id", "task_id", "task_hash", "status", "answer"}


def _write(path, value):
    path = Path(path)
    if path.exists():
        raise FileExistsError("preserve earlier artifacts; choose a fresh path")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_jsonl(path, rows):
    path = Path(path)
    if path.exists():
        raise FileExistsError("preserve earlier artifacts; choose a fresh path")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8", newline="\n")


def read_jsonl(path):
    path = Path(path)
    if path.stat().st_size > 32_000_000:
        raise ValueError("response/review import exceeds the fixed 32 MB ceiling")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) > 4096:
        raise ValueError("bounded import required")
    return rows


def _task(track, identity, core_ids, split, title, payload, graph, reference, **metadata):
    task = {"task_id": "qcb-task-" + digest([track, identity])[:24], "track": track,
            "view_id": identity, "core_ids": core_ids, "split": split, "title": title,
            "input": payload, "graph": graph, "reference": reference, **metadata}
    task["task_hash"] = digest({k: v for k, v in task.items() if k not in {"reference", "pair_id"}})
    return task


@lru_cache(maxsize=1)
def build_registry():
    """Validate frozen source registries once per process; never execute proofs."""
    from qcb_curriculum import load_catalog
    from qcb_learning_reference import qualify
    from qcb_learning_validity import load_cohort, stage_a_input
    from qcb_proof_session import ProofSession

    sys.path.insert(0, str(B / "scripts"))
    from lean_course_v3 import load_course

    catalog, items, _ = load_catalog()
    course, views, _, _, course_evidence = load_course()
    packet, _ = load_cohort()
    semantic_evidence = qualify(packet)
    tasks = []
    for core in catalog["cores"]:
        item = items[core["core_id"]]
        payload = {"schema_version": "qcb.nl_question_input.v1", "question": item["question"],
                   "assumptions": item["assumptions"], "conventions": item["conventions"],
                   "response_format": {"explanation": "A mathematical answer with an explicit argument; JSON string."}}
        tasks.append(_task("nonlean", core["core_id"] + ".nl", [core["core_id"]], core["split"], core["title"], payload,
                           {"snapshot_id": core["snapshot_id"], "target_nodes": core["target_nodes"],
                            "supporting_nodes": core["supporting_nodes"], "evidence_relation": core["evidence_relation"]},
                           {"answer": item["reference_answer"], "rubric": item["rubric"]},
                           contract_hashes={core["core_id"]: core["contract_hash"]},
                           difficulty=item["difficulty"], admission="canonical_nl_view"))
    for entry in course["entries"]:
        view = views[entry["view_id"]]
        tasks.append(_task("lean", entry["view_id"], [entry["core_id"]], entry["split"], entry["view_id"],
                           ProofSession(view["task"], exposure="approved_interface").agent_input(),
                           {"snapshot_id": catalog["snapshot_id"], "target_nodes": entry["source_node_ids"],
                            "supporting_nodes": [], "evidence_relation": "supplied_obligation_graph_not_proof_term_depth"},
                           {"recorded_reference_lineage": view["reference_lineage"], "rubric": [],
                            "proof_export_available": False,
                            "source": "Use the fixed authored course fixtures through scripts/lean_course_v3.py."},
                           contract_hashes={entry["core_id"]: view["task"]["contract_hash"]}, difficulty=entry["difficulty"],
                           admission="experimental_companion_no_new_core", formal_execution="ENV_BLOCKED"))
    for probe in packet["probes"]:
        payload = stage_a_input(probe)
        payload["response_format"]["decision"] = "holds | refuted; abstention uses status=abstained and answer=null"
        tasks.append(_task("semantic", probe["probe_id"], probe["parent_core_ids"], probe["split"],
                           probe["question"][:100], payload,
                           {"snapshot_id": packet["snapshot_id"], "target_nodes": probe["source_nodes"],
                            "supporting_nodes": [], "evidence_relation": "decision_polarity_reference_only"},
                           {"answer": probe["gold"]["answer"], "decision": probe["gold"]["decision"],
                            "rubric": probe["gold"]["rubric"], "proof": probe["gold"]["reference_proof"]},
                           contract_hashes=probe["parent_contracts"], difficulty=probe["difficulty"],
                           admission="diagnostic_candidate_not_counted", pair_id=probe["pair_id"], cluster_id=probe["cluster_id"]))
    if len({t["task_id"] for t in tasks}) != len(tasks):
        raise ValueError("task identity collision")
    source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=R, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=R, text=True).strip())
    sources = {"catalog_hash": catalog["catalog_hash"], "snapshot_id": catalog["snapshot_id"],
               "course_digest": course_evidence["course_digest"], "semantic_receipt_digest": semantic_evidence["reference_receipt_digest"],
               "proof_inputs_sha256": packet["proof_inputs_sha256"], "production_lean_revision": packet["library_revision"],
               "lean_toolchain": packet["lean_toolchain"]}
    runtime_paths = [B / "src/qcb_bench_runtime.py", B / "scripts/bench.py"]
    runtime_paths += [p for p in (B / "runtime/portable-v1").rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    runtime_sources = {path.relative_to(R).as_posix(): hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest() for path in sorted(runtime_paths)}
    return {"schema_version": "qcb.runtime_registry.v1", "registry_hash": digest({"tasks": tasks, "sources": sources, "runtime_sources": runtime_sources}),
            "source_commit": source_commit, "source_identities": sources, "tasks": tasks,
            "source_tree_dirty": dirty,
            "runtime_sources": runtime_sources,
            "summary": {"task_views": len(tasks), "canonical_core_ids": len(catalog["cores"]),
                        "by_track": dict(Counter(t["track"] for t in tasks)), "by_split": dict(Counter(t["split"] for t in tasks)),
                        "diagnostic_candidates": len(packet["probes"]), "new_canonical_core_ids": 0,
                        "native_lean_admissions": sum("lean" in c["views"] for c in catalog["cores"]),
                        "global_semantic_dedup_complete": False, "hidden_holdout": False, "model_performance_measured": False}}


def public_index(registry):
    """Expert-facing mapping: this is not a closed-book student prompt."""
    return {k: deepcopy(v) for k, v in registry.items() if k != "tasks"} | {
        "tasks": [{k: deepcopy(v) for k, v in t.items() if k not in {"input", "reference", "pair_id"}} for t in registry["tasks"]]}


def select_tasks(registry, *, split=None, track=None, task_ids=None):
    if split not in SPLITS | {None} or track not in TRACKS | {None}:
        raise ValueError("unknown split or track")
    task_ids = task_ids or []
    if len(task_ids) != len(set(task_ids)) or set(task_ids) - {t["task_id"] for t in registry["tasks"]}:
        raise ValueError("unknown or duplicate task selection")
    tasks = [t for t in registry["tasks"] if (split is None or t["split"] == split)
             and (track is None or t["track"] == track) and (not task_ids or t["task_id"] in task_ids)]
    if not tasks:
        raise ValueError("empty task selection")
    if task_ids and {t["task_id"] for t in tasks} != set(task_ids):
        raise ValueError("explicit tasks conflict with split/track filters")
    return tasks


def student_record(task):
    return {"schema_version": "qcb.student_task.v1", "task_id": task["task_id"], "task_hash": task["task_hash"],
            "input": deepcopy(task["input"])}


def export_records(registry, *, purpose="evaluation", split=None, track=None, task_ids=None):
    if purpose not in {"evaluation", "training", "reference"}:
        raise ValueError("unknown export purpose")
    if purpose == "training":
        if split not in {None, "train"}:
            raise ValueError("training export is restricted to inherited train aliases")
        split = "train"
    tasks = select_tasks(registry, split=split, track=track, task_ids=task_ids)
    if purpose == "training":
        if track == "lean" or (task_ids and any(t["track"] == "lean" for t in tasks)):
            raise ValueError("Lean views expose recorded references, not SFT completions; use the qualified course source fixtures")
        tasks = [t for t in tasks if t["track"] != "lean"]
    records = []
    for task in tasks:
        row = student_record(task)
        if purpose in {"training", "reference"}:
            row["reference"] = deepcopy(task["reference"])
            row["split"] = task["split"]
            row["use"] = "supervised_training" if purpose == "training" else "public_oracle_not_student_input"
        if purpose == "training":
            target = {"explanation": task["reference"]["answer"]}
            if task["track"] == "semantic":
                target["decision"] = task["reference"]["decision"]
            row["messages"] = [{"role": "user", "content": json.dumps(task["input"], ensure_ascii=False)},
                               {"role": "assistant", "content": json.dumps(target, ensure_ascii=False)}]
        records.append(row)
    return records


def response_template(tasks, run_id):
    return [{"schema_version": "qcb.response.v1", "run_id": run_id, "task_id": t["task_id"], "task_hash": t["task_hash"],
             "status": "not_run", "answer": None} for t in tasks]


def review_template(tasks, responses):
    response_by_id = {r["task_id"]: r for r in responses}
    return [{"schema_version": "qcb.response_review.v1", "task_id": t["task_id"], "task_hash": t["task_hash"],
             "response_hash": digest(response_by_id[t["task_id"]]),
             "reviewer": {"identity": None, "kind": None, "method": None},
             "criteria": [{"id": c["id"], "criterion": c["criterion"], "weight": c["weight"], "met": None}
                          for c in t["reference"]["rubric"]]} for t in tasks if t["track"] != "lean"]


def prepare_run(registry, output, *, split="test_public", track="semantic", task_ids=None, exposure="closed_book"):
    tasks = select_tasks(registry, split=split, track=track, task_ids=task_ids)
    if exposure not in {"closed_book", "open_library", "approved_interface"}:
        raise ValueError("declare closed_book, open_library or approved_interface exposure")
    if any(t["track"] == "lean" for t in tasks) and exposure != "approved_interface":
        raise ValueError("Lean course inputs retain their approved_interface protocol")
    if exposure == "approved_interface" and any(t["track"] != "lean" for t in tasks):
        raise ValueError("prepare formal approved-interface and natural-language runs separately")
    output = Path(output)
    if output.exists():
        raise FileExistsError("choose a fresh run directory")
    run_id = secrets.token_hex(16)
    manifest = {"schema_version": "qcb.run_manifest.v1", "run_id": run_id,
                "registry_hash": registry["registry_hash"], "source_commit": registry["source_commit"], "runtime_sources": registry["runtime_sources"],
                "source_tree_dirty": registry.get("source_tree_dirty", False),
                "source_identities": registry["source_identities"], "tasks": [{"task_id": t["task_id"], "task_hash": t["task_hash"]} for t in tasks],
                "split": split, "track": track, "exposure": exposure, "runtime": "offline_import",
                "model": {"provider": None, "model_id": None, "checkpoint": None, "tokenizer": None,
                          "chat_template": None, "thinking_mode": None, "decoding": None},
                "budget": {"max_model_calls": 0, "max_cost_usd": 0, "max_output_tokens": 0},
                "student_code_execution": "ENV_BLOCKED", "model_generation_authorized": False,
                "source_solutions_public": True, "hidden_holdout": False}
    manifest["manifest_hash"] = digest(manifest)
    _write(output / "manifest.json", manifest)
    write_jsonl(output / "input/tasks.jsonl", [student_record(t) for t in tasks])
    responses = response_template(tasks, run_id)
    write_jsonl(output / "output/responses.template.jsonl", responses)
    _write(output / "operator/model-profile.template.json", manifest["model"] | {"observed_usage": None})
    return manifest


def _manifest_tasks(registry, manifest):
    if registry["registry_hash"] != digest({"tasks": registry["tasks"], "sources": registry["source_identities"], "runtime_sources": registry["runtime_sources"]}):
        raise ValueError("registry contents differ from their published hash")
    value = {k: v for k, v in manifest.items() if k != "manifest_hash"}
    required = {"schema_version", "run_id", "registry_hash", "source_commit", "runtime_sources", "source_tree_dirty",
                "source_identities", "tasks", "split", "track", "exposure", "runtime", "model", "budget",
                "student_code_execution", "model_generation_authorized", "source_solutions_public", "hidden_holdout", "manifest_hash"}
    if (set(manifest) != required or not isinstance(manifest["run_id"], str)
            or re.fullmatch(r"[0-9a-f]{32}", manifest["run_id"]) is None
            or not isinstance(manifest["source_commit"], str) or re.fullmatch(r"[0-9a-f]{40}", manifest["source_commit"]) is None
            or manifest["source_commit"] != registry["source_commit"] or type(manifest["source_tree_dirty"]) is not bool
            or manifest["source_tree_dirty"] != registry.get("source_tree_dirty", False)
            or manifest["runtime"] != "offline_import" or manifest["student_code_execution"] != "ENV_BLOCKED"
            or manifest["model_generation_authorized"] is not False or manifest["source_solutions_public"] is not True
            or manifest["hidden_holdout"] is not False):
        raise ValueError("exact typed prepared-run manifest and source provenance required")
    if (manifest.get("schema_version") != "qcb.run_manifest.v1" or digest(value) != manifest.get("manifest_hash")
            or manifest.get("registry_hash") != registry["registry_hash"]
            or manifest.get("runtime_sources") != registry["runtime_sources"]
            or manifest.get("source_identities") != registry["source_identities"]):
        raise ValueError("stale or altered registry/run manifest")
    expected = select_tasks(registry, split=manifest["split"], track=manifest["track"], task_ids=[t["task_id"] for t in manifest["tasks"]])
    if [{"task_id": t["task_id"], "task_hash": t["task_hash"]} for t in expected] != manifest["tasks"]:
        raise ValueError("run task hashes/order differ from the registry")
    if (manifest.get("exposure") not in {"closed_book", "open_library", "approved_interface"}
            or (manifest["exposure"] != "approved_interface" and any(t["track"] == "lean" for t in expected))
            or (manifest["exposure"] == "approved_interface" and any(t["track"] != "lean" for t in expected))):
        raise ValueError("exposure differs from the supplied interface capability")
    return expected


def validate_responses(registry, manifest, responses):
    tasks = _manifest_tasks(registry, manifest)
    by_id = {t["task_id"]: t for t in tasks}
    seen = set()
    for row in responses:
        if not isinstance(row, dict) or set(row) != RESPONSE_FIELDS or row["schema_version"] != "qcb.response.v1":
            raise ValueError("closed response schema required; scores are evaluator-owned")
        task = by_id.get(row["task_id"])
        if task is None or row["task_id"] in seen or row["task_hash"] != task["task_hash"] or row["run_id"] != manifest["run_id"]:
            raise ValueError("unknown, duplicate or stale response binding")
        seen.add(row["task_id"])
        if row["status"] not in STATUSES:
            raise ValueError("unknown response status")
        answer = row["answer"]
        if row["status"] == "answered":
            allowed = {"decision", "explanation"} if task["track"] == "semantic" else {"explanation"} if task["track"] == "nonlean" else {"proof"}
            if not isinstance(answer, dict) or set(answer) != allowed:
                raise ValueError("answer format differs from task track")
            if any(not isinstance(v, str) or not v.strip() or len(v) > 64000 for v in answer.values()):
                raise ValueError("bounded nonempty answer strings required")
            if task["track"] == "semantic" and answer["decision"] not in {"holds", "refuted"}:
                raise ValueError("decision must be holds or refuted; use abstained status for abstention")
        elif answer is not None:
            raise ValueError("unanswered statuses must not contain an answer")
    return tasks


def score(registry, manifest, responses, reviews=()):
    tasks = validate_responses(registry, manifest, responses)
    by_response = {r["task_id"]: r for r in responses}
    by_task = {t["task_id"]: t for t in tasks}
    reviewed, review_records = {}, {}
    for review in reviews:
        if not isinstance(review, dict) or set(review) != {"schema_version", "task_id", "task_hash", "response_hash", "reviewer", "criteria"}:
            raise ValueError("closed review schema required")
        task, response = by_task.get(review["task_id"]), by_response.get(review["task_id"])
        if (task is None or response is None or response["status"] != "answered" or task["track"] == "lean"
                or review["task_id"] in reviewed or review["schema_version"] != "qcb.response_review.v1"
                or review["task_hash"] != task["task_hash"] or review["response_hash"] != digest(response)):
            raise ValueError("review is not bound to this exact answered response")
        identity = review["reviewer"]
        if (not isinstance(identity, dict) or set(identity) != {"identity", "kind", "method"}
                or identity["kind"] not in {"human", "ai"} or any(not isinstance(v, str) or not v.strip() for v in identity.values())):
            raise ValueError("actual declared reviewer identity, kind and method required")
        criteria = review["criteria"]
        if not isinstance(criteria, list) or len(criteria) != len(task["reference"]["rubric"]):
            raise ValueError("complete exact rubric required")
        for criterion, original in zip(criteria, task["reference"]["rubric"]):
            if (not isinstance(criterion, dict) or set(criterion) != {"id", "criterion", "weight", "met"}
                    or {k: v for k, v in criterion.items() if k != "met"} != original
                    or type(criterion["weight"]) is not type(original["weight"])
                    or type(criterion["met"]) is not bool):
                raise ValueError("review must preserve every rubric criterion and supply explicit Boolean marks")
        reviewed[review["task_id"]] = sum(c["weight"] for c in criteria if c["met"]) / sum(c["weight"] for c in criteria)
        review_records[review["task_id"]] = review
    rows = []
    for task in tasks:
        response = by_response.get(task["task_id"])
        status = response["status"] if response else "missing"
        answer = response["answer"] if response else None
        decision = (answer["decision"] == task["reference"]["decision"]) if task["track"] == "semantic" and status == "answered" else None
        review = review_records.get(task["task_id"])
        rows.append({"task_id": task["task_id"], "task_hash": task["task_hash"], "track": task["track"], "core_ids": task["core_ids"], "status": status,
                     "response_hash": digest(response) if response is not None else None,
                     "review_hash": digest(review) if review is not None else None,
                     "reviewer": deepcopy(review["reviewer"]) if review is not None else None,
                     "review_identity_authenticated": False,
                     "decision_correct": decision, "semantic_rubric_score": reviewed.get(task["task_id"]),
                     "formal_proof_score": None, "formal_execution": "ENV_BLOCKED" if task["track"] == "lean" else "not_requested"})
    decisions = [r for r in rows if r["track"] == "semantic"]
    complete_pairs = []
    for pair in {t["pair_id"] for t in tasks if t["track"] == "semantic"}:
        pair_tasks = [t for t in tasks if t.get("pair_id") == pair]
        if len(pair_tasks) == 2:
            pair_rows = [r for r in rows if r["task_id"] in {t["task_id"] for t in pair_tasks}]
            complete_pairs.append(all(r["decision_correct"] is True for r in pair_rows))
    return {"schema_version": "qcb.run_score.v1", "registry_hash": registry["registry_hash"], "manifest_hash": manifest["manifest_hash"],
            "source_commit": manifest["source_commit"], "runtime_sources": manifest["runtime_sources"],
            "source_tree_dirty": manifest["source_tree_dirty"],
            "planned_task_views": len(tasks), "distinct_parent_core_ids": len({c for t in tasks for c in t["core_ids"]}),
            "outcomes": dict(Counter(r["status"] for r in rows)), "rows": rows,
            "decision_accuracy_over_planned": sum(r["decision_correct"] is True for r in decisions) / len(decisions) if decisions else None,
            "decision_accuracy_on_answered": sum(r["decision_correct"] is True for r in decisions) / sum(r["status"] == "answered" for r in decisions) if any(r["status"] == "answered" for r in decisions) else None,
            "pair_joint_accuracy_over_selected_pairs": sum(complete_pairs) / len(complete_pairs) if complete_pairs else None,
            "semantic_review_coverage": len(reviewed), "aggregate_semantic_score": sum(reviewed.values()) / len(tasks) if len(reviewed) == len(tasks) and len({t["track"] for t in tasks}) == 1 else None,
            "semantic_scores_by_track": {track: sum(reviewed[t["task_id"]] for t in group) / len(group) if all(t["task_id"] in reviewed for t in group) else None
                                         for track in {t["track"] for t in tasks}
                                         if (group := [t for t in tasks if t["track"] == track])},
            "formal_proof_score": None, "learning_gain": None, "model_identity_authenticated": False,
            "imported_review_authenticity": "declared_identity_only_not_authenticated", "model_performance_measured": False,
            "evidence_kind": "unattested_imported_records", "hidden_holdout": False}


def review_pack(registry, manifest, responses, output, *, run_directory):
    """Join operator review material without executing or grading an argument.

    The returned templates use the existing response-bound review schema. Keep
    this answer-bearing export outside the prepared run and student workspace.
    """
    report = score(registry, manifest, responses)
    tasks = _manifest_tasks(registry, manifest)
    output, run_directory = Path(output).resolve(), Path(run_directory).resolve()
    student_roots = [run_directory]
    if (run_directory.parent / "task.json").is_file():
        student_roots.append((run_directory.parent / "environment").resolve())
    if any(output == root or output.is_relative_to(root) for root in student_roots):
        raise ValueError("operator review pack must be outside the prepared run and portable student environment")
    if output.exists():
        raise FileExistsError("choose a fresh operator review directory")
    by_response = {r["task_id"]: r for r in responses}
    answered = [t for t in tasks if by_response.get(t["task_id"], {}).get("status") == "answered"]
    templates = review_template(answered, responses)
    by_template = {r["task_id"]: r for r in templates}
    cases = []
    for task, result in zip(tasks, report["rows"]):
        response = by_response.get(task["task_id"])
        state = ("no_answer_to_review" if result["status"] != "answered" else
                 "formal_verifier_required" if task["track"] == "lean" else "needs_rubric_review")
        cases.append({"schema_version": "qcb.review_case.v1", "run_id": manifest["run_id"],
                      "run_manifest_hash": manifest["manifest_hash"], "registry_hash": registry["registry_hash"],
                      "task_id": task["task_id"], "task_hash": task["task_hash"], "track": task["track"],
                      "title": task["title"], "core_ids": deepcopy(task["core_ids"]), "split": task["split"],
                      "graph": deepcopy(task["graph"]), "input": deepcopy(task["input"]),
                      "response": deepcopy(response), "response_hash": result["response_hash"],
                      "status": result["status"], "review_state": state,
                      "reference": deepcopy(task["reference"]),
                      "review_template": deepcopy(by_template.get(task["task_id"])),
                      "decision_correct": result["decision_correct"], "semantic_rubric_score": None,
                      "formal_proof_score": None, "formal_execution": result["formal_execution"]})
    write_jsonl(output / "cases.jsonl", cases)
    write_jsonl(output / "reviews.template.jsonl", templates)
    instructions = """# Operator mathematical review pack

This directory contains reference answers. Keep it outside every student
mount and prompt. `cases.jsonl` joins each planned question, actual response,
reference, graph anchors and rubric using the prepared run identities.
Missing, abstained, blocked and unrun responses remain visible.

1. Inspect each `needs_rubric_review` case. Judge the actual mathematical
   argument against every criterion; alternative valid arguments are allowed.
   The exact decision label, where present, is a separate score.
2. Copy `reviews.template.jsonl` to `reviews.completed.jsonl`. Preserve all
   task/response hashes, criterion text, IDs and weights. Supply the reviewer's
   identity, kind (`human` or `ai`) and method, then mark every criterion with
   JSON `true` or `false`. An untouched template cannot be scored.
3. Use the original run and exact response file with the completed reviews:

```sh
python benchmarks/quantumcomputingbench/scripts/bench.py score --manifest RUN/manifest.json --responses RESPONSES.jsonl --reviews REVIEW_DIR/reviews.completed.jsonl --output FRESH_SCORE.json
```

Only answered natural-language and semantic tasks have review templates.
Unanswered tasks have no invented marks; incomplete review leaves the complete
aggregate ungraded. Lean text requires the separate accepted isolated verifier
and receives no proof score or mathematical rubric score from this pack.
Submitted text is data: this command executes no response code or proof.
Declared reviewer identity is recorded provenance, not authentication.
"""
    (output / "README.md").write_text(instructions, encoding="utf-8", newline="\n")
    files = {name: hashlib.sha256((output / name).read_bytes()).hexdigest()
             for name in ("cases.jsonl", "reviews.template.jsonl", "README.md")}
    summary = {"schema_version": "qcb.review_pack.v1", "run_id": manifest["run_id"],
               "run_manifest_hash": manifest["manifest_hash"], "registry_hash": registry["registry_hash"],
               "source_commit": manifest["source_commit"], "source_identities": deepcopy(manifest["source_identities"]),
               "runtime_sources": deepcopy(manifest["runtime_sources"]), "source_tree_dirty": manifest["source_tree_dirty"],
               "responses_hash": digest(responses), "planned_task_views": len(tasks),
               "review_records": len(templates), "outcomes": report["outcomes"],
               "review_states": dict(Counter(case["review_state"] for case in cases)),
               "contains_reference_answers": True, "audience": "operator_only", "student_access_permitted": False,
               "ready_to_score": False, "formal_proof_score": None, "model_performance_measured": False,
               "model_calls": 0, "lean_calls": 0, "files": files}
    summary["pack_hash"] = digest(summary)
    _write(output / "review-manifest.json", summary)
    return summary


def write_downloads(output, registry=None):
    registry = registry or build_registry()
    output = Path(output)
    _write(output / "task-index.json", public_index(registry))
    for name, purpose, split in (("train.jsonl", "training", "train"), ("eval-prompts.jsonl", "evaluation", "test_public"), ("dev-prompts.jsonl", "evaluation", "dev")):
        write_jsonl(output / name, export_records(registry, purpose=purpose, split=split))
    tasks = select_tasks(registry, split="test_public")
    write_jsonl(output / "response-template.jsonl", response_template(tasks, "REPLACE_WITH_PREPARED_RUN_ID"))
    manifest = {"schema_version": "qcb.download_manifest.v1", "registry_hash": registry["registry_hash"],
                "source_commit": registry["source_commit"], "files": {p.name: {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size} for p in sorted(output.iterdir()) if p.is_file()},
                "usage": {"train.jsonl": "Train aliases only; supervised references included.", "eval-prompts.jsonl": "Public test prompts only; reference solutions remain public in the source repository.",
                          "response-template.jsonl": "Illustrative format; prepare-run binds actual run identities."}, "model_performance_measured": False}
    _write(output / "download-manifest.json", manifest)
    return manifest


def verify_downloads(output, registry):
    """Check exact source projections and bytes; reject extra gold files."""
    output = Path(output)
    names = {"task-index.json", "train.jsonl", "eval-prompts.jsonl", "dev-prompts.jsonl", "response-template.jsonl", "download-manifest.json"}
    if {p.name for p in output.iterdir()} != names or any(not p.is_file() for p in output.iterdir()):
        raise ValueError("runtime downloads contain missing or unexpected artifacts")
    if read_json(output / "task-index.json") != public_index(registry):
        raise ValueError("public task index differs from the current source registry")
    for name, purpose, split in (("train.jsonl", "training", "train"), ("eval-prompts.jsonl", "evaluation", "test_public"), ("dev-prompts.jsonl", "evaluation", "dev")):
        if read_jsonl(output / name) != export_records(registry, purpose=purpose, split=split):
            raise ValueError("task download differs from its exact split/projection: " + name)
    expected = response_template(select_tasks(registry, split="test_public"), "REPLACE_WITH_PREPARED_RUN_ID")
    if read_jsonl(output / "response-template.jsonl") != expected:
        raise ValueError("response template changed task identities or defaults")
    manifest = read_json(output / "download-manifest.json")
    files = {p.name: {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size} for p in output.iterdir() if p.name != "download-manifest.json"}
    if (manifest.get("schema_version") != "qcb.download_manifest.v1" or manifest.get("files") != files
            or manifest.get("registry_hash") != registry["registry_hash"] or manifest.get("source_commit") != registry["source_commit"]
            or manifest.get("model_performance_measured") is not False):
        raise ValueError("download byte/source manifest is stale")
    return {"passed": True, "artifacts": len(names), "registry_hash": registry["registry_hash"], "model_calls": 0}


def doctor():
    return {"python": sys.version.split()[0], "docker_binary_present": shutil.which("docker") is not None,
            "docker_engine_probed": False, "container_execution_verified": False,
            "student_lean_execution": "ENV_BLOCKED", "model_endpoint_required_for_authoring": False,
            "commands_execute_models": False, "training_launch_supported": False}


def bundle(registry, output, *, split="test_public", track="semantic", task_ids=None):
    """Generate a runnable CPU question workspace and independent grader.

    This is QCB's portable format, not a claim of Harbor TaskConfig support.
    Docker execution is recorded separately by the operator/CI smoke.
    """
    tasks = select_tasks(registry, split=split, track=track, task_ids=task_ids)
    if any(t["track"] == "lean" for t in tasks):
        raise ValueError("question-only CPU bundle cannot execute Lean; use the registered isolated prover harness")
    output = Path(output)
    if output.exists():
        raise FileExistsError("choose a fresh bundle directory")
    manifest = prepare_run(registry, output / "run", split=split, track=track, task_ids=task_ids)
    template = B / "runtime/portable-v1"
    shutil.copytree(template, output, dirs_exist_ok=True)
    workspace = output / "environment/workspace"
    write_jsonl(workspace / "tasks.jsonl", [student_record(t) for t in tasks])
    write_jsonl(workspace / "responses.template.jsonl", response_template(tasks, manifest["run_id"]))
    _write(output / "grader/registry.json", registry)
    _write(output / "grader/manifest.json", manifest)
    for name in ("qcb_bench_runtime.py", "qcb_core.py", "qcb_integrity.py"):
        shutil.copyfile(B / "src" / name, output / "grader" / name)
    profile = {"schema_version": "qcb.question_workspace.v1", "format": "QCB portable, not Harbor TaskConfig",
               "image_tag": "python:3.11.15-slim-bookworm", "image_digest": "sha256:d29f48a31a8b408ed19272ca1e7b10ebae13b240a27e862d3d4217c528e2e0c3", "image_execution": "NOT_RUN",
               "agent_build_context": "environment", "grader_build_context": "grader",
               "student_access": ["environment/workspace", "run/output"], "network": "none",
               "cpu": 1, "memory_mib": 1024, "pids": 128, "read_only_root": True,
               "student_lean_execution": "ENV_BLOCKED", "model_calls": 0,
               "run_manifest_hash": manifest["manifest_hash"], "registry_hash": registry["registry_hash"]}
    _write(output / "task.json", profile)
    return profile


def smoke(registry, output):
    output = Path(output)
    if output.exists():
        raise FileExistsError("choose a fresh smoke directory")
    manifest = prepare_run(registry, output / "run", split=None, track="semantic")
    tasks = _manifest_tasks(registry, manifest)
    oracle = response_template(tasks, manifest["run_id"])
    for row, task in zip(oracle, tasks):
        row.update(status="answered", answer={"decision": task["reference"]["decision"], "explanation": task["reference"]["answer"]})
    none = response_template(tasks, manifest["run_id"])
    for row in none:
        row["status"] = "abstained"
    wrong_labels = deepcopy(oracle)
    for row in wrong_labels:
        row["answer"]["decision"] = "refuted" if row["answer"]["decision"] == "holds" else "holds"
    reports = {"oracle": score(registry, manifest, oracle), "none": score(registry, manifest, none),
               "wrong": score(registry, manifest, wrong_labels), "missing": score(registry, manifest, [])}
    assert reports["oracle"]["decision_accuracy_over_planned"] == 1
    assert reports["none"]["decision_accuracy_over_planned"] == reports["missing"]["decision_accuracy_over_planned"] == 0
    assert reports["wrong"]["decision_accuracy_over_planned"] == reports["wrong"]["pair_joint_accuracy_over_selected_pairs"] == 0
    wrong = deepcopy(oracle)
    wrong[0]["task_hash"] = "0" * 64
    rejected = False
    try:
        score(registry, manifest, wrong)
    except ValueError:
        rejected = True
    if not rejected:
        raise AssertionError("stale response escaped the negative control")
    for name, rows in (("oracle-responses.jsonl", oracle), ("none-responses.jsonl", none), ("wrong-responses.jsonl", wrong_labels)):
        write_jsonl(output / name, rows)
    result = {"schema_version": "qcb.runtime_smoke.v1", "passed": True, "synthetic_fixture": True,
              "decision_only": True, "reports": reports, "tampered_response_rejected": rejected,
              "model_calls": 0, "lean_calls": 0, "container_calls": 0, "model_performance_measured": False}
    portable = output / "portable"
    bundle(registry, portable, split=None, track="semantic")
    oracle_bytes = subprocess.check_output([sys.executable, str(portable / "solution/oracle.py")])
    (portable / "run/output/oracle.jsonl").write_bytes(oracle_bytes)
    wrong_portable = [json.loads(line) for line in oracle_bytes.decode().splitlines()]
    for row in wrong_portable:
        row["answer"]["decision"] = "refuted" if row["answer"]["decision"] == "holds" else "holds"
    write_jsonl(portable / "run/output/wrong.jsonl", wrong_portable)
    for filename, expected in (("oracle.jsonl", 1), ("responses.template.jsonl", 0), ("wrong.jsonl", 0)):
        graded = subprocess.check_output([sys.executable, str(portable / "grader/grade.py"), str(portable / "run/output" / filename)])
        report = json.loads(graded)
        if report["decision_accuracy_over_planned"] != expected or (filename == "wrong.jsonl" and report["pair_joint_accuracy_over_selected_pairs"] != 0):
            raise AssertionError("standalone independent grader disagrees with the protocol control")
    result["standalone_oracle_and_grader_passed"] = True
    _write(output / "smoke-report.json", result)
    return result
