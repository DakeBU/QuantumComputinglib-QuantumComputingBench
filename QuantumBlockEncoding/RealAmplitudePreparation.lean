import QuantumBlockEncoding.UniformlyControlledRy
import QuantumBlockEncoding.PrimitiveBasisLE
import QuantumBlockEncoding.StatePreparation

/-!
# Constructive preparation of finite real amplitude tables

Wires are ordered little-endian. The recursive construction prepares the
low-wire marginal norms first, then splits each marginal with a uniformly
controlled rotation on the new highest wire. The angles are exact real
expressions; finite numerical export is a separate evaluation obligation.
-/

namespace QuantumBlockEncoding.RealAmplitudePreparation

open Robin.ComplexLCU
open scoped Kronecker

/-- Adjoin a most-significant bit; existing wire numbers do not change. -/
def lastBasisEquiv (n : Nat) : PrimitiveBasis (n + 1) ≃ PrimitiveBasis n × Fin 2 :=
  (Fin.snocEquiv (fun _ : Fin (n + 1) => Fin 2)).symm.trans (Equiv.prodComm _ _)

@[simp] theorem lastBasisEquiv_apply {n : Nat} (b : PrimitiveBasis (n + 1)) :
    lastBasisEquiv n b = (Fin.init b, b (Fin.last n)) := rfl

@[simp] theorem lastBasisEquiv_symm_apply {n : Nat} (b : PrimitiveBasis n) (v : Fin 2) :
    (lastBasisEquiv n).symm (b, v) = Fin.snoc b v := rfl

theorem basis_eq_iff {n : Nat} (a b : PrimitiveBasis (n + 1)) :
    a = b ↔ Fin.init a = Fin.init b ∧ a (Fin.last n) = b (Fin.last n) := by
  rw [← (lastBasisEquiv n).injective.eq_iff]
  simp

/-- Tensor a circuit matrix with an untouched highest wire. -/
noncomputable def liftLastMatrix {n : Nat}
    (M : _root_.Matrix (PrimitiveBasis n) (PrimitiveBasis n) ℂ) :
    _root_.Matrix (PrimitiveBasis (n + 1)) (PrimitiveBasis (n + 1)) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (lastBasisEquiv n).symm
    (M ⊗ₖ (1 : _root_.Matrix (Fin 2) (Fin 2) ℂ))

@[simp] theorem liftLastMatrix_apply {n : Nat}
    (M : _root_.Matrix (PrimitiveBasis n) (PrimitiveBasis n) ℂ)
    (a b : PrimitiveBasis (n + 1)) :
    liftLastMatrix M a b =
      if a (Fin.last n) = b (Fin.last n) then M (Fin.init a) (Fin.init b) else 0 := by
  simp [liftLastMatrix, _root_.Matrix.reindexAlgEquiv_apply,
    _root_.Matrix.reindex_apply, _root_.Matrix.submatrix_apply,
    _root_.Matrix.one_apply, mul_ite]

@[simp] theorem liftLastMatrix_one (n : Nat) :
    liftLastMatrix (1 : _root_.Matrix (PrimitiveBasis n) (PrimitiveBasis n) ℂ) = 1 := by
  simp [liftLastMatrix]

theorem liftLastMatrix_mul {n : Nat}
    (M N : _root_.Matrix (PrimitiveBasis n) (PrimitiveBasis n) ℂ) :
    liftLastMatrix (M * N) = liftLastMatrix M * liftLastMatrix N := by
  simp [liftLastMatrix, ← _root_.Matrix.mul_kronecker_mul]

/-- Embed every instruction without changing its original wire number. -/
def liftGate {n : Nat} : PrimitiveGate n → PrimitiveGate (n + 1)
  | .x t => .x t.castSucc
  | .ry t a => .ry t.castSucc a
  | .rz t a => .rz t.castSucc a
  | .cx c t h => .cx c.castSucc t.castSucc (fun e => h (Fin.castSucc_injective _ e))

