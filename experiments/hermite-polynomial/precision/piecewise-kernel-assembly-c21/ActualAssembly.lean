import IndexedKernel
import ActualCoefficients

namespace HermitePiecewiseAssembly
open scoped BigOperators Matrix
open QuantumBlockEncoding TensorTrainCanonical Matrix HermitePiecewiseUniform
open HermitePiecewiseKernelProducer HermitePiecewiseSourceBudget HermiteFiniteExp
open HermiteFiniteExpDegree HermiteFiniteMiddleSource

structure Block (α : Type) where
  kernel : IKernel α
  left : α → ℝ
  right : α → ℝ

noncomputable def Block.value {α : Type} [Fintype α] (b : Block α)
    {n : ℕ} (x : Word n) : ℝ := amplitude b.kernel b.left b.right 0 x

noncomputable def Block.prod {α β : Type} (b : Block α) (c : Block β) : Block (α × β) :=
  ⟨productKernel b.kernel c.kernel, productBoundary b.left c.left,
    productBoundary b.right c.right⟩

noncomputable def Block.sum {α β : Type} (b : Block α) (c : Block β) : Block (α ⊕ β) :=
  ⟨sumKernel b.kernel c.kernel, sumBoundary b.left c.left, sumBoundary b.right c.right⟩

theorem Block.prod_value {α β : Type} [Fintype α] [Fintype β]
    (b : Block α) (c : Block β) (n : ℕ) (x : Word n) :
    (b.prod c).value x = b.value x*c.value x := product_amplitude _ _ _ _ _ _ n 0 x

theorem Block.sum_value {α β : Type} [Fintype α] [Fintype β]
    (b : Block α) (c : Block β) (n : ℕ) (x : Word n) :
    (b.sum c).value x = b.value x+c.value x := sum_amplitude _ _ _ _ _ _ n 0 x

noncomputable def thresholdBlock (n cut : ℕ) (flip : Bool) : Block (Fin 3) :=
  ⟨comparisonKernel cut, equalBoundary,
    if flip then (fun a => 1-acceptBoundary (n+1) cut a) else acceptBoundary (n+1) cut⟩

private theorem comparison_amplitude_right (cut n : ℕ) (right : Fin 3 → ℝ)
    (x : Word (n+1)) :
    amplitude (comparisonKernel cut) equalBoundary right 0 x = right (scan cut x 1) := by
  rw [canonical_amplitude _ _ _ n, MatrixProductChain.ofKernel_contract]
  rw [Finset.sum_eq_single 1]
  · simp only [equalBoundary, readout_scan, pow_zero, Nat.div_one]
    simp
  · intro b _ hb
    simp [equalBoundary, hb]
  · simp

theorem thresholdBlock_value (n cut : ℕ) (hc : cut ≤ 2^(n+1))
    (flip : Bool) (x : Word (n+1)) :
    (thresholdBlock n cut flip).value x =
      if flip then 1-(if wordValue x < cut then 1 else 0) else
        (if wordValue x < cut then 1 else 0) := by
  have h := comparison_mask_contract n cut hc x
  rw [← canonical_amplitude _ _ _ n, comparison_amplitude_right] at h
  cases flip <;> simp only [thresholdBlock, Block.value, Bool.false_eq_true,
    if_false, if_true, comparison_amplitude_right, h]

def gridPoint (n : ℕ) (R : ℚ) (x : Word (n+1)) : ℚ :=
  -R+2*R*(wordValue x : ℚ)/(2:ℚ)^(n+1)

def wordIndex (n : ℕ) (x : Word (n+1)) : Fin (gridSize (n+1)) :=
  ⟨wordValue x, wordValue_lt _ x⟩

theorem rationalGrid_wordIndex (n : ℕ) (R : ℚ) (x : Word (n+1)) :
    rationalGrid n R (wordIndex n x) = gridPoint n R x := by
  simp [rationalGrid, wordIndex, gridPoint, gridSize]

