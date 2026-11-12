import GrayTarget
import ExplicitControls
import QuantumBlockEncoding.StoredRectangularGivens

/-! Actual stored SO sweep to chronological elementary primitive emission.
Contract: local-so-emission-contract.json. The input is in Gray numeric order;
no uncharged input reindexing is asserted. Selected integer operations use the
declared field-tag overcount; real/rational finite-bit costs are not certified. -/
namespace QuantumBlockEncoding.StagedLocalSOEmission
open scoped BigOperators
open StoredGivens AdjacentGivens

set_option maxHeartbeats 120000

theorem rectangular_full_steps {N : ℕ} (A : _root_.Matrix (Fin N) (Fin N) ℝ)
    (k remaining : ℕ) (dimension : k+remaining=N) :
    RectangularGivens.sweepSteps A k remaining dimension.le =
      fullSweepSteps A k remaining dimension := by
  induction remaining generalizing A k with
  | zero => rfl
  | succ remaining ih =>
    cases remaining with
    | zero =>
      have hk : k<N := by omega
      have count : N-1-k=0 := by omega
      simp [RectangularGivens.sweepSteps, fullSweepSteps, hk, count,
        columnSweepSteps]
    | succ remaining =>
      have hk : k<N := by omega
      have count : N-1-k=remaining+1 := by omega
      rw [RectangularGivens.sweepSteps, dif_pos hk, fullSweepSteps]
      simp only [count]
      rw [ih _ (k+1) (by omega)]
      have updates : columnSweep A ⟨k, hk⟩ k (N-1-k) (by omega) =
          columnSweep A ⟨k, hk⟩ k (remaining+1) (by omega) := by
        exact congrArg (fun c : {c : ℕ // k+c<N} => columnSweep A ⟨k, hk⟩ k c.val c.property)
          (show (⟨N-1-k, by omega⟩ : {c : ℕ // k+c<N}) = ⟨remaining+1, by omega⟩ from
            Subtype.ext count)
      rw [updates]

/-- Actual record reads, a charged real negation, record/list writes, and a
tail-recursive accumulator. No reverse/map pass is supplied as a free view. -/
noncomputable def reverseInverse {N : ℕ} : List (Step N) → List (Step N) → Run (List (Step N))
  | [], acc => charge .read acc
  | step::rest, acc =>
    let current := charge .read step
    let first := charge .read current.value.first
    let second := charge .read current.value.second
    let angle := charge .read current.value.angle
    let negated := StoredGivens.sub 0 angle.value
    let record := charge .write
      ({ first := first.value
         second := second.value
         adjacent := current.value.adjacent
         angle := negated.value } : Step N)
    let cell := charge .write (record.value::acc)
    let result := reverseInverse rest cell.value
    ⟨result.value, current.cost+first.cost+second.cost+angle.cost+negated.cost+
      record.cost+cell.cost+result.cost⟩

theorem reverseInverse_value {N : ℕ} (steps acc : List (Step N)) :
    (reverseInverse steps acc).value = steps.reverse.map Step.inverse ++ acc := by
  induction steps generalizing acc with
  | nil => rfl
  | cons step rest ih =>
    simp [reverseInverse, ih, charge, StoredGivens.sub, Step.inverse, List.reverse_cons,
      List.append_assoc]

theorem reverseInverse_cost {N : ℕ} (steps acc : List (Step N)) (op : Op) :
    (reverseInverse steps acc).cost op =
      steps.length*(4*tick .read op+tick .field op+2*tick .write op)+tick .read op := by
  induction steps generalizing acc with
  | nil => simp [reverseInverse, charge]
  | cons step rest ih =>
    simp [reverseInverse, ih, charge, StoredGivens.sub]
    ring

noncomputable def soLog {N : ℕ} (A : StoredMatrix N N) : Run (List (Step N)) :=
  let swept := StoredRectangularGivens.sweep A 0 N (by omega)
  let inverted := reverseInverse swept.value.steps []
  ⟨inverted.value, swept.cost+inverted.cost⟩

theorem soLog_value {N : ℕ} (A : StoredMatrix N N) :
    (soLog A).value = decomposeSO (denote A) := by
  simp only [soLog, reverseInverse_value, List.append_nil,
    StoredRectangularGivens.sweep_steps]
  rw [rectangular_full_steps]
  rfl

/-- Target discovery is the actual explicit recursion. Quotient/remainder
operations are charged in the index-overcount field category. -/
def target {q : ℕ} (step : Step (2^(q+1))) : Run (Fin (q+1)) :=
  let found := HermiteGrayTargetCandidate.discover (q+1) step.first step.second step.adjacent
  ⟨found.target, (found.quotients+found.remainders) • tick .field +
    found.comparisons • tick .compare + tick .write⟩

theorem target_value {q : ℕ} (step : Step (2^(q+1))) :
    (target step).value = GrayGivensCompiler.stepTarget step :=
  HermiteGrayTargetCandidate.discover_step_target step

/-- Cast the actual rational coefficient and multiply the cached real angle.
The returned primitive gate contains the resulting real, not a free AST eval. -/
noncomputable def realizeGate {n : ℕ} (angle : ℝ) : SelectedRyTrace.Gate n → Run (PrimitiveGate n)
  | .ry wire coefficient => do
    let realCoefficient ← charge .field (coefficient : ℝ)
    let actual ← StoredGivens.mul realCoefficient angle
    pure (.ry wire (.real actual))
  | .cx control wire distinct => pure (.cx control wire distinct)

noncomputable def realize {n : ℕ} (angle : ℝ) :
    List (SelectedRyTrace.Gate n) → Run (PrimitiveCircuit n)
  | [] => charge .read []
  | gate::rest => do
    let current ← charge .read gate
    let actual ← realizeGate angle current
    let tail ← realize angle rest
    let emitted ← charge .emit actual
    charge .write (emitted::tail)

theorem realize_eval {n : ℕ} (angle : ℝ) (trace : List (SelectedRyTrace.Gate n)) :
    evalPrimitiveCircuit (realize angle trace).value =
      evalPrimitiveCircuit (SelectedRyTrace.instantiate (.real angle) trace) := by
  induction trace with
  | nil => rfl
  | cons gate rest ih =>
    cases gate <;> simp [realize, realizeGate, bind, pure, Run.bind, Run.pure, charge,
      StoredGivens.mul, SelectedRyTrace.instantiate, SelectedRyTrace.Gate.instantiate,
      evalPrimitiveCircuit, evalPrimitiveGate, ExactAngle.eval, ih]

theorem realize_length {n : ℕ} (angle : ℝ) (trace : List (SelectedRyTrace.Gate n)) :
    (realize angle trace).value.length = trace.length := by
  induction trace with
  | nil => rfl
  | cons gate rest ih =>
    cases gate <;> simp [realize, realizeGate, bind, pure, Run.bind, Run.pure,
      charge, StoredGivens.mul, ih]

noncomputable def plane {q : ℕ} (step : Step (2^(q+1))) : Run (PrimitiveCircuit (q+1)) :=
  let found := target step
  let bits := HermiteGrayTargetCandidate.word (q+1) step.first
  let firstBit := StoredGivens.read bits.value found.value
  let signed := if firstBit.value=0 then
    (⟨step.angle, tick .compare⟩ : Run ℝ)
    else
      let negated := StoredGivens.sub 0 step.angle
      ⟨negated.value, tick .compare+negated.cost⟩
  let trace := HermiteExplicitControlsCandidate.selected found.value bits.value
  let actual := realize signed.value trace.value
  ⟨actual.value, found.cost+bits.cost+firstBit.cost+signed.cost+trace.cost+actual.cost⟩

theorem plane_eval {q : ℕ} (step : Step (2^(q+1))) :
    evalPrimitiveCircuit (plane step).value =
      GrayGivensCompiler.transport (GrayBasis.equiv (q+1)) step.matrix := by
  simp only [plane]
  rw [realize_eval, HermiteExplicitControlsCandidate.selected_plane]
  have bits : (fun i : OtherPrimitiveWires (target step).value =>
      (HermiteGrayTargetCandidate.word (q+1) step.first).value[i.val.val]) =
      (splitPrimitiveWire (target step).value (GrayBasis.equiv (q+1) step.first)).2 := by
    funext i
    exact HermiteGrayTargetCandidate.word_value (q+1) step.first i.val
  rw [bits]
  have signed : (if (StoredGivens.read
      (HermiteGrayTargetCandidate.word (q+1) step.first).value (target step).value).value=0 then
      (⟨step.angle, tick .compare⟩ : Run ℝ) else
      let negated := StoredGivens.sub 0 step.angle
      ⟨negated.value, tick .compare+negated.cost⟩).value =
      if GrayBasis.equiv (q+1) step.first (target step).value=0 then step.angle else -step.angle := by
    simp [StoredGivens.read, charge, HermiteGrayTargetCandidate.word_value,
      StoredGivens.sub]
    split_ifs <;> rfl
  simp only [ExactAngle.eval] at *
  rw [signed]
  rw [← GrayGivensCompiler.edge_plane_transport (GrayBasis.equiv (q+1))
    step.first step.second step.distinct (target step).value
    (by rw [target_value]; exact GrayGivensCompiler.stepTarget_action step) step.angle]
  rfl

noncomputable def emitSteps {q : ℕ} : List (Step (2^(q+1))) → Run (PrimitiveCircuit (q+1))
  | [] => charge .read []
  | step::rest => do
    let current ← charge .read step
    let first ← plane current
    let tail ← emitSteps rest
    StoredSelectedRyTrace.append first tail

theorem emitSteps_eval {q : ℕ} (steps : List (Step (2^(q+1)))) :
    evalPrimitiveCircuit (emitSteps steps).value =
      GrayGivensCompiler.transport (GrayBasis.equiv (q+1)) (stepsMatrix steps) := by
  induction steps with
  | nil => simp [emitSteps, charge, evalPrimitiveCircuit, stepsMatrix]
  | cons step rest ih =>
    simp only [emitSteps, bind, Run.bind, charge, StoredSelectedRyTrace.append_value]
    rw [evalPrimitiveCircuit_append, ih, plane_eval, stepsMatrix, map_mul]

noncomputable def compileGray {q : ℕ} (A : StoredMatrix (2^(q+1)) (2^(q+1))) :
    Run (PrimitiveCircuit (q+1)) := do
  let steps ← soLog A
  emitSteps steps

theorem compileGray_eval {q : ℕ} (A : StoredMatrix (2^(q+1)) (2^(q+1)))
    (hO : (denote A).transpose * denote A=1) (hD : (denote A).det=1) :
    evalPrimitiveCircuit (compileGray A).value =
      GrayGivensCompiler.transport (GrayBasis.equiv (q+1)) (denote A) := by
  simp only [compileGray, bind, Run.bind]
  rw [emitSteps_eval, soLog_value, decomposeSO_matrix (denote A) hO hD]

def gatesPerPlane (q : ℕ) : ℕ := 2^q+2*(2^q-1)

theorem plane_length {q : ℕ} (step : Step (2^(q+1))) :
    (plane step).value.length = gatesPerPlane q := by
  simp only [plane, realize_length, HermiteExplicitControlsCandidate.selected]
  exact StoredSelectedRyTrace.selected_length _ _ _ _

theorem emitSteps_length {q : ℕ} (steps : List (Step (2^(q+1)))) :
    (emitSteps steps).value.length = steps.length*gatesPerPlane q := by
  induction steps with
  | nil => simp [emitSteps, charge]
  | cons step rest ih =>
    simp [emitSteps, bind, Run.bind, charge, StoredSelectedRyTrace.append_value,
      plane_length, ih, Nat.add_mul]
    omega

theorem compileGray_gateCount {q : ℕ} (A : StoredMatrix (2^(q+1)) (2^(q+1))) :
    (compileGray A).value.gateCount =
      (2^(q+1)*(2^(q+1)-1)/2)*gatesPerPlane q := by
  simp only [compileGray, bind, Run.bind, PrimitiveCircuit.gateCount,
    emitSteps_length, soLog_value, decomposeSO_length]

private theorem total_add (a b : Cost) :
    StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a+StoredRectangularGivens.total b := by
  simp [StoredRectangularGivens.total]
  omega

private theorem total_tick (op : Op) : StoredRectangularGivens.total (tick op)=1 := by
  cases op <;> simp [StoredRectangularGivens.total, tick]

private theorem total_mono {a b : Cost} (h : ∀ op, a op ≤ b op) :
    StoredRectangularGivens.total a ≤ StoredRectangularGivens.total b := by
  dsimp only [StoredRectangularGivens.total]
  have hf := h .field
  have hs := h .sqrt
  have ha := h .angle
  have ht := h .trig
  have hc := h .compare
  have hr := h .read
  have hw := h .write
  have he := h .emit
  omega

theorem target_total_cost_le {q : ℕ} (step : Step (2^(q+1))) :
    StoredRectangularGivens.total (target step).cost ≤ 4*(q+1)+1 := by
  have bound := HermiteGrayTargetCandidate.discover_cost
    (q+1) step.first step.second step.adjacent
  simp [target, StoredRectangularGivens.total, tick]
  omega

def realizationBudget (count : ℕ) : Cost := fun op =>
  count*(tick .read op+2*tick .field op+tick .emit op+tick .write op)+tick .read op

theorem realize_cost_le {n : ℕ} (angle : ℝ) (trace : List (SelectedRyTrace.Gate n)) (op : Op) :
    (realize angle trace).cost op ≤ realizationBudget trace.length op := by
  induction trace with
  | nil => simp [realize, charge, realizationBudget]
  | cons gate rest ih =>
    cases gate <;>
      simp [realize, realizeGate, bind, pure, Run.bind, Run.pure, charge,
        StoredGivens.mul, realizationBudget] at * <;> nlinarith

theorem realize_total_cost_le {n : ℕ} (angle : ℝ) (trace : List (SelectedRyTrace.Gate n)) :
    StoredRectangularGivens.total (realize angle trace).cost ≤ 5*trace.length+1 := by
  have h := total_mono (realize_cost_le angle trace)
  have budget : StoredRectangularGivens.total (realizationBudget trace.length) =
      5*trace.length+1 := by
    simp [realizationBudget, StoredRectangularGivens.total, tick]
    ring
  rw [budget] at h
  exact h

theorem soLog_length {N : ℕ} (A : StoredMatrix N N) :
    (soLog A).value.length = N*(N-1)/2 := by rw [soLog_value, decomposeSO_length]

theorem soLog_total_cost_le {N : ℕ} (A : StoredMatrix N N) :
    StoredRectangularGivens.total (soLog A).cost ≤ 26*N^3+30*N^2+N+1 := by
  have hs := total_mono (StoredRectangularGivens.sweep_cost_le A 0 N (by omega))
  have hlen : (StoredRectangularGivens.sweep A 0 N (by omega)).value.steps.length ≤ N*N := by
    rw [StoredRectangularGivens.sweep_steps]
    exact RectangularGivens.decompose_length_le (denote A)
  have hr : StoredRectangularGivens.total
      (reverseInverse (StoredRectangularGivens.sweep A 0 N (by omega)).value.steps []).cost =
      7*(StoredRectangularGivens.sweep A 0 N (by omega)).value.steps.length+1 := by
    simp [StoredRectangularGivens.total, reverseInverse_cost, tick]
    ring
  simp only [soLog, total_add, hr]
  simp [StoredRectangularGivens.total, StoredRectangularGivens.columnBudget,
    stepBudget, eliminationBudget, coefficientBudget, angleBudget, tick] at hs
  simp only [StoredRectangularGivens.total]
  nlinarith

def planeBudget (q : ℕ) : ℕ :=
  (16*q+12)*2^q+5*q^2+14*q+8*(q+1)*(q+10)+4*(q+1)+5*gatesPerPlane q+5

theorem plane_total_cost_le {q : ℕ} (step : Step (2^(q+1))) :
    StoredRectangularGivens.total (plane step).cost ≤ planeBudget q := by
  have ht := target_total_cost_le step
  have hw := HermiteGrayTargetCandidate.word_total_cost_le (q+1) step.first
  have hs := HermiteExplicitControlsCandidate.selected_total_cost_le (target step).value
    (HermiteGrayTargetCandidate.word (q+1) step.first).value
  have length : (HermiteExplicitControlsCandidate.selected (target step).value
      (HermiteGrayTargetCandidate.word (q+1) step.first).value).value.length = gatesPerPlane q := by
    simp only [HermiteExplicitControlsCandidate.selected]
    exact StoredSelectedRyTrace.selected_length _ _ _ _
  have actual angle := realize_total_cost_le angle
    (HermiteExplicitControlsCandidate.selected (target step).value
      (HermiteGrayTargetCandidate.word (q+1) step.first).value).value
  simp only [length] at actual
  simp only [plane, total_add]
  by_cases hb : (HermiteGrayTargetCandidate.word (q+1) step.first).value[(target step).value.val]=0
  all_goals simp [StoredGivens.read, charge, hb, StoredGivens.sub, total_tick, total_add]
  all_goals dsimp only [planeBudget]
  all_goals have h := actual step.angle
  all_goals have h' := actual (-step.angle)
  all_goals nlinarith

def emissionBudget (q : ℕ) : ℕ := planeBudget q+2*gatesPerPlane q+2

theorem emitSteps_total_cost_le {q : ℕ} (steps : List (Step (2^(q+1)))) :
    StoredRectangularGivens.total (emitSteps steps).cost ≤ steps.length*emissionBudget q+1 := by
  induction steps with
  | nil => simp [emitSteps, charge, total_tick]
  | cons step rest ih =>
    have hp := plane_total_cost_le step
    have ha : StoredRectangularGivens.total
        (StoredSelectedRyTrace.append (plane step).value (emitSteps rest).value).cost =
        2*gatesPerPlane q+1 := by
      simp [StoredRectangularGivens.total, StoredSelectedRyTrace.append_cost, plane_length, tick]
      ring
    simp only [emitSteps, bind, Run.bind, charge, total_add, total_tick, ha]
    simp only [List.length_cons, emissionBudget] at ih ⊢
    nlinarith

def compilerBudget (q : ℕ) : ℕ :=
  let N := 2^(q+1)
  26*N^3+30*N^2+N+1+N^2*emissionBudget q+1

theorem compileGray_total_cost_le {q : ℕ} (A : StoredMatrix (2^(q+1)) (2^(q+1))) :
    StoredRectangularGivens.total (compileGray A).cost ≤ compilerBudget q := by
  have hl : (soLog A).value.length ≤ (2^(q+1))^2 := by
    rw [soLog_value, decomposeSO_length]
    have hdiv := Nat.div_le_self (2^(q+1)*(2^(q+1)-1)) 2
    have hprod := Nat.mul_le_mul_left (2^(q+1)) (Nat.sub_le (2^(q+1)) 1)
    nlinarith
  have hs := soLog_total_cost_le A
  have he := emitSteps_total_cost_le (soLog A).value
  have hm := Nat.mul_le_mul_right (emissionBudget q) hl
  simp only [compileGray, bind, Run.bind, total_add, compilerBudget]
  omega

private def Transcendental (op : Op) : Prop := op=.sqrt ∨ op=.angle ∨ op=.trig

private theorem head_quiet (index : ℕ) (op : Op) (ho : Transcendental op) :
    (HermiteGrayTargetCandidate.head index).cost op=0 := by
  rcases ho with rfl | rfl | rfl
  all_goals by_cases hp : index/2%2=0
  all_goals simp [HermiteGrayTargetCandidate.head, bind, pure, Run.bind, Run.pure,
    charge, tick, hp]

private theorem bit_quiet (n : ℕ) (index : Fin (2^n)) (wire : Fin n)
    (op : Op) (ho : Transcendental op) :
    (HermiteGrayTargetCandidate.bit n index wire).cost op=0 := by
  induction n with
  | zero => exact Fin.elim0 wire
  | succ n ih =>
    refine Fin.cases ?_ (fun rest => ?_) wire
    · exact head_quiet index.val op ho
    · simp only [HermiteGrayTargetCandidate.bit, Fin.cases_succ, bind, Run.bind, charge,
        Pi.add_apply, ih]
      rcases ho with rfl | rfl | rfl <;> simp [tick]

private theorem word_quiet (n : ℕ) (index : Fin (2^n)) (op : Op) (ho : Transcendental op) :
    (HermiteGrayTargetCandidate.word n index).cost op=0 := by
  simp only [HermiteGrayTargetCandidate.word, collect_cost, bit_quiet n index _ op ho,
    Finset.sum_const_zero, zero_add]
  rcases ho with rfl | rfl | rfl <;> simp [tick]

private theorem selected_quiet {q : ℕ} (target : Fin (q+1)) (bits : Vector (Fin 2) (q+1))
    (op : Op) (ho : Transcendental op) :
    (HermiteExplicitControlsCandidate.selected target bits).cost op=0 := by
  have encoding := StoredSelectedRyTrace.encodingCost_bound q op
  have trace := StoredSelectedRyTrace.traceCost_unused q
  rcases ho with rfl | rfl | rfl
  all_goals simp [tick] at encoding
  all_goals simp [HermiteExplicitControlsCandidate.selected,
    HermiteExplicitControlsCandidate.wires_cost, HermiteExplicitControlsCandidate.pattern_cost,
    StoredSelectedRyTrace.selected_cost, tick, encoding, trace.1,
    trace.2.1, trace.2.2.1]

private theorem realize_quiet {n : ℕ} (angle : ℝ) (trace : List (SelectedRyTrace.Gate n))
    (op : Op) (ho : Transcendental op) : (realize angle trace).cost op=0 := by
  have h := realize_cost_le angle trace op
  rcases ho with rfl | rfl | rfl
  all_goals simpa [realizationBudget, tick] using Nat.eq_zero_of_le_zero h

private theorem plane_quiet {q : ℕ} (step : Step (2^(q+1)))
    (op : Op) (ho : Transcendental op) : (plane step).cost op=0 := by
  simp only [plane, Pi.add_apply, word_quiet _ _ op ho,
    selected_quiet _ _ op ho, realize_quiet _ _ op ho, add_zero]
  rcases ho with rfl | rfl | rfl
  all_goals simp [target, StoredGivens.read, charge, StoredGivens.sub, tick]
  all_goals split_ifs <;> simp [tick]

private theorem emitSteps_quiet {q : ℕ} (steps : List (Step (2^(q+1))))
    (op : Op) (ho : Transcendental op) : (emitSteps steps).cost op=0 := by
  induction steps with
  | nil => rcases ho with rfl | rfl | rfl <;> simp [emitSteps, charge, tick]
  | cons step rest ih =>
    simp only [emitSteps, bind, Run.bind, charge, Pi.add_apply, plane_quiet step op ho,
      ih, StoredSelectedRyTrace.append_cost]
    rcases ho with rfl | rfl | rfl <;> simp [tick]

theorem compileGray_transcendental_cost_le {q : ℕ}
    (A : StoredMatrix (2^(q+1)) (2^(q+1))) :
    (compileGray A).cost .sqrt ≤ (2^(q+1))^2 ∧
    (compileGray A).cost .angle ≤ (2^(q+1))^2 ∧
    (compileGray A).cost .trig ≤ 2*(2^(q+1))^2 := by
  have equal (op : Op) (ho : Transcendental op) :
      (compileGray A).cost op = (StoredRectangularGivens.sweep A 0 (2^(q+1)) (by omega)).cost op := by
    simp only [compileGray, bind, Run.bind, Pi.add_apply, emitSteps_quiet _ op ho,
      add_zero, soLog, reverseInverse_cost]
    rcases ho with rfl | rfl | rfl <;> simp [tick]
  have hs := StoredRectangularGivens.sweep_cost_le A 0 (2^(q+1)) (by omega) .sqrt
  have ha := StoredRectangularGivens.sweep_cost_le A 0 (2^(q+1)) (by omega) .angle
  have ht := StoredRectangularGivens.sweep_cost_le A 0 (2^(q+1)) (by omega) .trig
  rw [equal .sqrt (Or.inl rfl), equal .angle (Or.inr (Or.inl rfl)),
    equal .trig (Or.inr (Or.inr rfl))]
  simp [StoredRectangularGivens.columnBudget, stepBudget, eliminationBudget,
    coefficientBudget, angleBudget, tick] at hs ha ht
  constructor
  · nlinarith
  constructor <;> nlinarith

theorem realize_emit {n : ℕ} (angle : ℝ) (trace : List (SelectedRyTrace.Gate n)) :
    (realize angle trace).cost .emit = trace.length := by
  induction trace with
  | nil => simp [realize, charge, tick]
  | cons gate rest ih =>
    cases gate <;> simp [realize, realizeGate, bind, pure, Run.bind, Run.pure,
      charge, StoredGivens.mul, tick, ih]

private theorem head_emit_zero (index : ℕ) :
    (HermiteGrayTargetCandidate.head index).cost .emit=0 := by
  by_cases hp : index/2%2=0
  all_goals simp [HermiteGrayTargetCandidate.head, bind, pure, Run.bind, Run.pure,
    charge, tick, hp]

private theorem bit_emit_zero (n : ℕ) (index : Fin (2^n)) (wire : Fin n) :
    (HermiteGrayTargetCandidate.bit n index wire).cost .emit=0 := by
  induction n with
  | zero => exact Fin.elim0 wire
  | succ n ih =>
    refine Fin.cases ?_ (fun rest => ?_) wire
    · exact head_emit_zero index.val
    · simp [HermiteGrayTargetCandidate.bit, bind, Run.bind, charge, ih, tick]

private theorem word_emit_zero (n : ℕ) (index : Fin (2^n)) :
    (HermiteGrayTargetCandidate.word n index).cost .emit=0 := by
  simp [HermiteGrayTargetCandidate.word, collect_cost, bit_emit_zero, tick]

theorem plane_emit {q : ℕ} (step : Step (2^(q+1))) :
    (plane step).cost .emit=2*gatesPerPlane q := by
  have selected : (HermiteExplicitControlsCandidate.selected (target step).value
      (HermiteGrayTargetCandidate.word (q+1) step.first).value).cost .emit=gatesPerPlane q := by
    simp only [HermiteExplicitControlsCandidate.selected, Pi.add_apply,
      HermiteExplicitControlsCandidate.wires_cost, HermiteExplicitControlsCandidate.pattern_cost]
    rw [StoredSelectedRyTrace.selected_emit, StoredSelectedRyTrace.selected_length]
    simp [tick, gatesPerPlane]
  simp only [plane, Pi.add_apply, word_emit_zero, realize_emit, selected]
  have length : (HermiteExplicitControlsCandidate.selected (target step).value
      (HermiteGrayTargetCandidate.word (q+1) step.first).value).value.length=gatesPerPlane q := by
    simp only [HermiteExplicitControlsCandidate.selected]
    exact StoredSelectedRyTrace.selected_length _ _ _ _
  simp only [length]
  simp [target, StoredGivens.read, charge, StoredGivens.sub, tick, gatesPerPlane]
  split_ifs <;> simp [tick] <;> omega

theorem emitSteps_emit {q : ℕ} (steps : List (Step (2^(q+1)))) :
    (emitSteps steps).cost .emit=2*(steps.length*gatesPerPlane q) := by
  induction steps with
  | nil => simp [emitSteps, charge, tick]
  | cons step rest ih =>
    simp [emitSteps, bind, Run.bind, charge, plane_emit, ih,
      StoredSelectedRyTrace.append_cost, tick, Nat.add_mul]
    ring

theorem sweep_emit {N M : ℕ} (A : StoredMatrix N M) (k remaining : ℕ)
    (columns : k+remaining≤M) :
    (StoredRectangularGivens.sweep A k remaining columns).cost .emit =
      (StoredRectangularGivens.sweep A k remaining columns).value.steps.length := by
  induction remaining generalizing A k with
  | zero => simp [StoredRectangularGivens.sweep, pure, Run.pure]
  | succ remaining ih =>
    by_cases h : k<N
    · simp only [StoredRectangularGivens.sweep, dif_pos h, bind, pure, Run.bind,
        Run.pure, StoredRectangularGivens.append, Pi.add_apply, add_zero,
        List.length_append, StoredGivens.columnSweep_emit,
        StoredGivens.columnSweep_steps_length, ih]
      simp [tick]
    · simp only [StoredRectangularGivens.sweep, dif_neg h, Pi.add_apply, ih]
      simp [tick]

theorem soLog_emit {N : ℕ} (A : StoredMatrix N N) :
    (soLog A).cost .emit=N*(N-1)/2 := by
  simp only [soLog, Pi.add_apply, reverseInverse_cost, sweep_emit]
  simp only [tick]
  rw [StoredRectangularGivens.sweep_steps, rectangular_full_steps]
  have length := decomposeSO_length (denote A)
  simpa [decomposeSO] using length

/-- The ledger includes intermediate sweep records and rational-template
records, not just the final primitive instruction list. -/
theorem compileGray_emit {q : ℕ} (A : StoredMatrix (2^(q+1)) (2^(q+1))) :
    (compileGray A).cost .emit =
      (2^(q+1)*(2^(q+1)-1)/2)*(1+2*gatesPerPlane q) := by
  simp only [compileGray, bind, Run.bind, Pi.add_apply, soLog_emit, emitSteps_emit,
    soLog_length]
  ring

/-! Small regressions exercise the actual output interfaces; no deficient
matrix is falsely presented as SO. -/
example (A : StoredMatrix 0 0) : (soLog A).value=[] := by
  simp [soLog_value, decomposeSO, fullSweepSteps]

example (A : StoredMatrix 1 1) : (soLog A).value=[] := by
  simp [soLog_value, decomposeSO, fullSweepSteps]

example : (emitSteps ([] : List (Step (2^(0+1))))).value=[] := rfl

example : (StoredGivens.angle 0 0).value=0 := by
  simp [StoredGivens.angle, StoredGivens.mul, StoredGivens.add, StoredGivens.sqrt,
    zeroTest, bind, pure, Run.bind, Run.pure, charge]

def regression01 : Step 4 := ⟨0, 1, by decide, 3⟩
def regression23 : Step 4 := ⟨2, 3, by decide, 5⟩

example : (reverseInverse [regression01, regression23] []).value=
    [regression23.inverse, regression01.inverse] := by
  rw [reverseInverse_value]
  rfl

example : (HermiteGrayTargetCandidate.word 2 regression23.first).value[
    (target regression23).value.val]=1 := by native_decide

example (A : StoredMatrix 2 2) : (compileGray (q:=0) A).value.gateCount=1 := by
  rw [compileGray_gateCount]
  norm_num [gatesPerPlane]

example (A : StoredMatrix 4 4) : (compileGray (q:=1) A).value.gateCount=24 := by
  rw [compileGray_gateCount]
  norm_num [gatesPerPlane]

noncomputable def regressionSigned : StoredMatrix 2 2 := #v[#v[0,-1],#v[1,0]]

theorem regressionSigned_orthogonal :
    (denote regressionSigned).transpose * denote regressionSigned=1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [regressionSigned, denote, Matrix.mul_apply, Fin.sum_univ_two]

theorem regressionSigned_det : (denote regressionSigned).det=1 := by
  norm_num [regressionSigned, denote, Matrix.det_fin_two]

example : evalPrimitiveCircuit (compileGray (q:=0) regressionSigned).value=
    GrayGivensCompiler.transport (GrayBasis.equiv 1) (denote regressionSigned) :=
  compileGray_eval (q:=0) regressionSigned regressionSigned_orthogonal regressionSigned_det

#print axioms compileGray_eval
#print axioms compileGray_gateCount
#print axioms compileGray_total_cost_le
#print axioms compileGray_transcendental_cost_le
#print axioms emitSteps_emit
#print axioms compileGray_emit

end QuantumBlockEncoding.StagedLocalSOEmission
