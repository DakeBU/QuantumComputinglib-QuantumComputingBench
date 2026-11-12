# Primitive semantics c28: independent source-only mathematical review

## 0. Identity, evidence boundary, and verdict

Reviewer: `primitive_semantics_source_review_c28`, an independent phase-1 source reviewer. Sole mathematical input: `hermite-export-work/primitive-semantics-author-c28/source-only.md`, “Finite state action, exact primitive circuits, and reversible address logic”. Its actually checked SHA256 is `696a9dce55a0ab9af6139b96ed8ba619fa0b946a0519bbe740cbdc58666e44b5`.

Evidence class: retrospective local source; historical formalizer identity UNKNOWN. This is not evidence of an external paper, a pre-formalization proof, historical independence from implementation, or novelty. Process instructions read completely: `AGENTS.md`, `HARNESS.md`, `.agents/skills/qbe-substantive-worker/SKILL.md`, `.agents/skills/qbe-source-dependency-audit/SKILL.md`, `docs/theorem-publication-protocol.md`, `docs/proof-digestion-protocol.md`, and `docs/evidence-routed-memory-protocol.md`.

No implementation, author mapping, decoder, compilation record, old review, atlas, graph, inventory, publication, cache, or test material was consulted. No Lean, Git, network, simulator, subagent, process termination, or deletion was used. Only the named source supplied mathematics. Node IDs below identify source regions, not Lean declarations or existing graph identities. This document is to be frozen before any separate formal authorization.

Verdict: **SOURCE_ONLY_PASS_WITH_BOUNDARIES**. I find the exact finite mathematics correct under its own domains and limited claims. No correction is proposed. This is not implementation acceptance, formal signature acceptance, Proof Seal, publication admission, or resource/physical-realization certification. The actual formal binders, definitions, dependencies, and denotation fidelity remain UNREAD/UNKNOWN.

## 1. Frozen mathematical contract

The source separates general finite coordinate matrices, semiring-valued action, rational symbolic interpretation, complex unitarity, exact-real angles, and named-wire assignment matrices. Rows are outputs, columns inputs. A qubit register has dimension 2^n, including 1 when n=0. Signal-system flattening is signal-high/system-low: `(a,i)->a*r+i` for rows and `(b,j)->b*c+j` for columns. This is not an integer endian convention for later assignments `b:[n]->[2]`.

Instruction lists are chronological: later matrices multiply on the left. Y has a negative upper-right entry, Z has opposite imaginary signs on the two diagonal entries, and both use half angles. All matrix and program equalities are literal, not modulo phase. Declared program phase is retained. State evidence assumes standard unitarity, an arbitrary specified proposition N, and exact state action; supplied circuit/schedule/auxiliary/resource metadata has no automatic realization theorem. Lift unitarity assumes supplied G-unitarity, whereas actual primitive unitarity is derived.

The reversible classical proof language is separate from the four-form primitive language. The ccx action formula is unrestricted, its involution needs each control distinct from target, and its constructor requires all three pairwise distinctions. No compilation bridge is claimed.

## 2. Independent derivation

### 2.1 Finite action and state evidence (§§1–2)

For j:[c], evaluate each output coordinate:

`(U e_j)_i = sum_l U_(i,l)*delta_(l,j) = U_(i,j)`.

Every l unequal to j contributes zero; the remaining factor is right multiplication by 1. Finite addition and the zero/one multiplication laws suffice. Multiplication associativity is not needed for this identity, so the source's restricted nonassociative-semiring qualification is sound. It is not permission to reassociate arbitrary matrix products over that carrier; later circuit products are complex and associative.

For complex a,b and j,k, distribute both vector addition and finite summation, commute complex scalars as needed, and apply the basis identity. This gives `a U_(i,j)+b U_(i,k)`. If j=k it becomes `(a+b) U_(i,j)`, so no distinctness premise is needed. For c=0 no j exists; for r=0 both output vectors are empty.

Since 2^n is positive even when n=0, column 0 exists. First-column equality and `Ue_0=v` are equivalent by coordinate evaluation. The certificate's explicit proofs of standard complex unitarity, N, and state action are exactly enough for its weak package and first-column readback. Reading its stored preparation proof is not new semantic evidence.

N need not be the usual norm formula. Separately, genuine unitarity and `Ue_0=v` imply ordinary squared norm one for v. These facts are compatible: arbitrary true N is an additional target proposition, not a new definition of Hilbert norm and not license to certify an unnormalized v using a genuinely unitary U. The presentation circuit, schedule, resource record and auxiliary count remain unrelated data unless further evidence connects them to U. A default auxiliary count zero proves no physical cleanup.

