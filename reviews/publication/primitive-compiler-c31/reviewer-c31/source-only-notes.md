# Primitive compiler c31: independent source-first phase1 notes

## 0. Scope, provenance, and stopping rule

This is an independent mathematical reconstruction of `$AUTHOR/source-only.md`, sections S1–S10, using no implementation mathematics. The source SHA256 actually read is `5907262565b6202fec61b189c42d942cb84d6215223a0da4211d63b92d3ad168`, matching the assigned digest. The source is a parent-authored, retrospective, implementation-informed local mathematical account. Its historical formalizer is UNKNOWN. It is not an external-paper reproduction, novelty evidence, historical pre-proof seal, or compiler certificate.

Reviewer identity: `/root/primitive_compiler_source_first_c31`. Source authoring agent: `/root`. This establishes separation from this local source authoring act only; historical implementation authorship has not been established. No claim about independence from an UNKNOWN historical formalizer is made.

The reviewer fully read the seven assigned process documents and the complete mathematical source. Process documents were used only as process instructions, not mathematical evidence. The two selected skills require explicit source coverage, binder/definition classification, and keeping mathematical proof ingredients as dependency edges. They do not authorize crossing the assigned phase boundary.

No actual Lean source, author-private-coverage, source-freeze, other author files, graph, atlas, registry, decoder/reviewer artifacts, CI, compile records, caches, runtime evidence, external mathematical sources, other chats, Git, network, Lean, or subagents were used. Only the two files in `$REVIEWER` are authored. The mathematical source bytes were not changed.

Conclusion at this layer: the stated exact-matrix mathematics can be reconstructed, with the representational/certificate gaps below retained. This is neither native acceptance, formal acceptance, proof sealing, root closure, main admission, nor PURIFIED status. Stop after hashing the two phase1 artifacts; actual formal signatures, axioms, implementation correspondence, and builds require separate phase2 authorization.

## 1. Independent reconstruction: S1 and S2

Let Bq be the finite set of functions from q named wires to {0,1}. A matrix entry U[r,c] has output r and input c. Temporal execution A then B gives BA, not AB. A stored phase phi denotes exp(i phi) times the ordered product. Splitting a target t gives a bijection Bq with pairs (s,x), where s is the target bit and x assigns all other wires. A fixed one-qubit lift has entries

    L(A)[(s,x),(u,y)] = [x=y] A[s,u].

In the product L(B)L(A), the sum over (v,z) is zero unless x=y=z, and the remaining sum over v is (BA)[s,u]. Hence L(B)L(A)=L(BA); also L(lambda A)=lambda L(A). For context-dependent blocks Bx and Ax the same calculation gives block (Bx Ax), not a product involving a changed context. This is the exact algebra needed later; no flat integer bit order was used.

Write k=sqrt(2)/2. Direct substitution gives Rz(pi)=diag(-i,i) and Ry(pi/2)=[[k,-k],[k,k]]. Their product is [[-ik,-ik],[-ik,ik]], so multiplying by i gives H=[[k,k],[k,-k]]. Likewise exp(i theta/2)Rz(theta)=diag(1,exp(i theta)). At theta=pi/4 and -pi/4 these are T and inverse-T. The claimed lists have precisely this chronological order, and their stored phases supply i, exp(i pi/8), and exp(-i pi/8). The lifting calculation extends each identity to all named wires.

Negative discriminators, not simulator output:

- Ry(pi/2)[0,1]=-k, whereas H[0,1]=k.
- Phase-free Rz(pi/4)[0,0]=exp(-i pi/8), whereas T[0,0]=1.
- The H list without its stored phase evaluates to -i H, not H.
- A phase that is global on a standalone gate becomes relative between a controlled branch and its complement if one naively controls only the phase-free body. Exact phases therefore cannot be discarded in a reusable controlled construction.

These are exact complex matrix equalities, not equivalence classes modulo phase. The existence of symbolic real-valued angle data alone does not specify an approximation or serialization algorithm.

## 2. Independent reconstruction: S3 monomial algebra

For a finite index set, define M(p,sigma)[r,c]=p(c) when r=sigma(c), and zero otherwise, with sigma a permutation. If L executes before R, then

    (M_R M_L)[r,c]
      = sum_k [r=sigma_R(k)] p_R(k) [k=sigma_L(c)] p_L(c)
      = [r=sigma_R(sigma_L(c))] p_L(c) p_R(sigma_L(c)).

