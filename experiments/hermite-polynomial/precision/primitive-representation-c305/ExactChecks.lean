import PrimitiveRepresentationProof

namespace C298ExactChecks

/-- The closed sealed signature with every project function body expanded. -/
def primitiveRepresentationExpandedCheck :
    ∀ (op : HermiteRationalHeight.Operation) (x y : ℚ),
      let w : HermiteRationalHeight.Witness :=
        match op with
        | .add => ⟨x.num * (y.den : ℤ) + y.num * (x.den : ℤ), x.den * y.den⟩
        | .sub => ⟨x.num * (y.den : ℤ) - y.num * (x.den : ℤ), x.den * y.den⟩
        | .mul => ⟨x.num * y.num, x.den * y.den⟩
        | .div =>
            if y.num = 0 then ⟨0, 1⟩ else
              ⟨if y.num < 0 then -(x.num * (y.den : ℤ)) else x.num * (y.den : ℤ),
                x.den * y.num.natAbs⟩
      let result : ℚ :=
        match op with
        | .add => x + y
        | .sub => x - y
        | .mul => x * y
        | .div => x / y
      0 < w.denominator ∧ (w.numerator : ℚ) / (w.denominator : ℚ) = result ∧
        result.den ∣ w.denominator ∧ result.num.natAbs ≤ w.numerator.natAbs ∧
        max 1 (max (Nat.size result.num.natAbs) (Nat.size result.den)) ≤
          max 1 (max (Nat.size w.numerator.natAbs) (Nat.size w.denominator)) :=
  HermiteRationalHeight.primitiveRepresentation

#check (HermiteRationalHeight.primitiveRepresentation : HermiteRationalHeight.PrimitiveRepresentationSpec)
#check primitiveRepresentationExpandedCheck
#print axioms HermiteRationalHeight.primitiveRepresentation
#print axioms primitiveRepresentationExpandedCheck

end C298ExactChecks
