# Worker handoff v2: compiled finite coherent branch isometry

This successor changes the evidence/status of `HANDOFF.md`, not the frozen
statement or implementation. The earlier environment-blocked handoff and all
failed attempts remain immutable. No source/proof-body repair was needed.

## Objective / mathematical delta / frontier effect

**Locally proved preparatory Class-B candidate:** an actual complex-linear
isometry from input Hilbert space into the canonical Mathlib finite Hilbert
direct sum, consuming the reviewed completeness root. This advances the
mathematical frontier from scalar total squared norm to the full coherent
branch vector and its preserved complex cross-overlaps. It does not establish
production admission, a tensor-register or physical dilation, circuits or costs.

For the full frozen ambient context in `STATEMENT_SEAL-v1.md`, the three exact
compiled interfaces are:

```lean
noncomputable def branchIsometry (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) :
    E →ₗᵢ[ℂ] PiLp 2 (fun _ : ι => F)

@[simp] theorem branchIsometry_apply (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) (i : ι) :
    branchIsometry M hM ψ i = M i ψ

theorem sum_inner_eq (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ φ : E) :
    ∑ i, inner ℂ (M i ψ) (M i φ) = inner ℂ ψ φ
```

Names are in `QuantumBlockEncoding.MeasurementCoherent`.
`evidence/checked-signatures.txt` is the actual successful full-type output,
including all universes and typeclass binders; it matches the pre-proof seal.

## Exact source / pre-proof bindings

- Source: `QuantumBlockEncoding/MeasurementCoherent.lean`, SHA-256
  `22ef9784a3fe636b9ea07cf622bce01572425e2706e540e547934ec078dba34c`.
- Statement seal v1: SHA-256
  `dfeff3145f5f0bf3010b4ad211e80bbc679551607635f2da2e24138e919661e3`.
- Source-blind formal packet v1: SHA-256
  `2a1af6af46029820d070b3818a787b74414a28224acc976bf01265f88342aa79`.
- Exact reviewed predecessor source: SHA-256
  `33c1a01b8f1e752f22acbc12ae47faa503e5dc7ae5f3f4d73dff39eeb9505775`.

`BINDING-v2.json` binds the focused runtime and all supporting Lean inputs.
Portable runtime evidence SHA-256:
`e421693627d277a154e6ed6ca3633c81bdfcf1cc5a231c60562bf9b83be0cbd6`.
The source and both pre-proof files are unchanged across every attempt.

## Actual successful evidence

Attempt-03 used the exact Lean 4.33.0 binary, explicit `LEAN_PATH` with its own
output first and package providers only (no production project build path).
It freshly compiled the exact predecessor, selected that `.olean` in the new
module's `--deps`, compiled the unchanged isometry source, selected that new
own `.olean` in the consumer's `--deps`, and compiled the consumer.

- Fresh predecessor `.olean` SHA-256:
  `625af00c28111098ce09150cdbeea0ea8163b4ba24202acdc96ebac52f8f445c`.
- Fresh coherent `.olean` SHA-256:
  `a4f93ddc6d788a6260c00306cccad7d518596e94deb6f606048421ea01ff1c4a`.
- Source compile: 18.563 seconds, exit 0. Predecessor: 46.375 seconds, exit 0.
- Consumer: 17.437 seconds, exit 0. Its tests use actual isometry linearity and
  injectivity, and the finite overlap theorem for orthogonal inputs.
- The predecessor root and all three new roots have actual axiom observations
  exactly `propext`, `Classical.choice`, `Quot.sound`; no additional axiom.
- Continuation-05 selected the same exact own provider, successfully printed
  every complete root type (17.891 seconds, exit 0), and rejected output-side
  completeness as an input-side completeness argument (19.25 seconds, exit 1).
  The actual expected/received adjoint-order type mismatch is retained;
  a secondary noncomputability diagnostic is retained too, not suppressed.

Every launch used one compiler at a time, `-j1`, 1536 MiB cap and 120-second
timeout, after measuring at least 5120 MiB available. No reserve or cap was
changed. The source gate passed on the first actual proof compilation.

## Preserved failures and precise classifications

