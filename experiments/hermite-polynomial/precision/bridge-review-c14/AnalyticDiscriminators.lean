import FiniteExp
import GlobalRadiusBudget

namespace IndependentBridgeReviewC14

theorem closed_segment_derivative_bound (q : ℚ) (m : ℕ) (hq : q ≤ 0)
    (x : ℝ) (hx : x ∈ Set.uIcc (0 : ℝ) (q : ℝ)) :
    |iteratedDeriv m Real.exp x| ≤ 1 := by
  have hqR : (q : ℝ) ≤ 0 := by exact_mod_cast hq
  rw [Set.uIcc_comm, Set.uIcc_of_le hqR] at hx
  rw [iteratedDeriv_eq_iterate, Real.iter_deriv_exp,
    abs_of_pos (Real.exp_pos x)]
  exact Real.exp_le_one_iff.mpr hx.2

open HermiteFiniteExp

example : poly (-1/2) 1 = 1/2 ∧ radius (-1/2) 1 = 1/8 := by
  norm_num [poly, radius, Finset.sum_range_succ]
example : bounds (-1/2) 1 1 = (3/8,5/8) := by
  norm_num [bounds, poly, radius, Finset.sum_range_succ]
example : bounds (-1) 1 0 = (0,1/2) := by norm_num [bounds, tailRadius]
example : checked (-1) (1/4) 1 0 = none := by
  norm_num [checked, bounds, tailRadius]
example : checked (-1) (1/2) 1 0 = some (0,1/2) := by
  norm_num [checked, bounds, tailRadius]
example : checked (1/2) 1 1 0 = none := by norm_num [checked]
example : checked (-1) 0 1 0 = none := by simp [checked]

open QuantumBlockEncoding
open ExperimentalGlobalRadiusBudget ExperimentalRadiusStability
open ExperimentalNormalizationStability

example : deltaRadius 0 1 1 = 1/256 ∧ deltaRadius 0 0 1 = 1/128 := by
  norm_num [deltaRadius, lipschitzQ]
example : deltaRadius 1 0 1 = 1/98304 := by norm_num [deltaRadius, lipschitzQ]

theorem actual_original_target_radius_reserve (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (hepsilon : 0 < epsilon) :
    ‖NormedSpace.normalize (radiusVector k n (allocatedRadius k n L epsilon : ℝ))-
      targetVector k n (L : ℝ)‖ ≤ (epsilon : ℝ)/4 :=
  normalized_allocatedRadius_error k n L epsilon hL hepsilon

#print axioms closed_segment_derivative_bound
#print axioms actual_original_target_radius_reserve

end IndependentBridgeReviewC14
