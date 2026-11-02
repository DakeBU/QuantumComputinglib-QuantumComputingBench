"""The agentic frontier must not turn warmups or public gold into new claims."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_agentic import audit_catalog, export_warmups
from qcb_core import digest
from qcb_curriculum import load_catalog


class AgenticFrontierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.items, _ = load_catalog()

    def test_counts_are_views_not_new_mathematics_or_model_results(self):
        audit = audit_catalog(self.catalog)
        expected = [c for c in self.catalog["cores"] if "lean" in c["views"]]
        self.assertEqual(audit["counts"]["lean_warmup_views"], len(expected))
        self.assertEqual(audit["counts"]["distinct_lean_warmup_cores"], len(expected))
        self.assertEqual(audit["evidence_boundaries"]["new_core_admissions"], 0)
        self.assertFalse(audit["evidence_boundaries"]["deep_proof_synthesis_established"])
        self.assertFalse(audit["evidence_boundaries"]["model_performance_measured"])
        self.assertEqual(len(audit["capabilities"]), 6)

    def test_export_has_no_gold_and_preserves_contract_split_and_exact_target(self):
        export = export_warmups(self.catalog, self.items)
        cores = {c["core_id"]: c for c in self.catalog["cores"]}
        for task in export["tasks"]:
            core = cores[task["core_id"]]
            for k in ("family", "split", "contract_hash", "snapshot_id"):
                self.assertEqual(task[k], core[k])
            self.assertEqual(task["formal_context"], core["views"]["lean"]["formal_context"])
            for k in ("reference_proof", "reference_answer", "rubric", "reviews", "native_nl"):
                self.assertNotIn(k, task)
            self.assertEqual(task["task_hash"], digest({k: v for k, v in task.items() if k != "task_hash"}))
        self.assertEqual(export["distinct_mathematical_cores"], len(export["tasks"]))
        self.assertIn("not blind", export["answer_exposure"])
        self.assertIn("disabled", export["candidate_execution"])

    def test_export_returns_copies_and_does_not_copy_untrusted_new_metadata(self):
        export = export_warmups(self.catalog, self.items)
        export["tasks"][0]["formal_context"]["imports"].append("Forbidden.NewImport")
        again = export_warmups(self.catalog, self.items)
        self.assertNotIn("Forbidden.NewImport", again["tasks"][0]["formal_context"]["imports"])
        changed = deepcopy(self.catalog)
        for core in changed["cores"]:
            if "lean" in core["views"]:
                core["views"]["lean"]["formal_context"]["private_note"] = "SECRET_GOLD_SENTINEL"
        self.assertNotIn("SECRET_GOLD_SENTINEL", str(export_warmups(changed, self.items)))

    def test_changed_question_or_split_cannot_inherit_a_formal_view(self):
        key = audit_catalog(self.catalog)["formal_core_ids"][0]
        for field, value in (("question", "An easier different question"), ("split", "dev")):
            items = deepcopy(self.items)
            items[key][field] = value
            with self.assertRaisesRegex(ValueError, "canonical core"):
                export_warmups(self.catalog, items)

    def test_duplicate_or_withheld_core_cannot_enter_tasks(self):
        catalog = deepcopy(self.catalog)
        catalog["cores"].append(deepcopy(catalog["cores"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit_catalog(catalog)
        catalog = deepcopy(self.catalog)
        catalog["withheld_cores"].append(deepcopy(catalog["cores"][0]))
        with self.assertRaisesRegex(ValueError, "overlap"):
            export_warmups(catalog, self.items)

    def test_future_task_kinds_require_explicit_new_admission_logic(self):
        catalog = deepcopy(self.catalog)
        core = next(c for c in catalog["cores"] if "lean" in c["views"])
        core["views"]["lean"]["task_kind"] = "deep_multi_node_synthesis"
        with self.assertRaisesRegex(ValueError, "unsupported"):
            audit_catalog(catalog)

    def test_split_projection_does_not_reallocate_cores(self):
        complete = export_warmups(self.catalog, self.items)
        parts = [export_warmups(self.catalog, self.items, split=s)
                 for s in ("train", "dev", "test_public")]
        self.assertEqual(sorted(t["task_id"] for t in complete["tasks"]),
                         sorted(t["task_id"] for part in parts for t in part["tasks"]))
        with self.assertRaisesRegex(ValueError, "unknown split"):
            export_warmups(self.catalog, self.items, split="private_test")


if __name__ == "__main__":
    unittest.main()
