import QuantumBlockEncoding.PrimitiveMacros
import Mathlib.Tactic

/-!
# Clean-workspace C3X and three-bit modular addition

The reversible IR makes the arithmetic proof finite and transparent. Its
compiler emits only the repository's primitive `X`, `RY`, `RZ`, and `CX`
instructions; CCX and C3X remain specification-level macro names.
-/

namespace QuantumBlockEncoding

open QuantumBlockEncoding.Robin.ComplexLCU

def primitiveXProgram {qubits : Nat} (target : Fin qubits) :
    PrimitiveProgram qubits where
  circuit := [.x target]
  globalPhase := .rational 0

theorem primitiveXProgram_eval {qubits : Nat} (target : Fin qubits) :
    evalPrimitiveProgram (primitiveXProgram target) =
      Robin.ComplexLCU.equivPermutationMatrix (xBasisEquiv target) := by
  change evalGlobalPhase (.rational 0) •
      evalPrimitiveCircuit [.x target] = _
  have zeroPhase : evalGlobalPhase (.rational 0) = 1 := by
    simp [evalGlobalPhase, ExactAngle.eval]
  rw [zeroPhase, one_smul]
  simp [evalPrimitiveCircuit, evalPrimitiveGate]

noncomputable def compileReversibleGate {qubits : Nat} :
    ReversibleGate qubits → PrimitiveProgram qubits
  | .x target => primitiveXProgram target
  | .cx control target distinct =>
      primitiveCxProgram control target distinct
  | .ccx control0 control1 target c0_ne_c1 c0_ne_target c1_ne_target =>
      primitiveCCXProgram control0 control1 target c0_ne_c1
        c0_ne_target c1_ne_target

theorem compileReversibleGate_eval {qubits : Nat}
    (gate : ReversibleGate qubits) :
    evalPrimitiveProgram (compileReversibleGate gate) =
      Robin.ComplexLCU.equivPermutationMatrix (evalReversibleGate gate) := by
  cases gate with
  | x target => exact primitiveXProgram_eval target
  | cx control target distinct =>
      exact primitiveCxProgram_eval control target distinct
  | ccx control0 control1 target c0_ne_c1 c0_ne_target c1_ne_target =>
      exact primitiveCCXProgram_eval control0 control1 target c0_ne_c1
        c0_ne_target c1_ne_target

noncomputable def compileReversibleProgram {qubits : Nat} :
    ReversibleProgram qubits → PrimitiveProgram qubits
  | [] => PrimitiveProgram.identity qubits
  | gate :: rest =>
      (compileReversibleGate gate).seq (compileReversibleProgram rest)

theorem compileReversibleProgram_eval {qubits : Nat}
    (program : ReversibleProgram qubits) :
    evalPrimitiveProgram (compileReversibleProgram program) =
      Robin.ComplexLCU.equivPermutationMatrix
        (evalReversibleProgram program) := by
  induction program with
  | nil =>
      rw [compileReversibleProgram, evalPrimitiveProgram_identity]
      ext row column
      simp [evalReversibleProgram,
        Robin.ComplexLCU.equivPermutationMatrix,
        _root_.Matrix.one_apply] <;> rfl
  | cons gate rest induction =>
      rw [compileReversibleProgram, evalPrimitiveProgram_seq, induction,
        compileReversibleGate_eval, Robin.ComplexLCU.equivPermutationMatrix_mul]
      rfl

def cleanC3XReversibleProgram {qubits : Nat}
    (control0 control1 control2 target work : Fin qubits)
    (c0_ne_c1 : control0 ≠ control1)
    (c0_ne_work : control0 ≠ work)
    (c1_ne_work : control1 ≠ work)
    (work_ne_c2 : work ≠ control2)
    (work_ne_target : work ≠ target)
    (c2_ne_target : control2 ≠ target) : ReversibleProgram qubits :=
  [ .ccx control0 control1 work c0_ne_c1 c0_ne_work c1_ne_work
  , .ccx work control2 target work_ne_c2 work_ne_target c2_ne_target
  , .ccx control0 control1 work c0_ne_c1 c0_ne_work c1_ne_work
  ]

