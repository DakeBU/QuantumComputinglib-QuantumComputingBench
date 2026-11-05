import PrimitiveWidthProof

namespace C310ExactChecks

/-- Closed original signature with all project function bodies expanded. -/
def primitiveWidthExpandedCheck :
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
      let B : ℕ :=
        max 1 (max (Nat.size x.num.natAbs) (Nat.size x.den)) +
        max 1 (max (Nat.size y.num.natAbs) (Nat.size y.den)) +
          (match op with | .add => 1 | .sub => 1 | .mul => 0 | .div => 0)
      let zs : List ℤ :=
        match op with
        | .add => [x.num * (y.den : ℤ), y.num * (x.den : ℤ), w.numerator, (w.denominator : ℤ)]
        | .sub => [x.num * (y.den : ℤ), y.num * (x.den : ℤ), w.numerator, (w.denominator : ℤ)]
        | .mul => [w.numerator, (w.denominator : ℤ)]
        | .div => [x.num * (y.den : ℤ), (x.den : ℤ) * y.num, w.numerator, (w.denominator : ℤ)]
      max 1 (max (Nat.size w.numerator.natAbs) (Nat.size w.denominator)) ≤ B ∧
        ∀ z ∈ zs, Nat.size z.natAbs ≤ B :=
  HermiteRationalHeight.primitiveWidth

#check (HermiteRationalHeight.primitiveWidth : HermiteRationalHeight.PrimitiveWidthSpec)
#check primitiveWidthExpandedCheck
#print axioms HermiteRationalHeight.primitiveWidth
#print axioms primitiveWidthExpandedCheck

end C310ExactChecks
