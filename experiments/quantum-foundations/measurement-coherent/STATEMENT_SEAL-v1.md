# Finite coherent branch isometry — statement seal v1

Frozen before proof implementation/search on 2026-10-23. Declaration class B:
canonical-library candidate, with an original mathematical interface contract.
This is not an AxQM source-theorem equivalence claim. Integration and independent
semantic/source-blind review are pending.

## Mathematical contract

Let `ι` be finite, possibly empty, and let `E,F` be complex Hilbert spaces,
possibly zero or infinite-dimensional and not necessarily of equal dimension.
For bounded complex-linear maps `M_i : E → F` assume the input-side equality
`∑ i, M_i† M_i = I_E`. Construct the literal map

\[
V_M:E\longrightarrow\bigoplus_{i\in\iota}^{\ell^2}F,
\qquad (V_M\psi)_i=M_i\psi
\]

as Mathlib's `LinearIsometry` with codomain `PiLp 2 (fun _ : ι => F)`.
The pointwise action must be proved. A finite cross-overlap identity must be
derived through this checked isometry, not a second operator-family proof:

\[
\sum_i\langle M_i\psi,M_i\phi\rangle_{\mathbb C}
=\langle\psi,\phi\rangle_{\mathbb C}.
\]

The useful consumer is coherent bookkeeping before forgetting outcomes:
generalized measurement/POVM constructions need the full branch amplitudes,
not only their nonnegative squared norms. This map retains complex linear
superpositions and relative phases, while the cross-overlap identity certifies
preservation of interference/orthogonality for distinct inputs. It does not
assert that individual branch maps preserve inner products or are orthogonal.

## Exact frozen ambient context and interfaces

```lean
import QuantumBlockEncoding.MeasurementProbability
import Mathlib.Analysis.InnerProductSpace.PiL2

namespace QuantumBlockEncoding.MeasurementCoherent
open scoped InnerProductSpace
variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

noncomputable def branchIsometry (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) :
    E →ₗᵢ[ℂ] PiLp 2 (fun _ : ι => F)

@[simp] theorem branchIsometry_apply (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) (i : ι) :
    branchIsometry M hM ψ i = M i ψ

theorem sum_inner_eq (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ φ : E) :
    ∑ i, inner ℂ (M i ψ) (M i φ) = inner ℂ ψ φ
end QuantumBlockEncoding.MeasurementCoherent
```

## Binder and definition audit

`ι,E,F` and normed/inner-product/complete-space structures are TYPING for
the finite Hilbert/adjoint setting. `M,ψ,φ,i` are data. `hM` is SOURCE in this
original interface contract; it is exactly input completeness, not a supplied
norm/isometry/inner-product preservation fact. No project-owned bundle hides
additional premises. No EXCESS binders, unit-norm, nonempty, nontrivial,
finite-dimensional, equal-dimension, nonzero-vector/branch, positivity, or
probability assumptions are allowed.

`branchIsometry` is literal: all coordinates are exactly `M i ψ`, on the whole
carrier. It is neither chosen from an existence theorem nor a quotient or
representative. Noncomputability is ordinary real-norm/proof packaging, not
an existence-based choice of operator, a default fallback, or a resource claim.

## Dependency and bounded reuse audit

The predecessor is the exact reviewed preparatory source
`experiments/quantum-foundations/measurement-completeness/QuantumBlockEncoding/MeasurementProbability.lean`,
SHA-256 `33c1a01b8f1e752f22acbc12ae47faa503e5dc7ae5f3f4d73dff39eeb9505775`.
Its `sum_norm_sq_eq` is a dependency edge supplying norm preservation; it must
not be added as a public hypothesis. It has no production/main admission.

Local production search found no matching finite-family coherent branch map.
Mathlib already owns `PiLp 2`, its finite-sum norm and inner product, and
`LinearIsometry`/`LinearIsometry.inner_map_map`; these are reused directly.
Existing `piLpCongrLeft/Right` are reindexing/component equivalences, not this
single-input operator-family assembly. External quantum-library cards were
read; their referenced checkouts are absent in this private context. No code
or unverified assertion is imported from them. This is a bounded reuse search,
not ecosystem nonexistence or novelty evidence.

## Construction graph and boundaries

`NODE completeness` + `NODE exact M` → `NODE predecessor total squared norm`
→ `NODE literal PiLp branch linear map` + `NODE PiLp norm identity`
→ `NODE branch LinearIsometry` → `NODE finite complex overlap identity`.
This original mathematical construction graph is not an AxQM proof graph,
and conceptual arrows are not claims of already observed Lean proof references.

All tensor/register identification, ancilla preparation/cleanup, surjectivity,
unitary completion/dilation, density/trace semantics, normalized outcome state,
instrument/channel, circuit, oracle-access, gate/resource/finite-bit and QA
admission claims are EXCLUDED. The output is a finite mathematical Hilbert
direct sum only. No basis/order, global-phase quotient, register permutation,
postselection or success-error convention is introduced.

Acceptance requires exact own freshly compiled predecessor and consumer
`.olean` providers on Lean 4.33.0, explicit `LEAN_PATH`, ordinary-three-axiom
observations, no placeholders/new axioms, preserved failed attempts, and
independent source-blind/semantic review. Full repository/Tests/site/publication
gates and post-integration purification remain separate obligations.

Process-memory IDs consulted: `QBE-PM-LOW-TOKEN-CONTROL-PLANE`,
`QBE-PM-VERIFIER-SEMANTIC-LEVEL`. Direction fingerprint:
`finite-operator-family-to-canonical-PiLp2-linear-isometry`.
Expected information gain: whether the existing completeness root supports an
actual coherent linear embedding without a duplicate measurement/tensor API.
