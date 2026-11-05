"""Small, task-oriented entry pages; detailed mathematical records stay canonical."""
from __future__ import annotations

import html
from pathlib import PurePosixPath

HUB = 'quantumcomputingbench/'
SECTIONS = (
    ('Overview', '', ()),
    ('Tasks', 'tasks/', ('cores/', 'diagnostics/')),
    ('Run', 'run/', ()),
    ('Results', 'run/results/', ()),
    ('Study & review', 'study/', ('non-lean/', 'lean/', 'course/', 'reasoning/', 'expert/', 'evidence/', 'contribute/')),
)


def esc(value):
    return html.escape(str(value), quote=True)


def local_nav(route):
    """One level of navigation, with correct relative links at arbitrary depth."""
    prefix = '../' * len(PurePosixPath(route).parts)
    child = route.removeprefix(HUB)
    selected = 'Results' if child.startswith('run/results/') else None
    if selected is None:
        selected = next((label for label, path, aliases in SECTIONS
                         if (path and child.startswith(path)) or any(child.startswith(a) for a in aliases)), 'Overview')
    return ('<nav class="qcb-local-nav" aria-label="QuantumComputingBench">'
            + ''.join('<a href="' + prefix + HUB + path + 'index.html"'
                      + (' aria-current="page"' if label == selected else '') + '>' + label + '</a>'
                      for label, path, _ in SECTIONS) + '</nav>')


def card(title, description, href, eyebrow=''):
    return ('<article class="qcb-card">' + ('<p class="eyebrow">' + esc(eyebrow) + '</p>' if eyebrow else '')
            + '<h2><a href="' + esc(href) + '">' + esc(title) + '</a></h2><p>' + esc(description) + '</p></article>')


def overview(intro, catalog, native_lean_count):
    body = intro('QuantumComputingBench', 'Evaluate quantum-computing knowledge, mathematical reasoning and Lean proof skills against a traceable library graph.')
    body += '<div class="qcb-actions"><a class="button" href="run/index.html">Run the benchmark →</a><a class="button secondary" href="tasks/index.html">Explore tasks</a></div>'
    body += '<div class="qcb-grid qcb-capability-paths">'
    body += card('Knowledge & reasoning', 'Answer precise mathematical questions, justify deductions and diagnose missing assumptions.', 'tasks/index.html', 'Natural language')
    body += card('Agentic Lean', 'Work on fixed proof targets, inspect supplied interfaces and compare proof-completion methods.', 'run/agentic-lean/index.html', 'Formal proof')
    body += card('Graph-grounded coverage', 'Locate every task in the source library, from a local interface to a connected argument.', 'expert/index.html', 'For experts')
    body += '</div>'
    body += '<p class="qcb-inventory-line">' + str(len(catalog['cores'])) + ' shared mathematical cores · ' + str(native_lean_count) + ' admitted native Lean views · <a href="study/index.html">Study by subject or difficulty</a></p>'
    body += '<p class="qcb-status-line">Open development edition. Public answers support study and diagnostics; measured model results and a hidden holdout are not yet published. <a href="evidence/index.html">Scope and evidence →</a></p>'
    return body + '</div>'