noncomputable def strictBlock (n : ℕ) (R s : ℚ) (flip : Bool) : Block (Fin 3) :=
  thresholdBlock n (strictCut (n+1) R s) flip
noncomputable def inclusiveBlock (n : ℕ) (R s : ℚ) (flip : Bool) : Block (Fin 3) :=
  thresholdBlock n (inclusiveCut (n+1) R s) flip

theorem strictBlock_value (n : ℕ) (R s : ℚ) (hR : 0 < R) (flip : Bool)
    (x : Word (n+1)) :
    (strictBlock n R s flip).value x =
      if flip then 1-(indicator (gridPoint n R x < s) : ℝ)
      else (indicator (gridPoint n R x < s) : ℝ) := by
  rw [strictBlock, thresholdBlock_value n (strictCut (n+1) R s)
    (by unfold strictCut; exact min_le_left _ _) flip x]
  simp only [strictCut_correct _ _ _ hR _ (wordValue_lt _ x)]
  change (if flip then 1-(if gridPoint n R x < s then 1 else 0) else
    (if gridPoint n R x < s then 1 else 0)) = _
  cases flip <;> by_cases h : gridPoint n R x < s <;>
    simp [indicator, h]

theorem inclusiveBlock_value (n : ℕ) (R s : ℚ) (hR : 0 < R) (flip : Bool)
    (x : Word (n+1)) :
    (inclusiveBlock n R s flip).value x =
      if flip then 1-(indicator (gridPoint n R x ≤ s) : ℝ)
      else (indicator (gridPoint n R x ≤ s) : ℝ) := by
  rw [inclusiveBlock, thresholdBlock_value n (inclusiveCut (n+1) R s)
    (by unfold inclusiveCut; exact min_le_left _ _) flip x]
  simp only [inclusiveCut_correct _ _ _ hR _ (wordValue_lt _ x)]
  change (if flip then 1-(if gridPoint n R x ≤ s then 1 else 0) else
    (if gridPoint n R x ≤ s then 1 else 0)) = _
  cases flip <;> by_cases h : gridPoint n R x ≤ s <;>
    simp [indicator, h]

noncomputable def polyBlock (d : ℕ) (origin step : ℚ)
    (coeff : Fin (d+1) → ℚ) : Block (Fin (d+1)) :=
  ⟨polynomialKernel d step, HermiteTransferCores.rowFeatures d (origin : ℝ),
    fun i => (coeff i : ℝ)⟩

theorem polyBlock_value (d n : ℕ) (origin step : ℚ) (coeff : Fin (d+1) → ℚ)
    (x : Word (n+1)) :
    (polyBlock d origin step coeff).value x =
      (∑ i : Fin (d+1), coeff i*(origin+step*(wordValue x : ℚ))^i.val : ℚ) := by
  exact (canonical_amplitude _ _ _ n 0 x).trans
    (polynomial_mask_free_contract d n origin step coeff x)

noncomputable def tailBlock (n : ℕ) (R delta : ℚ) (negate : Bool) :
    Block (Fin (sourceDegree delta+1)) :=
  polyBlock (sourceDegree delta) (if negate then R else -R)
    (if negate then -gridStepQ (n+1) R else gridStepQ (n+1) R)
    (fun i => 1/(i.val.factorial : ℚ))

theorem tailBlock_value (n : ℕ) (R delta : ℚ) (negate : Bool) (x : Word (n+1)) :
    (tailBlock n R delta negate).value x =
      (activeValue delta (if negate then -gridPoint n R x else gridPoint n R x) : ℝ) := by
  rw [tailBlock, polyBlock_value]
  have hp : ∀ b : Bool, (if b then R else -R)+
      (if b then -gridStepQ (n+1) R else gridStepQ (n+1) R)*(wordValue x : ℚ) =
      if b then -gridPoint n R x else gridPoint n R x := by
    intro b
    cases b <;> simp [gridStepQ, gridPoint] <;> ring
  rw [hp]
  unfold activeValue poly
  congr 1
  simp only [one_div_mul_eq_div]
  exact Fin.sum_univ_eq_sum_range
    (fun i : ℕ => (if negate then -gridPoint n R x else gridPoint n R x)^i/(i.factorial : ℚ))
    (sourceDegree delta+1)