def cleanC3XBasisEquiv {qubits : Nat}
    (control0 control1 control2 target work : Fin qubits)
    (c0_ne_c1 : control0 ≠ control1)
    (c0_ne_work : control0 ≠ work)
    (c1_ne_work : control1 ≠ work)
    (work_ne_c2 : work ≠ control2)
    (work_ne_target : work ≠ target)
    (c2_ne_target : control2 ≠ target) :
    PrimitiveBasis qubits ≃ PrimitiveBasis qubits :=
  evalReversibleProgram
    (cleanC3XReversibleProgram control0 control1 control2 target work
      c0_ne_c1 c0_ne_work c1_ne_work work_ne_c2 work_ne_target
      c2_ne_target)

def c3xBasisAction {qubits : Nat}
    (control0 control1 control2 target : Fin qubits)
    (state : PrimitiveBasis qubits) : PrimitiveBasis qubits :=
  if state control0 = 1 ∧ state control1 = 1 ∧ state control2 = 1 then
    xBasisAction target state
  else state

theorem cleanC3XBasisAction {qubits : Nat}
    (control0 control1 control2 target work : Fin qubits)
    (c0_ne_c1 : control0 ≠ control1)
    (c0_ne_work : control0 ≠ work)
    (c1_ne_work : control1 ≠ work)
    (work_ne_c2 : work ≠ control2)
    (work_ne_target : work ≠ target)
    (c0_ne_target : control0 ≠ target)
    (c1_ne_target : control1 ≠ target)
    (c2_ne_target : control2 ≠ target)
    (state : PrimitiveBasis qubits) (workClean : state work = 0) :
    cleanC3XBasisEquiv control0 control1 control2 target work
        c0_ne_c1 c0_ne_work c1_ne_work work_ne_c2 work_ne_target
        c2_ne_target state =
      c3xBasisAction control0 control1 control2 target state := by
  have bitCases (bit : Fin 2) : bit = 0 ∨ bit = 1 := by
    fin_cases bit <;> simp
  rcases bitCases (state control0) with hc0 | hc0 <;>
    rcases bitCases (state control1) with hc1 | hc1 <;>
    rcases bitCases (state control2) with hc2 | hc2
  all_goals
    funext wire
    by_cases wireTarget : wire = target <;>
      by_cases wireWork : wire = work
  all_goals
      subst_vars
      simp_all [cleanC3XBasisEquiv, cleanC3XReversibleProgram,
        evalReversibleProgram, evalReversibleGate,
        ccxBasisAction, c3xBasisAction, xBasisAction, flipBit,
        c0_ne_work, c1_ne_work, work_ne_c2, work_ne_target,
        c0_ne_target, c1_ne_target,
        Ne.symm c0_ne_work, Ne.symm c1_ne_work,
        Ne.symm work_ne_c2, Ne.symm work_ne_target]

theorem cleanC3XWorkspaceClean {qubits : Nat}
    (control0 control1 control2 target work : Fin qubits)
    (c0_ne_c1 : control0 ≠ control1)
    (c0_ne_work : control0 ≠ work)
    (c1_ne_work : control1 ≠ work)
    (work_ne_c2 : work ≠ control2)
    (work_ne_target : work ≠ target)
    (c0_ne_target : control0 ≠ target)
    (c1_ne_target : control1 ≠ target)
    (c2_ne_target : control2 ≠ target)
    (state : PrimitiveBasis qubits) (workClean : state work = 0) :
    cleanC3XBasisEquiv control0 control1 control2 target work
        c0_ne_c1 c0_ne_work c1_ne_work work_ne_c2 work_ne_target
        c2_ne_target state work = 0 := by
  rw [cleanC3XBasisAction control0 control1 control2 target work
    c0_ne_c1 c0_ne_work c1_ne_work work_ne_c2 work_ne_target
    c0_ne_target c1_ne_target c2_ne_target state workClean]
  by_cases active :
      state control0 = 1 ∧ state control1 = 1 ∧ state control2 = 1
  · simp [c3xBasisAction, active, xBasisAction, work_ne_target, workClean]
  · simp [c3xBasisAction, active, workClean]

