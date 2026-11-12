import QuantumBlockEncoding.ConstructiveThinLQ
import QuantumBlockEncoding.TensorTrainCanonical

/-!
# Deterministic exact-real tensor-train canonicalization

The producer recursively canonicalizes the actual tail, absorbs its residual
into the current core, and calls deterministic thin LQ. The output contains
the actual residual and actual rank-reduced right-canonical chain. All-word
action and normalized-boundary theorems certify that output, without choosing
a chain or factor from an existence theorem. Arithmetic evaluation and storage
costs are separate refinement obligations.
-/

namespace QuantumBlockEncoding.ConstructiveTensorTrain

open scoped BigOperators
open TensorTrainCanonical

/-- The physical bit/right-bond indexing is retained in the returned core. -/
structure CoreFactorization {l r : ℕ} (A : Core l r) where
  R : _root_.Matrix (Fin l) (Fin (min l (2 * r))) ℝ
  Q : Core (min l (2 * r)) r
  factorization : A = R * Q
  orthogonal : Q * Q.transpose = 1

/-- Relabel the deterministic matrix factors by the explicit product index. -/
noncomputable def factorCore {l r : ℕ} (A : Core l r) : CoreFactorization A := by
  let e : Fin 2 × Fin r ≃ Fin (2 * r) := finProdFinEquiv
  let factors := ConstructiveThinLQ.factor (fun a j => A a (e.symm j))
  refine ⟨factors.R, fun a j => factors.Q a (e j), ?_, ?_⟩
  · ext a j
    change A a j = ∑ k, factors.R a k * factors.Q k (e j)
    simpa only [Equiv.symm_apply_apply, _root_.Matrix.mul_apply] using
      congrFun (congrFun factors.factorization a) (e j)
  · ext a b
    have h := congrFun (congrFun factors.orthogonal a) b
    simp only [_root_.Matrix.mul_apply, _root_.Matrix.transpose_apply] at h ⊢
    exact (e.sum_comp (fun j => factors.Q a j * factors.Q b j)).trans h

/-- Concrete canonical data, indexed by the precise original chain. -/
structure Result {n l r : ℕ} (C : Chain n l r) where
  rank : ℕ
  residual : _root_.Matrix (Fin l) (Fin rank) ℝ
  canonical : Chain n rank r
  rightCanonical : RightCanonical canonical
  rankReduced : RankReduced C canonical
  action : ∀ x, contract C x = residual * contract canonical x

/-- Structural recursion on the source chain; no factor or basis selection. -/
noncomputable def canonicalize : {n l r : ℕ} → (C : Chain n l r) → Result C
  | _, _, _, .nil r =>
      { rank := r, residual := 1, canonical := .nil r,
        rightCanonical := trivial, rankReduced := .nil r,
        action := fun _ => by simp [contract] }
  | _, l, _, .cons A C =>
      let tailResult := canonicalize C
      let headResult := factorCore (absorb A tailResult.residual)
      { rank := min l (2 * tailResult.rank), residual := headResult.R,
        canonical := .cons headResult.Q tailResult.canonical,
        rightCanonical := ⟨headResult.orthogonal, tailResult.rightCanonical⟩,
        rankReduced := .cons tailResult.rankReduced,
        action := by
          intro x
          change slice A x.1 * contract C x.2 =
            headResult.R * (slice headResult.Q x.1 * contract tailResult.canonical x.2)
          rw [tailResult.action, ← _root_.Matrix.mul_assoc, ← absorb_slice]
          have hs : slice (absorb A tailResult.residual) x.1 =
              headResult.R * slice headResult.Q x.1 := by
            ext a b
            exact congrFun (congrFun headResult.factorization a) (x.1, b)
          rw [hs, _root_.Matrix.mul_assoc] }

theorem canonicalize_rightCanonical {n l r : ℕ} (C : Chain n l r) :
    RightCanonical (canonicalize C).canonical := (canonicalize C).rightCanonical

theorem canonicalize_rankReduced {n l r : ℕ} (C : Chain n l r) :
    RankReduced C (canonicalize C).canonical := (canonicalize C).rankReduced

theorem canonicalize_action {n l r : ℕ} (C : Chain n l r) (x : Word n) :
    contract C x = (canonicalize C).residual * contract (canonicalize C).canonical x :=
  (canonicalize C).action x

theorem canonicalize_maxBond_le {n l r : ℕ} (C : Chain n l r) :
    maxBond (canonicalize C).canonical ≤ maxBond C :=
  (canonicalize C).rankReduced.maxBond_le

/-- The returned residual converts an original boundary into its new boundary. -/
noncomputable def boundary {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) :
    Fin (canonicalize C).rank → ℝ := _root_.Matrix.vecMul v (canonicalize C).residual

theorem boundary_action {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) (x : Word n) :
    _root_.Matrix.vecMul v (contract C x) =
      _root_.Matrix.vecMul (boundary C v) (contract (canonicalize C).canonical x) := by
  rw [canonicalize_action, ← _root_.Matrix.vecMul_vecMul]
  rfl

/-- Total source mass is obtained from the small returned residual boundary. -/
theorem boundary_mass {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) :
    chainMass C v = mass (boundary C v) :=
  residual_mass C (canonicalize C).canonical (canonicalize C).residual
    (canonicalize C).rightCanonical (canonicalize C).action v

theorem boundary_normalized {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ)
    (normalized : chainMass C v = 1) : mass (boundary C v) = 1 :=
  (boundary_mass C v).symm.trans normalized

/-- Concrete scalar-boundary state data, without requiring normalization. -/
noncomputable def stateBoundary {n : ℕ} (C : Chain n 1 1) :
    Fin (canonicalize C).rank → ℝ := boundary C (fun _ => 1)

theorem stateBoundary_action {n : ℕ} (C : Chain n 1 1) (x : Word n) :
    contract C x 0 0 = ∑ a, stateBoundary C a * contract (canonicalize C).canonical x a 0 := by
  have h := congrFun (congrFun (canonicalize_action C x) 0) 0
  simpa [stateBoundary, boundary, _root_.Matrix.mul_apply, _root_.Matrix.vecMul,
    dotProduct] using h

theorem stateBoundary_normalized {n : ℕ} (C : Chain n 1 1)
    (normalized : (∑ x : Word n, (contract C x 0 0) ^ 2) = 1) :
    mass (stateBoundary C) = 1 := by
  apply boundary_normalized
  simpa [chainMass, mass, _root_.Matrix.vecMul, dotProduct] using normalized

end QuantumBlockEncoding.ConstructiveTensorTrain
