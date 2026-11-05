"""Short benchmark workflow pages backed by the executable QCB runtime."""
from __future__ import annotations

import html
from collections import Counter

from website.scripts.qcb_navigation import card
from website.scripts.qcb_lean_reader import fold

HUB = 'quantumcomputingbench/'
CLI = 'python benchmarks/quantumcomputingbench/scripts/bench.py '


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
    counts = Counter(t['track'] for t in tasks)
    routes = []
    docs = source_link(publication_commit, 'benchmarks/quantumcomputingbench/docs/runtime.md', 'Runtime manual')
    benchcard = source_link(publication_commit, 'benchmarks/quantumcomputingbench/BENCHMARK_CARD.md', 'Benchmark card')

    def page(path, title, deck, content):
        write(HUB + 'run/' + path, title, intro(title, deck) + content + '</div>', deck)
        routes.append(HUB + 'run/' + path + 'index.html')

    content = '<div class="qcb-grid">'
    content += card('1. Check the environment', 'A CPU-only smoke verifies task binding and grading, without a model or Lean installation.', 'quickstart/index.html')
    content += card('2. Evaluate a model', 'Prepare answer-free tasks, collect responses and review the actual mathematical argument.', 'evaluation/index.html')
    content += card('3. Evaluate Agentic Lean', 'Compare proof workflows with a pinned library and an accepted isolated verifier.', 'agentic-lean/index.html')
    content += '</div><p><a href="training/index.html">Training data</a> · <a href="downloads/index.html">Data downloads</a> · <a href="protocol/index.html">Task and scoring contract</a></p>'
    content += '<p><a href="../lean/index.html">New to formal proof? Follow the four-stage Lean route →</a></p>'
    content += '<p class="qcb-status-line">' + ('CPU container workflow verified; model results are a separate experiment.' if (environment or {}).get('passed') is True else 'This build has not executed the CPU container gate.') + ' <a href="../../data/quantumcomputingbench/environment-smoke.json">Environment record</a>.</p>'
    page('', 'Run QuantumComputingBench', 'Choose a workflow. Each run keeps its question contract, source revision, exposure mode and evidence.', content)

    content = section('Run from a full checkout', '<p>Python 3.11 or newer. Keep full Git history so recorded source evidence can be checked.</p>' + commands('python -m pip install -r benchmarks/quantumcomputingbench/requirements.txt\n' + CLI + 'doctor\n' + CLI + 'validate\n' + CLI + 'smoke --output _out/qcb-smoke-001'), 'quickstart')
    content += '<p>The smoke uses synthetic oracle, incorrect and missing responses. It checks the workflow; it is not a model score.</p><p>Next: <a href="../evaluation/index.html">prepare your first evaluation →</a></p>'
    page('quickstart/', 'First CPU check', 'Verify the task and grading pipeline before using a model service.', content)

    content = '<ol class="qcb-workflow"><li><h2>Choose a capability</h2><p><strong>Knowledge and mathematical reasoning:</strong> use <code>--track nonlean</code>; grade explanations against the bound rubric. <strong>Semantic distinctions:</strong> use <code>--track semantic</code>; the decision label can be checked automatically, while the argument still needs review.</p></li>'
    content += '<li><h2>Prepare answer-free input</h2>' + commands(CLI + 'prepare-run --split test_public --track nonlean --output _out/qcb-nl-run-001') + '<p>Give the student only <code>input/tasks.jsonl</code>. Copy <code>output/responses.template.jsonl</code> for the response schema. Keep the source repository and operator files outside a closed-book student workspace.</p></li>'
    content += '<li><h2>Collect and score responses</h2><p>Use your model or agent to fill the bound response records. Record model/checkpoint, prompt template, thinking mode, decoding and token/call/time budgets. This command does not call a model:</p>' + commands(CLI + 'score --manifest _out/qcb-nl-run-001/manifest.json --responses PATH_TO_RESPONSES.jsonl --output _out/qcb-nl-score-001.json') + '</li></ol>'
    content += '<p><a href="review/index.html">Review mathematical explanations →</a> · <a href="../protocol/index.html">Understand the score dimensions</a></p><p class="qcb-status-line">Public answers exist. Report exposure and contamination limits; an answer-free export is not a hidden test set.</p>'
    page('evaluation/', 'Evaluate knowledge & reasoning', 'A complete evaluation needs the model response and a defensible score for the requested mathematical capability.', content)

    content = section('Create an operator-only review pack', commands(CLI + 'review-pack --manifest _out/qcb-nl-run-001/manifest.json --responses PATH_TO_RESPONSES.jsonl --output _out/qcb-nl-review-001') + '<p>The pack joins the exact question, actual response, reference, weighted rubric and graph anchors. Missing, abstained and blocked responses remain visible. Never give this pack to the student.</p>', 'review-pack')
    content += section('Grade the reasoning, then rescore', '<p>A human or disclosed AI reviewer completes <code>reviews.template.jsonl</code> using the unchanged criteria and saves <code>reviews.completed.jsonl</code>. Accept valid alternative arguments; matching the reference wording is not the criterion.</p>' + commands(CLI + 'score --manifest _out/qcb-nl-run-001/manifest.json --responses PATH_TO_RESPONSES.jsonl --reviews _out/qcb-nl-review-001/reviews.completed.jsonl --output _out/qcb-nl-reviewed-score-001.json'), 'score')
    content += '<p>Each review binds the exact response hash. Unreviewed explanations stay ungraded; reviewer identity is recorded provenance, not independently authenticated expert approval.</p>'
    page('evaluation/review/', 'Review the mathematical argument', 'Judge the response against the target and premises, not just a final label.', content)

    content = section('What is available now?', '<ul><li>' + str(counts['lean']) + ' registered formal task views with authored reference evidence, overlapping existing mathematical cores.</li><li>Approved-interface task exports retain exact roots and supplied obligations.</li><li>The live agent harness covers its original pilot registry; additional course companions are not automatically live model tasks.</li></ul>', 'availability')
    content += section('Inspect and prepare a formal task', commands(CLI + 'list --track lean\n' + CLI + 'prepare-run --track lean --exposure approved_interface --output _out/qcb-lean-run-001') + '<p>This prepares tasks only. It does not run a model or execute submitted proofs. The generic CPU bundle has no Lean compiler and rejects Lean tasks.</p>', 'prepare')
    content += fold('Inspect the course Agentic-proof suite', commands('python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py list --suite course-v4\npython benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py export --suite course-v4 --mode proof_dag --exposure approved_interface --output _out/qcb-course-proof-tasks-001.json') + '<p>The explicit suite selects qualified course companions; omitting it preserves the pilot default. Listing and exporting do not run a model. A synthetic fixture does not execute real Lean, and isolated generated-proof execution remains blocked until an accepted verifier is connected.</p><p><a href="../../lean/index.html">Follow the staged Lean route</a></p>', 'course-suite')
    content += section('Run a controlled experiment', '<ol><li>Choose the same root, permitted imports/interfaces, model and budget for every method.</li><li>Compare a complete-proof attempt, incremental tactic feedback and an NL-led shadow workflow only where the harness supports them. Record actual feedback timing, state reuse and all input/output costs.</li><li>Use the accepted isolated verifier. Success needs a fresh replay of the unchanged root and permitted transitive axioms; a legal tactic or an empty goal list alone is insufficient.</li><li>Report completion, failed attempts, timeouts, verifier calls, tokens and elapsed time separately. Until connected to accepted verifier receipts, formal model scores stay ungraded.</li></ol>', 'experiment')
    content += '<p class="qcb-status-line">Reference proof acceptance is not evidence that an arbitrary generated proof was isolated or that every NL sentence is correct.</p><p><a href="../../lean/index.html">Explore formal targets</a> · <a href="../../course/index.html">Inspect supplied proof routes</a> · ' + docs + '</p>'
    page('agentic-lean/', 'Evaluate Agentic Lean', 'Measure formal completion and tool use under an explicit library-access and verifier contract.', content)

    content = '<p class="qcb-status-line" data-qcb-results-status="no_model_results">No measured model leaderboard has been published. Synthetic workflow checks are labeled separately.</p>'
    content += section('What a publishable result should contain', '<ul><li>Model, checkpoint, harness revision, exposure mode and source/task hashes.</li><li>Planned-task counts, missing and blocked outcomes, plus subject and task-mode breakdowns.</li><li>Semantic decision accuracy, reviewed mathematical argument scores and isolated formal completion as separate dimensions.</li><li>Tokens, tool calls, elapsed time and run artifacts under a declared budget.</li></ul>', 'report')
    content += '<p><a href="../evaluation/index.html">Prepare an evaluation →</a> · <a href="../../../data/quantumcomputingbench/environment-smoke.json">Inspect the synthetic environment check</a></p>'
    page('results/', 'Results & reporting', 'Comparable results need reproducible task bindings and explicit scoring evidence.', content)

    content = section('Export train-only supervision', commands(CLI + 'export --purpose training --split train --output _out/qcb-train-001.jsonl') + '<p>Includes inherited train questions, assumptions, answers and rubrics. Preserve family/split identity across views; keep public-test data outside supervised training. A teacher-data export is not a training launch.</p><p><a download href="../../../data/quantumcomputingbench/runtime/train.jsonl">Download train-only JSONL</a>.</p>', 'export')
    content += fold('Export whole-root Lean references', commands('python benchmarks/quantumcomputingbench/scripts/lean_training.py --output _out/qcb-lean-train-001.json') + '<p>Choose a fresh output path. This exports train-only complete standalone root references from qualified course companions; dev and public-test cores remain excluded. It does not launch training or certify isolation for arbitrary model-generated proofs.</p><p><a href="../../lean/index.html">Read the corresponding mathematical and formal targets</a></p>', 'lean-supervision')
    content += '<p>Keep tokenizer, chat template, matched SFT-to-RL gate and isolated verifier configuration in the training project. Public solutions require contamination-aware reporting in subsequent studies.</p>'
    page('training/', 'Prepare training data', 'Export reviewed supervision while preserving the benchmark split contract.', content)

    content = '<ul class="qcb-download-list">'
    for filename, label in (
        ('task-index.json', 'Task index · identities, modes, splits and graph anchors'),
        ('train.jsonl', 'Training examples · train-only supervision'),
        ('eval-prompts.jsonl', 'Public-test prompts · no reference answers'),
        ('dev-prompts.jsonl', 'Development prompts · no reference answers'),
        ('response-template.jsonl', 'Response template · task-bound schema'),
        ('download-manifest.json', 'Manifest · content hashes')):
        content += '<li><a download href="../../../data/quantumcomputingbench/runtime/' + filename + '">' + label + '</a></li>'
    content += '</ul><p>' + str(len(catalog['cores'])) + ' canonical cores, ' + str(len(tasks)) + ' task views. View split totals: ' + ', '.join(esc(k) + ' ' + str(v) for k, v in sorted(splits.items())) + '.</p>'
    content += '<p>The <a href="../../non-lean/workbook/index.html">supplementary workbook</a> has separate downloads and unassigned candidates; it does not add scored holdouts.</p>'
    page('downloads/', 'Data downloads', 'Choose question-only evaluation input or train-only supervision. References have a separate role.', content)

    content = section('Three dimensions, separate evidence', '<dl class="qcb-legend"><dt>Knowledge and explanation</dt><dd>Grade the actual response against the weighted mathematical rubric. No review means ungraded.</dd><dt>Semantic decision</dt><dd>Check holds/refuted labels, planned-task accuracy and complete-contrast accuracy. A correct label does not establish a correct argument.</dd><dt>Formal completion</dt><dd>An accepted isolated verifier checks a fixed root and allowed axioms. Authored reference replay is not a model score.</dd></dl>', 'scores')
    content += section('Why the library graph matters', '<p>Exact source and graph anchors let experts see which definitions, premises and interfaces a task uses. Connected tasks can examine composition and reuse; a larger graph distance is not automatically a harder mathematical problem.</p><p><a href="../../expert/index.html">Open the expert graph atlas</a> · <a href="../../reasoning/index.html">Read task topology examples</a></p>', 'coverage')
    content += section('Portable and inspectable tasks', '<p>Each task separates instruction, environment, reference and verification, following the useful packaging model in <a href="https://docs.harborframework.com/tasks/overview">Harbor</a>. QCB keeps mathematical review, decision checks and formal verification distinct.</p><p>' + docs + ' · ' + benchcard + ' · <a href="../../evidence/index.html">Release boundaries</a></p>', 'contract')
    page('protocol/', 'Task & scoring contract', 'Understand what a result demonstrates before comparing models.', content)
    return {'schema_version': 'qcb.benchmark_center.v2', 'task_views': len(tasks), 'canonical_cores': len(catalog['cores']), 'routes': routes}
