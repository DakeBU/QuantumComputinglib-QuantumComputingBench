# Deterministic right-canonicalization of a finite real tensor train

The specified tail-first procedure returns a residual matrix and a
right-canonical chain that preserve every word amplitude and every terminal
bond label. Its bond sizes never exceed the original maximum bond. Moving an
initial row boundary through the returned residual transfers the complete
chain mass to that new boundary. Normalization is a conditional consequence,
not an output supplied for an arbitrary input.

This is a retrospective local mathematical contract for
`QuantumBlockEncoding/ConstructiveTensorTrain.lean`. It describes existing
definitions and proofs, not a historical pre-proof Statement Seal, an
external-paper reconstruction, or a claim of original mathematical novelty.
Independent decoding, source-first comparison, and integrated reader gates
remain pending. The packet author is not identified as the historical
formalizer. No new Lean execution is claimed here.

## Carriers, word order, and the terminal bond

Fix natural bond dimensions $d_0,\ldots,d_n$, allowing zero. At site $i$,
the real core has entries
$A_i(a,b,j)$ with $a\in\operatorname{Fin}d_i$,
$b\in\operatorname{Fin}2$, and $j\in\operatorname{Fin}d_{i+1}$.
Thus a core is a matrix whose row is the left bond and whose column is the
pair (emitted bit, right bond). Let $A_i(b)$ be its fixed-bit slice.
The empty chain at terminal dimension $r$ has contraction $I_r$.
For $x=(x_0,\ldots,x_{n-1})$ in the recursively ordered carrier
$\mathrm{Word}(0)=\mathrm{Unit}$,
$\mathrm{Word}(n+1)=\operatorname{Fin}2\times\mathrm{Word}(n)$, put

$$
M_C(x)=A_0(x_0)\cdots A_{n-1}(x_{n-1}).
$$

The first core emits the first recursive word bit. The matrix $M_C(x)$ has
all initial rows and all terminal columns; none are projected away.
These are the definitions `Core`, `slice`, `Chain`, `Word`, and `contract`
in `TensorTrainCanonical`. No identification of this word with a physical
little-endian integer basis is supplied by this module.

For a real core $Q$ with $s$ left rows, right-canonical means

$$
\sum_{b=0}^1\sum_j Q(a,b,j)Q(c,b,j)=\delta_{ac},
\qquad QQ^{\mathsf T}=I_s.
$$

`RightCanonical` requires this equation at every site and is true for an
empty chain. The equation sums both bits and the entire right bond. It is
real transpose semantics, not a complex conjugate-transpose input contract.

## The specified deterministic core supplier

For a core $B$ with dimensions $l,r$, use the actual equivalence
`finProdFinEquiv` to flatten its column pair:

$$
e(b,j)=br+j,\qquad \widehat B(a,k)=B(a,e^{-1}(k)).
$$

This is bit-major indexing: the right-bond index varies fastest. At $r=0$
both column carriers are empty, so no division or inverse address needs to
be evaluated on an inhabitant. `factorCore` calls
`ConstructiveThinLQ.factor` on this flattened matrix and relabels its
returned $Q$ back by $e$. If $s=\min(l,2r)$, the returned data satisfy

$$
B=RQ,\qquad R\in\mathbb R^{l\times s},\qquad
Q\in\mathbb R^{s\times(2r)},\qquad QQ^{\mathsf T}=I_s.
$$

The supplier fixes actual factors; it does not select a witness of
`exists_core_lq`. For completeness, its shape branches are as follows.
For a matrix $H\in\mathbb R^{m\times q}$ with $m\le q$, deterministic
adjacent-row elimination of $H^{\mathsf T}$ returns
$Z=T H^{\mathsf T}$ with $T^{\mathsf T}T=I_q$ and $Z(k,a)=0$ for $k>a$.
The factors are $R(a,k)=Z(k,a)$ and $Q(k,j)=T(k,j)$ for $k<m$.
Transposing exact recovery gives $H=Z^{\mathsf T}T$; the vanishing rows
restrict that product to the prefix $k<m$, while orthogonality of $T$
gives orthonormal rows of $Q$. For $m>q$, the actual branch returns
$R=H$ and $Q=I_q$. Equality is handled by the first branch.
The providers are `wide_factorization`, `wide_orthogonal`, and `factor`.

Elimination visits columns in increasing order and each eligible column
uses a bottom-up adjacent-row sweep. Its pair angle is the negative of
`RealAmplitudePreparation.splitAngle` evaluated exactly; a zero pair has
angle zero. Therefore deficient rows and signed entries do not require a
full-rank premise. The output dimension is $\min(m,q)$, not numerical rank.
For example, even a zero $2\times2$ matrix retains two orthonormal rows in
$Q$ and carries its vanishing action through $R$.
The bijection $e$ preserves finite sums, so relabeling preserves both
factorization and the row inner products. `CoreFactorization` records
these equations as produced fields, not as hypotheses for canonicalization.