### 2.2 Product coordinates and clean branch (§3)

For a<s and i<r, `a*r+i < a*r+r = (a+1)*r <= s*r`. If r=0 no i exists and the assertion is vacuous. The same argument uses c for columns. Thus all displayed flattening coordinates are well typed without blanket positivity. The product view is defined by substitution; no unproved inverse-flattening procedure is needed for the claimed equality.

Projection evaluates to `M_(a*r+i,a*c+j)` in both views. In the square case the embedding is `(a,i)->a*d+i`; restriction along it is the same entrywise block, including the rational specialization. No swap occurs.

Apply the basis-column identity to input a*d+j and output a*d+i:

`[Ue_(a*d+j)]_(a*d+i) = U_(a*d+i,a*d+j) = (P_a U)_(i,j)`.

Substitution proves both directions of the pointwise target equivalence. The same selected a occurs at input and output. No unitarity, probability, target normalizer or normalized failure branch is used. If s=0 there is no a. If d=0 there are no i,j and the universal claims are vacuous. Other signal outputs and any full failure/cleanup/physical realization contract remain outside this bridge.

### 2.3 Exact rotations and coefficient interpretation (§4)

Writing c_u=cos u and s_u=sin u, direct multiplication of `R(v)R(u)` gives diagonal `c_v*c_u-s_v*s_u=cos(u+v)`, upper-right `-(c_v*s_u+s_v*c_u)=-sin(u+v)`, lower-left sin(u+v), and the same second diagonal. Consequently `Y(beta)Y(alpha)=Y(alpha+beta)` with the exact source order and half angles. Same-axis rotations commute, but this is not permission to reverse unrelated gates.

Parity of sine/cosine gives `R(-t)=R(t)^T`. Entries are real, hence transpose equals dagger here. Multiplying either way with R(t) gives I by cos²+sin²=1, proving unitarity. Swapping both rows and columns with X gives `X R(t) X=R(-t)`. At zero angle the matrix is I. All are full-matrix equalities.

Embedding a real t into C commutes with sine, cosine and division by 2. Those embedded values are fixed by complex conjugation. Thus the source's scalar formulas at t+0i and (t+0i)/2 are valid. Matrix dagger still transposes, so scalar conjugation alone does not establish a dagger law.

`Y(2 arccos c)=R(arccos c)=A(c)` is factor-two cancellation; it does not use interval bounds. The coefficient interpretation `cos(arccos c)=c` does use -1<=c<=1. Within this interval the first column is `(c,sin(arccos c))=(c,sqrt(1-c²))`; c's sign is preserved. In particular c=-1,0,1 give (-1,0),(0,1),(1,0). These extra evaluations are independent checks, not a strengthened target. Outside the interval the source promises no coefficient-loading meaning.

At pi/4 both sine and cosine equal sqrt(2)/2, giving the whole W matrix as Y(pi/2). Its second column differs from Hadamard even though the uniform first column agrees.

For Z put `z_-=c-i*s`, `z_+=c+i*s`, with c,s at theta/2. Conjugation interchanges them and their product is c²+s²=1. The diagonal matrix has both unitary products I. Negating theta reverses sine, giving Z(-theta)=Z(theta)^dagger. Both signs and half angles survive; no scalar phase is dropped.

Arccos-expression syntax carries rational [-1,1] evidence, or rational [0,1] evidence before square root. Those conditions are not restrictions on arbitrary given-real primitive angles. Exact real interpretation does not imply a computable decimal export or costed evaluation.

### 2.4 Named wires, lifts and permutations (§5)

On [2], flip exchanges 0 and 1, so two cases prove involution. A target update preserves all other wires and flips t twice. For cx with c!=t, the target update preserves the control. A zero control is inactive twice; a nonzero control is active twice and the target flips cancel. Thus the stated equivalence is self-inverse. Without that inequality the bare formula need not be injective: for c=t, 0 stays 0 while 1 flips to 0. This demonstrates necessity of the existing hypothesis, not a source counterexample.

S_t has explicit inverse assigning q at t and the rest component at every other wire. Checking at t and at each different wire proves both inverse laws and the restriction property. Transport of `G tensor I` gives the displayed lift entry formula: the I factor is the equality delta on other-wire assignments.

