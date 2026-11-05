# Independent whole-module formal reconstruction, decoder c24

Direction: `CTT_WHOLE_MODULE_FORMAL_RECONSTRUCTION`.
Opaque binding: `9be3c975b10363ad36778d6dc9da4c7a941857f6571f3e2f6072c73d65a51c09`.
Packet SHA-256: `48d4fed3a31e56033467a47631d6c4bdbef8858ea147ca12a2a892289e44d8cd`.
Target: `QuantumBlockEncoding/ConstructiveTensorTrain.lean`.
Target SHA-256: `081e409bd31b91513ab38ad1041bd7dbcad88675275ba4197ae3587686c1d58d`.

This is a reconstruction from the formal interface and actual formal source, not a comparison with any external mathematical source. No source-agreement, publication, novelty, or independent-review verdict is issued. No authored lesson, proposed source metadata, graph proposal, publication candidate, previous decoder report, reviewer artifact, or verdict was read. The opaque binding was preserved, not recomputed. There were no subagents and no production or Git writes.

## 1. Ambient objects, expanded

Write `[d]={0,...,d-1}` for `Fin d`, including the empty set `[0]`. A real matrix with row set I and column set J is a function `I → J → ℝ`. Products use finite sums, transposition does not conjugate, and identity matrices have Kronecker-delta entries. No nonzero-dimension or full-rank convention is implicit.

A `Core l r` is a real matrix on `[l] × ({0,1} × [r])`. Its entry is written `A(a,(s,b))`. Its bit-slice is the matrix

\[
 A_s(a,b)=A(a,(s,b)).
\]

A `Chain n l r` is a dependently indexed sequence of n such cores. The constructors are an empty chain `nil r : Chain 0 r r`, and `cons A C : Chain (n+1) l r` for `A : Core l m` and `C : Chain n m r`. Thus the terminal bond is retained, and an empty chain necessarily has equal initial and terminal dimensions. For an explicit chain denote its bond dimensions by `b_0=l,...,b_n=r`, and its cores by `A_i : Core b_i b_(i+1)`.

`Word 0 = Unit`; `Word (n+1) = Fin 2 × Word n`. A word is therefore an ordered list `(s_0,...,s_(n-1))`, with the first core emitting the first component. There is one empty word. The target module has no flat integer indexing of complete words and no wire-placement equivalence of its own.

`contract C x`, written `T_C(x)`, is an `[l] × [r]` matrix:

\[
 T_{\mathrm{nil}\,r}(*)=I_r,\qquad
 T_{\mathrm{cons}\,A\,C}(s,y)=A_sT_C(y).
\]

Equivalently it is the product of the slices in core order. With an initial row boundary `v:[l]→ℝ`, the amplitude at the FULL output label `(x,t)∈Word n × [r]` is

\[
 f_{C,v}(x,t)=\sum_{a\in[l]}v(a)T_C(x)_{a,t}.
\]

This terminal coordinate is not optional: for general r the output is not merely an n-bit scalar amplitude table.

`RightCanonical C` means `True` for an empty chain and, recursively, both `A Aᵀ=I_l` and right-canonicality of the tail for a nonempty chain. In entries, every core satisfies

\[
 \sum_{s=0}^1\sum_{b\in[m]} A(a,(s,b))A(c,(s,b))=\delta_{a,c}.
\]

These are orthonormal ROWS, or columns after transposing to output-row/input-column state-map convention. They do not assert that a general rectangular core is a square unitary.

`RankReduced C D` is an inductive relation on actual chains, not a matrix-rank predicate. Its empty constructor relates `nil r` to itself. Its nonempty constructor relates `cons A C` to `cons Q D` whenever `RankReduced C D` and the tail D starts in dimension m', with `Q : Core (min l (2*m')) m'`. Thus, for the original dimensions b_i, the new dimensions d_i obey exactly

\[
 d_n=r,\qquad d_i=\min(b_i,2d_{i+1})\quad(i=n-1,...,0).
\]

The relation itself does not impose equations on core entries or certify equality of contractions. Those are separate fields of the returned result. In particular d_i is not asserted to equal an algebraic or Schmidt rank; it depends on dimensions, not on whether entries vanish or are linearly dependent.

`absorb A S` multiplies a residual into only the right-bond coordinate:

