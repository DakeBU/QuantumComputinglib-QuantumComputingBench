"""Public assessment guidance and coverage; sealed questions never enter HTML."""
from __future__ import annotations

import html
import hashlib
from pathlib import Path
from urllib.parse import quote

BASE = 'quantumcomputingbench/run/assessment/'


def training_package(registry, lean_export, commit):
    from qcb_bench_runtime import export_records
    rows = export_records(registry, purpose='training')
    cores = {c for t in registry['tasks'] if t['split'] == 'train' for c in t['core_ids']}
    expected = {t['task_id']: t for t in registry['tasks'] if t['split'] == 'train' and t['track'] != 'lean'}
    if (len(rows) != len(expected) or {r['task_id'] for r in rows} != set(expected)
            or any(r['split'] != 'train' or r['task_hash'] != expected[r['task_id']]['task_hash']
                   or r['reference'] != expected[r['task_id']]['reference'] for r in rows)):
        raise ValueError('language supervision leaked an evaluation task or changed its reference')
    if (lean_export['split'] != 'train' or lean_export['dev_and_test_references_projected'] is not False
            or any(e['split'] != 'train' or e['core_id'] not in cores for e in lean_export['examples'])):
        raise ValueError('combined supervision must preserve the declared train identities')
    root = Path(__file__).resolve().parents[2]
    sources = ['website/scripts/qcb_assessment_reader.py',
               'benchmarks/quantumcomputingbench/src/qcb_bench_runtime.py',
               'benchmarks/quantumcomputingbench/src/qcb_course_training.py']
    return {'schema_version': 'qcb.complementary_training_download.v2', 'source_commit': commit,
            'split': 'train', 'nl_and_semantic_examples': rows, 'lean_examples': lean_export['examples'],
            'counts': {'nl_and_semantic_views': len(rows), 'lean_views': len(lean_export['examples']),
                       'distinct_existing_cores': len(cores)},
            'producer_sources_sha256_lf': {p: hashlib.sha256((root / p).read_bytes().replace(b'\r\n', b'\n')).hexdigest() for p in sources},
            'reference_exposure': 'public_authored_supervision; pretraining_exposure_unknown',
            'workbook_included': False, 'assessment_bank_included': False,
            'new_mathematical_cores': 0, 'training_launched': False}


def esc(value):
    return html.escape(str(value), quote=True)


def fold(title, body, anchor):
    return ('<details class="qcb-disclosure" id="' + esc(anchor) + '"><summary>' + esc(title)
            + '</summary><div class="qcb-details-content">' + body + '</div></details>')


