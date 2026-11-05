import CachedPrimitivesProof
import StoredProducer
import QuantumBlockEncoding.StoredBinaryCoordinates

/-!
C243 definitions-only materialization of the C237 operational proposal.
The eight counters are inherited scalar/word annotations. The two additional
counters name selected index quotient/remainder operations, not bit runtime.
Only carrier/index transport proofs occur here. No new value or cost theorem
is asserted. The numerical body never executes a semantic source kernel.
-/

namespace HermiteExplicitCachedStored

open QuantumBlockEncoding QuantumBlockEncoding.StoredGivens
open QuantumBlockEncoding.StoredTensorTrain
open QuantumBlockEncoding.StoredBinaryCoordinates
open HermitePiecewiseAssembly HermitePiecewiseStored
open HermiteFiniteExpDegree

def liftRun {α : Type} (x : Run α) : IndexedRun α := ⟨x, 0, 0⟩

/-- Bind already returned records; no callback is rerun to obtain metadata. -/
def indexedBind {α β : Type} (x : IndexedRun α)
    (f : α → IndexedRun β) : IndexedRun β :=
  let y := f x.run.value
  ⟨⟨y.run.value, x.run.cost + y.run.cost⟩,
    x.quotientCalls + y.quotientCalls,
    x.remainderCalls + y.remainderCalls⟩

/-- Same five-summand carrier, parameterized by already produced degrees. -/
abbrev FiveIndex (d m : ℕ) :=
  ComponentIndex 0 ⊕ (ComponentIndex d ⊕
    (ComponentIndex m ⊕ (ComponentIndex 0 ⊕ ComponentIndex d)))

def fiveSize (d m : ℕ) : ℕ :=
  componentSize 0 + (componentSize d +
    (componentSize m + (componentSize 0 + componentSize d)))

/-- One literal sum-bound test. Its caller reserves the four possible tests. -/
def splitIndex (m n : ℕ) (i : Fin (m+n)) : Fin m ⊕ Fin n :=
  if h : i.val < m then Sum.inl ⟨i.val, h⟩
  else Sum.inr ⟨i.val-m, by have hi := i.isLt; omega⟩

/-- Exactly two product decodes (two named quotients and remainders).
Fixed product arithmetic is index arithmetic, not a rational scalar callback. -/
def unpackComponent (r : ℕ) (i : Fin (componentSize r)) : ComponentIndex r :=
  let first : Fin 3 × Fin (3*(r+1)) := finProdFinEquiv.symm i
  let second : Fin 3 × Fin (r+1) := finProdFinEquiv.symm first.2
  (first.1, second)

/-- C243 API refinement: degrees, not delta, are numerical decoder inputs.
Four explicit sum tests are conservatively reserved even on shorter paths. -/
def decode (d m : ℕ) (i : Fin (fiveSize d m)) : IndexedRun (FiveIndex d m) :=
  let result : FiveIndex d m :=
    match splitIndex (componentSize 0)
        (componentSize d + (componentSize m + (componentSize 0 + componentSize d))) i with
    | .inl a => .inl (unpackComponent 0 a)
    | .inr rest =>
      match splitIndex (componentSize d)
          (componentSize m + (componentSize 0 + componentSize d)) rest with
      | .inl a => .inr (.inl (unpackComponent d a))
      | .inr rest =>
        match splitIndex (componentSize m) (componentSize 0 + componentSize d) rest with
        | .inl a => .inr (.inr (.inl (unpackComponent m a)))
        | .inr rest =>
          match splitIndex (componentSize 0) (componentSize d) rest with
          | .inl a => .inr (.inr (.inr (.inl (unpackComponent 0 a))))
          | .inr a => .inr (.inr (.inr (.inr (unpackComponent d a))))
  ⟨⟨result, 4 • tick .compare⟩, 2, 2⟩

