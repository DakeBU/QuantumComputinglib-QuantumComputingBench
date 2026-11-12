import CachedPrimitivesProof

/-! C183 proof-only successor to the preserved failed C176 candidate.
The C156 target and C150 executable bodies are unchanged. Only original-guard
elimination and matching bind-normalization of the final bound are repaired.
Only the eight-counter scalar/word annotation is bounded. Captured actualBlocksQ
construction/setup and kernel/left scalar work remain unaccounted. This is not
a native runtime, bitlength, GCD, sharing, or physical one-evaluation theorem.
The author has not compiled this packet; a fresh parent gate is required. -/

namespace HermiteCachedPiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens

private theorem c176_total_add (x y : Cost) :
    StoredRectangularGivens.total (x+y) =
      StoredRectangularGivens.total x + StoredRectangularGivens.total y := by
  simp only [StoredRectangularGivens.total, Pi.add_apply]
  ring

private theorem c176_total_field :
    StoredRectangularGivens.total (tick .field) = 1 := by
  simp [StoredRectangularGivens.total, tick]

private theorem c176_pow_total (x : ℚ) (m : ℕ) :
    StoredRectangularGivens.total (powQ x m).cost = m := by
  simp [StoredRectangularGivens.total, powQ_cost, tick]

private theorem c176_collect_total {α : Type} {n : ℕ} (f : Fin n → Run α) :
    StoredRectangularGivens.total (collect f).cost =
      (∑ i : Fin n, StoredRectangularGivens.total (f i).cost) + 4*n := by
  simp [StoredRectangularGivens.total, collect_cost, tick, Finset.sum_add_distrib]
  <;> ring

private theorem c176_collect_le {α : Type} {n : ℕ} (f : Fin n → Run α)
    (B : ℕ) (h : ∀ i, StoredRectangularGivens.total (f i).cost ≤ B) :
    StoredRectangularGivens.total (collect f).cost ≤ n*(B+4) := by
  rw [c176_collect_total]
  have hs : (∑ i : Fin n, StoredRectangularGivens.total (f i).cost) ≤ n*B := by
    calc
      _ ≤ ∑ _i : Fin n, B := Finset.sum_le_sum (fun i _ => h i)
      _ = _ := by simp
  nlinarith

private theorem c176_sum_total {n : ℕ} (f : Fin n → Run ℚ) :
    StoredRectangularGivens.total (HermiteChargedSourceCache.sumEntries f).cost =
      (∑ i : Fin n, StoredRectangularGivens.total (f i).cost) + n := by
  induction n with
  | zero => simp [HermiteChargedSourceCache.sumEntries, pure, Run.pure,
      StoredRectangularGivens.total]
  | succ n ih =>
    simp only [HermiteChargedSourceCache.sumEntries, bind, Run.bind,
      HermiteChargedSourceCache.qAdd, charge, c176_total_add, c176_total_field]
    rw [ih, Fin.sum_univ_succ]
    ring

private theorem c176_sum_le {n : ℕ} (f : Fin n → Run ℚ) (B : ℕ)
    (h : ∀ i, StoredRectangularGivens.total (f i).cost ≤ B) :
    StoredRectangularGivens.total (HermiteChargedSourceCache.sumEntries f).cost ≤
      n*(B+1) := by
  rw [c176_sum_total]
  have hs : (∑ i : Fin n, StoredRectangularGivens.total (f i).cost) ≤ n*B := by
    calc
      _ ≤ ∑ _i : Fin n, B := Finset.sum_le_sum (fun i _ => h i)
      _ = _ := by simp
  nlinarith

private theorem c176_factorials_total (n : ℕ) :
    StoredRectangularGivens.total (HermiteChargedSourceCache.factorials n).cost ≤
      80*(n+1)^2 := by
  have hf := HermiteChargedSourceCache.factorials_cost_le n .field
  have hs := HermiteChargedSourceCache.factorials_cost_le n .sqrt
  have ha := HermiteChargedSourceCache.factorials_cost_le n .angle
  have ht := HermiteChargedSourceCache.factorials_cost_le n .trig
  have hc := HermiteChargedSourceCache.factorials_cost_le n .compare
  have hr := HermiteChargedSourceCache.factorials_cost_le n .read
  have hw := HermiteChargedSourceCache.factorials_cost_le n .write
  have he := HermiteChargedSourceCache.factorials_cost_le n .emit
  simp only [StoredRectangularGivens.total]
  omega

