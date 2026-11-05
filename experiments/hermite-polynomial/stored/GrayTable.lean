import GrayTarget
import QuantumBlockEncoding.ConstructiveIsometryLocal

/-! Charged pullback of an actual stored completion table into Gray order.
This is a staging provider. Integer encoding is charged in `field`; neither
bit complexity nor a complete Hermite compiler is certified here. -/
namespace QuantumBlockEncoding.StagedGrayTable
open StoredGivens ConstructiveIsometryLocal
open scoped BigOperators

def encode : (n : ℕ) → Vector (Fin 2) n → Run (Fin (2^n))
  | 0, _ => pure 0
  | n+1, bits => do
      let low ← StoredGivens.read bits 0
      let tail ← collect (fun i : Fin n => StoredGivens.read bits i.succ)
      let upper ← encode n tail
      let twice := 2*upper.val
      let result : Fin (2^(n+1)) := ⟨low.val+twice, by
        have a := low.isLt
        have b := upper.isLt
        rw [pow_succ]
        omega⟩
      ⟨result, 2 • tick .field⟩

theorem encode_value (n : ℕ) (bits : Vector (Fin 2) n) :
    (encode n bits).value = primitiveBasisLEEquiv n (fun i => bits[i.val]) := by
  induction n with
  | zero => apply Fin.ext; rfl
  | succ n ih =>
      apply Fin.ext
      simp only [encode, bind, Run.bind, StoredGivens.read, charge]
      rw [ih]
      simpa [collect, StoredGivens.read, charge] using
        (primitiveBasisLEEquiv_succ_value n (fun i => bits[i.val])).symm

theorem encode_cost (n : ℕ) (bits : Vector (Fin 2) n) (op : Op) :
    (encode n bits).cost op ≤ n*(5*n+3) := by
  induction n with
  | zero => simp [encode, pure, Run.pure]
  | succ n ih =>
      have h := ih (collect (fun i : Fin n => StoredGivens.read bits i.succ)).value
      have ht := HermiteGrayTargetCandidate.tick_le_one .field op
      have hr := HermiteGrayTargetCandidate.tick_le_one .read op
      have hw := HermiteGrayTargetCandidate.tick_le_one .write op
      simp only [encode, bind, Run.bind, charge, StoredGivens.read, Pi.add_apply,
        collect_cost, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
        Pi.smul_apply, smul_eq_mul] at ⊢
      simp only [StoredGivens.read, charge] at h
      nlinarith

def label (q : ℕ) (index : Fin (2^(q+1))) : Run (Fin (2*2^q)) := do
  let bits ← HermiteGrayTargetCandidate.word (q+1) index
  let data ← StoredGivens.read bits (Fin.last q)
  let bondBits ← collect (fun i : Fin q => StoredGivens.read bits i.castSucc)
  let bond ← encode q bondBits
  ⟨finProdFinEquiv (data,bond), 2 • tick .field⟩

theorem label_value (q : ℕ) (index : Fin (2^(q+1))) :
    (label q index).value = coordinates q (GrayBasis.equiv (q+1) index) := by
  simp only [label, bind, Run.bind, StoredGivens.read, charge, encode_value, collect_value,
    HermiteGrayTargetCandidate.word_value]
  rfl

def labelBudget (q : ℕ) : ℕ := (q+1)*(q+10)+1+5*q+q*(5*q+3)+2

theorem label_cost (q : ℕ) (index : Fin (2^(q+1))) (op : Op) :
    (label q index).cost op ≤ labelBudget q := by
  have hword := HermiteGrayTargetCandidate.word_cost_le (q+1) index op
  have henc := encode_cost q (collect (fun i : Fin q =>
    StoredGivens.read (HermiteGrayTargetCandidate.word (q+1) index).value i.castSucc)).value op
  have hf := HermiteGrayTargetCandidate.tick_le_one .field op
  have hr := HermiteGrayTargetCandidate.tick_le_one .read op
  have hw := HermiteGrayTargetCandidate.tick_le_one .write op
  simp only [label, bind, Run.bind, charge, StoredGivens.read, Pi.add_apply,
    collect_cost, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    smul_eq_mul, Pi.smul_apply, labelBudget] at ⊢
  simp only [StoredGivens.read, charge] at henc
  nlinarith

def labels (q : ℕ) : Run (Vector (Fin (2*2^q)) (2^(q+1))) := collect (label q)

theorem labels_value (q : ℕ) (i : Fin (2^(q+1))) :
    (labels q).value[i.val] = coordinates q (GrayBasis.equiv (q+1) i) := by
  simp [labels, label_value]

def reindex (q : ℕ) (A : StoredMatrix (2*2^q) (2*2^q)) :
    Run (StoredMatrix (2^(q+1)) (2^(q+1))) := do
  let cached ← labels q
  materialize (fun i j => do
    let row ← StoredGivens.read cached i
    let col ← StoredGivens.read cached j
    let values ← StoredGivens.read A row
    StoredGivens.read values col)

