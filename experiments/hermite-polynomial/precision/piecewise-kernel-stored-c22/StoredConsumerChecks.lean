import AccountedTraffic

namespace HermitePiecewiseStored
open QuantumBlockEncoding TensorTrainCanonical StoredTensorTrain StoredRectangularGivens
open HermitePiecewiseAssembly HermitePiecewiseSourceBudget HermiteFiniteExpDegree

theorem allocated_stored_source (k n : ℕ) (L epsilon : ℚ)
    (hL : 0<L) (he : 0<epsilon) (x : Word (n+1)) :
    let R := ExperimentalGlobalRadiusBudget.allocatedRadius k n L epsilon
    let delta := sourceDelta k n epsilon
    let result := produceStored k n R delta
    denoteChain result.value = actualChain k n R delta ∧
      contract (denoteChain result.value) x 0 0 =
        (piecewiseValue k delta (rationalGrid n R (wordIndex n x)) : ℝ) ∧
      maxBond (denoteChain result.value) ≤ 18*(sourceDegree delta+1)+9*(2*k+1+1)+18 ∧
      MatrixProductChain.storedScalars (denoteChain result.value) ≤
        2*(n+1)*(18*(sourceDegree delta+1)+9*(2*k+1+1)+18)^2 := by
  exact ⟨produceStored_refines _ _ _ _,
    produceStored_source _ _ _ _
      (ExperimentalGlobalRadiusBudget.allocatedRadius_positive _ _ _ _ hL he) x,
    produceStored_maxBond _ _ _ _, produceStored_scalars _ _ _ _⟩

#print allocated_stored_source
#print axioms allocated_stored_source
end HermitePiecewiseStored
