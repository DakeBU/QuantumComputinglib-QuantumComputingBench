import QuantumBlockEncoding.ThinLQ
import QuantumBlockEncoding.SequentialBondPreparation

/-!
# Exact right-canonicalization of finite real tensor trains

Bond dimensions are dependent indices, not padded columns. Canonicalization
proceeds from the terminal bond to the initial bond, absorbing each residual
matrix into the preceding core. All input ranks, including zero and deficient
ones, are allowed. The orthonormal completions use classical choice: these
theorems do not certify an arithmetic algorithm or a preprocessing cost.
-/

namespace QuantumBlockEncoding.TensorTrainCanonical

open scoped BigOperators

abbrev Core (l r : ℕ) := _root_.Matrix (Fin l) (Fin 2 × Fin r) ℝ

def slice {l r : ℕ} (A : Core l r) (bit : Fin 2) :
    _root_.Matrix (Fin l) (Fin r) ℝ := fun a b => A a (bit, b)

/-- The first core emits the first bit. The terminal bond is explicit. -/
inductive Chain : ℕ → ℕ → ℕ → Type
  | nil (r : ℕ) : Chain 0 r r
  | cons {n l m r : ℕ} (head : Core l m) (tail : Chain n m r) : Chain (n + 1) l r

/-- Bit words indexed recursively in the same order as the cores. -/
def Word : ℕ → Type
  | 0 => Unit
  | n + 1 => Fin 2 × Word n

instance wordFintype (n : ℕ) : Fintype (Word n) := by
  induction n with
  | zero => exact inferInstanceAs (Fintype Unit)
  | succ n ih => exact inferInstanceAs (Fintype (Fin 2 × Word n))

/-- Matrix of bond-to-bond amplitudes for one fixed emitted word. -/
noncomputable def contract : {n l r : ℕ} → Chain n l r → Word n →
    _root_.Matrix (Fin l) (Fin r) ℝ
  | _, _, _, .nil _, _ => 1
  | _, _, _, .cons A C, x => slice A x.1 * contract C x.2

/-- Right-canonical means orthonormal rows at every individual core. -/
def RightCanonical : {n l r : ℕ} → Chain n l r → Prop
  | _, _, _, .nil _ => True
  | _, _, _, .cons A C => A * A.transpose = 1 ∧ RightCanonical C

