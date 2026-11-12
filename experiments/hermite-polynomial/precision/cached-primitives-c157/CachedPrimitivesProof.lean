import CachedRightSetup

/-! C156-sealed phase-3A proof candidate. This source has not been compiled by
its author. Only bounded primitive values/counters and the right-entry counter
are addressed. No complete setup, middle, chain or runtime conclusion follows.
Captured actualBlocksQ construction/setup, as well as kernel/left scalar work,
remain unaccounted; source bindings do not certify physical evaluation sharing. -/

namespace HermiteCachedPiecewiseStored
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open HermitePiecewiseAssembly

theorem powQ_value :
    ∀ (x : ℚ) (m : ℕ), (powQ x m).value = x^m := by
  intro x m
  induction m with
  | zero => simp [powQ, pure, Run.pure]
  | succ m ih =>
    simp [powQ, bind, Run.bind, HermiteChargedSourceCache.qMul, charge, ih, pow_succ]

theorem powQ_cost :
    ∀ (x : ℚ) (m : ℕ) (op : Op),
    (powQ x m).cost op = m*tick .field op := by
  intro x m op
  induction m with
  | zero => simp [powQ, pure, Run.pure]
  | succ m ih =>
    simp only [powQ, bind, Run.bind, HermiteChargedSourceCache.qMul, charge,
      Pi.add_apply]
    rw [ih]
    ring

theorem cutoffQ_value :
    ∀ (delta : ℚ),
    (cutoffQ delta).value = HermiteFiniteExp.tailCutoff delta := by
  intro delta
  rfl

theorem gridStepRun_value :
    ∀ (width : ℕ) (R : ℚ),
    (gridStepRun width R).value = HermitePiecewiseUniform.gridStepQ width R := by
  intro width R
  simp [gridStepRun, bind, Run.bind, HermiteChargedSourceCache.qMul,
    HermiteChargedSourceCache.qDiv, charge, powQ_value,
    HermitePiecewiseUniform.gridStepQ]

theorem acceptRun_value :
    ∀ (width cut : ℕ) (a : Fin 3) (flip : Bool),
    (acceptRun width cut a flip).value =
      if flip then 1-HermitePiecewiseStored.acceptQ width cut a
      else HermitePiecewiseStored.acceptQ width cut a := by
  intro width cut a flip
  cases flip <;>
    by_cases hzero : cut = 0 <;>
    by_cases hfull : cut = 2^width <;>
    by_cases haccept : a = 0 <;>
    simp [acceptRun, HermitePiecewiseStored.acceptQ, qSub,
      charge, bind, Run.bind, pure, Run.pure, hzero, hfull, haccept]

theorem acceptRun_total_le :
    ∀ (width cut : ℕ) (a : Fin 3) (flip : Bool),
    StoredRectangularGivens.total (acceptRun width cut a flip).cost ≤ 4 := by
  intro width cut a flip
  cases flip <;>
    by_cases hzero : cut = 0 <;>
    by_cases hfull : cut = 2^width <;>
    by_cases haccept : a = 0 <;>
    simp [acceptRun, qSub, charge, bind, Run.bind, pure, Run.pure,
      StoredRectangularGivens.total, tick, Pi.add_apply,
      hzero, hfull, haccept]

private theorem c157_total_add (a b : Cost) :
    StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  simp only [StoredRectangularGivens.total, Pi.add_apply]
  ring

private theorem c157_total_field_tick :
    StoredRectangularGivens.total (tick .field) = 1 := by
  simp [StoredRectangularGivens.total, tick]

private theorem c157_read_total {α : Type} {N : ℕ}
    (xs : Vector α N) (i : Fin N) :
    StoredRectangularGivens.total
      (QuantumBlockEncoding.StoredGivens.read xs i).cost = 1 := by
  simp [QuantumBlockEncoding.StoredGivens.read, charge,
    StoredRectangularGivens.total, tick]

/-- Exact compositional cost; arbitrary coefficient work remains in the sum.
No cost assumption or pure callback is inserted into a public result. -/
private theorem c157_rightProduct_total (width cutA cutB : ℕ)
    (flipA flipB : Bool) (a b : Fin 3) (coefficient : Run ℚ) :
    StoredRectangularGivens.total
        (rightProduct width cutA cutB flipA flipB a b coefficient).cost =
      StoredRectangularGivens.total (acceptRun width cutA a flipA).cost +
      StoredRectangularGivens.total (acceptRun width cutB b flipB).cost +
      StoredRectangularGivens.total coefficient.cost + 2 := by
  simp only [rightProduct, bind, Run.bind, HermiteChargedSourceCache.qMul,
    charge, c157_total_add, c157_total_field_tick]
  ring

private theorem c157_rightProduct_pure_le (width cutA cutB : ℕ)
    (flipA flipB : Bool) (a b : Fin 3) (c : ℚ) :
    StoredRectangularGivens.total
      (rightProduct width cutA cutB flipA flipB a b (pure c)).cost ≤ 11 := by
  rw [c157_rightProduct_total]
  have first := acceptRun_total_le width cutA a flipA
  have second := acceptRun_total_le width cutB b flipB
  have scalar : StoredRectangularGivens.total (pure c : Run ℚ).cost = 0 := by
    simp [pure, Run.pure, StoredRectangularGivens.total]
  rw [scalar]
  omega

private theorem c157_rightProduct_read_le {N : ℕ} (width cutA cutB : ℕ)
    (flipA flipB : Bool) (a b : Fin 3) (xs : Vector ℚ N) (i : Fin N) :
    StoredRectangularGivens.total
      (rightProduct width cutA cutB flipA flipB a b
        (QuantumBlockEncoding.StoredGivens.read xs i)).cost ≤ 11 := by
  rw [c157_rightProduct_total, c157_read_total]
  have first := acceptRun_total_le width cutA a flipA
  have second := acceptRun_total_le width cutB b flipB
  omega

theorem rightEntry_total_le :
    ∀ (k n : ℕ) (R delta : ℚ) (s : RightSetup n R delta)
      (middle : Vector ℚ (2*k+2)) (z : FullIndex k delta),
    StoredRectangularGivens.total (rightEntry k n R delta s middle z).cost ≤ 11 := by
  intro k n R delta s middle z
  rcases z with ⟨a,b,j⟩ | z
  · exact c157_rightProduct_pure_le (n+1) s.cutMinusOne s.cutMinusT
      false false a b s.clipped
  rcases z with ⟨a,b,j⟩ | z
  · exact c157_rightProduct_read_le (n+1) s.cutMinusOne s.cutMinusT
      false true a b s.tailCoeffs j
  rcases z with ⟨a,b,j⟩ | z
  · exact c157_rightProduct_read_le (n+1) s.cutMinusOne s.cutZero
      true false a b middle j
  rcases z with ⟨a,b,j⟩ | ⟨a,b,j⟩
  · exact c157_rightProduct_pure_le (n+1) s.cutZero s.cutT
      true true a b s.clipped
  · exact c157_rightProduct_read_le (n+1) s.cutZero s.cutT
      true false a b s.tailCoeffs j

#print axioms powQ_value
#print axioms powQ_cost
#print axioms cutoffQ_value
#print axioms gridStepRun_value
#print axioms acceptRun_value
#print axioms acceptRun_total_le
#print axioms rightEntry_total_le

end HermiteCachedPiecewiseStored
