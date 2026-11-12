import RadiusSupplier
import RadiusStability

namespace QuantumBlockEncoding.ExperimentalGlobalRadiusBudget

open ExperimentalRadiusSupplier ExperimentalRadiusStability
open HermitePolynomial ExperimentalNormalizationStability

def lipschitzQ (k : ℕ) : ℚ :=
  2*(k+1)^2*2^(3*k)*(2*k+2)*(2*k+1)*2^(2*k+1)

def deltaRadius (k n : ℕ) (epsilon : ℚ) : ℚ :=
  epsilon/(8*2^(n+1)*lipschitzQ k)

def allocatedRadius (k n : ℕ) (L epsilon : ℚ) : ℚ :=
  logRadius L (deltaRadius k n epsilon)

theorem lipschitzQ_cast (k : ℕ) :
    (lipschitzQ k : ℝ) = sourceLipschitzConstant k := by
  unfold lipschitzQ sourceLipschitzConstant ExperimentalCoefficientRange.coarseBound
  push_cast
  ring

theorem deltaRadius_positive (k n : ℕ) (epsilon : ℚ) (hepsilon : 0 < epsilon) :
    0 < deltaRadius k n epsilon := by
  unfold deltaRadius lipschitzQ
  positivity

theorem allocatedRadius_positive (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (hepsilon : 0 < epsilon) : 0 < allocatedRadius k n L epsilon :=
  logRadius_positive L _ hL (deltaRadius_positive k n epsilon hepsilon)

theorem allocatedRadius_error (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (hepsilon : 0 < epsilon) :
    |(allocatedRadius k n L epsilon : ℝ)-Real.pi*(L : ℝ)| ≤
      (deltaRadius k n epsilon : ℝ) :=
  logRadius_error L _ hL (deltaRadius_positive k n epsilon hepsilon)

theorem normalized_allocatedRadius_error (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (hepsilon : 0 < epsilon) :
    ‖NormedSpace.normalize (radiusVector k n (allocatedRadius k n L epsilon : ℝ))-
      targetVector k n (L : ℝ)‖ ≤ (epsilon : ℝ)/4 := by
  have hLR : (0 : ℝ) < L := by exact_mod_cast hL
  have heR : (0 : ℝ) < epsilon := by exact_mod_cast hepsilon
  have hC : (0 : ℝ) < sourceLipschitzConstant k :=
    lt_of_lt_of_le (by norm_num) (sourceLipschitzConstant_ge_one k)
  have hN : (1 : ℝ) ≤ gridSize (n+1) := by
    unfold gridSize
    exact_mod_cast (Nat.one_le_pow (n+1) 2 (by norm_num))
  have hs : Real.sqrt (gridSize (n+1) : ℝ) ≤ (gridSize (n+1) : ℝ) := by
    have hsq := Real.sq_sqrt (show (0 : ℝ) ≤ gridSize (n+1) by positivity)
    have hn := Real.sqrt_nonneg (gridSize (n+1) : ℝ)
    nlinarith
  have hd : (deltaRadius k n epsilon : ℝ) =
      (epsilon : ℝ)/(8*(gridSize (n+1) : ℝ)*sourceLipschitzConstant k) := by
    unfold deltaRadius gridSize
    push_cast
    rw [lipschitzQ_cast]
  have hdpos : (0 : ℝ) ≤ deltaRadius k n epsilon := by
    exact_mod_cast (deltaRadius_positive k n epsilon hepsilon).le
  have he := normalized_radius_error k n (L : ℝ) hLR
    (allocatedRadius k n L epsilon) (allocatedRadius_positive k n L epsilon hL hepsilon)
  calc
    _ ≤ 2*Real.sqrt (gridSize (n+1) : ℝ)*sourceLipschitzConstant k*
        (deltaRadius k n epsilon : ℝ) := he.trans
      (mul_le_mul_of_nonneg_left (allocatedRadius_error k n L epsilon hL hepsilon)
        (by positivity))
    _ ≤ 2*(gridSize (n+1) : ℝ)*sourceLipschitzConstant k*
        (deltaRadius k n epsilon : ℝ) := by gcongr
    _ = _ := by rw [hd]; field_simp; ring

theorem allocatedTermCount_size (k n : ℕ) (L epsilon : ℚ) :
    logTermCount L (deltaRadius k n epsilon) ≤
      Nat.size (max 1 (Nat.ceil (160*L*2^(n+1)*lipschitzQ k/epsilon)))+1 := by
  have hid : 20*L/deltaRadius k n epsilon =
      160*L*2^(n+1)*lipschitzQ k/epsilon := by
    unfold deltaRadius
    rw [div_div_eq_mul_div]
    ring
  simpa only [hid] using logTermCount_size L (deltaRadius k n epsilon)

#print axioms lipschitzQ_cast
#print axioms deltaRadius_positive
#print axioms allocatedRadius_positive
#print axioms allocatedRadius_error
#print axioms normalized_allocatedRadius_error
#print axioms allocatedTermCount_size

end QuantumBlockEncoding.ExperimentalGlobalRadiusBudget
