# Tensor-train canonical and norm-environment formal reconstruction

Decoder `ttc-norm-decoder-c25`; fingerprint `TTC_PADDED_COMPLEX_CORE_AND_NORM_ENV_SEMANTICS_NOT_PHYSICAL_COST`.
Actual input HEAD observed read-only: `00691177919c4437939f3f2b6714e2ad0de60b7a`.
Initial formal-input seal: `7d4454d0e1b6f490df384bc8d4d0dc6444e2ec20dac5780a72dae0bd748005d7`.

Actual Canonical source SHA-256: `0b51ec0335aaf6248f40b3f8dcf6014172c231b9ae512bf5bb09d84ebf66f808`.
Actual NormEnvironment source SHA-256: `a898ff4a83a1cc6426af7e85d3adc812c46175af0a31c1fd5eb2d48c776afb0d`.

This is independent FORMAL → MATH reconstruction of the whole actual modules `QuantumBlockEncoding/TensorTrainCanonical.lean` and `QuantumBlockEncoding/TensorTrainNormEnvironment.lean`, not an external-source comparison, publication verdict, or migration-minimal-delta audit. I previously read Canonical, ThinLQ, SequentialBondPreparation and RealAmplitudePreparation as formal providers during the earlier CTT work; this is NOT first exposure to that code. The current actual files were re-read and separately sealed. No natural-language source package, authored lesson, candidate, graph, plan, prior review or desired verdict was read in this new SAU. The initial seal preceded any author packet; none was supplied at that stage.

Independent inventory finds 33 non-instance Canonical roots and 15 NormEnvironment roots: 48 requested roots. Canonical also declares the explicit named instance `wordFintype`, separately reconstructed and checked below, making 49 named source declarations if instances are counted. Generated constructors/recursors are expanded where relevant, not counted as extra source roots. Complete independently extracted source headers and subsequent actual probe types are retained in `signatures.json`; lexical source signatures alone are not called fresh elaborated types.

## 1. Common carriers and conventions

Write [d] for `Fin d`, including the empty set [0]. Matrices are functions on their row and column index sets, with finite-sum multiplication and ordinary Kronecker-delta identities. All core and chain amplitudes are REAL. Complex values appear only in the explicit lift and local-stage/padding interfaces. No positivity, nonzero dimension, nonzero pivot, full rank, or unit normalization is a standing convention.

For a chain with n cores, write its actual bond dimensions as `b_0=l,...,b_n=r`, its cores as A_i, and a word as `(s_0,...,s_(n-1))`. The full bond-to-bond contraction matrix is T_C(x). With a real initial ROW boundary v, define the full output amplitude

\[
 f_{C,v}(x,t)=\sum_{a\in[l]}v(a)T_C(x)_{a,t},
 \qquad (x,t)\in\operatorname{Word}(n)\times[r].
\]

The terminal bond is part of the full output carrier; it is not implicitly projected out or cleaned. In particular a general r>1 chain is not merely a scalar n-bit amplitude table.

The imported sequential types are different representations: `PrimitiveBasis n = Fin n → Fin 2`, `SequentialBondPreparation.Core B = Matrix (Fin 2 × B) B ℂ`, `Stage B = Matrix (Fin 2 × B) (Fin 2 × B) ℂ`, and `BondState n B = PrimitiveBasis n × B → ℂ`. Stage rows are outputs, columns are inputs. A stage acts on a fresh zero bit, leaving the previous prefix passive via an identity tensor factor. Its actual formula is

\[
 \operatorname{step}(U,w)(x,b)=
 \sum_a U((x(n),b),(0,a))\,w(\operatorname{init}x,a).
\]

Here x(n) means `x(Fin.last n)`: the newly emitted bit is appended at the highest named wire; `Fin.init x` contains the old prefix. `Word n` is instead a recursive head-first product. The targets do not supply a whole-chain equivalence identifying those two representations or a flattened physical circuit; the local adapter formulas below do not silently provide that extra bridge.

## 2. Canonical module: all 33 roots and the extra named instance

