import CachedPrimitivesProof

/-! C156-sealed bounded middle VALUE proof candidate. Not compiled by its
author. No cost400, right-value or chain theorem is asserted here. All scalar
signs and full finite index ranges are retained. Native/captured-block setup,
kernel/left work, bitlength/GCD and physical runtime remain outside this claim. -/

namespace HermiteCachedPiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens

private theorem c167_weighted_first (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1))
    (i : Fin (k+1)) :
    (weightedSources k e a).value.first[i.val] = e*a[i.val]*(-1)^(k+1) := by
  simp [weightedSources, bind, Run.bind, pure, Run.pure,
    QuantumBlockEncoding.StoredGivens.read, HermiteChargedSourceCache.qMul,
    charge, powQ_value]

private theorem c167_weighted_second (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1))
    (i : Fin (k+1)) :
    (weightedSources k e a).value.second[i.val] = a[i.val]*(-1)^i.val := by
  simp [weightedSources, bind, Run.bind, pure, Run.pure,
    QuantumBlockEncoding.StoredGivens.read, HermiteChargedSourceCache.qMul,
    charge, powQ_value]

/-- The factorial correctness dependency is supplied by the actual generated
table, not by a caller's correctness premise. hr/hn only type the accesses. -/
private theorem c167_generated_choose (N n r : ℕ) (hr : r ≤ n) (hn : n ≤ N) :
    (HermiteChargedSourceCache.chooseFrom
      (HermiteChargedSourceCache.factorials N).value.values n r hr hn).value =
      (Nat.choose n r : ℚ) := by
  exact HermiteChargedSourceCache.chooseFrom_value _
    (HermiteChargedSourceCache.factorials_value N) n r hr hn

private theorem c167_first_term (k : ℕ) (u : Vector ℚ (k+1))
    (j : Fin (2*k+2)) (i : Fin (k+1)) :
    (middleFirstTerm k
      (HermiteChargedSourceCache.factorials (2*k+1)).value.values u j i).value =
      if k+1 ≤ j.val then
        u[i.val]*(Nat.choose i.val (j.val-(k+1)) : ℚ) else 0 := by
  by_cases hstart : k+1 ≤ j.val
  · by_cases hbinomial : j.val-(k+1) ≤ i.val
    · simp [middleFirstTerm, hstart, hbinomial, bind, Run.bind,
        QuantumBlockEncoding.StoredGivens.read, HermiteChargedSourceCache.qMul,
        charge, c167_generated_choose]
    · have hzero : Nat.choose i.val (j.val-(k+1)) = 0 :=
        Nat.choose_eq_zero_of_lt (by omega)
      simp [middleFirstTerm, hstart, hbinomial, hzero, pure, Run.pure]
  · simp [middleFirstTerm, hstart, pure, Run.pure]

private theorem c167_second_term (k : ℕ) (v : Vector ℚ (k+1))
    (j : Fin (2*k+2)) (i : Fin (k+1)) :
    (middleSecondTerm k
      (HermiteChargedSourceCache.factorials (2*k+1)).value.values v j i).value =
      if i.val ≤ j.val then
        v[i.val]*(Nat.choose (k+1) (j.val-i.val) : ℚ) else 0 := by
  by_cases hstart : i.val ≤ j.val
  · by_cases hbinomial : j.val-i.val ≤ k+1
    · simp [middleSecondTerm, hstart, hbinomial, bind, Run.bind,
        QuantumBlockEncoding.StoredGivens.read, HermiteChargedSourceCache.qMul,
        charge, c167_generated_choose]
    · have hzero : Nat.choose (k+1) (j.val-i.val) = 0 :=
        Nat.choose_eq_zero_of_lt (by omega)
      simp [middleSecondTerm, hstart, hbinomial, hzero, pure, Run.pure]
  · simp [middleSecondTerm, hstart, pure, Run.pure]

theorem middleFromCache_entry :
    ∀ (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)) (j : Fin (2*k+2)),
    (middleFromCache k e a).value[j.val] = middleExpr k e a j := by
  intro k e a j
  simp only [middleFromCache, bind, Run.bind, collect_value,
    HermiteChargedSourceCache.qAdd, charge, HermiteChargedSourceCache.sumEntries_value,
    c167_first_term, c167_second_term, c167_weighted_first,
    c167_weighted_second, middleExpr]

theorem actual_cache_middle :
    ∀ (k : ℕ) (delta : ℚ) (j : Fin (2*k+2)),
    (middleFromCache k (HermiteFiniteMiddleSource.expMidpoint delta)
      (HermiteChargedSourceCache.produceSourceCache k).value).value[j.val] =
      HermitePiecewiseAssembly.middleCoeffQ k delta j.val := by
  intro k delta j
  rw [middleFromCache_entry]
  simp only [middleExpr, HermiteChargedSourceCache.produceSourceCache_entry,
    HermitePiecewiseAssembly.middleCoeffQ]
  congr 1
  · exact Fin.sum_univ_eq_sum_range
      (fun i : ℕ =>
        if k+1 ≤ j.val then
          HermiteFiniteMiddleSource.expMidpoint delta*
            HermitePiecewiseAssembly.sourceCoefficientQ k i*(-1)^(k+1)*
            (Nat.choose i (j.val-(k+1)) : ℚ)
        else 0) (k+1)
  · exact Fin.sum_univ_eq_sum_range
      (fun i : ℕ =>
        if i ≤ j.val then
          HermitePiecewiseAssembly.sourceCoefficientQ k i*(-1)^i*
            (Nat.choose (k+1) (j.val-i) : ℚ)
        else 0) (k+1)

#print axioms middleFromCache_entry
#print axioms actual_cache_middle

end HermiteCachedPiecewiseStored
