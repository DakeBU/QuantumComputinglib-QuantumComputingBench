import QuantumBlockEncoding.MeasurementCoherent

open QuantumBlockEncoding.MeasurementCoherent
open scoped InnerProductSpace

variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

-- Direct consumers of the canonical interface, not additional public lemmas.
example (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ φ : E) (c : ℂ) :
    branchIsometry M hM (ψ + c • φ) =
      branchIsometry M hM ψ + c • branchIsometry M hM φ := by
  simp only [map_add, map_smul]

example (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ φ : E)
    (h : branchIsometry M hM ψ = branchIsometry M hM φ) : ψ = φ :=
  (branchIsometry M hM).injective h

example (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ φ : E)
    (h : inner ℂ ψ φ = 0) :
    ∑ i, inner ℂ (M i ψ) (M i φ) = 0 := by
  rw [sum_inner_eq M hM ψ φ, h]

#print axioms QuantumBlockEncoding.MeasurementProbability.sum_norm_sq_eq
#print axioms QuantumBlockEncoding.MeasurementCoherent.branchIsometry
#print axioms QuantumBlockEncoding.MeasurementCoherent.branchIsometry_apply
#print axioms QuantumBlockEncoding.MeasurementCoherent.sum_inner_eq
