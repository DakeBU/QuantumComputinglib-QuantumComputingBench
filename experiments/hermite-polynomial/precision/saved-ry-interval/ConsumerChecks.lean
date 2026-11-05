import SavedRyInterval

namespace HermiteSavedRyInterval.Consumer
open QuantumBlockEncoding HermiteFiniteTrig
open scoped Matrix.Norms.L2Operator

theorem zero_angle (n : ℕ) : finiteRy 0 n = 1 := by
  have h := local_operator_error 0 n
  have hz : (radius (0 / 2) n : ℝ) = 0 := by simp [radius]
  rw [hz, mul_zero] at h
  have he := norm_eq_zero.mp (le_antisymm h (norm_nonneg _))
  simpa only [Rat.cast_zero, standardRyMatrix_zero] using (sub_eq_zero.mp he)

theorem signed_half_angle :
    midpoint 1 1 0 1 = -(1 / 2 : ℚ) ∧ midpoint 1 1 1 0 = (1 / 2 : ℚ) ∧
    midpoint (-1) 1 0 1 = (1 / 2 : ℚ) ∧ midpoint (-1) 1 1 0 = -(1 / 2 : ℚ) ∧
    midpoint 1 1 1 0 ≠ (1 : ℚ) := by
  norm_num [midpoint, rationalRotation, cosPoly, sinPoly, cosCoeff, sinCoeff,
    Finset.sum_range_succ]

private theorem context01 :
    (splitPrimitiveWire (0 : Fin 3) (primitiveBits3LE 1)).2 =
      (splitPrimitiveWire (0 : Fin 3) (primitiveBits3LE 0)).2 := by
  funext wire
  rcases wire with ⟨wire, h⟩
  fin_cases wire <;> norm_num [splitPrimitiveWire, primitiveBits3LE] at *
  exact (h rfl).elim

private theorem context12 :
    (splitPrimitiveWire (1 : Fin 3) (primitiveBits3LE 2)).2 =
      (splitPrimitiveWire (1 : Fin 3) (primitiveBits3LE 0)).2 := by
  funext wire
  rcases wire with ⟨wire, h⟩
  fin_cases wire <;> norm_num [splitPrimitiveWire, primitiveBits3LE] at *
  exact (h rfl).elim

private theorem context24 :
    (splitPrimitiveWire (2 : Fin 3) (primitiveBits3LE 4)).2 =
      (splitPrimitiveWire (2 : Fin 3) (primitiveBits3LE 0)).2 := by
  funext wire
  rcases wire with ⟨wire, h⟩
  fin_cases wire <;> norm_num [splitPrimitiveWire, primitiveBits3LE] at *
  exact (h rfl).elim

theorem physical_wire_discriminators :
    liftPrimitiveOneQubit (0 : Fin 3) (finiteRy 1 1)
      (primitiveBits3LE 1) (primitiveBits3LE 0) = (1 / 2 : ℂ) ∧
    liftPrimitiveOneQubit (1 : Fin 3) (finiteRy 1 1)
      (primitiveBits3LE 2) (primitiveBits3LE 0) = (1 / 2 : ℂ) ∧
    liftPrimitiveOneQubit (2 : Fin 3) (finiteRy 1 1)
      (primitiveBits3LE 4) (primitiveBits3LE 0) = (1 / 2 : ℂ) := by
  simp only [liftPrimitiveOneQubit_apply, context01, context12, context24, if_true]
  repeat' apply And.intro
  all_goals change finiteRy 1 1 1 0 = (1 / 2 : ℂ)
  all_goals norm_num [finiteRy, midpoint, rationalRotation, cosPoly,
    sinPoly, cosCoeff, sinCoeff, Finset.sum_range_succ]

theorem spectator_discriminator :
    liftPrimitiveOneQubit (0 : Fin 3) (finiteRy 1 1)
      (primitiveBits3LE 2) (primitiveBits3LE 0) = 0 := by
  have h : (splitPrimitiveWire (0 : Fin 3) (primitiveBits3LE 2)).2 ≠
      (splitPrimitiveWire (0 : Fin 3) (primitiveBits3LE 0)).2 := by
    intro he
    have hc := congrFun he (⟨1, by decide⟩ : OtherPrimitiveWires (0 : Fin 3))
    norm_num [splitPrimitiveWire, primitiveBits3LE] at hc
  simp [liftPrimitiveOneQubit_apply, h]

theorem cx_basis_discriminator :
    cxBasisAction (0 : Fin 2) 1 (primitiveBits2LE 0) = primitiveBits2LE 0 ∧
    cxBasisAction (0 : Fin 2) 1 (primitiveBits2LE 1) = primitiveBits2LE 3 ∧
    cxBasisAction (0 : Fin 2) 1 (primitiveBits2LE 2) = primitiveBits2LE 2 ∧
    cxBasisAction (0 : Fin 2) 1 (primitiveBits2LE 3) = primitiveBits2LE 1 := by
  repeat' apply And.intro
  all_goals funext wire; fin_cases wire
  all_goals norm_num [cxBasisAction, xBasisAction, flipBit, primitiveBits2LE,
    Function.update]

def firstSavedTheta : ℚ := -86958955523179937 / 100000000000000000

theorem actual_saved_first_entry (row col : Fin 2) :
    ‖(finiteRy firstSavedTheta 96 - standardRyMatrix (firstSavedTheta : ℝ)) row col‖ ≤
      (radius (firstSavedTheta / 2) 96 : ℝ) := entry_error firstSavedTheta 96 row col

theorem actual_saved_first_operator :
    ‖finiteRy firstSavedTheta 96 - standardRyMatrix (firstSavedTheta : ℝ)‖ ≤
      2 * (radius (firstSavedTheta / 2) 96 : ℝ) := local_operator_error firstSavedTheta 96

#check finiteRy_literal
#check entry_error
#check difference_decomposition
#check local_operator_error
#check lifted_operator_error
#check lifted_clm_error
#check lifted_vector_error
#check lifted_entry_error

#print axioms finiteRy_literal
#print axioms entry_error
#print axioms difference_decomposition
#print axioms local_operator_error
#print axioms lifted_operator_error
#print axioms lifted_clm_error
#print axioms lifted_vector_error
#print axioms lifted_entry_error
#print axioms zero_angle
#print axioms signed_half_angle
#print axioms physical_wire_discriminators
#print axioms spectator_discriminator
#print axioms cx_basis_discriminator
#print axioms actual_saved_first_entry
#print axioms actual_saved_first_operator

end HermiteSavedRyInterval.Consumer
