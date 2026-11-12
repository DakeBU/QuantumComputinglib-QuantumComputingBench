import ExplicitScalarValueProof
import CachedChainValueProof

/-! C250-sealed same-returned-data VALUE proof candidate, author-uncompiled.
Actual generated factorials/setup/cache/middle and the original charged right
entry are consumed. No arbitrary correctness or cost promise is a root premise.
No same-run cost theorem is asserted in this VALUE-only packet. -/

namespace HermiteExplicitCachedStored

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain
open QuantumBlockEncoding.StoredBinaryCoordinates
open HermitePiecewiseAssembly HermitePiecewiseStored HermitePiecewiseUniform
open HermiteFiniteExpDegree

private theorem c252_componentKernel_value (L r q : ℕ) (hr : r ≤ L)
    (cutA cutB : ℕ) (step : ℚ) (bit : Fin 2) (a b : ComponentIndex r) :
    (componentKernel L r q (HermiteChargedSourceCache.factorials L).value.values
      hr cutA cutB step bit a b).run.value =
      comparisonEntry cutA q bit a.1 b.1 *
        (comparisonEntry cutB q bit a.2.1 b.2.1 *
          translationCoreQ r (step*2^q*(bit.val : ℚ)) a.2.2 b.2.2) := by
  simp only [componentKernel, indexedBind, liftRun, comparisonQ_value,
    translationQ_actual_factorials, bind, Run.bind,
    HermiteChargedSourceCache.qMul, charge]

private theorem c252_kernelAt_value (k n : ℕ) (R delta : ℚ) (L q : ℕ)
    (ht : sourceDegree delta ≤ L) (hm : 2*k+1 ≤ L) (bit : Fin 2)
    (a b : FullIndex k delta) :
    (kernelAt (sourceDegree delta) (2*k+1) L q
      (HermiteChargedSourceCache.factorials L).value.values ht hm
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutMinusOne
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutZero
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutMinusT
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutT
      (gridStepQ (n+1) R) (-gridStepQ (n+1) R) bit a b).run.value =
      (actualBlocksQ k n R delta).kernel q bit a b := by
  obtain ⟨hA, hB, hC, hD, _hF, _hclip, _hmid⟩ :=
    HermiteCachedPiecewiseStored.rightSetup_values n R delta
  rcases a with a | a | a | a | a <;>
    rcases b with b | b | b | b | b <;>
    simp only [kernelAt, c252_componentKernel_value, liftRun, pure, Run.pure,
      hA, hB, hC, hD, actualBlocksQ, BlockQ.sum, BlockQ.prod, strictQ, inclusiveQ,
      thresholdQ, constantQ, tailQ, middleQ, polyQ,
      Bool.false_eq_true, if_false, if_true, Sum.elim]

private theorem c252_kernelEntry_value (k n : ℕ) (R delta : ℚ) (L : ℕ)
    (ht : sourceDegree delta ≤ L) (hm : 2*k+1 ≤ L)
    (q : Fin (n+1)) (a : Fin (assemblySize k delta))
    (j : Fin (2*assemblySize k delta)) :
    (kernelEntry (sourceDegree delta) (2*k+1) n L
      (HermiteChargedSourceCache.factorials L).value.values ht hm
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutMinusOne
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutZero
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutMinusT
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutT
      (gridStepQ (n+1) R) (-gridStepQ (n+1) R) q a j).run.value =
      actualEntryQ k n R delta q.val (finProdFinEquiv.symm j).1 a
        (finProdFinEquiv.symm j).2 := by
  let A : ℕ := assemblySize k delta
  let out : Fin 2 × Fin A :=
    (finProdFinEquiv (m := 2) (n := A)).symm j
  -- C319_TYPECHECK_K: whole original target, one explicit product carrier.
  change
    (kernelAt (sourceDegree delta) (2*k+1) L q.val
      (HermiteChargedSourceCache.factorials L).value.values ht hm
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutMinusOne
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutZero
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutMinusT
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value.cutT
      (gridStepQ (n+1) R) (-gridStepQ (n+1) R) out.1
      (decode (sourceDegree delta) (2*k+1) a).run.value
      (decode (sourceDegree delta) (2*k+1) out.2).run.value).run.value =
        actualEntryQ k n R delta q.val out.1 a out.2
  rw [decode_value k delta a, decode_value k delta out.2]
  simpa only [actualEntryQ] using
    c252_kernelAt_value k n R delta L q.val ht hm
      out.1 ((fullEquiv k delta).symm a) ((fullEquiv k delta).symm out.2)

