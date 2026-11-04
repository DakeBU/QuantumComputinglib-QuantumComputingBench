"""Human-facing benchmark entry points backed by the executable QCB runtime."""
from __future__ import annotations

import html
from collections import Counter

HUB = 'quantumcomputingbench/'


def esc(value):
    return html.escape(str(value), quote=True)


def commands(value):
    return '<pre class="qcb-command"><code>' + esc(value) + '</code></pre>'


def section(title, body, anchor):
    return '<section class="qcb-section" id="' + anchor + '"><h2>' + title + '</h2>' + body + '</section>'


def source_link(commit, path, label):
    import re
    if not re.fullmatch(r'[a-f0-9]{40}', commit or ''):
        return esc(label) + ' (source revision unavailable)'
    return '<a href="https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/' + commit + '/' + path + '">' + esc(label) + '</a>'


def publish_center(write, intro, catalog, registry, publication_commit, environment=None):
    tasks = registry['tasks']
    splits = Counter(t['split'] for t in tasks)
    ncores = len(catalog['cores'])
    breadcrumbs = '<p class="qcb-breadcrumb"><a href="../index.html">QuantumComputingBench</a> / Run the benchmark</p>'
    deck = ('Use the same versioned questions for mathematical study, train-only supervision, '
            'answer-free evaluation and expert review. Begin on a CPU; choose an isolated Lean '
            'backend when you need to execute a model-generated proof.')
    body = intro('Run QuantumComputingBench', deck) + breadcrumbs
    environment = environment or {'execution_status': 'not_run', 'passed': None}
    status = ('CPU containers and separate grading verified with oracle, wrong-label, not-run and tampered-task controls.'
              if environment.get('passed') is True else 'Portable CPU environment available; this build did not execute its Docker gate.')
    body += '<p class="qcb-status-line">' + status + ' <a href="../../data/quantumcomputingbench/environment-smoke.json">Inspect the environment record</a>.</p>'
    body += '<nav class="qcb-jump" aria-label="Benchmark workflow"><a href="#quickstart">Quick start</a><a href="training/index.html">Training data</a><a href="evaluation/index.html">Evaluation</a><a href="../expert/index.html">Expert graph review</a><a href="#downloads">Downloads</a></nav>'
    body += section('Choose the capability you want to measure', '<div class="qcb-grid">'
        '<article class="qcb-card"><h3>Mathematical knowledge and explanation</h3><p>Read the assumptions, answer in natural language, and assess the argument against a versioned rubric. Expert marks are separate from an automatically checked binary decision.</p></article>'
        '<article class="qcb-card"><h3>Semantic distinctions and counterexamples</h3><p>Decide whether a precisely stated claim holds, explain the distinction and give a proof or counterexample. Balanced contrasts expose always-one-label strategies.</p></article>'
        '<article class="qcb-card"><h3>Formal construction and repair</h3><p>Inspect the fixed formal target and supplied obligations. Open-library tasks preserve source and proof receipts; model proof execution requires the accepted verifier boundary.</p></article></div>'
        '<p>The registry contains ' + str(ncores) + ' canonical mathematical cores and ' + str(len(tasks)) + ' task views. Natural-language, diagnostic and Lean views are separately labeled; view count is not a count of new mathematical cores.</p>', 'capabilities')
    quick = ('python -m pip install -r benchmarks/quantumcomputingbench/requirements.txt\n'
             'python benchmarks/quantumcomputingbench/scripts/bench.py doctor\n'
             'python benchmarks/quantumcomputingbench/scripts/bench.py validate\n'
             'python benchmarks/quantumcomputingbench/scripts/bench.py list\n'
             'python benchmarks/quantumcomputingbench/scripts/bench.py smoke --output _out/qcb-smoke-001')
    body += section('Start with a reproducible CPU check', '<p>Run these commands from a full repository checkout. The smoke uses fixed reference fixtures and deliberately wrong or missing responses. Its result checks the workflow; it is labeled synthetic.</p>' + commands(quick)
        + '<p>Next: <a href="evaluation/index.html">prepare an answer-free run</a>, <a href="training/index.html">export train-only examples</a>, or <a href="../expert/index.html">review where the questions sit in the graph</a>.</p>', 'quickstart')
    downloads = '<p>These files are generated from the current checked registry. Prompts, supervision and result templates have distinct purposes.</p><ul>'
    for filename, label in (
        ('task-index.json', 'Task index: identities, splits, views and graph anchors'),
        ('train.jsonl', 'Training examples: inherited train split only, with reference answers'),
        ('eval-prompts.jsonl', 'Public-test evaluation prompts: no reference answers'),
        ('dev-prompts.jsonl', 'Development prompts: no reference answers'),
        ('response-template.jsonl', 'Response schema and task-bound template'),
        ('download-manifest.json', 'Download manifest and content hashes')):
        downloads += '<li><a download href="../../data/quantumcomputingbench/runtime/' + filename + '">' + label + '</a></li>'
    body += section('Download the current task views', downloads + '</ul><p>Task-view split totals: ' + ', '.join(esc(k) + ': ' + str(v) for k, v in sorted(splits.items())) + '. Shared source aliases retain their existing split.</p>', 'downloads')
    body += section('A task is more than a question', '<ol><li><strong>Instruction:</strong> an explicit target, assumptions, conventions and response contract.</li><li><strong>Environment:</strong> the disclosed library access and bounded workspace.</li><li><strong>Reference:</strong> a reviewed answer or checked authored proof, outside the student input.</li><li><strong>Verification:</strong> decision checks, bound expert marks and formal evidence as distinct dimensions.</li><li><strong>Trace:</strong> graph anchors, source revision, task hashes and run artifacts.</li></ol><p>Our task packaging follows the useful instruction/environment/solution/verifier separation described by <a href="https://docs.harborframework.com/tasks/overview">Harbor</a>. Runtime support and actual execution evidence are recorded for each export.</p>', 'task-contract')
    docs = source_link(publication_commit, 'benchmarks/quantumcomputingbench/docs/runtime.md', 'Runtime manual')
    card = source_link(publication_commit, 'benchmarks/quantumcomputingbench/BENCHMARK_CARD.md', 'Benchmark card')
    body += section('Supplementary practice and contribution review', '<p><a href="../non-lean/workbook/index.html">The supplementary mathematics workbook</a> has four existing-core expositions and eight unassigned candidate targets. Its question-only and reference downloads are separate from the canonical training/evaluation files above. Study and review these source-grounded problems without treating them as additional scored holdouts.</p>', 'supplementary')
    body += section('Review and contribute', '<p>' + docs + ' · ' + card + ' · <a href="../expert/index.html">Expert graph atlas</a> · <a href="../contribute/index.html">Contributor protocol</a>.</p><p>Review the mathematical target and scoring contract first. Report a questionable answer, missing premise, graph mismatch or verifier loophole with its task ID and source revision.</p>', 'contribute')
    write(HUB + 'run/', 'Run QuantumComputingBench', body + '</div>', deck)

    body = intro('Prepare training data', 'Export reviewed supervision from the inherited train split and retain the source identity of every example.')
    body += '<p><a href="../index.html">Run the benchmark</a> / Training</p>'
    body += section('Train-only supervision', '<p>The training export contains questions, assumptions, reference answers, rubrics and task bindings from train aliases. Use the evaluation export for development or public-test prompts. A teacher-data export is not a training launch.</p>'
        + commands('python benchmarks/quantumcomputingbench/scripts/bench.py export --purpose training --split train --output _out/qcb-train-001.jsonl')
        + '<p><a download href="../../../data/quantumcomputingbench/runtime/train.jsonl">Download the current train-only JSONL</a>.</p>', 'export')
    body += section('Keep examples and evaluations traceable', '<ol><li>Record the registry and task hashes with your training data.</li><li>Keep inherited source families and cross-view aliases in their original split.</li><li>Separate natural-language supervision from formal completion examples and process-reward labels.</li><li>Preserve the model-specific matched SFT-to-RL gate and verifier isolation in the training project.</li></ol><p>Open reference answers support teacher training. Public solutions and repeated source theorems require contamination-aware reporting in subsequent model studies.</p>', 'provenance')
    write(HUB + 'run/training/', 'Training data · QuantumComputingBench', body + '</div>', 'Train-only exports with source, graph and task bindings.')

    body = intro('Prepare and score an evaluation', 'Create a reproducible run, provide task-bound responses, then apply the appropriate verification and review steps.')
    body += '<p><a href="../index.html">Run the benchmark</a> / Evaluation</p>'
    body += section('A prepared run', '<p>Use a fresh output directory. The student receives the input payload; operator manifests and review materials stay outside that mount. Record the model, harness, exposure mode and budget before collecting responses.</p>'
        + commands('python benchmarks/quantumcomputingbench/scripts/bench.py prepare-run --track semantic --output _out/qcb-run-001')
        + '<p>The runtime manual specifies the response-file schema and scoring command. The same preparation flow supports a later external model service or a collaborator-operated agent.</p>', 'prepare')
    body += section('Read each result dimension separately', '<table class="qcb-table"><thead><tr><th>Dimension</th><th>Evidence</th></tr></thead><tbody>'
        '<tr><td>Decision</td><td>Exact holds/refuted label on the semantic tasks, plus complete-contrast accuracy.</td></tr>'
        '<tr><td>Explanation</td><td>A reviewer grades the actual response against the bound mathematical criteria. Unreviewed remains ungraded.</td></tr>'
        '<tr><td>Formal completion</td><td>An accepted isolated verifier checks the exact root; local author proofs are reference evidence.</td></tr>'
        '<tr><td>Resources</td><td>Observed tokens, calls, elapsed time and the declared runtime configuration.</td></tr>'
        '<tr><td>Coverage</td><td>Source-bound subjects, graph anchors and task views, with missing and excluded cases visible.</td></tr></tbody></table>'
        '<p>Missing, abstained, blocked and incorrect responses remain different outcomes. Explanation and formal scores stay ungraded until their evidence exists.</p>', 'scores')
    body += section('Use the required environment', '<p>Closed-book natural-language runs use question-only input. Formal companion exports retain their approved-interface contract and pinned library. The portable task bundle provides an agent workspace and separate grading entry point; the environment report states whether it was actually executed on your machine.</p>'
        + '<p>' + docs + ' · <a href="../../expert/index.html">Inspect task locations and graph coverage</a> · <a download href="../../../data/quantumcomputingbench/runtime/response-template.jsonl">Download a response template</a>.</p>', 'environment')
    write(HUB + 'run/evaluation/', 'Evaluation workflow · QuantumComputingBench', body + '</div>', 'Question-only inputs, task-bound responses and separate scoring dimensions.')
    return {'schema_version': 'qcb.benchmark_center.v1', 'task_views': len(tasks), 'canonical_cores': ncores,
            'routes': [HUB + 'run/index.html', HUB + 'run/training/index.html', HUB + 'run/evaluation/index.html']}
