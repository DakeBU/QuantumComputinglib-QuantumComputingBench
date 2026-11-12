import StageOperatorBound
import NonunitaryTransport

/-! Internal full-carrier exact real contraction and actual interval-stage transport.
No identification with the separate complex primitive circuit evaluator is asserted. -/
namespace HermiteNominalStageTransport
open HermiteSavedStageInterpreter HermiteSavedRounding
open QuantumBlockEncoding.ExperimentalNonunitaryTransport
open scoped Matrix

noncomputable def vectorStep {width : ℕ} (g : Instruction width)
    (x : Basis width → ℝ) : Basis width → ℝ :=
  match g with
  | .ry theta q => fun i =>
      let p := realRyRow theta (x (low q i), x (high q i))
      if bit q i then p.2 else p.1
  | .cx c t _ => fun i => x (cxRow c t i)

theorem sum_involution {α : Type*} [Fintype α] (f : α → α)
    (hf : Function.Involutive f) (v : α → ℝ) :
    (∑ i, v (f i)) = ∑ i, v i := by
  let e : α ≃ α := ⟨f, f, hf, hf⟩
  exact Equiv.sum_comp e v

theorem ry_pair_square (theta : ℚ) (u v : ℝ) :
    (realRyRow theta (u,v)).1 ^ 2 + (realRyRow theta (u,v)).2 ^ 2 =
      u ^ 2 + v ^ 2 := by
  have h := Real.sin_sq_add_cos_sq ((theta : ℝ) / 2)
  dsimp [realRyRow]
  nlinarith [sq_nonneg u, sq_nonneg v]

theorem vectorStep_ry_pair {width : ℕ} (theta : ℚ) (q : Fin width)
    (x : Basis width → ℝ) (i : Basis width) :
    vectorStep (.ry theta q) x i ^ 2 +
      vectorStep (.ry theta q) x (flip q i) ^ 2 = x i ^ 2 + x (flip q i) ^ 2 := by
  cases h : bit q i with
  | false =>
      simpa [vectorStep, low, high, h, bit_flip, HermiteSavedStageInterpreter.flip_flip] using
        ry_pair_square theta (x i) (x (flip q i))
  | true =>
      simpa [vectorStep, low, high, h, bit_flip, HermiteSavedStageInterpreter.flip_flip, add_comm] using
        ry_pair_square theta (x (flip q i)) (x i)

theorem vectorStep_sum_square {width : ℕ} (g : Instruction width)
    (x : Basis width → ℝ) :
    (∑ i, vectorStep g x i ^ 2) = ∑ i, x i ^ 2 := by
  cases g with
  | ry theta q =>
      have hp := congrArg (fun f : Basis width → ℝ => ∑ i, f i)
        (funext (vectorStep_ry_pair theta q x))
      simp only [Finset.sum_add_distrib] at hp
      rw [sum_involution (flip q) (HermiteSavedStageInterpreter.flip_flip q)
          (fun i => vectorStep (.ry theta q) x i ^ 2),
        sum_involution (flip q) (HermiteSavedStageInterpreter.flip_flip q)
          (fun i => x i ^ 2)] at hp
      linarith
  | cx c t hne =>
      exact sum_involution (cxRow c t) (cxRow_involutive c t hne) (fun i => x i ^ 2)

theorem realStep_mulVec {width : ℕ} (g : Instruction width) (m : RealMatrix width)
    (x : Basis width → ℝ) :
    realStep g m *ᵥ x = vectorStep g (m *ᵥ x) := by
  funext i
  cases g with
  | ry theta q =>
      cases h : bit q i <;>
        simp [realStep, vectorStep, h, realRyRow, Matrix.mulVec, dotProduct,
          Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.mul_sum, sub_mul, add_mul,
          mul_assoc]
  | cx c t hne => rfl

