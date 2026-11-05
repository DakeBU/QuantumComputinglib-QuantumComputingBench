import LiteralComplexAdapter
import ChronologicalTransport
import QuantumBlockEncoding.PrimitiveRyPerturbation

/-! Actual saved-interval stage precision on the existing COMPLEX physical carrier.
No Valid, contraction or operator-identification premise is supplied by consumers.
No scientific ROOT, finite-bit/runtime or physical-local/global lift is asserted. -/
namespace HermiteComplexStageTransport
open HermiteLiteralComplexAdapter HermiteSavedStageInterpreter HermiteSavedRounding
open QuantumBlockEncoding
open QuantumBlockEncoding.ExperimentalNonunitaryTransport
open scoped Matrix Matrix.Norms.L2Operator

theorem complex_entry_bound_euclidean_opnorm {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℂ) (r : ℝ) (hr : 0 ≤ r) (hA : ∀ i j, ‖A i j‖ ≤ r) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ) A‖ ≤ (Fintype.card ι : ℝ) * r := by
  let T := Matrix.toEuclideanCLM (𝕜 := ℂ) A
  have hN : (0 : ℝ) ≤ Fintype.card ι := by positivity
  apply T.opNorm_le_bound (mul_nonneg hN hr)
  intro x
  apply (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (mul_nonneg hN hr)
    (norm_nonneg _))).mp
  have hrow : ∀ i : ι, ‖(A *ᵥ x.ofLp) i‖ ^ 2 ≤
      (Fintype.card ι : ℝ) * r ^ 2 * ‖x‖ ^ 2 := by
    intro i
    have ha : (∑ j : ι, ‖A i j‖ ^ 2) ≤ (Fintype.card ι : ℝ) * r ^ 2 := by
      calc
        _ ≤ ∑ j : ι, r ^ 2 := Finset.sum_le_sum (fun j _ =>
          (sq_le_sq₀ (norm_nonneg _) hr).mpr (hA i j))
        _ = _ := by simp
    have ht : ‖(A *ᵥ x.ofLp) i‖ ≤ ∑ j : ι, ‖A i j‖ * ‖x.ofLp j‖ := by
      simpa only [Matrix.mulVec, dotProduct, norm_mul] using
        norm_sum_le (Finset.univ : Finset ι) (fun j => A i j * x.ofLp j)
    calc
      _ ≤ (∑ j : ι, ‖A i j‖ * ‖x.ofLp j‖) ^ 2 :=
        (sq_le_sq₀ (norm_nonneg _) (Finset.sum_nonneg (fun j _ =>
          mul_nonneg (norm_nonneg _) (norm_nonneg _)))).mpr ht
      _ ≤ (∑ j : ι, ‖A i j‖ ^ 2) * ∑ j : ι, ‖x.ofLp j‖ ^ 2 :=
        Finset.sum_mul_sq_le_sq_mul_sq (Finset.univ : Finset ι)
          (fun j => ‖A i j‖) (fun j => ‖x.ofLp j‖)
      _ = (∑ j : ι, ‖A i j‖ ^ 2) * ‖x‖ ^ 2 := by
        rw [EuclideanSpace.norm_sq_eq]
      _ ≤ _ := mul_le_mul_of_nonneg_right ha (sq_nonneg _)
  calc
    ‖T x‖ ^ 2 = ∑ i : ι, ‖(A *ᵥ x.ofLp) i‖ ^ 2 := by
      rw [EuclideanSpace.norm_sq_eq]
      rfl
    _ ≤ ∑ i : ι, (Fintype.card ι : ℝ) * r ^ 2 * ‖x‖ ^ 2 :=
      Finset.sum_le_sum (fun i _ => hrow i)
    _ = ((Fintype.card ι : ℝ) * r * ‖x‖) ^ 2 := by simp; ring

theorem namedCast_identity {width : ℕ} :
    namedCast (realIdentity : RealMatrix width) = 1 := by
  have h : castMatrix (realIdentity : RealMatrix width) = 1 := by
    ext i j
    by_cases h : i = j <;> simp [castMatrix, realIdentity, Matrix.one_apply, h]
  rw [namedCast, h]
  exact (Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width).symm).map_one

theorem namedCast_nominal {width : ℕ} (word : List (Instruction width)) :
    namedCast (realWord word realIdentity) = evalPrimitiveCircuit (compileWord word) := by
  rw [namedCast_word, namedCast_identity, mul_one]

theorem stage_entry_error {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) (i j : PrimitiveBasis width) :
    ‖(namedCast (stageCenter word degree bits) -
      evalPrimitiveCircuit (compileWord word)) i j‖ ≤
      (maxRadius (intervalWord word degree bits intervalIdentity) : ℝ) := by
  rw [← namedCast_nominal]
  change ‖((stageCenter word degree bits (primitiveBasisLEEquiv width i)
      (primitiveBasisLEEquiv width j) : ℝ) : ℂ) -
    ((realWord word realIdentity (primitiveBasisLEEquiv width i)
      (primitiveBasisLEEquiv width j) : ℝ) : ℂ)‖ ≤ _
  rw [← Complex.ofReal_sub, Complex.norm_real, Real.norm_eq_abs]
  exact stage_max_entry_error word degree bits _ _

