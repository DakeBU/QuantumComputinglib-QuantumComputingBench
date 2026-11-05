import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.UnitaryGroup
import QuantumBlockEncoding.BlockEncodingClassics
import QuantumBlockEncoding.CircuitSemantics
import QuantumBlockEncoding.StatePreparation

/-!
# Concrete finite matrix semantics

This module is the narrow bridge between ABEIS's lightweight finite matrices
and Mathlib matrix-vector action.  It also names the equivalence between the
flattened signal-system indexing used by circuit semantics and an explicit
product-register view.

The definitions here do not certify an arbitrary candidate as unitary.  They
only replace repeatedly reconstructed representation steps with compiled
lemmas.
-/

namespace QuantumBlockEncoding
namespace ConcreteSemantics

/-- A Mathlib finite matrix, definitionally compatible with ABEIS `Matrix`. -/
abbrev FiniteMatrix (rows cols : Nat) (α : Type u) :=
  _root_.Matrix (Fin rows) (Fin cols) α

/-- A finite column vector. -/
abbrev StateVector (dimension : Nat) (α : Type u) :=
  Fin dimension -> α

/-- A computational-basis ket in the concrete finite backend. -/
def basisKet (dimension : Nat) {α : Type u} [Zero α] [One α]
    (index : Fin dimension) : StateVector dimension α :=
  Pi.single index 1

/-- A computational-basis ket is exactly a Kronecker delta at its named index.
Keeping this lemma in the concrete backend avoids exposing `Pi.single` inside
fixed-width circuit proofs. -/
@[simp] theorem basisKet_apply {dimension : Nat} {α : Type u}
    [Zero α] [One α] (index row : Fin dimension) :
    basisKet dimension (α := α) index row =
      if index = row then 1 else 0 := by
  by_cases hit : index = row
  · subst row
    simp [basisKet]
  · simp [basisKet, hit]

/-- The all-zero computational-basis ket for an `n`-qubit register. -/
def zeroKet (qubits : Nat) {α : Type u} [Zero α] [One α] :
    StateVector (gridSize qubits) α :=
  basisKet (gridSize qubits) (zeroBasisIndex qubits)

/-- Matrix-vector action using Mathlib's finite sum semantics. -/
def applyVec {rows cols : Nat} {α : Type u} [NonUnitalNonAssocSemiring α]
    (operator : FiniteMatrix rows cols α) (state : StateVector cols α) :
    StateVector rows α :=
  operator.mulVec state

/--
A finite complex gate whose unitarity is the standard Mathlib unitary-group
predicate rather than an unconstrained proposition.
-/
structure ComplexUnitaryGate (qubits : Nat) where
  matrix : FiniteMatrix (gridSize qubits) (gridSize qubits) ℂ
  unitary :
    matrix ∈ _root_.Matrix.unitaryGroup (Fin (gridSize qubits)) ℂ

/-- Acting on a basis ket selects the corresponding matrix column. -/
@[simp] theorem applyVec_basisKet {rows cols : Nat} {α : Type u}
    [NonAssocSemiring α] (operator : FiniteMatrix rows cols α)
    (index : Fin cols) :
    applyVec operator (basisKet cols index) = operator.col index := by
  exact _root_.Matrix.mulVec_single_one operator index

/-- Acting on a two-term sparse superposition needs only the two named matrix
columns.  Keeping this linearity fact in the concrete backend prevents every
finite state-preparation witness from rebuilding a large `mulVec` proof term. -/
theorem applyVec_twoBasisSuperposition {rows cols : Nat}
    (operator : FiniteMatrix rows cols ℂ) (a b : ℂ)
    (left right : Fin cols) :
    applyVec operator
        (a • basisKet cols left + b • basisKet cols right) =
      a • operator.col left + b • operator.col right := by
  unfold applyVec basisKet
  rw [_root_.Matrix.mulVec_add, _root_.Matrix.mulVec_smul,
    _root_.Matrix.mulVec_smul, _root_.Matrix.mulVec_single_one,
    _root_.Matrix.mulVec_single_one]

/-- Coordinate form of `applyVec_twoBasisSuperposition`.  Paper-route proofs
use this compiled scalar interface so the kernel never has to rebuild a whole
vector rewrite just to read one output amplitude. -/
theorem applyVec_twoBasisSuperposition_apply {rows cols : Nat}
    (operator : FiniteMatrix rows cols ℂ) (a b : ℂ)
    (left right : Fin cols) (row : Fin rows) :
    applyVec operator
        (a • basisKet cols left + b • basisKet cols right) row =
      a * operator row left + b * operator row right := by
  have h := congrFun (applyVec_twoBasisSuperposition operator a b left right) row
  simpa using h