noncomputable def cleanC3XPrimitiveProgram {qubits : Nat}
    (control0 control1 control2 target work : Fin qubits)
    (c0_ne_c1 : control0 ≠ control1)
    (c0_ne_work : control0 ≠ work)
    (c1_ne_work : control1 ≠ work)
    (work_ne_c2 : work ≠ control2)
    (work_ne_target : work ≠ target)
    (c2_ne_target : control2 ≠ target) : PrimitiveProgram qubits :=
  compileReversibleProgram
    (cleanC3XReversibleProgram control0 control1 control2 target work
      c0_ne_c1 c0_ne_work c1_ne_work work_ne_c2 work_ne_target
      c2_ne_target)

theorem cleanC3XPrimitiveProgram_eval {qubits : Nat}
    (control0 control1 control2 target work : Fin qubits)
    (c0_ne_c1 : control0 ≠ control1)
    (c0_ne_work : control0 ≠ work)
    (c1_ne_work : control1 ≠ work)
    (work_ne_c2 : work ≠ control2)
    (work_ne_target : work ≠ target)
    (c2_ne_target : control2 ≠ target) :
    evalPrimitiveProgram
        (cleanC3XPrimitiveProgram control0 control1 control2 target work
          c0_ne_c1 c0_ne_work c1_ne_work work_ne_c2 work_ne_target
          c2_ne_target) =
      Robin.ComplexLCU.equivPermutationMatrix
        (cleanC3XBasisEquiv control0 control1 control2 target work
          c0_ne_c1 c0_ne_work c1_ne_work work_ne_c2 work_ne_target
          c2_ne_target) := by
  exact compileReversibleProgram_eval _

/-! ## Fixed three-bit little-endian adder -/

def littleEndian3Value (state : PrimitiveBasis 7)
    (wire0 wire1 wire2 : Fin 7) : Nat :=
  (state wire0).val + 2 * (state wire1).val + 4 * (state wire2).val

/-- Wire order is `a0,a1,a2,b0,b1,b2,work`. -/
def modularAdd3ReversibleProgram : ReversibleProgram 7 :=
  [ .ccx 3 0 6 (by decide) (by decide) (by decide)
  , .ccx 6 1 2 (by decide) (by decide) (by decide)
  , .ccx 3 0 6 (by decide) (by decide) (by decide)
  , .ccx 3 0 1 (by decide) (by decide) (by decide)
  , .cx 3 0 (by decide)
  , .ccx 4 1 2 (by decide) (by decide) (by decide)
  , .cx 4 1 (by decide)
  , .cx 5 2 (by decide)
  ]

def modularAdd3BasisEquiv : PrimitiveBasis 7 ≃ PrimitiveBasis 7 :=
  evalReversibleProgram modularAdd3ReversibleProgram

theorem modularAdd3_cleanAction (state : PrimitiveBasis 7)
    (workClean : state 6 = 0) :
    let output := modularAdd3BasisEquiv state
    littleEndian3Value output 0 1 2 =
        (littleEndian3Value state 0 1 2 +
          littleEndian3Value state 3 4 5) % 8 ∧
      output 3 = state 3 ∧ output 4 = state 4 ∧
      output 5 = state 5 ∧ output 6 = 0 := by
  native_decide +revert

noncomputable def modularAdd3PrimitiveProgram : PrimitiveProgram 7 :=
  compileReversibleProgram modularAdd3ReversibleProgram

theorem modularAdd3Primitive_eval :
    evalPrimitiveProgram modularAdd3PrimitiveProgram =
      Robin.ComplexLCU.equivPermutationMatrix modularAdd3BasisEquiv := by
  exact compileReversibleProgram_eval modularAdd3ReversibleProgram

theorem modularAdd3Primitive_workspaceClean (state : PrimitiveBasis 7)
    (workClean : state 6 = 0) :
    modularAdd3BasisEquiv state 6 = 0 :=
  (modularAdd3_cleanAction state workClean).2.2.2.2

/-- The resource is definitionally computed from the emitted primitive list. -/
theorem modularAdd3Primitive_resource_faithful :
    modularAdd3PrimitiveProgram.resource =
      modularAdd3PrimitiveProgram.circuit.resource := rfl

theorem modularAdd3Primitive_oracleCalls_eq_zero :
    modularAdd3PrimitiveProgram.resource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

end QuantumBlockEncoding
