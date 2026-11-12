import CachedPrimitivesProof

/-! Author-authored exact-type/axiom consumer for the parent's fresh output.
Not independent review and not run by the author. -/
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open HermitePiecewiseAssembly HermiteCachedPiecewiseStored

#check (powQ_value :
  ∀ (x : ℚ) (m : ℕ), (powQ x m).value = x^m)

#check (powQ_cost :
  ∀ (x : ℚ) (m : ℕ) (op : Op),
  (powQ x m).cost op = m*tick .field op)

#check (cutoffQ_value :
  ∀ (delta : ℚ), (cutoffQ delta).value = HermiteFiniteExp.tailCutoff delta)

#check (gridStepRun_value :
  ∀ (width : ℕ) (R : ℚ),
  (gridStepRun width R).value = HermitePiecewiseUniform.gridStepQ width R)

#check (acceptRun_value :
  ∀ (width cut : ℕ) (a : Fin 3) (flip : Bool),
  (acceptRun width cut a flip).value =
    if flip then 1-HermitePiecewiseStored.acceptQ width cut a
    else HermitePiecewiseStored.acceptQ width cut a)

#check (acceptRun_total_le :
  ∀ (width cut : ℕ) (a : Fin 3) (flip : Bool),
  StoredRectangularGivens.total (acceptRun width cut a flip).cost ≤ 4)

#check (rightEntry_total_le :
  ∀ (k n : ℕ) (R delta : ℚ) (s : RightSetup n R delta)
    (middle : Vector ℚ (2*k+2)) (z : FullIndex k delta),
  StoredRectangularGivens.total (rightEntry k n R delta s middle z).cost ≤ 11)

#print axioms powQ_value
#print axioms powQ_cost
#print axioms cutoffQ_value
#print axioms gridStepRun_value
#print axioms acceptRun_value
#print axioms acceptRun_total_le
#print axioms rightEntry_total_le
