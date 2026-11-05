"""Final sidebar contracts: unique destinations, retained content, idempotence."""
import json
import tempfile
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

from website.scripts import build_site, research_atlas
from website.scripts.sidebar_navigation import render_navigation, replace_navigation
from website.scripts import reader_hierarchy

ROOT = Path(__file__).resolve().parents[2]


class NavigationParser(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.open_sections, self.parts = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            self.links.append(attrs)
        if tag == 'details' and 'data-book-part' in attrs:
            self.parts.append(attrs['data-book-part'])
        if tag == 'details' and 'data-nav-section' in attrs and 'open' in attrs:
            self.open_sections.append(attrs['data-nav-section'])


class SidebarNavigationTests(unittest.TestCase):
    def setUp(self):
        self.papers = json.loads((ROOT/'website/papers.json').read_text(encoding='utf-8'))
        self.cases = [
            dict(slug='bell-test', shortTitle='Bell', kind='statePreparation'),
            dict(slug='be-test', shortTitle='BE test', kind='blockEncoding'),
        ]

    def test_each_destination_occurs_once_at_all_depths(self):
        for prefix in ('./', '../', '../../', '../../../'):
            nav = NavigationParser(render_navigation(prefix, 'index.html', self.papers, self.cases))
            duplicates = [href for href, count in Counter(x['href'] for x in nav.links).items() if count > 1]
            self.assertEqual(duplicates, [])
            self.assertEqual(len(nav.parts), 4)
            self.assertEqual(len(set(nav.parts)), 4)

    def test_home_is_compact_and_has_only_one_progress_entry(self):
        text = render_navigation('./', 'index.html', self.papers, self.cases)
        nav = NavigationParser(text)
        self.assertEqual(nav.open_sections, [])
        self.assertNotIn(' open>', text)
        self.assertEqual(text.count('href="./progress/index.html"'), 1)
        self.assertNotIn('href="./roadmap/index.html"', text)

    def test_current_collection_opens_and_exact_page_is_marked(self):
        for route, sections in (('example-cases/bell-test/index.html', ['research', 'examples']),
                                ('library/index.html', ['textbooks']), ('progress/index.html', ['research']),
                                ('community/index.html', ['tools', 'project']), ('papers/index.html', ['research', 'papers']),
                                ('quantumcomputingbench/run/results/index.html', ['quantumcomputingbench']),
                                ('quantumcomputingbench/non-lean/workbook/index.html', ['quantumcomputingbench', 'bench-study'])):
            nav = NavigationParser(render_navigation('../../', route, self.papers, self.cases))
            self.assertEqual(nav.open_sections, sections)
            self.assertEqual(sum(x.get('aria-current') == 'page' for x in nav.links), 1)

    def test_both_graphs_are_primary_and_catalogs_are_one_level_quieter(self):
        text = render_navigation('./', 'index.html', self.papers, self.cases)
        spans = reader_hierarchy.Spans(text)
        primary = spans.one(lambda n: n.has_class('sidebar-primary'))
        for target, label in (('lean-graph/', 'Lean Graph'), ('functor-hypergraph/', 'Functor Hypergraph')):
            graph = spans.one(lambda n: n.tag == 'a' and n.attrs.get('href') == './' + target + 'index.html')
            self.assertGreaterEqual(graph.start, primary.open_end)
            self.assertLessEqual(graph.end, primary.close_start)
            self.assertIn(label, text[graph.start:graph.end])
        root_details = [node for node in spans.nodes if node.tag == 'details' and node.parent is not None and spans.nodes[node.parent].tag == 'nav']
        self.assertEqual(len(root_details), 4)
        self.assertIn('LEAN LIBS &amp; TEXTBOOKS', text)
        for target in ('learning/', 'state-preparation/', 'lean-graph/', 'functor-hypergraph/'):
            nav = NavigationParser(render_navigation('../', target + 'index.html', self.papers, self.cases))
            self.assertEqual(sum(x.get('aria-current') == 'page' for x in nav.links), 1)

    def test_every_guided_chapter_case_and_paper_is_retained(self):
        text = render_navigation('./', 'index.html', self.papers, self.cases)
        for chapter in build_site.CHAPTERS:
            self.assertEqual(text.count(f'./chapters/{chapter["slug"]}/index.html'), 1)
        for case in self.cases:
            self.assertEqual(text.count(f'data-case="{case["slug"]}"'), 1)
        for paper in self.papers['featured'] + self.papers['queue']:
            if paper.get('route'):
                self.assertEqual(text.count(f'./{paper["route"]}index.html'), 1)
        for target in ('library/', 'lean-graph/', 'implementation-map/', 'workflow/', 'ide/', 'blueprint/'):
            self.assertIn(f'href="./{target}index.html"', text)

    def test_legacy_graph_link_label_is_retained_for_published_pages(self):
        text = render_navigation('../../', 'case-studies/robin/index.html', self.papers, self.cases)
        self.assertEqual(text.count('Underlying Lean Graph of Libraries'), 1)
        self.assertIn('href="../../lean-graph/index.html"', text)

    def test_replacement_is_idempotent_and_does_not_touch_body(self):
        page = build_site.site_header('./', '') + '<main><a href="roadmap/">Keep body link</a></main>'
        once = replace_navigation(page, './', 'index.html', self.papers, self.cases)
        self.assertEqual(replace_navigation(once, './', 'index.html', self.papers, self.cases), once)
        self.assertIn('<main><a href="roadmap/">Keep body link</a></main>', once)

    def test_absent_or_duplicate_sidebar_fails_closed(self):
        nav = render_navigation('./', 'index.html', self.papers, self.cases)
        for text in ('<main>No sidebar</main>', nav + nav):
            with self.assertRaisesRegex(ValueError, 'expected one common sidebar'):
                replace_navigation(text, './', 'index.html', self.papers, self.cases)

    def test_actual_final_publisher_is_idempotent_and_skips_blueprint(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'data').mkdir()
            (root/'data/example-cases.json').write_text(json.dumps({'cases':self.cases}), encoding='utf-8')
            (root/'data/papers.json').write_text(json.dumps(self.papers), encoding='utf-8')
            index = root/'index.html'
            index.write_text(build_site.site_header('./', ''), encoding='utf-8')
            (root/'blueprint').mkdir()
            blueprint = root/'blueprint/index.html'
            blueprint.write_text('Blueprint is a separate navigation surface', encoding='utf-8')
            research_atlas.patch_navigation(root)
            first = index.read_bytes()
            research_atlas.patch_navigation(root)
            self.assertEqual(index.read_bytes(), first)
            self.assertEqual(blueprint.read_text(encoding='utf-8'), 'Blueprint is a separate navigation surface')


class ReaderHierarchyTests(unittest.TestCase):
    def test_math_asset_version_binds_actual_script_bytes_without_rewriting_code_samples(self):
        import hashlib
        version = hashlib.sha256((ROOT / 'website/static/math-reader.js').read_bytes()).hexdigest()[:16]
        text = '<html><body><script src="../../static/math-reader.js?v=old"></script><pre>&lt;script src="static/math-reader.js"&gt;</pre></body></html>'
        result = reader_hierarchy.transform_page(text, 'library/modules/fixture/index.html')
        self.assertIn('src="../../static/math-reader.js?v=' + version + '"', result)
        self.assertIn('&lt;script src="static/math-reader.js"&gt;', result)
        self.assertEqual(reader_hierarchy.transform_page(result, 'library/modules/fixture/index.html'), result)

    def page(self, route='index.html'):
        coverage, gate, context = {'publicDeclarationCount': 0, 'sourceDocstringCount': 0}, {'passed': True}, {'shortCommit': 'test'}
        if route == 'index.html':
            return build_site.render_home({'declarations': []}, coverage, gate, context)
        return build_site.render_learning(coverage, gate, context)

    def test_original_home_sections_and_scope_are_preserved_exactly_once(self):
        original = self.page()
        result = reader_hierarchy.transform_page(original, 'index.html')
        before, after = reader_hierarchy.Spans(original), reader_hierarchy.Spans(result)
        for key in ('math-2-0', 'applications', 'state-process', 'block-process', 'evidence', 'pipeline', 'use', 'news', 'chapters', 'navigation'):
            section = before.one(lambda n: n.tag == 'section' and n.attrs.get('id') == key)
            self.assertEqual(result.count(original[section.start:section.end]), 1, key)
            after.one(lambda n: n.attrs.get('id') == key)
        hero = before.one(lambda n: n.has_class('home-hero'))
        hero_nodes = reader_hierarchy.Spans(original[hero.start:hero.end])
        for name in ('hero-scope', 'home-book-links', 'evidence-note'):
            node = hero_nodes.one(lambda n: n.has_class(name))
            self.assertEqual(result.count(hero_nodes.text[node.start:node.end]), 1, name)
        self.assertEqual(reader_hierarchy.transform_page(result, 'index.html'), result)
        self.assertNotIn('startOnLoad: true', result)

    def test_learning_sections_remain_complete_and_closed_until_requested(self):
        original = self.page('learning/index.html')
        result = reader_hierarchy.transform_page(original, 'learning/index.html')
        for section in reader_hierarchy.Spans(original).nodes:
            if section.tag == 'section' and section.attrs.get('id') in ('reading-map', 'chapter-list', 'textbook-explorer', 'future-curriculum'):
                self.assertEqual(result.count(original[section.start:section.end]), 1)
        details = [node for node in reader_hierarchy.Spans(result).nodes if node.has_class('reader-disclosure')]
        self.assertEqual(len(details), 4)
        self.assertTrue(all('open' not in node.attrs for node in details))
        self.assertEqual(reader_hierarchy.transform_page(result, 'learning/index.html'), result)

    def test_exact_benchmark_panel_follows_global_intro_on_republication(self):
        panel = '<!-- qcb-textbook:start --><section id="quantumcomputingbench"><h2>Benchmark</h2><a href="quantumcomputingbench/run/index.html">Run</a></section><!-- qcb-textbook:end -->'
        original = self.page().replace('<main id="main-content">', '<main id="main-content">' + panel, 1)
        result = reader_hierarchy.transform_page(original, 'index.html')
        self.assertEqual(result.count(panel), 1)
        hero = reader_hierarchy.Spans(result).one(lambda n: n.has_class('home-hero'))
        self.assertEqual(result.index(panel), hero.end)
        republished = reader_hierarchy.PANEL.sub('', result).replace('<main id="main-content">', '<main id="main-content">' + panel, 1)
        self.assertEqual(reader_hierarchy.transform_page(republished, 'index.html'), result)

    def test_final_output_publisher_is_idempotent_and_skips_blueprint(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'learning').mkdir()
            (root/'blueprint').mkdir()
            (root/'index.html').write_text(self.page(), encoding='utf-8')
            (root/'learning/index.html').write_text(self.page('learning/index.html'), encoding='utf-8')
            (root/'blueprint/index.html').write_text('Separate Blueprint', encoding='utf-8')
            first_report = reader_hierarchy.publish(root)
            first = {p.relative_to(root): p.read_bytes() for p in root.rglob('*.html')}
            self.assertEqual(reader_hierarchy.publish(root), first_report)
            self.assertEqual({p.relative_to(root): p.read_bytes() for p in root.rglob('*.html')}, first)
            self.assertEqual(first_report['entry_routes'], ['index.html', 'learning/index.html'])
            self.assertEqual((root/'blueprint/index.html').read_text(), 'Separate Blueprint')


if __name__ == '__main__':
    unittest.main()
