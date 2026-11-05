# c26 physical tensor-train source-only review

Status: SOURCE_ONLY_FROZEN; FORMAL_CONTENT_UNSEEN for the three new targets.
Reviewer: `ttc_norm_source_first_review_c25`, continuing as the c26 independent
source reviewer, not claiming an unrelated identity or wholly context-free run.
Direction: `TT_PHYSICAL_RANK_BOUNDARY_LSB_MSB_AND_EXACT_RESOURCE_MODEL`.

## Exposure, authority and provenance

Prior raw-byte hash I/O: TRUE. In c25, programs read all production/test input
bytes, including the three now-targeted files, for hashes and binding digests.
Those three source texts were not displayed, explained, or semantically viewed.
Prior target semantic-text exposure: FALSE. Their module names were visible.
No author mapping of those three targets was seen. I initially stopped to
report this distinction; the parent expressly approved continuation as
FORMAL_CONTENT_UNSEEN, not absolute file-unread. This review does not describe
that prior raw-byte I/O as absence of all prior exposure.

Previously known c25 mathematics includes the complete Canonical and
NormEnvironment modules, ThinLQ and SequentialBondPreparation, necessary
RealAmplitudePreparation/PrimitiveBasisLE/PrimitiveSemantics context, and
ordinary Mathlib finite matrix, orthonormal-basis, square-root and finite-index
definitions. I also saw the c25 independent decoder's reconstruction and
bounded compile evidence after my c25 source/static seals. That is disclosed
provider knowledge, not semantic reading of TensorTrainLocalCompiler,
TensorTrainWord or TensorTrainPrimitivePreparation. Their implementation,
author mapping, declaration inventories, c26 decoder/graphs and compile
evidence remain prohibited and unseen in this phase.

The only new mathematical input was the actual private execution file
`finite-real-tt-physical-source-only.txt`, read fully as UTF-8 at lines 1–151:
21,210 original bytes, SHA256
`d71f16da026938debcd024d6f2fa9fa9268ade2096b5854a030d2065828b315d`.
This basename identifies a private input actually read, not a public bundle
that is being falsely claimed to have existed. The source is retrospective
local mathematics from pre-existing material. Historical formalizer UNKNOWN;
no external-paper/book reproduction, pre-proof chronology, historical author
independence or novelty follows. No c26 formal agreement is being decided.

The already-read applicable AGENTS/HARNESS, substantive-worker/source-audit
skills and publication/proof-digestion/evidence-memory protocols govern the
source-first separation. No new implementation/frontier lookup was made to
satisfy generic workflow. Only this designated source and own scratch outputs
were accessed for the c26 source phase. No Git, Lean, cache, simulation,
sub-agent, main-tree write or author-private coverage/freeze/handoff read.

## Independent mathematical reconstruction and checks

### S1: complete finite carriers and actual sites

All bond dimensions are natural, including zero. Core rows are old bond a;
columns are (emitted bit b,new bond j). Contraction is the real product of
bit slices in head-first word order, with empty identity and every boundary
index retained. Canonicality is orthonormal ROWS, not columns. The time-dependent
active dimension r_t stops changing after N, but the extracted coefficient
table is deliberately ZERO after N. Its realness and output-zero-tail properties
hold at all times; active-column isometry requires an ACTUAL site t<N,
canonicality and both active dimensions fitting into the physical label space.

For q natural, S=2^q is strictly positive, including q=0. The physical bond
basis is q named bits with little-endian map L_q. A local stage has q LOW
bond wires and a HIGHEST fresh bit. Its coordinate map is
`append(z,b) -> (b,L_q(z))`. The occupied fresh-zero input positions are the
injection `a -> (0,a)` transported through this map. Their being distinct is
essential; their being a prefix of another local basis ordering is NOT needed.

### S2: unused column fixes orientation, not an advertised block

