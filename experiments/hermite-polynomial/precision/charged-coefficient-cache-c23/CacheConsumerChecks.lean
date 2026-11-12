import ChargedSourceCache
import QuantumBlockEncoding.StoredHermiteCoefficients

namespace HermiteChargedSourceCache
open QuantumBlockEncoding
open scoped BigOperators

/-- The cached vector supplies the actual C21 coefficient on its full range. -/
theorem produceSourceCache_actual (k : ℕ) (i : Fin (k+1)) :
    (produceSourceCache k).value[i.val] = HermiteFiniteMiddleSource.coefficientQ k i.val := by
  rw [produceSourceCache_entry]
  exact HermitePiecewiseAssembly.sourceCoefficientQ_eq k i.val (by omega)

/-- Rational refinement of the existing real source-coefficient producer.
This does not identify the Bernstein compile output or alter its exp primitive. -/
theorem produceSourceCache_real_sources (k : ℕ) (i : Fin (k+1)) :
    ((produceSourceCache k).value[i.val] : ℝ) =
      (StoredHermiteCoefficients.sources k
        (StoredHermiteCoefficients.factorials (2*k+1)).value.values).value[i.val] := by
  rw [produceSourceCache_entry,
    StoredHermiteCoefficients.sources_value k _ (StoredHermiteCoefficients.factorials_value _),
    HermiteBernstein.sourceCoefficient_eq]
  simp [HermitePiecewiseAssembly.sourceCoefficientQ]

/-- Eight ordinary counters from the SAME cached producer; not GCD/bit runtime. -/
theorem produceSourceCache_total_le (k : ℕ) :
    StoredRectangularGivens.total (produceSourceCache k).cost ≤ 416*(k+1)^2 := by
  have h1 := produceSourceCache_cost_le k .field
  have h2 := produceSourceCache_cost_le k .sqrt
  have h3 := produceSourceCache_cost_le k .angle
  have h4 := produceSourceCache_cost_le k .trig
  have h5 := produceSourceCache_cost_le k .compare
  have h6 := produceSourceCache_cost_le k .read
  have h7 := produceSourceCache_cost_le k .write
  have h8 := produceSourceCache_cost_le k .emit
  simp only [StoredRectangularGivens.total]
  omega

theorem same_cache_contract (k : ℕ) :
    (∀ i : Fin (k+1), (produceSourceCache k).value[i.val] =
      HermiteFiniteMiddleSource.coefficientQ k i.val) ∧
    StoredRectangularGivens.total (produceSourceCache k).cost ≤ 416*(k+1)^2 :=
  ⟨produceSourceCache_actual k, produceSourceCache_total_le k⟩

-- Supporting finite evaluations only; parametric roots above carry the claim.
example : (produceSourceCache 0).value.toList = [1] := by native_decide
example : (produceSourceCache 1).value.toList = [1,3] := by native_decide
example : (produceSourceCache 2).value.toList = [1,4,19/2] := by native_decide
example : (produceSourceCache 3).value.toList = [1,5,29/2,193/6] := by native_decide
example : StoredRectangularGivens.total (produceSourceCache 3).cost ≤ 416*4^2 := by native_decide

#print axioms produceSourceCache_actual
#print axioms produceSourceCache_real_sources
#print axioms produceSourceCache_total_le
#print axioms same_cache_contract
end HermiteChargedSourceCache
