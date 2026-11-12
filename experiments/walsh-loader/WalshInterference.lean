import QuantumBlockEncoding.PrimitiveMacros

/-!
Experimental exact interference spine for arXiv:2307.08384v3 Eq. (3).
Data labels precede the ancilla. No packed bit order or Walsh parity map is chosen.
The output is an actual composition of matrix actions, not the branch formula.
-/

namespace QuantumBlockEncoding.WalshInterference

open scoped BigOperators

variable {α : Type*} [Fintype α] [DecidableEq α]

/-- Literal data-preserving lift of a one-qubit matrix. -/
noncomputable def ancillaMatrix (G : _root_.Matrix (Fin 2) (Fin 2) ℂ) :
    _root_.Matrix (α × Fin 2) (α × Fin 2) ℂ :=
  fun p q => if p.1 = q.1 then G p.2 q.2 else 0

/-- Controlled sampled diagonal: identity at ancilla zero, z(x) at one. -/
noncomputable def controlledDiagonal (z : α → ℂ) :
    _root_.Matrix (α × Fin 2) (α × Fin 2) ℂ :=
  _root_.Matrix.diagonal (fun p => if p.2 = 0 then 1 else z p.1)

def initialState (s : α → ℂ) : α × Fin 2 → ℂ :=
  fun p => if p.2 = 0 then s p.1 else 0

noncomputable def interferenceOutput (z s : α → ℂ) : α × Fin 2 → ℂ :=
  (ancillaMatrix (phaseMatrix (-Real.pi / 2))).mulVec
    ((ancillaMatrix hadamardMatrix).mulVec
      ((controlledDiagonal z).mulVec
        ((ancillaMatrix hadamardMatrix).mulVec (initialState s))))

noncomputable def sampledPhase (f : α → ℝ) (tau : ℝ) (x : α) : ℂ :=
  Complex.exp (((-tau * f x : ℝ) : ℂ) * Complex.I)

noncomputable def sampledOutput (f : α → ℝ) (tau : ℝ) (s : α → ℂ) :
    α × Fin 2 → ℂ := interferenceOutput (sampledPhase f tau) s

theorem ancillaMatrix_mulVec (G : _root_.Matrix (Fin 2) (Fin 2) ℂ)
    (v : α × Fin 2 → ℂ) (x : α) (a : Fin 2) :
    (ancillaMatrix G).mulVec v (x, a) =
      G a 0 * v (x, 0) + G a 1 * v (x, 1) := by
  simp [ancillaMatrix, _root_.Matrix.mulVec, dotProduct, Fintype.sum_prod_type,
    Fin.sum_univ_two, ite_mul]

theorem controlledDiagonal_mulVec (z : α → ℂ) (v : α × Fin 2 → ℂ)
    (x : α) (a : Fin 2) :
    (controlledDiagonal z).mulVec v (x, a) =
      (if a = 0 then 1 else z x) * v (x, a) := by
  simp [controlledDiagonal, _root_.Matrix.mulVec_diagonal]

private theorem phase_minus_half_pi :
    Complex.exp (((-Real.pi / 2 : ℝ) : ℂ) * Complex.I) = -Complex.I := by
  rw [Complex.exp_ofReal_mul_I]
  simp only [neg_div, Real.cos_neg, Real.sin_neg, Real.cos_pi_div_two,
    Real.sin_pi_div_two, Complex.ofReal_zero, Complex.ofReal_neg,
    Complex.ofReal_one, zero_add, neg_one_mul]

private theorem hadamard_scale_square :
    ((Real.sqrt 2 / 2 : ℝ) : ℂ) ^ 2 = (1 / 2 : ℂ) := by
  have hs : (Real.sqrt 2) ^ 2 = (2 : ℝ) := Real.sq_sqrt (by norm_num)
  have hr : (Real.sqrt 2 / 2 : ℝ) ^ 2 = 1 / 2 := by nlinarith
  rw [← Complex.ofReal_pow, hr]
  norm_num

