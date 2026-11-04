"""Real-browser acceptance for mathematical rendering and benchmark entry points."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote


def settle_math(page):
    page.wait_for_function('Boolean(window.MathJax?.startup?.promise)', timeout=60000)
    page.evaluate('''async () => {
      await window.MathJax.startup.promise;
      await new Promise(r => setTimeout(r, 40));
      await window.qcbMathReady?.();
    }''')
    errors = page.locator('mjx-merror, [data-mjx-error]').count()
    if errors:
        raise AssertionError('A displayed mathematical expression failed MathJax compilation.')


def check_ecosystem(page, base, root, manifest, output):
    from website.scripts.qcb_math import _QUESTION_COMPANIONS, algebra_spans
    root, output = Path(root), Path(output)
    items = json.loads((root / 'data/quantumcomputingbench/reader-items.json').read_text())['items']
    project = Path(__file__).resolve().parents[2]
    probes = json.loads((project / 'benchmarks/quantumcomputingbench/tracks/lean/learning-validity/v1/cohort.json').read_text())['probes']
    expressions = {s.tex for item in items for key in ('question', 'reference_answer') for s in algebra_spans(item[key])}
    expressions.update(s.tex for p in probes for text in (p['question'], p['gold']['answer']) for s in algebra_spans(text))
    expressions.update(x['tex'] for x in _QUESTION_COMPANIONS.values())
    page.goto(base + 'quantumcomputingbench/run/index.html', wait_until='networkidle')
    settle_math(page)
    failures = page.evaluate('''formulas => formulas.flatMap(tex => {
      try {
        const mml = MathJax.tex2mml(tex);
        return /<merror|data-mjx-error/.test(mml) ? [{tex, error: mml.slice(0, 250)}] : [];
      } catch (e) { return [{tex, error: String(e)}]; }
    })''', sorted(expressions))
    if failures:
        raise AssertionError('Actual corpus TeX compilation failed: ' + json.dumps(failures[:5]))
    # A visibly labeled renderer fixture tests engine features, not model scores.
    shapes = page.evaluate(r'''() => {
      const tex = String.raw`x^{k+1}+\frac{a}{b}+\begin{pmatrix}1&0\\0&1\end{pmatrix}`;
      const out = document.createElement('section');
      out.id = 'qcb-renderer-capability-fixture';
      out.setAttribute('aria-label', 'Synthetic renderer capability fixture');
      out.appendChild(MathJax.tex2chtml(tex)); document.querySelector('main').appendChild(out);
      return {superscript: !!out.querySelector('mjx-msup, msup'),
              fraction: !!out.querySelector('mjx-mfrac, mfrac'), matrix: !!out.querySelector('mjx-mtable, mtable')};
    }''')
    if not all(shapes.values()):
        raise AssertionError('The math engine did not produce actual superscript/fraction/matrix structures.')
    index = json.loads((root / 'data/quantumcomputingbench/expert-index.json').read_text())
    linked = {e['source'] for e in index['structural_edges']} | {e['target'] for e in index['structural_edges']}
    node = next(k for k, v in index['nodes'].items() if k.startswith('declaration:')
                and v.get('live_identity') == 'present_by_exact_id' and k in linked)
    page.goto(base + 'quantumcomputingbench/expert/node/index.html?node=' + quote(node, safe=''), wait_until='networkidle')
    page.wait_for_selector('[data-qcb-expert-result] svg', timeout=15000)
    if not page.locator('[data-qcb-expert-result] a').count():
        raise AssertionError('The focused graph has no actionable question or source links.')
    page.goto(base + 'quantumcomputingbench/expert/nodes/index.html', wait_until='networkidle')
    search = page.locator('[data-qcb-expert-filter] input')
    search.fill('NO_SUCH_EXACT_GRAPH_NODE_20261104')
    if page.locator('[data-qcb-expert-row]:visible').count():
        raise AssertionError('Expert reverse-index search does not filter its actual rows.')
    search.fill('')
    if page.locator('[data-qcb-expert-row]:visible').count() == 0:
        raise AssertionError('Expert reverse-index reset lost every source anchor.')
    samples = []
    for width in (390, 1280):
        page.set_viewport_size({'width': width, 'height': 900})
        for theme in ('modern', 'blueprint', 'bold'):
            for core in ('qcb-core-sp-101', 'qcb-core-la-205', 'qcb-core-sp-009'):
                page.goto(base + 'quantumcomputingbench/cores/' + core + '/index.html', wait_until='networkidle')
                page.evaluate('t => document.documentElement.dataset.theme = t', theme)
                settle_math(page)
                if not page.locator('#question mjx-container').count():
                    raise AssertionError('A representative mathematical question was left uncompiled: ' + core)
                panel = page.locator('#solution')
                panel.locator(':scope > summary').click()
                settle_math(page)
                if page.locator('pre mjx-container, code mjx-container').count():
                    raise AssertionError('Lean/source code was typeset as mathematical prose.')
                if page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'):
                    raise AssertionError('Mathematical question/expanded solution overflow: ' + core)
                page.screenshot(path=str(output / f'math-{core}-{width}-{theme}.png'))
                samples.append({'core_id': core, 'width': width, 'theme': theme, 'compiled_question_and_open_solution': True})
    return {'actual_unique_corpus_formulas_compiled': len(expressions), 'renderer_capability_fixture': shapes,
            'expert_focused_node': node, 'expert_reverse_search_checked': True,
            'representative_math_readability_checks': samples,
            'presentation_digest': manifest['presentation']['digest'], 'runtime_registry_hash': manifest['runtime_registry_hash']}