<!-- lean-disclosures: CoreFactorization factorCore -->
<!-- begin generated Lean disclosures -->
<details>
<summary>Exact Lean statement: CoreFactorization</summary>

```lean
structure CoreFactorization {l r : ℕ} (A : Core l r) where
  R : _root_.Matrix (Fin l) (Fin (min l (2 * r))) ℝ
  Q : Core (min l (2 * r)) r
  factorization : A = R * Q
  orthogonal : Q * Q.transpose = 1
```

</details>

<details>
<summary>Exact Lean statement: factorCore</summary>

```lean
noncomputable def factorCore {l r : ℕ} (A : Core l r) : CoreFactorization A
```

</details>

<details>
<summary>Exact Lean definition or proof: factorCore</summary>

```lean
:= by
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
```

</details>
<!-- end generated Lean disclosures -->


## Tail-first recursion and exact all-word action

For a chain $C$ from initial bond $l$ to terminal bond $r$, `Result C`
contains a natural dimension $s$, a residual $R:l\times s$, a chain $D$
of the same length and terminal dimension $r$, and proofs of
right-canonicality, the dimension recurrence, and
$M_C(x)=R M_D(x)$ for every word $x$.

For the empty chain, `canonicalize` returns $s=r$, $R=I_r$, and the same
empty chain. For a nonempty chain $A::C$, first recursively obtain the
tail residual $S:m\times t$ and tail chain $E$. Define absorption without
mixing the emitted bit:

$$
B(a,b,j)=\sum_{u\in\operatorname{Fin}m} A(a,b,u)S(u,j).
$$

Apply the specified `factorCore` to this actual $B$, obtaining $B=RQ$.
Return $R$ and $Q::E$. Consequently the dimensions satisfy

$$
s_n=d_n,\qquad s_i=\min(d_i,2s_{i+1}).
$$

`RankReduced` encodes precisely this relation on the two actual chains.
It does not claim smallest possible bond, singular-value truncation,
numerical-rank detection, or a unique representation among all equivalent
tensor trains. Deterministic here means fixed by the specified producer,
not invariance under changing its input gauge or choosing another algorithm.

To prove the action, write a word as $(b,y)$. The tail induction hypothesis,
`absorb_slice`, core factorization, and associativity give

$$
\begin{aligned}
M_{A::C}(b,y)
 &=A(b)M_C(y)\\
 &=A(b)S M_E(y)\\
 &=B(b)M_E(y)\\
 &=R Q(b)M_E(y)\\
 &=R M_{Q::E}(b,y).
\end{aligned}
$$

The empty case uses $I_r=I_r I_r$. This proves the equation for every
initial and terminal entry, not just a scalar projection or a norm.
Each new core is row-orthonormal by its supplier and the tail already is
right-canonical. Since $s_i\le d_i$ and the terminal bond is unchanged,
the maximum bond, including both boundaries, cannot increase.
The public projection theorems expose these fields of this same returned
result; `canonicalize_maxBond_le` uses `RankReduced.maxBond_le`.

<!-- lean-disclosures: Result canonicalize canonicalize_rightCanonical canonicalize_rankReduced canonicalize_action canonicalize_maxBond_le -->
<!-- begin generated Lean disclosures -->
<details>
<summary>Exact Lean statement: Result</summary>

```lean
structure Result {n l r : ℕ} (C : Chain n l r) where
  rank : ℕ
  residual : _root_.Matrix (Fin l) (Fin rank) ℝ
  canonical : Chain n rank r
  rightCanonical : RightCanonical canonical
  rankReduced : RankReduced C canonical
  action : ∀ x, contract C x = residual * contract canonical x
```

</details>

<details>
<summary>Exact Lean statement: canonicalize</summary>

```lean
noncomputable def canonicalize : {n l r : ℕ} → (C : Chain n l r) → Result C
```

</details>

<details>
<summary>Exact Lean definition or proof: canonicalize</summary>

```lean
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
```

</details>

<details>
<summary>Exact Lean statement: canonicalize_rightCanonical</summary>

```lean
theorem canonicalize_rightCanonical {n l r : ℕ} (C : Chain n l r) :
    RightCanonical (canonicalize C).canonical
```

</details>

<details>
<summary>Exact Lean definition or proof: canonicalize_rightCanonical</summary>

```lean
:= (canonicalize C).rightCanonical
```

</details>

<details>
<summary>Exact Lean statement: canonicalize_rankReduced</summary>

```lean
theorem canonicalize_rankReduced {n l r : ℕ} (C : Chain n l r) :
    RankReduced C (canonicalize C).canonical
```

</details>

<details>
<summary>Exact Lean definition or proof: canonicalize_rankReduced</summary>

