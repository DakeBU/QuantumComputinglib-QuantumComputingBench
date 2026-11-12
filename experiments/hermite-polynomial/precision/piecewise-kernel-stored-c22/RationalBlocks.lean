import AssemblyConsumerChecks

namespace HermitePiecewiseStored
open scoped BigOperators
open QuantumBlockEncoding TensorTrainCanonical HermitePiecewiseAssembly HermitePiecewiseUniform
open HermitePiecewiseKernelProducer HermiteFiniteExp HermiteFiniteExpDegree

structure BlockQ (α : Type) where
  kernel : ℕ → Fin 2 → α → α → ℚ
  left : α → ℚ
  right : α → ℚ

private theorem block_ext {α : Type} {b c : Block α}
    (hk : b.kernel=c.kernel) (hl : b.left=c.left) (hr : b.right=c.right) : b=c := by
  cases b; cases c
  cases hk; cases hl; cases hr
  rfl

noncomputable def BlockQ.cast {α : Type} (b : BlockQ α) : Block α :=
  ⟨fun q bit a c => (b.kernel q bit a c : ℝ), fun a => (b.left a : ℝ),
    fun a => (b.right a : ℝ)⟩

def BlockQ.prod {α β : Type} (b : BlockQ α) (c : BlockQ β) : BlockQ (α × β) :=
  ⟨fun q bit a d => b.kernel q bit a.1 d.1*c.kernel q bit a.2 d.2,
    fun a => b.left a.1*c.left a.2, fun a => b.right a.1*c.right a.2⟩

def BlockQ.sum {α β : Type} (b : BlockQ α) (c : BlockQ β) : BlockQ (α ⊕ β) :=
  ⟨fun q bit a d => match a,d with
    | .inl a,.inl d => b.kernel q bit a d
    | .inr a,.inr d => c.kernel q bit a d
    | _,_ => 0,
    Sum.elim b.left c.left, Sum.elim b.right c.right⟩

theorem BlockQ.prod_cast {α β : Type} (b : BlockQ α) (c : BlockQ β) :
    (b.prod c).cast = b.cast.prod c.cast := by
  apply block_ext
  · funext q bit a d
    simp [BlockQ.prod, BlockQ.cast, Block.prod, productKernel]
  · funext a
    simp [BlockQ.prod, BlockQ.cast, Block.prod, productBoundary]
  · funext a
    simp [BlockQ.prod, BlockQ.cast, Block.prod, productBoundary]

theorem BlockQ.sum_cast {α β : Type} (b : BlockQ α) (c : BlockQ β) :
    (b.sum c).cast = b.cast.sum c.cast := by
  apply block_ext
  · funext q bit a d
    cases a <;> cases d <;> simp [BlockQ.sum, BlockQ.cast, Block.sum, sumKernel]
  · funext a
    cases a <;> rfl
  · funext a
    cases a <;> rfl

def acceptQ (width cut : ℕ) (a : Fin 3) : ℚ :=
  if cut=0 then 0 else if cut=2^width then 1 else if a=0 then 1 else 0

theorem acceptQ_cast (width cut : ℕ) (a : Fin 3) :
    (acceptQ width cut a : ℝ) = acceptBoundary width cut a := by
  unfold acceptQ acceptBoundary
  split_ifs <;> norm_num

def thresholdQ (n cut : ℕ) (flip : Bool) : BlockQ (Fin 3) :=
  ⟨comparisonEntry cut, fun a => if a=1 then 1 else 0,
    fun a => if flip then 1-acceptQ (n+1) cut a else acceptQ (n+1) cut a⟩

theorem thresholdQ_cast (n cut : ℕ) (flip : Bool) :
    (thresholdQ n cut flip).cast = thresholdBlock n cut flip := by
  apply block_ext
  · rfl
  · funext a
    simp only [thresholdQ, BlockQ.cast, thresholdBlock, equalBoundary]
    split_ifs <;> norm_num
  · funext a
    cases flip <;> simp [thresholdQ, BlockQ.cast, thresholdBlock, acceptQ_cast]

def strictQ (n : ℕ) (R s : ℚ) (flip : Bool) : BlockQ (Fin 3) :=
  thresholdQ n (strictCut (n+1) R s) flip
def inclusiveQ (n : ℕ) (R s : ℚ) (flip : Bool) : BlockQ (Fin 3) :=
  thresholdQ n (inclusiveCut (n+1) R s) flip

def polyQ (d : ℕ) (origin step : ℚ) (coeff : Fin (d+1) → ℚ) : BlockQ (Fin (d+1)) :=
  ⟨fun q bit a b => translationCoreQ d (step*2^q*(bit.val : ℚ)) a b,
    fun a => origin^a.val, coeff⟩

