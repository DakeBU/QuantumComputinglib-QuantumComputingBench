import CachedStoredProducer
import AccountedTraffic
import CacheConsumerChecks

/-! Type/proposition probe ONLY. Every #check below checks the formation of a
candidate proposition; none provides a proof. Numeric bounds are unaccepted
proposals. Parent must inspect exact executable definitions and issue a
StatementSeal before any mathematical proof search. -/

namespace HermiteCachedPiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain QuantumBlockEncoding.TensorTrainCanonical
open HermitePiecewiseAssembly HermitePiecewiseStored HermitePiecewiseSourceBudget
open HermiteFiniteExpDegree

-- powQ_value
#check (∀ (x : ℚ) (m : ℕ), (powQ x m).value = x^m)

-- powQ_cost
#check (∀ (x : ℚ) (m : ℕ) (op : Op),
  (powQ x m).cost op = m*tick .field op)

-- middleFromCache_entry; no cache-correctness premise.
#check (∀ (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)) (j : Fin (2*k+2)),
  (middleFromCache k e a).value[j.val] = middleExpr k e a j)

-- middleFromCache_total_le; proposed 400, not accepted/proved.
#check (∀ (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)),
  StoredRectangularGivens.total (middleFromCache k e a).cost ≤ 400*(k+1)^2)

-- actual_cache_middle; internal scalar specialization, not a free setup claim.
#check (∀ (k : ℕ) (delta : ℚ) (j : Fin (2*k+2)),
  (middleFromCache k (HermiteFiniteMiddleSource.expMidpoint delta)
    (HermiteChargedSourceCache.produceSourceCache k).value).value[j.val] =
    HermitePiecewiseAssembly.middleCoeffQ k delta j.val)

-- cutoffQ_value; includes delta=0 and delta<0 literal rational behavior.
#check (∀ (delta : ℚ),
  (cutoffQ delta).value = HermiteFiniteExp.tailCutoff delta)

-- gridStepRun_value
#check (∀ (width : ℕ) (R : ℚ),
  (gridStepRun width R).value = HermitePiecewiseUniform.gridStepQ width R)

-- rightSetup_values, exact generic values, no positivity/regularity premise.
#check (∀ (n : ℕ) (R delta : ℚ),
  let s := (rightSetup n R delta).value
  s.cutMinusOne = HermitePiecewiseUniform.strictCut (n+1) R (-1) ∧
  s.cutZero = HermitePiecewiseUniform.inclusiveCut (n+1) R 0 ∧
  s.cutMinusT = HermitePiecewiseUniform.inclusiveCut (n+1) R
    (-(HermiteFiniteExp.tailCutoff delta : ℚ)) ∧
  s.cutT = HermitePiecewiseUniform.strictCut (n+1) R
    (HermiteFiniteExp.tailCutoff delta : ℚ) ∧
  (∀ i : Fin (sourceDegree delta+1),
    s.tailCoeffs[i.val] = 1/(i.val.factorial : ℚ)) ∧
  s.clipped = HermitePiecewiseKernelProducer.clippedValue delta ∧
  s.midpoint = HermiteFiniteMiddleSource.expMidpoint delta)

-- acceptRun_value
#check (∀ (width cut : ℕ) (a : Fin 3) (flip : Bool),
  (acceptRun width cut a flip).value =
    if flip then 1-HermitePiecewiseStored.acceptQ width cut a
    else HermitePiecewiseStored.acceptQ width cut a)

-- acceptRun_total_le
#check (∀ (width cut : ℕ) (a : Fin 3) (flip : Bool),
  StoredRectangularGivens.total (acceptRun width cut a flip).cost ≤ 4)

-- rightEntry_total_le; proposed 11, not accepted/proved.
#check (∀ (k n : ℕ) (R delta : ℚ) (s : RightSetup n R delta)
  (middle : Vector ℚ (2*k+2)) (z : FullIndex k delta),
  StoredRectangularGivens.total (rightEntry k n R delta s middle z).cost ≤ 11)

-- actual_cached_right; actual setup and middle facts are goals, not premises.
#check (∀ (k n : ℕ) (R delta : ℚ) (z : FullIndex k delta),
  let s := (rightSetup n R delta).value
  let a := (HermiteChargedSourceCache.produceSourceCache k).value
  let m := (middleFromCache k s.midpoint a).value
  (rightEntry k n R delta s m z).value =
    (HermitePiecewiseStored.actualBlocksQ k n R delta).right z)

-- produceCachedQData_value; same entire old data, not only a selected entry.
#check (∀ (k n : ℕ) (R delta : ℚ),
  (produceCachedQData k n R delta).value =
    (HermitePiecewiseStored.produceQData k n R delta).value)

-- produceCachedData_window; Window is produced, never an extra hypothesis.
#check (∀ (k n : ℕ) (R delta : ℚ),
  StoredMatrixProductChain.Window (produceCachedData k n R delta).value.tables
    (reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel) 0)

-- produceCachedStored_refines
#check (∀ (k n : ℕ) (R delta : ℚ),
  denoteChain (produceCachedStored k n R delta).value = actualChain k n R delta)

-- produceCachedStored_source; hR is the unchanged source interpretation premise.
#check (∀ (k n : ℕ) (R delta : ℚ) (_hR : 0 < R) (x : Word (n+1)),
  contract (denoteChain (produceCachedStored k n R delta).value) x 0 0 =
    (piecewiseValue k delta (rationalGrid n R (wordIndex n x)) : ℝ))

-- produceCachedStored_same_run; PARTIAL scalar/word ledger, same returned run.
-- Actual concrete setup.cost stays in the bound; it is not a premise or zero.
#check (∀ (k n : ℕ) (R delta : ℚ),
  let result := produceCachedStored k n R delta
  let D := assemblySize k delta
  denoteChain result.value = actualChain k n R delta ∧
  StoredRectangularGivens.total result.cost ≤
    816*(k+1)^2 + StoredRectangularGivens.total (rightSetup n R delta).cost +
    11*D + 9*HermitePiecewiseStored.passContainers n D +
    20*D^2 + 30*D + 5*n^2 + 7*n + 31)

end HermiteCachedPiecewiseStored
