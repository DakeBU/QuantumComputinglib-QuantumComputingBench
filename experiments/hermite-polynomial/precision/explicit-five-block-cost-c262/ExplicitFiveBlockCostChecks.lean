import ExplicitFiveBlockCostProof

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open HermitePiecewiseAssembly HermitePiecewiseStored HermiteExplicitCachedStored

-- Exact cost/counter projection of the C250 same-result conclusion.
example :
    ∀ (k n : ℕ) (R delta : ℚ),
    let result := produceExplicitStored k n R delta
    StoredRectangularGivens.total result.run.cost ≤ frontierBudget k n delta ∧
    result.quotientCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta ∧
    result.remainderCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta :=
  produceExplicitStored_cost_counters

#check HermiteExplicitCachedStored.produceExplicitStored_cost_counters
#print axioms HermiteExplicitCachedStored.produceExplicitStored_cost_counters