private theorem c176_weighted_total (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)) :
    StoredRectangularGivens.total (weightedSources k e a).cost ≤ 14*(k+1)^2 := by
  let first : Fin (k+1) → Run ℚ := fun i => do
    let x ← QuantumBlockEncoding.StoredGivens.read a i
    let scaled ← HermiteChargedSourceCache.qMul e x
    HermiteChargedSourceCache.qMul scaled (powQ (-1) (k+1)).value
  let second : Fin (k+1) → Run ℚ := fun i => do
    let x ← QuantumBlockEncoding.StoredGivens.read a i
    let sign ← powQ (-1) i.val
    HermiteChargedSourceCache.qMul x sign
  have hfirst := c176_collect_le first 3 (by
    intro i
    simp [first, bind, Run.bind, QuantumBlockEncoding.StoredGivens.read,
      HermiteChargedSourceCache.qMul, charge, StoredRectangularGivens.total, tick])
  have hsecond := c176_collect_le second (k+2) (by
    intro i
    have hi := i.isLt
    simp [second, bind, Run.bind, QuantumBlockEncoding.StoredGivens.read,
      HermiteChargedSourceCache.qMul, charge, StoredRectangularGivens.total,
      powQ_cost, tick] <;> omega)
  have hcost : StoredRectangularGivens.total (weightedSources k e a).cost =
      (k+1) + StoredRectangularGivens.total (collect first).cost +
        StoredRectangularGivens.total (collect second).cost := by
    change StoredRectangularGivens.total
      ((powQ (-1) (k+1)).cost + ((collect first).cost + ((collect second).cost + 0))) = _
    simp only [c176_total_add, c176_pow_total]
    simp [StoredRectangularGivens.total]
    <;> ring
  rw [hcost]
  nlinarith [Nat.zero_le (k*(k+1))]

private theorem c176_first_term_le (k : ℕ) (F : Vector ℚ (2*k+2))
    (u : Vector ℚ (k+1)) (j : Fin (2*k+2)) (i : Fin (k+1)) :
    StoredRectangularGivens.total (middleFirstTerm k F u j i).cost ≤ 9 := by
  by_cases h : k+1 ≤ j.val ∧ j.val-(k+1) ≤ i.val
  · simp only [middleFirstTerm, dif_pos h]
    simp [bind, Run.bind, QuantumBlockEncoding.StoredGivens.read,
      HermiteChargedSourceCache.qMul, charge, StoredRectangularGivens.total,
      Pi.add_apply, HermiteChargedSourceCache.chooseFrom_cost, tick]
  · simp only [middleFirstTerm, dif_neg h]
    simp [pure, Run.pure, StoredRectangularGivens.total, tick]

private theorem c176_second_term_le (k : ℕ) (F : Vector ℚ (2*k+2))
    (v : Vector ℚ (k+1)) (j : Fin (2*k+2)) (i : Fin (k+1)) :
    StoredRectangularGivens.total (middleSecondTerm k F v j i).cost ≤ 9 := by
  by_cases h : i.val ≤ j.val ∧ j.val-i.val ≤ k+1
  · simp only [middleSecondTerm, dif_pos h]
    simp [bind, Run.bind, QuantumBlockEncoding.StoredGivens.read,
      HermiteChargedSourceCache.qMul, charge, StoredRectangularGivens.total,
      Pi.add_apply, HermiteChargedSourceCache.chooseFrom_cost, tick]
  · simp only [middleSecondTerm, dif_neg h]
    simp [pure, Run.pure, StoredRectangularGivens.total, tick]

private theorem c176_table_total (k : ℕ) (F : Vector ℚ (2*k+2))
    (weights : WeightedSources k) :
    StoredRectangularGivens.total (collect fun j : Fin (2*k+2) => do
      let first ← HermiteChargedSourceCache.sumEntries
        (middleFirstTerm k F weights.first j)
      let second ← HermiteChargedSourceCache.sumEntries
        (middleSecondTerm k F weights.second j)
      HermiteChargedSourceCache.qAdd first second).cost ≤ 50*(k+1)^2 := by
  have hentry : ∀ j : Fin (2*k+2),
      StoredRectangularGivens.total (do
        let first ← HermiteChargedSourceCache.sumEntries
          (middleFirstTerm k F weights.first j)
        let second ← HermiteChargedSourceCache.sumEntries
          (middleSecondTerm k F weights.second j)
        HermiteChargedSourceCache.qAdd first second : Run ℚ).cost ≤ 20*(k+1)+1 := by
    intro j
    have hf := c176_sum_le (middleFirstTerm k F weights.first j) 9
      (c176_first_term_le k F weights.first j)
    have hs := c176_sum_le (middleSecondTerm k F weights.second j) 9
      (c176_second_term_le k F weights.second j)
    simp only [bind, Run.bind, HermiteChargedSourceCache.qAdd, charge,
      c176_total_add, c176_total_field]
    omega
  have hc := c176_collect_le (fun j : Fin (2*k+2) => do
    let first ← HermiteChargedSourceCache.sumEntries
      (middleFirstTerm k F weights.first j)
    let second ← HermiteChargedSourceCache.sumEntries
      (middleSecondTerm k F weights.second j)
    HermiteChargedSourceCache.qAdd first second) (20*(k+1)+1) hentry
  nlinarith [Nat.zero_le (k*(k+1))]

theorem middleFromCache_total_le :
    ∀ (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)),
    StoredRectangularGivens.total (middleFromCache k e a).cost ≤ 400*(k+1)^2 := by
  intro k e a
  have hf := c176_factorials_total (2*k+1)
  have hw := c176_weighted_total k e a
  have ht := c176_table_total k
    (HermiteChargedSourceCache.factorials (2*k+1)).value.values
    (weightedSources k e a).value
  simp only [bind, Run.bind] at ht
  simp only [middleFromCache, bind, Run.bind, c176_total_add]
  nlinarith [Nat.zero_le ((k+1)^2)]

end HermiteCachedPiecewiseStored