Given arbitrary finite row basis I, orthonormal real columns V indexed [r],
an injection e locating them in the square matrix, and strict `r<|I|`, extend
those columns to an orthonormal basis with each original column at e(a).
For the resulting orthogonal U_0, determinant squared is one. If det U_0=-1,
choose k outside image(e), let H be diagonal with H_kk=-1 and all other
diagonal entries one, and set U=U_0 H. Then U is orthogonal,
det U=det U_0 det H=+1, and U(:,e(a))=V(:,a) on EVERY output row.
The k-column flip cannot leak into an active column. No correction is needed
if the original determinant is +1. Simultaneous row/column relabeling conjugates
by a permutation matrix, leaving determinant and column inner products intact.

This is nonunique existential completion, not unique characterization or a
classical runtime algorithm. The spare inequality is a SOURCE premise:
completely specifying the 1x1 column [-1], or any full determinant-minus-one
orthogonal matrix, defeats determinant-one completion with all columns fixed.

### S3: actual exact-real primitive instructions

RY uses the HALF physical angle. X/RZ/CNOT have the given exact matrix/basis
semantics; CNOT control and target are distinct, and untouched wires are fixed.
Chronological lists evaluate with later matrices on the LEFT. The ambient
composition statements admit all four primitives, although the SO compiler
uses only RY and CNOT. Every primitive is unitary on the whole carrier.

For a pair (x,y), put rho=sqrt(x^2+y^2). If rho>0, choose a planar rotation
with cos(phi)=x/rho and sin(phi)=-y/rho, hence it sends (x,y) to (rho,0).
An RY physical angle 2phi gives this matrix. If the pair is zero choose zero.
Negative x or y is not replaced by an absolute-value amplitude. Adjacent
bottom-up row sweeps on each increasing column do not disturb already fixed
standard-basis columns, because their entries on both affected rows vanish.
Orthogonality then makes each newly fixed column exactly the positive standard
basis vector. After D(D-1)/2 scheduled pairs, the final sign is + by determinant
one. D=0/1 are harmless identity/no-pair cases of this mathematical decomposition;
the actual local use has D=2S>=2.

If E_m ... E_1 U=I, then U=E_1^-1 ... E_m^-1. Thus the CHRONOLOGICAL
implementation list is E_m^-1,...,E_1^-1: reverse order AND negate angles.
Negating angles without reversing, or reversing without inversion, is not the
claimed circuit. Full matrix equality, not only the zero-input state, is used.

In Gray coordinates adjacent labels differ on exactly one target wire. A
rotation selected by all other q wire bits realizes precisely that two-level
pair and fixes all other basis states. If the ordered first endpoint has target
bit one, the 0/1 basis swap conjugates RY(theta) to RY(-theta), so negate the
PHYSICAL angle. Gray reindexing is internal conjugation/bookkeeping; final
gates have original named-wire semantics and no extra physical permutation.

The selected rotation comes from a multiplexed angle table. Splitting on an
added control, use half-sum a=(theta_0+theta_1)/2 and half-difference
b=(theta_0-theta_1)/2 with chronological blocks RY(a),CX,RY(b),CX, recursively
on remaining controls. Control zero gives RY(a+b); control one gives
X RY(b) X RY(a)=RY(a-b). This proves the two branches without a hidden
multi-control oracle or work wire. Starting at one RY, induction gives
R(q)=2^q=S and C(q)=2(S-1) CNOTs, so each selected list has 3S-2 instructions.
There are S(2S-1) pairs for D=2S. The total is
`S(2S-1)(3S-2)=6S^3-7S^2+2S <= 6S^3` for S>=1.
The looser product bound `(2S^2)(3S)` agrees. Zero-angle entries remain counted.

### S4: local circuits are produced

At an actual canonical site with maxBond<=S, the extracted real columns,
transported to q+1-wire rows, are orthonormal by S1. Their physical positions
are injected fresh-zero labels. Since r_t<=S and S>0, `r_t<2S`; this supplies
the spare column without a rank/full-rank/positive-q assumption. S2 then
produces SO completion and S3 produces a concrete finite instruction list.
The same constructed local circuit has the entire prescribed active columns,
length<=6S^3 and no oracle-call instructions. Its other columns remain free.
There is no final-state action assumed to establish this existence.

q=0 gives S=1 and a one-wire local circuit, not a forbidden edge case. Empty
active input columns are vacuous but allowed. No isometry/compilation assertion
is made about the intentionally zero tables after t=N; those sites never run.

