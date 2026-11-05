# Lean curriculum: interval restriction and phase-aware proof

This continuation adds three experimental formal companions to existing
mathematical questions. The cumulative course has 21 shared cores. It is a
bounded State Preparation and Block Encoding slice, not whole-library coverage.
Canonical NL questions, families, splits and formal admissions remain unchanged.
The independently authored NL workbook and future NL proposals retain their
own review/admission process.

## Learn and assess progressively

Use the [Lean learning route](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/lean/).
Its four child pages separate contract understanding, local proofs, interface
composition and parameterized arguments. Mathematical questions are readable
without Lean; exact formal targets, solutions and evidence are folded.

| Shared core | Construction band | New formal assessment | Explicit boundary |
| --- | --- | --- | --- |
| BE101 | D2 | Finite XOR loader table, selector preservation and two-step cancellation | Kernel finite decision is a disclosed shortcut; no arbitrary-width synthesis or cost claim |
| SP110 | D3 | Bernstein restriction preserves coefficient bounds through two admissible interval transformations | Exact real arithmetic; no floating-point stability or circuit bound |
| BE104 | D4 | Compiler induction over all gate lists and an exact concrete phase ledger, including rejection of phase-free equality | Bare and phase-aware denotations differ; no gate optimality or hardware claim |

BE120 was also prepared and author-checked, but its frozen anchors retain
`Partial route` inventory status. The existing course gate requires `Compiled`;
the companion is deferred rather than promoted by changing that rule. Its
involution, finite bijection, counterexample and stored inverse-record equality
remain inspectable in the author/diagnostic files. Symbolic `Coeff` record
equality is not a complex matrix-square or physical adjoint theorem. A reviewed
versioned evidence refresh or separately designed scoped-anchor mechanism is
needed before course admission; the frozen graph and original NL core remain
unchanged. See [the deferred record](../../reports/lean-course-v4/deferred-be120.json).

SP116 also remains diagnostic. Its prepared positive-affine-grid theorem for
the particular `sourceInterpolant` has correct explicit width `8k+12`, but the
independent source comparison rejected alignment to the current broader
grid/polynomial question. The mathematical theorem was not refuted. Its
author proofs and exact rejected verdict are preserved; it is not an admitted
course companion and its missing source restrictions are not silently added
to the NL question. See [the source-scope record](../../reports/lean-course-v4/deferred-sp116.json).

D0 reads the objects, premises and conventions of these same cores. It adds no
question. D1--D4 describe the disclosed construction route, not empirical model
difficulty. Full imports and exact-root shortcuts remain callable: a successful
library application must be reported separately from a constructed proof.

The supplied obligation DAG records available intermediate results. It is not
an exhaustive extraction of proof-term dependencies. Imported helper facts can
remain outside it. All listed AND prerequisites are enforced in supplied-DAG
mode; whole-root mode may attempt the fixed root directly. Neither mode is a
persistent tactic-state REPL or a test of autonomous decomposition discovery.

## Inspect, export and exercise the protocol

From the repository root, using fresh output names:

```sh
python benchmarks/quantumcomputingbench/scripts/lean_course_v4.py audit
python benchmarks/quantumcomputingbench/scripts/lean_course_v4.py export \
  --split train --output _out/course-v4-train-inputs.json
python benchmarks/quantumcomputingbench/scripts/lean_course_v4.py export \
  --band D4 --mode root_only --exposure closed_book \
  --output _out/course-v4-D4-root-inputs.json
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py list --suite course-v4
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py export \
  --suite course-v4 --split dev --output _out/course-v4-dev-inputs.json
python benchmarks/quantumcomputingbench/scripts/evaluate_agentic.py run-fixture \
  --suite course-v4 --view qcb-course-be-104-v1 \
  --episode-dir ../qcb-eval-private/be104-fixture-fresh
```

The explicit course suite connects every qualified companion to the existing
bounded action loop. The preserved four-view pilot remains the default suite.
Offline profile/schema commands do not load either registry. A synthetic
fixture calls neither Lean nor a model and cannot produce a formal certificate.
Real formal mode still exits before adapter construction until an accepted
isolated verifier is connected. No administrator contact or privilege reuse is
part of this curriculum.

## Export formal training supervision

```sh
python benchmarks/quantumcomputingbench/scripts/lean_training.py \
  --output _out/course-v4-train-supervision.json
```

This separate exporter includes only existing `train` cores and their checked
standalone whole-root references. It has no split override. Dev and public-test
proofs are omitted, inputs and targets are separate, and every example binds
its task, contract, source and recorded reference lineage. It uses the
constructed whole-root control where available, otherwise an explicitly
identified library application. It neither launches training nor invents
process-reward labels. A public authored proof is supervision for an observable
formal result, not evidence of a model's faithful internal thoughts.

Evaluation exports omit reference bodies and rubrics. The same references are
public elsewhere, so these exercises are not secret or contamination-free tests.
Common library interfaces legitimately recur across splits. BE104 and BE111,
for example, both use permutation/composition mathematics; their different
assessed targets do not make every subproof independent. Keep that exposure in
later learning/generalization reports. Do not move any existing split to make
a comparison appear cleaner.

## Mathematical and execution evidence

The fixed three-core cohort is [graph-course-v4.json](fixtures/graph-course-v4.json).
It binds the canonical question and exact covered formal targets. Independent
formal-only reconstructions and a distinct source-aware comparison use
sanitized inputs: question, reference answer, assumptions and conventions,
without historical approval metadata or author proof bodies. AI role separation
and hashes do not authenticate human review or mathematical truth by themselves.
Exact coverage and remaining NL obligations are reported per core.

The [fourth-cohort reports](../../reports/lean-course-v4/) preserve author
probes, source/decoder bindings, actual authored-reference execution and
remaining limitations. Old cohorts and frozen releases are not re-sealed.
Reference checking uses an inspected hash allowlist, the pinned Lean runtime,
fixed root types and the standard three-axiom policy. Wrong-target and `sorryAx`
controls test rejection; mathematical counterexamples have a separate role.

Reproduce the authored-only replay in a matching, already-built checkout:

```sh
python benchmarks/quantumcomputingbench/scripts/lean_course_v4.py check-references \
  --build-root PATH_TO_MATCHING_BUILT_CHECKOUT --trusted-local-reference \
  --output _out/course-v4-authored-fresh.json \
  --raw-output ../qcb-eval-private/course-v4-authored-raw-fresh.json
```

The reviewed pipeline must be committed before replay. The fixed profile allows
3,600 seconds per batch, 600 per supplied-DAG session, 120 per compiler check and
180 per standalone control. These are authored-development ceilings, not matched
model-compute budgets or aggregate sandbox limits. Finish proof-bearing work
with `lake build` and `lake build Tests`; publication has additional site gates.

The next frontier is broader reviewed domain coverage and accepted isolated
model evaluation. Neither graph size, tactics accepted, node count, metadata
validation nor a reference replay establishes that a model learned quantum
computing, that intermediate actions were useful, or that the benchmark is a
stable whole-graph release. Producing this question/reference corpus does not
require collecting real-model responses.
