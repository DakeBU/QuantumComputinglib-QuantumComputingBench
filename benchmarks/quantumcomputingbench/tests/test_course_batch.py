"""Source-aware payload binding, including correctly rehashed substitutions.

These are metadata checks, not source-review independence or new Lean evidence.
"""
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
import qcb_course_batch as batch
from qcb_core import digest, read_json
from qcb_course_expansion import EVIDENCE, EXPECTED, FIXTURE
from qcb_graph_course_pilot import load_candidates


class CourseBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases, _, _, _ = load_candidates(require_semantics=False, fixture=FIXTURE,
                                              evidence_dir=EVIDENCE, expected_cores=EXPECTED)
        cls.documents = {p.name: read_json(p) for p in EVIDENCE.glob("*-decoder*.json")}
        cls.documents.update({name: read_json(EVIDENCE / name) for name in ("comparison.json", "comparison-input.json")})
        cls.documents[FIXTURE.name] = read_json(FIXTURE)
        cls.canonical = {r["core_id"]: r["source_item"] for r in cls.documents["comparison-input.json"]["views"]}

    def check(self, docs, cases=None):
        with patch.object(batch, "read_json", side_effect=lambda p: deepcopy(docs[Path(p).name])):
            batch.bind_review_input(FIXTURE, EVIDENCE, self.cases if cases is None else cases)

    def rehash(self, docs):
        docs["comparison.json"]["comparison_input_digest"] = digest(docs["comparison-input.json"])

    def sanitized_documents(self):
        docs = deepcopy(self.documents)
        docs["comparison-input.json"]["schema_version"] = "qcb.course_semantic_comparison_input.v2"
        cases = {c["task"]["core_id"]: c for c in self.cases}
        for row in docs["comparison-input.json"]["views"]:
            row["source_semantics"] = batch.source_semantics(row.pop("source_item"))
            row["retrieval_interfaces"] = cases[row["core_id"]]["task"]["interfaces"]
        self.rehash(docs)
        return docs

    def sanitized_check(self, docs):
        with patch.object(batch, "read_json", side_effect=lambda p: deepcopy(docs[Path(p).name])), \
                patch.object(batch, "_canonical_items", return_value=self.canonical):
            batch.bind_review_input(FIXTURE, EVIDENCE, self.cases, require_sanitized=True)

    def test_actual_preceding_review_payloads_match_their_labelled_source_and_decoder(self):
        self.check(self.documents)

    def test_sanitized_projection_is_lossless_for_source_mathematics(self):
        docs = self.sanitized_documents()
        self.sanitized_check(docs)
        for row in docs["comparison-input.json"]["views"]:
            self.assertEqual(set(row["source_semantics"]), set(batch.SOURCE_FIELDS))
            self.assertNotIn("reviews", row["source_semantics"])

    def test_sanitized_mode_rejects_historical_full_item_shape(self):
        with self.assertRaises(ValueError):
            self.sanitized_check(self.documents)

    def test_rehashed_prior_reviews_cannot_be_smuggled_back(self):
        for change in (
            lambda d: d["comparison-input.json"].update(reviews=[{"verdict": "SOFTWARE-MOCK-ACCEPT"}]),
            lambda d: d["comparison-input.json"]["views"][0].update(reviews=[{"verdict": "SOFTWARE-MOCK-ACCEPT"}]),
            lambda d: d["comparison-input.json"]["views"][0]["source_semantics"].update(reviews=[]),
        ):
            docs = self.sanitized_documents(); change(docs); self.rehash(docs)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.sanitized_check(docs)

    def test_sanitized_source_and_retrieval_bodies_are_bound_beyond_labels(self):
        for change in (
            lambda r: r["source_semantics"].update(question="SOFTWARE-MOCK-DIFFERENT-QUESTION"),
            lambda r: r.update(retrieval_interfaces=[{"name": "Unreviewed.declaration"}]),
        ):
            docs = self.sanitized_documents(); change(docs["comparison-input.json"]["views"][0]); self.rehash(docs)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.sanitized_check(docs)

    def test_rehashed_source_question_or_answer_substitution_is_not_alignment(self):
        for field in ("question", "reference_answer", "assumptions", "conventions"):
            docs = deepcopy(self.documents)
            row = docs["comparison-input.json"]["views"][0]
            row["source_item"][field] = "SOFTWARE-MOCK-SUBSTITUTION"
            self.rehash(docs)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "substituted"):
                self.check(docs)

    def test_rehashed_formal_or_decoder_substitutions_are_rejected(self):
        for change in (
            lambda r: r["formal_view"]["formal_context"].update(target="True"),
            lambda r: r["ambient_context"].update(ambient_definitions=[]),
            lambda r: r["source_blind_decode"].update(reconstructed_statement="SOFTWARE MOCK DIFFERENT RECONSTRUCTION"),
            lambda r: r.update(task_hash="0"*64),
            lambda r: r.update(formal_context_digest="0"*64),
            lambda r: r.update(source_item_digest="0"*64),
        ):
            docs = deepcopy(self.documents)
            change(docs["comparison-input.json"]["views"][0])
            self.rehash(docs)
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "substituted"):
                self.check(docs)

    def test_exact_review_coverage_cannot_be_shrunk_or_duplicated(self):
        for duplicate in (False, True):
            docs = deepcopy(self.documents)
            if duplicate:
                docs["comparison-input.json"]["views"][1] = deepcopy(docs["comparison-input.json"]["views"][0])
            else:
                docs["comparison-input.json"]["views"].pop()
            self.rehash(docs)
            with self.subTest(duplicate=duplicate), self.assertRaisesRegex(ValueError, "exact cohort"):
                self.check(docs)

    def test_malformed_payload_fails_with_typed_gate_error(self):
        for payload in (None, ["not a view"], [{"core_id": c["task"]["core_id"]} for c in self.cases]):
            docs = deepcopy(self.documents); docs["comparison-input.json"]["views"] = payload
            self.rehash(docs)
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                self.check(docs)


if __name__ == "__main__":
    unittest.main()