### S5: signed boundary absorption really pays initialization

The row matrix B_u has squared norm sum_a u_a^2. For unit u and orthonormal
core rows, `(B_u A)(B_u A)^T=B_u(A A^T)B_u^T=I_1`. The contraction identity
`M_(B_u A::T)(w)=B_u M_(A::T)(w)` needs neither norm-one u nor canonical A;
those hypotheses belong only to the row-isometry conclusion.

For a POSITIVE-length normalized scalar-boundary input C, tail-first thin
factorization produces E and u with exactly the original signed amplitudes,
unit mass u and non-increased maxBond. These are produced dependencies, not
free initial-state data. Nonempty E has a head into which B_u is multiplied.
The resulting D has initial and terminal dimension one, is canonical, preserves
every original scalar amplitude and has the same bound: the replacement
initial dimension one fits because original maxBond>=1. Tail dimensions do not
change. No absolute values, omitted relative sign or selected terminal sector.

This is exact existence with choices. Positivity of N is genuinely used to
supply that first core; q need not be positive. A scalar amplitude -1 cannot
be absorbed into a nonexistent zero-core head. The empty scalar chain already
has its sole amplitude +1, and is not an arbitrary signed zero-wire state.

### S6: real zero initialization and full terminal cleanup

The nonnegative recurrence `L_(q+1)(z)=z_0+2L_q(tail z)` proves label zero iff
ALL bits zero, including q=0. The padded rank-one boundary (1) is therefore
literally the all-zero column of the empty q-wire circuit, of length zero.
It is not an arbitrary normalized u supplied without cost: u was absorbed.

Bond-only transport along e:B~C is the literal simultaneous index change
`U^e((b,j),(b',a))=U((b,e(j)),(b',e(a)))`. Changing the summation variable
shows the stated equality of runs with boundary v and v composed with e^-1.
Prefix bits stay fixed. No unitarity or desired global action is assumed for
this algebraic transport.

For a generic scalar-boundary D, the conditional sequential action assumes
exact active clean columns at t<N and maxBond<=S, not canonicality or
normalization. Initial support is rank one. At each step input support makes
unused completion columns irrelevant; active output zero tails propagate the
next support invariant. Expansion is the padded row-vector core product.
Induction yields the FULL amplitude at every chronological data y and physical
bond z: `delta(z,0^q) M_D(w(y))(0,0)`. The terminal rank-one padding gives
integer label zero, and then the zero-label theorem gives all bond bits zero.
There is no projection or postselection. For a nonnormalized D, suitable
unitary circuit-column premises need not be satisfiable; this conditional
identity is not circuit existence for every arbitrary D.

At N=0 no site equation is required, the scalar empty contraction is I_1,
and the empty physical list leaves the zero bond untouched. This algebraic
helper case does not remove positivity from the separate boundary-absorption
existence route.

### S7–S8: word order, public layout, and actual one-list composition

Head-first word to basis function puts first bit at coordinate zero; inverse
reads coordinate zero and recurses. Word-to-Boolean-list preserves length.
Basis reversal rev_N is an involution even at N=0. The sample map is
`J(w)=L_N(rev_N(wordBasis(w)))`, with MSB recurrence
`J(b::v)=2^(length v)b+J(v)`. This follows from the LE append identity
`L_(N+1)(append(x,b))=L_N(x)+2^N b`. The special direct Boolean-list index
claim is at positive width k+1; the general bijections and reversals include
zero width. Consequently `J(word(rev_N(x)))=L_N(x)`; no sampled target
function action follows without its own pointwise core/action premise.

Internally wires 0..q-1 are bond; chronological emitted data y_t goes at q+t.
Lifting an earlier list over a fresh zero bit and placing/then appending the
next stage gives one actual list on q+N wires. Full passive-prefix matrix
entries supply the induction to sequential action, not an assumed global map.
The public rename is a finite wire bijection:

`bond a -> N+a`, and `chronological data q+t -> N-1-t`.

