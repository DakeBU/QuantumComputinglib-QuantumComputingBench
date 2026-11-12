import ChargedSourceCache
import Mathlib.Order.Interval.Finset.Nat

/-! C342 observation/interface definitions only. No numerical producer is changed.
The observers below describe literal dropped calls of C23 sumEntries at its actual
factorial table. They are not replacement cache producers, execution traces,
cost specifications, native scratch observations or one-evaluation claims.
The three closed Prop definitions are UNPROVED. -/

namespace HermiteSourceSuffix

open scoped BigOperators
open QuantumBlockEncoding.StoredGivens

/-- The table actually bound inside produceSourceCache, never a supplied F. -/
def actualFactorials (k : ℕ) : Vector ℚ (2*k+2) :=
  (HermiteChargedSourceCache.factorials (2*k+1)).value.values

/-- Literal sourceEntry term body with that fixed actual table. -/
def actualSourceTerm (k : ℕ) (i : Fin (k+1)) (r : Fin (i.val+1)) : Run ℚ :=
  let F := actualFactorials k
  do
    let binomial ← HermiteChargedSourceCache.chooseFrom (N := 2*k+1)
      F (k+i.val-r.val) k (by omega) (by omega)
    let denominator ← QuantumBlockEncoding.StoredGivens.read F ⟨r.val, by omega⟩
    HermiteChargedSourceCache.qDiv binomial denominator

/-- After s drops, local index r names original index s+r. Empty s=i+1
has domain Fin 0. Only Fin-index formation is proved in these definitions. -/
def droppedTerms (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2))
    (r : Fin (i.val+1-s.val)) : Run ℚ :=
  actualSourceTerm k i ⟨s.val+r.val, by
    have hr := r.isLt
    have hs := s.isLt
    omega⟩

/-- Value of the actual summation body after s successive drops. -/
def actualSuffixObservation (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)) : ℚ :=
  (HermiteChargedSourceCache.sumEntries (droppedTerms k i s)).value

/-- Literal f(r.succ) tail of the currently dropped body, not a presumed
equality to the next offset. The empty branch is explicitly zero. -/
def actualTailObservation (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)) : ℚ :=
  if h : s.val < i.val+1 then
    (HermiteChargedSourceCache.sumEntries fun r : Fin (i.val-s.val) =>
      droppedTerms k i s ⟨r.val+1, by
        have hr := r.isLt
        omega⟩).value
  else 0

/-- Mathematical Ico observation only; not executed by the C23 producer. -/
def SourceSuffix (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)) : ℚ :=
  ∑ r ∈ Finset.Ico s.val (i.val+1),
    (Nat.choose (k+i.val-r) k : ℚ)/(r.factorial : ℚ)

/-- Pending source binding, all offsets, actual recursive tail/next connection,
and the actual initial sourceEntry call. No correctness premise is supplied. -/
def ActualSuffixSpec : Prop :=
  ∀ (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)),
    actualSuffixObservation k i s = SourceSuffix k i s ∧
    actualSuffixObservation k i ⟨0, by omega⟩ =
      (HermiteChargedSourceCache.sourceEntry k (actualFactorials k) i).value ∧
    (if h : s.val < i.val+1 then
      let next : Fin (i.val+2) := ⟨s.val+1, by omega⟩
      actualTailObservation k i s = actualSuffixObservation k i next ∧
      actualSuffixObservation k i s =
        (actualSourceTerm k i ⟨s.val, h⟩).value + actualTailObservation k i s
    else actualSuffixObservation k i s = 0)

/-- Pending mathematical envelope. Actual observation bounds are obtained by
the first conjunct of ActualSuffixSpec, not a caller assumption. -/
def SuffixEnvelopeSpec : Prop :=
  ∀ (k : ℕ) (i : Fin (k+1)) (s : Fin (i.val+2)),
    let q := SourceSuffix k i s
    q.den ∣ k.factorial ∧ 0 ≤ q ∧
      q ≤ (((i.val+1-s.val)*2^(2*k) : ℕ) : ℚ)

/-- Pending same-object returned-cache corollary. Offset zero reuses the
original actual sourceEntry/collect/bind chain, not another coefficient source. -/
def ReturnedCacheSpec : Prop :=
  ∀ (k : ℕ) (i : Fin (k+1)),
    let a := (HermiteChargedSourceCache.produceSourceCache k).value[i.val]
    a = actualSuffixObservation k i ⟨0, by omega⟩ ∧
      a.den ∣ k.factorial ∧ 0 ≤ a ∧
      a ≤ (((k+1)*2^(2*k) : ℕ) : ℚ)

end HermiteSourceSuffix
