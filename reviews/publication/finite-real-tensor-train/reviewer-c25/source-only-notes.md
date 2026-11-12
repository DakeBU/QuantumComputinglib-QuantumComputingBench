# TTC/NORM: independent source-only review, phase 1

Status: SOURCE_ONLY_FROZEN; no formal equivalence verdict.
Direction fingerprint: `TTC_NORM_SOURCE_FULL_CARRIER_LOCAL_COLUMN_AND_SYNTACTIC_COST_BOUNDARY`.

## Evidence and blindness

The sole mathematical input was the private execution file named
`finite-real-tt-source-only.txt`, read completely as UTF-8, lines 1–160.
Its original-byte SHA256 is
`895ec97fe7e95146ec8d374bdcbecf4edbf40ff7e787135d032e376841d773b7`
(13,531 bytes). This basename is an evidence identifier, not a claim that a
public bundle was read. No public source URL or external paper was supplied.
The source describes itself as retrospective local exposition. The task says
another author-curator assembled it after existing material; the historical
formalizer is UNKNOWN. Neither pre-proof chronology, independent authorship
relative to the historic formalizer, novelty, nor external-paper fidelity is
established by this review.

The applicable repository AGENTS/HARNESS, both requested skills, and all three
requested protocols were read before the mathematical source. Initial combined
instruction outputs were truncated; subsequent reads recovered the full
instruction text, including HARNESS lines 76–150. No instruction file was used
as mathematical evidence. General frontier, process-memory, implementation
search, build and publication-ledger requirements were deferred where they
would violate the explicit phase-1 blind boundary. This is not a Lean Proof
Seal or publication admission.

I did not read Lean implementation, formal ambient definitions, declaration
inventory, candidates, coverage maps, author coverage JSON, review-batch files,
other decoder/reviewer packets, or existing mathematical graphs. No Lean,
Git operation, cache write, simulator or sub-agent was run. The parent's
reported commits were context only, not independently verified here.

## Reconstructed mathematical contract

All dimensions are natural numbers, including zero. Bond label `[d]` is the
finite numeric prefix. Scalars in cores, residuals, contractions and
environments are real. Complex numbers enter only the local column interfaces.
A core `A : [l] × {0,1} × [r] -> R` is flattened with rows `[l]` and columns
`{0,1} × [r]`. Its bit slice is `l × r`. The recursive word carrier has one
empty word and front-cons bits; no physical endian identification is made.
An empty chain has equal boundary bonds and contraction `I_r`; a cons chain
contracts as `A(b) M_tail(y)`. Every initial row and terminal column survives.

Right canonical means `Q Q^T = I` for each flattened core. It is not column
orthogonality. `B(C)` includes both boundaries. The following are separate
results, not convenient premises of one all-purpose theorem:

1. **Absorption / thin existence (S2).** Absorb an `m × s` residual by
   `A'(a,b,c)=sum_j A(a,b,j)S(j,c)`. For arbitrary `l × 2r` real `A`, set
   `s=min(l,2r)` and obtain `A=RQ`, `R:l×s`, `Q:s×2r`, `QQ^T=I_s`.
   Extend the row span to `s` orthonormal rows if `l<=2r`; if `l>2r`,
   `R=A,Q=I_(2r)` works. Rank deficiency does not shrink the prescribed
   carrier. Flattening `e(b,j)=br+j` is bijective even when both sides are
   empty at `r=0`; an inverse is never evaluated at a nonexistent label.
   Factor choice is nonunique. This is neither a uniquely characterized
   factor nor a deterministic algorithm with a cost bound.

2. **Tail-first construction (S3).** On an empty chain return `(I_r,empty)`.
   Given tail `M_T=S M_E`, factor the absorbed head `A(b)S=R Q(b)` and
   prepend `Q`. Thus `M_C(b,y)=R Q(b)M_E(y)` on every word. The new bonds
   satisfy `s_n=d_n`, `s_i=min(d_i,2s_(i+1))`. This dimension relation alone
   implies all new bonds are no larger, each nonempty head is at most twice
   its new tail, the scalar-terminal one-site bound is two, and
   `B(D)<=B(C)`. It does not itself assert numerical factorization.

