import FiniteTrigProducer
import RadiusSupplier
import RadiusStability
import NonunitaryTransport
import Mathlib.Analysis.Normed.Operator.NormedSpace

namespace ProviderReviewC13

open HermiteFiniteTrig

theorem signed_endpoints_ordered (q : ℚ) (n : ℕ) :
    ((sinBounds q n).1 : ℝ) ≤ ((sinBounds q n).2 : ℝ) ∧
    ((cosBounds q n).1 : ℝ) ≤ ((cosBounds q n).2 : ℝ) :=
  ⟨(sin_mem q n).1.trans (sin_mem q n).2,
   (cos_mem q n).1.trans (cos_mem q n).2⟩

example : radius (-3) 2 = 9/2 := by norm_num [radius]
example : sinPoly (-3) 2 = -3 := by
  norm_num [sinPoly, sinCoeff, Finset.sum_range_succ]
example : cosPoly (-3) 2 = -7/2 := by
  norm_num [cosPoly, cosCoeff, Finset.sum_range_succ]
example : selectDegree 0 (-1) 0 = none := by
  norm_num [selectDegree, radius, List.range_succ]

open QuantumBlockEncoding.ExperimentalRadiusSupplier

example : logTermCount 1 20 = 1 := by norm_num [logTermCount]
example : logTermCount 1 10 = 2 := by
  have hc : Nat.clog 2 2 = 1 := by simpa using Nat.clog_pow 2 1 (by norm_num)
  norm_num [logTermCount, hc]
example : logTermCount 1 5 = 3 := by
  have hc : Nat.clog 2 4 = 2 := by simpa using Nat.clog_pow 2 2 (by norm_num)
  norm_num [logTermCount, hc]
example : logRadiusInterval 1 20 = (-8146/1195, 15754/1195) := by
  norm_num [logRadiusInterval, logTermCount, piApprox, atanSum, Finset.sum_range_succ]

theorem radius_endpoints_ordered (L eps : ℚ) (hL : 0 < L) (heps : 0 < eps) :
    ((logRadiusInterval L eps).1 : ℝ) ≤ ((logRadiusInterval L eps).2 : ℝ) :=
  (logRadius_membership L eps hL heps).1.trans
    (logRadius_membership L eps hL heps).2

open QuantumBlockEncoding.ExperimentalNonunitaryTransport

theorem two_stage_chronology {R : Type*} [NormedRing R] (a b : Stage R) :
    nominalProduct [a,b] = b.nominal * a.nominal ∧
    surrogateProduct [a,b] = b.surrogate * a.surrogate := by
  simp [nominalProduct, surrogateProduct]

theorem three_stage_chronology {R : Type*} [NormedRing R] (a b c : Stage R) :
    surrogateProduct [a,b,c] = (c.surrogate * b.surrogate) * a.surrogate := by
  simp [surrogateProduct]

theorem whole_space_action {E : Type*} [NormedAddCommGroup E]
    [NormedSpace ℝ E] [Nontrivial E]
    (stages : List (Stage (E →L[ℝ] E))) (h : Valid stages) (x : E) :
    ‖surrogateProduct stages x - nominalProduct stages x‖ ≤
      (growth stages - 1) * ‖x‖ := by
  exact (ContinuousLinearMap.le_opNorm
    (surrogateProduct stages - nominalProduct stages) x).trans
    (mul_le_mul_of_nonneg_right (product_error_le stages h) (norm_nonneg x))

theorem operator_chronology {E : Type*} [NormedAddCommGroup E]
    [NormedSpace ℝ E] (a b : Stage (E →L[ℝ] E)) (x : E) :
    surrogateProduct [a,b] x = b.surrogate (a.surrogate x) := by
  simp [surrogateProduct]

#print axioms signed_endpoints_ordered
#print axioms radius_endpoints_ordered
#print axioms two_stage_chronology
#print axioms three_stage_chronology
#print axioms whole_space_action
#print axioms operator_chronology

end ProviderReviewC13
