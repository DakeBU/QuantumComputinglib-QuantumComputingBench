import ExplicitFiveBlockDefinitions
import CachedMiddleCostProof
import SetupCostProof
import CacheConsumerChecks
import AccountedTraffic

/-! C253 author-uncompiled cost/counter projection of the C250 same-run target.
No C252 value proof is imported. All producers and the budget are unchanged.
Only the eight scalar/word counters and two selected index counters are bounded;
native evaluator/index/bit/Rat/GCD/allocation/sharing and quantum costs remain open. -/

namespace HermiteExplicitCachedStored
open scoped BigOperators
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain QuantumBlockEncoding.StoredBinaryCoordinates
open HermitePiecewiseAssembly HermitePiecewiseStored HermiteFiniteExpDegree

private theorem c253_total_add (x y : Cost) :
    StoredRectangularGivens.total (x+y) =
      StoredRectangularGivens.total x + StoredRectangularGivens.total y := by
  simp only [StoredRectangularGivens.total, Pi.add_apply]
  ring

private theorem c253_total_tick (op : Op) :
    StoredRectangularGivens.total (tick op) = 1 := by
  cases op <;> simp [StoredRectangularGivens.total, tick]

private theorem c253_total_nsmul (n : ℕ) (x : Cost) :
    StoredRectangularGivens.total (n • x) = n*StoredRectangularGivens.total x := by
  simp [StoredRectangularGivens.total, Pi.smul_apply, nsmul_eq_mul]
  ring

private theorem c253_total_zero : StoredRectangularGivens.total (0 : Cost) = 0 := by
  simp [StoredRectangularGivens.total]

private theorem c253_sum_le {m : ℕ} (f : Fin m → ℕ) (B : ℕ)
    (h : ∀ i, f i ≤ B) : (∑ i, f i) ≤ m*B := by
  calc
    _ ≤ ∑ _i : Fin m, B := Finset.sum_le_sum (fun i _ => h i)
    _ = _ := by simp

private theorem c253_collect_total {α : Type} {m : ℕ} (f : Fin m → IndexedRun α) :
    StoredRectangularGivens.total (collectIndexed f).run.cost =
      (∑ i, StoredRectangularGivens.total (f i).run.cost)+4*m := by
  simp [StoredRectangularGivens.total, collectIndexed_cost, tick,
    Finset.sum_add_distrib] <;> ring

private theorem c253_collect_le {α : Type} {m : ℕ} (f : Fin m → IndexedRun α)
    (B : ℕ) (h : ∀ i, StoredRectangularGivens.total (f i).run.cost ≤ B) :
    StoredRectangularGivens.total (collectIndexed f).run.cost ≤ m*(B+4) := by
  rw [c253_collect_total]
  have hs := c253_sum_le _ B h
  nlinarith

private theorem c253_collect_counts {α : Type} {m : ℕ} (f : Fin m → IndexedRun α)
    (B : ℕ) (h : ∀ i, (f i).quotientCalls ≤ B ∧ (f i).remainderCalls ≤ B) :
    (collectIndexed f).quotientCalls ≤ m*B ∧
    (collectIndexed f).remainderCalls ≤ m*B := by
  have hq := c253_sum_le (fun i => (f i).quotientCalls) B (fun i => (h i).1)
  have hr := c253_sum_le (fun i => (f i).remainderCalls) B (fun i => (h i).2)
  simpa [collectIndexed] using And.intro hq hr

private theorem c253_decode_total (d m : ℕ) (a : Fin (fiveSize d m)) :
    StoredRectangularGivens.total (decode d m a).run.cost = 4 := by
  simp only [decode, c253_total_nsmul, c253_total_tick]

private theorem c253_decode_quotients (d m : ℕ) (a : Fin (fiveSize d m)) :
    (decode d m a).quotientCalls = 2 := rfl

private theorem c253_decode_remainders (d m : ℕ) (a : Fin (fiveSize d m)) :
    (decode d m a).remainderCalls = 2 := rfl

private theorem c253_comparison_total (cut q : ℕ) (bit : Fin 2) (a b : Fin 3) :
    StoredRectangularGivens.total (comparisonQ cut q bit a b).run.cost = 3 := by
  simp [comparisonQ, charge, StoredRectangularGivens.total, tick]

