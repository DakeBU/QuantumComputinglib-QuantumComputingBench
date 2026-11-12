import QuantumBlockEncoding.StoredHermiteRawCost
import QuantumBlockEncoding.StoredTensorTrainNorm
import QuantumBlockEncoding.ConstructiveTensorTrainCompiler

/-!
Staged same-run normalized signed-unit-boundary supplier.
Contract: normalized-canonical-contract.json (sealed before proof search).
No primitive compilation or finite-bit runtime claim. Each actual producer is
bound once; the raw extraordinary counters are carried through unchanged.
-/

namespace QuantumBlockEncoding.StagedNormalizedCanonical

set_option maxHeartbeats 20000

open scoped BigOperators
open StoredGivens StoredTensorTrain TensorTrainCanonical
open StoredHermiteRawSource

private theorem bind_value (x : Run α) (f : α → Run β) :
    (x >>= f).value = (f x.value).value := rfl

/-- Scalar supplier adapter; this is the actual charged first-core operation. -/
noncomputable def normalizeWith {n : ℕ} (z : ℝ) (C : StoredChain (n+1) 1 1) :
    Run (StoredChain (n+1) 1 1) := do
  let inverse ← StoredGivens.div 1 z
  let left ← charge .write (#v[inverse] : Vector ℝ 1)
  StoredMatrixProductChain.closeLeft left C

/-- Normalize only the first core. The tail's stored core references are shared. -/
noncomputable def normalize {n : ℕ} (C : StoredChain (n+1) 1 1) :
    Run (StoredChain (n+1) 1 1) := do
  let z ← StoredTensorTrainNorm.norm C
  normalizeWith z C

noncomputable def semanticNormalized {n : ℕ} (C : StoredChain (n+1) 1 1) :
    Chain (n+1) 1 1 :=
  MatrixProductChain.closeLeft
    (fun _ => 1 / TensorTrainNormEnvironment.norm (denoteChain C)) (denoteChain C)

theorem normalizeWith_value {n : ℕ} (z : ℝ) (C : StoredChain (n+1) 1 1) :
    denoteChain (normalizeWith z C).value =
      MatrixProductChain.closeLeft (fun _ => 1/z) (denoteChain C) := by
  have singleton : (fun i : Fin 1 => (#v[1/z] : Vector ℝ 1)[i.val]) =
      (fun _ : Fin 1 => 1/z) := by
    funext i
    fin_cases i
    rfl
  change denoteChain (StoredMatrixProductChain.closeLeft (#v[1/z] : Vector ℝ 1) C).value = _
  rw [StoredMatrixProductChain.closeLeft_value, singleton]

theorem normalize_value {n : ℕ} (C : StoredChain (n+1) 1 1) :
    denoteChain (normalize C).value = semanticNormalized C := by
  rw [normalize, bind_value, normalizeWith_value]
  exact congrArg (fun z : ℝ => MatrixProductChain.closeLeft (fun _ => 1/z) (denoteChain C))
    (StoredTensorTrainNorm.norm_value C)

theorem normalize_contract {n : ℕ} (C : StoredChain (n+1) 1 1) (x : Word (n+1)) :
    contract (denoteChain (normalize C).value) x 0 0 =
      contract (denoteChain C) x 0 0 /
        TensorTrainNormEnvironment.norm (denoteChain C) := by
  rw [normalize_value, semanticNormalized, MatrixProductChain.closeLeft_contract]
  simp [div_eq_mul_inv, mul_comm]

theorem normalize_maxBond {n : ℕ} (C : StoredChain (n+1) 1 1) :
    maxBond (denoteChain (normalize C).value) = maxBond (denoteChain C) := by
  rw [normalize_value]
  cases C with
  | cons A C => rfl

theorem normalize_normalized {n : ℕ} (C : StoredChain (n+1) 1 1)
    (hz : TensorTrainNormEnvironment.norm (denoteChain C) ≠ 0) :
    (∑ x : Word (n+1), contract (denoteChain (normalize C).value) x 0 0 ^ 2) = 1 := by
  simp_rw [normalize_contract, div_pow]
  rw [← Finset.sum_div, ← TensorTrainNormEnvironment.norm_sq]
  exact div_self (pow_ne_zero 2 hz)

/-- Consume exactly the returned canonicalization data. The signed residual
row is read, not replaced by its norm or regenerated from semantic callbacks. -/
noncomputable def unitBoundaryStored {n : ℕ} (C : StoredChain (n+1) 1 1) :
    Run (StoredChain (n+1) 1 1) := do
  let result ← canonicalize C
  let left ← StoredGivens.read result.residual 0
  StoredMatrixProductChain.closeLeft left result.canonical

private theorem semantic_closeLeft_eq_absorb {n l : ℕ} (u : Fin l → ℝ)
    (C : Chain (n+1) l 1) :
    MatrixProductChain.closeLeft u C = ConstructiveTensorTrainCompiler.absorbBoundary u C := by
  cases C with
  | cons A C => rfl

theorem unitBoundaryStored_value {n : ℕ} (C : StoredChain (n+1) 1 1) :
    denoteChain (unitBoundaryStored C).value =
      ConstructiveTensorTrainCompiler.unitBoundary (denoteChain C) := by
  simp only [unitBoundaryStored, bind_value, StoredGivens.read, charge,
    StoredMatrixProductChain.closeLeft_value]
  rw [semantic_closeLeft_eq_absorb]
  let view (result : ConstructiveTensorTrain.Result (denoteChain C)) : Chain (n+1) 1 1 :=
    ConstructiveTensorTrainCompiler.absorbBoundary (fun a => result.residual 0 a) result.canonical
  change view (canonicalize C).value.toSemantic = _
  rw [canonicalize_refines C]
  dsimp only [view, ConstructiveTensorTrainCompiler.unitBoundary]
  congr 1
  funext a
  simp [ConstructiveTensorTrain.stateBoundary, ConstructiveTensorTrain.boundary,
    _root_.Matrix.vecMul, dotProduct]

theorem unitBoundaryStored_contract {n : ℕ} (C : StoredChain (n+1) 1 1)
    (x : Word (n+1)) :
    contract (denoteChain (unitBoundaryStored C).value) x 0 0 =
      contract (denoteChain C) x 0 0 := by
  rw [unitBoundaryStored_value]
  exact ConstructiveTensorTrainCompiler.unitBoundary_contract (denoteChain C) x

theorem unitBoundaryStored_canonical {n : ℕ} (C : StoredChain (n+1) 1 1)
    (hNorm : (∑ x : Word (n+1), contract (denoteChain C) x 0 0 ^ 2) = 1) :
    RightCanonical (denoteChain (unitBoundaryStored C).value) := by
  rw [unitBoundaryStored_value]
  exact ConstructiveTensorTrainCompiler.unitBoundary_canonical _ hNorm

theorem unitBoundaryStored_maxBond {n : ℕ} (C : StoredChain (n+1) 1 1) :
    maxBond (denoteChain (unitBoundaryStored C).value) ≤ maxBond (denoteChain C) := by
  rw [unitBoundaryStored_value]
  exact ConstructiveTensorTrainCompiler.unitBoundary_maxBond_le _

noncomputable def compile (k n : ℕ) (L : ℝ) : RawRun (StoredChain (n+1) 1 1) :=
  let source := raw k n L
  let normalized := normalize source.run.value
  let prepared := unitBoundaryStored normalized.value
  { run := ⟨prepared.value, source.run.cost + normalized.cost + prepared.cost⟩
    exponentialCalls := source.exponentialCalls
    quotientCalls := source.quotientCalls
    remainderCalls := source.remainderCalls
    integerDoublings := source.integerDoublings
    integerAdditions := source.integerAdditions }

theorem compile_value (k n : ℕ) (L : ℝ) :
    denoteChain (compile k n L).run.value =
      ConstructiveTensorTrainCompiler.unitBoundary
        (semanticNormalized (raw k n L).run.value) := by
  change denoteChain (unitBoundaryStored (normalize (raw k n L).run.value).value).value = _
  rw [unitBoundaryStored_value, normalize_value]

theorem raw_norm (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    TensorTrainNormEnvironment.norm (denoteChain (raw k n L).run.value) =
      HermiteStatePreparation.sampleNorm k (n+1) L := by
  rw [raw_value k n L hL]
  exact HermiteExplicitBond.rawSourceChain_norm k n L hL

theorem raw_maxBond (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    maxBond (denoteChain (raw k n L).run.value) ≤ 2*k+6 := by
  rw [raw_value k n L hL]
  exact HermiteExplicitBond.rawSourceChain_maxBond k n L

theorem compile_contract (k n : ℕ) (L : ℝ) (hL : 0 < L) (x : Word (n+1)) :
    contract (denoteChain (compile k n L).run.value) x 0 0 =
      HermiteStatePreparation.sampledAmplitude k (n+1) L
        (TensorTrainWord.sampleEquiv (n+1) x) /
      HermiteStatePreparation.sampleNorm k (n+1) L := by
  change contract (denoteChain (unitBoundaryStored (normalize (raw k n L).run.value).value).value)
    x 0 0 = _
  rw [unitBoundaryStored_contract, normalize_contract, raw_contract k n L hL,
    raw_norm k n L hL]

theorem compile_canonical (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    RightCanonical (denoteChain (compile k n L).run.value) := by
  apply unitBoundaryStored_canonical
  apply normalize_normalized
  rw [raw_norm k n L hL]
  exact ne_of_gt (HermiteStatePreparation.sampleNorm_pos k (n+1) L)

theorem compile_maxBond (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    maxBond (denoteChain (compile k n L).run.value) ≤ 2*k+6 := by
  exact (unitBoundaryStored_maxBond _).trans
    (by rw [normalize_maxBond]; exact raw_maxBond k n L hL)

private theorem total_add (a b : Cost) :
    StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  rw [← StoredHermiteRawCost.ordinary_eq_total,
    StoredHermiteRawCost.ordinary_add,
    StoredHermiteRawCost.ordinary_eq_total,
    StoredHermiteRawCost.ordinary_eq_total]

private theorem total_tick (op : Op) : StoredRectangularGivens.total (tick op) = 1 := by
  rw [← StoredHermiteRawCost.ordinary_eq_total, StoredHermiteRawCost.ordinary_tick]

private theorem node_total : StoredRectangularGivens.total nodeBudget = 6 := by
  simp [nodeBudget, StoredRectangularGivens.total, tick]

/-- Scalar or at-most-scalar left boundary. The actual first-core contraction,
full materialization and chain-node allowance are all included. -/
theorem closeLeft_total_cost_le {n l : ℕ} (left : Vector ℝ l)
    (C : StoredChain (n+1) l 1) (D : ℕ) (hl : l ≤ 1)
    (bound : maxBond (denoteChain C) ≤ D) :
    StoredRectangularGivens.total (StoredMatrixProductChain.closeLeft left C).cost ≤
      18*D+10 := by
  cases C with
  | @cons n l m r A C =>
    have ht : maxBond (denoteChain C) ≤ D := (max_le_iff.mp bound).2
    have hm : m ≤ D := by
      cases C with
      | nil r => exact ht
      | cons B C => exact (max_le_iff.mp ht).1
    simp only [StoredMatrixProductChain.closeLeft, bind, Run.bind, total_add,
      StoredMatrixProductChain.initial_total_cost, node_total]
    have hmul : m*l ≤ D := (Nat.mul_le_mul_left m hl).trans (by simpa using hm)
    nlinarith

def normBudget (n D : ℕ) : ℕ :=
  (n+1)*(24*D^3 + 25*D^2 + 20*D + 6) + 5*D^2 + 4*D + 9

def canonicalBudget (n D : ℕ) : ℕ :=
  (n+1)*(176*D^3 + 116*D^2 + 29*D + 8) + 5*D^2 + 4*D + 6

theorem normalize_total_cost_le {n : ℕ} (C : StoredChain (n+1) 1 1) (D : ℕ)
    (bound : maxBond (denoteChain C) ≤ D) :
    StoredRectangularGivens.total (normalize C).cost ≤ normBudget n D + 18*D+12 := by
  have hn := StoredTensorTrainNorm.norm_total_cost_le C D bound
  have hc := closeLeft_total_cost_le
    (#v[1 / (StoredTensorTrainNorm.norm C).value] : Vector ℝ 1) C D le_rfl bound
  simp only [normalize, normalizeWith, bind, Run.bind, StoredGivens.div, charge,
    total_add, total_tick]
  unfold normBudget
  omega

theorem unitBoundaryStored_total_cost_le {n : ℕ} (C : StoredChain (n+1) 1 1)
    (D : ℕ) (bound : maxBond (denoteChain C) ≤ D) :
    StoredRectangularGivens.total (unitBoundaryStored C).cost ≤
      canonicalBudget n D + 18*D+11 := by
  have hk := canonicalize_total_cost_le C D bound
  have hc := closeLeft_total_cost_le (canonicalize C).value.residual[0]
    (canonicalize C).value.canonical D (canonicalize C).value.rank_le
    ((canonicalize_maxBond_le C).trans bound)
  simp only [unitBoundaryStored, bind, Run.bind, StoredGivens.read, charge,
    total_add, total_tick, Fin.val_zero]
  unfold canonicalBudget
  omega

def compilerBudget (k n : ℕ) : ℕ :=
  StoredHermiteRawCost.rawBudget k n +
    (n+1)*(200*(2*k+6)^3 + 141*(2*k+6)^2 + 49*(2*k+6) + 14) +
    10*(2*k+6)^2 + 44*(2*k+6) + 100

/-- Same-returned-object ordinary work. No hypothetical input callbacks or
zero-cost raw source are substituted for the actual supplier ledgers. -/
theorem compile_total_cost_le (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    StoredHermiteRawCost.ordinary (compile k n L).run.cost ≤ compilerBudget k n := by
  have hr := StoredHermiteRawCost.raw_stored_total_cost_le k n L
  have hn := normalize_total_cost_le (raw k n L).run.value (2*k+6)
    (raw_maxBond k n L hL)
  have hb : maxBond (denoteChain (normalize (raw k n L).run.value).value) ≤ 2*k+6 := by
    rw [normalize_maxBond]
    exact raw_maxBond k n L hL
  have hc := unitBoundaryStored_total_cost_le
    (normalize (raw k n L).run.value).value (2*k+6) hb
  rw [StoredHermiteRawCost.ordinary_eq_total]
  simp only [compile, total_add]
  have budget : compilerBudget k n = StoredHermiteRawCost.rawBudget k n +
      normBudget n (2*k+6) + canonicalBudget n (2*k+6) + 36*(2*k+6) + 85 := by
    unfold compilerBudget normBudget canonicalBudget
    ring
  rw [budget]
  omega

theorem compile_extraCounters (k n : ℕ) (L : ℝ) :
    (compile k n L).exponentialCalls = (raw k n L).exponentialCalls ∧
    (compile k n L).quotientCalls = (n+1)*(n+2) ∧
    (compile k n L).remainderCalls = (n+1)^2 ∧
    (compile k n L).integerDoublings = n ∧
    (compile k n L).integerAdditions = 4*(n+1) :=
  ⟨rfl, StoredHermiteRawCost.raw_quotientCalls k n L,
    StoredHermiteRawCost.raw_remainderCalls k n L,
    StoredHermiteRawCost.raw_integerDoublings k n L,
    StoredHermiteRawCost.raw_integerAdditions k n L⟩

/-- Sealed source-facing frontier node. Right-canonicity, normalized source
action, bond bound and cost all concern this one actual returned chain. -/
theorem compile_certified (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    let result := compile k n L
    RightCanonical (denoteChain result.run.value) ∧
    maxBond (denoteChain result.run.value) ≤ 2*k+6 ∧
    (∀ x : Word (n+1), contract (denoteChain result.run.value) x 0 0 =
      HermiteStatePreparation.sampledAmplitude k (n+1) L
        (TensorTrainWord.sampleEquiv (n+1) x) /
        HermiteStatePreparation.sampleNorm k (n+1) L) ∧
    StoredHermiteRawCost.ordinary result.run.cost ≤ compilerBudget k n ∧
    result.exponentialCalls ≤ 3*(n+1)+1 ∧
    result.quotientCalls = (n+1)*(n+2) ∧ result.remainderCalls = (n+1)^2 ∧
    result.integerDoublings = n ∧ result.integerAdditions = 4*(n+1) := by
  exact ⟨compile_canonical k n L hL, compile_maxBond k n L hL,
    compile_contract k n L hL, compile_total_cost_le k n L hL,
    StoredHermiteRawCost.raw_exponentialCalls_le k n L,
    (compile_extraCounters k n L).2⟩

namespace Tests

set_option backward.isDefEq.respectTransparency false

def signedCore : StoredCore 1 1 :=
  Vector.ofFn (fun _ => Vector.ofFn (fun j : Fin 2 => if j = 0 then -3 else 4))

def signedState : StoredChain 1 1 1 := .cons signedCore (.nil 1)

theorem signedNorm : TensorTrainNormEnvironment.norm (denoteChain signedState) = 5 := by
  norm_num [signedState, denoteChain, TensorTrainNormEnvironment.norm,
    TensorTrainNormEnvironment.gram, slice, denoteCore, signedCore, denote,
    _root_.Matrix.mul_apply, finProdFinEquiv, Fin.sum_univ_two]

/-- Negative amplitudes survive both first-core scaling and canonical boundary absorption. -/
example : contract (denoteChain (unitBoundaryStored (normalize signedState).value).value)
    ((0, ()) : Word 1) 0 0 = -3/5 := by
  rw [unitBoundaryStored_contract, normalize_contract, signedNorm]
  norm_num [signedState, denoteChain, contract, slice, denoteCore, signedCore,
    denote, _root_.Matrix.mul_apply, finProdFinEquiv]

example : contract (denoteChain (unitBoundaryStored (normalize signedState).value).value)
    ((1, ()) : Word 1) 0 0 = 4/5 := by
  rw [unitBoundaryStored_contract, normalize_contract, signedNorm]
  norm_num [signedState, denoteChain, contract, slice, denoteCore, signedCore,
    denote, _root_.Matrix.mul_apply, finProdFinEquiv]

example : RightCanonical
    (denoteChain (unitBoundaryStored (normalize signedState).value).value) := by
  apply unitBoundaryStored_canonical
  apply normalize_normalized
  rw [signedNorm]
  norm_num

def zeroCore (l r : ℕ) : StoredCore l r := Vector.replicate l (Vector.replicate (2*r) 0)
def zeroInterior : StoredChain 2 1 1 :=
  .cons (zeroCore 1 0) (.cons (zeroCore 0 1) (.nil 1))

/-- Zero inputs have literal generic producer behavior, not a falsely normalized certificate. -/
example : maxBond (denoteChain (normalize zeroInterior).value) = 1 := by
  rw [normalize_maxBond]
  simp [zeroInterior, denoteChain, maxBond]

example : StoredRectangularGivens.total (normalize zeroInterior).cost ≤ normBudget 1 1+30 := by
  exact normalize_total_cost_le zeroInterior 1 (by simp [zeroInterior, denoteChain, maxBond])

/-- Source specialization uses the actual one-data-bit returned chain. -/
example (k : ℕ) (L : ℝ) (hL : 0 < L) :
    RightCanonical (denoteChain (compile k 0 L).run.value) ∧
    maxBond (denoteChain (compile k 0 L).run.value) ≤ 2*k+6 :=
  ⟨compile_canonical k 0 L hL, compile_maxBond k 0 L hL⟩

example (k n : ℕ) (L : ℝ) (hL : 0 < L) :
    StoredHermiteRawCost.ordinary (compile k n L).run.cost ≤ compilerBudget k n :=
  compile_total_cost_le k n L hL

/-- Chronological 01/10 remain different source labels after normalization. -/
example (k : ℕ) (L : ℝ) (hL : 0 < L) :
    contract (denoteChain (compile k 1 L).run.value) ((0,1,()) : Word 2) 0 0 =
      HermiteStatePreparation.sampledAmplitude k 2 L ⟨1, by norm_num [gridSize]⟩ /
        HermiteStatePreparation.sampleNorm k 2 L := by
  rw [compile_contract k 1 L hL]
  congr 2

example (k : ℕ) (L : ℝ) (hL : 0 < L) :
    contract (denoteChain (compile k 1 L).run.value) ((1,0,()) : Word 2) 0 0 =
      HermiteStatePreparation.sampledAmplitude k 2 L ⟨2, by norm_num [gridSize]⟩ /
        HermiteStatePreparation.sampleNorm k 2 L := by
  rw [compile_contract k 1 L hL]
  congr 2

example (k : ℕ) (L : ℝ) : (compile k 0 L).quotientCalls = 2 ∧
    (compile k 0 L).remainderCalls = 1 ∧ (compile k 0 L).integerDoublings = 0 ∧
    (compile k 0 L).integerAdditions = 4 := by
  simpa using (compile_extraCounters k 0 L).2

end Tests

#print axioms normalize_value
#print axioms unitBoundaryStored_value
#print axioms compile_value
#print axioms compile_certified

end QuantumBlockEncoding.StagedNormalizedCanonical