For `L(G)^dagger L(G)`, delta conditions force the two external rest assignments to agree and fix the internal rest assignment. The remaining internal target-bit sum is `(G^dagger G)_(q',q)`, the target delta when G is unitary. The opposite product uses `G G^dagger=I`. Reindexing both axes preserves these products. This proves exactly the conditional lift theorem, not arbitrary-G unitarity. Transpose and conjugate the entry formula to get `L(G)^dagger=L(G^dagger)`.

Q_sigma has one 1 in column b, at row sigma(b), hence sends e_b to e_sigma(b). The dagger entry at (b',b) is 1 iff `b=sigma(b')`, equivalently `b'=sigma^(-1)(b)`. Thus dagger is Q of the inverse, and both products are I. Orientation agrees with rows-as-outputs.

Applying these facts to x, distinct-wire cx, Y and Z derives all four primitive unitarity claims. Instruction-adjoint denotation follows from the actual permutation involutions or from rotation negation plus lift-dagger compatibility. An arbitrary G-unitarity hypothesis is legitimate for the reusable lift, but must not replace the internal derivation for each explicit primitive.

### 2.5 Chronological circuits, phases and refinement (§6)

The recursion expands a list `[g1,...,gm]` to `E(gm)...E(g1)`. Identity and closure under unitary products prove circuit unitarity by induction. For concatenation, the empty-first-list case is `E(D)I`. The step is

`E((g::C)++D)=E(C++D)E(g)=E(D)E(C)E(g)=E(D)E(g::C)`.

This uses the tail induction hypothesis and associative complex multiplication. Reversing the list and adjointing each instruction gives `E(g1)^dagger...E(gm)^dagger`, exactly the original product's dagger. Reversal is indispensable for unrelated gates.

For real phi, conjugation gives `conj(exp(i*phi))=exp(-i*phi)`. Either scalar product is exp(0)=1, proving unit modulus and p(-phi)=conj(p(phi)). Composition concatenates first then second and adds phase. The exponential addition law and central scalar multiplication give exactly `F(P;Q)=F(Q)F(P)`. Scaling a unitary by p preserves both unitary products; negating phase and taking the adjoint circuit gives `F(P^dagger)=F(P)^dagger`.

Refinement is the literal witness `E(C)=T` on the same basis. A phased program instead gives p(phi)T. For example empty circuit with phase pi gives -I rather than I, even on the zero-wire 1D space. This validates the source's stated limitation. Label-dependent discarded phases would become relative under coherent control; no phase-dropping permission occurs.

For n=0 there is exactly one empty assignment but no target wire, hence no primitive instruction, and the empty circuit is the 1D identity. A program may still carry a phase. For n=1 the remaining-wire assignment set has one element, so its identity tensor factor is dimension one, not zero. Distinct cx wires need n>=2.

### 2.6 Reversible classical proof language (§7)

If both ccx controls are 1 and each differs from target, the target flip preserves both controls. The second application remains active and cancels the flip. If inactive, the assignment never changes and remains inactive. This proof does not compare controls to each other. Equal controls distinct from target reduce to cx and remain involutive, but are not a legal pairwise-distinct triple instruction. Either control equal to target can destroy injectivity, so neither control-target inequality is redundant.

The instruction constructor's three pairwise inequalities are stronger than the equivalence proof's two required ones. Its denotation may ignore the redundant control-control proof, not the two control-target proofs. Head-then-tail evaluation and induction give exactly the displayed nested chronological action; composition of equivalences is reversible. No gate count, phase convention for compiled ccx, primitive expansion, address-arithmetic specification or indicator-predicate theorem follows just from the language's intended name. On fewer than three wires no triple constructor exists; on one or two wires other legal instructions may still exist. On zero wires only the empty program exists.

## 3. Exhaustive source-region disposition

Every display and substantive paragraph is included. NODE includes scope/boundary nodes because negative statements constrain permissible conclusions. The source has no external citations or diagrams. Anchors below are frozen section/formula descriptions, not implementation-origin identities.