Names in this section have prefix `QuantumBlockEncoding.TensorTrainCanonical`. All natural parameters and displayed data are universally quantified unless existentially bound. Statements cover every valid value of their actual dependent types.

### C1. `Core`

`Core l r` abbreviates the real matrix `[l] × ({0,1}×[r]) → ℝ`. Its entry is A(a,(s,b)): old/left bond a is a ROW, and emitted bit s together with next/right bond b is a COLUMN.

### C2. `slice`

For every A:Core l r and bit s∈[2], `slice A s` is the `[l]×[r]` matrix A_s(a,b)=A(a,(s,b)). No sum or basis change occurs.

### C3. `Chain`

This dependent inductive type has exactly the constructors `nil r : Chain 0 r r` and `cons A C : Chain (n+1) l r` for A:Core l m and C:Chain n m r. Thus adjacent bond dimensions match by type, and the empty chain necessarily has equal initial and terminal dimensions. There is no padding in this carrier.

### C4. `Word`, plus named instance `wordFintype`

`Word 0 = Unit` and `Word (n+1) = Fin 2 × Word n`. The first core takes the first bit. There is one empty word, and the explicit instance `wordFintype n` recursively equips every Word n with finite enumeration. This instance is additional named ambient evidence beyond the 48 non-instance roots; it introduces no mathematical hypothesis.

### C5. `contract`

\[
 T_{\mathrm{nil}\,r}(*)=I_r,\qquad
 T_{\mathrm{cons}\,A\,C}(s,y)=A_sT_C(y).
\]

This is a real `[l]×[r]` matrix for each word; equivalently the product of all slices in chain order. It is not restricted to a scalar boundary or one terminal label.

### C6. `RightCanonical`

This predicate is True for nil, and for cons A C it means BOTH `A Aᵀ=I_l` and `RightCanonical C`. Each core therefore has orthonormal rows:

\[
 \sum_{s\in[2],b\in[m]}A(a,(s,b))A(c,(s,b))=\delta_{a,c}.
\]

It is not square unitarity and it is not assumed for arbitrary input chains.

### C7. `RankReduced`

The relation's empty constructor relates nil r to itself. Its cons constructor relates cons A C to cons Q D when the tails are related and, if D starts in dimension m', Q has type `Core (min l (2*m')) m'`. Accordingly new actual bond dimensions satisfy

\[
 d_n=r,\qquad d_i=\min(b_i,2d_{i+1}).
\]

The relation constrains dimensions and chain shape, NOT core entries or numerical matrix/Schmidt ranks. It does not itself assert equality of amplitudes or canonicality. It retains the terminal dimension exactly.

### C8. `absorb`

For A:Core l m and real R:[m]×[r], this returns Core l r with
`absorb(A,R)(a,(s,c))=Σ_b A(a,(s,b))R(b,c)`. Only the right bond is summed; physical bit labels are not mixed.

### C9. `absorb_slice`

For every such A,R and bit s, `slice(absorb A R)s = A_s R` exactly.

### C10. `exists_core_lq`

For every A:Core l r, with q=min(l,2r), there EXIST real R:[l]×[q] and Q:Core q r satisfying BOTH A=R Q and Q Qᵀ=I_q. No full-rank or nonzero-row premise is present. The proof flattens `(s,b)` by the actual equivalence `b+r*s`, uses ThinLQ existence, then reindexes Q back to physical-bit/right-bond labels.

The actual imported wide ThinLQ proof completes a Gram–Schmidt family to an orthonormal basis by classical choice; the tall case uses the original matrix and identity. Deficient and empty shapes remain allowed. The result is existential algebraic data, not an efficient or deterministic arithmetic producer, and q is not asserted to be the true rank.

### C11. `exists_rightCanonical`

For EVERY input C:Chain n l r, there exist l', R:[l]×[l'], and D:Chain n l' r such that ALL of the following hold: `RightCanonical D`, `RankReduced C D`, and `∀x, T_C(x)=R T_D(x)`. The latter is full matrix equality for every word, every original initial label and every terminal label.

