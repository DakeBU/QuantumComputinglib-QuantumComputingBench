import CachedPrimitivesProof

/-! C217 author-uncompiled proof-only successor of C212/C216 for the exact C202 internal
rightSetup counter target. C150 bodies and original C156 targets are unchanged.
Only the eight-counter annotation is bounded, not native/bit/GCD/evaluator
runtime, sharing, captured block setup, kernel/left work, or quantum resources. -/

namespace HermiteCachedPiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens

-- Local counter bookkeeping, not new executable producers or foundations.
private theorem c204_total_add (x y : Cost) :
    StoredRectangularGivens.total (x+y) =
      StoredRectangularGivens.total x + StoredRectangularGivens.total y := by
  simp only [StoredRectangularGivens.total, Pi.add_apply]
  ring

private theorem c204_total_zero : StoredRectangularGivens.total (0 : Cost) = 0 := by
  simp [StoredRectangularGivens.total]

private theorem c204_total_tick (op : Op) :
    StoredRectangularGivens.total (tick op) = 1 := by
  cases op <;> simp [StoredRectangularGivens.total, tick]

private theorem c204_collect_total {α : Type} {m : ℕ} (f : Fin m → Run α) :
    StoredRectangularGivens.total (collect f).cost =
      (∑ i : Fin m, StoredRectangularGivens.total (f i).cost) + 4*m := by
  simp [StoredRectangularGivens.total, collect_cost, tick, Finset.sum_add_distrib]
  <;> ring

/-- The extra one per element includes addition to the empty suffix. -/
private theorem c204_sum_le {m : ℕ} (f : Fin m → Run ℚ) (B : ℕ)
    (h : ∀ i, StoredRectangularGivens.total (f i).cost ≤ B) :
    StoredRectangularGivens.total (HermiteChargedSourceCache.sumEntries f).cost ≤
      m*(B+1) := by
  induction m with
  | zero =>
      simp [HermiteChargedSourceCache.sumEntries, pure, Run.pure,
        StoredRectangularGivens.total]
  | succ m ih =>
      simp only [HermiteChargedSourceCache.sumEntries, bind, Run.bind,
        HermiteChargedSourceCache.qAdd, charge, c204_total_add, c204_total_tick]
      have first := h 0
      have rest := ih (fun i : Fin m => f i.succ) (fun i => h i.succ)
      rw [Nat.succ_mul]
      omega

/-- Convert the original per-counter factorial bound to all eight counters. -/
private theorem c204_factorials_total (d : ℕ) :
    StoredRectangularGivens.total (HermiteChargedSourceCache.factorials d).cost ≤
      80*(d+1)^2 := by
  have hf := HermiteChargedSourceCache.factorials_cost_le d .field
  have hs := HermiteChargedSourceCache.factorials_cost_le d .sqrt
  have ha := HermiteChargedSourceCache.factorials_cost_le d .angle
  have ht := HermiteChargedSourceCache.factorials_cost_le d .trig
  have hc := HermiteChargedSourceCache.factorials_cost_le d .compare
  have hr := HermiteChargedSourceCache.factorials_cost_le d .read
  have hw := HermiteChargedSourceCache.factorials_cost_le d .write
  have he := HermiteChargedSourceCache.factorials_cost_le d .emit
  simp only [StoredRectangularGivens.total]
  omega

private theorem c204_cutoff_total (delta : ℚ) :
    StoredRectangularGivens.total (cutoffQ delta).cost = 1 := by
  simp [cutoffQ, bind, Run.bind, pure, Run.pure,
    HermiteChargedSourceCache.qDiv, charge, StoredRectangularGivens.total, tick]

private theorem c204_gridStep_total (width : ℕ) (R : ℚ) :
    StoredRectangularGivens.total (gridStepRun width R).cost = width+2 := by
  simp [gridStepRun, bind, Run.bind, HermiteChargedSourceCache.qMul,
    HermiteChargedSourceCache.qDiv, charge, StoredRectangularGivens.total,
    powQ_cost, tick] <;> omega

private theorem c204_strict_total (cap : ℕ) (R step s : ℚ) :
    StoredRectangularGivens.total (strictCutFrom cap R step s).cost = 3 := by
  simp [strictCutFrom, bind, Run.bind, HermiteChargedSourceCache.qAdd,
    HermiteChargedSourceCache.qDiv, charge, StoredRectangularGivens.total, tick]

private theorem c204_inclusive_total (cap : ℕ) (R step s : ℚ) :
    StoredRectangularGivens.total (inclusiveCutFrom cap R step s).cost = 4 := by
  simp [inclusiveCutFrom, bind, Run.bind, HermiteChargedSourceCache.qAdd,
    HermiteChargedSourceCache.qDiv, charge, StoredRectangularGivens.total, tick]

private theorem c204_qSub_total (x y : ℚ) :
    StoredRectangularGivens.total (qSub x y).cost = 1 := by
  simp [qSub, charge, StoredRectangularGivens.total, tick]

