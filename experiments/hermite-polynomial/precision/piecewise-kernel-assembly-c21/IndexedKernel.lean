import UniformTranslation
import UniformThresholds

namespace HermitePiecewiseAssembly
open scoped BigOperators Matrix
open QuantumBlockEncoding TensorTrainCanonical Matrix

abbrev IKernel (α : Type) := ℕ → Fin 2 → Matrix α α ℝ

noncomputable def ireadout {α : Type} [Fintype α] (K : IKernel α)
    (right : α → ℝ) (start : ℕ) : {n : ℕ} → Word n → α → ℝ
  | 0, _ => right
  | _+1, x => (K start x.1).mulVec (ireadout K right (start+1) x.2)

noncomputable def amplitude {α : Type} [Fintype α] (K : IKernel α)
    (left right : α → ℝ) (start : ℕ) {n : ℕ} (x : Word n) : ℝ :=
  ∑ a, left a * ireadout K right start x a

noncomputable def productKernel {α β : Type} (K : IKernel α) (J : IKernel β) :
    IKernel (α × β) := fun q bit a b => K q bit a.1 b.1 * J q bit a.2 b.2

noncomputable def productBoundary {α β : Type} (l : α → ℝ) (r : β → ℝ) :
    α × β → ℝ := fun a => l a.1*r a.2

theorem product_readout {α β : Type} [Fintype α] [Fintype β]
    (K : IKernel α) (J : IKernel β) (r : α → ℝ) (s : β → ℝ)
    (n start : ℕ) (x : Word n) (a : α × β) :
    ireadout (productKernel K J) (productBoundary r s) start x a =
      ireadout K r start x a.1 * ireadout J s start x a.2 := by
  induction n generalizing start a with
  | zero => rfl
  | succ n ih =>
    simp only [ireadout, mulVec, dotProduct, productKernel, Fintype.sum_prod_type, ih]
    simp only [Finset.sum_mul, Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro b _
    apply Finset.sum_congr rfl
    intro c _
    ring

theorem product_amplitude {α β : Type} [Fintype α] [Fintype β]
    (K : IKernel α) (J : IKernel β) (l r : α → ℝ) (u v : β → ℝ)
    (n start : ℕ) (x : Word n) :
    amplitude (productKernel K J) (productBoundary l u) (productBoundary r v) start x =
      amplitude K l r start x * amplitude J u v start x := by
  simp only [amplitude, product_readout, productBoundary, Fintype.sum_prod_type,
    Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro b _
  ring

noncomputable def sumKernel {α β : Type} (K : IKernel α) (J : IKernel β) :
    IKernel (α ⊕ β) := fun q bit a b => match a,b with
  | .inl a, .inl b => K q bit a b
  | .inr a, .inr b => J q bit a b
  | _,_ => 0

noncomputable def sumBoundary {α β : Type} (l : α → ℝ) (r : β → ℝ) :
    α ⊕ β → ℝ := Sum.elim l r

theorem sum_readout {α β : Type} [Fintype α] [Fintype β]
    (K : IKernel α) (J : IKernel β) (r : α → ℝ) (s : β → ℝ)
    (n start : ℕ) (x : Word n) :
    ireadout (sumKernel K J) (sumBoundary r s) start x =
      sumBoundary (ireadout K r start x) (ireadout J s start x) := by
  induction n generalizing start with
  | zero => rfl
  | succ n ih =>
    funext a
    simp only [ireadout, ih]
    cases a <;> simp [mulVec, dotProduct, Fintype.sum_sum_type,
      sumKernel, sumBoundary]

theorem sum_amplitude {α β : Type} [Fintype α] [Fintype β]
    (K : IKernel α) (J : IKernel β) (l r : α → ℝ) (u v : β → ℝ)
    (n start : ℕ) (x : Word n) :
    amplitude (sumKernel K J) (sumBoundary l u) (sumBoundary r v) start x =
      amplitude K l r start x + amplitude J u v start x := by
  simp only [amplitude, sum_readout]
  simp [Fintype.sum_sum_type, sumBoundary]

noncomputable def reindexKernel {α : Type} {D : ℕ} (e : α ≃ Fin D)
    (K : IKernel α) : MatrixProductChain.Kernel D :=
  fun q bit a b => K q bit (e.symm a) (e.symm b)

theorem reindex_readout {α : Type} [Fintype α] {D : ℕ}
    (e : α ≃ Fin D) (K : IKernel α) (r : α → ℝ)
    (n start : ℕ) (x : Word n) (a : α) :
    MatrixProductChain.readout (reindexKernel e K) (r ∘ e.symm) start x (e a) =
      ireadout K r start x a := by
  induction n generalizing start a with
  | zero => simp [MatrixProductChain.readout, ireadout]
  | succ n ih =>
    simp only [MatrixProductChain.readout, ireadout, mulVec, dotProduct,
      reindexKernel, Equiv.symm_apply_apply]
    exact Fintype.sum_equiv e.symm _ _ (fun b => by simp [← ih])

theorem reindex_contract {α : Type} [Fintype α] {D : ℕ}
    (e : α ≃ Fin D) (K : IKernel α) (l r : α → ℝ)
    (n start : ℕ) (x : Word (n+1)) :
    contract (MatrixProductChain.ofKernel (reindexKernel e K)
      (l ∘ e.symm) (r ∘ e.symm) start n) x 0 0 = amplitude K l r start x := by
  rw [MatrixProductChain.ofKernel_contract]
  unfold amplitude
  exact Fintype.sum_equiv e.symm _ _ (fun b => by simp [← reindex_readout e K r])

theorem canonical_amplitude {D : ℕ} (K : MatrixProductChain.Kernel D)
    (l r : Fin D → ℝ) (n start : ℕ) (x : Word (n+1)) :
    amplitude K l r start x = contract (MatrixProductChain.ofKernel K l r start n) x 0 0 := by
  rw [MatrixProductChain.ofKernel_contract]
  unfold amplitude
  have hr : ∀ {m : ℕ} (y : Word m) (q : ℕ),
      ireadout K r q y = MatrixProductChain.readout K r q y := by
    intro m y q
    induction m generalizing q with
    | zero => rfl
    | succ m ih => simp only [ireadout, MatrixProductChain.readout, ih]
  rw [hr]

#print axioms product_amplitude
#print axioms sum_amplitude
#print axioms reindex_contract
end HermitePiecewiseAssembly
