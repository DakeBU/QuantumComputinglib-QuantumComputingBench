"""Second-cohort software boundaries. Mocks are never mathematical evidence.

No test launches Lean, a model, a network request, or a candidate process.
Semantic decision objects below are deliberately synthetic routing fixtures.
"""
import asyncio
import io
import json
import secrets
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
sys.path.insert(0, str(B / "scripts"))
import lean_course as cli
import lean_course_v2 as successor

import qcb_course_expansion as expansion
import qcb_graph_course_pilot as pilot
from qcb_core import digest, read_json
from qcb_lean_course import coverage, export_course
from qcb_proof_session import bound_reply, proof_sha


def software_semantic_fixture(packet, cases):
    """Construct hash-consistent MOCK decisions, not reviewer evidence."""
    documents = {}
    for group in ("lcu", "conditioning"):
        for suffix in ("-decoder-input.json", "-decoder.json"):
            documents[group + suffix] = read_json(expansion.EVIDENCE / (group + suffix))
    comparison = {
        "schema_version": "qcb.course_semantic_comparison.v1",
        "candidate_batch_digest": digest(packet), "source_blind": False,
        "reviewer": "software-mock-no-semantic-authority", "views": [],
        "packet_digests": {}, "decoder_digests": {},
    }
    for case in cases:
        evidence = case["semantic_evidence"]
        context = documents[evidence["group"] + "-decoder-input.json"]
        formal = next(v["formal_context"] for v in context["views"] if v["anonymous_id"] == evidence["anonymous_id"])
        comparison["views"].append({"core_id": case["task"]["core_id"],
            "task_hash": digest(case["task"]), "formal_context_digest": digest(formal),
            "source_item_digest": case["source_item_digest"], "verdict": "accept",
            "reasoning": "SOFTWARE MOCK; no mathematical assessment.",
            "whole_question_coverage": {"software_mock": "No mathematical or source assessment."}})
    documents["comparison.json"] = comparison
    reseal_mock_documents(packet, documents)
    return documents


def reseal_mock_documents(packet, documents):
    comparison = documents["comparison.json"]
    comparison["candidate_batch_digest"] = digest(packet)
    for group in ("lcu", "conditioning"):
        context, decoder = documents[group + "-decoder-input.json"], documents[group + "-decoder.json"]
        decoder["packet_digest"] = digest(context)
        comparison["packet_digests"][group] = digest(context)
        comparison["decoder_digests"][group] = digest(decoder)


class CourseExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = read_json(expansion.FIXTURE)
        cls.catalog_bundle = pilot.load_catalog()
        with patch.object(pilot, "load_catalog", return_value=cls.catalog_bundle):
            cls.cases, cls.identity, cls.catalog, cls.graph = pilot.load_candidates(
                require_semantics=False, fixture=expansion.FIXTURE, evidence_dir=expansion.EVIDENCE,
                expected_cores=expansion.EXPECTED, excluded_authors=expansion.AUTHORS)
        cls.cores = {c["core_id"]: c for c in cls.catalog["cores"]}
        cls.documents = software_semantic_fixture(cls.packet, cls.cases)

    def semantic_check(self, *, packet=None, cases=None, documents=None):
        docs = self.documents if documents is None else documents
        with patch.object(pilot, "read_json", side_effect=lambda path: deepcopy(docs[Path(path).name])):
            pilot.check_semantics(self.packet if packet is None else packet,
                                  self.cases if cases is None else cases, self.cores,
                                  evidence_dir=expansion.EVIDENCE, excluded_authors=expansion.AUTHORS)

    def candidate_check(self, packet):
        original = pilot.read_json
        def reader(path):
            return deepcopy(packet) if Path(path).resolve() == expansion.FIXTURE.resolve() else original(path)
        with patch.object(pilot, "read_json", side_effect=reader), \
                patch.object(pilot, "load_catalog", return_value=self.catalog_bundle):
            return pilot.load_candidates(require_semantics=False, fixture=expansion.FIXTURE,
                evidence_dir=expansion.EVIDENCE, expected_cores=expansion.EXPECTED,
                excluded_authors=expansion.AUTHORS)

    def test_four_exact_cores_nineteen_obligations_and_complete_allowlists(self):
        self.assertEqual({c["task"]["core_id"] for c in self.cases}, expansion.EXPECTED)
        self.assertEqual(sum(len(c["references"]) for c in self.cases), 19)
        for case in self.cases:
            self.assertEqual(set(case["references"]), {n["id"] for n in case["task"]["nodes"]})
            self.assertEqual(set(case["controls"]), {"library_control", "constructed_whole_root"})
            for proof in [*case["controls"].values(), *case["negative_controls"].values()]:
                self.assertIn(proof, case["allowed_proofs"][case["task"]["root_id"]])

    def test_mock_semantic_control_is_structurally_valid(self):
        self.semantic_check()

    def test_fixed_wrapper_cannot_shrink_second_cohort(self):
        packet = deepcopy(self.packet);packet["cases"].pop()
        with self.assertRaisesRegex(ValueError, "exact sealed"):
            self.candidate_check(packet)

    def test_evaluator_paths_cannot_escape_benchmark(self):
        for keyword in ("fixture", "evidence_dir"):
            with self.subTest(keyword=keyword), self.assertRaisesRegex(ValueError, "bounded evaluator-owned"):
                pilot.load_candidates(**{keyword: B.parent.parent / "outside.json"})

    def test_task_cannot_contain_gold_fields(self):
        packet = deepcopy(self.packet);packet["cases"][0]["task"]["reference_answer"] = "by trivial"
        with self.assertRaisesRegex(ValueError, "exclude gold"):
            self.candidate_check(packet)

    def test_stale_source_binding_rejects(self):
        packet = deepcopy(self.packet);packet["cases"][0]["source_bindings"][0]["sha256_lf"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "source binding changed"):
            self.candidate_check(packet)

    def test_universe_and_target_changes_do_not_pass_existing_review(self):
        for change in (lambda c: c[0]["task"].update(universe_parameters=["changed"]),
                       lambda c: c[0]["task"]["nodes"][-1].update(target="True")):
            cases = deepcopy(self.cases);change(cases)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.semantic_check(cases=cases)

    def test_group_path_traversal_and_unknown_evidence_class_reject(self):
        for change in (lambda c: c[0]["semantic_evidence"].update(group="../lcu"),
                       lambda c: c[0]["semantic_evidence"].update(kind="unreviewed")):
            cases = deepcopy(self.cases);change(cases)
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.semantic_check(cases=cases)

    def test_duplicate_or_missing_anonymous_contexts_reject(self):
        for file in ("lcu-decoder-input.json", "lcu-decoder.json"):
            documents = deepcopy(self.documents)
            documents[file]["views"][1] = deepcopy(documents[file]["views"][0])
            reseal_mock_documents(self.packet, documents)
            with self.subTest(file=file), self.assertRaises(ValueError):
                self.semantic_check(documents=documents)

    def test_author_and_comparator_cannot_be_decoder(self):
        for identity in (*expansion.AUTHORS, self.packet["author"], self.documents["comparison.json"]["reviewer"]):
            documents = deepcopy(self.documents);documents["lcu-decoder.json"]["decoder_identity"] = identity
            reseal_mock_documents(self.packet, documents)
            with self.subTest(identity=identity), self.assertRaises(ValueError):
                self.semantic_check(documents=documents)

    def test_blind_packet_and_decoder_schema_are_enforced(self):
        for file in ("lcu-decoder-input.json", "conditioning-decoder-input.json", "lcu-decoder.json"):
            documents = deepcopy(self.documents);documents[file]["schema_version"] = "unsupported.schema.v999"
            reseal_mock_documents(self.packet, documents)
            with self.subTest(file=file), self.assertRaises(ValueError):
                self.semantic_check(documents=documents)

    def test_blind_packets_cannot_carry_proof_or_candidate_answers(self):
        for key in ("references", "candidate_proof", "expected_answer"):
            documents = deepcopy(self.documents)
            documents["lcu-decoder-input.json"][key] = "SOFTWARE-MOCK-GOLD-LEAK"
            reseal_mock_documents(self.packet, documents)
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.semantic_check(documents=documents)

    def test_source_blind_input_cannot_disclaim_its_own_blindness(self):
        documents = deepcopy(self.documents);documents["lcu-decoder-input.json"]["source_blind"] = False
        reseal_mock_documents(self.packet, documents)
        with self.assertRaises(ValueError):
            self.semantic_check(documents=documents)

    def test_reconstruction_and_source_reasoning_require_text(self):
        for which in ("reconstructed_statement", "reasoning", "whole_question_coverage"):
            documents = deepcopy(self.documents)
            if which == "reconstructed_statement":
                documents["lcu-decoder.json"]["views"][0][which] = True
            else:
                documents["comparison.json"]["views"][0][which] = True
            reseal_mock_documents(self.packet, documents)
            with self.subTest(which=which), self.assertRaises(ValueError):
                self.semantic_check(documents=documents)

    def test_zero_admission_counts_require_actual_integers(self):
        for key in ("new_mathematical_cores", "new_canonical_formal_admissions"):
            for value in (False, 0.0):
                packet = deepcopy(self.packet);packet[key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    self.candidate_check(packet)

    def test_comparison_input_digest_and_maps_cannot_drift(self):
        inputs = read_json(expansion.EVIDENCE / "comparison-input.json")
        comparison = {**deepcopy(self.documents["comparison.json"]), "comparison_input_digest": digest(inputs)}
        documents = {"comparison-input.json": inputs, "comparison.json": comparison,
                     expansion.FIXTURE.name: self.packet}
        # A valid software baseline must reach the selected loader.
        with patch.object(expansion, "read_json", side_effect=lambda p: deepcopy(documents[Path(p).name])), \
                patch.object(expansion, "load_candidates", return_value="software-mock-only") as loader:
            self.assertEqual(expansion.candidates(), "software-mock-only")
            self.assertEqual(loader.call_args.kwargs["expected_cores"], expansion.EXPECTED)
        for change in (lambda d: d["comparison.json"].update(comparison_input_digest="0" * 64),
                       lambda d: d["comparison-input.json"].update(candidate_batch_digest="0" * 64),
                       lambda d: d["comparison-input.json"]["packet_digests"].update(lcu="0" * 64)):
            mutated = deepcopy(documents);change(mutated)
            with self.subTest(change=change), \
                    patch.object(expansion, "read_json", side_effect=lambda p, docs=mutated: deepcopy(docs[Path(p).name])), \
                    patch.object(expansion, "load_candidates", side_effect=AssertionError("stale input reached loader")), \
                    self.assertRaises(ValueError):
                expansion.candidates()

    def test_thirteen_core_course_exports_preserve_old_views_and_hide_authored_proofs(self):
        # Original receipts are read as historical Git-bound records; no replay.
        previous_course = cli.load_course()
        additional = {c["view_id"]: {"task": c["task"]} for c in self.cases}
        mock_status = {"software_mock_only": True, "new_mathematical_cores": 0}
        with patch.object(successor.previous, "load_course", return_value=previous_course), \
                patch.object(successor, "qualified", return_value=(additional, mock_status, self.catalog, self.graph)):
            plan, views, catalog, graph, report = successor.load_course()
        self.assertEqual(len(views), 13)
        self.assertEqual(report["distinct_shared_cores"], 13)
        self.assertEqual(coverage(plan, views, catalog, graph)["new_mathematical_cores"], 0)
        for key, value in previous_course[1].items():
            self.assertEqual(views[key], value)
        all_proofs = {p for c in self.cases for k in ("references", "controls", "negative_controls") for p in c[k].values()}
        forbidden = {"references", "reference_answer", "controls", "negative_controls", "allowed_proofs", "source_binder_audit"}
        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(value.keys() & forbidden)
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)
        for mode in ("root_only", "proof_dag"):
            for exposure in ("closed_book", "approved_interface"):
                exported = export_course(plan, views, catalog, graph, mode=mode, exposure=exposure)
                self.assertEqual(len(exported["tasks"]), 13)
                for row in exported["tasks"]:
                    inspect(row["input"])
                    dumped = json.dumps(row["input"], ensure_ascii=False)
                    self.assertTrue(all(json.dumps(p, ensure_ascii=False)[1:-1] not in dumped for p in all_proofs))

    def test_successor_rejects_a_colliding_historical_view(self):
        key = self.cases[0]["view_id"]
        with patch.object(successor.previous, "load_course", return_value=(None, {key: {}}, None, None, {})), \
                patch.object(successor, "qualified", return_value=({key: {}}, {}, self.catalog, self.graph)), \
                self.assertRaisesRegex(ValueError, "overwrite historical"):
            successor.load_course()

    def mock_receipt(self):
        negatives = {proof_sha(c["negative_controls"]["wrong_target"]) for c in self.cases}
        sorry_controls = {proof_sha(c["negative_controls"]["sorry_axiom"]) for c in self.cases}
        class SoftwareMockOnly:
            execution_class = "trusted_local_authored_reference"
            isolated = False
            def __init__(self, task, allowlist, build_root):
                self.replays = []
            async def verify(self, request):
                negative = proof_sha(request["proof"]) in negatives | sorry_controls
                return bound_reply(request, status="compile_error" if negative else "verified",
                    execution_id=secrets.token_hex(16), kernel_checked=not negative,
                    axioms=["sorryAx"] if proof_sha(request["proof"]) in sorry_controls else [])
        raw = []
        with patch.object(cli, "AuthoredReferenceVerifier", SoftwareMockOnly), redirect_stdout(io.StringIO()):
            report = asyncio.run(cli.check_references(self.cases, self.identity, "unused-software-mock", raw,
                "f" * 40, profile=expansion.PROFILE))
        report["pipeline_source_hashes_lf"] = {p: "a" * 64 for p in expansion.PIPELINE_PATHS}
        report["receipt_digest"] = digest(report)
        return report, raw

    def test_mock_replay_profile_is_authored_only_and_raw_is_distinct(self):
        report, raw = self.mock_receipt()
        self.assertTrue(report["passed"])
        self.assertEqual(len(raw), 12)
        self.assertEqual(report["authored_reference_profile"], expansion.PROFILE)
        self.assertEqual(report["model_calls"], 0)
        self.assertFalse(report["model_performance_measured"])
        self.assertFalse(report["standalone_controls_are_completed_protocol_sessions"])
        self.assertTrue(all(r["final_replay"]["kernel_checked"] for r in report["results"]))
        self.assertEqual(sum(r["session"]["metrics"]["verifier_calls"] for r in raw), 39)
        for record in raw:
            limits = record["session"]["limits"]
            self.assertEqual(limits["check_seconds"], expansion.PROFILE["check_seconds"])
            ceiling = "session_wall_seconds" if record["condition"] == "provided_dag_repair" else "control_wall_seconds"
            self.assertEqual(limits["wall_seconds"], expansion.PROFILE[ceiling])

    def test_qualified_reader_rejects_profile_or_pipeline_shrink_before_lineage(self):
        good, _ = self.mock_receipt()
        for change in (lambda r: r["authored_reference_profile"].update(check_seconds=45),
                       lambda r: r["pipeline_source_hashes_lf"].pop(next(iter(r["pipeline_source_hashes_lf"]))),
                       lambda r: r.update(model_performance_measured=True)):
            report = deepcopy(good);change(report);report.pop("receipt_digest");report["receipt_digest"] = digest(report)
            with self.subTest(change=change), \
                    patch.object(expansion, "candidates", return_value=(self.cases, self.identity, self.catalog, self.graph)), \
                    patch.object(expansion, "read_json", return_value=report), \
                    patch.object(expansion, "_source_lineage", side_effect=AssertionError("bad metadata reached Git lineage")), \
                    self.assertRaises(ValueError):
                expansion.qualified()

    def test_existing_summary_and_raw_outputs_are_preserved_before_replay(self):
        with tempfile.TemporaryDirectory(prefix="qcb-v2-output-") as directory:
            for name in ("summary", "raw"):
                summary, raw = Path(directory) / "summary.json", Path(directory) / "raw.json"
                target = summary if name == "summary" else raw
                target.write_bytes(b"prior-immutable-receipt\n")
                args = ["lean_course_v2.py", "check-references", "--output", str(summary),
                        "--raw-output", str(raw), "--build-root", "unused", "--trusted-local-reference"]
                with patch.object(sys, "argv", args), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    self.assertEqual(cli.main(pipeline_loader=lambda: self.fail("existing output reached replay")), 1)
                self.assertEqual(target.read_bytes(), b"prior-immutable-receipt\n")
                target.unlink()

    def test_raw_alias_and_repository_raw_outputs_reject_before_replay(self):
        with tempfile.TemporaryDirectory(prefix="qcb-v2-alias-") as directory:
            output = Path(directory) / "summary.json"
            for raw in (Path(directory) / "nested/../summary.json", B / "review-raw-never-write.json"):
                args = ["lean_course_v2.py", "check-references", "--output", str(output),
                        "--raw-output", str(raw), "--build-root", "unused", "--trusted-local-reference"]
                with patch.object(sys, "argv", args), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    self.assertEqual(cli.main(pipeline_loader=lambda: self.fail("bad path reached replay")), 1)
                self.assertFalse(output.exists())

    def test_replay_failure_or_source_change_preserves_raw_without_summary(self):
        for failure in ("replay_failure", "source_changed"):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(prefix="qcb-v2-partial-") as directory:
                output, raw_output = Path(directory) / "summary.json", Path(directory) / "raw.json"
                async def replay(cases, identity, build_root, raw, tested_code, *, profile, failure_case=failure):
                    self.assertEqual(profile, expansion.PROFILE)
                    raw.append({"software_mock_only": True, "condition": "partial-evidence"})
                    if failure_case == "replay_failure":
                        raise RuntimeError("software-mock replay failure")
                    return {"passed": True, "software_mock_only": True}
                sources = {"mock": "a" * 64}
                calls = [sources, {"mock": "b" * 64}]
                args = ["lean_course_v2.py", "check-references", "--output", str(output),
                        "--raw-output", str(raw_output), "--build-root", "unused", "--trusted-local-reference"]
                with patch.object(sys, "argv", args), \
                        patch.object(cli, "_source_lineage", return_value={"recorded_pipeline_matches_current_sources": True}), \
                        patch.object(cli.subprocess, "check_output", return_value="f" * 40), \
                        patch.object(cli, "check_references", side_effect=replay), \
                        redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    code = cli.main(source_loader=lambda: (self.cases, self.identity, self.catalog, self.graph),
                                    pipeline_loader=lambda pending=calls: pending.pop(0), reference_profile=expansion.PROFILE)
                self.assertEqual(code, 1)
                self.assertFalse(output.exists())
                saved = read_json(raw_output)
                self.assertEqual(saved["records"], [{"software_mock_only": True, "condition": "partial-evidence"}])


if __name__ == "__main__":
    unittest.main()
