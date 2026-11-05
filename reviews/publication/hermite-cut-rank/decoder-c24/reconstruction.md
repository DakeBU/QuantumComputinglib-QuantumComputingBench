# HermiteCutRank: independent FORMAL → MATH reconstruction

Decoder: `hcr-decoder-c24`. Direction fingerprint: `HCR_AFFINE_CUT_SIGNED_THRESHOLD_AND_RANK_ONLY`.
Actual repository HEAD observed: `565516d28bcab79f39301c92f669ff43bbc68428`.
Target: `QuantumBlockEncoding/HermiteCutRank.lean`, SHA-256 `4953db6b9d5e255f0dd63094a243ef7bb6685053e86e920ffe02552faee86ce0`.
Initial formal-input seal SHA-256: `7c29e0242ae949324338c1863fdb7d48484cbd2cbe3c11ae1f1141f2398af531`.

This report reconstructs the entire actual formal module, not a migration-minimal delta and not an external source comparison. Its inventory was independently extracted from actual source: 20 public roots, including the definition and abbreviation. No authored lesson, scientific source metadata, publication candidate, graph proposal, previous review, or desired verdict was read. No source-agreement, publication, novelty, or integration verdict is issued. No subagents, production edits, cache writes, Git writes, or edits to the earlier CTT artifacts occurred.

The independent input seal predates the author packet. The later packet/context was read only afterward, and is bound separately by `later-binding-bridge.json`; the old seal has not been amended to pretend otherwise.

## 1. Carriers and ambient definitions

The ambient types α, β, ι and κ are arbitrary types, potentially empty or infinite. A `Matrix α β ℝ` is simply a real-valued function on the full Cartesian carrier α×β. Rows need NOT be finite. A finite width index ι supplies a `Fintype ι` and hence a finite sum. Only the four public rank statements require `Fintype β`: `FactorsThrough.rank_le`, `polynomial_add_rank_le`, `hermite_polynomial_add_rank_le`, and `hermite_affine_cut_rank_le`. Their row type α remains unrestricted.

For finite β, the actual imported definition of matrix rank is

\[
 \operatorname{rank}(F)=\dim_{\mathbb R}
 \operatorname{range}\left(z\in\mathbb R^\beta\mapsto
   \bigl(x\mapsto\sum_{y\in\beta}F(x,y)z(y)\bigr)\in\mathbb R^\alpha\right).
\]

This is natural-valued `Module.finrank` of the range of `F.mulVecLin`; over ℝ and finite β the range is finite-dimensional, even when α is infinite. It is neither approximate rank nor a rank of a state-preparation circuit.

`p : ℝ[X]` is an ordinary real univariate polynomial; `p.eval z` is evaluation at z. `natDegree` is its ordinary degree when nonzero and is zero for the zero polynomial. Mathlib's `taylor r p` is literally `p.comp (X + C r)`, so `(taylor r p).eval s = p.eval(s+r)`. Its coefficient at i equals `p^(i)(r)/i!` over ℝ. Powers with exponent zero equal one, including `0^0` in these polynomial formulas.

`Nat.ceil z` is the LEAST NONNEGATIVE INTEGER n with `z≤n`. Thus it is zero for z≤0; it is not an unbounded integer ceiling that may be negative. Its exact characterization used here is `j < Nat.ceil z ↔ (j:ℝ) < z` for every natural j. All natural-to-real casts in the sampled index are exact mathematical casts.

### The particular polynomial and piecewise function

Expand `HermitePolynomial.sourceInterpolant k` as the following particular polynomial P_k, not an arbitrary polynomial postulated to satisfy some endpoint conditions. For k≥0 define

\[
 c_{k,r}=\sum_{m=0}^{r}\frac{\binom{k+r-m}{k}}{m!},\qquad
 A_k(z)=\sum_{r=0}^{k}c_{k,r}z^r.
\]

For t=p+1, its value is exactly

\[
 P_k(p)=e^{-1}(1-t)^{k+1}A_k(t)
             +t^{k+1}A_k(1-t).
\]

