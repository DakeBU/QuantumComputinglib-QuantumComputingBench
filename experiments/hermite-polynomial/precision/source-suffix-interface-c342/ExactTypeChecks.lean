import SourceSuffixDefinitions

/-! Type-formation intentions only. These queries do not prove the three Props
and do not provide an axiom certificate or resolved binary selection. -/

open HermiteSourceSuffix

#check actualFactorials
#check actualSourceTerm
#check droppedTerms
#check actualSuffixObservation
#check actualTailObservation
#check SourceSuffix
#print ActualSuffixSpec
#print SuffixEnvelopeSpec
#print ReturnedCacheSpec

-- All public input binders are k/i/s; no F, cache, correctness or bound premise.
#check (show Prop from
  ∀ (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)),
    actualSuffixObservation k i s = SourceSuffix k i s ∧
    actualSuffixObservation k i ⟨0, by omega⟩ =
      (HermiteChargedSourceCache.sourceEntry k (actualFactorials k) i).value ∧
    (if h : s.val < i.val+1 then
      let next : Fin (i.val+2) := ⟨s.val+1, by omega⟩
      actualTailObservation k i s = actualSuffixObservation k i next ∧
      actualSuffixObservation k i s =
        (actualSourceTerm k i ⟨s.val, h⟩).value + actualTailObservation k i s
    else actualSuffixObservation k i s = 0))

#check (show Prop from
  ∀ (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)),
    let q := SourceSuffix k i s
    q.den ∣ k.factorial ∧ 0 ≤ q ∧
      q ≤ (((i.val+1-s.val)*2^(2*k) : ℕ) : ℚ))

#check (show Prop from
  ∀ (k : ℕ) (i : Fin (k+1)),
    let a := (HermiteChargedSourceCache.produceSourceCache k).value[i.val]
    a = actualSuffixObservation k i ⟨0, by omega⟩ ∧
      a.den ∣ k.factorial ∧ 0 ≤ a ∧
      a ≤ (((k+1)*2^(2*k) : ℕ) : ℚ))