3. **Full mass (S3).** `mass(z)=sum_j z_j^2` and
   `Phi_C(v)=sum_x sum_j (v M_C(x))_j^2`. Orthogonal-row flattened `Q`
   satisfies `mass(vQ)=mass(v)`. Induction gives
   `Phi_D(v)=sum_b Phi_tail(vQ(b))=sum_b mass(vQ(b))=mass(v)`.
   Consequently all-word factorization AND canonicality give
   `Phi_C(v)=mass(vR)`. With scalar terminal and unit full mass this produces
   a normalized residual row. With both original boundaries one, `u=(1)R`
   has unit mass and exactly reconstructs each signed scalar amplitude.
   Normalization is derived, not assumed as a new factorization premise.

4. **Real-to-complex local columns (S4).** Transposing roles gives
   `V((b,j),a)=A(a,b,j)` in `C`, so real row orthogonality yields
   `V*V=I_l`. For equal bonds `l=r`, a square `U` on `{0,1}×[r]`
   satisfying its fresh-zero input-column equations acts on an arbitrary
   passive-prefix amplitude family as
   `sum_a A(a,x_k,j)v(x^-,a)`. This needs the column equations but not
   unitarity or canonicality. A fresh bit is appended at the highest wire;
   the recursive chain emits its first bit at the head. Their global
   correspondence has not been proved. Unspecified columns remain free.

5. **Active prefix / padding (S5).** `P_d^B` is zero fill when `d<=B`
   and only restriction otherwise. The active-prefix summation identity
   needs `d<=B`. The padded coefficient table is zero unless `a<l,j<r`.
   A local square `U` must match this table on all physical output rows but
   only the fresh-zero active input columns. From `l<=B`, input zero-fill
   and these equations, the output equals `P_r^B w`, including zero for
   physical `j>=r`. This equality does NOT require `r<=B`; losslessness on
   the entire outgoing bond does. Active-column orthonormality requires
   BOTH `l<=B` AND `r<=B` AND real row orthogonality. No zero constraint is
   imposed on all unused columns of a unitary completion.

6. **Gram norm (S6).** For every real chain, independently of canonicality,
   `E_empty=I_r` and `E_cons=sum_b A(b)E_tail A(b)^T`. Induction using
   `(AB)^T=B^TA^T` proves `E_C=sum_x M_C(x)M_C(x)^T`, including the complete
   terminal sum. For scalar boundaries `E_C(0,0)=sum_x M_C(x)(0,0)^2>=0`.
   `N(C)=sqrt(E_C(0,0))` is defined also for zero trains; its square is the
   complete sum and a nonzero amplitude makes it positive. The empty scalar
   chain has norm one. A supplied bijection `e:W_n~I` AND the pointwise
   scalar-amplitude equality to `f(e(x))` transport this to the target
   Euclidean norm. The target's norm equality is not a premise.

7. **Syntactic costs (S7).** Dense retained environment entries are DEFINED
   by `H(empty)=r^2`, `H(cons)=l^2+H(tail)`; with `B(C)<=D`,
   `H(C)<=(n+1)D^2`. Per bit, the two products have `lm^2` and `l^2m`
   inner-product terms. Charging a multiply and at most one add per term,
   doing both bits, and adding `l^2` for the final combination gives
   `T(l,m)=4(lm^2+l^2m)+l^2`. The recursive formal budget `F` therefore
   obeys `F(C)<=9nD^3`; `D=0` is handled separately, not by assuming `D>0`.
   Neither `F` nor `H` is an executed/stored program refinement theorem.

Definitions of contractions, mass, environments, padding and budgets are
literal on their stated carriers. Thin factors and canonical outputs are
noncanonical existence witnesses; downstream mass claims are factor-choice
independent under the proved relations. A local unitary completion would be
another noncanonical representative, but it is not constructed here.

## Independent source proof/construction topology

The following stable identities are reconstructed here, not imported from a
repository graph. `AND{...} -> head` means every listed tail is required;
separate arrows from each tail would falsely imply independent sufficiency.

