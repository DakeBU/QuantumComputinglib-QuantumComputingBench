"""Current-source checks for frozen c26 WIP; not source/publication acceptance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[2]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class C26Staging(unittest.TestCase):
    def test_actual_public_decoder_originals(self):
        freeze = PACKET / "decoder-c26/freeze.json"
        self.assertEqual(digest(freeze), "83b45975a001f11daef7f4cdfd1f1d316d5426de3b7a960181ff410579cd9f36")
        data = read(freeze)
        self.assertTrue(data["frozen"])
        self.assertEqual(len(data["public_artifacts"]), 15)
        for artifact in data["public_artifacts"]:
            with self.subTest(path=artifact["path"]):
                target = PACKET / "decoder-c26" / artifact["path"]
                self.assertTrue(target.is_file())
                self.assertEqual(digest(target), artifact["sha256"])
        self.assertIsNone(data["source_agreement_verdict"])
        self.assertIsNone(data["publication_verdict"])

    def test_same_source_and_honest_source_first_seal(self):
        lesson = ROOT / "docs/lessons/finite-real-tt-primitive-preparation-and-word-order.md"
        self.assertEqual(digest(lesson), "d71f16da026938debcd024d6f2fa9fa9268ade2096b5854a030d2065828b315d")
        seal = PACKET / "reviewer-c26/phase1-seal.json"
        self.assertEqual(digest(seal), "0e6c0bedcc98ae6ba2f8089bbd96e29e79b1da3b646458bc85bd093805304359")
        data = read(seal)
        self.assertEqual(digest(PACKET / "reviewer-c26/source-only-notes.md"), data["artifacts"]["notes"]["sha256"])
        self.assertTrue(data["exposure"]["prior_raw_byte_hash_IO"])
        self.assertFalse(data["exposure"]["prior_target_semantic_text_exposure"])
        self.assertFalse(data["exposure"]["absolute_file_unread_claim"])
        self.assertEqual(data["source_review"]["source_AND_edges"], 32)
        self.assertTrue(data["source_review"]["all_seven_semantic_slots_reviewed"])
        self.assertTrue(data["source_review"]["no_formal_target_matching_claim"])

    def test_actual_targets_and_all_37_real_probes(self):
        evidence = read(PACKET / "decoder-c26/evidence.json")
        signatures = read(PACKET / "decoder-c26/signatures.json")
        inventory = read(ROOT / "web/library/declarations.json")["declarations"]
        expected_counts = [10, 12, 15]
        observed = []
        for target, group, count, output in zip(evidence["modules"], signatures["modules"], expected_counts,
                                              ("probe-local-output.txt", "probe-word-output.txt", "probe-preparation-output.txt")):
            self.assertEqual(target["path"], group["path"])
            self.assertEqual(digest(ROOT / target["path"]), target["source_sha256"])
            self.assertEqual((target["compile_exit_code"], target["probe_exit_code"]), (0, 0))
            roots = group["roots"]
            self.assertEqual(len(roots), count)
            names = [x["fullName"] for x in inventory if x["source"] == target["path"]]
            self.assertEqual([x["name"] for x in roots], names)
            raw = (PACKET / "decoder-c26" / output).read_text(encoding="utf-8")
            for item in roots:
                self.assertIn(item["elaborated_type_display"], raw)
                self.assertIn(item["ordinary_axiom_output"], raw)
                self.assertNotIn("sorryAx", item["ordinary_axioms"])
                self.assertTrue(set(item["ordinary_axioms"]) <= {"propext", "Classical.choice", "Quot.sound"})
                observed.append(item["name"])
        self.assertEqual(len(set(observed)), 37)
        self.assertEqual(signatures["count"], 37)
        self.assertTrue(evidence["compiler"]["setup_overrides"]["source_Preparation_imports_fresh_LocalCompiler"])
        self.assertTrue(evidence["compiler"]["no_transitive_dependency_rebuild"])

    def test_failures_warnings_and_compiler_boundary_not_erased(self):
        evidence = read(PACKET / "decoder-c26/evidence.json")
        freeze = read(PACKET / "decoder-c26/freeze.json")
        self.assertEqual(freeze["checks"]["final_six_exit_codes"], [0] * 6)
        self.assertEqual(freeze["checks"]["preserved_failed_calls"], 3)
        self.assertEqual(freeze["checks"]["all_proof_process_calls_including_failures"], 9)
        calls = evidence["compiler"]["call_results"]
        self.assertEqual(sum(x["exit_code"] != 0 for x in calls), 3)
        self.assertEqual(sum(x["successful_intended_run"] for x in calls), 6)
        warnings = evidence["compiler"]["source_compile_warnings"]
        self.assertEqual([warnings[x]["count"] for x in ("TensorTrainLocalCompiler", "TensorTrainWord", "TensorTrainPrimitivePreparation")], [2, 1, 0])
        for item in freeze["private_artifact_hashes"]:
            self.assertFalse((PACKET / "decoder-c26" / item["path"]).exists())

    def test_current_previous_canonical_records_still_validate(self):
        spec = importlib.util.spec_from_file_location("c26_current_publication", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        inventory = {x["fullName"]: x for x in read(ROOT / "web/library/declarations.json")["declarations"]}
        records = read(ROOT / "website/research/publications.json")["records"]
        for record in records:
            checker.validate_record(ROOT, record, inventory)

    def test_missing_actual_artifact_is_not_green(self):
        original = Path.is_file
        absent = PACKET / "decoder-c26/probe-word-output.txt"
        with patch.object(Path, "is_file", lambda p: False if p == absent else original(p)):
            result = unittest.TestResult()
            C26Staging("test_actual_public_decoder_originals").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_frozen_author_inputs_lossless_source_and_bounded_graph(self):
        manifest = PACKET / "outputs-manifest.json"
        self.assertEqual(digest(manifest), "d37d184b5990b95db1cddbc1b19bbed0f6da6da68ba67aa9de03264741f3557f")
        for item in read(manifest)["artifacts"]:
            target = ROOT / item["planned_canonical_path"]
            self.assertEqual(digest(target), item["sha256"])
            self.assertEqual(target.stat().st_size, item["bytes"])
        coverage = read(PACKET / "author-source-coverage.json")
        source = ROOT / coverage["source_path"]
        self.assertEqual(len(coverage["source_paragraphs"]), 74)
        self.assertEqual("".join(p["exact_text"] for p in coverage["source_paragraphs"]).encode(), source.read_bytes())
        self.assertEqual(len(coverage["whole_module_inventory"]), 37)
        self.assertEqual(coverage["additional_top_level_named_instances"], 0)
        self.assertEqual(coverage["private_target_helpers"], 0)
        graph = read(PACKET / "author-graph-views.json")
        self.assertEqual(graph["coverage_sha256"], digest(PACKET / "author-source-coverage.json"))
        sg = graph["views"]["source-construction-graph"]
        nodes = {n["id"]: n for n in sg["nodes"]}
        self.assertEqual(len(sg["hyperedges"]), 32)
        for edge in sg["hyperedges"]:
            self.assertEqual(edge["logic"], "AND")
            self.assertTrue(set(edge["tails"] + edge["heads"]) <= nodes.keys())
        gaps = {key for key, node in nodes.items() if node["kind"] == "SOURCE_GAP"}
        self.assertEqual(gaps, set(coverage["open_source_gap_ids"]))
        self.assertEqual(len(gaps), 6)
        self.assertTrue(all(nodes[g]["status"] == "OPEN" and not nodes[g]["mathematical_proof_node"] for g in gaps))
        self.assertEqual(len(graph["views"]["lean-graph"]["target_import_edges"]), 10)
        self.assertEqual(len(graph["views"]["lean-graph"]["ownership_edges"]), 37)
        self.assertFalse(graph["views"]["functor-hypergraph"]["certified_transport"])
        context = read(PACKET / "author-formal-context.json")
        for target in context["target_files"]:
            self.assertEqual("".join(target["full_source_lines"]).encode(), (ROOT / target["path"]).read_bytes())
            self.assertEqual(digest(ROOT / target["path"]), target["sha256"])
        self.assertEqual(len(context["provider_index"]), 41)
        for provider in context["provider_index"]:
            self.assertEqual(digest(ROOT / provider["path"]), provider["sha256"])

    def test_original_author_script_in_reconstructed_assembly_layout(self):
        # Replay the declared original assembly layout without editing frozen
        # script/source bytes or pretending it is the public directory layout.
        with tempfile.TemporaryDirectory(prefix="c26-author-replay-") as folder:
            assembly = Path(folder)
            for item in read(PACKET / "outputs-manifest.json")["artifacts"]:
                (assembly / item["path"]).write_bytes((ROOT / item["planned_canonical_path"]).read_bytes())
            result = subprocess.run([sys.executable, "-B", str(assembly / "author-publication-selftest.py"),
                                     "--root", str(ROOT), "--packet", str(assembly)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["status"], "MECHANICAL_AUTHOR_INTEGRITY_PASS_NOT_ADMISSION")
            self.assertEqual(data["inventory"], 37)
            self.assertEqual(len(data["public_binding_digest_replayed"]), 3)
            self.assertFalse(data["validate_record_called"])

    def test_direct_original_native_decoder_evidence(self):
        freeze = PACKET / "decoder-c26/native-evidence-freeze.json"
        self.assertEqual(digest(freeze), "897e30b67c10c9ae195458dc2269c319d2d65b9050a313c4c2ce7db8f3ec438e")
        data = read(freeze)
        for item in data["native_artifacts"] + data["prior_frozen_artifact_bindings"]:
            self.assertEqual(digest(PACKET / "decoder-c26" / item["path"]), item["sha256"])
        for item in data["author_formal_metadata"]:
            self.assertEqual(digest(PACKET / item["path"]), item["sha256"])
        bindings = {r["module"]: r["binding_sha256"] for r in data["publication_bindings"]}
        for item in data["native_artifacts"]:
            evidence = read(PACKET / "decoder-c26" / item["path"])
            self.assertEqual(evidence["role"], "decoder")
            self.assertTrue(evidence["source_blind"])
            self.assertEqual(evidence["binding_sha256"], bindings[evidence["target_module"]])
            self.assertEqual(digest(ROOT / evidence["packet_path"]), evidence["packet_sha256"])
            self.assertEqual(digest(ROOT / evidence["artifact_path"]), evidence["artifact_sha256"])
            self.assertEqual(evidence["new_lean_invocations"], 0)
            self.assertIsNone(evidence["source_agreement_verdict"])


    def test_new_source_first_companion_keeps_private_original_private(self):
        companion = PACKET / "reviewer-c26r/phase1-public-transport-seal.json"
        self.assertEqual(digest(companion), "42f8748552b6ea71816230f8974b0e2a4ce32563a7f5bab64dfea8f8e1c2bae9")
        seal = read(companion)
        self.assertEqual(seal["run_id"], "tt-physical-source-review-c26r")
        self.assertFalse(seal["chronology"]["new_mathematical_review_performed"])
        self.assertTrue(seal["chronology"]["companion_created_before_formal_delivery_to_this_reviewer"])
        self.assertFalse(seal["chronology"]["formal_provider_or_decoder_read_before_companion"])
        self.assertEqual(seal["original_private_seal"]["sha256"], "6db4b6dae8374c33e804a01bdb02195f75011bdf806c21c30c32ad44b5646a22")
        self.assertTrue(seal["original_private_seal"]["original_unmodified"])
        self.assertFalse((PACKET / "reviewer-c26r/phase1-seal.json").exists())
        self.assertEqual(digest(PACKET / "reviewer-c26r/source-only-notes.md"), seal["source_only_notes"]["sha256"])
        self.assertEqual(digest(ROOT / "docs/lessons/finite-real-tt-primitive-preparation-and-word-order.md"), seal["source"]["sha256"])

    def test_actual_new_static_inputs_and_unmodified_prospective_bindings(self):
        path = PACKET / "static-review-inputs-c26r.json"
        self.assertEqual(digest(path), "bf51e531930af580a2fc1dbc685fadbca51087e3208df0e1ccfd461588e361b0")
        packet = read(path)
        self.assertEqual(len(packet["input_sha256"]), 26)
        for name, expected in packet["input_sha256"].items():
            self.assertNotIn("/decoder-c26/", name)
            self.assertNotIn("/reviewer-c26/", name)
            self.assertEqual(digest(ROOT / name), expected)
        self.assertTrue(packet["old_run_not_resumed_or_impersonated"])
        self.assertFalse(packet["canonical_main_reader_purified_or_scientific_ROOT"])
        keys = ("module", "source_id", "source_statement", "source_anchor", "lesson_path",
                "declarations", "obligation_map", "assumption_deltas", "graph_contribution",
                "formalizer", "residual_boundary", "binding_sha256")
        for name in packet["candidate_paths"]:
            proposed = read(ROOT / name)
            slug = Path(name).name.removeprefix("parent-proposal-").removesuffix("-c26r.json")
            original = read(PACKET / ("publication-candidate-" + slug + ".json"))
            self.assertEqual({k: proposed[k] for k in keys}, {k: original[k] for k in keys})
            self.assertEqual(proposed["status"], "PARENT_PROPOSAL_WIP_NOT_ADMITTED")
            self.assertIn("/reviewer-c26r/", proposed["reviewer_evidence"])


    def test_joint_static_seal_precedes_actual_final_decoder_delivery(self):
        seal_path = PACKET / "reviewer-c26r/phase2-static-seal.json"
        self.assertEqual(digest(seal_path), "fc8c22e47585c41450bf978a3515b5c98dcab15c655d56971adb3c773160b107")
        seal = read(seal_path)
        self.assertTrue(seal["chronology"]["decoder_and_compile_delivery_not_yet_read"])
        self.assertEqual(seal["comparison_report"]["sha256"], digest(PACKET / "reviewer-c26r/phase2-static-comparison.md"))
        self.assertEqual(seal["static_input_packet"]["sha256"], digest(PACKET / "static-review-inputs-c26r.json"))
        final = PACKET / "final-review-inputs-c26r.json"
        self.assertEqual(digest(final), "2548f8727f1dbdad173bfe4550c28c8bf23f6d5b0f1ceb8af5cbc1c7c19e2107")
        data = read(final)
        self.assertEqual(data["role"], "PARENT_DELIVERY_NOT_A_REVIEW_OR_ACCEPTANCE")
        self.assertEqual(len(data["input_sha256"]), 53)
        for name, expected in data["input_sha256"].items():
            self.assertEqual(digest(ROOT / name), expected)
        self.assertEqual(len(data["native_decoder"]), 3)
        self.assertFalse(seal["acceptance_boundary"]["accepted_publication_review"])


    def test_actual_final_distinct_reviewer_and_three_canonical_records(self):
        path = PACKET / "reviewer-c26r/final-review-seal.json"
        self.assertEqual(digest(path), "137138132a8066ee688422acec86eac8add16432a5b29541217ee1f89cf82013")
        seal = read(path)
        self.assertEqual(seal["verdict"], "accepted")
        self.assertTrue(seal["chronology"]["joint_static_frozen_before_decoder_compile_delivery"])
        self.assertFalse(seal["chronology"]["historical_worker_impersonated_or_old_final_seal_fabricated"])
        for item in seal["final_outputs"]:
            self.assertEqual(digest(ROOT / item["path"]), item["sha256"])
        records = {r["module"]: r for r in read(ROOT / "website/research/publications.json")["records"]}
        for slug in ("local-compiler", "word", "primitive-preparation"):
            reviewer = read(PACKET / ("reviewer-c26r/" + slug + "-evidence.json"))
            proposal = read(PACKET / ("parent-proposal-" + slug + "-c26r.json"))
            self.assertEqual(reviewer["identity"], "tt-physical-source-review-c26r")
            self.assertEqual(reviewer["role"], "reviewer")
            self.assertEqual(reviewer["binding_sha256"], proposal["binding_sha256"])
            self.assertEqual(reviewer["decoder_evidence_sha256"], digest(ROOT / proposal["decoder_evidence"]))
            self.assertEqual(reviewer["packet_sha256"], digest(ROOT / reviewer["packet_path"]))
            self.assertEqual(reviewer["artifact_sha256"], digest(ROOT / reviewer["artifact_path"]))
            self.assertTrue(reviewer["anti_anchored"])
            self.assertEqual(set(reviewer["semantic_slots"]), {"target", "normalization", "registers", "oracles", "ancillas_phases", "error_success", "resources"})
            self.assertTrue(all(reviewer["semantic_slots"].values()))
            current = records[proposal["module"]]
            self.assertEqual(current["reviewer_evidence"], proposal["reviewer_evidence"])
            self.assertEqual(current["status"], "SOURCE_REVIEWED_LOCAL_INTEGRATION_PENDING")
            self.assertFalse(current["main_admission"])
            self.assertFalse(current["scientific_ROOT"])

    def test_missing_actual_new_reviewer_evidence_is_rejected(self):
        spec = importlib.util.spec_from_file_location("c26_missing_reviewer", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        inventory = {x["fullName"]: x for x in read(ROOT / "web/library/declarations.json")["declarations"]}
        record = next(r for r in read(ROOT / "website/research/publications.json")["records"]
                      if r["module"] == "QuantumBlockEncoding/TensorTrainWord.lean")
        original = Path.is_file
        absent = ROOT / record["reviewer_evidence"]
        with patch.object(Path, "is_file", lambda path: False if path == absent else original(path)):
            with self.assertRaises(ValueError):
                checker.validate_record(ROOT, record, inventory)


if __name__ == "__main__":
    unittest.main()
