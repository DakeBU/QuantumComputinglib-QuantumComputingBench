import QuantumBlockEncoding.StoredThinLQ
import QuantumBlockEncoding.ConstructiveTensorTrain

/-!
# Stored, costed tensor-train canonicalization

Input and output cores are stored finite tables. Residual absorption evaluates
each local contraction once through charged reads and field operations, then
materializes its output before deterministic stored thin LQ. No dense all-word
amplitude table or uncharged semantic absorption is evaluated by the producer.
-/

namespace QuantumBlockEncoding.StoredTensorTrain

open scoped BigOperators
open StoredGivens
open TensorTrainCanonical

abbrev StoredCore (l r : ℕ) := StoredMatrix l (2 * r)

def denoteCore {l r : ℕ} (A : StoredCore l r) : Core l r :=
  fun a out => denote A a (finProdFinEquiv out)

inductive StoredChain : ℕ → ℕ → ℕ → Type
  | nil (r : ℕ) : StoredChain 0 r r
  | cons {n l m r : ℕ} (head : StoredCore l m) (tail : StoredChain n m r) :
      StoredChain (n + 1) l r

def denoteChain : {n l r : ℕ} → StoredChain n l r → Chain n l r
  | _, _, _, .nil r => .nil r
  | _, _, _, .cons A C => .cons (denoteCore A) (denoteChain C)

/-- Each callback is invoked once; its arithmetic cost remains charged. -/
noncomputable def sumEntries : {k : ℕ} → (Fin k → Run ℝ) → Run ℝ
  | 0, _ => pure 0
  | k + 1, f => do
      let first ← f 0
      let rest ← sumEntries (fun i : Fin k => f i.succ)
      StoredGivens.add first rest

theorem sumEntries_value {k : ℕ} (f : Fin k → Run ℝ) :
    (sumEntries f).value = ∑ i, (f i).value := by
  induction k with
  | zero => simp [sumEntries, pure, Run.pure]
  | succ k ih =>
      simp only [sumEntries, bind, Run.bind, StoredGivens.add, charge]
      rw [ih, Fin.sum_univ_succ]

theorem sumEntries_cost_le {k : ℕ} (f : Fin k → Run ℝ) (op : Op) (B : ℕ)
    (bound : ∀ i, (f i).cost op ≤ B) :
    (sumEntries f).cost op ≤ k * (B + tick .field op) := by
  induction k with
  | zero => simp [sumEntries, pure, Run.pure]
  | succ k ih =>
      simp only [sumEntries, bind, Run.bind, StoredGivens.add, charge, Pi.add_apply]
      have first := bound 0
      have rest := ih (fun i => f i.succ) (fun i => bound i.succ)
      rw [Nat.succ_mul]
      omega

/-- Multiply the residual into a single bit-preserving output entry. -/
noncomputable def absorptionEntry {l m r : ℕ} (A : StoredCore l m)
    (R : StoredMatrix m r) (a : Fin l) (out : Fin 2 × Fin r) : Run ℝ :=
  sumEntries fun b => do
    let x ← StoredThinLQ.entry A a (finProdFinEquiv (out.1, b))
    let y ← StoredThinLQ.entry R b out.2
    StoredGivens.mul x y

theorem absorptionEntry_value {l m r : ℕ} (A : StoredCore l m)
    (R : StoredMatrix m r) (a : Fin l) (out : Fin 2 × Fin r) :
    (absorptionEntry A R a out).value = absorb (denoteCore A) (denote R) a out := by
  rw [absorptionEntry, sumEntries_value]
  rfl

theorem absorptionEntry_cost_le {l m r : ℕ} (A : StoredCore l m)
    (R : StoredMatrix m r) (a : Fin l) (out : Fin 2 × Fin r) (op : Op) :
    (absorptionEntry A R a out).cost op ≤ m * (4 * tick .read op + 2 * tick .field op) := by
  have h := sumEntries_cost_le (fun b => do
    let x ← StoredThinLQ.entry A a (finProdFinEquiv (out.1, b))
    let y ← StoredThinLQ.entry R b out.2
    StoredGivens.mul x y) op (4 * tick .read op + tick .field op) (by
      intro b
      simp [bind, Run.bind, StoredGivens.mul, charge]
      omega)
  simpa only [absorptionEntry, Nat.add_assoc, ← two_mul] using h

noncomputable def absorption {l m r : ℕ} (A : StoredCore l m)
    (R : StoredMatrix m r) : Run (StoredCore l r) :=
  materialize (fun a j => absorptionEntry A R a (finProdFinEquiv.symm j))

theorem absorption_value {l m r : ℕ} (A : StoredCore l m)
    (R : StoredMatrix m r) :
    denoteCore (absorption A R).value = absorb (denoteCore A) (denote R) := by
  ext a out
  simp only [denoteCore, absorption, materialize, denote, collect_value,
    Equiv.symm_apply_apply]
  exact absorptionEntry_value A R a out

