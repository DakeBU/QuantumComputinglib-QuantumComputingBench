"""Fourth-cohort contracts, source bindings and answer-free curriculum exports.

Mock role records test routing only; actual review and compiler evidence are
required separately by the production audit.
"""
import ast
import json
import sys
import unittest
from contextlib import ExitStack
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
sys.path[:0] = [str(B / "src"), str(B / "scripts")]
import lean_course_v3 as previous
import lean_course_v4 as driver
import qcb_course_batch as batch
import qcb_course_fourth as fourth
import qcb_graph_course_pilot as pilot
from qcb_core import digest, read_json
from qcb_lean_course import coverage, export_course
from test_course_third import mock_documents, reseal_mock


class FourthCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = read_json(fourth.FIXTURE)
        cls.bundle = pilot.load_catalog()
        cls.cases, cls.identity, cls.catalog, cls.graph = pilot.load_candidates(
            require_semantics=False, fixture=fourth.FIXTURE, expected_cores=fourth.EXPECTED)

    def checked(self, packet=None, mutate=None):
        packet = deepcopy(self.packet if packet is None else packet)
        docs = mock_documents(packet, packet["cases"], self.bundle[1],
                              evidence_dir=fourth.EVIDENCE, fixture=fourth.FIXTURE)
        if mutate:
            mutate(docs)
            reseal_mock(packet, docs)
        reader = lambda path: deepcopy(docs[Path(path).name])
        with ExitStack() as stack:
            for module in (pilot, batch):
                stack.enter_context(patch.object(module, "read_json", side_effect=reader))
            stack.enter_context(patch.object(pilot, "load_catalog", return_value=self.bundle))
            stack.enter_context(patch.object(batch, "_canonical_items", return_value=self.bundle[1]))
            return fourth.candidates()

    def test_fixed_three_core_batch_and_current_shared_contracts(self):
        cases, identity, _, _ = self.checked()
        self.assertEqual({c["task"]["core_id"] for c in cases}, fourth.EXPECTED)
        self.assertEqual(identity["fixture_digest"], digest(self.packet))
        for case in cases:
            t = case["task"]
            item = self.bundle[1][t["core_id"]]
            for field in ("question", "assumptions", "conventions"):
                self.assertEqual(t[field], item[field])
            self.assertEqual(set(case["references"]), {n["id"] for n in t["nodes"]})

    def test_rehashed_source_formal_and_retrieval_substitutions_still_fail(self):
        attacks = (
            lambda d: d["comparison-input.json"]["views"][0]["source_semantics"].update(question="Replacement"),
            lambda d: d["comparison-input.json"]["views"][0]["formal_view"]["formal_context"].update(target="False"),
            lambda d: d["comparison-input.json"]["views"][0].update(retrieval_interfaces=[]),
            lambda d: d["comparison-input.json"].update(schema_version="qcb.course_semantic_comparison_input.v1"),
        )
        for i, attack in enumerate(attacks):
            with self.subTest(attack=i), self.assertRaises(ValueError):
                self.checked(mutate=attack)

    def test_old_contract_split_or_added_assumptions_do_not_qualify(self):
        for field, value in (("contract_hash", "stale"), ("split", "test_public"), ("assumptions", ["Convenient new premise"])):
            packet = deepcopy(self.packet)
            packet["cases"][0]["task"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.checked(packet)

    def test_cumulative_plan_retains_all_18_predecessor_entries(self):
        prior = previous.load_course()
        before = digest(prior)
        extra = {c["view_id"]: {"task": c["task"]} for c in self.cases}
        with patch.object(driver.previous, "load_course", return_value=prior), \
                patch.object(driver, "qualified", return_value=(extra, {"software_mock_only": True}, self.catalog, self.graph)):
            plan, views, catalog, graph, report = driver.load_course()
        self.assertEqual(digest(prior), before)
        self.assertEqual(plan["entries"][:18], prior[0]["entries"])
        self.assertEqual(len(views), 21)
        self.assertEqual(report["distinct_shared_cores"], 21)
        self.assertEqual(coverage(plan, views, catalog, graph)["new_mathematical_cores"], 0)
        proofs = {c["view_id"]: {p for k in ("references", "controls", "negative_controls") for p in c[k].values()}
                  for c in self.cases}
        forbidden = {"references", "controls", "negative_controls", "allowed_proofs", "reference_answer", "source_binder_audit"}
        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(value.keys() & forbidden)
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)
        for split in (None, "train", "dev", "test_public"):
            for band in (None, "D1", "D2", "D3", "D4"):
                if not any((split is None or e["split"] == split) and
                           (band is None or e["difficulty"]["construction_band"] == band) for e in plan["entries"]):
                    continue
                exported = export_course(plan, views, catalog, graph, split=split, band=band)
                inspect(exported)
                for row in exported["tasks"]:
                    # An unrelated old target contains `(by decide)` solely as
                    # a Fin literal's positivity proof. Compare each new view
                    # to its own authored bodies, with matching JSON escaping.
                    text = json.dumps(row["input"], ensure_ascii=False)
                    self.assertTrue(all(json.dumps(proof, ensure_ascii=False)[1:-1] not in text
                                        for proof in proofs.get(row["view_id"], ())))
                self.assertFalse(exported["reference_answers_projected"])

    def test_deferred_source_history_and_decoder_projections_remain_lossless(self):
        fourth.check_decoder_projection("analytic")
        fourth.check_decoder_projection("oracle")
        fourth.check_review_projection()
        real_read = fourth.read_json
        for name, field in (("analytic-decoder.json", "views"), ("oracle-decoder.json", "views"), ("comparison.json", "views")):
            def altered(path):
                value = deepcopy(real_read(path))
                if Path(path).name == name:
                    value[field][0]["reconstructed_statement" if "decoder" in name else "reasoning"] = "Substituted content."
                return value
            with self.subTest(name=name), patch.object(fourth, "read_json", side_effect=altered), self.assertRaises(ValueError):
                if name == "comparison.json":
                    fourth.check_review_projection()
                else:
                    fourth.check_decoder_projection(name.split("-")[0])

    def test_reference_pipeline_covers_every_static_local_import(self):
        files = [*(B / "src").glob("*.py"), *(B / "scripts").glob("*.py"), R / "website/scripts/proof_inputs.py"]
        modules = {p.stem: p for p in files}
        seen, todo = set(), ["lean_course_v4"]
        while todo:
            name = todo.pop()
            if name in seen:
                continue
            seen.add(name)
            for node in ast.walk(ast.parse(modules[name].read_text(encoding="utf-8-sig"))):
                imports = ([a.name for a in node.names] if isinstance(node, ast.Import) else
                           [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
                todo.extend(n.split(".")[0] for n in imports if n.split(".")[0] in modules)
        self.assertEqual({modules[n].relative_to(R).as_posix() for n in seen},
                         {p for p in fourth.PIPELINE_PATHS if p.endswith(".py")})


if __name__ == "__main__":
    unittest.main()
