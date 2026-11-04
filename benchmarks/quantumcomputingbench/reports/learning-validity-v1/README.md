# Quantum-semantic reference pilot: authored evidence

This checkpoint qualifies questions and reference answers, not a model or a
claim that a model has learned quantum computing. The public pilot contains 16
candidate propositions in eight balanced true/refuted contrasts over four
mathematical mechanisms. The five parent cores and their inherited splits are
unchanged; no canonical core or native formal admission is added.

## What was actually checked

- Formal meaning was decoded before the intended NL question and gold were
  shown. A distinct comparer then checked correspondence and independently
  derived the mathematics before reviewing the author's answer and rubric.
- All 16 answers and repaired rubrics were accepted in that AI-assisted review.
  Eight restrictive criteria were repaired to admit equivalent valid proofs or
  counterexamples. The rejection and intermediate repairs remain in this folder.
- The fixed authored references passed 38 actual Lean checks: one submission and
  one separate fresh final-root replay for every proposition, plus wrong-target
  and forbidden-axiom controls for each of the three import contexts.
- Accepted roots use only `propext`, `Classical.choice` and `Quot.sound`.
  The `sorry` controls compiled but were rejected because of `sorryAx`;
  wrong-target controls were rejected by elaboration. Neither is an execution
  timeout relabeled as a mathematical rejection.
- The 367-test benchmark suite passed. The 10 focused reader tests passed and
  cover exact question/premise/rubric projection, closed answers, source links,
  stale evidence rejection and unchanged canonical inventories.
- Two shuffled answer-free exports preserved all 16 question payloads and
  omitted gold answers and proofs. Synthetic decision controls behaved as
  expected: an always-one-label response scores 0.5 individually and 0 on
  complete contrasts. These are fixtures, not model responses.
- All 87 pre-existing benchmark Python files remain unchanged from the base
  commit. Earlier release, agentic registry and all three course CLI gates pass.

## Evidence and reproduction

Read [qualification.json](qualification.json),
[reference-checks.json](reference-checks.json),
[execution-summary.json](execution-summary.json), and the
[actual production proof gate](production-lean-gate.json). The reference source
checkpoint is `107c70404775c5c444b8888ab89769291f511d24`; retain that Git history
when integrating this branch. The receipt validates exact recorded Git blobs,
not a moving branch name. It can be rechecked with
`python benchmarks/quantumcomputingbench/scripts/learning_validity.py audit`.

Actual Lean execution used a clean matching production checkout at
`f2cba045611a0d11c5995c29607569726bf1d6c5`, Lean 4.29.1. Its complete source/config
digest matches the feature checkout. Fresh `lake build`, `lake build Tests` and
all 202 explicit source-module targets passed there. This records the actual
checkout used; it does not assert a separate compilation at the feature commit.
Publication additionally validates the unchanged proof/Blueprint input mapping
and the rendered website.

The executable reference scope is trusted local, frozen, reviewed author code.
It does not certify a sandbox for model-generated Lean. Private raw compiler
transcripts are preserved outside the public repository; the curated receipt
retains request/source/runtime/result bindings without publishing host paths.
Consistency checks establish artifact agreement, not independent authentication
of arbitrary externally supplied execution claims.

## Limits retained

Lean covers each exact decision polarity, not every explanatory sentence,
repair or resource interpretation. The pilot is public and source-exposed;
imports can include a theorem with the requested conclusion. Its 12 train and
4 public-test aliases are inherited, not a fresh held-out learning study.
Construction bands remain provisional. No model call, training run, GPU job or
actual learning measurement was required or performed. Fresh-family and
unseen-composition assessment still require independently reviewed parallel
forms and a separate actual experiment.

See the [question-authoring guide](../../tracks/lean/LEARNING_VALIDITY.md) for
the mathematical themes, optional staged assessment and reproduction commands.
