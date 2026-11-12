# TTC/NORM: independent actual-source static comparison

Status: STATIC_COMPARISON_FROZEN_BEFORE_DECODER_OR_AUTHOR_METADATA.
Reviewer: `ttc_norm_source_first_review_c25`.
Direction: `TTC_NORM_SOURCE_FULL_CARRIER_LOCAL_COLUMN_AND_SYNTACTIC_COST_BOUNDARY`.

## Authority, evidence, and limits

The parent explicitly authorized phase 2 only after phase 1 had been frozen.
The phase-1 notes and seal original bytes were rehashed and preserved:

- notes: `84011962ce0cdaedbf27027c7f7c17c0b50562da716fd1b5d030a5a0dbb3051b`;
- seal: `fe9c73b69d5e0d48990d94ebb8becf6f82157bf0335161002c443cf2d15650f8`.

Mathematical source remains the retrospective private execution source
`finite-real-tt-source-only.txt`, SHA256
`895ec97fe7e95146ec8d374bdcbecf4edbf40ff7e787135d032e376841d773b7`.
It is not an external book/paper, pre-proof record, or novelty certificate.
Historical formalizer identity remains UNKNOWN. Private execution file
identifiers here do not assert that a public package was read.

I read both actual target modules completely, including bodies, module
comments, imports, scopes, inductive constructors, and the named instance:

- `QuantumBlockEncoding/TensorTrainCanonical.lean` (TC), lines 1–320,
  SHA256 `0b51ec0335aaf6248f40b3f8dcf6014172c231b9ae512bf5bb09d84ebf66f808`;
- `QuantumBlockEncoding/TensorTrainNormEnvironment.lean` (NE), lines 1–144,
  SHA256 `a898ff4a83a1cc6426af7e85d3adc812c46175af0a31c1fd5eb2d48c776afb0d`.

The supplied target hashes match. I did not inspect a generated inventory,
author graph, author coverage, publication record, reconstruction, decoder,
other review, or build report. The parent reports an independently compiled
packet exists; I have NOT seen it and do not adopt its result. No Lean command,
Git operation, simulator, cache write, or sub-agent occurred. These are static
source findings, not an independently rerun kernel/axiom audit. The source
contains no `sorry`, `admit`, `axiom`, `unsafe`, `extern`, `implemented_by` or
`native_decide` in either target or in the two fully read direct providers;
this textual check is not an elaborated trust-closure certificate.

Repository-root instructions from phase 1 still apply. Exact-name checks found
no additional AGENTS/HARNESS in the target directory or inspected Mathlib
ancestors. Only new own-scratch artifacts were created. Any subsequently
provided author metadata must be labelled late assembly, not retroactively
treated as this review's prior input.

## Actual provider expansion and ambient meanings

`ThinLQ.lean` was read completely, lines 1–94 (SHA256
`1b5b8434ba90063bb7d14ffe133ca7733a38772d4fe95f24427800d4edc62614`).
It imports actual Mathlib GramSchmidtOrtho and Matrix.Basic. Its wide factor
supplier takes only `m<=n` and an arbitrary real `m×n` matrix. It zero-extends
the input rows to `n` Euclidean vectors, invokes a completed orthonormal basis,
uses the first `m` basis rows for Q, and uses representation coefficients for R.
The omitted coefficients vanish by the actual inverse-triangular theorem with
`i<m<=k`, not by an unmentioned full-rank assumption. Its `exists_thin_lq`
splits dimensions; for `n<=m` the witnesses are `A,1`. Rank deficiency and
empty matrices remain allowed. `sum_prefix_of_zero` has the stated prefix
bound and zero-tail assumption, with an arbitrary additive commutative monoid;
it is not a truncation identity without those conditions.

Actual Mathlib `gramSchmidtOrthonormalBasis` chooses an orthonormal extension
of the nonzero Gram-Schmidt family. Its assumptions are a finite ordered
index, finite-dimensional real/complex inner product space and equality of
finrank and index cardinality, NOT linear independence of the supplied family.
The relevant definition, zero-completion behavior, representation formula,
orthonormal inner-product identity, sum reconstruction, and inverse-triangular
proofs were inspected. For `EuclideanSpace R (Fin n)`, the inner product is the
coordinate sum and `WithLp.toLp 2` is a type wrapper, not a change of entries.
Thus this provider refines the source's existence argument; it does not
upgrade it to deterministic costed factor selection or unique factors.