| Source region | Disposition and node | Content covered |
| --- | --- | --- |
| Title and section headings | EXCLUDED(navigation-only) | No implication or cost/address correctness follows from a heading. |
| §1 paragraph 1 | NODE C01 | [d], finite function carriers, output-row/input-column convention, 2^n including n=0. |
| §1 action display and adjoint paragraph | NODE C02 | Finite-sum action, conjugate transpose, two-sided unitarity, no arbitrary-matrix certificate. |
| §1 symbolic paragraph, every sentence | NODE C03 | Rational grammar/environment/interpretation; ordered product folds; syntactic versus interpreted zero; no trig/unitary implication. |
| §1 final paragraph | NODE C04 | Literal finite formulas, empty axes and zero sums, index-existence requirements. |
| §2 basis display and all-zero paragraph | NODE B01 | Kronecker basis column; e_0 for all qubit counts. |
| §2 semiring display and proof | NODE B02 | Ue_j/Ue_0 column identities, finite-sum laws, restricted nonassociative applicability. |
| §2 complex two-column display and proof | NODE B03 | Arbitrary complex a,b, j=k allowed; vector and coordinate action formulas. |
| §2 target paragraph and contract display | NODE B04 | v,N, optional source text; arbitrary supplied N; first-column/action equivalence. |
| §2 concrete certificate paragraph | NODE B05 | Standard complex U-unitarity, proof of N and state action; generic/candidate/verified packaging and first-column extraction. |
| §2 metadata paragraph | NODE B06 | No circuit/schedule/auxiliary/resource realization, no imposed norm formula, stored-proof readback. |
| §3 first paragraph and flattening display | NODE I01 | Separate rectangular row/column indices, signal high, bounds and product dimensions. |
| §3 product-view display | NODE I02 | Flat matrix restriction to product coordinates. |
| §3 selected projection display | NODE I03 | Same selected signal label at input and output. |
| §3 following embedding/clean-block paragraph | NODE I04 | Flat/product equality, square numerical embedding, rational specialization, no swap. |
| §3 clean-action display | NODE I05 | Semiring square U; basis-input/output entry identity. |
| §3 target iff display and substitution proof | NODE I06 | Universal pointwise equivalence, no unitarity/failure-normalization premise. |
| §3 final scope sentences | NODE I07 | No normalizer/probability/cleanup/physical realization; s=0,d=0 and rectangular zero axes. |
| §4 angle-language paragraph | NODE R01 | Exact-real grammar; rational/pi/arccos/sqrt-arccos/arbitrary-real forms and domain evidence; sums/negation/scaling; no decimal guarantee. |
| §4 R,Y,X display and convention sentence | NODE R02 | Ordered 0,1 basis, full matrices, half angle and sign. |
| §4 four-identity display and proof paragraph | NODE R03 | Zero, ordered addition, negation/dagger, X conjugation; trig proof and Y unitarity. |
| §4 conjugation paragraph/display/following sentence | NODE R04 | Real-complex compatibility, scalar conjugation and half argument, distinction from matrix transpose. |
| §4 A(c) definition/identity and interval explanation | NODE R05 | Coefficient-domain bounds versus factor cancellation and top-left coefficient interpretation. |
| §4 W display and following sentence | NODE R06 | Full W=Y(pi/2), not Hadamard. |
| §4 Z display and following paragraph | NODE R07 | Both diagonal signs and half angles, modulus, unitarity, adjoint by negation, no phase quotient. |
| §5 assignment/flip paragraph | NODE W01 | Named-wire assignments, no integer endian flattening, flip involution. |
| §5 x/cx paragraph/display/following proof | NODE W02 | Target update; unrestricted cx formula; c!=t needed for self-inverse equivalence and control preservation. |
| §5 S_t display and inverse paragraph | NODE W03 | Target/rest bijection, reconstruction, exact other-wire restriction. |
| §5 lift display and surrounding proof | NODE W04 | Tensor transport entries, other-wire preservation, conditional unitarity and simultaneous reindexing. |
| §5 lift dagger display and justification | NODE W05 | Exact adjoint compatibility. |
| §5 permutation display and paragraph | NODE W06 | Q_sigma orientation, basis action, unitarity and inverse-dagger law. |
| §5 four-instruction paragraph/denotation display | NODE W07 | Exactly four forms, interpreted exact angles, distinct cx, full denotations and derived unitarity. |
| §5 final adjoint sentences | NODE W08 | Bit forms fixed, rotations negated, derived instruction dagger law. |
| §6 circuit recursion display/introduction | NODE E01 | Chronological list, later factors left. |
| §6 concatenation display/induction proof | NODE E02 | Circuit unitarity and exact concatenation order. |
| §6 reversed-adjoint display/proof | NODE E03 | Reverse and pointwise adjoints; product dagger order. |
| §6 phase paragraph | NODE E04 | Exact exponential phase, unit modulus, conjugation/negation. |
| §6 program definition/display/identity sentences | NODE E05 | Declared scalar phase times E; identity program. |
| §6 sequential-composition paragraph/display | NODE E06 | First then second, phases added, F(Q)F(P). |
| §6 program unitarity/adjoint display | NODE E07 | Unit-modulus scaling, exact program dagger. |
| §6 refinement/scope paragraph | NODE E08 | Phase retained, literal same-basis equality, no arbitrary phased-program refinement. |
| §6 zero-/one-wire paragraph | NODE E09 | Empty assignment, no zero-wire primitive, 1D identity/phase, 1D rest, cx minimum wires. |
| §7 language-distinction paragraph | NODE V01 | Separate classical proof instructions and triple constructor; no extra final primitive form. |
| §7 ccx definition/display/involution paragraph | NODE V02 | Conjunction-control action; formula unrestricted; only control-target distinctions needed for involution. |
| §7 constructor/distinction sentences | NODE V03 | Three pairwise constructor inequalities; precise semantically redundant proof. |
| §7 instruction/program paragraph/action display | NODE V04 | Appropriate basis equivalences, empty identity, head then tail, nested chronological reversible action. |
| §7 final scope sentences | NODE V05 | No ccx-to-primitive compilation; wire minima and zero-wire empty program. |
| §8 paragraph 1 | NODE S01 | Exactness; no error/measurement/success/amplification; exact phases; no unspecified cleanup; conditional lift versus derived primitive/circuit/program unitarity. |
| §8 paragraph 2 | NODE S02 | No evaluation runtime/finite-bit/Clifford+T/connectivity/depth/preprocessing/oracle/readout costs; metadata not cost theorem; no charged ccx or synthesis certificate. |