There is no input canonicality, normalization, residual-factorization or global-action premise. The proof starts at the actual tail, absorbs its residual into the preceding core and applies C10. Nil uses l'=r, R=I_r, D=nil r. Existence and classical orthonormal completion do not supply costed preprocessing or a named output function.

### C12. `RankReduced.head_bound`

For related C:Chain(n+1) l r and D:Chain(n+1) l' r, l'≤l, and there exist m', Q:Core l' m', and tail:Chain n m' r such that D=cons Q tail and l'≤2m'. The sole logical premise is the expanded rank-reduction relation; D need not separately be assumed canonical.

### C13. `RankReduced.last_bond_le_two`

For related C:Chain 1 l 1 and D:Chain 1 l' 1, l'≤2. This applies to a ONE-core chain ending at dimension one, not arbitrary unrelated penultimate bonds.

### C14. `mass`

For any finite type I and v:I→ℝ, `mass v = Σ_i v(i)^2`. This is squared Euclidean mass, not its square root; it includes empty I, signed entries and zero vectors.

### C15. `mass_vecMul`

For finite I,J, decidable equality on I, real A:I×J with premise A Aᵀ=I_I, and arbitrary real row vector v:I→ℝ,
`mass(v A)=mass v`. Expanded, `Σ_j(Σ_i v_i A_ij)^2=Σ_i v_i²`. No positivity or normalized boundary premise is required.

### C16. `chainMass`

For every real boundary v:[l]→ℝ,

\[
 \operatorname{chainMass}(C,v)=
 \sum_{x\in\operatorname{Word}(n)}\sum_{t\in[r]}f_{C,v}(x,t)^2.
\]

Every terminal label is included. Nil's singleton word gives mass v, not zero.

### C17. `chainMass_eq`

Given C and premise `RightCanonical C`, for every real v, `chainMass C v = mass v`. Local row orthogonality is assumed in this reusable implication. The proof recursively sums both physical bits and all final labels. No postselection or terminal cleanup is inferred.

### C18. `residual_mass`

For C:Chain n l r, D:Chain n l' r, R:[l]×[l'], premises `RightCanonical D` and `∀x, T_C(x)=R T_D(x)`, and arbitrary v,
`chainMass C v = mass(v R)`. Both premises are genuine inputs to THIS generic lemma. There is no RankReduced premise, nor a claim mass(vR)=mass v for arbitrary input C.

### C19. `exists_rightCanonical_normalized`

For C:Chain n l 1 and real v with the SINGLE mathematical premise `chainMass C v=1`, there exist l',R,D ending in terminal dimension ONE, with right canonicality, rank reduction, the full all-word MATRIX action, and `mass(vR)=1`. Canonicality/action are delivered, not additional caller premises. It does not normalize an arbitrary unnormalized input by division.

### C20. `exists_normalized_state`

For C:Chain n 1 1 with premise `Σ_x T_C(x)_(0,0)^2=1`, there exist l', real u:[l']→ℝ and D:Chain n l' 1 such that D is right canonical, ranks are related, mass u=1, and

