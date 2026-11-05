import CachedStoredProducer
import CachedSetupProof
import CachedMiddleValueProof

/-! C187 Fin-index proof-only successor of the failed C181/C186 VALUE integration.
C156-sealed signatures and C150 definitions are unchanged; author-uncompiled.
The actual returned cache/setup/middle/right arrays feed the same returned
rational data, cast, and stored-chain assembly. No resource bound is asserted.
Kernel/left scalar work and captured block setup remain unaccounted. -/

namespace HermiteCachedPiecewiseStored
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain QuantumBlockEncoding.TensorTrainCanonical
open HermitePiecewiseAssembly HermitePiecewiseStored HermitePiecewiseSourceBudget

private theorem c187_rightProduct_value (width cutA cutB : ℕ)
    (flipA flipB : Bool) (a b : Fin 3) (coefficient : Run ℚ) :
    (rightProduct width cutA cutB flipA flipB a b coefficient).value =
      (if flipA then 1-acceptQ width cutA a else acceptQ width cutA a) *
        ((if flipB then 1-acceptQ width cutB b else acceptQ width cutB b) *
          coefficient.value) := by
  simp only [rightProduct, bind, Run.bind, HermiteChargedSourceCache.qMul,
    charge, acceptRun_value]

private theorem c187_read_value {α : Type} {N : ℕ}
    (v : Vector α N) (i : Fin N) :
    (QuantumBlockEncoding.StoredGivens.read v i).value = v.get i := by
  rfl

theorem actual_cached_right :
  ∀ (k n : ℕ) (R delta : ℚ) (z : FullIndex k delta),
  let s := (rightSetup n R delta).value
  let a := (HermiteChargedSourceCache.produceSourceCache k).value
  let m := (middleFromCache k s.midpoint a).value
  (rightEntry k n R delta s m z).value =
    (HermitePiecewiseStored.actualBlocksQ k n R delta).right z := by
  intro k n R delta z
  dsimp only
  obtain ⟨hA, hB, hC, hD, hF, hclip, hmid⟩ := rightSetup_values n R delta
  have hmiddle :
      (middleFromCache k (rightSetup n R delta).value.midpoint
        (HermiteChargedSourceCache.produceSourceCache k).value).value =
      (middleFromCache k (HermiteFiniteMiddleSource.expMidpoint delta)
        (HermiteChargedSourceCache.produceSourceCache k).value).value :=
    congrArg (fun e : ℚ =>
      (middleFromCache k e
        (HermiteChargedSourceCache.produceSourceCache k).value).value) hmid
  have hFget (i : Fin (HermiteFiniteExpDegree.sourceDegree delta+1)) :
      (rightSetup n R delta).value.tailCoeffs.get i =
        1/(i.val.factorial : ℚ) :=
    hF i
  have hm (j : Fin (2*k+2)) :
      (middleFromCache k (rightSetup n R delta).value.midpoint
        (HermiteChargedSourceCache.produceSourceCache k).value).value.get j =
        middleCoeffQ k delta j.val :=
    (congrArg (fun v : Vector ℚ (2*k+2) => v.get j) hmiddle).trans
      (actual_cache_middle k delta j)
  rcases z with ⟨a,b,j⟩ | ⟨a,b,j⟩ | ⟨a,b,j⟩ | ⟨a,b,j⟩ | ⟨a,b,j⟩ <;>
    simp only [rightEntry, c187_rightProduct_value, pure, Run.pure,
      c187_read_value, charge,
      hA, hB, hC, hD, hFget, hm, hclip,
      actualBlocksQ, BlockQ.sum, BlockQ.prod, strictQ, inclusiveQ,
      thresholdQ, constantQ, tailQ, middleQ, polyQ,
      Bool.false_eq_true, if_false, if_true, Sum.elim]

private theorem c187_collect_value_eq {α : Type} {N : ℕ}
    (f g : Fin N → Run α) (h : ∀ i, (f i).value = (g i).value) :
    (collect f).value = (collect g).value := by
  apply Vector.ext
  intro i hi
  exact (collect_value f ⟨i,hi⟩).trans
    ((h ⟨i,hi⟩).trans (collect_value g ⟨i,hi⟩).symm)

theorem produceCachedQData_value :
  ∀ (k n : ℕ) (R delta : ℚ),
  (produceCachedQData k n R delta).value =
    (HermitePiecewiseStored.produceQData k n R delta).value := by
  intro k n R delta
  simp only [produceCachedQData, produceQData, bind, Run.bind, pure, Run.pure]
  congr 1
  apply c187_collect_value_eq
  intro a
  exact actual_cached_right k n R delta ((fullEquiv k delta).symm a)

private theorem c187_produceCachedData_value (k n : ℕ) (R delta : ℚ) :
    (produceCachedData k n R delta).value =
      (produceData k n R delta).value := by
  simp only [produceCachedData, produceData, bind, Run.bind, produceCachedQData_value]

theorem produceCachedData_window :
  ∀ (k n : ℕ) (R delta : ℚ),
  StoredMatrixProductChain.Window (produceCachedData k n R delta).value.tables
    (reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel) 0 := by
  intro k n R delta
  rw [c187_produceCachedData_value]
  exact produceData_window k n R delta

private theorem c187_produceCachedStored_value (k n : ℕ) (R delta : ℚ) :
    (produceCachedStored k n R delta).value =
      (produceStored k n R delta).value := by
  simp only [produceCachedStored, produceStored, bind, Run.bind,
    c187_produceCachedData_value]

theorem produceCachedStored_refines :
  ∀ (k n : ℕ) (R delta : ℚ),
  denoteChain (produceCachedStored k n R delta).value = actualChain k n R delta := by
  intro k n R delta
  rw [c187_produceCachedStored_value]
  exact produceStored_refines k n R delta

theorem produceCachedStored_source :
  ∀ (k n : ℕ) (R delta : ℚ) (_hR : 0 < R) (x : Word (n+1)),
  contract (denoteChain (produceCachedStored k n R delta).value) x 0 0 =
    (piecewiseValue k delta (rationalGrid n R (wordIndex n x)) : ℝ) := by
  intro k n R delta hR x
  rw [produceCachedStored_refines]
  exact actualChain_contract k n R delta hR x

#check c187_read_value
#print axioms c187_read_value
#check c187_rightProduct_value
#print axioms c187_rightProduct_value
#check c187_collect_value_eq
#print axioms c187_collect_value_eq
#check c187_produceCachedData_value
#print axioms c187_produceCachedData_value
#check c187_produceCachedStored_value
#print axioms c187_produceCachedStored_value

end HermiteCachedPiecewiseStored