\[
 \operatorname{absorb}(A,S)(a,(s,c))
 =\sum_{b\in[m]}A(a,(s,b))S(b,c).
\]

Its s-slice is `A_s S`; it does not mix bit labels.

For any finite real vector w, `mass w = Σ_i w(i)^2`. Therefore

\[
 \operatorname{chainMass}(C,v)
 =\sum_{x\in Word\ n}\sum_{t\in[r]}f_{C,v}(x,t)^2.
\]

`maxBond` is the maximum of all actual bond dimensions INCLUDING both boundaries: `maxBond(nil r)=r` and `maxBond(cons A C)=max(l,maxBond C)`.

## 2. All 15 public declarations

All names below have prefix `QuantumBlockEncoding.ConstructiveTensorTrain`. All natural-number parameters are universally quantified unless bound as input to the structure. Matrices and boundaries are arbitrary real-valued functions of the displayed finite labels.

### 1. `CoreFactorization`

For `A : Core l r`, set `q=min(l,2r)`. This is the data type of quadruples `(R,Q,hA,hQ)` with

\[
 R\in\mathbb R^{[l]\times[q]},\quad
 Q\in\mathbb R^{[q]\times(\{0,1\}\times[r])},\quad
 A=RQ,\quad QQ^T=I_q.
\]

In particular `A(a,(s,b))=Σ_k R(a,k)Q(k,(s,b))`. Factorization and orthogonality are proof FIELDS of an inhabitant. They are not preconditions for a user calling `factorCore`.

### 2. `factorCore`

For every l,r,A, this noncomputable definition returns a particular `CoreFactorization A`. It flattens the product column label by the explicit equivalence

\[
 e(s,b)=b+r s\in[2r],
\]

applies `ConstructiveThinLQ.factor` to `B(a,j)=A(a,e⁻¹(j))`, and returns its R and `Q(k,(s,b))=Q_flat(k,e(s,b))`. This is bit-major block indexing for this local flattening, not an asserted global little-endian word encoding.

Expanding the actual supplier: if `l≤2r`, it performs rectangular adjacent-row elimination on `Bᵀ`. If H is the accumulated orthogonal transform and `E=H Bᵀ` the upper-trapezoidal residual, the returned factors are `R(i,k)=E(k,i)` and `Q_flat(k,j)=H(k,j)` for `k∈[l]`. If `l>2r`, it returns `R=B` and `Q_flat=I_(2r)`. The equality case follows the first branch.

The elimination processes columns in increasing order; each existing pivot gets a bottom-up adjacent-row sweep using the changing matrix. For a pair (x,y), let `ρ=√(x²+y²)`. Its preparation angle is zero if ρ=0, otherwise `2*(-arccos(x/ρ))` when y<0, and `2*arccos(x/ρ)` otherwise. Elimination uses the negative of that angle and the real plane with entries `cos(θ/2), -sin(θ/2), sin(θ/2), cos(θ/2)`. Zero pairs produce identity rotations. This fixes an actual exact-real recurrence, not arbitrary existential factor selection. It does not establish uniqueness among all valid factorizations, numerical computability, or a cost bound.

### 3. `Result`

For an input `C : Chain n l r`, this is the data type of six fields:

\[
 k\in\mathbb N,\quad S\in\mathbb R^{[l]\times[k]},\quad
 D : \operatorname{Chain}(n,k,r),
\]

together with `RightCanonical D`, `RankReduced C D`, and the proof `∀x∈Word n, T_C(x)=S T_D(x)`. The named fields are `rank`, `residual`, `canonical`, `rightCanonical`, `rankReduced`, and `action`, in that order. The last three are OUTPUT proofs. The structure contains actual chain and residual data, not only a proposition saying that some data exist.

### 4. `canonicalize`

For every input chain C, this noncomputable recursive definition returns `Result C`, with no canonicality, normalization, full-rank, nonzero, or state-action input premise.

For `nil r` it returns `(r,I_r,nil r)` and their proofs. For `cons A C_tail`, first canonicalize the actual tail, obtaining `(m',S_tail,D_tail)`. Factor the absorbed core `absorb A S_tail` by `factorCore`, obtaining `(R,Q)`. Return

