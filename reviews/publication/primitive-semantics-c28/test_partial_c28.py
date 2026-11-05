"""Assert genuine partial evidence, never turn OOM or missing files green."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[2]
DECODER = PACKET / "decoder-c28"
RESUME = PACKET / "decoder-c28-resume1"
RESUME2 = PACKET / "decoder-c28-resume2"
read = lambda p: json.loads(p.read_text(encoding="utf-8"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def signature_header(name):
    return re.compile(r"^" + re.escape(name) + r"(?:\.\{[^}\n]*\})?(?:\s|\()", re.M)


class PartialC28(unittest.TestCase):
    def test_actual_final_reviewer_records_and_boundaries(self):
        folder = PACKET / "reviewer-c28"
        self.assertEqual(sha(folder / "final-review-seal.json"), "5ab948c98136fe72afae8bc8a7a3ad5dbdbc45478e1d013faaa9ede456990ee2")
        seal = read(folder / "final-review-seal.json")
        self.assertEqual(seal["verdict"], "accepted")
        self.assertEqual(sha(folder / "final-review.md"), seal["authored_final_artifacts"]["final-review.md"]["sha256"])
        self.assertTrue(seal["review_completeness"]["C28_020_OfNat_zero_API_restriction_preserved"])
        self.assertFalse(seal["main_admission"])
        self.assertFalse(seal["scientific_ROOT"])
        self.assertFalse(seal["PURIFIED"])
        for short in ("ConcreteSemantics", "PrimitiveSemantics", "ReversibleClassical"):
            name = short + "-evidence.json"
            path = folder / name
            self.assertEqual(sha(path), seal["authored_final_artifacts"][name]["sha256"])
            evidence = read(path)
            self.assertEqual(evidence["role"], "reviewer")
            self.assertEqual(evidence["identity"], seal["identity"])
            self.assertEqual(evidence["run_id"], seal["run_id"])
            self.assertEqual(evidence["verdict"], "accepted")
            self.assertTrue(evidence["anti_anchored"])
            self.assertEqual(evidence["decoder_evidence_sha256"], sha(DECODER / name))
            self.assertEqual(set(evidence["semantic_slots"]), {"target", "normalization", "registers", "oracles", "ancillas_phases", "error_success", "resources"})

    def test_actual_canonical_cohort_and_previous_records_validate(self):
        spec = importlib.util.spec_from_file_location("c28_actual", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        records = read(ROOT / "website/research/publications.json")["records"]
        inventory = {r["fullName"]: r for r in read(ROOT / "web/library/declarations.json")["declarations"]}
        wanted = {"QuantumBlockEncoding/" + s + ".lean" for s in ("ConcreteSemantics", "PrimitiveSemantics", "ReversibleClassical")}
        self.assertEqual({r["module"] for r in records if r["module"] in wanted}, wanted)
        for record in records:
            checker.validate_record(ROOT, record, inventory)

    def test_missing_actual_native_reviewer_is_rejected(self):
        spec = importlib.util.spec_from_file_location("c28_missing", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        record = next(r for r in read(ROOT / "website/research/publications.json")["records"] if r["module"] == "QuantumBlockEncoding/PrimitiveSemantics.lean")
        inventory = {r["fullName"]: r for r in read(ROOT / "web/library/declarations.json")["declarations"]}
        absent = ROOT / record["reviewer_evidence"]
        original = Path.is_file
        with patch.object(Path, "is_file", lambda path: False if path == absent else original(path)):
            with self.assertRaises(ValueError):
                checker.validate_record(ROOT, record, inventory)

    def test_final_delivery_has_real_role_outputs_and_exact_aliases(self):
        path = PACKET / "final-review-inputs-c28.json"
        self.assertEqual(sha(path), "3944ca94096538eb31bf36404462464d4c6111fe72cee0b357ee7f50edff56ac")
        packet = read(path)
        self.assertEqual(len(packet["input_sha256"]), 82)
        self.assertFalse(packet["main_reader_purification_scientific_ROOT"])
        for name, expected in packet["input_sha256"].items():
            actual = ROOT / name
            self.assertTrue(actual.is_file(), name)
            self.assertEqual(sha(actual), expected)
        static = read(PACKET / "reviewer-c28/phase2-static-seal.json")
        self.assertFalse(static["implementation_accepted"])
        self.assertFalse(static["accepted_native_implementation_record_emitted"])
        self.assertEqual(sha(PACKET / "reviewer-c28/phase2-static-comparison.md"), static["report"]["sha256"])
        self.assertIn("OfNat", static["visible_api_restriction"])
        self.assertEqual(len(packet["exact_byte_log_aliases"]), 3)
        for alias in packet["exact_byte_log_aliases"]:
            self.assertEqual((ROOT / alias["original"]).read_bytes(), (ROOT / alias["alias"]).read_bytes())
            self.assertEqual(sha(ROOT / alias["alias"]), alias["sha256"])
            self.assertTrue(alias["same_run_not_new_evidence"])
        for name in packet["native_decoder"].values():
            decoder = read(ROOT / name)
            self.assertEqual(decoder["role"], "decoder")
            self.assertIsNone(decoder["sourceAgreement"])
            self.assertIsNone(decoder["publication_verdict"])
            self.assertEqual(sha(ROOT / decoder["artifact_path"]), decoder["artifact_sha256"])
            self.assertEqual(sha(ROOT / decoder["probe_stdout_path"]), decoder["probe_stdout_sha256"])
            self.assertEqual(decoder["new_Lean_calls_for_bridge"], 0)

    def test_missing_final_native_input_is_not_green(self):
        absent = PACKET / "decoder-c28/late-context-bridge.json"
        original = Path.is_file
        with patch.object(Path, "is_file", lambda path: False if path == absent else original(path)):
            result = unittest.TestResult()
            PartialC28("test_final_delivery_has_real_role_outputs_and_exact_aliases").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_actual_resume2_transport_preserves_failures_and_cost(self):
        path = PACKET / "parent-resume2-transport.json"
        self.assertEqual(sha(path), "4783c7448988c2d75c9a9752b5c3c8f635b1a195a9612233e2d2dd50942bff82")
        transport = read(path)
        self.assertFalse(transport["new_source_review_or_admission"])
        self.assertEqual(len(transport["artifacts"]), 18)
        for row in transport["artifacts"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(sha(path), row["sha256"])
            self.assertEqual(path.stat().st_size, row["bytes"])
        result = read(RESUME2 / "verification-summary.json")
        self.assertTrue(result["all_latest_actual_targets_compiled"])
        self.assertFalse(result["fresh_Concrete_recompiled"])
        self.assertTrue(result["original_oom_preserved"])
        self.assertFalse(result["all_original_plus_new_lean_calls_exit_zero"])
        self.assertFalse(result["clean_transitive_rebuild"])
        self.assertIsNone(result["sourceAgreement"])
        self.assertIsNone(result["publicationBinding"])
        self.assertEqual(result["new_proof_call_count"], 5)
        self.assertEqual(result["single_thread_flag"], "--threads=1")
        calls = [c for c in result["new_calls"] if c["category"] != "help_metadata"]
        self.assertEqual(len(calls), 5)
        self.assertTrue(all(c["exit_code"] == 0 for c in result["new_calls"]))
        self.assertAlmostEqual(sum(c["elapsed_seconds"] for c in calls), result["new_proof_wall_seconds"])
        self.assertEqual(result["new_help_metadata_call_count"], 1)
        for name, expected in result["original_public_artifact_sha256"].items():
            self.assertEqual(sha(DECODER / name), expected)
        for name, expected in result["resume1_public_artifact_sha256"].items():
            self.assertEqual(sha(RESUME / name), expected)

    def test_all88_actual_signature_and_axiom_outputs(self):
        result = read(RESUME2 / "verification-summary.json")
        self.assertEqual(result["explicit_named_root_check_axiom_count"], 88)
        seen = {}
        for module, count in (("ConcreteSemantics", 25), ("PrimitiveSemantics", 55), ("ReversibleClassical", 8)):
            info = result["evidence"][module]
            log = RESUME2 / ("logs/Probe" + module + "_v1.stdout.public.log")
            self.assertEqual(sha(log), info["probe_public_stdout_sha256"])
            raw = log.read_text(encoding="utf-8")
            actual = dict(re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", raw, re.S))
            actual.update({name: "" for name in re.findall(r"'([^']+)' does not depend on any axioms", raw)})
            self.assertEqual(set(actual), set(info["named_roots"]))
            self.assertEqual(len(actual), count)
            for name, axioms in actual.items():
                self.assertIsNotNone(signature_header(name).search(raw), name)
                self.assertEqual(re.sub(r"\s+", "", axioms), re.sub(r"\s+", "", info["axioms"][name]))
                names = {re.sub(r"\.\{[^}]*\}", "", a.strip()) for a in axioms.split(",") if a.strip()}
                self.assertTrue(names <= {"propext", "Classical.choice", "Quot.sound"})
            seen.update(actual)
        self.assertEqual(len(seen), 88)

    def test_signature_header_retains_universes_and_rejects_missing_or_prefix(self):
        matcher = signature_header("QuantumBlockEncoding.ConcreteSemantics.basisKet_apply")
        self.assertIsNotNone(matcher.search("QuantumBlockEncoding.ConcreteSemantics.basisKet_apply.{u} {n : Nat} : Prop"))
        self.assertIsNotNone(matcher.search("QuantumBlockEncoding.ConcreteSemantics.basisKet_apply (n : Nat) : Prop"))
        self.assertIsNone(matcher.search("QuantumBlockEncoding.ConcreteSemantics.basisKet_apply_extra : Prop"))
        self.assertIsNone(matcher.search("'QuantumBlockEncoding.ConcreteSemantics.basisKet_apply' depends on axioms: [propext]"))

    def test_author_wip_originals_and_lossless_coverage(self):
        path = PACKET / "outputs-manifest.json"
        self.assertEqual(sha(path), "1e238b21c3209fe3d4cf9e662c9bde1eaca6441529dce2e5e660e79dee236cd0")
        manifest = read(path)
        self.assertEqual(len(manifest["artifacts"]), 18)
        self.assertFalse(manifest["independent_acceptance"])
        for row in manifest["artifacts"]:
            actual = ROOT / row["planned_canonical_path"]
            self.assertEqual(sha(actual), row["sha256"])
            self.assertEqual(actual.stat().st_size, row["bytes"])
        coverage = read(PACKET / "author-source-coverage.json")
        paragraphs = coverage["source_paragraphs"]
        self.assertEqual(len(paragraphs), 39)
        self.assertEqual("".join(p["exact_text"] for p in paragraphs).encode(), (PACKET / "source-only.md").read_bytes())
        self.assertEqual(len(coverage["whole_module_inventory"]), 88)
        source_graph = read(PACKET / "author-graph-views.json")["views"]["source-construction-graph"]
        self.assertEqual(len(source_graph["AND_hyperedges"]), 23)
        self.assertEqual(len(source_graph["open_source_gap_ids"]), 7)
        nodes = {n["id"] for n in source_graph["nodes"]}
        for edge in source_graph["AND_hyperedges"]:
            self.assertEqual(edge["logic"], "AND")
            self.assertTrue(set(edge["tails"] + edge["heads"]) <= nodes)

    def test_actual_static_delivery_excludes_decoder_and_compiler(self):
        path = PACKET / "static-review-inputs-c28.json"
        self.assertEqual(sha(path), "f8a52c1757c243ec9ab4b9521ace7522ee902a08c0e55c97264cc4222c9ba12b")
        packet = read(path)
        self.assertEqual(len(packet["input_sha256"]), 31)
        self.assertFalse(packet["main_reader_purification_scientific_ROOT"])
        for name, expected in packet["input_sha256"].items():
            self.assertNotIn("/decoder-c28", name)
            self.assertNotIn("parent-partial-transport", name)
            self.assertEqual(sha(ROOT / name), expected)

    def test_prospective_bindings_replay_without_admission(self):
        spec = importlib.util.spec_from_file_location("c28_prospective", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        source = read(PACKET / "author-source-row-candidate.json")["source"]
        catalog = read(ROOT / "website/research/sources.json")
        own = [row for row in catalog["sources"] if row["id"] == source["id"]]
        if own:
            self.assertEqual(own, [source])
        else:
            catalog["sources"].append(source)
        original = checker.load
        with patch.object(checker, "load", lambda root, name: catalog if name == "website/research/sources.json" else original(root, name)):
            for path in read(PACKET / "static-review-inputs-c28.json")["candidate_paths"]:
                record = read(ROOT / path)
                self.assertEqual(checker.binding_digest(ROOT, record), record["binding_sha256"])
                self.assertEqual(record["status"], "PARENT_PROPOSAL_WIP_NOT_ADMITTED")
                self.assertIn("/decoder-c28/", record["decoder_evidence"])
                self.assertIn("/reviewer-c28/", record["reviewer_evidence"])

    def test_all_actual_public_bytes(self):
        path = PACKET / "parent-partial-transport.json"
        self.assertEqual(sha(path), "3451bdd118862f32ba12bbf701bec1e429e995244b08f20e2881f944074771df")
        manifest = read(path)
        self.assertFalse(manifest["admission"])
        self.assertEqual(len(manifest["artifacts"]), 20)
        for row in manifest["artifacts"]:
            path = ROOT / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(sha(path), row["sha256"])
            self.assertEqual(path.stat().st_size, row["bytes"])

    def test_missing_partial_input_is_not_green(self):
        original = Path.is_file
        absent = RESUME / "environment-precheck.json"
        with patch.object(Path, "is_file", lambda p: False if p == absent else original(p)):
            result = unittest.TestResult()
            PartialC28("test_all_actual_public_bytes").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_original_whole_source_and_configuration_bindings(self):
        seal = read(DECODER / "initial-seal-v2.json")
        self.assertEqual(len(seal["inputs"]), 23)
        self.assertEqual(seal["phase"], "before_first_Lean_command")
        for module, row in seal["inputs"].items():
            name = module.replace(".", "/")
            self.assertEqual(sha(ROOT / (name + ".lean")), row["source_sha256"])
            self.assertEqual(sha(ROOT / ".lake/build/lib/lean" / (name + ".olean")), row["inherited_olean_sha256"])
        for name, expected in seal["configuration"].items():
            self.assertEqual(sha(ROOT / name), expected)
        for name, count in (("ConcreteSemantics", 25), ("PrimitiveSemantics", 55), ("ReversibleClassical", 8)):
            rows = seal["inputs"]["QuantumBlockEncoding." + name]["inventory"]["declarations"]
            self.assertEqual(len(rows), count)
            self.assertFalse(any(row["private"] for row in rows))
        self.assertEqual(sha(DECODER / "initial-seal.json"), seal["supersedes_inventory_only"]["sha256"])

    def test_original_oom_is_not_axiom_or_source_acceptance(self):
        result = read(DECODER / "verification-summary.json")
        self.assertEqual(result["successful_actual_source_compiles"], ["ConcreteSemantics"])
        self.assertIn("out of memory", result["failed_actual_source_compiles"]["PrimitiveSemantics"])
        self.assertEqual(result["unattempted_actual_source_compiles"], ["ReversibleClassical"])
        self.assertEqual(result["executed_check_axiom_probes"], 0)
        self.assertEqual(result["pending_named_root_check_axiom_probes"], 88)
        self.assertIsNone(result["sourceAgreement"])
        self.assertIsNone(result["opaqueAuthorPacketBinding"])
        self.assertFalse(result["axiom_cleanliness_claim"])
        self.assertFalse(result["clean_transitive_rebuild"])
        self.assertIn("out of memory", (DECODER / "logs/PrimitiveSemantics.stderr.public.log").read_text())
        self.assertEqual((DECODER / "logs/PrimitiveSemantics.stdout.public.log").read_bytes(), b"")

    def test_resume_stopped_before_lean(self):
        result = read(RESUME / "decoder-packet.json")
        self.assertEqual(result["status"], "ENV_BLOCKED_PRECHECK_NO_LEAN_LAUNCH")
        self.assertEqual(result["original_packet_sha256"], sha(DECODER / "decoder-packet.json"))
        self.assertEqual(result["verification_summary_sha256"], sha(RESUME / "verification-summary.json"))
        env = read(RESUME / "environment-precheck.json")
        self.assertLess(env["free_virtual_bytes"], env["thresholds_bytes"]["virtual_min"])
        self.assertFalse(env["checks"]["virtual"])
        self.assertEqual(env["proof_calls"], 0)
        self.assertEqual(env["lean_help_calls"], 0)
        self.assertEqual(read(RESUME / "log-allowlist.json")["new_lean_logs"], [])
        self.assertIsNone(result["sourceAgreement"])

    def test_source_first_review_not_implementation_review(self):
        seal = read(PACKET / "reviewer-c28/phase1-seal.json")
        self.assertEqual(sha(PACKET / "source-only.md"), seal["source"]["sha256"])
        self.assertEqual(sha(PACKET / "reviewer-c28/source-only-notes.md"), seal["notes"]["sha256"])
        self.assertEqual(seal["phase"], "SOURCE_ONLY_FROZEN_BEFORE_FORMAL_ACCESS")
        self.assertFalse(seal["implementation_accepted"])
        self.assertFalse(seal["publication_admission_granted"])
        self.assertIn("implementation and actual formal signatures", seal["unread"])
        self.assertIn("decoder reconstruction", seal["unread"])


if __name__ == "__main__":
    unittest.main()
