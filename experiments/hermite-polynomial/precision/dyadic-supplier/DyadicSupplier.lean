import GlobalAssembly
import QuantumBlockEncoding.PrimitiveCircuitPerturbation
import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Algebra.Order.Floor.Semiring

/-! Actual literal dyadic RY rounding supplier. Statement seal v2.
The floor operation consumes exact real semantics and is NOT a numerical
finite-bit algorithm. The returned angles are integer / power-of-two rationals;
no instruction order, physical target or non-RY instruction is changed. -/
namespace QuantumBlockEncoding.DyadicSupplier
open PrimitiveCircuitPerturbation
open scoped Matrix.Norms.L2Operator

def dyadicRat (bits : ℕ) (numerator : ℤ) : ℚ :=
  (numerator : ℚ) / (2 : ℚ)^bits

noncomputable def numerator (bits : ℕ) (angle : ExactAngle) : ℤ :=
  Int.floor (angle.eval * (2 : ℝ)^bits)

noncomputable def roundAngle (bits : ℕ) (angle : ExactAngle) : ExactAngle :=
  .rational (dyadicRat bits (numerator bits angle))

theorem roundAngle_eval (bits : ℕ) (angle : ExactAngle) :
    (roundAngle bits angle).eval =
      (Int.floor (angle.eval * (2 : ℝ)^bits) : ℝ) / (2 : ℝ)^bits := by
  simp [roundAngle, ExactAngle.eval, dyadicRat, numerator]

theorem roundAngle_error (bits : ℕ) (angle : ExactAngle) :
    |angle.eval - (roundAngle bits angle).eval| ≤ 1 / (2 : ℝ)^bits := by
  rw [roundAngle_eval]
  have hd : (0 : ℝ) < 2^bits := by positivity
  have hlo := Int.floor_le (angle.eval * (2 : ℝ)^bits)
  have hhi := (Int.lt_floor_add_one (angle.eval * (2 : ℝ)^bits)).le
  have hnonneg : 0 ≤ angle.eval -
      (Int.floor (angle.eval * (2 : ℝ)^bits) : ℝ) / (2 : ℝ)^bits := by
    rw [sub_nonneg, div_le_iff₀ hd]
    exact hlo
  rw [abs_of_nonneg hnonneg]
  have identity : angle.eval - (Int.floor (angle.eval * (2 : ℝ)^bits) : ℝ) /
      (2 : ℝ)^bits = (angle.eval * (2 : ℝ)^bits -
        (Int.floor (angle.eval * (2 : ℝ)^bits) : ℝ)) / (2 : ℝ)^bits := by
    field_simp
  rw [identity, div_le_div_iff_of_pos_right hd]
  linarith

noncomputable def roundGate (bits : ℕ) : PrimitiveGate qubits → PrimitiveGate qubits
  | .ry target angle => .ry target (roundAngle bits angle)
  | .x target => .x target
  | .rz target angle => .rz target angle
  | .cx control target distinct => .cx control target distinct

noncomputable def roundCircuit (bits : ℕ) (circuit : PrimitiveCircuit qubits) :
    PrimitiveCircuit qubits := circuit.map (roundGate bits)

theorem roundGate_aligned (bits : ℕ) (gate : PrimitiveGate qubits) :
    GateAligned (1 / (2 : ℝ)^bits) gate (roundGate bits gate) := by
  cases gate with
  | ry target angle => exact .ry target angle _ (roundAngle_error bits angle)
  | x target => exact .unchanged _
  | rz target angle => exact .unchanged _
  | cx control target distinct => exact .unchanged _

theorem roundCircuit_aligned (bits : ℕ) (circuit : PrimitiveCircuit qubits) :
    Aligned (1 / (2 : ℝ)^bits) circuit (roundCircuit bits circuit) := by
  induction circuit with
  | nil => exact .nil
  | cons gate rest ih => exact .cons (roundGate_aligned bits gate) ih

theorem roundCircuit_length (bits : ℕ) (circuit : PrimitiveCircuit qubits) :
    (roundCircuit bits circuit).length = circuit.length := List.length_map _

