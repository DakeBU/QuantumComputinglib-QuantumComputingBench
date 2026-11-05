"""Check actual reading load, task discovery and progressive-disclosure behavior."""
from __future__ import annotations

from website.scripts.qcb_ecosystem_browser import settle_math

HUB = 'quantumcomputingbench/'


def check_hierarchy(page, base, root, manifest, output):
    rows = []
    for width in (390, 1280):
        page.set_viewport_size({'width': width, 'height': 900})
        for route in ('index.html', 'tasks/index.html', 'run/index.html', 'study/index.html', 'course/index.html'):
            page.goto(base + HUB + route, wait_until='networkidle')
            settle_math(page)
            # innerText omits closed details, exactly the text a reader is asked to process.
            words = page.locator('main').inner_text().split()
            if len(words) > 390:
                raise AssertionError(f'Landing reading load exceeds 390 words: {route}: {len(words)}')
            if page.locator('.qcb-local-nav a[aria-current="page"]').count() != 1:
                raise AssertionError('Missing unambiguous local navigation: ' + route)
            if page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'):
                raise AssertionError('Hierarchy landing overflow: ' + route)
            if width == 1280:
                for target in ('lean-graph/', 'functor-hypergraph/'):
                    link = page.locator('.sidebar-primary a[href$="' + target + 'index.html"]')
                    if not link.is_visible():
                        raise AssertionError('Primary graph entry is hidden: ' + target)
            page.screenshot(path=str(output / ('hierarchy-' + route.replace('/', '-') + '-' + str(width) + '.png')))
            rows.append({'route': HUB + route, 'width': width, 'visible_main_words': len(words)})
    page.goto(base + HUB + 'tasks/all/index.html', wait_until='networkidle')
    page.wait_for_selector('[data-qcb-task-filters]:visible')
    if page.locator('[data-task-row]:visible').count() != 15:
        raise AssertionError('Task pagination did not bound the initial reading load.')
    first = page.locator('[data-task-row]:visible h2 a').first.inner_text()
    page.locator('[data-task-next]').click()
    if page.locator('[data-task-row]:visible h2 a').first.inner_text() == first:
        raise AssertionError('Pagination did not change tasks.')
    page.locator('[data-task-view]').select_option('lean')
    if page.locator('[data-task-row]:visible').count() != manifest['admitted_native_lean_views']:
        raise AssertionError('Formal-view filter confused reference courses with canonical admission.')
    page.locator('[data-task-query]').fill('NO_SUCH_QCB_QUESTION_20261105')
    if page.locator('[data-task-row]:visible').count() or not page.locator('[data-task-empty]').is_visible():
        raise AssertionError('Empty task search hides its state or shows irrelevant tasks.')
    page.locator('[data-task-query]').fill('')
    page.locator('[data-task-view]').select_option('')
    page.locator('[data-task-part]').select_option('state-preparation')
    page.locator('[data-task-split]').select_option('test_public')
    page.locator('[data-task-kind]').select_option('proof')
    visible = page.locator('[data-task-row]:visible')
    if not visible.count():
        raise AssertionError('Combined meaningful task filters lost valid tasks.')
    for i in range(visible.count()):
        row = visible.nth(i)
        if (row.get_attribute('data-part'), row.get_attribute('data-split'), row.get_attribute('data-kind')) != ('state-preparation', 'test_public', 'proof'):
            raise AssertionError('Combined filters do not reflect actual rows.')
    preview = visible.first.locator('details > summary')
    preview.focus(); page.keyboard.press('Enter'); settle_math(page)
    if visible.first.locator('details').get_attribute('open') is None:
        raise AssertionError('Question preview is not keyboard accessible.')
    # Direct links must open the chosen dossier without revealing the answer.
    page.goto(base + HUB + 'cores/qcb-core-sp-009/index.html#graph', wait_until='networkidle')
    settle_math(page)
    if not page.locator('#graph[open]').count() or page.locator('#solution[open]').count():
        raise AssertionError('A graph deep link failed or exposed a solution.')
    page.goto(base + HUB + 'run/results/index.html', wait_until='networkidle')
    if not page.locator('[data-qcb-results-status="no_model_results"]').is_visible():
        raise AssertionError('The results page conflates workflow fixtures with measured models.')
    return {'landing_checks': rows, 'task_pagination_and_filters': True, 'graph_deep_link': True,
            'results_evidence_boundary': True, 'canonical_admissions_changed': False}
