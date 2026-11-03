# QuantumComputingBench

Graph-grounded quantum-computing QA for training and evaluating specialized
mathematical models, backed by QuantumComputinglib's sources and graph.

Current distribution: **v0.1.0-preview.1**. This is a working public preview,
not complete whole-graph coverage or a newly certified mathematical teacher.
See the [integration/release notes](docs/integration-release-2026-10-22.md).
The [latest field/tensor/entry-ledger checkpoint](docs/textbook-field-tensor-and-entry-ledgers-2026-10-23.md)
clarifies abelian-irrep dimension, field-valued characters, algebraic versus
metric swap decompositions, universal tensor-square reducibility and the full
original-entry-query cost of amplitude loading.
The preceding [topology/coherent-record checkpoint](docs/textbook-topology-and-coherent-records-2026-10-23.md)
separates convex extremality from topological boundary, equivariance from
linearity, clean union projectors from physical register sharing, and joint
coherence from a signal marginal. It also corrects excess versus total copy
counts without changing that question's contract.
The preceding [symmetry/search checkpoint](docs/textbook-symmetry-and-search-boundaries-2026-10-23.md)
separates invariant states from symmetric support, pointwise from minimax
statistics, normalized blocks from arbitrary scales, and windowed search
guarantees from unconditional growth or certainty claims.
The preceding [convention/guard-count checkpoint](docs/textbook-convention-and-guard-count-checkpoint-2026-10-23.md)
explains explicit premise revisions, the actual Hermite producer's sharp
exponential-call count, and substantive revalidation of code-bound reviews.
The preceding [operator/bond checkpoint](docs/textbook-operator-and-bond-boundaries-2026-10-23.md)
explains clean projection versus cleanup, phase-aware compilation, finite
support/permutation domains and actual producer bounds. Shared cross-split
answer fragments remain subject to reconciliation. The preceding
[Hermite rank/regularity checkpoint](docs/textbook-hermite-rank-and-regularity-2026-10-23.md)
explains threshold domains, exact-real versus finite-bit resources, indexed
smoothness and bounded historical reconciliation. The preceding
[Hermite/directed-qubitization checkpoint](docs/textbook-hermite-and-directed-qubitization-2026-10-23.md)
explains actual endpoint/grid dependencies, directed maps, projected outputs and
compatible continuation. The earlier
[quantum-contract checkpoint](docs/textbook-quantum-contract-checkpoint-2026-10-23.md)
records source/answer repairs and their remaining obligations. The
[polynomial/converse checkpoint](docs/textbook-polynomial-and-converse-checkpoint-2026-10-23.md)
remains available as historical evidence.

## Hierarchical exercise book

The website reader organizes the retained native cores into five parts:
shared foundations, State Preparation, Block Encoding, Quantum Information,
and Quantum Scientific Computing. Part pages lead to topics, then canonical
exercise pages with assumptions first and hints, solutions, rubrics and evidence
folded by default. It uses the existing QuantumComputinglib textbook shell.

- [Mathematical reader (no Lean required)](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/non-lean/)
- [Lean companion and diagnostic warmups](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/lean/)
- [Shared core and split contract](shared/CONTRACT.md)
- [Non-Lean collaborator goal](tracks/non-lean/AGENT_GOAL.md)
- [Lean collaborator goal](tracks/lean/AGENT_GOAL.md)

These are two views/contribution tracks, not duplicate datasets. Existing core
contracts and splits are preserved; new UUID proposals remain uncounted until
semantic admission. The reader is an editorial checkpoint, not a relabeling of
the preview as stable. Inspect the remaining acceptance gates with:

```sh
python benchmarks/quantumcomputingbench/scripts/curriculum.py validate
python benchmarks/quantumcomputingbench/scripts/curriculum.py export --output _out/qcb-cores.json
python benchmarks/quantumcomputingbench/scripts/curriculum.py export-reader --output _out/qcb-reader.json
python benchmarks/quantumcomputingbench/scripts/curriculum.py stable-check
```

`stable-check` intentionally exits 2 while reviews/reconciliation remain pending.
No broad whole-graph completeness, new isolated evaluator or model baseline is
implied by the website presentation.