theorem reindex_value (q : ℕ) (A : StoredMatrix (2*2^q) (2*2^q)) :
    denote (reindex q A).value = (denote A).submatrix
      (fun i => coordinates q (GrayBasis.equiv (q+1) i))
      (fun i => coordinates q (GrayBasis.equiv (q+1) i)) := by
  ext i j
  simp [reindex, bind, Run.bind, materialize, denote, StoredGivens.read, charge, labels_value]

/-- The named physical-matrix consumer sees precisely this table, not its
transpose or inverse permutation. The data wire is last; bond wires are low. -/
theorem reindex_grayCoordinates (q : ℕ) (A : StoredMatrix (2*2^q) (2*2^q)) :
    denote (reindex q A).value = GrayGivensCompiler.grayCoordinates
      ((denote A).submatrix (coordinates q) (coordinates q)) := by
  ext i j
  simp [reindex_value, GrayGivensCompiler.grayCoordinates,
    Matrix.reindexAlgEquiv_apply, Matrix.reindex_apply]

def tableBudget (q : ℕ) : ℕ :=
  2^(q+1)*(labelBudget q+4)+8*(2^(q+1))^2+4*2^(q+1)

theorem reindex_cost (q : ℕ) (A : StoredMatrix (2*2^q) (2*2^q)) (op : Op) :
    (reindex q A).cost op ≤ tableBudget q := by
  have sum : (∑ i : Fin (2^(q+1)), (label q i).cost op) ≤
      2^(q+1)*labelBudget q := by
    calc
      _ ≤ ∑ _i : Fin (2^(q+1)), labelBudget q :=
        Finset.sum_le_sum (fun i _ => label_cost q i op)
      _ = _ := by simp
  have hr := HermiteGrayTargetCandidate.tick_le_one .read op
  have hw := HermiteGrayTargetCandidate.tick_le_one .write op
  have readBound : (6*(2^(q+1))^2+4*2^(q+1))*tick .read op ≤
      6*(2^(q+1))^2+4*2^(q+1) := by
    calc
      _ ≤ (6*(2^(q+1))^2+4*2^(q+1))*1 := Nat.mul_le_mul_left _ hr
      _ = _ := Nat.mul_one _
  have writeBound : (2*(2^(q+1))^2+4*2^(q+1))*tick .write op ≤
      2*(2^(q+1))^2+4*2^(q+1) := by
    calc
      _ ≤ (2*(2^(q+1))^2+4*2^(q+1))*1 := Nat.mul_le_mul_left _ hw
      _ = _ := Nat.mul_one _
  calc
    _ = (∑ i : Fin (2^(q+1)), (label q i).cost op) +
        (6*(2^(q+1))^2+4*2^(q+1))*tick .read op +
        (2*(2^(q+1))^2+4*2^(q+1))*tick .write op := by
      simp only [reindex, bind, Run.bind, labels, materialize, collect_cost,
        StoredGivens.read, charge, Pi.add_apply, Finset.sum_add_distrib, Finset.sum_const,
        Finset.card_univ, Fintype.card_fin, smul_eq_mul]
      ring
    _ ≤ 2^(q+1)*labelBudget q + (6*(2^(q+1))^2+4*2^(q+1)) +
        (2*(2^(q+1))^2+4*2^(q+1)) := by
      exact Nat.add_le_add (Nat.add_le_add sum readBound) writeBound
    _ = tableBudget q := by unfold tableBudget; ring

theorem reindex_total_cost (q : ℕ) (A : StoredMatrix (2*2^q) (2*2^q)) :
    StoredRectangularGivens.total (reindex q A).cost ≤ 8*tableBudget q := by
  have h op := reindex_cost q A op
  dsimp [StoredRectangularGivens.total]
  have a := h .field
  have b := h .sqrt
  have c := h .angle
  have d := h .trig
  have e := h .compare
  have f := h .read
  have g := h .write
  have k := h .emit
  omega

example : (labels 0).value = #v[0,1] := by native_decide
example : (labels 2).value = #v[0,1,3,2,6,7,5,4] := by native_decide
example : (encode 3 #v[1,0,1]).value = 5 := by native_decide

/-- Any stored signed, nonsymmetric table is covered; this entry would differ
under an accidental transpose or inverse permutation. -/
example (A : StoredMatrix 4 4) :
    denote (reindex 1 A).value 2 1 = denote A 3 1 := by
  have row : coordinates 1 (GrayBasis.equiv 2 (2 : Fin 4)) = 3 := by native_decide
  have col : coordinates 1 (GrayBasis.equiv 2 (1 : Fin 4)) = 1 := by native_decide
  simp [reindex_value, row, col]

#print axioms encode_value
#print axioms label_value
#print axioms reindex_value
#print axioms reindex_grayCoordinates
#print axioms reindex_total_cost
end QuantumBlockEncoding.StagedGrayTable
