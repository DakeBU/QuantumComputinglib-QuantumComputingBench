import PiecewiseSourceBudget

namespace HermitePiecewiseSourceBudget

open scoped BigOperators
open QuantumBlockEncoding HermitePolynomial HermiteFiniteMiddleSource
open ExperimentalNormalizationStability

theorem allocatedVector_nonzero (k n : ℕ) (L epsilon : ℚ) :
    allocatedVector k n L epsilon ≠ 0 := by
  intro hz
  have h := finiteVector_central k n
    (ExperimentalGlobalRadiusBudget.allocatedRadius k n L epsilon)
    (sourceDelta k n epsilon)
  change allocatedVector k n L epsilon (HermiteIntervalMass.centralIndex n) = 1 at h
  rw [hz] at h
  simp at h

theorem allocatedVector_unit (k n : ℕ) (L epsilon : ℚ) :
    ‖NormedSpace.normalize (allocatedVector k n L epsilon)‖ = 1 :=
  NormedSpace.norm_normalize (allocatedVector_nonzero k n L epsilon)

theorem original_amplitude_error_sq (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (he : 0 < epsilon) :
    ∑ j, Complex.normSq
      (NormedSpace.normalize (allocatedVector k n L epsilon) j-
        HermiteStatePreparation.normalizedAmplitude k (n+1) (L : ℝ) j) ≤
      (epsilon : ℝ)^2/4 := by
  rw [← target_error_sq]
  have h := normalized_original_error k n L epsilon hL he
  have hs := pow_le_pow_left₀ (norm_nonneg _) h 2
  calc
    _ ≤ ((epsilon : ℝ)/2)^2 := hs
    _ = _ := by ring

theorem positive_scaled_original_error (k n : ℕ) (L epsilon : ℚ) (F : ℝ)
    (hL : 0 < L) (he : 0 < epsilon) (hF : 0 < F) :
    ‖NormedSpace.normalize (F⁻¹ • allocatedVector k n L epsilon)-
      targetVector k n (L : ℝ)‖ ≤ (epsilon : ℝ)/2 := by
  rw [NormedSpace.normalize_smul_of_pos (inv_pos.mpr hF)]
  exact normalized_original_error k n L epsilon hL he

theorem exact_left_owner (k : ℕ) (delta : ℚ) :
    piecewiseValue k delta (-1) = expMidpoint delta := by
  simp [piecewiseValue, literal_left_endpoint]

theorem clipped_midpoint (q delta : ℚ)
    (hc : q ≤ -(HermiteFiniteExp.tailCutoff delta : ℚ)) :
    negativeMidpoint q delta =
      HermiteFiniteExp.tailRadius (HermiteFiniteExp.tailCutoff delta)/2 := by
  simp [negativeMidpoint, HermiteFiniteExp.bounds, hc]

example : piecewiseValue 1 2 (-1/3) = 19/18 := by
  norm_num [piecewiseValue, middleValueQ, expMidpoint,
    HermiteFiniteExp.bounds, HermiteFiniteExp.tailCutoff, HermiteFiniteExp.tailRadius,
    coefficientValueQ, coefficientQ, ExperimentalCoefficientRange.sourceNumerator,
    Finset.sum_range_succ, Nat.choose]

example : piecewiseValue 1 2 (-2/3) = 7/9 := by
  norm_num [piecewiseValue, middleValueQ, expMidpoint,
    HermiteFiniteExp.bounds, HermiteFiniteExp.tailCutoff, HermiteFiniteExp.tailRadius,
    coefficientValueQ, coefficientQ, ExperimentalCoefficientRange.sourceNumerator,
    Finset.sum_range_succ, Nat.choose]

example : rationalGrid 1 3 ⟨0, by norm_num [gridSize]⟩ = -3 := by
  norm_num [rationalGrid, gridSize]
example : rationalGrid 1 3 ⟨1, by norm_num [gridSize]⟩ = -3/2 := by
  norm_num [rationalGrid, gridSize]
example : rationalGrid 1 3 ⟨2, by norm_num [gridSize]⟩ = 0 := by
  norm_num [rationalGrid, gridSize]
example : rationalGrid 1 3 ⟨3, by norm_num [gridSize]⟩ = 3/2 := by
  norm_num [rationalGrid, gridSize]

#eval (List.map (fun p => piecewiseValue 1 2 p) [-2,-1,-2/3,-1/3,0,1,2])
#eval (List.map (fun j : Fin 4 => rationalGrid 1 3 j) (List.finRange 4))
#eval (List.map (fun j : Fin 4 => piecewiseValue 1 2 (rationalGrid 1 3 j)) (List.finRange 4))
#eval (sourceDelta 1 2 (1/4), sourceDelta 0 0 2)
#eval (negativeMidpoint (-1000000000000000) (1/8))
#print axioms allocatedVector_nonzero
#print axioms allocatedVector_unit
#print axioms original_amplitude_error_sq
#print axioms positive_scaled_original_error
#print axioms exact_left_owner
#print axioms clipped_midpoint

end HermitePiecewiseSourceBudget
