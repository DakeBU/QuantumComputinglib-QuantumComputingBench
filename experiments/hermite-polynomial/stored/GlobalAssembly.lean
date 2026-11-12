import StagePrimitive
import QuantumBlockEncoding.ConstructiveHermitePreparation

/-! One cached source, every actual primitive stage, and persistent physical
placement. Contract: global-assembly-contract.json, sealed before proof search.
The index-word placement allowance is not a finite-bit runtime certificate. -/
namespace QuantumBlockEncoding.StagedGlobalAssembly
open scoped BigOperators
open StoredGivens StoredTensorTrain TensorTrainCanonical TensorTrainSchedule
open SequentialPrimitiveAssembly RealAmplitudePreparation

set_option maxHeartbeats 400000

private theorem total_add (a b : Cost) :
    StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  simp [StoredRectangularGivens.total]
  omega

/-- Closed, named placement kernels: no arbitrary entry/gate callback. -/
inductive Placement : ℕ → ℕ → Type where
  | lift (m : ℕ) : Placement m (m+1)
  | stage (q t : ℕ) : Placement ((q+1)+t) ((q+t)+1)
  | output (q N : ℕ) : Placement (q+N) (N+q)

def Placement.apply : Placement m p → PrimitiveGate m → PrimitiveGate p
  | .lift _, g => liftGate g
  | .stage q t, g => PrimitiveWireRename.gate (stageWires q t) g
  | .output q N, g => PrimitiveWireRename.gate (outputWires q N) g

/-- Internal fixed-word placement kernel: read one primitive instruction,
eight index-word allowances, and write one persistent output node. The only
callers are liftGate and the explicit stage/public wire maps. -/
def mapPlacement (f : Placement m p) :
    PrimitiveCircuit m → Run (PrimitiveCircuit p)
  | [] => charge .read []
  | g::gs => do
    let head ← charge .read g
    let mapped : Run (PrimitiveGate p) := ⟨f.apply head, 8 • tick .field⟩
    let value ← mapped
    let tail ← mapPlacement f gs
    charge .write (value::tail)

theorem mapPlacement_value (f : Placement m p)
    (c : PrimitiveCircuit m) : (mapPlacement f c).value = c.map f.apply := by
  induction c with
  | nil => rfl
  | cons g gs ih => simpa [mapPlacement, bind, Run.bind, charge] using congrArg (f.apply g :: ·) ih

theorem mapPlacement_total (f : Placement m p)
    (c : PrimitiveCircuit m) :
    StoredRectangularGivens.total (mapPlacement f c).cost = 10*c.length+1 := by
  induction c with
  | nil => simp [mapPlacement, charge, StoredRectangularGivens.total, tick]
  | cons g gs ih =>
    simp [mapPlacement, bind, Run.bind, charge,
      StoredRectangularGivens.total, tick] at ih ⊢
    omega

def padStored {m : ℕ} (c : PrimitiveCircuit m) :
    (t : ℕ) → Run (PrimitiveCircuit (m+t))
  | 0 => pure c
  | t+1 => do
    let previous ← padStored c t
    mapPlacement (.lift _) previous

theorem padStored_value {m : ℕ} (c : PrimitiveCircuit m) (t : ℕ) :
    (padStored c t).value = pad c t := by
  induction t with
  | zero => rfl
  | succ t ih => simp [padStored, bind, Run.bind, mapPlacement_value, Placement.apply, ih, pad]

theorem padStored_total {m : ℕ} (c : PrimitiveCircuit m) (t : ℕ) :
    StoredRectangularGivens.total (padStored c t).cost = t*(10*c.length+1) := by
  induction t with
  | zero => simp [padStored, pure, Run.pure, StoredRectangularGivens.total]
  | succ t ih =>
    simp only [padStored, bind, Run.bind, total_add, mapPlacement_total,
      padStored_value]
    have hl : (pad c t).length = c.length := pad_gateCount c t
    rw [hl, ih]
    ring

def placeStored {q : ℕ} (t : ℕ) (c : PrimitiveCircuit (q+1)) :
    Run (PrimitiveCircuit ((q+t)+1)) := do
  let padded ← padStored c t
  mapPlacement (.stage q t) padded

theorem placeStored_value {q : ℕ} (t : ℕ) (c : PrimitiveCircuit (q+1)) :
    (placeStored t c).value = placeStage t c := by
  simp [placeStored, bind, Run.bind, padStored_value, mapPlacement_value,
    placeStage, PrimitiveWireRename.circuit, Placement.apply]