This proves the chronological formula, with no unit-modulus assumption and no invertibility requirement on p. The order of the phases matters through their arguments even though the scalar multiplication commutes. Controlled-X with distinct control and target is a phase-one monomial permutation. P(theta) on t has identity permutation and phase exp(i theta b_t).

If a primitive-program equality is stored in a refinement, its sequential constructor must combine both stored equalities with this multiplication formula and the actual temporal program-evaluation law. It cannot certify an unrelated target by merely storing p and sigma. For a unitary primitive program, equality to M would imply |p(c)|=1, since column c has norm |p(c)|; this is a consequence, not a premise of the general multiplication identity.

Counterexample to automatic unitarity: on a singleton, p=2 gives M=[2] and M* M=[4]. The p=0 case is singular. Thus an added unit-modulus binder on the general monomial multiplication theorem would be unnecessary drift; removing the equality proof from a proof-carrying refinement would also be drift.

## 3. Independent reconstruction: S4 exact phase network and CCX

Assume a,b,t pairwise distinct. Write initial bits as a,b,t as well. After the four target flips, the target sequence at the phase gates is t xor b, t xor b xor a, t xor a, and t; b stays initial until the later a-to-b pair. The successive T exponents, in units pi/4, are

    -(t xor b), +(t xor b xor a), -(t xor a), +b, +t, +a, -(b xor a).

The last term sees b xor a because it occurs between the two a-to-b flips. All flipped wires are restored, so the permutation is identity. The total E is exactly the displayed source expression.

Independent eight-case evaluation:

| (a,b,t) | E |
| --- | ---: |
| (0,0,0) | 0 |
| (0,0,1) | 0 |
| (0,1,0) | 0 |
| (0,1,1) | 0 |
| (1,0,0) | 0 |
| (1,0,1) | 0 |
| (1,1,0) | 0 |
| (1,1,1) | 4 |

An independent symbolic route uses x xor y=x+y-2xy and

    t xor b xor a = t+b+a-2tb-2ta-2ab+4abt.

Substitution cancels every linear and quadratic term, leaving 4abt. Thus the network phase is exp(i pi abt), equal to -1 only at 111. Exact T/inverse-T macro semantics, including their stored phases, are needed to identify these exponents as the literal phase gates. The middle circuit has four T and three inverse-T occurrences, six controlled-X occurrences, and no net permutation.

For fixed other-wire context, set k=ab. The middle target block is diag(1,(-1)^k), namely I if k=0 and Z if k=1. Direct multiplication of H gives H squared=I and HZH=X. Temporal H–middle–H therefore gives I or X on t, with every context bit preserved and with no residual phase. This proves the exact CCX matrix, including its action on arbitrary superpositions by linearity.

The block identity itself needs only a!=t and b!=t: if a=b it still describes a conjunction of the same context bit. The literal displayed phase network requires a!=b as well, because it includes CX(a,b). With a=b, the ordinary controlled-flip rule would send the same bit 1 to 0 and 0 to 0; it is not a permutation. That is a concrete reason not to weaken the final network binder or unnecessarily strengthen every intermediate block lemma.

This derivation gives elementary-macro semantics. It gives neither scheduling/connectivity results nor finite-bit rotation synthesis. No CCX theorem is needed by the controlled-Ry or cubic route below.

## 4. Independent reconstruction: S5 and S6 context specification and recursion

Take n control positions, a map w from positions to q named wires, a target t, and w(j)!=t for all j. Do not assume injectivity. A context x on all wires other than t determines the tuple u_x=(x(w(0)),...,x(w(n-1))). Define independently of a circuit

    C_theta[(s,x),(v,y)] = [x=y] Ry(theta(u_x))[s,v].

This is literal block-diagonal semantics on every assignment. Only physically consistent control tuples occur when w repeats wires. For n=0, the unique tuple is empty and this is exactly a one-qubit lift. A valid CX(h,t) has context block I if x(h)=0 and X if x(h)=1. These are matrix-entry facts, not promises from a recursive definition.

At a recursion step, h=w(0), tail controls are the remaining positions, and

    alpha(u)=(theta(0,u)+theta(1,u))/2,
    delta(u)=(theta(0,u)-theta(1,u))/2.

Both tail calls still avoid t. The emitted temporal list is P_alpha; CX(h,t); P_delta; CX(h,t). List evaluation and induction on the two emitted recursive lists give the recursive matrix product

    CX(h,t) U_delta CX(h,t) U_alpha.

