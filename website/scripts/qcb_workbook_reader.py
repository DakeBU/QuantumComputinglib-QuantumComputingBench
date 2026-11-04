"""Publish supplemental source-grounded NL mathematics in the shared reader."""
from __future__ import annotations

import hashlib
import html
from collections import defaultdict
from pathlib import PurePosixPath
from urllib.parse import quote

from website.scripts.qcb_math import render_prose

HUB = 'quantumcomputingbench/'
BASE = HUB + 'non-lean/workbook/'
REPO = 'https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench'
READING_LINKS = {
    'A2': (('A3', 'Apply the explicitly supplied stability interface to an accepted quantum branch.'),
           ('C4', 'Apply the same explicitly supplied interface to perturbed polynomial samples.')),
    'A3': (('A2', 'The stability result is supplied here; A2 asks for its derivation and domain boundary.'),),
    'A4': (('B3', 'Use this rotation-distance interface, supplied in B3, in a precision-allocation problem.'),),
    'B3': (('A4', 'The exact rotation-distance result is supplied here; A4 asks for its derivation.'),),
    'C4': (('A2', 'The stability result is supplied here; A2 derives it independently of polynomial sampling.'),),
}


def esc(v):
    return html.escape(str(v), quote=True)


def section(title, content, anchor):
    return '<section class="qcb-section" id="' + esc(anchor) + '"><h2>' + esc(title) + '</h2>' + content + '</section>'


def folded(title, content, anchor):
    return ('<details class="qcb-disclosure" id="' + esc(anchor) + '"><summary>' + esc(title)
            + '</summary><div class="qcb-details-content tex2jax_ignore" data-qcb-math-deferred>' + content + '</div></details>')


def prose_list(values):
    return '<ul>' + ''.join('<li>' + render_prose(v) + '</li>' for v in values) + '</ul>'


def route(entry):
    return BASE + entry['slot'].lower() + '/'


def node_anchor(node):
    return 'node-' + hashlib.sha256(node.encode()).hexdigest()[:16]


def graph_location(packet, graph, live_ids, prefix):
    out = '<p>Exact frozen graph anchors. Target and support roles describe this exercise; they do not certify an extracted proof dependency.</p><ul>'
    for field, role in (('target_nodes', 'Target'), ('supporting_nodes', 'Support')):
        for node in packet[field]:
            label = graph[node].get('label', node)
            href = (prefix + 'lean-graph/index.html?focus=' + quote(node, safe='') if node in live_ids
                    else prefix + BASE + 'graph/index.html#' + node_anchor(node))
            out += '<li><strong>' + role + ':</strong> <a data-qcb-workbook-graph href="' + esc(href) + '">' + esc(label) + '</a>'
            out += ' <small>(' + ('current exact ID' if node in live_ids else 'frozen snapshot only') + ')</small></li>'
    return out + '</ul><p><a href="' + prefix + BASE + 'graph/index.html">Find the other exercises using these nodes</a></p>'


def cards(entries, prefix):
    result = '<div class="qcb-grid">'
    for e in entries:
        p = e['packet']
        status = ('Additional exposition of ' + p['core_id'].removeprefix('qcb-core-').upper()
                  if p['contribution_type'] == 'existing_core_view' else 'Unassigned supplementary candidate')
        result += ('<article class="qcb-card"><p class="qcb-meta">' + esc(e['band']) + ' · ' + esc(status)
                   + '</p><h3><a href="' + prefix + route(e) + 'index.html">' + esc(p['title'])
                   + '</a></h3>' + render_prose(p['mathematical_target']) + '</article>')
    return result + '</div>'


def reasoning_map(entry):
    m = entry['display_reasoning_map']
    out = '<p>This is an author-supplied mathematical reasoning route, not extracted Lean proof dependencies. Every listed input of a step is required together; boundary diagnostics can replace assumptions only in their stated scope.</p>'
    out += '<h3>Inputs and conventions</h3><dl>'
    for n in m['inputs']:
        out += '<dt><code>' + esc(n['id']) + '</code> · ' + esc(n.get('kind', 'input')) + '</dt><dd>' + render_prose(n['statement']) + '</dd>'
    out += '</dl><h3>Reasoning steps</h3><ol class="qcb-workbook-steps">'
    for n in m['steps']:
        out += '<li id="step-' + esc(n['id']) + '"><h4>' + esc(n['id']) + ': ' + esc(n['claim']) + '</h4>'
        out += '<p class="qcb-meta">All required inputs: ' + esc(', '.join(n['required_inputs'])) + '</p>'
        out += prose_list(n.get('assumptions', [])) + render_prose(n['conclusion']) + render_prose(n['justification'])
        note = entry['clarifications'].get('step_notes', {}).get(n['id'])
        if note:
            out += '<aside class="qcb-boundary">' + render_prose(note) + '</aside>'
        out += '</li>'
    return out + '</ol>'


