import Mathlib.Analysis.Normed.Ring.Basic
import Mathlib.Tactic

/-! Internal product-error transport for nonunitary numerical surrogates.
It neither creates nor certifies a saved circuit decoder or a Hermite target.
Stages are in chronological order: the latest factor acts on the left. -/

namespace QuantumBlockEncoding.ExperimentalNonunitaryTransport

variable {R : Type*} [NormedRing R] [NormOneClass R]

structure Stage (R : Type*) where
  nominal : R
  surrogate : R
  error : ℝ

def Valid (stages : List (Stage R)) : Prop :=
  ∀ s ∈ stages, 0 ≤ s.error ∧ ‖s.nominal‖ ≤ 1 ∧
    ‖s.surrogate - s.nominal‖ ≤ s.error

def nominalProduct : List (Stage R) → R
  | [] => 1
  | s :: rest => nominalProduct rest * s.nominal

def surrogateProduct : List (Stage R) → R
  | [] => 1
  | s :: rest => surrogateProduct rest * s.surrogate

def growth : List (Stage R) → ℝ
  | [] => 1
  | s :: rest => growth rest * (1 + s.error)

omit [NormOneClass R] in
private theorem valid_tail {s : Stage R} {rest : List (Stage R)}
    (h : Valid (s :: rest)) : Valid rest := by
  intro t ht
  exact h t (List.mem_cons_of_mem s ht)

omit [NormOneClass R] in
private theorem valid_head {s : Stage R} {rest : List (Stage R)}
    (h : Valid (s :: rest)) :
    0 ≤ s.error ∧ ‖s.nominal‖ ≤ 1 ∧ ‖s.surrogate - s.nominal‖ ≤ s.error :=
  h s (List.mem_cons_self)

theorem growth_ge_one (stages : List (Stage R)) (h : Valid stages) :
    1 ≤ growth stages := by
  induction stages with
  | nil => simp [growth]
  | cons s rest ih =>
    have he := (valid_head h).1
    have hg := ih (valid_tail h)
    simp only [growth]
    nlinarith

theorem nominalProduct_norm_le_one (stages : List (Stage R)) (h : Valid stages) :
    ‖nominalProduct stages‖ ≤ 1 := by
  induction stages with
  | nil => simp [nominalProduct]
  | cons s rest ih =>
    have hn := (valid_head h).2.1
    have ht := ih (valid_tail h)
    calc
      ‖nominalProduct (s :: rest)‖ ≤ ‖nominalProduct rest‖ * ‖s.nominal‖ :=
        norm_mul_le _ _
      _ ≤ 1 * 1 := mul_le_mul ht hn (norm_nonneg _) (by norm_num)
      _ = 1 := by ring

theorem surrogateProduct_norm_le_growth (stages : List (Stage R)) (h : Valid stages) :
    ‖surrogateProduct stages‖ ≤ growth stages := by
  induction stages with
  | nil => simp [surrogateProduct, growth]
  | cons s rest ih =>
    have he := (valid_head h).1
    have hn := (valid_head h).2.1
    have hd := (valid_head h).2.2
    have ht := ih (valid_tail h)
    have hg : 0 ≤ growth rest := le_trans (by norm_num) (growth_ge_one rest (valid_tail h))
    have hs : ‖s.surrogate‖ ≤ 1 + s.error := by
      calc
        ‖s.surrogate‖ = ‖(s.surrogate - s.nominal) + s.nominal‖ := by simp
        _ ≤ ‖s.surrogate - s.nominal‖ + ‖s.nominal‖ := norm_add_le _ _
        _ ≤ 1 + s.error := by linarith
    calc
      ‖surrogateProduct (s :: rest)‖ ≤
          ‖surrogateProduct rest‖ * ‖s.surrogate‖ := norm_mul_le _ _
      _ ≤ growth rest * (1 + s.error) := mul_le_mul ht hs (norm_nonneg _) hg
      _ = growth (s :: rest) := rfl

theorem product_error_le (stages : List (Stage R)) (h : Valid stages) :
    ‖surrogateProduct stages - nominalProduct stages‖ ≤ growth stages - 1 := by
  induction stages with
  | nil => simp [surrogateProduct, nominalProduct, growth]
  | cons s rest ih =>
    have he := (valid_head h).1
    have hn := (valid_head h).2.1
    have hd := (valid_head h).2.2
    have ht := ih (valid_tail h)
    have hg : 0 ≤ growth rest := le_trans (by norm_num) (growth_ge_one rest (valid_tail h))
    have hb := surrogateProduct_norm_le_growth rest (valid_tail h)
    have hid : surrogateProduct rest * s.surrogate - nominalProduct rest * s.nominal =
        (surrogateProduct rest - nominalProduct rest) * s.nominal +
          surrogateProduct rest * (s.surrogate - s.nominal) := by noncomm_ring
    calc
      ‖surrogateProduct (s :: rest) - nominalProduct (s :: rest)‖ =
          ‖(surrogateProduct rest - nominalProduct rest) * s.nominal +
            surrogateProduct rest * (s.surrogate - s.nominal)‖ := by
        change ‖surrogateProduct rest * s.surrogate - nominalProduct rest * s.nominal‖ = _
        rw [hid]
      _ ≤ ‖(surrogateProduct rest - nominalProduct rest) * s.nominal‖ +
          ‖surrogateProduct rest * (s.surrogate - s.nominal)‖ := norm_add_le _ _
      _ ≤ ‖surrogateProduct rest - nominalProduct rest‖ * ‖s.nominal‖ +
          ‖surrogateProduct rest‖ * ‖s.surrogate - s.nominal‖ :=
        add_le_add (norm_mul_le _ _) (norm_mul_le _ _)
      _ ≤ (growth rest - 1) * 1 + growth rest * s.error :=
        add_le_add
          (mul_le_mul ht hn (norm_nonneg _) (sub_nonneg.mpr (growth_ge_one rest (valid_tail h))))
          (mul_le_mul hb hd (norm_nonneg _) hg)
      _ = growth (s :: rest) - 1 := by simp only [growth]; ring

noncomputable def expandingStage : Stage ℝ := ⟨1, 11 / 10, 1 / 10⟩

theorem expanding_valid : Valid [expandingStage, expandingStage] := by
  intro s hs
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hs
  rcases hs with rfl | rfl <;>
    norm_num [expandingStage, Real.norm_eq_abs]

theorem expanding_discriminator :
    ‖surrogateProduct [expandingStage, expandingStage] -
        nominalProduct [expandingStage, expandingStage]‖ = (21 : ℝ) / 100 ∧
    (2 : ℝ) / 10 < (21 : ℝ) / 100 ∧
    growth [expandingStage, expandingStage] - 1 = (21 : ℝ) / 100 := by
  norm_num [surrogateProduct, nominalProduct, growth, expandingStage, Real.norm_eq_abs]

#check growth_ge_one
#check nominalProduct_norm_le_one
#check surrogateProduct_norm_le_growth
#check product_error_le
#print axioms growth_ge_one
#print axioms nominalProduct_norm_le_one
#print axioms surrogateProduct_norm_le_growth
#print axioms product_error_le
#print axioms expanding_valid
#print axioms expanding_discriminator

end QuantumBlockEncoding.ExperimentalNonunitaryTransport
