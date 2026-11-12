import QuantumBlockEncoding.PrimitiveSemantics

/-! Isolated proof-only candidate: the existing complete module is reproduced
with kernel `decide` in place of native finite evaluation. Exact declarations
and bodies are unchanged; never import alongside the production module.
Not production admission, source review, or a circuit/resource certificate. -/

/-!
# Little-endian primitive basis indexing

The primitive circuit semantics names qubits by `Fin q`.  This file fixes the
conversion to flat matrix indices: wire zero is the least-significant bit.
Keeping this equivalence explicit prevents executable backends from silently
choosing a different register order.
-/

namespace QuantumBlockEncoding

/-- Convert named primitive bits to a flat little-endian matrix index. -/
def primitiveBasisLEEquiv : (q : Nat) -> PrimitiveBasis q ≃ Fin (gridSize q)
  | 0 =>
      { toFun := fun _ => ⟨0, by decide⟩
        invFun := fun _ => Fin.elim0
        left_inv := fun bits => funext fun wire => Fin.elim0 wire
        right_inv := fun index => by fin_cases index; rfl }
  | q + 1 =>
      (Fin.consEquiv (fun _ : Fin (q + 1) => Fin 2)).symm
        |>.trans (Equiv.prodCongr (Equiv.refl (Fin 2)) (primitiveBasisLEEquiv q))
        |>.trans (Equiv.prodComm (Fin 2) (Fin (gridSize q)))
        |>.trans finProdFinEquiv
        |>.trans (finCongr (by simp [gridSize, pow_succ]))

@[simp] theorem primitiveBasisLEEquiv_zero_apply (bits : PrimitiveBasis 0) :
    (primitiveBasisLEEquiv 0 bits).val = 0 := by
  rfl

/-- The recursive equation makes the little-endian convention inspectable. -/
theorem primitiveBasisLEEquiv_succ_value (q : Nat)
    (bits : PrimitiveBasis (q + 1)) :
    (primitiveBasisLEEquiv (q + 1) bits).val =
      (bits 0).val + 2 *
        (primitiveBasisLEEquiv q (fun wire => bits wire.succ)).val := by
  rfl

/-- Six-wire expansion used by the fixed Robin executable benchmark. -/
theorem primitiveBasisLEEquiv_six_value (bits : PrimitiveBasis 6) :
    (primitiveBasisLEEquiv 6 bits).val =
      (bits 0).val + 2 * (bits 1).val + 4 * (bits 2).val +
      8 * (bits 3).val + 16 * (bits 4).val + 32 * (bits 5).val := by
  decide +revert

/-- Explicit inverse used by finite two-wire state-preparation proofs. -/
def primitiveBits2LE (index : Fin 4) : PrimitiveBasis 2
  | 0 => ⟨index.val % 2, by omega⟩
  | _ => ⟨(index.val / 2) % 2, by omega⟩

@[simp] theorem primitiveBasisLEEquiv_two_symm (index : Fin 4) :
    (primitiveBasisLEEquiv 2).symm index = primitiveBits2LE index := by
  fin_cases index <;> decide

/-- Fixed-width coordinate reductions whose domain exactly matches the
`gridSize`-indexed finite matrix backend. -/
@[simp] theorem primitiveBasisLEEquiv_two_symm_wire_zero
    (index : Fin (gridSize 2)) :
    ((primitiveBasisLEEquiv 2).symm index) (0 : Fin 2) =
      ⟨index.val % 2, by omega⟩ := by
  decide +revert

@[simp] theorem primitiveBasisLEEquiv_two_symm_wire_one
    (index : Fin (gridSize 2)) :
    ((primitiveBasisLEEquiv 2).symm index) (1 : Fin 2) =
      ⟨(index.val / 2) % 2, by omega⟩ := by
  decide +revert

/-- Concrete inverse images used after `fin_cases`; these avoid relying on type
normalization between `Fin (gridSize 2)` and `Fin 4`. -/
@[simp] theorem primitiveBasisLEEquiv_two_symm_0 :
    (primitiveBasisLEEquiv 2).symm
        (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 2)) =
      primitiveBits2LE (0 : Fin 4) := by decide
@[simp] theorem primitiveBasisLEEquiv_two_symm_1 :
    (primitiveBasisLEEquiv 2).symm
        (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 2)) =
      primitiveBits2LE (1 : Fin 4) := by decide
@[simp] theorem primitiveBasisLEEquiv_two_symm_2 :
    (primitiveBasisLEEquiv 2).symm
        (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 2)) =
      primitiveBits2LE (2 : Fin 4) := by decide
@[simp] theorem primitiveBasisLEEquiv_two_symm_3 :
    (primitiveBasisLEEquiv 2).symm
        (⟨3, by norm_num [gridSize]⟩ : Fin (gridSize 2)) =
      primitiveBits2LE (3 : Fin 4) := by decide

