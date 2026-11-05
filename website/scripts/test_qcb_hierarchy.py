"""Reader navigation must not invent tasks, labels, admissions or model results."""
import unittest
from html.parser import HTMLParser

from website.scripts import qcb_benchmark_center as center
from website.scripts import qcb_navigation as nav


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs))


class HierarchyTests(unittest.TestCase):
    def test_nested_navigation_preserves_relative_depth_and_one_selection(self):
        for path, active in (('', 'index.html'), ('tasks/all/', 'tasks/index.html'),
                             ('run/evaluation/review/', 'run/index.html'),
                             ('run/results/', 'run/results/index.html'),
                             ('cores/core-1/', 'tasks/index.html'),
                             ('non-lean/workbook/a1/', 'study/index.html')):
            route = nav.HUB + path
            links = Links(nav.local_nav(route)).links
            selected = [link for link in links if link.get('aria-current') == 'page']
            self.assertEqual(len(selected), 1)
            prefix = '../' * len(nav.PurePosixPath(route).parts)
            self.assertEqual(selected[0]['href'], prefix + nav.HUB + active)

    def test_search_projection_contains_only_existing_questions_and_admissions(self):
        parts = [{'id': 'foundations', 'title': 'Foundations', 'topics': ['algebra']}]
        core = {'core_id': 'core-1', 'topic': 'algebra', 'part': 'foundations',
                'split': 'test_public', 'views': {'non-lean': {}, 'lean': {}}}
        item = {'question': 'Prove the requested <statement>.', 'task_kind': 'proof',
                'reference_answer': 'SECRET reference answer'}
        pages = {}
        nav.publish_navigation(lambda route, title, body, desc: pages.update({route: body}),
                               lambda title, deck: '<div>' + title + deck,
                               {'parts': parts, 'cores': [core]}, {'core-1': item}, {})
        listing = pages[nav.HUB + 'tasks/all/']
        self.assertEqual(listing.count('data-task-row '), 1)
        self.assertIn('data-lean="true"', listing)
        self.assertIn('Prove the requested &lt;statement&gt;.', listing)
        self.assertNotIn('SECRET', ''.join(pages.values()))

    def test_results_do_not_turn_author_fixtures_into_a_model_score(self):
        pages = {}
        report = center.publish_center(lambda route, title, body, desc: pages.update({route: body}),
            lambda title, deck: '<div>' + title + deck, {'cores': [{}]},
            {'tasks': [{'track': 'lean', 'split': 'dev'}]}, 'a' * 40, {'passed': True})
        result = pages[nav.HUB + 'run/results/']
        self.assertIn('data-qcb-results-status="no_model_results"', result)
        self.assertIn('No measured model leaderboard', result)
        self.assertNotIn('<table', result)
        lean = pages[nav.HUB + 'run/agentic-lean/']
        self.assertIn('--exposure approved_interface', lean)
        self.assertIn('does not run a model or execute submitted proofs', lean)
        self.assertEqual(set(report['routes']), {route + 'index.html' for route in pages})


if __name__ == '__main__':
    unittest.main()
