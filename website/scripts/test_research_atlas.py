from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path, PurePosixPath, PureWindowsPath
from unittest.mock import patch

from website.scripts import research_atlas as atlas
from website.scripts import check_research_publications as publication


class ResearchCatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = atlas.load_catalog()

    def test_catalog(self):
        atlas.validate_catalog(self.catalog)

    def test_every_requested_research_direction_has_acceptance_steps(self):
        routes = {item["id"]: item for item in self.catalog["wiki"]["routes"]}
        self.assertEqual(set(routes), {"spw-structured", "spw-envelope", "spw-no-qram", "spw-controlled", "spw-ground", "spw-gibbs", "spw-fault-tolerant", "spw-verification", "spw-cvdv", "spw-walsh", "spw-diagonal", "spw-uncompute"})
        self.assertTrue(all(len(r["steps"]) >= 3 for r in routes.values()))

    def test_cannot_promote_conceptual_functor(self):
        self.catalog["atlas"]["hyperedges"][0]["status"] = "Lean-certified"
        with self.assertRaisesRegex(ValueError, "certified Lean functor"):
            atlas.validate_catalog(self.catalog)

    def test_empty_and_tail_fails(self):
        self.catalog["atlas"]["hyperedges"][0]["tails"] = []
        with self.assertRaisesRegex(ValueError, "AND"):
            atlas.validate_catalog(self.catalog)

    def test_unknown_node_fails(self):
        self.catalog["atlas"]["hyperedges"][0]["tails"].append("family:not-a-node")
        with self.assertRaisesRegex(ValueError, "endpoint"):
            atlas.validate_catalog(self.catalog)

    def test_model_switch_is_not_a_lower_bound_result(self):
        self.catalog["wiki"]["routes"][0]["lower_bound"]["comparison_key"] = "free-qram"
        with self.assertRaisesRegex(ValueError, "changes model"):
            atlas.validate_catalog(self.catalog)

    def test_source_candidate_is_retained_not_promoted(self):
        source = next(s for s in self.catalog["sources"]["sources"] if s["id"] == "butterworth-2026-candidate")
        self.assertEqual(source["status"], "primary-source-unavailable")
        self.assertEqual(source["formal_status"], "external-reference")

    def test_unknown_lean_ref_fails_at_publication(self):
        with self.assertRaisesRegex(ValueError, "unknown generated Lean"):
            atlas.validate_catalog(self.catalog, {})

    def test_lookup_packet_is_bounded_and_keeps_full_hyperedges(self):
        packet = atlas.context_packet(self.catalog, route_id="spw-envelope", limit=1000)
        self.assertLessEqual(len(packet["families"]), 6)
        self.assertEqual(len(packet["routes"]), 1)
        original = {e["id"]: e for e in self.catalog["atlas"]["hyperedges"]}
        for edge in packet["hyperedges"]:
            self.assertEqual(edge["tails"], original[edge["id"]]["tails"])
            self.assertTrue(edge["failure_boundary"])

    def test_specific_search_finds_structure(self):
        packet = atlas.context_packet(self.catalog, query="Bernstein")
        self.assertIn("family:hermite-bernstein", [f["id"] for f in packet["families"]])

    def technical_card(self, catalog=None):
        catalog = self.catalog if catalog is None else catalog
        return next(f["technical_card"] for f in catalog["atlas"]["families"] if f["id"] == "family:walsh-diagonal-phase")

    def test_planned_technical_cards_and_routes_are_retrievable(self):
        for family_id, route_id, query in (("family:walsh-diagonal-phase", "spw-walsh", "Walsh"),
                                            ("family:diagonal-postselection", "spw-diagonal", "diagonal postselection")):
            with self.subTest(family=family_id):
                packet = atlas.context_packet(self.catalog, route_id=route_id)
                family = next(f for f in packet["families"] if f["id"] == family_id)
                card = family["technical_card"]
                self.assertEqual(card["lean_status"], "obligation")
                self.assertEqual(card["lean_decl"], [])
                self.assertIn(route_id, card["used_by"])
                self.assertIn(family_id, [f["id"] for f in atlas.context_packet(self.catalog, query=query)["families"]])
                originals = {s["id"]: s for s in self.catalog["sources"]["sources"]}
                packet_sources = {s["id"]: s for s in packet["sources"]}
                records = packet["families"] + packet["routes"] + packet["hyperedges"] + [card]
                for record in records:
                    for source_id in record.get("source_ids", []):
                        self.assertEqual(packet_sources[source_id], originals[source_id])
                originals = {e["id"]: e for e in self.catalog["atlas"]["hyperedges"]}
                self.assertTrue(packet["hyperedges"])
                self.assertLessEqual(len(packet["hyperedges"]), 4)
                for edge in packet["hyperedges"]:
                    self.assertEqual(edge, originals[edge["id"]])

    def test_card_fields_and_reference_types_are_checked(self):
        for field in tuple(self.technical_card()):
            with self.subTest(missing=field):
                catalog = copy.deepcopy(self.catalog)
                del self.technical_card(catalog)[field]
                with self.assertRaisesRegex(ValueError, "missing"):
                    atlas.validate_catalog(catalog)
        for field, bad in (("source_ids", ["missing-source"]), ("used_by", ["spw-missing"]),
                           ("dependencies", ["family:missing"]), ("lean_status", "certified"),
                           ("source_ids", "not-a-list"), ("failure_modes", []), ("statement", [])):
            with self.subTest(field=field, bad=bad):
                catalog = copy.deepcopy(self.catalog)
                self.technical_card(catalog)[field] = bad
                with self.assertRaisesRegex(ValueError, "technical card"):
                    atlas.validate_catalog(catalog)

    def test_technical_card_status_cannot_promote_or_downgrade_certificate(self):
        card = self.technical_card()
        card["lean_status"] = "formalized"
        with self.assertRaisesRegex(ValueError, "requires a local declaration"):
            atlas.validate_catalog(self.catalog)
        card["lean_decl"] = ["Invented.localCertificate"]
        with self.assertRaisesRegex(ValueError, "unknown generated Lean declaration in technical card"):
            atlas.validate_catalog(self.catalog, {})
        for status in atlas.TECHNICAL_STATES - {"formalized"}:
            card["lean_status"] = status
            with self.subTest(status=status), self.assertRaisesRegex(ValueError, "cannot claim a local certificate"):
                atlas.validate_catalog(self.catalog)

    def test_source_audit_status_never_promotes_technical_card(self):
        card = self.technical_card()
        source = next(s for s in self.catalog["sources"]["sources"] if s["id"] == card["source_ids"][0])
        for status in atlas.SOURCE_STATES:
            with self.subTest(source_status=status):
                source["status"] = status
                packet = atlas.context_packet(self.catalog, route_id="spw-walsh")
                exported = next(f["technical_card"] for f in packet["families"] if f["id"] == "family:walsh-diagonal-phase")
                self.assertEqual(exported["lean_status"], "obligation")
                self.assertEqual(exported["lean_decl"], [])
                self.assertEqual(next(s for s in packet["sources"] if s["id"] == source["id"])["status"], status)

    def test_open_or_experimental_declaration_cannot_certify_card(self):
        card = self.technical_card()
        card.update(lean_status="formalized", lean_decl=["Test.card"])
        for flag in ("openProof", "experimental"):
            with self.subTest(flag=flag), self.assertRaisesRegex(ValueError, "non-certified technical card declaration"):
                atlas.validate_catalog(self.catalog, {"Test.card": {flag: True}})

    def test_duplicate_technical_card_identity_is_rejected(self):
        families = self.catalog["atlas"]["families"]
        other = next(f for f in families if f["id"] == "family:diagonal-postselection")
        other["technical_card"]["id"] = self.technical_card()["id"]
        with self.assertRaisesRegex(ValueError, "duplicate technical card id"):
            atlas.validate_catalog(self.catalog)

    def test_technical_card_render_has_visible_uncertified_boundary(self):
        card = self.technical_card()
        rendered = atlas.render_technical_card(card,
            {f["id"]: f for f in self.catalog["atlas"]["families"]},
            {r["id"]: r for r in self.catalog["wiki"]["routes"]},
            {s["id"]: s for s in self.catalog["sources"]["sources"]}, {}, "../../")
        self.assertIn("Planned / uncertified", rendered)
        self.assertIn("not a local Lean certificate", rendered)
        self.assertIn(atlas.esc(card["statement"]), rendered)
        self.assertIn(atlas.esc(card["next_action"]), rendered)
        for failure in card["failure_modes"]:
            self.assertIn(atlas.esc(failure), rendered)

    def test_route_order_and_relevant_complete_hyperedges_have_priority(self):
        route = next(r for r in self.catalog["wiki"]["routes"] if r["id"] == "spw-walsh")
        families = route["families"]
        self.assertGreaterEqual(len(families), 2)
        template = copy.deepcopy(self.catalog["atlas"]["hyperedges"][0])
        unrelated = []
        for index in range(4):
            edge = copy.deepcopy(template)
            edge.update(id=f"transport:test-generic-{index}", tails=[families[0]], heads=[families[0]])
            unrelated.append(edge)
        relevant = copy.deepcopy(template)
        relevant.update(id="transport:test-direct-route", tails=list(families), heads=[families[-1]])
        self.catalog["atlas"]["hyperedges"] = unrelated + [relevant]
        packet = atlas.context_packet(self.catalog, route_id=route["id"], limit=1)
        self.assertEqual(packet["families"][0]["id"], families[0])
        self.assertEqual(packet["hyperedges"][0], relevant)
        self.assertEqual(packet["hyperedges"][0]["tails"], families)

    def test_latex_is_a_lesson_not_proof_promotion(self):
        family = copy.deepcopy(self.catalog["atlas"]["families"][0])
        family["formula"] = "U^† U = I"
        text = atlas.family_latex(family)
        self.assertIn("not a new theorem certificate", text)
        self.assertIn(r"\dagger", text)
        self.assertNotIn("†", text)

    def test_new_papers_are_queued_not_locally_formalized(self):
        papers = atlas.read_json(atlas.ROOT / "website/papers.json")
        queue = {p["key"]: p for p in papers["queue"]}
        sources = {s["id"]: s for s in self.catalog["sources"]["sources"]}
        for key in ("zylberman-debbasch-2024-walsh", "zylberman-et-al-2025-diagonal"):
            self.assertEqual(queue[key]["status"], "queued")
            self.assertFalse(queue[key].get("leanRoots"))
            self.assertEqual(sources[key]["formal_status"], "planned-formalization")
            self.assertEqual(queue[key]["url"], sources[key]["url"])
            self.assertRegex(sources[key]["url"], r"v\d+$")
            self.assertTrue(queue[key]["sourceAnchors"])
            route_id = queue[key]["planningRoute"].split("/")[1]
            route = next(r for r in self.catalog["wiki"]["routes"] if r["id"] == route_id)
            self.assertIn(key, route["source_ids"])

    def test_walsh_route_retains_source_sign_and_success_boundary(self):
        packet = atlas.context_packet(self.catalog, route_id="spw-walsh")
        edge = next(e for e in packet["hyperedges"] if e["id"] == "transport:walsh-loader")
        self.assertIn(r"-i(I-e^{-i\tau F_S})", edge["formula"])
        self.assertIn("family:diagonal-postselection", edge["tails"])
        self.assertIn("family:charged-access", edge["tails"])
        self.assertEqual(edge["status"], "proposal")
        self.assertEqual(edge["lean_refs"], [])
        route = packet["routes"][0]
        self.assertIn("infidelity", " ".join(route["assumptions"]))
        self.assertIn("Nonzero constant", " ".join(route["benchmarks"]))

    def test_paper_queue_links_to_uncertified_plan(self):
        from unittest.mock import patch
        from website.scripts import publish_taxonomy
        papers = atlas.read_json(atlas.ROOT / "website/papers.json")
        with patch.object(publish_taxonomy.build_site, "page_template", side_effect=lambda **kw: kw["body"]):
            page = publish_taxonomy.render_paper_topic_page("statePreparation", papers, {}, {}, {})
        self.assertIn("Read formalization plan (not a certificate)", page)
        for route in ("spw-walsh", "spw-diagonal"):
            self.assertIn(f'../../state-preparation-wiki/{route}/index.html', page)