private theorem c253_translation_total (L r q : ℕ) (F : Vector ℚ (L+1))
    (hr : r ≤ L) (step : ℚ) (bit : Fin 2) (i j : Fin (r+1)) :
    StoredRectangularGivens.total (translationQ L r q F hr step bit i j).cost ≤
      q+r+10 := by
  have hj := j.isLt
  by_cases h : i.val ≤ j.val
  · simp only [translationQ, dif_pos h]
    simp [bind, Run.bind, HermiteChargedSourceCache.qMul, charge,
      HermiteChargedSourceCache.chooseFrom_cost,
      HermiteCachedPiecewiseStored.powQ_cost, StoredRectangularGivens.total, tick]
    <;> omega
  · simp only [translationQ, dif_neg h]
    simp [pure, Run.pure, charge, StoredRectangularGivens.total, tick]

private theorem c253_component_total (L r q : ℕ) (F : Vector ℚ (L+1))
    (hr : r ≤ L) (cutA cutB : ℕ) (step : ℚ) (bit : Fin 2)
    (a b : ComponentIndex r) :
    StoredRectangularGivens.total
      (componentKernel L r q F hr cutA cutB step bit a b).run.cost ≤ q+r+18 := by
  have ht := c253_translation_total L r q F hr step bit a.2.2 b.2.2
  simp only [componentKernel, indexedBind, liftRun, c253_total_add,
    bind, Run.bind, HermiteChargedSourceCache.qMul, charge,
    c253_total_tick, c253_comparison_total]
  omega

private theorem c253_kernelAt_total (d m L q : ℕ) (F : Vector ℚ (L+1))
    (hd : d ≤ L) (hm : m ≤ L) (ca cb cc cd : ℕ) (step minusStep : ℚ)
    (bit : Fin 2) (a b : FiveIndex d m) :
    StoredRectangularGivens.total
      (kernelAt d m L q F hd hm ca cb cc cd step minusStep bit a b).run.cost ≤
      q+L+26 := by
  rcases a with a | a | a | a | a <;>
    rcases b with b | b | b | b | b <;>
    simp only [kernelAt, liftRun, pure, Run.pure, c253_total_add,
      c253_total_nsmul, c253_total_tick, c253_total_zero]
  all_goals first
  | omega
  | exact (Nat.add_le_add_left (c253_component_total ..) 8).trans (by omega)

private theorem c253_kernelAt_counts (d m L q : ℕ) (F : Vector ℚ (L+1))
    (hd : d ≤ L) (hm : m ≤ L) (ca cb cc cd : ℕ) (step minusStep : ℚ)
    (bit : Fin 2) (a b : FiveIndex d m) :
    (kernelAt d m L q F hd hm ca cb cc cd step minusStep bit a b).quotientCalls ≤ 2 ∧
    (kernelAt d m L q F hd hm ca cb cc cd step minusStep bit a b).remainderCalls ≤ 2 := by
  rcases a with a | a | a | a | a <;>
    rcases b with b | b | b | b | b <;>
    simp [kernelAt, componentKernel, indexedBind, liftRun, comparisonQ]

private theorem c253_kernelEntry_total (d m n L : ℕ) (F : Vector ℚ (L+1))
    (hd : d ≤ L) (hm : m ≤ L) (ca cb cc cd : ℕ) (step minusStep : ℚ)
    (q : Fin (n+1)) (a : Fin (fiveSize d m)) (j : Fin (2*fiveSize d m)) :
    StoredRectangularGivens.total
      (kernelEntry d m n L F hd hm ca cb cc cd step minusStep q a j).run.cost ≤
      n+L+34 := by
  let out : Fin 2 × Fin (fiveSize d m) := finProdFinEquiv.symm j
  have h := c253_kernelAt_total d m L q.val F hd hm ca cb cc cd step minusStep
    out.1 (decode d m a).run.value (decode d m out.2).run.value
  have hq := q.isLt
  simp only [kernelEntry, c253_total_add, c253_decode_total]
  change 4+4+StoredRectangularGivens.total
    (kernelAt d m L q.val F hd hm ca cb cc cd step minusStep out.1
      (decode d m a).run.value (decode d m out.2).run.value).run.cost ≤ _
  omega

