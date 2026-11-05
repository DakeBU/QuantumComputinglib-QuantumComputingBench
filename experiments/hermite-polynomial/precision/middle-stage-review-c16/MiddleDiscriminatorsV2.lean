import ConsumerChecks

namespace MiddleStageReviewC16V2

open Polynomial QuantumBlockEncoding HermitePolynomial
open HermiteFiniteMiddleSource ExperimentalCoefficientRange

theorem central_matches_original (k : ℕ) (delta : ℚ) :
    (middleValueQ k delta 0 : ℝ) = smoothInitial k 0 := by
  have hs : smoothInitial k 0 = 1 := by
    rw [smoothInitial_middle k 0 (by norm_num)]
    simpa using sourceInterpolant_right_jet k 0 (by omega)
  simp [rational_central, hs]

theorem left_is_literal_midpoint (k : ℕ) (delta : ℚ) :
    middleValueQ k delta (-1) = expMidpoint delta := literal_left_endpoint k delta

theorem kzero_affine (delta p : ℚ) :
    middleValueQ 0 delta p = expMidpoint delta*(-p)+(p+1) := by
  norm_num [middleValueQ, coefficientValueQ, coefficientQ, sourceNumerator,
    Finset.sum_range_succ]

theorem asymmetric_first (delta : ℚ) :
    middleValueQ 1 delta (-1/3) = expMidpoint delta/3+8/9 := by
  norm_num [middleValueQ, coefficientValueQ, coefficientQ, sourceNumerator,
    Finset.sum_range_succ, Nat.choose] <;> ring

theorem asymmetric_reflected (delta : ℚ) :
    middleValueQ 1 delta (-2/3) = 8*expMidpoint delta/9+1/3 := by
  norm_num [middleValueQ, coefficientValueQ, coefficientQ, sourceNumerator,
    Finset.sum_range_succ, Nat.choose] <;> ring

theorem endpoint_amplification_exceeds_one :
    (1-(1/10:ℚ))^2*coefficientValueQ 1 (1/10) = 1053/1000 ∧
    1 < (1-(1/10:ℚ))^2*coefficientValueQ 1 (1/10) := by
  norm_num [coefficientValueQ, coefficientQ, sourceNumerator,
    Finset.sum_range_succ, Nat.choose]

theorem valid_coefficient_cast (k i : ℕ) (hi : i ≤ k) :
    (coefficientQ k i : ℝ) = HermiteBernstein.sourceCoefficient k i :=
  coefficientQ_cast k i hi

theorem invalid_index_cast_is_false :
    (coefficientQ 0 2 : ℝ) ≠ HermiteBernstein.sourceCoefficient 0 2 := by
  norm_num [coefficientQ, sourceNumerator, HermiteBernstein.sourceCoefficient_eq,
    Finset.sum_range_succ, Nat.choose]

theorem scalar_budget_not_four_coordinate_budget :
    (1/10:ℚ)^2 < 4*(1/10:ℚ)^2 := by norm_num

#print axioms central_matches_original
#print axioms left_is_literal_midpoint
#print axioms kzero_affine
#print axioms asymmetric_first
#print axioms asymmetric_reflected
#print axioms endpoint_amplification_exceeds_one
#print axioms valid_coefficient_cast
#print axioms invalid_index_cast_is_false
#print axioms scalar_budget_not_four_coordinate_budget
#eval (expMidpoint 2, middleValueQ 1 2 (-1/3), middleValueQ 1 2 (-2/3))
#eval (middleValueQ 0 0 0, middleValueQ 3 0 0)

end MiddleStageReviewC16V2