def absorptionBudget (l m r : ℕ) : Cost := fun op =>
  l * (2 * r) * m * (4 * tick .read op + 2 * tick .field op) +
    (l * (2 * r) + l) * (2 * tick .read op + 2 * tick .write op)

theorem absorption_cost_le {l m r : ℕ} (A : StoredCore l m)
    (R : StoredMatrix m r) (op : Op) :
    (absorption A R).cost op ≤ absorptionBudget l m r op := by
  rw [absorption, materialize_cost]
  have h : (∑ a : Fin l, ∑ j : Fin (2 * r),
      (absorptionEntry A R a (finProdFinEquiv.symm j)).cost op) ≤
      l * (2 * r) * (m * (4 * tick .read op + 2 * tick .field op)) := by
    calc
      _ ≤ ∑ _a : Fin l, ∑ _j : Fin (2 * r),
          m * (4 * tick .read op + 2 * tick .field op) := by
        apply Finset.sum_le_sum
        intro a _
        apply Finset.sum_le_sum
        intro j _
        exact absorptionEntry_cost_le A R a _ op
      _ = _ := by simp; ring
  simp only [absorptionBudget]
  nlinarith

structure CoreResult {l r : ℕ} (A : StoredCore l r) where
  R : StoredMatrix l (min l (2 * r))
  Q : StoredCore (min l (2 * r)) r
  factorization : denoteCore A = denote R * denoteCore Q
  orthogonal : denoteCore Q * (denoteCore Q).transpose = 1

noncomputable def factorCore {l r : ℕ} (A : StoredCore l r) : Run (CoreResult A) :=
  let result := StoredThinLQ.compile A
  ⟨{ R := result.value.R, Q := result.value.Q,
     factorization := by
       ext a out
       exact congrFun (congrFun (StoredThinLQ.compile_correct A).1 a) (finProdFinEquiv out),
     orthogonal := by
       ext a b
       have h := congrFun (congrFun (StoredThinLQ.compile_correct A).2 a) b
       simp only [_root_.Matrix.mul_apply, _root_.Matrix.transpose_apply] at h ⊢
       exact (finProdFinEquiv.sum_comp (fun j =>
         denote result.value.Q a j * denote result.value.Q b j)).trans h }, result.cost⟩

structure Result {n l r : ℕ} (C : StoredChain n l r) where
  rank : ℕ
  residual : StoredMatrix l rank
  canonical : StoredChain n rank r
  rightCanonical : RightCanonical (denoteChain canonical)
  rankReduced : RankReduced (denoteChain C) (denoteChain canonical)
  action : ∀ x, contract (denoteChain C) x = denote residual * contract (denoteChain canonical) x
  rank_le : rank ≤ l

/-- Read the input tag/payload and allocate the output chain node. -/
def nodeBudget : Cost := 3 • tick .read + 3 • tick .write

noncomputable def canonicalize : {n l r : ℕ} → (C : StoredChain n l r) → Run (Result C)
  | _, _, _, .nil r =>
      let I := StoredRectangularGivens.identity r
      ⟨{ rank := r, residual := I.value, canonical := .nil r,
         rightCanonical := trivial, rankReduced := .nil r,
         action := fun _ => by simp [denoteChain, contract, I, StoredRectangularGivens.identity_value],
         rank_le := le_rfl }, nodeBudget + I.cost⟩
  | _, l, _, .cons A C =>
      let tailResult := canonicalize C
      let absorbed := absorption A tailResult.value.residual
      let headResult := factorCore absorbed.value
      ⟨{ rank := min l (2 * tailResult.value.rank), residual := headResult.value.R,
         canonical := .cons headResult.value.Q tailResult.value.canonical,
         rightCanonical := ⟨headResult.value.orthogonal, tailResult.value.rightCanonical⟩,
         rankReduced := .cons tailResult.value.rankReduced,
         action := by
           intro x
           change slice (denoteCore A) x.1 * contract (denoteChain C) x.2 =
             denote headResult.value.R *
               (slice (denoteCore headResult.value.Q) x.1 *
                 contract (denoteChain tailResult.value.canonical) x.2)
           rw [tailResult.value.action, ← _root_.Matrix.mul_assoc, ← absorb_slice]
           have hs : slice (absorb (denoteCore A) (denote tailResult.value.residual)) x.1 =
               denote headResult.value.R * slice (denoteCore headResult.value.Q) x.1 := by
             rw [← absorption_value]
             ext a b
             exact congrFun (congrFun headResult.value.factorization a) (x.1, b)
           rw [hs, _root_.Matrix.mul_assoc],
         rank_le := min_le_left _ _ },
       nodeBudget + tailResult.cost + absorbed.cost + headResult.cost⟩