That equality alone is not the independent specification theorem. To prove the latter, fix the complete context x. Both recursive calls and both CX gates leave x unchanged. By the induction hypothesis, on this block the calls act by Ry(alpha(u_x)) and Ry(delta(u_x)). Put A=alpha(u_x)/2 and D=delta(u_x)/2; ordinary sine/cosine addition directly gives Ry(delta)Ry(alpha)=Ry(alpha+delta). Direct entry multiplication also gives X Ry(delta) X=Ry(-delta). Therefore:

- If x(h)=0, the target block is Ry(delta)Ry(alpha)=Ry(theta(0,u_x)).
- If x(h)=1, it is X Ry(delta) X Ry(alpha)=Ry(alpha-delta)=Ry(theta(1,u_x)).

These are exact matrix identities. Reassembling the context blocks proves the compiler equals C_theta. No branch gets an untracked phase. The base case has one Ry, the angle at the empty tuple, and no controlled-X. Induction also proves every non-target bit is preserved throughout the entire emitted program and the global stored phase remains zero if the compiler constructor uses zero-phase leaves and phase-additive composition.

Noninjective-control discriminator: n=2 with w(0)=w(1)=k!=t. Physical contexts only access theta(0,0) and theta(1,1). The first recursive rotation still reads the same stable bit k; the two X gates affect t, not k. The preceding two-case proof remains valid for u_x=x(k), even though u_x is correlated with x(h). Values theta(0,1) and theta(1,0) may be changed arbitrarily without changing the specified physical matrix. They cannot be advertised as independently addressable inputs. Requiring Injective(w) for the full theorem would be an EXCESS restriction absent from this source.

Target-overlap discriminator: if w(0)=t, the context cannot even read this wire. A naive basis-column choice theta(0)=0 and theta(1)=pi would send both target basis vectors to the same output up to sign, so it is not a unitary controlled block. The avoidance condition is mathematically substantive, not merely an API issue.

## 5. Independent reconstruction: S7 resource recurrence

With no cancellation or optimization pass, the emitted lists satisfy

    r(0)=1, c(0)=0;
    r(n+1)=2r(n), c(n+1)=2c(n)+2.

Induction gives r(n)=2^n and c(n)=2(2^n-1): the successor c is 4(2^n-1)+2=2(2^(n+1)-1). The total emitted length is 3*2^n-2. At n=2 this is four Ry, six CX, length ten; at n=5 it is 32 Ry, 62 CX, length 94. These are literal reference-list counts, not optimality results.

The primitive instructions in this construction contain only Ry and CX, so opaque oracle instructions occur zero times. This does not count the work needed to obtain angle values. The generic input table has 2^n entries, and the output length is already exponential in the number n of control positions. If repeated wires reduce the number k of independent physical control bits, the reference list still has 2^n Ry; one must not silently substitute k for n or infer an optimization. The source's independent-control exponential claim is valid in the injective-control regime, which is the usual worst case.

No storage/caching, classical arithmetic or transcendental evaluation, finite-bit precision, T-count, depth, routing, or family-wide oracle construction cost follows. A finite angle data object with real evaluation is not itself a runtime theorem.

## 6. Independent reconstruction: S8 finite two-control cubic circuit

Here, and only here, fix named wires 0 and 1 as system bits and wire 2 as signal. Read j=b0+2b1. On j=0,1,2,3 the values (j/4)^3 are respectively 0,1/64,1/8,27/64, each nonnegative and at most one by exact rational arithmetic. Casting these inequalities into the real field does not change them. Set theta_j=2 arccos(d_j), with principal real arccos. Then theta_j/2=arccos(d_j), so cos(theta_j/2)=d_j. Its sine is nonnegative and its square is 1-d_j^2; hence sin(theta_j/2)=sqrt(1-d_j^2). The sign is not optional: cosine alone would not determine the desired positive signal amplitude.

Using the control tuple (b0,b1), let A=theta_0, B=theta_1, C=theta_2, D=theta_3. The recursion expands into the following ten temporal instructions, all with global phase zero:

    Ry_2((A+B+C+D)/4), CX(1,2),
    Ry_2((A+B-C-D)/4), CX(1,2), CX(0,2),
    Ry_2((A-B+C-D)/4), CX(1,2),
    Ry_2((A-B-C+D)/4), CX(1,2), CX(0,2).

This expansion is independently derived from S6, not read from an implementation. A formal implementation must match the angle-table bit order; swapping control roles without the corresponding table permutation changes the target values at j=1 and j=2 (1/64 versus 1/8).