theorem placeStored_total {q : ℕ} (t : ℕ) (c : PrimitiveCircuit (q+1)) :
    StoredRectangularGivens.total (placeStored t c).cost = (t+1)*(10*c.length+1) := by
  simp only [placeStored, bind, Run.bind, total_add, padStored_total,
    mapPlacement_total, padStored_value]
  have hl : (pad c t).length = c.length := pad_gateCount c t
  rw [hl]
  ring

/-- The empty fallback is outside the finite schedule, never a source gate. -/
def stageAt {N q : ℕ} (stages : Vector (PrimitiveCircuit (q+1)) N) (t : ℕ) :
    PrimitiveCircuit (q+1) := if ht : t<N then stages[t] else []

def assembleStored {N q : ℕ} (stages : Vector (PrimitiveCircuit (q+1)) N) :
    (t : ℕ) → t ≤ N → Run (PrimitiveCircuit (q+t))
  | 0, _ => pure []
  | t+1, bound => do
    let previous ← assembleStored stages t (by omega)
    let lifted ← mapPlacement (.lift _) previous
    let stageCircuit ← StoredGivens.read stages ⟨t, by omega⟩
    let placed ← placeStored t stageCircuit
    StoredSelectedRyTrace.append lifted placed

theorem assembleStored_value {N q : ℕ} (stages : Vector (PrimitiveCircuit (q+1)) N)
    (t : ℕ) (bound : t≤N) :
    (assembleStored stages t bound).value = assemble q (stageAt stages) t := by
  induction t with
  | zero => rfl
  | succ t ih =>
    simp [assembleStored, bind, Run.bind, mapPlacement_value, StoredGivens.read,
      charge, placeStored_value, StoredSelectedRyTrace.append_value, ih,
      assemble, stageAt, Placement.apply, show t<N by omega]

theorem assembleStored_length {N q : ℕ} (stages : Vector (PrimitiveCircuit (q+1)) N)
    (K : ℕ) (hK : ∀ i : Fin N, stages[i.val].length = K)
    (t : ℕ) (bound : t≤N) :
    (assembleStored stages t bound).value.length = t*K := by
  rw [assembleStored_value]
  change (assemble q (stageAt stages) t).gateCount = _
  rw [TensorTrainPrimitivePreparation.assemble_gateCount]
  calc
    _ = ∑ _i ∈ Finset.range t, K := by
      apply Finset.sum_congr rfl
      intro i hi
      have hin : i<N := (Finset.mem_range.mp hi).trans_le bound
      simpa [stageAt, hin, PrimitiveCircuit.gateCount] using hK ⟨i, hin⟩
    _ = _ := by simp

theorem assembleStored_total_le {N q : ℕ} (stages : Vector (PrimitiveCircuit (q+1)) N)
    (K : ℕ) (hK : ∀ i : Fin N, stages[i.val].length = K)
    (t : ℕ) (bound : t≤N) :
    StoredRectangularGivens.total (assembleStored stages t bound).cost ≤
      t^2*(32*K+6) := by
  induction t with
  | zero => simp [assembleStored, pure, Run.pure, StoredRectangularGivens.total]
  | succ t ih =>
    have prev := ih (by omega)
    have plen := assembleStored_length stages K hK t (by omega)
    have llen := hK ⟨t, by omega⟩
    simp only [assembleStored, bind, Run.bind, total_add, mapPlacement_total,
      StoredGivens.read, charge, placeStored_total]
    have alen : (mapPlacement (.lift _)
        (assembleStored stages t (by omega)).value).value.length = t*K := by
      rw [mapPlacement_value, List.length_map, plen]
    have ac : StoredRectangularGivens.total (StoredSelectedRyTrace.append
        (mapPlacement (.lift _) (assembleStored stages t (by omega)).value).value
        (placeStored t stages[t]).value).cost = 2*(t*K)+1 := by
      simp [StoredRectangularGivens.total, StoredSelectedRyTrace.append_cost,
        tick, alen]
      ring
    rw [ac, plen, llen]
    simp [StoredRectangularGivens.total, tick] at prev ⊢
    nlinarith

def publicStored {N q : ℕ} (stages : Vector (PrimitiveCircuit (q+1)) N) :
    Run (PrimitiveCircuit (N+q)) := do
  let assembled ← assembleStored stages N le_rfl
  mapPlacement (.output q N) assembled

