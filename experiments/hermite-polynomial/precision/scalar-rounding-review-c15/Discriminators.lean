import FiniteExpDegree
import SavedRounding

namespace ScalarRoundingReviewC15

theorem clipping_keeps_nonzero_width :
    HermiteFiniteExp.checked (-20) (1/8) 3 43 = some (0,1/8) := by
  norm_num [HermiteFiniteExp.checked, HermiteFiniteExp.bounds, HermiteFiniteExp.tailRadius]

theorem zero_cutoff_is_not_zero_exp :
    HermiteFiniteExp.checked 0 2 0 (HermiteFiniteExpDegree.degree 0 0) = some (0,1) := by
  norm_num [HermiteFiniteExp.checked, HermiteFiniteExp.bounds, HermiteFiniteExp.tailRadius]

theorem zero_precision_rejected :
    HermiteFiniteExp.checked (-20) 0 3 43 = none := by
  simp [HermiteFiniteExp.checked]

theorem negative_precision_rejected :
    HermiteFiniteExp.checked (-20) (-1/8) 3 43 = none := by
  norm_num [HermiteFiniteExp.checked]

theorem conservative_allocation : HermiteFiniteExpDegree.degree 80 80 = 25761 := by
  norm_num [HermiteFiniteExpDegree.degree, HermiteFiniteExpDegree.halfDegree]

theorem high_precision_complete :
    HermiteFiniteExp.checked (-1) (1/(2:ℚ)^80)
      (HermiteFiniteExp.tailCutoff (1/(2:ℚ)^80))
      (HermiteFiniteExpDegree.sourceDegree (1/(2:ℚ)^80)) =
      some (HermiteFiniteExp.bounds (-1)
        (HermiteFiniteExp.tailCutoff (1/(2:ℚ)^80))
        (HermiteFiniteExpDegree.sourceDegree (1/(2:ℚ)^80))) :=
  HermiteFiniteExpDegree.checked_complete _ _ (by norm_num) (by positivity)

theorem signed_outward_not_truncation :
    HermiteSavedRounding.outward ⟨-1/10,-1/10⟩ 0 = ⟨-1,0⟩ := by
  norm_num [HermiteSavedRounding.outward, HermiteSavedRounding.grid,
    HermiteSavedRounding.Interval.mk.injEq]

theorem mixed_product :
    HermiteSavedRounding.times ⟨-2,3⟩ ⟨-4,5⟩ = ⟨-12,15⟩ := by
  norm_num [HermiteSavedRounding.times, HermiteSavedRounding.Interval.mk.injEq]

theorem empty_trace (uv : HermiteSavedRounding.Interval × HermiteSavedRounding.Interval) :
    HermiteSavedRounding.rowTrace [] 1 0 uv = uv := rfl

theorem scalar_squared_not_four_coordinate_squared :
    (1/10:ℚ)^2 < 4*(1/10:ℚ)^2 := by norm_num

#print axioms clipping_keeps_nonzero_width
#print axioms zero_cutoff_is_not_zero_exp
#print axioms zero_precision_rejected
#print axioms negative_precision_rejected
#print axioms conservative_allocation
#print axioms high_precision_complete
#print axioms signed_outward_not_truncation
#print axioms mixed_product
#print axioms empty_trace
#print axioms scalar_squared_not_four_coordinate_squared
#eval (HermiteFiniteExp.tailCutoff 2, HermiteFiniteExpDegree.sourceDegree 2)
#eval HermiteFiniteExp.checked (-(10:ℚ)^1000) (1/(2:ℚ)^80) 80 25761

end ScalarRoundingReviewC15