theorem canonicalize_maxBond_le {n l r : ℕ} (C : StoredChain n l r) :
    maxBond (denoteChain (canonicalize C).value.canonical) ≤ maxBond (denoteChain C) :=
  (canonicalize C).value.rankReduced.maxBond_le

private theorem total_add (a b : Cost) :
    StoredRectangularGivens.total (a + b) =
      StoredRectangularGivens.total a + StoredRectangularGivens.total b := by
  simp only [StoredRectangularGivens.total, Pi.add_apply]
  ring

theorem absorption_total_cost_le {l m r : ℕ} (A : StoredCore l m)
    (R : StoredMatrix m r) :
    StoredRectangularGivens.total (absorption A R).cost ≤
      12 * l * m * r + 8 * l * r + 4 * l := by
  have hf := absorption_cost_le A R .field
  have hs := absorption_cost_le A R .sqrt
  have ha := absorption_cost_le A R .angle
  have ht := absorption_cost_le A R .trig
  have hc := absorption_cost_le A R .compare
  have hr := absorption_cost_le A R .read
  have hw := absorption_cost_le A R .write
  have he := absorption_cost_le A R .emit
  simp [absorptionBudget, tick] at hf hs ha ht hc hr hw he
  simp only [StoredRectangularGivens.total]
  nlinarith

theorem factorCore_total_cost_le {l r : ℕ} (A : StoredCore l r) (D : ℕ)
    (hl : l ≤ D) (hr : r ≤ D) :
    StoredRectangularGivens.total (factorCore A).cost ≤
      164 * D ^ 3 + 108 * D ^ 2 + 25 * D + 2 := by
  have bound := StoredThinLQ.compile_total_cost_le A
  change StoredRectangularGivens.total (StoredThinLQ.compile A).cost ≤ _
  calc
    _ ≤ (2 * r) * l * (22 * l + 30 * (2 * r) + 41) +
        5 * (2 * r) * (2 * r) + 6 * l * l + 8 * (2 * r) + 9 * l + 2 := bound
    _ ≤ (2 * D) * D * (22 * D + 30 * (2 * D) + 41) +
        5 * (2 * D) * (2 * D) + 6 * D * D + 8 * (2 * D) + 9 * D + 2 := by gcongr
    _ = _ := by ring

private theorem identity_total_cost (r : ℕ) :
    StoredRectangularGivens.total (StoredRectangularGivens.identity r).cost =
      5 * r ^ 2 + 4 * r := by
  simp [StoredRectangularGivens.total, StoredRectangularGivens.identity_cost,
    StoredRectangularGivens.identityBudget, tick]
  ring

/-- The actual stored producer uses linear-in-length, cubic-in-bond work in
the declared exact-real model, including absorption, storage, and node costs. -/
theorem canonicalize_total_cost_le {n l r : ℕ} (C : StoredChain n l r) (D : ℕ)
    (bound : maxBond (denoteChain C) ≤ D) :
    StoredRectangularGivens.total (canonicalize C).cost ≤
      n * (176 * D ^ 3 + 116 * D ^ 2 + 29 * D + 8) + 5 * D ^ 2 + 4 * D + 6 := by
  induction C with
  | nil r =>
      have hr : r ≤ D := bound
      simp only [canonicalize, total_add, identity_total_cost, Nat.zero_mul, zero_add]
      have node : StoredRectangularGivens.total nodeBudget = 6 := by
        simp [nodeBudget, StoredRectangularGivens.total, tick]
      rw [node]
      have square := Nat.pow_le_pow_left hr 2
      omega
  | @cons n l m r A C ih =>
      have hl : l ≤ D := (max_le_iff.mp bound).1
      have ht : maxBond (denoteChain C) ≤ D := (max_le_iff.mp bound).2
      have hm : m ≤ D := by
        cases C with
        | nil r => exact ht
        | cons B C => exact (max_le_iff.mp ht).1
      have hr : (canonicalize C).value.rank ≤ D := (canonicalize C).value.rank_le.trans hm
      have tail := ih ht
      have absorbed := absorption_total_cost_le A (canonicalize C).value.residual
      have absorbBound : 12 * l * m * (canonicalize C).value.rank +
          8 * l * (canonicalize C).value.rank + 4 * l ≤
          12 * D ^ 3 + 8 * D ^ 2 + 4 * D := by
        calc
          _ ≤ 12 * D * D * D + 8 * D * D + 4 * D := by gcongr
          _ = _ := by ring
      have head := factorCore_total_cost_le (absorption A (canonicalize C).value.residual).value D hl hr
      simp only [canonicalize, total_add]
      have node : StoredRectangularGivens.total nodeBudget = 6 := by
        simp [nodeBudget, StoredRectangularGivens.total, tick]
      rw [node]
      nlinarith

