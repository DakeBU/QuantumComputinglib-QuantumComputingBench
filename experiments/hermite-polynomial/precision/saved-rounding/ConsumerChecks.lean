import SavedRounding

namespace HermiteSavedRounding

example : outward ⟨-1/10, 1/5⟩ 0 = ⟨-1, 1⟩ := by
  norm_num [outward, grid, Interval.mk.injEq]
example : outward ⟨-3/8, 5/8⟩ 80 = ⟨-3/8, 5/8⟩ := by
  norm_num [outward, grid, Interval.mk.injEq]
example : times ⟨-2, 3⟩ ⟨-4, 5⟩ = ⟨-12, 15⟩ := by
  norm_num [times, Interval.mk.injEq]
example : plus ⟨-1/3, -1/3⟩ (negative ⟨-1/3, -1/3⟩) = ⟨0, 0⟩ := by
  norm_num [plus, negative, Interval.mk.injEq]

def singleton (q : ℚ) : Interval := ⟨q,q⟩
theorem singleton_mem (q : ℚ) : Mem (singleton q) (q:ℝ) := ⟨le_rfl, le_rfl⟩

theorem actual_first_saved_ry (u v : Interval) (x y : ℝ)
    (hu : Mem u x) (hv : Mem v y) :
    Mem (ryRow (-86958955523179937 / 100000000000000000) 96 80 u v).1
      (realRyRow (-86958955523179937 / 100000000000000000) (x,y)).1 ∧
    Mem (ryRow (-86958955523179937 / 100000000000000000) 96 80 u v).2
      (realRyRow (-86958955523179937 / 100000000000000000) (x,y)).2 :=
  ryRow_mem _ _ _ _ _ _ _ hu hv

theorem literal_column_trace (angles : List ℚ) (n bits : ℕ) (u v : ℚ) :
    Mem (rowTrace angles n bits (singleton u, singleton v)).1
      (realTrace angles ((u:ℝ),(v:ℝ))).1 ∧
    Mem (rowTrace angles n bits (singleton u, singleton v)).2
      (realTrace angles ((u:ℝ),(v:ℝ))).2 :=
  rowTrace_mem angles n bits _ _ (singleton_mem u) (singleton_mem v)

theorem final_column_center_error (angles : List ℚ) (n bits : ℕ) (u v : ℚ) :
    let p := rowTrace angles n bits (singleton u, singleton v)
    let z := realTrace angles ((u:ℝ),(v:ℝ))
    |z.1 - (midpoint p.1:ℝ)| ≤ (((p.1.hi-p.1.lo)/2:ℚ):ℝ) ∧
    |z.2 - (midpoint p.2:ℝ)| ≤ (((p.2.hi-p.2.lo)/2:ℚ):ℝ) := by
  have h := literal_column_trace angles n bits u v
  exact ⟨midpoint_error _ _ h.1, midpoint_error _ _ h.2⟩

#print axioms outward_widening
#print axioms scaled_floor_num
#print axioms scaled_ceil_num
#print axioms times_mem
#print axioms ryRow_mem
#print axioms rowTrace_mem
#print axioms actual_first_saved_ry
#print axioms final_column_center_error
#check outward_mem
#check ryRow_mem
#check rowTrace_mem
#check final_column_center_error

end HermiteSavedRounding
