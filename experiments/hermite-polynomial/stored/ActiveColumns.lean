import NormalizedCanonical
import QuantumBlockEncoding.StoredIsometryCompletion
import QuantumBlockEncoding.ConstructiveIsometryLocal

/-! Staged charged active-column extraction. See active-columns-contract.json.
`Op.field` additionally charges the selected natural quotient/remainder and
multiply/add index operations here. This is NOT a finite-bit runtime bound.
The frozen normalized supplier is imported from an external compiler cache. -/

namespace QuantumBlockEncoding.StagedActiveColumns

set_option maxHeartbeats 40000

open scoped BigOperators
open StoredGivens StoredTensorTrain TensorTrainCanonical TensorTrainSchedule
open TensorTrainLocalCompiler ConstructiveIsometryLocal

/-- Numeric layout: bit*S+bond, two quotient/remainder operations. -/
def decode (q : ℕ) (row : Fin (2 * 2^q)) : Run (Fin 2 × Fin (2^q)) :=
  ⟨finProdFinEquiv.symm row, 2 • tick .field⟩

/-- Stored core layout: bit*m+bond, two multiply/add operations. -/
def flatten {m : ℕ} (out : Fin 2 × Fin m) : Run (Fin (2*m)) :=
  ⟨finProdFinEquiv out, 2 • tick .field⟩

def coreEntry {l m : ℕ} (A : StoredCore l m) (q : ℕ)
    (row : Fin (2*2^q)) (a : Fin l) : Run ℝ := do
  let out ← decode q row
  if hb : out.2.val < m then
    let col := flatten (out.1, ⟨out.2.val, hb⟩)
    let result := col >>= fun j => StoredThinLQ.entry A a j
    ⟨result.value, tick .compare + result.cost⟩
  else
    ⟨0, tick .compare⟩

def coreMatrix {l m : ℕ} (A : StoredCore l m) (q : ℕ) :
    Run (StoredMatrix (2*2^q) l) := materialize (coreEntry A q)

theorem coreMatrix_value {l m : ℕ} (A : StoredCore l m) (q : ℕ)
    (hl : l ≤ 2^q) :
    denote (coreMatrix A q).value = fun row a =>
      (paddedCore (denoteCore A) (finProdFinEquiv.symm row) (Fin.castLE hl a)).re := by
  ext row a
  simp [coreMatrix, materialize, denote, coreEntry, bind, Run.bind, decode,
    paddedCore, Fin.castLE, a.isLt, flatten, StoredThinLQ.entry, StoredGivens.read,
    charge, denoteCore, finProdFinEquiv]
  by_cases hb : row.val % 2^q < m <;> simp [hb]

def cellBudget : Cost := 4 • tick .field + 2 • tick .read + tick .compare

theorem coreEntry_cost_le {l m : ℕ} (A : StoredCore l m) (q : ℕ)
    (row : Fin (2*2^q)) (a : Fin l) (op : Op) :
    (coreEntry A q row a).cost op ≤ cellBudget op := by
  simp [coreEntry, bind, Run.bind, decode, flatten, StoredThinLQ.entry,
    StoredGivens.read, charge, cellBudget, finProdFinEquiv]
  split_ifs <;> simp_all <;> omega

def matrixBudget (q l : ℕ) : Cost := fun op =>
  (2*2^q*l) * cellBudget op + (2*2^q*l+2*2^q) *
    (2*tick .read op+2*tick .write op)

theorem coreMatrix_cost_le {l m : ℕ} (A : StoredCore l m) (q : ℕ) (op : Op) :
    (coreMatrix A q).cost op ≤ matrixBudget q l op := by
  have hsum : (∑ row : Fin (2*2^q), ∑ a : Fin l,
      (coreEntry A q row a).cost op) ≤ (2*2^q*l)*cellBudget op := by
    calc
      _ ≤ ∑ _row : Fin (2*2^q), ∑ _a : Fin l, cellBudget op :=
        Finset.sum_le_sum fun row _ => Finset.sum_le_sum fun a _ =>
          coreEntry_cost_le A q row a op
      _ = _ := by simp; ring
  simp only [coreMatrix, materialize_cost, matrixBudget]
  omega

