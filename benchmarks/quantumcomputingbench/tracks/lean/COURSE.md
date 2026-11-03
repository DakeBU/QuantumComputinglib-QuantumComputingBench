# Graph-grounded Lean course

This experimental course develops quantum-computing proof assessment by
mathematical prerequisites and mechanisms. It preserves the shared core IDs,
contracts, families and splits. Knowledge, Lean syntax and mixed views of the
same target remain one question. The non-Lean track and frozen releases remain
independent of this sidecar's qualification.

The candidate plan is [course-v1.json](curriculum/course-v1.json). Its new
companions require their content-bound semantic review and actual authored
reference receipt before `lean_course.py audit` or `export` succeeds. A candidate
file, graph node or difficulty label alone cannot enable evaluation gold.

## Difficulty is conditional

| Layer | Construction assessment | Examples in this slice |
| --- | --- | --- |
| D0 | Knowledge of assumptions, objects and conventions, assessed using the same core's canonical semantic rubric | Distinguish row Gram from column isometry, joint mass from a marginal, finite-width rank from a circuit bound |
| D1 | Precise statement reading and a disclosed library application | SP009 real-to-complex isometry calibration |
| D2 | Local symbolic construction and entry/sum reasoning | BE105 normalization iff, BE107 block Gram, SP005 marginal norm |
| D3 | Joining mathematical interfaces and preserving every AND premise | BE109 nested tensor lift, SP114 Taylor factorization and rank, LA102 determinant invariance |
| D4 | Parametric induction and global invariant/representation control | SP007 transfer induction, SP008 real joint probability |

D0 facets do not create extra questions. D1--D4 are provisional mathematical
assessments of the inspected construction routes, not measured model difficulty.
An imported exact-root theorem can turn a D3 construction into a D1 application.
Controls and callable shortcuts are disclosed, not hidden to inflate difficulty.
Actual model calibration needs fixed model/exposure/tool profiles and measured
outcomes. Tactic count, source lines, graph distance and node count do not define
these bands.

## Scope of the first expansion

The original four experimental roots remain unchanged. Five companions add
BE105, BE107, BE109, SP114 and the already aligned native SP009 calibration.
The course therefore plans nine distinct existing cores, not nine new
mathematical targets or canonical admissions. SP005/LA102 use their existing
construction views rather than counting their native warmups again.

BE105 includes both directions of the unitary-normalization equivalence. The
existing library's sufficient-condition theorem alone does not supply its
necessary direction. SP114 requests the explicit shifted-Taylor identity,
factorization through `Fin (d+1)` and rank bound together; degree controls a
width upper bound, not rank equality or minimal width. Finite-column typing and
the arbitrary-row generalization are disclosed. All prose, requested proof
methods and physical/resource interpretations require separate assessment.

Source statements/definitions, semantic reconstruction and actual kernel checks
remain separate. The normalized ambient interfaces added after the first blind
decode are explicitly labelled; earlier local packets and probe failures are
preserved. No new source-module audit, finite-bit compiler or circuit-resource
certificate is inferred from these exercise roots.

## Graphs and curriculum edges

`topology` describes the evaluator-supplied AND-obligation graph. It does not
claim to extract Lean proof-term dependencies or measure semantic reasoning
depth. The snapshot also contains module imports/ownership, conceptual and
planned relations, with their own evidence boundaries. They are not silently
converted into theorem implications.

Single roots, chains, AND joins and reused interfaces are explicit. A transitive
reuse triangle is not labelled a genuine diamond: that requires incomparable
branches with a shared ancestor and later reconvergence. Missing shapes remain
in the next-batch frontier; nodes are not padded to manufacture coverage.

Course prerequisites are recommended pedagogical edges, not extra theorem
hypotheses or claims of actual proof dependence. They cannot run from a later
evaluation split into training. Export ordering respects prerequisites, including
same-band prerequisites; filtered stages list omitted prerequisites without
injecting their answers. Existing splits are never silently reassigned.