`SequentialBondPreparation.lean` (SBP) was read completely, lines 1–342
(SHA256 `ad4542b108d44f196f2a02f78e59b58f43d45b1e890709cf4c22e1222805d5c5`).
Its namespace has `{B:Type*} [Fintype B] [DecidableEq B]`; individual declarations
retain only used instances, and `step_apply` explicitly omits `DecidableEq B`.
These are type/enumeration data, not extra quantum promises. In the targets
`B=Fin r` or `Fin B`, so the standard instances are supplied automatically.

The actual SBP meanings used by the targets are:

- `Core B = Matrix (Fin 2 × B) B C`, output row first;
- `Stage B = Matrix (Fin 2 × B) (Fin 2 × B) C`, an arbitrary square MATRIX,
  not a unitary subtype and not a primitive circuit;
- `BondState n B = PrimitiveBasis n × B -> C`;
- `freshZero v (p,(bit,a)) = if bit=0 then v(p,a) else 0`;
- `liftStage n U = I_prefix ⊗ U`;
- `step U v (x,b)` evaluates that matrix-vector action at
  `(Fin.init x,(x(Fin.last n),b))`;
- `step_apply` expands it to `sum_a U(x_last,b)(0,a)v(init x,a)` without
  requiring full U unitarity.

`RealAmplitudePreparation.lean` lines 1–45 were read to expand the actual
`lastBasisEquiv`: it splits a primitive word into `Fin.init` and `Fin.last`,
with inverse `Fin.snoc`. `PrimitiveSemantics.lean` lines 1–190 were read;
`PrimitiveBasis q` is literally `Fin q -> Fin 2` at line 116.
`PrimitiveBasisLE.lean` lines 1–90 were read; its numerical index map makes
wire zero least significant. The target theorems do not invoke that index map.
Initial direct probes for modules named RealAmplitude and PrimitiveBasis
failed because those filenames do not exist; only the actual providers just
identified were read. This is a retrieval correction, not a mathematical or
Lean compilation failure.

Actual Mathlib matrix definitions were checked: matrices are row/column
functions with matrix multiplication, not pointwise multiplication; `mulVec`
is column action, `vecMul` is row action, transpose swaps indices,
conjugate transpose additionally stars entries, and the identity is the
Kronecker delta. Kronecker multiplication preserves the passive prefix.
`finProdFinEquiv (b,j)` has value `j+r*b`, agreeing with source `br+j`;
the empty-column case is typed by an empty Fin carrier. Actual toolchain
`Fin.castLE` retains the numeric value and changes only its bound proof.
Actual Real.sqrt is the nonnegative square root with zero on negative inputs,
but NE proves the Gram entry nonnegative before applying `sq_sqrt`; no
off-source negative fallback enters any norm result.

No target has a hidden top-level `variable`, source contract structure,
Prop alias, oracle typeclass or assumption-bearing section. TC opens only
BigOperators. NE opens BigOperators and TC. Canonicality and RankReduced were
expanded rather than trusted as names. Plain finite/decidable instances,
standard R/C algebra, and ordinary classical choice explain the ambient
context. No `NeZero`, `Nonempty (Fin d)`, positive bond, rank or positivity
assumption was discovered in the targets.

## All 49 hand-written named items, not a count-only review

The TC namespace is `QuantumBlockEncoding.TensorTrainCanonical`; NE is
`QuantumBlockEncoding.TensorTrainNormEnvironment`. Each row was checked in its
actual source body. This list is independently reconstructed, not read from an
inventory. It lists the 48 non-instance items and `wordFintype`; autogenerated
inductive constructors/recursors are not being asserted to be the only other
kernel declarations. The Chain/RankReduced constructors are separately
expanded below.