private theorem c253_kernelEntry_counts (d m n L : ℕ) (F : Vector ℚ (L+1))
    (hd : d ≤ L) (hm : m ≤ L) (ca cb cc cd : ℕ) (step minusStep : ℚ)
    (q : Fin (n+1)) (a : Fin (fiveSize d m)) (j : Fin (2*fiveSize d m)) :
    (kernelEntry d m n L F hd hm ca cb cc cd step minusStep q a j).quotientCalls ≤ 7 ∧
    (kernelEntry d m n L F hd hm ca cb cc cd step minusStep q a j).remainderCalls ≤ 7 := by
  let out : Fin 2 × Fin (fiveSize d m) := finProdFinEquiv.symm j
  have h := c253_kernelAt_counts d m L q.val F hd hm ca cb cc cd step minusStep
    out.1 (decode d m a).run.value (decode d m out.2).run.value
  simpa only [kernelEntry, c253_decode_quotients, c253_decode_remainders,
    out] using
    And.intro (Nat.add_le_add_left h.1 5) (Nat.add_le_add_left h.2 5)

private theorem c253_componentLeft_total (r : ℕ) (origin : ℚ) (a : ComponentIndex r) :
    StoredRectangularGivens.total (componentLeft r origin a).cost ≤ r+4 := by
  have hi := a.2.2.isLt
  simp [componentLeft, bind, Run.bind, HermiteChargedSourceCache.qMul, charge,
    HermiteCachedPiecewiseStored.powQ_cost, StoredRectangularGivens.total, tick]
  omega

private theorem c253_leftAt_total (d m L : ℕ) (hd : d ≤ L) (hm : m ≤ L)
    (R minusR : ℚ) (a : FiveIndex d m) :
    StoredRectangularGivens.total (leftAt d m R minusR a).cost ≤ L+8 := by
  rcases a with a | a | a | a | a <;>
    simp only [leftAt, c253_total_add, c253_total_nsmul, c253_total_tick]
  all_goals exact (Nat.add_le_add_left (c253_componentLeft_total ..) 4).trans (by omega)

private theorem c253_leftEntry_total (d m L : ℕ) (hd : d ≤ L) (hm : m ≤ L)
    (R minusR : ℚ) (a : Fin (fiveSize d m)) :
    StoredRectangularGivens.total (leftEntry d m R minusR a).run.cost ≤ L+12 := by
  have h := c253_leftAt_total d m L hd hm R minusR (decode d m a).run.value
  simp only [leftEntry, c253_total_add, c253_decode_total]
  omega

private theorem c253_rightEntry_total (k n : ℕ) (R delta : ℚ) (d : ℕ)
    (hd : d = sourceDegree delta) (setup : HermiteCachedPiecewiseStored.RightSetup n R delta)
    (middle : Vector ℚ (2*k+2)) (a : Fin (fiveSize d (2*k+1))) :
    StoredRectangularGivens.total (rightEntry k n R delta d hd setup middle a).run.cost ≤ 19 := by
  have h := HermiteCachedPiecewiseStored.rightEntry_total_le k n R delta setup middle
    (Eq.mp (congrArg (fun e => FiveIndex e (2*k+1)) hd) (decode d (2*k+1) a).run.value)
  simp only [rightEntry, c253_total_add, c253_decode_total,
    c253_total_nsmul, c253_total_tick]
  omega

