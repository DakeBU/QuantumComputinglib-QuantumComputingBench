# From complete measurement operators to a coherent branch map

Status: **proved_locally, independently reviewed preparatory library candidate**
on Lean 4.33.0. This directory is not a production import, main admission,
refreshed production graph, complete QA formal view, or PURIFIED result.

## What the result means

Let $M_i:E\to F$ be a finite family of bounded complex-linear maps between
Hilbert spaces. Assume input-side completeness:

$$\sum_i M_i^\dagger M_i=I_E.$$

The earlier [completeness fragment](../measurement-completeness/README.md)
proves that the squared lengths of all branches add to the input squared
length. This package uses that result to assemble the actual full tuple

$$V_M\psi=(M_i\psi)_i\quad\text{in}\quad\bigoplus_i^{\ell^2}F.$$

This is a complex-linear isometric embedding. It retains the branch vectors
and their phases, not just their probabilities. Consequently, for any two
inputs,

$$\sum_i\langle M_i\psi,M_i\phi\rangle=\langle\psi,\phi\rangle.$$

The output coordinates are orthogonal in the mathematical Hilbert product;
no physical outcome-register or tensor-layout identification is proved here.
Individual branches need not be isometries. The combined map need not be onto,
so it is not automatically a unitary operation.

## The short mathematical proof

The tuple map is linear because each component is linear. Mathlib's existing
Hilbert-product norm formula and the earlier completeness theorem give

$$\|V_M\psi\|^2=\sum_i\|M_i\psi\|^2=\|\psi\|^2.$$

Both norms are nonnegative, so their equality of squares gives equality of
norms. This supplies the norm-preserving field of Mathlib's `LinearIsometry`.
Its existing inner-product-preservation theorem then supplies the displayed
complex overlap identity. No second adjoint-sum proof, measurement structure,
state wrapper, or tensor API is introduced.

The finite outcome type may be empty; the input/output spaces may be zero,
infinite-dimensional, or different. Completeness itself rules out impossible
cases. There is no input normalization, nonzero branch, finite-dimensionality
or surjectivity hypothesis.

## Exact Lean interfaces and observed reuse

The full source is `QuantumBlockEncoding/MeasurementCoherent.lean`; its namespace
is `QuantumBlockEncoding.MeasurementCoherent`. The exact checked signatures are
in `evidence/checked-signatures.txt` and the pre-proof interface in
`STATEMENT_SEAL-v1.md`.

- `branchIsometry`: the actual map into Mathlib `PiLp 2`.
- `branchIsometry_apply`: its literal coordinate action; simp bookkeeping, not
  an independent mathematical discovery.
- `sum_inner_eq`: the full-overlap consumer of that assembled isometry.

`evidence/parent-helper-graph.json` observes the public roots and their bounded
generated-helper slice. Lean outlines the norm proof, so the actual reuse path
is `branchIsometry` → `branchIsometry._proof_11` → the predecessor
`MeasurementProbability.sum_norm_sq_eq`. The overlap proof directly references
the isometry. These are observed constant references, not a whole-library,
minimal-support, or scientific-novelty graph. Generated proof helpers do not
become additional mathematical nodes in the compressed reader view.

## Evidence and limits

Actual Lean 4.33 runs compiled a fresh exact predecessor, selected that own
provider, compiled the unchanged new source and selected its own provider in
real consumers. Superposition, injectivity and orthogonal-input consumers
compile. Complete types and the four required axiom observations were checked;
the observed axioms are exactly `propext`, `Classical.choice`, `Quot.sound`.
The wrong adjoint-order fixture was rejected with the actual expected/received
type mismatch; its secondary noncomputability diagnostic is retained too.

Source-blind reconstruction and a distinct static semantic/canonicality review
are separately bound under `reviews/`. The latter did not claim independent
compilation. A separate decoder public display removes only private path
spellings and preserves its original hashes and real run identity.

Memory-preflight stops, the capped exporter failure, an invalid display-option
probe, and the parent's too-strong direct-root-edge expectation are retained as
separate failures. A separately recorded 2048 MiB helper-observation continuation
succeeded without changing the source or rewriting those records. Raw local
outputs may contain host paths and are not public artifacts.

This is an original small interface contract using existing Mathlib mathematics,
not a novelty claim or an AxQM source-theorem equivalence. The pinned AxQM
attribution remains in the predecessor and its technical card. No private
benchmark solutions or new external code are imported.

## Production Graph, QA and integration obligations

`GRAPH_DELTA.json` and `QA_SUPPORT.json` are explicit pending-admission records.
They reuse existing identities, not a second graph or completion ledger. No new
QA core, train example, split move or frozen answer rewrite is introduced.
Existing public-test cores plan-201/202 receive only a partial-support proposal.
POVM square-root and block-branch adapters, register factors and conditional
mixed-state update are not silently supplied by this isometry.

Before formal production admission: select the canonical import location, bind
both complete modules and the current source/dependency context to their honest
independent evidence, establish the downstream textbook use, and pass the real
library/Tests/publication/site/reader gates. Then review the production graph
and QA snapshot update and perform purification/Exposition Seal. Current main
and this preparatory Lean 4.33 evidence are reported separately.

Tensor registers, unitary extension/dilation, density/trace semantics,
instruments/channels, selected-branch normalization, circuits, oracle access,
ancilla cleanup, resource counts and finite-bit implementation remain outside
this result. Their absence does not refute the mathematical interface, but
future claims about them require their own certificates.

## Independent portable replay

The parent ran the fixed-source portable runner in a new output directory.
It freshly recompiled the predecessor and this module, selected their own
providers, compiled the consumers, printed the full signatures and the four
ordinary-axiom observations, rejected the wrong completeness orientation and
successfully observed the bounded helper graph. The public-safe receipt is
`evidence/portable-replay-c409.json`; its graph is
`evidence/portable-helper-graph.json`. All fourteen launch stages passed their
specified checks (the expected negative control exits 1). This is a second
source-bound focused execution, not an independent semantic review or a clean
transitive Mathlib rebuild.

The initial portable attempt remains in
`evidence/portable-replay-c408-failed.json`: Lean emitted a legitimate repeated
non-owned `Init.olean` dependency, which the first parser rejected. The corrected
parser still requires exactly one own provider and rejects foreign or malformed
providers. Twenty-one static regressions pass. Neither this tooling correction
nor its successful replay changes the mathematical source, acceptance roots,
axiom policy, production graph, QA gold or main admission status. The original
author handoffs retain their original limited graph status; the parent's
successor `PARENT_CHECKPOINT-v3.json` binds these later observations separately.
All transported source, review and runtime evidence bytes retain their exact
hashes, including the runtime records' original line separators. The decoder's
separately bound public display remains the only declared content derivation;
transport itself is not another execution or review.
