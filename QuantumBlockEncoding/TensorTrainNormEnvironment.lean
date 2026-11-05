import QuantumBlockEncoding.TensorTrainCanonical

/-!
# Local Gram environments for tensor-train norms

Compute the full squared norm by one small Gram matrix per core, without
forming the exponentially sized amplitude vector. The semantics theorem
identifies this local recursion with the full word sum. Storage and explicit
naive real-arithmetic budgets are separate from finite-bit implementation.
-/

namespace QuantumBlockEncoding.TensorTrainNormEnvironment

open scoped BigOperators
open TensorTrainCanonical

/-- Right Gram environment. Each update uses only two local matrix products
per physical bit, with the previous environment as its right factor. -/
noncomputable def gram : {n l r : ℕ} → Chain n l r → _root_.Matrix (Fin l) (Fin l) ℝ
  | _, _, _, .nil r => 1
  | _, _, _, .cons A C =>
      let E := gram C
      ∑ bit : Fin 2, slice A bit * E * (slice A bit).transpose

/-- Exact semantics of the small-matrix recursion, including every terminal
bond label. The full word sum appears only in the specification. -/
theorem gram_eq_sum {n l r : ℕ} (C : Chain n l r) :
    gram C = ∑ x : Word n, contract C x * (contract C x).transpose := by
  induction C with
  | nil r =>
    change (1 : _root_.Matrix (Fin r) (Fin r) ℝ) =
      ∑ _x : Unit, (1 : _root_.Matrix (Fin r) (Fin r) ℝ) *
        (1 : _root_.Matrix (Fin r) (Fin r) ℝ).transpose
    simp
  | @cons n l m r A C ih =>
    change (∑ bit : Fin 2, slice A bit * gram C * (slice A bit).transpose) =
      ∑ x : Fin 2 × Word n, (slice A x.1 * contract C x.2) *
        (slice A x.1 * contract C x.2).transpose
    rw [Fintype.sum_prod_type, ih]
    simp only [_root_.Matrix.transpose_mul, _root_.Matrix.mul_sum, _root_.Matrix.sum_mul,
      _root_.Matrix.mul_assoc]

/-- A scalar-boundary train's environment entry is its complete squared norm. -/
theorem gram_scalar {n : ℕ} (C : Chain n 1 1) :
    gram C 0 0 = ∑ x : Word n, (contract C x 0 0) ^ 2 := by
  rw [gram_eq_sum]
  simp [_root_.Matrix.sum_apply, _root_.Matrix.mul_apply, _root_.Matrix.transpose_apply, pow_two]

theorem gram_scalar_nonneg {n : ℕ} (C : Chain n 1 1) : 0 ≤ gram C 0 0 := by
  rw [gram_scalar]
  exact Finset.sum_nonneg (fun _ _ => sq_nonneg _)

/-- Local-core norm supplier; only one square root is performed after the Gram
recursion. This is meaningful for zero trains as well as normalized trains. -/
noncomputable def norm {n : ℕ} (C : Chain n 1 1) : ℝ := Real.sqrt (gram C 0 0)

theorem norm_eq {n : ℕ} (C : Chain n 1 1) :
    norm C = Real.sqrt (∑ x : Word n, (contract C x 0 0) ^ 2) := by
  rw [norm, gram_scalar]

theorem norm_sq {n : ℕ} (C : Chain n 1 1) :
    norm C ^ 2 = ∑ x : Word n, (contract C x 0 0) ^ 2 := by
  rw [norm, Real.sq_sqrt (gram_scalar_nonneg C), gram_scalar]

theorem norm_pos_of_nonzero {n : ℕ} (C : Chain n 1 1)
    (h : ∃ x, contract C x 0 0 ≠ 0) : 0 < norm C := by
  rw [norm, Real.sqrt_pos, gram_scalar]
  obtain ⟨x, hx⟩ := h
  exact Finset.sum_pos' (fun _ _ => sq_nonneg _) ⟨x, Finset.mem_univ _, sq_pos_of_ne_zero hx⟩

