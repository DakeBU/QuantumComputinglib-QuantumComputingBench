import ExplicitFiveBlockDefinitions

/-! C275 interface probe only. No failed scalar import; no scientific root. -/

namespace HermiteExplicitCachedStored.C275Probe

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredBinaryCoordinates
open HermitePiecewiseAssembly HermitePiecewiseUniform

private theorem c268_sumInverse {α β : Type} {m n : ℕ}
    (e : α ≃ Fin m) (f : β ≃ Fin n) (i : Fin (m+n)) :
    ((Equiv.sumCongr e f).trans finSumFinEquiv).symm i =
      match finSumFinEquiv.symm i with
      | .inl x => .inl (e.symm x)
      | .inr y => .inr (f.symm y) := by
  change Sum.map e.symm f.symm (finSumFinEquiv.symm i) = _
  cases finSumFinEquiv.symm i <;> rfl

/-- Isolate the actual first inr binder/constructor obstruction.
The tail is left as its exact original equivalence, not a callback premise. -/
theorem firstInr_constructor_iota_hSecond (k : ℕ) (delta : ℚ)
    (rest : Fin (componentSize (HermiteFiniteExpDegree.sourceDegree delta) + (componentSize (2*k+1) +
        (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta))))) :
    ((match (Sum.inr rest : Fin (componentSize 0) ⊕ Fin (componentSize (HermiteFiniteExpDegree.sourceDegree delta) + (componentSize (2*k+1) +
        (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta))))) with
      | .inl x => .inl ((componentEquiv 0).symm x)
      | .inr y => .inr (match finSumFinEquiv.symm y with
        | .inl x => .inl ((componentEquiv (HermiteFiniteExpDegree.sourceDegree delta)).symm x)
        | .inr z => .inr (((Equiv.sumCongr (componentEquiv (2*k+1)) ((Equiv.sumCongr (componentEquiv 0) (componentEquiv (HermiteFiniteExpDegree.sourceDegree delta))).trans finSumFinEquiv)).trans finSumFinEquiv).symm z))) : FullIndex k delta) =
    ((match (Sum.inr rest : Fin (componentSize 0) ⊕ Fin (componentSize (HermiteFiniteExpDegree.sourceDegree delta) + (componentSize (2*k+1) +
        (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta))))) with
      | .inl x => .inl ((componentEquiv 0).symm x)
      | .inr y => .inr (((Equiv.sumCongr (componentEquiv (HermiteFiniteExpDegree.sourceDegree delta)) ((Equiv.sumCongr (componentEquiv (2*k+1)) ((Equiv.sumCongr (componentEquiv 0) (componentEquiv (HermiteFiniteExpDegree.sourceDegree delta))).trans finSumFinEquiv)).trans finSumFinEquiv)).trans finSumFinEquiv).symm y)) : FullIndex k delta) := by
  let e4 : (ComponentIndex 0 ⊕ ComponentIndex (HermiteFiniteExpDegree.sourceDegree delta)) ≃
      Fin (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta)) :=
    (Equiv.sumCongr (componentEquiv 0) (componentEquiv (HermiteFiniteExpDegree.sourceDegree delta))).trans finSumFinEquiv
  let e3 : (ComponentIndex (2*k+1) ⊕
      (ComponentIndex 0 ⊕ ComponentIndex (HermiteFiniteExpDegree.sourceDegree delta))) ≃
      Fin (componentSize (2*k+1) + (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta))) :=
    (Equiv.sumCongr (componentEquiv (2*k+1)) e4).trans finSumFinEquiv
  let e2 : (ComponentIndex (HermiteFiniteExpDegree.sourceDegree delta) ⊕
      (ComponentIndex (2*k+1) ⊕
        (ComponentIndex 0 ⊕ ComponentIndex (HermiteFiniteExpDegree.sourceDegree delta)))) ≃
      Fin (componentSize (HermiteFiniteExpDegree.sourceDegree delta) + (componentSize (2*k+1) +
        (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta)))) :=
    (Equiv.sumCongr (componentEquiv (HermiteFiniteExpDegree.sourceDegree delta)) e3).trans finSumFinEquiv
  change
    ((match (Sum.inr rest : Fin (componentSize 0) ⊕ Fin (componentSize (HermiteFiniteExpDegree.sourceDegree delta) + (componentSize (2*k+1) +
        (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta))))) with
      | .inl x => .inl ((componentEquiv 0).symm x)
      | .inr y => .inr (match finSumFinEquiv.symm y with
        | .inl x => .inl ((componentEquiv (HermiteFiniteExpDegree.sourceDegree delta)).symm x)
        | .inr z => .inr ((e3).symm z))) : FullIndex k delta) =
    ((match (Sum.inr rest : Fin (componentSize 0) ⊕ Fin (componentSize (HermiteFiniteExpDegree.sourceDegree delta) + (componentSize (2*k+1) +
        (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta))))) with
      | .inl x => .inl ((componentEquiv 0).symm x)
      | .inr y => .inr ((e2).symm y)) : FullIndex k delta)
  have hSecond := c268_sumInverse
    (m := componentSize (HermiteFiniteExpDegree.sourceDegree delta))
    (n := componentSize (2*k+1) + (componentSize 0 + componentSize (HermiteFiniteExpDegree.sourceDegree delta)))
    (componentEquiv (HermiteFiniteExpDegree.sourceDegree delta)) e3 rest
  change e2.symm rest = _ at hSecond
  change
    (Sum.inr (match finSumFinEquiv.symm rest with
      | .inl x => .inl ((componentEquiv
          (HermiteFiniteExpDegree.sourceDegree delta)).symm x)
      | .inr z => .inr (e3.symm z)) : FullIndex k delta) =
      Sum.inr (e2.symm rest)
  rw [hSecond]
  rfl

#check c268_sumInverse
#print axioms c268_sumInverse
#check HermiteExplicitCachedStored.C275Probe.firstInr_constructor_iota_hSecond
#print axioms HermiteExplicitCachedStored.C275Probe.firstInr_constructor_iota_hSecond

end HermiteExplicitCachedStored.C275Probe
