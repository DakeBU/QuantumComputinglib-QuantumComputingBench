import ChargedSourceCache
import QuantumBlockEncoding.StoredHermiteCoefficients

/-! Independent internal arithmetic/count consumer. No publication, ROOT,
finite-bit, or complete C22 claim. Does not reuse the author's joined consumer. -/
namespace C23InternalReview
open scoped BigOperators
open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open HermiteChargedSourceCache

theorem same_object_arithmetic_and_count (k : ℕ) :
    let run := produceSourceCache k
    (∀ i : Fin (k+1), run.value[i.val] = HermiteFiniteMiddleSource.coefficientQ k i.val) ∧
    (∀ op : Op, run.cost op ≤ 52*(k+1)^2) ∧
    StoredRectangularGivens.total run.cost ≤ 416*(k+1)^2 := by
  dsimp only
  refine ⟨?_, produceSourceCache_cost_le k, ?_⟩
  · intro i
    rw [produceSourceCache_entry]
    exact HermitePiecewiseAssembly.sourceCoefficientQ_eq k i.val (by omega)
  · have hf := produceSourceCache_cost_le k .field
    have hs := produceSourceCache_cost_le k .sqrt
    have ha := produceSourceCache_cost_le k .angle
    have ht := produceSourceCache_cost_le k .trig
    have hc := produceSourceCache_cost_le k .compare
    have hr := produceSourceCache_cost_le k .read
    have hw := produceSourceCache_cost_le k .write
    have he := produceSourceCache_cost_le k .emit
    simp only [StoredRectangularGivens.total]
    omega

def lookup (k : ℕ) (i : Fin (k+1)) : Run ℚ := do
  let cache ← produceSourceCache k
  QuantumBlockEncoding.StoredGivens.read cache i

theorem lookup_same_object (k : ℕ) (i : Fin (k+1)) :
    (lookup k i).value = HermiteFiniteMiddleSource.coefficientQ k i.val ∧
    StoredRectangularGivens.total (lookup k i).cost ≤ 416*(k+1)^2+1 := by
  have h := same_object_arithmetic_and_count k
  dsimp only at h
  constructor
  · simpa [lookup, bind, Run.bind, QuantumBlockEncoding.StoredGivens.read, charge] using h.1 i
  · have ht := h.2.2
    simp only [StoredRectangularGivens.total] at ht
    simp [lookup, bind, Run.bind, QuantumBlockEncoding.StoredGivens.read, charge,
      StoredRectangularGivens.total, tick]
    omega

theorem produced_factorial_positive (n : ℕ) (i : Fin (n+1)) :
    0 < (factorials n).value.values[i.val] := by
  rw [factorials_value]
  exact_mod_cast Nat.factorial_pos i.val

theorem choose_denominator_nonzero (N n r : ℕ) (hr : r ≤ n) (hn : n ≤ N) :
    (factorials N).value.values[r] * (factorials N).value.values[n-r] ≠ 0 := by
  exact mul_ne_zero (ne_of_gt (produced_factorial_positive N ⟨r, by omega⟩))
    (ne_of_gt (produced_factorial_positive N ⟨n-r, by omega⟩))

theorem source_denominator_nonzero (k : ℕ) (i : Fin (k+1)) (r : Fin (i.val+1)) :
    (factorials (2*k+1)).value.values[r.val] ≠ 0 := by
  exact ne_of_gt (produced_factorial_positive (2*k+1) ⟨r.val, by omega⟩)

theorem real_source_bridge (k : ℕ) (i : Fin (k+1)) :
    ((produceSourceCache k).value[i.val] : ℝ) =
      (StoredHermiteCoefficients.sources k
        (StoredHermiteCoefficients.factorials (2*k+1)).value.values).value[i.val] := by
  rw [produceSourceCache_entry,
    StoredHermiteCoefficients.sources_value k _ (StoredHermiteCoefficients.factorials_value _),
    HermiteBernstein.sourceCoefficient_eq]
  simp [HermitePiecewiseAssembly.sourceCoefficientQ]

