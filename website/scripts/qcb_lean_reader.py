"""A staged Lean reading route over existing, source-bound course companions.

The caller supplies the qualified course plan. This presentation layer never
selects a release, admits a formal view, or creates a new mathematical task.
"""
from __future__ import annotations

from collections import Counter
import html
import re

HUB = "quantumcomputingbench/"
STAGES = (
    ("understand", "Understand the contract", "D0–D1", "Read the objects and assumptions, then connect the conclusion to an available interface.", "D1"),
    ("local", "Build a local proof", "D2", "Work through entries, finite sums, coefficients or a concrete reversible action.", "D2"),
    ("compose", "Compose interfaces", "D3", "Join established ingredients while retaining every required premise.", "D3"),
    ("families", "Control a whole family", "D4", "Use induction, invariants or a global argument for a parameterized target.", "D4"),
)


def esc(value):
    return html.escape(str(value), quote=True)


def fold(title, content, anchor):
    return ('<details class="qcb-disclosure" id="' + esc(anchor) + '"><summary>' + esc(title)
            + '</summary><div class="qcb-details-content tex2jax_ignore" data-qcb-math-deferred>'
            + content + '</div></details>')


def _entries(plan, key, band):
    entries = plan["entries"]
    # D0 reads every existing target. It is not another independent cohort.
    if key != "understand":
        entries = [entry for entry in entries if entry["difficulty"]["construction_band"] == band]
    return sorted(entries, key=lambda entry: (entry["difficulty"]["construction_band"], entry["core_id"]))


def _cards(entries, label, prefix):
    cards = []
    for entry in entries:
        core_id = entry["core_id"]
        target = prefix + esc(core_id) + "/index.html"
        cards.append('<article class="qcb-card" data-qcb-course-core="' + esc(core_id) + '">'
                     '<p class="qcb-meta">' + esc(core_id.removeprefix("qcb-core-").upper()) + ' · '
                     + esc(entry["difficulty"]["construction_band"]) + ' supplied route · ' + esc(entry["split"]) + '</p>'
                     '<h3>' + esc(label(core_id)) + '</h3>'
                     '<p><a href="' + target + '#question">Mathematical question</a> · '
                     '<a href="' + target + '#course">Supplied formal target</a></p></article>')
    return '<div class="qcb-grid">' + ''.join(cards) + '</div>'