/-- Encode the non-target wire of a two-qubit little-endian basis state. -/
def primitiveBits2LEWithout (target : Fin 2) (index : Fin 4) : Nat :=
  match target.val with
  | 0 => index.val / 2
  | _ => index.val % 2

/-- Same context code, but with the unreduced `gridSize` domain used by the
concrete matrix semantics. -/
def primitiveBits2LEGridWithout
    (target : Fin 2) (index : Fin (gridSize 2)) : Nat :=
  match target.val with
  | 0 => index.val / 2
  | _ => index.val % 2

@[simp] theorem splitPrimitiveWire_primitiveBits2LE_context_eq
    (target : Fin 2) (left right : Fin 4) :
    (splitPrimitiveWire target (primitiveBits2LE left)).2 =
        (splitPrimitiveWire target (primitiveBits2LE right)).2 ↔
      primitiveBits2LEWithout target left =
        primitiveBits2LEWithout target right := by
  decide +revert

@[simp] theorem splitPrimitiveWire_primitiveBasisLEEquiv_two_symm_context_eq
    (target : Fin 2) (left right : Fin (gridSize 2)) :
    (splitPrimitiveWire target ((primitiveBasisLEEquiv 2).symm left)).2 =
        (splitPrimitiveWire target ((primitiveBasisLEEquiv 2).symm right)).2 ↔
      primitiveBits2LEGridWithout target left =
        primitiveBits2LEGridWithout target right := by
  decide +revert

/-- Explicit inverse used by finite three-wire compiler proofs. -/
def primitiveBits3LE (index : Fin 8) : PrimitiveBasis 3
  | 0 => ⟨index.val % 2, by omega⟩
  | 1 => ⟨(index.val / 2) % 2, by omega⟩
  | _ => ⟨(index.val / 4) % 2, by omega⟩

@[simp] theorem primitiveBasisLEEquiv_three_symm (index : Fin 8) :
    (primitiveBasisLEEquiv 3).symm index = primitiveBits3LE index := by
  fin_cases index <;> decide

@[simp] theorem primitiveBasisLEEquiv_three_symm_wire_zero
    (index : Fin (gridSize 3)) :
    ((primitiveBasisLEEquiv 3).symm index) (0 : Fin 3) =
      ⟨index.val % 2, by omega⟩ := by
  decide +revert

@[simp] theorem primitiveBasisLEEquiv_three_symm_wire_one
    (index : Fin (gridSize 3)) :
    ((primitiveBasisLEEquiv 3).symm index) (1 : Fin 3) =
      ⟨(index.val / 2) % 2, by omega⟩ := by
  decide +revert

@[simp] theorem primitiveBasisLEEquiv_three_symm_wire_two
    (index : Fin (gridSize 3)) :
    ((primitiveBasisLEEquiv 3).symm index) (2 : Fin 3) =
      ⟨(index.val / 4) % 2, by omega⟩ := by
  decide +revert

/-- Concrete inverse images for all eight three-qubit basis states. -/
@[simp] theorem primitiveBasisLEEquiv_three_symm_0 :
    (primitiveBasisLEEquiv 3).symm
        (⟨0, by norm_num [gridSize]⟩ : Fin (gridSize 3)) =
      primitiveBits3LE (0 : Fin 8) := by decide
@[simp] theorem primitiveBasisLEEquiv_three_symm_1 :
    (primitiveBasisLEEquiv 3).symm
        (⟨1, by norm_num [gridSize]⟩ : Fin (gridSize 3)) =
      primitiveBits3LE (1 : Fin 8) := by decide
@[simp] theorem primitiveBasisLEEquiv_three_symm_2 :
    (primitiveBasisLEEquiv 3).symm
        (⟨2, by norm_num [gridSize]⟩ : Fin (gridSize 3)) =
      primitiveBits3LE (2 : Fin 8) := by decide
@[simp] theorem primitiveBasisLEEquiv_three_symm_3 :
    (primitiveBasisLEEquiv 3).symm
        (⟨3, by norm_num [gridSize]⟩ : Fin (gridSize 3)) =
      primitiveBits3LE (3 : Fin 8) := by decide
@[simp] theorem primitiveBasisLEEquiv_three_symm_4 :
    (primitiveBasisLEEquiv 3).symm
        (⟨4, by norm_num [gridSize]⟩ : Fin (gridSize 3)) =
      primitiveBits3LE (4 : Fin 8) := by decide
@[simp] theorem primitiveBasisLEEquiv_three_symm_5 :
    (primitiveBasisLEEquiv 3).symm
        (⟨5, by norm_num [gridSize]⟩ : Fin (gridSize 3)) =
      primitiveBits3LE (5 : Fin 8) := by decide
