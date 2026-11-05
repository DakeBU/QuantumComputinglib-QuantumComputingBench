import QuantumBlockEncoding.PrimitiveWireRename
import QuantumBlockEncoding.SequentialBondPreparation

/-! Actual finite primitive lists for repeated finite-bond stages.
Bond wires are `0,...,q-1`; stage `t` emits data wire `q+t`.
The complete clean-input action is identified with
`SequentialBondPreparation.run`, with exact primitive-list counts.
Changing labels below costs no SWAP because instructions themselves are
placed on their final physical wires; no state is moved for free. -/

namespace QuantumBlockEncoding.SequentialPrimitiveAssembly
open RealAmplitudePreparation

def pad {m : Nat} (c : PrimitiveCircuit m) : (extra : Nat) → PrimitiveCircuit (m + extra)
  | 0 => c
  | extra + 1 => (pad c extra).map liftGate

noncomputable def padMatrix {m : Nat}
    (M : _root_.Matrix (PrimitiveBasis m) (PrimitiveBasis m) ℂ) :
    (extra : Nat) → _root_.Matrix (PrimitiveBasis (m + extra)) (PrimitiveBasis (m + extra)) ℂ
  | 0 => M
  | extra + 1 => liftLastMatrix (padMatrix M extra)

theorem eval_pad {m : Nat} (c : PrimitiveCircuit m) (extra : Nat) :
    evalPrimitiveCircuit (pad c extra) = padMatrix (evalPrimitiveCircuit c) extra := by
  induction extra with
  | zero => rfl
  | succ extra ih => rw [pad, eval_liftCircuit, ih]; rfl

theorem padMatrix_append {m : Nat}
    (M : _root_.Matrix (PrimitiveBasis m) (PrimitiveBasis m) ℂ)
    (t : Nat) (a b : PrimitiveBasis m) (x y : PrimitiveBasis t) :
    padMatrix M t (Fin.append a x) (Fin.append b y) =
      if x = y then M a b else 0 := by
  induction t with
  | zero =>
    have ha : Fin.append a x = a := by
      funext i
      simpa only [Fin.cast, Fin.castAdd, Fin.castLE] using Fin.append_left a x i
    have hb : Fin.append b y = b := by
      funext i
      simpa only [Fin.cast, Fin.castAdd, Fin.castLE] using Fin.append_left b y i
    rw [padMatrix, ha, hb, if_pos (Subsingleton.elim x y)]
  | succ t ih =>
    obtain ⟨⟨x, u⟩, rfl⟩ := (lastBasisEquiv t).symm.surjective x
    obtain ⟨⟨y, v⟩, rfl⟩ := (lastBasisEquiv t).symm.surjective y
    simp only [lastBasisEquiv_symm_apply, Fin.append_snoc, padMatrix,
      liftLastMatrix_apply, Fin.init_snoc, Fin.snoc_last, ih, Fin.snoc_inj]
    by_cases h : x = y <;> by_cases hv : u = v <;> simp [h, hv]

@[simp] theorem pad_ryCount {m : Nat} (c : PrimitiveCircuit m) (extra : Nat) :
    (pad c extra).ryCount = c.ryCount := by
  induction extra with
  | zero => rfl
  | succ extra ih => rw [pad, liftCircuit_ryCount, ih]

@[simp] theorem pad_cxCount {m : Nat} (c : PrimitiveCircuit m) (extra : Nat) :
    (pad c extra).cxCount = c.cxCount := by
  induction extra with
  | zero => rfl
  | succ extra ih => rw [pad, liftCircuit_cxCount, ih]

@[simp] theorem pad_gateCount {m : Nat} (c : PrimitiveCircuit m) (extra : Nat) :
    (pad c extra).gateCount = c.gateCount := by
  induction extra with
  | zero => rfl
  | succ extra ih => simpa [pad, PrimitiveCircuit.gateCount] using ih