/-- Rational-literal version of the original three-test comparison algorithm. -/
def comparisonQ (cut q : ℕ) (bit : Fin 2) (a b : Fin 3) : IndexedRun ℚ :=
  let digit := (cut / 2^q) % 2
  let low := charge .compare (decide (bit.val < digit))
  let high := charge .compare (decide (digit < bit.val))
  let next : Fin 3 := if low.value then 0 else if high.value then 2 else a
  let hit := charge .compare (decide (next = b))
  ⟨⟨if hit.value then 1 else 0, low.cost + high.cost + hit.cost⟩, 1, 1⟩

/-- Only the legal triangular branch reads actual factorials. All rational
powers are the existing charged multiplication recurrence. -/
def translationQ (L r q : ℕ) (F : Vector ℚ (L+1)) (hr : r ≤ L)
    (step : ℚ) (bit : Fin 2) (i j : Fin (r+1)) : Run ℚ :=
  let result : Run ℚ :=
    if h : i.val ≤ j.val then do
      let binomial ← HermiteChargedSourceCache.chooseFrom F j.val i.val h
        (by have hj := j.isLt; omega)
      let dyadic ← HermiteCachedPiecewiseStored.powQ 2 q
      let bitValue ← charge .compare (if bit = 1 then (1 : ℚ) else 0)
      let scaled ← HermiteChargedSourceCache.qMul step dyadic
      let w ← HermiteChargedSourceCache.qMul scaled bitValue
      let power ← HermiteCachedPiecewiseStored.powQ w (j.val-i.val)
      HermiteChargedSourceCache.qMul binomial power
    else pure 0
  ⟨result.value, tick .compare + result.cost⟩

def componentKernel (L r q : ℕ) (F : Vector ℚ (L+1)) (hr : r ≤ L)
    (cutA cutB : ℕ) (step : ℚ) (bit : Fin 2)
    (a b : ComponentIndex r) : IndexedRun ℚ :=
  indexedBind (comparisonQ cutA q bit a.1 b.1) fun first =>
  indexedBind (comparisonQ cutB q bit a.2.1 b.2.1) fun second =>
  indexedBind (liftRun (translationQ L r q F hr step bit a.2.2 b.2.2)) fun scalar =>
  liftRun (do
    let inner ← HermiteChargedSourceCache.qMul second scalar
    HermiteChargedSourceCache.qMul first inner)

/-- Literal five-way block diagonal dispatch. Masks are not flipped here.
Eight comparison ticks reserve the paired tag dispatch. -/
def kernelAt (d m L q : ℕ) (F : Vector ℚ (L+1)) (hd : d ≤ L) (hm : m ≤ L)
    (cutMinusOne cutZero cutMinusT cutT : ℕ) (step minusStep : ℚ)
    (bit : Fin 2) (a b : FiveIndex d m) : IndexedRun ℚ :=
  let result : IndexedRun ℚ := match a,b with
    | .inl a, .inl b =>
        componentKernel L 0 q F (Nat.zero_le L) cutMinusOne cutMinusT 0 bit a b
    | .inr (.inl a), .inr (.inl b) =>
        componentKernel L d q F hd cutMinusOne cutMinusT step bit a b
    | .inr (.inr (.inl a)), .inr (.inr (.inl b)) =>
        componentKernel L m q F hm cutMinusOne cutZero step bit a b
    | .inr (.inr (.inr (.inl a))), .inr (.inr (.inr (.inl b))) =>
        componentKernel L 0 q F (Nat.zero_le L) cutZero cutT 0 bit a b
    | .inr (.inr (.inr (.inr a))), .inr (.inr (.inr (.inr b))) =>
        componentKernel L d q F hd cutZero cutT minusStep bit a b
    | _,_ => liftRun (pure 0)
  ⟨⟨result.run.value, 8 • tick .compare + result.run.cost⟩,
    result.quotientCalls, result.remainderCalls⟩

