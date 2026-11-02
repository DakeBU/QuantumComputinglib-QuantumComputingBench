"""Content-bound diagnostics never become formal or model certificates."""
import asyncio
import sys
import unittest
from copy import deepcopy
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_capabilities import assess, validate_rubric
from qcb_capability_pilot import (
    load_capability_pilot,
    reports_from_record,
    validate_engineered_examples,
)
from qcb_core import digest
from qcb_proof_session import ProofSession


class CapabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases, cls.identity = load_capability_pilot()
        cls.case = cls.cases[0]

    def report(self, *, explanation=None, returned=(), exposure="approved_interface"):
        session = ProofSession(self.case["task"], exposure=exposure)
        if explanation is not None:
            asyncio.run(session.act({"kind": "explain", "state_id": session.state_id, "answer": explanation}))
        report = session.report()
        if returned:
            # Synthetic evaluator-owned retrieval observations isolate AND/OR
            # arithmetic; no claim that these rows were returned by a real run.
            entries = [deepcopy(e) for e in self.case["task"]["interfaces"] if e["name"] in returned]
            for index in range(0, len(entries), 6):
                report["events"].append({"action": {"kind": "search"},
                                         "response": {"status": "returned", "entries": entries[index:index+6]}})
        return report

    def adjudication(self, report):
        rubric = self.case["capability_rubric"]
        return {"schema_version": "qcb.explanation_adjudication.v1", "task_hash": digest(self.case["task"]),
                "report_digest": digest(report), "rubric_digest": digest(rubric), "answer_index": 0,
                "answer_digest": digest(report["explanations"][0]),
                "reviewer": {"identity": "unit-test-evaluator", "kind": "ai", "method": "Synthetic expected labels only"},
                "respondent_identity": "unit-test-respondent", "semantic_fidelity": "faithful",
                "reasoning": "Engineered software fixture, not a model or new semantic review.",
                "criteria": [{"id": c["id"], "score": 1, "reasoning": "Fixed test expectation."}
                             for c in rubric["knowledge_criteria"]]}

    def assess(self, report, adjudication=None, rubric=None):
        return assess(self.case["task"], report, rubric or self.case["capability_rubric"], adjudication)

    def test_whole_canonical_rubric_includes_normalization_propagation(self):
        rubric = self.case["capability_rubric"]
        self.assertEqual(rubric["knowledge_source"]["criterion_ids"], ["r1", "r2", "r3", "r4"])
        self.assertIn("normalization invariant", rubric["knowledge_criteria"][-1]["criterion"])
        changed = deepcopy(rubric)
        changed["knowledge_criteria"].pop()
        with self.assertRaises(ValueError):
            validate_rubric(self.case["task"], changed)
        changed = deepcopy(rubric)
        changed["knowledge_source"]["item_digest"] = "f" * 64
        with self.assertRaises(ValueError):
            validate_rubric(self.case["task"], changed)

    def test_leaf_group_is_not_a_complete_root_route_and_empty_groups_stay_unscored(self):
        names = self.case["capability_rubric"]["obligation_groups"][0]["required_names"]
        result = self.assess(self.report(returned=names))["retrieval"]
        self.assertAlmostEqual(result["curated_target_coverage"], 3/7)
        self.assertFalse(result["curated_route_complete"])
        self.assertTrue(result["obligation_groups"][0]["local_interface_group_complete"])
        self.assertIsNone(result["obligation_groups"][-1]["local_interface_group_complete"])
        self.assertFalse(result["local_groups_are_root_alternatives"])

    def test_all_retrieved_interfaces_do_not_award_proof_or_semantic_credit(self):
        result = self.assess(self.report(returned=[e["name"] for e in self.case["task"]["interfaces"]]))
        self.assertTrue(result["retrieval"]["curated_route_complete"])
        self.assertIsNone(result["explanation"]["weighted_supplied_mark"])
        self.assertFalse(result["formal_root_status_from_evaluator_record"])
        self.assertFalse(result["formal_certificate_issued_by_this_assessment"])
        self.assertFalse(result["model_performance_measured"])
        self.assertIsNone(result["joint_capability_score"])

    def test_root_routes_use_or_between_alternatives_and_and_inside_each(self):
        rubric = deepcopy(self.case["capability_rubric"])
        names = [e["name"] for e in self.case["task"]["interfaces"]]
        rubric["routes"] = [{**rubric["routes"][0], "id": "synthetic-route-a", "required_names": names[:2]},
                            {**rubric["routes"][0], "id": "synthetic-route-b", "required_names": names[2:4]}]
        self.assertFalse(self.assess(self.report(returned=[names[0], names[2]]), rubric=rubric)["retrieval"]["curated_route_complete"])
        self.assertTrue(self.assess(self.report(returned=names[:2]), rubric=rubric)["retrieval"]["curated_route_complete"])
        rubric["routes"][0]["required_names"] = []
        with self.assertRaises(ValueError):
            self.assess(self.report(), rubric=rubric)

    def test_closed_book_is_not_a_zero_retrieval_grade_and_changed_interfaces_are_rejected(self):
        result = self.assess(self.report(exposure="closed_book"))["retrieval"]
        self.assertIsNone(result["curated_target_coverage"])
        report = self.report(returned=[self.case["task"]["interfaces"][0]["name"]])
        report["events"][-1]["response"]["entries"][0]["type"] = "False"
        with self.assertRaises(ValueError):
            self.assess(report)

    def test_supplied_marks_stay_distinct_from_fidelity_and_kernel_truth(self):
        report = self.report(explanation="A fixed software-test explanation.")
        mark = self.adjudication(report)
        result = self.assess(report, mark)["explanation"]
        self.assertEqual(result["weighted_supplied_mark"], 1)
        self.assertFalse(result["kernel_certified"])
        self.assertFalse(result["reviewer_authenticity_or_independence_verified_by_schema"])
        mark["semantic_fidelity"] = "uncertain"
        self.assertIsNone(self.assess(report, mark)["explanation"]["weighted_supplied_mark"])

    def test_stale_partial_nonfinite_or_self_graded_adjudications_fail_closed(self):
        report = self.report(explanation="An unchanged answer.")
        changes = [lambda m: m.update(answer_digest="stale"), lambda m: m.update(report_digest="stale"),
                   lambda m: m.update(rubric_digest="stale"), lambda m: m.update(answer_index=True),
                   lambda m: m["criteria"].pop(), lambda m: m["criteria"][0].update(score=float("nan")),
                   lambda m: m.update(respondent_identity="unit-test-evaluator")]
        for change in changes:
            mark = self.adjudication(report)
            change(mark)
            with self.assertRaises(ValueError):
                self.assess(report, mark)

    def test_changed_explanations_and_duplicate_report_sets_are_rejected(self):
        report = self.report(explanation="Recorded answer.")
        report["explanations"][0] = "Unrecorded replacement."
        with self.assertRaises(ValueError):
            self.assess(report)
        with self.assertRaises(ValueError):
            reports_from_record({"schema_version": "qcb.authored_obligation_smoke.v1", "results": [{"session": report}, {"session": report}]})

    def test_changed_fixed_text_labels_or_provenance_cannot_reuse_expectations(self):
        examples = self.case["engineered_explanations"]
        canonical = [{k: c[k] for k in ("id", "criterion", "weight")} for c in self.case["capability_rubric"]["knowledge_criteria"]]
        changes = [lambda e: e[0].update(answer="No mathematical argument."),
                   lambda e: e[0]["canonical_criteria"].pop("r4"),
                   lambda e: e[0]["canonical_criteria"]["r1"].update(verdict="unreviewed"),
                   lambda e: e[0]["assumption_audit"].update(contract_preserved=1),
                   lambda e: e[0].update(model_answer=True)]
        for change in changes:
            value = deepcopy(examples)
            change(value)
            with self.assertRaises(ValueError):
                validate_engineered_examples(value, canonical)


if __name__ == "__main__":
    unittest.main()