The full target block at system value j is

    [[d_j, -sqrt(1-d_j^2)], [sqrt(1-d_j^2), d_j]].

Thus zero signal gives exactly the advertised state action; one signal gives the other column, with its minus sign. In particular j=0 gives Ry(pi)=[[0,-1],[1,0]], not X: a truth-table-only or zero-input-only annotation would miss that relative sign. The positive signal amplitudes on j=0,1,2,3 are 1, sqrt(4095)/64, sqrt(63)/8, and sqrt(3367)/64 respectively.

This is a four-value theorem, not arbitrary-width sampling evidence. The full compiler proof supplies the full matrix, while the rational check and arccos facts identify the numerical target exactly.

## 7. Independent reconstruction: S9 encoding, clean extraction, and LE adapter

Define E(s,j) by bits (j mod 2, floor(j/2) mod 2, s), for s in {0,1} and 0<=j<4. For j=0,1,2,3 the first two bits are 00,10,01,11. Therefore decoding b0+2b1 recovers j. Two E(s,r), E(v,c) have the same non-signal context precisely when r=c; this does not require s=v.

Insert these facts in the independent controlled-block entry formula. If r!=c the entry is zero, while if r=c and s=v=0, the entry is Ry(theta_r)[0,0]=d_r. Hence

    U[E(0,r),E(0,c)] = [r=c] (r/4)^3.

The same argument gives the entire signal-block formula, not just the clean sector. Named-wire-to-flat little-endian indexing is F(b)=b0+2b1+4b2. Its inverse on 0<=k<8 uses bits k mod 2, floor(k/2) mod 2, and floor(k/4) mod 2. Quotient/remainder reconstruction proves the inverse; equivalently the images E(0,j), E(1,j) are the eight distinct integers j and j+4. In particular F(E(s,j))=j+4s. This is the concrete adapter behind the displayed tensor-like notation. A different conventional tensor ordering must not replace it silently.

Let P denote the permutation matrix of this basis equivalence. Reindexed U is P U P inverse. Since P inverse=P adjoint, U adjoint U=I implies the reindexed matrix is unitary, and the clean entries transport to flat indices r,c in 0..3. There are two independent mathematical ways to supply U's unitarity:

1. Each valid primitive is unitary: X is an involutive permutation, Ry is real orthogonal by cos squared+sin squared=1, Rz has unit-modulus diagonal, valid CX is an involutive permutation, and any stored real phase has modulus one. Products are unitary.
2. Each context block above is Ry(theta_j), hence unitary; distinct contexts do not mix. The context-sum product therefore gives U adjoint U=I directly.

The second is an independent mathematical cross-check, not evidence of which route an implementation uses. Either route plus the correct basis equivalence and clean entries supplies a block-encoding witness with normalizer 1, two system qubits, one signal qubit, no extra pure workspace, and no discarded context garbage. No assertion of a unique dilation is warranted: many unitaries can have the same clean block, but this program constructs one explicit U.

Counterexamples to stronger interpretations:

- D2 has diagonal 0,1/64,1/8,27/64. Its rank is three, not one, so it is not a rank-one state-loader.
- D2 is not unitary: it annihilates the j=0 basis vector, and D2 adjoint D2 has diagonal 0,1/4096,1/64,729/4096. Its operator norm is 27/64.
- The vector of these four d_j has squared norm 397/2048, not one. A unitary dilation is not a normalized-state preparation certificate for this vector.
- Signal-zero success on input j=0 is zero. There is no input-independent positive success lower bound. On the normalized uniform system input, the signal-zero probability is 397/8192; a later normalized-state claim would have to supply the input, nonzero probability, and normalization/amplification argument explicitly.
- Angle placeholders with gate kinds and wire numbers do not determine a runnable angle-complete QASM circuit, even though the mathematical exact-angle list is well-defined.

The emitted resource tuple and zero oracle field are source-level expectations. A wrapper must contain the actual unitary and clean-entry propositions with proofs, not merely metadata true. Whether actual definitions enforce this is uninspected. No native or executable acceptance follows from this notes file.

## 8. Exhaustive source disposition inventory

Every substantive source region is assigned below. Multiple displayed equalities in one region are explicitly included in its NODE. NODE means a source obligation/construction region, not formal acceptance.