private theorem c253_materialize_total (k n : ℕ) (R delta : ℚ) (d : ℕ)
    (hd : d = sourceDegree delta) (L : ℕ) (ht : d ≤ L) (hm : 2*k+1 ≤ L)
    (setup : HermiteCachedPiecewiseStored.RightSetup n R delta)
    (middle : Vector ℚ (2*k+2)) (F : Vector ℚ (L+1)) (step minusR minusStep : ℚ) :
    StoredRectangularGivens.total
      (materializePrepared k n R delta d hd L ht hm setup middle F step minusR minusStep).run.cost ≤
      2*(n+1)*(fiveSize d (2*k+1))^2*(n+L+34) +
      fiveSize d (2*k+1)*(L+31) + 4*passContainers n (fiveSize d (2*k+1)) := by
  let D := fiveSize d (2*k+1)
  let entry := kernelEntry d (2*k+1) n L F ht hm setup.cutMinusOne setup.cutZero
    setup.cutMinusT setup.cutT step minusStep
  let tables := collectIndexed fun q : Fin (n+1) =>
    collectIndexed fun a : Fin D => collectIndexed fun j : Fin (2*D) => entry q a j
  let left := collectIndexed fun a : Fin D => leftEntry d (2*k+1) R minusR a
  let right := collectIndexed fun a : Fin D => rightEntry k n R delta d hd setup middle a
  have he (q : Fin (n+1)) (a : Fin D) (j : Fin (2*D)) :
      StoredRectangularGivens.total (entry q a j).run.cost ≤ n+L+34 :=
    c253_kernelEntry_total ..
  have htables := c253_collect_le (fun q : Fin (n+1) =>
    collectIndexed fun a : Fin D => collectIndexed fun j : Fin (2*D) => entry q a j)
    (D*(2*D*(n+L+34+4)+4)) (fun q =>
      c253_collect_le _ (2*D*(n+L+34+4)) (fun a => c253_collect_le _ _ (he q a)))
  have hleft := c253_collect_le _ (L+12)
    (fun a : Fin D => c253_leftEntry_total d (2*k+1) L ht hm R minusR a)
  have hright := c253_collect_le _ 19
    (fun a : Fin D => c253_rightEntry_total k n R delta d hd setup middle a)
  have hc : StoredRectangularGivens.total
      (materializePrepared k n R delta d hd L ht hm setup middle F step minusR minusStep).run.cost =
      StoredRectangularGivens.total tables.run.cost +
      StoredRectangularGivens.total left.run.cost + StoredRectangularGivens.total right.run.cost := by
    simp only [materializePrepared, tables, left, right, entry, D, c253_total_add]
  rw [hc]
  change _ ≤ 2*(n+1)*D^2*(n+L+34)+D*(L+31)+4*passContainers n D
  calc
    _ ≤ (n+1)*(D*(2*D*(n+L+34+4)+4)+4)+D*(L+12+4)+D*(19+4) :=
      Nat.add_le_add (Nat.add_le_add htables hleft) hright
    _ = _ := by simp only [passContainers]; ring

private theorem c253_materialize_counts (k n : ℕ) (R delta : ℚ) (d : ℕ)
    (hd : d = sourceDegree delta) (L : ℕ) (ht : d ≤ L) (hm : 2*k+1 ≤ L)
    (setup : HermiteCachedPiecewiseStored.RightSetup n R delta)
    (middle : Vector ℚ (2*k+2)) (F : Vector ℚ (L+1)) (step minusR minusStep : ℚ) :
    (materializePrepared k n R delta d hd L ht hm setup middle F step minusR minusStep).quotientCalls ≤
      14*(n+1)*(fiveSize d (2*k+1))^2+4*fiveSize d (2*k+1) ∧
    (materializePrepared k n R delta d hd L ht hm setup middle F step minusR minusStep).remainderCalls ≤
      14*(n+1)*(fiveSize d (2*k+1))^2+4*fiveSize d (2*k+1) := by
  let D := fiveSize d (2*k+1)
  let entry := kernelEntry d (2*k+1) n L F ht hm setup.cutMinusOne setup.cutZero
    setup.cutMinusT setup.cutT step minusStep
  have he (q : Fin (n+1)) (a : Fin D) (j : Fin (2*D)) :
      (entry q a j).quotientCalls ≤ 7 ∧ (entry q a j).remainderCalls ≤ 7 :=
    c253_kernelEntry_counts ..
  have htables := c253_collect_counts (fun q : Fin (n+1) =>
    collectIndexed fun a : Fin D => collectIndexed fun j : Fin (2*D) => entry q a j)
    (D*(2*D*7)) (fun q => c253_collect_counts _ (2*D*7)
      (fun a => c253_collect_counts _ 7 (he q a)))
  have hl := c253_collect_counts (fun a : Fin D => leftEntry d (2*k+1) R minusR a) 2
    (by intro a; constructor <;> exact Nat.le_refl 2)
  have hr := c253_collect_counts (fun a : Fin D => rightEntry k n R delta d hd setup middle a) 2
    (by intro a; constructor <;> exact Nat.le_refl 2)
  have heq : (n+1)*(D*(2*D*7))+D*2+D*2 = 14*(n+1)*D^2+4*D := by ring
  constructor
  · have h := Nat.add_le_add (Nat.add_le_add htables.1 hl.1) hr.1
    rw [heq] at h
    simpa only [materializePrepared, entry, D] using h
  · have h := Nat.add_le_add (Nat.add_le_add htables.2 hl.2) hr.2
    rw [heq] at h
    simpa only [materializePrepared, entry, D] using h

