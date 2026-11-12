"""Actual frozen c27 evidence checks; not source or publication acceptance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[2]
DECODER = PACKET / "decoder-c27r"
MODULES = ("HermiteSmoothness", "HermiteTransferCores", "HermiteBinaryCutoff",
           "StoredHermiteChildGeometry", "StoredHermiteKernelTable")
read = lambda path: json.loads(path.read_text(encoding="utf-8"))
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


class C27Staging(unittest.TestCase):
    def test_actual_final_reviewer_and_native_outputs(self):
        folder = PACKET / "reviewer-c27r"
        self.assertEqual(digest(folder / "final-review-seal.json"), "0c342b16bf2f8c766f57d9215200dab44c88f57916fb5da2284d3f035c82d966")
        seal = read(folder / "final-review-seal.json")
        self.assertEqual(seal["verdict"], "accepted")
        self.assertTrue(seal["anti_anchored"])
        self.assertEqual(digest(folder / "final-review.md"), seal["final_artifact"]["sha256"])
        self.assertEqual(len(seal["native_reviewer_records"]), 5)
        for row in seal["native_reviewer_records"]:
            path = ROOT / row["planned_repository_path"]
            self.assertEqual(digest(path), row["sha256"])
            evidence = read(path)
            self.assertEqual(evidence["identity"], "hermite_substrate_source_review_c27r")
            self.assertEqual(evidence["role"], "reviewer")
            self.assertEqual(evidence["verdict"], "accepted")
            self.assertEqual(evidence["binding_sha256"], row["binding_sha256"])
            self.assertEqual(digest(ROOT / evidence["decoder_evidence_path"]), row["decoder_evidence_sha256"])
            self.assertEqual(set(evidence["semantic_slots"]), {"target", "normalization", "registers", "oracles", "ancillas_phases", "error_success", "resources"})
        self.assertTrue(all(value is False for value in seal["no_expansive_acceptance"].values()))

    def test_canonical_records_validate_with_unchanged_checker(self):
        spec = importlib.util.spec_from_file_location("c27_actual_checker", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        inventory = {row["fullName"]: row for row in read(ROOT / "web/library/declarations.json")["declarations"]}
        records = read(ROOT / "website/research/publications.json")["records"]
        wanted = {"QuantumBlockEncoding/" + name + ".lean" for name in MODULES}
        self.assertEqual({row["module"] for row in records if row["module"] in wanted}, wanted)
        for record in records:
            checker.validate_record(ROOT, record, inventory)

    def test_missing_actual_reviewer_is_rejected_by_original_checker(self):
        spec = importlib.util.spec_from_file_location("c27_missing_checker", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        inventory = {row["fullName"]: row for row in read(ROOT / "web/library/declarations.json")["declarations"]}
        record = next(row for row in read(ROOT / "website/research/publications.json")["records"] if row["module"] == "QuantumBlockEncoding/HermiteSmoothness.lean")
        absent = ROOT / record["reviewer_evidence"]
        original = Path.is_file
        with patch.object(Path, "is_file", lambda path: False if path == absent else original(path)):
            with self.assertRaises(ValueError):
                checker.validate_record(ROOT, record, inventory)

    def test_actual_final_delivery_and_late_same_decoder_binding(self):
        path = PACKET / "final-review-inputs-c27r.json"
        self.assertEqual(digest(path), "c9cbbb4fd852053d4ef7090bc51d3fde377f0ed87355a1b72d33528ea0418c39")
        packet = read(path)
        self.assertEqual(len(packet["input_sha256"]), 64)
        self.assertEqual(packet["role"], "PARENT_DELIVERY_NOT_A_REVIEW_OR_ACCEPTANCE")
        for name, expected in packet["input_sha256"].items():
            actual = ROOT / name
            self.assertTrue(actual.is_file(), name)
            self.assertEqual(digest(actual), expected)
        phase2 = read(PACKET / "reviewer-c27r/phase2-static-seal.json")
        self.assertFalse(phase2["withheld_and_not_performed"]["actual_decoder_c27r_files_read"])
        self.assertFalse(phase2["acceptance"]["implementation_accepted"])
        self.assertEqual(digest(PACKET / "reviewer-c27r/phase2-static-comparison.md"), phase2["comparison"]["sha256"])
        bridge = read(DECODER / "late-context-bridge.json")
        self.assertEqual(bridge["identity"], "hermite-substrate-decoder-c27r")
        self.assertIsNone(bridge["sourceAgreement"])
        self.assertFalse(bridge["binding_chronology"]["new_independent_worker"])
        self.assertFalse(bridge["binding_chronology"]["original_artifacts_modified"])
        self.assertEqual(bridge["runtime_history"]["new_lean_calls"], 0)
        self.assertFalse(bridge["runtime_history"]["first_failed_partial_stdout_retained"])
        self.assertEqual(bridge["provider_accounting"]["providers"], 52)
        self.assertEqual(bridge["provider_accounting"]["new_providers"], [])
        for proposal_path in packet["proposals"]:
            proposal = read(ROOT / proposal_path)
            decoder = read(ROOT / proposal["decoder_evidence"])
            self.assertEqual(decoder["binding_sha256"], proposal["binding_sha256"])
            self.assertEqual(decoder["role"], "decoder")
            self.assertIsNone(decoder["publication_verdict"])
            self.assertIsNone(decoder["sourceAgreement"])
            self.assertEqual(digest(ROOT / decoder["artifact_path"]), decoder["artifact_sha256"])
            self.assertEqual(digest(ROOT / decoder["late_context_bridge_path"]), decoder["late_context_bridge_sha256"])

    def test_missing_final_delivery_input_is_not_green(self):
        original = Path.is_file
        absent = DECODER / "late-context-bridge.json"
        with patch.object(Path, "is_file", lambda path: False if path == absent else original(path)):
            result = unittest.TestResult()
            C27Staging("test_actual_final_delivery_and_late_same_decoder_binding").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_actual_byte_exact_wip_transport(self):
        path = PACKET / "parent-wip-transport.json"
        self.assertEqual(digest(path), "ff492209ba667c98e850b5cbd3729838ef1a4d87f8b2713e2f6939379e48e1fe")
        items = read(path)["artifacts"]
        self.assertEqual(len(items), 14)
        for item in items:
            target = ROOT / item["path"]
            self.assertTrue(target.is_file(), item["path"])
            self.assertEqual(digest(target), item["sha256"])
            self.assertEqual(target.stat().st_size, item["bytes"])

    def test_all_actual_source_and_inherited_project_bindings(self):
        seal = read(DECODER / "initial-seal.json")
        self.assertEqual(digest(DECODER / "initial-seal.json"), "581f718b18b559d60bc1bf7f3dae87e9bea35e893ca050a431868cf98edde783")
        self.assertEqual(len(seal["inputs"]), 57)
        for name, value in seal["inputs"].items():
            source = ROOT / (name.replace(".", "/") + ".lean")
            artifact = ROOT / ".lake/build/lib/lean" / (name.replace(".", "/") + ".olean")
            self.assertEqual(digest(source), value["source_sha256"])
            self.assertEqual(source.stat().st_size, value["source_bytes"])
            self.assertEqual(digest(artifact), value["inherited_olean_sha256"])
        for name, expected in seal["configuration"].items():
            self.assertEqual(digest(ROOT / name), expected)

    def test_current_inventory_equals_all_71_public_and_four_private_roots(self):
        seal = read(DECODER / "initial-seal.json")
        summary = read(DECODER / "verification-summary.json")
        catalog = read(ROOT / "web/library/declarations.json")["declarations"]
        counts = []
        private = []
        for name in MODULES:
            prefix = "QuantumBlockEncoding." + name
            declarations = seal["inputs"][prefix]["inventory"]["declarations"]
            public = {prefix + "." + row["name"] for row in declarations if not row["private"]}
            private.extend(row for row in declarations if row["private"])
            actual = {row["fullName"] for row in catalog if row["source"] == prefix.replace(".", "/") + ".lean"}
            self.assertEqual(public, actual)
            self.assertEqual(public, set(summary["evidence"][name]["public_roots"]))
            counts.append(len(public))
        self.assertEqual(counts, [12, 10, 9, 24, 16])
        self.assertEqual(len(private), 4)

    def test_all_75_real_axiom_reports_are_successful_and_ordinary(self):
        summary = read(DECODER / "verification-summary.json")
        seen = {}
        for name in MODULES:
            info = summary["evidence"][name]
            log = DECODER / ("Probe" + name + ".public.log")
            self.assertEqual(digest(log), info["public_log_sha256"])
            raw = log.read_text(encoding="utf-8")
            reports = dict(re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", raw, re.S))
            # Lean explicitly prints this different successful result for the
            # axiom-free Flags/ChildRun structure types. Missing output is not
            # interpreted as an empty axiom set.
            reports.update({name: "" for name in re.findall(r"'([^']+)' does not depend on any axioms", raw)})
            self.assertEqual(set(reports), set(info["public_roots"]))
            for root, axioms in reports.items():
                self.assertRegex(raw, re.compile(r"^" + re.escape(root) + r"(?:\s|\()", re.M))
                self.assertEqual(re.sub(r"\s+", "", axioms), re.sub(r"\s+", "", info["axioms"][root]))
            seen.update(reports)
        raw = (DECODER / "ProbePrivateRoots.public.log").read_text(encoding="utf-8")
        reports = dict(re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", raw, re.S))
        self.assertEqual(set(reports), set(summary["private_root_axioms"]))
        self.assertEqual(len(reports), 4)
        seen.update(reports)
        self.assertEqual(len(seen), 75)
        for axioms in seen.values():
            names = {re.sub(r"\.\{[^}]*\}", "", x.strip()) for x in axioms.split(",") if x.strip()}
            self.assertTrue(names <= {"propext", "Classical.choice", "Quot.sound"}, names)

    def test_failures_and_nonclean_trust_boundary_not_relabelled(self):
        summary = read(DECODER / "verification-summary.json")
        self.assertEqual(len(summary["lean_calls"]), 14)
        self.assertEqual(summary["actual_source_compile_count"], 5)
        self.assertEqual(summary["successful_public_probe_count"], 5)
        self.assertEqual(summary["successful_private_probe_count"], 1)
        self.assertEqual(summary["failed_probe_count"], 3)
        self.assertEqual(sum(x["exit_code"] != 0 for x in summary["lean_calls"]), 3)
        self.assertFalse(summary["all_calls_exit_zero"])
        self.assertTrue(summary["latest_each_target_exit_zero"])
        self.assertTrue(summary["latest_private_probe_exit_zero"])
        self.assertFalse(summary["clean_transitive_rebuild"])
        self.assertIsNone(summary["sourceAgreement"])
        self.assertIsNone(summary["opaqueAuthorPacketBinding"])
        self.assertTrue(all(x["exit_code"] == 0 for x in summary["lean_calls"] if x["name"] in MODULES))
        self.assertGreater(summary["failed_probe_wall_seconds"], 59)
        for pattern in summary["private_boundary"]:
            self.assertEqual(list(DECODER.glob(pattern)), [])

    def test_source_only_review_precedes_formal_exposure(self):
        seal = read(PACKET / "reviewer-c27r/phase1-seal.json")
        self.assertEqual(digest(PACKET / "reviewer-c27r/phase1-seal.json"), "e59d43f1a64077be1968b82fc8e69e5740b482525f36899e2ab622318391ac8b")
        self.assertEqual(digest(PACKET / "reviewer-c27r/source-only-notes.md"), seal["notes"]["sha256"])
        self.assertEqual(digest(PACKET / "source-only.md"), seal["source"]["sha256"])
        for name in ("implementation_lean_read", "author_mapping_read", "decoder_read", "previous_review_read", "compile_or_cache_results_read"):
            self.assertFalse(seal["exposure"][name])
        self.assertFalse(seal["formal_review"]["implementation_accepted"])

    def test_missing_bound_file_is_not_green(self):
        original = Path.is_file
        absent = DECODER / "ProbePrivateRoots.public.log"
        with patch.object(Path, "is_file", lambda path: False if path == absent else original(path)):
            result = unittest.TestResult()
            C27Staging("test_actual_byte_exact_wip_transport").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])


    def test_frozen_author_metadata_and_complete_lossless_coverage(self):
        path = PACKET / "outputs-manifest.json"
        self.assertEqual(digest(path), "312e432c61f9e7cbdbe1b0dbc4b9ee1e7ffb5c906eaad742fc3e8804f32b3e55")
        items = read(path)["artifacts"]
        self.assertEqual(len(items), 21)
        for row in items:
            actual = ROOT / row["planned_canonical_path"]
            self.assertEqual(digest(actual), row["sha256"])
            self.assertEqual(actual.stat().st_size, row["bytes"])
        coverage = read(PACKET / "author-source-coverage.json")
        paragraphs = coverage["source_paragraphs"]
        self.assertEqual(len(paragraphs), 102)
        self.assertEqual("".join(p["exact_text"] for p in paragraphs).encode(), (PACKET / "source-only.md").read_bytes())
        self.assertEqual(len(coverage["whole_module_inventory"]), 75)
        graph = read(PACKET / "author-graph-views.json")["views"]["source-construction-graph"]
        self.assertEqual(len(graph["AND_hyperedges"]), 22)
        nodes = {n["id"]: n for n in graph["nodes"]}
        for edge in graph["AND_hyperedges"]:
            self.assertEqual(edge["logic"], "AND")
            self.assertTrue(set(edge["tails"] + edge["heads"]) <= nodes.keys())
        gaps = {name for name, row in nodes.items() if row["kind"] == "SOURCE_GAP"}
        self.assertEqual(gaps, set(graph["open_source_gap_ids"]))
        self.assertEqual(len(gaps), 6)

    def test_actual_static_inputs_and_prospective_binding_replay_only(self):
        path = PACKET / "static-review-inputs-c27r.json"
        self.assertEqual(digest(path), "e7a03dfdcd050fdc2396c3d6cb216c80bae9711d8006f79a67728486e6bc1d4d")
        packet = read(path)
        self.assertEqual(len(packet["input_sha256"]), 38)
        for name, expected in packet["input_sha256"].items():
            self.assertNotIn("/decoder-c27r/", name)
            self.assertEqual(digest(ROOT / name), expected)
        self.assertFalse(packet["main_reader_purification_scientific_ROOT"])
        spec = importlib.util.spec_from_file_location("c27_prospective_digest", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        original_load = checker.load
        source = read(PACKET / "author-source-row-candidate.json")["source"]
        catalog = read(ROOT / "website/research/sources.json")
        owned = [row for row in catalog["sources"] if row["id"] == source["id"]]
        if owned:
            self.assertEqual(owned, [source])
        else:
            catalog["sources"].append(source)
        # Prospective input-data overlay only; the checker function is unchanged
        # and no canonical row, verifier or acceptance evidence is written here.
        with patch.object(checker, "load", lambda root, name: catalog if name == "website/research/sources.json" else original_load(root, name)):
            for name in packet["candidate_paths"]:
                record = read(ROOT / name)
                self.assertEqual(checker.binding_digest(ROOT, record), record["binding_sha256"])
                self.assertEqual(record["status"], "PARENT_PROPOSAL_WIP_NOT_ADMITTED")
                self.assertIn("/decoder-c27r/", record["decoder_evidence"])
                self.assertIn("/reviewer-c27r/", record["reviewer_evidence"])


if __name__ == "__main__":
    unittest.main()
