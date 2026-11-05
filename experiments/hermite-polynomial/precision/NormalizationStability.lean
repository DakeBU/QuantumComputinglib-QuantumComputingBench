import QuantumBlockEncoding.HermiteIntervalMass
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Module.Normalize

/-!
Internal exact-real precision bridge, not floating-point certification.
All caller error bounds must be supplied for the actual computed/serialized
object. The norm is Euclidean (PiLp 2), not the sup norm on plain functions.
Positive scales preserve literal signed complex amplitudes, not a phase class.
-/

namespace QuantumBlockEncoding.ExperimentalNormalizationStability

open scoped BigOperators
open NormedSpace

section Generic
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

theorem norm_normalize_le_one (y : E) : ‖normalize y‖ ≤ 1 := by
  by_cases hy : y = 0
  · simp [hy]
  · exact (norm_normalize hy).le

/-- Dimension-free, one-sided reference-norm stability, even if y=0. -/
theorem normalization_stability (x y : E) (hx : x ≠ 0) :
    ‖normalize y - normalize x‖ ≤ 2 * ‖y - x‖ / ‖x‖ := by
  have ha : 0 < ‖x‖ := norm_pos_iff.mpr hx
  have identity : ‖x‖ • (normalize y - normalize x) =
      (‖x‖ - ‖y‖) • normalize y + (y - x) := by
    rw [smul_sub, norm_smul_normalize, sub_smul, norm_smul_normalize]
    abel
  have bound : ‖x‖ * ‖normalize y - normalize x‖ ≤ 2 * ‖y - x‖ := by
    calc
      ‖x‖ * ‖normalize y - normalize x‖ =
          ‖‖x‖ • (normalize y - normalize x)‖ := by
        rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (norm_nonneg x)]
      _ = ‖(‖x‖ - ‖y‖) • normalize y + (y - x)‖ := congrArg norm identity
      _ ≤ ‖(‖x‖ - ‖y‖) • normalize y‖ + ‖y - x‖ := norm_add_le _ _
      _ = |‖x‖ - ‖y‖| * ‖normalize y‖ + ‖y - x‖ := by
        rw [norm_smul, Real.norm_eq_abs]
      _ ≤ |‖x‖ - ‖y‖| + ‖y - x‖ := by
        nlinarith [norm_normalize_le_one y, abs_nonneg (‖x‖ - ‖y‖)]
      _ ≤ 2 * ‖y - x‖ := by
        have h := abs_norm_sub_norm_le x y
        rw [norm_sub_rev x y] at h
        linarith
  exact (le_div_iff₀ ha).mpr (by simpa [mul_comm] using bound)

omit [NormedSpace ℝ E] in
theorem computed_nonzero (x y : E) {m δ : ℝ} (_hm : 0 < m)
    (floor : m ≤ ‖x‖) (error : ‖y - x‖ ≤ δ) (small : δ < m) : y ≠ 0 := by
  intro hy
  simp only [hy, zero_sub, norm_neg] at error
  linarith

/-- Explicit output error, including the inverse-normalizer and replay budgets. -/
theorem serialized_output_error (x y w : E) (hx : x ≠ 0) (hy : y ≠ 0)
    {s τ ζ : ℝ} (_hs : 0 < s) (scalar_error : |‖y‖ / s - 1| ≤ τ)
    (output_error : ‖w - s⁻¹ • y‖ ≤ ζ) :
    ‖w - normalize x‖ ≤ 2 * ‖y - x‖ / ‖x‖ + τ + ζ := by
  have hi : s⁻¹ • y - normalize y = (‖y‖ / s - 1) • normalize y := by
    rw [sub_smul, one_smul, div_eq_inv_mul, mul_smul, norm_smul_normalize]
  have hn : ‖s⁻¹ • y - normalize y‖ ≤ τ := by
    rw [hi, norm_smul, Real.norm_eq_abs, norm_normalize hy, mul_one]
    exact scalar_error
  have ht := norm_add_le (w - s⁻¹ • y) (s⁻¹ • y - normalize y)
  have hu := norm_add_le (w - normalize y) (normalize y - normalize x)
  simp only [sub_add_sub_cancel] at ht hu
  have hb := normalization_stability x y hx
  linarith

end Generic

