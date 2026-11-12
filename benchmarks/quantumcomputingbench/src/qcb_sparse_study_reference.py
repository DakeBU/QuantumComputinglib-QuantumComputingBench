"""Replay only the fixed owner-reviewed sparse assessment references."""
from copy import deepcopy
from time import monotonic

from qcb_assessment_v3 import _committed
from qcb_core import digest
from qcb_learning_reference import (
    REFERENCE_PROFILE, _RecordedAuthoredVerifier, _compact_evidence, validate_reference_results,
)
from qcb_learning_validity import challenge_task
from qcb_proof_session import ProofSession, SessionLimits
from qcb_sparse_study import CHECKS, current_commit, load_private_bank, pipeline_identity

NEGATIVES = {"wrong_target": "by exact True.intro", "sorry_axiom": "by sorry"}


async def replay(directory, build_root, *, progress):
    packet, seal = load_private_bank(directory, require_qualified=False)
    identity, commit = pipeline_identity(), current_commit()
    _committed(identity, commit)
    start = monotonic()
    rows = []

    def session_for(task, verifier):
        remaining = REFERENCE_PROFILE["batch_wall_seconds"] - (monotonic() - start)
        if remaining <= 0:
            raise TimeoutError("authored sparse reference budget exhausted")
        return ProofSession(task, verifier, mode="root_only", limits=SessionLimits(
            wall_seconds=min(REFERENCE_PROFILE["session_wall_seconds"], remaining),
            check_seconds=REFERENCE_PROFILE["check_seconds"]))

    async def submit(session, proof):
        return await session.act({"kind": "submit", "state_id": session.state_id,
                                  "node_id": "assessment_root", "proof": proof})

    for index, probe in enumerate(packet["probes"]):
        decision, proof = (probe["gold"][key] for key in ("decision", "reference_proof"))
        task = challenge_task(probe, decision, snapshot_id=packet["snapshot_id"],
                              library_revision=packet["library_revision"])
        controls = NEGATIVES if index == 0 else {}
        verifier = _RecordedAuthoredVerifier(task, {"assessment_root": [proof, *controls.values()]}, build_root)
        session = session_for(task, verifier)
        submitted = await submit(session, proof)
        finished = await session.act({"kind": "finish", "state_id": session.state_id})
        progress({"probe_id": probe["probe_id"], "submitted": submitted,
                  "finished": finished, "replays": deepcopy(verifier.replays)})
        if not session.report()["formal_root_checked"]:
            raise RuntimeError("fixed sparse reference failed; consult private replay transcript")
        rejected = []
        for name, bad in controls.items():
            reply = await submit(session_for(task, verifier), bad)
            progress({"probe_id": probe["probe_id"], "control": name, "reply": reply,
                      "replay": verifier.replays[-1]})
            rejected.append({"kind": name, "status": reply["status"],
                             "evidence": _compact_evidence(reply.get("evidence"))})
        rows.append({"probe_id": probe["probe_id"], "probe_digest": digest(probe),
                     "task_hash": digest(task), "formal_target_sha256": digest(task["nodes"][0]["target"]),
                     "gold_polarity": decision, "submitted_status": submitted["status"],
                     "finish_status": finished["status"], "formal_root_checked": True,
                     "submission_evidence": _compact_evidence(submitted["evidence"]),
                     "final_evidence": _compact_evidence(finished["final_replay"]),
                     "negative_controls": rejected, "replays": deepcopy(verifier.replays)})

    validated = validate_reference_results(packet, rows)
    if validated["checked_replays"] != CHECKS["total"] or identity != pipeline_identity():
        raise ValueError("sparse reference accounting or pipeline changed")
    return {"schema_version": "qcb.sparse_authored_reference_receipt.v1", "seal_digest": digest(seal),
            "cohort_digest": digest(packet), "tested_code_commit": commit,
            "pipeline_source_hashes_lf": identity, "profile": REFERENCE_PROFILE, "passed": True,
            "results": rows, "elapsed_seconds": monotonic() - start,
            "execution_class": "trusted_local_authored_reference", "isolated": False, "model_calls": 0}