All substantive regions are NODE. Only navigation headings are EXCLUDED. SOURCE_GAP set is empty for the source's stated scope. Physical implementation, precision, costs, cleanup, probability and proof-language compilation are explicit outside-scope requirements, not omitted bridges to a claimed conclusion. If a later Anchor advertises such a stronger result it incurs new obligations; this phase does not silently close them.

## 4. Source construction topology: full AND tails and guarded OR cases

This is a source-derived graph, not a Lean graph. Each brace set is an AND-tail; individual inputs are not independently sufficient. Basic arithmetic/trigonometric/finite-sum laws shown in tails are ordinary mathematical dependencies, not assumed quantum results or hidden public binders.

- `{C01,C02,C04,B01, finite-sum zero/one laws}` -> B02.
- `{C01,C02,B01, complex distributivity and scalar commutativity}` -> B03.
- `{B01,B02, target v,N, square-register typing}` -> B04.
- `{B04, supplied standard-unitary proof, supplied N proof, supplied Ue_0=v proof, supplied presentation metadata}` -> B05 packaging/readback. B06 forbids interpreting this as physical realization or resource certification.
- `{C01,C04, a<s, i<r, j<c, natural arithmetic bounds}` -> I01. `{I01,flat M}` -> I02. `{I02,same selected a on both axes}` -> I03.
- `{I01,I02,I03,r=c=d specialization}` -> I04; rational coefficients specialize this same equality, not a separate sufficient route.
- `{B02,I03,I04, semiring U of shape sd by sd, a:[s], i,j:[d]}` -> I05.
- `{I05,target T,pointwise extensionality}` -> I06. I07 remains attached to all its consumers.
- `{R01,R02,sine/cosine addition and parity,cos²+sin²=1,real-complex compatibility}` -> R03/R04. C03's arbitrary rational symbolic environment is not a substitute for this tail.
- `{R01,R02,factor-two cancellation}` -> R05's matrix identity. `{R05,-1<=c<=1,inverse-cosine identity}` -> the top-left=c interpretation. These two heads have different complete tails.
- `{R02,sin/cos(pi/4) values}` -> R06. `{R01,R07 literal formula,trig parity,cos²+sin²=1}` -> R07 unitarity and adjoint law.
- `{W01,target t}` -> W02.x involution. `{W01,W02.x,c!=t,control preservation}` -> W02.cx involution/equivalence.
- `{W01,target t,piecewise reconstruction}` -> W03.
- `{W03,tensor-I delta formula}` -> W04 entries. `{W03,W04 entries,supplied G-unitarity}` -> W04 unitarity. `{W04 entries,conjugate transpose}` -> W05.
- `{finite-basis equivalence sigma,W06 literal formula,B02,inverse law}` -> W06 basis action/dagger/unitarity.
- W07 uses guarded primitive-tag cases: X has tail `{W02.x,W06}`; Y has `{R03,W04}`; Z has `{R07,W04}`; cx has `{c!=t,W02.cx,W06}`. This is exhaustive guarded OR case analysis for the selected tag. It is not a claim that any one primitive implements an arbitrary primitive, and not four unconditionally required premises about a single tag.
- W08 has corresponding guards: bit forms use their involutions and W06; Y uses `{R03,W05}`; Z uses `{R07,W05}`. Guard conditions must not be erased.
- E02 is list induction: empty guard uses `{E01,identity unitarity}`; nonempty guard uses `{W07,E02 on tail,unitary product closure}`. Its concatenation head additionally uses the induction hypothesis and associative complex multiplication.
- `{E01,E02 concatenation,W08,product-dagger reversal}` -> E03.
- `{E04 formula,phi real,complex exponential conjugation/addition}` -> phase modulus/conjugation. `{E01,E04,E05 definition}` -> identity-program denotation.
- `{E02 concatenation,E04 exponential addition,E05,scalar centrality}` -> E06.
- `{E02 circuit unitarity,E04,E05}` -> E07 program unitarity. `{E03,E04 conjugation,E05}` -> E07 program dagger.
- E08 is a literal evidence-bearing refinement definition. No OR-route bypasses phase evidence for arbitrary program refinement.
- `{W01,no element of [0],constructor target requirements}` -> E09 instruction exclusion. `{E01,E04,E05}` supplies the 1D circuit/program conclusions. Other wire minima use cardinality and distinctness.
- `{W01,W02.x,c0!=t,c1!=t,conjunction-control preservation}` -> V02 involution/equivalence. V03 adds the stronger pairwise-distinct constructor guard but does not alter that theorem's minimal condition.
- V04 instruction cases have guarded tails `{W02.x}`, `{W02.cx,c!=t}`, or `{V02,V03 legality}`. Empty program uses identity; nonempty uses `{head equivalence,tail equivalence,equivalence composition}`. V05 preserves no-compilation and minimum-wire boundaries.
- `{all preceding exact statements,B06,I07,E08,V05}` -> S01/S02 scope accounting, not a new synthesis or resource theorem.