/-- Read the three stored cons-node words at each visited stage. No head
entry callback is evaluated until the selected core is reached. -/
def extract : {n l r : ℕ} → (C : StoredChain n l r) → (q t : ℕ) → (ht : t<n) →
    Run (StoredMatrix (2*2^q) (rankAt (denoteChain C) t))
  | _, _, _, .nil _, _, _, ht => False.elim (Nat.not_lt_zero _ ht)
  | _, _, _, .cons A _, q, 0, _ =>
      let result := coreMatrix A q
      ⟨result.value, 3 • tick .read + result.cost⟩
  | _, _, _, .cons _ C, q, t+1, ht =>
      let result := extract C q t (by omega)
      ⟨result.value, 3 • tick .read + result.cost⟩

theorem extract_value {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    denote (extract C q t ht).value = fun row a =>
      activeColumns (denoteChain C) t hB ((coordinates q).symm row) a := by
  induction C generalizing t with
  | nil _ => omega
  | @cons n l m r A C ih =>
    cases t with
    | zero =>
      have hl : l ≤ 2^q := (le_max_left _ _).trans hB
      change denote (coreMatrix A q).value = _
      rw [coreMatrix_value A q hl]
      ext row a
      change (paddedCore (denoteCore A) (finProdFinEquiv.symm row)
        (Fin.castLE hl a)).re =
        (paddedCore (denoteCore A)
          ((localIndex q) ((localIndex q).symm (finProdFinEquiv.symm row)))
          (Fin.castLE hl a)).re
      rw [Equiv.apply_symm_apply]
    | succ t =>
      exact ih ((le_max_right _ _).trans hB) t (by omega)

def extractionBudget (q rank t : ℕ) : Cost :=
  matrixBudget q rank + (3*(t+1)) • tick .read

theorem extract_cost_le {n l r : ℕ} (C : StoredChain n l r)
    (q t : ℕ) (ht : t<n) (op : Op) :
    (extract C q t ht).cost op ≤
      extractionBudget q (rankAt (denoteChain C) t) t op := by
  induction C generalizing t with
  | nil _ => omega
  | @cons n l m r A C ih =>
    cases t with
    | zero =>
      have h := coreMatrix_cost_le A q op
      simp [extract, extractionBudget, rankAt, denoteChain] at *
      nlinarith
    | succ t =>
      have h := ih t (by omega)
      simp [extract, extractionBudget, rankAt, denoteChain] at *
      nlinarith

theorem extractionBudget_total (q rank t : ℕ) :
    StoredRectangularGivens.total (extractionBudget q rank t) =
      22*2^q*rank+8*2^q+3*(t+1) := by
  simp [StoredRectangularGivens.total, extractionBudget, matrixBudget, cellBudget, tick]
  ring

theorem extract_total_cost_le {n l r : ℕ} (C : StoredChain n l r)
    (q t : ℕ) (ht : t<n) :
    StoredRectangularGivens.total (extract C q t ht).cost ≤
      22*2^q*(rankAt (denoteChain C) t)+8*2^q+3*(t+1) := by
  rw [← extractionBudget_total q (rankAt (denoteChain C) t) t]
  have h op := extract_cost_le C q t ht op
  simp only [StoredRectangularGivens.total]
  exact Nat.add_le_add (Nat.add_le_add (Nat.add_le_add (Nat.add_le_add
    (Nat.add_le_add (Nat.add_le_add (Nat.add_le_add (h .field) (h .sqrt))
      (h .angle)) (h .trig)) (h .compare)) (h .read)) (h .write)) (h .emit)

/-- Prefix input labels are stored explicitly; casting a label does not
evaluate a scalar callback. The additional write charges each label record. -/
def prefixPositions {N rank : ℕ} (h : rank ≤ N) :
    Run (StoredIsometryCompletion.Positions N rank) :=
  StoredIsometryCompletion.Positions.materialize
    (fun a => charge .write (Fin.castLE h a)) (by
      intro a b equal
      exact Fin.ext (congrArg (fun x : Fin N => x.val) equal))

theorem prefixPositions_value {N rank : ℕ} (h : rank ≤ N) (a : Fin rank) :
    (prefixPositions h).value.embedding a = Fin.castLE h a := by
  simp [prefixPositions, StoredIsometryCompletion.Positions.materialize_value, charge]

theorem prefixPositions_cost {N rank : ℕ} (h : rank ≤ N) (op : Op) :
    (prefixPositions h).cost op = rank*(2*tick .read op+3*tick .write op) := by
  simp [prefixPositions, StoredIsometryCompletion.Positions.materialize_cost, charge]
  ring

private theorem spare {rank q : ℕ} (h : rank ≤ 2^q) : rank < 2*2^q := by
  have : 0 < 2^q := by positivity
  omega

/-- Completion consumes the actual charged columns and actual stored prefix
labels. Isometry is a theorem about the returned input, not a public premise. -/
noncomputable def completeAt {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    Run (StoredMatrix (2*2^q) (2*2^q)) :=
  let hs := spare ((rankAt_le_maxBond (denoteChain C) t).trans hB)
  StoredIsometryCompletion.completeFrom hs (extract C q t ht) (prefixPositions hs.le)

private theorem prefix_named {q rank : ℕ} (hl : rank ≤ 2^q) :
    (prefixPositions (spare hl).le).value.embedding =
      (activePositions hl).trans (coordinates q).toEmbedding := by
  ext a
  rw [prefixPositions_value]
  simp [activePositions, coordinates,
    finProdFinEquiv, Fin.castLE]

/-- Refinement to the existing actual named-stage producer, not merely an
arbitrary SO matrix with matching columns. -/
theorem completeAt_value {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    denote (completeAt C hB t ht).value =
      (completeStage (denoteChain C) hB t).submatrix
        (coordinates q).symm (coordinates q).symm := by
  simp only [completeAt, StoredIsometryCompletion.completeFrom_value]
  rw [extract_value C hB t ht,
    prefix_named ((rankAt_le_maxBond (denoteChain C) t).trans hB)]
  ext row col
  simp [completeStage, localCompletion, ConstructiveIsometryCompletion.completeNamed,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply]
  rfl

theorem completeAt_spec {n l r q : ℕ} (C : StoredChain n l r)
    (hC : RightCanonical (denoteChain C))
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    (denote (completeAt C hB t ht).value).transpose *
        denote (completeAt C hB t ht).value = 1 ∧
    (denote (completeAt C hB t ht).value).det = 1 ∧
    ∀ row a, denote (completeAt C hB t ht).value row
      (Fin.castLE (spare ((rankAt_le_maxBond (denoteChain C) t).trans hB)).le a) =
      activeColumns (denoteChain C) t hB ((coordinates q).symm row) a := by
  let hs := spare ((rankAt_le_maxBond (denoteChain C) t).trans hB)
  have hV : (denote (extract C q t ht).value).transpose *
      denote (extract C q t ht).value = 1 := by
    rw [extract_value C hB t ht]
    ext a b
    have h := congrFun (congrFun (activeColumns_isometry (denoteChain C) hC hB t ht) a) b
    simp only [_root_.Matrix.mul_apply, _root_.Matrix.transpose_apply] at h ⊢
    exact ((coordinates q).symm.sum_comp (fun row =>
      activeColumns (denoteChain C) t hB row a *
        activeColumns (denoteChain C) t hB row b)).trans h
  have spec := StoredIsometryCompletion.complete_spec hs (extract C q t ht).value
    (prefixPositions hs.le).value hV
  change (denote (StoredIsometryCompletion.complete hs (extract C q t ht).value
      (prefixPositions hs.le).value).value).transpose * _ = 1 ∧ _
  refine ⟨spec.1, spec.2.1, ?_⟩
  intro row a
  change denote (StoredIsometryCompletion.complete hs (extract C q t ht).value
    (prefixPositions hs.le).value).value row (Fin.castLE hs.le a) = _
  rw [← prefixPositions_value hs.le a, spec.2.2 row a]
  exact congrFun (congrFun (extract_value C hB t ht) row) a

def stageBudget (q rank t : ℕ) : ℕ :=
  22*2^q*rank+8*2^q+3*(t+1)+5*rank+
    (2*2^q)*rank*(22*rank+30*(2*2^q)+43)+
    20*(2*2^q)^2+27*(2*2^q)+5*rank+3

private theorem total_add (a b : Cost) :
    StoredRectangularGivens.total (a+b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  simp [StoredRectangularGivens.total]
  omega

theorem completeAt_total_cost_le {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n) :
    StoredRectangularGivens.total (completeAt C hB t ht).cost ≤
      stageBudget q (rankAt (denoteChain C) t) t := by
  let hs := spare ((rankAt_le_maxBond (denoteChain C) t).trans hB)
  have hx := extract_total_cost_le C q t ht
  have hp : StoredRectangularGivens.total (prefixPositions hs.le).cost =
      5*(rankAt (denoteChain C) t) := by
    simp [StoredRectangularGivens.total, prefixPositions_cost, tick]
    ring
  have hc := StoredIsometryCompletion.complete_total_cost_le hs
    (extract C q t ht).value (prefixPositions hs.le).value
  simp only [completeAt, StoredIsometryCompletion.completeFrom, bind, Run.bind,
    total_add]
  change _ ≤ stageBudget q (rankAt (denoteChain C) t) t
  dsimp only [stageBudget]
  nlinarith

theorem stageBudget_mono (q : ℕ) {rank rank' t t' : ℕ}
    (hr : rank ≤ rank') (ht : t ≤ t') :
    stageBudget q rank t ≤ stageBudget q rank' t' := by
  dsimp only [stageBudget]
  gcongr

/-- The actual normalized/canonical source is bound once, then the stored
active-column/completion supplier consumes precisely that returned chain.
Raw source exceptional counters are retained, not advertised as total index
counts of the expanded pipeline. -/
noncomputable def hermiteStage (k n : ℕ) (L : ℝ) (hL : 0<L) (t : Fin (n+1)) :
    StoredHermiteRawSource.RawRun
      (StoredMatrix (2*2^(HermiteFiniteChain.bondQubits k))
        (2*2^(HermiteFiniteChain.bondQubits k))) :=
  let source := StagedNormalizedCanonical.compile k n L
  let bound := (StagedNormalizedCanonical.compile_maxBond k n L hL).trans
    (HermiteFiniteChain.bond_fits k)
  let stage := completeAt source.run.value bound t.val t.isLt
  { run := ⟨stage.value, source.run.cost+stage.cost⟩
    exponentialCalls := source.exponentialCalls
    quotientCalls := source.quotientCalls
    remainderCalls := source.remainderCalls
    integerDoublings := source.integerDoublings
    integerAdditions := source.integerAdditions }

set_option maxHeartbeats 200000 in
theorem hermiteStage_value (k n : ℕ) (L : ℝ) (hL : 0<L) (t : Fin (n+1)) :
    denote (hermiteStage k n L hL t).run.value =
      (completeStage (denoteChain (StagedNormalizedCanonical.compile k n L).run.value)
        ((StagedNormalizedCanonical.compile_maxBond k n L hL).trans
          (HermiteFiniteChain.bond_fits k)) t.val).submatrix
        (coordinates (HermiteFiniteChain.bondQubits k)).symm
        (coordinates (HermiteFiniteChain.bondQubits k)).symm := by
  simp only [hermiteStage]
  exact completeAt_value (StagedNormalizedCanonical.compile k n L).run.value
    ((StagedNormalizedCanonical.compile_maxBond k n L hL).trans
      (HermiteFiniteChain.bond_fits k)) t.val t.isLt

def hermiteStageBudget (k n : ℕ) : ℕ :=
  StagedNormalizedCanonical.compilerBudget k n +
    stageBudget (HermiteFiniteChain.bondQubits k) (2*k+6) n

/-- These counters retain their RAW SOURCE scope. Extraction's additional
selected integer index work is charged separately in its field-tag budget. -/
theorem hermiteStage_raw_extraCounters (k n : ℕ) (L : ℝ) (hL : 0<L)
    (t : Fin (n+1)) :
    (hermiteStage k n L hL t).exponentialCalls =
      (StoredHermiteRawSource.raw k n L).exponentialCalls ∧
    (hermiteStage k n L hL t).quotientCalls = (n+1)*(n+2) ∧
    (hermiteStage k n L hL t).remainderCalls = (n+1)^2 ∧
    (hermiteStage k n L hL t).integerDoublings = n ∧
    (hermiteStage k n L hL t).integerAdditions = 4*(n+1) :=
  StagedNormalizedCanonical.compile_extraCounters k n L

theorem hermiteStage_total_cost_le (k n : ℕ) (L : ℝ) (hL : 0<L)
    (t : Fin (n+1)) :
    StoredRectangularGivens.total (hermiteStage k n L hL t).run.cost ≤
      hermiteStageBudget k n := by
  have source := StagedNormalizedCanonical.compile_total_cost_le k n L hL
  rw [StoredHermiteRawCost.ordinary_eq_total] at source
  have stage := completeAt_total_cost_le
    (StagedNormalizedCanonical.compile k n L).run.value
    ((StagedNormalizedCanonical.compile_maxBond k n L hL).trans
      (HermiteFiniteChain.bond_fits k)) t.val t.isLt
  have rank := (rankAt_le_maxBond
    (denoteChain (StagedNormalizedCanonical.compile k n L).run.value) t.val).trans
    (StagedNormalizedCanonical.compile_maxBond k n L hL)
  have bound := stageBudget_mono (HermiteFiniteChain.bondQubits k) rank
    (Nat.le_of_lt_succ t.isLt)
  simp only [hermiteStage, total_add, hermiteStageBudget]
  omega

/-- Source-facing acceptance combines actual stored value refinement, SO
semantics and the charged supplier budget. Only L>0 is a source premise. -/
theorem hermiteStage_certified (k n : ℕ) (L : ℝ) (hL : 0<L) (t : Fin (n+1)) :
    let result := hermiteStage k n L hL t
    (denote result.run.value).transpose * denote result.run.value = 1 ∧
    (denote result.run.value).det = 1 ∧
    (∀ (bit : Fin 2) (b a : PrimitiveBasis (HermiteFiniteChain.bondQubits k)),
      (primitiveBasisLEEquiv (HermiteFiniteChain.bondQubits k) a).val <
        rankAt (denoteChain (StagedNormalizedCanonical.compile k n L).run.value) t.val →
      (denote result.run.value
        (coordinates _ (Fin.snoc b bit)) (coordinates _ (Fin.snoc a 0)) : ℂ) =
        paddedAt (denoteChain (StagedNormalizedCanonical.compile k n L).run.value)
          t.val (bit, primitiveBasisLEEquiv _ b) (primitiveBasisLEEquiv _ a)) ∧
    StoredRectangularGivens.total result.run.cost ≤ hermiteStageBudget k n := by
  have bound := (StagedNormalizedCanonical.compile_maxBond k n L hL).trans
    (HermiteFiniteChain.bond_fits k)
  have spec := completeAt_spec (StagedNormalizedCanonical.compile k n L).run.value
    (StagedNormalizedCanonical.compile_canonical k n L hL) bound t.val t.isLt
  refine ⟨spec.1, spec.2.1, ?_, hermiteStage_total_cost_le k n L hL t⟩
  intro bit b a ha
  rw [hermiteStage_value]
  simp only [_root_.Matrix.submatrix_apply, Equiv.symm_apply_apply]
  exact (completeStage_spec
    (denoteChain (StagedNormalizedCanonical.compile k n L).run.value)
    (StagedNormalizedCanonical.compile_canonical k n L hL) bound t.val t.isLt).2.2
      bit b a ha

theorem extract_output_padding {n l r q : ℕ} (C : StoredChain n l r)
    (hB : maxBond (denoteChain C) ≤ 2^q) (t : ℕ) (ht : t<n)
    (row : Fin (2*2^q)) (a : Fin (rankAt (denoteChain C) t))
    (hb : rankAt (denoteChain C) (t+1) ≤ (finProdFinEquiv.symm row).2.val) :
    denote (extract C q t ht).value row a = 0 := by
  rw [extract_value C hB t ht]
  have hc : localIndex q ((coordinates q).symm row) = finProdFinEquiv.symm row :=
    (localIndex q).apply_symm_apply _
  simp only [activeColumns, hc]
  rw [paddedAt_supported (denoteChain C) t _ _ _ hb]
  rfl

/-- Here the field-tag count is precisely the declared selected index work;
there is no real field arithmetic in extraction. Loop metadata is excluded. -/
theorem extract_selected_index_le {n l r : ℕ} (C : StoredChain n l r)
    (q t : ℕ) (ht : t<n) :
    (extract C q t ht).cost .field ≤ 4*(2*2^q)*(rankAt (denoteChain C) t) := by
  have h := extract_cost_le C q t ht .field
  simpa [extractionBudget, matrixBudget, cellBudget, tick, mul_assoc, mul_left_comm,
    mul_comm] using h

section Regression

noncomputable def layoutCore : StoredCore 2 1 := #v[#v[1, 2], #v[-3, 4]]
noncomputable def layoutChain : StoredChain 1 2 1 := .cons layoutCore (.nil 1)

-- Deficient/noncanonical inputs still extract literally; no isometry claimed.
example : denote (extract layoutChain 1 0 (by decide)).value 0 ⟨1, by decide⟩ = -3 := by
  change denote (coreMatrix layoutCore 1).value 0 (1 : Fin 2) = -3
  rw [coreMatrix_value layoutCore 1 (by decide)]
  norm_num [paddedCore, denoteCore, denote, layoutCore, finProdFinEquiv, Fin.castLE]
example : denote (extract layoutChain 1 0 (by decide)).value 2 ⟨1, by decide⟩ = 4 := by
  change denote (coreMatrix layoutCore 1).value 2 (1 : Fin 2) = 4
  rw [coreMatrix_value layoutCore 1 (by decide)]
  norm_num [paddedCore, denoteCore, denote, layoutCore, finProdFinEquiv, Fin.castLE]
example : denote (extract layoutChain 1 0 (by decide)).value 1 ⟨0, by decide⟩ = 0 := by
  change denote (coreMatrix layoutCore 1).value 1 (0 : Fin 2) = 0
  rw [coreMatrix_value layoutCore 1 (by decide)]
  norm_num [paddedCore, denoteCore, denote, layoutCore, finProdFinEquiv, Fin.castLE]
example : denote (extract layoutChain 1 0 (by decide)).value 3 ⟨1, by decide⟩ = 0 := by
  change denote (coreMatrix layoutCore 1).value 3 (1 : Fin 2) = 0
  rw [coreMatrix_value layoutCore 1 (by decide)]
  norm_num [paddedCore, denoteCore, denote, layoutCore, finProdFinEquiv, Fin.castLE]

-- Two actual rows of rank-one output in a power-of-two padded register.
example (row : Fin 4) (a : Fin 2)
    (hb : 1 ≤ ((finProdFinEquiv (m:=2) (n:=2)).symm row).2.val) :
    denote (extract layoutChain 1 0 (by decide)).value row a = 0 :=
  extract_output_padding (q:=1) layoutChain (by decide) 0 (by decide) row a hb

def zeroNextCore : StoredCore 1 0 := #v[#v[]]
def zeroNextChain : StoredChain 2 1 1 :=
  .cons zeroNextCore (.cons (#v[] : StoredCore 0 1) (.nil 1))

example (row : Fin 8) (a : Fin 1) :
    denote (extract zeroNextChain 2 0 (by decide)).value row a = 0 :=
  extract_output_padding (q:=2) zeroNextChain (by decide) 0 (by decide) row a
    (by simp [zeroNextChain, denoteChain, rankAt])

example : StoredRectangularGivens.total (extract zeroNextChain 2 1 (by decide)).cost ≤
    8*2^2+3*2 := by
  simpa [zeroNextChain, denoteChain, rankAt] using
    extract_total_cost_le zeroNextChain 2 1 (by decide)

-- Empty train has no valid stage, while source n=0 has exactly one stage.
example (t : ℕ) (ht : t<0) : False := Nat.not_lt_zero t ht
example (k : ℕ) (L : ℝ) (hL : 0<L) :
    (denote (hermiteStage k 0 L hL ⟨0, by decide⟩).run.value).det = 1 :=
  (hermiteStage_certified k 0 L hL ⟨0, by decide⟩).2.1

-- Completion preserves a signed column at a NON-prefix physical position.
def highPosition : StoredIsometryCompletion.Positions 2 1 :=
  ⟨#v[1], by intro a b _; exact Subsingleton.elim a b⟩
noncomputable def negativeColumn : StoredMatrix 2 1 := #v[#v[-1], #v[0]]
theorem negativeColumn_isometry :
    (denote negativeColumn).transpose * denote negativeColumn = 1 := by
  ext a b
  fin_cases a
  fin_cases b
  norm_num [negativeColumn, denote, _root_.Matrix.mul_apply, Fin.sum_univ_two]

example : denote (StoredIsometryCompletion.complete (by decide : 1<2)
    negativeColumn highPosition).value 0 1 = -1 := by
  simpa [negativeColumn, denote, highPosition, StoredIsometryCompletion.Positions.embedding]
    using (StoredIsometryCompletion.complete_spec (by decide) negativeColumn highPosition
      negativeColumn_isometry).2.2 0 0

example (k n : ℕ) (L : ℝ) (hL : 0<L) (t : Fin (n+1)) :
    (hermiteStage k n L hL t).exponentialCalls =
      (StagedNormalizedCanonical.compile k n L).exponentialCalls := rfl

end Regression

#print axioms QuantumBlockEncoding.StagedActiveColumns.extract_value
#print axioms QuantumBlockEncoding.StagedActiveColumns.completeAt_value
#print axioms QuantumBlockEncoding.StagedActiveColumns.hermiteStage_certified
#print axioms QuantumBlockEncoding.StagedActiveColumns.hermiteStage_total_cost_le

end QuantumBlockEncoding.StagedActiveColumns