\[
 \forall x,\quad T_C(x)_{0,0}=\sum_{a\in[l']}u(a)T_D(x)_{a,0}.
\]

This is the scalar-boundary specialization; it preserves signed amplitudes. No target-state equality is assumed, and no primitive preparation circuit is returned.

### C21. `maxBond`

`maxBond(nil r)=r`; `maxBond(cons A C)=max(l,maxBond C)`. It includes BOTH boundaries, not merely internal bonds.

### C22. `RankReduced.maxBond_le`

For related chains C,D, `maxBond D≤maxBond C`. This is dimension monotonicity, not a runtime, gate or physical-register count.

### C23. `complexCore`

For real A:Core l r define the rectangular complex matrix K with output ROW `(s,b)∈[2]×[r]` and input COLUMN a∈[l] by `K((s,b),a)=(A(a,(s,b)):ℂ)`. This transposes input/output orientation and embeds real entries into ℂ; it does not accept general complex-valued input cores or remove signs.

### C24. `complexCore_isometry`

Given A and premise A Aᵀ=I_l, the returned K obeys K†K=I_l, where † is conjugate transpose. This is column isometry; K K†=I_(2r) is NOT asserted. Degenerate rectangular shapes are included.

### C25. `sequentialCore`

For an equal-rank real A:Core r r, this is literally `complexCore A` as `SequentialBondPreparation.Core (Fin r)`. It is a type/orientation adapter, not a stage completion or gate compiler.

### C26. `sequential_step`

For A:Core r r, an arbitrary complex square Stage U on `[2]×[r]`, and the premise
`∀s,b,a, U((s,b),(0,a))=(A(a,(s,b)):ℂ)`, every complex prefix/bond vector v and every x,b satisfy

\[
 \operatorname{step}(U,v)(x,b)=
 \sum_{a\in[r]}(A(a,(x(n),b)):\mathbb C)v(\operatorname{init}x,a).
\]

Only clean-zero input columns are prescribed. Neither U's unitarity nor A's canonicality is an input here; the conclusion is exact local action, not norm preservation. All nonzero-bit input columns remain irrelevant to fresh-zero action.

### C27. `padVector`

For ANY d,B and complex v:[d]→ℂ, its value at b∈[B] is v(b.val) if b.val<d, and zero otherwise. There is NO d≤B premise in the definition. Hence this is zero extension when d≤B, but truncation when d>B. B is an arbitrary natural, not necessarily a power of two.

### C28. `padVector_active`

With premise d≤B, every a∈[d] is embedded by `Fin.castLE` without changing its numerical label, and `padVector v (castLE a)=v(a)`.

### C29. `paddedCore`

For ANY l,r,B and real A:Core l r, the complex matrix P with output `(s,b)∈[2]×[B]` and input a∈[B] is

\[
 P((s,b),a)=\begin{cases}
 (A(a,(s,b)):\mathbb C),&a<l\text{ and }b<r,\\
 0,&\text{otherwise}.
 \end{cases}
\]

Bounds l≤B and r≤B are NOT required to define it. Without them it may truncate; zeros on inactive padded input labels do not prescribe arbitrary columns of a full Stage U unless an explicit stage-column hypothesis says so.

### C30. `paddedCore_inactive_output`

For arbitrary such A, bit s, a,b∈[B], if r≤b.val then P((s,b),a)=0. No rank/canonicality or padding-size premise is needed.

### C31. `sum_padVector`

With d≤B, complex f:[B]→ℂ and v:[d]→ℂ,
`Σ_(a∈[B]) f(a)padVector(v)(a) = Σ_(a∈[d]) f(castLE a)v(a)`.
The unused padded inputs vanish. This uses ordinary multiplication, not conjugating inner product.

### C32. `sequential_step_padded`

Inputs are l≤B, real A:Core l r, complex Stage U on `[2]×[B]`, and matching columns ONLY on occupied clean inputs:
`∀s,b,a∈[l], U((s,b),(0,castLE a))=P((s,b),castLE a)`.
For ANY complex v:PrimitiveBasis n×[l]→ℂ, all x:PrimitiveBasis(n+1) and b∈[B],

\[
 \operatorname{step}\bigl(U,(p,a)\mapsto
     \operatorname{padVector}(v(p,\cdot))(a)\bigr)(x,b)
 =\operatorname{padVector}\left(c\mapsto
   \sum_{a\in[l]}(A(a,(x(n),c)):\mathbb C)v(\operatorname{init}x,a)\right)(b).
\]

There is notably NO premise r≤B, no unitarity premise, and no canonicality premise. Equality remains valid on every output b in the actual padded carrier, but when r>B the right-hand padVector truncates the next-bond vector. Thus this theorem alone is not a lossless physical embedding of every r-dimensional output. Unoccupied clean-input columns and all nonzero-bit input columns of U remain unconstrained.

### C33. `paddedCore_active_isometry`

Given l≤B, r≤B, A:Core l r with A Aᵀ=I_l, every a,c∈[l] satisfies

\[
 \sum_{s\in[2],b\in[B]}
 \overline{P((s,b),\operatorname{castLE}a)}
 P((s,b),\operatorname{castLE}c)=\delta_{a,c}.
\]

Both size premises matter for the lossless active input/output interpretation here. Only active clean columns are certified; a full unitary Stage completion, compiler and physical register embedding are not produced.

## 3. NormEnvironment module: all 15 roots

Names in this section have prefix `QuantumBlockEncoding.TensorTrainNormEnvironment`. The actual module imports Canonical and opens its namespace; it adds no ambient hypotheses.

### N1. `gram`

For ANY real chain C:Chain n l r it computes an `[l]×[l]` real matrix E_C:

\[
 E_{\mathrm{nil}\,r}=I_r,\qquad
 E_{\mathrm{cons}\,A\,C}=\sum_{s\in[2]}A_s E_C A_s^T.
\]

This is a right-to-left local matrix recursion, not construction of all word amplitudes. Its terminal environment is the full identity I_r, not a projector onto one terminal bond label. No right-canonical or normalization premise is used.

### N2. `gram_eq_sum`

For every C,

\[
 E_C=\sum_{x\in\operatorname{Word}(n)}T_C(x)T_C(x)^T.
\]

In entries, `E_C(a,c)=Σ_x Σ_(t∈[r]) T_C(x)_(a,t)T_C(x)_(c,t)`. This explicitly includes ALL words and ALL terminal labels. The theorem has no full-action or norm-supplier-correctness premise.

### N3. `gram_scalar`

For C:Chain n 1 1, `gram C 0 0 = Σ_x T_C(x)_(0,0)^2`. Both boundaries are literally dimension one; a general terminal dimension r is not silently discarded.

### N4. `gram_scalar_nonneg`

For every C:Chain n 1 1, `0≤gram C 0 0`, proved from the full sum of squares, without an extra input premise.

### N5. `norm`

For C:Chain n 1 1, `norm C = Real.sqrt(gram C 0 0)`. Mathlib's total real sqrt is nonnegative and returns zero on nonpositive inputs; here N4 proves the argument is nonnegative, so no negative-input fallback is needed to invent semantics. This definition accepts zero and unnormalized trains. It does not divide by the norm or define a normalized state.

### N6. `norm_eq`

For all scalar-boundary C, `norm C = sqrt(Σ_x T_C(x)_(0,0)^2)` exactly. The word sum is the specification, not the local recursion's evaluated data structure.

### N7. `norm_sq`

For all such C, `(norm C)^2 = Σ_x T_C(x)_(0,0)^2`. No nonzero premise is needed; N4 supplies the square-root condition inside the proof.

### N8. `norm_pos_of_nonzero`

Given C and the explicit premise `∃x, T_C(x)_(0,0)≠0`, then `0<norm C`. No positive-entry or full-rank assumption is substituted for this actual nonzero-amplitude premise.

### N9. `norm_eq_of_contract`

Given C:Chain n 1 1, a finite type I, a full equivalence `e : Word n ≃ I`, a real target:I→ℝ, and the premise `∀x, T_C(x)_(0,0)=target(e x)`, then
`norm C = sqrt(Σ_(i∈I) target(i)^2)`.

The all-word target-action equality IS a genuine input to this generic target adapter. It does not assume the norm recursion already equals the target norm, but neither does it construct cores for an arbitrary target. The equivalence is bijective onto the whole target carrier, so no omitted target sectors or duplicate-address identification are allowed.

### N10. `environmentScalars`

This natural counter is `environmentScalars(nil r)=r²` and `environmentScalars(cons A C)=l²+environmentScalars C`. For the actual dimensions it is exactly `Σ_(i=0)^n b_i²`, counting all square environments if retained, including the final identity. It is not byte usage, streaming peak space, or a proved allocation count for a runtime.

### N11. `environmentScalars_le`

For any C:Chain n l r and D∈ℕ, premise `maxBond C≤D` implies
`environmentScalars C≤(n+1)D²`. The dimension bound includes both boundaries, and the statement covers D=0. It does not charge input-core storage or output arrays of another implementation.

### N12. `updateArithmeticBudget`

For any l,m∈ℕ its EXACT definition is

\[
 U(l,m)=4(lm^2+l^2m)+l^2.
\]

The described schedule uses two bits, and per bit computes the two dense products `(l×m)(m×m)` followed by `(l×m)(m×l)`, charging one multiplication and at most one addition per inner-product term, then l² additions to combine the bits. Transposes/copies are treated as index views in this syntactic model. This is a natural polynomial counter, not a costed machine operation semantics.

### N13. `arithmeticBudget`

`arithmeticBudget(nil r)=0`; `arithmeticBudget(cons A C)=U(l,m)+arithmeticBudget C`, where m is that core's actual right-bond dimension. Thus it sums U over actual adjacent bond pairs, not padded maximal dimensions. It excludes terminal-identity initialization, data access/copying, finite-bit precision, and the FINAL square root in norm.

### N14. `updateArithmeticBudget_le`

For any l,m,D with both premises l≤D and m≤D, `U(l,m)≤9D³`. No D>0 premise is present; the proof handles D=0 separately when bounding D² by D³.

### N15. `arithmeticBudget_le`

For C:Chain n l r and D with premise maxBond C≤D, `arithmeticBudget C≤9nD³`. This is an exact bound on the DEFINED syntactic real-operation counter. There is no theorem here refining an external evaluator, proving finite-bit runtime, efficient input callbacks, quantum gate complexity, or numerical stability.

## 4. Mechanisms and degenerate dimensions

The canonicalization proof uses a small residual at each tail: first factor the tail action as S times a canonical tail, replace A_s by A_s S without mixing the emitted bit, factor that widened core, and compose its residual. Local row orthogonality then composes by finite sums to total mass preservation on Word n×[r]. The normalized existence roots use that output mass identity, not an assumed circuit or global target-action certificate.

The Gram proof independently distributes `A_s (Σ_y T_tail(y)T_tail(y)ᵀ) A_sᵀ` and uses transpose-of-product to obtain the full product for `(s,y)`. It does not require canonicality, so the norm supplier also applies to arbitrary noncanonical input cores. No general complex Hermitian Gram recursion is defined by these roots: their transpose and core scalar field are real, while complex lifting is a separate adapter.

- All natural dimensions, including zero, are valid. Identities, sums and contractions on empty carriers have ordinary empty-matrix semantics. Zero or dependent rows in input cores need no special caller certificate; dimension-based min reduction is not numerical-rank detection.
- For n=0, C is nil r with l=r; T_C(*)=I_r, chainMass(C,v)=mass(v), Gram(C)=I_r, environmentScalars(C)=r² and arithmeticBudget(C)=0. The scalar case nil1 has sole amplitude1 and norm1, not norm0.
- A zero internal bond or empty terminal dimension makes every emitted output amplitude zero; normalization hypotheses then cannot hold. General Gram matrices can be zero even when the boundary type is nonempty. No fallback nonzero normalized state is fabricated.
- An all-zero scalar-boundary nonempty chain has norm0 and satisfies norm_sq. Only norm_pos_of_nonzero excludes it. Real signs are retained; taking a norm does not imply all source amplitudes were nonnegative.
- `padVector` and `paddedCore` are total even when active dimensions exceed B. Preservation theorems add the precise needed inequalities; particularly C32 lacks r≤B, whereas C33 includes it. An arbitrary B is a finite label carrier, not a physical B-level register realization or a qubit count.
- If l=0, active-column isometry is vacuous; if r=0, a nonzero l cannot satisfy A Aᵀ=I_l. The theorems impose no false positivity convention to hide these cases. If B=0, output labels are empty; padding may discard a larger active vector unless bounds prevent it.
- In the counters, zero dimensions are included literally. U(0,m)=0; U(l,0)=l², charging the formal bit-combination additions even though products are zero. For n=0 there are no update charges, although the retained terminal environment still has r² scalar slots. Bounds with D=0 remain valid when their actual maxBond premise holds.

## 5. Binder and definition audit

Every project alias used in an input premise has been expanded above. Existence-root outputs (right canonicality, min recurrence, residual action, normalized residual boundary) must not be read as caller inputs. Conversely generic reusable implications retain their real premises: orthogonal rows in C15/C24/C33; canonicality in C17/C18; all-word matrix action in C18; mass-one hypotheses in C19/C20; local clean-column equalities in C26/C32; padding bounds exactly where displayed; nonzero scalar amplitude in N8; target-action equality AND a full carrier equivalence in N9; dimension bounds in N11/N14/N15. None is silently omitted or upgraded to a construction.

Pure natural parameters, finite index types, Fintype instances, dependent chain shapes and the explicit `DecidableEq I` for the identity in C15 are type/formation data. No external-source SOURCE/STANDING/EXCESS classification is inferred because the external natural-language source is withheld. Public definitions are literal finite functions, recursive matrices, logical shape relations or natural counters. Existence of nonunique orthonormal completions is not falsely reclassified as uniqueness/canonical representatives. `padVector`'s zero values are explicitly part of its public carrier semantics; no claim it is a lossless embedding without bounds is made.

## 6. Seven quantum semantic slots

| Slot | Exact certified interface and boundary |
|---|---|
| Target/normalization | Real chain contraction on all Word n×[r], squared boundary/output masses, scalar-boundary norm. Canonicalized data exist; unit mass is required only in the normalized existence roots. No arbitrary-target cores, prepared state or density operator is supplied. |
| Dimensions/scalar/basis/order | All natural dimensions including zero, core rows left bond and columns physical-bit/right-bond; exact real→complex transposition lift. Sequential basis is Fin n→Fin2 with new bit at last wire. Prefix-padding preserves numerical labels under bounds. No whole-chain Word/PrimitiveBasis or qubit register embedding is silently assumed. |
| Oracle/access/inverse/control | Mathematical core functions and arbitrary local Stage matrices; no coherent parameter oracle, inverse, control implementation, lookup/storage contract, or input-evaluation cost certificate. |
| Ancilla/workspace/cleanup | The local step introduces a fresh zero bit and leaves prior prefix passive. Matching occupied clean-input columns yields exact output including inactive padded labels. Unoccupied/nonzero-bit columns stay unconstrained. General terminal r remains present; these roots do not construct a full unitary completion or prove an entire physical run with cleaned ancillas. |
| Phase/sign | Exact signed real contractions embed into complex amplitudes; arbitrary complex prefix states are allowed in local adapters. Complex isometry uses conjugation correctly. No equality merely up to phase, phase quotient or probability-only replacement is used; no general complex-core canonicalization theorem is claimed. |
| Norm/error/success | Exact all-word/all-terminal sums; scalar nonnegativity and square-root identity including zero trains. No approximation tolerance, rounding error, postselection probability, failure confidence or amplification contract. |
| Resources/physical costs | Actual bond maxima; retained environment scalar slots; and an explicitly defined exact-real dense-operation budget. These are not byte counts, wall time, finite-bit complexity, norm-square-root cost, numerical conditioning, physical qubits, gates, depth, connectivity, noise, circuit synthesis or readout cost. |

## 7. Scope and handoff evidence

`formal-input-seal.json` records actual source/configuration/protocol digests, precise full/partial read extents, the actual namespace/scopes/imports, all48 source-root headers and the extra instance, plus the prior formal-only exposure. Both target sources and ThinLQ, SequentialBondPreparation, RealAmplitudePreparation were re-read fully. PrimitiveSemantics' actual basis definition, Mathlib's finite product equivalence, real sqrt and classical Gram–Schmidt basis-completion definitions were read at the sealed extents. Other transitive project/Mathlib source is inherited formal context, not an exhaustive fresh source audit.

Canonical imports exactly ThinLQ and SequentialBondPreparation. NormEnvironment imports exactly Canonical. Both use scoped BigOperators; NormEnvironment additionally opens TensorTrainCanonical. Neither target has a global hypothesis block. The standalone named instance for Word's finite enumeration is explicitly accounted for rather than hiding it behind the requested count.

The initial source seal is separate from eventual author-packet/opaque metadata. Compiler outcome, actual fresh-object digests, inherited-provider boundary, exact commands/diagnostics and complete signature/axiom output are recorded in the accompanying evidence/probe artifacts. Private setup/command artifacts contain local paths and must not be published verbatim. Fresh source checking is not claimed merely because a cached target exists.

### Actual bounded compiler results

Both actual target sources were newly compiled with the direct Lean4.33.0 compiler (`x86_64-w64-windows-gnu`, commit `d8b18978322de05a8f3dba51ef03cf5461676c17`, Release), `-j 1 -M 3072`, one after the other. Both exited0 with EMPTY diagnostics. NormEnvironment's `--setup importArts` explicitly points to this run's fresh Canonical object. No dependency was rebuilt and no inherited cache was written. Produced objects:

```text
fresh/QuantumBlockEncoding/TensorTrainCanonical.olean
b1b78e21793e7fdf1a966996d19efc3cacc44d0163af5336437bf3e49b6c6cc9

fresh/QuantumBlockEncoding/TensorTrainNormEnvironment.olean
dd28a6b215d444045d040b240c5f32225d0cd895b491a2a66998cd44e36a48ac
```

Two subsequent serial probes both exited0: Canonical checks its33 non-instance roots plus wordFintype; Norm checks its15 roots. Probes use full names, explicit arguments and universes. The Canonical probe's setup maps Canonical to its fresh object; the Norm probe's setup maps BOTH targets to their fresh objects. Thus neither uses an old cached target as evidence of freshly checked target source. All49 `#check` outputs and all49 ordinary axiom censuses are retained completely in the two probe-output files. Only `Word` and `updateArithmeticBudget` have no axioms; the remaining47 named declarations list exactly `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorryAx` or extra project axiom in these root censuses. This does not audit unused declarations in every imported dependency.

The four proof commands total two source compiles plus two probes, with no retry; one additional compiler call only printed the runtime version. Actual total process time and per-worker token usage were not measured. Normal project/provider and manifest-package caches are inherited and not rechecked at trust0. Direct ThinLQ/SequentialBondPreparation olean hashes and all sealed input hashes were revalidated unchanged when these bounded gates ended. The parent was then notified that no Lean process remained; later parent integration gates are not this decoder's evidence.

Public command forms use only location placeholders:

```text
LEAN -j 1 -M 3072 --root REPO -o SCRATCH/fresh/QuantumBlockEncoding/TensorTrainCanonical.olean REPO/QuantumBlockEncoding/TensorTrainCanonical.lean
LEAN -j 1 -M 3072 --setup NormCompileSetup.private.json --root REPO -o SCRATCH/fresh/QuantumBlockEncoding/TensorTrainNormEnvironment.olean REPO/QuantumBlockEncoding/TensorTrainNormEnvironment.lean
LEAN -j 1 -M 3072 --setup ProbeCanonicalSetup.private.json ProbeCanonical.lean
LEAN -j 1 -M 3072 --setup ProbeNormSetup.private.json ProbeNorm.lean
```

The LEAN_PATH recipe is the normal project build root followed by all actual manifest package build roots in manifest order; it does not prepend a sparse fresh namespace directory. Exact expanded local commands/setup remain PRIVATE. Final bounded failure class is `NONE`; full repository and publication/source-comparison gates remain NOT_RUN. There were no proof failures to turn into mathematical refutations.

Objective/frontier: independent whole-module formal decoding of these two dependent modules. Mathematical delta: explicit full carriers and all logical/type premises, rank versus dimension, real/complex orientation, padding versus truncation, Gram/terminal semantics, and counter versus physical-runtime distinctions. No mathematical route is rejected, no source agreement or publication verdict is supplied. No subagents, production/Git/cache edits or changes to previous decoder artifacts were made. Source-dependency-audit process instructions were inspected, but their external paper-reading workflow was not used under the formal-only boundary. No curated mathematical process-memory records, alternative-route comparator, purification or Exposition Seal are claimed. Parent owns packet assembly, registry, source comparison, full repository gates and Git integration. This bounded decoder does not run or claim full `lake build`, Tests, transitive fresh rebuild, trust0 recheck, website or publication gates.