theorem polyQ_cast (d : ℕ) (origin step : ℚ) (coeff : Fin (d+1) → ℚ) :
    (polyQ d origin step coeff).cast = polyBlock d origin step coeff := by
  apply block_ext
  · rfl
  · funext a
    simp [polyQ, BlockQ.cast, polyBlock, HermiteTransferCores.rowFeatures]
  · rfl

def tailQ (n : ℕ) (R delta : ℚ) (negate : Bool) :
    BlockQ (Fin (sourceDegree delta+1)) :=
  polyQ (sourceDegree delta) (if negate then R else -R)
    (if negate then -gridStepQ (n+1) R else gridStepQ (n+1) R)
    (fun i => 1/(i.val.factorial : ℚ))

def middleQ (k n : ℕ) (R delta : ℚ) : BlockQ (Fin (2*k+1+1)) :=
  polyQ (2*k+1) (-R) (gridStepQ (n+1) R) (fun i => middleCoeffQ k delta i.val)

def constantQ (c : ℚ) : BlockQ (Fin 1) := polyQ 0 0 0 (fun _ => c)

def actualBlocksQ (k n : ℕ) (R delta : ℚ) : BlockQ (FullIndex k delta) :=
  let A := strictQ n R (-1) false
  let Ac := strictQ n R (-1) true
  let B := inclusiveQ n R 0 false
  let Bc := inclusiveQ n R 0 true
  let C := inclusiveQ n R (-(tailCutoff delta : ℚ)) false
  let Cc := inclusiveQ n R (-(tailCutoff delta : ℚ)) true
  let D := strictQ n R (tailCutoff delta : ℚ) true
  let Dc := strictQ n R (tailCutoff delta : ℚ) false
  let c := constantQ (clippedValue delta)
  let F := tailQ n R delta false
  let Fr := tailQ n R delta true
  let M := middleQ k n R delta
  (A.prod (C.prod c)).sum ((A.prod (Cc.prod F)).sum
    ((Ac.prod (B.prod M)).sum ((Bc.prod (D.prod c)).sum (Bc.prod (Dc.prod Fr)))))

theorem actualBlocksQ_cast (k n : ℕ) (R delta : ℚ) :
    (actualBlocksQ k n R delta).cast = actualBlocks k n R delta := by
  simp only [actualBlocksQ, actualBlocks, BlockQ.sum_cast, BlockQ.prod_cast,
    strictQ, inclusiveQ, strictBlock, inclusiveBlock, thresholdQ_cast,
    constantQ, constantBlock, tailQ, tailBlock, middleQ, middleBlock, polyQ_cast]

def actualEntryQ (k n : ℕ) (R delta : ℚ) (q : ℕ) (bit : Fin 2)
    (a b : Fin (assemblySize k delta)) : ℚ :=
  (actualBlocksQ k n R delta).kernel q bit ((fullEquiv k delta).symm a)
    ((fullEquiv k delta).symm b)

def actualLeftQ (k n : ℕ) (R delta : ℚ) (a : Fin (assemblySize k delta)) : ℚ :=
  (actualBlocksQ k n R delta).left ((fullEquiv k delta).symm a)
def actualRightQ (k n : ℕ) (R delta : ℚ) (a : Fin (assemblySize k delta)) : ℚ :=
  (actualBlocksQ k n R delta).right ((fullEquiv k delta).symm a)

theorem actualEntryQ_cast (k n : ℕ) (R delta : ℚ) (q : ℕ) (bit : Fin 2)
    (a b : Fin (assemblySize k delta)) :
    (actualEntryQ k n R delta q bit a b : ℝ) =
      reindexKernel (fullEquiv k delta) (actualBlocks k n R delta).kernel q bit a b := by
  have h := congrArg Block.kernel (actualBlocksQ_cast k n R delta)
  exact congrFun (congrFun (congrFun (congrFun h q) bit) ((fullEquiv k delta).symm a))
    ((fullEquiv k delta).symm b)

theorem actualLeftQ_cast (k n : ℕ) (R delta : ℚ) (a : Fin (assemblySize k delta)) :
    (actualLeftQ k n R delta a : ℝ) =
      (actualBlocks k n R delta).left ((fullEquiv k delta).symm a) :=
  congrFun (congrArg Block.left (actualBlocksQ_cast k n R delta)) _

theorem actualRightQ_cast (k n : ℕ) (R delta : ℚ) (a : Fin (assemblySize k delta)) :
    (actualRightQ k n R delta a : ℝ) =
      (actualBlocks k n R delta).right ((fullEquiv k delta).symm a) :=
  congrFun (congrArg Block.right (actualBlocksQ_cast k n R delta)) _

#print axioms actualBlocksQ_cast
#print axioms actualEntryQ_cast
#print axioms actualLeftQ_cast
#print axioms actualRightQ_cast
end HermitePiecewiseStored
