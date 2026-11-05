import QuantumBlockEncoding.StoredSelectedRyTrace
import Mathlib.Logic.Equiv.Fin.Basic

/-! Staged actual complement-table supplier. No choice-based complement
enumeration and no source correctness assumptions. Input Gray words and target
discovery are separate dependencies. Integer/address arithmetic and angle
instantiation remain outside the inherited stored-word cost model. -/
namespace QuantumBlockEncoding.HermiteExplicitControlsCandidate
open StoredGivens

def nextWire {q : ℕ} (target : Fin (q + 1)) (i : Fin q) : Run (Fin (q + 1)) := do
  let below ← charge .compare (decide (i.castSucc < target))
  pure (if below then i.castSucc else i.succ)

theorem nextWire_value {q : ℕ} (target : Fin (q + 1)) (i : Fin q) :
    (nextWire target i).value = target.succAbove i := by
  simp [nextWire, bind, pure, Run.bind, Run.pure, charge, Fin.succAbove]

def wires {q : ℕ} (target : Fin (q + 1)) : Run (Vector (Fin (q + 1)) q) :=
  collect (nextWire target)

theorem wires_value {q : ℕ} (target : Fin (q + 1)) (i : Fin q) :
    (wires target).value[i.val] = target.succAbove i := by
  simp [wires, nextWire_value]

theorem wires_distinct {q : ℕ} (target : Fin (q + 1)) (i : Fin q) :
    (wires target).value[i.val] ≠ target := by
  rw [wires_value]
  exact target.succAbove_ne i

def pattern {q : ℕ} (ws : Vector (Fin (q + 1)) q) (bits : Vector (Fin 2) (q + 1)) :
    Run (Vector (Fin 2) q) :=
  collect fun i => do
    let wire ← StoredGivens.read ws i
    StoredGivens.read bits wire

theorem pattern_value {q : ℕ} (ws : Vector (Fin (q + 1)) q)
    (bits : Vector (Fin 2) (q + 1)) (i : Fin q) :
    (pattern ws bits).value[i.val] = bits[ws[i.val].val] := by
  simp [pattern, StoredGivens.read, charge, bind, Run.bind]

def selected {q : ℕ} (target : Fin (q + 1)) (bits : Vector (Fin 2) (q + 1)) :
    Run (List (SelectedRyTrace.Gate (q + 1))) :=
  let ws := wires target
  let chosen := pattern ws.value bits
  let trace := StoredSelectedRyTrace.selected ws.value target (wires_distinct target) chosen.value
  ⟨trace.value, ws.cost + chosen.cost + trace.cost⟩

theorem selected_plane {q : ℕ} (target : Fin (q + 1))
    (bits : Vector (Fin 2) (q + 1)) (angle : ExactAngle) :
    evalPrimitiveCircuit (SelectedRyTrace.instantiate angle (selected target bits).value) =
      (selectedRyPlaneMatrix target (fun i => bits[i.val.val]) angle.eval).map Complex.ofReal := by
  simp only [selected]
  rw [StoredSelectedRyTrace.selected_refines]
  have ws : (fun i : Fin q => (wires target).value[i.val]) =
      (fun i => (finSuccAboveEquiv target i).val) := by
    funext i
    simp [wires_value, finSuccAboveEquiv_apply]
  have ps : StoredSelectedRyTrace.denoteBits (pattern (wires target).value bits).value =
      (fun i => bits[(finSuccAboveEquiv target i).val.val]) := by
    funext i
    simp [StoredSelectedRyTrace.denoteBits, pattern_value, wires_value, finSuccAboveEquiv_apply]
  simp only [ws, ps]
  exact compileSelectedRy_eval_plane target (finSuccAboveEquiv target)
    (fun i => bits[i.val.val]) angle

theorem wires_cost {q : ℕ} (target : Fin (q + 1)) (op : Op) :
    (wires target).cost op = q * (tick .compare op + 2 * tick .read op + 2 * tick .write op) := by
  simp [wires, collect_cost, nextWire, bind, pure, Run.bind, Run.pure, charge]
  ring

theorem pattern_cost {q : ℕ} (ws : Vector (Fin (q + 1)) q)
    (bits : Vector (Fin 2) (q + 1)) (op : Op) :
    (pattern ws bits).cost op = q * (4 * tick .read op + 2 * tick .write op) := by
  simp [pattern, collect_cost, StoredGivens.read, charge, bind, Run.bind]
  ring

theorem selected_total_cost_le {q : ℕ} (target : Fin (q + 1))
    (bits : Vector (Fin 2) (q + 1)) :
    StoredRectangularGivens.total (selected target bits).cost ≤
      (16 * q + 12) * 2 ^ q + 5 * q ^ 2 + 14 * q := by
  have bound := StoredSelectedRyTrace.selected_total_cost_le (wires target).value target
    (wires_distinct target) (pattern (wires target).value bits).value
  have wc : StoredRectangularGivens.total (wires target).cost = 5 * q := by
    simp [StoredRectangularGivens.total, wires_cost, tick]
    ring
  have pc : StoredRectangularGivens.total (pattern (wires target).value bits).cost = 6 * q := by
    simp [StoredRectangularGivens.total, pattern_cost, tick]
    ring
  have add (a b : Cost) : StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
    simp [StoredRectangularGivens.total]
    ring
  simp only [selected, add, wc, pc]
  omega

example : (wires (1 : Fin 4)).value = #v[0, 2, 3] := by native_decide
example : (wires (0 : Fin 1)).value = #v[] := by native_decide
example : (pattern (wires (1 : Fin 4)).value #v[1, 0, 0, 1]).value = #v[1, 0, 1] := by native_decide

#print axioms selected_plane
#print axioms selected_total_cost_le
end QuantumBlockEncoding.HermiteExplicitControlsCandidate