theorem interference_branches (z s : α → ℂ) (x : α) :
    interferenceOutput z s (x, 0) = (1 + z x) * s x / 2 ∧
    interferenceOutput z s (x, 1) = -Complex.I * (1 - z x) * s x / 2 := by
  have hs := hadamard_scale_square
  constructor <;>
    simp only [interferenceOutput, ancillaMatrix_mulVec, controlledDiagonal_mulVec,
      initialState, hadamardMatrix_apply, phaseMatrix_apply, phase_minus_half_pi,
      Fin.isValue, ↓reduceIte, Fin.reduceEq, one_mul, zero_mul, add_zero,
      mul_zero, Fin.val_zero, Fin.val_one]
  · linear_combination hs * s x * (1 + z x)
  · linear_combination hs * (-Complex.I) * s x * (1 - z x)

theorem sampled_branches (f : α → ℝ) (tau : ℝ) (s : α → ℂ) (x : α) :
    sampledOutput f tau s (x, 0) = (1 + sampledPhase f tau x) * s x / 2 ∧
    sampledOutput f tau s (x, 1) = -Complex.I * (1 - sampledPhase f tau x) * s x / 2 :=
  interference_branches (sampledPhase f tau) s x

theorem constant_branches (c tau : ℝ) (s : α → ℂ) (x : α) :
    sampledOutput (fun _ => c) tau s (x, 0) =
      (1 + Complex.exp (((-tau * c : ℝ) : ℂ) * Complex.I)) * s x / 2 ∧
    sampledOutput (fun _ => c) tau s (x, 1) =
      -Complex.I * (1 - Complex.exp (((-tau * c : ℝ) : ℂ) * Complex.I)) * s x / 2 :=
  sampled_branches (fun _ => c) tau s x

theorem omitted_constant_zero (s : α → ℂ) (x : α) :
    interferenceOutput (fun _ => 1) s (x, 1) = 0 := by
  simpa using (interference_branches (fun _ => 1) s x).2

omit [Fintype α] in
/-- A controlled constant phase is exactly an ancilla phase gate, not a
    discardable global phase on the joint register. -/
theorem controlled_constant_phase (c tau : ℝ) :
    controlledDiagonal (sampledPhase (fun _ : α => c) tau) =
      ancillaMatrix (phaseMatrix (-tau * c)) := by
  ext ⟨x, a⟩ ⟨y, b⟩
  by_cases h : x = y
  · subst y
    fin_cases a <;> fin_cases b <;>
      simp [controlledDiagonal, _root_.Matrix.diagonal, ancillaMatrix,
        phaseMatrix_apply, sampledPhase]
  · simp [controlledDiagonal, _root_.Matrix.diagonal, ancillaMatrix,
      h, Prod.mk.injEq]

/-- Exact branch mass; it is a Born probability only for normalized input. -/
noncomputable def acceptedMass (f : α → ℝ) (tau : ℝ) (s : α → ℂ) : ℝ :=
  ∑ x, Complex.normSq (sampledOutput f tau s (x, 1))

private theorem phase_difference_normSq (theta : ℝ) :
    Complex.normSq (1 - Complex.exp ((theta : ℂ) * Complex.I)) =
      4 * Real.sin (theta / 2) ^ 2 := by
  have ht := Real.sin_sq_add_cos_sq theta
  have hh := Real.sin_sq_add_cos_sq (theta / 2)
  have hc := Real.cos_two_mul (theta / 2)
  rw [show 2 * (theta / 2) = theta by ring] at hc
  simp only [Complex.normSq_apply, Complex.sub_re, Complex.sub_im,
    Complex.one_re, Complex.one_im, Complex.exp_ofReal_mul_I_re,
    Complex.exp_ofReal_mul_I_im]
  nlinarith

theorem accepted_mass_exact (f : α → ℝ) (tau : ℝ) (s : α → ℂ) :
    acceptedMass f tau s = ∑ x, Complex.normSq (s x) *
      Real.sin (tau * f x / 2) ^ 2 := by
  unfold acceptedMass
  apply Finset.sum_congr rfl
  intro x _
  rw [(sampled_branches f tau s x).2]
  simp only [Complex.normSq_div, Complex.normSq_mul, Complex.normSq_neg,
    Complex.normSq_I, one_mul]
  rw [sampledPhase, phase_difference_normSq]
  simp [neg_mul, neg_div, Real.sin_neg]
  ring