private theorem pad_empty (q N : ℕ) : pad ([] : PrimitiveCircuit q) N = [] := by
  induction N with
  | zero => rfl
  | succ N ih => simp [pad, ih]

theorem publicStored_value {N q : ℕ} (stages : Vector (PrimitiveCircuit (q+1)) N) :
    (publicStored stages).value = publicCircuit [] (stageAt stages) N := by
  simp [publicStored, bind, Run.bind, assembleStored_value, mapPlacement_value,
    publicCircuit, withInitial, PrimitiveWireRename.circuit, Placement.apply, pad_empty]

def localGates (q : ℕ) : ℕ :=
  (2^(q+1)*(2^(q+1)-1)/2)*StagedLocalSOEmission.gatesPerPlane q

theorem localGates_cubic (q : ℕ) : localGates q ≤ 6*(2^q)^3 := by
  let S := 2^q
  have he : S*2*(S*2-1)/2 ≤ 2*S^2 := by
    have hd := Nat.div_mul_le_self (S*2*(S*2-1)) 2
    have hm := Nat.mul_le_mul_left (S*2) (Nat.sub_le (S*2) 1)
    nlinarith
  have hg : StagedLocalSOEmission.gatesPerPlane q ≤ 3*S := by
    unfold StagedLocalSOEmission.gatesPerPlane
    have hs := Nat.sub_le S 1
    change S+2*(S-1) ≤ 3*S
    omega
  unfold localGates
  rw [pow_succ]
  calc
    _ ≤ (2*S^2)*(3*S) := Nat.mul_le_mul he hg
    _ = _ := by dsimp [S]; ring

noncomputable def compileStages {N l r q : ℕ} (C : StoredChain N l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) :
    Run (Vector (PrimitiveCircuit (q+1)) N) :=
  collect fun t => StagedStagePrimitive.compileAt C hB t.val t.isLt

noncomputable def compileFrom {N q : ℕ} (C : StoredChain N 1 1)
    (hB : maxBond (denoteChain C) ≤ 2^q) : Run (PrimitiveCircuit (N+q)) := do
  let stages ← compileStages C hB
  publicStored stages

theorem stageAt_compileStages {N l r q : ℕ} (C : StoredChain N l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<N) :
    stageAt (compileStages C hB).value t = (StagedStagePrimitive.compileAt C hB t ht).value := by
  simp only [stageAt, dif_pos ht, compileStages]
  exact collect_value _ ⟨t, ht⟩