Coverage reports count exact task anchors and their source files in the frozen
snapshot. Its full declaration inventory is an audit denominator, not an estimate
of how many valid or reviewed questions can be generated. Task review does not
clear an entire legacy node/module's source-semantic audit debt. Withheld and
planned nodes remain outside current gold.

## Commands

Run from the repository root. Every audit/export revalidates the recorded
reference qualification:

```sh
python benchmarks/quantumcomputingbench/scripts/lean_course.py audit
python benchmarks/quantumcomputingbench/scripts/lean_course.py export \
  --split train --output _out/lean-course-train.json
python benchmarks/quantumcomputingbench/scripts/lean_course.py export \
  --band D3 --output _out/lean-course-D3.json
python benchmarks/quantumcomputingbench/scripts/lean_course.py run-fixture \
  --view qcb-course-be-105-v1 --episode-dir ../qcb-eval-private/be105-course-fixture-fresh
```

Exports contain fixed questions/targets and answer-free protocol state. They
omit reference proofs, controls, negative proofs, source comparison verdicts
and grading answers. References remain public elsewhere; this is not a blind
test. The fixture command uses a simulation verifier and measures no Lean or
model performance.

## Actual first-expansion checkpoint

The [reference receipt](../../reports/lean-course-v1/reference-checks.json)
records 37 actual Lean checks over the five added companions: 13 positive
obligations, nine standalone controls, ten expected type/axiom rejections and
five distinct final-root replays. All positive axioms are within the standard
approved set. Four new mathematical roots have a distinct blind decode and
source-aware comparison; the SP009 calibration reuses its unchanged canonical
native alignment. Every whole-question explanation/method boundary remains
visible rather than inferred from a successful proof.

This replay ran at commit `d4660e0a9ff9a45cac7b35c89021f199ec600d31`, with
Lean 4.29.1 in the matching pinned cached production tree. Fresh `lake build`
and `lake build Tests` passed afterward, with existing linter warnings. Later
reader-only hardening rejects contradictory receipt flags, malformed axiom
lists, copied final-replay identities and incomplete pipeline maps. It does not
relabel the earlier run as execution of the newer reader. The historical Git
blobs stay checked and `recorded_pipeline_matches_current_sources` is false for
that complete recorded pipeline after the reader/CLI changes.

The supplied graphs cover single roots, chains, AND joins and shared interfaces.
A genuine incomparable-branch diamond is still a visible coverage gap. The
current nine cores anchor 20 snapshot declarations in six source files; this
does not clear whole-module review debt or certify a capacity for thousands of
questions. No measured model score, new mathematical core, canonical formal
admission or stable publication is produced by this course checkpoint.

The authored replay requires the reviewed pipeline to be committed, all semantic
inputs bound, and the matching already-built Lean checkout:

```sh
python benchmarks/quantumcomputingbench/scripts/lean_course.py check-references \
  --build-root PATH_TO_MATCHING_BUILT_CHECKOUT --trusted-local-reference \
  --output _out/lean-course-authored-fresh.json \
  --raw-output ../qcb-eval-private/lean-course-authored-raw-fresh.json
```

It checks every provided obligation, wrong-target and `sorryAx` controls, a fresh
final replay and standalone comparison roots. Standalone controls are checked
once in fresh compiler processes; they are not relabelled as completed
two-check protocol sessions. Budgets and actual check counts must be reported
with that distinction. Raw diagnostic trajectories stay outside the repository;
outputs must use fresh paths. Finish proof-bearing batches with `lake build`
and `lake build Tests` in the matching production tree.

Real model-generated Lean remains blocked pending accepted isolation. The course
does not contact administrators, start GPU training, merge the development PR,
publish a stable release or deploy the website.

## Next bounded batches

[backlog-v1.json](curriculum/backlog-v1.json) reserves source-bound inspection
targets in LCU/permutation composition, Hermite analytic prerequisites and
reversible-oracle semantics. It preserves existing contracts and splits; its
entries have no prepared reference proof, calibrated difficulty or current-gold
status. Select a coherent group, seal its literal statements, perform the same
semantic roundtrip, then replay its authored references before extending the
qualified course. Missing formal interfaces remain obstructions rather than
convenient extra public hypotheses.
