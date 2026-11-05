import SourceSuffixBindingProof

namespace HermiteSourceSuffix

theorem actualSuffix_expanded :
    ∀ (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)),
      actualSuffixObservation k i s = SourceSuffix k i s ∧
      actualSuffixObservation k i ⟨0, by omega⟩ =
        (HermiteChargedSourceCache.sourceEntry k (actualFactorials k) i).value ∧
      (if h : s.val < i.val+1 then
        let next : Fin (i.val+2) := ⟨s.val+1, by omega⟩
        actualTailObservation k i s = actualSuffixObservation k i next ∧
        actualSuffixObservation k i s =
          (actualSourceTerm k i ⟨s.val, h⟩).value + actualTailObservation k i s
      else actualSuffixObservation k i s = 0) := actualSuffix

#check actualSuffix
#check actualSuffix_expanded
#print axioms actualSuffix
#print axioms actualSuffix_expanded

end HermiteSourceSuffix
