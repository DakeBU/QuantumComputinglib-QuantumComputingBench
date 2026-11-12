import ExplicitChainValueProof

/-! Exact C250 VALUE signatures and actual dependency-axiom queries.
This consumer is authored, not run by the author. Cost root is intentionally
absent: it belongs to a separately authorized worker/composition phase. -/

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain
open HermitePiecewiseAssembly HermitePiecewiseStored
open HermiteExplicitCachedStored

#check (HermiteExplicitCachedStored.decode_value :
  ∀ (k : ℕ) (delta : ℚ) (a : Fin (assemblySize k delta)),
  (HermiteExplicitCachedStored.decode (HermiteFiniteExpDegree.sourceDegree delta)
    (2*k+1) a).run.value = (fullEquiv k delta).symm a)
#print axioms HermiteExplicitCachedStored.decode_value

#check (HermiteExplicitCachedStored.comparisonQ_value :
  ∀ (cut q : ℕ) (bit : Fin 2) (a b : Fin 3),
  (comparisonQ cut q bit a b).run.value =
    HermitePiecewiseUniform.comparisonEntry cut q bit a b)
#print axioms HermiteExplicitCachedStored.comparisonQ_value

#check (HermiteExplicitCachedStored.translationQ_actual_factorials :
  ∀ (L r q : ℕ) (hr : r ≤ L) (step : ℚ) (bit : Fin 2)
    (i j : Fin (r+1)),
  (translationQ L r q (HermiteChargedSourceCache.factorials L).value.values
    hr step bit i j).value =
    HermitePiecewiseUniform.translationCoreQ r (step*2^q*(bit.val : ℚ)) i j)
#print axioms HermiteExplicitCachedStored.translationQ_actual_factorials

#check (HermiteExplicitCachedStored.produceExplicitQData_value :
  ∀ (k n : ℕ) (R delta : ℚ),
  (produceExplicitQData k n R delta).run.value =
    (HermiteCachedPiecewiseStored.produceCachedQData k n R delta).value)
#print axioms HermiteExplicitCachedStored.produceExplicitQData_value

#check (HermiteExplicitCachedStored.produceExplicitData_window :
  ∀ (k n : ℕ) (R delta : ℚ),
  StoredMatrixProductChain.Window (produceExplicitData k n R delta).run.value.tables
    (reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel) 0)
#print axioms HermiteExplicitCachedStored.produceExplicitData_window

#check (HermiteExplicitCachedStored.produceExplicitStored_refines :
  ∀ (k n : ℕ) (R delta : ℚ),
  denoteChain (produceExplicitStored k n R delta).run.value = actualChain k n R delta)
#print axioms HermiteExplicitCachedStored.produceExplicitStored_refines

#check (HermiteExplicitCachedStored.produceExplicitStored_source :
  ∀ (k n : ℕ) (R delta : ℚ) (_hR : 0 < R)
    (x : TensorTrainCanonical.Word (n+1)),
  TensorTrainCanonical.contract
    (denoteChain (produceExplicitStored k n R delta).run.value) x 0 0 =
    (HermitePiecewiseSourceBudget.piecewiseValue k delta
      (HermitePiecewiseSourceBudget.rationalGrid n R (wordIndex n x)) : ℝ))
#print axioms HermiteExplicitCachedStored.produceExplicitStored_source

-- Check actual imported bodies rather than infer semantics from their names.
#print HermiteExplicitCachedStored.decode
#print HermiteExplicitCachedStored.comparisonQ
#print HermiteExplicitCachedStored.translationQ
#print HermiteExplicitCachedStored.kernelAt
#print HermiteExplicitCachedStored.leftAt
#print HermiteExplicitCachedStored.rightEntry
#print HermiteExplicitCachedStored.produceExplicitQData
#print HermiteExplicitCachedStored.produceExplicitData
#print HermiteExplicitCachedStored.produceExplicitStored