/-- The active ranks satisfy the exact backward `min` recurrence, with an
unchanged terminal bond. This is a relation on actual core chains. -/
inductive RankReduced : {n l l' r : ℕ} → Chain n l r → Chain n l' r → Prop
  | nil (r : ℕ) : RankReduced (.nil r) (.nil r)
  | cons {n l m r m' : ℕ} {A : Core l m} {C : Chain n m r}
      {Q : Core (min l (2 * m')) m'} {D : Chain n m' r}
      (tail : RankReduced C D) : RankReduced (.cons A C) (.cons Q D)

/-- Multiply a residual into the right bond without mixing the emitted bit. -/
noncomputable def absorb {l m r : ℕ} (A : Core l m)
    (R : _root_.Matrix (Fin m) (Fin r) ℝ) : Core l r :=
  fun a x => ∑ b, A a (x.1, b) * R b x.2

theorem absorb_slice {l m r : ℕ} (A : Core l m)
    (R : _root_.Matrix (Fin m) (Fin r) ℝ) (bit : Fin 2) :
    slice (absorb A R) bit = slice A bit * R := rfl

/-- Thin LQ with the physical bit/right-bond product index made explicit. -/
theorem exists_core_lq {l r : ℕ} (A : Core l r) :
    ∃ (R : _root_.Matrix (Fin l) (Fin (min l (2 * r))) ℝ)
      (Q : Core (min l (2 * r)) r), A = R * Q ∧ Q * Q.transpose = 1 := by
  classical
  let e : Fin 2 × Fin r ≃ Fin (2 * r) := finProdFinEquiv
  obtain ⟨R, Q, hA, hQ⟩ := ThinLQ.exists_thin_lq (fun a j => A a (e.symm j))
  refine ⟨R, fun a j => Q a (e j), ?_, ?_⟩
  · ext a j
    change A a j = ∑ b, R a b * Q b (e j)
    simpa only [Equiv.symm_apply_apply, _root_.Matrix.mul_apply] using
      congrFun (congrFun hA a) (e j)
  · ext a b
    have h := congrFun (congrFun hQ a) b
    simp only [_root_.Matrix.mul_apply, _root_.Matrix.transpose_apply] at h ⊢
    exact (e.sum_comp (fun j => Q a j * Q b j)).trans h

/-- Exact all-length right-canonicalization, preserving every amplitude.
No full-rank assumption or global state-action hypothesis is used. -/
theorem exists_rightCanonical {n l r : ℕ} (C : Chain n l r) :
    ∃ (l' : ℕ) (R : _root_.Matrix (Fin l) (Fin l') ℝ) (D : Chain n l' r),
      RightCanonical D ∧ RankReduced C D ∧ ∀ x, contract C x = R * contract D x := by
  induction C with
  | nil r =>
    exact ⟨r, 1, .nil r, trivial, .nil r, fun x => by simp [contract]⟩
  | @cons n l m r A C ih =>
    obtain ⟨m', S, D, hD, hRanks, hC⟩ := ih
    obtain ⟨R, Q, hA, hQ⟩ := exists_core_lq (absorb A S)
    refine ⟨min l (2 * m'), R, .cons Q D, ⟨hQ, hD⟩, .cons hRanks, ?_⟩
    intro x
    change slice A x.1 * contract C x.2 = R * (slice Q x.1 * contract D x.2)
    rw [hC, ← _root_.Matrix.mul_assoc, ← absorb_slice]
    have hs : slice (absorb A S) x.1 = R * slice Q x.1 := by
      ext a b
      exact congrFun (congrFun hA a) (x.1, b)
    rw [hs, _root_.Matrix.mul_assoc]

/-- Every nonempty canonicalized train has a left rank bounded by the
original left rank and by twice its next active rank. -/
theorem RankReduced.head_bound {n l l' r : ℕ} {C : Chain (n + 1) l r}
    {D : Chain (n + 1) l' r} (h : RankReduced C D) :
    l' ≤ l ∧ ∃ m', ∃ (Q : Core l' m') (tail : Chain n m' r),
      D = .cons Q tail ∧ l' ≤ 2 * m' := by
  cases h with
  | @cons _ _ _ _ m' A C Q D h =>
    exact ⟨min_le_left _ _, m', Q, D, rfl, min_le_right _ _⟩

/-- In particular, the penultimate active bond has dimension at most two. -/
theorem RankReduced.last_bond_le_two {l l' : ℕ} {C : Chain 1 l 1}
    {D : Chain 1 l' 1} (h : RankReduced C D) : l' ≤ 2 := by
  obtain ⟨_, m', Q, tail, _, hb⟩ := h.head_bound
  cases tail
  simpa using hb

/-- Squared Euclidean mass for an arbitrary finite real boundary. -/
noncomputable def mass {I : Type*} [Fintype I] (v : I → ℝ) : ℝ := ∑ i, v i ^ 2

/-- An orthonormal-row matrix acts isometrically on row-vector boundaries. -/
theorem mass_vecMul {I J : Type*} [Fintype I] [Fintype J] [DecidableEq I]
    (A : _root_.Matrix I J ℝ) (hA : A * A.transpose = 1) (v : I → ℝ) :
    mass (_root_.Matrix.vecMul v A) = mass v := by
  change (∑ j, (_root_.Matrix.vecMul v A) j ^ 2) = ∑ i, v i ^ 2
  simp only [pow_two]
  change dotProduct (_root_.Matrix.vecMul v A) (_root_.Matrix.vecMul v A) =
    dotProduct v v
  calc
    _ = dotProduct (_root_.Matrix.vecMul v A) (A.transpose.mulVec v) := by
      rw [_root_.Matrix.mulVec_transpose]
    _ = dotProduct (_root_.Matrix.vecMul (_root_.Matrix.vecMul v A) A.transpose) v :=
      _root_.Matrix.dotProduct_mulVec _ _ _
    _ = _ := by rw [_root_.Matrix.vecMul_vecMul, hA, _root_.Matrix.vecMul_one]

/-- Total mass of all emitted amplitudes, including the terminal bond. -/
noncomputable def chainMass {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) : ℝ :=
  ∑ x : Word n, mass (_root_.Matrix.vecMul v (contract C x))

/-- Local row-isometries compose to an all-length mass-preserving state map. -/
theorem chainMass_eq {n l r : ℕ} (C : Chain n l r) (hC : RightCanonical C)
    (v : Fin l → ℝ) : chainMass C v = mass v := by
  induction C with
  | nil r =>
    change (∑ _ : Unit, mass (_root_.Matrix.vecMul v (1 : _root_.Matrix (Fin r) (Fin r) ℝ))) = mass v
    simp
  | @cons n l m r A C ih =>
    obtain ⟨hA, hC⟩ := hC
    change (∑ x : Fin 2 × Word n,
      mass (_root_.Matrix.vecMul v (slice A x.1 * contract C x.2))) = mass v
    rw [Fintype.sum_prod_type]
    simp_rw [← _root_.Matrix.vecMul_vecMul]
    change (∑ bit : Fin 2, chainMass C (_root_.Matrix.vecMul v (slice A bit))) = mass v
    simp_rw [ih hC]
    have he : (∑ bit : Fin 2, mass (_root_.Matrix.vecMul v (slice A bit))) =
        mass (_root_.Matrix.vecMul v A) := by
      simp only [mass, Fintype.sum_prod_type, _root_.Matrix.vecMul, slice]
    rw [he, mass_vecMul A hA]

/-- Factorization preserves total mass, and canonicality identifies it with
the mass of the new initial boundary. -/
theorem residual_mass {n l l' r : ℕ} (C : Chain n l r) (D : Chain n l' r)
    (R : _root_.Matrix (Fin l) (Fin l') ℝ) (hD : RightCanonical D)
    (h : ∀ x, contract C x = R * contract D x) (v : Fin l → ℝ) :
    chainMass C v = mass (_root_.Matrix.vecMul v R) := by
  calc
    _ = chainMass D (_root_.Matrix.vecMul v R) := by
      simp only [chainMass, h, _root_.Matrix.vecMul_vecMul]
    _ = _ := chainMass_eq D hD _

/-- A normalized input train has a normalized residual initial boundary.
The terminal bond remains exactly dimension one. -/
theorem exists_rightCanonical_normalized {n l : ℕ} (C : Chain n l 1)
    (v : Fin l → ℝ) (hv : chainMass C v = 1) :
    ∃ (l' : ℕ) (R : _root_.Matrix (Fin l) (Fin l') ℝ) (D : Chain n l' 1),
      RightCanonical D ∧ RankReduced C D ∧
      (∀ x, contract C x = R * contract D x) ∧ mass (_root_.Matrix.vecMul v R) = 1 := by
  obtain ⟨l', R, D, hD, hRanks, h⟩ := exists_rightCanonical C
  exact ⟨l', R, D, hD, hRanks, h, (residual_mass C D R hD h v).symm.trans hv⟩

/-- Scalar-boundary state version: the new initial vector is normalized and
every individual target amplitude is recovered by contracting it with the
right-canonical train. No target-state equality is a hypothesis. -/
theorem exists_normalized_state {n : ℕ} (C : Chain n 1 1)
    (hC : (∑ x : Word n, (contract C x 0 0) ^ 2) = 1) :
    ∃ (l' : ℕ) (u : Fin l' → ℝ) (D : Chain n l' 1),
      RightCanonical D ∧ RankReduced C D ∧ mass u = 1 ∧
      ∀ x, contract C x 0 0 = ∑ a, u a * contract D x a 0 := by
  have hv : chainMass C (fun _ => 1) = 1 := by
    simpa [chainMass, mass, _root_.Matrix.vecMul, dotProduct] using hC
  obtain ⟨l', R, D, hD, hRanks, h, hu⟩ :=
    exists_rightCanonical_normalized C (fun _ => 1) hv
  refine ⟨l', _root_.Matrix.vecMul (fun _ => 1) R, D, hD, hRanks, hu, ?_⟩
  intro x
  have hx := congrFun (congrFun (h x) 0) 0
  simpa [_root_.Matrix.mul_apply, _root_.Matrix.vecMul, dotProduct] using hx

/-- Largest actual bond in a chain, including both boundaries. -/
def maxBond : {n l r : ℕ} → Chain n l r → ℕ
  | _, _, _, .nil r => r
  | _, l, _, .cons _ C => max l (maxBond C)

/-- Backward canonicalization never enlarges any maximal bond dimension. -/
theorem RankReduced.maxBond_le {n l l' r : ℕ} {C : Chain n l r}
    {D : Chain n l' r} (h : RankReduced C D) : maxBond D ≤ maxBond C := by
  induction h with
  | nil r => exact le_rfl
  | cons _ ih => exact max_le_max (min_le_left _ _) ih

/-- In circuit convention the emitted bit/new bond are output rows, and
the old bond is the input column. Real amplitudes embed into complex ones. -/
def complexCore {l r : ℕ} (A : Core l r) :
    _root_.Matrix (Fin 2 × Fin r) (Fin l) ℂ := fun out a => (A a out : ℂ)

/-- Right-canonical rows are exactly orthonormal circuit input columns. -/
theorem complexCore_isometry {l r : ℕ} (A : Core l r)
    (hA : A * A.transpose = 1) :
    (complexCore A).conjTranspose * complexCore A = 1 := by
  ext a b
  have h := congrFun (congrFun hA a) b
  simp only [_root_.Matrix.mul_apply, _root_.Matrix.transpose_apply,
    _root_.Matrix.one_apply] at h
  apply Complex.ext
  · simpa [complexCore, _root_.Matrix.mul_apply, _root_.Matrix.conjTranspose_apply,
      _root_.Matrix.one_apply, Complex.mul_re, apply_ite] using h
  · simp [complexCore, _root_.Matrix.mul_apply, _root_.Matrix.conjTranspose_apply,
      _root_.Matrix.one_apply, apply_ite]

/-- Equal-rank specialization lands literally in the existing sequential
preparation core type; padding varying ranks is a separate register embedding. -/
def sequentialCore {r : ℕ} (A : Core r r) : SequentialBondPreparation.Core (Fin r) :=
  complexCore A

/-- Exact clean-column semantic adapter, in output-row/input-column order.
This premise concerns one local stage, not the target state or full run. -/
theorem sequential_step {n r : ℕ} (A : Core r r)
    (U : SequentialBondPreparation.Stage (Fin r))
    (hU : ∀ bit b a, U (bit, b) (0, a) = complexCore A (bit, b) a)
    (v : SequentialBondPreparation.BondState n (Fin r))
    (x : PrimitiveBasis (n + 1)) (b : Fin r) :
    SequentialBondPreparation.step U v (x, b) =
      ∑ a, (A a (x (Fin.last n), b) : ℂ) * v (Fin.init x, a) := by
  rw [SequentialBondPreparation.step_apply]
  simp_rw [hU, complexCore]

/-- Embed a varying active bond into a fixed physical register by zero fill. -/
def padVector {d B : ℕ} (v : Fin d → ℂ) (b : Fin B) : ℂ :=
  if h : b.val < d then v ⟨b.val, h⟩ else 0

@[simp] theorem padVector_active {d B : ℕ} (hd : d ≤ B) (v : Fin d → ℂ)
    (a : Fin d) : padVector v (Fin.castLE hd a) = v a := by
  simp [padVector, a.isLt]

/-- Padded matrix has zero output outside the next active rank and specifies
only the active clean-input columns; other completion columns stay free. -/
def paddedCore {l r B : ℕ} (A : Core l r) : SequentialBondPreparation.Core (Fin B) :=
  fun out a => if ha : a.val < l then
    if hb : out.2.val < r then (A ⟨a.val, ha⟩ (out.1, ⟨out.2.val, hb⟩) : ℂ) else 0
    else 0

theorem paddedCore_inactive_output {l r B : ℕ} (A : Core l r)
    (bit : Fin 2) (b a : Fin B) (hb : r ≤ b.val) : paddedCore A (bit, b) a = 0 := by
  simp [paddedCore, Nat.not_lt.mpr hb]

theorem sum_padVector {d B : ℕ} (hd : d ≤ B) (f : Fin B → ℂ) (v : Fin d → ℂ) :
    (∑ a : Fin B, f a * padVector v a) =
      ∑ a : Fin d, f (Fin.castLE hd a) * v a := by
  symm
  simpa only [padVector_active] using ThinLQ.sum_prefix_of_zero hd
    (fun a => f a * padVector v a)
    (fun a ha => by simp [padVector, Nat.not_lt.mpr ha])

/-- Rank-changing local action in the existing sequential semantics. The
only circuit premise is equality on active clean-input columns. The output
is the zero-padded exact core contraction, including every inactive label. -/
theorem sequential_step_padded {n l r B : ℕ} (hl : l ≤ B) (A : Core l r)
    (U : SequentialBondPreparation.Stage (Fin B))
    (columns : ∀ bit b (a : Fin l),
      U (bit, b) (0, Fin.castLE hl a) = paddedCore A (bit, b) (Fin.castLE hl a))
    (v : PrimitiveBasis n × Fin l → ℂ) (x : PrimitiveBasis (n + 1)) (b : Fin B) :
    SequentialBondPreparation.step U
      (fun z => padVector (fun a => v (z.1, a)) z.2) (x, b) =
      padVector (fun c : Fin r =>
        ∑ a : Fin l, (A a (x (Fin.last n), c) : ℂ) * v (Fin.init x, a)) b := by
  rw [SequentialBondPreparation.step_apply]
  change (∑ a, U (x (Fin.last n), b) (0, a) *
    padVector (fun a => v (Fin.init x, a)) a) = _
  rw [sum_padVector hl]
  simp_rw [columns]
  by_cases hb : b.val < r
  · simp [paddedCore, padVector, hb]
  · simp [paddedCore, padVector, hb]

/-- Active columns of a right-canonical core remain orthonormal after
embedding the output into a larger physical register. -/
theorem paddedCore_active_isometry {l r B : ℕ} (hl : l ≤ B) (hr : r ≤ B)
    (A : Core l r) (hA : A * A.transpose = 1) (a c : Fin l) :
    (∑ out : Fin 2 × Fin B,
      star (paddedCore A out (Fin.castLE hl a)) *
        paddedCore A out (Fin.castLE hl c)) = if a = c then 1 else 0 := by
  have h := congrFun (congrFun (complexCore_isometry A hA) a) c
  simp only [_root_.Matrix.mul_apply, _root_.Matrix.conjTranspose_apply,
    _root_.Matrix.one_apply] at h
  rw [Fintype.sum_prod_type]
  have he (bit : Fin 2) :
      (∑ b : Fin B, star (paddedCore A (bit, b) (Fin.castLE hl a)) *
        paddedCore A (bit, b) (Fin.castLE hl c)) =
      ∑ b : Fin r, star (complexCore A (bit, b) a) * complexCore A (bit, b) c := by
    symm
    have hs := ThinLQ.sum_prefix_of_zero hr
      (fun b => star (paddedCore A (bit, b) (Fin.castLE hl a)) *
        paddedCore A (bit, b) (Fin.castLE hl c))
      (fun b hb => by simp [paddedCore, Nat.not_lt.mpr hb])
    simpa [paddedCore, complexCore] using hs
  simp_rw [he]
  simpa only [Fintype.sum_prod_type] using h

end QuantumBlockEncoding.TensorTrainCanonical