| ID | Complete AND tail | Mathematical head / source region |
| --- | --- | --- |
| E01 | real finite carriers, slice multiplication, residual shape | ABSORB: `A'(b)=A(b)S` (S2) |
| E02 | finite real inner product, row-span extension, `s=min(l,2r)` | THIN: `A=RQ,QQ^T=I_s` (S2) |
| E03 | THIN, pair-column bijection, finite-sum transport | CORE-THIN: core-shaped factorization and canonical head (S2) |
| E04 | empty contraction identity | CANON-BASE: empty canonical factorization (S3) |
| E05 | tail canonical factorization, ABSORB, CORE-THIN, matrix associativity | CANON-STEP: all-word factorization AND canonicality AND recursive dimensions (S3) |
| E06 | CANON-BASE, CANON-STEP, chain induction | CANON-EXISTS (S3) |
| E07 | rank-related dimension recurrence, finite maxima, terminal equality | DIM-BOUNDS; no numerical-core assumptions (S3) |
| E08 | `QQ^T=I`, row mass definition, finite distributivity | ROW-MASS (S3) |
| E09 | ROW-MASS, canonical tail induction, recursive word enumeration, empty identity | CANON-FULL-MASS (S3) |
| E10 | all-word `M_C=R M_D`, canonicality of D, CANON-FULL-MASS | RESIDUAL-MASS `Phi_C(v)=mass(vR)` (S3) |
| E11 | CANON-EXISTS, RESIDUAL-MASS, scalar boundaries, source unit-mass assumption | NORMALIZED-RESIDUAL + exact signed amplitude reconstruction (S3) |
| E12 | real-core row orthogonality, real-to-complex map, full pair-column sum | COMPLEX-ISOMETRY `V*V=I` (S4) |
| E13 | equal bonds, exact specified fresh-zero U columns, zero-bit input, passive-prefix semantics, matrix-vector action | LOCAL-UNPADDED-ACTION (S4); unitarity not in tail |
| E14 | `d<=B`, literal zero fill, active-prefix decomposition | PAD-SUM (S5) |
| E15 | `l<=B`, PAD-SUM, exact active padded U columns on ALL physical outputs, zero-bit input, passive-prefix action | LOCAL-PADDED-ACTION = `P_r^B w` (S5); `r<=B` not in tail |
| E16 | `l<=B`, `r<=B`, real row orthogonality, COMPLEX-ISOMETRY, inactive output zeros | PADDED-ACTIVE-ORTHONORMALITY (S5) |
| E17 | environment recursion, contraction recursion, finite word decomposition, product/transpose laws, empty identity | GRAM-EXPANSION (S6) |
| E18 | GRAM-EXPANSION, scalar boundaries, finite squares, real square-root laws | FULL-NORM, zero and positive cases (S6) |
| E19 | FULL-NORM, bijection of whole word carrier, pointwise target amplitude equality | TARGET-NORM-ADAPTER (S6) |
| E20 | literal retained-table recurrence, `B(C)<=D`, chain length n | STORAGE-ENTRY-BOUND (S7) |
| E21 | stated two-product-per-bit schedule, stated term charges, final `l^2` combining adds | UPDATE-BUDGET T (S7) |
| E22 | UPDATE-BUDGET, recursive F, `B(C)<=D`, integer dimensions, separate D=0 case | SYNTACTIC-ARITHMETIC-BOUND (S7) |

The row-span-extension method and the identity construction for `l>2r` are
dimension-conditional cases of THIN, not independent enough to cover all
dimensions each. The direct Gram route and canonical factor/mass route give
alternative mathematical access to full mass. They are not both required by
the Gram norm theorem. The source does not claim a full unitary or a global
preparation circuit via either route.

Diagnostic nodes are separate from the mathematical graph: DIAG-ZERO-EMPTY
(zero bonds, empty words, empty scalar norm), DIAG-SIGNED-RANK (signed and
deficient cores), DIAG-PAD-TRUNCATION (`r>B`), DIAG-D0-COST (zero budget cap).
These are review discriminators, not premises or universal proofs. No
executable diagnostic was run. Their symbolic cases were checked below.

## Exhaustive source disposition

Every substantive paragraph and displayed formula has a mathematical or
boundary node below. Blank separators are EXCLUDED(layout). Section titles
are EXCLUDED(navigation); the title at line 1 is EXCLUDED(title).