noncomputable def middleBlock (k n : ℕ) (R delta : ℚ) : Block (Fin (2*k+1+1)) :=
  polyBlock (2*k+1) (-R) (gridStepQ (n+1) R) (fun i => middleCoeffQ k delta i.val)

theorem middleBlock_value (k n : ℕ) (R delta : ℚ) (x : Word (n+1)) :
    (middleBlock k n R delta).value x = (middleValueQ k delta (gridPoint n R x) : ℝ) := by
  rw [middleBlock, polyBlock_value]
  have hp : -R+gridStepQ (n+1) R*(wordValue x : ℚ) = gridPoint n R x := by
    unfold gridStepQ gridPoint
    ring
  rw [hp, middleCoeffQ_eval]

noncomputable def constantBlock (c : ℚ) : Block (Fin 1) :=
  polyBlock 0 0 0 (fun _ => c)

theorem constantBlock_value (n : ℕ) (c : ℚ) (x : Word (n+1)) :
    (constantBlock c).value x = (c : ℝ) := by
  rw [constantBlock, polyBlock_value]
  simp

abbrev ComponentIndex (d : ℕ) := Fin 3 × (Fin 3 × Fin (d+1))
abbrev FullIndex (k : ℕ) (delta : ℚ) :=
  ComponentIndex 0 ⊕ (ComponentIndex (sourceDegree delta) ⊕
    (ComponentIndex (2*k+1) ⊕ (ComponentIndex 0 ⊕ ComponentIndex (sourceDegree delta))))

noncomputable def actualBlocks (k n : ℕ) (R delta : ℚ) : Block (FullIndex k delta) :=
  let A := strictBlock n R (-1) false
  let Ac := strictBlock n R (-1) true
  let B := inclusiveBlock n R 0 false
  let Bc := inclusiveBlock n R 0 true
  let C := inclusiveBlock n R (-(tailCutoff delta : ℚ)) false
  let Cc := inclusiveBlock n R (-(tailCutoff delta : ℚ)) true
  let D := strictBlock n R (tailCutoff delta : ℚ) true
  let Dc := strictBlock n R (tailCutoff delta : ℚ) false
  let c := constantBlock (clippedValue delta)
  let F := tailBlock n R delta false
  let Fr := tailBlock n R delta true
  let M := middleBlock k n R delta
  (A.prod (C.prod c)).sum ((A.prod (Cc.prod F)).sum
    ((Ac.prod (B.prod M)).sum ((Bc.prod (D.prod c)).sum (Bc.prod (Dc.prod Fr)))))

theorem actualBlocks_value (k n : ℕ) (R delta : ℚ) (hR : 0 < R)
    (x : Word (n+1)) :
    (actualBlocks k n R delta).value x = (fiveValue k delta (gridPoint n R x) : ℝ) := by
  simp only [actualBlocks, Block.sum_value, Block.prod_value,
    strictBlock_value _ _ _ hR, inclusiveBlock_value _ _ _ hR,
    tailBlock_value, middleBlock_value, constantBlock_value,
    Bool.false_eq_true, if_false, if_true]
  have hd : (indicator (gridPoint n R x < (tailCutoff delta : ℚ)) : ℝ) =
      1-(indicator ((tailCutoff delta : ℚ) ≤ gridPoint n R x) : ℝ) := by
    by_cases h : gridPoint n R x < (tailCutoff delta : ℚ)
    · simp [indicator, h, not_le.mpr h]
    · simp [indicator, h, le_of_not_gt h]
  rw [hd]
  simp only [fiveValue, Rat.cast_add, Rat.cast_mul, Rat.cast_sub, Rat.cast_one]
  ring