The actual provider defines A_k by truncating `exp(X)/(1-X)^(k+1)`, forms `(1-X)^(k+1) A_k(X)`, and translates the symmetric expression by `taylor 1`. Its proved finite-sum and evaluation formulas yield precisely the expression above on ALL real p. The provider proves `natDegree P_k ≤ 2k+1`, `P_k(-1)=e^-1`, and `P_k(0)=1` (indeed the corresponding endpoint jets through order k). The cut-rank module uses the degree bound and the zero-endpoint value as dependencies, not as caller premises.

The actual `smoothInitial k p`, written S_k(p), is

\[
 S_k(p)=\begin{cases}
 e^p,&p<-1,\\
 P_k(p),&-1\le p\le0,\\
 e^{-p},&p>0.
 \end{cases}
\]

Both junctions belong to the polynomial branch in the literal definition. A target theorem below moves ONLY the zero endpoint to the right exponential branch using `P_k(0)=1`; it does not change the function. There is no normalization factor in S_k.

## 2. All 20 public roots, with their exact mathematical content

Every name in this section has prefix `QuantumBlockEncoding.HermiteCutRank`. The associated complete source signatures and line numbers are independently frozen in `signatures.json`. Existence conclusions below have their ordinary logical quantifiers; they are not new required input certificates.

### 1. `FactorsThrough`

For a specified finite index ι and F:α×β→ℝ, this proposition means

\[
 \exists L : \alpha\times\iota\to\mathbb R,\quad
 \exists R : \iota\times\beta\to\mathbb R,\quad
 \forall x\in\alpha\ \forall y\in\beta,\quad
 F(x,y)=\sum_{i\in\iota}L(x,i)R(i,y).
\]

The definition has no positivity, orthogonality, normalization, sparsity, full-rank, stability, or runtime condition on either factor. It is a `Prop` with existential witnesses, NOT a data structure returning stored arrays or an executable factor supplier.

### 2. `FactorsThrough.rank_le`

Assume finite β and ι and the displayed finite-width factorization of F. Then `rank(F)≤|ι|`. In the proof F=L R and `rank(LR)≤rank(L)≤|ι|`. No finiteness of α is needed. The factorization is an input premise in this generic implication; downstream target factorization is proved separately rather than assumed.

### 3. `polynomial_add_factorization`

For ANY real polynomial p, natural d, premise `natDegree p≤d`, and arbitrary functions u:α→ℝ and v:β→ℝ,

\[
 F(x,y)=p(u(x)+v(y))
\]

factors through `Fin(d+1)`. Explicit witnesses in the formal proof are

\[
 L(x,i)=[X^i]p(X+u(x)),\qquad R(i,y)=v(y)^i,
 \qquad 0\le i\le d.
\]

Taylor translation preserves the degree, so these terms evaluate the polynomial exactly, not as an approximation. No finite α or β premise is present.

### 4. `polynomial_add_rank_le`

With the same p,d,degree premise,u,v and additionally finite β,
`rank((x,y)↦p(u(x)+v(y)))≤d+1`.

### 5. `hermite_polynomial_add_rank_le`

For every natural k, real-valued u,v and finite β,
`rank((x,y)↦P_k(u(x)+v(y)))≤2k+2`. The caller supplies NO degree hypothesis; the imported actual P_k degree theorem supplies it. This is the POLYNOMIAL component alone, not the full piecewise S_k sample matrix.

### 6. `product_factorization`

For arbitrary real u:α→ℝ and v:β→ℝ, `(x,y)↦u(x)v(y)` factors through `Unit`. The witnesses are L(x,*)=u(x), R(*,y)=v(y). No nonzero or finite-domain assumption occurs. The width is one, but the theorem does not assert rank exactly one.

### 7. `exponential_add_factorization`

For arbitrary real u,v, `(x,y)↦exp(u(x)+v(y))` factors through `Unit`, with L(x,*)=exp(u(x)) and R(*,y)=exp(v(y)). This uses the exact real exponential identity, without numerical evaluation guarantees.

### 8. `FactorsThrough.add`

Given a width-ι factorization F=L R and width-κ factorization G=C D, F+G factors through the DISJOINT SUM `Sum ι κ`. On the left and right summands take the respective original factors. The width is |ι|+|κ|. Both factorization premises are required; this is not two independently sufficient implications.

