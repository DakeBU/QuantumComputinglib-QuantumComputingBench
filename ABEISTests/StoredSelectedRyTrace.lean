import QuantumBlockEncoding.StoredSelectedRyTrace

namespace StoredSelectedRyTraceTests

open QuantumBlockEncoding StoredGivens StoredSelectedRyTrace

/-- Computable inspection keeps both the physical wires and exact coefficient. -/
def view {n : Nat} : SelectedRyTrace.Gate n → Nat × Nat × Nat × Rat
  | .ry target coefficient => (0, target.val, 0, coefficient)
  | .cx control target _ => (1, control.val, target.val, 0)

/-- Native finite replay is a test command, not an axiom in a symbolic theorem. -/
def assertEqual [BEq α] [Repr α] (actual expected : α) : IO Unit := do
  unless actual == expected do
    throw (IO.userError s!"stored trace regression: got {repr actual}, expected {repr expected}")

/-- Zero controls: exactly one rotation, even with a negative nonintegral scalar. -/
example : ((compile 0 (#v[] : Vector (Fin 5) 0) 4 (by decide)
    (#v[-7 / 3] : Coefficients 0)).value.map view) = [(0, 4, 0, -7 / 3)] := rfl

example : (compile 0 (#v[] : Vector (Fin 5) 0) 4 (by decide) (#v[0] : Coefficients 0)).cost .read = 1 ∧
    (compile 0 (#v[] : Vector (Fin 5) 0) 4 (by decide) (#v[0] : Coefficients 0)).cost .write = 1 ∧
    (compile 0 (#v[] : Vector (Fin 5) 0) 4 (by decide) (#v[0] : Coefficients 0)).cost .emit = 1 := by
  decide

/- All-zero input must not prune either rotation or either CNOT. -/
#eval assertEqual ((compile 1 (#v[3] : Vector (Fin 4) 1) 1 (by decide)
    (#v[0, 0] : Coefficients 1)).value.map view)
      [(0, 1, 0, 0), (1, 3, 1, 0), (0, 1, 0, 0), (1, 3, 1, 0)]

#eval assertEqual (split (q := 1) (#v[1, 2, 3, 4] : Coefficients 2)).value
    ((#v[2, 3], #v[-1, -1]) : Coefficients 1 × Coefficients 1)

example : (split (q := 1) (#v[1, 2, 3, 4] : Coefficients 2)).cost .field = 8 ∧
    (split (q := 1) (#v[1, 2, 3, 4] : Coefficients 2)).cost .read = 20 ∧
    (split (q := 1) (#v[1, 2, 3, 4] : Coefficients 2)).cost .write = 12 := by decide

/- The first control is the high half, not an accidentally reversed bit order. -/
#eval assertEqual (encode 3 (#v[1, 0, 1] : Vector (Fin 2) 3)).value.val 5

#eval assertEqual (selectedCoefficients (#v[1, 0] : Vector (Fin 2) 2)).value
    (#v[0, 0, 1, 0] : Coefficients 2)

/- Non-prefix, nonmonotone physical control layout; target is an interior wire. -/
#eval assertEqual ((selected (#v[3, 0] : Vector (Fin 4) 2) 2 (by decide)
    (#v[1, 0] : Vector (Fin 2) 2)).value.map view)
    [(0, 2, 0, 1 / 4), (1, 0, 2, 0), (0, 2, 0, 1 / 4), (1, 0, 2, 0),
      (1, 3, 2, 0), (0, 2, 0, -1 / 4), (1, 0, 2, 0),
      (0, 2, 0, -1 / 4), (1, 0, 2, 0), (1, 3, 2, 0)]

/-- Independent finite check of the actual ledger, including encoding and copying. -/
example : StoredRectangularGivens.total
    (selected (#v[3, 0] : Vector (Fin 4) 2) 2 (by decide) (#v[1, 0] : Vector (Fin 2) 2)).cost =
      173 := by decide

example : StoredRectangularGivens.total
    (selected (#v[] : Vector (Fin 1) 0) 0 (by decide) (#v[] : Vector (Fin 2) 0)).cost = 8 := by
  decide

example : (StoredSelectedRyTrace.append ([] : List Nat) [8, 9]).value = [8, 9] ∧
    (StoredSelectedRyTrace.append ([] : List Nat) [8, 9]).cost .read = 1 ∧
    (StoredSelectedRyTrace.append ([] : List Nat) [8, 9]).cost .write = 0 := by decide

example : (StoredSelectedRyTrace.append [1, 2, 3] [8, 9]).value = [1, 2, 3, 8, 9] ∧
    (StoredSelectedRyTrace.append [1, 2, 3] [8, 9]).cost .read = 4 ∧
    (StoredSelectedRyTrace.append [1, 2, 3] [8, 9]).cost .write = 3 := by decide

/-- No additional wire-injectivity assumption is smuggled into exact refinement. -/
example (xs : Coefficients 2) :
    (compile 2 (#v[3, 3] : Vector (Fin 4) 2) 1 (by decide) xs).value =
      SelectedRyTrace.compile 2 (fun _ : Fin 2 => (3 : Fin 4)) 1 (by decide) (denote xs) := by
  have wires_eq : (fun i : Fin 2 => (#v[3, 3] : Vector (Fin 4) 2)[i.val]) =
      (fun _ : Fin 2 => (3 : Fin 4)) := by
    funext i
    fin_cases i <;> rfl
  simpa only [wires_eq] using compile_value (#v[3, 3] : Vector (Fin 4) 2) 1 (by decide) xs

example {qubits q : Nat} (wires : Vector (Fin qubits) q) (target : Fin qubits)
    (distinct : ∀ i : Fin q, wires[i.val] ≠ target) (xs : Coefficients q) :
    (compile q wires target distinct xs).cost .emit =
      (compile q wires target distinct xs).value.length := compile_emit _ _ _ _

example {qubits q : Nat} (wires : Vector (Fin qubits) q) (target : Fin qubits)
    (distinct : ∀ i : Fin q, wires[i.val] ≠ target) (chosen : Vector (Fin 2) q) (angle : ExactAngle) :
    evalPrimitiveCircuit (SelectedRyTrace.instantiate angle (selected wires target distinct chosen).value) =
      evalPrimitiveCircuit (compileSelectedRy (fun i => wires[i.val]) target distinct
        (denoteBits chosen) angle) := selected_refines _ _ _ _ _

example {qubits q : Nat} (wires : Vector (Fin qubits) q) (target : Fin qubits)
    (distinct : ∀ i : Fin q, wires[i.val] ≠ target) (chosen : Vector (Fin 2) q) :
    StoredRectangularGivens.total (selected wires target distinct chosen).cost ≤
      (16 * q + 12) * 2 ^ q + 5 * q ^ 2 + 3 * q := selected_total_cost_le _ _ _ _

#print axioms StoredSelectedRyTrace.compile_value
#print axioms StoredSelectedRyTrace.compile_cost
#print axioms StoredSelectedRyTrace.traceCost_fields
#print axioms StoredSelectedRyTrace.compile_total_cost_le
#print axioms StoredSelectedRyTrace.encode_index_operations
#print axioms StoredSelectedRyTrace.selected_value
#print axioms StoredSelectedRyTrace.selected_refines
#print axioms StoredSelectedRyTrace.selected_field_tag_split
#print axioms StoredSelectedRyTrace.selected_emit
#print axioms StoredSelectedRyTrace.selected_total_cost_le

end StoredSelectedRyTraceTests
