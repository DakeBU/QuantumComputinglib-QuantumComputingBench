import CachedSameRunProof

/-! C208 same-author exact C156 type/axiom consumer, not independent review.
Select only this successor's fresh own output, never the failed C207 module. -/

open QuantumBlockEncoding QuantumBlockEncoding.StoredTensorTrain
open HermitePiecewiseAssembly HermiteCachedPiecewiseStored

#check (produceCachedStored_same_run :
  ∀ (k n : ℕ) (R delta : ℚ),
  let result := produceCachedStored k n R delta
  let D := assemblySize k delta
  denoteChain result.value = actualChain k n R delta ∧
  StoredRectangularGivens.total result.cost ≤
    816*(k+1)^2 + StoredRectangularGivens.total (rightSetup n R delta).cost +
    11*D + 9*HermitePiecewiseStored.passContainers n D +
    20*D^2 + 30*D + 5*n^2 + 7*n + 31)

#print axioms produceCachedStored_same_run