### 9. `FactorsThrough.neg`

Given F=L R through finite ι, -F factors through the same ι by replacing L with -L. No new factor index is added and no sign restriction is imposed.

### 10. `FactorsThrough.pointwise_mul`

Given F=L R through finite ι and G=C D through finite κ, the ENTRYWISE product F(x,y)G(x,y) factors through `ι×κ`, with

\[
 L'(x,(i,j))=L(x,i)C(x,j),\qquad
 R'((i,j),y)=R(i,y)D(j,y).
\]

This is not the matrix product F G. The width multiplies, and no dense-matrix runtime or storage statement follows from these function witnesses.

### 11. `blockIndex_lt_iff`

For natural M,x,y,T with the SINGLE logical premise y<M,

\[
 Mx+y<T\iff x<\lfloor T/M\rfloor\ \lor\
   (x=\lfloor T/M\rfloor\ \land\ y<T\bmod M).
\]

Division and remainder here are natural Euclidean operations. The premise implies M>0. There is no upper bound on x and no assumption that M is a power of two or T lies within a fixed total register range. The disjunction is disjoint; a quotient-boundary row can be partial while all earlier rows are full.

### 12. `threshold_factorization`

For natural M,T, functions u:α→ℕ, v:β→ℕ and the premise `∀y∈β, v(y)<M`, the indicator

\[
 I_T(x,y)=\mathbf1\{Mu(x)+v(y)<T\}
\]

factors through `Fin 2`. Write q=T/M and r=T mod M. The exact factors, at every label, are

\[
 L_T(x,0)=\mathbf1\{u(x)<q\},\quad L_T(x,1)=\mathbf1\{u(x)=q\},
 \qquad R_T(0,y)=1,\quad R_T(1,y)=\mathbf1\{v(y)<r\}.
\]

Thus I_T equals the sum of the full-row and boundary-row terms. No finite-domain, bit-string, binary-size or injectivity premise is present.

### 13. `threshold_complement_factorization`

Under exactly the preceding hypotheses, 1-I_T also factors through `Fin 2`, NOT a three-element sum obtained by appending a constant term. It uses the SAME R_T and

\[
 \bar L_T(x,0)=1-\mathbf1\{u(x)<q\},\qquad
 \bar L_T(x,1)=-\mathbf1\{u(x)=q\}.
\]

The second coefficient may be -1. The final matrix is a 0/1 complement indicator, but the witnesses are signed real factors, not probabilities or nonnegative factors.

### 14. `affine_lt_cut`

For all real a,h,t with the premise h>0, and natural j,

\[
 a+hj<t\iff j<\operatorname{Nat.ceil}((t-a)/h).
\]

No endpoint alignment, representability, bound on j, or sign assumption on t-a is needed. A nonpositive quotient gives cut zero and correctly selects no natural j. If the quotient is a nonnegative integer m, the strict test is j<m, so a sample exactly at t is excluded. h=0 and h<0 are NOT covered.

### 15. `smoothInitial_strict`

For every k and every real p, S_k(p) equals e^p for p<-1, P_k(p) for -1≤p<0, and e^-p for p≥0. There is no logical input premise: P_k(0)=1 is proved from its actual provider. At p=-1 this version still chooses the polynomial; at p=0 it chooses the right exponential, with equal values.

### 16. `HermiteBond`

This abbreviation is the EXACT finite index type

```text
Sum
  (Sum (Fin 2 × Unit)
       ((Sum (Fin 2) (Fin 2)) × Fin (2*k+2)))
  (Fin 2 × Unit).
```

Its labels remember the left piece, the signed four-term middle threshold difference times polynomial index, and the right piece. It is not itself a tensor-train core, a physical register, a normalized bond vector, or an isometry.

### 17. `hermiteBond_card`

For all k, `|HermiteBond k|=8k+12`: left width 2, middle width `4(2k+2)`, right width 2. This is an exact index-cardinality identity, not a minimal width or a qubit/gate complexity theorem.

### 18. `hermite_affine_factorization`

For arbitrary natural k,M, real a,h with h>0, functions u:α→ℕ and v:β→ℕ, and `∀y, v(y)<M`, the full matrix

