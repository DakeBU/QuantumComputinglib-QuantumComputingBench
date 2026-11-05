import BasisCompatibility

/-! Exact internal adapter to the existing primitive evaluator, on the full carrier.
No phase quotient, register discarding, approximation, or resource certification. -/
namespace HermiteLiteralComplexAdapter
open HermiteSavedStageInterpreter HermiteSavedRounding QuantumBlockEncoding
open QuantumBlockEncoding.Robin.ComplexLCU
set_option allowUnsafeReducibility true in
attribute [local reducible] gridSize

def compileInstruction {width : ℕ} : Instruction width → PrimitiveGate width
  | .ry theta q => .ry q (.rational theta)
  | .cx c t h => .cx c t h

def compileWord {width : ℕ} (word : List (Instruction width)) : PrimitiveCircuit width :=
  word.map compileInstruction

noncomputable def castMatrix {width : ℕ} (m : RealMatrix width) :
    Matrix (Basis width) (Basis width) ℂ := fun i j => (m i j : ℂ)

noncomputable def namedCast {width : ℕ} (m : RealMatrix width) :
    Matrix (PrimitiveBasis width) (PrimitiveBasis width) ℂ :=
  Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width).symm (castMatrix m)

theorem split_symm_target {width : ℕ} (q : Fin width)
    (p : Fin 2 × (OtherPrimitiveWires q → Fin 2)) :
    (splitPrimitiveWire q).symm p q = p.1 :=
  congrArg Prod.fst ((splitPrimitiveWire q).apply_symm_apply p)

theorem lift_mul_apply {width : ℕ} (q : Fin width)
    (g : Matrix (Fin 2) (Fin 2) ℂ)
    (a : Matrix (PrimitiveBasis width) (PrimitiveBasis width) ℂ)
    (r c : PrimitiveBasis width) :
    (liftPrimitiveOneQubit q g * a) r c =
      ∑ v : Fin 2, g (r q) v *
        a ((splitPrimitiveWire q).symm (v, (splitPrimitiveWire q r).2)) c := by
  classical
  rw [Matrix.mul_apply, ← Equiv.sum_comp (splitPrimitiveWire q).symm]
  rw [Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro v _
  simp only [liftPrimitiveOneQubit_apply, Equiv.apply_symm_apply, split_symm_target]
  change (∑ ctx, (if (splitPrimitiveWire q r).2 = ctx then g (r q) v else 0) *
    a ((splitPrimitiveWire q).symm (v, ctx)) c) = _
  simp [eq_comm]

theorem namedCast_step {width : ℕ} (g : Instruction width) (m : RealMatrix width) :
    namedCast (realStep g m) = evalPrimitiveGate (compileInstruction g) * namedCast m := by
  ext r c
  cases g with
  | cx control target h =>
      rw [compileInstruction, evalPrimitiveGate, equivPermutationMatrix_mul_apply]
      change (m (cxRow control target (primitiveBasisLEEquiv width r))
        (primitiveBasisLEEquiv width c) : ℂ) =
        (m (primitiveBasisLEEquiv width (cxBasisAction control target r))
          (primitiveBasisLEEquiv width c) : ℂ)
      have hc := decode_cxRow (primitiveBasisLEEquiv width r) control target
      simp only [Equiv.symm_apply_apply] at hc
      exact congrArg (fun i => (m i (primitiveBasisLEEquiv width c) : ℂ))
        ((Equiv.symm_apply_eq (primitiveBasisLEEquiv width)).mp hc)
  | ry theta q =>
      rw [compileInstruction, evalPrimitiveGate, lift_mul_apply, Fin.sum_univ_two]
      have hl := decode_low (primitiveBasisLEEquiv width r) q
      have hh := decode_high (primitiveBasisLEEquiv width r) q
      simp only [Equiv.symm_apply_apply] at hl hh
      have hl' := (Equiv.symm_apply_eq (primitiveBasisLEEquiv width)).mp hl
      have hh' := (Equiv.symm_apply_eq (primitiveBasisLEEquiv width)).mp hh
      have hb := encode_testBit width r q
      change bit q (primitiveBasisLEEquiv width r) = decide (r q = 1) at hb
      simp only [namedCast, castMatrix, Matrix.coe_reindexAlgEquiv,
        Matrix.reindex_apply, Matrix.submatrix_apply, Equiv.symm_symm]
      rw [← hl', ← hh']
      change ((if bit q (primitiveBasisLEEquiv width r) then
          (realRyRow theta (m (low q (primitiveBasisLEEquiv width r))
            (primitiveBasisLEEquiv width c), m (high q (primitiveBasisLEEquiv width r))
            (primitiveBasisLEEquiv width c))).2 else
          (realRyRow theta (m (low q (primitiveBasisLEEquiv width r))
            (primitiveBasisLEEquiv width c), m (high q (primitiveBasisLEEquiv width r))
            (primitiveBasisLEEquiv width c))).1 : ℝ) : ℂ) = _
      rw [hb]
      generalize r q = v
      fin_cases v <;>
        simp [standardRyMatrix, ExactAngle.eval, realRotation, realOrthogonalRotation,
          realRyRow, Complex.ofReal_add, Complex.ofReal_sub, Complex.ofReal_mul] <;> ring

theorem namedCast_word {width : ℕ} (word : List (Instruction width)) (m : RealMatrix width) :
    namedCast (realWord word m) = evalPrimitiveCircuit (compileWord word) * namedCast m := by
  induction word generalizing m with
  | nil => simp [realWord, compileWord, evalPrimitiveCircuit]
  | cons g rest ih =>
      change namedCast (realWord rest (realStep g m)) = _
      rw [ih, namedCast_step]
      simp [compileWord, evalPrimitiveCircuit, mul_assoc]

theorem realWord_input_eq_primitive {width : ℕ} (word : List (Instruction width))
    (m : RealMatrix width) :
    castMatrix (realWord word m) =
      Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width)
        (evalPrimitiveCircuit (compileWord word)) * castMatrix m := by
  have h := congrArg (Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width))
    (namedCast_word word m)
  simpa only [namedCast, map_mul,
    ← Matrix.symm_reindexAlgEquiv, AlgEquiv.apply_symm_apply] using h

theorem realWord_eq_primitive {width : ℕ} (word : List (Instruction width)) :
    castMatrix (realWord word realIdentity) =
      Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv width)
        (evalPrimitiveCircuit (compileWord word)) := by
  rw [realWord_input_eq_primitive]
  have h : castMatrix (realIdentity : RealMatrix width) = 1 := by
    ext i j
    by_cases h : i = j <;> simp [castMatrix, realIdentity, Matrix.one_apply, h]
  rw [h, mul_one]

end HermiteLiteralComplexAdapter
