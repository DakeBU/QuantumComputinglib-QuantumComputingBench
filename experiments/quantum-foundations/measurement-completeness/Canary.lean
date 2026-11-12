import QuantumBlockEncoding.MeasurementProbability

namespace MeasurementIntakeCanary
open QuantumBlockEncoding.MeasurementProbability
variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

theorem normalized_total (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) (hψ : ‖ψ‖ = 1) :
    ∑ i, ‖M i ψ‖ ^ 2 = 1 := by
  rw [sum_norm_sq_eq M hM ψ, hψ, one_pow]

theorem qa_consumer (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) (hψ : ‖ψ‖ = 1) :
    (∑ i, ‖M i ψ‖ ^ 2 = 1) ∧ ∀ i, ‖M i ψ‖ ^ 2 ∈ Set.Icc (0 : ℝ) 1 := by
  exact ⟨normalized_total M hM ψ hψ,
    fun i => outcome_probability_mem_Icc M hM ψ hψ i⟩

#print axioms QuantumBlockEncoding.MeasurementProbability.sum_norm_sq_eq
#print axioms QuantumBlockEncoding.MeasurementProbability.outcome_probability_mem_Icc
#print axioms MeasurementIntakeCanary.qa_consumer
end MeasurementIntakeCanary