theorem roundCircuit_resource (bits : ℕ) (circuit : PrimitiveCircuit qubits) :
    (roundCircuit bits circuit).resource = circuit.resource := by
  have one : ∀ (c : PrimitiveCircuit qubits) (a : ℕ),
      (c.map (roundGate bits)).foldl (fun t g => t + g.oneQubitCount) a =
        c.foldl (fun t g => t + g.oneQubitCount) a := by
    intro c
    induction c with
    | nil => intro a; rfl
    | cons g gs ih =>
        intro a
        cases g <;> simp only [List.map_cons, List.foldl_cons, roundGate,
          PrimitiveGate.oneQubitCount] <;> exact ih _
  have two : ∀ (c : PrimitiveCircuit qubits) (a : ℕ),
      (c.map (roundGate bits)).foldl (fun t g => t + g.twoQubitCount) a =
        c.foldl (fun t g => t + g.twoQubitCount) a := by
    intro c
    induction c with
    | nil => intro a; rfl
    | cons g gs ih =>
        intro a
        cases g <;> simp only [List.map_cons, List.foldl_cons, roundGate,
          PrimitiveGate.twoQubitCount] <;> exact ih _
  have wires : ∀ (c : PrimitiveCircuit qubits) (a : Fin qubits → ℕ),
      (c.map (roundGate bits)).foldl PrimitiveCircuit.nextWireDepth a =
        c.foldl PrimitiveCircuit.nextWireDepth a := by
    intro c
    induction c with
    | nil => intro a; rfl
    | cons g gs ih =>
        intro a
        simp only [List.map_cons, List.foldl_cons, ih]
        have ht := (roundGate_aligned bits g).touched_eq
        simp only [PrimitiveCircuit.nextWireDepth, ht]
  simp only [PrimitiveCircuit.resource, PrimitiveCircuit.oneQubitCount,
    PrimitiveCircuit.twoQubitCount, PrimitiveCircuit.depth, PrimitiveCircuit.wireDepths,
    roundCircuit, one, two, wires]

theorem roundCircuit_counts (bits : ℕ) (circuit : PrimitiveCircuit qubits) :
    (roundCircuit bits circuit).ryCount = circuit.ryCount ∧
    (roundCircuit bits circuit).cxCount = circuit.cxCount := by
  induction circuit with
  | nil => exact ⟨rfl, rfl⟩
  | cons g gs ih =>
      cases g <;> simpa [roundCircuit, roundGate, PrimitiveCircuit.ryCount,
        PrimitiveCircuit.cxCount] using ih

def errorCoefficient (k n : ℕ) : ℝ :=
  24 * ((n+1 : ℕ) : ℝ) * ((2*k+6 : ℕ) : ℝ)^3

noncomputable def bitsFor (k n : ℕ) (epsilon : ℝ) : ℕ :=
  Nat.clog 2 (max 1 (Nat.ceil (errorCoefficient k n / epsilon)))

noncomputable def compile (k n : ℕ) (L : ℝ) (hL : 0<L) (bits : ℕ) :
    PrimitiveCircuit ((n+1)+HermiteFiniteChain.bondQubits k) :=
  let exact := StagedGlobalAssembly.compile k n L hL
  roundCircuit bits exact.run.value

theorem compile_resource (k n : ℕ) (L : ℝ) (hL : 0<L) (bits : ℕ) :
    (compile k n L hL bits).resource =
      (StagedGlobalAssembly.compile k n L hL).run.value.resource :=
  roundCircuit_resource bits _

theorem compile_gateCount (k n : ℕ) (L : ℝ) (hL : 0<L) (bits : ℕ) :
    (compile k n L hL bits).gateCount ≤ 48*(n+1)*(2*k+6)^3 := by
  change (roundCircuit bits _).length ≤ _
  rw [roundCircuit_length]
  exact StagedGlobalAssembly.compile_gateCount_polynomial k n L hL

theorem compile_operator_error (k n : ℕ) (L : ℝ) (hL : 0<L) (bits : ℕ) :
    ‖evalPrimitiveCircuit (compile k n L hL bits) -
      evalPrimitiveCircuit (StagedGlobalAssembly.compile k n L hL).run.value‖ ≤
        errorCoefficient k n / (2 : ℝ)^bits := by
  have bound := aligned_eval_distance_le (by positivity)
    (roundCircuit_aligned bits (StagedGlobalAssembly.compile k n L hL).run.value)
  have count : ((StagedGlobalAssembly.compile k n L hL).run.value.length : ℝ) ≤
      48 * ((n+1 : ℕ) : ℝ) * ((2*k+6 : ℕ) : ℝ)^3 := by
    exact_mod_cast StagedGlobalAssembly.compile_gateCount_polynomial k n L hL
  apply bound.trans
  unfold errorCoefficient
  calc
    _ ≤ (48 * ((n+1 : ℕ) : ℝ) * ((2*k+6 : ℕ) : ℝ)^3) *
        (1/(2 : ℝ)^bits) / 2 := by gcongr
    _ = _ := by ring

