# Formal context v1

Only the following definitions and interfaces are in scope. No source title,
author verdict, external correspondence claim, proof implementation, or desired
review conclusion is supplied.

```lean
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.PiL2

namespace QuantumBlockEncoding.MeasurementProbability
open scoped InnerProductSpace
variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
theorem sum_norm_sq_eq (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) :
    ∑ i, ‖M i ψ‖ ^ 2 = ‖ψ‖ ^ 2
end QuantumBlockEncoding.MeasurementProbability

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

`E →L[ℂ] F` is Mathlib's bundled bounded complex-linear map. `adjoint`
is the Hilbert adjoint; `.comp` composes its right argument first; `1` is
the input-space identity. The finite sum is over all elements of `ι`.
`E →ₗᵢ[ℂ] G` is Mathlib's complex-linear norm-preserving map, not necessarily
surjective. `PiLp 2 (fun _ : ι => F)` is the finite product with squared norm
`∑ i, ‖x i‖²` and complex inner product `∑ i, inner ℂ (x i) (y i)`.
The complex inner product is conjugate-linear in its first slot and linear
in its second. No project-owned aliases or bundled hypotheses are present.
