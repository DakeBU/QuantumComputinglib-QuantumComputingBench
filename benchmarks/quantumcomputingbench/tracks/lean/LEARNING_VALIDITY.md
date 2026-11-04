# Quantum-semantic questions and qualified reference answers

This workstream authors questions, reference answers, scoring criteria and
verification evidence. It does not require a model endpoint or actual student
responses. Model experiments can be conducted later in the separate prover
project; they are not an acceptance gate for the question bank.

The existing [course](COURSE.md) supplies construction routes and optional
subgoals. Completing a supplied route, or calling a theorem with the same
conclusion, does not by itself demonstrate that a model understands the quantum
mathematics. This additive pilot asks whether the respondent can distinguish a
valid statement from a nearby invalid one, explain the distinction, and provide
a proof or counterexample under the stated conventions.

## Current mathematical scope

The [cohort](learning-validity/v1/cohort.json) contains **16 propositions in eight
balanced true/refuted contrasts**, grouped into four mathematical mechanisms:

| Mechanism | Propositions | What the questions distinguish |
| --- | ---: | --- |
| State-core isometry and mass | 6 | Preserving arbitrary mass versus producing unit mass; changing output order versus preserving labeled entries; column isometry versus coisometry and range projection |
| Marginal norm and linearity | 2 | Preserving squared norm versus being an additive linear operation |
| Controlled permutations | 6 | Correct register/control order, inverse selection and matrix composition chronology |
| Hermite endpoint multiplicity | 2 | Uniqueness below a degree boundary versus a nonzero polynomial with the prescribed vanishing jets |

The questions retain the contracts and source aliases of five existing parent
cores: SP005, SP009, BE110, BE111 and SP104. Twelve inherit `train` and four
inherit `test_public`; none inherit `dev`. They are **public diagnostic contract
candidates**, not sixteen newly admitted canonical cores, a new hidden test set,
or interchangeable pre/post forms. They change neither the canonical core count
nor the native formal-view admission count. UUIDs identify diagnostic records;
they do not authorize independent split allocation.

Difficulty bands are provisional assessments of the mathematical construction.
An exact finite counterexample can refute a universal statement even when its
positive counterpart requires an argument for every parameter. In particular,
the false Hermite boundary admits a small counterexample; the supplied all-order
counterexample family is additional mathematical exposition. Node count, proof
length and polarity are not measured model difficulty.

## Questions and answers come before model evaluation

Every question records its assumptions, dimensions, register order, scalar
domain and exact proposition. Its reference packet contains a readable answer,
a fixed Lean proof of the correct decision polarity, and separate explanation
criteria. Equivalent valid arguments and counterexamples receive credit: the
reference route is not the only permitted method.

The independent review sequence is preserved in
[the evidence directory](../../reports/learning-validity-v1/):

1. A decoder reconstructs the quantifiers and mathematical meaning of the exact
   formal proposition and ambient definitions without seeing its intended NL
   question, polarity or reference answer.
2. A distinct comparer reads the question and decoded proposition, checks their
   correspondence, and derives the result before seeing the author's answer.
3. The comparer then reviews the answer and actual scoring criteria. Review
   identified eight overly restrictive criteria. The rejection and repair
   history remain available; alternative valid proofs and witnesses are now
   explicitly accepted.
4. The frozen authored proof is compiled, then the same fixed root is checked
   independently in a fresh process. Wrong-target and forbidden-axiom controls
   accompany each import context. Actual execution receipts bind the proof,
   target, source inputs, runtime, pipeline and source commit.

These are AI-assisted, content-bound reviews, not invented human expert
approval. Digest and consistency checks make substitutions visible; they do
not independently authenticate every claim about the outside world.

For a true proposition `P`, the formal reference establishes `P`. For a false
one, it establishes `not P` with an actual mathematical obstruction. A failed
compiler invocation does not establish that a proposition is false. Accepted
foundational axioms are `propext`, `Classical.choice` and `Quot.sound`; `sorryAx`
is forbidden. Compilation covers **decision polarity only**, not every sentence
of the explanation, the quality of a reasoning process, or a learning claim.