theorem bitsFor_error (k n : ℕ) {epsilon : ℝ} (he : 0<epsilon) :
    errorCoefficient k n / (2 : ℝ)^(bitsFor k n epsilon) ≤ epsilon := by
  have hp : max 1 (Nat.ceil (errorCoefficient k n / epsilon)) ≤
      2^(bitsFor k n epsilon) := Nat.le_pow_clog (by norm_num) _
  have hc := Nat.le_ceil (errorCoefficient k n / epsilon)
  have hpow : (errorCoefficient k n / epsilon) ≤ (2 : ℝ)^(bitsFor k n epsilon) := by
    apply hc.trans
    exact_mod_cast (le_max_right 1 _).trans hp
  rw [div_le_iff₀ (by positivity)]
  have hh := (div_le_iff₀ he).mp hpow
  nlinarith

noncomputable def column {qubits : ℕ}
    (A : _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ) :
    EuclideanSpace ℂ (PrimitiveBasis qubits) :=
  WithLp.toLp 2 (fun z => A z (fun _ => 0))

noncomputable def target (k n : ℕ) (L : ℝ) :
    EuclideanSpace ℂ (PrimitiveBasis ((n+1)+HermiteFiniteChain.bondQubits k)) :=
  WithLp.toLp 2 (fun z =>
    if (fun i => z (Fin.natAdd (n+1) i)) = (fun _ => 0) then
      HermiteStatePreparation.normalizedAmplitude k (n+1) L
        (primitiveBasisLEEquiv (n+1) (fun i => z (Fin.castAdd _ i))) else 0)

theorem target_append (k n : ℕ) (L : ℝ) (x : PrimitiveBasis (n+1))
    (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)) :
    target k n L (Fin.append x b) =
      if b = (fun _ => 0) then HermiteStatePreparation.normalizedAmplitude k (n+1) L
        (primitiveBasisLEEquiv (n+1) x) else 0 := by
  simp [target]

theorem exact_column_target (k n : ℕ) (L : ℝ) (hL : 0<L) :
    column (evalPrimitiveCircuit (StagedGlobalAssembly.compile k n L hL).run.value) =
      target k n L := by
  ext z
  have h := StagedGlobalAssembly.compile_columns k n L hL
    (fun i => z (Fin.castAdd _ i)) (fun i => z (Fin.natAdd (n+1) i))
  rw [Fin.append_castAdd_natAdd] at h
  exact h

theorem column_error {qubits : ℕ}
    (A B : _root_.Matrix (PrimitiveBasis qubits) (PrimitiveBasis qubits) ℂ) :
    ‖column A - column B‖ ≤ ‖A-B‖ := by
  let zeroState : EuclideanSpace ℂ (PrimitiveBasis qubits) :=
    EuclideanSpace.single (fun _ => 0) 1
  have identity : _root_.Matrix.toEuclideanCLM (𝕜 := ℂ) (n := PrimitiveBasis qubits)
      (A-B) zeroState = column A-column B := by
    ext z
    simp [zeroState, column, _root_.Matrix.ofLp_toEuclideanCLM, _root_.Matrix.col_apply]
  have bound := (_root_.Matrix.toEuclideanCLM (𝕜 := ℂ) (n := PrimitiveBasis qubits)
    (A-B)).le_opNorm zeroState
  rw [identity, _root_.Matrix.l2_opNorm_toEuclideanCLM] at bound
  simpa [zeroState] using bound

/-- Full state norm: the garbage sectors remain in the vector and cannot be
discarded by projection, conditioning or quotient-by-phase comparison. -/
theorem compile_state_error (k n : ℕ) (L : ℝ) (hL : 0<L) (bits : ℕ) :
    ‖column (evalPrimitiveCircuit (compile k n L hL bits)) - target k n L‖ ≤
      errorCoefficient k n / (2 : ℝ)^bits := by
  rw [← exact_column_target k n L hL]
  exact (column_error _ _).trans (compile_operator_error k n L hL bits)

/-- Internally supplied logarithmic allocation and alignment; callers do not
provide an angle-error or a circuit-action certificate. -/
theorem compile_epsilon (k n : ℕ) (L : ℝ) (hL : 0<L)
    {epsilon : ℝ} (he : 0<epsilon) :
    ‖column (evalPrimitiveCircuit (compile k n L hL (bitsFor k n epsilon))) -
      target k n L‖ ≤ epsilon :=
  (compile_state_error k n L hL _).trans (bitsFor_error k n he)

