import QuantumBlockEncoding.HermiteBoundaryInjection
import QuantumBlockEncoding.StoredGivens

/-!
# Exact-comparison binary search for the Hermite source cutoff

The implementation carries real interval endpoints instead of evaluating a
natural ceiling or enumerating the grid. Its counters cover real arithmetic
and exact real comparisons. Natural index arithmetic, powers of two, and
counter bookkeeping are outside this scalar model; finite-bit comparison of
arbitrary real inputs is not claimed. In particular this does not remove the
input/separation issue recorded in the classical-cost audit.
-/

namespace QuantumBlockEncoding.HermiteBinaryCutoff

open StoredGivens HermiteBoundaryInjection

noncomputable def below (x : ℝ) : Run Bool :=
  charge .compare (decide (x < -1))

/-- Search an interval with `2^remaining` grid cells. `lower` is its first
grid point and `span` its full real width. No grid-sized table is built. -/
noncomputable def search : (remaining start : ℕ) → (lower span : ℝ) → Run ℕ
  | 0, start, lower, _ => do
      let yes ← below lower
      pure (if yes then start + 1 else start)
  | remaining + 1, start, lower, span => do
      let half ← StoredGivens.div span 2
      let middle ← StoredGivens.add lower half
      let yes ← below middle
      if yes then search remaining (start + 2 ^ remaining) middle half
      else search remaining start lower half

theorem search_cost (remaining start : ℕ) (lower span : ℝ) (op : Op) :
    (search remaining start lower span).cost op =
      2 * remaining * tick .field op + (remaining + 1) * tick .compare op := by
  induction remaining generalizing start lower span with
  | zero =>
      simp [search, below, charge, bind, pure, Run.bind, Run.pure]
  | succ remaining ih =>
      simp only [search, StoredGivens.div, StoredGivens.add, below, charge,
        bind, Run.bind]
      by_cases h : lower + span / 2 < -1 <;> simp [h, ih] <;> ring

private theorem half_span (step : ℝ) (remaining : ℕ) :
    (step * (2 : ℝ) ^ (remaining + 1)) / 2 = step * (2 : ℝ) ^ remaining := by
  rw [pow_succ]
  ring

private theorem middle_point (n remaining start : ℕ) (L : ℝ) :
    gridPointNat n L start + gridStep n L * (2 : ℝ) ^ remaining =
      gridPointNat n L (start + 2 ^ remaining) := by
  simp only [gridPointNat, affinePoint, Nat.cast_add, Nat.cast_pow, Nat.cast_ofNat]
  ring

/-- A full interval invariant proves the actual returned index, including
the cutoff at either endpoint and the one-cell case. -/
theorem search_value (n remaining start : ℕ) (L : ℝ) (hL : 0 < L)
    (hlo : start ≤ cutIndex n L) (hhi : cutIndex n L ≤ start + 2 ^ remaining) :
    (search remaining start (gridPointNat n L start)
      (gridStep n L * (2 : ℝ) ^ remaining)).value = cutIndex n L := by
  induction remaining generalizing start with
  | zero =>
      simp only [search, below, charge, bind, pure, Run.bind, Run.pure]
      by_cases h : gridPointNat n L start < -1
      · have hc := (gridPointNat_lt_neg_one_iff n L hL start).mp h
        simp [h]
        norm_num at hhi
        omega
      · have hc : ¬ start < cutIndex n L := by
          intro hc
          exact h ((gridPointNat_lt_neg_one_iff n L hL start).mpr hc)
        simp [h]
        omega
  | succ remaining ih =>
      simp only [search, StoredGivens.div, StoredGivens.add, below, charge,
        bind, Run.bind, half_span, middle_point]
      by_cases h : gridPointNat n L (start + 2 ^ remaining) < -1
      · simp only [h, decide_true, if_true]
        apply ih
        · have := (gridPointNat_lt_neg_one_iff n L hL _).mp h
          omega
        · rw [pow_succ] at hhi
          omega
      · simp only [h, decide_false, Bool.false_eq_true, if_false]
        apply ih start hlo
        have hc : ¬ start + 2 ^ remaining < cutIndex n L := by
          intro hc
          exact h ((gridPointNat_lt_neg_one_iff n L hL _).mpr hc)
        omega

/-- Source-level producer: one multiplication and negation initialize the
interval from `-pi*L` to zero, then binary search finds its cutoff. -/
noncomputable def compute (n : ℕ) (L : ℝ) : Run ℕ := do
  let width ← StoredGivens.mul Real.pi L
  let lower ← StoredGivens.sub 0 width
  search n 0 lower width

private theorem root_span (n : ℕ) (L : ℝ) :
    gridStep n L * (2 : ℝ) ^ n = Real.pi * L := by
  simp only [gridStep, gridSize, pow_succ]
  have hp : (2 : ℝ) ^ n ≠ 0 := pow_ne_zero _ (by norm_num)
  field_simp
  push_cast
  ring

theorem compute_value (n : ℕ) (L : ℝ) (hL : 0 < L) :
    (compute n L).value = cutIndex n L := by
  have h := search_value n n 0 L hL (Nat.zero_le _) (by
    simpa using cutIndex_le_midpoint n L hL)
  simpa [compute, StoredGivens.mul, StoredGivens.sub, charge, bind, Run.bind,
    gridPointNat, affinePoint, root_span] using h

theorem compute_cost (n : ℕ) (L : ℝ) (op : Op) :
    (compute n L).cost op =
      (2 * n + 2) * tick .field op + (n + 1) * tick .compare op := by
  simp [compute, StoredGivens.mul, StoredGivens.sub, charge, bind, Run.bind,
    search_cost]
  ring

theorem compute_comparisons (n : ℕ) (L : ℝ) :
    (compute n L).cost .compare = n + 1 := by
  simp [compute_cost, tick]

theorem compute_field_operations (n : ℕ) (L : ℝ) :
    (compute n L).cost .field = 2 * n + 2 := by
  simp [compute_cost, tick]

end QuantumBlockEncoding.HermiteBinaryCutoff
