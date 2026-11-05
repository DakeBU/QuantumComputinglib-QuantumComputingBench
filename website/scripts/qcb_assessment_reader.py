"""Public assessment guidance and coverage; sealed questions never enter HTML."""
from __future__ import annotations

import html
import hashlib
from copy import deepcopy
from pathlib import Path
from urllib.parse import quote

BASE = 'quantumcomputingbench/run/assessment/'


def publication_record(status, commit):
    """Encode review role identifiers without changing qualified evidence.

    Agent role IDs may look like Unix filesystem paths. Keep exact original
    IDs in the committed qualification; the site exposes stable hashes and
    commits to the unprojected record instead of publishing path-shaped IDs.
    """
    from qcb_core import digest
    record = deepcopy(status)
    record['source_commit'] = commit
    record['qualification_unprojected_digest'] = digest(status['qualification'])
    record['qualification_identity_encoding'] = 'sha256_utf8_of_exact_review_role_id'
    for field in ('decoder_identity', 'source_comparer_identity'):
        identity = record['qualification']['review'][field]
        record['qualification']['review'][field] = 'sha256:' + hashlib.sha256(identity.encode('utf-8')).hexdigest()
    return record


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
    study = {c['core_id']: c for c in record.get('study_core_index', [])}
    existing_parents = coverage.get('existing_catalog_parent_core_count', coverage['sealed_parent_core_count'])
    parent_scope = str(existing_parents) + ' existing evaluation cores'
    if study:
        parent_scope += ' and ' + str(len(study)) + ' additional study core contracts'
    body = intro('Assess what a model can do',
        'Train on declared examples, then test mathematical decisions, arguments and tool-assisted proofs separately.')
    body += '<p class="qcb-breadcrumb"><a href="../index.html">Run a benchmark</a> / Assessment</p>'
    body += '<ol class="qcb-ladder" data-qcb-assessment-stages>'
    body += '<li><strong>Study and train</strong><p>The baseline has 74 existing cores, 86 language/semantic views and 12 Lean proof views. Multiple views do not add independent questions.</p><p><a download href="../../../data/quantumcomputingbench/assessment-train.json">Download baseline · contains answers</a></p><a href="' + ('training-profiles/index.html' if study else '../training/index.html') + '">' + ('Choose a training profile →' if study else 'Training guide →') + '</a></li>'
    body += '<li><strong>Calibrate in public</strong><p>Read the public questions, workbook and solutions. These are useful study material; their public-test labels do not make their answers secret.</p><a href="../../diagnostics/index.html">Try public semantic contrasts →</a></li>'
    split_scope = (' Eight are for development and ten for held-out testing.' if study else '')
    body += '<li><strong>Assess on a sealed set</strong><p>' + str(len(rows)) + ' propositions form ' + str(pairs) + ' balanced contrasts, anchored to ' + parent_scope + '.' + split_scope + ' Questions, answers and full review records stay outside the website repository.</p><a href="protocol/index.html">Prepare a controlled assessment →</a></li></ol>'
    body += '<p class="qcb-status-line" data-qcb-assessment-claim="bounded">A passing result supports the capabilities exercised by these cases under the stated access and budget. It does not certify mastery of the whole graph or reveal internal understanding.</p>'
    body += '<p><a class="button" href="coverage/index.html">Inspect graph coverage</a> <a href="protocol/index.html">Read the scoring contract</a></p>'
    body += fold('What must be reported?', '<p>Report first-answer label accuracy over every planned item; independently reviewed arguments and complete-contrast success; then isolated formal completion and tool costs as separate results. Missing answers remain in the denominator. Unreviewed explanations remain ungraded.</p><p>No real-model results or empirically calibrated difficulty are published here. A library-lemma application can establish a formal conclusion while leaving the unaided knowledge question unanswered.</p>', 'claims')
    write(BASE, 'Assess what a model can do', body + '</div>',
          'Separate train-only supervision, public calibration and a privately sealed quantum-domain assessment.')

    body = intro('Where the assessment reaches',
                 'Inspect exact library anchors and visible gaps before interpreting a score.')
    body += '<p class="qcb-breadcrumb"><a href="../index.html">Assessment</a> / Coverage</p>'
    body += '<p>' + str(len(rows)) + ' sealed propositions use ' + parent_scope + '. The 21-core public Lean course and the sealed set are bounded slices of the library.</p>'
    body += '<dl class="qcb-legend"><dt>Frozen inventory</dt><dd>' + str(coverage['declaration_inventory']) + ' declarations; ' + str(coverage['compiled_inventory']) + ' carry Compiled inventory status. These counts include helper and implementation facts.</dd><dt>Assessment anchors</dt><dd>' + str(coverage['course_anchors']) + ' public-course anchors and ' + str(coverage['sealed_assessment_anchors']) + ' sealed-set anchors. An anchor identifies evidence; it does not mean all knowledge at that node has been tested.</dd><dt>Uncovered formal inventory</dt><dd>' + str(coverage['compiled_not_anchored_by_these_formal_suites']) + ' compiled-inventory declarations have no anchor in these two formal suites. Question capacity and mastery coverage cannot be obtained by dividing these counts.</dd></dl>'
    body += '<p>Sealed parents are disjoint from the 74 canonical train cores. Primitive lemmas, source nodes and related mathematical mechanisms can still recur; the scorer merges shared exposure groups and makes no independence claim.</p>'
    groups = {}
    for row in rows:
        groups.setdefault(row['cluster_id'], []).append(row)
    for i, (name, group) in enumerate(sorted(groups.items())):
        anchors = sorted({n for r in group for n in r['source_nodes']})
        parents = sorted({n for r in group for n in r['parent_core_ids']})
        links = '<ul>' + ''.join('<li><a href="../../../../lean-graph/index.html?focus=' + quote(n, safe='') + '">' + esc(n.removeprefix('declaration:')) + '</a></li>' for n in anchors) + '</ul>'
        links += '<p>Question identities: ' + ', '.join(
            '<a href="#study-' + esc(study[p]['probe_id']) + '">Study contract ' + esc(study[p]['probe_id'][:8]) + '</a>'
            if p in study else '<a href="../../../cores/' + esc(p) + '/index.html#expert">' + esc(p) + '</a>'
            for p in parents) + '.</p>'
        body += fold(name.replace('_', ' ').capitalize() + ' · ' + str(len(group)) + ' propositions', links, 'mechanism-' + str(i))
    modules = '<div class="table-scroll"><table class="qcb-table"><thead><tr><th>Source module</th><th>Compiled inventory</th><th>Course anchors</th><th>Sealed anchors</th></tr></thead><tbody>'
    for row in coverage['all_modules']:
        url = 'https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/' + commit + '/' + row['source']
        modules += '<tr><td><a href="' + esc(url) + '">' + esc(row['source'].removeprefix('QuantumBlockEncoding/')) + '</a></td><td>' + str(row['compiled_inventory_declarations']) + '</td><td>' + str(row['course_anchor_count']) + '</td><td>' + str(row['sealed_assessment_anchor_count']) + '</td></tr>'
    body += fold('Inspect every inventoried source module', modules + '</tbody></table></div>', 'modules')
    if study:
        contracts = '<p>These are four new study-local mathematical contracts, shared by the natural-language and Lean stages. They do not alter the public catalog or relabel a training question. Both Promise contrasts share one source group.</p><ul>'
        for c in study.values():
            contracts += '<li id="study-' + esc(c['probe_id']) + '">' + esc(c['core_id']) + '<br><span style="overflow-wrap:anywhere">Contract SHA-256: ' + esc(c['contract_hash']) + '</span></li>'
        body += fold('Additional study contracts and shared source group', contracts + '</ul><p>The baseline already teaches key subproof and witness templates. Its score tests new compositions. A separately filtered training profile withholds those templates; pretraining exposure is unknown under either profile.</p>', 'study-contracts')
    body += '<p><a href="../../../../lean-graph/index.html">Lean Graph</a> · <a href="../../../../functor-hypergraph/index.html">Functor Hypergraph</a> · <a href="../protocol/index.html">Assessment protocol</a></p>'
    write(BASE + 'coverage/', 'Assessment coverage and gaps', body + '</div>',
          'Source-bound assessment locations and untested inventory, with no whole-graph mastery claim.')

    body = intro('Run a controlled assessment',
                 'Keep student input, the private grader and formal verification as separate stages.')
    body += '<p class="qcb-breadcrumb"><a href="../index.html">Assessment</a> / Protocol</p>'
    body += '<ol><li><strong>Freeze the experiment.</strong> Record model/checkpoint, training material, public-source exposure, prompt template, tool permissions and resource ceilings. Inspect overlap groups.</li><li><strong>Collect the first answer.</strong> Present one question in a fresh context without tools or feedback. Each task has fresh aliases and natural-language fields, with no graph IDs, gold labels or formal statements. Preserve the first-response seal.</li><li><strong>Review the mathematics.</strong> Grade every exact response against its bound rubric. A correct label with a false or unreviewed argument cannot pass the argument gate. Complete contrasts require both items.</li><li><strong>Challenge the locked belief in Lean.</strong> The requested root follows the model’s original decision, not the reference label. Use an accepted isolated verifier and a fresh fixed-root replay. Record proof completion, lookup, search and costs separately.</li></ol>'
    body += '<p class="qcb-status-line">Generated-proof execution remains ENV_BLOCKED until an accepted isolated verifier is connected. Dataset preparation and trusted authored reference checking do not remove that boundary.</p>'
    cli = 'assessment_v3.py' if study else 'assessment.py'
    commands = ('python benchmarks/quantumcomputingbench/scripts/' + cli + ' audit\n'
                'python benchmarks/quantumcomputingbench/scripts/' + cli + ' export-training --output TRAIN.json\n'
                'python benchmarks/quantumcomputingbench/scripts/' + cli + ' prepare --bank PRIVATE_BANK --split test_public --student RUN/student/tasks.json --controller RUN/grader/controller.json')
    body += fold('Commands and packaging', '<pre><code>' + esc(commands) + '</code></pre><p>RUN and PRIVATE_BANK must be outside the public checkout. The student batch file is for the controller; deliver only the current row to a model. Per-task directories contain one task.json each. An agent environment receives only that leaf directory, not the batch root, grader, bank or rubrics. CLI files are created once rather than overwritten.</p><p>The sealed bundle is held locally for the study owner. Public metadata commits to its exact content; public CI cannot replay undisclosed questions. Authorized experts can inspect the complete private question-to-source map and execution evidence.</p>', 'commands')
    body += fold('Interpret results carefully', '<p>Label accuracy, reviewed argument success and isolated proof success are different outcomes. The program uses planned denominators; missing, abstained, blocked and wrong responses remain visible. Reviewer and model identity are operator declarations, not authenticated by JSON hashes.</p><p>The inherited items retain their split labels. The four study contracts belong to the owner-sealed test set; visibility and split labels are separate policies. Sharing the sealed bank with a participant makes it source-exposed. Public references may already be in pretraining, and fresh aliases alone do not prevent memorization.</p><p>The formal decoder receives P without the reference-selected sign. This is a specific information boundary, not a claim that question wording has been statistically balanced or is free of linguistic cues. Label accuracy alone is weak evidence; the response must also meet the exact mathematical argument criteria.</p><p>New mechanisms and compositions help probe transfer, but contrast counts are not counts of independent statistical samples. The scorer merges common parents, mechanisms and source nodes. Whole-domain learning and causal training gain require a separate, matched experiment.</p>', 'interpretation')
    body += '<p><a href="../coverage/index.html">Inspect scope before running →</a></p>'
    write(BASE + 'protocol/', 'Sealed assessment protocol', body + '</div>',
          'First-answer, rubric and isolated proof evidence under a controlled exposure and resource contract.')
    routes = [BASE + 'index.html', BASE + 'coverage/index.html', BASE + 'protocol/index.html']
    if study:
        body = intro('Choose the training boundary',
                     'Declare what a model may study before interpreting transfer.')
        body += '<p class="qcb-breadcrumb"><a href="../index.html">Assessment</a> / Training profiles</p>'
        body += '<ol class="qcb-ladder"><li><strong>Baseline: 74 cores · 98 views</strong><p>Use the complete train-only package for domain study. The Promise assessment then tests new compositions of already taught subproofs and witness patterns.</p><a download href="../../../../data/quantumcomputingbench/assessment-train.json">Download baseline</a></li><li><strong>Family profile: 61 cores · 77 views</strong><p>Omit 13 complete training cores and their 21 views. The remaining package has 61 language, 8 semantic and 8 Lean views. Original split labels and retained examples are unchanged.</p><a download href="../../../../data/quantumcomputingbench/assessment-train-family-holdout.json">Download family profile</a></li></ol>'
        body += '<p class="qcb-status-line">This is a controlled task-family withholding policy under declared generic mathematical foundations. It does not establish that a checkpoint has never seen the source, theorem or problem family.</p>'
        body += fold('Conditions for interpreting a family-profile result', '<p>Use only the selected training package as study supervision; do not add excluded baseline examples, public evaluation solutions, the workbook or full library proofs. Collect the first answer without tools. Record all other source exposure and the exact checkpoint. A selected CLI profile is an operator declaration, not authenticated proof of training history.</p><p>Keep the same profile and declared training/inference budgets across matched SFT and RL comparisons. Different package sizes alone do not give a causal learning comparison. Formal library-assisted success is a separate result.</p>', 'exposure-conditions')
        body += fold('Why whole cores are omitted', '<p>The independent audit found involution/double-use failures, restored-work/intermediate-read behavior, preserved-control inverse proofs, target-H/CCZ/target-H and wrong-selector X witnesses in baseline training. The profile removes each affected core across every response modality. Elementary permutation, matrix, sector, placement and state-support foundations remain declared prerequisites.</p><p><a href="../../../../data/quantumcomputingbench/assessment-training-profiles.json">Inspect exact profile identities, exclusions and commitments</a></p>', 'profile-boundary')
        body += '<p><a href="../protocol/index.html">Run with an explicit profile →</a></p>'
        write(BASE + 'training-profiles/', 'Assessment training profiles', body + '</div>',
              'Separate baseline compositional transfer from an explicit whole-core family-withholding study.')
        routes.append(BASE + 'training-profiles/index.html')
    return {'schema_version': 'qcb.assessment_reader.v3' if study else 'qcb.assessment_reader.v2', 'sealed_probes': len(rows),
            'contrast_pairs': pairs, 'parent_cores': coverage['sealed_parent_core_count'],
            'existing_catalog_parent_cores': existing_parents, 'additional_study_cores': len(study),
            'model_results': False, 'hidden_questions_published': False,
            'routes': routes}
