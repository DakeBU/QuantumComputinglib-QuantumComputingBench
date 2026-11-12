import FiniteTrig
import QuantumBlockEncoding.PrimitiveRyPerturbation
import QuantumBlockEncoding.PrimitiveBasisLE

/-! Internal provider: exact textual-rational RY half angles to finite Taylor
midpoints. No Python parser, outward rounding or saved-stage refinement is claimed.
The surrogate is not assumed unitary. Every operator norm is Euclidean L2. -/
namespace HermiteSavedRyInterval

open QuantumBlockEncoding QuantumBlockEncoding.Robin.ComplexLCU HermiteFiniteTrig
open scoped Matrix.Norms.L2Operator

def rationalRotation (c s : ℚ) : Matrix (Fin 2) (Fin 2) ℚ :=
  !![c, -s; s, c]

def midpoint (theta : ℚ) (n : ℕ) : Matrix (Fin 2) (Fin 2) ℚ :=
  rationalRotation (cosPoly (theta / 2) n) (sinPoly (theta / 2) n)

noncomputable def finiteRy (theta : ℚ) (n : ℕ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (midpoint theta n).map (fun x => ((x : ℝ) : ℂ))

theorem finiteRy_literal (theta : ℚ) (n : ℕ) :
    finiteRy theta n = realOrthogonalRotation
      (cosPoly (theta / 2) n : ℝ) (sinPoly (theta / 2) n : ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [finiteRy, midpoint, rationalRotation, realOrthogonalRotation]

theorem half_cast (theta : ℚ) : ((theta / 2 : ℚ) : ℝ) = (theta : ℝ) / 2 := by
  norm_cast

theorem entry_error (theta : ℚ) (n : ℕ) (row col : Fin 2) :
    ‖(finiteRy theta n - standardRyMatrix (theta : ℝ)) row col‖ ≤
      (radius (theta / 2) n : ℝ) := by
  have hs := sin_error (theta / 2) n
  have hc := cos_error (theta / 2) n
  rw [half_cast] at hs hc
  rw [finiteRy_literal]
  fin_cases row <;> fin_cases col
  · change ‖((cosPoly (theta / 2) n : ℝ) : ℂ) -
      (Real.cos ((theta : ℝ) / 2) : ℂ)‖ ≤ _
    rw [← Complex.ofReal_sub, Complex.norm_real, Real.norm_eq_abs]
    simpa only [abs_sub_comm] using hc
  · change ‖-((sinPoly (theta / 2) n : ℝ) : ℂ) -
      -(Real.sin ((theta : ℝ) / 2) : ℂ)‖ ≤ _
    rw [show -((sinPoly (theta / 2) n : ℝ) : ℂ) -
        -(Real.sin ((theta : ℝ) / 2) : ℂ) =
        -(((sinPoly (theta / 2) n : ℝ) : ℂ) -
          (Real.sin ((theta : ℝ) / 2) : ℂ)) by ring,
      norm_neg, ← Complex.ofReal_sub, Complex.norm_real, Real.norm_eq_abs]
    simpa only [abs_sub_comm] using hs
  · change ‖((sinPoly (theta / 2) n : ℝ) : ℂ) -
      (Real.sin ((theta : ℝ) / 2) : ℂ)‖ ≤ _
    rw [← Complex.ofReal_sub, Complex.norm_real, Real.norm_eq_abs]
    simpa only [abs_sub_comm] using hs
  · change ‖((cosPoly (theta / 2) n : ℝ) : ℂ) -
      (Real.cos ((theta : ℝ) / 2) : ℂ)‖ ≤ _
    rw [← Complex.ofReal_sub, Complex.norm_real, Real.norm_eq_abs]
    simpa only [abs_sub_comm] using hc

/- The actual signed error matrix is a linear combination of two fixed
unitaries I and RY(pi). This derives the operator bound without assuming it. -/
theorem difference_decomposition (theta : ℚ) (n : ℕ) :
    finiteRy theta n - standardRyMatrix (theta : ℝ) =
      (((cosPoly (theta / 2) n : ℝ) - Real.cos ((theta : ℝ) / 2) : ℝ) : ℂ) •
        standardRyMatrix 0 +
      (((sinPoly (theta / 2) n : ℝ) - Real.sin ((theta : ℝ) / 2) : ℝ) : ℂ) •
        standardRyMatrix Real.pi := by
  rw [finiteRy_literal]
  ext row col
  fin_cases row <;> fin_cases col <;>
    simp [standardRyMatrix, realRotation, realOrthogonalRotation] <;> ring

theorem local_operator_error (theta : ℚ) (n : ℕ) :
    ‖finiteRy theta n - standardRyMatrix (theta : ℝ)‖ ≤
      2 * (radius (theta / 2) n : ℝ) := by
  have hs := sin_error (theta / 2) n
  have hc := cos_error (theta / 2) n
  rw [half_cast] at hs hc
  rw [difference_decomposition]
  calc
    _ ≤ ‖(((cosPoly (theta / 2) n : ℝ) - Real.cos ((theta : ℝ) / 2) : ℝ) : ℂ) •
          standardRyMatrix 0‖ +
        ‖(((sinPoly (theta / 2) n : ℝ) - Real.sin ((theta : ℝ) / 2) : ℝ) : ℂ) •
          standardRyMatrix Real.pi‖ := norm_add_le _ _
    _ = |(cosPoly (theta / 2) n : ℝ) - Real.cos ((theta : ℝ) / 2)| +
        |(sinPoly (theta / 2) n : ℝ) - Real.sin ((theta : ℝ) / 2)| := by
      rw [norm_smul, norm_smul,
        CStarRing.norm_of_mem_unitary (standardRyMatrix_unitary 0),
        CStarRing.norm_of_mem_unitary (standardRyMatrix_unitary Real.pi)]
      simp only [Complex.norm_real, Real.norm_eq_abs, mul_one]
    _ ≤ _ := by rw [abs_sub_comm] at hs hc; linarith

private theorem lift_add {qubits : ℕ} (target : Fin qubits)
    (A B : Matrix (Fin 2) (Fin 2) ℂ) :
    liftPrimitiveOneQubit target (A + B) =
      liftPrimitiveOneQubit target A + liftPrimitiveOneQubit target B := by
  ext row col
  simp only [liftPrimitiveOneQubit_apply, Matrix.add_apply]
  split_ifs <;> simp

theorem lifted_operator_error {qubits : ℕ} (target : Fin qubits)
    (theta : ℚ) (n : ℕ) :
    ‖liftPrimitiveOneQubit target (finiteRy theta n) -
      evalPrimitiveGate (.ry target (.rational theta))‖ ≤
      2 * (radius (theta / 2) n : ℝ) := by
  have hs := sin_error (theta / 2) n
  have hc := cos_error (theta / 2) n
  rw [half_cast] at hs hc
  change ‖liftPrimitiveOneQubit target (finiteRy theta n) -
    liftPrimitiveOneQubit target (standardRyMatrix (theta : ℝ))‖ ≤ _
  rw [← PrimitiveRyPerturbation.lift_sub, difference_decomposition,
    lift_add, PrimitiveRyPerturbation.lift_smul, PrimitiveRyPerturbation.lift_smul]
  calc
    _ ≤ ‖(((cosPoly (theta / 2) n : ℝ) - Real.cos ((theta : ℝ) / 2) : ℝ) : ℂ) •
          liftPrimitiveOneQubit target (standardRyMatrix 0)‖ +
        ‖(((sinPoly (theta / 2) n : ℝ) - Real.sin ((theta : ℝ) / 2) : ℝ) : ℂ) •
          liftPrimitiveOneQubit target (standardRyMatrix Real.pi)‖ := norm_add_le _ _
    _ = |(cosPoly (theta / 2) n : ℝ) - Real.cos ((theta : ℝ) / 2)| +
        |(sinPoly (theta / 2) n : ℝ) - Real.sin ((theta : ℝ) / 2)| := by
      rw [norm_smul, norm_smul,
        CStarRing.norm_of_mem_unitary (liftPrimitiveOneQubit_unitary target _ (standardRyMatrix_unitary 0)),
        CStarRing.norm_of_mem_unitary (liftPrimitiveOneQubit_unitary target _ (standardRyMatrix_unitary Real.pi))]
      simp only [Complex.norm_real, Real.norm_eq_abs, mul_one]
    _ ≤ _ := by rw [abs_sub_comm] at hs hc; linarith

theorem lifted_clm_error {qubits : ℕ} (target : Fin qubits)
    (theta : ℚ) (n : ℕ) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (liftPrimitiveOneQubit target (finiteRy theta n) -
        evalPrimitiveGate (.ry target (.rational theta)))‖ ≤
      2 * (radius (theta / 2) n : ℝ) := by
  rw [Matrix.l2_opNorm_toEuclideanCLM]
  exact lifted_operator_error target theta n

theorem lifted_vector_error {qubits : ℕ} (target : Fin qubits)
    (theta : ℚ) (n : ℕ) (v : EuclideanSpace ℂ (PrimitiveBasis qubits)) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (liftPrimitiveOneQubit target (finiteRy theta n) -
        evalPrimitiveGate (.ry target (.rational theta))) v‖ ≤
      (2 * (radius (theta / 2) n : ℝ)) * ‖v‖ := by
  exact le_trans (ContinuousLinearMap.le_opNorm _ v)
    (mul_le_mul_of_nonneg_right (lifted_clm_error target theta n) (norm_nonneg v))

theorem lifted_entry_error {qubits : ℕ} (target : Fin qubits)
    (theta : ℚ) (n : ℕ) (row col : PrimitiveBasis qubits) :
    ‖(liftPrimitiveOneQubit target (finiteRy theta n) -
      evalPrimitiveGate (.ry target (.rational theta))) row col‖ ≤
      (radius (theta / 2) n : ℝ) := by
  simp only [evalPrimitiveGate, ExactAngle.eval, Matrix.sub_apply,
    liftPrimitiveOneQubit_apply]
  split_ifs
  · exact entry_error theta n (row target) (col target)
  · simp only [sub_self, norm_zero]
    exact_mod_cast (show (0 : ℚ) ≤ radius (theta / 2) n by unfold radius; positivity)

end HermiteSavedRyInterval