\[
 F(x,y)=S_k\bigl(a+h(Mu(x)+v(y))\bigr)
\]

factors through the EXACT `HermiteBond k`. Neither α nor β is assumed finite. This equality holds for EVERY pair in α×β, not only samples strictly inside one interval or away from either junction. No factorization, interpolation, amplitude-action, nonzero-normalizer, or rank certificate is an additional caller premise.

The proof's complete construction is expanded in Section 3 below.

### 19. `hermite_affine_cut_rank_le`

Under exactly the preceding data and hypotheses, plus finite β,

\[
 \operatorname{rank}\bigl((x,y)\mapsto
 S_k(a+h(Mu(x)+v(y)))\bigr)\le8k+12.
\]

This is an upper bound on exact real matrix rank across this one affine cut. No exact-rank equality, approximation guarantee, complete tensor-train construction, simultaneous choice of cores for all cuts, sequential canonicalization, state-action theorem, or state-preparation resource bound is in its conclusion.

### 20. `FactorsThrough.scale`

Given ANY width-ι factorization of F and ANY real scalar c, cF factors through the SAME ι with left factor cL and right factor R. In particular c may be zero or negative. A comment mentioning constant normalization does not prove that c is a normalizer, that it is computable, or that the resulting amplitudes have unit mass.

## 3. Explicit full Hermite separation and its endpoint logic

Fix the data of root 18. Let j(x,y)=Mu(x)+v(y), define

\[
 T_- =\operatorname{Nat.ceil}((-1-a)/h),\qquad
 T_0 =\operatorname{Nat.ceil}((0-a)/h),
\]

and set ρ(x)=a+hMu(x), σ(y)=hv(y). Then ρ(x)+σ(y)=a+hj(x,y). Let I_- and I_0 be the strict natural-index threshold indicators at T_- and T_0. By root 14 these are exactly the strict real tests p<-1 and p<0. In particular I_-≤I_0 pointwise; this is a consequence of the thresholds, not an assumed premise.

The full pointwise identity is

\[
 F=I_-e^{\rho+\sigma}
       +(I_0-I_-)P_k(\rho+\sigma)
       +(1-I_0)e^{-\rho-\sigma}.
\]

At p=-1, I_-=0 and I_0=1, so the middle polynomial supplies the value. At p=0, I_-=I_0=0, so the right exponential supplies the value 1, exactly agreeing with the literal polynomial endpoint. These are exact junction values, not limits or omitted grid points. If thresholds are zero or outside the sampled range the same formula still holds.

Use the threshold factors L_T,R_T of root 12 and complement factors of root 13. The actual witness blocks are:

- Left label `(s,*)∈Fin 2×Unit`: left value `L_(T_-)(x,s) exp(ρ(x))`, right value `R_(T_-)(s,y) exp(σ(y))`.
- Middle label `(z,i)∈(Fin 2 ⊕ Fin 2)×Fin(2k+2)`: for z=inl(s) use the T_0 threshold factors; for z=inr(s) use the NEGATIVE T_- left factors and unchanged T_- right factors. Multiply these respectively by `[X^i]P_k(X+ρ(x))` and `σ(y)^i`. The resulting block is exactly `(I_0-I_-)P_k(ρ+σ)`.
- Right label `(s,*)∈Fin 2×Unit`: left value `barL_(T_0)(x,s) exp(-ρ(x))`, right value `R_(T_0)(s,y) exp(-σ(y))`.

Direct-sum the first two blocks, then the third. This has precisely the nested Sum/Product carrier of root 16, not an unspecified width-isomorphic type. The signed subtraction is retained: none of these formulas asserts all intermediate factors are nonnegative. The factorization theorem supplies these witnesses inside an existential proposition, not a stored, costed classical algorithm.

## 4. Binder, definition and boundary audit

All index types and real/natural parameters are ordinary formation data. `Fintype` instances specify finite summation carriers; they are not independence or invertibility assumptions. Explicit substantive inputs are:

- generic polynomial roots 3 and 4: `natDegree p≤d`;
- generic factor operations and root 2: the applicable expanded existential factorization premise(s);
- root 11: y<M;
- roots 12 and 13: `∀y, v(y)<M`;
- root 14: h>0;
- roots 18 and 19: BOTH h>0 and `∀y, v(y)<M`.

Everything else used to factor the literal S_k samples is supplied by the implementation's dependencies. No public normalization, full state action, or resource bound is hidden in a contract structure. Whether any premise is an external-source hypothesis is intentionally not classified, because the external source is withheld.

The two local definitions are literal: a finite-sum existential relation and a concrete finite sum/product index type. There is no quotient representative, choice-defined interpolant, uniqueness claim for factors, default state, zero fallback, or selection of an unspecified object in the target interface. Its provider's P_k is an explicit polynomial formula, not a new arbitrary premise.

Degenerate cases are included in the quantified carriers:

- α or β may be empty. Factorization assertions are then vacuous over entry labels, with matrix witnesses still of the declared types. Finite-column rank is zero for an empty row or column carrier over ℝ.
- Empty ι is permitted in `FactorsThrough`; the sum is zero, so the predicate then means F is identically zero. Generic add/product/neg/scale retain the ordinary empty-sum behavior.
- The zero polynomial has natDegree zero, so it is covered even with d=0. Polynomial factors have d+1 slots regardless of actual degree or dependencies; the width/rank bound need not be sharp.
- There is no explicit M>0 binder in roots 12,13,18,19. If β is nonempty their suffix premise implies it. If β is empty, M=0 is permitted and there are no columns; this must not be silently removed from the public carrier. Root 11's individual y<M premise directly rules out M=0 there.
- With T=0 the threshold matrix is zero and its complement is one. If M>0 divides T exactly, the remainder term has empty strict suffix support. Neither case requires an additional branch in the formal statements.
- M=1 is allowed, so the suffix map is necessarily zero on every column. Neither u nor v needs to enumerate distinct samples, and there is no upper bound on u.
- k=0 is included; the exact declared HermiteBond cardinal is 12. The result does not assert this is minimal. Natural ceilings may be zero; arbitrary a is allowed. Reversed or zero grid spacing is excluded by h>0, not repaired by a fallback formula.

## 5. Seven quantum semantic slots

| Slot | Exact scope and omitted claims |
|---|---|
| Target and normalization | Full real matrix S_k(a+h(Mu+v)) on α×β, and generic polynomial/product/threshold kernels. No normalized state or density matrix is defined. Scaling preserves width but supplies no normalizing scalar or unit-mass proof. |
| Dimensions/scalar/basis/order | Real scalars; arbitrary α,β with finite β only for rank. The concatenation formula is literally M·prefix+suffix, with suffix<M. M need not be binary-sized. HermiteBond has exact nested sum/product order and cardinal8k+12, but no physical qubit order, bit layout, Fourier convention, or register embedding is supplied. |
| Access/oracles/inverses/controls | Inputs are mathematical functions and real parameters. No query oracle, coherent label access, inverse/control interface, efficient coefficient lookup, or input-evaluation cost contract appears. |
| Ancillas/workspace/cleanup | No circuit, initialized physical register, preserved/overwritten register action, dirty-workspace semantics, terminal cleanup or garbage-sector theorem is present. The complete mathematical output carrier is α×β; HermiteBond is an internal separation label, not an accepted measurement sector. |
| Phase/sign | Exact signed real equalities. The complement and middle subtraction explicitly allow negative factors. No complex phase family, global-phase quotient, probability-only replacement, or circuit phase certificate is asserted. |
| Norm/error/success | Exact finite-sum identities and rank inequalities, with no norm bound, tolerance, numerical truncation error, confidence, success probability, postselection or amplitude amplification statement. The polynomial is finite by definition, not an approximation certified here. |
| Resource tier | Width/cardinality and algebraic rank only. No full tensor train, canonical/isometric cores, PREPARE/SELECT implementation, gate synthesis, storage/runtime/bit complexity, finite-precision rounding, numerical conditioning, qubit/ancilla count, depth/connectivity, noise or readout bound is proved. Exact exp, real arithmetic, comparisons and Nat.ceil are mathematical operations without a cost model here. |

