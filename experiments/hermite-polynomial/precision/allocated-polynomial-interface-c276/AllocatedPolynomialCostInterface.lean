import AllocatedDegreeBudget
import ExplicitFiveBlockCostProof

/-!
C276 AUTHOR-UNTYPED proposition formations only. No theorem is proved here.
The actual allocated tolerance and producer are unchanged. These are bounds
on the partial eight-counter operation ledger and selected index-call counts,
NOT native-bit/Rat/GCD/evaluator/quantum-resource or scientific ROOT bounds.
Parent type formation and a real pre-proof Statement Seal must precede proof.
-/

namespace HermiteAllocatedPolynomialCost

/-- Physical register count is n+1; allocation is the literal C147 allocation. -/
def operationScale (k n : ℕ) (epsilon : ℚ) : ℕ :=
  n + 1 + 2*k + HermiteFiniteExp.tailCutoff
    (epsilon / (4 * ((k+1 : ℕ) : ℚ)^2))

/-- Positive-part dyadic precision, including arbitrarily large epsilon. -/
def intendedScaleDyadicBound : Prop :=
  ∀ (k n : ℕ) (epsilon : ℚ), 0 < epsilon →
    operationScale k n epsilon ≤
      n + 1 + 4*k + 2 + HermiteFiniteExp.tailCutoff epsilon

/-- Algebraic envelope for the actual allocation, not a producer-cost premise. -/
def intendedAllocatedBudgetEnvelope : Prop :=
  ∀ (k n : ℕ) (epsilon : ℚ), 0 < epsilon →
    let delta := HermitePiecewiseSourceBudget.sourceDelta k n epsilon
    HermiteExplicitCachedStored.frontierBudget k n delta ≤
        5000000 * (operationScale k n epsilon)^7 ∧
      14*(n+1)*(HermitePiecewiseAssembly.assemblySize k delta)^2 +
          4*HermitePiecewiseAssembly.assemblySize k delta ≤
        500000 * (operationScale k n epsilon)^5

/-- Same actual returned run; no value, normalization or extra cost assumption. -/
def intendedAllocatedSameRunPartialLedger : Prop :=
  ∀ (k n : ℕ) (R epsilon : ℚ), 0 < epsilon →
    let result := HermiteExplicitCachedStored.produceExplicitStored k n R
      (HermitePiecewiseSourceBudget.sourceDelta k n epsilon)
    QuantumBlockEncoding.StoredRectangularGivens.total result.run.cost ≤
        5000000 * (operationScale k n epsilon)^7 ∧
      result.quotientCalls ≤ 500000 * (operationScale k n epsilon)^5 ∧
      result.remainderCalls ≤ 500000 * (operationScale k n epsilon)^5

end HermiteAllocatedPolynomialCost
