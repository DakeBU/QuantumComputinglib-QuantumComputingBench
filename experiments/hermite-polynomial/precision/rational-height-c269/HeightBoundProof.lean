import Definitions
import Mathlib.Order.MinMax

namespace HermiteRationalHeight

/-- Canonical rational height is exactly a strict power-of-two field bound.
No positivity or nonzero premise is imposed on the rational or the bit cap. -/
theorem heightBound : HeightBoundSpec := by
  unfold HeightBoundSpec
  intro q B
  simp only [height, integerBits, max_le_iff, Nat.size_le]

end HermiteRationalHeight