| Item | Actual line | Source obligation and audit |
| --- | --- | --- |
| TC.Core | 18 | S1 literal `Matrix (Fin l) (Fin 2 × Fin r) R`; all rows/columns |
| TC.slice | 20 | S1 literal `A a (bit,b)`; no bit permutation |
| TC.Chain | 24 | S1 indexed length and two boundary bonds; nil equal endpoints, cons dimension match |
| TC.Word | 29 | S1 Unit at zero, `Fin 2 × Word n` at successor |
| TC.wordFintype | 33 | S1 recursive finite enumeration; ambient named instance, not omitted from this review |
| TC.contract | 39 | S1 nil identity and head slice times tail contraction |
| TC.RightCanonical | 45 | S1 nil True, cons AND{row orthogonality, canonical tail} |
| TC.RankReduced | 51 | S3 dimension relation, no numerical core premise |
| TC.absorb | 58 | S2 full incoming residual sum, same bit |
| TC.absorb_slice | 62 | S2 matrix multiplication identity; only typing arguments |
| TC.exists_core_lq | 67 | S2 existential R,Q at exact min carrier, factorization AND row orthogonality; no rank input |
| TC.exists_rightCanonical | 85 | S3 existential residual and D, canonicality AND RankReduced AND every-word factorization; no desired target input |
| TC.RankReduced.head_bound | 105 | S3 nonempty relation gives new head <= old AND tail witness with new head <= twice new next bond |
| TC.RankReduced.last_bond_le_two | 114 | S3 length-one scalar-terminal relation; no claim for arbitrary terminal dimension |
| TC.mass | 121 | S3 arbitrary finite real vector sum of squares |
| TC.mass_vecMul | 124 | S3 arbitrary finite real matrix with row orthogonality preserves row-vector mass |
| TC.chainMass | 139 | S3 all recursive words, then all terminal coordinates through mass(vecMul) |
| TC.chainMass_eq | 143 | S3 conditional canonicality, full mass output; proof inducts all words |
| TC.residual_mass | 164 | S3 canonicality AND all-word factorization; no rank relation or selected terminal sector needed |
| TC.exists_rightCanonical_normalized | 175 | S3 terminal one plus original `chainMass C v=1`; normalized residual is OUTPUT |
| TC.exists_normalized_state | 186 | S3 original scalar square sum one; existential u normalized AND exact signed amplitude equality |
| TC.maxBond | 201 | S1/S3 maximum includes nil terminal and each head |
| TC.RankReduced.maxBond_le | 206 | S3 relation alone, not numerical canonicality/factorization |
| TC.complexCore | 214 | S4 real embedding with output `(bit,new bond)` row, old bond column |
| TC.complexCore_isometry | 218 | S4 real row orthogonality -> conjugate-transpose column isometry |
| TC.sequentialCore | 233 | S4 equal-rank type adapter, literally complexCore |
| TC.sequential_step | 238 | S4 clean-zero column equality -> exact passive-prefix local action; no unitarity premise |
| TC.padVector | 249 | S5 literal numeric-prefix table; may restrict when active dimension exceeds physical |
| TC.padVector_active | 252 | S5 `d<=B`, numeric-preserving cast, active-coordinate identity |
| TC.paddedCore | 258 | S5 active input and output conditions, else zero |
| TC.paddedCore_inactive_output | 263 | S5 all physical inputs, output label `r<=b.val` gives zero |
| TC.sum_padVector | 267 | S5 `d<=B` -> full physical sum equals active sum |
| TC.sequential_step_padded | 278 | S5 `l<=B`, active-only clean columns -> padded outgoing contraction; NO `r<=B` added |
| TC.paddedCore_active_isometry | 298 | S5 BOTH embeddings fit AND real row orthogonality -> delta on active input columns |
| NE.gram | 19 | S6 literal empty identity and per-bit local Gram recursion |
| NE.gram_eq_sum | 27 | S6 arbitrary real chain -> complete word matrix sum |
| NE.gram_scalar | 44 | S6 scalar boundaries -> square amplitude sum |
| NE.gram_scalar_nonneg | 49 | S6 nonnegativity produced from squares, not assumed |
| NE.norm | 55 | S6 literal Real.sqrt of Gram scalar; defined at zero |
| NE.norm_eq | 57 | S6 full square-sum square root |
| NE.norm_sq | 61 | S6 square equals sum using produced gram nonnegativity |
| NE.norm_pos_of_nonzero | 65 | S6 existential nonzero amplitude -> norm positive |
| NE.norm_eq_of_contract | 73 | S6 finite target I, full carrier equivalence, pointwise action -> norm adapter |
| NE.environmentScalars | 83 | S7 literal retained entry recurrence; not actual allocated objects |
| NE.environmentScalars_le | 87 | S7 full maxBond bound -> `(n+1)D^2` |
| NE.updateArithmeticBudget | 105 | S7 exact literal `4(l*m*m+l*l*m)+l*l` |
| NE.arithmeticBudget | 109 | S7 nil zero and sum of local budgets |
| NE.updateArithmeticBudget_le | 113 | S7 dimension bounds only, D=0 handled -> `9D^3` |
| NE.arithmeticBudget_le | 128 | S7 maxBond bound -> `9*n*D^3`; no stored-operation model |