These ranges are disjoint and exhaustive, also for N=0/q=0. Injective renaming
preserves CNOT control/target distinctness and fixes the other named wires as
required. It constructs final gate labels, not a cost-free SWAP network on an
already produced state. Public data is LOW, bond HIGH; chronological data is
REVERSED. Thus the whole public all-zero-input amplitude is
`delta(z,0^q) M_D(word(rev_N(x)))(0,0)` at EVERY x,z.

For N=2, head bits (a,b) emit internally in that order; public x_1=a,x_0=b.
Then L_2(x)=b+2a=J(a::b), explicitly checking the two-endian relationship.
No hidden reversal of the bond bits occurs: bond a goes to high wire N+a.

Padding/lifting/placing/renaming each primitive preserves actual list length.
The single assembled list therefore has EXACT length sum_(t<N)length(c_t),
because initial preparation here is empty. Uniform bound K gives <=N K.
No extra qN overhead instruction is hidden, and no zero site after N is
executed. N=0 gives an empty sum/list. These are exact list counts, not
arithmetic proxy counts.

### S9–S10: one witness and precise scope

The root inputs are N>0, q natural, scalar-boundary real C, maxBond C<=2^q,
and the original complete amplitude square sum one. S5 produces canonical
same-amplitude D; S4 produces bounded actual circuits at finitely many sites;
S6 supplies genuine zero initialization and terminal cleanup; S8 composes and
renames ONE list. ALL outputs refer to that same c: length<=N*6*(2^q)^3,
zero oracle-call instructions, full-space unitarity, and the exact signed
amplitude at every public data/bond label. Unitarity follows from primitive
unitarity, not an assumed desired full-circuit map. No initial u preparation
term is omitted: its real signs were placed in the first core.

This closes the source's ideal exact-real local completion, ordering and
scalar-terminal cleanup route as natural mathematics. It does not by itself
prove any implementation matches. The model allows arbitrary exact real RY
angles and named-wire nonlocal CNOT, not finite-bit synthesis or fixed hardware.
An existential bounded finite list need not have a deterministic efficient
parameter producer. The bound is cubic in S=2^q (hence exponential in q), not
automatically polynomial in another scientific input parameter.

## Independent source construction topology

These stable source identities are invented for this natural source, not read
from Lean or author mappings. Every tail in each AND row is needed for that
local result; SOURCE premises stay distinct from produced proof dependencies.
Conditional helper identities are not unconditional existence results.