theorem compileStages_length {N l r q : ℕ} (C : StoredChain N l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (i : Fin N) :
    (compileStages C hB).value[i.val].length = localGates q := by
  simpa [compileStages, localGates, PrimitiveCircuit.gateCount] using
    StagedStagePrimitive.compileAt_gateCount C hB i.val i.isLt

theorem compileFrom_columns {N q : ℕ} (C : StoredChain N 1 1)
    (hC : RightCanonical (denoteChain C)) (hB : maxBond (denoteChain C) ≤ 2^q)
    (x : PrimitiveBasis N) (b : PrimitiveBasis q) :
    evalPrimitiveCircuit (compileFrom C hB).value (Fin.append x b) (fun _ => 0) =
      if b = (fun _ => 0) then
        (contract (denoteChain C) (wordOfBasis (fun i => x i.rev)) 0 0 : ℂ) else 0 := by
  simp only [compileFrom, bind, Run.bind, publicStored_value]
  apply TensorTrainPrimitivePreparation.publicCircuit_clean (denoteChain C) hB
  intro t ht bit b a ha
  rw [stageAt_compileStages C hB t ht]
  exact StagedStagePrimitive.compileAt_column C hC hB t ht bit b a ha

private theorem assembledMatrix_congr (q : ℕ)
    (left right : ℕ → PrimitiveCircuit (q+1)) (N : ℕ)
    (h : ∀ t, t<N → evalPrimitiveCircuit (left t) = evalPrimitiveCircuit (right t)) :
    assembledMatrix q left N = assembledMatrix q right N := by
  induction N with
  | zero => rfl
  | succ N ih =>
    rw [assembledMatrix, assembledMatrix, h N (by omega), ih (by
      intro t ht
      exact h t (by omega))]

private theorem publicCircuit_eval_congr (q : ℕ)
    (left right : ℕ → PrimitiveCircuit (q+1)) (N : ℕ)
    (h : ∀ t, t<N → evalPrimitiveCircuit (left t) = evalPrimitiveCircuit (right t)) :
    evalPrimitiveCircuit (publicCircuit ([] : PrimitiveCircuit q) left N) =
      evalPrimitiveCircuit (publicCircuit [] right N) := by
  simp only [publicCircuit, PrimitiveWireRename.eval_circuit, withInitial,
    evalPrimitiveCircuit_append, eval_assemble]
  rw [assembledMatrix_congr q left right N h]

/-- Full operator refinement to the existing deterministic local compiler on
the SAME canonical chain. No arbitrary unitary completion is substituted. -/
theorem compileFrom_eval {N q : ℕ} (C : StoredChain N 1 1)
    (hC : RightCanonical (denoteChain C)) (hB : maxBond (denoteChain C) ≤ 2^q) :
    evalPrimitiveCircuit (compileFrom C hB).value =
      evalPrimitiveCircuit (publicCircuit []
        (ConstructiveTensorTrainCompiler.stage (denoteChain C) hB) N) := by
  simp only [compileFrom, bind, Run.bind, publicStored_value]
  apply publicCircuit_eval_congr
  intro t ht
  rw [stageAt_compileStages C hB t ht, StagedStagePrimitive.compileAt_eval C hC hB t ht]
  have spec := ConstructiveIsometryLocal.completeStage_spec (denoteChain C) hC hB t ht
  symm
  exact GrayGivensCompiler.compileSO_eval _ spec.1 spec.2.1

def assemblyBudget (N q : ℕ) : ℕ :=
  N^2*(32*localGates q+6)+10*N*localGates q+1

theorem publicStored_total_le {N q : ℕ} (stages : Vector (PrimitiveCircuit (q+1)) N)
    (hK : ∀ i : Fin N, stages[i.val].length = localGates q) :
    StoredRectangularGivens.total (publicStored stages).cost ≤ assemblyBudget N q := by
  have hc := assembleStored_total_le stages (localGates q) hK N le_rfl
  have hl := assembleStored_length stages (localGates q) hK N le_rfl
  simp only [publicStored, bind, Run.bind, total_add, mapPlacement_total, hl]
  unfold assemblyBudget
  nlinarith

theorem collect_total {N : ℕ} (f : Fin N → Run α) :
    StoredRectangularGivens.total (collect f).cost =
      (∑ i : Fin N, StoredRectangularGivens.total (f i).cost)+4*N := by
  simp [StoredRectangularGivens.total, collect_cost, tick, Finset.sum_add_distrib]
  ring

theorem compileFrom_total_le {N q : ℕ} (C : StoredChain N 1 1)
    (hB : maxBond (denoteChain C) ≤ 2^q) (D T : ℕ)
    (hD : maxBond (denoteChain C) ≤ D) (hT : ∀ t, t<N → t≤T) :
    StoredRectangularGivens.total (compileFrom C hB).cost ≤
      N*(StagedStagePrimitive.stageBudget q D T+4)+assemblyBudget N q := by
  have hs : StoredRectangularGivens.total (compileStages C hB).cost ≤
      N*(StagedStagePrimitive.stageBudget q D T+4) := by
    rw [compileStages, collect_total]
    have sum : (∑ i : Fin N, StoredRectangularGivens.total
        (StagedStagePrimitive.compileAt C hB i.val i.isLt).cost) ≤
        N*StagedStagePrimitive.stageBudget q D T := by
      calc
        _ ≤ ∑ _i : Fin N, StagedStagePrimitive.stageBudget q D T := by
          apply Finset.sum_le_sum
          intro i _
          apply (StagedStagePrimitive.compileAt_total_cost C hB i.val i.isLt).trans
          unfold StagedStagePrimitive.stageBudget
          exact Nat.add_le_add_right
            (Nat.add_le_add_right (StagedActiveColumns.stageBudget_mono q
              ((rankAt_le_maxBond (denoteChain C) i.val).trans hD) (hT i.val i.isLt)) _) _
        _ = _ := by simp
    nlinarith
  have hp := publicStored_total_le (compileStages C hB).value (compileStages_length C hB)
  simpa only [compileFrom, bind, Run.bind, total_add] using Nat.add_le_add hs hp

theorem compileFrom_gateCount {N q : ℕ} (C : StoredChain N 1 1)
    (hB : maxBond (denoteChain C) ≤ 2^q) :
    (compileFrom C hB).value.gateCount = N*localGates q := by
  have hl := assembleStored_length (compileStages C hB).value (localGates q)
    (compileStages_length C hB) N le_rfl
  simpa [compileFrom, publicStored, bind, Run.bind, mapPlacement_value,
    PrimitiveCircuit.gateCount] using hl

noncomputable def compile (k n : ℕ) (L : ℝ) (hL : 0<L) :
    StoredHermiteRawSource.RawRun (PrimitiveCircuit ((n+1)+HermiteFiniteChain.bondQubits k)) :=
  let source := StagedNormalizedCanonical.compile k n L
  let bound := (StagedNormalizedCanonical.compile_maxBond k n L hL).trans
    (HermiteFiniteChain.bond_fits k)
  let result := compileFrom source.run.value bound
  { run := ⟨result.value, source.run.cost+result.cost⟩
    exponentialCalls := source.exponentialCalls
    quotientCalls := source.quotientCalls
    remainderCalls := source.remainderCalls
    integerDoublings := source.integerDoublings
    integerAdditions := source.integerAdditions }

def compilerBudget (k n : ℕ) : ℕ :=
  StagedNormalizedCanonical.compilerBudget k n +
    (n+1)*(StagedStagePrimitive.stageBudget (HermiteFiniteChain.bondQubits k) (2*k+6) n+4)+
    assemblyBudget (n+1) (HermiteFiniteChain.bondQubits k)

/-- Subtraction-free envelope permits transparent polynomial substitution of
the logarithmic local width; no 2^dataWidth table is hidden here. -/
def stageEnvelope (Q S H G R T : ℕ) : ℕ :=
  (22*S*R+8*S+3*(T+1)+5*R+(2*S)*R*(22*R+30*(2*S)+43)+
    20*(2*S)^2+27*(2*S)+5*R+3)+
  8*(H*((Q+1)*(Q+10)+1+5*Q+Q*(5*Q+3)+2+4)+8*H^2+4*H)+
  (26*H^3+30*H^2+H+1+
    H^2*((16*Q+12)*S+5*Q^2+14*Q+8*(Q+1)*(Q+10)+4*(Q+1)+5*G+5+2*G+2)+1)

theorem stageBudget_envelope (q R T : ℕ) :
    StagedStagePrimitive.stageBudget q R T =
      stageEnvelope q (2^q) (2^(q+1)) (StagedLocalSOEmission.gatesPerPlane q) R T := by
  unfold StagedStagePrimitive.stageBudget StagedActiveColumns.stageBudget
    StagedGrayTable.tableBudget StagedGrayTable.labelBudget
    StagedLocalSOEmission.compilerBudget StagedLocalSOEmission.emissionBudget
    StagedLocalSOEmission.planeBudget stageEnvelope
  rfl

theorem stageEnvelope_mono {Q Q' S S' H H' G G' R R' T T' : ℕ}
    (hq : Q≤Q') (hs : S≤S') (hh : H≤H') (hg : G≤G') (hr : R≤R') (ht : T≤T') :
    stageEnvelope Q S H G R T ≤ stageEnvelope Q' S' H' G' R' T' := by
  unfold stageEnvelope
  gcongr

def polynomialBudget (k n : ℕ) : ℕ :=
  let D := 2*k+6
  let N := n+1
  StagedNormalizedCanonical.compilerBudget k n +
    N*(stageEnvelope (2*D) (2*D) (4*D) (6*D) D n+4)+
    (N^2*(32*(48*D^3)+6)+10*N*(48*D^3)+1)

theorem compilerBudget_polynomial (k n : ℕ) : compilerBudget k n ≤ polynomialBudget k n := by
  let q := HermiteFiniteChain.bondQubits k
  let D := 2*k+6
  have hs : 2^q ≤ 2*D := HermiteFiniteChain.padded_bond_le_twice k
  have hq : q≤2*D := (Nat.le_of_lt (show q<2^q from Nat.lt_two_pow_self)).trans hs
  have hh : 2^(q+1)≤4*D := by rw [pow_succ]; nlinarith
  have hg : StagedLocalSOEmission.gatesPerPlane q ≤ 6*D := by
    unfold StagedLocalSOEmission.gatesPerPlane
    have sub := Nat.sub_le (2^q) 1
    omega
  have hl : localGates q ≤ 48*D^3 := by
    apply (localGates_cubic q).trans
    calc
      _ ≤ 6*(2*D)^3 := Nat.mul_le_mul_left _ (Nat.pow_le_pow_left hs 3)
      _ = _ := by ring
  have stage := stageEnvelope_mono hq hs hh hg (le_refl D) (le_refl n)
  rw [← stageBudget_envelope] at stage
  dsimp only [compilerBudget, polynomialBudget, assemblyBudget]
  change _ ≤ StagedNormalizedCanonical.compilerBudget k n+
    (n+1)*(stageEnvelope (2*D) (2*D) (4*D) (6*D) D n+4)+
    ((n+1)^2*(32*(48*D^3)+6)+10*(n+1)*(48*D^3)+1)
  gcongr

theorem compile_columns (k n : ℕ) (L : ℝ) (hL : 0<L)
    (x : PrimitiveBasis (n+1)) (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)) :
    evalPrimitiveCircuit (compile k n L hL).run.value (Fin.append x b) (fun _ => 0) =
      if b = (fun _ => 0) then HermiteStatePreparation.normalizedAmplitude k (n+1) L
        (primitiveBasisLEEquiv (n+1) x) else 0 := by
  simp only [compile]
  rw [compileFrom_columns _ (StagedNormalizedCanonical.compile_canonical k n L hL),
    StagedNormalizedCanonical.compile_contract k n L hL, TensorTrainWord.sampleEquiv_public]
  rfl