def componentSize (d : ℕ) : ℕ := 3*(3*(d+1))
def assemblySize (k : ℕ) (delta : ℚ) : ℕ :=
  componentSize 0+(componentSize (sourceDegree delta)+
    (componentSize (2*k+1)+(componentSize 0+componentSize (sourceDegree delta))))

def componentEquiv (d : ℕ) : ComponentIndex d ≃ Fin (componentSize d) :=
  (Equiv.prodCongr (Equiv.refl _) finProdFinEquiv).trans finProdFinEquiv

def fullEquiv (k : ℕ) (delta : ℚ) : FullIndex k delta ≃ Fin (assemblySize k delta) :=
  (Equiv.sumCongr (componentEquiv 0)
    ((Equiv.sumCongr (componentEquiv (sourceDegree delta))
      ((Equiv.sumCongr (componentEquiv (2*k+1))
        ((Equiv.sumCongr (componentEquiv 0) (componentEquiv (sourceDegree delta))).trans
          finSumFinEquiv)).trans finSumFinEquiv)).trans finSumFinEquiv)).trans finSumFinEquiv

theorem assemblySize_eq (k : ℕ) (delta : ℚ) :
    assemblySize k delta = 18*(sourceDegree delta+1)+9*(2*k+1+1)+18 := by
  unfold assemblySize componentSize
  omega

noncomputable def actualChain (k n : ℕ) (R delta : ℚ) : Chain (n+1) 1 1 :=
  let b := actualBlocks k n R delta
  let e := fullEquiv k delta
  MatrixProductChain.ofKernel (reindexKernel e b.kernel) (b.left ∘ e.symm)
    (b.right ∘ e.symm) 0 n

theorem actualChain_contract (k n : ℕ) (R delta : ℚ) (hR : 0 < R)
    (x : Word (n+1)) :
    contract (actualChain k n R delta) x 0 0 =
      (piecewiseValue k delta (rationalGrid n R (wordIndex n x)) : ℝ) := by
  rw [actualChain, reindex_contract]
  change (actualBlocks k n R delta).value x = _
  rw [actualBlocks_value k n R delta hR, rationalGrid_wordIndex, five_components]

theorem actualChain_maxBond (k n : ℕ) (R delta : ℚ) :
    maxBond (actualChain k n R delta) ≤
      18*(sourceDegree delta+1)+9*(2*k+1+1)+18 := by
  have h := MatrixProductChain.ofKernel_maxBond
    (reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel)
    ((actualBlocks k n R delta).left ∘ (fullEquiv k delta).symm)
    ((actualBlocks k n R delta).right ∘ (fullEquiv k delta).symm) 0 n
  change maxBond (actualChain k n R delta) ≤ _ at h
  rw [assemblySize_eq, max_eq_left (by omega)] at h
  exact h

theorem allocated_actualChain_contract (k n : ℕ) (L epsilon : ℚ)
    (hL : 0 < L) (he : 0 < epsilon) (x : Word (n+1)) :
    contract (actualChain k n (ExperimentalGlobalRadiusBudget.allocatedRadius k n L epsilon)
      (sourceDelta k n epsilon)) x 0 0 =
    (piecewiseValue k (sourceDelta k n epsilon)
      (rationalGrid n (ExperimentalGlobalRadiusBudget.allocatedRadius k n L epsilon)
        (wordIndex n x)) : ℝ) :=
  actualChain_contract _ _ _ _ (ExperimentalGlobalRadiusBudget.allocatedRadius_positive _ _ _ _ hL he) x

#print axioms rationalGrid_wordIndex
#print axioms actualBlocks_value
#print axioms actualChain_contract
#print axioms actualChain_maxBond
#print axioms allocated_actualChain_contract
end HermitePiecewiseAssembly