| Source lines | Disposition and stable node(s) |
| --- | --- |
| 3 | NODE PROVENANCE-RETROSPECTIVE (evidence boundary, not theorem) |
| 7 | NODE FINITE-CORE-CARRIERS |
| 9 | NODE WORD-CARRIER-ENUMERATION |
| 11–13 | NODE CHAIN-CONTRACTION-EMPTY-CONS |
| 15 | NODE FULL-BOUNDARIES, CANONICAL-DEFINITION, BOND-MAX; no physical order claim |
| 19–23 | NODE ABSORB |
| 25–29 | NODE THIN, prescribed-rank and deficient-rank boundary |
| 31 | NODE CORE-THIN, ZERO-FLATTENING; SOURCE_GAP-DETERMINISTIC-FACTORS boundary |
| 35–41 | NODE CANON-EXISTS, RECURSIVE-DIMENSIONS |
| 43 | NODE RANK-RELATED, DIM-BOUNDS, scalar one-site specialization |
| 45–50 | NODE CANON-BASE, CANON-STEP, exact all-word construction proof |
| 52–54 | NODE MASS-DEFINITION, FULL-CHAIN-MASS |
| 56 | NODE ROW-MASS, CANON-FULL-MASS, empty base |
| 58–62 | NODE RESIDUAL-MASS, choice independence, terminal completeness |
| 64–66 | NODE NORMALIZED-RESIDUAL, exact signed reconstruction, no postselection |
| 70–74 | NODE COMPLEX-ISOMETRY, transpose role and real-scalar boundary |
| 76–78 | NODE LOCAL-COLUMN-INTERFACE, equal-bond typing |
| 80–84 | NODE LOCAL-UNPADDED-ACTION, passive prefix, appended wire; SOURCE_GAP-WORD-WIRE and SOURCE_GAP-UNITARY-GATES boundaries |
| 88–93 | NODE ZERO-FILL, PAD-SUM, restriction versus injection boundary |
| 95–99 | NODE PADDED-TABLE, ACTIVE-COLUMN-INTERFACE, unused completion columns free |
| 101–105 | NODE LOCAL-PADDED-ACTION, outgoing truncation boundary |
| 107–112 | NODE PADDED-ACTIVE-ORTHONORMALITY; SOURCE_GAP-UNITARY-GATES and SOURCE_GAP-CLEAN-COMPOSITION boundaries |
| 116–124 | NODE ENVIRONMENT-RECURSION, GRAM-EXPANSION, full terminal matrix product and order proof |
| 126–130 | NODE FULL-NORM, nonnegative square sum, zero/nonzero and empty cases |
| 132–136 | NODE TARGET-NORM-ADAPTER, bijection plus pointwise source action, real-only boundary |
| 140–144 | NODE RETAINED-ENTRY-RECURRENCE, STORAGE-ENTRY-BOUND, no allocation claim |
| 146–148 | NODE UPDATE-BUDGET, operation convention |
| 150–152 | NODE F-RECURRENCE, SYNTACTIC-ARITHMETIC-BOUND, D=0 case |
| 154 | NODE COST-OMISSIONS, coefficient-9 meaning, identity and square-root exclusions |
| 158 | NODE EXACT-FINITE-SCOPE; SOURCE_GAP-INPUT-RUNTIME, SOURCE_GAP-FINITE-BIT boundaries |
| 160 | NODE PHYSICAL-NONCLAIMS; all remaining physical SOURCE_GAP boundaries |

There are no cited mathematical results with missing bibliography in this
source. Orthonormal-basis extension and finite-dimensional matrix/sum laws are
ordinary mathematical dependencies, not external implementation evidence.

## Stable open SOURCE_GAP ledger

These are deliberately unfilled source/consumer bridges. They are not errors
in the limited claims and not proof that the stronger goals are impossible.

- `SOURCE_GAP-DETERMINISTIC-FACTORS`: an actual factor-selection procedure,
  its refinement to THIN, and its operation/input-access costs.
- `SOURCE_GAP-WORD-WIRE`: a specified bijection/order convention and global
  proof relating recursive words to appended highest-wire stages.
- `SOURCE_GAP-UNITARY-GATES`: construction/choice of local square unitary
  completions matching the active columns, plus actual gate realization.
- `SOURCE_GAP-CLEAN-COMPOSITION`: carrier encodings, clean workspace/ancilla
  choices, multi-stage action, and terminal/garbage cleanup. Algebraic full
  mass does not select a clean terminal sector for general terminal dimension.
- `SOURCE_GAP-INPUT-RUNTIME`: input producer/evaluation model and a deterministic
  stored program refining the environment schedule, with reads, writes,
  traversal, copying, identity initialization, integer and output costs.
- `SOURCE_GAP-FINITE-BIT`: precision, numerical stability, finite-angle synthesis,
  accumulated error, and finite-bit/logical resource accounting.
- `SOURCE_GAP-SP-BE-TRANSPORT`: no oracle/SELECT/inverse, block encoding,
  postselection or amplification transport is supplied by the source.