/-- All conclusions refer to this one actual returned rounded list. Quantum
resources are preserved; the exact source's classical cost is not extended to
the noncomputable floor operation by this theorem. -/
theorem compile_certified (k n : ℕ) (L : ℝ) (hL : 0<L)
    {epsilon : ℝ} (he : 0<epsilon) :
    let result := compile k n L hL (bitsFor k n epsilon)
    result.length = (StagedGlobalAssembly.compile k n L hL).run.value.length ∧
    result.resource = (StagedGlobalAssembly.compile k n L hL).run.value.resource ∧
    result.gateCount ≤ 48*(n+1)*(2*k+6)^3 ∧
    result.resource.depth ≤ 48*(n+1)*(2*k+6)^3 ∧
    result.resource.oracleCalls = 0 ∧
    evalPrimitiveCircuit result ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis ((n+1)+HermiteFiniteChain.bondQubits k)) ℂ ∧
    ‖column (evalPrimitiveCircuit result) - target k n L‖ ≤ epsilon := by
  exact ⟨roundCircuit_length _ _, compile_resource k n L hL _,
    compile_gateCount k n L hL _,
    (compile k n L hL _).resource_depth_le_gateCount.trans (compile_gateCount k n L hL _),
    rfl, evalPrimitiveCircuit_unitary _, compile_epsilon k n L hL he⟩

/-- One arbitrarily narrow enclosure [-a,a] straddling zero contains angles
whose exact floor numerators differ. This identifies why finite enclosures
alone do not automatically refine the literal exact-floor supplier. It is not
a claim that approximate angle production is impossible. -/
theorem floor_boundary_discriminator {a : ℝ} (ha : 0<a) (hsmall : a<1) :
    numerator 0 (.real a) = 0 ∧ numerator 0 (.real (-a)) = -1 := by
  simp only [numerator, ExactAngle.eval, pow_zero, mul_one]
  constructor
  · apply Int.floor_eq_iff.mpr
    norm_num
    exact ⟨ha.le, hsmall⟩
  · apply Int.floor_eq_iff.mpr
    norm_num
    exact ⟨hsmall.le, ha⟩

/-- Boolean constructor classifier, independent of all angle semantics. -/
def isRyCx : PrimitiveGate qubits → Bool
  | .ry _ _ | .cx _ _ _ => true
  | _ => false

private theorem realize_basis (angle : ℝ) (trace : List (SelectedRyTrace.Gate qubits)) :
    (StagedLocalSOEmission.realize angle trace).value.all isRyCx = true := by
  induction trace with
  | nil => rfl
  | cons g gs ih =>
      cases g <;> simp [StagedLocalSOEmission.realize, StagedLocalSOEmission.realizeGate,
        StoredGivens.Run.bind, StoredGivens.Run.pure, StoredGivens.charge,
        StoredGivens.mul, bind, pure, isRyCx, ih]

private theorem plane_basis (step : AdjacentGivens.Step (2^(q+1))) :
    (StagedLocalSOEmission.plane step).value.all isRyCx = true := by
  apply realize_basis

private theorem emitSteps_basis (steps : List (AdjacentGivens.Step (2^(q+1)))) :
    (StagedLocalSOEmission.emitSteps steps).value.all isRyCx = true := by
  induction steps with
  | nil => rfl
  | cons g gs ih =>
      simp only [StagedLocalSOEmission.emitSteps, bind, StoredGivens.Run.bind,
        StoredGivens.charge, StoredSelectedRyTrace.append_value, List.all_append]
      rw [plane_basis, ih]
      rfl

private theorem compileAt_basis {N l r q : ℕ} (C : StoredTensorTrain.StoredChain N l r)
    (hB : TensorTrainCanonical.maxBond (StoredTensorTrain.denoteChain C) ≤ 2^q)
    (t : ℕ) (ht : t<N) :
    (StagedStagePrimitive.compileAt C hB t ht).value.all isRyCx = true := by
  apply emitSteps_basis

private theorem mapPlacement_basis (f : StagedGlobalAssembly.Placement m p)
    (c : PrimitiveCircuit m) :
    (StagedGlobalAssembly.mapPlacement f c).value.all isRyCx = c.all isRyCx := by
  rw [StagedGlobalAssembly.mapPlacement_value, List.all_map]
  congr 1
  funext g
  cases f <;> cases g <;> rfl

private theorem padStored_basis (c : PrimitiveCircuit m) (t : ℕ) :
    (StagedGlobalAssembly.padStored c t).value.all isRyCx = c.all isRyCx := by
  induction t with
  | zero => rfl
  | succ t ih =>
      simp only [StagedGlobalAssembly.padStored, bind, StoredGivens.Run.bind,
        mapPlacement_basis, ih]

