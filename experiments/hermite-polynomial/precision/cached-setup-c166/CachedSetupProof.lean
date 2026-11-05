import CachedPrimitivesProof

/-! C156-sealed bounded setup-value proof candidate, not compiled by its author.
No middle/chain or cost theorem is addressed. Captured actualBlocksQ setup and
kernel/left scalar work remain unaccounted; no native runtime or sharing claim.
The source formulas are preserved for zero/negative radius or delta as well. -/

namespace HermiteCachedPiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open HermiteFiniteExpDegree

private theorem c162_strictCutFrom_value (cap : ℕ) (R step s : ℚ) :
    (strictCutFrom cap R step s).value =
      min cap (Nat.ceil ((s+R)/step)) := by
  rfl

private theorem c162_inclusiveCutFrom_value (cap : ℕ) (R step s : ℚ) :
    (inclusiveCutFrom cap R step s).value =
      min cap (if (s+R)/step < 0 then 0 else Nat.floor ((s+R)/step)+1) := by
  by_cases h : (s+R)/step < 0 <;>
    simp [inclusiveCutFrom, bind, Run.bind, HermiteChargedSourceCache.qAdd,
      HermiteChargedSourceCache.qDiv, charge, h]

private theorem c162_clippedRun_value (T : ℕ) :
    (clippedRun T).value = HermiteFiniteExp.tailRadius T/2 := by
  simp [clippedRun, bind, Run.bind, HermiteChargedSourceCache.qDiv,
    charge, powQ_value, HermiteFiniteExp.tailRadius]

/-- Only the actual generated factorial table occurs, not an assumed-correct
arbitrary table. The full finite output range is retained. -/
private theorem c162_tail_entry (d : ℕ) (i : Fin (d+1)) :
    (collect (fun j : Fin (d+1) => do
      let denominator ← QuantumBlockEncoding.StoredGivens.read
        (HermiteChargedSourceCache.factorials d).value.values j
      HermiteChargedSourceCache.qDiv 1 denominator)).value[i.val] =
      1/(i.val.factorial : ℚ) := by
  simp only [collect_value, bind, Run.bind, QuantumBlockEncoding.StoredGivens.read,
    HermiteChargedSourceCache.qDiv, charge, HermiteChargedSourceCache.factorials_value]

private theorem c162_midpointFrom_value (T d : ℕ) :
    (midpointFrom T d (HermiteChargedSourceCache.factorials d).value.values
      (HermiteFiniteExp.tailRadius T/2)).value =
      if T ≤ 1 then HermiteFiniteExp.tailRadius T/2
      else HermiteFiniteExp.poly (-1) d := by
  by_cases h : T ≤ 1
  · simp [midpointFrom, charge, bind, Run.bind, pure, Run.pure, h]
  · rw [if_neg h]
    calc
      _ = ∑ i : Fin (d+1), (-1 : ℚ)^i.val/(i.val.factorial : ℚ) := by
        simp [midpointFrom, charge, bind, Run.bind, pure, Run.pure, h,
          HermiteChargedSourceCache.sumEntries_value,
          QuantumBlockEncoding.StoredGivens.read, HermiteChargedSourceCache.qDiv,
          powQ_value, HermiteChargedSourceCache.factorials_value]
      _ = HermiteFiniteExp.poly (-1) d := by
        exact Fin.sum_univ_eq_sum_range
          (fun i : ℕ => (-1 : ℚ)^i/(i.factorial : ℚ)) (d+1)

private theorem c162_tail_test (T : ℕ) :
    (-1 : ℚ) ≤ -(T : ℚ) ↔ T ≤ 1 := by
  constructor
  · intro h
    have hcast : (T : ℚ) ≤ (1 : ℚ) := by linarith
    exact_mod_cast hcast
  · intro h
    have hcast : (T : ℚ) ≤ (1 : ℚ) := by exact_mod_cast h
    linarith