def publish_navigation(write, intro, catalog, items, registry, course_plan=None):
    """Publish selection pages without changing identities, splits or task payloads."""
    body = intro('Choose a task', 'Start with a subject, then open a topic and one question. Use the same mathematical core for natural-language and formal views.')
    body += '<div class="qcb-grid">'
    for part in catalog['parts']:
        count = sum(c['part'] == part['id'] for c in catalog['cores'])
        body += card(part['title'], str(count) + ' mathematical cores · ' + str(len(part['topics'])) + ' topics', '../non-lean/' + part['id'] + '/index.html')
    body += '</div><div class="qcb-reading-options">'
    body += '<p><a href="../course/index.html">Choose by difficulty: D0–D4</a> · <a href="../lean/index.html">Find available Lean views</a> · <a href="../diagnostics/index.html">Semantic contrasts</a></p>'
    body += '<p><a href="all/index.html">Search all canonical questions</a> · <a href="../non-lean/workbook/index.html">Supplementary mathematics workbook</a></p></div>'
    body += '<p class="qcb-status-line">Planned subject areas are labeled separately. Provisional difficulty describes a supplied route, not measured model performance.</p>'
    write(HUB + 'tasks/', 'Tasks · QuantumComputingBench', body + '</div>', 'Choose a subject, construction level or task mode.')

    body = intro('Search mathematical tasks', 'Filter the canonical questions by subject, split and formal-view availability. Open a row for the full assumptions and question.')
    body += '<p class="qcb-breadcrumb"><a href="../index.html">Choose a task</a> / Search all</p>'
    body += '<form class="qcb-task-filters" data-qcb-task-filters hidden><label>Search questions<input type="search" data-task-query autocomplete="off"></label>'
    body += '<label>Subject<select data-task-part><option value="">All subjects</option>' + ''.join('<option value="' + esc(p['id']) + '">' + esc(p['title']) + '</option>' for p in catalog['parts']) + '</select></label>'
    body += '<label>Split<select data-task-split><option value="">All splits</option>' + ''.join('<option value="' + esc(s) + '">' + esc(s) + '</option>' for s in sorted({c['split'] for c in catalog['cores']})) + '</select></label>'
    body += '<label>Question type<select data-task-kind><option value="">All types</option>' + ''.join('<option value="' + esc(k) + '">' + esc(k.title()) + '</option>' for k in sorted({i['task_kind'] for i in items.values()})) + '</select></label>'
    bands = {e['core_id']: e['difficulty']['construction_band'] for e in (course_plan or {}).get('entries', [])}
    body += '<label>Construction level<select data-task-band><option value="">All levels</option>' + ''.join('<option value="' + esc(b) + '">' + esc(b) + '</option>' for b in sorted(set(bands.values()))) + '<option value="unassigned">Not yet assigned</option></select></label>'
    body += '<label>View<select data-task-view><option value="">All questions</option><option value="lean">Admitted native Lean view</option></select></label><p data-task-count role="status" aria-live="polite"></p></form>'
    body += '<div class="qcb-task-list">'
    for core in catalog['cores']:
        item = items[core['core_id']]
        label = core['core_id'].removeprefix('qcb-core-').upper()
        search = core['core_id'] + ' ' + core['topic'] + ' ' + item['question']
        band = bands.get(core['core_id'], 'unassigned')
        body += '<article class="qcb-task-row" data-task-row data-search="' + esc(search.casefold()) + '" data-part="' + esc(core['part']) + '" data-split="' + esc(core['split']) + '" data-kind="' + esc(item['task_kind']) + '" data-band="' + esc(band) + '" data-lean="' + str('lean' in core['views']).lower() + '">'
        body += '<h2><a href="../../cores/' + esc(core['core_id']) + '/index.html">' + esc(label) + '</a> <span>' + esc(core['topic'].replace('_', ' ').title()) + '</span></h2>'
        # The prompt preview is optional: no hint or gold is smuggled into the browse list.
        body += '<details class="qcb-disclosure"><summary>Preview question</summary><div class="qcb-details-content tex2jax_ignore" data-qcb-math-deferred>' + _prose(item['question']) + '</div></details>'
        body += '<p class="qcb-meta">' + esc(core['split']) + ' · ' + esc(item['task_kind'].replace('_', ' ')) + (' · ' + esc(band) + ' supplied route' if band != 'unassigned' else '') + (' · Lean view available' if 'lean' in core['views'] else '') + '</p></article>'
    body += '</div><p data-task-empty hidden>No matching tasks. Clear a filter to broaden the search.</p><nav class="qcb-pagination" data-task-pages hidden aria-label="Task search pages"><button type="button" data-task-prev>← Previous</button><span data-task-page></span><button type="button" data-task-next>Next →</button></nav><p class="qcb-status-line">Construction levels apply only to annotated supplied routes; unassigned questions are not presumed easier. These are not calibrated model difficulty ratings.</p>'
    write(HUB + 'tasks/all/', 'Search tasks · QuantumComputingBench', body + '</div>', 'Filter canonical mathematical tasks without exposing their answers.')

    body = intro('Study & review', 'Read the mathematics at your own pace, or inspect how a task is grounded in the library.')
    body += '<div class="qcb-grid">'
    body += card('Browse the mathematics', 'Five subject areas, with assumptions, questions and folded solutions.', '../non-lean/index.html')
    body += card('Follow a course', 'D0 statement understanding through D4 connected and parameterized reasoning.', '../course/index.html')
    body += card('Inspect the library graph', 'Exact target and support anchors, source versions and related questions.', '../expert/index.html')
    body += card('Read the Lean companion', 'Available formal targets, supplied proof obligations and reference evidence.', '../lean/index.html')
    body += '</div><p><a href="../reasoning/index.html">How graph relations become reasoning tasks</a> · <a href="../non-lean/workbook/index.html">Supplementary workbook</a></p>'
    body += '<p><a href="../evidence/index.html">Evidence and release readiness</a> · <a href="../contribute/index.html">Contribute a question or formal view</a></p>'
    write(HUB + 'study/', 'Study and review · QuantumComputingBench', body + '</div>', 'Mathematics, difficulty routes and source-grounded expert review.')
    return {'schema_version': 'qcb.reader_hierarchy.v1', 'routes': [HUB + p + 'index.html' for p in ('tasks/', 'tasks/all/', 'study/')], 'canonical_cores': len(catalog['cores'])}


def _prose(text):
    from website.scripts.qcb_math import render_prose
    return render_prose(text)