```lean
:= (canonicalize C).rankReduced
```

</details>

<details>
<summary>Exact Lean statement: canonicalize_action</summary>

```lean
theorem canonicalize_action {n l r : ℕ} (C : Chain n l r) (x : Word n) :
    contract C x = (canonicalize C).residual * contract (canonicalize C).canonical x
```

</details>

<details>
<summary>Exact Lean definition or proof: canonicalize_action</summary>

```lean
:=
  (canonicalize C).action x
```

</details>

<details>
<summary>Exact Lean statement: canonicalize_maxBond_le</summary>

```lean
theorem canonicalize_maxBond_le {n l r : ℕ} (C : Chain n l r) :
    maxBond (canonicalize C).canonical ≤ maxBond C
```

</details>

<details>
<summary>Exact Lean definition or proof: canonicalize_maxBond_le</summary>

```lean
:=
  (canonicalize C).rankReduced.maxBond_le
```

</details>
<!-- end generated Lean disclosures -->


## Full boundary action and mass

Fix a real row vector $v\in\mathbb R^l$ and let
$w=vR=\mathrm{boundary}(C,v)$. Let
$\mathrm{mass}(z)=\sum_j z_j^2$ and define the full chain mass by

$$
\mathrm{chainMass}(C,v)
 =\sum_{x\in\mathrm{Word}(n)}\sum_{j\in\operatorname{Fin}r}
       (vM_C(x))_j^2.
$$

The action theorem gives the row-vector identity

$$
vM_C(x)=wM_D(x)
$$

for every word and terminal label. For a row-orthonormal core, the squared
mass of the expanded row $zQ$ equals that of $z$, because
$zQQ^{\mathsf T}z^{\mathsf T}=zz^{\mathsf T}$.
Sum over the first emitted bit and apply this identity inductively to the
tail. At length zero the single empty word acts by $I_r$. This is the
provider theorem `chainMass_eq`. Applying it to the returned $D$ yields

$$
\mathrm{chainMass}(C,v)
 =\mathrm{chainMass}(D,w)=\mathrm{mass}(w).
$$

`boundary_mass` invokes `residual_mass` with the produced action and
right-canonicality proofs. No normalization or nonzero boundary is needed.
Only `boundary_normalized` assumes $\mathrm{chainMass}(C,v)=1$; under
that hypothesis it concludes $\mathrm{mass}(w)=1$. The producer does not
normalize, divide by a norm, or certify input agreement with another
scientific target. Every terminal label remains in the sum; this is neither
postselection nor terminal-garbage cleanup.

<!-- lean-disclosures: boundary boundary_action boundary_mass boundary_normalized -->
<!-- begin generated Lean disclosures -->
<details>
<summary>Exact Lean statement: boundary</summary>

```lean
noncomputable def boundary {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) :
    Fin (canonicalize C).rank → ℝ
```

</details>

<details>
<summary>Exact Lean definition or proof: boundary</summary>

```lean
:= _root_.Matrix.vecMul v (canonicalize C).residual
```

</details>

<details>
<summary>Exact Lean statement: boundary_action</summary>

```lean
theorem boundary_action {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) (x : Word n) :
    _root_.Matrix.vecMul v (contract C x) =
      _root_.Matrix.vecMul (boundary C v) (contract (canonicalize C).canonical x)
```

</details>

<details>
<summary>Exact Lean definition or proof: boundary_action</summary>

```lean
:= by
  rw [canonicalize_action, ← _root_.Matrix.vecMul_vecMul]
  rfl
```

</details>

<details>
<summary>Exact Lean statement: boundary_mass</summary>

```lean
theorem boundary_mass {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ) :
    chainMass C v = mass (boundary C v)
```

</details>

<details>
<summary>Exact Lean definition or proof: boundary_mass</summary>

```lean
:=
  residual_mass C (canonicalize C).canonical (canonicalize C).residual
    (canonicalize C).rightCanonical (canonicalize C).action v
```

</details>

<details>
<summary>Exact Lean statement: boundary_normalized</summary>

```lean
theorem boundary_normalized {n l r : ℕ} (C : Chain n l r) (v : Fin l → ℝ)
    (normalized : chainMass C v = 1) : mass (boundary C v) = 1
```

</details>

<details>
<summary>Exact Lean definition or proof: boundary_normalized</summary>

```lean
:=
  (boundary_mass C v).symm.trans normalized
```

</details>
<!-- end generated Lean disclosures -->


## Scalar-boundary specialization

For $C:\mathrm{Chain}(n,1,1)$, define
$u=\mathrm{stateBoundary}(C)=\mathrm{boundary}(C,(1))$.
The unique initial and terminal indices are both $0$. Expanding the matrix
product in the all-word action gives

$$
M_C(x)_{00}=\sum_{a\in\operatorname{Fin}s}u_a M_D(x)_{a0}.
$$