def page_body(entry, workbook, graph, live_ids, publication_commit):
    p = entry['packet']
    prefix = '../' * len(PurePosixPath(route(entry)).parts)
    group = workbook['groups'][entry['slot'][0]]
    body = ('<article class="qcb-reader" data-qcb-workbook="' + esc(entry['slot']) + '"><p class="qcb-breadcrumb"><a href="'
            + prefix + BASE + 'index.html">Supplementary workbook</a> / <a href="' + prefix + BASE + group[0] + '/index.html">'
            + esc(group[1]) + '</a></p><p class="eyebrow">Natural-language mathematics · no Lean installation needed</p><h1>'
            + esc(p['title']) + '</h1><p class="qcb-meta">' + esc(entry['band']) + ' · provisional construction route</p>')
    if p['contribution_type'] == 'existing_core_view':
        body += '<p class="qcb-meta">Additional exposition of <a href="' + prefix + HUB + 'cores/' + esc(p['core_id']) + '/index.html">' + esc(p['core_id']) + '</a>. The same mathematical contract and ' + esc(p['split']) + ' split apply; this is not another question.</p>'
    else:
        body += '<p class="qcb-meta">Supplementary candidate · split unassigned · outside canonical train/test exports.</p>'
    body += section('Assumptions and conventions', prose_list(p['assumptions']) + prose_list(p['conventions']), 'assumptions')
    body += section('Question', render_prose(p['question']), 'question')
    equations = ''
    for eq in entry['notation']['equations']:
        equations += '<div class="qcb-equation" data-qcb-given-equation data-qcb-math-source="' + esc(eq['source_excerpt']) + '">\\[' + esc(eq['tex']) + '\\]</div>'
    if equations:
        body += section('Notation already given in the question', equations, 'given-notation')
    body += section('Location in the Lean graph', graph_location(p, graph, live_ids, prefix), 'graph')
    if entry['slot'] in READING_LINKS:
        connections = '<p>Reading connections preserve the disclosed supplied-result boundary; they do not create extra independent tests of that result.</p><ul>'
        for slot, explanation in READING_LINKS[entry['slot']]:
            peer = next(e for e in workbook['entries'] if e['slot'] == slot)
            connections += '<li><a href="../' + slot.lower() + '/index.html">' + esc(peer['packet']['title']) + '</a> — ' + esc(explanation) + '</li>'
        body += section('Connect the exercises', connections + '</ul>', 'connections')
    body += folded('Reference solution', render_prose(p['reference_answer']), 'solution')
    rubric = '<ol>' + ''.join('<li>' + render_prose(r['criterion']) + '<p class="qcb-meta">' + esc(r['weight']) + ' / 10 points · ' + esc(r['id']) + '</p></li>' for r in entry['display_rubric']) + '</ol>'
    rubric += '<p>Credit mathematically equivalent complete derivations satisfying the same premises. A displayed proof route is not the only accepted route.</p>'
    if entry['clarifications'].get('grading_notes'):
        rubric += '<h3>Reviewed grading clarifications</h3>' + prose_list(entry['clarifications']['grading_notes'])
    body += folded('Assessment rubric', rubric, 'rubric')
    cases = '<dl>'
    for c in p['boundary_cases']:
        cases += '<dt>' + esc(c['case']) + '</dt><dd>' + ''.join(render_prose(v) for k, v in c.items() if k != 'case') + '</dd>'
    body += folded('Boundary cases and common errors', cases + '</dl><h3>Common errors</h3>' + prose_list(p['common_errors']), 'boundaries')
    reasoning = reasoning_map(entry)
    if entry['clarifications'].get('changes'):
        reasoning = '<h3>Reader scope clarifications</h3>' + prose_list(entry['clarifications']['changes']) + reasoning
    body += folded('How the reasoning connects', reasoning, 'reasoning')
    d = p['difficulty']
    facet = d.get('D0_facet') or d.get('D0', {}).get('facet', '')
    rationale = d.get('rationale') or d.get('D1_D4', {}).get('rationale', '')
    body += folded('Knowledge facets and difficulty', render_prose(facet) + render_prose(rationale) + '<p>The band describes the supplied construction route. It is not calibrated model difficulty or graph distance.</p>', 'difficulty')
    sources = '<p>Source-grounded mathematical exposition, separately reviewed by AI agents. No human expert approval or new Lean proof execution is claimed.</p><ul>'
    for ref in p['source_refs']:
        revision = publication_commit if ref['path'].startswith('benchmarks/') else workbook['source_commit']
        sources += '<li><a href="' + REPO + '/blob/' + revision + '/' + esc(ref['path']) + '">' + esc(ref['path']) + '</a>' + render_prose(ref['anchor']) + '</li>'
    sources += '</ul><p><a href="' + REPO + '/blob/' + publication_commit + '/' + esc(entry['payload_path']) + '">Original contribution</a> · <a href="' + REPO + '/blob/' + publication_commit + '/' + esc(entry['review']['report_path']) + '">Intake mathematical review</a></p>'
    sources += prose_list(entry['review']['limitations'])
    body += folded('Sources, review and exact identities', sources + '<p>Question SHA-256: <code>' + entry['question_sha256'] + '</code>. Original payload SHA-256: <code>' + entry['payload_sha256'] + '</code>.</p>', 'sources')
    return body + '</article>'


