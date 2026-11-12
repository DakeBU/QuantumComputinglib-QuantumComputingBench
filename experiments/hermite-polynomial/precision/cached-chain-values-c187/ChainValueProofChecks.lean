import CachedChainValueProof

/-! Actual own-output audit consumer; these commands are not prefilled verdicts. -/
set_option pp.fullNames true
set_option pp.explicit true
set_option pp.universes true

#check HermiteCachedPiecewiseStored.actual_cached_right
#print HermiteCachedPiecewiseStored.actual_cached_right
#print axioms HermiteCachedPiecewiseStored.actual_cached_right
#check HermiteCachedPiecewiseStored.produceCachedQData_value
#print HermiteCachedPiecewiseStored.produceCachedQData_value
#print axioms HermiteCachedPiecewiseStored.produceCachedQData_value
#check HermiteCachedPiecewiseStored.produceCachedData_window
#print HermiteCachedPiecewiseStored.produceCachedData_window
#print axioms HermiteCachedPiecewiseStored.produceCachedData_window
#check HermiteCachedPiecewiseStored.produceCachedStored_refines
#print HermiteCachedPiecewiseStored.produceCachedStored_refines
#print axioms HermiteCachedPiecewiseStored.produceCachedStored_refines
#check HermiteCachedPiecewiseStored.produceCachedStored_source
#print HermiteCachedPiecewiseStored.produceCachedStored_source
#print axioms HermiteCachedPiecewiseStored.produceCachedStored_source

#print HermiteCachedPiecewiseStored.produceCachedQData
#print HermiteCachedPiecewiseStored.produceCachedData
#print HermiteCachedPiecewiseStored.produceCachedStored
#print HermiteCachedPiecewiseStored.rightEntry
#print HermitePiecewiseStored.actualBlocksQ
#print HermitePiecewiseStored.castData
#print QuantumBlockEncoding.StoredMatrixProductChain.ofTable
#check HermiteCachedPiecewiseStored.rightSetup_values
#print axioms HermiteCachedPiecewiseStored.rightSetup_values
#check HermiteCachedPiecewiseStored.actual_cache_middle
#print axioms HermiteCachedPiecewiseStored.actual_cache_middle

namespace HermiteCachedPiecewiseStored
open QuantumBlockEncoding QuantumBlockEncoding.StoredTensorTrain
open QuantumBlockEncoding.TensorTrainCanonical
open HermitePiecewiseAssembly HermitePiecewiseSourceBudget

-- Explicit typed consumers of all five sealed conclusions, with no new premise.
example (k n : ℕ) (R delta : ℚ) (z : FullIndex k delta) :
    let s := (rightSetup n R delta).value
    let a := (HermiteChargedSourceCache.produceSourceCache k).value
    let m := (middleFromCache k s.midpoint a).value
    (rightEntry k n R delta s m z).value =
      (HermitePiecewiseStored.actualBlocksQ k n R delta).right z :=
  actual_cached_right k n R delta z

example (k n : ℕ) (R delta : ℚ) :
    (produceCachedQData k n R delta).value =
      (HermitePiecewiseStored.produceQData k n R delta).value :=
  produceCachedQData_value k n R delta

example (k n : ℕ) (R delta : ℚ) :
    StoredMatrixProductChain.Window (produceCachedData k n R delta).value.tables
      (reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel) 0 :=
  produceCachedData_window k n R delta

example (k n : ℕ) (R delta : ℚ) :
    denoteChain (produceCachedStored k n R delta).value = actualChain k n R delta :=
  produceCachedStored_refines k n R delta

example (k n : ℕ) (R delta : ℚ) (hR : 0 < R) (x : Word (n+1)) :
    contract (denoteChain (produceCachedStored k n R delta).value) x 0 0 =
      (piecewiseValue k delta (rationalGrid n R (wordIndex n x)) : ℝ) :=
  produceCachedStored_source k n R delta hR x

end HermiteCachedPiecewiseStored
