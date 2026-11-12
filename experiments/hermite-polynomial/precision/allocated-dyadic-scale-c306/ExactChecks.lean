import AllocatedDyadicScaleProof

namespace C306ExactChecks

def scaleDyadicExpandedCheck :
    ∀ (k n : ℕ) (epsilon : ℚ), 0 < epsilon →
      n + 1 + 2*k + HermiteFiniteExp.tailCutoff
        (epsilon / (4 * ((k+1 : ℕ) : ℚ)^2)) ≤
      n + 1 + 4*k + 2 + HermiteFiniteExp.tailCutoff epsilon :=
  HermiteAllocatedPolynomialCost.scaleDyadicBound

#check (HermiteAllocatedPolynomialCost.scaleDyadicBound :
  HermiteAllocatedPolynomialCost.intendedScaleDyadicBound)
#check scaleDyadicExpandedCheck
#print axioms HermiteAllocatedPolynomialCost.scaleDyadicBound
#print axioms scaleDyadicExpandedCheck

end C306ExactChecks