private theorem c253_factorials_total (L : ℕ) :
    StoredRectangularGivens.total (HermiteChargedSourceCache.factorials L).cost ≤ 80*(L+1)^2 := by
  have h1 := HermiteChargedSourceCache.factorials_cost_le L .field
  have h2 := HermiteChargedSourceCache.factorials_cost_le L .sqrt
  have h3 := HermiteChargedSourceCache.factorials_cost_le L .angle
  have h4 := HermiteChargedSourceCache.factorials_cost_le L .trig
  have h5 := HermiteChargedSourceCache.factorials_cost_le L .compare
  have h6 := HermiteChargedSourceCache.factorials_cost_le L .read
  have h7 := HermiteChargedSourceCache.factorials_cost_le L .write
  have h8 := HermiteChargedSourceCache.factorials_cost_le L .emit
  simp only [StoredRectangularGivens.total]
  omega

private theorem c253_gridStep_total (width : ℕ) (R : ℚ) :
    StoredRectangularGivens.total (HermiteCachedPiecewiseStored.gridStepRun width R).cost = width+2 := by
  simp [HermiteCachedPiecewiseStored.gridStepRun, bind, Run.bind,
    HermiteChargedSourceCache.qMul, HermiteChargedSourceCache.qDiv, charge,
    StoredRectangularGivens.total, HermiteCachedPiecewiseStored.powQ_cost, tick] <;> omega

private theorem c253_qSub_total (x y : ℚ) :
    StoredRectangularGivens.total (HermiteCachedPiecewiseStored.qSub x y).cost = 1 := by
  simp [HermiteCachedPiecewiseStored.qSub, charge, StoredRectangularGivens.total, tick]

private theorem c253_cutoff_total (delta : ℚ) :
    StoredRectangularGivens.total (HermiteCachedPiecewiseStored.cutoffQ delta).cost = 1 := by
  simp [HermiteCachedPiecewiseStored.cutoffQ, bind, Run.bind, pure, Run.pure,
    HermiteChargedSourceCache.qDiv, charge, StoredRectangularGivens.total, tick]

private theorem c253_qdata_total (k n : ℕ) (R delta : ℚ) :
    StoredRectangularGivens.total (produceExplicitQData k n R delta).run.cost ≤
      816*(k+1)^2+81*(sourceDegree delta+1)^2+8*(sourceDegree delta+1)+
      80*(sourceDegree delta+2*k+1+1)^2+
      2*(n+1)*(assemblySize k delta)^2*(n+(sourceDegree delta+2*k+1)+34)+
      assemblySize k delta*(sourceDegree delta+2*k+1+31)+
      4*passContainers n (assemblySize k delta)+2*n+HermiteFiniteExp.tailCutoff delta+28 := by
  let d := sourceDegree delta
  let L := d+2*k+1
  let D := assemblySize k delta
  let cache := (HermiteChargedSourceCache.produceSourceCache k).value
  let setup := (HermiteCachedPiecewiseStored.rightSetup n R delta).value
  let middle := (HermiteCachedPiecewiseStored.middleFromCache k setup.midpoint cache).value
  let F := (HermiteChargedSourceCache.factorials L).value.values
  let step := (HermiteCachedPiecewiseStored.gridStepRun (n+1) R).value
  let minusR := (HermiteCachedPiecewiseStored.qSub 0 R).value
  let minusStep := (HermiteCachedPiecewiseStored.qSub 0 step).value
  let pass := materializePrepared k n R delta d rfl L (by dsimp [L]; omega)
    (by dsimp [L]; omega) setup middle F step minusR minusStep
  have hp : StoredRectangularGivens.total pass.run.cost ≤
      2*(n+1)*D^2*(n+L+34)+D*(L+31)+4*passContainers n D :=
    c253_materialize_total k n R delta d rfl L (by dsimp [L]; omega)
      (by dsimp [L]; omega) setup middle F step minusR minusStep
  have hc := HermiteChargedSourceCache.produceSourceCache_total_le k
  have hm := HermiteCachedPiecewiseStored.middleFromCache_total_le k setup.midpoint cache
  have hsetup := HermiteCachedPiecewiseStored.rightSetup_total_le n R delta
  have hf := c253_factorials_total L
  have heq : StoredRectangularGivens.total (produceExplicitQData k n R delta).run.cost =
      StoredRectangularGivens.total (HermiteChargedSourceCache.produceSourceCache k).cost+
      StoredRectangularGivens.total (HermiteCachedPiecewiseStored.rightSetup n R delta).cost+
      StoredRectangularGivens.total (HermiteCachedPiecewiseStored.middleFromCache k setup.midpoint cache).cost+
      StoredRectangularGivens.total (HermiteChargedSourceCache.factorials L).cost+
      StoredRectangularGivens.total pass.run.cost+n+6 := by
    simp only [produceExplicitQData, indexedBind, liftRun, c253_total_add,
      c253_cutoff_total, c253_gridStep_total, c253_qSub_total]
    dsimp only [pass, F, L, d, setup, middle, cache, step, minusR, minusStep,
      sourceDegree]
    dsimp only [HermiteCachedPiecewiseStored.cutoffQ,
      HermiteChargedSourceCache.qDiv, charge, bind, Run.bind, pure, Run.pure,
      HermiteFiniteExp.tailCutoff]
    ring
  rw [heq]
  change _ ≤ 816*(k+1)^2+81*(d+1)^2+8*(d+1)+80*(L+1)^2+
    2*(n+1)*D^2*(n+L+34)+D*(L+31)+4*passContainers n D+
    2*n+HermiteFiniteExp.tailCutoff delta+28
  change StoredRectangularGivens.total (HermiteCachedPiecewiseStored.rightSetup n R delta).cost ≤
    81*(d+1)^2+8*(d+1)+n+HermiteFiniteExp.tailCutoff delta+22 at hsetup
  omega