## Seven semantic slots and binder audit

| Semantic slot | Source-only finding |
| --- | --- |
| 1. Target and normalization | Whole real chain contraction and full-terminal mass; scalar-boundary N; normalized residual only under original unit square sum. Target adapter needs pointwise action, not norm correctness as an assumption. |
| 2. Dimensions, scalar, basis/order | All finite natural dimensions including zero; real cores, complex local columns; pair flattening `br+j`; recursive front-bit words distinct from highest-appended physical wires until bridge. |
| 3. Oracle and coherent access | No input-generation, coherent oracle, controls or inverse is produced. Local U equations are conditional algebraic interfaces. No constant-time core callback is assumed. |
| 4. Ancilla/workspace/overwrites | Fresh zero bit, passive previous prefix, active bond zero fill; output bond may be truncated if `r>B`; global clean terminal/ancilla behavior remains open. |
| 5. Relative/global phases | Signed real amplitudes preserved exactly. Embedding introduces no imaginary phase; no parameter-labelled coherent phase convention or complex-core extension is certified. |
| 6. Norm/error/success | Exact real Euclidean mass/norm and local linear action. No approximation tolerance, success probability, accepted branch, or postselection advantage. Zero trains are defined, not normalized into a state. |
| 7. Resource tier | H entry count, F exact-real syntactic arithmetic, no square root or stored-program overhead. Not deterministic runtime, bit complexity, actual memory, gates, depth, connectivity or readout. |

TYPING: finite labels, dimensional matches, real/complex carriers, chain length.
STANDING: finite sum/matrix laws and ordinary real square-root conventions.
SOURCE premises: canonicality for canonical mass; all-word factorization for
residual mass; original unit mass for normalized residual; exact local U
columns and fresh-zero action for local interfaces; `l<=B` for incoming
padding; additionally `r<=B` and canonicality for active-column isometry;
scalar boundaries for N; target bijection plus pointwise action for adapter;
`B(C)<=D` for budget bounds. These are per-result, not globally accumulated.
RULED: none. EXCESS premises detected in the natural source: none. In
particular normalized residuals, canonical factors, final norm correctness,
unitary completion and executable costs must not later be smuggled into
stronger public theorem premises as though produced here.

SP/BE direction is a boundary, not an edge proved by this source. A complete
SP-to-BE route would require AND{PREPARE, SELECT, inverse/unprepare,
coefficient/phase data, clean-register and resource semantics}. A BE-to-SP
consumer would require AND{BE, prepared input, nonzero accepted branch,
normalization, postselection/amplification analysis}. Neither direction follows
from one local isometry or from GRAM-EXPANSION.

## Mathematical checks and phase-1 verdict

No contradiction or incorrect displayed identity was found in S1–S8 under
their local stated scopes. This is an independent natural-mathematics review,
not a machine-checked proof. Specific danger checks:

- If `r=0`, `s=0`; all contraction entries and row masses are interpreted on
  empty finite carriers without an invalid inverse address. Canonicality of a
  positive-dimensional row into zero columns would be impossible, but the
  constructed dimension recurrence avoids making that claim.
- If the input matrix is zero but `min(l,2r)>0`, thin Q still has the prescribed
  nonzero row carrier; choose orthonormal rows and let R be zero. Numerical
  rank is not confused with carrier dimension.
- The empty scalar chain has exactly one amplitude, equal to one; a nonempty
  zero scalar train instead has N=0 and cannot satisfy the unit-mass premise.
- For terminal dimension greater than one, selecting one terminal coordinate
  need not preserve mass. The stated proofs sum all coordinates and so do
  not make this false inference.
- If `r>B`, padded local action is an equality on existing physical labels
  only. It does not imply active-column orthogonality or lossless outgoing
  data; both are carefully separately scoped.
- `D=0` forces every bond zero, giving H=F=0. For `D>=1`, the two cubic terms
  are each at most D^3 and l^2 at most D^3, yielding `4(2D^3)+D^3=9D^3`.
  The coefficient is not a counter-category count.

Mathematical failure class: NONE for the limited natural claims. Stronger
construction claims remain OPEN at the stable SOURCE_GAP nodes. No API or
environment failure is being reclassified as mathematical failure. No salvage
or route retirement is needed. Independent topology cross-check, formal
comparison, Proof Seal, publication, purification and Exposition Seal are NOT
performed. Await separate phase-2 authorization without changing this seal.
