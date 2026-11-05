import Mathlib.Analysis.InnerProductSpace.Adjoint

/-!
Finite measurement completeness on the existing Mathlib Hilbert-space API.
Source correspondence: AxQM/Basic/Measurement.lean at independent commit
2ccf167efca86eb5164f1df8cedb72b84626b479 (Axiomatic AI; Winston Yin,
Frank Koppens; Apache-2.0). This independent local proof does not import AxQM,
copy its measurement/state structures, or use a benchmark task's missing proof.
Only the pure-vector operator substrate is proved, not mixed-state updates,
an instrument/dilation, physical implementation or circuit resource theorem.
-/

namespace QuantumBlockEncoding.MeasurementProbability

open scoped InnerProductSpace

variable {ι E F : Type*} [Fintype ι]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

/-- Completeness preserves squared norm even for an unnormalized input.
The outcome set may be empty and the Hilbert spaces may be zero-dimensional. -/
theorem sum_norm_sq_eq (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E) :
    ∑ i, ‖M i ψ‖ ^ 2 = ‖ψ‖ ^ 2 := by
  calc
    _ = ∑ i, RCLike.re (inner ℂ ((M i).adjoint.comp (M i) ψ) ψ) := by
      apply Finset.sum_congr rfl
      intro i _
      exact (M i).apply_norm_sq_eq_inner_adjoint_left ψ
    _ = RCLike.re (inner ℂ ((∑ i, (M i).adjoint.comp (M i)) ψ) ψ) := by
      simp [sum_inner]
    _ = ‖ψ‖ ^ 2 := by
      rw [hM]
      simpa only [one_apply_eq_self] using (norm_sq_eq_re_inner (𝕜 := ℂ) ψ).symm

/-- Every outcome has probability in [0,1] for a normalized pure input.
No nonzero-outcome assumption or state-update claim is hidden here. -/
theorem outcome_probability_mem_Icc (M : ι → E →L[ℂ] F)
    (hM : ∑ i, (M i).adjoint.comp (M i) = 1) (ψ : E)
    (hψ : ‖ψ‖ = 1) (i : ι) : ‖M i ψ‖ ^ 2 ∈ Set.Icc (0 : ℝ) 1 := by
  have hsum : ∑ j, ‖M j ψ‖ ^ 2 = 1 := by
    rw [sum_norm_sq_eq M hM ψ, hψ, one_pow]
  refine ⟨sq_nonneg _, ?_⟩
  calc
    _ ≤ ∑ j, ‖M j ψ‖ ^ 2 :=
      Finset.single_le_sum (fun j _ => sq_nonneg ‖M j ψ‖) (Finset.mem_univ i)
    _ = 1 := hsum

end QuantumBlockEncoding.MeasurementProbability