def kernelEntry (d m n L : ℕ) (F : Vector ℚ (L+1)) (hd : d ≤ L) (hm : m ≤ L)
    (cutMinusOne cutZero cutMinusT cutT : ℕ) (step minusStep : ℚ)
    (q : Fin (n+1)) (a : Fin (fiveSize d m)) (j : Fin (2*fiveSize d m)) :
    IndexedRun ℚ :=
  let out : Fin 2 × Fin (fiveSize d m) := finProdFinEquiv.symm j
  let row := decode d m a
  let col := decode d m out.2
  let result := kernelAt d m L q.val F hd hm cutMinusOne cutZero cutMinusT cutT
    step minusStep out.1 row.run.value col.run.value
  ⟨⟨result.run.value, row.run.cost + col.run.cost + result.run.cost⟩,
    1 + row.quotientCalls + col.quotientCalls + result.quotientCalls,
    1 + row.remainderCalls + col.remainderCalls + result.remainderCalls⟩

def componentLeft (r : ℕ) (origin : ℚ) (a : ComponentIndex r) : Run ℚ := do
  let first ← charge .compare (if a.1 = 1 then (1 : ℚ) else 0)
  let second ← charge .compare (if a.2.1 = 1 then (1 : ℚ) else 0)
  let scalar ← HermiteCachedPiecewiseStored.powQ origin a.2.2.val
  let inner ← HermiteChargedSourceCache.qMul second scalar
  HermiteChargedSourceCache.qMul first inner

/-- Four tag-dispatch ticks; constant components retain exponent-zero powers. -/
def leftAt (d m : ℕ) (R minusR : ℚ) (a : FiveIndex d m) : Run ℚ :=
  let result : Run ℚ := match a with
    | .inl a => componentLeft 0 0 a
    | .inr (.inl a) => componentLeft d minusR a
    | .inr (.inr (.inl a)) => componentLeft m minusR a
    | .inr (.inr (.inr (.inl a))) => componentLeft 0 0 a
    | .inr (.inr (.inr (.inr a))) => componentLeft d R a
  ⟨result.value, 4 • tick .compare + result.cost⟩

def leftEntry (d m : ℕ) (R minusR : ℚ) (a : Fin (fiveSize d m)) : IndexedRun ℚ :=
  let index := decode d m a
  let result := leftAt d m R minusR index.run.value
  ⟨⟨result.value, index.run.cost + result.cost⟩,
    index.quotientCalls, index.remainderCalls⟩

/-- Actual original charged right entry, not its old semantic callback.
The degree equality is index transport only; the extra dispatch is charged. -/
def rightEntry (k n : ℕ) (R delta : ℚ) (d : ℕ) (hd : d = sourceDegree delta)
    (setup : HermiteCachedPiecewiseStored.RightSetup n R delta)
    (middle : Vector ℚ (2*k+2)) (a : Fin (fiveSize d (2*k+1))) : IndexedRun ℚ :=
  let index := decode d (2*k+1) a
  let original : FullIndex k delta := Eq.mp (congrArg (fun e => FiveIndex e (2*k+1)) hd) index.run.value
  let result := HermiteCachedPiecewiseStored.rightEntry k n R delta setup middle original
  ⟨⟨result.value, index.run.cost + 4 • tick .compare + result.cost⟩,
    index.quotientCalls, index.remainderCalls⟩

