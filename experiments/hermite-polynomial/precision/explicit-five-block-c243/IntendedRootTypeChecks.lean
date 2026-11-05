import ExplicitFiveBlockDefinitions
import CachedStoredProducer

/-! Proposition formation candidates only. No proof or axiom declarations.
The source objects below are specifications, not producer-body evaluations. -/

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain
open HermitePiecewiseAssembly HermitePiecewiseStored
open HermiteExplicitCachedStored

#check HermiteExplicitCachedStored.decode
#check comparisonQ
#check translationQ
#check kernelAt
#check kernelEntry
#check leftAt
#check leftEntry
#check HermiteExplicitCachedStored.rightEntry
#check materializePrepared
#check produceExplicitQData
#check produceExplicitData
#check produceExplicitStored
#check frontierBudget

-- Exact original layout, specialized from the degree-parameterized decoder.
#check (∀ (k : ℕ) (delta : ℚ) (a : Fin (assemblySize k delta)),
  (HermiteExplicitCachedStored.decode (HermiteFiniteExpDegree.sourceDegree delta)
    (2*k+1) a).run.value = (fullEquiv k delta).symm a)

#check (∀ (cut q : ℕ) (bit : Fin 2) (a b : Fin 3),
  (comparisonQ cut q bit a b).run.value =
    HermitePiecewiseUniform.comparisonEntry cut q bit a b)

#check (∀ (L r q : ℕ) (hr : r ≤ L) (step : ℚ) (bit : Fin 2)
    (i j : Fin (r+1)),
  (translationQ L r q (HermiteChargedSourceCache.factorials L).value.values
    hr step bit i j).value =
    HermitePiecewiseUniform.translationCoreQ r (step*2^q*(bit.val : ℚ)) i j)

#check (∀ (k n : ℕ) (R delta : ℚ),
  (produceExplicitQData k n R delta).run.value =
    (HermiteCachedPiecewiseStored.produceCachedQData k n R delta).value)

#check (∀ (k n : ℕ) (R delta : ℚ),
  StoredMatrixProductChain.Window (produceExplicitData k n R delta).run.value.tables
    (reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel) 0)

#check (∀ (k n : ℕ) (R delta : ℚ),
  denoteChain (produceExplicitStored k n R delta).run.value = actualChain k n R delta)

#check (∀ (k n : ℕ) (R delta : ℚ) (_hR : 0 < R)
    (x : TensorTrainCanonical.Word (n+1)),
  TensorTrainCanonical.contract
    (denoteChain (produceExplicitStored k n R delta).run.value) x 0 0 =
    (HermitePiecewiseSourceBudget.piecewiseValue k delta
      (HermitePiecewiseSourceBudget.rationalGrid n R (wordIndex n x)) : ℝ))

-- SAME returned value and ledger; no callback/cost/normalization premises.
#check (∀ (k n : ℕ) (R delta : ℚ),
  let result := produceExplicitStored k n R delta
  denoteChain result.run.value = actualChain k n R delta ∧
  StoredRectangularGivens.total result.run.cost ≤ frontierBudget k n delta ∧
  result.quotientCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta ∧
  result.remainderCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta)