| ID | Anchor and complete disposition |
| --- | --- |
| X00 | Opening provenance paragraph: EXCLUDED from mathematical premises; retained as process/provenance limitation. |
| N01 | S1 paragraph 1: NODE basis carrier, matrix direction, temporal order, stored phase, exact-angle boundary. |
| N02 | S1 displayed Ry/Rz/X matrices and exact phase/endianness paragraph: NODE literal primitive semantics. |
| N03 | S1 target/context paragraph: NODE splitting, unchanged-context entries, multiplication/scalar lifts. |
| N04 | S2 displayed H and P definitions and displayed resulting matrices: NODE exact local macro identities. |
| N05 | S2 program/phase paragraph: NODE chronological full-register H/T/inverse-T equalities and phase counterexamples. |
| N06 | S3 displayed M definition and its generality paragraph: NODE arbitrary complex monomial matrix, not automatically unitary. |
| N07 | S3 chronological composition formula and collapsing-sum proof: NODE monomial composition. |
| N08 | S3 controlled-X/P descriptions and proof-carrying program paragraph: NODE primitive monomials and refinement composition; unrelated-contract boundary. |
| N09 | S4 displayed 13-step middle network: NODE literal temporal circuit, all stages retained. |
| N10 | S4 restoration paragraph and displayed E: NODE identity permutation and exact accumulated phase. |
| N11 | S4 eight-case/XOR alternatives and -1 diagonal conclusion: NODE phase-polynomial identity and exact CCZ. |
| N12 | S4 H-conjugation paragraph: NODE H squared, HZH, unchanged-context composition, exact CCX primitive refinement. |
| N13 | S4 final paragraph: NODE distinctness hierarchy and no new approximation/connectivity/asymptotic resource theorem. |
| N14 | S5 first paragraph: NODE independent controlled-Ry context specification with target avoidance and repeated wires allowed. |
| N15 | S5 second paragraph: NODE consistency locus, empty controls, lifted Ry, controlled-X context blocks. |
| N16 | S6 base/recursion paragraph and alpha/delta display: NODE recursive literal compiler and well-typed tails. |
| N17 | S6 recursive-matrix paragraph: NODE emitted-evaluation to recursive-formula identity with reverse matrix order. |
| N18 | S6 context-proof paragraph: NODE independent-spec induction, both control cases, rotation addition, X conjugation, exact phases, no injectivity need. |
| N19 | S7 recurrence paragraph and count display: NODE both recurrences, solutions, five-control specialization. |
| N20 | S7 remaining paragraph: NODE zero opaque oracle count and exponential/exact-real cost exclusions. |
| N21 | S8 fixed-wire/LE paragraph and d_j display: NODE finite four-point cubic definition and [0,1] rational bounds. |
| N22 | S8 exact-angle/phase paragraph: NODE theta_j=2 arccos(d_j), two-control instantiation, zero explicit global phase. |
| N23 | S8 full-matrix and displayed state-action paragraph: NODE cosine and positive-sine identification, exact signal-zero action. |
| N24 | S8 last paragraph: NODE actual signal placement, finite rational-to-real casts, no arbitrary-width inference. |
| N25 | S9 encoding paragraph and clean-entry display: NODE E(s,j), control recovery, context iff, clean block D2 rather than rank-one loader. |
| N26 | S9 unitarity sentence: NODE full ambient unitary versus contractive clean block. |
| N27 | S9 LE-equivalence/reindex paragraph: NODE flat j+4s adapter, unitarity transport, normalization/dimensions/workspace and actual-proof wrapper. |
| N28 | S9 presentation/resource paragraph: NODE placeholders, definitional emitted resources, zero oracle, 4 Ry/6 CX, and excluded stronger certificates. |
| N29 | S10 first paragraph: NODE three distinct paths and absence of macro-path dependency in the cubic proof. |
| N30 | S10 helper paragraph: NODE prepend/half-sum/half-difference/base-block/CX-block providers and cast/phase/consistency boundaries. |
| N31 | S10 open-consumer paragraph: NODE explicit unproved efficient-general-cubic, structured Hermite, finite-bit, state/success, total resource and executable-family boundaries. |
| X01 | Title and section headings: EXCLUDED as navigation, no independent mathematical propositions. |
| X02 | External citations: EXCLUDED because there are none in the mathematical source; no external theorem was silently imported as source authority. |

## 9. Complete source dependency AND/OR structure

The following are source-level hyperedges. Each brace is one complete AND tail; no individual member is independently sufficient. Section 1–7 above supplies the actual mathematics for each edge. The package root is an inventory conjunction of distinct results, not an assertion that each route proves the others.