/-- Acting on the all-zero ket selects column zero. -/
@[simp] theorem applyVec_zeroKet {α : Type u} [NonAssocSemiring α]
    {qubits : Nat}
    (operator : FiniteMatrix (gridSize qubits) (gridSize qubits) α) :
    applyVec operator (zeroKet qubits) =
      operator.col (zeroBasisIndex qubits) := by
  exact applyVec_basisKet operator (zeroBasisIndex qubits)

/--
The ABEIS first-column contract is exactly the state-action equation
`U |0^n> = |psi>` in the concrete finite matrix backend.
-/
theorem firstColumnMatches_iff_applyVec_zeroKet
    {α : Type u} [NonAssocSemiring α] {qubits : Nat}
    (operator : FiniteMatrix (gridSize qubits) (gridSize qubits) α)
    (target : StatePreparationTarget α qubits) :
    FirstColumnMatches operator target ↔
      applyVec operator (zeroKet qubits) = target.amplitudes := by
  constructor
  · intro firstColumn
    rw [applyVec_zeroKet]
    exact funext firstColumn
  · intro action row
    rw [applyVec_zeroKet] at action
    exact congrFun action row

/--
Concrete state-preparation evidence.  This is an optional final semantic layer:
existing symbolic and rational candidates do not need to use it, but a complex
candidate cannot enter this record without standard unitarity and state action.
-/
structure ComplexStatePreparationCertificate (qubits : Nat) where
  target : StatePreparationTarget ℂ qubits
  gate : ComplexUnitaryGate qubits
  normalizationProof : target.normalization
  preparationProof :
    applyVec gate.matrix (zeroKet qubits) = target.amplitudes

namespace ComplexStatePreparationCertificate

/-- Repackage concrete semantics in the existing generic candidate interface. -/
def candidate (certificate : ComplexStatePreparationCertificate qubits)
    (circuit : Circuit) (schedule : LayeredCircuit) (resource : Resource)
    (auxiliaryQubits : Nat := 0) :
    StatePreparationCandidate ℂ qubits where
  target := certificate.target
  unitary := certificate.gate.matrix
  circuit := circuit
  schedule := schedule
  resource := resource
  auxiliaryQubits := auxiliaryQubits
  isUnitary :=
    certificate.gate.matrix ∈
      _root_.Matrix.unitaryGroup (Fin (gridSize qubits)) ℂ

/--
Promote a concrete certificate to the existing verified wrapper.  The generic
`isUnitary` field is instantiated by, rather than substituted for, the
Mathlib unitary-group predicate.
-/
def verified (certificate : ComplexStatePreparationCertificate qubits)
    (circuit : Circuit) (schedule : LayeredCircuit) (resource : Resource)
    (auxiliaryQubits : Nat := 0) :
    VerifiedStatePreparation ℂ qubits where
  candidate :=
    certificate.candidate circuit schedule resource auxiliaryQubits
  normalizationProof := certificate.normalizationProof
  unitaryProof := certificate.gate.unitary
  preparationProof :=
    (firstColumnMatches_iff_applyVec_zeroKet
      certificate.gate.matrix certificate.target).mpr
        certificate.preparationProof

theorem preparesVector (certificate : ComplexStatePreparationCertificate qubits) :
    applyVec certificate.gate.matrix (zeroKet qubits) =
      certificate.target.amplitudes :=
  certificate.preparationProof

end ComplexStatePreparationCertificate

/-- A matrix indexed by an explicit signal-register/system-register product. -/
abbrev ProductRegisterMatrix (signalDim rows cols : Nat) (α : Type u) :=
  (Fin signalDim × Fin rows) -> (Fin signalDim × Fin cols) -> α

/--
View a flattened signal-system matrix through explicit product-register
indices.  The signal register is high-order and the system register low-order.
-/
def flatToProductRegister {signalDim rows cols : Nat} {α : Type u}
    (operator : Matrix (signalDim * rows) (signalDim * cols) α) :
    ProductRegisterMatrix signalDim rows cols α :=
  fun row col =>
    operator
      ⟨signalSystemBlockRowIndex rows row.1.val row.2.val,
        signalSystemBlockRowIndex_lt row.1 row.2⟩
      ⟨signalSystemBlockColIndex cols col.1.val col.2.val,
        signalSystemBlockColIndex_lt col.1 col.2⟩

