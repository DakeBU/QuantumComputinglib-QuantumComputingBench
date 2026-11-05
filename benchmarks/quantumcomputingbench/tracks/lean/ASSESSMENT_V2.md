# Training, calibration and sealed assessment

QuantumComputingBench separates three uses of its mathematical material.
Train-only exports provide supervision. Public questions, solutions and the
supplementary workbook support study and calibration. A separately sealed
assessment contains additional propositions and counterfactuals whose full
questions, answers, proofs and reviewer records remain outside the public
repository. Public core IDs, contracts and inherited splits are preserved.

This release does not establish that any model has learned quantum computing.
It provides a reproducible way to assess specific observable capabilities.
Passing a finite test cannot guarantee internal understanding or mastery of
all results reachable in the library graph.

## What a result can support

| Measurement | Required evidence | Appropriate interpretation |
| --- | --- | --- |
| First-answer label accuracy | An unchanged question and sealed first response, scored over all planned items | The model selected the correct polarity on these items |
| Mathematical argument success | A response-bound review of every exact rubric criterion; equivalent valid arguments remain acceptable | The submitted argument establishes the requested conclusion or supplies a valid counterexample |
| Complete-contrast success | Both propositions in the planned pair pass the relevant gates | Success is sensitive to the changed assumptions or construction on this pair |
| Formal completion | Accepted isolated verifier receipts, unchanged root, fresh replay and allowed transitive axioms | The model/harness completed that formal task under the stated library access |
| Generalization or learning gain | Separately reviewed held-out mechanisms/forms, exposure audit and matched actual experiments | A scoped experimental conclusion; never inferred from question count or a reference replay |

A correct label with an incorrect or unreviewed explanation does not earn
argument success. Missing items remain in planned denominators. All necessary
rubric criteria must pass for binary argument success; a high partial weighted
score cannot compensate for a missing mathematical step. A public root theorem
can be directly callable through imports. Report library application and
tool-assisted completion separately from unaided mathematical reasoning.

## Data and exposure

The public training exporter combines 86 NL/semantic views and 12 checked
whole-root Lean references, covering 74 existing train cores. Multiple views of
one core are not independent questions. It excludes dev/test references, the
supplementary workbook and the sealed assessment. NL review and a formal
polarity/root certificate have different evidence scopes.

The sealed assessment contains 14 propositions in seven balanced contrasts.
They concern normalization and coherent probabilities, internal gauge and
interference, polynomial sampling structure, projected-block composition,
LCU weights, controlled phase and observable transport. All retain compiled
source anchors and the exact contracts/splits of their existing parent cores.
Their parent cores are outside the canonical train set. Primitive facts,
source nodes and mechanisms can still overlap training material; this is not
a claim of independent, novel mathematical families.

The inherited label `test_public` describes the parent split. It does not make
a new sealed question public. Likewise, keeping a question private does not
prove it or its mathematical content was absent from pretraining. Record all
public reading, retrieval, earlier assessment access and training data. Sharing
the private bank with a participant changes the exposure condition.

Fresh run aliases hide controller identities, not the mathematical content.
Deliver one question in a fresh context with no tools or feedback for the
first-answer stage. For an agent environment, mount only that task's leaf
directory. The projected batch index is for the controller, not an agent's
workspace. Keep all other questions, the controller, private bank and rubrics
outside that mount. A trusted operator and an appropriate runtime boundary are
still needed; JSON hashes cannot authenticate a dishonest operator or model.

## Reproduce the preparation and scoring

Use Python 3.11 or newer and the full Git history. Choose fresh paths.

```sh
python benchmarks/quantumcomputingbench/scripts/assessment.py audit
python benchmarks/quantumcomputingbench/scripts/assessment.py export-training \
  --output TRAIN/qcb-training.json

python benchmarks/quantumcomputingbench/scripts/assessment.py prepare \
  --bank PRIVATE_BANK --split test_public \
  --student RUN/student/tasks.json --controller RUN/grader/controller.json
```

`PRIVATE_BANK` and `RUN` must be outside the public checkout. Student and grader
directories must be disjoint. Preparation writes an answer-free batch index
and a `task.json` in each fresh per-task directory. It calls neither a model
nor Lean. The actual inference harness presents only the current question and
records the model/checkpoint, prompt/template, exposure, sampling and resource
ceilings. First-answer and tool-assisted stages require separate contexts.

The operator collects one response row per task:

`model_messages` supplies the canonical system/user messages without aliases or
controller metadata. The model returns the inner `decision`/`explanation`
object; `model_answer_row` wraps it with the controller's task alias. An inner
`abstain` becomes the explicit abstained outcome. Preserve the original raw
reply as well; this transport conversion does not repair mathematical answers.