def publish_assessment(write, intro, record, commit):
    seal, coverage = record['seal'], record['coverage']
    rows = seal['probe_index']
    pairs = len({r['pair_id'] for r in rows})
    body = intro('Assess what a model can do',
        'Train on declared examples, then test mathematical decisions, arguments and tool-assisted proofs separately.')
    body += '<p class="qcb-breadcrumb"><a href="../index.html">Run a benchmark</a> / Assessment</p>'
    body += '<ol class="qcb-ladder" data-qcb-assessment-stages>'
    body += '<li><strong>Study and train</strong><p>Use train-only exports: 74 existing cores, 86 language/semantic views and 12 Lean proof views. Multiple views do not add independent questions.</p><a download href="../../../data/quantumcomputingbench/assessment-train.json">Download train-only package · contains answers</a> · <a href="../training/index.html">Training guide →</a></li>'
    body += '<li><strong>Calibrate in public</strong><p>Read the public questions, workbook and solutions. These are useful study material; their public-test labels do not make their answers secret.</p><a href="../../diagnostics/index.html">Try public semantic contrasts →</a></li>'
    body += '<li><strong>Assess on a sealed set</strong><p>' + str(len(rows)) + ' additional propositions form ' + str(pairs) + ' balanced contrasts, anchored to ' + str(coverage['sealed_parent_core_count']) + ' existing evaluation cores. Their questions, answers and reviewer records stay outside the website repository.</p><a href="protocol/index.html">Prepare a controlled assessment →</a></li></ol>'
    body += '<p class="qcb-status-line" data-qcb-assessment-claim="bounded">A passing result supports the capabilities exercised by these cases under the stated access and budget. It does not certify mastery of the whole graph or reveal internal understanding.</p>'
    body += '<p><a class="button" href="coverage/index.html">Inspect graph coverage</a> <a href="protocol/index.html">Read the scoring contract</a></p>'
    body += fold('What must be reported?', '<p>Report first-answer label accuracy over every planned item; independently reviewed arguments and complete-contrast success; then isolated formal completion and tool costs as separate results. Missing answers remain in the denominator. Unreviewed explanations remain ungraded.</p><p>No real-model results or empirically calibrated difficulty are published here. A library-lemma application can establish a formal conclusion while leaving the unaided knowledge question unanswered.</p>', 'claims')
    write(BASE, 'Assess what a model can do', body + '</div>',
          'Separate train-only supervision, public calibration and a privately sealed quantum-domain assessment.')

    body = intro('Where the assessment reaches',
                 'Inspect exact library anchors and visible gaps before interpreting a score.')
    body += '<p class="qcb-breadcrumb"><a href="../index.html">Assessment</a> / Coverage</p>'
    body += '<p>' + str(len(rows)) + ' sealed propositions reuse ' + str(coverage['sealed_parent_core_count']) + ' existing evaluation cores. The 21-core public Lean course and the sealed set are bounded slices of the library.</p>'
    body += '<dl class="qcb-legend"><dt>Frozen inventory</dt><dd>' + str(coverage['declaration_inventory']) + ' declarations; ' + str(coverage['compiled_inventory']) + ' carry Compiled inventory status. These counts include helper and implementation facts.</dd><dt>Assessment anchors</dt><dd>' + str(coverage['course_anchors']) + ' public-course anchors and ' + str(coverage['sealed_assessment_anchors']) + ' sealed-set anchors. An anchor identifies evidence; it does not mean all knowledge at that node has been tested.</dd><dt>Uncovered formal inventory</dt><dd>' + str(coverage['compiled_not_anchored_by_these_formal_suites']) + ' compiled-inventory declarations have no anchor in these two formal suites. Question capacity and mastery coverage cannot be obtained by dividing these counts.</dd></dl>'
    body += '<p>Sealed parents are disjoint from the 74 canonical train cores. Primitive lemmas, source nodes and related mathematical mechanisms can still recur; the scorer merges shared exposure groups and makes no independence claim.</p>'
    groups = {}
    for row in rows:
        groups.setdefault(row['cluster_id'], []).append(row)
    for i, (name, group) in enumerate(sorted(groups.items())):
        anchors = sorted({n for r in group for n in r['source_nodes']})
        parents = sorted({n for r in group for n in r['parent_core_ids']})
        links = '<ul>' + ''.join('<li><a href="../../../../lean-graph/index.html?focus=' + quote(n, safe='') + '">' + esc(n.removeprefix('declaration:')) + '</a></li>' for n in anchors) + '</ul>'
        links += '<p>Existing parent cores: ' + ', '.join('<a href="../../../cores/' + esc(p) + '/index.html#expert">' + esc(p) + '</a>' for p in parents) + '.</p>'
        body += fold(name.replace('_', ' ').capitalize() + ' · ' + str(len(group)) + ' propositions', links, 'mechanism-' + str(i))
    modules = '<div class="table-scroll"><table class="qcb-table"><thead><tr><th>Source module</th><th>Compiled inventory</th><th>Course anchors</th><th>Sealed anchors</th></tr></thead><tbody>'
    for row in coverage['all_modules']:
        url = 'https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/' + commit + '/' + row['source']
        modules += '<tr><td><a href="' + esc(url) + '">' + esc(row['source'].removeprefix('QuantumBlockEncoding/')) + '</a></td><td>' + str(row['compiled_inventory_declarations']) + '</td><td>' + str(row['course_anchor_count']) + '</td><td>' + str(row['sealed_assessment_anchor_count']) + '</td></tr>'
    body += fold('Inspect every inventoried source module', modules + '</tbody></table></div>', 'modules')
    body += '<p><a href="../../../../lean-graph/index.html">Lean Graph</a> · <a href="../../../../functor-hypergraph/index.html">Functor Hypergraph</a> · <a href="../protocol/index.html">Assessment protocol</a></p>'
    write(BASE + 'coverage/', 'Assessment coverage and gaps', body + '</div>',
          'Source-bound assessment locations and untested inventory, with no whole-graph mastery claim.')

    body = intro('Run a controlled assessment',
                 'Keep student input, the private grader and formal verification as separate stages.')
    body += '<p class="qcb-breadcrumb"><a href="../index.html">Assessment</a> / Protocol</p>'
    body += '<ol><li><strong>Freeze the experiment.</strong> Record model/checkpoint, training material, public-source exposure, prompt template, tool permissions and resource ceilings. Inspect overlap groups.</li><li><strong>Collect the first answer.</strong> Present one question in a fresh context without tools or feedback. Each task has fresh aliases and natural-language fields, with no graph IDs, gold labels or formal statements. Preserve the first-response seal.</li><li><strong>Review the mathematics.</strong> Grade every exact response against its bound rubric. A correct label with a false or unreviewed argument cannot pass the argument gate. Complete contrasts require both items.</li><li><strong>Challenge the locked belief in Lean.</strong> The requested root follows the model’s original decision, not the reference label. Use an accepted isolated verifier and a fresh fixed-root replay. Record proof completion, lookup, search and costs separately.</li></ol>'
    body += '<p class="qcb-status-line">Generated-proof execution remains ENV_BLOCKED until an accepted isolated verifier is connected. Dataset preparation and trusted authored reference checking do not remove that boundary.</p>'
    commands = ('python benchmarks/quantumcomputingbench/scripts/assessment.py audit\n'
                'python benchmarks/quantumcomputingbench/scripts/assessment.py export-training --output TRAIN.json\n'
                'python benchmarks/quantumcomputingbench/scripts/assessment.py prepare --bank PRIVATE_BANK --split test_public --student RUN/student/tasks.json --controller RUN/grader/controller.json')
    body += fold('Commands and packaging', '<pre><code>' + esc(commands) + '</code></pre><p>RUN and PRIVATE_BANK must be outside the public checkout. The student batch file is for the controller; deliver only the current row to a model. Per-task directories contain one task.json each. An agent environment receives only that leaf directory, not the batch root, grader, bank or rubrics. CLI files are created once rather than overwritten.</p><p>The sealed bundle is held locally for the study owner. Public metadata commits to its exact content; public CI cannot replay undisclosed questions. Authorized experts can inspect the complete private question-to-source map and execution evidence.</p>', 'commands')
    body += fold('Interpret results carefully', '<p>Label accuracy, reviewed argument success and isolated proof success are different outcomes. The program uses planned denominators; missing, abstained, blocked and wrong responses remain visible. Reviewer and model identity are operator declarations, not authenticated by JSON hashes.</p><p>The new items retain their parent dev/test_public split labels; visibility is a separate policy. Sharing the sealed bank with a participant makes it source-exposed. Public references may already be in pretraining, and fresh aliases alone do not prevent memorization.</p><p>The formal decoder receives P without the reference-selected sign. This is a specific information boundary, not a claim that question wording has been statistically balanced or is free of linguistic cues. Label accuracy alone is weak evidence; the response must also meet the exact mathematical argument criteria.</p><p>New mechanisms and compositions help probe transfer, but seven contrast groups are not seven independent statistical samples. The scorer merges common parents, mechanisms and source nodes. Whole-domain learning and causal training gain require a separate, matched experiment.</p>', 'interpretation')
    body += '<p><a href="../coverage/index.html">Inspect scope before running →</a></p>'
    write(BASE + 'protocol/', 'Sealed assessment protocol', body + '</div>',
          'First-answer, rubric and isolated proof evidence under a controlled exposure and resource contract.')
    return {'schema_version': 'qcb.assessment_reader.v2', 'sealed_probes': len(rows),
            'contrast_pairs': pairs, 'parent_cores': coverage['sealed_parent_core_count'],
            'model_results': False, 'hidden_questions_published': False,
            'routes': [BASE + 'index.html', BASE + 'coverage/index.html', BASE + 'protocol/index.html']}
