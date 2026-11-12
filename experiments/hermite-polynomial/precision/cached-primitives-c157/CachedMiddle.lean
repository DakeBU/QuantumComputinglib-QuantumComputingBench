import ChargedSourceCache
import ActualCoefficients

/-! Phase-2 executable definitions only. No value or resource theorem is proved.
The rational arithmetic and stored-array traffic below are charged. Natural
index/control arithmetic, proof checking and counter metadata are outside this
partial scalar/word ledger; no finite-bit runtime claim is made. -/

namespace HermiteCachedPiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding.StoredGivens

def qSub (x y : ℚ) : Run ℚ := charge .field (x-y)

/-- A multiplication recurrence, not an uncharged rational power primitive. -/
def powQ (x : ℚ) : ℕ → Run ℚ
  | 0 => pure 1
  | m+1 => do
    let previous ← powQ x m
    HermiteChargedSourceCache.qMul previous x

/-- Literal specification only. Actual production does not execute Nat.choose
or use this expression as a desired-output callback. -/
def middleExpr (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1))
    (j : Fin (2*k+2)) : ℚ :=
  (∑ i : Fin (k+1),
    if k+1 ≤ j.val then e*a[i.val]*(-1)^(k+1)*
      (Nat.choose i.val (j.val-(k+1)) : ℚ) else 0) +
  ∑ i : Fin (k+1),
    if i.val ≤ j.val then a[i.val]*(-1)^i.val*
      (Nat.choose (k+1) (j.val-i.val) : ℚ) else 0

structure WeightedSources (k : ℕ) where
  first : Vector ℚ (k+1)
  second : Vector ℚ (k+1)

/-- Two actual scalar vectors. Their shared source cache is read, not recomputed.
No pair of scalar values is disguised as one scalar-storage word. -/
def weightedSources (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)) :
    Run (WeightedSources k) := do
  let sigma ← powQ (-1) (k+1)
  let first ← collect fun i : Fin (k+1) => do
    let x ← QuantumBlockEncoding.StoredGivens.read a i
    let scaled ← HermiteChargedSourceCache.qMul e x
    HermiteChargedSourceCache.qMul scaled sigma
  let second ← collect fun i : Fin (k+1) => do
    let x ← QuantumBlockEncoding.StoredGivens.read a i
    let sign ← powQ (-1) i.val
    HermiteChargedSourceCache.qMul x sign
  pure ⟨first,second⟩

/-- Reserve two comparison ticks, including a zero/short-circuit branch.
The second guard also prevents an out-of-range factorial-quotient binomial. -/
def middleFirstTerm (k : ℕ) (F : Vector ℚ (2*k+2))
    (u : Vector ℚ (k+1)) (j : Fin (2*k+2)) (i : Fin (k+1)) : Run ℚ :=
  let result : Run ℚ :=
    if h : k+1 ≤ j.val ∧ j.val-(k+1) ≤ i.val then do
      let x ← QuantumBlockEncoding.StoredGivens.read u i
      let binomial ← HermiteChargedSourceCache.chooseFrom (N := 2*k+1)
        F i.val (j.val-(k+1)) h.2 (by have hi := i.isLt; omega)
      HermiteChargedSourceCache.qMul x binomial
    else pure 0
  ⟨result.value, 2 • tick .compare + result.cost⟩

def middleSecondTerm (k : ℕ) (F : Vector ℚ (2*k+2))
    (v : Vector ℚ (k+1)) (j : Fin (2*k+2)) (i : Fin (k+1)) : Run ℚ :=
  let result : Run ℚ :=
    if h : i.val ≤ j.val ∧ j.val-i.val ≤ k+1 then do
      let x ← QuantumBlockEncoding.StoredGivens.read v i
      let binomial ← HermiteChargedSourceCache.chooseFrom (N := 2*k+1)
        F (k+1) (j.val-i.val) h.2 (by omega)
      HermiteChargedSourceCache.qMul x binomial
    else pure 0
  ⟨result.value, 2 • tick .compare + result.cost⟩

/-- Materialize the full signed monomial middle from one supplied cache.
This is not another source-coefficient producer. The second factorial pass is
explicitly counted because frozen C23 does not return its private factorials. -/
def middleFromCache (k : ℕ) (e : ℚ) (a : Vector ℚ (k+1)) :
    Run (Vector ℚ (2*k+2)) := do
  let F ← HermiteChargedSourceCache.factorials (2*k+1)
  let weights ← weightedSources k e a
  collect fun j : Fin (2*k+2) => do
    let first ← HermiteChargedSourceCache.sumEntries
      (middleFirstTerm k F.values weights.first j)
    let second ← HermiteChargedSourceCache.sumEntries
      (middleSecondTerm k F.values weights.second j)
    HermiteChargedSourceCache.qAdd first second

end HermiteCachedPiecewiseStored