```json
{"task_id":"PREPARED_UUID","status":"answered","answer":{"decision":"holds","explanation":"The actual mathematical argument."}}
```

Other explicit outcomes include `abstained`, `not_run`, `env_blocked`,
`budget_exhausted` and `protocol_error`, with `answer: null`. Absent rows are
recorded as missing. Do not silently repair a model answer after feedback.

```sh
python benchmarks/quantumcomputingbench/scripts/assessment.py freeze \
  --bank PRIVATE_BANK --student RUN/student/tasks.json \
  --controller RUN/grader/controller.json --responses RESPONSES.json \
  --output RUN/grader/first-answers.json

python benchmarks/quantumcomputingbench/scripts/assessment.py review-template \
  --bank PRIVATE_BANK --student RUN/student/tasks.json \
  --controller RUN/grader/controller.json --locked RUN/grader/first-answers.json \
  --output RUN/grader/reviews.json
```

Preserve the first seal before revealing any reference or feedback. The
template contains unset judgments and cannot score as a completed review.
An independent mathematical reviewer fills every exact criterion with a
Boolean judgment and substantive reason. Retain their identity, method and
the unchanged response/rubric hashes. Review evidence is private grader data.

```sh
python benchmarks/quantumcomputingbench/scripts/assessment.py score \
  --bank PRIVATE_BANK --student RUN/student/tasks.json \
  --controller RUN/grader/controller.json --locked RUN/grader/first-answers.json \
  --reviews RUN/grader/reviews.json --evidence-kind operator_supplied \
  --output RUN/grader/scores.json

python benchmarks/quantumcomputingbench/scripts/assessment.py formal-challenges \
  --bank PRIVATE_BANK --student RUN/student/tasks.json \
  --controller RUN/grader/controller.json --locked RUN/grader/first-answers.json \
  --output RUN/formal-student/tasks.json
```

The formal challenge requests P or not-P according to the locked student
belief, without selecting the reference answer for it. It supplies only a root
obligation, not an authored decomposition. These are compatible proof-task
contracts, not an executed tactic-state REPL. Generated-proof execution stays
`ENV_BLOCKED` until an accepted isolated verifier is connected. The generic CPU
student image is not a Lean verifier.

Scoring imports explicitly labeled artifacts. It does not authenticate a
model call, reviewer identity, source exposure, or causal training effect.
`synthetic_fixture` can never become a measured model result. The model and
formal-proof score fields remain unestablished until the appropriate actual
experiment and accepted verifier evidence are integrated.

## Mathematical and software qualification

The neutral decoder sees P rather than a gold-selected signed root. A distinct
source solver derives the decision and correspondence before seeing the author
answer; only afterward does that solver review the answer and rubric. Exact
inputs, first verdicts and repair history are preserved in the private bundle.
AI review is not authenticated human approval.

Here, neutral means that the formal decoder receives P without a
reference-selected sign. It does not mean that the natural-language question
style has been statistically balanced or shown to exclude linguistic cues.
All questions ask for a decision; some also conditionally request a witness or
repair. Interpret label accuracy as a diagnostic, not a sufficient assessment
of reasoning. The exact argument gate and full-contrast results remain
necessary, and the small set cannot support whole-domain statistical claims.

The public seal commits to the private cohort and review files. The inspected
reference pipeline is committed before replay. Authored-reference checking
binds fixed targets and proof hashes, uses the pinned matching library, checks
standard transitive axioms, performs a distinct final replay for every root,
and includes wrong-target and `sorryAx` rejection controls. This trusted author
workflow does not certify a sandbox for generated proofs.

Public mathematical qualification and software qualification are separate.
Changing a target/reference requires renewed mathematical review and replay.
Changing the scorer/CLI requires fresh software checks and source hashes, not
a reinterpretation of an older proof receipt. Public CI can verify source,
commitment, software and publication consistency without receiving secret
questions; full private reference replay requires the study-owner bundle.

The website exposes source/module coverage and gaps. Frozen Compiled inventory,
task anchors, extracted implementation dependencies and source-construction
topology remain distinct. Neither node count nor graph distance measures
knowledge coverage, reasoning depth or empirical model difficulty.

The design draws on paired informal/formal targets in
[ProofNet](https://arxiv.org/abs/2302.12433), library interaction in
[LeanDojo](https://leandojo.org/leandojo.html), and inspectable task/environment/
solution/test separation in [Terminal-Bench](https://www.tbench.ai/news/announcement).
These connections do not transfer those projects' validity or results to QCB.