There are no competing sufficient source constructions for the same fixed target other than tagged/guarded primitive cases and induction cases. Tensor transport and the lift entry formula describe the same object; they are not independent constructions with interchangeable assumptions. Rational symbolic interpretation and exact-real angle interpretation are not OR-proofs of the same unitarity claim. No SP-to-BE or BE-to-SP transport is proved: a clean-entry bridge alone supplies neither a general BE certificate nor normalized state preparation.

## 5. Expected mathematical binders and definition audit

These are source interfaces for later comparison, not an invented exact Lean signature. No formal signature has been authorized or read.

### 5.1 Binder classes

- TYPING: natural dimensions d,r,c,s,n; scalar carrier and the requisite algebraic structure; finite matrix/vector/function shapes; valid indices; assignment carrier; target wire; same-basis target matrix; finite basis carrier for sigma. An index of an empty set cannot be filled by a default.
- STANDING: output-row/input-column action; conjugate-transpose dagger; standard two-sided complex unitarity; exact-real angle semantics; named-wire basis; chronological lists. Signal-high/system-low is standing for its product-index interface only, not a global integer endian map for assignment matrices.
- SOURCE: arbitrary complex a,b and valid j,k, with no j!=k; arbitrary target v and proposition N; explicit certificate proofs of standard U-unitarity, N and Ue_0=v; selected a and arbitrary target T for the clean-entry equivalence; G-unitarity for the arbitrary-G lift theorem; supplied basis equivalence sigma; interval evidence in the arccos syntax constructors; -1<=c<=1 for the coefficient-domain/top-left interpretation; c!=t for cx involution and constructor; c0!=t and c1!=t for general ccx involution; all three pairwise inequalities for the triple instruction constructor; literal E(C)=T evidence for refinement.
- RULED: none. No correction was supplied or needed.
- EXCESS: none in the natural statements. A later formal comparison must detect excess premises rather than trusting these expected classes. Potential excesses include coefficient-interval restrictions on arbitrary rotation angles, j!=k, positive dimensions everywhere, assumed unitarity of the explicit primitive/circuit/program instead of derived unitarity, and normalized failure branches for clean-entry equality. Requiring correct metadata realization just to form the source's weaker evidence package would change its claim. Conversely, omitting actual index constraints, source evidence, or distinctness conditions is not justified.

