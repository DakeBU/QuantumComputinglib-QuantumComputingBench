import Mathlib.Algebra.Order.Field.Rat
import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Nat.Size

/-! C269 definitions and four UNPROVED proposition definitions only.
These are mathematical witnesses for canonical Rat arguments, not a new
numerical producer, native-temporary trace, cost model or Sites relation. -/

namespace HermiteRationalHeight

/-- Magnitude bits only; an encoded integer sign is a separate bit. -/
def integerBits (z : ℤ) : ℕ := Nat.size z.natAbs

/-- C257 height, using the actual canonical Rat fields. In particular h(0)=1. -/
def height (q : ℚ) : ℕ := max 1 (max (integerBits q.num) (Nat.size q.den))

/-- Unreduced mathematical pair. Positivity is a conclusion of the targets,
not an assumed field; commonWitness at Q=0 is not claimed a representation. -/
structure Witness where
  numerator : ℤ
  denominator : ℕ

def witnessValue (w : Witness) : ℚ := (w.numerator : ℚ) / (w.denominator : ℚ)

def witnessWidth (w : Witness) : ℕ :=
  max 1 (max (integerBits w.numerator) (Nat.size w.denominator))

/-- Supplied common denominator, not a cache actually built by a producer. -/
def commonWitness (q : ℚ) (Q : ℕ) : Witness :=
  ⟨q.num * ((Q / q.den : ℕ) : ℤ), Q⟩

inductive Operation where
  | add | sub | mul | div

/-- One canonical Rat operation, specification only; no Run is introduced. -/
def operationValue (op : Operation) (x y : ℚ) : ℚ :=
  match op with
  | .add => x+y
  | .sub => x-y
  | .mul => x*y
  | .div => x/y

/-- Division normalizes only the denominator sign, not a gcd. Its zero-divisor
branch explicitly witnesses Rat's total division result by the pair (0,1). -/
def rawWitness (op : Operation) (x y : ℚ) : Witness :=
  match op with
  | .add => ⟨x.num*(y.den : ℤ)+y.num*(x.den : ℤ), x.den*y.den⟩
  | .sub => ⟨x.num*(y.den : ℤ)-y.num*(x.den : ℤ), x.den*y.den⟩
  | .mul => ⟨x.num*y.num, x.den*y.den⟩
  | .div =>
      if y.num = 0 then ⟨0,1⟩ else
        ⟨if y.num < 0 then -(x.num*(y.den : ℤ)) else x.num*(y.den : ℤ),
          x.den*y.num.natAbs⟩

/-- Cross-products are retained even if the canonical result cancels to zero.
The division list also retains its signed raw denominator, including zero;
that integer is not asserted to be a valid positive-denominator witness. -/
def rawIntegers (op : Operation) (x y : ℚ) : List ℤ :=
  let w := rawWitness op x y
  match op with
  | .add => [x.num*(y.den : ℤ), y.num*(x.den : ℤ), w.numerator, (w.denominator : ℤ)]
  | .sub => [x.num*(y.den : ℤ), y.num*(x.den : ℤ), w.numerator, (w.denominator : ℤ)]
  | .mul => [w.numerator, (w.denominator : ℤ)]
  | .div => [x.num*(y.den : ℤ), (x.den : ℤ)*y.num, w.numerator, (w.denominator : ℤ)]

def operationWidth (op : Operation) (x y : ℚ) : ℕ :=
  height x + height y + (match op with
    | .add => 1
    | .sub => 1
    | .mul => 0
    | .div => 0)

/-- Target 1: non-strict bit bound is a STRICT power-of-two bound. -/
def HeightBoundSpec : Prop :=
  ∀ (q : ℚ) (B : ℕ), height q ≤ B ↔
    1 ≤ B ∧ q.num.natAbs < 2^B ∧ q.den < 2^B

/-- Target 2: a reusable common-denominator/magnitude bridge for signed sums.
Q,M are proof witnesses; these premises are not added to any producer root. -/
def CommonDenominatorSpec : Prop :=
  ∀ (q : ℚ) (Q M : ℕ), 0 < Q → q.den ∣ Q → |q| ≤ (M : ℚ) →
    let w := commonWitness q Q
    0 < w.denominator ∧ witnessValue w = q ∧ w.numerator.natAbs ≤ M*Q ∧
      height q ≤ max 1 (max (Nat.size (M*Q)) (Nat.size Q))

/-- Target 3: actual canonical result versus its unreduced mathematical pair.
No nonzero-divisor hypothesis: the zero branch is part of the conclusion. -/
def PrimitiveRepresentationSpec : Prop :=
  ∀ (op : Operation) (x y : ℚ),
    let w := rawWitness op x y
    let result := operationValue op x y
    0 < w.denominator ∧ witnessValue w = result ∧
      result.den ∣ w.denominator ∧ result.num.natAbs ≤ w.numerator.natAbs ∧
      height result ≤ witnessWidth w

/-- Target 4: one-operation widths, not normalization scratch or CPU time. -/
def PrimitiveWidthSpec : Prop :=
  ∀ (op : Operation) (x y : ℚ),
    witnessWidth (rawWitness op x y) ≤ operationWidth op x y ∧
      ∀ z ∈ rawIntegers op x y, integerBits z ≤ operationWidth op x y

end HermiteRationalHeight
