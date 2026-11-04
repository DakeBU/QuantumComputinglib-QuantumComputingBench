"""Shared-core, semantic binding, safe renderer and preview/stable regressions."""
import importlib.util
import sys
import tempfile
import unittest
import urllib.error
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "benchmarks/quantumcomputingbench/src"))

import qcb_curriculum as shared
from qcb_core import write_json

from website.scripts import quantumcomputingbench as reader
from website.scripts.sidebar_navigation import render_navigation
from website.scripts.test_sidebar_navigation import NavigationParser


class CurriculumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.items, cls.graph = shared.load_catalog()

    def proposal(self, track="lean"):
        c = self.catalog["cores"][0]
        return {"proposal_id": str(uuid4()), "track": track, "author": "test-author",
                "source_nodes": c["target_nodes"], "view_kind": "proof",
                **{k: c[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")}}

    def test_one_core_one_home_and_same_registry_for_both_tracks(self):
        expected = 213 - sum(r["status"].startswith("withheld_") for r in self.catalog["reader_decisions"])
        self.assertEqual(len(self.catalog["cores"]), expected)
        self.assertEqual(len(self.items), expected)
        self.assertEqual(len(self.catalog["parts"]), 5)
        self.assertEqual(len({c["core_id"] for c in self.catalog["cores"]}), expected)
        self.assertEqual({c["topic"] for c in self.catalog["cores"]},
                         {t for p in self.catalog["parts"] for t in p["topics"]})
        self.assertTrue(all("non-lean" in c["views"] and set(c["views"]) <= {"non-lean", "lean"} for c in self.catalog["cores"]))
        self.assertEqual(sum("lean" in c["views"] for c in self.catalog["cores"]),
                         self.catalog["native_formal_view_admission"].get("admitted_views", 0))

    def test_compatible_tracks_do_not_admit_another_core(self):
        result = shared.validate_proposals(self.catalog, [self.proposal(), self.proposal("non-lean")])
        self.assertEqual(result["new_cores_admitted"], 0)
        self.assertFalse(result["distributed_lock_claimed"])

    def test_course_is_a_separate_projection_with_complete_obligation_maps(self):
        before = deepcopy(self.catalog)
        plan, views, report = reader.course_reader()
        course_ids = {e['core_id'] for e in plan['entries']}
        self.assertEqual(set(reader.COURSE_LABELS), {c.removeprefix('qcb-core-') for c in course_ids})
        self.assertEqual(report['new_mathematical_cores'], 0)
        self.assertTrue({c['core_id'] for c in self.catalog['cores'] if 'lean' in c['views']} <= course_ids)
        for entry in plan['entries']:
            core = next(c for c in self.catalog['cores'] if c['core_id'] == entry['core_id'])
            body = reader.course_panel(core, '../../../')
            for node in views[entry['view_id']]['task']['nodes']:
                self.assertIn(reader.esc(node['target']), body)
            self.assertIn(reader.esc(entry['difficulty']['imported_shortcut']), body)
            self.assertIn('not extracted Lean proof-term dependencies', body)
        self.assertEqual(self.catalog, before)

    def test_course_levels_link_existing_cores_and_keep_d0_a_facet(self):
        plan, views, report = reader.course_reader()
        pages = {}
        def write(route, title, body, description):
            pages[route] = body
        def intro(title, description):
            return '<div class="qcb-reader"><h1>' + reader.esc(title) + '</h1>'
        reader.publish_course(write, intro, plan, views, report)
        for band in reader.COURSE_BANDS:
            page = pages[reader.HUB + 'course/' + band.lower() + '/']
            expected = plan['entries'] if band == 'D0' else [e for e in plan['entries'] if e['difficulty']['construction_band'] == band]
            parsed = NavigationParser(page)
            linked = {a['href'].split('/cores/')[1].split('/')[0] for a in parsed.links if '/cores/' in a['href']}
            self.assertEqual(linked, {e['core_id'] for e in expected})
        guide = pages[reader.HUB + 'reasoning/']
        for core in ('sp-009', 'be-111', 'be-106', 'sp-104'):
            self.assertIn('/cores/qcb-core-' + core + '/index.html', guide)
        for side_input in ('coprime', 'product degree', 'degree-to-vanishing'):
            self.assertIn(side_input, guide)

    def test_public_agent_identity_projection_is_lossless_and_internal_registry_unchanged(self):
        original = {"catalog_hash": "internal-binding", "cores": [
            {"author_identity": "/root/qcb_native_comparison", "core_id": "fixture"},
            {"author_identity": "human-reviewer"}], "withheld_cores": [{"author_identity": "/root"}]}
        before = deepcopy(original)
        public = reader.public_catalog(original)
        self.assertEqual(original, before)
        self.assertEqual(public["catalog_hash"], original["catalog_hash"])
        for collection in ("cores", "withheld_cores"):
            for source, displayed in zip(original[collection], public[collection]):
                identity = displayed["author_identity"]
                restored = "/" + identity.removeprefix("agent-task:") if identity.startswith("agent-task:") else identity
                self.assertEqual(restored, source["author_identity"])
        self.assertEqual(public["public_projection"]["catalog_hash_binds"], "unmodified_internal_registry")

    def test_public_identity_projection_keeps_real_path_leak_check_fail_closed(self):
        path = reader.ROOT / "scripts/sanitize-blueprint-paths.py"
        spec = importlib.util.spec_from_file_location("qcb_test_path_scanner", path)
        scanner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scanner)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            safe = {"cores": [{"author_identity": "/root/qcb_native_comparison"}]}
            write_json(output / "cores.json", reader.public_catalog(safe))
            self.assertEqual(scanner._assert_no_local_paths(output, reader.ROOT), 1)
            for unsafe in (
                {"cores": [{"author_identity": "/home/private/reviewer"}]},
                {"cores": [{"author_identity": "/root/qcb_native_comparison", "question": "/root/private/source.lean"}]},
            ):
                write_json(output / "cores.json", reader.public_catalog(unsafe))
                with self.assertRaises(ValueError):
                    scanner._assert_no_local_paths(output, reader.ROOT)

    def test_withheld_core_identity_and_split_remain_reserved(self):
        self.assertTrue(self.catalog["withheld_cores"])
        for core in self.catalog["withheld_cores"]:
            p = self.proposal()
            p.update({k: core[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")})
            p["source_nodes"] = core["target_nodes"]
            self.assertEqual(shared.validate_proposals(self.catalog, [p])["new_cores_admitted"], 0)
            p["split"] = "other"
            with self.assertRaisesRegex(ValueError, "contract/family/split"):
                shared.validate_proposals(self.catalog, [p])

    def test_withdrawal_cannot_shrink_stable_review_obligation(self):
        result = shared.stable_readiness(self.catalog)
        withheld = {c["core_id"] for c in self.catalog["withheld_cores"]}
        self.assertEqual(result["required_core_reviews"], self.catalog["historical_native_core_count"])
        self.assertTrue(withheld <= set(result["pending_core_ids"]))
        self.assertEqual(set(result["withheld_core_ids"]), withheld)
        self.assertFalse(result["gates"]["reader_withdrawals_resolved"])
        reduced = deepcopy(self.catalog)
        reduced["cores"].pop()
        with self.assertRaisesRegex(ValueError, "historical core obligation"):
            shared.stable_readiness(reduced)

    def test_existing_contract_and_split_mutations_fail(self):
        for key in ("contract_hash", "family", "split", "snapshot_id"):
            p = self.proposal()
            p[key] = "changed"
            with self.assertRaisesRegex(ValueError, "contract/family/split"):
                shared.validate_proposals(self.catalog, [p])

    def test_duplicate_views_and_proposal_ids_fail(self):
        p = self.proposal()
        for q in (dict(p), {**p, "proposal_id": str(uuid4())}):
            with self.assertRaises(ValueError):
                shared.validate_proposals(self.catalog, [p, q])

    def test_question_successor_exposes_revision_and_rejects_stale_companion(self):
        revised = [c for c in self.catalog["cores"] if c.get("question_successor")]
        self.assertTrue(revised)
        for c in revised:
            with self.subTest(core=c["core_id"]):
                p = self.proposal()
                p.update({k: c[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")})
                self.assertEqual(shared.validate_proposals(self.catalog, [p])["new_cores_admitted"], 0)
                p["contract_hash"] = c["question_successor"]["predecessor_contract_hash"]
                with self.assertRaisesRegex(ValueError, "contract/family/split"):
                    shared.validate_proposals(self.catalog, [p])
                self.assertEqual(c["question_source_record"], c["answer_source_record"])
                self.assertEqual(c["question_version"], 2)
                body = reader.core_body(c, self.items[c["core_id"]], self.catalog, self.graph, set(self.graph), "../../../")
                self.assertIn('data-qcb-question-version="2"', body)
                self.assertIn("Question revision lineage", body)
                self.assertIn(c["question_successor"]["predecessor_contract_hash"], body)
                self.assertIn(c["contract_hash"], body)
                self.assertNotIn("Additive answer successor with", body)

    def test_exact_predecessor_acceptance_remains_history_not_new_question_approval(self):
        c = next(c for c in self.catalog["cores"] if c.get("question_successor"))
        decision = next(d for d in self.catalog['reader_decisions'] if d['core_id'] == c['core_id'])
        from qcb_core import read_json
        packet = read_json(shared.B / decision['prior_withdrawal']['review'])
        finding = next(r for r in packet['items'] if r['core_id'] == c['core_id'])
        finding['verdict'], finding['semantic_core_verdict'] = 'accept', 'distinct_or_explicit_alias'
        packet['items'] = [finding]
        with tempfile.TemporaryDirectory() as tmp, patch.object(shared, 'B', Path(tmp)):
            write_json(Path(tmp) / 'reports/textbook-v1/reader-reviews/old-positive.json', packet)
            unapproved = deepcopy(self.catalog)
            current = next(r for r in unapproved['cores'] if r['core_id'] == c['core_id'])
            current['question_successor'] = None
            accepted, disputed = shared.content_review_status(unapproved)
            self.assertNotIn(c['core_id'], accepted)
            self.assertNotIn(c['core_id'], disputed)

    def test_current_conventions_are_separate_from_historical_audit(self):
        revisions = [c for c in self.catalog['cores']
                     if 'conventions' in (c.get('question_successor') or {}).get('changed_contract_fields', [])]
        self.assertTrue(revisions, 'the admitted convention migration must have a renderer regression')
        for core in revisions:
            item, lineage = self.items[core['core_id']], core['question_successor']
            body = reader.core_body(core, item, self.catalog, self.graph, set(self.graph), '../../../')
            active = body.split('id="assumptions"', 1)[1].split('</section>', 1)[0]
            self.assertIn('data-qcb-convention-revision="2"', body)
            self.assertIn('Historical conventions (audit only)', body)
            self.assertIn('Current conventions', body)
            for text in lineage['current_conventions']:
                self.assertIn(reader.esc(text), active)
            for text in lineage['original_conventions']:
                self.assertIn(reader.esc(text), body.split('id="revision"', 1)[1])
                if text not in lineage['current_conventions']:
                    self.assertNotIn(reader.esc(text), active)
            proposal = self.proposal()
            proposal.update({k: core[k] for k in ('core_id', 'contract_hash', 'family', 'split', 'snapshot_id')})
            proposal['source_nodes'] = core['target_nodes']
            shared.validate_proposals(self.catalog, [proposal])
            proposal['contract_hash'] = lineage['predecessor_contract_hash']
            with self.assertRaisesRegex(ValueError, 'contract/family/split'):
                shared.validate_proposals(self.catalog, [proposal])

    def test_convention_migration_requires_its_actual_browser_gate(self):
        self.assertTrue(any('conventions' in (c.get('question_successor') or {}).get('changed_contract_fields', [])
                            for c in self.catalog['cores']))
        browser = {'catalog_hash': self.catalog['catalog_hash'],
                   'reader_source_digest': shared.reader_source_digest(), 'failures': [],
                   'all_core_mobile_checks': len(self.catalog['cores']),
                   'checks': {key: True for key in ('mobile_no_overflow', 'desktop_no_overflow', 'themes',
                       'solution_disclosure', 'graph_links', 'search_excludes_answers', 'native_formal_panels',
                       'quarantined_content_excluded', 'question_revision_lineage')}}
        actual_read = shared.read_json
        actual_is_file = Path.is_file
        with patch.object(shared, 'read_json', side_effect=lambda path:
                browser if Path(path).name == 'browser-report.json' else actual_read(path)), \
                patch.object(Path, 'is_file', lambda path:
                    path.name == 'browser-report.json' or actual_is_file(path)):
            self.assertFalse(shared.stable_readiness(self.catalog)['gates']['rendered_browser_checks'])
            browser['checks']['convention_revision_lineage'] = True
            result = shared.stable_readiness(self.catalog)
            self.assertTrue(result['gates']['rendered_browser_checks'])
            self.assertFalse(result['stable'])
            self.assertFalse(result['gates']['cross_cohort_semantic_reconciliation'])

    def test_candidate_never_self_admits_or_allocates_permanent_core(self):
        p = self.proposal()
        p.update(core_id="candidate:" + p["proposal_id"], admission="candidate_not_counted", dedup_review_required=True)
        self.assertEqual(shared.validate_proposals(self.catalog, [p])["new_cores_admitted"], 0)
        for changes in ({"core_id": "qcb-core-new-999"}, {"admission": "gold"}, {"proposal_id": "aaaaaaaa-aaaaaaaa-aaaaaaaa-aaaaaaaaaa"}):
            with self.assertRaises(ValueError):
                shared.validate_proposals(self.catalog, [{**p, **changes}])

    def test_preview_cannot_be_promoted_by_renaming(self):
        c = deepcopy(self.catalog)
        c["version"] = "v1.0.0"
        result = shared.stable_readiness(c)
        self.assertFalse(result["stable"])
        self.assertGreaterEqual(result["content_bound_second_pass_reviews"], 4)
        self.assertFalse(result["gates"]["cross_cohort_semantic_reconciliation"])

    def test_stale_self_and_conflicting_reviews_fail_closed(self):
        core = self.catalog["cores"][0]
        packet = {"reviewer": "independent-test-reader", "method": "independent-mathematical-reader-review", "items": [{
            "core_id": core["core_id"], "item_digest": core["item_digest"], "verdict": "accept",
            "semantic_core_verdict": "distinct_or_explicit_alias", "reasoning": "Test fixture only.",
            "source_checks": [{"file": "QuantumBlockEncoding/StatePreparation.lean", "sha256_lf": reader.text_sha(reader.ROOT / "QuantumBlockEncoding/StatePreparation.lean")}]}]}
        with tempfile.TemporaryDirectory() as tmp, patch.object(shared, "B", Path(tmp)):
            baseline = sum(bool(c.get("textbook_successor") or c.get("question_successor")) for c in self.catalog["cores"])
            path = Path(tmp) / "reports/textbook-v1/reader-reviews/a.json"
            write_json(path, packet)
            self.assertEqual(shared.stable_readiness(self.catalog)["content_bound_second_pass_reviews"], baseline + 1)
            rejected = deepcopy(packet)
            rejected["reviewer"] = "other-test-reader"
            rejected["items"][0]["verdict"] = "uncertain"
            write_json(path.with_name("b.json"), rejected)
            self.assertEqual(shared.stable_readiness(self.catalog)["content_bound_second_pass_reviews"], baseline)
            packet["reviewer"] = core["author_identity"]
            write_json(path, packet)
            with self.assertRaisesRegex(ValueError, "self-certify"):
                shared.stable_readiness(self.catalog)
            packet["reviewer"] = "independent-test-reader"
            packet["items"][0]["item_digest"] = "stale"
            write_json(path, packet)
            with self.assertRaisesRegex(ValueError, "current mathematical content"):
                shared.stable_readiness(self.catalog)

    def test_renderer_preserves_exact_reviewed_content_and_folds_answers(self):
        c = self.catalog["cores"][0]
        i = self.items[c["core_id"]]
        body = reader.core_body(c, i, self.catalog, self.graph, set(self.graph), "../../../")
        from website.scripts.qcb_render_test_support import recover_prose_source
        self.assertEqual(recover_prose_source(body, i["question"]), i["question"])
        self.assertEqual(recover_prose_source(body, i["reference_answer"]), i["reference_answer"])
        self.assertIn('id="solution"', body)
        self.assertNotIn(' open', body)
        self.assertLess(body.index('id="assumptions"'), body.index('id="question"'))
        self.assertIn("No aligned Lean view has been admitted", body)
        self.assertNotIn(reader.esc(c["title"]), body.split('id="hint"')[0])
        cards = reader.exercise_cards([c], "../../../", self.items)
        self.assertNotIn(reader.esc(c["title"]), cards)
        self.assertNotIn(reader.esc(i["reference_answer"]), cards)

    def test_html_and_source_url_injection_are_not_executable(self):
        self.assertNotIn("<script>", reader.prose('<script>alert(1)</script>'))
        body = reader.source_list({"source_refs": [{"path": "../../evil", "anchor": '<img onerror="x">'}],
                                   "primary_sources": [{"url": "javascript:alert(1)", "title": "bad"}]})
        self.assertNotIn('href="javascript:', body)
        self.assertNotIn("<img", body)
        self.assertNotIn("/blob/", body)

    def test_native_formal_panel_exposes_exact_target_not_kernel_certified_prose(self):
        rows = [c for c in self.catalog["cores"] if "lean" in c["views"]]
        for core in rows:
            view = core["views"]["lean"]
            body = reader.core_body(core, self.items[core["core_id"]], self.catalog, self.graph, set(self.graph), "../../../")
            self.assertIn(reader.esc(view["formal_context"]["target"]), body)
            self.assertIn(reader.esc(view["reference_proof"]), body)
            self.assertIn("kernel does not certify every sentence", body)
            self.assertNotIn("No aligned Lean view has been admitted", body)
            self.assertIn("#lean", reader.exercise_cards([core], "../../../", self.items, "lean"))

    def test_formal_diagnostics_bind_exact_records_not_native_alias_guesses(self):
        warmups = reader.formal_warmups()
        self.assertEqual(len(warmups), 3)
        self.assertTrue(all(r["verdict"] == "accept" for _, r in warmups))
        self.assertTrue(all(i["formal"]["target"] == r["formal_target"] for i, r in warmups))

    def test_repaired_answer_keeps_core_contract_and_split_without_old_acceptance_transfer(self):
        from qcb_textbook_policy import (
            apply_current_reader_policy,
            frozen_native_is_current,
        )
        _, _, originals, _ = shared.preview.checked()
        current, decisions = apply_current_reader_policy(originals)
        old = next(i for i in originals if i["core_id"] == "qcb-core-sp-002")
        successor = next((i for i in current if i["core_id"] == old["core_id"]), None)
        self.assertFalse(frozen_native_is_current(originals))
        if successor is not None:
            self.assertEqual(shared.core_contract(old), shared.core_contract(successor))
            self.assertNotEqual(old["id"], successor["id"])
            self.assertNotEqual(old["reference_answer"], successor["reference_answer"])
            self.assertEqual(successor["reviews"][0]["method"], "independent-answer-successor-review")
            self.assertIn("inherited_predecessor_reviews", successor)
        else:
            self.assertEqual(decisions[0]["status"], "withheld_pending_distinct_repair_review")

    def test_bench_navigation_does_not_replace_the_four_existing_textbooks(self):
        from qcb_core import read_json
        papers = read_json(reader.ROOT / "website/papers.json")
        parsed = NavigationParser(render_navigation("../../", "quantumcomputingbench/lean/index.html", papers, []))
        self.assertEqual(len(parsed.parts), 4)
        self.assertEqual(parsed.open_sections, ["quantumcomputingbench"])
        self.assertEqual(sum(a.get("aria-current") == "page" for a in parsed.links), 1)
        self.assertEqual(len(parsed.links), len({a["href"] for a in parsed.links}))

    def test_full_publisher_is_idempotent_and_search_contains_questions_not_solutions(self):
        from qcb_core import read_json

        from website.scripts import build_site
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "static").mkdir()
            graph_path = root / "data/lean-graph.json"
            write_json(graph_path, {"nodes": list(self.graph.values())})
            graph_bytes = graph_path.read_bytes()
            report = {"coverage": {"publicDeclarationCount": 1}, "searchEntryCount": 0,
                      "leanGate": {"passed": True, "commit": "UNIT-TEST-FIXTURE-NOT-EXECUTION"}}
            for filename in ("build-report.json", "site-metadata.json"):
                write_json(root / filename, report)
            write_json(root / "search-index.json", {"entries": [], "entryCount": 0, "pageEntryCount": 0})
            write_json(root / "data/example-cases.json", {"cases": []})
            write_json(root / "data/papers.json", read_json(reader.ROOT / "website/papers.json"))
            (root / "index.html").write_text(build_site.site_header("./", "") + '<main id="main-content"></main>', encoding="utf-8")
            with patch.object(build_site, "git_context", return_value={"commit": "UNIT-TEST-FIXTURE-NOT-EXECUTION", "shortCommit": "fixture"}):
                first = reader.publish(root)
                before = (root / "search-index.json").read_bytes()
                reader.publish(root)
            self.assertGreater(first["pages"], 260)
            self.assertEqual(graph_path.read_bytes(), graph_bytes)
            self.assertEqual((root / "search-index.json").read_bytes(), before)
            self.assertTrue(reader.check_site(root)["question_only_search"])
            for core in self.catalog["withheld_cores"]:
                notice = (root / reader.HUB / "cores" / core["core_id"] / "index.html").read_text(encoding="utf-8")
                self.assertIn("data-qcb-withheld", notice)
                self.assertNotIn('id="solution"', notice)
                self.assertNotIn('id="hint"', notice)
            exported = read_json(root / "data/quantumcomputingbench/reader-items.json")["items"]
            self.assertFalse({c["core_id"] for c in self.catalog["withheld_cores"]} & {i["core_id"] for i in exported})
            export_path = root / "data/quantumcomputingbench/reader-items.json"
            tampered = read_json(export_path)
            tampered["items"][0]["reference_answer"] = "An unreviewed replacement answer."
            write_json(export_path, tampered)
            with self.assertRaisesRegex(ValueError, "exact reviewed content"):
                reader.check_site(root)
            text = (root / "index.html").read_text(encoding="utf-8")
            self.assertEqual(text.count('id="quantumcomputingbench"'), 1)

    def test_transport_retry_never_retries_rejected_origins_or_not_found(self):
        from unittest.mock import MagicMock

        from website.scripts import restore_published_blueprint as restore
        response = MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = restore.ORIGIN + "fixture"
        response.read.return_value = b"fixture"
        with patch.object(restore.urllib.request, "urlopen", side_effect=[OSError("TLS interrupted"), response]) as get, patch.object(restore.time, "sleep"):
            self.assertEqual(restore.resource(restore.ORIGIN + "fixture"), b"fixture")
            self.assertEqual(get.call_count, 2)
        with patch.object(restore.urllib.request, "urlopen", side_effect=urllib.error.HTTPError("fixture", 404, "missing", {}, None)) as get:
            with self.assertRaises(urllib.error.HTTPError):
                restore.resource(restore.ORIGIN + "fixture")
            self.assertEqual(get.call_count, 1)
        response.geturl.return_value = "https://unapproved.invalid/"
        with patch.object(restore.urllib.request, "urlopen", return_value=response) as get:
            with self.assertRaisesRegex(ValueError, "approved origin"):
                restore.resource(restore.ORIGIN + "fixture")
            self.assertEqual(get.call_count, 1)


if __name__ == "__main__":
    unittest.main()