theorem compile_prepare_column (k n : ℕ) (L : ℝ) (hL : 0<L)
    (x : PrimitiveBasis (n+1)) (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)) :
    evalPrimitiveCircuit (compile k n L hL).run.value (Fin.append x b) (fun _ => 0) =
      evalPrimitiveCircuit (ConstructiveHermitePreparation.prepare k n L)
        (Fin.append x b) (fun _ => 0) := by
  rw [compile_columns, ConstructiveHermitePreparation.prepare_columns k n L hL]

theorem normalizedRaw_bond (k n : ℕ) (L : ℝ) (hL : 0<L) :
    maxBond (StagedNormalizedCanonical.semanticNormalized (StoredHermiteRawSource.raw k n L).run.value) ≤
      2^HermiteFiniteChain.bondQubits k := by
  rw [← StagedNormalizedCanonical.normalize_value, StagedNormalizedCanonical.normalize_maxBond]
  exact (StagedNormalizedCanonical.raw_maxBond k n L hL).trans (HermiteFiniteChain.bond_fits k)

private theorem stage_chain_congr {N q : ℕ} {D E : Chain N 1 1} (h : D=E)
    (hD : maxBond D ≤ 2^q) (hE : maxBond E ≤ 2^q) :
    ConstructiveTensorTrainCompiler.stage D hD = ConstructiveTensorTrainCompiler.stage E hE := by
  cases h
  rfl

