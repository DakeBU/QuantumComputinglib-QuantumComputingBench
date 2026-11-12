import FiniteExp

namespace HermiteFiniteExpDegree

open HermiteFiniteExp

def halfDegree (T b : ℕ) : ℕ := 2*T^2+b+1
def degree (T b : ℕ) : ℕ := 2*halfDegree T b-1
def sourceDegree (epsilon : ℚ) : ℕ := degree (tailCutoff epsilon) (tailCutoff epsilon)

theorem degree_formula (T b : ℕ) : degree T b = 4*T^2+2*b+1 := by
  unfold degree halfDegree
  omega

theorem sourceDegree_size (epsilon : ℚ) :
    sourceDegree epsilon ≤ 4*(Nat.size (max 1 (Nat.ceil (1/epsilon))))^2+
      2*(Nat.size (max 1 (Nat.ceil (1/epsilon))))+1 := by
  unfold sourceDegree
  rw [degree_formula]
  have h := tailCutoff_size epsilon
  gcongr <;> exact h

theorem factorial_block (d : ℕ) : d^d ≤ (2*d).factorial := by
  have h := Nat.factorial_mul_pow_sub_le_factorial (n := d) (m := 2*d) (by omega)
  have hf : 1 ≤ d.factorial := Nat.factorial_pos d
  have hm : d^d ≤ d.factorial*d^d := by
    simpa using Nat.mul_le_mul_right (d^d) hf
  exact hm.trans (by simpa [show 2*d-d = d by omega] using h)

theorem radius_degree (q : ℚ) (T b : ℕ) (hq : |q| ≤ (T : ℚ)) :
    radius q (degree T b) ≤ 1/(2 : ℚ)^(b+1) := by
  let d := halfDegree T b
  have hd : 1 ≤ d := by dsimp [d, halfDegree]; omega
  have hn : degree T b+1 = 2*d := by dsimp [degree, d]; omega
  have hbase : (2 : ℚ)*(T : ℚ)^2 ≤ (d : ℚ) := by
    dsimp [d, halfDegree]
    push_cast
    linarith [Nat.cast_nonneg (α := ℚ) b]
  have hpow : |q|^(2*d)*(2 : ℚ)^d ≤ (d : ℚ)^d := by
    calc
      |q|^(2*d)*(2 : ℚ)^d = (2*|q|^2)^d := by rw [mul_pow, pow_mul]; ring
      _ ≤ (2*(T : ℚ)^2)^d := by gcongr
      _ ≤ (d : ℚ)^d := pow_le_pow_left₀ (by positivity) hbase d
  have hf : (d : ℚ)^d ≤ ((2*d).factorial : ℚ) := by exact_mod_cast factorial_block d
  have hr : radius q (degree T b) ≤ 1/(2 : ℚ)^d := by
    unfold radius
    rw [hn]
    apply (div_le_div_iff₀ (by positivity) (by positivity)).mpr
    simpa using hpow.trans hf
  have hb : b+1 ≤ d := by dsimp [d, halfDegree]; omega
  exact hr.trans (one_div_le_one_div_of_le (by positivity)
    (pow_le_pow_right₀ (by norm_num : (1 : ℚ) ≤ 2) hb))

theorem checked_complete (q epsilon : ℚ) (hq : q ≤ 0) (he : 0 < epsilon) :
    checked q epsilon (tailCutoff epsilon) (sourceDegree epsilon) =
      some (bounds q (tailCutoff epsilon) (sourceDegree epsilon)) := by
  have hw : (bounds q (tailCutoff epsilon) (sourceDegree epsilon)).2-
      (bounds q (tailCutoff epsilon) (sourceDegree epsilon)).1 ≤ epsilon := by
    by_cases hc : q ≤ -(tailCutoff epsilon : ℚ)
    · simpa [bounds, hc] using tailCutoff_budget epsilon he
    · have hr := radius_degree q (tailCutoff epsilon) (tailCutoff epsilon)
        (active_magnitude q (tailCutoff epsilon) hq hc).le
      have hp : (2 : ℚ)^(tailCutoff epsilon) > 0 := by positivity
      have hw' : 2*radius q (sourceDegree epsilon) ≤ tailRadius (tailCutoff epsilon) := by
        unfold sourceDegree
        unfold tailRadius
        rw [pow_succ] at hr
        have := (le_div_iff₀ (by positivity : (0 : ℚ) < 2^tailCutoff epsilon*2)).mp hr
        apply (le_div_iff₀ hp).mpr
        nlinarith
      simp only [bounds, if_neg hc]
      linarith [hw'.trans (tailCutoff_budget epsilon he)]
  simp [checked, hq, he, hw]

theorem complete_enclosure (q epsilon : ℚ) (hq : q ≤ 0) (he : 0 < epsilon) :
    Real.exp (q : ℝ) ∈ Set.Icc
      ((bounds q (tailCutoff epsilon) (sourceDegree epsilon)).1 : ℝ)
      ((bounds q (tailCutoff epsilon) (sourceDegree epsilon)).2 : ℝ) ∧
    (bounds q (tailCutoff epsilon) (sourceDegree epsilon)).2-
      (bounds q (tailCutoff epsilon) (sourceDegree epsilon)).1 ≤ epsilon := by
  exact (checked_sound q epsilon (tailCutoff epsilon) (sourceDegree epsilon) _
    (checked_complete q epsilon hq he)).2

#print axioms factorial_block
#print axioms degree_formula
#print axioms sourceDegree_size
#print axioms radius_degree
#print axioms checked_complete
#print axioms complete_enclosure

end HermiteFiniteExpDegree