## 6. Exact context, later packet bridge and execution boundary

`formal-input-seal.json` lists every actual source/protocol/configuration file read with SHA-256 and exact full/partial extent. The process files were read fully: AGENTS, HARNESS, `qbe-substantive-worker`, `qbe-source-dependency-audit`, theorem-publication, proof-digestion and evidence-routed-memory protocols. The target and its only project provider `QuantumBlockEncoding/HermitePolynomial.lean` were read in full. Selected actual Mathlib rank, natural-ceiling, Taylor, evaluation/degree and natDegree definitions were expanded at the recorded extents. No complete transitive source or proof-term dependency audit is claimed.

The target imports are exactly `QuantumBlockEncoding.HermitePolynomial`, `Mathlib.LinearAlgebra.Matrix.Rank`, and `Mathlib.Algebra.Order.Floor.Semiring`. It uses a `noncomputable section`, namespace `QuantumBlockEncoding.HermiteCutRank`, `open Polynomial`, scoped `BigOperators`, and implicit type variables α,β,ι,κ. No additional global hypothesis block exists. Actual `lean-toolchain`, `lake-manifest.json`, and `lakefile.lean` were read and sealed. Toolchain is Lean4.33.0; Mathlib is manifest-pinned at `db584cd6d46c92f209a44c0f1c829460d327499d`.

Later packet path: `reviews/publication/hermite-cut-rank/author-decoder-packet.json`, SHA-256 `a9e89e6e3014ff7199db15dc84fbd3b4765ca3a578268914867ea3f1f8ffa5d2`.
Later context path: `reviews/publication/hermite-cut-rank/author-formal-context.json`, SHA-256 `f2829280ca4e4eefc0c258c7d6f3f846acd45eb1d4ae34b602f9789cc49250f1`.
Opaque binding preserved without recomputation: `4c21761e76780c5f175e4416bb26bb01f1b6b12cf72b703eb0c0bb6f6d687727`.

The bridge independently verifies exact UTF-8 source bytes from both formal-context file payloads against the initial source hashes, all20 full `source_exact` declarations and positions, declaration order, target/toolchain/manifest/lakefile equality. The snapshot's `full_source_lines` already contain newline characters: concatenate with NO separator. An initial comparison adding newline separators failed because of that comparison method; the corrected exact-byte checks pass and both outcomes are retained.

Eleven `statement_source` convenience fields in the context split prematurely at a named argument `:=`; for example `(ι := ι)` was cut after `(ι`. This is a lexical-extraction limitation, not a target theorem mismatch: the full `source_exact` declarations and full file payloads are intact. The reconstruction uses the independently sealed complete source signatures, not the truncated fields. The context explicitly supplies no fresh compilation or cache attestation.

The subsequently supplied v2 formal-only packet/context were independently checked and are separately frozen in `later-binding-bridge-v2.json`. Packet v2 SHA-256 is `d3554a962721b44b228f6e5c29966973c295af538ed66758b098f6432c2bf7c8`; context v2 SHA-256 is `37831aec1c838ac37490386b1145b904976916e1419295cfd2d519667adf3eb0`. All20 v2 `statement_source` strings exactly match the original independent complete source-signature seal. All20 `source_exact` strings and both reconstructed full-source byte strings are unchanged from v1 and actual source. Toolchain, manifest, lakefile, target and opaque binding remain identical. Neither the initial seal nor the preserved v1 bridge was overwritten.

A later v3 packet is independently frozen in `binding-bridge-v3.json`: packet SHA-256 `7e2e5fa7f2a9312ec91430f81defe82e5892fd9ff9fb033bf6a4239c51dbe15b`, new opaque binding `a754b4c7b288d0c2adadbaf7ab29984a985458c1b917421c36ef54d8c6754f84`. A strict field-by-field comparison found ONLY `binding_sha256` and `supersedes` changed from v2. Its formal-context-v2 reference/hash, all20 roots, target/toolchain/manifest/lakefile and every other field are unchanged. The binding was not recomputed, no withheld files were opened, no mathematical content of this reconstruction changed, and no compiler was rerun for v3.