/-- Full operator refinement, not only prepared-state equality, to the existing
deterministic TT compiler applied to the literal stored normalized raw source.
The legacy Hermite representation is compared separately on its clean column. -/
theorem compile_eval (k n : ℕ) (L : ℝ) (hL : 0<L) :
    evalPrimitiveCircuit (compile k n L hL).run.value =
      evalPrimitiveCircuit (ConstructiveTensorTrainCompiler.compile
        (StagedNormalizedCanonical.semanticNormalized (StoredHermiteRawSource.raw k n L).run.value)
        (normalizedRaw_bond k n L hL)) := by
  simp only [compile]
  rw [compileFrom_eval _ (StagedNormalizedCanonical.compile_canonical k n L hL)]
  unfold ConstructiveTensorTrainCompiler.compile
  apply congrArg (fun stages : ℕ → PrimitiveCircuit (HermiteFiniteChain.bondQubits k+1) =>
    evalPrimitiveCircuit (publicCircuit [] stages (n+1)))
  exact stage_chain_congr (StagedNormalizedCanonical.compile_value k n L) _ _

theorem compile_total_le (k n : ℕ) (L : ℝ) (hL : 0<L) :
    StoredHermiteRawCost.ordinary (compile k n L hL).run.cost ≤ compilerBudget k n := by
  have source := StagedNormalizedCanonical.compile_total_cost_le k n L hL
  rw [StoredHermiteRawCost.ordinary_eq_total] at source ⊢
  have body := compileFrom_total_le (StagedNormalizedCanonical.compile k n L).run.value
    ((StagedNormalizedCanonical.compile_maxBond k n L hL).trans (HermiteFiniteChain.bond_fits k))
    (2*k+6) n (StagedNormalizedCanonical.compile_maxBond k n L hL) (by omega)
  simpa only [compile, total_add, compilerBudget, Nat.add_assoc] using Nat.add_le_add source body