| Edge | Complete AND tail | Head |
| --- | --- | --- |
| P01 | finite real cores, dependent matching bonds, recursive words, empty identity | CHAIN-ACTION, all boundaries |
| P02 | arbitrary natural physical B, active dimensions, coefficient extraction, zero-after-schedule convention | REAL-TABLE + OUTPUT-SUPPORT, all times, including B=0 |
| P03 | t<N, canonical head rows, old/new dimensions<=B, zero-tail finite sum | ACTIVE-COLUMN-ISOMETRY on the full finite physical carrier |
| P04 | q natural, binary LE recurrence, finite bit coordinates | LE-BOND-BIJECTION + S>0 + LOCAL-COORDINATES |
| P05 | real orthonormal columns, injection e, strict r<card(I), finite basis extension | ORTHOGONAL-PRESCRIBED-COMPLETION |
| P06 | previous completion, det=+1 OR det=-1, unused column, diagonal sign flip | SO-PRESCRIBED-COMPLETION, full active columns |
| P07 | primitive X/RY/RZ/CNOT semantics, distinct controls, fixed other wires, chronological list convention | PRIMITIVE-UNITARITY + LIST-COMPOSITION |
| P08 | real SO matrix, signed pair rotations, adjacent sweeps, already-fixed columns, determinant final sign | ADJACENT-ELIMINATION + pair count |
| P09 | ordered elimination identity, inverse rotations, chronological order | EXACT-SO-ROTATION-LIST via reversed negated list |
| P10 | Gray adjacent-pair property, all-other-wire selection, ordered endpoint sign, coordinate conjugation | NAMED-WIRE-TWO-LEVEL-LIFT |
| P11 | half-sum/difference tables, two CNOTs, X RY X identity, recursive control reduction | SELECTED-ROTATION-LIST + S RY + 2(S-1) CNOT |
| P12 | P09, P10, P11, D=2S, S>=1, pair/list arithmetic | EXACT-SO-PRIMITIVE-LIST + length<=6S^3 + no oracles |
| P13 | actual-site ACTIVE-COLUMN-ISOMETRY specialized at B=S, local-coordinate injection, maxBond<=S, S>0 | active count<2S |
| P14 | P13, SO-PRESCRIBED-COMPLETION, P12, real coefficient embedding | LOCAL-CIRCUIT-EXISTS, same witness bounded and active-column exact |
| P15 | arbitrary real u, head A, slice/chain multiplication laws | BOUNDARY-CONTRACTION, no norm/canonical premise |
| P16 | mass(u)=1, A A^T=I, associativity and transpose product | ABSORBED-HEAD-CANONICAL |
| P17 | original chain, tail-first thin factorization, dimension recurrence, full-terminal mass identity, original unit scalar mass | CANONICAL-E + normalized u + exact amplitude + nonincreasing bonds |
| P18 | N>0, P17, P15, P16, original initial dimension one, original maxBond<=B | CANONICAL-SCALAR-D with original amplitudes and bound |
| P19 | LE recurrence, nonnegative bit values, q=0 base | ZERO-INTEGER-IFF-ALL-ZERO |
| P20 | P19, scalar boundary (1), zero fill into S, empty-circuit identity | ZERO-INITIALIZATION, zero instructions |
| P21 | finite bond bijection, transported local matrices, boundary transport, finite-sum reindexing | BOND-RUN-TRANSPORT, prefix unchanged |
| P22 | scalar-boundary D, maxBond<=S, t<N active-column equations, initial active support, output support, stage expansion, whole-chain induction | CONDITIONAL-SEQUENTIAL-ACTION + full terminal cleanup |
| P23 | P22 and empty scalar chain identity at N=0 | EMPTY-SEQUENTIAL-HELPER, no arbitrary signed-scalar absorption |
| P24 | head-first word recursion, first-coordinate basis recursion, empty base | WORD-BASIS-BIJECTION + Boolean list length |
| P25 | finite coordinate reversal, empty base | REVERSAL-INVOLUTION |
| P26 | LE append arithmetic, P24, reversal sends cons to append | SAMPLE-J-MSB-RECURRENCE + positive-width list-index identity |
| P27 | SAMPLE-J definition, P24, P25 | PUBLIC-INDEX-CANCELLATION J(word(rev x))=L(x) |
| P28 | primitive wire placement/lifting, passive prefix entries, list evaluation composition, stage induction | ONE-INTERNAL-LIST = sequential action |
| P29 | disjoint exhaustive public wire rename, primitive renamed semantics, P28, P22, P25 | PUBLIC-LOW-DATA-HIGH-BOND-ACTION with reversed data |
| P30 | primitive-preserving padding/lift/place/rename, empty initial list, concatenation lengths | EXACT-ASSEMBLED-LENGTH=sum stage lengths |
| P31 | P30, each executed stage length<=K, finite N-term sum | TOTAL-LENGTH<=N K, including N=0 |
| P32 | N>0, q natural, original scalar C, maxBond<=S, original unit square sum, P18, P14, finite stage choices, P20, P21-P22, P29-P31, primitive unitarity | ONE-PUBLIC-CIRCUIT: exact signed full state AND unitarity AND no oracles AND N*6S^3 length |

P06 has guarded determinant cases, not both signs required simultaneously.
The zero/nonzero pair cases in P08 are exhaustive OR-branches; both receive
the stated fixed-schedule count. Generic transported/conditional circuits and
the existential canonical route are different interfaces, not a false AND of
all source hypotheses for every helper. No alternative independently
sufficient end-to-end construction is claimed by this source.

Diagnostics are NOT proof nodes and no executable diagnostic was run:
DIAG-SPARE-COLUMN (fully prescribed det=-1 counterexample outside hypothesis),
DIAG-Q0-SIGNED (RY(2pi)|0>=-|0> demonstrates exact sign possible with a spare
column), DIAG-N0 (unique empty scalar-chain +1 versus arbitrary signed scalar),
DIAG-ENDIAN-N2 (a,b emission -> public b,a), DIAG-AFTER-SCHEDULE (zero table
not isometry on positive active rank), DIAG-LENGTH-WITNESS (same list for all
conjuncts, and zero-angle instructions still count).