The first actual-source compiler attempt used the direct Lean4.33.0 compiler with `-j 1 -M 3072`, the actual target source, an output olean path in this decoder's scratch, and normal project/package import-cache roots. It did not rebuild dependencies or import the cached target as proof of a fresh source check. This attempt exited1 with sole diagnostic `libc++abi: terminating due to uncaught exception of type std::bad_alloc: std::bad_alloc`. This is retained as `ENV_BLOCKED(resource)` for that attempt, not refutation or an API/source mismatch. The successful retry below does not erase this failed attempt; no successful axiom census is inferred from the failed command.

After the parent reported that the competing compiler processes had released memory, the single allowed target retry used the same command and exited0. The complete diagnostics are retained in `compile-output.txt` with ONLY the checkout prefix replaced by repository-relative paths; the unsanitized original is PRIVATE. Both warnings are at `QuantumBlockEncoding/HermiteCutRank.lean:257`: unused simp arguments `Matrix.add_apply` and `Matrix.neg_apply`. No warning was suppressed or source changed. The fresh target olean SHA-256 is `daf7a8c8461a82d4d41fe49d17faf10e3a0347c45a832b6993d208dfb82110fa`.

The probe explicitly resolves `QuantumBlockEncoding.HermiteCutRank` through `--setup importArts` to that NEW olean, not the cached target. The normal project/package roots resolve all other imports. All20 `#check @...` and all20 `#print axioms` commands completed with exit0. `HermiteBond` has no axioms; each of the other19 roots lists exactly `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx` or extra project axiom appears. The initial successful print omitted implicit return-type arguments; it is retained as `probe-output-initial.txt`. The final `probe-output.txt` uses `pp.explicit=true` in addition to full names and universes, retaining the complete displayed signature arguments. This census concerns these20 roots, not every unused declaration in every imported module.

Public command forms, with REPO, SCRATCH and LEAN standing only for local locations, are:

```text
LEAN -j 1 -M 3072 --root REPO -o SCRATCH/fresh/QuantumBlockEncoding/HermiteCutRank.olean REPO/QuantumBlockEncoding/HermiteCutRank.lean
LEAN -j 1 -M 3072 --setup ProbeSetup.private.json Probe.lean
```

LEAN_PATH consists of the normal project build root followed by all actual manifest package build roots in manifest order. Imported dependencies are INHERITED caches, not freshly rebuilt or checked at trust0. The three direct imported olean digests were measured before and after and stayed unchanged, and every sealed source/configuration/protocol digest was revalidated unchanged. Thus the scoped target was freshly compiled against inherited providers; this is not a fresh transitive rebuild or a source/cached-provider equality certificate for the entire dependency graph.

The read-only Git HEAD command initially failed sandbox access; a scoped read-only escalation then returned the stated actual HEAD with exit0. No Git operation wrote state. Exact expanded local commands and setup paths remain in clearly PRIVATE artifacts and are not suitable for publication verbatim.

## 7. Handoff

Objective: whole-module source-blind formal decoding, all20 actual roots. Mathematical delta: explicit full carriers, precise hypotheses, natural-ceiling saturation and junction conventions, signed two-slot complement, exact middle factor index, and separation/rank-only boundary. Named evidence: bound actual formal source, complete source signatures, imported definitions, immutable input seal and later exact-byte packet bridge; compiler status is recorded without promoting a failed attempt. No mathematical route was rejected or retired.

Final bounded-task failure class: `NONE`; the historical first compile failure remains `ENV_BLOCKED(resource)` in the attempt log. Fresh actual-target and fresh-target-mapped signature/ordinary-axiom gates succeeded. Full repository, source-comparison and publication gates remain NOT_RUN, not passed by implication.

Process memory consulted: no mathematical memory records, because scope is the frozen formal inputs. Parallel admission/common-blind-spot/comparator: not applicable; no subagent or alternate route selection. Salvage: the complete sealed source reconstruction and probe source remain reusable regardless of compiler resource availability. Purification/Exposition Seal: no production integration or seal claimed. Parent owns canonical packet wrappers, registry, full repository gates and Git actions. No `lake build`, `lake build Tests`, full transitive rebuild, website, or publication/source-comparison gate is claimed by this decoder.