theorem sumEntries_exact_cost {n : ℕ} (f : Fin n → Run ℚ) (op : Op) :
    (sumEntries f).cost op = (∑ i, (f i).cost op)+n*tick .field op := by
  induction n with
  | zero => simp [sumEntries, pure, Run.pure]
  | succ n ih =>
    simp only [sumEntries, bind, Run.bind, qAdd, charge, Pi.add_apply]
    rw [ih, Fin.sum_univ_succ]
    ring

theorem sourceEntry_exact_cost (k : ℕ) (F : Vector ℚ (2*k+2))
    (i : Fin (k+1)) (op : Op) :
    (sourceEntry k F i).cost op = (i.val+1)*(4*tick .read op+4*tick .field op) := by
  rw [sourceEntry, sumEntries_exact_cost]
  simp only [bind, Run.bind, QuantumBlockEncoding.StoredGivens.read, qDiv, charge,
    Pi.add_apply, chooseFrom_cost]
  simp
  ring

def counts (k : ℕ) : List ℕ :=
  let c := (produceSourceCache k).cost
  [c .field, c .sqrt, c .angle, c .trig, c .compare, c .read, c .write, c .emit]

-- Small ordinary-kernel checked cases support, but do not replace, the parametric roots.
theorem values_zero : (produceSourceCache 0).value.toList = [1] := by decide +kernel
theorem values_one : (produceSourceCache 1).value.toList = [1,3] := by decide +kernel
theorem values_two : (produceSourceCache 2).value.toList = [1,4,19/2] := by decide +kernel
theorem values_three : (produceSourceCache 3).value.toList = [1,5,29/2,193/6] := by decide +kernel
theorem counts_zero : counts 0 = [6,0,0,0,2,14,8,0] := by decide
theorem counts_one : counts 1 = [18,0,0,0,9,45,24,0] := by decide
theorem counts_two : counts 2 = [34,0,0,0,20,92,48,0] := by decide
theorem counts_three : counts 3 = [54,0,0,0,35,155,80,0] := by decide
theorem total_zero : StoredRectangularGivens.total (produceSourceCache 0).cost = 30 := by decide
theorem total_one : StoredRectangularGivens.total (produceSourceCache 1).cost = 96 := by decide
theorem total_two : StoredRectangularGivens.total (produceSourceCache 2).cost = 194 := by decide
theorem total_three : StoredRectangularGivens.total (produceSourceCache 3).cost = 324 := by decide

-- Reject broad interpretations, not the actual hypothesis-free producer.
theorem arbitrary_factorial_table_is_not_a_choose_certificate :
    (chooseFrom (Vector.replicate 1 (0 : ℚ)) 0 0 (by omega) (by omega)).value ≠
      (Nat.choose 0 0 : ℚ) := by decide +kernel
theorem full_carrier_bridge_is_false :
    HermitePiecewiseAssembly.sourceCoefficientQ 0 2 ≠ HermiteFiniteMiddleSource.coefficientQ 0 2 := by
  decide +kernel

#print axioms same_object_arithmetic_and_count
#print axioms lookup_same_object
#print axioms produced_factorial_positive
#print axioms choose_denominator_nonzero
#print axioms source_denominator_nonzero
#print axioms real_source_bridge
#print axioms sumEntries_exact_cost
#print axioms sourceEntry_exact_cost
#print axioms values_zero
#print axioms values_one
#print axioms values_two
#print axioms values_three
#print axioms counts_zero
#print axioms counts_one
#print axioms counts_two
#print axioms counts_three
#print axioms total_zero
#print axioms total_one
#print axioms total_two
#print axioms total_three
#print axioms arbitrary_factorial_table_is_not_a_choose_certificate
#print axioms full_carrier_bridge_is_false
end C23InternalReview
