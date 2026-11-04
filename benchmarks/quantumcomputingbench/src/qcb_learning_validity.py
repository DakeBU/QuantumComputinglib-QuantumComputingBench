"""Staged quantum-semantic assessment, separate from proof or learning success.

Stage A deliberately excludes Lean statements, source identifiers and gold.
An immutable first decision precedes the Stage B proof challenge. The latter
follows the submitted belief, not the reference polarity. This module executes
neither models nor Lean and does not authenticate imported execution records.
"""
from __future__ import annotations

import secrets
from collections import Counter
from copy import deepcopy
from pathlib import Path
from uuid import UUID

from qcb_core import digest, read_json
from qcb_lean import _trusted_target
from qcb_proof_session import validate_task

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
COHORT = B / "tracks/lean/learning-validity/v1/cohort.json"
DECISIONS = {"holds", "refuted", "abstain"}
OUTCOMES = {"answered", "abstained", "not_run", "env_blocked", "protocol_error", "budget_exhausted"}
PROBE_FIELDS = {
    "probe_id", "pair_id", "cluster_id", "parent_core_ids", "parent_contracts", "canonical_relation",
    "split", "question", "assumptions", "conventions", "formal_context", "gold", "source_nodes",
    "reasoning_kind", "difficulty", "author_identity", "formal_coverage",
}


def _uuid(value):
    try:
        return isinstance(value, str) and str(UUID(value)) == value
    except (ValueError, TypeError, AttributeError):
        return False


def _text(value, label, limit=64000):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError("bounded nonempty text required: " + label)


def validate_probe(probe):
    if not isinstance(probe, dict) or set(probe) != PROBE_FIELDS:
        raise ValueError("unexpected diagnostic fields; use a separate unadmitted probe contract")
    if not _uuid(probe["probe_id"]) or not _uuid(probe["pair_id"]):
        raise ValueError("opaque UUID probe and pair identities required")
    for key in ("cluster_id", "question", "author_identity"):
        _text(probe[key], key)
    if probe["split"] not in {"train", "dev", "test_public"}:
        raise ValueError("probe split must retain known source/alias obligations")
    if probe["canonical_relation"] not in {"possible_alias", "diagnostic_contract_candidate"}:
        raise ValueError("diagnostics cannot grant their own canonical admission")
    if probe["formal_coverage"] != "decision_polarity_only":
        raise ValueError("a polarity certificate must not certify the full NL explanation")
    for key in ("assumptions", "conventions", "parent_core_ids", "source_nodes"):
        values = probe[key]
        if not isinstance(values, list) or len(set(values)) != len(values) or any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError("invalid ordered source/premise list: " + key)
    if not probe["parent_core_ids"] or not probe["source_nodes"] or set(probe["parent_contracts"]) != set(probe["parent_core_ids"]):
        raise ValueError("source parents and exact reserved contract bindings required")
    context = probe["formal_context"]
    if not isinstance(context, dict) or set(context) != {"imports", "proposition"}:
        raise ValueError("neutral proposition and frozen imports required")
    _trusted_target(context["proposition"])
    gold = probe["gold"]
    if not isinstance(gold, dict) or set(gold) != {"decision", "reference_proof", "answer", "rubric"} or gold["decision"] not in {"holds", "refuted"}:
        raise ValueError("gold polarity is private evaluator data, never an abstention")
    _text(gold["reference_proof"], "reference proof", 16000)
    _text(gold["answer"], "reference answer")
    rubric = gold["rubric"]
    if not isinstance(rubric, list) or not rubric:
        raise ValueError("substantive criterion rubric required")
    criterion_ids = set()
    for criterion in rubric:
        if (not isinstance(criterion, dict) or set(criterion) != {"id", "criterion", "weight"}
                or criterion["id"] in criterion_ids or type(criterion["weight"]) is not int
                or not 1 <= criterion["weight"] <= 100):
            raise ValueError("criterion IDs and bounded integer weights required")
        _text(criterion["id"], "criterion identity", 128)
        _text(criterion["criterion"], "criterion")
        criterion_ids.add(criterion["id"])
    if probe["reasoning_kind"] not in {"assumption_diagnosis", "representation_transport", "composition", "boundary_counterfactual", "norm_vs_linearity"}:
        raise ValueError("unknown semantic assessment mechanism")
    difficulty = probe["difficulty"]
    if (not isinstance(difficulty, dict) or set(difficulty) != {"band", "rationale", "status", "measured_model_difficulty"}
            or difficulty["band"] not in {"D1", "D2", "D3", "D4"}
            or difficulty["status"] != "provisional_author_mathematical_assessment"
            or difficulty["measured_model_difficulty"] is not None):
        raise ValueError("construction bands do not establish measured model difficulty")
    _text(difficulty["rationale"], "difficulty rationale")
    return deepcopy(probe)