The first [native Lean companion batch](tracks/lean/README.md#first-native-formal-view-batch)
contains three aligned library-lemma applications over existing core IDs.
Source-blind decoding, independent comparison and actual reference/axiom checks
are separate evidence records. They are not three new questions, deep proof
synthesis results, or kernel certification of the entire NL explanation.

## Lean-enabled agentic evaluation

The [experimental evaluator](tracks/lean/EVALUATOR.md) exposes four
reference-qualified proof-task views with fixed shared IDs, scoped premise
retrieval, provided proof obligations and repair/final-replay protocols. Its
[handoff](tracks/lean/LOCAL_PILOT_HANDOFF.md) separates actual authored Lean
evidence from synthetic scheduling tests and unmeasured model performance.
Offline profile templates and validation prepare bounded model configurations;
model-generated formal proofs remain gated on accepted isolated execution.
The canonical catalog and public-preview release status are unchanged.

The [staged Lean course](tracks/lean/COURSE.md) extends that pilot to 13
existing cores with explicit mathematical-construction bands, prerequisite and
split checks, source-node coverage and answer-free exports. Its reference
qualification is separate from canonical formal-view admission and empirical
model-difficulty calibration.

## Audited mathematical corrections

<details>
<summary>Exact repairs, historical boundaries and replay evidence</summary>

**Current textbook corrections:** fresh State Preparation reviews found an
input/output bond-index defect (`sp-002`), an unsupported arbitrary-signed
loader claim (`sp-006`), and a terminal active-dimension feasibility error
(`sp-011`). [Current policy](shared/current-policy.json) withholds those exact
predecessors and admits only separately reviewed additive successors, including
their explanatory summaries/steps when affected. Frozen
preview assets remain historical, not automatically current gold. Their native
scoring/repackaging entry fails closed until a separately versioned data release
is prepared. The current reader export preserves the original core and split.

**Further reader review:** exact rejected or ambiguous questions/answers are
withheld through the same [bound current policy](shared/current-policy.json),
without inventing a replacement. Their core IDs, contracts and splits remain
reserved for corrections, and old links display a withdrawal notice rather than
an unapproved answer. Current reader/search exports exclude these records.
Withdrawal does **not** remove a core from the stable-release review obligation.
All historical content and the substantive findings remain inspectable.

**Explicit question versions:** an answer-only repair cannot fix a false question
by silently proving a weaker target. The [LA206 version-2 successor](shared/repairs/la-206-cost-contract-successor.json)
asks the reader to refute literal budget equality, derive the actual-cost sum,
then prove the upper bound and same-run LQ identities. Its
[distinct contract-change review](reports/textbook-v1/repairs/la-206-cost-contract-successor-review.json)
binds both question contracts. Core/family/split stay reserved; the registry and
page disclose the change, and an old-hash Lean companion is rejected as stale.
The predecessor remains audit history, not an equivalent second exercise.

The [SP108](shared/repairs/sp-108-question-degree-successor.json) and
[SP111](shared/repairs/sp-111-question-degree-successor.json) version-2 questions
retain the original false degree assertions for explicit assessment. They then
ask for the correct endpoint-factor degree or squared-affine degree bound,
including endpoint and zero-step cases. Their distinct exact-content reviews
preserve the same core/family/split and do not transfer old formal companions
or claim that existing elevation/mass lemmas prove every new obligation.

The [fixed Lean support](reports/textbook-v1/repairs/fixed-references/WideLQCostContract.lean)
and its [actual receipt](reports/textbook-v1/repairs/fixed-references/wide-lq-checked-receipt.json)
check the general actual-cost identity and actual/budget emit mismatch, including
sorry and wrong-target negative controls. These three roots are not another
native formal-view admission. Replay only the inspected reference using
`scripts/wide_lq_contract_reference.py --build-root PATH --trusted-local-reference --output NEW_RECEIPT`.

The [oracle/composition, representation and scientific-algorithm reviews](reports/textbook-v1/reader-reviews/)
also separate phase-aware programs from bare gate products, unitary composition
from deterministic cleanup, finite-dimensional representation hypotheses from
unrestricted claims, and original bit-oracle costs from derived angle-oracle
costs. Primary-source access limits are recorded honestly. Earlier scientific
reader batches inspected primary text without freshly verifying its binary
hash; those reports are unchanged. The later exact repair reviews below did
independently retrieve matching bytes, without retroactively approving the
whole source or every earlier derivation.

Three [reviewed answer repairs](shared/repairs/) restore the original questions:
BE102 distinguishes actual dirty-input failure from absence of a clean-input
certificate; plan107 retains the right adjoint in the Pauli twirl; plan204
retains the complex conjugate and derives the full positive-POVM spectrum.
Their exact [independent reviews](reports/textbook-v1/repairs/) cover the whole
answer, rubric and explanatory steps, not only an isolated corrected formula.
No real-overlap, full-rank or extra oracle premise was added.

Further exact repairs distinguish genuine physical ensemble variation from
isometry redundancy, establish the Werner separable converse by an explicit
product twirl, and retain the source Young-symmetrizer action order. See the
[checkpoint](docs/textbook-polynomial-and-converse-checkpoint-2026-10-23.md) and
the content-bound reviews; these are source-only mathematics, not new Lean views.

The [dirty-work support source](reports/textbook-v1/repairs/fixed-references/DirtyWorkBoundary.lean)
and [actual receipt](reports/textbook-v1/repairs/fixed-references/dirty-work-checked-receipt.json)
check four named roots for the fixed seven-wire program: unconditional entering
work/row preservation and two distinguishing dirty-input examples. The allowed
axioms and real sorry/wrong-target controls are recorded. This does not create
four native Lean views or certify arbitrary-width adders or all quantum prose.
Replay only the inspected source using
`scripts/dirty_work_boundary_reference.py --build-root PATH --trusted-local-reference --output NEW_RECEIPT`.

The [linear-algebra and stored-cost second pass](reports/textbook-v1/reader-reviews/)
also distinguishes strict staircase zeros from diagonal entries, generated
backend counts from optimal-synthesis lower bounds, upper budgets from actual
costs, and maximum-bond bounds from attained dimensions. The reviewed
[supplier-bound repair](shared/repairs/la-214-uniform-supplier-bound-repair.json)
uses an arbitrary-work family at fixed matrix dimensions; the
[angle-cost repair](shared/repairs/la-215-branch-cost-repair.json) distinguishes
all three execution branches. Exact predecessor findings remain in history.

The [inspected fixed-reference source](reports/textbook-v1/repairs/fixed-references/StoredCostRepair.lean)
and [actual receipt](reports/textbook-v1/repairs/fixed-references/checked-receipt.json)
support these two repairs with seven named Lean roots and two real negative
controls. Three roots check concrete branch representatives; they do not replace
the independent universal control-flow argument or certify every NL sentence.
These are support checks, not additional native Lean views or isolated model
evaluation. To replay only this inspected source against a matching built tree,
choose a new receipt path rather than overwriting published evidence:

```sh
python benchmarks/quantumcomputingbench/scripts/cost_repair_references.py \
  --build-root PATH_TO_MATCHING_BUILT_CHECKOUT --trusted-local-reference \
  --output _out/cost-repair-recheck.json
```


</details>

## What is ready

| Cohort | Current scope | Evidence and use |
| --- | --- | --- |
| Frozen native preview, `nl-v12` + integration admission overlay | 213 preview core IDs from 238 active records; 21 provisional + 4 integration quarantines | Historical public distribution, before subsequent current-reader withdrawals; not automatically current gold |
| Legacy, `release-v3` | 26 inherited-review diagnostics | Separate public diagnostic cohort, not pooled native training |
| Legacy provisional | 12 repaired/new diagnostics plus 8 other historical candidates | Preserved for review; not released gold |
| Fixed Lean references | 16 checked claims and 3 reference application harnesses | Formal reference evidence, not certification of all NL answers or untrusted predictions |
| Coverage universe | 5,153 nodes with dispositions | A denominator/ledger, not 5,153 questions or completed coverage |

Frozen preview evidence remains separated: 60 local-source-supported answers, 53 original
NL bridges and 100 primary-source NL-only answers. Native train/dev/public-test
counts are **74 / 21 / 118**. Current-reader totals and exclusions are generated
by `scripts/curriculum.py validate`; do not reuse the frozen totals as current
reader counts. Nine historical admitted same-core repairs do not add cores.
The questions require mathematical understanding, not Lean syntax or API recall.

The four integration quarantines concern square roots/instruments, a PPT
dimension boundary, a trace-norm argument/scalar counterexample and a tensor-action
convention. The [bound admission audit](manifests/integration-20261022/admission.json)
retains exact item digests and reasons. Frozen `nl-v12` files and their 217-item
historical admission records remain unchanged; they are not the current gold set.

Cross-cohort semantic core reconciliation and actual external Lean-collaborator
acknowledgment remain pending. We deliberately publish **no aggregate distinct-core
count** and no combined training split. The preview co-releases preserved cohorts;
it does not fabricate shared-core approval.

The [first bounded cross-cohort audit](reports/textbook-v1/cohort-reconciliation/review-at-8533b9b.json)
records its prior selection snapshot, a confirmed same-core pair and cross-split
mechanism overlap. It is not exhaustive global deduplication, does not approve
unlisted pairs, and predates the current withdrawals and latest answer repairs.
Its historical inventory count must not be reused as the latest reader count.

The [first-eight refresh](reports/textbook-v1/cohort-reconciliation/review-at-policy-adbf736a-first-eight.json)
binds a later exact policy snapshot, reuses sixteen earlier comparisons without
counting them again, and examines five omitted candidates. The newly identified
controlled-inverse specialization crosses separate legacy/native splits but is
not a whole-question alias. This remains partial evidence, not authorization to
pool cohorts or a claim that a subsequent question version inherits its digest.

**Isolated untrusted Lean evaluation: ENV_BLOCKED. Real-model baseline: UNMEASURED.**
Source inspection, successful execution, useful progress, formal correctness and
faithful NL explanation are different evidence classes.

## Quick start

Use Python 3.11 and a full Git checkout, not a source ZIP without history:

```bash
python -m pip install -r benchmarks/quantumcomputingbench/requirements.txt
python -m unittest discover -s benchmarks/quantumcomputingbench/tests -v
python benchmarks/quantumcomputingbench/scripts/release.py validate
```

The entry validates the historical preview, source/review bindings and canonical
paths, and separately reports current reader decisions. The historical packaging
command below now fails closed while a withdrawn predecessor differs from the
reader; do not overwrite the existing tag or bypass this guard:

```bash
python benchmarks/quantumcomputingbench/scripts/release.py build
```

Outputs under `_out/qcb-release/`: a deterministic data ZIP, `SHA256SUMS`, and a
commit-bound manifest. The ZIP separates native splits, answer-free prompts,
legacy diagnostics, provisional audit material and provenance. It is a data
distribution; source-bound validation/scoring still needs the full repository.

## Data, scoring and review

- [Current admission overlay](manifests/integration-20261022/admission.json),
  [frozen native source release (historical admissions)](data/public/nl-v12/release.json),
  [provisional queue](manifests/nl-v12/review-queue.json), and
  [native dataset card](docs/native-nl-dataset-card.md).
- [Imported native coverage](reports/nl-v12/coverage.md) and
  [historical summary](reports/nl-v12/summary.json); use `release.py validate`
  for current admission counts and `build` for current data exports.
- [Legacy release](data/public/release-v3/release.json),
  [legacy dataset card](DATASET_CARD.md), and
  [mathematical repair audit](docs/repair-review-2026-10-21.md).
- [Core coordination proposal](docs/nl-collaborator-handoff.md) and
  [whole-graph authoring objective](AGENT_GOAL.md).

Predictions are JSON arrays of `{"id":"qcb-...","answer":"..."}`:

```bash
python benchmarks/quantumcomputingbench/scripts/release.py score \
  --cohort native --predictions ../predictions.json --ratings ../ratings.json
# Explicitly separate legacy diagnostics:
python benchmarks/quantumcomputingbench/scripts/release.py score \
  --cohort legacy --predictions ../legacy-predictions.json
```

NL explanations require actual content-rubric ratings bound to item/prediction
hashes and separate fidelity judgments. Reference copying, keywords and length do
not automatically earn credit. Fixtures are not model results. Public test
questions and answers are reproducible diagnostics, not blind, secret or
contamination-free assessment; model pretraining exposure is unknown.

Known withdrawn legacy/native answers remain in history for audit but are excluded
by current scoring. Use the current release entry, not historical commands to
resurrect old gold. Frozen QA, source hashes and review artifacts are preserved;
the [explicit compatibility ledger](manifests/integration-20261022/compatibility.json)
admits only the exact attribution update and restricted loader substitutions.
Original and current code are not falsely described as byte-identical.

## Lean reference evidence and safety

With the pinned toolchain and dependencies provisioned:

```bash
python website/scripts/run_lean_gate.py
python benchmarks/quantumcomputingbench/scripts/check_references.py \
  --trusted-local-reference --output ../qcb-local-reference-checks.json
```

Only inspected fixed reference sources may use this local path. Never send model
output to it. Complete proofs, frozen targets/imports and transitive axiom checks
are required; empty goals, exit code zero or searching for the word `sorry` are
insufficient. Local fixed-reference checking does not provision a sandbox.
The container evaluator stays disabled until its real pinned-image integration
tests pass.

The [integration reference replay](reports/integration-20261022/lean-reference-checks.json)
records the fresh 16-root/three-harness check and both actual negative controls,
bound to the identical 202-module production/test proof tree.

## Continue contributing

Keep changes under this benchmark directory on separate working branches. Use
successor versions rather than overwriting frozen data or hashes. One mathematical
core spans NL/Lean/hybrid views, paraphrases and trivial parameter variants.

```bash
python benchmarks/quantumcomputingbench/scripts/authoring_packets.py \
  --version release-v3 --batch-size 8
```

Packets are resumable source-bound starting points, not generated QA or released
coverage. Inspect complete source statements and definitions. Module imports and
ownership are not theorem-proof dependencies; Hypergraph transports retain all AND
premises and failure boundaries. Keep planned/source-only topics distinct from
local formal closure, and measure primary targets separately from incidental
support.

Historical files and contributor records are retained. Duplicate root-level
uploads were moved to the canonical namespace only after equality checks; see the
[path migration ledger](manifests/integration-20261022/path-migration.json).
Original authored QA/code use repository MIT terms; external-source rights remain
separate. No PDFs, credentials, private gold, raw generations, paid API calls,
training jobs or GPU experiments are part of this release.
