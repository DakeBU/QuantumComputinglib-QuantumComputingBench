import FiniteTrig

namespace HermiteFiniteTrig

def selectDegree (q eps : ℚ) (cap : ℕ) : Option ℕ :=
  (List.range (cap + 1)).find? (fun n => decide (2 * radius q n ≤ eps))

theorem selectDegree_sound (q eps : ℚ) (cap n : ℕ)
    (h : selectDegree q eps cap = some n) : n ≤ cap ∧ 2 * radius q n ≤ eps := by
  have hm : n ∈ List.range (cap + 1) := List.mem_of_find?_eq_some h
  have hp := List.find?_some h
  exact ⟨by simpa using hm, by simpa using hp⟩

theorem selected_sin_sound (q eps : ℚ) (cap n : ℕ)
    (h : selectDegree q eps cap = some n) :
    ((sinBounds q n).1 : ℝ) ≤ Real.sin (q : ℝ) ∧
    Real.sin (q : ℝ) ≤ ((sinBounds q n).2 : ℝ) ∧
    (sinBounds q n).2 - (sinBounds q n).1 ≤ eps := by
  exact ⟨(sin_mem q n).1, (sin_mem q n).2,
    by rw [sin_width]; exact (selectDegree_sound q eps cap n h).2⟩

theorem selected_cos_sound (q eps : ℚ) (cap n : ℕ)
    (h : selectDegree q eps cap = some n) :
    ((cosBounds q n).1 : ℝ) ≤ Real.cos (q : ℝ) ∧
    Real.cos (q : ℝ) ≤ ((cosBounds q n).2 : ℝ) ∧
    (cosBounds q n).2 - (cosBounds q n).1 ≤ eps := by
  exact ⟨(cos_mem q n).1, (cos_mem q n).2,
    by rw [cos_width]; exact (selectDegree_sound q eps cap n h).2⟩

end HermiteFiniteTrig