Proved ingredients remain dependencies: primitive unitarity, tensor/reindexing facts, control preservation, phase modulus, product/adjoint laws and the clean-entry bridge must not be added as convenient public premises for conclusions the source derives. The source's certificate and refinement deliberately receive evidence as data; their conditional nature is faithful, not an excess. An implementation cannot turn a derived theorem into a fake closure by additionally assuming its own conclusion.

In mathematical signature form, the expected families include: Ue_j=column_j(U) for semiring/nonassociative-semiring laws sufficient to that identity; complex superposition action for all a,b,j,k; first-column iff state action for every n,U,v; clean-action iff pointwise projection for all s,d,U,T and a:[s]; all-real Y/Z identities; unitary G -> unitary L_t(G); basis equivalence sigma -> permutation dagger/unitarity; all legal primitive instructions -> unitary and adjoint-compatible denotation; all chronological primitive lists/programs -> unitary and ordered composition/adjoint; and both minimally guarded ccx equivalence and the more restrictive legal classical instruction/program action. The certificate's mathematical conclusion is packaging/readback, not a theorem that an arbitrary presentation circuit denotes its U.

### 5.2 Definition kinds and well-definedness

All actual source definitions are literal: [d]; matrices/vectors as functions; action, dagger and unitary predicate; symbolic syntax and recursive rational interpretation; basis and zero columns; target/certificate/metadata packages; flattening, product view, projection, clean amplitude; angle syntax and real interpretation; R/Y/X/A/W/Z; flip, x/cx/ccx action; split and explicit reconstruction; lift and permutation matrices; primitive constructors and instruction adjoint; chronological E, p and phase-bearing F; program composition/adjoint, refinement; reversible classical instruction/program evaluation. Equivalence wrappers use those same literal functions with proved inverse laws, not selected substitute functions.

There is no characterized object introduced by unique existence or classical-choice fallback. W=Y(pi/2) and tensor-versus-entry descriptions verify literal definitions; they are not existential selections. A future choice-based implementation needs a faithful bridge on the whole source carrier and cannot invent off-source default values.

There is no quotient/representative definition. Phases and matrices are exact; reindexing uses a specific bijection on both axes. No purification, dilation, Kraus/spectral selection, phase-class representative or canonical preparation unitary is introduced. Many unitaries can prepare a fixed state; the source records a supplied one and claims no uniqueness.

A(c)'s coefficient-loading meaning is source-restricted to [-1,1], despite total real arccos allowing algebraic cancellation statements outside that interval. The angle-expression constructor's interval proof belongs to syntax. Empty matrix axes are allowed, but selected indices and wires must exist. Default indices, zero-matrix fallbacks or silently chosen representatives would need scrutiny in phase 2.

## 6. Seven quantum semantic slots

| Slot | Source semantics | Not supplied |
| --- | --- | --- |
| 1. Target/normalization | General vectors/matrices; exact state or first-column action; arbitrary supplied N; certificate requires genuine complex unitarity; clean block equals arbitrary T pointwise. | No fixed BE normalizer or accepted-branch normalization. N is not prescribed a norm formula; usual norm-one of a certified v follows separately from U-unitarity. |
| 2. Scalars/dimensions/basis/order | General, semiring, rational-symbolic, complex and real-angle layers distinguished; 2^0=1; product signal high/system low; named-wire assignments without integer endian map; exact Y/Z signs and half angles. | No Fourier convention, integer endian flattening of assignments, automatic external-library basis adapter, or default empty-set index. |
| 3. Access/inverses/controls | Finite matrix/function inputs, possibly arbitrary given real angles; explicit primitive/program adjoints; distinct cx; separately specified ccx guards and constructor domain. | No coherent parameter oracle, constant-time entry access, costed angle/symbol evaluator, generic controlled-program construction, or ccx-to-four-primitive compilation. |
| 4. Ancilla/overwrite/garbage | x/cx/ccx change only target; other-wire values preserved under their controls. Lift has equality of remaining assignments. Clean extraction reads same a on both axes. Auxiliary count is data. | No unspecified workspace cleanup or full failure/garbage contract; no physical interpretation of a default auxiliary count. Projected entries alone do not prove clean ancillas for an implementation. |
| 5. Phase | Literal signed matrices; dagger transposes as well as conjugates. Program p(phi) retained in composition and adjoint. Refinement is exact on same assignments. | No phase quotient, no arbitrary phased-program refinement from a circuit witness, no dropping coherent label-dependent phases. |
| 6. Error/success | Exact finite equalities and two-sided unitarity. Clean entries have no probabilistic claim. | No approximation norm/tolerance, measurement protocol, confidence, success/postselection probability, normalized failure branch or amplification bound. |
| 7. Resource tier | Four ideal exact-angle primitive forms with mathematical full-register denotations; separate reversible proof language; supplied presentation/schedule/resource/auxiliary metadata. | No physical implementation, costed real arithmetic, finite-bit precision, synthesis error, Clifford+T count, depth/connectivity, preprocessing/oracle construction/readout cost, or charged ccx. Names do not fill these slots. |