@[simp] theorem primitiveBasisLEEquiv_three_symm_6 :
    (primitiveBasisLEEquiv 3).symm
        (⟨6, by norm_num [gridSize]⟩ : Fin (gridSize 3)) =
      primitiveBits3LE (6 : Fin 8) := by decide
@[simp] theorem primitiveBasisLEEquiv_three_symm_7 :
    (primitiveBasisLEEquiv 3).symm
        (⟨7, by norm_num [gridSize]⟩ : Fin (gridSize 3)) =
      primitiveBits3LE (7 : Fin 8) := by decide

def primitiveBits3LEWithout (target : Fin 3) (index : Fin 8) : Nat :=
  match target.val with
  | 0 => index.val / 2
  | 1 => index.val % 2 + 2 * (index.val / 4)
  | _ => index.val % 4

/-- Grid-sized companion of `primitiveBits3LEWithout`, used before the type
normalizer has turned `Fin (gridSize 3)` into `Fin 8`. -/
def primitiveBits3LEGridWithout
    (target : Fin 3) (index : Fin (gridSize 3)) : Nat :=
  match target.val with
  | 0 => index.val / 2
  | 1 => index.val % 2 + 2 * (index.val / 4)
  | _ => index.val % 4

@[simp] theorem splitPrimitiveWire_primitiveBits3LE_context_eq
    (target : Fin 3) (left right : Fin 8) :
    (splitPrimitiveWire target (primitiveBits3LE left)).2 =
        (splitPrimitiveWire target (primitiveBits3LE right)).2 ↔
      primitiveBits3LEWithout target left =
        primitiveBits3LEWithout target right := by
  decide +revert

@[simp] theorem splitPrimitiveWire_primitiveBasisLEEquiv_three_symm_context_eq
    (target : Fin 3) (left right : Fin (gridSize 3)) :
    (splitPrimitiveWire target ((primitiveBasisLEEquiv 3).symm left)).2 =
        (splitPrimitiveWire target ((primitiveBasisLEEquiv 3).symm right)).2 ↔
      primitiveBits3LEGridWithout target left =
        primitiveBits3LEGridWithout target right := by
  decide +revert

end QuantumBlockEncoding


#check @QuantumBlockEncoding.primitiveBasisLEEquiv
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_zero_apply
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_zero_apply
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_succ_value
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_succ_value
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_six_value
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_six_value
#check @QuantumBlockEncoding.primitiveBits2LE
#print axioms QuantumBlockEncoding.primitiveBits2LE
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_wire_zero
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_wire_zero
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_wire_one
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_wire_one
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_0
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_0
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_1
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_1
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_2
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_2
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_3
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_two_symm_3
#check @QuantumBlockEncoding.primitiveBits2LEWithout
#print axioms QuantumBlockEncoding.primitiveBits2LEWithout
#check @QuantumBlockEncoding.primitiveBits2LEGridWithout
#print axioms QuantumBlockEncoding.primitiveBits2LEGridWithout
#check @QuantumBlockEncoding.splitPrimitiveWire_primitiveBits2LE_context_eq
#print axioms QuantumBlockEncoding.splitPrimitiveWire_primitiveBits2LE_context_eq
#check @QuantumBlockEncoding.splitPrimitiveWire_primitiveBasisLEEquiv_two_symm_context_eq
#print axioms QuantumBlockEncoding.splitPrimitiveWire_primitiveBasisLEEquiv_two_symm_context_eq
#check @QuantumBlockEncoding.primitiveBits3LE
#print axioms QuantumBlockEncoding.primitiveBits3LE
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_wire_zero
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_wire_zero
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_wire_one
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_wire_one
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_wire_two
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_wire_two
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_0
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_0
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_1
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_1
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_2
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_2
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_3
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_3
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_4
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_4
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_5
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_5
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_6
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_6
#check @QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_7
#print axioms QuantumBlockEncoding.primitiveBasisLEEquiv_three_symm_7
#check @QuantumBlockEncoding.primitiveBits3LEWithout
#print axioms QuantumBlockEncoding.primitiveBits3LEWithout
#check @QuantumBlockEncoding.primitiveBits3LEGridWithout
#print axioms QuantumBlockEncoding.primitiveBits3LEGridWithout
#check @QuantumBlockEncoding.splitPrimitiveWire_primitiveBits3LE_context_eq
#print axioms QuantumBlockEncoding.splitPrimitiveWire_primitiveBits3LE_context_eq
#check @QuantumBlockEncoding.splitPrimitiveWire_primitiveBasisLEEquiv_three_symm_context_eq
#print axioms QuantumBlockEncoding.splitPrimitiveWire_primitiveBasisLEEquiv_three_symm_context_eq