/-- A reusable target adapter. This identifies a proven core action with the
target norm; it does not assume the norm supplier is already correct. -/
theorem norm_eq_of_contract {n : ℕ} {I : Type*} [Fintype I]
    (C : Chain n 1 1) (e : Word n ≃ I) (target : I → ℝ)
    (h : ∀ x, contract C x 0 0 = target (e x)) :
    norm C = Real.sqrt (∑ i : I, target i ^ 2) := by
  rw [norm_eq]
  simp_rw [h]
  rw [e.sum_comp (fun i => target i ^ 2)]

/-- Storage if every intermediate environment is retained. Streaming can use
less; no exponential word address occurs in this definition. -/
def environmentScalars : {n l r : ℕ} → Chain n l r → ℕ
  | _, _, r, .nil _ => r ^ 2
  | _, l, _, .cons _ C => l ^ 2 + environmentScalars C

theorem environmentScalars_le {n l r : ℕ} (C : Chain n l r) (D : ℕ)
    (hD : maxBond C ≤ D) : environmentScalars C ≤ (n + 1) * D ^ 2 := by
  induction C with
  | nil r =>
    simp only [environmentScalars, maxBond, zero_add, one_mul] at *
    exact Nat.pow_le_pow_left hD 2
  | @cons n l m r A C ih =>
    have hl : l ≤ D := (max_le_iff.mp hD).1
    have ht : maxBond C ≤ D := (max_le_iff.mp hD).2
    have hs := Nat.pow_le_pow_left hl 2
    have hc := ih ht
    simp only [environmentScalars]
    nlinarith

/-- A conservative count for direct dense real arithmetic at one update:
two bits, products (l by m)*(m by m) and (l by m)*(m by l), charging
one multiplication and at most one addition per inner-product term, then
l^2 additions to combine the two bits. Copies/transposes are index views. -/
def updateArithmeticBudget (l m : ℕ) : ℕ := 4 * (l * m * m + l * l * m) + l * l

/-- Syntactic real-operation budget of the stated local evaluation schedule.
This is not a cost semantics for an external runtime or finite-bit arithmetic. -/
def arithmeticBudget : {n l r : ℕ} → Chain n l r → ℕ
  | _, _, _, .nil _ => 0
  | _, l, _, @Chain.cons _ _ m _ _ C => updateArithmeticBudget l m + arithmeticBudget C

theorem updateArithmeticBudget_le (l m D : ℕ) (hl : l ≤ D) (hm : m ≤ D) :
    updateArithmeticBudget l m ≤ 9 * D ^ 3 := by
  have h1 : l * m * m ≤ D * D * D :=
    Nat.mul_le_mul (Nat.mul_le_mul hl hm) hm
  have h2 : l * l * m ≤ D * D * D :=
    Nat.mul_le_mul (Nat.mul_le_mul hl hl) hm
  have h3 : l * l ≤ D * D := Nat.mul_le_mul hl hl
  have h4 : D * D ≤ D * D * D := by
    by_cases hz : D = 0
    · simp [hz]
    · have hd : 1 ≤ D := by omega
      simpa using Nat.mul_le_mul_left (D * D) hd
  unfold updateArithmeticBudget
  nlinarith [h4]

theorem arithmeticBudget_le {n l r : ℕ} (C : Chain n l r) (D : ℕ)
    (hD : maxBond C ≤ D) : arithmeticBudget C ≤ 9 * n * D ^ 3 := by
  induction C with
  | nil r => simp [arithmeticBudget]
  | @cons n l m r A C ih =>
    have hl : l ≤ D := (max_le_iff.mp hD).1
    have ht : maxBond C ≤ D := (max_le_iff.mp hD).2
    have hm : m ≤ D := by
      cases C with
      | nil r => exact ht
      | cons B C => exact (max_le_iff.mp ht).1
    have hu := updateArithmeticBudget_le l m D hl hm
    have hc := ih ht
    simp only [arithmeticBudget]
    nlinarith

end QuantumBlockEncoding.TensorTrainNormEnvironment
