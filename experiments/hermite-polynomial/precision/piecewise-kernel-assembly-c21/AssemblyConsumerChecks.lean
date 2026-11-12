import ActualAssembly

namespace HermitePiecewiseAssembly
open QuantumBlockEncoding TensorTrainCanonical HermitePiecewiseSourceBudget
open HermiteFiniteExpDegree

theorem actualChain_scalarEnvelope (k n : ℕ) (R delta : ℚ) :
    MatrixProductChain.storedScalars (actualChain k n R delta) ≤
      2*(n+1)*(18*(sourceDegree delta+1)+9*(2*k+1+1)+18)^2 :=
  MatrixProductChain.storedScalars_le _ _ (actualChain_maxBond k n R delta)

/-- The source allocation, exact amplitudes, and bond bound concern one identical object.
The scalar envelope is an address count, not a charged stored-data producer. -/
theorem full_actual_source_supplier (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (he : 0 < epsilon) (x : Word (n+1)) :
    let R := ExperimentalGlobalRadiusBudget.allocatedRadius k n L epsilon
    let delta := sourceDelta k n epsilon
    let C := actualChain k n R delta
    contract C x 0 0 = (piecewiseValue k delta (rationalGrid n R (wordIndex n x)) : ℝ) ∧
      maxBond C ≤ 18*(sourceDegree delta+1)+9*(2*k+1+1)+18 ∧
      MatrixProductChain.storedScalars C ≤
        2*(n+1)*(18*(sourceDegree delta+1)+9*(2*k+1+1)+18)^2 := by
  exact ⟨allocated_actualChain_contract k n L epsilon hL he x,
    actualChain_maxBond _ _ _ _, actualChain_scalarEnvelope _ _ _ _⟩

#print full_actual_source_supplier
#print axioms actualChain_scalarEnvelope
#print axioms full_actual_source_supplier
end HermitePiecewiseAssembly