private theorem split_castSucc_eq {n : Nat} (t : Fin n)
    (a b : PrimitiveBasis (n + 1)) :
    (splitPrimitiveWire t.castSucc a).2 = (splitPrimitiveWire t.castSucc b).2 ↔
      (splitPrimitiveWire t (Fin.init a)).2 = (splitPrimitiveWire t (Fin.init b)).2 ∧
      a (Fin.last n) = b (Fin.last n) := by
  constructor
  · intro h
    constructor
    · funext w
      exact congrFun h ⟨w.1.castSucc, by simpa using w.2⟩
    · exact congrFun h ⟨Fin.last n, Ne.symm (Fin.castSucc_ne_last t)⟩
  · rintro ⟨h, hl⟩
    funext w
    obtain ⟨w, hw⟩ := w
    change a w = b w
    revert hw
    refine Fin.lastCases ?_ (fun i => ?_) w
    · intro _; exact hl
    · intro hi
      exact congrFun h ⟨i, by simpa using hi⟩

theorem lift_oneQubit {n : Nat} (t : Fin n)
    (M : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    liftPrimitiveOneQubit t.castSucc M = liftLastMatrix (liftPrimitiveOneQubit t M) := by
  ext a b
  simp only [liftPrimitiveOneQubit_apply, liftLastMatrix_apply, split_castSucc_eq]
  by_cases hc : (splitPrimitiveWire t (Fin.init a)).2 =
      (splitPrimitiveWire t (Fin.init b)).2 <;>
    by_cases hl : a (Fin.last n) = b (Fin.last n) <;>
    simp [hc, hl, Fin.init]

private theorem xBasis_lift {n : Nat} (t : Fin n) (b : PrimitiveBasis (n + 1)) :
    Fin.init (xBasisAction t.castSucc b) = xBasisAction t (Fin.init b) := by
  funext i
  simp [xBasisAction, Fin.init, Function.update_apply]

private theorem cxBasis_lift {n : Nat} (c t : Fin n) (b : PrimitiveBasis (n + 1)) :
    Fin.init (cxBasisAction c.castSucc t.castSucc b) =
      cxBasisAction c t (Fin.init b) := by
  by_cases h : b c.castSucc = 0 <;>
    simp [cxBasisAction, h, Fin.init, xBasis_lift]

theorem eval_liftGate {n : Nat} (g : PrimitiveGate n) :
    evalPrimitiveGate (liftGate g) = liftLastMatrix (evalPrimitiveGate g) := by
  cases g with
  | ry t a => exact lift_oneQubit t _
  | rz t a => exact lift_oneQubit t _
  | x t =>
    ext a b
    simp only [liftGate, evalPrimitiveGate, equivPermutationMatrix, liftLastMatrix_apply]
    change (if a = xBasisAction t.castSucc b then 1 else 0) =
      if a (Fin.last n) = b (Fin.last n) then
        if Fin.init a = xBasisAction t (Fin.init b) then 1 else 0 else 0
    have hl : xBasisAction t.castSucc b (Fin.last n) = b (Fin.last n) := by
      simp [xBasisAction, Ne.symm (Fin.castSucc_ne_last t)]
    simp only [basis_eq_iff, xBasis_lift, hl]
    by_cases h : a (Fin.last n) = b (Fin.last n) <;> simp [h]
  | cx c t h =>
    ext a b
    simp only [liftGate, evalPrimitiveGate, equivPermutationMatrix, liftLastMatrix_apply]
    change (if a = cxBasisAction c.castSucc t.castSucc b then 1 else 0) =
      if a (Fin.last n) = b (Fin.last n) then
        if Fin.init a = cxBasisAction c t (Fin.init b) then 1 else 0 else 0
    have hl : cxBasisAction c.castSucc t.castSucc b (Fin.last n) = b (Fin.last n) := by
      by_cases hc : b c.castSucc = 0 <;>
        simp [cxBasisAction, hc, xBasisAction, Ne.symm (Fin.castSucc_ne_last t)]
    simp only [basis_eq_iff, cxBasis_lift, hl]
    by_cases h : a (Fin.last n) = b (Fin.last n) <;> simp [h]

theorem eval_liftCircuit {n : Nat} (c : PrimitiveCircuit n) :
    evalPrimitiveCircuit (c.map liftGate) = liftLastMatrix (evalPrimitiveCircuit c) := by
  induction c with
  | nil => simp [evalPrimitiveCircuit]
  | cons g c ih =>
    simp only [List.map_cons, evalPrimitiveCircuit, ih, eval_liftGate, liftLastMatrix_mul]

/-- Euclidean mass at one binary split. -/
noncomputable def pairNorm (a b : ℝ) : ℝ := Real.sqrt (a ^ 2 + b ^ 2)

theorem pairNorm_nonneg (a b : ℝ) : 0 ≤ pairNorm a b := Real.sqrt_nonneg _

theorem pairNorm_sq (a b : ℝ) : pairNorm a b ^ 2 = a ^ 2 + b ^ 2 := by
  exact Real.sq_sqrt (add_nonneg (sq_nonneg a) (sq_nonneg b))

/-- Twice the signed polar angle, with the zero subtree assigned angle zero.
The arccos formula avoids an unverified numerical `atan2` primitive. -/
noncomputable def splitAngle (a b : ℝ) : ExactAngle :=
  if pairNorm a b = 0 then .rational 0 else
    .real (2 * if b < 0 then -Real.arccos (a / pairNorm a b)
      else Real.arccos (a / pairNorm a b))

theorem splitAngle_firstColumn (a b : ℝ) (v : Fin 2) :
    standardRyMatrix (splitAngle a b).eval v 0 * (pairNorm a b : ℂ) =
      if v = 0 then (a : ℂ) else (b : ℂ) := by
  have hr := pairNorm_nonneg a b
  have hr2 := pairNorm_sq a b
  by_cases hz : pairNorm a b = 0
  · have ha : a = 0 := by nlinarith [sq_nonneg b]
    have hb : b = 0 := by nlinarith [sq_nonneg a]
    rw [hz, Complex.ofReal_zero, mul_zero]
    simp [ha, hb]
  · have hp : 0 < pairNorm a b := lt_of_le_of_ne hr (Ne.symm hz)
    have ha : -pairNorm a b ≤ a ∧ a ≤ pairNorm a b := by
      constructor <;> nlinarith [sq_nonneg b]
    have lower : -1 ≤ a / pairNorm a b := (le_div_iff₀ hp).2 (by linarith)
    have upper : a / pairNorm a b ≤ 1 := (div_le_iff₀ hp).2 (by linarith)
    have hc : Real.cos (Real.arccos (a / pairNorm a b)) * pairNorm a b = a := by
      rw [Real.cos_arccos lower upper, div_mul_cancel₀ _ hz]
    have hs : 0 ≤ Real.sin (Real.arccos (a / pairNorm a b)) * pairNorm a b :=
      mul_nonneg (Real.sin_nonneg_of_nonneg_of_le_pi
        (Real.arccos_nonneg _) (Real.arccos_le_pi _)) hr
    have hs2 : (Real.sin (Real.arccos (a / pairNorm a b)) * pairNorm a b) ^ 2 = b ^ 2 := by
      have h := congrArg (fun x : ℝ => x * pairNorm a b ^ 2)
        (Real.sin_sq_add_cos_sq (Real.arccos (a / pairNorm a b)))
      nlinarith [sq_nonneg (Real.sin (Real.arccos (a / pairNorm a b)) * pairNorm a b)]
    have hangle : (2 * (if b < 0 then -Real.arccos (a / pairNorm a b)
        else Real.arccos (a / pairNorm a b))) / 2 =
        if b < 0 then -Real.arccos (a / pairNorm a b) else Real.arccos (a / pairNorm a b) := by
      ring
    simp only [splitAngle, if_neg hz, ExactAngle.eval, standardRyMatrix]
    rw [hangle]
    fin_cases v
    · change realRotation (if b < 0 then -Real.arccos (a / pairNorm a b)
          else Real.arccos (a / pairNorm a b)) 0 0 * (pairNorm a b : ℂ) = (a : ℂ)
      rw [realRotation_zero_zero]
      by_cases hb : b < 0
      · simpa only [if_pos hb, Real.cos_neg, Complex.ofReal_mul] using
          congrArg Complex.ofReal hc
      · simpa only [if_neg hb, Complex.ofReal_mul] using congrArg Complex.ofReal hc
    · change realRotation (if b < 0 then -Real.arccos (a / pairNorm a b)
          else Real.arccos (a / pairNorm a b)) 1 0 * (pairNorm a b : ℂ) = (b : ℂ)
      rw [realRotation_one_zero]
      by_cases hb : b < 0
      · have he : -(Real.sin (Real.arccos (a / pairNorm a b)) * pairNorm a b) = b := by
          nlinarith
        simpa only [if_pos hb, Real.sin_neg, Complex.ofReal_neg, Complex.ofReal_mul,
          neg_mul] using congrArg Complex.ofReal he
      · have he : Real.sin (Real.arccos (a / pairNorm a b)) * pairNorm a b = b := by
          nlinarith
        simpa only [if_neg hb, Complex.ofReal_mul] using congrArg Complex.ofReal he

/-- Marginal amplitudes on all but the highest wire. -/
noncomputable def marginal {n : Nat} (f : PrimitiveBasis (n + 1) → ℝ) :
    PrimitiveBasis n → ℝ := fun b => pairNorm (f (Fin.snoc b 0)) (f (Fin.snoc b 1))

theorem marginal_nonneg {n : Nat} (f : PrimitiveBasis (n + 1) → ℝ) (b : PrimitiveBasis n) :
    0 ≤ marginal f b := pairNorm_nonneg _ _

/-- True squared Euclidean norm of the complete amplitude table. -/
noncomputable def normSq {n : Nat} (f : PrimitiveBasis n → ℝ) : ℝ := ∑ b, f b ^ 2

theorem normSq_nonneg {n : Nat} (f : PrimitiveBasis n → ℝ) : 0 ≤ normSq f :=
  Finset.sum_nonneg (fun _ _ => sq_nonneg _)

theorem normSq_marginal {n : Nat} (f : PrimitiveBasis (n + 1) → ℝ) :
    normSq (marginal f) = normSq f := by
  unfold normSq
  simp only [marginal, pairNorm_sq]
  rw [← (lastBasisEquiv n).symm.sum_comp]
  simp [Fintype.sum_prod_type, Fin.sum_univ_two]

/-- Chronological low-bit-first binary tree, compiled entirely to RY and CX. -/
noncomputable def prepareCircuit : (n : Nat) → (PrimitiveBasis n → ℝ) → PrimitiveCircuit n
  | 0, _ => []
  | n + 1, f =>
    (prepareCircuit n (marginal f)).map liftGate ++
      compileUniformlyControlledRy n Fin.castSucc (Fin.last n) Fin.castSucc_ne_last
        (fun b => splitAngle (f (Fin.snoc b 0)) (f (Fin.snoc b 1)))

theorem prepareCircuit_unitary {n : Nat} (f : PrimitiveBasis n → ℝ) :
    evalPrimitiveCircuit (prepareCircuit n f) ∈
      _root_.Matrix.unitaryGroup (PrimitiveBasis n) ℂ :=
  evalPrimitiveCircuit_unitary _

private theorem last_context_eq {n : Nat} (a b : PrimitiveBasis (n + 1)) :
    (splitPrimitiveWire (Fin.last n) a).2 = (splitPrimitiveWire (Fin.last n) b).2 ↔
      Fin.init a = Fin.init b := by
  constructor
  · intro h
    funext i
    exact congrFun h ⟨i.castSucc, Fin.castSucc_ne_last i⟩
  · intro h
    funext w
    obtain ⟨w, hw⟩ := w
    change a w = b w
    revert hw
    refine Fin.lastCases ?_ (fun i => ?_) w
    · intro h; exact (h rfl).elim
    · intro _; exact congrFun h i

theorem controlledLast_apply {n : Nat} (angles : PrimitiveBasis n → ExactAngle)
    (a b : PrimitiveBasis (n + 1)) :
    controlledRyBlockMatrix Fin.castSucc (Fin.last n) Fin.castSucc_ne_last angles a b =
      if Fin.init a = Fin.init b then
        standardRyMatrix (angles (Fin.init a)).eval (a (Fin.last n)) (b (Fin.last n))
      else 0 := by
  simp only [controlledRyBlockMatrix_apply, last_context_eq]
  rfl

theorem controlledLast_mul_lift {n : Nat} (angles : PrimitiveBasis n → ExactAngle)
    (M : _root_.Matrix (PrimitiveBasis n) (PrimitiveBasis n) ℂ)
    (a : PrimitiveBasis (n + 1)) :
    (controlledRyBlockMatrix Fin.castSucc (Fin.last n) Fin.castSucc_ne_last angles *
        liftLastMatrix M) a (fun _ => 0) =
      standardRyMatrix (angles (Fin.init a)).eval (a (Fin.last n)) 0 *
        M (Fin.init a) (fun _ => 0) := by
  rw [_root_.Matrix.mul_apply, ← (lastBasisEquiv n).symm.sum_comp]
  simp only [controlledLast_apply, liftLastMatrix_apply]
  simp [Fintype.sum_prod_type]
  exact Or.inl rfl

/-- The compiled first column is the normalized input table. This version
also covers the zero-qubit register, whose sole amplitude must be nonnegative. -/
theorem prepareCircuit_firstColumn {n : Nat} (f : PrimitiveBasis n → ℝ)
    (nonneg : ∀ b, 0 ≤ f b) (positive : 0 < normSq f) (b : PrimitiveBasis n) :
    evalPrimitiveCircuit (prepareCircuit n f) b (fun _ => 0) =
      ((f b / Real.sqrt (normSq f) : ℝ) : ℂ) := by
  induction n with
  | zero =>
    have heq : b = (fun _ => 0) := Subsingleton.elim _ _
    have hnorm : normSq f = f b ^ 2 := by
      calc
        normSq f = ∑ _x : PrimitiveBasis 0, f b ^ 2 :=
          Finset.sum_congr rfl (fun x _ => congrArg (fun x => f x ^ 2) (Subsingleton.elim x b))
        _ = f b ^ 2 := by simp
    have hf : 0 < f b := by have := nonneg b; rw [hnorm] at positive; nlinarith
    rw [hnorm, Real.sqrt_sq (le_of_lt hf), div_self (ne_of_gt hf)]
    simp [prepareCircuit, evalPrimitiveCircuit, heq]
  | succ n ih =>
    simp only [prepareCircuit, evalPrimitiveCircuit_append, eval_liftCircuit,
      compileUniformlyControlledRy_eval_controlledRyBlockMatrix]
    rw [controlledLast_mul_lift]
    rw [ih (marginal f) (marginal_nonneg f) (by simpa [normSq_marginal] using positive)]
    rw [normSq_marginal]
    push_cast
    rw [← mul_div_assoc]
    change
      (standardRyMatrix
        (splitAngle (f (Fin.snoc (Fin.init b) 0)) (f (Fin.snoc (Fin.init b) 1))).eval
          (b (Fin.last n)) 0 *
        (pairNorm (f (Fin.snoc (Fin.init b) 0)) (f (Fin.snoc (Fin.init b) 1)) : ℂ)) /
          (Real.sqrt (normSq f) : ℂ) = _
    rw [splitAngle_firstColumn]
    congr 1
    have hs : Fin.snoc (Fin.init b) (b (Fin.last n)) = b := Fin.snoc_init_self b
    generalize hv : b (Fin.last n) = v at *
    fin_cases v <;> simp_all

/-- Normalization is the actual sum of squared amplitudes, not a certificate flag. -/
theorem normalized_sum_sq {n : Nat} (f : PrimitiveBasis n → ℝ)
    (positive : 0 < normSq f) :
    (∑ b, (f b / Real.sqrt (normSq f)) ^ 2) = 1 := by
  simp_rw [div_pow]
  rw [← Finset.sum_div]
  change normSq f / Real.sqrt (normSq f) ^ 2 = 1
  rw [Real.sq_sqrt (normSq_nonneg f), div_self (ne_of_gt positive)]

theorem normSq_pos_of_positive {n : Nat} (f : PrimitiveBasis n → ℝ)
    (positive : ∀ b, 0 < f b) : 0 < normSq f := by
  apply Finset.sum_pos
  · intro b _; exact sq_pos_of_pos (positive b)
  · exact Finset.univ_nonempty

theorem liftCircuit_ryCount {n : Nat} (c : PrimitiveCircuit n) :
    PrimitiveCircuit.ryCount (c.map liftGate) = c.ryCount := by
  induction c with
  | nil => rfl
  | cons g c ih =>
    cases g <;> simp_all [PrimitiveCircuit.ryCount, liftGate]

theorem liftCircuit_cxCount {n : Nat} (c : PrimitiveCircuit n) :
    PrimitiveCircuit.cxCount (c.map liftGate) = c.cxCount := by
  induction c with
  | nil => rfl
  | cons g c ih =>
    cases g <;> simp_all [PrimitiveCircuit.cxCount, liftGate]

/-- The unoptimized reference tree uses exactly one RY per internal tree node. -/
theorem prepareCircuit_ryCount {n : Nat} (f : PrimitiveBasis n → ℝ) :
    (prepareCircuit n f).ryCount = 2 ^ n - 1 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [prepareCircuit, PrimitiveCircuit.ryCount_append, liftCircuit_ryCount,
      compileUniformlyControlledRy_ryCount, ih, pow_succ]
    have hp : 0 < 2 ^ n := pow_pos (by decide) _
    omega

/-- CX count for the recursive reference multiplexor, without Gray-code optimization. -/
theorem prepareCircuit_cxCount {n : Nat} (f : PrimitiveBasis n → ℝ) :
    (prepareCircuit n f).cxCount = 2 * (2 ^ n - 1 - n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [prepareCircuit, PrimitiveCircuit.cxCount_append, liftCircuit_cxCount,
      compileUniformlyControlledRy_cxCount, ih, pow_succ]
    have hp : n < 2 ^ n := Nat.lt_two_pow_self
    omega

theorem prepareCircuit_oracleCalls {n : Nat} (f : PrimitiveBasis n → ℝ) :
    (prepareCircuit n f).resource.oracleCalls = 0 :=
  PrimitiveCircuit.resource_oracleCalls_eq_zero _

@[simp] theorem primitiveBasisLE_zero (n : Nat) :
    primitiveBasisLEEquiv n (fun _ => 0) = zeroBasisIndex n := by
  apply Fin.ext
  induction n with
  | zero => rfl
  | succ n ih =>
    change 0 + 2 * (primitiveBasisLEEquiv n (fun _ => 0)).val = 0
    have ihVal : (primitiveBasisLEEquiv n (fun _ => 0)).val = 0 := by
      simpa [zeroBasisIndex] using ih
    simp [ihVal]

@[simp] theorem primitiveBasisLE_zero_symm (n : Nat) :
    (primitiveBasisLEEquiv n).symm (zeroBasisIndex n) = (fun _ => 0) := by
  apply (primitiveBasisLEEquiv n).injective
  simp

/-- The same circuit matrix on flat little-endian integer indices. -/
noncomputable def prepareMatrixLE {n : Nat} (f : Fin (gridSize n) → ℝ) :
    _root_.Matrix (Fin (gridSize n)) (Fin (gridSize n)) ℂ :=
  _root_.Matrix.reindexAlgEquiv ℂ ℂ (primitiveBasisLEEquiv n)
    (evalPrimitiveCircuit (prepareCircuit n (fun b => f (primitiveBasisLEEquiv n b))))

theorem prepareMatrixLE_unitary {n : Nat} (f : Fin (gridSize n) → ℝ) :
    prepareMatrixLE f ∈ _root_.Matrix.unitaryGroup (Fin (gridSize n)) ℂ :=
  reindex_unitary _ _ (prepareCircuit_unitary _)

theorem normSq_reindex {n : Nat} (f : Fin (gridSize n) → ℝ) :
    normSq (fun b => f (primitiveBasisLEEquiv n b)) = ∑ j, f j ^ 2 := by
  exact (primitiveBasisLEEquiv n).sum_comp (fun j => f j ^ 2)

theorem prepareMatrixLE_firstColumn {n : Nat} (f : Fin (gridSize n) → ℝ)
    (positive : ∀ j, 0 < f j) (j : Fin (gridSize n)) :
    prepareMatrixLE f j (zeroBasisIndex n) =
      ((f j / Real.sqrt (∑ i, f i ^ 2) : ℝ) : ℂ) := by
  unfold prepareMatrixLE
  simp only [_root_.Matrix.reindexAlgEquiv_apply, _root_.Matrix.reindex_apply,
    _root_.Matrix.submatrix_apply, primitiveBasisLE_zero_symm]
  rw [prepareCircuit_firstColumn _ (fun b => le_of_lt (positive _))
    (normSq_pos_of_positive _ (fun b => positive _)), normSq_reindex]
  simp

theorem normalized_sum_sq_LE {n : Nat} (f : Fin (gridSize n) → ℝ)
    (positive : ∀ j, 0 < f j) :
    (∑ j, (f j / Real.sqrt (∑ i, f i ^ 2)) ^ 2) = 1 := by
  have h := normalized_sum_sq (fun b => f (primitiveBasisLEEquiv n b))
    (normSq_pos_of_positive _ (fun b => positive _))
  rw [normSq_reindex] at h
  calc
    _ = ∑ b, (f (primitiveBasisLEEquiv n b) / Real.sqrt (∑ i, f i ^ 2)) ^ 2 :=
      ((primitiveBasisLEEquiv n).sum_comp _).symm
    _ = 1 := h

end QuantumBlockEncoding.RealAmplitudePreparation