## Exact binder, definition, output, and logical dependency comparison

### S1–S2: carriers and thin factors

Chain is not a vector with implicit scalar boundaries. `nil r : Chain 0 r r`
and `cons (head:Core l m)(tail:Chain n m r):Chain(n+1)l r` preserve every
initial row and terminal column even if zero-dimensional. Word's named finite
instance is recursive Unit/product enumeration; no cardinality `2^n` theorem
is assumed or needed for these finite sums.

`exists_core_lq` quantifies only arbitrary natural `l,r` and real core A.
Its outputs have `R:l×min(l,2r)` and `Q:min(l,2r)×(bit,r)`.
Its proof calls ThinLQ on a reindexed arbitrary matrix, transports the
factorization pointwise and transports the row inner-product sum along the
actual bijection. It has no full rank, nonzero matrix, canonicality, input
mass or target-action binder. Noncanonical choice belongs inside the provider,
not as a pre-supplied public factor witness. No false uniqueness is claimed.

### S3: construction, dimensions, and normalization

`RankReduced.nil` pairs exactly the same terminal empty chain.
`RankReduced.cons` takes any old head and any new head having left dimension
`min l (2*m')`, together with the recursively related tails. No arithmetic
entries are constrained. Therefore the relation is not a proof ingredient
masquerading as canonicality, and its dimension-only inequalities are faithful.

`exists_rightCanonical` obtains its tail residual, canonicality, rank relation
and every-word factorization from the induction hypothesis. It absorbs that
produced residual into the old head and invokes the produced thin factor.
The required conjunction is in its OUTPUT. The proof realizes the frozen
source E01–E06 topology, not just a wrapper around an assumed global action.

`mass_vecMul` alone explicitly takes `hA:A*A.transpose=1` on arbitrary finite
I,J; `DecidableEq I` is required to express identity on the left row carrier
(TYPING, not an extra mathematical promise). `chainMass_eq` explicitly takes
`RightCanonical C`, precisely the conditional source identity. `residual_mass`
explicitly takes canonical D and the all-word factorization; those are allowed
source premises for this general helper, but are produced internally when the
existential normalized anchors use it. They are not newly assumed of the
original arbitrary C.

`exists_rightCanonical_normalized` has only the original unit full-mass premise
in addition to C,v and scalar terminal typing. `exists_normalized_state` has
only `sum_x contract C x 0 0 ^2=1` in addition to a scalar-boundary chain.
It chooses `u=vecMul (fun _=>1)R`, proves mass u=1, and derives each amplitude
from the factorization. Neither theorem takes normalized residuals, positivity
of a target norm, an already normalized state oracle, nor target-state equality
as input. Products and real signs are unchanged.

The source's assertion that EACH new bond is bounded by its old counterpart
has no separate universal bond-index theorem in this module. It follows by
recursing on the fully specified RankReduced constructors; head and global
max inequalities have explicit named roots. This is a SOURCE_IMPLICIT derived
consequence of the dimension relation, not a new certified indexed theorem
name and not an unfilled mathematical construction gap.

### S4–S5: precise local interface, not a hidden physical compiler

`complexCore` is a literal transpose-of-roles plus real embedding, not an
arbitrary complex-core transpose. `complexCore_isometry` assumes only the
canonical row equation and proves conjugate column orthogonality, including
both bits and all outgoing labels. Real-entry conjugation is expanded in the
proof. No phase magnitude is substituted for amplitude.

The unpadded theorem is restricted by TYPE to equal bonds. Its U is an
arbitrary square stage. Its sole logical premise states its entries for input
`(0,a)` on all active a and all outputs. `step_apply` then supplies the exact
local sum; it does not require unitarity. This source interface is legitimately
conditional. It must not be publicized as having produced the U or a circuit.

`padVector` intentionally has no `d<=B` binder. On the larger physical carrier
it zero-fills, while on a smaller one it restricts; active agreement and the
lossless sum lemma have the needed bound. The `Fin.castLE` embeddings preserve
numeric labels. `paddedCore` tests BOTH active input and active output bounds.
Its inactive-output theorem quantifies every input, but that is a theorem
about the TABLE, not about every unspecified U completion column.

