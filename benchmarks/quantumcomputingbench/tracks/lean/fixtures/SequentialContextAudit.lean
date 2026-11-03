import QuantumBlockEncoding.SequentialBondPreparation

universe u v
open scoped BigOperators
namespace QuantumComputingBench.SequentialContextAudit
open scoped Kronecker
open QuantumBlockEncoding.RealAmplitudePreparation
variable {B : Type u} [Fintype B] [DecidableEq B]
abbrev Core (B : Type u) := _root_.Matrix (Fin 2 × B) B ℂ
abbrev Stage (B : Type u) := _root_.Matrix (Fin 2 × B) (Fin 2 × B) ℂ
abbrev BondState (n : Nat) (B : Type u) := QuantumBlockEncoding.PrimitiveBasis n × B → ℂ

def freshZero {n : Nat} (v : BondState n B) : QuantumBlockEncoding.PrimitiveBasis n × (Fin 2 × B) → ℂ := fun x => if x.2.1 = 0 then v (x.1, x.2.2) else 0

noncomputable def liftStage (n : Nat) (U : Stage B) : _root_.Matrix (QuantumBlockEncoding.PrimitiveBasis n × (Fin 2 × B)) (QuantumBlockEncoding.PrimitiveBasis n × (Fin 2 × B)) ℂ := (1 : _root_.Matrix (QuantumBlockEncoding.PrimitiveBasis n) (QuantumBlockEncoding.PrimitiveBasis n) ℂ) ⊗ₖ U

noncomputable def step {n : Nat} (U : Stage B) (v : BondState n B) : BondState (n + 1) B := fun x => ((liftStage n U).mulVec (freshZero v)) (Fin.init x.1, (x.1 (Fin.last n), x.2))

noncomputable def run (U : Nat → Stage B) (boundary : B → ℂ) : (n : Nat) → BondState n B | 0 => fun x => boundary x.2 | n + 1 => step (U n) (run U boundary n)

def coreSlice (K : Core B) (bit : Fin 2) : _root_.Matrix B B ℂ := fun b a => K (bit, b) a

noncomputable def transfer (K : Nat → Core B) : (n : Nat) → QuantumBlockEncoding.PrimitiveBasis n → _root_.Matrix B B ℂ | 0, _ => 1 | n + 1, x => coreSlice (K n) (x (Fin.last n)) * transfer K n (Fin.init x)

def basisBoundary (initial : B) : B → ℂ := fun b => if b = initial then 1 else 0

noncomputable def amplitudeMass {I : Type v} [Fintype I] (v : I → ℂ) : ℂ := ∑ i, star (v i) * v i

end QuantumComputingBench.SequentialContextAudit

namespace QuantumComputingBench.SequentialContextAudit
abbrev reconstructedPrimitiveBasis (qubits : Nat) := Fin qubits → Fin 2
theorem basisCarrier : ∀ n : ℕ, reconstructedPrimitiveBasis n = QuantumBlockEncoding.PrimitiveBasis n := by intro n; rfl
variable {B : Type u} [Fintype B] [DecidableEq B]
theorem coreCarrier : Core B = QuantumBlockEncoding.SequentialBondPreparation.Core B := rfl
theorem stageCarrier : Stage B = QuantumBlockEncoding.SequentialBondPreparation.Stage B := rfl
theorem stateCarrier (n : ℕ) : BondState n B = QuantumBlockEncoding.SequentialBondPreparation.BondState n B := rfl
theorem freshEqual {n : ℕ} (z : BondState n B) : freshZero z = QuantumBlockEncoding.SequentialBondPreparation.freshZero z := rfl
theorem liftEqual (n : ℕ) (U : Stage B) : liftStage n U = QuantumBlockEncoding.SequentialBondPreparation.liftStage n U := rfl
theorem stepEqual {n : ℕ} (U : Stage B) (z : BondState n B) : step U z = QuantumBlockEncoding.SequentialBondPreparation.step U z := rfl
theorem sliceEqual (K : Core B) (bit : Fin 2) : coreSlice K bit = QuantumBlockEncoding.SequentialBondPreparation.coreSlice K bit := rfl
theorem runEqual (U : ℕ → Stage B) (boundary : B → ℂ) : ∀ n : ℕ, run U boundary n = QuantumBlockEncoding.SequentialBondPreparation.run U boundary n := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
    change QuantumBlockEncoding.SequentialBondPreparation.step (U n) (run U boundary n) = QuantumBlockEncoding.SequentialBondPreparation.step (U n) (QuantumBlockEncoding.SequentialBondPreparation.run U boundary n)
    rw [ih]
theorem transferEqual (K : ℕ → Core B) : ∀ (n : ℕ) (x : QuantumBlockEncoding.PrimitiveBasis n), transfer K n x = QuantumBlockEncoding.SequentialBondPreparation.transfer K n x := by
  intro n
  induction n with
  | zero => intro x; rfl
  | succ n ih =>
    intro x
    change QuantumBlockEncoding.SequentialBondPreparation.coreSlice (K n) (x (Fin.last n)) * transfer K n (Fin.init x) = QuantumBlockEncoding.SequentialBondPreparation.coreSlice (K n) (x (Fin.last n)) * QuantumBlockEncoding.SequentialBondPreparation.transfer K n (Fin.init x)
    rw [ih]
theorem boundaryEqual (initial : B) : basisBoundary initial = QuantumBlockEncoding.SequentialBondPreparation.basisBoundary initial := rfl
theorem massEqual {I : Type v} [Fintype I] (z : I → ℂ) : amplitudeMass z = QuantumBlockEncoding.SequentialBondPreparation.amplitudeMass z := rfl
theorem normFormula : ∀ z : ℂ, Complex.normSq z = z.re * z.re + z.im * z.im := by intro z; rfl
#print axioms runEqual
#print axioms transferEqual
#print axioms massEqual
end QuantumComputingBench.SequentialContextAudit