1. Attempt-01: 4588 MiB available; `ENV_BLOCKED`, no compiler launched.
2. Attempt-02: 4654 MiB available; `ENV_BLOCKED`, no compiler launched.
3. Attempt-03 expression exporter only: interpreter memory exception at fixed
   1536 MiB cap, exit 3221226505, 20.735 seconds. Specific class `ENV_BLOCKED`.
   The generic runner's original raw label `IMPLEMENTATION_FAILED` is retained
   unchanged and explicitly distinguished in portable evidence. Source and
   consumer success are not erased by this graph-only diagnostic failure;
   whole replay success is nevertheless false. **No exact-root expression
   graph is available**, and source-level references are not relabelled as
   expression-observed dependencies.
4. Continuation-04: unknown display option `pp.width` in the separate signature
   probe. Specific class `IMPLEMENTATION_FAILED`; its generic raw label
   `ENV_BLOCKED` remains unchanged. Removing only that display option produced
   continuation-05 success. The core source/contract did not change.

Raw commands/host paths, snapshots and result records remain under `PRIVATE/`.
The public-safe summary contains logical paths only. It binds raw hashes while
reporting the specific classifications honestly. The negative control output
is sanitized only by deleting its exact absolute directory prefix.

## Genuine consumer, reuse and assumptions

The central consumer is the actual coherent `LinearIsometry`, not a normalized
probability conjunction. It retains `M_i ψ` as complex amplitudes in every
coordinate, so generalized measurement/POVM reasoning can preserve coherent
superpositions before forgetting outcomes. The finite cross-overlap formula
exhibits preservation of interference/orthogonality between distinct inputs.
It is proved through the checked isometry's existing `inner_map_map`, not a
second local operator-family argument. If canonicality review finds that
public formula unnecessary, move it to applications/tests rather than retain
wrappers for declaration counts; the actual map remains substantive.

Local production, Mathlib and attributed external-library cards were searched
before implementation. Mathlib directly supplies `PiLp 2`,
`PiLp.norm_sq_eq_of_L2`, `LinearIsometry`, `LinearIsometry.inner_map_map` and
`PiLp.inner_apply`. The predecessor supplies only
`MeasurementProbability.sum_norm_sq_eq`, as a dependency, not a new public
hypothesis. No exact duplicate was found by the bounded search; this is not
ecosystem-wide nonexistence or novelty evidence. Referenced external checkouts
were absent; no external code was imported/copied. The predecessor remains a
reviewed preparatory fragment with no production/main admission.

Finite outcomes may be empty. Hilbert `E,F` may be zero, infinite-dimensional
and rectangular. No normalized input, nonempty outcome, nontrivial space,
nonzero branch, probability, finite-dimensionality, equal-dimension or
positivity premise is added. Completeness remains input-side. The map is
literal, not chosen from an existence theorem, a representative or default
fallback. There is no new state/measurement/tensor API.

## Graph, purity and remaining obligations

Construction/source-level route: input completeness + exact operator family
→ predecessor squared-norm identity + literal PiLp linear map + canonical
PiLp norm identity → actual `LinearIsometry` → canonical inner-product
preservation → finite cross-overlap formula. This original contract is not
an AxQM source theorem equivalence. The failed expression observer supplies
no additional machine graph claim.

All tensor-register identification, ancilla preparation/cleanup, unitary
completion/dilation, density/trace/Born adapter, normalized branch update,
instrument/channel, circuit/oracle, resources and finite-bit claims remain
outside scope. Only this preparation directory was written; no production,
Git, benchmark/split, dependency/toolchain or web changes were made.

The parent is coordinating independent decoder `finite_branch_blind_c404` and
distinct semantic reviewer `finite_branch_semantics_c405`; their verdicts are
not asserted by this formalizer. Full whole-module publication binding,
repository/Tests, reader/site/integration gates and post-merge purification
remain required. Graph-only diagnostics may be continued separately under a
separately recorded resource envelope, without rewriting this capped run or
changing source. No full integration, `PROOF_SEALED`, main admission, QA gold,
`PURIFIED` or Exposition Seal is claimed.

Process memory: `QBE-PM-LOW-TOKEN-CONTROL-PLANE`,
`QBE-PM-VERIFIER-SEMANTIC-LEVEL`. Direction fingerprint:
`finite-operator-family-to-canonical-PiLp2-linear-isometry`. Expected information
gain is now resolved positively at the bounded focused Lean layer. No subagents
were spawned by this worker. One mathematical route was used; no comparative
efficiency or multiple-route common-blind-spot review is claimed. Salvage:
retain compiled source/consumer/provider/axiom evidence; preserve the graph gap
and tooling failures separately. Default route: canonical PiLp/LinearIsometry
reuse. Recommended next frontier: independent review and an exact admitted
shared-node integration, not a premature circuit/dilation extension.