/-- All loops use d already obtained from the charged cutoff. The equality
argument is only an erased carrier transport for the original right interface. -/
def materializePrepared (k n : ℕ) (R delta : ℚ) (d : ℕ)
    (hd : d = sourceDegree delta) (L : ℕ) (ht : d ≤ L) (hm : 2*k+1 ≤ L)
    (setup : HermiteCachedPiecewiseStored.RightSetup n R delta)
    (middle : Vector ℚ (2*k+2)) (F : Vector ℚ (L+1))
    (step minusR minusStep : ℚ) : IndexedRun (RationalData n (fiveSize d (2*k+1))) :=
  let tables := collectIndexed fun q : Fin (n+1) =>
    collectIndexed fun a : Fin (fiveSize d (2*k+1)) =>
      collectIndexed fun j : Fin (2*fiveSize d (2*k+1)) =>
        kernelEntry d (2*k+1) n L F ht hm setup.cutMinusOne setup.cutZero
          setup.cutMinusT setup.cutT step minusStep q a j
  let left := collectIndexed fun a : Fin (fiveSize d (2*k+1)) =>
    leftEntry d (2*k+1) R minusR a
  let right := collectIndexed fun a : Fin (fiveSize d (2*k+1)) =>
    rightEntry k n R delta d hd setup middle a
  ⟨⟨⟨tables.run.value, left.run.value, right.run.value⟩,
      tables.run.cost + left.run.cost + right.run.cost⟩,
    tables.quotientCalls + left.quotientCalls + right.quotientCalls,
    tables.remainderCalls + left.remainderCalls + right.remainderCalls⟩

/-- One actual cache/setup/middle prefix, then counted regeneration of the
discarded cutoff, step and factorial intermediates. No source object is captured. -/
def produceExplicitQData (k n : ℕ) (R delta : ℚ) :
    IndexedRun (RationalData n (assemblySize k delta)) :=
  let cache := HermiteChargedSourceCache.produceSourceCache k
  let setup := HermiteCachedPiecewiseStored.rightSetup n R delta
  let middle := HermiteCachedPiecewiseStored.middleFromCache k setup.value.midpoint cache.value
  let cutoff := HermiteCachedPiecewiseStored.cutoffQ delta
  let T := cutoff.value
  let d := HermiteFiniteExpDegree.degree T T
  have hd : d = sourceDegree delta := by rfl
  let L := d+2*k+1
  have ht : d ≤ L := by omega
  have hm : 2*k+1 ≤ L := by omega
  have hsize : fiveSize d (2*k+1) = assemblySize k delta := by rw [hd]; rfl
  let result :=
    indexedBind (liftRun (HermiteCachedPiecewiseStored.gridStepRun (n+1) R)) fun step =>
    indexedBind (liftRun (HermiteCachedPiecewiseStored.qSub 0 R)) fun minusR =>
    indexedBind (liftRun (HermiteCachedPiecewiseStored.qSub 0 step)) fun minusStep =>
    indexedBind (liftRun (HermiteChargedSourceCache.factorials L)) fun F =>
      materializePrepared k n R delta d hd L ht hm setup.value middle.value F.values
        step minusR minusStep
  let data : RationalData n (assemblySize k delta) := hsize ▸ result.run.value
  ⟨⟨data, cache.cost + setup.cost + middle.cost + cutoff.cost + result.run.cost⟩,
    result.quotientCalls, result.remainderCalls⟩

noncomputable def produceExplicitData (k n : ℕ) (R delta : ℚ) :
    IndexedRun (RealData n (assemblySize k delta)) :=
  indexedBind (produceExplicitQData k n R delta) fun data =>
    liftRun (HermitePiecewiseStored.castData data)

noncomputable def produceExplicitStored (k n : ℕ) (R delta : ℚ) :
    IndexedRun (StoredChain (n+1) 1 1) :=
  indexedBind (produceExplicitData k n R delta) fun data =>
    liftRun (StoredMatrixProductChain.ofTable data.tables data.left data.right)

/-- Specification-side candidate bound only; it is not evaluated by producers. -/
def frontierBudget (k n : ℕ) (delta : ℚ) : ℕ :=
  let T := HermiteFiniteExp.tailCutoff delta
  let d := sourceDegree delta
  let L := d+2*k+1
  let D := assemblySize k delta
  let P := (n+1)*(2*D^2+D+1)+2*D
  816*(k+1)^2 + 81*(d+1)^2 + 8*(d+1) + 80*(L+1)^2 +
    2*(n+1)*D^2*(n+L+34) + D*(L+61) + 9*P + 20*D^2 +
    5*n^2 + 9*n + T + 59

end HermiteExplicitCachedStored