`sequential_step_padded` assumes `hl:l<=B` only. Its `columns` quantifier is
`forall bit b (a:Fin l)`, with fresh-zero physical input
`(0,Fin.castLE hl a)`; all physical output labels b are covered. The conclusion
is the literal padVector of the exact outgoing contraction, and therefore
remains true as restriction for `r>B`. No outgoing losslessness is silently
claimed. `paddedCore_active_isometry` adds BOTH `l<=B` and `r<=B` and canonical
row orthogonality. The result is only for active input a,c. Zero-filled
inactive input TABLE columns are not required to be the other columns of a
unitary U. For instance zero input table columns do not establish a square
isometry on the whole padded input register.

The imported SBP module does contain conditional run/transfer/support/terminal
cleanup theorems, and circuitStage adapters conditional on actual circuit
column equations. None is invoked to prove a complete TTC-generated global
physical run. Their existence does not discharge the word/wire adapter,
concrete unitary completion or compiler-column obligations of this source.

### S6: no norm-correctness premise

`gram_eq_sum` assumes no canonicality, rank, scalar boundaries, target action,
positivity or precomputed full sum. The body proves the all-word matrix
identity by induction and matrix transpose/distributivity laws. Matrix products
sum the FULL terminal bond. `gram_scalar` then specializes to scalar endpoints.
`gram_scalar_nonneg` proves positivity's weak form from real squares.
`norm_sq` uses it rather than assuming it. `norm_pos_of_nonzero` has precisely
the stated nonzero-amplitude premise and no arbitrary fallback normalization.

`norm_eq_of_contract` carries `{I:Type*}[Fintype I]`, a genuine equivalence
`Word n ≃ I`, a real target, and pointwise amplitude equality. Equivalence
includes injectivity AND surjectivity: it does not lose words, add zero sectors,
or duplicate amplitudes. The proof transports the sum; it does not assume the
desired norm equality. These input facts must be supplied for any downstream
target adapter, not counted as produced target-state preparation.

The source's empty scalar chain norm-one assertion has no dedicated named
root here. It is a definitional/mathlib consequence of gram nil=identity,
Fin-one entry, norm=sqrt and sqrt_one. Likewise zero-amplitude trains yielding
norm zero follow by norm_eq and sqrt_zero. They are SOURCE_IMPLICIT corollaries,
not fabricated independent exported declarations. Zero is in the definition's
full carrier; no nonzero binder was inserted to define norm.

### S7–S8: three interfaces must remain distinct

The mathematical Gram recursion is present. A deterministic stored data
producer and a cost-semantics refinement of such a producer are NOT present
in these modules. `gram` is noncomputable; this marker alone is not a proof
of inefficient mathematics, just as its recursive shape is not proof of an
efficient implementation.

`environmentScalars` defines the sum of dense intermediate table sizes. Its
bound is proved from every bond being bounded via maxBond, including the
terminal identity. It is not measured allocated memory or peak live space.
`updateArithmeticBudget` is exactly the source's scalar convention, with the
two matrix products per bit and final l^2 combining additions. `arithmeticBudget`
charges the empty identity zero. Its inequalities explicitly handle D=0.
There is no eight-category operation counter, load/store trace, table-cache
refinement, square-root/angle cost or emitted-instruction count in these
definitions. In particular `norm` wraps a square root outside arithmeticBudget.

The source's explanation of this syntactic schedule is faithful to the shapes
and formulas, but there is no independent kernel theorem saying an external
execution trace uses <=F operations. That is the already-open
SOURCE_GAP-INPUT-RUNTIME, not an omitted premise that would invalidate the
syntactic inequality. H counts tables if retained by specification; it does
not prove a runtime retains them. Source prose and comments saying “compute”
or “one square root is performed” must be read as this expression/evaluation
schedule, not upgraded into execution evidence.

## Source topology versus actual proof dependencies

The frozen phase-1 graph remains authoritative as the independently extracted
SOURCE topology; it has not been rewritten to mimic Lean. Actual inspected
proof bodies align at these complete AND boundaries:

- CORE-THIN uses AND{ThinLQ supplier, pair equivalence, sum transport};
  canonical existence uses AND{tail-produced residual/canonicality/ranks/action,
  absorption, core thin factor, matrix associativity}.
- Full canonical mass uses AND{right-canonical head, canonical tail induction,
  product-word enumeration, row-vector mass}. Residual mass uses
  AND{all-word factorization, canonical D, canonical mass}; normalized anchors
  produce these ingredients rather than exposing them as extra hypotheses.
- Local action uses AND{exact clean columns, fresh-zero definition,
  passive-prefix identity action}. Padded action also uses incoming prefix
  bound and sum transport; outgoing bound is reserved for padded isometry.