## 7. Edge cases and discriminators

All checks here are mathematical reasoning, not simulations:

- n=0: e_0 is the one-coordinate value 1, but no target wire exists. No conflict arises between a 1D register matrix and absence of primitive instructions. A zero-wire program may still have phase.
- d=0: vector/clean-action universal claims are vacuous; this is different from zero-qubit dimension 1. With s=0, a selected signal cannot be instantiated.
- r=0 or c=0: rectangular formulas retain their stated empty axes; a named basis column still needs a column index even with no rows.
- j=k: complex superposition action combines coefficients correctly without extra distinctness.
- Coincident cx control/target: 0 and 1 both map to 0, confirming why the source requires c!=t for equivalence.
- Equal ccx controls distinct from t: involution remains true, but the triple instruction is not legal. Either control equal to t can collapse inputs, distinguishing the redundant control-control proof from essential control-target proofs.
- Coefficient c=-1,0,1: signs and endpoint amplitudes are retained. Cancellation of the factor two does not grant out-of-domain coefficient interpretation.
- W versus Hadamard: same first column does not establish full primitive refinement.
- Arbitrary rational symbol environment: values with names resembling cosine/sine need not satisfy their quadratic identity, so symbolic interpretation alone supplies no complex unitarity.
- Arbitrary lift input G=2I: the lift is not unitary. The source's conditional G premise prevents this false generalization.
- Chronology: Y and Z generally do not commute; the second executed gate occurs on the left. Same-axis Y addition must not hide an ordering error elsewhere.
- Empty circuit plus phase pi: program is -I, not I, even for n=0. Exact program refinement needs phase tracking.
- Clean branch: accepted entries alone do not fix other signal rows, input-dependent probability, a BE normalizer, or amplification cost.

No example refutes the frozen source. Each tests the stated guard or confirms an explicit limitation. No replacement target is hidden in these checks.

## 8. Structured handoff and freeze status

Objective/frontier node: complete independent source-only review of the primitive-semantics natural contract.

Mathematical delta: independent derivation of basis/state/clean-block identities, exact Y/Z and phase conventions, named-wire lifts/permutations, chronological products/adjoints and reversible-program action; exhaustive source coverage and complete AND/guarded-case topology; expected binder/definition audit and seven-slot boundary record.

Root effect: the natural-source mathematical leg is ready for separately authorized formal comparison. No formal leg is closed. No exact Lean signature, module content, dependency, build, decoder reconstruction or implementation/publication verdict is asserted.

Failure class: NONE for the source as stated. No REFUTED or SOURCE_INVALID conclusion. Environment/API/implementation were not tested and are neither passed nor failed.

Salvage: no failed route and no cleanup. The derivations are source-only evidence, not compiled reusable library fragments.

Process-memory IDs: none; restricted scope allowed the named protocols and source, not history or curated records.

Direction fingerprint: `fresh-natural-source-only/exact-finite-action/phase-order-empty-domain/primitive-vs-proof-language`. Expected information gain: identify source correctness and exact comparison obligations without implementation anchoring.

Parallel admission: explicitly assigned independent source review; no child agent spawned. No competing construction was examined. Common-blind-spot/comparator status is not applicable to this single-source phase; guarded cases remain guarded rather than treated as competing implementations.

Default verified route: none chosen for implementation/publication. The source's own literal constructions were audited. Purification/Exposition Seal: NOT PERFORMED / NOT GRANTED. No production/graph/lesson/cache/public file was changed. Source expansion anchors are in §3; Lean expansion nodes remain UNREAD/UNKNOWN.

Recommended next step: bind these actual bytes in `phase1-seal.json`, report both artifact hashes, then wait for separate formal authorization. Do not modify this frozen record after receiving formal information. Any mismatch or proposed repair belongs in a new phase-2 artifact, keeping the pinned source, this independent reconstruction, discovered mismatch and proposed repair distinct.

Confidence: high for the elementary finite mathematics within the stated scope. Formal carrier coverage, actual binder/definition fidelity, proof dependency and metadata semantics, repository gates, source-history identity, external provenance, novelty and public admission remain unreviewed.
