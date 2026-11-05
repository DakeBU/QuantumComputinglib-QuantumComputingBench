import PiecewiseSourceBudget

namespace HermitePiecewiseKernelProducer
open HermitePiecewiseSourceBudget HermiteFiniteExp HermiteFiniteExpDegree
open HermiteFiniteMiddleSource

def indicator (P : Prop) [Decidable P] : ℚ := if P then 1 else 0

def clippedValue (delta : ℚ) : ℚ := tailRadius (tailCutoff delta)/2
def activeValue (delta p : ℚ) : ℚ := poly p (sourceDegree delta)

theorem negativeMidpoint_split (q delta : ℚ) :
    negativeMidpoint q delta =
      if q ≤ -(tailCutoff delta : ℚ) then clippedValue delta else activeValue delta q := by
  unfold negativeMidpoint bounds clippedValue activeValue
  split_ifs <;> dsimp <;> ring

def fiveValue (k : ℕ) (delta p : ℚ) : ℚ :=
  let A := indicator (p < -1)
  let B := indicator (p ≤ 0)
  let C := indicator (p ≤ -(tailCutoff delta : ℚ))
  let D := indicator ((tailCutoff delta : ℚ) ≤ p)
  A*C*clippedValue delta + A*(1-C)*activeValue delta p +
    (1-A)*B*middleValueQ k delta p + (1-B)*D*clippedValue delta +
    (1-B)*(1-D)*activeValue delta (-p)

theorem five_components (k : ℕ) (delta p : ℚ) :
    piecewiseValue k delta p = fiveValue k delta p := by
  by_cases hA : p < -1
  · have hB : p ≤ 0 := by linarith
    by_cases hC : p ≤ -(tailCutoff delta : ℚ)
    · simp [piecewiseValue, fiveValue, indicator, hA, hB, hC, negativeMidpoint_split]
    · simp [piecewiseValue, fiveValue, indicator, hA, hB, hC, negativeMidpoint_split]
  · by_cases hB : p ≤ 0
    · simp [piecewiseValue, fiveValue, indicator, hA, hB]
    · have hD : -p ≤ -(tailCutoff delta : ℚ) ↔ (tailCutoff delta : ℚ) ≤ p := by
        constructor <;> intro h <;> linarith
      by_cases hCut : (tailCutoff delta : ℚ) ≤ p
      · simp [piecewiseValue, fiveValue, indicator, hA, hB, negativeMidpoint_split, hD, hCut]
      · simp [piecewiseValue, fiveValue, indicator, hA, hB, negativeMidpoint_split, hD, hCut]

theorem actual_grid_five_components (k n : ℕ) (R delta : ℚ)
    (j : Fin (QuantumBlockEncoding.gridSize (n+1))) :
    piecewiseValue k delta (rationalGrid n R j) = fiveValue k delta (rationalGrid n R j) :=
  five_components k delta _

#print axioms negativeMidpoint_split
#print axioms five_components
#print axioms actual_grid_five_components
end HermitePiecewiseKernelProducer
