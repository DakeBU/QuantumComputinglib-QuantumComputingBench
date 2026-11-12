import SavedRounding

namespace ScalarRoundingReviewC15

theorem negative_ry_second_column_entry :
    (HermiteSavedRounding.ryRow (-1) 1 3 ⟨1,1⟩ ⟨0,0⟩).2 = ⟨-5/8,-3/8⟩ := by
  norm_num [HermiteSavedRounding.ryRow, HermiteSavedRounding.outward,
    HermiteSavedRounding.grid, HermiteSavedRounding.plus,
    HermiteSavedRounding.times, HermiteSavedRounding.negative,
    HermiteSavedRounding.sine, HermiteSavedRounding.cosine,
    HermiteFiniteTrig.sinBounds, HermiteFiniteTrig.cosBounds,
    HermiteFiniteTrig.sinPoly, HermiteFiniteTrig.cosPoly,
    HermiteFiniteTrig.sinCoeff, HermiteFiniteTrig.cosCoeff,
    HermiteFiniteTrig.radius, Finset.sum_range_succ,
    HermiteSavedRounding.Interval.mk.injEq]

#print axioms negative_ry_second_column_entry
end ScalarRoundingReviewC15
