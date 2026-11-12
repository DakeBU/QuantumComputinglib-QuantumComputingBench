import FiniteTrig
import Mathlib.Data.Rat.Floor

/-! Literal rational interval operations used by saved_action.py. This is not
a formal refinement of the Python runtime, nor a full stage matrix certificate. -/
namespace HermiteSavedRounding

structure Interval where
  lo : ℚ
  hi : ℚ
  deriving DecidableEq

def Ordered (a : Interval) : Prop := a.lo ≤ a.hi
def Mem (a : Interval) (x : ℝ) : Prop := (a.lo : ℝ) ≤ x ∧ x ≤ (a.hi : ℝ)
def plus (a b : Interval) : Interval := ⟨a.lo + b.lo, a.hi + b.hi⟩
def negative (a : Interval) : Interval := ⟨-a.hi, -a.lo⟩
def times (a b : Interval) : Interval :=
  ⟨min (min (a.lo*b.lo) (a.lo*b.hi)) (min (a.hi*b.lo) (a.hi*b.hi)),
   max (max (a.lo*b.lo) (a.lo*b.hi)) (max (a.hi*b.lo) (a.hi*b.hi))⟩
def grid (bits : ℕ) : ℚ := 2 ^ bits
def outward (a : Interval) (bits : ℕ) : Interval :=
  ⟨(⌊a.lo * grid bits⌋ : ℚ) / grid bits,
   (⌈a.hi * grid bits⌉ : ℚ) / grid bits⟩
def sine (theta : ℚ) (n bits : ℕ) : Interval :=
  outward ⟨(HermiteFiniteTrig.sinBounds (theta/2) n).1,
    (HermiteFiniteTrig.sinBounds (theta/2) n).2⟩ bits
def cosine (theta : ℚ) (n bits : ℕ) : Interval :=
  outward ⟨(HermiteFiniteTrig.cosBounds (theta/2) n).1,
    (HermiteFiniteTrig.cosBounds (theta/2) n).2⟩ bits
def ryRow (theta : ℚ) (n bits : ℕ) (u v : Interval) : Interval × Interval :=
  (outward (plus (times (cosine theta n bits) u)
    (negative (times (sine theta n bits) v))) bits,
   outward (plus (times (sine theta n bits) u)
    (times (cosine theta n bits) v)) bits)
def midpoint (a : Interval) : ℚ := (a.lo + a.hi) / 2
noncomputable def realRyRow (theta : ℚ) (xy : ℝ × ℝ) : ℝ × ℝ :=
  (Real.cos ((theta:ℝ)/2)*xy.1 - Real.sin ((theta:ℝ)/2)*xy.2,
   Real.sin ((theta:ℝ)/2)*xy.1 + Real.cos ((theta:ℝ)/2)*xy.2)
def rowTrace (angles : List ℚ) (n bits : ℕ) (uv : Interval × Interval) :
    Interval × Interval :=
  angles.foldl (fun p theta => ryRow theta n bits p.1 p.2) uv
noncomputable def realTrace (angles : List ℚ) (xy : ℝ × ℝ) : ℝ × ℝ :=
  angles.foldl (fun p theta => realRyRow theta p) xy

theorem grid_pos (bits : ℕ) : 0 < grid bits := by unfold grid; positivity

private theorem scaled_num (q : ℚ) (bits : ℕ) :
    q * grid bits = ((q.num * (2^bits:ℤ) : ℤ):ℚ) / (q.den:ℚ) := by
  calc
    q * grid bits = ((q.num:ℚ)/(q.den:ℚ)) * grid bits := by rw [Rat.num_div_den]
    _ = _ := by simp only [grid, Int.cast_mul, Int.cast_pow, Int.cast_ofNat]; ring

theorem scaled_floor_num (q : ℚ) (bits : ℕ) :
    ⌊q * grid bits⌋ = (q.num * (2^bits:ℤ)) / (q.den:ℤ) := by
  rw [scaled_num]
  exact Rat.floor_intCast_div_natCast _ _