/-- Preserve bond indices and send the local fresh bit to the new highest wire. -/
def stageWires (q t : Nat) : Fin ((q + 1) + t) ≃ Fin ((q + t) + 1) where
  toFun := Fin.addCases
    (Fin.lastCases (Fin.last (q + t)) (fun i => (Fin.castAdd t i).castSucc))
    (fun i => (Fin.natAdd q i).castSucc)
  invFun := Fin.lastCases (Fin.castAdd t (Fin.last q))
    (Fin.addCases (fun i => Fin.castAdd t i.castSucc) (Fin.natAdd (q + 1)))
  left_inv i := by
    refine Fin.addCases (fun i => ?_) (fun i => ?_) i
    · refine Fin.lastCases ?_ (fun i => ?_) i <;>
        simp only [Fin.addCases_left, Fin.lastCases_last,
          Fin.lastCases_castSucc]
    · simp only [Fin.addCases_right, Fin.lastCases_castSucc]
  right_inv i := by
    refine Fin.lastCases ?_ (fun i => ?_) i
    · simp only [Fin.addCases_left, Fin.lastCases_last]
    · refine Fin.addCases (fun i => ?_) (fun i => ?_) i <;>
        simp only [Fin.addCases_left, Fin.addCases_right,
          Fin.lastCases_castSucc]

@[simp] theorem stageWires_fresh (q t : Nat) :
    stageWires q t (Fin.castAdd t (Fin.last q)) = Fin.last (q + t) := by
  simp [stageWires]

theorem stageWires_bond (q t : Nat) (i : Fin q) :
    (stageWires q t (Fin.castAdd t i.castSucc)).val = i.val := by
  simp [stageWires]

theorem stageWires_basis (q t : Nat) (b : PrimitiveBasis q)
    (x : PrimitiveBasis t) (bit : Fin 2) :
    (fun w : Fin ((q + 1) + t) =>
      (Fin.snoc (Fin.append b x) bit : PrimitiveBasis ((q + t) + 1)) (stageWires q t w)) =
      Fin.append (Fin.snoc b bit) x := by
  funext w
  refine Fin.addCases (fun i => ?_) (fun i => ?_) w
  · refine Fin.lastCases ?_ (fun i => ?_) i <;> simp [stageWires]
  · simp only [stageWires, Equiv.coe_fn_mk, Fin.addCases_right,
      Fin.snoc_castSucc, Fin.append_right]

def placeStage {q : Nat} (t : Nat) (c : PrimitiveCircuit (q + 1)) :
    PrimitiveCircuit ((q + t) + 1) :=
  PrimitiveWireRename.circuit (stageWires q t) (pad c t)

noncomputable def placedMatrix {q : Nat} (t : Nat)
    (M : _root_.Matrix (PrimitiveBasis (q + 1)) (PrimitiveBasis (q + 1)) ℂ) :
    _root_.Matrix (PrimitiveBasis ((q + t) + 1)) (PrimitiveBasis ((q + t) + 1)) ℂ :=
  PrimitiveWireRename.matrix (stageWires q t) (padMatrix M t)

theorem eval_placeStage {q : Nat} (t : Nat) (c : PrimitiveCircuit (q + 1)) :
    evalPrimitiveCircuit (placeStage t c) = placedMatrix t (evalPrimitiveCircuit c) := by
  rw [placeStage, PrimitiveWireRename.eval_circuit, eval_pad]
  rfl

theorem placedMatrix_apply {q : Nat} (t : Nat)
    (M : _root_.Matrix (PrimitiveBasis (q + 1)) (PrimitiveBasis (q + 1)) ℂ)
    (a b : PrimitiveBasis q) (x y : PrimitiveBasis t) (u v : Fin 2) :
    placedMatrix t M (Fin.snoc (Fin.append a x) u) (Fin.snoc (Fin.append b y) v) =
      if x = y then M (Fin.snoc a u) (Fin.snoc b v) else 0 := by
  rw [placedMatrix, PrimitiveWireRename.matrix_apply, stageWires_basis,
    stageWires_basis, padMatrix_append]

@[simp] theorem placeStage_ryCount {q : Nat} (t : Nat) (c : PrimitiveCircuit (q + 1)) :
    (placeStage t c).ryCount = c.ryCount := by simp [placeStage]