/-- The output's semantic boundary is obtained from its stored residual. -/
noncomputable def boundary {n l r : ℕ} (C : StoredChain n l r) (v : Fin l → ℝ) :
    Fin (canonicalize C).value.rank → ℝ := _root_.Matrix.vecMul v (denote (canonicalize C).value.residual)

theorem boundary_mass {n l r : ℕ} (C : StoredChain n l r) (v : Fin l → ℝ) :
    chainMass (denoteChain C) v = mass (boundary C v) :=
  residual_mass (denoteChain C) (denoteChain (canonicalize C).value.canonical)
    (denote (canonicalize C).value.residual) (canonicalize C).value.rightCanonical
    (canonicalize C).value.action v

theorem boundary_normalized {n l r : ℕ} (C : StoredChain n l r) (v : Fin l → ℝ)
    (normalized : chainMass (denoteChain C) v = 1) : mass (boundary C v) = 1 :=
  (boundary_mass C v).symm.trans normalized

/-- Forget storage, retaining the actual concrete canonicalization data. -/
def Result.toSemantic {n l r : ℕ} {C : StoredChain n l r} (result : Result C) :
    ConstructiveTensorTrain.Result (denoteChain C) where
  rank := result.rank
  residual := denote result.residual
  canonical := denoteChain result.canonical
  rightCanonical := result.rightCanonical
  rankReduced := result.rankReduced
  action := result.action

theorem factorCore_R {l r : ℕ} (A : StoredCore l r) :
    denote (factorCore A).value.R = (ConstructiveTensorTrain.factorCore (denoteCore A)).R := by
  change denote (StoredThinLQ.compile A).value.R =
    (ConstructiveThinLQ.factor (fun a j => denoteCore A a (finProdFinEquiv.symm j))).R
  have flatten : (fun a j => denoteCore A a (finProdFinEquiv.symm j)) = denote A := by
    funext a j
    exact congrArg (denote A a)
      ((finProdFinEquiv : Fin 2 × Fin r ≃ Fin (2 * r)).apply_symm_apply j)
  rw [flatten]
  exact StoredThinLQ.compile_R A

theorem factorCore_Q {l r : ℕ} (A : StoredCore l r) :
    denoteCore (factorCore A).value.Q = (ConstructiveTensorTrain.factorCore (denoteCore A)).Q := by
  ext a out
  change denote (StoredThinLQ.compile A).value.Q a (finProdFinEquiv out) =
    (ConstructiveThinLQ.factor (fun a j => denoteCore A a (finProdFinEquiv.symm j))).Q a
      (finProdFinEquiv out)
  have flatten : (fun a j => denoteCore A a (finProdFinEquiv.symm j)) = denote A := by
    funext a j
    exact congrArg (denote A a)
      ((finProdFinEquiv : Fin 2 × Fin r ≃ Fin (2 * r)).apply_symm_apply j)
  rw [flatten]
  rw [StoredThinLQ.compile_Q]

private noncomputable def semanticStep {n l m r : ℕ} {C : Chain n m r}
    (A : Core l m) (tailResult : ConstructiveTensorTrain.Result C) :
    ConstructiveTensorTrain.Result (.cons A C) :=
  let headResult := ConstructiveTensorTrain.factorCore (absorb A tailResult.residual)
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

/-- Exact data refinement, not just another witness of the same contract. -/
theorem canonicalize_refines {n l r : ℕ} (C : StoredChain n l r) :
    (canonicalize C).value.toSemantic = ConstructiveTensorTrain.canonicalize (denoteChain C) := by
  induction C with
  | nil r =>
      simp only [canonicalize, Result.toSemantic, denoteChain,
        ConstructiveTensorTrain.canonicalize, StoredRectangularGivens.identity_value]
  | @cons n l m r A C ih =>
      change _ = semanticStep (denoteCore A) (ConstructiveTensorTrain.canonicalize (denoteChain C))
      rw [← ih]
      have hR := (factorCore_R (absorption A (canonicalize C).value.residual).value).trans
        (congrArg (fun B : Core l (canonicalize C).value.rank =>
          (ConstructiveTensorTrain.factorCore B).R)
          (absorption_value A (canonicalize C).value.residual))
      have hQ := (factorCore_Q (absorption A (canonicalize C).value.residual).value).trans
        (congrArg (fun B : Core l (canonicalize C).value.rank =>
          (ConstructiveTensorTrain.factorCore B).Q)
          (absorption_value A (canonicalize C).value.residual))
      simp only [canonicalize, semanticStep, Result.toSemantic, denoteChain,
        hR, hQ]

end QuantumBlockEncoding.StoredTensorTrain
