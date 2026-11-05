import FiniteTrigProducer

open HermiteFiniteTrig

-- A saved RY's primary scalar argument is literal textual theta / 2.
example (theta : ℚ) (n : ℕ) :
    ((sinBounds (theta / 2) n).1 : ℝ) ≤ Real.sin ((theta / 2 : ℚ) : ℝ) ∧
    Real.sin ((theta / 2 : ℚ) : ℝ) ≤ ((sinBounds (theta / 2) n).2 : ℝ) :=
  sin_mem (theta / 2) n

example (theta : ℚ) (n : ℕ) :
    ((cosBounds (theta / 2) n).1 : ℝ) ≤ Real.cos ((theta / 2 : ℚ) : ℝ) ∧
    Real.cos ((theta / 2 : ℚ) : ℝ) ≤ ((cosBounds (theta / 2) n).2 : ℝ) :=
  cos_mem (theta / 2) n

example : radius (1/3) 7 = 1/264539520 := by norm_num [radius]
example : sinPoly (-1) 7 = -4241/5040 := by norm_num [sinPoly, sinCoeff, Finset.sum_range_succ]
example : cosPoly (-1) 7 = 389/720 := by norm_num [cosPoly, cosCoeff, Finset.sum_range_succ]
example : sinBounds 0 0 = (0, 0) := by norm_num [sinBounds, sinPoly, sinCoeff, radius]
example : cosBounds 0 0 = (1, 1) := by norm_num [cosBounds, cosPoly, cosCoeff, radius]
example : selectDegree 0 0 0 = some 0 := by norm_num [selectDegree, radius]
example : selectDegree 1 0 2 = none := by norm_num [selectDegree, radius, List.range_succ]

#eval sinBounds (1/3) 7
#eval cosBounds (1/3) 7
#eval selectDegree 8 (1 / 2^80) 128

#print axioms HermiteFiniteTrig.derivative_coeff
#print axioms HermiteFiniteTrig.sin_error
#print axioms HermiteFiniteTrig.cos_error
#print axioms HermiteFiniteTrig.sin_mem
#print axioms HermiteFiniteTrig.cos_mem
#print axioms HermiteFiniteTrig.sin_width
#print axioms HermiteFiniteTrig.cos_width
#print axioms HermiteFiniteTrig.selectDegree_sound
#print axioms HermiteFiniteTrig.selected_sin_sound
#print axioms HermiteFiniteTrig.selected_cos_sound
