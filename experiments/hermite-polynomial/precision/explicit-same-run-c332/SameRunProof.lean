import ExplicitChainValueProof
import ExplicitFiveBlockCostProof

namespace HermiteExplicitCachedStored

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain
open HermitePiecewiseAssembly

theorem produceExplicitStored_same_run :
  ∀ (k n : ℕ) (R delta : ℚ),
  let result := produceExplicitStored k n R delta
  denoteChain result.run.value = actualChain k n R delta ∧
  StoredRectangularGivens.total result.run.cost ≤ frontierBudget k n delta ∧
  result.quotientCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta ∧
  result.remainderCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta := by
  intro k n R delta
  exact And.intro (produceExplicitStored_refines k n R delta)
    (produceExplicitStored_cost_counters k n R delta)

#check produceExplicitStored_same_run
#print axioms produceExplicitStored_same_run

end HermiteExplicitCachedStored
