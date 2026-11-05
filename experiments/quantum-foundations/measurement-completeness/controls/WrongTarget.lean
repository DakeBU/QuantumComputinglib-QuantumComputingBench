import QuantumBlockEncoding.MeasurementProbability

variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

-- Fixed negative fixture: all parameters are determined, but the goal is wrong.
example (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) : (0 : ℝ) = 1 := by
  exact QuantumBlockEncoding.MeasurementProbability.sum_norm_sq_eq M hM ψ
