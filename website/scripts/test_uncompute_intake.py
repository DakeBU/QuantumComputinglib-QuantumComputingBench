"""A priority intake must not become an unearned local certificate."""
import copy,json,unittest
from pathlib import Path
from website.scripts import research_atlas as atlas
ROOT=Path(__file__).resolve().parents[2]
PIN='64b5a13aa249f1360846657392e6c66817b26d0f'
class UncomputeIntakeTests(unittest.TestCase):
    def setUp(self):self.catalog=atlas.load_catalog()
    def route(self):return next(r for r in self.catalog['wiki']['routes'] if r['id']=='spw-uncompute')
    def test_priority_preserves_no_local_proof_boundary(self):
        route=self.route();self.assertEqual(route['priority'],0);self.assertEqual(route['status'],'research-target')
        self.assertEqual(route['lean_refs'],[]);self.assertEqual(len(route['steps']),7)
        self.assertIn('4.33.0',route['input_model']+' '.join(route['assumptions']))
        self.assertIn('533',route['known_boundary']);self.assertIn('590',route['known_boundary'])
    def test_exact_upstream_pin_and_author_credit(self):
        sources={s['id']:s for s in self.catalog['sources']['sources']}
        source=sources['uncompute-upstream-64b5a13'];self.assertTrue(source['url'].endswith(PIN))
        self.assertIn('4.32.2',source['scope']);self.assertIn('4.33.1',source['scope']);self.assertIn('Apache-2.0',source['scope'])
        self.assertIn('Gu',sources['gu-kemeny-yelin-lukin-2026-uncompute']['authors'])
    def test_retrieval_keeps_card_and_all_no_certificate_status(self):
        packet=atlas.context_packet(self.catalog,route_id='spw-uncompute')
        family=next(f for f in packet['families'] if f['id']=='family:reachable-branch-recovery')
        self.assertEqual(family['technical_card']['lean_decl'],[])
        self.assertEqual(family['technical_card']['lean_status'],'obligation')
        self.assertEqual({s['id'] for s in packet['sources']}.intersection(self.route()['source_ids']),set(self.route()['source_ids']))
    def test_four_reading_depths_are_closed_by_default_markup(self):
        self.assertEqual(len(self.route()['reading_layers']),4)
        source=(ROOT/'website/scripts/research_atlas.py').read_text()
        self.assertIn('data-reading-layer',source);self.assertNotIn('data-reading-layer open',source)
    def test_invalid_reading_layer_cannot_publish(self):
        self.route()['reading_layers'][0]['items']=['']
        with self.assertRaisesRegex(ValueError,'reading layer'):atlas.validate_catalog(self.catalog)
    def test_archived_news_links_real_research_route_and_does_not_announce_completion(self):
        for path in ('PROJECT_GUIDE.md',):
            text=(ROOT/path).read_text();self.assertIn('spw-uncompute/index.html',text);self.assertIn('2610.22367v1',text)
            self.assertIn('work in progress',text.lower())
    def test_actual_home_preserves_the_existing_live_curriculum_label(self):
        from website.scripts.build_site import render_home
        page=render_home({'declarations':[]},{'publicDeclarationCount':0,'sourceDocstringCount':0},
                         {'passed':True},{'shortCommit':'test'})
        self.assertIn('four peer parts',page.casefold())
        self.assertIn('spw-uncompute/index.html',page)
    def test_spbe_evolution_is_planned_and_contract_matched_not_a_certificate(self):
        route=self.route();steps={s['id']:s for s in route['steps']}
        self.assertIn('First research priority',route['goal'])
        self.assertIn('controlled',route['goal'])
        for key in ('function-oracle-spbe','prepare-select-lab'):
            self.assertTrue(steps[key]['target'].startswith('Planned'))
        self.assertIn('success probability',steps['function-oracle-spbe']['acceptance'])
        self.assertIn('unprepare',steps['prepare-select-lab']['acceptance'])
        self.assertIn('operator-norm',' '.join(route['assumptions']))
        self.assertIn('never modify the trusted verifier',' '.join(route['assumptions']))
        self.assertIn('no new best-known circuit is promised',route['target_bound'])
        self.assertIn('not newly certified graph edges',' '.join(route['reading_layers'][2]['items']))
if __name__=='__main__':unittest.main()
