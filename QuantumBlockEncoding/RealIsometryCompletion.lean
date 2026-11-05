import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# Prescribed real isometry columns and special-orthogonal completion

An orthonormal family can be placed at arbitrary distinct matrix columns and
completed to an orthogonal matrix. With one unused column, the orientation can
be corrected without modifying any prescribed column. These are classical
existence theorems, not arithmetic algorithms or preprocessing-cost bounds.
-/

namespace QuantumBlockEncoding.RealIsometryCompletion

open scoped BigOperators
open InnerProductSpace

/-- An arbitrary injection specifies the physical positions of the active
columns, so no assumption that they form a prefix is needed. -/
theorem exists_orthogonal_completion {N r : ℕ}
    (V : _root_.Matrix (Fin N) (Fin r) ℝ) (e : Fin r ↪ Fin N)
    (hV : V.transpose * V = 1) :
    ∃ U : _root_.Matrix (Fin N) (Fin N) ℝ,
      U.transpose * U = 1 ∧ ∀ i a, U i (e a) = V i a := by
  classical
  let col : Fin r → EuclideanSpace ℝ (Fin N) := fun a => WithLp.toLp 2 (fun i => V i a)
  have hc : Orthonormal ℝ col := by
    rw [orthonormal_iff_ite]
    intro a b
    have h := congrFun (congrFun hV a) b
    simp only [col, PiLp.inner_apply]
    change (∑ i, V i b * V i a) = if a = b then (1 : ℝ) else 0
    simpa [_root_.Matrix.mul_apply,
      _root_.Matrix.transpose_apply, _root_.Matrix.one_apply, mul_comm] using h
  let f : Fin N → EuclideanSpace ℝ (Fin N) := fun j =>
    if h : ∃ a, e a = j then col h.choose else 0
  have hf (a : Fin r) : f (e a) = col a := by
    dsimp [f]
    split_ifs with h
    · exact congrArg col (e.injective h.choose_spec)
    · exact False.elim (h ⟨a, rfl⟩)
  have ho : Orthonormal ℝ ((Set.range e).restrict f) := by
    rw [orthonormal_iff_ite]
    rintro ⟨i, a, rfl⟩ ⟨j, b, rfl⟩
    change ⟪f (e a), f (e b)⟫_ℝ =
      if (⟨e a, ⟨a, rfl⟩⟩ : Set.range e) = ⟨e b, ⟨b, rfl⟩⟩ then 1 else 0
    rw [hf, hf]
    simpa [Subtype.ext_iff, e.injective.eq_iff] using
      (orthonormal_iff_ite.mp hc a b)
  have hd : Module.finrank ℝ (EuclideanSpace ℝ (Fin N)) = Fintype.card (Fin N) := by simp
  obtain ⟨basis, hb⟩ := ho.exists_orthonormalBasis_extension_of_card_eq hd
  let U : _root_.Matrix (Fin N) (Fin N) ℝ := fun i j => basis j i
  refine ⟨U, ?_, ?_⟩
  · ext a b
    have h := basis.inner_eq_ite a b
    simp only [PiLp.inner_apply] at h
    rw [_root_.Matrix.mul_apply]
    change (∑ i, basis a i * basis b i) = if a = b then (1 : ℝ) else 0
    simpa [mul_comm] using h
  · intro i a
    change basis (e a) i = V i a
    rw [hb (e a) ⟨a, rfl⟩, hf]

/-- Change the sign of one chosen column; every other column is unchanged. -/
def signFlip {N : ℕ} (j : Fin N) : _root_.Matrix (Fin N) (Fin N) ℝ :=
  _root_.Matrix.diagonal (fun i => if i = j then -1 else 1)

theorem signFlip_orthogonal {N : ℕ} (j : Fin N) :
    (signFlip j).transpose * signFlip j = 1 := by
  rw [signFlip, _root_.Matrix.diagonal_transpose, _root_.Matrix.diagonal_mul_diagonal]
  convert (_root_.Matrix.diagonal_one :
    _root_.Matrix.diagonal (1 : Fin N → ℝ) = 1) using 1
  congr 1
  funext i
  by_cases hi : i = j <;> simp [hi]

theorem signFlip_det {N : ℕ} (j : Fin N) : (signFlip j).det = -1 := by
  simp [signFlip, _root_.Matrix.det_diagonal]

theorem mul_signFlip_preserves {N : ℕ} (U : _root_.Matrix (Fin N) (Fin N) ℝ)
    (j i a : Fin N) (ha : a ≠ j) : (U * signFlip j) i a = U i a := by
  simp [signFlip, _root_.Matrix.mul_diagonal, ha]

/-- Correct a negative determinant using a known unused column. All active
columns remain exact, and the result lies in SO(N), not merely O(N). -/
theorem exists_specialOrthogonal_completion_of_unused {N r : ℕ}
    (V : _root_.Matrix (Fin N) (Fin r) ℝ) (e : Fin r ↪ Fin N)
    (hV : V.transpose * V = 1) (unused : Fin N) (hu : ∀ a, e a ≠ unused) :
    ∃ U : _root_.Matrix (Fin N) (Fin N) ℝ,
      U.transpose * U = 1 ∧ U.det = 1 ∧ ∀ i a, U i (e a) = V i a := by
  obtain ⟨U, hU, hc⟩ := exists_orthogonal_completion V e hV
  have hd : U.det * U.det = 1 := by
    have h := congrArg _root_.Matrix.det hU
    simpa [_root_.Matrix.det_mul, _root_.Matrix.det_transpose] using h
  by_cases hpos : U.det = 1
  · exact ⟨U, hU, hpos, hc⟩
  · have hneg : U.det = -1 := (mul_self_eq_one_iff.mp hd).resolve_left hpos
    refine ⟨U * signFlip unused, ?_, ?_, ?_⟩
    · rw [_root_.Matrix.transpose_mul]
      calc
        _ = (signFlip unused).transpose * (U.transpose * U) * signFlip unused := by
          simp only [_root_.Matrix.mul_assoc]
        _ = 1 := by rw [hU, _root_.Matrix.mul_one, signFlip_orthogonal]
    · rw [_root_.Matrix.det_mul, signFlip_det, hneg]
      norm_num
    · intro i a
      rw [mul_signFlip_preserves U unused i (e a) (hu a), hc]

/-- A strict active-dimension bound guarantees a spare orientation column. -/
theorem exists_specialOrthogonal_completion {N r : ℕ} (hr : r < N)
    (V : _root_.Matrix (Fin N) (Fin r) ℝ) (e : Fin r ↪ Fin N)
    (hV : V.transpose * V = 1) :
    ∃ U : _root_.Matrix (Fin N) (Fin N) ℝ,
      U.transpose * U = 1 ∧ U.det = 1 ∧ ∀ i a, U i (e a) = V i a := by
  have hn : ¬ Function.Surjective e := by
    intro hs
    have hcard := Fintype.card_le_of_surjective e hs
    simp only [Fintype.card_fin] at hcard
    omega
  simp only [Function.Surjective, not_forall] at hn
  obtain ⟨unused, hu⟩ := hn
  apply exists_specialOrthogonal_completion_of_unused V e hV unused
  intro a ha
  exact hu ⟨a, ha⟩

end QuantumBlockEncoding.RealIsometryCompletion
