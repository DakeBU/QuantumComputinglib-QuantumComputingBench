import GlobalRadiusBudget

open QuantumBlockEncoding
open ExperimentalGlobalRadiusBudget ExperimentalRadiusSupplier
open ExperimentalRadiusStability ExperimentalNormalizationStability

example (k n : ℕ) (L epsilon : ℚ) (hL : 0 < L) (hepsilon : 0 < epsilon) :
    ‖NormedSpace.normalize (radiusVector k n (allocatedRadius k n L epsilon : ℝ))-
      targetVector k n (L : ℝ)‖ ≤ (epsilon : ℝ)/4 :=
  normalized_allocatedRadius_error k n L epsilon hL hepsilon

example :
    ‖NormedSpace.normalize (radiusVector 0 200
        (allocatedRadius 0 200 (1/(10 : ℚ)^100) (1/(10 : ℚ)^110) : ℝ))-
      targetVector 0 200 ((1/(10 : ℚ)^100 : ℚ) : ℝ)‖ ≤
      ((1/(10 : ℚ)^110 : ℚ) : ℝ)/4 :=
  normalized_allocatedRadius_error 0 200 _ _ (by positivity) (by positivity)

#eval (lipschitzQ 0, deltaRadius 0 0 (1/1000))
#eval logTermCount (1/(10 : ℚ)^100) (deltaRadius 0 0 (1/(10 : ℚ)^110))
#eval logTermCount 1 (deltaRadius 0 200 (1/1000))
#eval logTermCount 1 (deltaRadius 20 0 (1/1000))
#eval let r := allocatedRadius 0 0 (1/(10 : ℚ)^100) (1/(10 : ℚ)^110)
      (decide (0 < r), Nat.size r.num.natAbs, Nat.size r.den)
#eval decide (deltaRadius 0 200 (1/1000) < deltaRadius 0 0 (1/1000))
#eval decide (deltaRadius 20 0 (1/1000) < deltaRadius 0 0 (1/1000))

#print axioms normalized_allocatedRadius_error
