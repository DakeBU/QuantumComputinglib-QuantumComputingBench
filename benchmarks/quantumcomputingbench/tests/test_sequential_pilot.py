"""New companion roots retain canonical contracts and separate evidence gates."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import read_json
from qcb_proof_session import UNIVERSE_TASK_SCHEMA
from qcb_sequential_pilot import (
    EVIDENCE,
    FIXTURE,
    export_sequential,
    load_sequential_pilot,
)


class SequentialPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases, cls.identity = load_sequential_pilot()

    def test_current_two_cores_six_obligations_and_explicit_universe(self):
        self.assertEqual({c["task"]["core_id"] for c in self.cases}, {"qcb-core-sp-007", "qcb-core-sp-008"})
        self.assertEqual(sum(len(c["task"]["nodes"]) for c in self.cases), 6)
        for case in self.cases:
            self.assertEqual(case["task"]["schema_version"], UNIVERSE_TASK_SCHEMA)
            self.assertEqual(case["task"]["universe_parameters"], ["u"])
            self.assertIn("partial", case["semantic_coverage"])
            self.assertEqual(set(case["references"]), {n["id"] for n in case["task"]["nodes"]})
            self.assertNotIn("QuantumComputingBench.SequentialMath.", " ".join(case["references"].values()))

    def test_root_boundaries_and_real_probability_are_retained(self):
        transfer, probability = self.cases
        a = next(n["target"] for n in transfer["task"]["nodes"] if n["id"] == transfer["task"]["root_id"])
        b = next(n["target"] for n in probability["task"]["nodes"] if n["id"] == probability["task"]["root_id"])
        self.assertIn("boundary : B → ℂ", a)
        self.assertNotIn("unitaryGroup", a)
        self.assertIn("(0, a)", a)
        self.assertIn("Complex.normSq", b)
        self.assertIn("PrimitiveBasis n × B", b)
        self.assertTrue(transfer["library_control_one_call"])
        self.assertFalse(probability["library_control_one_call"])

    def test_export_hides_proofs_controls_reviews_and_rubrics(self):
        result = export_sequential(self.cases, self.identity)
        encoded = json.dumps(result)
        for case in self.cases:
            for proof in [*case["references"].values(), *case["controls"].values(), case["wrong_reference"]["proof"]]:
                self.assertNotIn(json.dumps(proof)[1:-1], encoded)
        for entry in result["tasks"]:
            self.assertNotIn("interfaces", entry["task"])
            self.assertNotIn("preamble", entry["task"])
        self.assertFalse(result["blind_test"])
        self.assertFalse(result["model_performance_measured"])
        self.assertEqual(result["new_canonical_formal_admissions"], 0)

    def test_stale_decoder_target_split_or_empty_cohort_fails_closed(self):
        fixture = read_json(FIXTURE)
        decoder = read_json(EVIDENCE / "decoder.json")
        changes = [("decoder.json", lambda d: d.update(packet_digest="stale")),
                   (FIXTURE.name, lambda d: d["cases"][0]["binding"].update(split="train")),
                   (FIXTURE.name, lambda d: d["cases"][0]["formal_context"].update(target="True")),
                   (FIXTURE.name, lambda d: d.update(cases=[]))]
        for filename, change in changes:
            value = deepcopy(decoder if filename == "decoder.json" else fixture)
            change(value)

            def read(path, selected=filename, replacement=value):
                return deepcopy(replacement) if Path(path).name == selected else read_json(path)

            with patch("qcb_sequential_pilot.read_json", side_effect=read), self.assertRaises(ValueError):
                load_sequential_pilot()

    def test_public_review_has_only_relative_locators_and_keeps_display_caveat(self):
        review = read_json(EVIDENCE / "comparison.json")
        text = json.dumps(review)
        self.assertNotIn("C:\\\\Users", text)
        self.assertTrue(all("read_absolute_path" not in row for row in review["source_checks"]))
        self.assertTrue(review["public_projection"]["changed_fields"])
        self.assertIn("universe_v_caveat", review["display_context_fidelity"])
        self.assertFalse(review["display_context_fidelity"]["byte_literal_extraction"])
        self.assertTrue(all(v["verdict"] == "accept" for v in review["views"]))


if __name__ == "__main__":
    unittest.main()