private theorem c253_qdata_counts (k n : ℕ) (R delta : ℚ) :
    (produceExplicitQData k n R delta).quotientCalls ≤
      14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta ∧
    (produceExplicitQData k n R delta).remainderCalls ≤
      14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta := by
  let d := sourceDegree delta
  let L := d+2*k+1
  let setup := (HermiteCachedPiecewiseStored.rightSetup n R delta).value
  let middle := (HermiteCachedPiecewiseStored.middleFromCache k setup.midpoint
    (HermiteChargedSourceCache.produceSourceCache k).value).value
  let step := (HermiteCachedPiecewiseStored.gridStepRun (n+1) R).value
  have h := c253_materialize_counts k n R delta d rfl L (by dsimp [L]; omega)
    (by dsimp [L]; omega) setup middle (HermiteChargedSourceCache.factorials L).value.values
    step (HermiteCachedPiecewiseStored.qSub 0 R).value
    (HermiteCachedPiecewiseStored.qSub 0 step).value
  dsimp only [produceExplicitQData, indexedBind, liftRun]
  dsimp only [d, L, setup, middle, step, sourceDegree, fiveSize, assemblySize,
    HermiteCachedPiecewiseStored.cutoffQ, HermiteChargedSourceCache.qDiv,
    charge, bind, Run.bind, pure, Run.pure, HermiteFiniteExp.tailCutoff] at h ⊢
  simpa only [zero_add, add_zero] using h

private theorem c253_cast_total {n D : ℕ} (data : RationalData n D) :
    StoredRectangularGivens.total (castData data).cost = 5*passContainers n D := by
  simp [StoredRectangularGivens.total, castData_traffic, tick] <;> ring

/-- Exactly the cost/counter tail of C250's same-result root. Value refinement
is a separate dependency; it is neither assumed here nor imported from C252. -/
theorem produceExplicitStored_cost_counters :
    ∀ (k n : ℕ) (R delta : ℚ),
    let result := produceExplicitStored k n R delta
    StoredRectangularGivens.total result.run.cost ≤ frontierBudget k n delta ∧
    result.quotientCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta ∧
    result.remainderCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta := by
  intro k n R delta
  dsimp only
  constructor
  · have hq := c253_qdata_total k n R delta
    have ha := StoredMatrixProductChain.ofTable_total_cost_le
      (produceExplicitData k n R delta).run.value.tables
      (produceExplicitData k n R delta).run.value.left
      (produceExplicitData k n R delta).run.value.right
    simp only [produceExplicitData, indexedBind, liftRun] at ha
    simp only [produceExplicitStored, produceExplicitData, indexedBind, liftRun,
      c253_total_add, c253_cast_total]
    dsimp only [frontierBudget]
    simp only [passContainers] at hq ⊢
    nlinarith only [hq, ha]
  · have h := c253_qdata_counts k n R delta
    simpa only [produceExplicitStored, produceExplicitData, indexedBind, liftRun,
      add_zero] using h

end HermiteExplicitCachedStored