- Gram proof uses AND{contraction recursion, Gram recursion, finite word
  product sum, transpose/matrix laws}; norm uses scalar-boundary Gram squares.
  It does NOT depend on canonicalization, complex isometry or local U.
- Entry bound uses AND{literal H, maxBond bound, dimension arithmetic};
  arithmetic bound uses AND{literal T/F, local dimension bounds, induction}.
  It does NOT derive any memory or gate bound from Gram semantics alone.

These are hand-audited source references from proof bodies, not an elaborated
proof-term dependency extraction. Module import of TC by NE does not mean
norm depends mathematically on every TC result. Source diagnostic checks
remain separate; no finite executable check was promoted to these proofs.
The dimension cases in ThinLQ are exhaustive case branches, not a false AND
or two independently sufficient global algorithms. No source OR-route has
been silently deleted or merged into an AND tail.

## All seven semantic slots after formal comparison

| Slot | Comparison outcome |
| --- | --- |
| Target/normalization | MATCH: complete real contractions, all terminal mass, scalar norm; residual normalization produced under source unit-mass premise. |
| Dimensions/scalar/basis/order | MATCH: Fin zero allowed; exact min recurrence; real cores, complex columns; product address equals br+j. No recursive Word-to-physical-wire equivalence is presumed. |
| Oracle/coherent access/inverses | MATCHED NONCLAIM: no oracle producer, coherent parameter interface, SELECT or inverse supplied; stage entries are explicit local premises. |
| Ancillas/workspace/overwrites | MATCH: zero fresh bit and passive prefix actual semantics; numeric active embedding; r>B restriction not losslessness; no complete TTC physical cleanup certificate. |
| Phases | MATCH: literal real signs preserved; complexCore embeds real entries; no global-phase quotient or parameter-relative-phase theorem substituted. |
| Norm/error/success | MATCH: exact finite R/C algebra; nonnegativity proved; no finite-bit approximation, probability or accepted-branch semantics asserted. |
| Resource tier | MATCH: H/F syntactic entry/arithmetic definitions and inequalities; no actual runtime/space/cache/finite-angle or logical-gate complexity theorem. |

Binder classification: all per-result logical premises identified above are
SOURCE; finite carrier/instance and dimension-index formation is TYPING;
ordinary R/C and finite-dimensional algebra is STANDING. RULED corrections:
none. EXCESS public mathematical premises found: none. There is no project
contract bundle left unexpanded in either target. No per-result premise was
pooled into a stronger claim about arbitrary original chains.

All seven frozen SOURCE_GAP identifiers remain OPEN for stronger consumers:
DETERMINISTIC-FACTORS, WORD-WIRE, UNITARY-GATES, CLEAN-COMPOSITION,
INPUT-RUNTIME, FINITE-BIT, SP-BE-TRANSPORT (each with `SOURCE_GAP-` prefix).
The limited local physical equalities are proved conditionally, so their column
premises are not failures of those equalities. Realized stages/gates are
PREREQUISITES for a physical consumer, not products of these roots. The
bondwise inequalities and empty/zero scalar norm corollaries are
SOURCE_IMPLICIT as described; they are not misleadingly given nonexistent
kernel names. No SP/BE edge is proved. Its complete missing transport tails
from phase 1 remain unchanged.

## Static verdict and next gate

`STATIC_MATCH_LIMITED_SOURCE_WITH_OPEN_CONSUMER_BOUNDARIES`.
No blocking source-to-formal binder, full-carrier, sign, normalization,
local-column or syntactic-cost mismatch was found in the inspected actual
sources. This is not an unconditional physical preparation claim and not
proof that the whole project/book is complete. The narrower wording is
essential to the verdict.

Failure class: NONE for this static comparison. There is no mathematical
route retirement or salvage requirement. Confidence: high in the enumerated
mathematical/type comparison; kernel compilation, exact elaborated axiom
closure, toolchain/manifest admission, independent decoder reconciliation,
author graph/coverage fidelity, late-assembly provenance, and publication gates
are explicitly NOT reviewed yet. The local toolchain declaration is
`leanprover/lean4:v4.33.0`; no compiler was invoked to verify it.

Phase 1 stays immutable. Freeze this comparison now; only after the static
seal may the parent deliver build/decoder and late-assembled author metadata
for a separately recorded reconciliation. Do not backdate such future inputs.