private theorem c204_clipped_total (T : ℕ) :
    StoredRectangularGivens.total (clippedRun T).cost = T+2 := by
  simp [clippedRun, bind, Run.bind, HermiteChargedSourceCache.qDiv, charge,
    StoredRectangularGivens.total, powQ_cost, tick] <;> omega

/-- Arbitrary stored F is enough for the cost; no correctness promise. -/
private theorem c204_tail_total (d : ℕ) (F : Vector ℚ (d+1)) :
    StoredRectangularGivens.total (collect fun i : Fin (d+1) => do
      let denominator ← QuantumBlockEncoding.StoredGivens.read F i
      HermiteChargedSourceCache.qDiv 1 denominator).cost = 6*(d+1) := by
  rw [c204_collect_total]
  simp [bind, Run.bind, QuantumBlockEncoding.StoredGivens.read,
    HermiteChargedSourceCache.qDiv, charge, StoredRectangularGivens.total, tick]
  <;> ring

/-- Uniform over both the literal T<=1 branch and arbitrary rational data. -/
private theorem c204_midpoint_total (T d : ℕ) (F : Vector ℚ (d+1)) (c : ℚ) :
    StoredRectangularGivens.total (midpointFrom T d F c).cost ≤
      1+(d+1)*(d+3) := by
  let terms : Fin (d+1) → Run ℚ := fun i => do
    let numerator ← powQ (-1) i.val
    let denominator ← QuantumBlockEncoding.StoredGivens.read F i
    HermiteChargedSourceCache.qDiv numerator denominator
  have hs : StoredRectangularGivens.total
      (HermiteChargedSourceCache.sumEntries terms).cost ≤ (d+1)*(d+3) := by
    apply c204_sum_le terms (d+2)
    intro i
    have hi := i.isLt
    simp [terms, bind, Run.bind, QuantumBlockEncoding.StoredGivens.read,
      HermiteChargedSourceCache.qDiv, charge, StoredRectangularGivens.total,
      powQ_cost, tick] <;> omega
  by_cases h : T ≤ 1
  · have hc : StoredRectangularGivens.total (midpointFrom T d F c).cost = 1 := by
      simp [midpointFrom, bind, Run.bind, charge, pure, Run.pure, h,
        StoredRectangularGivens.total, tick]
    rw [hc]
    omega
  · have hc : StoredRectangularGivens.total (midpointFrom T d F c).cost =
        1+StoredRectangularGivens.total
          (HermiteChargedSourceCache.sumEntries terms).cost := by
      simp [midpointFrom, terms, bind, Run.bind, charge, h,
        c204_total_add, c204_total_tick]
    rw [hc]
    omega

theorem rightSetup_total_le :
  ∀ (n : ℕ) (R delta : ℚ),
  StoredRectangularGivens.total (rightSetup n R delta).cost ≤
    81*(HermiteFiniteExpDegree.sourceDegree delta+1)^2 +
    8*(HermiteFiniteExpDegree.sourceDegree delta+1) + n +
    HermiteFiniteExp.tailCutoff delta + 22 := by
  intro n R delta
  let T := HermiteFiniteExp.tailCutoff delta
  let d := HermiteFiniteExpDegree.sourceDegree delta
  let F := (HermiteChargedSourceCache.factorials d).value.values
  let tailRun : Run (Vector ℚ (d+1)) := collect fun i : Fin (d+1) => do
    let denominator ← QuantumBlockEncoding.StoredGivens.read F i
    HermiteChargedSourceCache.qDiv 1 denominator
  let c := (clippedRun T).value
  have hf := c204_factorials_total d
  have ht : StoredRectangularGivens.total tailRun.cost = 6*(d+1) :=
    c204_tail_total d F
  have hm := c204_midpoint_total T d F c
  have hc : StoredRectangularGivens.total (rightSetup n R delta).cost =
      n+T+21 +
        StoredRectangularGivens.total (HermiteChargedSourceCache.factorials d).cost +
        StoredRectangularGivens.total tailRun.cost +
        StoredRectangularGivens.total (midpointFrom T d F c).cost := by
    simp only [rightSetup, bind, Run.bind, cutoffQ_value,
      c204_total_add, c204_cutoff_total, c204_gridStep_total,
      c204_strict_total, c204_inclusive_total, c204_qSub_total,
      c204_clipped_total, pure, Run.pure, c204_total_zero]
    dsimp only [d, T, F, tailRun, c, HermiteFiniteExpDegree.sourceDegree,
      bind, Run.bind, pure, Run.pure]
    dsimp only [cutoffQ, HermiteChargedSourceCache.qDiv, charge,
      bind, Run.bind, pure, Run.pure, HermiteFiniteExp.tailCutoff]
    ring
  change StoredRectangularGivens.total (rightSetup n R delta).cost ≤
    81*(d+1)^2+8*(d+1)+n+T+22
  rw [hc, ht]
  nlinarith

end HermiteCachedPiecewiseStored