## Exhaustive substantive source disposition

Blank lines are EXCLUDED(layout), line 1 EXCLUDED(title), and section headings
5/22/32/51/63/81/101/117/131/147 EXCLUDED(navigation). All substantive ranges:

| Lines | NODE disposition |
| --- | --- |
| 3 | RETROSPECTIVE-PROVENANCE / evidence boundary |
| 7 | P01 full chain/word carriers |
| 9–18 | P02–P03 real/support/isometry table and actual-site restriction |
| 20 | P04 LE coordinates and arbitrary injected active positions |
| 24–30 | P05–P06 full-column SO completion, spare counterexample, nonunique choice |
| 34–39 | P07 all primitive semantics and chronological lists |
| 41 | P08–P09 signed adjacent elimination, determinant, inverse order |
| 43 | P10 Gray transport and endpoint orientation |
| 45–49 | P11–P12 recursive selected list, exact count and cost exclusions |
| 53–59 | P13–P14 local existence, same produced columns/unitarity/bound |
| 61 | local q=0 and after-schedule boundary |
| 65–69 | P15–P16 norm/canonical hypotheses separated from contraction identity |
| 71–75 | P17 canonical-factor/full-mass supplier and normalized residual output |
| 77–79 | P18 signed first-head absorption, positive N and max-bound argument |
| 83 | P19–P20 all-zero initialization with zero list cost |
| 85–89 | P21 finite-label transport, arbitrary complex boundary, passive prefix |
| 91–97 | P22 conditional all-output sequential action and complete terminal cleanup |
| 99 | P23 zero-length conditional helper and signed-empty limitation |
| 103 | P24–P25 word/basis/list maps and reversal |
| 105–115 | P26–P27 MSB list samples, LE append, positive-width comparison and reversal cancellation |
| 119 | P28 one actual internal list by placement/lifting/composition |
| 121 | P29 public named-wire rename, not free physical SWAP; hardware boundary |
| 123–127 | P29 full public amplitude, arbitrary supplied stage columns, no canonicality premise |
| 129 | P30–P31 exact list sum/uniform bound/empty cases |
| 133–145 | P32 root inputs, one-circuit AND outputs, exact phase and positive route scope |
| 149–151 | exact-real gate model and stable stronger-consumer gaps below |

There are no external mathematical citations in the source requiring an
invented bibliography or external-paper attribution. Ordinary finite basis
extension, planar-angle existence and matrix/finite-sum laws are mathematical
dependencies, not evidence that any particular Lean implementation matches.

## Seven semantic slots and premise/output audit

| Key | Independent source contract |
| --- | --- |
| target | Original real normalized scalar-boundary C, positive length in complete existence route; exact full public amplitude delta(clean bond)*M_C(word(rev x)), not probabilities alone. Generic conditional helpers keep their broader chain scope. |
| normalization | Original unit all-word square sum is root SOURCE premise. Canonical residual unit mass, absorbed canonical head, and zero-input physical state are produced. No arbitrary boundary state is initialized for free. |
| registers | Natural/zero active bonds, q>=0, S=2^q>0; local low bond/high fresh bit; internal low bond/chronological data; public LOW data/HIGH bond with reversed chronological data. Word/list/LE maps are explicit. |
| oracles | Actual lists use RY/CNOT for SO construction, ambient X/RZ allowed. No oracle-call instruction; no supplied coherent data oracle, input producer, inverse/control/BE access contract. |
| ancillas_phases | Only q bond wires plus data/fresh site wires, no selected-rotation work ancilla; exact signed boundary absorbed; same circuit is fully unitary and output bond zero at every data/bond amplitude, not postselected. |
| error_success | Exact real angles and matrices; no global-phase quotient or probability-only target replacement. No finite precision/error/noise/success-amplification theorem. Full unitary state action has deterministic ideal cleanup, not an accepted-branch probability claim. |
| resources | Actual instruction count <=N*6*S^3 (same c); exact sum of executed stage lists, zero initialization and no implicit Gray/SWAP instructions. Not parameter computation/storage/runtime/finite-bit/connectivity/depth/readout or external-parameter polynomial scaling. |

