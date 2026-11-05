import FiniteExpDegree
import QuantumBlockEncoding.HermitePolynomial

open QuantumBlockEncoding.HermitePolynomial
open HermiteFiniteExp HermiteFiniteExpDegree

theorem hermite_left_complete (k : ℕ) (p epsilon : ℚ)
    (hp : (p : ℝ) < -1) (he : 0 < epsilon) :
    smoothInitial k (p : ℝ) ∈ Set.Icc
      ((bounds p (tailCutoff epsilon) (sourceDegree epsilon)).1 : ℝ)
      ((bounds p (tailCutoff epsilon) (sourceDegree epsilon)).2 : ℝ) ∧
    (bounds p (tailCutoff epsilon) (sourceDegree epsilon)).2-
      (bounds p (tailCutoff epsilon) (sourceDegree epsilon)).1 ≤ epsilon := by
  rw [smoothInitial_left k (p : ℝ) hp]
  exact complete_enclosure p epsilon
    (by exact_mod_cast (show (p : ℝ) ≤ 0 by linarith)) he

theorem hermite_right_complete (k : ℕ) (p epsilon : ℚ)
    (hp : 0 < (p : ℝ)) (he : 0 < epsilon) :
    smoothInitial k (p : ℝ) ∈ Set.Icc
      ((bounds (-p) (tailCutoff epsilon) (sourceDegree epsilon)).1 : ℝ)
      ((bounds (-p) (tailCutoff epsilon) (sourceDegree epsilon)).2 : ℝ) ∧
    (bounds (-p) (tailCutoff epsilon) (sourceDegree epsilon)).2-
      (bounds (-p) (tailCutoff epsilon) (sourceDegree epsilon)).1 ≤ epsilon := by
  rw [smoothInitial_right k (p : ℝ) hp]
  simpa using complete_enclosure (-p) epsilon
    (by exact_mod_cast (show -(p : ℝ) ≤ 0 by linarith)) he

theorem endpoint_complete (epsilon : ℚ) (he : 0 < epsilon) :
    Real.exp (-1) ∈ Set.Icc
      ((bounds (-1) (tailCutoff epsilon) (sourceDegree epsilon)).1 : ℝ)
      ((bounds (-1) (tailCutoff epsilon) (sourceDegree epsilon)).2 : ℝ) ∧
    (bounds (-1) (tailCutoff epsilon) (sourceDegree epsilon)).2-
      (bounds (-1) (tailCutoff epsilon) (sourceDegree epsilon)).1 ≤ epsilon := by
  simpa using complete_enclosure (-1) epsilon (by norm_num) he

example : checked (-1) (1/1000) (tailCutoff (1/1000)) (sourceDegree (1/1000)) =
    some (bounds (-1) (tailCutoff (1/1000)) (sourceDegree (1/1000))) :=
  checked_complete _ _ (by norm_num) (by norm_num)

example : checked (-1) (1/(2 : ℚ)^80) (tailCutoff (1/(2 : ℚ)^80))
    (sourceDegree (1/(2 : ℚ)^80)) =
    some (bounds (-1) (tailCutoff (1/(2 : ℚ)^80)) (sourceDegree (1/(2 : ℚ)^80))) :=
  checked_complete _ _ (by norm_num) (by positivity)

example : radius 0 (degree 0 0) ≤ 1/(2 : ℚ) := by
  simpa using radius_degree 0 0 0 (by norm_num)

example : checked 1 (1/1000) 10 (degree 10 10) = none := by simp [checked]
example : checked (-1) 0 10 (degree 10 10) = none := by simp [checked]
example : checked (-1) (-1/1000) 10 (degree 10 10) = none := by norm_num [checked]
example : checked (-1) (1/1000) 10 0 = none := by
  norm_num [checked, bounds, poly, radius, Finset.sum_range_succ]
example : checked (-1) 2 0 (degree 0 0) = some (0,1) := by
  norm_num [checked, bounds, tailRadius]
example : degree 10 10 = 421 := by norm_num [degree, halfDegree]
example : degree 80 80 = 25761 := by norm_num [degree, halfDegree]

#eval (tailCutoff (1/1000), sourceDegree (1/1000))
#eval (tailCutoff (1/(2 : ℚ)^80), sourceDegree (1/(2 : ℚ)^80))
#eval (checked (-1) (1/1000) (tailCutoff (1/1000)) (sourceDegree (1/1000))).isSome
#eval checked (-(10 : ℚ)^1000) (1/(2 : ℚ)^80)
  (tailCutoff (1/(2 : ℚ)^80)) (sourceDegree (1/(2 : ℚ)^80))
#eval (tailCutoff 2, sourceDegree 2, checked 0 2 (tailCutoff 2) (sourceDegree 2))

#print axioms hermite_left_complete
#print axioms hermite_right_complete
#print axioms endpoint_complete