## Optional two-stage assessment

Stage A presents an ordinary mathematical question. The answer-free export
contains the question, assumptions, conventions, response schema and an opaque
probe ID. It omits gold answers, proofs, polarity, pair membership, parent/source
identifiers and formal targets. The respondent commits an initial decision and
explanation before receiving the optional formal challenge.

Stage B constructs one unscaffolded root from the **submitted decision**: `P`
when the respondent claims it holds, and `not P` when the respondent claims it
is refuted. It does not choose the target using the hidden gold label. Abstention
has no formal challenge. Imports remain available, including existing source
theorems; this pilot supplies neither a theorem firewall nor evidence of novel
proof discovery. Model-generated Lean execution remains `ENV_BLOCKED` until an
accepted isolated verifier is available.

Keep the scores separate:

- Decision accuracy and joint accuracy on complete contrast pairs.
- Mathematical explanation, assumptions and counterexample quality, graded by
  an actual bound review rather than a self-reported score.
- Exact formal completion, if an authorized isolated evaluation is later run.
- Method and tool-use evidence, distinct from mere kernel acceptance.
- Learning or transfer, which require a separately designed actual experiment.

An always-one-label response gets half the individual decisions right and no
complete contrast pair right. This is a diagnostic control, not a substitute
for explanation grading. The perfect gold-oracle fixture is synthetic; it is
never reported as model performance. Missing, abstained, blocked and incorrect
responses remain distinct outcomes.

## Inspect and reuse

Run these commands from the repository root. Each output path must be fresh;
retain historical receipts instead of overwriting them.

```sh
python benchmarks/quantumcomputingbench/scripts/learning_validity.py audit
python benchmarks/quantumcomputingbench/scripts/learning_validity.py export-stage-a --seed 23 --output _out/semantic-stage-a-001.json
python benchmarks/quantumcomputingbench/scripts/learning_validity.py run-fixture --output _out/semantic-fixtures-001.json
```

`audit` requires the current complete semantic reviews and actual reference
receipt. `audit --draft` only inspects a draft and does not qualify it for
evaluation. The public cohort contains solutions; use the explicit answer-free
projection for student prompts. A solution-bearing repository checkout is not
a hidden evaluation environment.

To reproduce only the reviewed, frozen authored references, use a matching
built checkout with the pinned production proof inputs:

```sh
python benchmarks/quantumcomputingbench/scripts/learning_validity.py check-references \
  --trusted-local-reference --build-root PATH_TO_MATCHING_BUILT_CHECKOUT \
  --output _out/semantic-reference-recheck-001.json \
  --raw-output ../private-evidence/semantic-reference-001.jsonl
```

This is trusted local authored-reference execution, not a sandbox for arbitrary
student code. Raw compiler transcripts stay outside the public repository.
The fixed budget is 2,400 seconds per batch, 300 per session, 120 per check,
65,536 output bytes and at most 48 replays. Per-check evidence is preserved if a
later check fails. The standard publication proof gate remains `lake build`
and `lake build Tests`, including the exhaustive source-module gate.

## What remains before claims about learning

The [optional matched-experiment specification](LEARNING_EXPERIMENT.md) separates
an in-context lesson from a weight update, matches model/runtime/prompt
conditions and keeps a no-update control. Its templates launch nothing and
default to zero endpoint spend. A public retest is calibration, not evidence of
fresh-family or unseen-composition transfer. This cohort has no reviewed
parallel-form registry; those transfer registrations remain `NOT_READY`.

Next question-authoring priorities are independently reviewed fresh forms,
broader node and boundary coverage, and compositions whose premises really
interact. Preserve parent aliases and splits across all views. Planned graph
nodes may suggest questions, but they cannot supply verified gold until their
own mathematical and Lean evidence is accepted. Existing canonical questions,
frozen releases and historical contributions remain intact.
