"""Actual-browser acceptance of the source-grounded supplementary workbook."""
import json
from pathlib import Path

from website.scripts.qcb_ecosystem_browser import settle_math
from website.scripts.qcb_math import algebra_spans
from website.scripts.qcb_render_test_support import recover_prose_source
from website.scripts.qcb_workbook_reader import route


def check_workbook(page, base, root, manifest, output):
    from qcb_nonlean_workbook import load_workbook
    workbook = load_workbook()
    output = Path(output)
    if manifest['supplementary_workbook']['workbook_digest'] != workbook['workbook_digest']:
        raise AssertionError('Browser workbook differs from the source-qualified intake.')
    expressions = set()
    for entry in workbook['entries']:
        p = entry['packet']
        texts = [p['question'], p['reference_answer']] + p['assumptions'] + p['conventions']
        texts += [r['criterion'] for r in entry['display_rubric']]
        texts += p['common_errors']
        texts += [str(v) for row in p['boundary_cases'] for v in row.values()]
        m = entry['display_reasoning_map']
        texts += [n['statement'] for n in m['inputs']]
        for n in m['steps']:
            texts += [n['conclusion'], n['justification']] + n.get('assumptions', [])
        expressions.update(s.tex for text in texts for s in algebra_spans(text))
        expressions.update(eq['tex'] for eq in entry['notation']['equations'])
    page.goto(base + 'quantumcomputingbench/non-lean/workbook/index.html', wait_until='networkidle')
    settle_math(page)
    errors = page.evaluate('''xs => xs.flatMap(tex => {
      try { const x=MathJax.tex2mml(tex); return /<merror|data-mjx-error/.test(x) ? [{tex,error:x.slice(0,240)}] : []; }
      catch(e) {return [{tex,error:String(e)}];}
    })''', sorted(expressions))
    if errors:
        raise AssertionError('Supplemental corpus TeX failed: ' + json.dumps(errors[:5]))
    rows = []
    for width in (390, 1280):
        page.set_viewport_size({'width': width, 'height': 1000})
        for theme in ('modern', 'blueprint', 'bold'):
            for entry in workbook['entries']:
                page.goto(base + route(entry) + 'index.html', wait_until='networkidle')
                page.evaluate('t=>document.documentElement.dataset.theme=t', theme)
                settle_math(page)
                if page.locator('.qcb-disclosure[open]').count():
                    raise AssertionError('Supplementary references exposed before attempting the question.')
                actual = recover_prose_source(page.locator('#question').inner_html(), entry['packet']['question'])
                if ' '.join(actual.split()) != ' '.join(entry['packet']['question'].split()):
                    raise AssertionError('Typesetting changed the actual student question.')
                notation = page.locator('#given-notation')
                if entry['notation']['equations']:
                    notation.locator(':scope > summary').focus()
                    page.keyboard.press('Enter')
                    settle_math(page)
                if notation.locator('mjx-container').count() != len(entry['notation']['equations']):
                    raise AssertionError('Given notation did not compile on ' + entry['slot'])
                if not page.locator('[data-qcb-workbook-graph]').count():
                    raise AssertionError('No exact graph anchor on a supplemental exercise.')
                for panel in ('solution', 'rubric', 'reasoning', 'boundaries'):
                    summary = page.locator('#' + panel + ' > summary')
                    summary.focus()
                    page.keyboard.press('Enter')
                    settle_math(page)
                    if page.locator('#' + panel).get_attribute('open') is None:
                        raise AssertionError('Keyboard disclosure failed: ' + panel)
                    if page.evaluate('document.documentElement.scrollWidth>innerWidth+2'):
                        raise AssertionError('Expanded supplemental math overflow: ' + entry['slot'])
                if entry['slot'] == 'A4' and not page.locator('#given-notation mjx-mtable').count():
                    raise AssertionError('The supplied rotation matrix did not render as a matrix.')
                if entry['slot'] in {'A4', 'B2', 'C2'}:
                    page.locator('#given-notation').scroll_into_view_if_needed()
                    page.screenshot(path=str(output / f'workbook-{entry["slot"]}-{width}-{theme}.png'))
                rows.append({'slot': entry['slot'], 'width': width, 'theme': theme,
                             'question_preserved': True, 'given_notation_compiled': True,
                             'references_closed_initially': True, 'expanded_panels_no_overflow': True})
    return {'workbook_digest': workbook['workbook_digest'], 'actual_unique_formulas_compiled': len(expressions),
            'view_checks': rows, 'canonical_admissions_changed': False,
            'scored_training_or_evaluation_rows_added': 0}