/-- Project one signal branch from an explicit product-register matrix. -/
def productRegisterBlockProjection {signalDim rows cols : Nat} {α : Type u}
    (operator : ProductRegisterMatrix signalDim rows cols α)
    (signalIndex : Fin signalDim) : Matrix rows cols α :=
  fun row col => operator (signalIndex, row) (signalIndex, col)

/--
Product-register projection after viewing a flat matrix is definitionally the
existing ABEIS flattened block projection.
-/
theorem productRegisterBlockProjection_flatToProductRegister
    {signalDim rows cols : Nat} {α : Type u} [OfNat α 0]
    (operator : Matrix (signalDim * rows) (signalDim * cols) α)
    (signalIndex : Fin signalDim) :
    productRegisterBlockProjection
        (flatToProductRegister operator) signalIndex =
      signalSystemBlockProjection signalDim rows cols operator signalIndex := by
  rfl

/-- The classic product index and circuit-semantics row index have the same value. -/
theorem productIndex_val_eq_signalSystemBlockRowIndex
    {signalDim systemDim : Nat}
    (signalIndex : Fin signalDim) (systemIndex : Fin systemDim) :
    (BlockEncodingClassics.productIndex signalIndex systemIndex).val =
      signalSystemBlockRowIndex
        systemDim signalIndex.val systemIndex.val := by
  rfl

/--
The classic rational clean block and the generic circuit-semantics projection
are the same pointwise matrix under the shared register order.
-/
theorem signalSystemBlockProjection_eq_cleanBlockProduct
    {signalDim systemDim : Nat}
    (operator : Matrix (signalDim * systemDim) (signalDim * systemDim) Rat)
    (signalIndex : Fin signalDim) :
    Matrix.PointwiseEq
      (signalSystemBlockProjection
        signalDim systemDim systemDim operator signalIndex)
      (BlockEncodingClassics.cleanBlockProduct signalIndex operator) := by
  intro row col
  rfl

/--
The clean output amplitude obtained by applying `operator` to a clean
signal-system basis input.  Naming this quantity makes the two common
block-encoding proof styles explicit: prove the projected matrix block, or
prove the clean branch of the action on every basis input.
-/
def cleanBasisActionAmplitude {signalDim systemDim : Nat} {α : Type u}
    [NonAssocSemiring α]
    (operator : FiniteMatrix (signalDim * systemDim) (signalDim * systemDim) α)
    (signalIndex : Fin signalDim) (output input : Fin systemDim) : α :=
  applyVec operator
    (basisKet (signalDim * systemDim)
      (BlockEncodingClassics.productIndex signalIndex input))
    (BlockEncodingClassics.productIndex signalIndex output)

/-- Acting on a clean basis input and reading a clean output is one projected-block entry. -/
theorem cleanBasisActionAmplitude_eq_signalSystemBlockProjection
    {signalDim systemDim : Nat} {α : Type u} [NonAssocSemiring α]
    (operator : FiniteMatrix (signalDim * systemDim) (signalDim * systemDim) α)
    (signalIndex : Fin signalDim) (output input : Fin systemDim) :
    cleanBasisActionAmplitude operator signalIndex output input =
      signalSystemBlockProjection signalDim systemDim systemDim
        operator signalIndex output input := by
  unfold cleanBasisActionAmplitude
  rw [applyVec_basisKet]
  unfold signalSystemBlockProjection
  congr 1

/--
Finite-dimensional bridge between the projected-block definition and the
clean-branch action proof.  Linearity then extends the basis statement to an
arbitrary system state; any normalized orthogonal failure branch is additional
unitarity evidence, not a different block-encoding contract.
-/
theorem pointwiseProjection_iff_cleanBasisAction
    {signalDim systemDim : Nat} {α : Type u} [NonAssocSemiring α]
    (operator : FiniteMatrix (signalDim * systemDim) (signalDim * systemDim) α)
    (signalIndex : Fin signalDim) (target : Matrix systemDim systemDim α) :
    Matrix.PointwiseEq
        (signalSystemBlockProjection signalDim systemDim systemDim
          operator signalIndex)
        target ↔
      ∀ output input,
        cleanBasisActionAmplitude operator signalIndex output input =
          target output input := by
  constructor
  · intro projected output input
    rw [cleanBasisActionAmplitude_eq_signalSystemBlockProjection]
    exact projected output input
  · intro action output input
    rw [← cleanBasisActionAmplitude_eq_signalSystemBlockProjection]
    exact action output input

end ConcreteSemantics
end QuantumBlockEncoding
