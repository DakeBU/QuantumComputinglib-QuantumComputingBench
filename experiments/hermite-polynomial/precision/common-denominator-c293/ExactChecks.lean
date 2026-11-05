import CommonDenominatorProof

namespace C293ExactChecks

/-- All project definitions in the original closed signature are expanded. -/
def commonDenominatorExpandedCheck :
    ∀ (q : ℚ) (Q M : ℕ), 0 < Q → q.den ∣ Q → |q| ≤ (M : ℚ) →
      0 < Q ∧
        ((q.num * ((Q / q.den : ℕ) : ℤ) : ℤ) : ℚ) / (Q : ℚ) = q ∧
        (q.num * ((Q / q.den : ℕ) : ℤ)).natAbs ≤ M * Q ∧
        max 1 (max (Nat.size q.num.natAbs) (Nat.size q.den)) ≤
          max 1 (max (Nat.size (M * Q)) (Nat.size Q)) :=
  HermiteRationalHeight.commonDenominator

#check (HermiteRationalHeight.commonDenominator : HermiteRationalHeight.CommonDenominatorSpec)
#check commonDenominatorExpandedCheck
#print axioms HermiteRationalHeight.commonDenominator
#print axioms commonDenominatorExpandedCheck

end C293ExactChecks
