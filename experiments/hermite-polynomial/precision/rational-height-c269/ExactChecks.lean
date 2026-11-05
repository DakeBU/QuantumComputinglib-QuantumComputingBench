import HeightBoundProof

namespace C282ExactChecks

/-- Closed expanded signature assignment against the selected author output. -/
def heightBoundExpandedCheck :
    ∀ (q : ℚ) (B : ℕ),
      max 1 (max (Nat.size q.num.natAbs) (Nat.size q.den)) ≤ B ↔
        1 ≤ B ∧ q.num.natAbs < 2^B ∧ q.den < 2^B :=
  HermiteRationalHeight.heightBound

#check (HermiteRationalHeight.heightBound : HermiteRationalHeight.HeightBoundSpec)
#check heightBoundExpandedCheck
#print axioms HermiteRationalHeight.heightBound
#print axioms heightBoundExpandedCheck

end C282ExactChecks
