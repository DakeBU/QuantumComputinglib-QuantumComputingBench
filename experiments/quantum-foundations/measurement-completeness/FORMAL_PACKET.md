# Formal context for independent mathematical reconstruction

Read only this file for the reconstruction. No source comparison or target
verdict is requested. Do not search other private work or external sources.

The imports and ambient variables are:

```lean
import Mathlib.Analysis.InnerProductSpace.Adjoint
namespace QuantumBlockEncoding.MeasurementProbability
open scoped InnerProductSpace
variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
```

`E →L[ℂ] F` is Mathlib's bounded complex-linear map. `adjoint` is its Hilbert
adjoint, `comp` is composition, `1` is the identity on E, `∑` is the finite sum,
and `‖ · ‖` on vectors is the inner-product norm. There are no project-defined
contract aliases or definitions. The exact proposed declarations are:

```lean
theorem sum_norm_sq_eq (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) :
    ∑ i, ‖M i ψ‖ ^ 2 = ‖ψ‖ ^ 2

theorem outcome_probability_mem_Icc (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E)
    (hψ : ‖ψ‖ = 1) (i : ι) : ‖M i ψ‖ ^ 2 ∈ Set.Icc (0 : ℝ) 1
```

Reconstruct the literal mathematics, all quantifiers and assumptions; identify
what follows and what does not, including degenerate/empty cases. Return your
own report and exact input hash, actor identity and scope. Do not modify these
signatures or create acceptance metadata for another role.
