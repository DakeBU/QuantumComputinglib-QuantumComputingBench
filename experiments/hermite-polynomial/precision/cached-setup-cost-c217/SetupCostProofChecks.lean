import SetupCostProof

/-! Same-author own-output exact-type/axiom consumer. Not independent review. -/
open QuantumBlockEncoding

#check (HermiteCachedPiecewiseStored.rightSetup_total_le :
  ∀ (n : ℕ) (R delta : ℚ),
  StoredRectangularGivens.total (HermiteCachedPiecewiseStored.rightSetup n R delta).cost ≤
    81*(HermiteFiniteExpDegree.sourceDegree delta+1)^2 +
    8*(HermiteFiniteExpDegree.sourceDegree delta+1) + n +
    HermiteFiniteExp.tailCutoff delta + 22)

#print axioms HermiteCachedPiecewiseStored.rightSetup_total_le