This equality is unconditional. If, separately,
$\sum_x M_C(x)_{00}^2=1$, then full chain mass with initial row $(1)$ is
one, and `boundary_normalized` gives $\sum_a u_a^2=1$.
These are `stateBoundary_action` and `stateBoundary_normalized`.
The singleton terminal carrier is mathematical data; identifying it with
a chosen clean physical register label still needs an embedding bridge.

<!-- lean-disclosures: stateBoundary stateBoundary_action stateBoundary_normalized -->
<!-- begin generated Lean disclosures -->
<details>
<summary>Exact Lean statement: stateBoundary</summary>

```lean
noncomputable def stateBoundary {n : ℕ} (C : Chain n 1 1) :
    Fin (canonicalize C).rank → ℝ
```

</details>

<details>
<summary>Exact Lean definition or proof: stateBoundary</summary>

```lean
:= boundary C (fun _ => 1)
```

</details>

<details>
<summary>Exact Lean statement: stateBoundary_action</summary>

```lean
theorem stateBoundary_action {n : ℕ} (C : Chain n 1 1) (x : Word n) :
    contract C x 0 0 = ∑ a, stateBoundary C a * contract (canonicalize C).canonical x a 0
```

</details>

<details>
<summary>Exact Lean definition or proof: stateBoundary_action</summary>

```lean
:= by
  have h := congrFun (congrFun (canonicalize_action C x) 0) 0
  simpa [stateBoundary, boundary, _root_.Matrix.mul_apply, _root_.Matrix.vecMul,
    dotProduct] using h
```

</details>

<details>
<summary>Exact Lean statement: stateBoundary_normalized</summary>

```lean
theorem stateBoundary_normalized {n : ℕ} (C : Chain n 1 1)
    (normalized : (∑ x : Word n, (contract C x 0 0) ^ 2) = 1) :
    mass (stateBoundary C) = 1
```

</details>

<details>
<summary>Exact Lean definition or proof: stateBoundary_normalized</summary>

```lean
:= by
  apply boundary_normalized
  simpa [chainMass, mass, _root_.Matrix.vecMul, dotProduct] using normalized
```

</details>
<!-- end generated Lean disclosures -->


## Empty and zero-dimensional cases

No positivity assumption is imposed on the natural bonds. Empty finite
sums are zero, the $0\times0$ identity and row-orthogonality are valid empty
matrix equalities, and every construction uses those same carriers.
An empty chain retains its original $r$ and transports $v$ by $I_r$.
If a terminal or intermediate bond is zero, contractions through it have
zero action; the backward recurrence propagates zero to all preceding
active dimensions. The mass identity then has zero on both sides.
The conditional normalization premise is impossible for such a zero-action
input. For the empty scalar chain, the sole contraction is $I_1$, the
state boundary is $(1)$, and the conditional scalar statement remains
consistent. No exceptional replacement semantics are invented.

## Dependency views and remaining boundary

The local source-construction topology has one sufficient route:
flattened deterministic core supplier plus absorbed tail recursion, followed
by all-word action, dimension bounds, and a separate all-terminal mass
consumer. Scalar specialization is a consumer of that route. This is an
author-proposed retrospective topology, not independent source-topology
approval. There is no claimed alternative construction in this packet.

The Lean view records the two actual module imports
`ConstructiveThinLQ` and `TensorTrainCanonical`, and ownership of this
module's public declarations. Named provider calls above are source-level
reference signals, not an exported elaborated proof-term dependency graph.
The compressed spine is deterministic exact-real right-canonicalization
with residual-boundary transport; the full equations remain its drill-down.

A proposed transport to physical sequential preparation has a complete
AND-tail: this exact contraction, normalized initial boundary, compatible
word/wire order, active-bond register embeddings, realized local isometry
completions, exact primitive clean-column action, and full terminal cleanup.
Finite-angle compilation and cost/error bounds must additionally be supplied
for a finite-bit resource claim. None of these additional inputs is created
merely by canonicalization. This conceptual transport is not a certified
functor or a new Lean implication in this module.

The inputs are arbitrary real core functions. Their generation, storage,
evaluation cost, and availability as executable data are uncosted here.
Exact comparisons, square roots, signed inverse trigonometric angles and
field operations do not constitute finite-bit arithmetic, runtime, or
numerical-stability bounds. The `noncomputable` marker alone neither proves
nor disproves an efficient implementation. Stored operation counting belongs
to the separate `StoredTensorTrain` refinement, and is not a theorem of
this module. No approximation, success probability, gate count, depth,
connectivity, ancilla synthesis, coherent oracle implementation, readout cost,
or complete scientific state-preparation root is certified here. Signed
amplitudes are preserved exactly, not only up to global phase; physical
phase and ancillary sectors await their own composition theorem.
