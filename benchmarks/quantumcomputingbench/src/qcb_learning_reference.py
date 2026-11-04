"""Content-bound qualification for the staged semantic diagnostic cohort.

Actual authored replay is separate from source/NL comparison and from models.
No old pipeline, receipt, source split or canonical admission is modified.
"""
from __future__ import annotations

import asyncio
import hashlib
import math
import re
import subprocess
from copy import deepcopy
from pathlib import Path
from time import monotonic
from types import SimpleNamespace

from qcb_authored_session import AuthoredReferenceVerifier
from qcb_core import digest, read_json
from qcb_integrity import text_sha
from qcb_lean import APPROVED_AXIOMS
from qcb_learning_validity import COHORT, B, R, challenge_task
from qcb_proof_session import ProofSession, SessionLimits

EVIDENCE = B / "reports/learning-validity-v1"
REFERENCE_PROFILE = {"batch_wall_seconds": 2400, "session_wall_seconds": 300, "check_seconds": 120,
                     "output_cap_bytes": 65536, "max_root_replays": 48}
DEFINITION_SLICES = (
    ("QuantumBlockEncoding/TensorTrainCanonical.lean", "QuantumBlockEncoding.TensorTrainCanonical", 18, 18),
    ("QuantumBlockEncoding/TensorTrainCanonical.lean", "QuantumBlockEncoding.TensorTrainCanonical", 120, 120),
    ("QuantumBlockEncoding/TensorTrainCanonical.lean", "QuantumBlockEncoding.TensorTrainCanonical", 211, 213),
    ("QuantumBlockEncoding/PrimitiveSemantics.lean", "QuantumBlockEncoding", 116, 116),
    ("QuantumBlockEncoding/RealAmplitudePreparation.lean", "QuantumBlockEncoding.RealAmplitudePreparation", 143, 143),
    ("QuantumBlockEncoding/RealAmplitudePreparation.lean", "QuantumBlockEncoding.RealAmplitudePreparation", 204, 205),
    ("QuantumBlockEncoding/RealAmplitudePreparation.lean", "QuantumBlockEncoding.RealAmplitudePreparation", 211, 211),
    ("QuantumBlockEncoding/Robin/ComplexLCU.lean", "QuantumBlockEncoding.Robin.ComplexLCU", 148, 151),
    ("QuantumBlockEncoding/Robin/ComplexLCU.lean", "QuantumBlockEncoding.Robin.ComplexLCU", 250, 251),
    ("QuantumBlockEncoding/Robin/ComplexLCU.lean", "QuantumBlockEncoding.Robin.ComplexLCU", 315, 327),
    ("QuantumBlockEncoding/Robin/ComplexLCU.lean", "QuantumBlockEncoding.Robin.ComplexLCU", 330, 337),
    ("QuantumBlockEncoding/HermitePolynomial.lean", "QuantumBlockEncoding.HermitePolynomial", 120, 120),
    ("QuantumBlockEncoding/HermitePolynomial.lean", "QuantumBlockEncoding.HermitePolynomial", 123, 123),
)


REPLAY_FIELDS = {"node_id", "request_hash", "execution_id", "final_replay", "proof_sha256", "source_sha256",
                 "runtime_checkout_commit", "proof_inputs_sha256", "actual_lean_version", "pipeline_sha256",
                 "exit_code", "status", "axioms", "failure", "elapsed_seconds", "execution_class", "isolated",
                 "request_metadata", "pipeline_source_sha256_lf"}
EVIDENCE_FIELDS = {"request_hash", "proof_sha256", "execution_id", "status", "axioms", "kernel_checked",
                   "failure_class", "execution_class", "isolated"}


def _compact_evidence(reply):
    if not isinstance(reply, dict) or not EVIDENCE_FIELDS <= set(reply):
        return None
    return {key: deepcopy(reply[key]) for key in EVIDENCE_FIELDS}


class _RecordedAuthoredVerifier(AuthoredReferenceVerifier):
    async def verify(self, request):
        reply = await super().verify(request)
        if self.replays and self.replays[-1]["request_hash"] == digest(request):
            self.replays[-1]["request_metadata"] = {key: request[key] for key in ("request_id", "timeout_seconds", "deadline_monotonic")}
            self.replays[-1]["pipeline_source_sha256_lf"] = text_sha(B / "src/qcb_authored_session.py")
        return reply


