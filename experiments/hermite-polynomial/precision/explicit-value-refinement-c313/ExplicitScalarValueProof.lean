import ExplicitFiveBlockDefinitions

/-! C250-sealed scalar VALUE proof candidate. Author-uncompiled.
No cost root, source/counter change, or extra whole-producer premise. -/

namespace HermiteExplicitCachedStored

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredBinaryCoordinates
open HermitePiecewiseAssembly HermitePiecewiseUniform

private theorem c252_splitIndex_eq (m n : ℕ) (i : Fin (m+n)) :
    splitIndex m n i = finSumFinEquiv.symm i := by
  refine Fin.addCases (fun a => ?_) (fun b => ?_) i
  · rw [finSumFinEquiv_symm_apply_castAdd]
    unfold splitIndex
    simp only [Fin.val_castAdd, dif_pos a.isLt]
  · have hb : ¬ (Fin.natAdd m b).val < m := by
      change ¬ m+b.val < m
      omega
    rw [finSumFinEquiv_symm_apply_natAdd]
    unfold splitIndex
    rw [dif_neg hb]
    exact congrArg (Sum.inr : Fin n → Fin m ⊕ Fin n)
      (Fin.ext (by change m+b.val-m = b.val; omega))

private theorem c252_unpackComponent_eq (r : ℕ) (i : Fin (componentSize r)) :
    unpackComponent r i = (componentEquiv r).symm i := by
  rfl

private theorem c268_sumInverse {α β : Type} {m n : ℕ}
    (e : α ≃ Fin m) (f : β ≃ Fin n) (i : Fin (m+n)) :
    ((Equiv.sumCongr e f).trans finSumFinEquiv).symm i =
      match finSumFinEquiv.symm i with
      | .inl x => .inl (e.symm x)
      | .inr y => .inr (f.symm y) := by
  change Sum.map e.symm f.symm (finSumFinEquiv.symm i) = _
  cases finSumFinEquiv.symm i <;> rfl

theorem decode_value :
  ∀ (k : ℕ) (delta : ℚ) (a : Fin (assemblySize k delta)),
  (HermiteExplicitCachedStored.decode (HermiteFiniteExpDegree.sourceDegree delta)
    (2*k+1) a).run.value = (fullEquiv k delta).symm a := by
  intro k delta a
  let d := HermiteFiniteExpDegree.sourceDegree delta
  let m := 2*k+1
  let e4 : (ComponentIndex 0 ⊕ ComponentIndex d) ≃
      Fin (componentSize 0 + componentSize d) :=
    (Equiv.sumCongr (componentEquiv 0) (componentEquiv d)).trans finSumFinEquiv
  let e3 : (ComponentIndex m ⊕ (ComponentIndex 0 ⊕ ComponentIndex d)) ≃
      Fin (componentSize m + (componentSize 0 + componentSize d)) :=
    (Equiv.sumCongr (componentEquiv m) e4).trans finSumFinEquiv
  let e2 : (ComponentIndex d ⊕
      (ComponentIndex m ⊕ (ComponentIndex 0 ⊕ ComponentIndex d))) ≃
      Fin (componentSize d + (componentSize m +
        (componentSize 0 + componentSize d))) :=
    (Equiv.sumCongr (componentEquiv d) e3).trans finSumFinEquiv
  have hOuter := c268_sumInverse
    (m := componentSize 0)
    (n := componentSize d + (componentSize m +
      (componentSize 0 + componentSize d)))
    (componentEquiv 0) e2 a
  change (fullEquiv k delta).symm a = _ at hOuter
  dsimp only [decode]
  rw [c252_splitIndex_eq (componentSize 0)
    (componentSize d + (componentSize m +
      (componentSize 0 + componentSize d))) a]
  simp only [c252_splitIndex_eq, c252_unpackComponent_eq]
  rw [hOuter]
  cases h0 : (finSumFinEquiv.symm a :
      Fin (componentSize 0) ⊕
        Fin (componentSize d + (componentSize m +
          (componentSize 0 + componentSize d)))) with
  | inl x => rfl
  | inr rest =>
    have hSecond := c268_sumInverse
      (m := componentSize d)
      (n := componentSize m + (componentSize 0 + componentSize d))
      (componentEquiv d) e3 rest
    change e2.symm rest = _ at hSecond
    simp only []
    rw [hSecond]
    cases h1 : (finSumFinEquiv.symm rest :
        Fin (componentSize d) ⊕
          Fin (componentSize m + (componentSize 0 + componentSize d))) with
    | inl x => rfl
    | inr rest =>
      have hThird := c268_sumInverse
        (m := componentSize m)
        (n := componentSize 0 + componentSize d)
        (componentEquiv m) e4 rest
      change e3.symm rest = _ at hThird
      simp only []
      rw [hThird]
      cases h2 : (finSumFinEquiv.symm rest :
          Fin (componentSize m) ⊕ Fin (componentSize 0 + componentSize d)) with
      | inl x => rfl
      | inr rest =>
        have hFourth := c268_sumInverse
          (m := componentSize 0) (n := componentSize d)
          (componentEquiv 0) (componentEquiv d) rest
        change e4.symm rest = _ at hFourth
        simp only []
        rw [hFourth]
        cases h3 : (finSumFinEquiv.symm rest :
            Fin (componentSize 0) ⊕ Fin (componentSize d)) with
        | inl x => rfl
        | inr x => rfl