def challenge_task(probe, decision, *, snapshot_id, library_revision):
    """Freeze P or not-P from the submitted belief, without consulting gold."""
    if decision not in {"holds", "refuted"}:
        raise ValueError("an abstention has no formal belief to challenge")
    context = probe["formal_context"]
    target = context["proposition"] if decision == "holds" else "¬ (" + context["proposition"] + ")"
    contract = {"probe_id": probe["probe_id"], "imports": context["imports"], "proposition": context["proposition"],
                "decision": decision, "assumptions": probe["assumptions"], "conventions": probe["conventions"]}
    return validate_task({"schema_version": "qcb.proof_obligation_task.v1",
        "core_id": "candidate:" + probe["probe_id"], "contract_hash": digest(contract),
        "family": probe["cluster_id"], "split": probe["split"], "snapshot_id": snapshot_id,
        "library_revision": library_revision, "imports": context["imports"], "question": probe["question"],
        "assumptions": probe["assumptions"], "conventions": probe["conventions"],
        "root_id": "assessment_root", "nodes": [{"id": "assessment_root", "target": target, "depends_on": []}],
        "interfaces": [], "alignment_status": "experimental_diagnostic_not_canonical; decision_polarity_only"})


def load_cohort(path=COHORT):
    import sys

    from qcb_curriculum import load_catalog
    from qcb_integrity import text_sha
    sys.path.insert(0, str(R / "website/scripts"))
    from proof_inputs import proof_input_digest
    packet = read_json(path)
    expected = {"schema_version", "cohort_id", "base_commit", "library_revision", "proof_inputs_sha256",
                "lean_toolchain", "catalog_hash", "snapshot_id", "source_bindings", "probes",
                "admission", "new_canonical_formal_admissions", "model_performance_measured", "blind_test"}
    if (set(packet) != expected or packet["schema_version"] != "qcb.learning_validity_cohort.v1"
            or not _uuid(packet["cohort_id"]) or packet["admission"] != "candidate_not_counted"
            or type(packet["new_canonical_formal_admissions"]) is not int or packet["new_canonical_formal_admissions"] != 0
            or packet["model_performance_measured"] is not False or packet["blind_test"] is not False):
        raise ValueError("diagnostic cohort cannot promote its own mathematical or model claims")
    catalog, _, graph = load_catalog()
    if (packet["catalog_hash"] != catalog["catalog_hash"] or packet["snapshot_id"] != catalog["snapshot_id"]
            or packet["proof_inputs_sha256"] != proof_input_digest(R)
            or packet["lean_toolchain"] != (R / "lean-toolchain").read_text().strip()):
        raise ValueError("cohort source/snapshot bindings changed")
    sources = packet["source_bindings"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("source-bound diagnostic context required")
    for source in sources:
        path = R / source["path"]
        if (set(source) != {"path", "sha256_lf"} or not path.resolve().is_relative_to(R)
                or not source["path"].startswith("QuantumBlockEncoding/") or text_sha(path) != source["sha256_lf"]):
            raise ValueError("diagnostic source file binding mismatch")
    probes = packet["probes"]
    if not isinstance(probes, list) or not 2 <= len(probes) <= 64:
        raise ValueError("bounded nonvacuous diagnostic cohort required")
    known = {c["core_id"]: c for c in catalog["cores"]}
    ids, pairs, pair_clusters = set(), {}, {}
    for raw in probes:
        probe = validate_probe(raw)
        if probe["probe_id"] in ids:
            raise ValueError("duplicate diagnostic identity")
        ids.add(probe["probe_id"])
        for parent in probe["parent_core_ids"]:
            if (parent not in known or probe["parent_contracts"][parent] != known[parent]["contract_hash"]
                    or probe["split"] != known[parent]["split"]):
                raise ValueError("parent contract or inherited split changed; quarantine the composition")
        for node in probe["source_nodes"]:
            if node not in graph or graph[node].get("inventory_status") != "Compiled" or graph[node].get("open_obligation") is not False:
                raise ValueError("planned/uncompiled anchors cannot become checked diagnostic gold")
        pair = probe["pair_id"]
        pairs.setdefault(pair, []).append(probe["gold"]["decision"])
        pair_clusters.setdefault(pair, set()).add(probe["cluster_id"])
        for decision in ("holds", "refuted"):
            challenge_task(probe, decision, snapshot_id=packet["snapshot_id"], library_revision=packet["library_revision"])
    if any(Counter(values) != {"holds": 1, "refuted": 1} or len(pair_clusters[key]) != 1 for key, values in pairs.items()):
        raise ValueError("each contrast must contain one true and one refuted proposition in one cluster")
    return packet, {"cohort_digest": digest(packet), "diagnostic_probes": len(probes), "contrast_pairs": len(pairs),
                    "independent_cluster_count_claimed": False, "clusters": sorted({p["cluster_id"] for p in probes}),
                    "new_mathematical_cores_admitted": 0, "canonical_admissions_changed": False,
                    "model_performance_measured": False, "learning_gain": None, "blind_test": False}


def stage_a_input(probe):
    """Explicit allowlist: changing evaluator metadata cannot expose an answer."""
    return {"schema_version": "qcb.semantic_decision_input.v1", "probe_id": probe["probe_id"],
            "question": probe["question"], "assumptions": deepcopy(probe["assumptions"]),
            "conventions": deepcopy(probe["conventions"]),
            "response_format": {"decision": "holds | refuted | abstain", "explanation": "Your mathematical argument or precise witness; include the required boundary/repair reasoning."}}


def validate_answer(answer):
    if not isinstance(answer, dict) or set(answer) != {"decision", "explanation"} or answer["decision"] not in DECISIONS:
        raise ValueError("answer contains only a decision and its mathematical explanation")
    _text(answer["explanation"], "explanation", 16000)
    return deepcopy(answer)


class DecisionSession:
    """Harness-mediated ordering, not a guarantee against out-of-band exposure."""
    def __init__(self, probe, *, snapshot_id, library_revision):
        self._probe = validate_probe(probe)
        self._snapshot, self._revision = snapshot_id, library_revision
        self._public = stage_a_input(probe)
        self._session_id = secrets.token_hex(16)
        self._answer = None
        self._challenge = None

    @property
    def state_id(self):
        # Never hash secret gold into a model-visible state: a binary unknown
        # could otherwise be tested by recomputing two candidate hashes.
        return digest({"session_id": self._session_id, "public": self._public, "answer": self._answer,
                       "challenge_requested": self._challenge is not None})

    def input(self):
        return {**deepcopy(self._public), "state_id": self.state_id}

    def commit(self, answer, *, state_id):
        if state_id != self.state_id or self._answer is not None:
            raise ValueError("stale state or attempted overwrite of the sealed initial decision")
        self._answer = validate_answer(answer)
        return {"status": "decision_sealed", "state_id": self.state_id, "answer_digest": digest(self._answer)}

    def challenge(self, *, state_id):
        if state_id != self.state_id or self._answer is None:
            raise ValueError("a sealed semantic decision must precede formal feedback")
        if self._challenge is not None:
            raise ValueError("a formal challenge is issued once; retain its fixed identity")
        self._challenge = challenge_task(self._probe, self._answer["decision"], snapshot_id=self._snapshot,
                                         library_revision=self._revision)
        return {"schema_version": "qcb.sealed_semantic_challenge.v1", "state_id": self.state_id,
                "initial_answer_digest": digest(self._answer), "task": deepcopy(self._challenge),
                "exposure": "imported_api; no supplied intermediate DAG; exact-root source shortcuts may remain callable",
                "model_generated_proof_execution": "ENV_BLOCKED; no accepted isolated executor connected"}

    def operator_record(self):
        return {"probe_id": self._probe["probe_id"], "session_id": self._session_id,
                "generation_status": "not_run" if self._answer is None else "abstained" if self._answer["decision"] == "abstain" else "answered",
                "answer": deepcopy(self._answer), "answer_digest": None if self._answer is None else digest(self._answer),
                "challenge_hash": None if self._challenge is None else digest(self._challenge),
                "semantic_review": None, "formal_root_correct": None, "model_performance_measured": False,
                "evidence_note": "Operator transcript only; imported JSON is not authenticated model/verifier evidence."}


def decision_report(packet, records, *, evidence_kind):
    """Binary decisions are diagnostic; explanations remain separately ungraded."""
    if evidence_kind not in {"synthetic_fixture", "unattested_import", "operator_model_observation"}:
        raise ValueError("explicit observation provenance required")
    index = {p["probe_id"]: p for p in packet["probes"]}
    observed = {}
    statuses = Counter()
    rows = []
    for record in records:
        key = record["probe_id"]
        if key not in index or key in observed or record["generation_status"] not in OUTCOMES:
            raise ValueError("unknown/duplicate probe or untyped generation outcome")
        status = record["generation_status"]
        answer = record.get("answer")
        if status in {"answered", "abstained"}:
            answer = validate_answer(answer)
            if (answer["decision"] == "abstain") != (status == "abstained") or record.get("answer_digest") != digest(answer):
                raise ValueError("answer status or content binding differs")
        elif answer is not None or record.get("answer_digest") is not None:
            raise ValueError("unanswered outcome must not carry an invented answer")
        if record.get("formal_root_correct") is not None or record.get("semantic_review") is not None:
            raise ValueError("decision-only reporting cannot accept self-declared proof or semantic grades")
        correct = None if status != "answered" else answer["decision"] == index[key]["gold"]["decision"]
        row = {"probe_id": key, "generation_status": status, "decision_correct": correct,
               "explanation_correct": None, "formal_root_correct": None}
        observed[key] = row
        statuses[status] += 1
        rows.append(row)
    statuses["not_submitted"] = len(index) - len(observed)
    answered = [r for r in rows if r["decision_correct"] is not None]
    pairs = {}
    for probe in packet["probes"]:
        pairs.setdefault(probe["pair_id"], []).append(probe["probe_id"])
    complete_pairs = [keys for keys in pairs.values() if all(key in observed and observed[key]["decision_correct"] is not None for key in keys)]
    return {"schema_version": "qcb.semantic_decision_report.v1", "cohort_digest": digest(packet),
            "evidence_kind": evidence_kind, "planned_probes": len(index), "outcomes": dict(statuses),
            "answered_probes": len(answered), "complete_contrast_pairs": len(complete_pairs),
            "decision_accuracy_on_answered": None if not answered else sum(r["decision_correct"] for r in answered) / len(answered),
            "pair_joint_decision_accuracy_on_complete": None if not complete_pairs else sum(all(observed[k]["decision_correct"] for k in keys) for keys in complete_pairs) / len(complete_pairs),
            "semantic_explanation_accuracy": None, "formal_proof_accuracy": None, "learning_gain": None,
            "understanding_established": False, "actual_model_identity_authenticated": False,
            "scope": "Polarity discrimination only, not full semantic approval, proof success, or observed learning.", "rows": rows}