private theorem c252_leftAt_value (k n : ℕ) (R delta : ℚ) (a : FullIndex k delta) :
    (leftAt (sourceDegree delta) (2*k+1) R (-R) a).value =
      (actualBlocksQ k n R delta).left a := by
  rcases a with a | a | a | a | a <;>
    simp only [leftAt, componentLeft, bind, Run.bind,
      HermiteChargedSourceCache.qMul, charge,
      HermiteCachedPiecewiseStored.powQ_value,
      actualBlocksQ, BlockQ.sum, BlockQ.prod, strictQ, inclusiveQ,
      thresholdQ, constantQ, tailQ, middleQ, polyQ,
      Bool.false_eq_true, if_false, if_true, Sum.elim]

private theorem c252_leftEntry_value (k n : ℕ) (R delta : ℚ)
    (a : Fin (assemblySize k delta)) :
    (leftEntry (sourceDegree delta) (2*k+1) R (-R) a).run.value =
      actualLeftQ k n R delta a := by
  simp only [leftEntry, decode_value]
  exact c252_leftAt_value k n R delta ((fullEquiv k delta).symm a)

/-- Actual indexed collection refines actual ordinary collection by values.
Fin-indexed entries avoid manufacturing accessor witnesses through congrArg. -/
private theorem c252_collectIndexed_eq_collect {α : Type} {N : ℕ}
    (f : Fin N → IndexedRun α) (g : Fin N → Run α)
    (h : ∀ i, (f i).run.value = (g i).value) :
    (collectIndexed f).run.value = (collect g).value := by
  apply Vector.ext
  intro i hi
  exact (collectIndexed_value f ⟨i,hi⟩).trans
    ((h ⟨i,hi⟩).trans (collect_value g ⟨i,hi⟩).symm)

private theorem c252_prepared_value (k n : ℕ) (R delta : ℚ) (L : ℕ)
    (ht : sourceDegree delta ≤ L) (hm : 2*k+1 ≤ L) :
    (materializePrepared k n R delta (sourceDegree delta) rfl L ht hm
      (HermiteCachedPiecewiseStored.rightSetup n R delta).value
      (HermiteCachedPiecewiseStored.middleFromCache k
        (HermiteCachedPiecewiseStored.rightSetup n R delta).value.midpoint
        (HermiteChargedSourceCache.produceSourceCache k).value).value
      (HermiteChargedSourceCache.factorials L).value.values
      (gridStepQ (n+1) R) (-R) (-gridStepQ (n+1) R)).run.value =
      (HermiteCachedPiecewiseStored.produceCachedQData k n R delta).value := by
  dsimp only [materializePrepared, HermiteCachedPiecewiseStored.produceCachedQData,
    bind, Run.bind, pure, Run.pure]
  congr 1
  · apply c252_collectIndexed_eq_collect
    intro q
    apply c252_collectIndexed_eq_collect
    intro a
    apply c252_collectIndexed_eq_collect
    intro j
    exact c252_kernelEntry_value k n R delta L ht hm q a j
  · apply c252_collectIndexed_eq_collect
    intro a
    exact c252_leftEntry_value k n R delta a
  · apply c252_collectIndexed_eq_collect
    intro a
    let actualRight : FullIndex k delta → ℚ := fun z =>
      (HermiteCachedPiecewiseStored.rightEntry k n R delta
        (HermiteCachedPiecewiseStored.rightSetup n R delta).value
        (HermiteCachedPiecewiseStored.middleFromCache k
          (HermiteCachedPiecewiseStored.rightSetup n R delta).value.midpoint
          (HermiteChargedSourceCache.produceSourceCache k).value).value z).value
    dsimp only [HermiteExplicitCachedStored.rightEntry]
    change actualRight ((decode (sourceDegree delta) (2*k+1) a).run.value) =
      actualRight ((fullEquiv k delta).symm a)
    exact congrArg actualRight
      (decode_value k delta (a : Fin (assemblySize k delta)))

