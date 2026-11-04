# Run, train and review QuantumComputingBench

QuantumComputingBench has three executable entry tracks: ordinary mathematical
answers, semantic decisions with explanations, and registered Lean course views.
The task registry joins the actual source-qualified inventories. Task views do
not create additional canonical mathematical cores. The public task index maps
each opaque task ID to its parent core, inherited split, graph anchors and
evidence class. Student JSONL is a separate answer-free projection.

The first checkout must retain full Git history: evidence qualification checks
the exact recorded source blobs. Python 3.11 or newer and the existing benchmark
requirements suffice for export, preparation and scoring. No model service,
GPU or Lean installation is required for these offline commands.

```sh
python -m pip install -r benchmarks/quantumcomputingbench/requirements.txt
python benchmarks/quantumcomputingbench/scripts/bench.py doctor
python benchmarks/quantumcomputingbench/scripts/bench.py validate
python benchmarks/quantumcomputingbench/scripts/bench.py list --track semantic
```

`validate` checks the canonical reader policy, all three cumulative Lean course
cohorts, semantic reviews and recorded reference receipts. It does not recompile
Lean, execute arbitrary proofs, or call a model. The first registry load can take
time because it verifies historical source and mathematical evidence. Results
are cached only within the current process; a fresh command checks fresh inputs.

## Download data for training or evaluation

```sh
python benchmarks/quantumcomputingbench/scripts/bench.py export --purpose training --output _out/qcb-train-001.jsonl
python benchmarks/quantumcomputingbench/scripts/bench.py export --purpose evaluation --split test_public --output _out/qcb-eval-001.jsonl
python benchmarks/quantumcomputingbench/scripts/bench.py export --purpose evaluation --split dev --output _out/qcb-dev-001.jsonl
python benchmarks/quantumcomputingbench/scripts/bench.py downloads --output _out/qcb-downloads-001
```

Training export is restricted to inherited `train` aliases and includes their
reference answers and complete rubrics. Each row also has `messages` with a user
question turn and an assistant reference-answer JSON turn, ready for a chat-data
loader. Model-specific tokenization, chat templates and actual training remain
the operator's separately validated integration. It rejects attempts to select `dev` or
`test_public` records as training. Lean course views have recorded references,
not synthesized SFT completions; they are excluded from this training export.
Use the existing qualified course source fixtures for authored formal proofs.
The natural-language and semantic training data do not authorize an SFT/RL
launch or bypass a model-specific matched SFT-to-RL gate.

Evaluation export contains `task_id`, `task_hash` and the exact question input.
`task_hash` binds the public task contract, not gold polarity, answers or pair
membership. The evaluator registry hash separately binds references and runtime
source identities. The source repository and textbook publicly contain solutions;
an answer-free file is therefore not a hidden test set or a contamination audit.
Cross-family and cross-split alias reconciliation remains an explicit release gate.

The download directory contains `task-index.json`, `train.jsonl`,
`eval-prompts.jsonl`, `dev-prompts.jsonl`, `response-template.jsonl` and a
SHA-256 `download-manifest.json`. The task index is for humans/operators. Keep
its source and graph mappings outside a closed-book student's prompt.

## Prepare a bound response run

```sh
python benchmarks/quantumcomputingbench/scripts/bench.py prepare-run --split test_public --track semantic --output _out/qcb-run-001
```

The run contains:

```text
manifest.json                     # registry/source/exposure/runtime identities
input/tasks.jsonl                 # only this input goes to the student
output/responses.template.jsonl   # copy schema and preserve exact identities
operator/model-profile.template.json
```

The preparation defaults to closed-book exposure and zero authorized calls or
spend. It launches nothing. An operator can collect responses later using any
model/agent implementation, recording actual model/checkpoint, tokenizer,
template, thinking mode, decoding, token/call/time usage and execution logs in
separate evidence. Filling a profile does not authenticate an imported run.
Do not edit the manifest after collecting responses; changed task hashes or run
IDs are rejected. New conditions use a fresh run directory.

For each task, write a record with `schema_version=qcb.response.v1`, the prepared
`run_id`, `task_id`, `task_hash`, `status`, and `answer`. An answered semantic
record has `answer={"decision":"holds","explanation":"..."}` or `refuted`.
An ordinary NL record has only `explanation` inside `answer`. For `abstained`,
`not_run`, `env_blocked` and `budget_exhausted`, `answer` is null. Omitted tasks
are recorded as missing, not silently dropped from the denominator.

