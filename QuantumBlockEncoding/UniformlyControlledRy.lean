import QuantumBlockEncoding.PrimitiveSemantics

/-!
# Reference compiler for uniformly controlled RY

This is the deliberately simple recursive compiler used before any Gray-code
optimization.  With `n` controls it emits `2^n` RY gates and
`2 * (2^n - 1)` CX gates.
-/

namespace QuantumBlockEncoding

open Robin.ComplexLCU
open scoped Kronecker

private def prependControlBit {n : Nat} (bit : Fin 2)
    (tail : PrimitiveBasis n) : PrimitiveBasis (n + 1) :=
  Fin.cons bit tail

private def halfAddAngles {n : Nat}
    (angles : PrimitiveBasis (n + 1) → ExactAngle) :
    PrimitiveBasis n → ExactAngle := fun tail =>
  ExactAngle.halfAdd
    (angles (prependControlBit 0 tail))
    (angles (prependControlBit 1 tail))

private def halfSubAngles {n : Nat}
    (angles : PrimitiveBasis (n + 1) → ExactAngle) :
    PrimitiveBasis n → ExactAngle := fun tail =>
  ExactAngle.halfSub
    (angles (prependControlBit 0 tail))
    (angles (prependControlBit 1 tail))

def primitiveControlAssignment {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (context : OtherPrimitiveWires target → Fin 2) : PrimitiveBasis controls :=
  fun control => context ⟨wires control, distinct control⟩

/-- Backend-independent specification: each fixed assignment of the non-target
wires owns one exact two-dimensional RY block selected by the control bits. -/
noncomputable def controlledRyBlockMatrix {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
    (_root_.Matrix.blockDiagonal fun context =>
      standardRyMatrix (angles (primitiveControlAssignment wires target distinct context)).eval)

@[simp] theorem controlledRyBlockMatrix_apply {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle)
    (row column : PrimitiveBasis qubits) :
    controlledRyBlockMatrix wires target distinct angles row column =
      if (splitPrimitiveWire target row).2 =
          (splitPrimitiveWire target column).2 then
        standardRyMatrix
          (angles (primitiveControlAssignment wires target distinct
            (splitPrimitiveWire target row).2)).eval
          (row target) (column target)
      else 0 := by
  simp [controlledRyBlockMatrix, _root_.Matrix.blockDiagonal_apply,
    splitPrimitiveWire]

private theorem kronecker_one_eq_blockDiagonal
    {context : Type*} [Fintype context] [DecidableEq context]
    (gate : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    gate ⊗ₖ (1 : _root_.Matrix context context ℂ) =
      _root_.Matrix.blockDiagonal (fun _ : context => gate) := by
  ext ⟨row, rowContext⟩ ⟨column, columnContext⟩
  by_cases equal : rowContext = columnContext
  · subst columnContext
    simp [_root_.Matrix.blockDiagonal_apply]
  · simp [_root_.Matrix.blockDiagonal_apply, equal]

private theorem evalPrimitiveRy_eq_controlledRyBlockMatrix_zero
    {qubits : Nat} (target : Fin qubits) (angle : ExactAngle) :
    evalPrimitiveGate (.ry target angle) =
      controlledRyBlockMatrix (fun index : Fin 0 => Fin.elim0 index)
        target (fun index => Fin.elim0 index) (fun _ => angle) := by
  change
    _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (standardRyMatrix angle.eval ⊗ₖ
          (1 : _root_.Matrix (OtherPrimitiveWires target → Fin 2)
            (OtherPrimitiveWires target → Fin 2) ℂ)) = _
  unfold controlledRyBlockMatrix
  congr 1
  rw [kronecker_one_eq_blockDiagonal]

private def controlledXBlock {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) (context : OtherPrimitiveWires target → Fin 2) :
    _root_.Matrix (Fin 2) (Fin 2) ℂ :=
  if context ⟨control, distinct⟩ = 0 then 1 else xMatrix

private theorem xMatrix_flipBit (bit : Fin 2) :
    xMatrix (flipBit bit) bit = 1 := by
  fin_cases bit <;> rfl

private theorem evalPrimitiveCx_eq_controlledXBlock
    {qubits : Nat} (control target : Fin qubits)
    (distinct : control ≠ target) :
    evalPrimitiveGate (.cx control target distinct) =
      _root_.Matrix.reindexAlgEquiv ℂ ℂ (splitPrimitiveWire target).symm
        (_root_.Matrix.blockDiagonal
          (controlledXBlock control target distinct)) := by
  ext row column
  simp only [evalPrimitiveGate, equivPermutationMatrix,
    _root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, _root_.Matrix.blockDiagonal_apply,
    cxBasisEquiv_apply, Equiv.symm_symm]
  by_cases contextsEqual :
      (splitPrimitiveWire target row).2 = (splitPrimitiveWire target column).2
  · have controlEqual : row control = column control := by
      simpa [splitPrimitiveWire, distinct] using
        congrFun contextsEqual ⟨control, distinct⟩
    have contextFunctionsEqual :
        (fun wire : OtherPrimitiveWires target => row wire.1) =
          fun wire => column wire.1 := by
      simpa [splitPrimitiveWire] using contextsEqual
    by_cases controlZero : column control = 0
    · have rowControlZero : row control = 0 := by simpa [controlEqual]
      have rowEq : row = column ↔ row target = column target := by
        constructor
        · intro equality
          exact congrFun equality target
        · intro targetEqual
          apply (splitPrimitiveWire target).injective
          apply Prod.ext
          · simpa [splitPrimitiveWire]
          · exact contextsEqual
      simp [controlledXBlock, contextsEqual, controlZero, rowControlZero,
        cxBasisAction, splitPrimitiveWire, rowEq,
        contextFunctionsEqual, Equiv.symm_symm]
      change (if row target = column target then 1 else 0) =
        if row target = column target then 1 else 0
      rfl
    · have rowControlNonzero : row control ≠ 0 := by simpa [controlEqual]
      by_cases targetFlipped : row target = flipBit (column target)
      · have action : row = cxBasisAction control target column := by
          funext wire
          by_cases wireTarget : wire = target
          · subst wire
            simpa [cxBasisAction, controlZero, xBasisAction] using targetFlipped
          · have outside := congrFun contextsEqual ⟨wire, wireTarget⟩
            simpa [cxBasisAction, controlZero, xBasisAction, splitPrimitiveWire,
              wireTarget] using outside
        have xContext :
            (fun wire : OtherPrimitiveWires target =>
              xBasisAction target column wire.1) =
              fun wire => column wire.1 := by
          funext wire
          simp [xBasisAction, wire.property]
        have xControl :
            xBasisAction target column control = column control := by
          simp [xBasisAction, distinct]
        have xTargetNe :
            xBasisAction target column target ≠ column target := by
          have flipNeAll : ∀ bit : Fin 2, flipBit bit ≠ bit := by decide
          have flipNe := flipNeAll (column target)
          simpa [xBasisAction] using flipNe
        simp [controlledXBlock, contextsEqual, controlZero,
          action, cxBasisAction, xMatrix, splitPrimitiveWire,
          contextFunctionsEqual, targetFlipped, xContext, xControl,
          xMatrix_flipBit, Equiv.symm_symm, xTargetNe]
      · have actionMiss : row ≠ cxBasisAction control target column := by
          intro action
          apply targetFlipped
          have := congrFun action target
          simpa [cxBasisAction, controlZero, xBasisAction] using this
        have bitComplement : ∀ left right : Fin 2,
            left ≠ flipBit right → left = right := by decide
        have targetEqual : row target = column target :=
          bitComplement _ _ targetFlipped
        simp [controlledXBlock, contextsEqual, controlZero, rowControlNonzero,
          actionMiss, xMatrix, splitPrimitiveWire, targetFlipped,
          targetEqual, contextFunctionsEqual, Equiv.symm_symm]
  · have actionMiss : row ≠ cxBasisAction control target column := by
      intro action
      apply contextsEqual
      funext wire
      have actionWire := congrFun action wire.1
      have unchanged :
          cxBasisAction control target column wire.1 = column wire.1 := by
        by_cases controlZero : column control = 0 <;>
          simp [cxBasisAction, controlZero, xBasisAction, wire.property]
      simpa [splitPrimitiveWire, unchanged] using actionWire
    simp [contextsEqual, actionMiss]

/-- Reference recursive compiler.  Controls are consumed from low to high in
the supplied control tuple; circuit execution remains chronological. -/
def compileUniformlyControlledRy {qubits : Nat} :
    (controls : Nat) →
    (wires : Fin controls → Fin qubits) →
    (target : Fin qubits) →
    (∀ control, wires control ≠ target) →
    (PrimitiveBasis controls → ExactAngle) →
    PrimitiveCircuit qubits
  | 0, _, target, _, angles =>
      [.ry target (angles fun index => Fin.elim0 index)]
  | controls + 1, wires, target, distinct, angles =>
      let head := wires 0
      let tailWires : Fin controls → Fin qubits := fun index => wires index.succ
      let tailDistinct : ∀ control, tailWires control ≠ target :=
        fun control => distinct control.succ
      let controlled := PrimitiveGate.cx head target (distinct 0)
      compileUniformlyControlledRy controls tailWires target tailDistinct
          (halfAddAngles angles) ++
        [controlled] ++
        compileUniformlyControlledRy controls tailWires target tailDistinct
          (halfSubAngles angles) ++
        [controlled]

/-- Recursive matrix specification corresponding to the standard multiplexor
identity.  This definition is backend-independent and mentions only exact
primitive matrix semantics. -/
noncomputable def uniformlyControlledRyMatrix {qubits : Nat} :
    (controls : Nat) →
    (wires : Fin controls → Fin qubits) →
    (target : Fin qubits) →
    (∀ control, wires control ≠ target) →
    (PrimitiveBasis controls → ExactAngle) →
    _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ
  | 0, _, target, _, angles =>
      evalPrimitiveGate (.ry target (angles fun index => Fin.elim0 index))
  | controls + 1, wires, target, distinct, angles =>
      let head := wires 0
      let tailWires : Fin controls → Fin qubits := fun index => wires index.succ
      let tailDistinct : ∀ control, tailWires control ≠ target :=
        fun control => distinct control.succ
      let controlled := evalPrimitiveGate
        (PrimitiveGate.cx head target (distinct 0))
      controlled *
        uniformlyControlledRyMatrix controls tailWires target tailDistinct
          (halfSubAngles angles) *
        controlled *
        uniformlyControlledRyMatrix controls tailWires target tailDistinct
          (halfAddAngles angles)

theorem compileUniformlyControlledRy_eval {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    evalPrimitiveCircuit
        (compileUniformlyControlledRy controls wires target distinct angles) =
      uniformlyControlledRyMatrix controls wires target distinct angles := by
  induction controls with
  | zero =>
      simp [compileUniformlyControlledRy, uniformlyControlledRyMatrix,
        evalPrimitiveCircuit]
  | succ controls induction =>
      simp only [compileUniformlyControlledRy, uniformlyControlledRyMatrix,
        evalPrimitiveCircuit_append, evalPrimitiveCircuit]
      rw [induction, induction]
      simp [mul_assoc]

/-- The recursive compiler satisfies the independent block-diagonal
specification selected by the computational-basis controls. -/
theorem compileUniformlyControlledRy_eval_controlledRyBlockMatrix
    {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    evalPrimitiveCircuit
        (compileUniformlyControlledRy controls wires target distinct angles) =
      controlledRyBlockMatrix wires target distinct angles := by
  induction controls with
  | zero =>
      have wiresEq : wires = fun index : Fin 0 => Fin.elim0 index := by
        funext index
        exact Fin.elim0 index
      have anglesEq : angles = fun _ => angles (fun index => Fin.elim0 index) := by
        funext bits
        congr 1
        funext index
        exact Fin.elim0 index
      subst wires
      rw [anglesEq]
      simpa [compileUniformlyControlledRy, evalPrimitiveCircuit] using
        evalPrimitiveRy_eq_controlledRyBlockMatrix_zero target
          (angles fun index => Fin.elim0 index)
  | succ controls induction =>
      simp only [compileUniformlyControlledRy, evalPrimitiveCircuit_append,
        evalPrimitiveCircuit]
      rw [induction, induction,
        evalPrimitiveCx_eq_controlledXBlock]
      unfold controlledRyBlockMatrix
      simp only [_root_.Matrix.one_mul, ← mul_assoc]
      rw [← _root_.Matrix.reindexAlgEquiv_mul,
        ← _root_.Matrix.reindexAlgEquiv_mul,
        ← _root_.Matrix.reindexAlgEquiv_mul]
      apply_fun (_root_.Matrix.reindexAlgEquiv ℂ ℂ
        (splitPrimitiveWire target).symm).symm
      simp only [AlgEquiv.symm_apply_apply]
      rw [← _root_.Matrix.blockDiagonal_mul,
        ← _root_.Matrix.blockDiagonal_mul,
        ← _root_.Matrix.blockDiagonal_mul]
      congr 1
      funext context
      let tailBits : PrimitiveBasis controls :=
        primitiveControlAssignment (fun index => wires index.succ) target
          (fun index => distinct index.succ) context
      by_cases headZero : context ⟨wires 0, distinct 0⟩ = 0
      · have assignmentZero' :
            prependControlBit 0 tailBits =
              primitiveControlAssignment wires target distinct context := by
          funext index
          refine Fin.cases ?_ ?_ index
          · exact headZero.symm
          · intro tail
            rfl
        simp only [controlledXBlock, headZero, if_pos, one_mul, mul_one]
        change
          standardRyMatrix (halfSubAngles angles tailBits).eval *
              standardRyMatrix (halfAddAngles angles tailBits).eval =
            standardRyMatrix
              (angles (primitiveControlAssignment wires target distinct context)).eval
        rw [show
          standardRyMatrix
                ((halfSubAngles angles tailBits).eval) *
              standardRyMatrix ((halfAddAngles angles tailBits).eval) =
            standardRyMatrix
              ((halfAddAngles angles tailBits).eval +
                (halfSubAngles angles tailBits).eval) by
              rw [standardRyMatrix_add]]
        congr 2
        simp only [halfAddAngles, halfSubAngles, ExactAngle.eval_half_add,
          ExactAngle.eval_half_sub]
        rw [assignmentZero']
        ring
      · have headOne : context ⟨wires 0, distinct 0⟩ = 1 := by
          have nonzeroIsOne : ∀ bit : Fin 2, bit ≠ 0 → bit = 1 := by decide
          exact nonzeroIsOne _ headZero
        have assignmentOne' :
            prependControlBit 1 tailBits =
              primitiveControlAssignment wires target distinct context := by
          funext index
          refine Fin.cases ?_ ?_ index
          · exact headOne.symm
          · intro tail
            rfl
        simp only [controlledXBlock, headZero, if_neg]
        change
          (xMatrix * standardRyMatrix (halfSubAngles angles tailBits).eval *
              xMatrix) *
              standardRyMatrix (halfAddAngles angles tailBits).eval =
            standardRyMatrix
              (angles (primitiveControlAssignment wires target distinct context)).eval
        rw [show
          xMatrix * standardRyMatrix (halfSubAngles angles tailBits).eval *
                xMatrix =
              standardRyMatrix (-(halfSubAngles angles tailBits).eval) by
            exact xMatrix_conjugates_standardRy _]
        rw [show
          standardRyMatrix (-(halfSubAngles angles tailBits).eval) *
              standardRyMatrix (halfAddAngles angles tailBits).eval =
            standardRyMatrix
              ((halfAddAngles angles tailBits).eval -
                (halfSubAngles angles tailBits).eval) by
              simpa [sub_eq_add_neg] using
                (standardRyMatrix_add
                  (halfAddAngles angles tailBits).eval
                  (-(halfSubAngles angles tailBits).eval)).symm]
        congr 2
        simp only [halfAddAngles, halfSubAngles, ExactAngle.eval_half_add,
          ExactAngle.eval_half_sub]
        rw [assignmentOne']
        ring

theorem compileUniformlyControlledRy_ryCount {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    (compileUniformlyControlledRy controls wires target distinct angles).ryCount =
      2 ^ controls := by
  induction controls with
  | zero => simp [compileUniformlyControlledRy, PrimitiveCircuit.ryCount]
  | succ controls induction =>
      simp only [compileUniformlyControlledRy,
        PrimitiveCircuit.ryCount_append,
        PrimitiveCircuit.ryCount_singleton_cx, Nat.add_zero]
      rw [induction, induction]
      simp [pow_succ]
      omega

theorem compileUniformlyControlledRy_cxCount {qubits controls : Nat}
    (wires : Fin controls → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    (compileUniformlyControlledRy controls wires target distinct angles).cxCount =
      2 * (2 ^ controls - 1) := by
  induction controls with
  | zero => simp [compileUniformlyControlledRy, PrimitiveCircuit.cxCount]
  | succ controls induction =>
      simp only [compileUniformlyControlledRy,
        PrimitiveCircuit.cxCount_append,
        PrimitiveCircuit.cxCount_singleton_cx]
      rw [induction, induction]
      rw [pow_succ]
      have powerPositive : 0 < 2 ^ controls := pow_pos (by decide) _
      omega

theorem compileUniformlyControlledRy_oracleCalls_eq_zero
    {qubits controls : Nat} (wires : Fin controls → Fin qubits)
    (target : Fin qubits) (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis controls → ExactAngle) :
    (compileUniformlyControlledRy controls wires target distinct angles).resource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

/-- Frozen Robin reference count: five controls require 32 RY and 62 CX. -/
theorem compileUniformlyControlledRy_five_control_counts
    {qubits : Nat} (wires : Fin 5 → Fin qubits) (target : Fin qubits)
    (distinct : ∀ control, wires control ≠ target)
    (angles : PrimitiveBasis 5 → ExactAngle) :
    (compileUniformlyControlledRy 5 wires target distinct angles).ryCount = 32 ∧
    (compileUniformlyControlledRy 5 wires target distinct angles).cxCount = 62 := by
  constructor
  · simpa using compileUniformlyControlledRy_ryCount wires target distinct angles
  · simpa using compileUniformlyControlledRy_cxCount wires target distinct angles

end QuantumBlockEncoding