theorem uniform_accepted_mass (n : ℕ) (f : Fin (2 ^ n) → ℝ) (tau : ℝ) :
    acceptedMass f tau
      (fun _ => ((1 / Real.sqrt ((2 ^ n : ℕ) : ℝ) : ℝ) : ℂ)) =
      (∑ x : Fin (2 ^ n), Real.sin (tau * f x / 2) ^ 2) /
        ((2 ^ n : ℕ) : ℝ) := by
  have hp : (0 : ℝ) < ((2 ^ n : ℕ) : ℝ) := by positivity
  have hs : Real.sqrt ((2 ^ n : ℕ) : ℝ) * Real.sqrt ((2 ^ n : ℕ) : ℝ) =
      ((2 ^ n : ℕ) : ℝ) := Real.mul_self_sqrt (le_of_lt hp)
  rw [accepted_mass_exact]
  simp only [Complex.normSq_ofReal]
  simp_rw [div_mul_div_comm, one_mul, hs, div_mul_eq_mul_div]
  rw [Finset.sum_div]
  simp only [one_mul]

theorem constant_pi_accepted (s : α → ℂ) (x : α) :
    sampledOutput (fun _ => 1) Real.pi s (x, 1) = -Complex.I * s x := by
  rw [(constant_branches 1 Real.pi s x).2]
  rw [show -Real.pi * (1 : ℝ) = -Real.pi by ring,
    Complex.exp_ofReal_mul_I]
  simp only [Real.cos_neg, Real.sin_neg, Real.cos_pi, Real.sin_pi,
    neg_zero, Complex.ofReal_neg, Complex.ofReal_one, Complex.ofReal_zero,
    zero_mul, add_zero]
  ring

end QuantumBlockEncoding.WalshInterference

/- Focused symbolic regression tests. These are exact Lean proofs, not numerical
   simulations. Fin 1 covers a data register of zero qubits. -/
namespace QuantumBlockEncoding.WalshInterference.Tests

example (s : Fin 1 → ℂ) :
    interferenceOutput (fun _ => 1) s (0, 1) = 0 :=
  omitted_constant_zero s 0

example : sampledOutput (fun _ : Fin 1 => 1) Real.pi (fun _ => 1) (0, 1) =
    -Complex.I := by
  simpa using constant_pi_accepted (fun _ : Fin 1 => (1 : ℂ)) 0

example : sampledOutput (fun _ : Fin 1 => 1) Real.pi (fun _ => 1) (0, 1) ≠
    interferenceOutput (fun _ : Fin 1 => 1) (fun _ => 1) (0, 1) := by
  rw [constant_pi_accepted, omitted_constant_zero]
  simp

example {α : Type*} [Fintype α] [DecidableEq α] (s : α → ℂ) (x : α) :
    sampledOutput (fun _ => 0) (1 : ℝ) s (x, 1) = 0 := by
  rw [(sampled_branches (fun _ => 0) 1 s x).2]
  simp [sampledPhase]

example {α : Type*} [Fintype α] [DecidableEq α] (f : α → ℝ) (s : α → ℂ)
    (x : α) : sampledOutput f 0 s (x, 1) = 0 := by
  rw [(sampled_branches f 0 s x).2]
  simp [sampledPhase]

example (f : Fin 1 → ℝ) (tau : ℝ) :
    acceptedMass f tau (fun _ => 1) = Real.sin (tau * f 0 / 2) ^ 2 := by
  simp [accepted_mass_exact]

#check @interference_branches
#check @sampled_branches
#check @controlled_constant_phase
#check @accepted_mass_exact
#check @uniform_accepted_mass
#check @constant_pi_accepted
#print axioms interference_branches
#print axioms sampled_branches
#print axioms controlled_constant_phase
#print axioms accepted_mass_exact
#print axioms uniform_accepted_mass
#print axioms constant_pi_accepted

end QuantumBlockEncoding.WalshInterference.Tests
