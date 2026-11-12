import NominalStageTransport

namespace HermiteNominalStageTransport
open HermiteSavedStageInterpreter
open QuantumBlockEncoding.ExperimentalNonunitaryTransport
open scoped Matrix

theorem realIdentity_eq_one {width : ℕ} : (realIdentity : RealMatrix width) = 1 := by
  ext i j
  simp [realIdentity, Matrix.one_apply]

theorem realStep_right_mul {width : ℕ} (g : Instruction width)
    (m n : RealMatrix width) : realStep g (m * n) = realStep g m * n := by
  ext i j
  rw [Matrix.mul_apply]
  cases g with
  | ry theta q =>
      cases h : bit q i <;>
        simp [realStep, h, HermiteSavedRounding.realRyRow, Matrix.mul_apply,
          Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.mul_sum, sub_mul, add_mul,
          mul_assoc]
  | cx c t hne => rfl

theorem realWord_right_mul {width : ℕ} (word : List (Instruction width))
    (m n : RealMatrix width) : realWord word (m * n) = realWord word m * n := by
  induction word generalizing m with
  | nil => rfl
  | cons g rest ih =>
      change realWord rest (realStep g (m * n)) = realWord rest (realStep g m) * n
      rw [realStep_right_mul, ih]

theorem realWord_append_composition {width : ℕ} (left right : List (Instruction width)) :
    realWord (left ++ right) realIdentity =
      realWord right realIdentity * realWord left realIdentity := by
  rw [realWord, List.foldl_append]
  change realWord right (realWord left realIdentity) = _
  have h := realWord_right_mul right realIdentity (realWord left realIdentity)
  simpa only [realIdentity_eq_one, one_mul] using h

theorem nominalProduct_eq_flatten {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) :
    nominalProduct (actualStages words degree bits) =
      Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord words.flatten realIdentity) := by
  induction words with
  | nil =>
      simp [actualStages, nominalProduct, realWord, realIdentity_eq_one]
  | cons word rest ih =>
      change nominalProduct (actualStages rest degree bits) *
        Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord word realIdentity) =
        Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord (word ++ rest.flatten) realIdentity)
      rw [ih, realWord_append_composition, map_mul]

theorem actual_flatten_product_error {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) :
    ‖surrogateProduct (actualStages words degree bits) -
      Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord words.flatten realIdentity)‖ ≤
      growth (actualStages words degree bits) - 1 := by
  rw [← nominalProduct_eq_flatten words degree bits]
  exact actual_product_error words degree bits

theorem actual_flatten_apply_error {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) (x : StageSpace width) :
    ‖surrogateProduct (actualStages words degree bits) x -
      Matrix.toEuclideanCLM (𝕜 := ℝ) (realWord words.flatten realIdentity) x‖ ≤
      (growth (actualStages words degree bits) - 1) * ‖x‖ := by
  rw [← nominalProduct_eq_flatten words degree bits]
  exact actual_apply_error words degree bits x

end HermiteNominalStageTransport