def formal_root(probe):
    p = probe["formal_context"]["proposition"]
    return p if probe["gold"]["decision"] == "holds" else "¬ (" + p + ")"


def decoder_payload(packet):
    """Withhold original questions, answers, rubrics and author verdicts."""
    definitions = []
    for source, namespace, first, last in DEFINITION_SLICES:
        path = R / source
        definitions.append({"path": source, "namespace": namespace, "sha256_lf": text_sha(path),
                            "first_line": first, "last_line": last,
                            "source": "\n".join(path.read_text(encoding="utf-8").splitlines()[first-1:last])})
    return {"schema_version": "qcb.learning_formal_decoder_input.v1",
            "lean_toolchain": packet["lean_toolchain"], "dependency_manifest_sha256_lf": text_sha(R / "lake-manifest.json"),
            "ambient_definitions": definitions,
            "formal_items": [{"probe_id": p["probe_id"], "imports": p["formal_context"]["imports"],
                              "formal_statement": formal_root(p)} for p in packet["probes"]]}


def source_payload(packet, decoder):
    return {"schema_version": "qcb.learning_source_comparison_input.v1", "decoder_record_digest": digest(decoder),
            "decoder_input_digest": digest(decoder_payload(packet)),
            "items": [{"probe_id": p["probe_id"], "question": p["question"], "assumptions": p["assumptions"],
                       "conventions": p["conventions"], "formal_context": p["formal_context"],
                       "formal_statement": formal_root(p)} for p in packet["probes"]],
            "decoded_formal_mathematics": deepcopy(decoder["items"]),
            "source_bindings": deepcopy(packet["source_bindings"])}


def answer_payload(packet, decoder, comparison):
    return {"schema_version": "qcb.learning_answer_review_input.v1", "source_comparison_digest": digest(comparison),
            "source_input_digest": digest(source_payload(packet, decoder)),
            "items": [{"probe_id": p["probe_id"], "question": p["question"], "assumptions": p["assumptions"],
                       "conventions": p["conventions"], "reference_answer": p["gold"]["answer"],
                       "rubric": p["gold"]["rubric"], "formal_coverage": p["formal_coverage"]} for p in packet["probes"]]}


def _items(record, ids):
    rows = record.get("items")
    if not isinstance(rows, list) or len(rows) != len(ids) or {r.get("probe_id") for r in rows} != ids:
        raise ValueError("semantic review must cover every sealed probe exactly once")
    return rows


def _substantive(row, key):
    if not isinstance(row.get(key), str) or len(row[key].strip()) < 30:
        raise ValueError("substantive mathematical review required: " + key)


def check_semantics(packet, evidence_dir=EVIDENCE):
    ids = {p["probe_id"] for p in packet["probes"]}
    authors = {p["author_identity"] for p in packet["probes"]}
    decoder_input = read_json(evidence_dir / "decoder-input.json")
    decoder = read_json(evidence_dir / "decoder.json")
    if decoder_input != decoder_payload(packet) or decoder.get("input_digest") != digest(decoder_input):
        raise ValueError("decoder context changed")
    decoder_id = decoder.get("reviewer_identity")
    if not isinstance(decoder_id, str) or not decoder_id or decoder_id in authors:
        raise ValueError("a genuinely distinct recorded decoder is required")
    for row in _items(decoder, ids):
        _substantive(row, "decoded_mathematics")
        _substantive(row, "semantic_slots")
    source_input = read_json(evidence_dir / "source-input.json")
    comparison = read_json(evidence_dir / "source-comparison.json")
    if source_input != source_payload(packet, decoder) or comparison.get("input_digest") != digest(source_input):
        raise ValueError("anti-anchored source comparison changed")
    reviewer = comparison.get("reviewer_identity")
    if not isinstance(reviewer, str) or not reviewer or reviewer in authors | {decoder_id}:
        raise ValueError("source comparison needs a third recorded identity")
    for row in _items(comparison, ids):
        if row.get("alignment_verdict") != "aligned" or row.get("formal_coverage") != "decision_polarity_only":
            raise ValueError("unresolved source/formal alignment; do not export evaluation gold")
        _substantive(row, "independent_derivation")
        _substantive(row, "reasoning")
    review_input = read_json(evidence_dir / "answer-input.json")
    review = read_json(evidence_dir / "answer-review.json")
    if (review_input != answer_payload(packet, decoder, comparison) or review.get("input_digest") != digest(review_input)
            or review.get("reviewer_identity") != reviewer):
        raise ValueError("reference answer review changed or lacks its independently derived source comparison")
    for row in _items(review, ids):
        if row.get("answer_verdict") != "accepted" or row.get("rubric_verdict") != "accepted":
            raise ValueError("reference explanation or rubric remains unresolved")
        _substantive(row, "reasoning")
        _substantive(row, "source_checks")
    return {"decoder_identity": decoder_id, "source_reviewer_identity": reviewer,
            "decoder_digest": digest(decoder), "source_comparison_digest": digest(comparison), "answer_review_digest": digest(review),
            "automatic_semantic_truth_or_real_world_independence_established": False}


