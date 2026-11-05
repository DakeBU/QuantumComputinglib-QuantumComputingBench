import RadiusSupplier
import RadiusStability

open QuantumBlockEncoding
open ExperimentalRadiusSupplier ExperimentalRadiusStability
open HermitePolynomial ExperimentalNormalizationStability

theorem normalized_logRadius_error (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (hepsilon : 0 < epsilon) :
    ‖NormedSpace.normalize (radiusVector k n (logRadius L epsilon : ℝ))-
      targetVector k n (L : ℝ)‖ ≤
      2*Real.sqrt (gridSize (n+1) : ℝ)*sourceLipschitzConstant k*(epsilon : ℝ) := by
  have hLR : (0 : ℝ) < L := by exact_mod_cast hL
  exact (normalized_radius_error k n (L : ℝ) hLR (logRadius L epsilon)
    (logRadius_positive L epsilon hL hepsilon)).trans
    (mul_le_mul_of_nonneg_left (logRadius_error L epsilon hL hepsilon) (by
      have hC := sourceLipschitzConstant_ge_one k
      positivity))

example : Real.pi*((1/(10 : ℚ)^100 : ℚ) : ℝ) ∈
    Set.Icc ((logRadiusInterval (1/(10 : ℚ)^100) (1/(10 : ℚ)^110)).1 : ℝ)
      ((logRadiusInterval (1/(10 : ℚ)^100) (1/(10 : ℚ)^110)).2 : ℝ) := by
  exact logRadius_membership (1/(10 : ℚ)^100) (1/(10 : ℚ)^110)
    (by positivity) (by positivity)

#eval logTermCount 1 (1/1000)
#eval logTermCount 1 100
#eval logTermCount ((10 : ℚ)^100) (1/(10 : ℚ)^100)
#eval logTermCount (1/(10 : ℚ)^100) (1/(10 : ℚ)^110)
#eval let r := logRadius (1/(10 : ℚ)^100) (1/(10 : ℚ)^110)
      (decide (0 < r), Nat.size r.num.natAbs, Nat.size r.den)
#eval (logRadius 1 100, logRadiusInterval 1 100)

#print axioms normalized_logRadius_error