theorem compile_gateCount (k n : ℕ) (L : ℝ) (hL : 0<L) :
    (compile k n L hL).run.value.gateCount =
      (n+1)*localGates (HermiteFiniteChain.bondQubits k) :=
  compileFrom_gateCount _ _

theorem compile_gateCount_polynomial (k n : ℕ) (L : ℝ) (hL : 0<L) :
    (compile k n L hL).run.value.gateCount ≤ 48*(n+1)*(2*k+6)^3 := by
  rw [compile_gateCount]
  apply (Nat.mul_le_mul_left (n+1) (localGates_cubic (HermiteFiniteChain.bondQubits k))).trans
  simpa only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using
    HermiteFiniteChain.cubic_stage_budget k n

theorem compile_total_polynomial (k n : ℕ) (L : ℝ) (hL : 0<L) :
    StoredHermiteRawCost.ordinary (compile k n L hL).run.cost ≤ polynomialBudget k n :=
  (compile_total_le k n L hL).trans (compilerBudget_polynomial k n)

/-- Additional non-real counters retain RAW SOURCE scope. Selected downstream
index-word work is included in field-tag overcounts, not silently omitted. -/
theorem compile_raw_extraCounters (k n : ℕ) (L : ℝ) (hL : 0<L) :
    (compile k n L hL).exponentialCalls = (StoredHermiteRawSource.raw k n L).exponentialCalls ∧
    (compile k n L hL).quotientCalls = (n+1)*(n+2) ∧
    (compile k n L hL).remainderCalls = (n+1)^2 ∧
    (compile k n L hL).integerDoublings = n ∧
    (compile k n L hL).integerAdditions = 4*(n+1) :=
  StagedNormalizedCanonical.compile_extraCounters k n L

theorem compile_certified (k n : ℕ) (L : ℝ) (hL : 0<L) :
    let result := compile k n L hL
    result.run.value.gateCount = (n+1)*localGates (HermiteFiniteChain.bondQubits k) ∧
    result.run.value.resource.depth ≤ (n+1)*localGates (HermiteFiniteChain.bondQubits k) ∧
    result.run.value.resource.oracleCalls = 0 ∧
    evalPrimitiveCircuit result.run.value ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis ((n+1)+HermiteFiniteChain.bondQubits k)) ℂ ∧
    StoredHermiteRawCost.ordinary result.run.cost ≤ compilerBudget k n ∧
    ∀ (x : PrimitiveBasis (n+1)) (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)),
      evalPrimitiveCircuit result.run.value (Fin.append x b) (fun _ => 0) =
        if b = (fun _ => 0) then HermiteStatePreparation.normalizedAmplitude k (n+1) L
          (primitiveBasisLEEquiv (n+1) x) else 0 := by
  exact ⟨compile_gateCount k n L hL,
    (compile k n L hL).run.value.resource_depth_le_gateCount.trans (le_of_eq (compile_gateCount k n L hL)),
    rfl, evalPrimitiveCircuit_unitary _, compile_total_le k n L hL, compile_columns k n L hL⟩

namespace Tests

noncomputable def signedPrepared : StoredChain 1 1 1 :=
  StagedNormalizedCanonical.unitBoundaryStored
    (StagedNormalizedCanonical.normalize StagedNormalizedCanonical.Tests.signedState).value |>.value

theorem signedPrepared_canonical : RightCanonical (denoteChain signedPrepared) := by
  apply StagedNormalizedCanonical.unitBoundaryStored_canonical
  apply StagedNormalizedCanonical.normalize_normalized
  rw [StagedNormalizedCanonical.Tests.signedNorm]
  norm_num

theorem signedPrepared_bound : maxBond (denoteChain signedPrepared) ≤ 2^0 := by
  apply (StagedNormalizedCanonical.unitBoundaryStored_maxBond _).trans
  rw [StagedNormalizedCanonical.normalize_maxBond]
  simp [StagedNormalizedCanonical.Tests.signedState, denoteChain, maxBond]

