import PiecewiseConsumerChecks

namespace Cycle17SourceReview
open HermitePiecewiseSourceBudget HermiteFiniteMiddleSource
open QuantumBlockEncoding ExperimentalNormalizationStability

theorem invalid_delta_central (k : ℕ) : piecewiseValue k 0 0 = 1 := piecewise_central k 0
theorem unconditional_floor (k n : ℕ) (R delta : ℚ) :
    1 ≤ ‖finiteVector k n R delta‖ := finiteVector_norm_floor k n R delta
theorem literal_original (k n : ℕ) (L epsilon : ℚ) (hL : 0 < L) (he : 0 < epsilon) :
    ‖NormedSpace.normalize (allocatedVector k n L epsilon) -
      WithLp.toLp 2 (HermiteStatePreparation.normalizedAmplitude k (n+1) (L : ℝ))‖ ≤
      (epsilon : ℝ)/2 := normalized_original_error k n L epsilon hL he
theorem source_delta_numeric : sourceDelta 2 3 (1/8) = 1/73728 := by
  norm_num [sourceDelta, amplificationQ]
theorem precision_degree_not_old_k_rank : HermiteFiniteExpDegree.sourceDegree (1/8) = 43 ∧
    43 > 2*0+6 := by
  norm_num [HermiteFiniteExpDegree.sourceDegree, HermiteFiniteExpDegree.degree,
    HermiteFiniteExpDegree.halfDegree, HermiteFiniteExp.tailCutoff]
theorem zero_cutoff : HermiteFiniteExp.tailCutoff 2 = 0 := by
  norm_num [HermiteFiniteExp.tailCutoff]
theorem one_cutoff : HermiteFiniteExp.tailCutoff (1/2) = 1 := by
  norm_num [HermiteFiniteExp.tailCutoff]
theorem left_active_empty (p : ℚ) (hp : p < -1) : ¬ (-1 < p) := by linarith
theorem both_clipped_masks : piecewiseValue 0 (1/8) (-3) = 1/16 ∧
    piecewiseValue 0 (1/8) 3 = 1/16 := by
  norm_num [piecewiseValue, negativeMidpoint, HermiteFiniteExp.bounds,
    HermiteFiniteExp.tailCutoff, HermiteFiniteExp.tailRadius]
theorem one_cutoff_left_clipped : piecewiseValue 0 (1/2) (-3/2) = 1/4 := by
  norm_num [piecewiseValue, negativeMidpoint, HermiteFiniteExp.bounds,
    HermiteFiniteExp.tailCutoff, HermiteFiniteExp.tailRadius]
theorem negative_scaling_not_phase_quotient : NormedSpace.normalize (-1 : ℝ) ≠
    NormedSpace.normalize (1 : ℝ) := by norm_num [NormedSpace.normalize, Real.norm_eq_abs]
theorem coordinate_accumulation :
    ‖(WithLp.toLp 2 (fun _ : Fin 4 => (1 : ℝ)) : EuclideanSpace ℝ (Fin 4))‖^2 = 4 := by
  rw [EuclideanSpace.real_norm_sq_eq]
  norm_num

#print axioms invalid_delta_central
#print axioms unconditional_floor
#print axioms literal_original
#print axioms source_delta_numeric
#print axioms precision_degree_not_old_k_rank
#print axioms zero_cutoff
#print axioms one_cutoff
#print axioms left_active_empty
#print axioms both_clipped_masks
#print axioms one_cutoff_left_clipped
#print axioms negative_scaling_not_phase_quotient
#print axioms coordinate_accumulation
end Cycle17SourceReview