@[simp] theorem placeStage_cxCount {q : Nat} (t : Nat) (c : PrimitiveCircuit (q + 1)) :
    (placeStage t c).cxCount = c.cxCount := by simp [placeStage]

@[simp] theorem placeStage_gateCount {q : Nat} (t : Nat) (c : PrimitiveCircuit (q + 1)) :
    (placeStage t c).gateCount = c.gateCount := by
  simp only [placeStage, PrimitiveWireRename.gateCount, pad_gateCount]

/-- Assemble one actual primitive list, with each bond stage on its final wires. -/
def assemble (q : Nat) (stages : Nat → PrimitiveCircuit (q + 1)) :
    (n : Nat) → PrimitiveCircuit (q + n)
  | 0 => []
  | n + 1 => (assemble q stages n).map liftGate ++ placeStage n (stages n)

noncomputable def assembledMatrix (q : Nat)
    (stages : Nat → PrimitiveCircuit (q + 1)) :
    (n : Nat) → _root_.Matrix (PrimitiveBasis (q + n)) (PrimitiveBasis (q + n)) ℂ
  | 0 => 1
  | n + 1 => placedMatrix n (evalPrimitiveCircuit (stages n)) *
      liftLastMatrix (assembledMatrix q stages n)

theorem eval_assemble (q : Nat) (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat) :
    evalPrimitiveCircuit (assemble q stages n) = assembledMatrix q stages n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [assemble, evalPrimitiveCircuit_append, eval_placeStage, eval_liftCircuit, ih]
    rfl

theorem assembledMatrix_clean_column (q : Nat)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat)
    (a b : PrimitiveBasis q) (x : PrimitiveBasis n) :
    assembledMatrix q stages n (Fin.append b x) (Fin.append a (fun _ => 0)) =
      SequentialBondPreparation.run (fun t => SequentialBondPreparation.circuitStage (stages t))
        (SequentialBondPreparation.basisBoundary a) n (x, b) := by
  classical
  induction n generalizing b with
  | zero =>
    have hx : Fin.append b x = b := by
      funext i
      simpa only [Fin.cast, Fin.castAdd, Fin.castLE] using Fin.append_left b x i
    have ha : Fin.append a (fun _ : Fin 0 => (0 : Fin 2)) = a := by
      funext i
      simpa only [Fin.cast, Fin.castAdd, Fin.castLE] using Fin.append_left a (fun _ => 0) i
    simp [assembledMatrix, hx, ha, SequentialBondPreparation.run,
      SequentialBondPreparation.basisBoundary, _root_.Matrix.one_apply]
  | succ n ih =>
    obtain ⟨⟨x, bit⟩, rfl⟩ := (lastBasisEquiv n).symm.surjective x
    have hz : (fun _ : Fin (n + 1) => (0 : Fin 2)) = Fin.snoc (fun _ => 0) 0 := by
      funext i
      refine Fin.lastCases ?_ (fun i => ?_) i <;> simp
    simp only [lastBasisEquiv_symm_apply, hz, Fin.append_snoc, assembledMatrix,
      SequentialBondPreparation.run, SequentialBondPreparation.step_apply,
      Fin.init_snoc, Fin.snoc_last, SequentialBondPreparation.circuitStage_apply]
    rw [_root_.Matrix.mul_apply, ← (lastBasisEquiv (q + n)).symm.sum_comp]
    simp only [Fintype.sum_prod_type, lastBasisEquiv_symm_apply, liftLastMatrix_apply,
      Fin.init_snoc, Fin.snoc_last, mul_ite, mul_zero, Finset.sum_ite_eq',
      Finset.mem_univ, if_true]
    rw [← (Fin.appendEquiv q n).sum_comp]
    simp only [Fin.appendEquiv, Equiv.coe_fn_mk, Fintype.sum_prod_type,
      placedMatrix_apply, ite_mul, zero_mul, Finset.sum_ite_eq,
      Finset.mem_univ, if_true]
    simp only [ih]
    simp [Fin.snoc]

