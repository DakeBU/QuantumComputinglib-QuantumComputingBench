import CachedSetupProof

/-! Author-authored exact sealed-type and fresh-output axiom consumer.
Not independent review, not run by the author. -/
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open HermiteCachedPiecewiseStored HermiteFiniteExpDegree

#check (rightSetup_values :
  ∀ (n : ℕ) (R delta : ℚ),
  let s := (rightSetup n R delta).value
  s.cutMinusOne = HermitePiecewiseUniform.strictCut (n+1) R (-1) ∧
  s.cutZero = HermitePiecewiseUniform.inclusiveCut (n+1) R 0 ∧
  s.cutMinusT = HermitePiecewiseUniform.inclusiveCut (n+1) R
    (-(HermiteFiniteExp.tailCutoff delta : ℚ)) ∧
  s.cutT = HermitePiecewiseUniform.strictCut (n+1) R
    (HermiteFiniteExp.tailCutoff delta : ℚ) ∧
  (∀ i : Fin (sourceDegree delta+1),
    s.tailCoeffs[i.val] = 1/(i.val.factorial : ℚ)) ∧
  s.clipped = HermitePiecewiseKernelProducer.clippedValue delta ∧
  s.midpoint = HermiteFiniteMiddleSource.expMidpoint delta)

#print axioms rightSetup_values
