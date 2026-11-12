import SameRunProof

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain
open HermitePiecewiseAssembly HermiteExplicitCachedStored

namespace C332ExactChecks

theorem sameRunExactCheck :
  ∀ (k n : ℕ) (R delta : ℚ),
  let result := produceExplicitStored k n R delta
  denoteChain result.run.value = actualChain k n R delta ∧
  StoredRectangularGivens.total result.run.cost ≤ frontierBudget k n delta ∧
  result.quotientCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta ∧
  result.remainderCalls ≤ 14*(n+1)*(assemblySize k delta)^2+4*assemblySize k delta :=
  HermiteExplicitCachedStored.produceExplicitStored_same_run

#check HermiteExplicitCachedStored.produceExplicitStored_same_run
#check sameRunExactCheck
#print axioms HermiteExplicitCachedStored.produceExplicitStored_same_run
#print axioms sameRunExactCheck
#print axioms HermiteExplicitCachedStored.produceExplicitStored_refines
#print axioms HermiteExplicitCachedStored.produceExplicitStored_cost_counters

end C332ExactChecks
