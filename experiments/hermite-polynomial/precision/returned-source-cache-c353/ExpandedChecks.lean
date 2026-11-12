import ReturnedSourceCacheProof

/-! Exact closed C345 THIRD-root consumer. ReturnedCacheSpec and the
observation wrapper are expanded; the original numerical producer is retained. -/

namespace C353ExpandedChecks

theorem returnedCacheExpanded :
    ∀ (k : ℕ) (i : Fin (k+1)),
      let a : ℚ := (HermiteChargedSourceCache.produceSourceCache k).value[i.val]
      a = (HermiteChargedSourceCache.sumEntries
        (HermiteSourceSuffix.droppedTerms k i ⟨0, by omega⟩)).value ∧
      a.den ∣ k.factorial ∧ 0 ≤ a ∧
        a ≤ (((k+1)*2^(2*k) : ℕ) : ℚ) :=
  HermiteSourceSuffix.returnedCache

#check (HermiteSourceSuffix.actualSuffix : HermiteSourceSuffix.ActualSuffixSpec)
#check (HermiteSourceSuffix.suffixEnvelope : HermiteSourceSuffix.SuffixEnvelopeSpec)
#check (HermiteSourceSuffix.returnedCache : HermiteSourceSuffix.ReturnedCacheSpec)
#check returnedCacheExpanded
#print HermiteChargedSourceCache.produceSourceCache
#print HermiteChargedSourceCache.sources
#print HermiteSourceSuffix.actualFactorials
#print HermiteSourceSuffix.actualSourceTerm
#print HermiteSourceSuffix.droppedTerms
#print HermiteSourceSuffix.actualSuffixObservation
#print HermiteSourceSuffix.SourceSuffix
#print HermiteSourceSuffix.ReturnedCacheSpec
#print axioms HermiteSourceSuffix.actualSuffix
#print axioms HermiteSourceSuffix.suffixEnvelope
#print axioms HermiteSourceSuffix.returnedCache
#print axioms returnedCacheExpanded

end C353ExpandedChecks
