import CachedMiddle
import RationalBlocks

/-! Actual rational setup and all five charged right-boundary branches.
This is a partial scalar/word ledger, not native or finite-bit complexity.
In particular Nat.ceil/floor/clog, natural conversions and large-integer index
arithmetic are not certified constant-time by a pure or charge below. -/

namespace HermiteCachedPiecewiseStored
open QuantumBlockEncoding.StoredGivens
open HermitePiecewiseAssembly HermiteFiniteExpDegree

structure RightSetup (n : ℕ) (R delta : ℚ) where
  cutMinusOne : ℕ
  cutZero : ℕ
  cutMinusT : ℕ
  cutT : ℕ
  tailCoeffs : Vector ℚ (sourceDegree delta+1)
  clipped : ℚ
  midpoint : ℚ

/-- Only rational division is charged here. The exact natural ceil/log
conversion remains outside this partial ledger, not an O(1) primitive. -/
def cutoffQ (delta : ℚ) : Run ℕ := do
  let reciprocal ← HermiteChargedSourceCache.qDiv 1 delta
  pure (Nat.clog 2 (max 1 (Nat.ceil reciprocal)))

def gridStepRun (width : ℕ) (R : ℚ) : Run ℚ := do
  let denominator ← powQ 2 width
  let numerator ← HermiteChargedSourceCache.qMul 2 R
  HermiteChargedSourceCache.qDiv numerator denominator

/-- The final natural minimum is charged as one comparison. Computing the
natural ceiling itself is explicitly outside the ledger. -/
def strictCutFrom (cap : ℕ) (R step s : ℚ) : Run ℕ := do
  let numerator ← HermiteChargedSourceCache.qAdd s R
  let quotient ← HermiteChargedSourceCache.qDiv numerator step
  charge .compare (min cap (Nat.ceil quotient))

/-- Keep the negative-quotient branch and the original floor-plus-one rule,
including step=0. Floor/conversion and natural addition are not native-costed. -/
def inclusiveCutFrom (cap : ℕ) (R step s : ℚ) : Run ℕ := do
  let numerator ← HermiteChargedSourceCache.qAdd s R
  let quotient ← HermiteChargedSourceCache.qDiv numerator step
  let negative ← charge .compare (decide (quotient < 0))
  let raw := if negative then 0 else Nat.floor quotient+1
  charge .compare (min cap raw)

def clippedRun (T : ℕ) : Run ℚ := do
  let denominator ← powQ 2 T
  let tail ← HermiteChargedSourceCache.qDiv 1 denominator
  HermiteChargedSourceCache.qDiv tail 2

/-- The literal bounds(-1) dispatch is T<=1. In the active branch the two
radius terms cancel in their average; that equality is a pending value goal.
The actual supplied factorials, powers and summation are all counted. -/
def midpointFrom (T d : ℕ) (F : Vector ℚ (d+1)) (clipped : ℚ) : Run ℚ := do
  let tail ← charge .compare (decide (T ≤ 1))
  if tail then pure clipped else
    HermiteChargedSourceCache.sumEntries fun i : Fin (d+1) => do
      let numerator ← powQ (-1) i.val
      let denominator ← QuantumBlockEncoding.StoredGivens.read F i
      HermiteChargedSourceCache.qDiv numerator denominator

/-- Same returned cutoff is used to compute degree, tail and midpoint. The
definitional equality hd is solely an index-transport proof, not a final value
or cost theorem. Combining its two costs is the dependent-index form of bind. -/
def rightSetup (n : ℕ) (R delta : ℚ) : Run (RightSetup n R delta) :=
  let cutoff := cutoffQ delta
  let T := cutoff.value
  let d := HermiteFiniteExpDegree.degree T T
  have hd : d = sourceDegree delta := by rfl
  let result : Run (RightSetup n R delta) := do
    let step ← gridStepRun (n+1) R
    let cap := 2^(n+1)
    let cutMinusOne ← strictCutFrom cap R step (-1)
    let cutZero ← inclusiveCutFrom cap R step 0
    let minusT ← qSub 0 (T : ℚ)
    let cutMinusT ← inclusiveCutFrom cap R step minusT
    let cutT ← strictCutFrom cap R step (T : ℚ)
    let F ← HermiteChargedSourceCache.factorials d
    let tailCoeffs ← collect fun i : Fin (d+1) => do
      let denominator ← QuantumBlockEncoding.StoredGivens.read F.values i
      HermiteChargedSourceCache.qDiv 1 denominator
    let clipped ← clippedRun T
    let midpoint ← midpointFrom T d F.values clipped
    pure {
      cutMinusOne := cutMinusOne
      cutZero := cutZero
      cutMinusT := cutMinusT
      cutT := cutT
      tailCoeffs := hd ▸ tailCoeffs
      clipped := clipped
      midpoint := midpoint }
  ⟨result.value, cutoff.cost + result.cost⟩

/-- The original acceptQ endpoint dispatch. Each executed natural comparison
is charged; its operand bitlength and the cap power remain outside this ledger. -/
def acceptRun (width cut : ℕ) (a : Fin 3) (flip : Bool) : Run ℚ := do
  let empty ← charge .compare (decide (cut = 0))
  let base ← if empty then pure (0 : ℚ) else do
    let full ← charge .compare (decide (cut = 2^width))
    if full then pure (1 : ℚ) else do
      let accepted ← charge .compare (decide (a = 0))
      pure (if accepted then (1 : ℚ) else 0)
  if flip then qSub 1 base else pure base

/-- The coefficient is an already counted Run, not an uncosted callback.
The two multiplications follow the original nested product order. -/
def rightProduct (width cutA cutB : ℕ) (flipA flipB : Bool)
    (a b : Fin 3) (coefficient : Run ℚ) : Run ℚ := do
  let first ← acceptRun width cutA a flipA
  let second ← acceptRun width cutB b flipB
  let scalar ← coefficient
  let inner ← HermiteChargedSourceCache.qMul second scalar
  HermiteChargedSourceCache.qMul first inner

/-- Actual five-component sum order. The old actualBlocksQ.right callback is
not called. The middle branch performs an actual read of the returned middle.
Clipped scalars are fixed record projections, not arithmetic callbacks. -/
def rightEntry (k n : ℕ) (R delta : ℚ) (s : RightSetup n R delta)
    (middle : Vector ℚ (2*k+2)) (z : FullIndex k delta) : Run ℚ :=
  match z with
  | .inl (a,(b,_j)) =>
      rightProduct (n+1) s.cutMinusOne s.cutMinusT false false a b (pure s.clipped)
  | .inr (.inl (a,(b,j))) =>
      rightProduct (n+1) s.cutMinusOne s.cutMinusT false true a b
        (QuantumBlockEncoding.StoredGivens.read s.tailCoeffs j)
  | .inr (.inr (.inl (a,(b,j)))) =>
      rightProduct (n+1) s.cutMinusOne s.cutZero true false a b
        (QuantumBlockEncoding.StoredGivens.read middle j)
  | .inr (.inr (.inr (.inl (a,(b,_j))))) =>
      rightProduct (n+1) s.cutZero s.cutT true true a b (pure s.clipped)
  | .inr (.inr (.inr (.inr (a,(b,j))))) =>
      rightProduct (n+1) s.cutZero s.cutT true false a b
        (QuantumBlockEncoding.StoredGivens.read s.tailCoeffs j)

end HermiteCachedPiecewiseStored
