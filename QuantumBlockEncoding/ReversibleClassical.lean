import QuantumBlockEncoding.PrimitiveRefinement
import Mathlib.Tactic

/-!
# Exact reversible-classical proof IR

This intermediate language is used only while proving classical address and
indicator logic. Final T3 artifacts are compiled to `PrimitiveProgram`, whose
instruction set remains exactly `{X, RY, RZ, CX}`.
-/

namespace QuantumBlockEncoding

inductive ReversibleGate (qubits : Nat) where
  | x (target : Fin qubits)
  | cx (control target : Fin qubits) (distinct : control ≠ target)
  | ccx (control0 control1 target : Fin qubits)
      (c0_ne_c1 : control0 ≠ control1)
      (c0_ne_target : control0 ≠ target)
      (c1_ne_target : control1 ≠ target)

abbrev ReversibleProgram (qubits : Nat) := List (ReversibleGate qubits)

def ccxBasisAction {qubits : Nat} (control0 control1 target : Fin qubits)
    (state : PrimitiveBasis qubits) : PrimitiveBasis qubits :=
  if state control0 = 1 ∧ state control1 = 1 then
    xBasisAction target state
  else state

theorem ccxBasisAction_involutive {qubits : Nat}
    (control0 control1 target : Fin qubits)
    (c0_ne_target : control0 ≠ target)
    (c1_ne_target : control1 ≠ target) :
    Function.Involutive (ccxBasisAction control0 control1 target) := by
  intro state
  by_cases active : state control0 = 1 ∧ state control1 = 1
  · have c0 : xBasisAction target state control0 = state control0 := by
      simp [xBasisAction, c0_ne_target]
    have c1 : xBasisAction target state control1 = state control1 := by
      simp [xBasisAction, c1_ne_target]
    have first : ccxBasisAction control0 control1 target state =
        xBasisAction target state := if_pos active
    rw [first]
    have active' :
        xBasisAction target state control0 = 1 ∧
          xBasisAction target state control1 = 1 := by
      simpa [c0, c1] using active
    rw [ccxBasisAction, if_pos active']
    exact xBasisAction_involutive target state
  · simp [ccxBasisAction, active]

def ccxBasisEquiv {qubits : Nat} (control0 control1 target : Fin qubits)
    (c0_ne_target : control0 ≠ target)
    (c1_ne_target : control1 ≠ target) :
    PrimitiveBasis qubits ≃ PrimitiveBasis qubits where
  toFun := ccxBasisAction control0 control1 target
  invFun := ccxBasisAction control0 control1 target
  left_inv := ccxBasisAction_involutive control0 control1 target
    c0_ne_target c1_ne_target
  right_inv := ccxBasisAction_involutive control0 control1 target
    c0_ne_target c1_ne_target

@[simp] theorem ccxBasisEquiv_apply {qubits : Nat}
    (control0 control1 target : Fin qubits)
    (c0_ne_target : control0 ≠ target)
    (c1_ne_target : control1 ≠ target)
    (state : PrimitiveBasis qubits) :
    ccxBasisEquiv control0 control1 target c0_ne_target c1_ne_target state =
      ccxBasisAction control0 control1 target state := rfl

def evalReversibleGate {qubits : Nat} : ReversibleGate qubits →
    PrimitiveBasis qubits ≃ PrimitiveBasis qubits
  | .x target => xBasisEquiv target
  | .cx control target distinct => cxBasisEquiv control target distinct
  | .ccx control0 control1 target _ c0_ne_target c1_ne_target =>
      ccxBasisEquiv control0 control1 target c0_ne_target c1_ne_target

def evalReversibleProgram {qubits : Nat} : ReversibleProgram qubits →
    PrimitiveBasis qubits ≃ PrimitiveBasis qubits
  | [] => Equiv.refl _
  | gate :: rest => (evalReversibleGate gate).trans (evalReversibleProgram rest)

end QuantumBlockEncoding
