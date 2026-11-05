import CachedMiddleCostProof

/-! C183 same-author exact-type/axiom consumer, not independent review.
Compile only against the fresh own output of this proof-only successor. -/

open QuantumBlockEncoding

#check (HermiteCachedPiecewiseStored.middleFromCache_total_le :
  ∀ (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)),
  StoredRectangularGivens.total
    (HermiteCachedPiecewiseStored.middleFromCache k e a).cost ≤ 400*(k+1)^2)

#print axioms HermiteCachedPiecewiseStored.middleFromCache_total_le
