import SavedStageInterpreter
import Mathlib.Analysis.CStarAlgebra.Matrix

/-! Euclidean (not entrywise) operator error from the full interval stage.
No nominal contraction or NonunitaryTransport.Valid is assumed or claimed. -/
namespace HermiteSavedStageInterpreter
open HermiteSavedRounding
open scoped Matrix

def entryRadius (a : Interval) : ℚ := (a.hi - a.lo) / 2

def maxRadius {width : ℕ} (a : IntervalMatrix width) : ℚ :=
  (Finset.univ : Finset (Basis width × Basis width)).sup'
    ⟨(⟨0, by positivity⟩, ⟨0, by positivity⟩), Finset.mem_univ _⟩
    (fun ij => entryRadius (a ij.1 ij.2))

noncomputable def stageCenter {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) : RealMatrix width := fun i j =>
  (midpoint (intervalWord word degree bits intervalIdentity i j) : ℝ)

def stageEta {width : ℕ} (word : List (Instruction width)) (degree bits : ℕ) : ℚ :=
  (2 ^ width : ℚ) * maxRadius (intervalWord word degree bits intervalIdentity)

theorem entryRadius_le_maxRadius {width : ℕ} (a : IntervalMatrix width)
    (i j : Basis width) : entryRadius (a i j) ≤ maxRadius a := by
  unfold maxRadius
  exact Finset.le_sup' (s := (Finset.univ : Finset (Basis width × Basis width)))
    (f := fun ij : Basis width × Basis width => entryRadius (a ij.1 ij.2))
    (Finset.mem_univ (i,j))

theorem maxRadius_nonneg_of_encloses {width : ℕ} (a : IntervalMatrix width)
    (m : RealMatrix width) (h : Encloses a m) : 0 ≤ maxRadius a := by
  let z : Basis width := ⟨0, by positivity⟩
  have ho : (a z z).lo ≤ (a z z).hi := mem_ordered (a z z) (m z z) (h z z)
  have hr : 0 ≤ entryRadius (a z z) := by
    unfold entryRadius
    exact div_nonneg (sub_nonneg.mpr ho) (by norm_num)
  exact hr.trans (entryRadius_le_maxRadius _ z z)

theorem stage_maxRadius_nonneg {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) :
    0 ≤ maxRadius (intervalWord word degree bits intervalIdentity) :=
  maxRadius_nonneg_of_encloses _ _
    (word_encloses word degree bits intervalIdentity realIdentity identity_encloses)

theorem stage_max_entry_error {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) (i j : Basis width) :
    |(stageCenter word degree bits - realWord word realIdentity) i j| ≤
      (maxRadius (intervalWord word degree bits intervalIdentity) : ℝ) := by
  have hm := stage_midpoint_error word degree bits i j
  have hx : (entryRadius (intervalWord word degree bits intervalIdentity i j) : ℝ) ≤
      (maxRadius (intervalWord word degree bits intervalIdentity) : ℝ) := by
    exact_mod_cast entryRadius_le_maxRadius (intervalWord word degree bits intervalIdentity) i j
  change |(midpoint (intervalWord word degree bits intervalIdentity i j) : ℝ) -
    realWord word realIdentity i j| ≤ _
  rw [abs_sub_comm]
  exact hm.trans hx

theorem real_entry_bound_euclidean_opnorm {width : ℕ} (A : RealMatrix width)
    (r : ℝ) (hr : 0 ≤ r) (hA : ∀ i j, |A i j| ≤ r) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) A‖ ≤ (2 ^ width : ℝ) * r := by
  let T := Matrix.toEuclideanCLM (𝕜 := ℝ) A
  apply T.opNorm_le_bound (mul_nonneg (by positivity) hr)
  intro x
  apply (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (mul_nonneg (by positivity) hr)
    (norm_nonneg _))).mp
  have hrow : ∀ i : Basis width,
      ((A *ᵥ x.ofLp) i) ^ 2 ≤ (2 ^ width : ℝ) * r ^ 2 * ‖x‖ ^ 2 := by
    intro i
    have ha : (∑ j : Basis width, (A i j) ^ 2) ≤ (2 ^ width : ℝ) * r ^ 2 := by
      calc
        _ ≤ ∑ j : Basis width, r ^ 2 := Finset.sum_le_sum (fun j _ => by
          have h := (sq_le_sq₀ (abs_nonneg (A i j)) hr).mpr (hA i j)
          simpa only [sq_abs] using h)
        _ = _ := by simp [Basis]
    calc
      _ ≤ (∑ j : Basis width, (A i j) ^ 2) * ∑ j : Basis width, (x.ofLp j) ^ 2 := by
        simpa only [Matrix.mulVec, dotProduct] using
          Finset.sum_mul_sq_le_sq_mul_sq (Finset.univ : Finset (Basis width))
            (fun j => A i j) (fun j => x.ofLp j)
      _ = (∑ j : Basis width, (A i j) ^ 2) * ‖x‖ ^ 2 := by
        rw [EuclideanSpace.real_norm_sq_eq]
      _ ≤ _ := mul_le_mul_of_nonneg_right ha (sq_nonneg _)
  calc
    ‖T x‖ ^ 2 = ∑ i : Basis width, ((A *ᵥ x.ofLp) i) ^ 2 := by
      rw [EuclideanSpace.real_norm_sq_eq]
      rfl
    _ ≤ ∑ i : Basis width, (2 ^ width : ℝ) * r ^ 2 * ‖x‖ ^ 2 :=
      Finset.sum_le_sum (fun i _ => hrow i)
    _ = ((2 ^ width : ℝ) * r * ‖x‖) ^ 2 := by simp [Basis]; ring

theorem stage_euclidean_operator_error {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ)
      (stageCenter word degree bits - realWord word realIdentity)‖ ≤
      (stageEta word degree bits : ℝ) := by
  have hr : (0 : ℝ) ≤ (maxRadius (intervalWord word degree bits intervalIdentity) : ℝ) := by
    exact_mod_cast stage_maxRadius_nonneg word degree bits
  simpa only [stageEta, Rat.cast_mul, Rat.cast_pow, Rat.cast_ofNat] using
    real_entry_bound_euclidean_opnorm _ _ hr (stage_max_entry_error word degree bits)

end HermiteSavedStageInterpreter