def pipeline_identity():
    names = ["qcb_learning_reference.py", "qcb_learning_validity.py", "qcb_learning_design.py", "qcb_authored_session.py",
             "qcb_proof_session.py", "qcb_lean.py", "qcb_core.py", "qcb_integrity.py", "qcb_curriculum.py",
             "qcb_textbook_policy.py", "qcb_formal_views.py"]
    paths = [B / "src" / name for name in names]
    paths += [B / "scripts/learning_validity.py", COHORT, R / "website/scripts/proof_inputs.py"]
    paths += [EVIDENCE / name for name in ("decoder-input.json", "decoder.json", "source-input.json", "source-comparison.json", "answer-input.json", "answer-review.json")]
    return {p.relative_to(R).as_posix(): text_sha(p) for p in paths}


async def replay_references(packet, build_root, *, progress=None):
    """Only committed, inspected authored proofs; never candidate model text."""
    semantics = check_semantics(packet)
    if packet != read_json(COHORT):
        raise ValueError("only the fixed versioned cohort can be replayed")
    planned = 2 * len(packet["probes"]) + 2 * len({tuple(p["formal_context"]["imports"]) for p in packet["probes"]})
    if planned > REFERENCE_PROFILE["max_root_replays"]:
        raise ValueError("reference count exceeds the reviewed batch profile")
    identity = pipeline_identity()
    commit = (await asyncio.to_thread(subprocess.check_output, ["git", "rev-parse", "HEAD"], cwd=R, text=True)).strip()
    for path, expected in identity.items():
        raw = await asyncio.to_thread(subprocess.check_output, ["git", "show", commit + ":" + path], cwd=R)
        if hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest() != expected:
            raise ValueError("freeze and commit the complete reviewed reference pipeline first")
    started = monotonic()
    rows, raw = [], []
    negative_imports = set()
    for probe in packet["probes"]:
        remaining = REFERENCE_PROFILE["batch_wall_seconds"] - (monotonic() - started)
        if remaining <= 0:
            raise TimeoutError("bounded authored reference batch exhausted")
        task = challenge_task(probe, probe["gold"]["decision"], snapshot_id=packet["snapshot_id"], library_revision=packet["library_revision"])
        proof = probe["gold"]["reference_proof"]
        negatives = tuple(task["imports"]) not in negative_imports
        allowed = [proof] + (["by exact True.intro", "by sorry"] if negatives else [])
        verifier = _RecordedAuthoredVerifier(task, {"assessment_root": allowed}, build_root)
        session = ProofSession(task, verifier, mode="root_only", limits=SessionLimits(
            wall_seconds=min(REFERENCE_PROFILE["session_wall_seconds"], remaining), check_seconds=REFERENCE_PROFILE["check_seconds"]))
        submitted = await session.act({"kind": "submit", "state_id": session.state_id, "node_id": "assessment_root", "proof": proof})
        finished = await session.act({"kind": "finish", "state_id": session.state_id})
        if progress is not None:
            progress({"phase": "positive_checks", "probe_id": probe["probe_id"], "submitted": submitted,
                      "finished": finished, "session": session.report(), "replays": verifier.replays})
        row = {"probe_id": probe["probe_id"], "probe_digest": digest(probe), "task_hash": digest(task),
               "formal_target_sha256": digest(task["nodes"][0]["target"]), "gold_polarity": probe["gold"]["decision"],
               "submitted_status": submitted["status"], "finish_status": finished["status"],
               "submission_evidence": _compact_evidence(submitted["evidence"]) if "evidence" in submitted else None,
               "final_evidence": _compact_evidence(finished["final_replay"]) if "final_replay" in finished else None,
               "formal_root_checked": session.report()["formal_root_checked"], "negative_controls": []}
        if not row["formal_root_checked"]:
            raise RuntimeError("fixed authored root did not pass; raw progress preserves the actual typed failure")
        if negatives:
            negative_imports.add(tuple(task["imports"]))
            for label, bad_proof in (("wrong_target", "by exact True.intro"), ("sorry_axiom", "by sorry")):
                remaining = REFERENCE_PROFILE["batch_wall_seconds"] - (monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError("bounded authored reference batch exhausted")
                negative = ProofSession(task, verifier, mode="root_only", limits=SessionLimits(wall_seconds=min(180, remaining), check_seconds=120))
                reply = await negative.act({"kind": "submit", "state_id": negative.state_id, "node_id": "assessment_root", "proof": bad_proof})
                row["negative_controls"].append({"kind": label, "status": reply["status"],
                                                  "evidence": _compact_evidence(reply["evidence"]) if "evidence" in reply else None})
                if progress is not None:
                    progress({"phase": "negative_control", "probe_id": probe["probe_id"], "control": label,
                              "reply": reply, "replays": deepcopy(verifier.replays)})
        row["replays"] = [{k: v for k, v in replay.items() if k != "diagnostics"} for replay in verifier.replays]
        raw.append({"probe_id": probe["probe_id"], "submitted": submitted, "finished": finished, "session": session.report(), "replays": verifier.replays})
        if progress is not None:
            progress(deepcopy(raw[-1]))
        if not row["formal_root_checked"] or any(n["status"] != "compile_error" for n in row["negative_controls"]):
            raise RuntimeError("authored polarity/root/negative gate failed; preserve raw evidence")
        rows.append(row)
        print(__import__("json").dumps({"probe_id": probe["probe_id"], "formal_root_checked": True, "replay_count": len(verifier.replays)}), flush=True)
    if pipeline_identity() != identity:
        raise ValueError("reference pipeline drift during batch")
    return {"schema_version": "qcb.learning_validity_references.v1", "cohort_digest": digest(packet),
            "tested_code_commit": commit, "pipeline_source_hashes_lf": identity, "semantic_review": semantics,
            "profile": deepcopy(REFERENCE_PROFILE), "passed": len(rows) == len(packet["probes"]), "results": rows,
            "elapsed_seconds": monotonic()-started, "execution_class": "trusted_local_authored_reference", "isolated": False,
            "model_calls": 0, "model_performance_measured": False, "learning_gain": None,
            "formal_coverage": "decision_polarity_only", "new_canonical_formal_admissions": 0}, raw


def qualify(packet, *, evidence_dir=EVIDENCE):
    if Path(evidence_dir).resolve() != EVIDENCE.resolve() or packet != read_json(COHORT):
        raise ValueError("qualification uses only its fixed committed cohort and evidence directory")
    semantics = check_semantics(packet, evidence_dir)
    report = read_json(evidence_dir / "reference-checks.json")
    if (report.get("schema_version") != "qcb.learning_validity_references.v1" or report.get("cohort_digest") != digest(packet)
            or report.get("passed") is not True or report.get("semantic_review") != semantics
            or report.get("execution_class") != "trusted_local_authored_reference" or report.get("isolated") is not False
            or report.get("model_calls") != 0 or report.get("model_performance_measured") is not False
            or report.get("formal_coverage") != "decision_polarity_only" or report.get("learning_gain") is not None
            or report.get("profile") != REFERENCE_PROFILE):
        raise ValueError("reference checkpoint scope or cohort binding differs")
    if report.get("pipeline_source_hashes_lf") != pipeline_identity():
        raise ValueError("recorded reference pipeline differs from current sources; replay after review")
    # The exact recorded Git blobs are part of the execution provenance.
    for path, expected in report["pipeline_source_hashes_lf"].items():
        raw = subprocess.check_output(["git", "show", report["tested_code_commit"] + ":" + path], cwd=R)
        if hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest() != expected:
            raise ValueError("recorded execution source history unavailable or changed")
    results = report.get("results", [])
    by_id = {p["probe_id"]: p for p in packet["probes"]}
    if len(results) != len(by_id) or {r["probe_id"] for r in results} != set(by_id):
        raise ValueError("reference receipt must cover every diagnostic")
    validate_reference_results(packet, results)
    return {"status": "PUBLIC_SEMANTIC_REFERENCE_PILOT_QUALIFIED", "cohort_digest": digest(packet),
            "reference_receipt_digest": digest(report), "formal_coverage": "decision_polarity_only",
            "actual_model_performance_measured": False, "learning_gain": None, "hidden_holdout": False,
            "canonical_admissions_changed": False, "reference_replay_count": sum(len(r["replays"]) for r in results)}


def validate_reference_results(packet, results):
    """Artifact consistency checks, not authentication of a claimed execution."""
    by_id = {p["probe_id"]: p for p in packet["probes"]}
    if len(results) != len(by_id) or {r["probe_id"] for r in results} != set(by_id):
        raise ValueError("reference results must cover every fixed probe exactly once")
    negative_imports, execution_ids = set(), set()
    for row in results:
        probe = by_id[row["probe_id"]]
        task = challenge_task(probe, probe["gold"]["decision"], snapshot_id=packet["snapshot_id"], library_revision=packet["library_revision"])
        if (row.get("probe_digest") != digest(probe) or row.get("task_hash") != digest(task)
                or row.get("formal_target_sha256") != digest(task["nodes"][0]["target"])
                or row.get("gold_polarity") != probe["gold"]["decision"]
                or row.get("formal_root_checked") is not True or row.get("submitted_status") != "verified" or row.get("finish_status") != "verified"):
            raise ValueError("fixed diagnostic root binding or replay failed")
        if any(set(r) != REPLAY_FIELDS for r in row["replays"]):
            raise ValueError("complete actual replay metadata required")
        positives = [r for r in row["replays"] if r["status"] == "verified"]
        if (len(positives) != 2 or {r["final_replay"] for r in positives} != {False, True}
                or any(set(r["axioms"]) - APPROVED_AXIOMS or r["proof_inputs_sha256"] != packet["proof_inputs_sha256"]
                       or r["runtime_checkout_commit"] != packet["library_revision"] or r["node_id"] != "assessment_root"
                       or r["proof_sha256"] != hashlib.sha256(probe["gold"]["reference_proof"].encode()).hexdigest()
                       or type(r["exit_code"]) is not int or r["exit_code"] != 0 or r["failure"] is not None
                       or r["execution_class"] != "trusted_local_authored_reference" or r["isolated"] is not False
                       or "version " + packet["lean_toolchain"].split(":v")[-1] + "," not in r["actual_lean_version"] for r in positives)
                or len({r["execution_id"] for r in positives}) != 2):
            raise ValueError("two distinct fresh-root checks with fixed foundational axioms required")
        expected_negatives = tuple(task["imports"]) not in negative_imports
        negatives = row.get("negative_controls", [])
        if expected_negatives:
            negative_imports.add(tuple(task["imports"]))
            if (len(negatives) != 2 or {n["kind"] for n in negatives} != {"wrong_target", "sorry_axiom"}
                    or any(n["status"] != "compile_error" for n in negatives)
                    or not any(n["kind"] == "sorry_axiom" and "sorryAx" in n["evidence"]["axioms"] for n in negatives)):
                raise ValueError("actual wrong-target and forbidden-axiom controls required for each import context")
        elif negatives:
            raise ValueError("unexpected unregistered negative checks")
        if len(row["replays"]) != 2 + len(negatives):
            raise ValueError("replay/check accounting differs")
        evidence = [row.get("submission_evidence"), row.get("final_evidence")] + [n["evidence"] for n in negatives]
        if any(not isinstance(e, dict) or set(e) != EVIDENCE_FIELDS for e in evidence):
            raise ValueError("each submitted/final/control result needs a complete bound verifier reply")
        replies = {e["execution_id"]: e for e in evidence}
        if len(replies) != len(evidence):
            raise ValueError("verifier replies cannot reuse execution identities")
        if {row["submission_evidence"]["execution_id"], row["final_evidence"]["execution_id"]} != {r["execution_id"] for r in positives}:
            raise ValueError("positive summary must bind the actual submitted and final root checks")
        if row["submission_evidence"]["execution_id"] != next(r["execution_id"] for r in positives if not r["final_replay"]):
            raise ValueError("submission and fresh final-root evidence were swapped")
        for replay in row["replays"]:
            if (not isinstance(replay["execution_id"], str) or not re.fullmatch(r"[0-9a-f]{32}", replay["execution_id"])
                    or type(replay["final_replay"]) is not bool or not isinstance(replay["axioms"], list)
                    or any(not isinstance(a, str) for a in replay["axioms"])
                    or type(replay["elapsed_seconds"]) not in (int, float) or not math.isfinite(replay["elapsed_seconds"])
                    or replay["elapsed_seconds"] < 0):
                raise ValueError("typed actual nonce, final flag, axiom and timing evidence required")
            if (replay["runtime_checkout_commit"] != packet["library_revision"]
                    or replay["proof_inputs_sha256"] != packet["proof_inputs_sha256"]
                    or "version " + packet["lean_toolchain"].split(":v")[-1] + "," not in replay["actual_lean_version"]
                    or replay["node_id"] != "assessment_root"):
                raise ValueError("every control/root must bind the same actual runtime, proof inputs, toolchain and target node")
            if replay["execution_id"] in execution_ids:
                raise ValueError("fresh process execution identities must not be reused")
            execution_ids.add(replay["execution_id"])
            reply = replies.get(replay["execution_id"])
            if reply is None or any(reply[k] != replay[k] for k in ("request_hash", "proof_sha256", "execution_id", "status", "axioms", "execution_class", "isolated")):
                raise ValueError("summary/control evidence differs from its actual replay")
            proof = probe["gold"]["reference_proof"]
            if replay["status"] != "verified":
                negative = next((n for n in negatives if n["evidence"]["execution_id"] == replay["execution_id"]), None)
                if negative is None or replay["status"] != "compile_error" or replay["final_replay"] is not False or replay["failure"] is not None:
                    raise ValueError("environmental failure is not an expected rejected proof control")
                proof = "by sorry" if negative["kind"] == "sorry_axiom" else "by exact True.intro"
                if (type(replay["exit_code"]) is not int or replay["exit_code"] not in ({0} if negative["kind"] == "sorry_axiom" else {1})
                        or (negative["kind"] == "sorry_axiom" and "sorryAx" not in replay["axioms"])
                        or (negative["kind"] == "wrong_target" and replay["axioms"])):
                    raise ValueError("rejected control must carry the actual compiler/axiom outcome")
            meta = replay["request_metadata"]
            if (not isinstance(meta, dict) or set(meta) != {"request_id", "timeout_seconds", "deadline_monotonic"}
                    or not isinstance(meta["request_id"], str) or not meta["request_id"].isdigit()
                    or any(type(meta[k]) not in (int, float) or not math.isfinite(meta[k]) or meta[k] <= 0 for k in ("timeout_seconds", "deadline_monotonic"))
                    or meta["timeout_seconds"] > REFERENCE_PROFILE["check_seconds"]):
                raise ValueError("bounded actual request metadata required")
            request = {"schema_version": "qcb.obligation_check.v1", "task_hash": digest(task), "node_id": "assessment_root",
                       "imports": task["imports"], "target": task["nodes"][0]["target"], "universe_parameters": [],
                       "library_revision": packet["library_revision"], "proof": proof, "dependency_order": [], "dependencies": {},
                       "final_replay": replay["final_replay"], **meta}
            source_context = SimpleNamespace(task=task, nodes={}, allowlist={})
            source = AuthoredReferenceVerifier._source(source_context, request, replay["execution_id"])
            pipeline_lf = (B / "src/qcb_authored_session.py").read_bytes().replace(b"\r\n", b"\n")
            pipeline_raw_hashes = {hashlib.sha256(pipeline_lf).hexdigest(), hashlib.sha256(pipeline_lf.replace(b"\n", b"\r\n")).hexdigest()}
            if (digest(request) != replay["request_hash"] or hashlib.sha256(proof.encode()).hexdigest() != replay["proof_sha256"]
                    or hashlib.sha256(source.encode()).hexdigest() != replay["source_sha256"]
                    or replay["pipeline_source_sha256_lf"] != text_sha(B / "src/qcb_authored_session.py")
                    or replay["pipeline_sha256"] not in pipeline_raw_hashes):
                raise ValueError("actual proof/request/generated-source/pipeline binding differs")
            expected_failure = None if replay["status"] == "verified" else "IMPLEMENTATION_FAILED"
            if (reply["kernel_checked"] is not (replay["status"] == "verified") or reply["failure_class"] != expected_failure
                    or replay["execution_class"] != "trusted_local_authored_reference" or replay["isolated"] is not False):
                raise ValueError("actual authored kernel/control evidence class differs")
    return {"checked_probes": len(results), "checked_replays": len(execution_ids)}
