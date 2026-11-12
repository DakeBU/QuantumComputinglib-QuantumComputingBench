import AllocatedPolynomialLedgerProof

/-! Exact C295 expanded own-consumer candidate. Author-uncompiled.
No scaleDyadicBound or VALUE theorem is assumed or consumed here. -/

open QuantumBlockEncoding
open HermiteAllocatedPolynomialCost

#check (HermiteAllocatedPolynomialCost.allocatedBudgetEnvelope :
  HermiteAllocatedPolynomialCost.intendedAllocatedBudgetEnvelope)
#check (HermiteAllocatedPolynomialCost.allocatedBudgetEnvelope :
  ∀ (k n : ℕ) (epsilon : ℚ), 0 < epsilon →
    let delta := HermitePiecewiseSourceBudget.sourceDelta k n epsilon
    HermiteExplicitCachedStored.frontierBudget k n delta ≤
        5000000*(HermiteAllocatedPolynomialCost.operationScale k n epsilon)^7 ∧
      14*(n+1)*(HermitePiecewiseAssembly.assemblySize k delta)^2+
          4*HermitePiecewiseAssembly.assemblySize k delta ≤
        500000*(HermiteAllocatedPolynomialCost.operationScale k n epsilon)^5)
#print axioms HermiteAllocatedPolynomialCost.allocatedBudgetEnvelope

#check (HermiteAllocatedPolynomialCost.allocatedSameRunPartialLedger :
  HermiteAllocatedPolynomialCost.intendedAllocatedSameRunPartialLedger)
#check (HermiteAllocatedPolynomialCost.allocatedSameRunPartialLedger :
  ∀ (k n : ℕ) (R epsilon : ℚ), 0 < epsilon →
    let result := HermiteExplicitCachedStored.produceExplicitStored k n R
      (HermitePiecewiseSourceBudget.sourceDelta k n epsilon)
    StoredRectangularGivens.total result.run.cost ≤
        5000000*(HermiteAllocatedPolynomialCost.operationScale k n epsilon)^7 ∧
      result.quotientCalls ≤
        500000*(HermiteAllocatedPolynomialCost.operationScale k n epsilon)^5 ∧
      result.remainderCalls ≤
        500000*(HermiteAllocatedPolynomialCost.operationScale k n epsilon)^5)
#print axioms HermiteAllocatedPolynomialCost.allocatedSameRunPartialLedger

#check HermiteAllocatedDegreeBudget.allocated_tailCutoff_le
#print axioms HermiteAllocatedDegreeBudget.allocated_tailCutoff_le
#check HermiteAllocatedDegreeBudget.allocated_sourceDegree_le
#print axioms HermiteAllocatedDegreeBudget.allocated_sourceDegree_le
#check HermiteExplicitCachedStored.produceExplicitStored_cost_counters
#print axioms HermiteExplicitCachedStored.produceExplicitStored_cost_counters
#print HermiteAllocatedPolynomialCost.operationScale
#print HermiteAllocatedPolynomialCost.intendedAllocatedBudgetEnvelope
#print HermiteAllocatedPolynomialCost.intendedAllocatedSameRunPartialLedger
#print HermiteExplicitCachedStored.frontierBudget
#print HermitePiecewiseSourceBudget.sourceDelta
#print HermiteFiniteExpDegree.sourceDegree
#print HermiteFiniteExp.tailCutoff
