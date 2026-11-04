"""Adversarial ordering/leakage checks, not a model or mathematics benchmark."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_learning_validity import (
    DecisionSession,
    challenge_task,
    decision_report,
    stage_a_input,
    validate_probe,
)


def synthetic_probe(*, pair=None, decision="holds"):
    return {"probe_id": str(uuid4()), "pair_id": pair or str(uuid4()), "cluster_id": "synthetic-test-only",
        "parent_core_ids": ["synthetic-parent"], "parent_contracts": {"synthetic-parent": "a" * 64},
        "canonical_relation": "diagnostic_contract_candidate", "split": "test_public",
        "question": "Synthetic software check only: decide the displayed equality.",
        "assumptions": ["Software fixture, not a released quantum problem."], "conventions": ["Natural-number equality."],
        "formal_context": {"imports": ["Mathlib"], "proposition": "1 = 1" if decision == "holds" else "1 = 2"},
        "gold": {"decision": decision, "reference_proof": "PRIVATE_PROOF_SENTINEL",
                 "answer": "PRIVATE_ANSWER_SENTINEL", "rubric": [{"id": "reason", "criterion": "PRIVATE_RUBRIC_SENTINEL", "weight": 1}]},
        "source_nodes": ["PRIVATE_SOURCE_SENTINEL"], "reasoning_kind": "assumption_diagnosis",
        "difficulty": {"band": "D1", "rationale": "Synthetic ingestion test only.", "status": "provisional_author_mathematical_assessment", "measured_model_difficulty": None},
        "author_identity": "synthetic-test-author", "formal_coverage": "decision_polarity_only"}


class LearningValidityTests(unittest.TestCase):
    def setUp(self):
        pair = str(uuid4())
        self.probes = [synthetic_probe(pair=pair), synthetic_probe(pair=pair, decision="refuted")]
        self.packet = {"probes": self.probes}

    def session(self, probe=None):
        return DecisionSession(probe or self.probes[0], snapshot_id="fixture", library_revision="b" * 40)

    def answer(self, decision="holds"):
        return {"decision": decision, "explanation": "Synthetic recorded argument, not an adjudicated explanation."}

    def test_stage_a_allowlist_drops_all_gold_formal_and_source_metadata(self):
        probe = self.probes[0]
        probe["future_solution_field"] = {"answer": "PRIVATE_NEW_FIELD"}
        public = stage_a_input(probe)
        text = str(public)
        for value in ("PRIVATE_", "formal_context", "proposition", "gold", "source_nodes", "parent_core_ids", "pair_id", "cluster_id"):
            self.assertNotIn(value, text)
        public["assumptions"].append("mutation")
        self.assertNotIn("mutation", probe["assumptions"])

    def test_secret_polarity_cannot_be_guessed_from_public_state_hash(self):
        other = deepcopy(self.probes[0])
        other["gold"]["decision"] = "refuted"
        other["gold"]["answer"] = "another hidden gold"
        with patch("qcb_learning_validity.secrets.token_hex", return_value="fixed-software-test-session"):
            left, right = self.session(), self.session(other)
        self.assertEqual(left.input(), right.input())
        for session in (left, right):
            session.commit(self.answer(), state_id=session.state_id)
        self.assertEqual(left.state_id, right.state_id)
        self.assertEqual(left.challenge(state_id=left.state_id), right.challenge(state_id=right.state_id))

    def test_initial_decision_is_sealed_before_challenge_and_cannot_be_replaced(self):
        session = self.session()
        initial = session.state_id
        with self.assertRaisesRegex(ValueError, "precede"):
            session.challenge(state_id=initial)
        session.commit(self.answer("refuted"), state_id=initial)
        for state in (initial, session.state_id):
            with self.assertRaises(ValueError):
                session.commit(self.answer("holds"), state_id=state)
        challenge = session.challenge(state_id=session.state_id)
        self.assertEqual(challenge["task"]["nodes"][0]["target"], "¬ (1 = 1)")
        self.assertNotEqual(challenge["task"]["nodes"][0]["target"], self.probes[0]["formal_context"]["proposition"])
        self.assertIn("ENV_BLOCKED", challenge["model_generated_proof_execution"])
        self.assertEqual(len(challenge["task"]["nodes"]), 1)
        with self.assertRaises(ValueError):
            session.challenge(state_id=session.state_id)

    def test_bad_answer_is_not_committed_and_model_cannot_submit_its_own_grade(self):
        session = self.session()
        for response in ({**self.answer(), "correct": True}, {"decision": "holds", "explanation": ""}, {"decision": True, "explanation": "x"}):
            with self.assertRaises(ValueError):
                session.commit(response, state_id=session.state_id)
            self.assertEqual(session.operator_record()["generation_status"], "not_run")

    def test_abstention_is_distinct_from_wrong_and_has_no_proof_challenge(self):
        session = self.session()
        session.commit(self.answer("abstain"), state_id=session.state_id)
        with self.assertRaises(ValueError):
            session.challenge(state_id=session.state_id)
        report = decision_report(self.packet, [session.operator_record()], evidence_kind="synthetic_fixture")
        self.assertEqual(report["outcomes"]["abstained"], 1)
        self.assertEqual(report["outcomes"]["not_submitted"], 1)
        self.assertIsNone(report["decision_accuracy_on_answered"])
        self.assertEqual(report["complete_contrast_pairs"], 0)

    def test_always_holds_baseline_cannot_pass_balanced_contrast(self):
        records = []
        for probe in self.probes:
            session = self.session(probe)
            session.commit(self.answer(), state_id=session.state_id)
            records.append(session.operator_record())
        report = decision_report(self.packet, records, evidence_kind="synthetic_fixture")
        self.assertEqual(report["decision_accuracy_on_answered"], 0.5)
        self.assertEqual(report["pair_joint_decision_accuracy_on_complete"], 0)
        self.assertFalse(report["understanding_established"])
        for field in ("semantic_explanation_accuracy", "formal_proof_accuracy", "learning_gain"):
            self.assertIsNone(report[field])

    def test_blocked_and_missing_outcomes_are_not_turned_into_wrong_answers(self):
        record = {"probe_id": self.probes[0]["probe_id"], "generation_status": "env_blocked", "answer": None, "answer_digest": None}
        report = decision_report(self.packet, [record], evidence_kind="operator_model_observation")
        self.assertEqual(report["outcomes"]["env_blocked"], 1)
        self.assertEqual(report["outcomes"]["not_submitted"], 1)
        self.assertIsNone(report["rows"][0]["decision_correct"])
        self.assertIsNone(report["decision_accuracy_on_answered"])
        with self.assertRaises(ValueError):
            decision_report(self.packet, [record, record], evidence_kind="unattested_import")

    def test_decision_report_rejects_forged_proof_and_semantic_scores(self):
        session = self.session()
        session.commit(self.answer(), state_id=session.state_id)
        record = session.operator_record()
        for key, value in (("formal_root_correct", True), ("semantic_review", {"approved": True})):
            with self.assertRaises(ValueError):
                decision_report(self.packet, [{**record, key: value}], evidence_kind="operator_model_observation")
        record["answer"]["explanation"] = "changed after binding"
        with self.assertRaises(ValueError):
            decision_report(self.packet, [record], evidence_kind="unattested_import")

    def test_neutral_proposition_cannot_inject_an_import_or_new_proof_slot(self):
        for statement in ("True := by trivial", "True\nimport Lean", 'True -- hidden'):
            probe = deepcopy(self.probes[0])
            probe["formal_context"]["proposition"] = statement
            with self.assertRaises(ValueError):
                validate_probe(probe)
        probe = deepcopy(self.probes[0])
        probe["formal_context"]["imports"] = ["Mathlib\nimport Lean"]
        with self.assertRaises(ValueError):
            challenge_task(probe, "holds", snapshot_id="fixture", library_revision="b" * 40)


if __name__ == "__main__":
    unittest.main()