theorem produceExplicitQData_value :
  ∀ (k n : ℕ) (R delta : ℚ),
  (produceExplicitQData k n R delta).run.value =
    (HermiteCachedPiecewiseStored.produceCachedQData k n R delta).value := by
  intro k n R delta
  let A : ℕ := assemblySize k delta
  let T : ℕ := HermiteFiniteExp.tailCutoff delta
  let d : ℕ := degree T T
  let L : ℕ := d+2*k+1
  have hd : d = sourceDegree delta := by rfl
  have ht : d ≤ L := by dsimp only [L]; omega
  have hm : 2*k+1 ≤ L := by dsimp only [L]; omega
  have hsize : fiveSize d (2*k+1) = A := by rfl
  let setup := (HermiteCachedPiecewiseStored.rightSetup n R delta).value
  let middle := (HermiteCachedPiecewiseStored.middleFromCache k
    setup.midpoint (HermiteChargedSourceCache.produceSourceCache k).value).value
  let F : Vector ℚ (L+1) :=
    (HermiteChargedSourceCache.factorials L).value.values
  let raw (step minusR minusStep : ℚ) : RationalData n (fiveSize d (2*k+1)) :=
    (materializePrepared k n R delta d hd L ht hm setup middle F
      step minusR minusStep).run.value
  let toA : RationalData n (fiveSize d (2*k+1)) → RationalData n A :=
    Eq.mp (congrArg (fun D => RationalData n D) hsize)
  -- C319_TYPECHECK_Q: whole original equality at RationalData n A.
  -- The runtime cutoff/degree/size conversion is definition-only.
  change
    toA (raw (HermiteCachedPiecewiseStored.gridStepRun (n+1) R).value
      (HermiteCachedPiecewiseStored.qSub 0 R).value
      (HermiteCachedPiecewiseStored.qSub 0
        (HermiteCachedPiecewiseStored.gridStepRun (n+1) R).value).value) =
      toA (HermiteCachedPiecewiseStored.produceCachedQData k n R delta).value
  have preparedRaw :
      raw (gridStepQ (n+1) R) (-R) (-gridStepQ (n+1) R) =
        (HermiteCachedPiecewiseStored.produceCachedQData k n R delta).value := by
    exact c252_prepared_value k n R delta L ht hm
  calc
    toA (raw (HermiteCachedPiecewiseStored.gridStepRun (n+1) R).value
      (HermiteCachedPiecewiseStored.qSub 0 R).value
      (HermiteCachedPiecewiseStored.qSub 0
        (HermiteCachedPiecewiseStored.gridStepRun (n+1) R).value).value) =
        toA (raw (gridStepQ (n+1) R) (-R) (-gridStepQ (n+1) R)) := by
      apply congrArg toA
      simp only [HermiteCachedPiecewiseStored.gridStepRun_value,
        HermiteCachedPiecewiseStored.qSub, charge, zero_sub]
    _ = _ := congrArg toA preparedRaw

private theorem c252_data_value (k n : ℕ) (R delta : ℚ) :
    (produceExplicitData k n R delta).run.value =
      (HermiteCachedPiecewiseStored.produceCachedData k n R delta).value := by
  simp only [produceExplicitData, indexedBind, liftRun,
    HermiteCachedPiecewiseStored.produceCachedData, bind, Run.bind,
    produceExplicitQData_value]

theorem produceExplicitData_window :
  ∀ (k n : ℕ) (R delta : ℚ),
  StoredMatrixProductChain.Window (produceExplicitData k n R delta).run.value.tables
    (reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel) 0 := by
  intro k n R delta
  rw [c252_data_value]
  exact HermiteCachedPiecewiseStored.produceCachedData_window k n R delta

private theorem c252_stored_value (k n : ℕ) (R delta : ℚ) :
    (produceExplicitStored k n R delta).run.value =
      (HermiteCachedPiecewiseStored.produceCachedStored k n R delta).value := by
  simp only [produceExplicitStored, indexedBind, liftRun,
    HermiteCachedPiecewiseStored.produceCachedStored, bind, Run.bind, c252_data_value]

theorem produceExplicitStored_refines :
  ∀ (k n : ℕ) (R delta : ℚ),
  denoteChain (produceExplicitStored k n R delta).run.value = actualChain k n R delta := by
  intro k n R delta
  rw [c252_stored_value]
  exact HermiteCachedPiecewiseStored.produceCachedStored_refines k n R delta

theorem produceExplicitStored_source :
  ∀ (k n : ℕ) (R delta : ℚ) (_hR : 0 < R)
    (x : TensorTrainCanonical.Word (n+1)),
  TensorTrainCanonical.contract
    (denoteChain (produceExplicitStored k n R delta).run.value) x 0 0 =
    (HermitePiecewiseSourceBudget.piecewiseValue k delta
      (HermitePiecewiseSourceBudget.rationalGrid n R (wordIndex n x)) : ℝ) := by
  intro k n R delta hR x
  rw [produceExplicitStored_refines]
  exact actualChain_contract k n R delta hR x

#check c252_componentKernel_value
#print axioms c252_componentKernel_value
#check c252_kernelAt_value
#print axioms c252_kernelAt_value
#check c252_kernelEntry_value
#print axioms c252_kernelEntry_value
#check c252_leftAt_value
#print axioms c252_leftAt_value
#check c252_leftEntry_value
#print axioms c252_leftEntry_value
#check c252_collectIndexed_eq_collect
#print axioms c252_collectIndexed_eq_collect
#check c252_prepared_value
#print axioms c252_prepared_value
#check c252_data_value
#print axioms c252_data_value
#check c252_stored_value
#print axioms c252_stored_value

end HermiteExplicitCachedStored