### Shared base

    {N01,N02, finite target/context bijection} -> N03
    {N06, finite matrix-product sum} -> N07

### Exact elementary macro/CCX route

    {N02, exact trigonometric/exponential substitution} -> N04
    {N01,N03,N04, stored-phase arithmetic} -> N05
    {N02,N05,N06, valid CX permutation} -> N08
    {N07,N08,N09, chronological wire-stage transcript} -> N10
    OR-E: [eight-case proof] OR [XOR polynomial expansion] -> E=4abt
    {N10,E=4abt, exp(i*pi)=-1} -> N11
    {N03,N05,N11,H^2=I,HZH=X, pairwise distinct a,b,t} -> N12
    {N12, weaker-block/stronger-network distinction} -> N13

The macro route's root is N12 with the limitations N13. Either E proof is sufficient; they are not a false AND requirement.

### Controlled-rotation semantic route

    {N01,N02,N03, control-target avoidance} -> N14
    {N03,N14, unique empty tuple, CX basis rule} -> N15
    {exact angle half-sum/half-difference, prepend-bit decomposition} -> N16
    {N01,N16, base list evaluation, two tail induction equalities} -> N17
    {N03,N14,N15,N16, two recursive-spec hypotheses,
      Ry addition, X*Ry(delta)*X=Ry(-delta), alpha+delta=theta0,
      alpha-delta=theta1, context preservation} -> recursive-spec identity
    {N17,recursive-spec identity} -> N18
    {N16, list-count additivity, base counts} -> N19
    {N16,N19, instruction-kind inventory} -> N20

N17 alone does not imply N18. The count path N19–N20 is not a premise of semantic equality N18, nor is semantic equality enough to prove those literal list counts.

### Finite cubic and LE-clean-block route

    {fixed wires, j=b0+2b1, four exact rational evaluations} -> N21
    {N21, literal angle-table definition, arccos real-domain facts} -> N22
    {N18,N21,N22, positive-sine derivation, rational-real-complex casts} -> N23
    {N21,N23, fixed named-wire interpretation} -> N24
    {N14,N23, encoding inverse, context-equality iff} -> N25
    OR-U: [valid primitive unitarity + program product/phase laws]
          OR [unitary Ry blocks + context decomposition] -> N26
    OR-LE: [eight finite encodings] OR [binary quotient/remainder inverse]
          -> LE basis equivalence
    {N25,N26,LE basis equivalence, reindex transport,
      fixed dimensions/normalizer/workspace} -> mathematical certificate N27
    {N16,N19 at n=2, emitted-kind inventory, presentation definition} -> N28

N27 has the whole AND tail: clean entries without unitarity, or unitarity without the correct clean target, do not suffice. N12 is not in this cubic tail. N28 is separate presentation/resource evidence, not a substitute for N27. Exact state action N23 has a clean-block consumer N25; it does not by itself prove normalized state preparation.

### Scope and roots

    {macro root N12/N13, compiler root N18/N20,
      finite cubic root N27/N28, genuine nondependency distinctions} -> N29
    {N15,N16,N18, internal-provider classification, cast boundaries} -> N30
    {N13,N20,N24,N27,N28, absence of stronger premises/proofs} -> N31
    {N29,N30,N31} -> source package coverage root

There is no source-supplied alternative scalable compiler, Gray-code optimization, efficient Hermite path, or complete finite-bit emitter. Those are not OR routes available for source closure. The three headline paths prove different contracts and therefore must not be treated as interchangeable OR witnesses for one target.

## 10. SOURCE_GAP ledger and formal boundaries

All mathematical equalities used above have been independently derived. The following missing representation/implementation bridges must remain explicit rather than being supplied by author self-assessment:

| ID | Source gap or unexpanded bridge | Phase1 treatment and remaining obligation |
| --- | --- | --- |
| SG1 | S1/S6/S8 mention symbolic exact angles but do not define their syntax, evaluators, closure under halving/addition/negation/arccos, or evaluation equations. | Real-valued extensional mathematics is reconstructed. Whether the actual angle datatype represents these values and operations with these evaluations is unknown until phase2; no bit algorithm follows. |
| SG2 | S9 invokes the generic unitary evaluation of primitive programs without exposing validity enforcement for arbitrary named CX wires. | Unitarity is derived here for the present valid gates and, independently, for controlled-Ry blocks. Actual primitive typing/validity and the generic theorem's binders must be inspected in phase2. The same-wire CX counterexample forbids silently generalizing to invalid gates. |
| SG3 | S9 references a separately proved LE equivalence and encoded-context facts without supplying detailed proofs. | Explicit inverse and all four/two-signal encodings are reconstructed here. Actual equivalence direction, reindex convention, and flat clean-block signature remain uninspected. |
| SG4 | S3/S9 claim proof-carrying refinement/certificate wrappers but do not give the complete logical types or recursive expansion. | Expected substantive propositions are recorded here; actual hidden binders, fields, equality direction, normalization, and no-Boolean-only closure must be audited in phase2. |
| SG5 | S7/S9 say the resource row is definitionally the emitted resource and has oracle-call zero. The actual resource datatype and presentation emitter are absent. | Literal mathematical counts are proved. Actual resource fields, definitional identity, discarded angle data, and emitted presentation require phase2 inspection. |

SG3's omitted mathematical bridge is filled by this reviewer; this does not retroactively certify an implementation. SG1/SG2/SG4/SG5 do not refute the abstract source identities, but prevent treating this retrospective text as a formal/compiler certificate. The source explicitly excludes efficient general arithmetic, polynomial Hermite, finite-bit synthesis, complete runtime/storage/depth/connectivity, state normalization/amplification, and executable family acceptance: these are N31 boundaries, not fabricated missing proofs of claims the source made. No mathematical route is retired.

## 11. Expected binder audit for a later formal comparison

These are mathematical interface expectations, not guessed Lean declaration names or signatures. Actual formal signatures have NOT been read, so there is no sealed formal signature digest.

| Contract | Expected data/premises and classification | Must not be smuggled in as source-anchor premises |
| --- | --- | --- |
| One-qubit macro equality | q and t in q wires: TYPING; exact matrix/phase/temporal conventions: STANDING. | Macro equality itself, phase correction, gate evaluation result, unitary witness. |
| Monomial multiplication | Finite index carrier, sigma_L/sigma_R permutations, complex p_L/p_R: TYPING/literal data; source permits arbitrary phases: SOURCE scope. | |p|=1, nonzero p, program realizability. |
| Internal monomial refinement constructor | Program/p/sigma and its actual equality proof are fields of a proof-bearing INTERNAL PROVIDER. | Moving its desired final oracle/circuit contract into a public Anchor as an assumption. |
| CCX exact displayed network | q,a,b,t: TYPING; all three pairwise distinct: SOURCE. | H/T/network/CCX correctness assumptions; a metadata Boolean; a theorem only modulo phase. |
| Intermediate context HZH/CCX block | a!=t,b!=t: SOURCE/valid-context conditions, with no need for a!=b. | Unnecessary pairwise distinctness inherited from the final network. |
| General controlled-Ry specification/compiler | n,q,w,t, arbitrary exact-angle table: TYPING/literal data; every w(j)!=t: SOURCE. | Injective(w), pre-proved compiler equality, pre-proved block identity, normalized input, restrictions to accessible tuples only in the theorem carrier, or zero-control exclusion. |
| Reference costs | n and the fixed literal compiler definition: TYPING/literal data. | Cost recurrence as an external hypothesis; polynomial cost; free angle-generation oracle. |
| Finite cubic source Anchor | Exactly two system bits and one signal bit, fixed d_j and theta_j, fixed little-endian encoding: literal definitions/STANDING convention. | Amplitude [0,1] premise, arccos identity premise, compiler correctness premise, unitary witness premise, clean-block correctness premise, assumed basis equivalence, accepted certificate flag. These must be produced as dependencies. |
| LE transport/certificate | Constructed equivalence and explicit U, normalizer one, fixed register counts: literal data/derived provider outputs. | Unproved unitarity/clean equality packaged into an opaque public input; uniqueness of the dilation; state-preparation success. |

RULED corrections: none authorized. EXCESS binders: none added by the reconstruction; actual Lean EXCESS status is UNKNOWN. The target-avoidance premise is source-explicit and necessary, not a repair. No source-wide contract bundle has been read beyond the source text; recursively expanding actual project-owned Prop/typeclass/structure aliases is a phase2 obligation.

## 12. Definition audit expectations