theorem stage_operator_error {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (namedCast (stageCenter word degree bits) -
        evalPrimitiveCircuit (compileWord word))‖ ≤ (stageEta word degree bits : ℝ) := by
  have hr : (0 : ℝ) ≤ (maxRadius (intervalWord word degree bits intervalIdentity) : ℝ) := by
    exact_mod_cast stage_maxRadius_nonneg word degree bits
  have hc : Fintype.card (PrimitiveBasis width) = 2 ^ width := by
    rw [Fintype.card_congr (primitiveBasisLEEquiv width)]
    change Fintype.card (Fin (2 ^ width)) = 2 ^ width
    exact Fintype.card_fin _
  have h := complex_entry_bound_euclidean_opnorm _ _ hr (stage_entry_error word degree bits)
  simpa only [hc, Nat.cast_pow, Nat.cast_ofNat, stageEta, Rat.cast_mul,
    Rat.cast_pow, Rat.cast_ofNat] using h

theorem nominal_contraction {width : ℕ} (word : List (Instruction width)) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (evalPrimitiveCircuit (compileWord word))‖ ≤ 1 := by
  rw [Matrix.l2_opNorm_toEuclideanCLM]
  exact le_of_eq (CStarRing.norm_of_mem_unitary (evalPrimitiveCircuit_unitary _))

abbrev StageSpace (width : ℕ) := EuclideanSpace ℂ (PrimitiveBasis width)

noncomputable def actualStage {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) : Stage (StageSpace width →L[ℂ] StageSpace width) where
  nominal := Matrix.toEuclideanCLM (𝕜 := ℂ) (evalPrimitiveCircuit (compileWord word))
  surrogate := Matrix.toEuclideanCLM (𝕜 := ℂ) (namedCast (stageCenter word degree bits))
  error := (stageEta word degree bits : ℝ)

noncomputable def actualStages {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) := words.map (fun word => actualStage word degree bits)

theorem actual_stage_valid {width : ℕ} (word : List (Instruction width)) (degree bits : ℕ) :
    0 ≤ (actualStage word degree bits).error ∧
    ‖(actualStage word degree bits).nominal‖ ≤ 1 ∧
    ‖(actualStage word degree bits).surrogate - (actualStage word degree bits).nominal‖ ≤
      (actualStage word degree bits).error := by
  refine ⟨?_, nominal_contraction word, ?_⟩
  · change (0 : ℝ) ≤ (stageEta word degree bits : ℝ)
    exact_mod_cast HermiteNominalStageTransport.stageEta_nonneg word degree bits
  · change ‖Matrix.toEuclideanCLM (𝕜 := ℂ) (namedCast (stageCenter word degree bits)) -
        Matrix.toEuclideanCLM (𝕜 := ℂ) (evalPrimitiveCircuit (compileWord word))‖ ≤ _
    rw [← map_sub]
    exact stage_operator_error word degree bits

theorem actual_stages_valid {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) : Valid (actualStages words degree bits) := by
  intro s hs
  obtain ⟨word, _, rfl⟩ := List.mem_map.mp hs
  exact actual_stage_valid word degree bits

theorem nominalProduct_eq_flatten {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) :
    nominalProduct (actualStages words degree bits) =
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten)) := by
  induction words with
  | nil => simp [actualStages, nominalProduct, compileWord, evalPrimitiveCircuit]
  | cons word rest ih =>
      change nominalProduct (actualStages rest degree bits) *
        Matrix.toEuclideanCLM (𝕜 := ℂ) (evalPrimitiveCircuit (compileWord word)) =
        Matrix.toEuclideanCLM (𝕜 := ℂ)
          (evalPrimitiveCircuit (compileWord (word ++ rest.flatten)))
      rw [ih]
      simp only [compileWord, List.map_append, evalPrimitiveCircuit_append, map_mul]

theorem actual_flatten_product_error {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) :
    ‖surrogateProduct (actualStages words degree bits) -
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten))‖ ≤
      growth (actualStages words degree bits) - 1 := by
  rw [← nominalProduct_eq_flatten words degree bits]
  exact product_error_le _ (actual_stages_valid words degree bits)

theorem actual_flatten_apply_error {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) (x : StageSpace width) :
    ‖surrogateProduct (actualStages words degree bits) x -
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten)) x‖ ≤
      (growth (actualStages words degree bits) - 1) * ‖x‖ := by
  calc
    _ = ‖(surrogateProduct (actualStages words degree bits) -
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten))) x‖ := rfl
    _ ≤ ‖surrogateProduct (actualStages words degree bits) -
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten))‖ * ‖x‖ :=
      ContinuousLinearMap.le_opNorm _ _
    _ ≤ _ := mul_le_mul_of_nonneg_right (actual_flatten_product_error words degree bits)
      (norm_nonneg x)

#print axioms stage_operator_error
#print axioms nominal_contraction
#print axioms actual_stages_valid
#print axioms nominalProduct_eq_flatten
#print axioms actual_flatten_product_error
#print axioms actual_flatten_apply_error
end HermiteComplexStageTransport