/-- A flattened primitive circuit has exactly the sequential state action;
the fresh data inputs are all zero and every output amplitude is covered. -/
theorem assemble_clean_column (q : Nat)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat)
    (a b : PrimitiveBasis q) (x : PrimitiveBasis n) :
    evalPrimitiveCircuit (assemble q stages n)
        (Fin.append b x) (Fin.append a (fun _ => 0)) =
      SequentialBondPreparation.run (fun t => SequentialBondPreparation.circuitStage (stages t))
        (SequentialBondPreparation.basisBoundary a) n (x, b) := by
  rw [eval_assemble, assembledMatrix_clean_column]

theorem run_boundary_decomposition {q : Nat}
    (U : Nat → SequentialBondPreparation.Stage (PrimitiveBasis q))
    (v : PrimitiveBasis q → ℂ) (n : Nat) (x : PrimitiveBasis n) (b : PrimitiveBasis q) :
    SequentialBondPreparation.run U v n (x, b) =
      ∑ a, SequentialBondPreparation.run U (SequentialBondPreparation.basisBoundary a)
        n (x, b) * v a := by
  classical
  induction n generalizing b with
  | zero => simp [SequentialBondPreparation.run, SequentialBondPreparation.basisBoundary]
  | succ n ih =>
    simp only [SequentialBondPreparation.run, SequentialBondPreparation.step_apply, ih,
      Finset.mul_sum, Finset.sum_mul, mul_assoc]
    exact Finset.sum_comm

/-- The initial bond vector is prepared by an actual circuit, never supplied
as a free state. Its gate cost is added to the sequential-stage costs. -/
def withInitial {q : Nat} (initial : PrimitiveCircuit q)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat) : PrimitiveCircuit (q + n) :=
  pad initial n ++ assemble q stages n

theorem withInitial_column {q : Nat} (initial : PrimitiveCircuit q)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat)
    (a b : PrimitiveBasis q) (x : PrimitiveBasis n) :
    evalPrimitiveCircuit (withInitial initial stages n)
        (Fin.append b x) (Fin.append a (fun _ => 0)) =
      SequentialBondPreparation.run (fun t => SequentialBondPreparation.circuitStage (stages t))
        (fun c => evalPrimitiveCircuit initial c a) n (x, b) := by
  classical
  rw [withInitial, evalPrimitiveCircuit_append, eval_pad, _root_.Matrix.mul_apply,
    ← (Fin.appendEquiv q n).sum_comp]
  simp only [Fin.appendEquiv, Equiv.coe_fn_mk, Fintype.sum_prod_type,
    padMatrix_append, mul_ite, mul_zero, Finset.sum_ite_eq',
    Finset.mem_univ, if_true, assemble_clean_column]
  exact (run_boundary_decomposition _ _ n x b).symm

theorem assemble_ryCount (q : Nat) (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat) :
    (assemble q stages n).ryCount = ∑ t ∈ Finset.range n, (stages t).ryCount := by
  induction n with
  | zero => simp [assemble, PrimitiveCircuit.ryCount]
  | succ n ih =>
    rw [assemble, PrimitiveCircuit.ryCount_append, liftCircuit_ryCount,
      placeStage_ryCount, ih, Finset.sum_range_succ]

theorem assemble_cxCount (q : Nat) (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat) :
    (assemble q stages n).cxCount = ∑ t ∈ Finset.range n, (stages t).cxCount := by
  induction n with
  | zero => simp [assemble, PrimitiveCircuit.cxCount]
  | succ n ih =>
    rw [assemble, PrimitiveCircuit.cxCount_append, liftCircuit_cxCount,
      placeStage_cxCount, ih, Finset.sum_range_succ]

theorem assemble_noOracle (q : Nat) (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat) :
    (assemble q stages n).resource.oracleCalls = 0 := rfl

theorem withInitial_ryCount {q : Nat} (initial : PrimitiveCircuit q)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat) :
    (withInitial initial stages n).ryCount = initial.ryCount +
      ∑ t ∈ Finset.range n, (stages t).ryCount := by
  rw [withInitial, PrimitiveCircuit.ryCount_append, pad_ryCount, assemble_ryCount]