- Basis assignments, target/context split, matrix lifts, Ry/Rz/X, P/H products, M(p,sigma), independent controlled-Ry blocks, alpha/delta tables, recursive list, counts, d_j, encoding, and LE map are literal. Their actual bodies must match on the whole stated carrier, including empty controls and repeated wires. No out-of-locus default may invent behavior.
- Principal real arccos and nonnegative square root select explicit conventional real functions. The positive-sine argument is a theorem, not a new choice or assumed branch sign. The [0,1] bound is derived on all four finite inputs.
- A proof-carrying monomial refinement/certificate is a literal constructed proof-bearing package, not a Boolean characterization or unique-choice object. If actual code chooses a witness from a characterization, existence and the actual characterization must be proved first; there is no unique unitary extension of a clean block in the source.
- The LE basis equivalence is literal finite bijection data with both inverse laws. It is not an unrecorded identification of tensor and integer order.
- There are no quotient/global-phase classes in the claims. Exact representatives are fixed. Replacing equality by phase equivalence is contract drift, even if measurement probabilities agree.

## 13. Seven semantic slots and their exact boundaries

| Slot | Preserved source contract | Unproved/excluded stronger interpretation |
| --- | --- | --- |
| 1. Target and normalization | Exact H/T/inverse-T/CCX matrices; independent controlled-Ry full matrix; D2=diag(0,1/64,1/8,27/64), normalizer 1. | No normalized desired state or rank-one loader; D2 is not unitary. |
| 2. Dimensions, scalars, basis/order | Finite complex matrices, real evaluated angles, named wires first; finite cubic has system wires 0/1 and signal 2, j=b0+2b1, flat j+4s. | No implicit global integer endianness for generic named wires; no arbitrary-width cubic theorem. |
| 3. Access, controls, inverses | Literal X/Ry/Rz/CX primitives; all control wires avoid target; repeated control wires allowed; inverse-T exact; angle tables are mathematical input data. | No coherent arithmetic/oracle producer or free parameter lookup; inaccessible inconsistent tuples are not physical inputs. |
| 4. Ancillas/workspace/garbage | Compiler changes only target, preserving complete context; finite cubic uses one signal and no extra pure workspace; signal may be one outside clean sector. | No deterministic success claim from clean block; signal is not promised to end zero on arbitrary input; no unspecified dirty-workspace cleanup. |
| 5. Phase | Full complex equalities; macro phases retained; recursive compiler/final finite circuit have explicit zero global phase; relative sign in the signal-one column retained. | Not merely probability equivalence, equality up to global phase, or classical CCX truth tables. |
| 6. Norm/error/success | Ideal exact arithmetic and exact entries. Signal-zero amplitude for basis j is d_j; its probability is d_j squared. | No uniform numerical error bound, statistical confidence, prepared-state normalization, positive success for all inputs, or amplification certificate. |
| 7. Resources/model | Exact-real reference counts r=2^n, c=2(2^n-1); finite n=2 gives 4/6; zero stored opaque oracle instructions. | No finite-bit/Clifford+T, classical preprocessing/storage, depth/connectivity, readout, polynomial Hermite, optimized Gray-code, or independent executable-family guarantee. |

## 14. Handoff and phase boundary

Objective/frontier: independently reconstruct all S1–S10 mathematics without implementation shaping the source story. Delta: complete derivations, discriminating counterexamples, exhaustive coverage, distinct path roots, explicit AND/OR, source gaps, binder/definition expectations, and seven-slot preservation map. No production files changed.

Named evidence: this derivation and its bound source digest only. Lean roots/tests/axioms/imports: UNKNOWN, not inspected. Formal signature digest: null. Executable or finite simulator evidence: none. The eight Boolean cases and four rational values above are mathematical case proofs, not runtime evidence.

Failure class: NONE for the reconstructed abstract identities; representation/certificate gaps are open boundaries rather than implementation failures or theorem refutations. Salvage: exact macro, monomial, context-compiler, count, and finite-encoding arguments are useful candidate fragments but have not been formally admitted. Process-memory IDs consulted: none, by the source-only boundary.

Direction fingerprint: source-only independent phase/context/order/resource reconstruction for primitive compiler c31. Expected information gain: reveal source-level semantic drift before any implementation anchoring. No children were spawned. Other workers' conclusions were not read. The two local alternative proofs for phase arithmetic and unitarity are mathematical cross-checks, not a completed formal multi-route common-blind-spot gate or a verified-construction comparator. No default formally verified route has been selected.

Purification and Exposition Seal: NOT PERFORMED. Source expansion nodes are N01–N31; implementation expansion nodes are UNKNOWN. Remaining safe next action is to wait for separate formal phase2 authorization and then compare actual signatures/definitions/axioms and implementation correspondence to this frozen source-first record. Do not infer root/main/native acceptance from these files.
