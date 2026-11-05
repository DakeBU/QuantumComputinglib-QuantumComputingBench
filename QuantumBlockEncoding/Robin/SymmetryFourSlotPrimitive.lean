import QuantumBlockEncoding.PrimitiveRefinement
import QuantumBlockEncoding.Robin.SymmetryFourSlotBlockEncoding
import Mathlib.Tactic

/-!
# Primitive prerequisites for the Robin four-slot route

This module closes two independently auditable T3 leaves: the pair-coordinate
change is two physical CX gates, and every amplitude-table entry owns a typed
exact standard-RY angle.  The uniformly controlled RY synthesis remains a
separate refinement theorem; no full T3 certificate is claimed here.
-/

namespace QuantumBlockEncoding.Robin

/-- System-wire order is `(p0, p1, sector)`. -/
def warmRobinPairCoordinateCircuit : PrimitiveCircuit 3 :=
  [ .cx 2 1 (by decide), .cx 2 0 (by decide) ]

def warmRobinPairCoordinateBasisEquiv :
    PrimitiveBasis 3 ≃ PrimitiveBasis 3 :=
  (cxBasisEquiv (2 : Fin 3) (1 : Fin 3) (by decide)).trans
    (cxBasisEquiv (2 : Fin 3) (0 : Fin 3) (by decide))

theorem warmRobinPairCoordinateCircuit_eval_eq :
    evalPrimitiveCircuit warmRobinPairCoordinateCircuit =
      ComplexLCU.equivPermutationMatrix warmRobinPairCoordinateBasisEquiv := by
  simp only [warmRobinPairCoordinateCircuit, evalPrimitiveCircuit,
    evalPrimitiveGate, Matrix.one_mul]
  rw [ComplexLCU.equivPermutationMatrix_mul]
  rfl

def warmRobinPairBits (index : WarmRobinSymmetrySystem) : PrimitiveBasis 3 :=
  fun wire =>
    match wire.val with
    | 0 => ⟨index.2.val % 2, Nat.mod_lt _ (by decide)⟩
    | 1 => ⟨index.2.val / 2, by omega⟩
    | _ => index.1

def warmRobinOriginalBitsValue (state : PrimitiveBasis 3) : Nat :=
  state 0 + 2 * state 1 + 4 * state 2

/-- The two CX gates implement the non-free pair-coordinate reindex exactly. -/
theorem warmRobinPairCoordinateCircuit_image
    (index : WarmRobinSymmetrySystem) :
    warmRobinOriginalBitsValue
        (warmRobinPairCoordinateBasisEquiv (warmRobinPairBits index)) =
      (warmRobinPairSystemEquiv index).val := by
  rcases index with ⟨sector, pair⟩
  fin_cases sector <;> fin_cases pair <;> decide

theorem warmRobinPairCoordinateCircuit_bijective :
    Function.Bijective warmRobinPairCoordinateBasisEquiv :=
  warmRobinPairCoordinateBasisEquiv.bijective

/-- Lean-owned exact standard-RY angle for one loader branch. -/
noncomputable def warmRobinFourSlotExactAngle
    (slot : Fin 4) (column : WarmRobinSymmetrySystem) : ExactAngle :=
  .twiceArccosRational
    (warmRobinSymmetryFourShiftAmplitude column.1 slot column.2)
    (by
      simpa [warmRobinFourSlotCoefficient] using
        warmRobinFourSlotCoefficient_abs_le_one slot column)

@[simp] theorem warmRobinFourSlotExactAngle_eval
    (slot : Fin 4) (column : WarmRobinSymmetrySystem) :
    (warmRobinFourSlotExactAngle slot column).eval =
      2 * Real.arccos (warmRobinFourSlotCoefficient slot column) := by
  rfl

theorem warmRobinFourSlotExactRy_eq_rotation
    (slot : Fin 4) (column : WarmRobinSymmetrySystem) :
    standardRyMatrix (warmRobinFourSlotExactAngle slot column).eval =
      warmRobinFourSlotRotation slot column := by
  rw [warmRobinFourSlotExactAngle_eval]
  unfold warmRobinFourSlotRotation
  have bounded := abs_le.mp
    (warmRobinFourSlotCoefficient_abs_le_one slot column)
  exact standardRyMatrix_two_arccos_eq_amplitudeRotation _ bounded.1 bounded.2

end QuantumBlockEncoding.Robin