/-- Actual all-stage compileFrom, with no bond wires, retains the negative
source amplitude rather than abs or a quotient-by-phase representative. -/
example : evalPrimitiveCircuit (compileFrom signedPrepared signedPrepared_bound).value
    (Fin.append (fun _ => 0) (fun _ => 0)) (fun _ => 0) = (-3/5 : ℂ) := by
  rw [compileFrom_columns signedPrepared signedPrepared_canonical signedPrepared_bound]
  unfold signedPrepared
  rw [StagedNormalizedCanonical.unitBoundaryStored_contract,
    StagedNormalizedCanonical.normalize_contract, StagedNormalizedCanonical.Tests.signedNorm]
  norm_num [StagedNormalizedCanonical.Tests.signedState, denoteChain, contract, slice,
    denoteCore, StagedNormalizedCanonical.Tests.signedCore, denote,
    _root_.Matrix.mul_apply, finProdFinEquiv, wordOfBasis]

example : localGates 0 = 1 := by norm_num [localGates, StagedLocalSOEmission.gatesPerPlane]

example (C : StoredChain N 1 1) (hB : maxBond (denoteChain C) ≤ 2^0) :
    (compileFrom C hB).value.gateCount = N := by
  rw [compileFrom_gateCount]
  norm_num [localGates, StagedLocalSOEmission.gatesPerPlane]

example (stages : Vector (PrimitiveCircuit (q+1)) 0) :
    (publicStored stages).value = [] := rfl

example (first second : PrimitiveCircuit (q+1)) :
    (publicStored #v[first, second]).value = PrimitiveWireRename.circuit (outputWires q 2)
      ((placeStage 0 first).map liftGate ++ placeStage 1 second) := by
  rw [publicStored_value]
  simp [publicCircuit, withInitial, pad_empty, assemble, stageAt, PrimitiveWireRename.circuit]

example (k : ℕ) (L : ℝ) (hL : 0<L)
    (x : PrimitiveBasis 1) (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)) :
    evalPrimitiveCircuit (compile k 0 L hL).run.value (Fin.append x b) (fun _ => 0) =
      if b = (fun _ => 0) then HermiteStatePreparation.normalizedAmplitude k 1 L
        (primitiveBasisLEEquiv 1 x) else 0 := compile_columns k 0 L hL x b

example (k n : ℕ) (L : ℝ) (hL : 0<L) (x : PrimitiveBasis (n+1))
    (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)) (hb : b ≠ (fun _ => 0)) :
    evalPrimitiveCircuit (compile k n L hL).run.value (Fin.append x b) (fun _ => 0) = 0 := by
  rw [compile_columns, if_neg hb]

example (k : ℕ) (L : ℝ) (hL : 0<L)
    (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)) :
    evalPrimitiveCircuit (compile k 1 L hL).run.value
      (Fin.append (fun i : Fin 2 => if i=0 then 1 else 0) b) (fun _ => 0) =
      if b = (fun _ => 0) then HermiteStatePreparation.normalizedAmplitude k 2 L
        ⟨1, by norm_num [gridSize]⟩ else 0 := by
  have label : primitiveBasisLEEquiv 2 (fun i : Fin 2 => if i=0 then 1 else 0) =
      ⟨1, by norm_num [gridSize]⟩ := by native_decide
  rw [compile_columns, label]

example (k : ℕ) (L : ℝ) (hL : 0<L)
    (b : PrimitiveBasis (HermiteFiniteChain.bondQubits k)) :
    evalPrimitiveCircuit (compile k 1 L hL).run.value
      (Fin.append (fun i : Fin 2 => if i=1 then 1 else 0) b) (fun _ => 0) =
      if b = (fun _ => 0) then HermiteStatePreparation.normalizedAmplitude k 2 L
        ⟨2, by norm_num [gridSize]⟩ else 0 := by
  have label : primitiveBasisLEEquiv 2 (fun i : Fin 2 => if i=1 then 1 else 0) =
      ⟨2, by norm_num [gridSize]⟩ := by native_decide
  rw [compile_columns, label]

end Tests

#print axioms compileFrom_columns
#print axioms compileFrom_eval
#print axioms compile_eval
#print axioms compile_prepare_column
#print axioms compile_total_le
#print axioms compile_total_polynomial
#print axioms compile_gateCount_polynomial
#print axioms compile_certified
end QuantumBlockEncoding.StagedGlobalAssembly