```sh
python benchmarks/quantumcomputingbench/scripts/bench.py score --manifest _out/qcb-run-001/manifest.json --responses PATH_TO_RESPONSES.jsonl --output _out/qcb-score-001.json
```

Only the decision label is scored automatically. Reports distinguish accuracy
over every planned semantic task, accuracy on answered tasks, and joint accuracy
over selected contrast pairs. An always-one-label baseline cannot pass both
members of a balanced pair. Explanation quality and formal completion remain
separate. There is no pooled accuracy across incomparable NL, decision and Lean
views, and no automatic claim about model identity, learning or transfer.

## Review mathematical explanations

```sh
python benchmarks/quantumcomputingbench/scripts/bench.py review-template --manifest _out/qcb-run-001/manifest.json --responses PATH_TO_RESPONSES.jsonl --output _out/qcb-review-001.jsonl
python benchmarks/quantumcomputingbench/scripts/bench.py score --manifest _out/qcb-run-001/manifest.json --responses PATH_TO_RESPONSES.jsonl --reviews PATH_TO_COMPLETED_REVIEWS.jsonl --output _out/qcb-reviewed-score-001.json
```

An actual reviewer supplies their identity, human/AI kind, method and Boolean
marks for every unchanged weighted criterion. Each review binds the exact
response hash, so editing an answer invalidates its review. Alternative valid
arguments are judged against the mathematical criteria; reference-string
matching is not the grader. A partial review cannot produce a favourable
complete aggregate. Mixed tracks have separate semantic scores rather than one
pooled score. Declared reviewer identity is recorded provenance, not
independent authentication or invented expert approval.

## Portable CPU workspace and independent grader

```sh
python benchmarks/quantumcomputingbench/scripts/bench.py bundle --track semantic --split test_public --output _out/qcb-portable-001
```

The bundle has an agent-only `environment/` build context, `run/output/`
artifact directory, a separate `grader/` context and the trusted `solution/`
oracle. Its README gives Linux Docker commands. The Python base image is pinned
by the official multiarchitecture manifest digest. Run with no network, a
read-only root, no capabilities, no-new-privileges, CPU/memory/PID limits and
only the answer directory mounted writable. Record the actual built image ID
and container smoke results; source generation does not assert execution.

The CPU workspace contains Python stdlib and mathematical questions. It is
ready for an external answer-producing program or human, and starts by printing
its instructions. It contains no oracle, grader, model client or Lean toolchain.
A model-specific agent image is an operator integration, not an automatic
training job. The full repository or bundle must never be mounted into a
closed-book student environment because they contain public solutions.

The independent grader only parses response files. It does not execute submitted
Python, shell, Lean or other code. Model-generated Lean proof execution uses
the existing `scripts/evaluate_agentic.py` harness and stays `ENV_BLOCKED` until
its accepted isolated verifier gate passes. That live model-loop registry covers
its original pilot views. Additional course companions currently have qualified
task exports and synthetic fixture execution, not registration for live model
execution; a course view ID cannot simply be passed to the original registry.
To export a formal view here, use
`--track lean`; preparing such a run requires `--exposure approved_interface`,
matching the retained task input and its bounded interface protocol. It cannot
be relabeled as an open-library run without a separately defined protocol.
The generic CPU bundle rejects
Lean tasks rather than silently offering a compiler-free proof environment.

## Test the authoring and scoring workflow without models

```sh
python benchmarks/quantumcomputingbench/scripts/bench.py smoke --output _out/qcb-protocol-smoke-001
```

This executes the reviewed synthetic oracle, all-wrong-label, try-none and missing controls over
the qualified semantic cohort, rejects a tampered task hash, exports a portable
bundle, and checks its standalone oracle and grader as trusted CPU fixtures.
It starts no model, compiler or container. Oracle decision accuracy is a fixture
result; NL explanation and model-performance fields are not promoted by it.

Harbor/Terminal-Bench informed the task contract, environment/artifact boundary,
oracle and independent verifier design. QCB's portable JSON format does not
claim Harbor TaskConfig compatibility. Current upstream references:
[Terminal-Bench contribution guide](https://github.com/harbor-framework/terminal-bench/blob/main/CONTRIBUTING.md),
[Harbor task overview](https://docs.harborframework.com/tasks/overview),
[separate verifier](https://docs.harborframework.com/tasks/separate-verifier).