TYPING includes finite real/complex carriers, dimension-matched chains and wire
positions. SOURCE logical inputs include canonicality for local existence,
actual-site restriction and max bond; orthonormal columns/injection/strict spare
dimension for SO completion; unit u plus canonical A for absorbed isometry;
positive N and original normalized C for the complete route; local active
columns for conditional action; and stage length bounds for generic sum bounds.
The same local facts are PRODUCED inside the root route and may not later be
moved into its public premises. STANDING dependencies are ordinary finite
linear algebra/real angles and primitive semantics. RULED corrections: none.
No EXCESS premise or mathematical weakening is needed in this natural source.

Literal definitions: cores, words, active table, L, coordinate maps, B_u,
reversal, J, matrix transports, primitive denotations, list lengths. Chosen
orthonormal completions, thin factors, planar angle representatives and finite
stage circuits are noncanonical existence witnesses. No false uniqueness or
efficient selection procedure is claimed. Exact output amplitudes are
representative-independent only under the explicitly supplied column/action
relations; arbitrary completions need not agree on unused inputs.

## Stable open source/consumer gaps

These remain OPEN and do not refute the finite exact-real existence result:

- `SOURCE_GAP-C26-INPUT-TARGET`: actual concrete sampled-data/core producer,
  pointwise desired-amplitude theorem and matching original normalization.
- `SOURCE_GAP-C26-DETERMINISTIC-PARAMETERS`: deterministic factor/completion/
  angle and instruction-data producers refining the existential choices,
  including input access, storage, copying, arithmetic and actual runtime.
- `SOURCE_GAP-C26-FINITE-PRECISION`: stable finite-bit approximation, real-angle
  evaluation, finite gate-alphabet synthesis and accumulated state/operator error.
- `SOURCE_GAP-C26-HARDWARE-RESOURCES`: physical connectivity/routing,
  hardware/parallel depth, actual space/readout and complete resource model.
- `SOURCE_GAP-C26-ORACLE-BE-TRANSPORT`: coherent data/oracle/inverse/control
  interfaces, SELECT/unprepare, block encoding and accepted-branch/amplification
  transports with their complete AND prerequisites and resource costs.
- `SOURCE_GAP-C26-SCIENTIFIC-SCALING`: relating N and q to an external input
  family and proving appropriate resource scaling; cubic in 2^q is not a
  generic polynomial-in-q or scientific-input theorem.

The c25 missing ideal unitary realization, word/wire and scalar cleanup bridges
are not blindly copied as open c26 gaps: this source explicitly constructs
their mathematical exact-real counterparts, at the source's stated scope.
Whether the three as-yet-unseen formal targets implement these constructions
is an UNREVIEWED FORMAL COMPARISON, not a newly manufactured source gap.

SP-to-BE requires AND{this SP, appropriate coefficient/phase model, SELECT,
inverse/unprepare, clean-register semantics, matched resource accounting}.
BE-to-SP requires AND{BE, prepared input, nonzero accepted branch, normalization,
postselection/amplification analysis}. Neither direction is supplied just by
this exact state-preparation existence or by its sample-index bijection.

## Phase-1 verdict

No mathematical error was found in S1–S10 under their explicit per-result
scopes. The signed pair-angle, determinant correction, q=0, N=0 versus N>0,
support/terminal cleanup, reversal and same-list bound checks above are natural
mathematical derivations, not finite executable or Lean verification. The
32-edge independent construction table is source topology only; no target
declaration mapping or formal implementation graph has been inspected.

Failure class: NONE for the limited natural mathematics. All stronger-consumer
gaps remain OPEN. No route is refuted, no source repair or salvage is needed.
No formal agreement/Proof Seal, compiler/decoder acceptance, canonical/main/
reader/ROOT claim or purification is made. Freeze these notes and phase-1
seal; wait for separate authorization before any three-target semantic read.