theorem withInitial_cxCount {q : Nat} (initial : PrimitiveCircuit q)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat) :
    (withInitial initial stages n).cxCount = initial.cxCount +
      ∑ t ∈ Finset.range n, (stages t).cxCount := by
  rw [withInitial, PrimitiveCircuit.cxCount_append, pad_cxCount, assemble_cxCount]

theorem withInitial_primitive_bound {q : Nat} (initial : PrimitiveCircuit q)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n bound : Nat)
    (h : ∀ t < n, (stages t).ryCount + (stages t).cxCount ≤ bound) :
    (withInitial initial stages n).ryCount + (withInitial initial stages n).cxCount ≤
      initial.ryCount + initial.cxCount + n * bound := by
  rw [withInitial_ryCount, withInitial_cxCount]
  have hs : (∑ t ∈ Finset.range n, ((stages t).ryCount + (stages t).cxCount)) ≤ n * bound := by
    calc
      _ ≤ ∑ _t ∈ Finset.range n, bound := Finset.sum_le_sum (fun t ht => h t (Finset.mem_range.mp ht))
      _ = n * bound := by simp
  rw [Finset.sum_add_distrib] at hs
  omega

/-- Place the first emitted bit at the most-significant data wire, and the
bond after the data register. This relabels every instruction, not the state. -/
def outputWires (q n : Nat) : Fin (q + n) ≃ Fin (n + q) where
  toFun := Fin.addCases (Fin.natAdd n) (fun i => Fin.castAdd q i.rev)
  invFun := Fin.addCases (fun i => Fin.natAdd q i.rev) (Fin.castAdd n)
  left_inv i := by
    refine Fin.addCases (fun i => ?_) (fun i => ?_) i <;>
      simp only [Fin.addCases_left, Fin.addCases_right, Fin.rev_rev]
  right_inv i := by
    refine Fin.addCases (fun i => ?_) (fun i => ?_) i <;>
      simp only [Fin.addCases_left, Fin.addCases_right, Fin.rev_rev]

theorem outputWires_basis (q n : Nat) (b : PrimitiveBasis q) (x : PrimitiveBasis n) :
    (fun w => Fin.append x b (outputWires q n w)) =
      Fin.append b (fun i => x i.rev) := by
  funext w
  refine Fin.addCases (fun i => ?_) (fun i => ?_) w <;>
    simp only [outputWires, Equiv.coe_fn_mk, Fin.addCases_left,
      Fin.addCases_right, Fin.append_left, Fin.append_right]

/-- Physical output convention: low data wires are little-endian, clean bond
wires follow them. Both preparation and stages incur their actual gate costs. -/
def publicCircuit {q : Nat} (initial : PrimitiveCircuit q)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat) : PrimitiveCircuit (n + q) :=
  PrimitiveWireRename.circuit (outputWires q n) (withInitial initial stages n)

theorem publicCircuit_column {q : Nat} (initial : PrimitiveCircuit q)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n : Nat)
    (a b : PrimitiveBasis q) (x : PrimitiveBasis n) :
    evalPrimitiveCircuit (publicCircuit initial stages n)
        (Fin.append x b) (Fin.append (fun _ => 0) a) =
      SequentialBondPreparation.run (fun t => SequentialBondPreparation.circuitStage (stages t))
        (fun c => evalPrimitiveCircuit initial c a) n ((fun i => x i.rev), b) := by
  rw [publicCircuit, PrimitiveWireRename.eval_circuit, PrimitiveWireRename.matrix_apply,
    outputWires_basis, outputWires_basis, withInitial_column]

theorem publicCircuit_primitive_bound {q : Nat} (initial : PrimitiveCircuit q)
    (stages : Nat → PrimitiveCircuit (q + 1)) (n bound : Nat)
    (h : ∀ t < n, (stages t).ryCount + (stages t).cxCount ≤ bound) :
    (publicCircuit initial stages n).ryCount + (publicCircuit initial stages n).cxCount ≤
      initial.ryCount + initial.cxCount + n * bound := by
  simp only [publicCircuit, PrimitiveWireRename.ryCount, PrimitiveWireRename.cxCount]
  exact withInitial_primitive_bound initial stages n bound h

end QuantumBlockEncoding.SequentialPrimitiveAssembly
