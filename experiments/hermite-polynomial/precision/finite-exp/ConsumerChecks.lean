import FiniteExp
import QuantumBlockEncoding.HermitePolynomial

open QuantumBlockEncoding.HermitePolynomial
open HermiteFiniteExp

theorem hermite_left (k : ℕ) (p : ℚ) (T n : ℕ) (hp : (p : ℝ) < -1) :
    smoothInitial k (p : ℝ) ∈
      Set.Icc ((bounds p T n).1 : ℝ) ((bounds p T n).2 : ℝ) := by
  rw [smoothInitial_left k (p : ℝ) hp]
  exact membership p T n (by exact_mod_cast (show (p : ℝ) ≤ 0 by linarith))

theorem hermite_right (k : ℕ) (p : ℚ) (T n : ℕ) (hp : 0 < (p : ℝ)) :
    smoothInitial k (p : ℝ) ∈
      Set.Icc ((bounds (-p) T n).1 : ℝ) ((bounds (-p) T n).2 : ℝ) := by
  rw [smoothInitial_right k (p : ℝ) hp]
  simpa using membership (-p) T n (by exact_mod_cast (show -(p : ℝ) ≤ 0 by linarith))

theorem endpoint_scalar (T n : ℕ) : Real.exp (-1) ∈
    Set.Icc ((bounds (-1) T n).1 : ℝ) ((bounds (-1) T n).2 : ℝ) := by
  simpa using membership (-1) T n (by norm_num)

example : checked (-1) (1/1000) 10 8 ≠ none := by
  norm_num [checked, bounds, poly, radius, Finset.sum_range_succ] <;> simp
example : checked 0 (1/1000) 10 0 = some (1,1) := by
  norm_num [checked, bounds, poly, radius, Finset.sum_range_succ]
example : checked 1 (1/1000) 10 100 = none := by simp [checked]
example : checked (-1) 0 10 100 = none := by simp [checked]
example : checked (-1) (-1/1000) 10 100 = none := by norm_num [checked]
example : checked (-1) (1/1000) 10 0 = none := by
  norm_num [checked, bounds, poly, radius, Finset.sum_range_succ]
example : checked (-80) (1/(2 : ℚ)^80) 80 96 =
    some (0,1/(2 : ℚ)^80) := by norm_num [checked, bounds, tailRadius]
example : Real.exp (-80) ≤ ((1/(2 : ℚ)^80 : ℚ) : ℝ) := by
  simpa [tailRadius] using tail_bound (-80) 80 (by norm_num)

#eval tailCutoff (1/1000)
#eval tailCutoff (1/(2 : ℚ)^80)
#eval checked (-1) (1/1000) 10 8
#eval checked (-1) (1/1000) 10 0
#eval checked (-(10 : ℚ)^1000) (1/(2 : ℚ)^80) 80 0

#print axioms hermite_left
#print axioms hermite_right
#print axioms endpoint_scalar