/-- Relative norm approximation yields an explicit inverse-factor error. -/
theorem normalizer_relative_error {b s η : ℝ} (hb : 0 < b)
    (hη : 0 ≤ η) (small : η < 1) (error : |s - b| ≤ η * b) :
    0 < s ∧ |b / s - 1| ≤ η / (1 - η) := by
  have lower : (1 - η) * b ≤ s := by
    have he := (abs_le.mp error).1
    nlinarith
  have hd : 0 < 1 - η := by linarith
  have hs : 0 < s := lt_of_lt_of_le (mul_pos hd hb) lower
  refine ⟨hs, ?_⟩
  have hid : b / s - 1 = (b - s) / s := by field_simp
  rw [hid, abs_div, abs_of_pos hs, abs_sub_comm]
  apply (div_le_div_iff₀ hs hd).mpr
  calc
    |s - b| * (1 - η) ≤ (η * b) * (1 - η) :=
      mul_le_mul_of_nonneg_right error hd.le
    _ ≤ η * s := by nlinarith

noncomputable def sourceVector (k n : ℕ) (L : ℝ) :
    EuclideanSpace ℂ (Fin (gridSize (n + 1))) :=
  WithLp.toLp 2 (fun j => (HermiteStatePreparation.sampledAmplitude k (n + 1) L j : ℂ))

noncomputable def targetVector (k n : ℕ) (L : ℝ) :
    EuclideanSpace ℂ (Fin (gridSize (n + 1))) :=
  WithLp.toLp 2 (HermiteStatePreparation.normalizedAmplitude k (n + 1) L)

/-- Match the executable Euclidean metric, not plain-function sup norm. -/
theorem target_error_sq (k n : ℕ) (L : ℝ)
    (w : EuclideanSpace ℂ (Fin (gridSize (n + 1)))) :
    ‖w - targetVector k n L‖ ^ 2 =
      ∑ j, Complex.normSq (w j - HermiteStatePreparation.normalizedAmplitude k (n + 1) L j) := by
  simp [EuclideanSpace.norm_sq_eq, Complex.normSq_eq_norm_sq, targetVector]

theorem sourceVector_norm (k n : ℕ) (L : ℝ) :
    ‖sourceVector k n L‖ = HermiteStatePreparation.sampleNorm k (n + 1) L := by
  simp [sourceVector, EuclideanSpace.norm_eq, HermiteStatePreparation.sampleNorm,
    Complex.norm_real, Real.norm_eq_abs]

theorem hermite_norm_floor (k n : ℕ) (L : ℝ) :
    1 ≤ HermiteStatePreparation.sampleNorm k (n + 1) L := by
  unfold HermiteStatePreparation.sampleNorm
  have h := HermiteIntervalMass.sampled_mass_ge_one k n L
  have hh := Real.sqrt_le_sqrt h
  simpa using hh

theorem sourceVector_ne_zero (k n : ℕ) (L : ℝ) : sourceVector k n L ≠ 0 := by
  intro h
  have hf := hermite_norm_floor k n L
  rw [← sourceVector_norm, h, norm_zero] at hf
  linarith

theorem source_normalize_target (k n : ℕ) (L : ℝ) :
    normalize (sourceVector k n L) = targetVector k n L := by
  unfold NormedSpace.normalize
  rw [sourceVector_norm]
  ext j
  simp [sourceVector, targetVector,
    HermiteStatePreparation.normalizedAmplitude, div_eq_inv_mul]

/-- Literal positive rescaling with no new scientific premises. -/
theorem hermite_scaled_error (k n : ℕ) (L : ℝ) {F δ : ℝ} (hF : 0 < F)
    (y : EuclideanSpace ℂ (Fin (gridSize (n + 1))))
    (error : ‖y - F⁻¹ • sourceVector k n L‖ ≤ δ) :
    ‖normalize y - targetVector k n L‖ ≤ 2 * F * δ := by
  have hx : F⁻¹ • sourceVector k n L ≠ 0 :=
    smul_ne_zero (inv_ne_zero hF.ne') (sourceVector_ne_zero k n L)
  have hf : F⁻¹ ≤ ‖F⁻¹ • sourceVector k n L‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hF), sourceVector_norm]
    nlinarith [hermite_norm_floor k n L, inv_pos.mpr hF]
  have he := normalization_stability (F⁻¹ • sourceVector k n L) y hx
  rw [normalize_smul_of_pos (inv_pos.mpr hF), source_normalize_target] at he
  have hδ : 0 ≤ δ := le_trans (norm_nonneg _) error
  calc
    ‖normalize y - targetVector k n L‖ ≤
        2 * ‖y - F⁻¹ • sourceVector k n L‖ / ‖F⁻¹ • sourceVector k n L‖ := he
    _ ≤ 2 * δ / F⁻¹ := div_le_div₀ (by positivity) (by linarith) (inv_pos.mpr hF) hf
    _ = 2 * F * δ := by rw [div_inv_eq_mul]; ring

