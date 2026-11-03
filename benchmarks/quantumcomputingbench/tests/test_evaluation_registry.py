"""Registered reference qualification preserves exact scope and source lineage."""
import json
import sys
import unittest
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import digest, read_json
from qcb_evaluation_registry import MANIFEST, SOURCES, export_views, qualify


@lru_cache(maxsize=1)
def context():
    manifest = read_json(MANIFEST)
    cohorts = {name: s["loader"]() for name, s in SOURCES.items()}
    records = {name: read_json(B / s["checkpoint"]) for name, s in SOURCES.items()}
    views, qualification = qualify(manifest, cohorts, records)
    return manifest, cohorts, records, views, qualification


class EvaluationRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.cohorts, cls.records, cls.views, cls.qualification = context()

    def checked(self, manifest=None, cohorts=None, records=None):
        return qualify(manifest or self.manifest, cohorts or self.cohorts, records or self.records)

    def test_all_four_views_and_historical_vs_current_lineages(self):
        q = self.qualification
        self.assertEqual(q["qualified_views"], 4)
        self.assertEqual(q["distinct_shared_core_ids"], 4)
        self.assertFalse(q["source_lineages"]["obligation-v1"]["recorded_pipeline_matches_current_sources"])
        self.assertTrue(q["source_lineages"]["sequential-v1"]["recorded_pipeline_matches_current_sources"])
        self.assertFalse(q["validation_performed_lean_replay"])
        self.assertEqual(q["live_formal_certificates_issued"], 0)
        self.assertEqual(q["new_canonical_formal_admissions"], 0)

    def test_empty_missing_duplicate_or_changed_view_is_rejected(self):
        for change in (lambda m: m.update(entries=[]), lambda m: m["entries"].pop(),
                       lambda m: m["entries"].append(deepcopy(m["entries"][0])),
                       lambda m: m["entries"][0].update(task_hash="stale"),
                       lambda m: m["entries"][0].update(split="train")):
            manifest = deepcopy(self.manifest)
            change(manifest)
            with self.assertRaises(ValueError):
                self.checked(manifest=manifest)

    def test_changed_checkpoint_even_with_new_self_hash_cannot_replace_pinned_record(self):
        records = deepcopy(self.records)
        r = records["sequential-v1"]
        r["conditions"][0]["final_replay"]["axioms"] = ["sorryAx"]
        r.pop("checkpoint_digest")
        r["checkpoint_digest"] = digest(r)
        with self.assertRaisesRegex(ValueError, "registered pinned content"):
            self.checked(records=records)

    def test_condition_set_success_type_proof_and_axiom_guards(self):
        changes = [lambda r: r["conditions"].pop(),
                   lambda r: r["conditions"][0].update(passed="true"),
                   lambda r: r["conditions"][0]["final_replay"].update(kernel_checked=1),
                   lambda r: r["conditions"][0]["final_replay"].update(proof_sha256="f" * 64),
                   lambda r: r["conditions"][0]["final_replay"].update(axioms=["sorryAx"]),
                   lambda r: r.update(actual_replay_status_counts={"verified": 18})]
        for change in changes:
            records, manifest = deepcopy(self.records), deepcopy(self.manifest)
            record = records["sequential-v1"]
            change(record)
            record.pop("checkpoint_digest")
            record["checkpoint_digest"] = digest(record)
            for e in manifest["entries"]:
                if e["cohort"] == "sequential-v1":
                    e["checkpoint_digest"] = record["checkpoint_digest"]
            with self.assertRaises(ValueError):
                self.checked(manifest=manifest, records=records)

    def test_import_target_or_universe_changes_cannot_reuse_reference_evidence(self):
        for mutate in (lambda t: t["imports"].append("Mathlib.Tactic"),
                       lambda t: t["nodes"][-1].update(target="True"),
                       lambda t: t.update(universe_parameters=["v"])):
            cohorts = deepcopy(self.cohorts)
            mutate(cohorts["sequential-v1"][0][0]["task"])
            with self.assertRaises(ValueError):
                self.checked(cohorts=cohorts)

    def test_no_historical_to_current_pipeline_upgrade_without_exact_source_blobs(self):
        records, manifest = deepcopy(self.records), deepcopy(self.manifest)
        record = records["obligation-v1"]
        record["pipeline_source_hashes_lf"]["benchmarks/quantumcomputingbench/src/qcb_proof_session.py"] = "f" * 64
        record.pop("checkpoint_digest")
        record["checkpoint_digest"] = digest(record)
        for e in manifest["entries"]:
            if e["cohort"] == "obligation-v1":
                e["checkpoint_digest"] = record["checkpoint_digest"]
        with self.assertRaisesRegex(ValueError, "pinned Git revision"):
            self.checked(manifest=manifest, records=records)

    def test_export_selection_is_answer_free_and_does_not_count_strategies_as_cores(self):
        result = export_views(self.views, self.qualification, split="train", exposure="closed_book")
        self.assertEqual(result["selected_views"], 1)
        self.assertEqual(result["distinct_shared_core_ids"], 1)
        self.assertEqual(result["tasks"][0]["input"]["task"]["core_id"], "qcb-core-sp-008")
        encoded = json.dumps(result)
        for cases, _ in self.cohorts.values():
            for case in cases:
                for proof in [*case["references"].values(), *case["controls"].values()]:
                    self.assertNotIn(json.dumps(proof)[1:-1], encoded)
        self.assertEqual(result["new_mathematical_cores"], 0)
        for ids in ([], ["unknown"], [next(iter(self.views))]*2):
            with self.assertRaises(ValueError):
                export_views(self.views, self.qualification, view_ids=ids)
        with self.assertRaises(ValueError):
            export_views(self.views, self.qualification, split="dev")


if __name__ == "__main__":
    unittest.main()