theorem comparisonQ_value :
  ∀ (cut q : ℕ) (bit : Fin 2) (a b : Fin 3),
  (comparisonQ cut q bit a b).run.value =
    HermitePiecewiseUniform.comparisonEntry cut q bit a b := by
  intro cut q bit a b
  by_cases hlo : bit.val < (cut / 2^q) % 2 <;>
    by_cases hhi : (cut / 2^q) % 2 < bit.val <;>
    simp [comparisonQ, comparisonEntry, finish, charge, hlo, hhi]

private theorem c252_bitValue (bit : Fin 2) :
    (if bit = 1 then (1 : ℚ) else 0) = (bit.val : ℚ) := by
  have hbit : bit.val = 0 ∨ bit.val = 1 := by
    have hb := bit.isLt
    omega
  rcases hbit with hzero | hone
  · have hb : bit = 0 := Fin.ext hzero
    simp [hb]
  · have hb : bit = 1 := Fin.ext hone
    simp [hb]

theorem translationQ_actual_factorials :
  ∀ (L r q : ℕ) (hr : r ≤ L) (step : ℚ) (bit : Fin 2)
    (i j : Fin (r+1)),
  (translationQ L r q (HermiteChargedSourceCache.factorials L).value.values
    hr step bit i j).value =
    HermitePiecewiseUniform.translationCoreQ r (step*2^q*(bit.val : ℚ)) i j := by
  intro L r q hr step bit i j
  by_cases h : i.val ≤ j.val
  · simp only [translationQ, dif_pos h, bind, Run.bind,
      HermiteChargedSourceCache.chooseFrom_value _
        (HermiteChargedSourceCache.factorials_value L),
      HermiteCachedPiecewiseStored.powQ_value,
      HermiteChargedSourceCache.qMul, charge, c252_bitValue, translationCoreQ]
  · have hz : j.val.choose i.val = 0 :=
      Nat.choose_eq_zero_of_lt (lt_of_not_ge h)
    simp [translationQ, h, translationCoreQ, hz, pure, Run.pure]

#check c252_splitIndex_eq
#print axioms c252_splitIndex_eq
#check c252_unpackComponent_eq
#print axioms c252_unpackComponent_eq
#check c252_bitValue
#print axioms c252_bitValue
#check c268_sumInverse
#print axioms c268_sumInverse
#check HermiteExplicitCachedStored.decode_value
#print axioms HermiteExplicitCachedStored.decode_value
#check HermiteExplicitCachedStored.comparisonQ_value
#print axioms HermiteExplicitCachedStored.comparisonQ_value
#check HermiteExplicitCachedStored.translationQ_actual_factorials
#print axioms HermiteExplicitCachedStored.translationQ_actual_factorials

end HermiteExplicitCachedStored