theorem hermite_computed_nonzero (k n : ℕ) (L : ℝ) {F δ : ℝ} (hF : 0 < F)
    (y : EuclideanSpace ℂ (Fin (gridSize (n + 1))))
    (error : ‖y - F⁻¹ • sourceVector k n L‖ ≤ δ) (small : F * δ < 1) : y ≠ 0 := by
  have hf : F⁻¹ ≤ ‖F⁻¹ • sourceVector k n L‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hF), sourceVector_norm]
    nlinarith [hermite_norm_floor k n L, inv_pos.mpr hF]
  apply computed_nonzero (F⁻¹ • sourceVector k n L) y (inv_pos.mpr hF) hf error
  rw [← one_div]
  apply (lt_div_iff₀ hF).mpr
  simpa [one_div, mul_comm] using small

theorem hermite_serialized_error (k n : ℕ) (L : ℝ) {F δ s τ ζ : ℝ} (hF : 0 < F)
    (y w : EuclideanSpace ℂ (Fin (gridSize (n + 1))))
    (error : ‖y - F⁻¹ • sourceVector k n L‖ ≤ δ) (small : F * δ < 1)
    (_hs : 0 < s) (scalar_error : |‖y‖ / s - 1| ≤ τ)
    (output_error : ‖w - s⁻¹ • y‖ ≤ ζ) :
    ‖w - targetVector k n L‖ ≤ 2 * F * δ + τ + ζ := by
  have hy := hermite_computed_nonzero k n L hF y error small
  have hh : ‖s⁻¹ • y - normalize y‖ ≤ τ := by
    have hi : s⁻¹ • y - normalize y = (‖y‖ / s - 1) • normalize y := by
      rw [sub_smul, one_smul, div_eq_inv_mul, mul_smul, norm_smul_normalize]
    rw [hi, norm_smul, Real.norm_eq_abs, norm_normalize hy, mul_one]
    exact scalar_error
  have ht := norm_add_le (w - s⁻¹ • y) (s⁻¹ • y - normalize y)
  have hu := norm_add_le (w - normalize y) (normalize y - targetVector k n L)
  simp only [sub_add_sub_cancel] at ht hu
  have he := hermite_scaled_error k n L hF y error
  linarith

/-- The supplied relative norm and serialized-action errors compose explicitly. -/
theorem hermite_serialized_relative_error (k n : ℕ) (L : ℝ) {F δ s η ζ : ℝ}
    (hF : 0 < F) (y w : EuclideanSpace ℂ (Fin (gridSize (n + 1))))
    (error : ‖y - F⁻¹ • sourceVector k n L‖ ≤ δ) (small : F * δ < 1)
    (hη : 0 ≤ η) (ηsmall : η < 1) (norm_error : |s - ‖y‖| ≤ η * ‖y‖)
    (output_error : ‖w - s⁻¹ • y‖ ≤ ζ) :
    ‖w - targetVector k n L‖ ≤ 2 * F * δ + η / (1 - η) + ζ := by
  have hy := hermite_computed_nonzero k n L hF y error small
  obtain ⟨hs, hratio⟩ := normalizer_relative_error (norm_pos_iff.mpr hy) hη ηsmall norm_error
  exact hermite_serialized_error k n L hF y w error small hs hratio output_error

#check normalization_stability
#check normalizer_relative_error
#check hermite_norm_floor
#check target_error_sq
#check hermite_scaled_error
#check hermite_computed_nonzero
#check hermite_serialized_error
#check hermite_serialized_relative_error
#print axioms normalization_stability
#print axioms normalizer_relative_error
#print axioms hermite_scaled_error
#print axioms hermite_serialized_error
#print axioms hermite_serialized_relative_error
#print axioms target_error_sq

end QuantumBlockEncoding.ExperimentalNormalizationStability
