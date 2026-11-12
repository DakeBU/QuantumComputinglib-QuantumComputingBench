import CachedMiddleValueProof

/-! Author exact sealed-type/axiom consumer for a fresh own-output parent gate.
Not independent review; not run by the author. -/
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open HermiteCachedPiecewiseStored

#check (middleFromCache_entry :
  ∀ (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)) (j : Fin (2*k+2)),
  (middleFromCache k e a).value[j.val] = middleExpr k e a j)

#check (actual_cache_middle :
  ∀ (k : ℕ) (delta : ℚ) (j : Fin (2*k+2)),
  (middleFromCache k (HermiteFiniteMiddleSource.expMidpoint delta)
    (HermiteChargedSourceCache.produceSourceCache k).value).value[j.val] =
    HermitePiecewiseAssembly.middleCoeffQ k delta j.val)

#print axioms middleFromCache_entry
#print axioms actual_cache_middle
