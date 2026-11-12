import SourceSuffixEnvelopeProof

/-! Exact expanded consumer of the C345 SECOND root.
This is a consumer candidate, not evidence that any compiler has run. -/

namespace C347ExactChecks

open scoped BigOperators

theorem suffixEnvelopeExpandedCheck :
    ∀ (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)),
      let q : ℚ := ∑ r ∈ Finset.Ico s.val (i.val+1),
        (Nat.choose (k+i.val-r) k : ℚ) / (r.factorial : ℚ)
      q.den ∣ k.factorial ∧ 0 ≤ q ∧
        q ≤ (((i.val+1-s.val)*2^(2*k) : ℕ) : ℚ) :=
  HermiteSourceSuffix.suffixEnvelope

#check (HermiteSourceSuffix.suffixEnvelope : HermiteSourceSuffix.SuffixEnvelopeSpec)
#check suffixEnvelopeExpandedCheck
#print HermiteSourceSuffix.SourceSuffix
#print HermiteSourceSuffix.SuffixEnvelopeSpec
#print axioms HermiteSourceSuffix.suffixEnvelope
#print axioms suffixEnvelopeExpandedCheck

end C347ExactChecks
