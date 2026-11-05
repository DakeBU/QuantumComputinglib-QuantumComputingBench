import NonunitaryTransport
import Mathlib.Analysis.Normed.Operator.NormedSpace

open QuantumBlockEncoding.ExperimentalNonunitaryTransport

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [Nontrivial E]

theorem operator_apply_error (stages : List (Stage (E →L[ℝ] E)))
    (h : Valid stages) (x : E) :
    ‖surrogateProduct stages x - nominalProduct stages x‖ ≤
      (growth stages - 1) * ‖x‖ := by
  have hop := product_error_le stages h
  calc
    _ = ‖(surrogateProduct stages - nominalProduct stages) x‖ := rfl
    _ ≤ ‖surrogateProduct stages - nominalProduct stages‖ * ‖x‖ :=
      ContinuousLinearMap.le_opNorm _ _
    _ ≤ (growth stages - 1) * ‖x‖ :=
      mul_le_mul_of_nonneg_right hop (norm_nonneg _)

example : ‖surrogateProduct [expandingStage, expandingStage] -
    nominalProduct [expandingStage, expandingStage]‖ ≤ (21 : ℝ) / 100 := by
  have h := product_error_le _ expanding_valid
  norm_num [growth, expandingStage] at h ⊢
  exact h

#print axioms operator_apply_error
