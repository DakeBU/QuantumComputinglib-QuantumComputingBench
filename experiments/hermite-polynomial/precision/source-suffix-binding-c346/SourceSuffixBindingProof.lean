import SourceSuffixDefinitions
import Mathlib.Algebra.BigOperators.Intervals

namespace HermiteSourceSuffix

open scoped BigOperators
open QuantumBlockEncoding.StoredGivens

private theorem actualFactorials_entry (k : ℕ) (r : Fin (2*k+2)) :
    (actualFactorials k)[r.val] = (r.val.factorial : ℚ) := by
  exact HermiteChargedSourceCache.factorials_value (2*k+1) r

private theorem actualSourceTerm_value (k : ℕ) (i : Fin (k+1))
    (r : Fin (i.val+1)) :
    (actualSourceTerm k i r).value =
      (Nat.choose (k+i.val-r.val) k : ℚ)/(r.val.factorial : ℚ) := by
  simp only [actualSourceTerm, bind, Run.bind,
    QuantumBlockEncoding.StoredGivens.read, HermiteChargedSourceCache.qDiv, charge,
    HermiteChargedSourceCache.chooseFrom_value (actualFactorials k)
      (actualFactorials_entry k)]
  rw [actualFactorials_entry k ⟨r.val, by omega⟩]

private theorem suffix_eq_math (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)) :
    actualSuffixObservation k i s = SourceSuffix k i s := by
  unfold actualSuffixObservation SourceSuffix
  rw [HermiteChargedSourceCache.sumEntries_value,
    Finset.sum_Ico_eq_sum_range, ← Fin.sum_univ_eq_sum_range]
  apply Finset.sum_congr rfl
  intro r _
  simpa only [droppedTerms] using
    (actualSourceTerm_value k i ⟨s.val+r.val, by
      have hr := r.isLt
      have hs := s.isLt
      omega⟩)

private theorem suffix_zero (k : ℕ) (i : Fin (k+1)) :
    actualSuffixObservation k i ⟨0, by omega⟩ =
      (HermiteChargedSourceCache.sourceEntry k (actualFactorials k) i).value := by
  rw [suffix_eq_math,
    HermiteChargedSourceCache.sourceEntry_value k (actualFactorials k)
      (actualFactorials_entry k) i]
  change (∑ r ∈ Finset.Ico 0 (i.val+1),
    (Nat.choose (k+i.val-r) k : ℚ)/(r.factorial : ℚ)) =
    ∑ r ∈ Finset.range (i.val+1),
      (Nat.choose (k+i.val-r) k : ℚ)/(r.factorial : ℚ)
  rw [Nat.Ico_zero_eq_range]

private theorem tail_eq_next (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2))
    (h : s.val < i.val+1) :
    actualTailObservation k i s =
      actualSuffixObservation k i ⟨s.val+1, by omega⟩ := by
  rw [suffix_eq_math]
  unfold SourceSuffix
  rw [Finset.sum_Ico_eq_sum_range]
  have hlen : i.val+1-(s.val+1) = i.val-s.val := by omega
  rw [hlen]
  simp only [actualTailObservation, dif_pos h,
    HermiteChargedSourceCache.sumEntries_value, droppedTerms, actualSourceTerm_value]
  rw [← Fin.sum_univ_eq_sum_range]
  apply Finset.sum_congr rfl
  intro r _
  have heq : s.val+(r.val+1) = s.val+1+r.val := by omega
  rw [heq]

private theorem suffix_head_tail (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2))
    (h : s.val < i.val+1) :
    actualSuffixObservation k i s =
      (actualSourceTerm k i ⟨s.val, h⟩).value + actualTailObservation k i s := by
  rw [suffix_eq_math k i s, actualSourceTerm_value, tail_eq_next k i s h,
    suffix_eq_math]
  change (∑ r ∈ Finset.Ico s.val (i.val+1),
    (Nat.choose (k+i.val-r) k : ℚ)/(r.factorial : ℚ)) =
    (Nat.choose (k+i.val-s.val) k : ℚ)/(s.val.factorial : ℚ) +
      ∑ r ∈ Finset.Ico (s.val+1) (i.val+1),
        (Nat.choose (k+i.val-r) k : ℚ)/(r.factorial : ℚ)
  exact Finset.sum_eq_sum_Ico_succ_bot h
    (fun r => (Nat.choose (k+i.val-r) k : ℚ)/(r.factorial : ℚ))

private theorem suffix_empty (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2))
    (h : ¬s.val < i.val+1) : actualSuffixObservation k i s = 0 := by
  rw [suffix_eq_math]
  have hs : i.val+1 ≤ s.val := by omega
  simp only [SourceSuffix, Finset.Ico_eq_empty_of_le hs, Finset.sum_empty]

/-- Exact C345 source-binding root only; no denominator, magnitude or cost root. -/
theorem actualSuffix : ActualSuffixSpec := by
  unfold ActualSuffixSpec
  intro k i s
  refine ⟨suffix_eq_math k i s, suffix_zero k i, ?_⟩
  by_cases h : s.val < i.val+1
  · rw [dif_pos h]
    exact ⟨tail_eq_next k i s h, suffix_head_tail k i s h⟩
  · rw [dif_neg h]
    exact suffix_empty k i s h

#print axioms actualSuffix

end HermiteSourceSuffix