\[
 k=\min(l,2m'),\quad S=R,\quad D=\operatorname{cons}(Q,D_{tail}).
\]

The recursion is from the terminal bond backward. The all-word equality follows because `A_s T_tail(y)=A_s S_tail T_Dtail(y)=R Q_s T_Dtail(y)`. Thus every contraction matrix, every initial boundary, and every terminal coordinate are covered at once.

For declarations 5–12, fix the particular output `(k,S,D)=canonicalize C`.

### 5. `canonicalize_rightCanonical`

For every n,l,r,C, D has orthonormal rows at every core, exactly as expanded in Section 1. This extracts the returned proof, not an extra premise.

### 6. `canonicalize_rankReduced`

For every n,l,r,C, `RankReduced C D`; equivalently the actual output dimensions follow the exact backward-min recurrence with unchanged terminal bond. No numerical-rank minimality follows from the name.

### 7. `canonicalize_action`

For every C and every x,

\[
 T_C(x)_{a,t}=\sum_{j\in[k]}S(a,j)T_D(x)_{j,t}
 \quad(a\in[l],\ t\in[r]).
\]

This is entrywise exact real matrix equality, not equality only of norms, probabilities, one accepted branch, or one selected boundary.

### 8. `canonicalize_maxBond_le`

`maxBond D ≤ maxBond C`, with both initial and terminal boundaries included in each maximum. The proof comes from the dimension relation. There is no gate, runtime, storage, or qubit-count conclusion in this statement.

### 9. `boundary`

For every C and arbitrary `v:[l]→ℝ`, this returns the vector `u:[k]→ℝ` defined by

\[
 u(j)=\sum_{a\in[l]}v(a)S(a,j).
\]

It is a row-vector/matrix product, not S times a column v. No normalization is required to define u.

### 10. `boundary_action`

For every C,v,x the row vectors on `[r]` agree:

\[
 \sum_{a\in[l]}v(a)T_C(x)_{a,t}
 =\sum_{j\in[k]}u(j)T_D(x)_{j,t}\quad\text{for EVERY }t\in[r].
\]

Hence this preserves the amplitude on the whole output carrier `Word n × Fin r`, including all terminal sectors.

### 11. `boundary_mass`

For every C and v, with no normalization premise,

\[
 \sum_{x\in Word\ n}\sum_{t\in[r]}
   \left(\sum_{a\in[l]}v(a)T_C(x)_{a,t}\right)^2
 =\sum_{j\in[k]}u(j)^2.
\]

This is not the assertion `mass v = mass u` for an arbitrary noncanonical input chain. It identifies the original emitted-output mass with the mass of the transformed initial boundary.

### 12. `boundary_normalized`

For every C,v, the SINGLE logical premise is that the left side of the preceding equation equals one. The conclusion is `Σ_j u(j)^2=1`. There is no rescaling step: a normalized input output-table already produces a normalized residual boundary.

### 13. `stateBoundary`

For every n and `C : Chain n 1 1`, return `u=boundary C (a↦1)`. Thus `u(j)=S(0,j)`. This is defined even for an unnormalized, zero, or signed scalar-boundary amplitude table.

### 14. `stateBoundary_action`

For every `C : Chain n 1 1` and x,

\[
 T_C(x)_{0,0}=\sum_{j\in[k]}\operatorname{stateBoundary}(C)(j)T_D(x)_{j,0}.
\]

The right bond is dimension one in this specialization; this is why a single scalar amplitude per word suffices here. No global target-state equality is assumed.

### 15. `stateBoundary_normalized`

For every `C : Chain n 1 1`, if `Σ_(x∈Word n) T_C(x)_(0,0)^2=1`, then `Σ_(j∈[k]) stateBoundary(C)(j)^2=1`. This is the other, and only other, target declaration with a logical input premise. Signs remain intact.

## 3. Why the mass proof covers the full carrier

For any matrix A with orthonormal rows and any row vector w,

\[
 \sum_{s,b}\left(\sum_a w(a)A(a,(s,b))\right)^2
 =\sum_{a,c}w(a)w(c)\delta_{a,c}=\sum_a w(a)^2.
\]

Induct over all cores, summing over each emitted bit and then EVERY final bond label. This gives `chainMass D u = mass u`. Apply exact all-word action to obtain `chainMass C v = chainMass D u`. These are the actual imported `chainMass_eq` and `residual_mass` mechanisms used by the target. The proof does not discard a garbage sector, normalize conditionally on a measurement, or infer amplitude equality from mass equality.

## 4. Degenerate cases and public-carrier boundaries

All dimensions are arbitrary naturals. No `NeZero`, positivity, independence, nonsingularity, or nonzero-pivot assumption is supplied by a caller.

- If l=0 or r=0 in `factorCore`, q=0; the appropriate factors have empty rows or columns, identities are empty identities where appropriate, and the equations use empty sums. No nonexistent index is chosen.
- Deficient or identically zero cores still get q=min(l,2r) rows in Q. If q>0 the orthonormal rows do not disappear just because A has numerical rank zero. A zero residual can carry all the zero amplitude information.
- For an empty chain C=nil r, n=0 and l=r. The output is precisely k=r, S=I_r, D=nil r, boundary v=v. `chainMass C v=mass v`; no emitted-bit sum is missing, because `Word 0` is a singleton.
- For `Chain 0 1 1`, the only input chain is nil 1, its sole scalar contraction is 1, and its state boundary has sole entry 1. This includes the zero-bit specialization of the state declarations.
- A zero internal bond in a nonempty chain forces every full contraction amplitude to zero. The backward-min recurrence propagates a zero active dimension to the initial boundary. Empty output terminal dimension r=0 likewise makes the complete output mass zero. Such inputs are permitted, but cannot satisfy a mass-equals-one premise. The normalized results do not invent a nonzero fallback state.
- A terminal bond of dimension r>1 is unchanged, not proved clean or discarded. Its labels need not be a power-of-two register. No assertion about padding into physical qubits is made by these 15 declarations.

## 5. Seven quantum semantic slots

| Slot | Exact reconstructed content and boundary |
|---|---|
| Target and normalization | Arbitrary finite real core chains; full amplitudes on `Word n × Fin r`. Scalar n-bit state specialization only for l=r=1. Unit mass is assumed only in the two normalized theorems; not in construction. |
| Dimensions, scalar, basis, order | Natural dimensions, including zero; real matrices. Core columns `(bit,right-bond)`, local flattening `b+r*bit`; word/core order is recursive head first. The target establishes no global integer basis or physical wire embedding. |
| Oracle/access/inverse/control | Inputs are entire mathematical matrix functions and a chain. No oracle contract, coherent parameter-label interface, inverse oracle, controlled implementation, sampling access, or input-evaluation cost is specified. |
| Ancillas/workspace/cleanup | No physical register construction, clean ancilla allocation, dirty workspace protocol, overwritten-register action, or garbage-uncomputation theorem. General terminal bond remains present in the output. |
| Phase | Equality is exact signed REAL amplitude equality, stronger than probability equality and not modulo global phase. There is no complex input family, coherent phase between external labels, or phase-quotient construction in the target. |
| Error/probability/success | Exact identities, no tolerance parameter. Mass is the total sum of squared real amplitudes across every output label. No measurement branch, confidence bound, postselection probability, or amplification guarantee is specified. |
| Resources and physical implementation | Only maximum bond dimension is bounded here. The exact-real supplier uses arithmetic, comparisons, sqrt/arccos/trigonometry; no certified evaluation algorithm/time, stored-input model, copying cost, finite-bit precision, gate list, RY/CX/Clifford+T count, depth, connectivity, compilation, noise, query-construction, or readout cost is certified. Imported circuit theorems for other definitions do not confer these guarantees on this producer. |

`noncomputable` is a Lean evaluation marker, not by itself an impossibility or inefficiency theorem. Conversely, the presence of a specified recurrence does not prove an efficient implementation. Its exact evaluation and stored/costed refinements remain outside these statements.

## 6. Input binders versus supplied proofs

`CoreFactorization` and `Result` are ordinary data structures with certificate fields, not hypotheses bundles silently required of the original input. `factorCore` takes only dimensions and A; `canonicalize` takes only dimensions and C. `boundary` adds v; action theorems add a word x. The normalized theorems alone add the displayed mass-one equation. The scalar-boundary theorems restrict types to initial and terminal dimension one, rather than accepting a proof that a general final bond is clean.

No source hypothesis classification is inferred because the external source is withheld. At the actual formal interface, canonicality, residual factorization, exact global action and rank reduction are delivered as evidence, not assumed. The mathematical definition audit here is literal recurrence plus certified output data; neither uniqueness of the possible canonical decomposition nor a quotient-independent representative is claimed.

## 7. Exact formal context actually read

The process instructions read in full were `AGENTS.md`, `HARNESS.md`, `.agents/skills/qbe-substantive-worker/SKILL.md`, and its required `docs/theorem-publication-protocol.md`, `docs/proof-digestion-protocol.md`, `docs/evidence-routed-memory-protocol.md`. No curated mathematical process-memory file was consulted, because the task restricts mathematical evidence to the sealed formal context.

The packet and its designated `reviews/publication/constructive-tensor-train/author-formal-context.json` were parsed; all declaration entries, file inventory, ambient snapshot sources, scopes, upstream equivalence, and context-status fields were inspected. Long combined display results were truncated initially; the missing formal source was subsequently read from the actual matching files in bounded pieces. Each of the following eight actual source files was read in full and compared to its snapshot's complete text, with equality and SHA-256 matches for all eight:

1. `QuantumBlockEncoding/ConstructiveTensorTrain.lean`
2. `QuantumBlockEncoding/ConstructiveThinLQ.lean`
3. `QuantumBlockEncoding/TensorTrainCanonical.lean`
4. `QuantumBlockEncoding/RectangularGivens.lean`
5. `QuantumBlockEncoding/ThinLQ.lean`
6. `QuantumBlockEncoding/AdjacentGivens.lean`
7. `QuantumBlockEncoding/SequentialBondPreparation.lean`
8. `QuantumBlockEncoding/RealAmplitudePreparation.lean`

Actual `lean-toolchain`, `lake-manifest.json`, and `lakefile.lean` were read in full. The two target imports are exactly `QuantumBlockEncoding.ConstructiveThinLQ` and `QuantumBlockEncoding.TensorTrainCanonical`. The target namespace is `QuantumBlockEncoding.ConstructiveTensorTrain`, it opens scoped `BigOperators` and namespace `TensorTrainCanonical`, and there is no ambient `variable` or hypothesis block. Provider scopes and variables were read from their actual source, not inferred from names.

The actual Mathlib definition `finProdFinEquiv` and its adjacent proof body were read at `.lake/packages/mathlib/Mathlib/Logic/Equiv/Fin/Basic.lean:332` (through line 356); its whole-file digest matches the snapshot. Other Mathlib and transitive project source was NOT exhaustively read. Those imported modules remain inherited provider dependencies rather than newly source-audited declarations.

For executing an explicit artifact-map probe, compiler tooling source was read at `toolchain:src/lean/Lean/Setup.lean` lines 61–245 and `toolchain:src/lean/Lean/Data/Json/FromToJson/Basic.lean` lines 186–210. These reads establish how `--setup` resolves `importArts`, not additional mathematical assumptions. Runtime version/help, tool-path discovery, relevant cache-presence/directory metadata and file hashes were inspected. Unrelated cache contents were not opened. Hashes and precise read extents are recorded in `evidence.json`.

## 8. Compiler evidence and complete bounded diagnostic outcomes

Toolchain file: `leanprover/lean4:v4.33.0`. Executed compiler: Lean 4.33.0, `x86_64-w64-windows-gnu`, commit `d8b18978322de05a8f3dba51ef03cf5461676c17`, Release. Mathlib is manifest-pinned at `db584cd6d46c92f209a44c0f1c829460d327499d`. The manifest and Lake configuration hashes match the packet.

For reproducibility, use REPO for the checkout, SCRATCH for this decoder's own output directory, and LEAN for that toolchain's direct compiler. The exact expanded local command strings are private; public commands below differ only by those location aliases. LEAN_PATH was the normal project build root followed by the build roots for every package in the actual manifest, in manifest order.

Successful fresh target command:

```text
LEAN -j 2 --root REPO -o SCRATCH/fresh/QuantumBlockEncoding/ConstructiveTensorTrain.olean REPO/QuantumBlockEncoding/ConstructiveTensorTrain.lean
```

This read the ACTUAL target source, not a copy or cached-target import. It exited 0 with empty stdout/stderr. Its produced olean has SHA-256 `5ccedd5a7fb6b74a970823e31423cf8ec13f93279edf37f2f23620cfa9b6fb12`. Imported project/package oleans were inherited caches, not freshly rebuilt or rechecked at trust level zero. The pre-existing target olean was not used as the evidence for this source compilation.

Successful signature/axiom command:

```text
LEAN -j 2 --setup ProbeSetup.private.json Probe.lean
```

The setup explicitly maps module `QuantumBlockEncoding.ConstructiveTensorTrain` to the fresh olean just produced. Other imports use inherited provider caches. The probe exited 0, emitted 15 `#check @...` signatures, 15 `#print axioms` censuses, and expanded prints of both structures. Complete untruncated output is frozen in `probe-output.txt`; the exact probe source is `Probe.lean`.

All 15 declarations reported EXACTLY the same ordinary axiom set: `propext`, `Classical.choice`, `Quot.sound` (universe annotations shown in the raw output). There was no `sorryAx` or extra project axiom in these censuses. This is the compiler's transitive census for these roots, not a statement that every declaration in every imported module was audited.

Earlier diagnostics, retained rather than hidden:

- A read attempted `lakefile.toml`; that file was absent. The actual configuration is `lakefile.lean`, subsequently read and hash-matched.
- `lean --version` through the launcher exited 0 but warned twice that the checkout path could not be canonicalized. The direct compiler was then used; the successful source/probe commands had no such warning.
- A combined environment-discovery command exited 1 because WSL was unavailable (its localized output was encoding-garbled). WSL was not used for any evidence, and no installation or environment modification followed.
- The first fresh-target attempt put the sparse fresh output root first in LEAN_PATH. It exited 1 at the import header: `ConstructiveThinLQ.olean` was absent under that sparse root. Retrying with only the normal provider roots compiled the actual target successfully. This was a search-path execution failure, not a target theorem failure; no cache was modified to cure it.
- The first probe setup omitted a required JSON field and exited 1: `Lean.ModuleSetup.isModule: Bool expected`. The setup was completed with explicit package/import defaults, false `isModule`, and empty plugin/dynlib/options fields. The second probe exited 0. This was an artifact-map configuration error, not a proof or source mismatch.

No `lake build`, `lake build Tests`, whole-repository CI, publication checker, or website gate was run by this decoder. No outside-sandbox compiler write was needed, no scoped escalation was requested, and no permission failure was worked around. The bounded target/source gate succeeded; the inherited-cache/source-equality boundary remains explicit.

## 9. Handoff and residual boundary

Objective/frontier: independent whole-module formal decoding of the bound 15 declarations. Mathematical delta: the exact dimensions, actual returned data, complete output carrier, proof/input separation, and all degenerate cases are exposed above. Named evidence: the actual bound source, formal provider definitions, fresh-target compilation and independently invoked signature/ordinary-axiom probe. Files changed: only this decoder's own scratch artifacts. No production, registry or Git integration was performed.

Failure class at handoff: `NONE` for the bounded reconstruction and successful source/probe commands. Resolved diagnostic attempts were environmental/configuration execution failures, with no negative mathematical consequence; no unresolved `ENV_BLOCKED` condition remains for this bounded task. Full dependency rebuild and repository/publication gates are NOT_RUN, not passed by this report. There are no promoted fragments from a rejected mathematical route, and no mathematical route was retired.

Process-memory IDs: none. Direction fingerprint: source-blind complete formal-module expansion, independent of migration-minimal-delta or source-agreement audits. Expected information gain: distinguish exact certified tensor-chain algebra from numerical-rank, circuit, cleanup and resource interpretations not present in the interface. Parallel admission/common-blind-spot/comparator: not applicable; one decoder, one formal reconstruction, no alternate construction selection. Purification/Exposition Seal: no integration or seal claimed. The reconstruction preserves bit/core order, signs, terminal sectors, assumptions, exact mass, and the unproved physical/resource boundary.

Residual risk: imported provider caches were inherited and not freshly rebuilt from every transitive source; external source meaning was intentionally withheld. A distinct reviewer can compare this frozen reconstruction against the pinned external source without any verdict from this decoder. Parent owns canonical registry and Git actions. Hashes are frozen separately in `evidence.json` and `freeze.json` to avoid circular self-digests.