private theorem placeStored_basis (c : PrimitiveCircuit (q+1)) (t : ℕ) :
    (StagedGlobalAssembly.placeStored t c).value.all isRyCx = c.all isRyCx := by
  simp only [StagedGlobalAssembly.placeStored, bind, StoredGivens.Run.bind,
    mapPlacement_basis, padStored_basis]

private theorem assembleStored_basis (stages : Vector (PrimitiveCircuit (q+1)) N)
    (hs : ∀ i : Fin N, stages[i.val].all isRyCx = true) (t : ℕ) (ht : t≤N) :
    (StagedGlobalAssembly.assembleStored stages t ht).value.all isRyCx = true := by
  induction t with
  | zero => rfl
  | succ t ih =>
      simp only [StagedGlobalAssembly.assembleStored, bind, StoredGivens.Run.bind,
        StoredGivens.read, StoredGivens.charge, StoredSelectedRyTrace.append_value,
        List.all_append, mapPlacement_basis, placeStored_basis]
      rw [ih, hs ⟨t, by omega⟩]
      rfl

theorem exact_compile_basis (k n : ℕ) (L : ℝ) (hL : 0<L) :
    (StagedGlobalAssembly.compile k n L hL).run.value.all isRyCx = true := by
  simp only [StagedGlobalAssembly.compile, StagedGlobalAssembly.compileFrom,
    StagedGlobalAssembly.publicStored, bind, StoredGivens.Run.bind, mapPlacement_basis]
  apply assembleStored_basis
  intro i
  rw [StagedGlobalAssembly.compileStages, StoredGivens.collect_value]
  apply compileAt_basis

/-- Finite rational representation of every angle in the actual returned
Hermite instruction list, not just a conditional statement about RY inputs. -/
def isDyadicRyCx (bits : ℕ) : PrimitiveGate qubits → Prop
  | .ry _ a => ∃ m : ℤ, a = .rational (dyadicRat bits m)
  | .cx _ _ _ => True
  | _ => False

theorem compile_dyadic_basis (k n : ℕ) (L : ℝ) (hL : 0<L) (bits : ℕ)
    (g : PrimitiveGate ((n+1)+HermiteFiniteChain.bondQubits k))
    (hg : g ∈ compile k n L hL bits) : isDyadicRyCx bits g := by
  obtain ⟨original, ho, rfl⟩ := List.mem_map.mp hg
  have hb := List.all_eq_true.mp (exact_compile_basis k n L hL) original ho
  cases original <;> simp [isRyCx] at hb
  · exact ⟨_, rfl⟩
  · trivial

namespace Tests

example : dyadicRat 3 (-3) = (-3/8 : ℚ) := by norm_num [dyadicRat]
example : dyadicRat 0 (-7) = (-7 : ℚ) := by norm_num [dyadicRat]
example : (roundAngle 3 (.rational (-1/10))).eval = (-1/8 : ℝ) := by
  norm_num [roundAngle_eval, ExactAngle.eval]
example : (roundAngle 3 (.rational (1/10))).eval = 0 := by
  norm_num [roundAngle_eval, ExactAngle.eval]
example : (roundAngle 3 (.rational (-3/8))).eval = (-3/8 : ℝ) := by
  norm_num [roundAngle_eval, ExactAngle.eval]

example : bitsFor 0 0 (1 : ℝ) = 13 := by
  norm_num [bitsFor, errorCoefficient, Nat.clog]
  rfl

example (bits : ℕ) : roundCircuit bits ([] : PrimitiveCircuit 0) = [] := rfl
example (bits : ℕ) (angle : ExactAngle) :
    roundGate bits (.rz (0 : Fin 1) angle) = .rz 0 angle := rfl

example (bits : ℕ) (a b : ExactAngle) :
    roundCircuit bits [.ry (1 : Fin 2) a, .cx 1 0 (by decide), .ry 0 b] =
      [.ry 1 (roundAngle bits a), .cx 1 0 (by decide), .ry 0 (roundAngle bits b)] := rfl

example (k n : ℕ) (L : ℝ) (x : PrimitiveBasis (n+1))
    (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)) (hb : b ≠ (fun _ => 0)) :
    target k n L (Fin.append x b) = 0 := by rw [target_append, if_neg hb]

end Tests

#print axioms roundAngle_error
#print axioms roundCircuit_aligned
#print axioms roundCircuit_resource
#print axioms compile_operator_error
#print axioms bitsFor_error
#print axioms exact_column_target
#print axioms column_error
#print axioms compile_state_error
#print axioms compile_epsilon
#print axioms compile_certified
#print axioms floor_boundary_discriminator
#print axioms exact_compile_basis
#print axioms compile_dyadic_basis
end QuantumBlockEncoding.DyadicSupplier
