"""Fail-closed checks for frozen c25 staging, not publication admission."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[2]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FrozenStaging(unittest.TestCase):
    def test_manifest_exact_bytes_at_actual_destinations(self):
        manifest = PACKET / "outputs-manifest.json"
        self.assertEqual(digest(manifest), "8d48512050438af73e4560a56f1e1d68e15cb589990a5664eb5938253eebceef")
        for item in read(manifest)["artifacts"]:
            with self.subTest(path=item["planned_canonical_path"]):
                target = ROOT / item["planned_canonical_path"]
                self.assertTrue(target.is_file())
                self.assertEqual(target.stat().st_size, item["bytes"])
                self.assertEqual(digest(target), item["sha256"])

    def test_all_source_paragraphs_reconstruct_raw_lesson(self):
        coverage = read(PACKET / "author-source-coverage.json")
        source = ROOT / coverage["source_path"]
        blocks = coverage["source_paragraphs"]
        self.assertEqual(len(blocks), 79)
        self.assertEqual("".join(x["exact_text"] for x in blocks).encode(), source.read_bytes())
        self.assertEqual(digest(source), coverage["source_sha256"])
        offset = 0
        for block in blocks:
            raw = block["exact_text"].encode()
            self.assertEqual(block["start_utf8_byte"], offset)
            offset += len(raw)
            self.assertEqual(block["end_utf8_byte"], offset)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), block["sha256"])

    def test_full_formal_snapshots_and_actual_inputs_still_match(self):
        context = read(PACKET / "author-formal-context.json")
        for item in context["files"] + context["toolchain_manifest"]:
            self.assertEqual("".join(item["full_source_lines"]).encode(), (ROOT / item["path"]).read_bytes())
            self.assertEqual(digest(ROOT / item["path"]), item["sha256"])
        freeze = read(PACKET / "author-freeze.json")
        for item in freeze["production_inputs"] + freeze["other_fixed_inputs"]:
            self.assertEqual(digest(ROOT / item["path"]), item["sha256"])
        self.assertEqual(len(context["declarations"]), 49)
        self.assertEqual(sum(x["canonical_inventory_root"] for x in context["declarations"]), 48)

    def test_distinct_source_and_import_graphs_remain_bounded(self):
        views = read(PACKET / "author-graph-views.json")["views"]
        source = views["source-construction-graph"]
        nodes = {x["id"]: x for x in source["nodes"]}
        self.assertEqual(len(source["hyperedges"]), 22)
        self.assertEqual(len(source["independent_source_gap_ids"]), 7)
        for edge in source["hyperedges"]:
            self.assertEqual(edge["logic"], "AND")
            self.assertTrue(edge["tails"] and edge["heads"])
            self.assertTrue(set(edge["tails"] + edge["heads"]) <= nodes.keys())
        for ident in source["independent_source_gap_ids"]:
            self.assertEqual(nodes[ident]["status"], "OPEN")
            self.assertFalse(nodes[ident]["mathematical_proof_node"])
        self.assertEqual(len(views["lean-graph"]["target_import_edges"]), 3)
        self.assertEqual(len(views["lean-graph"]["ownership_edges"]), 49)
        self.assertFalse(views["functor-hypergraph"]["certified_transport"])

    def test_prior_independent_phases_are_present_and_unaltered(self):
        expected = {
            "source-only-notes.md": "84011962ce0cdaedbf27027c7f7c17c0b50562da716fd1b5d030a5a0dbb3051b",
            "phase1-seal.json": "fe9c73b69d5e0d48990d94ebb8becf6f82157bf0335161002c443cf2d15650f8",
            "phase2-static-comparison.md": "615f1be47ad998945e35bb370bd084d1b6fae812422e536fde7139ad359a39f5",
            "phase2-static-seal.json": "b9e43c4f479343322e9ece9d4f3bad41220e6470aa223111b6cbae4d3e78bcff",
        }
        for name, sha in expected.items():
            self.assertEqual(digest(PACKET / "reviewer-c25" / name), sha)
        static = read(PACKET / "reviewer-c25/phase2-static-seal.json")
        self.assertTrue(static["unseen_at_freeze"]["decoder_or_reconstruction"])
        self.assertTrue(static["unseen_at_freeze"]["assembled_author_metadata_packet"])

    def test_prospective_bindings_only_not_admission(self):
        spec = importlib.util.spec_from_file_location("c25_public_checker", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        original = checker.load
        row = read(PACKET / "author-source-row-candidate.json")["source"]

        def prospective_load(root, name):
            data = original(root, name)
            if name == "website/research/sources.json":
                existing = [x for x in data["sources"] if x["id"] == row["id"]]
                self.assertTrue(not existing or existing == [row])
                if not existing:
                    data["sources"].append(row)
            return data

        with patch.object(checker, "load", prospective_load):
            for name in ("publication-candidate-canonical.json", "publication-candidate-norm-environment.json"):
                record = read(PACKET / name)
                self.assertEqual(checker.binding_digest(ROOT, record), record["binding_sha256"])
                self.assertEqual(record["status"], "AUTHOR_WIP_NOT_ADMITTED")
                self.assertFalse(record["main_admission"])
                self.assertFalse(record["scientific_ROOT"])
                self.assertEqual(record["purification"]["status"], "PENDING")

    def test_actual_final_delivery_inputs_and_native_decoder_evidence(self):
        manifest = PACKET / "final-review-inputs-c25.json"
        self.assertEqual(digest(manifest), "385c6fda9f188e2b6b283e1ed895b1b9f22e40d37416e1ce2132282cbb5992b5")
        data = read(manifest)
        self.assertTrue(data["created_after_source_static_and_metadata_phases"])
        self.assertTrue(data["created_before_final_decoder_comparison"])
        self.assertEqual(len(data["input_sha256"]), 41)
        for name, sha in data["input_sha256"].items():
            self.assertEqual(digest(ROOT / name), sha)
        for name in ("canonical-evidence.json", "norm-environment-evidence.json"):
            evidence = read(PACKET / "decoder-c25" / name)
            self.assertEqual(evidence["role"], "decoder")
            self.assertEqual(evidence["identity"], "ttc-norm-decoder-c25")
            self.assertTrue(evidence["source_blind"])
            self.assertEqual(evidence["new_lean_invocations"], 0)
            self.assertIsNone(evidence["source_agreement_verdict"])
            self.assertEqual(digest(ROOT / evidence["packet_path"]), evidence["packet_sha256"])
            self.assertEqual(digest(ROOT / evidence["artifact_path"]), evidence["artifact_sha256"])
            self.assertEqual(evidence["binding_sha256"], data["opaque_bindings"][evidence["target_module"]])

    def test_missing_bound_file_is_not_green(self):
        original = Path.is_file
        missing = PACKET / "author-graph-views.json"

        def simulated_missing(path):
            return False if path == missing else original(path)

        with patch.object(Path, "is_file", simulated_missing):
            result = unittest.TestResult()
            FrozenStaging("test_manifest_exact_bytes_at_actual_destinations").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_corrupted_bound_bytes_are_not_green(self):
        original = Path.read_bytes
        corrupted = ROOT / "docs/lessons/finite-real-tensor-train-canonicalization-and-gram.md"

        def simulated_corruption(path):
            raw = original(path)
            return raw + b" " if path == corrupted else raw

        with patch.object(Path, "read_bytes", simulated_corruption):
            with self.assertRaises(AssertionError):
                self.test_all_source_paragraphs_reconstruct_raw_lesson()

    def test_actual_canonical_pair_and_frozen_reviewer_originals(self):
        seal = PACKET / "reviewer-c25/final-seal.json"
        self.assertEqual(digest(seal), "d9c1d2f3ceaf5f3525fa34e17bc1884bf8cc6865bd869aea220fd7cf9a9f0b56")
        for artifact in read(seal)["new_original_artifacts"]:
            target = PACKET / "reviewer-c25" / artifact["file"]
            self.assertEqual(digest(target), artifact["sha256"])
            self.assertEqual(target.stat().st_size, artifact["bytes"])
        spec = importlib.util.spec_from_file_location("c25_registered_checker", ROOT / "website/scripts/check_research_publications.py")
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        inventory = {x["fullName"]: x for x in read(ROOT / "web/library/declarations.json")["declarations"]}
        records = read(ROOT / "website/research/publications.json")["records"]
        targets = set(read(PACKET / "final-review-inputs-c25.json")["opaque_bindings"])
        selected = [r for r in records if r["module"] in targets]
        self.assertEqual(len(selected), 2)
        for record in selected:
            checker.validate_record(ROOT, record, inventory)
            self.assertEqual(record["status"], "SOURCE_REVIEWED_LOCAL_INTEGRATION_PENDING")
            self.assertFalse(record["main_admission"])
            self.assertFalse(record["scientific_ROOT"])
            evidence = read(ROOT / record["reviewer_evidence"])
            self.assertEqual(evidence["identity"], "ttc_norm_source_first_review_c25")
            self.assertEqual(evidence["verdict"], "accepted")


if __name__ == "__main__":
    unittest.main()