/-- The active radii cancel only in the average, not by dropping a source
error term or changing which branch is selected. -/
private theorem c162_bounds_midpoint (T d : ℕ) :
    ((HermiteFiniteExp.bounds (-1) T d).1+
      (HermiteFiniteExp.bounds (-1) T d).2)/2 =
      if T ≤ 1 then HermiteFiniteExp.tailRadius T/2
      else HermiteFiniteExp.poly (-1) d := by
  by_cases h : T ≤ 1
  · have hq := (c162_tail_test T).2 h
    simp [HermiteFiniteExp.bounds, hq, h]
  · have hq : ¬ (-1 : ℚ) ≤ -(T : ℚ) := by
      intro hq
      exact h ((c162_tail_test T).1 hq)
    simp only [HermiteFiniteExp.bounds, if_neg hq, if_neg h]
    ring

private theorem c162_midpoint_literal (T d : ℕ) :
    (midpointFrom T d (HermiteChargedSourceCache.factorials d).value.values
      (HermiteFiniteExp.tailRadius T/2)).value =
      ((HermiteFiniteExp.bounds (-1) T d).1+
        (HermiteFiniteExp.bounds (-1) T d).2)/2 := by
  rw [c162_midpointFrom_value, c162_bounds_midpoint]

theorem rightSetup_values :
    ∀ (n : ℕ) (R delta : ℚ),
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
    s.midpoint = HermiteFiniteMiddleSource.expMidpoint delta := by
  intro n R delta
  let T := HermiteFiniteExp.tailCutoff delta
  let d := sourceDegree delta
  let step := (gridStepRun (n+1) R).value
  let F := (HermiteChargedSourceCache.factorials d).value.values
  let tail := collect (fun i : Fin (d+1) => do
    let denominator ← QuantumBlockEncoding.StoredGivens.read F i
    HermiteChargedSourceCache.qDiv 1 denominator)
  let c := (clippedRun T).value
  let midpoint := (midpointFrom T d F c).value
  change
    (strictCutFrom (2^(n+1)) R step (-1)).value =
      HermitePiecewiseUniform.strictCut (n+1) R (-1) ∧
    (inclusiveCutFrom (2^(n+1)) R step 0).value =
      HermitePiecewiseUniform.inclusiveCut (n+1) R 0 ∧
    (inclusiveCutFrom (2^(n+1)) R step ((qSub 0 (T : ℚ)).value)).value =
      HermitePiecewiseUniform.inclusiveCut (n+1) R (-(T : ℚ)) ∧
    (strictCutFrom (2^(n+1)) R step (T : ℚ)).value =
      HermitePiecewiseUniform.strictCut (n+1) R (T : ℚ) ∧
    (∀ i : Fin (d+1), tail.value[i.val] = 1/(i.val.factorial : ℚ)) ∧
    c = HermitePiecewiseKernelProducer.clippedValue delta ∧
    midpoint = HermiteFiniteMiddleSource.expMidpoint delta
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [c162_strictCutFrom_value]
    dsimp only [step]
    rw [gridStepRun_value]
    rfl
  · rw [c162_inclusiveCutFrom_value]
    dsimp only [step]
    simpa only [gridStepRun_value, HermitePiecewiseUniform.inclusiveCut]
  · have minus : (qSub 0 (T : ℚ)).value = -(T : ℚ) := by
      simp [qSub, charge]
    rw [minus, c162_inclusiveCutFrom_value]
    dsimp only [step]
    simpa only [gridStepRun_value, HermitePiecewiseUniform.inclusiveCut]
  · rw [c162_strictCutFrom_value]
    dsimp only [step]
    rw [gridStepRun_value]
    rfl
  · intro i
    exact c162_tail_entry d i
  · dsimp only [c]
    rw [c162_clippedRun_value]
    rfl
  · dsimp only [midpoint, F, c]
    rw [c162_clippedRun_value, c162_midpoint_literal]
    rfl

#print axioms rightSetup_values

end HermiteCachedPiecewiseStored