theorem scaled_ceil_num (q : ℚ) (bits : ℕ) :
    ⌈q * grid bits⌉ = -((-(q.num * (2^bits:ℤ))) / (q.den:ℤ)) := by
  rw [scaled_num]
  exact Rat.ceil_intCast_div_natCast _ _

theorem outward_widening (a : Interval) (bits : ℕ) :
    a.lo - 1 / grid bits < (outward a bits).lo ∧
    (outward a bits).lo ≤ a.lo ∧ a.hi ≤ (outward a bits).hi ∧
    (outward a bits).hi < a.hi + 1 / grid bits := by
  have hg := grid_pos bits
  have hf := Int.floor_le (a.lo * grid bits)
  have hfl := Int.lt_floor_add_one (a.lo * grid bits)
  have hc := Int.le_ceil (a.hi * grid bits)
  have hcl := Int.ceil_lt_add_one (a.hi * grid bits)
  simp only [outward]
  constructor
  · apply (lt_div_iff₀ hg).mpr
    rw [sub_mul, div_mul_cancel₀ _ (ne_of_gt hg)]
    linarith
  constructor
  · exact (div_le_iff₀ hg).mpr hf
  constructor
  · exact (le_div_iff₀ hg).mpr hc
  · apply (div_lt_iff₀ hg).mpr
    rw [add_mul, div_mul_cancel₀ _ (ne_of_gt hg)]
    linarith

theorem outward_mem (a : Interval) (bits : ℕ) (x : ℝ) (hx : Mem a x) :
    Mem (outward a bits) x := by
  have h := outward_widening a bits
  constructor
  · exact (show ((outward a bits).lo : ℝ) ≤ (a.lo:ℝ) by exact_mod_cast h.2.1).trans hx.1
  · exact hx.2.trans (show (a.hi:ℝ) ≤ ((outward a bits).hi:ℝ) by exact_mod_cast h.2.2.1)

theorem mem_ordered (a : Interval) (x : ℝ) (hx : Mem a x) : Ordered a := by
  exact_mod_cast hx.1.trans hx.2

theorem plus_mem (a b : Interval) (x y : ℝ) (hx : Mem a x) (hy : Mem b y) :
    Mem (plus a b) (x+y) := by
  simp only [Mem, plus, Rat.cast_add] at *
  constructor <;> linarith [hx.1, hx.2, hy.1, hy.2]

theorem negative_mem (a : Interval) (x : ℝ) (hx : Mem a x) :
    Mem (negative a) (-x) := by
  simp only [Mem, negative, Rat.cast_neg] at *
  constructor <;> linarith [hx.1, hx.2]