theorem realStep_norm_preservation {width : ℕ} (g : Instruction width)
    (m : RealMatrix width) (x : EuclideanSpace ℝ (Basis width)) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (realStep g m) x‖ =
      ‖Matrix.toEuclideanCLM (𝕜 := ℝ) m x‖ := by
  apply (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp
  rw [EuclideanSpace.real_norm_sq_eq, EuclideanSpace.real_norm_sq_eq]
  change (∑ i, ((realStep g m *ᵥ x.ofLp) i) ^ 2) =
    ∑ i, ((m *ᵥ x.ofLp) i) ^ 2
  rw [realStep_mulVec]
  exact vectorStep_sum_square g _

theorem realWord_norm_preservation {width : ℕ} (word : List (Instruction width))
    (m : RealMatrix width) (x : EuclideanSpace ℝ (Basis width)) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord word m) x‖ =
      ‖Matrix.toEuclideanCLM (𝕜 := ℝ) m x‖ := by
  induction word generalizing m with
  | nil => rfl
  | cons g rest ih =>
      change ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord rest (realStep g m)) x‖ = _
      rw [ih, realStep_norm_preservation]

theorem nominal_norm_preservation {width : ℕ} (word : List (Instruction width))
    (x : EuclideanSpace ℝ (Basis width)) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord word realIdentity) x‖ = ‖x‖ := by
  rw [realWord_norm_preservation]
  have hid : (realIdentity : RealMatrix width) = 1 := by
    ext i j
    simp [realIdentity, Matrix.one_apply]
  rw [hid, map_one]
  rfl

theorem nominal_contraction {width : ℕ} (word : List (Instruction width)) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord word realIdentity)‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro x
  rw [nominal_norm_preservation, one_mul]

theorem stageEta_nonneg {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) : 0 ≤ stageEta word degree bits := by
  exact mul_nonneg (by positivity) (stage_maxRadius_nonneg word degree bits)

abbrev StageSpace (width : ℕ) := EuclideanSpace ℝ (Basis width)

noncomputable def actualStage {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) : Stage (StageSpace width →L[ℝ] StageSpace width) where
  nominal := Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord word realIdentity)
  surrogate := Matrix.toEuclideanCLM (𝕜 := ℝ) (stageCenter word degree bits)
  error := (stageEta word degree bits : ℝ)

noncomputable def actualStages {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) := words.map (fun word => actualStage word degree bits)

theorem actual_stage_valid {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) :
    0 ≤ (actualStage word degree bits).error ∧
    ‖(actualStage word degree bits).nominal‖ ≤ 1 ∧
    ‖(actualStage word degree bits).surrogate - (actualStage word degree bits).nominal‖ ≤
      (actualStage word degree bits).error := by
  refine ⟨?_, nominal_contraction word, ?_⟩
  · change (0 : ℝ) ≤ (stageEta word degree bits : ℝ)
    exact_mod_cast stageEta_nonneg word degree bits
  · change ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (stageCenter word degree bits) -
      Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord word realIdentity)‖ ≤ _
    rw [← map_sub]
    exact stage_euclidean_operator_error word degree bits

theorem actual_stages_valid {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) : Valid (actualStages words degree bits) := by
  intro s hs
  obtain ⟨word, _, rfl⟩ := List.mem_map.mp hs
  exact actual_stage_valid word degree bits

theorem actual_product_error {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) :
    ‖surrogateProduct (actualStages words degree bits) -
      nominalProduct (actualStages words degree bits)‖ ≤
      growth (actualStages words degree bits) - 1 :=
  product_error_le _ (actual_stages_valid words degree bits)

theorem actual_apply_error {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) (x : StageSpace width) :
    ‖surrogateProduct (actualStages words degree bits) x -
      nominalProduct (actualStages words degree bits) x‖ ≤
      (growth (actualStages words degree bits) - 1) * ‖x‖ := by
  calc
    _ = ‖(surrogateProduct (actualStages words degree bits) -
      nominalProduct (actualStages words degree bits)) x‖ := rfl
    _ ≤ ‖surrogateProduct (actualStages words degree bits) -
      nominalProduct (actualStages words degree bits)‖ * ‖x‖ :=
      ContinuousLinearMap.le_opNorm _ _
    _ ≤ _ := mul_le_mul_of_nonneg_right (actual_product_error words degree bits) (norm_nonneg x)

end HermiteNominalStageTransport
