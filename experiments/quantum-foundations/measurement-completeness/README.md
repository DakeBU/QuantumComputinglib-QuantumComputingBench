# Measurement completeness: first shared-foundation intake

Status: **proved_locally / preparatory shared-library fragment** on Lean 4.33.0.
Not production/main admission, a refreshed public graph, stable QA gold, or
PURIFIED. Independent semantic acceptance is bounded to the two exact roots;
an independently useful non-wrapper downstream consumer remains required.

For bounded complex-linear maps \(M_i:E\to F\), assume
\[
\sum_i M_i^\dagger M_i=I_E.
\]
Then for every vector (normalized or not),
\[
\sum_i\|M_i\psi\|^2=\|\psi\|^2.
\]
For \(\|\psi\|=1\), the outcome weights form a finite probability family and
each belongs to \([0,1]\). Input/output spaces need not have the same dimension.
Empty outcome families and zero spaces are retained, without inventing a unit
vector or nonzero branch. There is no division by an outcome probability.

## The mathematical mechanism

Mathlib already supplies the adjoint and quadratic-form identity. Sum it:
\[
\sum_i\|M_i\psi\|^2
=\operatorname{Re}\left\langle
  \left(\sum_iM_i^\dagger M_i\right)\psi,\psi\right\rangle
=\|\psi\|^2.
\]
Every summand is nonnegative, so any one is bounded by the sum. No second
state, density, channel, measurement or tensor-system structure was defined.
The operator order is input-side \(M_i^\dagger M_i\); swapping it is invalid
for rectangular maps. This is not a new algorithm or a novelty claim.

## Source and existing ownership

The source correspondence is [AxQM Measurement.lean](https://github.com/Axiomatic-AI/AxQM/blob/2ccf167efca86eb5164f1df8cedb72b84626b479/AxQM/Basic/Measurement.lean),
commit `2ccf167efca86eb5164f1df8cedb72b84626b479`, Git blob
`1a078f8cd71d6b41c3e87bb70c763c3a2a628aa0`. Credit Axiomatic AI, Winston Yin
and Frank Koppens. Their code is Apache-2.0 with its NOTICE; this package
contains an independent local proof using existing Mathlib, not copied AxQM
code or private task solutions. The source's density/trace probability and
state-update API is **not** identified with this pure-vector substrate yet.
The referenced Nielsen-Chuang section was not freshly inspected here.

Existing `contrib/effect-probability-stability` at
`0bf8979ab4600d458288aa2c19eb95b065e2799a` owns prior distinct Born/effect
stability work. Its definitions and theorems are not recreated or claimed new.
OpenAI Math and the other QIT libraries remain separate pinned adapter inputs;
this batch does not silently import their state/measurement foundations.

## Exact Lean and graph evidence

- Source: `QuantumBlockEncoding/MeasurementProbability.lean`.
- Roots: `QuantumBlockEncoding.MeasurementProbability.sum_norm_sq_eq` and
  `QuantumBlockEncoding.MeasurementProbability.outcome_probability_mem_Icc`.
- `Canary.lean` checks a normalized-total/conjunction application. It is a
  smoke/repackaging consumer, not an independently completed source theorem.
- `proof-term-graph.json` observes the exact two compiled roots' type and proof
  references, including projection-structure names. It is a direct expression
  slice, not a transitive/minimal/whole-library dependency graph.
- `evidence/` retains independent source-blind reconstruction and separate
  semantic review, original seals and actual focused runtime records.
- `controls/` contains deliberately invalid fixed fixtures. Never import them
  into the library; they must not be counted as proved declarations.

Run `python replay.py --output _out/measurement-completeness-NEW` from a matching
Lean4.33 checkout with dependencies already provisioned. The command does not
install packages, alter targets, reuse an old success directory or run model
output. Its raw local diagnostics may contain host paths: do not publish the
output directory wholesale. Portable public evidence contains hashes and
logical command paths only.

## QA integration without duplicate cores

`QA_SUPPORT.json` points to existing `qcb-core-plan-201` and `qcb-core-plan-202`,
both in the public-test generalized-measurement family. It proposes **partial
support**, not new questions, new core IDs, complete equivalent Lean views or
new train examples. Their contracts, family and split remain unchanged. A
reviewed graph-snapshot refresh and actual square-root/block-branch adapters
are still needed; frozen benchmark snapshots and old reviews are untouched.

## Remaining admission and purification

Do not copy this into production and claim completion from focused compilation.
Finish a genuine downstream measurement/POVM consumer, whole-module publication
bindings, current complete library/Tests and reader/site gates under Lean4.33,
then graph/QA snapshot review and purification. Mixed-state trace equivalence,
instrument/update, dilation, circuits, resource costs and private AxQM task
solutions remain outside this package. The main branch's actual toolchain is
reported separately from the local 4.33 evidence.