private theorem linear_bounds (l h x y : ℝ) (hl : l ≤ x) (hh : x ≤ h) :
    min (l*y) (h*y) ≤ x*y ∧ x*y ≤ max (l*y) (h*y) := by
  by_cases hy : 0 ≤ y
  · constructor
    · exact (min_le_left _ _).trans (mul_le_mul_of_nonneg_right hl hy)
    · exact (mul_le_mul_of_nonneg_right hh hy).trans (le_max_right _ _)
  · have hy' : y ≤ 0 := le_of_lt (lt_of_not_ge hy)
    constructor
    · exact (min_le_right _ _).trans (mul_le_mul_of_nonpos_right hh hy')
    · exact (mul_le_mul_of_nonpos_right hl hy').trans (le_max_left _ _)

theorem times_mem (a b : Interval) (x y : ℝ) (hx : Mem a x) (hy : Mem b y) :
    Mem (times a b) (x*y) := by
  have h := linear_bounds a.lo a.hi x y hx.1 hx.2
  have hl : min ((a.lo:ℝ)*b.lo) ((a.lo:ℝ)*b.hi) ≤ (a.lo:ℝ)*y ∧
      (a.lo:ℝ)*y ≤ max ((a.lo:ℝ)*b.lo) ((a.lo:ℝ)*b.hi) := by
    simpa only [mul_comm] using linear_bounds b.lo b.hi y a.lo hy.1 hy.2
  have hh : min ((a.hi:ℝ)*b.lo) ((a.hi:ℝ)*b.hi) ≤ (a.hi:ℝ)*y ∧
      (a.hi:ℝ)*y ≤ max ((a.hi:ℝ)*b.lo) ((a.hi:ℝ)*b.hi) := by
    simpa only [mul_comm] using linear_bounds b.lo b.hi y a.hi hy.1 hy.2
  simp only [Mem, times, Rat.cast_min, Rat.cast_max, Rat.cast_mul]
  constructor
  · exact (le_min ((min_le_left _ _).trans hl.1)
      ((min_le_right _ _).trans hh.1)).trans h.1
  · exact h.2.trans (max_le (hl.2.trans (le_max_left _ _))
      (hh.2.trans (le_max_right _ _)))

theorem sine_mem (theta : ℚ) (n bits : ℕ) :
    Mem (sine theta n bits) (Real.sin ((theta:ℝ)/2)) := by
  apply outward_mem
  simpa only [Mem, Rat.cast_div, Rat.cast_ofNat] using HermiteFiniteTrig.sin_mem (theta/2) n

theorem cosine_mem (theta : ℚ) (n bits : ℕ) :
    Mem (cosine theta n bits) (Real.cos ((theta:ℝ)/2)) := by
  apply outward_mem
  simpa only [Mem, Rat.cast_div, Rat.cast_ofNat] using HermiteFiniteTrig.cos_mem (theta/2) n

theorem ryRow_mem (theta : ℚ) (n bits : ℕ) (u v : Interval) (x y : ℝ)
    (hu : Mem u x) (hv : Mem v y) :
    Mem (ryRow theta n bits u v).1
      (Real.cos ((theta:ℝ)/2)*x - Real.sin ((theta:ℝ)/2)*y) ∧
    Mem (ryRow theta n bits u v).2
      (Real.sin ((theta:ℝ)/2)*x + Real.cos ((theta:ℝ)/2)*y) := by
  constructor
  · exact outward_mem _ _ _ (by
      simpa only [sub_eq_add_neg] using plus_mem _ _ _ _
        (times_mem _ _ _ _ (cosine_mem theta n bits) hu)
        (negative_mem _ _ (times_mem _ _ _ _ (sine_mem theta n bits) hv)))
  · exact outward_mem _ _ _ (plus_mem _ _ _ _
      (times_mem _ _ _ _ (sine_mem theta n bits) hu)
      (times_mem _ _ _ _ (cosine_mem theta n bits) hv))

theorem midpoint_error (a : Interval) (x : ℝ) (hx : Mem a x) :
    |x - (midpoint a : ℝ)| ≤ (((a.hi-a.lo)/2 : ℚ):ℝ) := by
  simp only [midpoint, Rat.cast_div, Rat.cast_add, Rat.cast_sub, Rat.cast_ofNat]
  apply abs_le.mpr
  constructor <;> linarith [hx.1, hx.2]

theorem rowTrace_mem (angles : List ℚ) (n bits : ℕ)
    (uv : Interval × Interval) (xy : ℝ × ℝ)
    (hu : Mem uv.1 xy.1) (hv : Mem uv.2 xy.2) :
    Mem (rowTrace angles n bits uv).1 (realTrace angles xy).1 ∧
    Mem (rowTrace angles n bits uv).2 (realTrace angles xy).2 := by
  induction angles generalizing uv xy with
  | nil => exact ⟨hu, hv⟩
  | cons theta rest ih =>
    have h := ryRow_mem theta n bits uv.1 uv.2 xy.1 xy.2 hu hv
    exact ih (ryRow theta n bits uv.1 uv.2) (realRyRow theta xy) h.1 h.2

end HermiteSavedRounding