def publish_lean_route(write, intro, catalog, plan, label, native_cards, subject_cards):
    entries = plan["entries"]
    core_ids = [entry["core_id"] for entry in entries]
    if len(core_ids) != len(set(core_ids)):
        raise ValueError("Lean reading route requires unique shared course cores")
    by_band = Counter(entry["difficulty"]["construction_band"] for entry in entries)
    native_count = sum("lean" in core["views"] for core in catalog["cores"])
    body = intro("From quantum mathematics to Lean proof", "Understand a target, construct a local proof, compose interfaces, then handle a whole family. Start with the mathematics; formal syntax is optional for reading.")
    body += '<p class="qcb-breadcrumb"><a href="../index.html">QuantumComputingBench</a> / Lean route</p>'
    body += '<p class="qcb-inventory-line" data-qcb-lean-course-count="' + str(len(core_ids)) + '">' + str(len(core_ids)) + ' existing mathematical cores have experimental course companions. Natural-language and formal views keep the same core, family and split.</p>'
    body += '<ol class="qcb-ladder" data-qcb-lean-stages>'
    for key, title, levels, description, band in STAGES:
        count = len(_entries(plan, key, band))
        counting = 'D0 reading facet across all ' + str(count) + ' cores; ' + str(by_band['D1']) + ' D1 routes' if key == 'understand' else str(count) + ' shared cores'
        body += '<li><a href="' + key + '/index.html"><span class="qcb-level">' + levels + '</span><strong>' + title + '</strong></a><p>' + description + '</p><small>' + counting + '</small></li>'
    body += '</ol><p class="qcb-status-line">D0 studies these same questions; it adds no core. D1–D4 describe provisional construction routes, not measured model difficulty.</p>'
    body += '<p>Each question offers a mathematical statement and optional formal obligations on one page. Attempt it before opening the hint, solution or reference proof.</p>'
    body += '<p><a class="button" href="understand/index.html">Start with the contract →</a> <a href="../run/agentic-lean/index.html">Prepare an Agentic Lean evaluation</a></p>'
    body += fold("What is checked?", '<dl class="qcb-legend"><dt>Knowledge</dt><dd>Read definitions, dimensions and assumptions. D0 is a facet of the same mathematical target.</dd><dt>Reasoning</dt><dd>Explain the local argument or interface composition. A checked formal root does not grade every explanatory sentence.</dd><dt>Agentic proof</dt><dd>Compare proof-completion methods under a declared import, feedback and verifier contract. A supplied obligation DAG is not an interactive Lean REPL or extracted proof-term dependency graph.</dd></dl><p>Admitted native views check exact conclusions by library-lemma application. Course companions have bounded authored-reference evidence; they do not automatically become canonical Lean admissions or live model tasks. Trusted reference replay is separate from isolated generated-proof evaluation.</p>', 'scope')
    if native_cards:
        body += fold('Admitted native formal views (' + str(native_count) + ')', native_cards, 'native-views')
    body += fold('Browse by subject', subject_cards, 'subjects')
    body += '<p><a href="warmups/index.html">Three legacy API warmups</a> · <a href="../diagnostics/index.html">Semantic contrasts</a> · <a href="../course/index.html">All course levels</a> · <a href="../evidence/index.html">Evidence details</a></p>'
    write(HUB + 'lean/', 'Lean learning route', body + '</div>', 'A staged route through existing quantum-computing questions and their optional formal companions.')

    routes = [HUB + 'lean/index.html']
    for index, (key, title, levels, description, band) in enumerate(STAGES):
        selected = _entries(plan, key, band)
        body = intro(str(index + 1) + ' · ' + title, description)
        body += '<p class="qcb-breadcrumb"><a href="../index.html">Lean route</a> / ' + levels + '</p>'
        body += '<p class="qcb-status-line">' + ('Read any target below as a D0 knowledge exercise; its displayed D1–D4 band still describes its formal construction route.' if key == 'understand' else 'Provisional ' + band + ' construction routes. Available imports and shortcuts can change solving difficulty.') + '</p>'
        steps = {
            'understand': ('Describe the mathematical objects and requested conclusion.', 'List dimensions, register order, normalization and other premises.', 'Compare the optional formal target with the same mathematical question.'),
            'local': ('Fix the conventions and identify the local identity to establish.', 'Derive the entries, coefficients or basis action before composing them.', 'Check the unchanged target; distinguish a library shortcut from constructing the argument.'),
            'compose': ('Identify the interfaces and their exact input assumptions.', 'Check each branch, then retain all side inputs at every join.', 'Prove the requested root without treating an import or conceptual edge as a theorem.'),
            'families': ('State the parameter, invariant and any base or boundary cases.', 'Keep local interfaces separate from the induction or global argument.', 'Check the quantified root; a finite example does not establish the whole family.'),
        }[key]
        body += '<ol>' + ''.join('<li>' + step + '</li>' for step in steps) + '</ol>'
        if selected:
            first = next((entry for entry in selected if entry['difficulty']['construction_band'] == 'D1'), selected[0]) if key == 'understand' else selected[0]
            body += '<p><a class="button" href="../../cores/' + esc(first['core_id']) + '/index.html">Try one question: ' + esc(label(first['core_id'])) + ' →</a></p>'
        body += fold('Choose a question (' + str(len(selected)) + ' shared cores)', _cards(selected, label, '../../cores/'), 'questions')
        body += fold('Read the supplied proof route', '<p>On a question page, open “Guided course and optional Lean obligations” to inspect exact imports, subgoals, the root and disclosed shortcuts. In supplied-DAG mode, listed AND inputs need accepted evidence before their consumer is checked. Imports can supply additional helpers; this is not an exhaustive mathematical dependency graph.</p><p>The supplied DAG is not an interactive Lean REPL. Whole-root mode can attempt the root directly; supplied-DAG mode also checks and reuses complete intermediate proof blocks. Both see the same decomposition. Reference receipts do not establish measured model performance or isolated execution of arbitrary submissions.</p><p><a href="../../reasoning/index.html">Read the topology guide</a> · <a href="../../run/agentic-lean/index.html">Inspect the evaluation workflow</a></p>', 'proof-route')
        following = STAGES[index + 1] if index + 1 < len(STAGES) else None
        body += '<p><a href="../index.html">All four stages</a>' + (' · <a href="../' + following[0] + '/index.html">Next: ' + following[1] + ' →</a>' if following else ' · <a href="../../run/agentic-lean/index.html">Continue to Agentic Lean evaluation →</a>') + '</p>'
        route = HUB + 'lean/' + key + '/'
        write(route, title + ' · Lean route', body + '</div>', description)
        routes.append(route + 'index.html')
    return {'schema_version': 'qcb.lean_reader_route.v1', 'course_id': plan['course_id'], 'distinct_shared_cores': len(core_ids), 'by_construction_band': dict(sorted(by_band.items())), 'new_mathematical_cores': 0, 'routes': routes}


def check_lean_route(root, manifest, plan):
    summary = manifest.get('lean_learning_route', {})
    counts = Counter(entry['difficulty']['construction_band'] for entry in plan['entries'])
    if (summary.get('course_id') != plan['course_id']
            or summary.get('distinct_shared_cores') != len(plan['entries'])
            or summary.get('new_mathematical_cores') != 0
            or summary.get('by_construction_band') != dict(sorted(counts.items()))):
        raise ValueError('Lean learning route has stale course identity or counts')
    expected_routes = [HUB + 'lean/index.html'] + [HUB + 'lean/' + key + '/index.html' for key, *_ in STAGES]
    if summary.get('routes') != expected_routes:
        raise ValueError('Lean learning route lost a stage')
    for key, _, _, _, band in STAGES:
        page = (root / HUB / 'lean' / key / 'index.html').read_text(encoding='utf-8')
        cards = re.findall(r'data-qcb-course-core="([^"]+)"', page)
        expected = [entry['core_id'] for entry in _entries(plan, key, band)]
        if cards != expected:
            raise ValueError('Lean stage does not project its exact shared course cores: ' + key)