def publish_workbook(write, intro, workbook, graph, live_ids, publication_commit):
    entries = workbook['entries']
    body = intro('Supplementary mathematics workbook', 'Twelve source-grounded exercises connect normalization, coherent implementations, tensor structure and polynomial sampling. Read the mathematics, inspect its reasoning route, then follow the exact library anchors.')
    body += '<p class="qcb-meta">One cohort, delivered in two overlapping ZIPs: four additional expositions of existing cores and eight unassigned candidate targets. No new canonical core or scored split is allocated here.</p>'
    body += section('Choose a subject', '<div class="qcb-grid">' + ''.join('<article class="qcb-card"><h2><a href="' + slug + '/index.html">' + title + '</a></h2><p>Four linked mathematical exercises with reference arguments and source anchors.</p></article>' for slug, title in workbook['groups'].values()) + '</div>', 'subjects')
    body += section('Choose a construction level', '<p>' + ' · '.join('<a href="levels/' + band.lower() + '/index.html">' + band + ' (' + str(count) + ')</a>' for band, count in sorted(workbook['counts']['by_band'].items())) + '</p><p>These are provisional reasoning-route bands. D0 is the knowledge-reading facet of each exercise; no extra question is counted for it.</p>', 'levels')
    body += section('Inspect the graph and data', '<p><a href="graph/index.html">Node-to-exercise map</a> · <a download href="../../../data/quantumcomputingbench/nonlean-workbook/questions.jsonl">Question-only JSONL</a> · <a download href="../../../data/quantumcomputingbench/nonlean-workbook/references.jsonl">References and rubrics</a> · <a download href="../../../data/quantumcomputingbench/nonlean-workbook/index.json">Source and review index</a></p><p>These supplementary files are outside canonical training/evaluation exports. Existing-core expositions retain their original split; candidate split reconciliation remains pending. Public answers do not constitute a hidden holdout.</p>', 'data')
    body += cards(entries, '../../../')
    write(BASE, 'Supplementary mathematics workbook', body + '</div>', 'Source-grounded supplementary exercises with disclosed difficulty, reasoning routes and exact graph anchors.')
    for group, (slug, title) in workbook['groups'].items():
        body = intro(title, 'A subject chapter in the supplementary natural-language workbook.')
        body += '<p><a href="../index.html">Workbook contents</a></p>' + cards([e for e in entries if e['slot'][0] == group], '../../../../')
        write(BASE + slug + '/', title, body + '</div>', title + ': supplementary questions and mathematical arguments.')
    for band in sorted(workbook['counts']['by_band']):
        body = intro(band + ' · supplementary reasoning', 'A provisional construction-route band, not measured model difficulty.')
        body += '<p><a href="../../index.html">Workbook contents</a></p>' + cards([e for e in entries if e['band'] == band], '../../../../../')
        write(BASE + 'levels/' + band.lower() + '/', band + ' · supplementary workbook', body + '</div>', band + ' supplementary mathematical construction routes.')
    reverse = defaultdict(list)
    for e in entries:
        write(route(e), e['packet']['title'], page_body(e, workbook, graph, live_ids, publication_commit), e['packet']['question'])
        for field in ('target_nodes', 'supporting_nodes'):
            for node in e['packet'][field]:
                reverse[node].append({'slot': e['slot'], 'role': field, 'view_id': e['view_id']})
    body = intro('Supplementary exercise graph map', 'Find the exact library anchors cited by these mathematical exercises and the other questions that reuse them.')
    body += '<div class="qcb-workbook-graph">'
    body += '<p><a href="../index.html">Workbook contents</a> · <a href="../../../expert/index.html">Canonical expert atlas</a></p><p>Target/support citations and author-supplied reasoning routes are distinct from extracted Lean proof dependencies. Current exact-ID presence is a navigation fact.</p>'
    for node, rows in sorted(reverse.items()):
        href = '../../../../lean-graph/index.html?focus=' + quote(node, safe='')
        title = graph[node].get('label', node)
        content = '<p>' + ('<a href="' + esc(href) + '">Open current graph node</a>' if node in live_ids else 'Frozen graph identity; no current exact-ID match.') + '</p><ul>'
        for row in rows:
            e = next(e for e in entries if e['slot'] == row['slot'])
            content += '<li><a href="../' + row['slot'].lower() + '/index.html">' + esc(e['packet']['title']) + '</a> · ' + ('target' if row['role'] == 'target_nodes' else 'support') + '</li>'
        body += section(title, content + '</ul>', node_anchor(node))
    write(BASE + 'graph/', 'Supplementary node-to-exercise map', body + '</div></div>', 'Exact graph anchors and reverse question links for the supplemental workbook.')
    return {'schema_version': 'qcb.nonlean_workbook_projection.v1', 'workbook_digest': workbook['workbook_digest'], **workbook['counts'], 'distinct_graph_anchors': len(reverse), 'new_canonical_admissions': False}