class PublicCatalogProjectionTests(unittest.TestCase):
    SOURCE_IDS = {
        "aspbe-local-exact-primitives-controlled-rotations-finite-cubic",
        "aspbe-local-stored-rectangular-elimination-v1",
        "aspbe-local-retrospective-sequential-primitive-assembly-c48",
    }

    def setUp(self):
        self.catalog = atlas.load_catalog()
        spec = importlib.util.spec_from_file_location(
            "publication_path_scanner", atlas.ROOT / "scripts/sanitize-blueprint-paths.py")
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        self.scanner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.scanner)

    def scan_sources(self, sources):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sources.json").write_text(json.dumps(sources), encoding="utf-8")
            return self.scanner._assert_no_local_paths(root, atlas.ROOT)

    def test_exact_lossless_display_preserves_canonical_bytes_and_scientific_fields(self):
        original = copy.deepcopy(self.catalog)
        canonical_bytes = {name: (atlas.DATA / filename).read_bytes()
                           for name, filename in atlas.FILES.items()}
        digest = atlas.source_digest()
        projected = atlas.public_catalog(self.catalog)
        self.assertEqual(self.catalog, original)
        self.assertEqual(atlas.source_digest(), digest)
        for name, filename in atlas.FILES.items():
            self.assertEqual((atlas.DATA / filename).read_bytes(), canonical_bytes[name])
        self.assertEqual(projected["atlas"], original["atlas"])
        self.assertEqual(projected["wiki"], original["wiki"])
        changed = set()
        for canonical, public in zip(original["sources"]["sources"], projected["sources"]["sources"]):
            if canonical != public:
                changed.add(canonical["id"])
                self.assertEqual(public["authors"], canonical["authors"].replace("/root", "agent-task:root"))
                self.assertEqual(public["authors"].replace("agent-task:", "/"), canonical["authors"])
                self.assertEqual({k: v for k, v in public.items() if k != "authors"},
                                 {k: v for k, v in canonical.items() if k != "authors"})
            else:
                self.assertNotIn(canonical["id"], self.SOURCE_IDS)
        self.assertEqual(changed, self.SOURCE_IDS)
        restored = copy.deepcopy(projected["sources"])
        disclosure = restored.pop("public_projection")
        self.assertEqual(disclosure["schema_version"], "research.sources_author_identity_display.v1")
        self.assertIn("no new source, mathematical or formalization review", disclosure["review_boundary"])
        self.assertIn("unmodified_canonical", disclosure["source_digest_binds"])
        for source in restored["sources"]:
            if source["id"] in self.SOURCE_IDS:
                source["authors"] = source["authors"].replace("agent-task:", "/")
        self.assertEqual(restored, original["sources"])
        with self.assertRaisesRegex(ValueError, "local filesystem paths"):
            self.scan_sources(original["sources"])
        self.assertEqual(self.scan_sources(projected["sources"]), 1)

    def test_unknown_or_extended_author_strings_and_real_paths_remain_detectable(self):
        source = next(s for s in self.catalog["sources"]["sources"] if s["id"] in self.SOURCE_IDS)
        canonical_authors = source["authors"]
        # Artificial paths are string-processing fixtures, never destinations.
        private_path = str(PurePosixPath("/", "root", "private", "report.json"))
        for authors in (canonical_authors + " " + private_path,
                        canonical_authors + " (unrecognized extra metadata)",
                        str(PurePosixPath("/", "root", "not_an_allowlisted_task")),
                        str(PurePosixPath("/", "home", "fixture", "private", "report.json")),
                        str(PureWindowsPath("Z:/", "Users", "fixture", "private", "report.json")),
                        str(PurePosixPath("/", "root", "primitive_compiler_metadata_c31", "report.json"))):
            with self.subTest(authors_kind=authors.split("/", 1)[0]):
                source["authors"] = authors
                public = atlas.public_catalog(self.catalog)["sources"]
                self.assertEqual(next(s for s in public["sources"] if s["id"] == source["id"])["authors"], authors)
                with self.assertRaisesRegex(ValueError, "local filesystem paths"):
                    self.scan_sources(public)

    def test_known_authors_on_an_unlisted_source_are_not_rewritten(self):
        source = copy.deepcopy(next(s for s in self.catalog["sources"]["sources"] if s["id"] in self.SOURCE_IDS))
        source["id"] = "fixture-unlisted-source"
        self.catalog["sources"]["sources"].append(source)
        public = atlas.public_catalog(self.catalog)["sources"]
        self.assertEqual(public["sources"][-1], source)
        with self.assertRaisesRegex(ValueError, "local filesystem paths"):
            self.scan_sources(public)

    def test_arbitrary_nested_fields_are_not_scrubbed(self):
        source = next(s for s in self.catalog["sources"]["sources"] if s["id"] in self.SOURCE_IDS)
        source["extra_metadata"] = {
            "authors": source["authors"],
            "path": str(PurePosixPath("/", "root", "private", "report.json")),
        }
        public = atlas.public_catalog(self.catalog)["sources"]
        displayed = next(s for s in public["sources"] if s["id"] == source["id"])
        self.assertEqual(displayed["extra_metadata"], source["extra_metadata"])
        with self.assertRaisesRegex(ValueError, "local filesystem paths"):
            self.scan_sources(public)

    def test_original_schema_is_validated_before_projection(self):
        self.catalog["sources"]["schema_version"] = 2
        with patch.object(atlas, "deepcopy", side_effect=AssertionError("projection ran before validation")):
            with self.assertRaisesRegex(ValueError, "unsupported sources schema"):
                atlas.public_catalog(self.catalog)

    def test_projection_cannot_overwrite_a_canonical_field(self):
        self.catalog["sources"]["public_projection"] = {"canonical": "must not be overwritten"}
        with self.assertRaisesRegex(ValueError, "canonical sources"):
            atlas.public_catalog(self.catalog)

    def test_publish_emits_exact_projected_json_before_reader_rendering(self):
        from website.scripts import build_site as site
        refs = {ref for collection in ("families", "hyperedges", "contributions")
                for item in self.catalog["atlas"][collection] for ref in item.get("lean_refs", [])}
        refs |= {ref for item in self.catalog["wiki"]["routes"] for ref in item.get("lean_refs", [])}
        refs |= {ref for item in self.catalog["atlas"]["families"]
                 for ref in item.get("technical_card", {}).get("lean_decl", [])}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixtures = {
                "library/declarations.json": {"declarations": [{"fullName": ref} for ref in refs]},
                "data/lean-graph.json": {"nodes": [{"id": "declaration:" + ref} for ref in refs]},
                "build-report.json": {"coverage": {}, "leanGate": {"passed": True, "commit": "a" * 40}},
            }
            for filename, value in fixtures.items():
                path = root / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(value), encoding="utf-8")
            # Deliberately bounded: exercise the real JSON write loop, not a full-site gate.
            with patch.object(atlas, "load_catalog", return_value=self.catalog), \
                 patch.object(site, "git_context", return_value={"commit": "a" * 40}), \
                 patch.object(atlas.shutil, "copyfile", side_effect=RuntimeError("stop before reader rendering")):
                with self.assertRaisesRegex(RuntimeError, "stop before reader rendering"):
                    atlas.publish(root)
            expected = atlas.public_catalog(self.catalog)
            for name, filename in atlas.FILES.items():
                self.assertEqual(atlas.read_json(root / "data/research" / filename), expected[name])
            self.assertEqual(self.scanner._assert_no_local_paths(root / "data/research", atlas.ROOT), 3)
            source_file = root / "data/research/sources.json"
            for field in ("authors", "status", "anchor", "scope", "formal_status"):
                tampered = copy.deepcopy(expected["sources"])
                tampered["sources"][0][field] = "tampered"
                source_file.write_text(json.dumps(tampered), encoding="utf-8")
                with self.subTest(field=field), self.assertRaisesRegex(ValueError, "display projection"):
                    atlas.check_published(root)


class PublicationBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.write("QuantumBlockEncoding/Test.lean", "theorem test : True := by trivial\n")
        self.write("lean-toolchain", "test-toolchain\n")
        self.write("lake-manifest.json", "{}\n")
        self.write("lesson.md", "Statement and mathematical proof.\n")
        self.write_json("website/research/sources.json", {"sources": [{"id": "test-source", "status": "primary-text-checked", "anchor": "synthetic fixture"}]})
        self.record = {"module": "QuantumBlockEncoding/Test.lean", "source_id": "test-source", "source_statement": "Synthetic test statement", "source_anchor": "fixture only", "lesson_path": "lesson.md", "declarations": ["test"], "obligation_map": [{"kind": "proof-edge", "source_obligation": "fixture", "declarations": ["test"]}], "assumption_deltas": [{"classification": "same", "source": "True", "formal": "True", "explanation": "fixture"}], "graph_contribution": {"baseline": "test-baseline", "classes": ["add-node"], "node_ids": ["declaration:test"], "views": ["lean-graph"], "preserved_contract": "fixture", "remaining_boundary": "fixture only"}, "formalizer": "test-author", "residual_boundary": "synthetic fixture, never publication evidence", "decoder_evidence": "decoder.json", "reviewer_evidence": "reviewer.json"}
        digest = publication.binding_digest(self.root, self.record)
        self.record["binding_sha256"] = digest
        self.write("decoder-packet.txt", "Anonymous formal context\n")
        self.write("review-packet.txt", "Source and reconstruction\n")
        self.write("decoder-artifact.txt", "Fixture reconstruction\n")
        self.write("review-artifact.txt", "Fixture verdict\n")
        self.decoder = {"role": "decoder", "binding_sha256": digest, "identity": "test-decoder", "run_id": "fixture", "packet_path": "decoder-packet.txt", "packet_sha256": hashlib.sha256((self.root / "decoder-packet.txt").read_bytes()).hexdigest(), "artifact_path": "decoder-artifact.txt", "source_blind": True, "reconstruction": "True"}
        self.reviewer = {"role": "reviewer", "binding_sha256": digest, "identity": "test-reviewer", "run_id": "fixture", "packet_path": "review-packet.txt", "packet_sha256": hashlib.sha256((self.root / "review-packet.txt").read_bytes()).hexdigest(), "artifact_path": "review-artifact.txt", "anti_anchored": True, "verdict": "accepted", "semantic_slots": {key: "fixture" for key in ("target", "normalization", "registers", "oracles", "ancillas_phases", "error_success", "resources")}}
        self.flush()
        self.inventory = {"test": {"source": "QuantumBlockEncoding/Test.lean"}}

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")

    def write_json(self, name, value):
        self.write(name, json.dumps(value))

    def flush(self):
        for evidence in (self.decoder, self.reviewer):
            evidence["artifact_sha256"] = hashlib.sha256((self.root / evidence["artifact_path"]).read_bytes()).hexdigest()
        self.write_json("decoder.json", self.decoder)
        self.reviewer["decoder_evidence_sha256"] = hashlib.sha256((self.root / "decoder.json").read_bytes()).hexdigest()
        self.write_json("reviewer.json", self.reviewer)

    def test_synthetic_integrity_fixture(self):
        publication.validate_record(self.root, self.record, self.inventory)

    def test_private_helper_change_invalidates_whole_module(self):
        self.write("QuantumBlockEncoding/Test.lean", "private def helper := False\ntheorem test : True := by trivial\n")
        with self.assertRaisesRegex(ValueError, "stale"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_toolchain_change_invalidates_review(self):
        self.write("lean-toolchain", "changed-toolchain\n")
        with self.assertRaisesRegex(ValueError, "stale"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_self_review_rejected(self):
        self.reviewer["identity"] = "test-author"
        self.flush()
        with self.assertRaisesRegex(ValueError, "distinct"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_refreshed_binding_does_not_reuse_old_verdict(self):
        self.record["source_statement"] = "Changed source"
        self.record["binding_sha256"] = publication.binding_digest(self.root, self.record)
        with self.assertRaisesRegex(ValueError, "stale context"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_changed_packet_rejected(self):
        self.write("decoder-packet.txt", "source leaked or context changed\n")
        with self.assertRaisesRegex(ValueError, "packet has changed"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_uninventoried_declaration_rejected(self):
        self.inventory["extra"] = {"source": "QuantumBlockEncoding/Test.lean"}
        with self.assertRaisesRegex(ValueError, "whole changed-module"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_missing_semantic_slot_rejected(self):
        del self.reviewer["semantic_slots"]["ancillas_phases"]
        self.flush()
        with self.assertRaisesRegex(ValueError, "all quantum semantic slots"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_decoder_result_cannot_change_after_review(self):
        self.decoder["reconstruction"] = "A different statement"
        self.write_json("decoder.json", self.decoder)
        with self.assertRaisesRegex(ValueError, "exact decoder result"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_review_result_bytes_are_bound(self):
        self.write("review-artifact.txt", "Changed verdict or reasoning")
        with self.assertRaisesRegex(ValueError, "artifact has changed"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_changed_local_dependency_invalidates_context(self):
        self.write("QuantumBlockEncoding/Other.lean", "def ambient := False")
        with self.assertRaisesRegex(ValueError, "stale"):
            publication.validate_record(self.root, self.record, self.inventory)

    def test_evidence_path_traversal_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-portable"):
            publication.local_file(self.root, "../review.json")


if __name__ == "__main__":
    unittest.main()
