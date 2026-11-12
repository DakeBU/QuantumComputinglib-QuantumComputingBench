# Local Robin constructions — natural source version 2

## A0. Version, scope and authority [N40,Q07]

This is a versioned, retrospective, implementation-informed LOCAL mathematical source, authored after the original 104-line source and explicitly authorized late Stage-3 comparison feedback. It is not historically pre-proof, source-blind, independently reviewed, or authenticated original-paper text. Historical formalizer: UNKNOWN. It changes exposition and specifications, not the quantum algorithm, Lean code, scoring, verifier, or scientific targets. Its statements and source graph are AUTHOR proposals for a new distinct raw-source-only review and later original-source/formal comparison.

Exactly nine target modules are in scope: ModularAdder3; Robin/PaperSevenPrepare; Robin/PaperSevenAmplitudePrimitive; Robin/PaperSevenPreparePrimitive; Robin/Figure4PreparePrimitive; Robin/Figure4T3; Robin/SymmetryFourSlotPrimitive; Robin/SymmetryXorFourSlotPrimitive; Robin/SystemConjugation, all under QuantumBlockEncoding. The legacy packet's tenth target, RobinMatrix, is NOT a tenth module reviewed here. Its small stencil-provider projection and the existing literal fixed target may supply context; its complete 26,985-line symbolic backend, obligations, and admission remain outside this source. The final paper-seven consumer is also outside these nine targets. This resolves the administrative scope of Q07 without modifying any old bytes.

Stable N01–N40, D01–D03 and the graph-v2 supplier identities are retained as source/construction anchors below. G01–G06 denote omissions in version1, not erased history. The delta document records which new regions propose to supply each omission. No gap is declared independently accepted, and no unavailable paper proof is invented.

## A1. Carriers, exact gates, phases and indices [N01,N02,N04]

For q physical wires the computational basis is B_q={0,1}^{Fin q}; a bit state is a function x:Fin q→Fin2. Its little-endian index is \(\ell_q(x)=\sum_{k=0}^{q-1}2^k x_k\). Square complex matrices act on columns. A chronological list \(g_1,\ldots,g_m\) denotes \(U(g_m)\cdots U(g_1)\); the empty list denotes identity.

A PrimitiveProgram is a literal gate list together with an ExactAngle \(\phi\), and denotes \(e^{i\phi}U(\text{list})\). Sequential composition concatenates lists and adds phases. Dagger reverses the list, replaces each RY/RZ angle by its negative, leaves X/CX self-adjoint, and negates the program phase. Exact matrix equality, not equality modulo global phase, is the contract.

The primitive gates are X, RY, RZ and CX. X flips its target; CX(c;t) flips target t iff control c is1, and requires c≠t. In the ordered target basis (0,1),
\[
 R_y(\theta)=\begin{pmatrix}\cos(\theta/2)&-\sin(\theta/2)\\
 \sin(\theta/2)&\cos(\theta/2)\end{pmatrix},\qquad
 R_z(\theta)=\operatorname{diag}(e^{-i\theta/2},e^{i\theta/2}).
\]
Each is unitary for every real angle. Define
\[
 R(c)=R_y(2\arccos c)=
 \begin{pmatrix}\cos(\arccos c)&-\sin(\arccos c)\\
 \sin(\arccos c)&\cos(\arccos c)\end{pmatrix}.
\]
This is unitary for every real c. Its (0,0) entry equals c only when −1≤c≤1; on that interval its off-diagonal sine is the nonnegative \(\sqrt{1-c^2}\). No out-of-domain coefficient fallback is introduced.

ExactAngle is syntax with these interpretations: rational(r)↦r; piRational(r)↦πr; twiceArccosRational(r,h)↦2arccos(r), with h:|r|≤1; twiceArccosSqrtRational(r,h)↦2arccos(√r), with h:0≤r≤1; real(t)↦t; and exact add, negation and rational scaling. These are the actual total constructors, not a proposal to encode the square-root angles by a different identity. The real constructor has no promised decimal algorithm. Bounds for concrete tables are constructed internally, not assumed in the final fixed-block statements.

For a distinguished target wire t, splitting a state gives (target bit, all other bits). The inverse inserts that bit back; these maps are explicit inverses on the whole carrier. A one-qubit matrix V lifted to t has entries zero unless all other bits match, and otherwise entry \(V_{x_t,y_t}\). For any finite equivalence e, reindexing a matrix means \(\mathrm{Re}_e(U)_{i,j}=U_{e^{-1}i,e^{-1}j}\). It preserves products, adjoints and unitarity. A change of coordinate labels is not itself an uncharged physical gate; the nontrivial physical coordinate circuit C in A8 is emitted and counted.

The logical product order is \(C\times(S\times H)\): coefficient, selector, system. A clean block fixes the chosen coefficient and selector labels on BOTH row and column, and fixes every further declared work coordinate where specified. It is a submatrix, not the full unitary. With normalized input ψ its accepted component is Aψ/α; this is not certain successful output or deterministic state preparation. No amplification or readout theorem follows.

## A2. Exact reversible compilation, H/T phases and C3X domains [N05,N06,N07]

A reversible X/CX/CCX instruction has its literal bit permutation. CCX(a,b;t) flips t iff a=b=1; its compiler input requires the three wires pairwise distinct: a≠b, a≠t, b≠t. Its physical compilation uses only the primitive alphabet.

The macro H(t) is the chronological primitive list RZ(t;π), RY(t;π/2), with program phase π/2. Thus its matrix is \(iR_y(\pi/2)R_z(\pi)=2^{-1/2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\). T(t) is RZ(t;π/4) with phase π/8, hence diag(1,e^{iπ/4}); T†(t) is RZ(t;−π/4) with phase −π/8. CX and X programs have phase0. Dropping these phases would not give the claimed exact macros.

The CCX compiler is H(t), the following thirteen-instruction middle, then H(t), in chronological order:
\[
\begin{gathered}
 \mathrm{CX}(b;t),T^\dagger(t),\mathrm{CX}(a;t),T(t),
 \mathrm{CX}(b;t),T^\dagger(t),\mathrm{CX}(a;t),\\
 T(b),T(t),\mathrm{CX}(a;b),T(a),T^\dagger(b),\mathrm{CX}(a;b).
\end{gathered}
\]
The middle restores all three bits. Its phase exponent, in units π/4, is
\[
 a+b+t-(a\mathbin{\oplus}b)-(a\mathbin{\oplus}t)
 -(b\mathbin{\oplus}t)+(a\mathbin{\oplus}b\mathbin{\oplus}t)=4abt.
\]
This identity is checked on the eight bit triples, or by expanding XOR as binary addition minus twice the product. Thus the middle is CCZ, with phase −1 only on111. HZH=X and H²=I then give CCX exactly. The primitive list has2RY,9RZ,6CX (17 gates), and its stored scalar phase is \(2(\pi/2)+4(\pi/8)-3(\pi/8)=9\pi/8\). These compensated phases are retained when macros compose.

Compiling a reversible list recursively compiles its head then its tail. The empty list is the identity program; multiplication reverses chronology. Induction gives exact equality between the complete compiled program and the permutation matrix of the complete reversible list for arbitrary ambient q. This is ambient-carrier generality for this finite instruction vocabulary, not an arbitrary-width adder theorem.

For C3X, write first controls a,b, third control c, target t and work w. The CONSTRUCTOR and exact compiler/permutation interface require exactly these SIX inequalities:
\[
 a\ne b,\quad a\ne w,\quad b\ne w,\quad
 w\ne c,\quad w\ne t,\quad c\ne t.
\]
The literal reversible list is CCX(a,b;w), CCX(w,c;t), CCX(a,b;w). It is a well-formed permutation under those six conditions, on every input, without a clean-work premise. A constructor may even have t=a or t=b; no ideal C3X behavior is claimed under those six guards alone.

The CLEAN-ACTION and work-cleanliness theorems require the same six inequalities PLUS \(a\ne t\) and \(b\ne t\), and input \(x_w=0\): EIGHT inequalities and one input condition. No a≠c or b≠c condition occurs. Third-control aliasing with either first control is allowed; five-way pairwise distinctness would be an unauthorized strengthening.

Under the eight wire conditions, a,b,c do not change. The first gate changes work to \(w\oplus ab\); the second flips target by \(c(w\oplus ab)\); the third restores w. For w=0 this is the intended triple-controlled flip \(t\mapsto t\oplus abc\), all other bits preserved, with work0 restored. This argument also explains why an initially dirty w can add an extra target flip cw. The full compiled matrix always realizes the actual three-gate permutation; the ideal C3X interpretation is only the stated clean-input theorem. This supplies historical omission G01 without adding an all-distinct guard or repairing dirty behavior.

## A3. The literal fixed three-bit adder [N08,N09]

The seven wires are (a0,a1,a2,b0,b1,b2,w)=(q0,q1,q2,q3,q4,q5,q6), with a and b interpreted little-endian. The chronological reversible list is exactly:
\[
\begin{array}{llll}
1:\mathrm{CCX}(3,0;6),&2:\mathrm{CCX}(6,1;2),&
3:\mathrm{CCX}(3,0;6),&4:\mathrm{CCX}(3,0;1),\\
5:\mathrm{CX}(3;0),&6:\mathrm{CCX}(4,1;2),&
7:\mathrm{CX}(4;1),&8:\mathrm{CX}(5;2).
\end{array}
\]
All wire inequalities here are concrete finite facts. On work0 the first three gates toggle a2 by a0b0a1 and restore work BEFORE a0,a1 are overwritten. The fourth adds the low carry c1=a0b0 into a1, and the fifth forms low sum a0⊕b0. The sixth adds b1(a1⊕c1) into a2; seventh and eighth complete the higher XOR sums. Hence the bit1-to-bit2 carry is
\(a1b1\oplus a1c1\oplus b1c1\), and the result is
\[
 a'=(a+b)\bmod8,\qquad b'=b,\qquad w'=0.
\]
Overflow is deliberately discarded modulo8. This is a fixed seven-wire, three-bit construction. The existing finite proof body uses native_decide on the entire finite input; it is read but NOT executed in this author work. The carry explanation above is natural mathematical reconstruction, not a new Lean proof.

Exact list compilation transports this permutation to complex program semantics on ALL128 basis inputs, while the arithmetic claim remains conditional on work0. Resource ownership is the literal emitted list; abstract oracleCalls is0. Expanding the five CCX macros gives55 one-qubit and33 CX gates (88 total); the same per-wire depth recurrence in A10 gives53. Its program phase is45π/8. Those are static arithmetic consequences of the specified unsimplified macro list, not new asymptotic, finite-bit, optimized, or compiler-acceptance theorems. This supplies G02's literal list and exact phase construction.

## A4. General controlled-RY compiler and the complete eight-label PREPARE [N10–N13,UCR-GENERAL,Q08]

Let \(w:\mathrm{Fin}\,k\to\mathrm{Fin}\,q\) be controls and t the target, with exactly \(\forall u,\ w(u)\ne t\). The generic compiler does NOT additionally assume controls are pairwise distinct or that w is injective. A full non-target context z determines the control tuple \(z(w(u))\). For an entire exact-angle table Θ on k control bits the independent block specification is
\[
 U_{\Theta,w,t}(x,y)=
 \begin{cases}
 R_y(\Theta(z(w(0)),\ldots,z(w(k-1))))_{x_t,y_t},
     &x_{\ne t}=y_{\ne t}=z,\\
 0,&\text{otherwise}.
 \end{cases}
\]
Thus every spectator, including dirty work, is part of the context. Repeated controls simply restrict which control tuples are reachable; there is no invented off-carrier lookup.

For k=0 emit RY(t;Θ(empty)). For k>0 let h be the first control, let \(\Theta_0,\Theta_1\) be the first-bit slices, and set \(A=(\Theta_0+\Theta_1)/2,\ B=(\Theta_0-\Theta_1)/2\) using exact angle syntax. Emit recursively Compile(A), CX(h;t), Compile(B), CX(h;t). On h=0 the target product is RY(B)RY(A)=RY(Θ0). On h=1 it is X RY(B) X RY(A)=RY(A−B)=RY(Θ1). Induct on the remaining controls and apply this argument in each COMPLETE non-target context. This establishes exact full-carrier block equality, with no discarded scalar phase. The recursion emits \(2^k\) RY and \(2(2^k-1)\) CX, including unreduced zero-angle branches.

For seven-state preparation define total angle functions, not just their active values:
\[
 h=2\arccos\sqrt{4/7},\quad \tau=2\arccos\sqrt{2/3},\qquad
 m(v)=\begin{cases}\pi/2&v=0\\\tau&v=1,\end{cases}
\]
\[
 l(u,v)=\begin{cases}0&u=v=1\\\pi/2&\text{otherwise}.\end{cases}
\]
h and τ use the actual twiceArccosSqrtRational constructor and bounds0≤4/7,2/3≤1. π/2 uses piRational(1/2); zero uses rational(0). Q08 is thereby specified, not repaired via a different rational-arccos representation.

Chronology on three selector bits is RY(q2;h), the one-control block q2→q1 with m, then the two-control block (q1,q2)→q0 with l. Define the FULL unitary P as Low·Middle·High, flattened little-endian to Fin8. The program phase is0. This product defines every matrix entry on all eight labels, not merely its first column; its inverse is reverse gate order with every angle negated.

From input000 the high split has probabilities4/7 and3/7. The first branch has two equal splits, making labels0,1,2,3 each1/7. The second middle split gives2/7 and1/7; the2/7 splits equally into labels4,5, while the1/7 branch leaves low0 and gives label6. Label7 has zero probability. Thus
\[
 \overline{P_{s0}}P_{s0}=\begin{cases}1/7&s=0,\ldots,6\\0&s=7.\end{cases}
\]
Only squared amplitudes are needed for the LCU contraction; no arbitrary common positive-phase assertion is substituted for this equation. The eighth basis state remains in the Hilbert space. The auxiliary label map is Some(s∈Fin7) when s<7 and None at7; it does not delete a physical state.

The emitted list is1+2+4=7RY and2+6=8CX, with zero abstract queries. Its primitive record is (oneQubit7,cnot8,oracle0,pureAncilla0,depth13). This is PREPARE, not SELECT or a complete block encoding.

## A5. Literal target and total coefficient tables [N03,N15,N22,N23,D01]

All fixed routes use \(A=M/12,\ \alpha=56/3\), so \(A/\alpha=M/224\), with the COMPLETE integer matrix
\[
M=\begin{pmatrix}
-30&32&-2&0&0&0&0&0\\
16&-31&16&-1&0&0&0&0\\
-1&16&-30&16&-1&0&0&0\\
0&-1&16&-30&16&-1&0&0\\
0&0&-1&16&-30&16&-1&0\\
0&0&0&-1&16&-30&16&-1\\
0&0&0&0&-1&16&-31&16\\
0&0&0&0&0&-2&32&-30
\end{pmatrix}.
\]
This fixed matrix is centrosymmetric under simultaneous reversal i,j↦7−i,7−j. It is NOT symmetric/Hermitian merely by that label: M01=32 while M10=16. Local teaching relates it to the dimensionless homogeneous Robin stencil; no new authentication of the original PDE derivation or paper is claimed. Physical Δx⁻² is factored out and is not silently reinstated in α.

For physical selector s∈Fin8 define
\[
 d=(3,2,1,0,7,6,5,4),\qquad r_s(j)=(j+d_s)\bmod8,\qquad W_{s,j}=M_{r_s(j),j}.
\]
Rows of this total W table are s=0,…,7 and columns are j=0,…,7:
\[
W=\begin{pmatrix}
0&0&0&0&0&0&0&0\\
-1&-1&-1&-1&-1&-2&0&0\\
16&16&16&16&16&16&32&0\\
-30&-31&-30&-30&-30&-30&-31&-30\\
0&32&16&16&16&16&16&16\\
0&0&-2&-1&-1&-1&-1&-1\\
0&0&0&0&0&0&0&0\\
0&0&0&0&0&0&0&0
\end{pmatrix}.
\]
For fixed j all eight addressed rows are distinct. The omitted eighth active-sum row is j+4 mod8, where M is zero. Therefore \(\sum_{s<7}\mathbf1_{i=r_s(j)}W_{s,j}=M_{ij}\), and |W|≤32. Slots0 and6 may be active labels with zero weights; seven active labels do not assert seven nonzero coefficients per column.

There are TWO different TOTAL loaders:
\[
 c_{\mathrm{paper7}}(s,j)=\begin{cases}W_{s,j}/32&s<7\\1&s=7,\end{cases}
 \qquad c_{\mathrm{Fig4}}(s,j)=W_{s,j}/32\quad\text{for ALL }s.
\]
Thus padded paper7 uses R(1)=I and Figure4 uses R(0), not identity, on slot7. Their matrices differ on that physical sector. Their CLEAN sums agree because P's slot7 probability is zero. Neither total definition is repaired or identified off the active set. All table bounds are finite consequences of these displayed entries, supplying typed angle constructors internally.

## A6. Eight-wire stage embeddings [N14–N18,CTX-8,PHASE-8]

The eight-wire order is system(q0,q1,q2), selector(q3,q4,q5), coefficient q6, work q7. Write j=x0+2x1+4x2 and s=x3+2x4+4x5. The exact decoding is
\[
 x\longleftrightarrow (x6,\ (s,\ (j,x7))).
\]
The inverse writes those bits into those wires. These are inverse maps on all256 states, including both work values. There is no assumed clean workspace in this adapter.

The amplitude loader uses six controls (q0,…,q5), target q6, and angle \(2\arccos c_{\mathrm{paper7}}(s,j)\). Its total64-branch angle table is fully determined by A5. The controlled compiler of A4 and the inverse decoding give equality with the logical block \(R(c_{\mathrm{paper7}}(s,j))\), with coefficient row AND column arbitrary. All other coordinates, including q7, are spectators on the full carrier. Its program phase is0; its circuit has64RY and126CX. This says nothing about SELECT's action on dirty q7.

The selector PREPARE embeds h on q5, m controlled by q5 on q4, and l controlled by (q4,q5) on q3. High, middle and low stage matrices are the same Fin8 matrices as in A4, under the displayed bit equivalence. For each stage, equality of all physical non-target bits is exactly equality of the coefficient bit, the corresponding non-target selector bits and the pair (system,work). The target-bit matrix entry and control assignment therefore agree. Multiplication yields \(I_{\mathrm{coeff}}\otimes(P\otimes I_{\mathrm{system,work}})\); reversed daggers yield its exact adjoint on the whole256-dimensional carrier.

For context only, the imported reversible eight-wire SELECT first flips selector q3,q4, uses the literal A3 adder with a=system,b=selector,work7, then flips q3,q4 back. On clean work it sends (s,j) to (s,r_s(j)) and restores work. On dirty work it is the actual reversible macro extension, not a newly chosen tensor identity: if \(b=\mathrm{bits}(d_s)\), original system bits a and work w, its intermediate formulas are
\(u=w\oplus b0a0,\ v2=a2\oplus u a1,\ v1=a1\oplus b0a0\),
then \(a0'=a0\oplus b0,\ a1'=v1\oplus b1,\ a2'=v2\oplus b1v1\oplus b2,\ w'=w\).
The amplitude spectator theorem cannot prove anything stronger about this SELECT.

The two eight-wire target modules supply stages and their exact full-carrier refinements. The final paper-seven block-encoding consumer is not one of the nine targets and is not a third newly admitted route in this source.

## A7. The coherent nine-wire Figure-4 construction [N19–N27,N24,N25,F4 suppliers]

### A7.1 Physical coordinates and PREPARE

The nine-wire order is address/selector(q0,q1,q2), system(q3,q4,q5), coefficient q6, indicator q7, work q8. Full decoding is
\[
 x\longleftrightarrow (x6,\ (s,\ (j,(x7,x8)))).
\]
Its inverse writes those coordinates back to exactly those wires. The FULL system factor includes both indicator and work. P embeds on targets q2,q1,q0 with controls q2 and (q1,q2), preserving q3–q8 on ALL512 states. Its program phase is0 and its dagger is the exact inverse lift.

Write \(T(s,j,a,i)\) for the basis state with those selector/system/coefficient/indicator values and work0. This is a notational abbreviation for an explicit zero-work input, NOT a fact that a physical work register is automatically initialized.

### A7.2 Indicator, bulk and boundary loaders

The correct bulk predicate is \(\beta(j)=[j=3\text{ or }j=4]\), a row test on D-transpose, i.e. a column test on D. It is NOT the row-bulk condition2≤j≤5. Columns2 and5 differ from the periodic stencil: M02=−2 instead of−1 and M75=−2 instead of−1.

The literal reversible indicator list is X(5), C3X(3,4,5;7|8), X(5), X(3), X(4), C3X(3,4,5;7|8), X(4), X(3), where each C3X expands to the three CCX instructions of A2. It pattern-matches system bits011 and100. On work0 it preserves selector,system,coefficient, restores work0, and toggles indicator by β(j), for BOTH initial indicator bits. Its compiled primitive program equals its actual full-space permutation, with macro phases retained. The inverse used later is its PROGRAM DAGGER, not a hand-chosen clean-sector extension.

Define the bulk coefficient array, in slot order0,…,7,
\[
 b_s=(0,-1,16,-30,16,-1,0,0)_s/32.
\]
The bulk loader controls (q0,q1,q2,q7), targets q6, and uses total angle \(2\arccos b_s\) if indicator=1, otherwise literal0. The boundary loader controls (q0,q1,q2,q3,q4,q5,q7), targets q6, and uses total angle \(2\arccos c_{\mathrm{Fig4}}(s,j)\) IFF indicator=0 AND NOT β(j); otherwise literal0. The extra NOT β(j) is part of its total definition and is not dropped on unreachable branches. Both work q8 and every non-target bit are full-context spectators.

Chronology is bulk loader then boundary loader. For the actual indicator value β(j), precisely the correct branch is active; \(c_{\mathrm{Fig4}}(s,j)=b_s\) when β(j). Hence their ENTIRE2×2 coefficient product is \(R(c_{\mathrm{Fig4}}(s,j))\), not only its00 entry. Inactive branches use RY(0)=I; an active zero coefficient uses RY(π), not an inactive identity. This distinction preserves signs and coherent off-diagonal amplitudes. The two compilers use k=4 and k=7 and zero program phases, giving16RY/30CX and128RY/254CX respectively.

The source labels “paper-literal single arccos” and “corrected executable double arccos” are retained as local historical interpretation labels. This source uses the standard-RY doubled angle; it does not newly establish an original-paper typo finding.

### A7.3 Distinct D-transpose and D accesses, swap and cleanup

Let \(e_s=(s+5)\bmod8=(5,6,7,0,1,2,3,4)_s\). For every slot, \(d_s+e_s=0\bmod8\).

The literal D-transpose access first emits X(0),X(1), converting selector s into \(s\mathbin{\oplus}3=d_s\), then emits the A3 adder with a=(q0,q1,q2), b=(q3,q4,q5), work=q8. It does NOT flip address bits back afterwards. On clean work its action is
\[
 T(s,j,a,i)\longmapsto T(r_s(j),j,a,i).
\]
The D access first emits CCX(0,1;2), CX(0;1), X(0), X(2), converting s into e_s (increment by1 modulo8 then toggle the high bit), then the same address-plus-system adder. Its clean action is
\[
 T(s,j,a,i)\longmapsto T((j+e_s)\bmod8,j,a,i).
\]
These distinct accesses are compiled as actual reversible lists. The register swap is the literal nine CX list implementing SWAP(0,3), SWAP(1,4), SWAP(2,5), each SWAP(u,v)=CX(u;v),CX(v;u),CX(u;v). It preserves coefficient,indicator,work.

After the coefficient loader, the post-loader chronology is D-transpose access, indicator-program dagger, homogeneous f=1 identity, register swap, D-access-program dagger. Its clean transcript, for every slot,column and BOTH coefficient basis values b, is
\[
\begin{aligned}
 T(s,j,b,\beta(j))
 &\xrightarrow{DT}T(r_s(j),j,b,\beta(j))\\
 &\xrightarrow{I^\dagger}T(r_s(j),j,b,0)\\
 &\xrightarrow{\mathrm{SWAP}}T(j,r_s(j),b,0)\\
 &\xrightarrow{D^\dagger}T(s,r_s(j),b,0).
\end{aligned}
\]
The last arrow is justified by applying forward D to its claimed preimage:
\(r_s(j)+e_s=j\bmod8\). Bijectivity then gives the inverse action. Thus work q8 stays/restores0 and indicator q7 becomes0 without any all-dirty-work simplification. The earlier standalone transported-cleanup fact permits an arbitrary indicator value and preserves it when the indicator dagger is omitted; it is not a different cleanup convention.

### A7.4 Full coefficient coherence, physical refinement and projected block

The actual middle is indicator, derivative loader, then the post-loader program. Starting from \(T(s,j,a,0)\), indicator writes β(j); the exact loader makes \(\sum_b R(c_{\mathrm{Fig4}}(s,j))_{b,a}T(s,j,b,\beta(j))\); the post-loader permutation acts on each b by A7.3. Consequently
\[
 B\,|a,s,j,0,0\rangle=
 \sum_{b=0}^1 R(c_{\mathrm{Fig4}}(s,j))_{b,a}
 |b,s,r_s(j),0,0\rangle .
\]
This proves the full clean middle entry
\[
 B_{(b,s,i,0,0),(a,t,j,0,0)}
 =\mathbf1_{s=t}\mathbf1_{i=r_t(j)}
 R(c_{\mathrm{Fig4}}(t,j))_{b,a}
\]
for arbitrary a,b∈Fin2 and s,t,i,j∈Fin8. The declaration named AllWorkspaceClean checks indicator followed by the POST-LOADER basis permutation; it does not itself contain the coefficient loader. Coherence comes from the separate full2×2 loader equality and its composition with the post-loader, as just shown. A basis-cleanliness lemma alone would not prove this formula.

The whole program is chronological PREPARE, middle, PREPARE dagger. Its matrix is exactly the reindexed \(P^\dagger B P\), including every emitted macro phase. The EVALUATED stored phase of this Figure4 program is −9π/8: indicator and indicator-dagger phases cancel; DT contains five CCX macros, while D contains six and is daggered; all other constituent program phases are0. This is an equality of the interpreted angle sum, not a claim that its angle syntax is already simplified. Full-space unitarity follows separately because every emitted primitive gate and scalar phase is unitary, not because its clean submatrix has the right value. On coefficient,selector,indicator,work all0, contract the two selector amplitudes:
\[
 U_{\mathrm{clean}}(i,j)=
 \sum_{s<7}\mathbf1_{i=r_s(j)}
 \overline{P_{s0}}P_{s0}\,W_{s,j}/32
 =M_{ij}/224 .
\]
Only squared selector amplitudes enter. The active-slot decomposition and padded zero from A5 supply the final equality; no SELECT/cleanup/table/phase fact has become a new final public premise.

Flatten the actual512 matrix using \(\ell_9\). The clean index is \(\ell_9(T(0,j,0,0))=8j\). The final exact root therefore says \(\forall i,j\in\mathrm{Fin}8,\ U_{8i,8j}=(A_{ij}/(56/3):\mathbb C)\), with NO normalization, PREPARE, SELECT, cleanup or refinement hypotheses supplied by the caller. Those facts were constructed as dependencies above. The candidate/refinement/witness packaging is specified separately in A10.

## A8. Full signed symmetry sectors, cyclic prerequisite and XOR circuit [N28–N37,D02,D03]

### A8.1 Coordinates, signed sectors and total tables

Let \(\rho(p)=7-p\) for p∈Fin4. Pair coordinates are (e,p)∈Fin2×Fin4, mapped to original index p when e=0 and 7−p when e=1. The physical coordinate circuit C is CX(2;1),CX(2;0). Its bit action sends low pair bits (p0,p1) to (p0⊕e,p1⊕e), retaining e=q2; hence its integer image is p for e=0 and7−p for e=1. The same two gates are emitted on both sides of the final circuit; C is an involution, not a free relabeling.

Set \(T_{pq}=M_{p,q}\) and \(K_{pq}=M_{p,7-q}\). In pair order the original integer matrix is \(\begin{pmatrix}T&K\\K&T\end{pmatrix}\) by centrosymmetry. Define the ACTUAL sectors \(M_+=T+K,\ M_-=T-K\):
\[
 M_+=\begin{pmatrix}
 -30&32&-2&0\\16&-31&16&-1\\-1&16&-30&15\\0&-1&15&-14
 \end{pmatrix},\qquad
 M_-=\begin{pmatrix}
 -30&32&-2&0\\16&-31&16&-1\\-1&16&-30&17\\0&-1&17&-46
 \end{pmatrix}.
\]
All sector entries are now specified; the former G05 provider-name-only gap is not replaced by another unspecified expectation.

For the CYCLIC prerequisite use \(\pi_s(p)=(p+s)\bmod4\), with total weight \(V_e(s,p)=M_e[\pi_s(p),p]\), where e=0 selects plus. Rows s and columns p of the complete tables are
\[
 V_+=\begin{pmatrix}-30&-31&-30&-14\\16&16&15&0\\-1&-1&-2&-1\\0&32&16&15\end{pmatrix},
\quad
 V_-=\begin{pmatrix}-30&-31&-30&-46\\16&16&17&0\\-1&-1&-2&-1\\0&32&16&17\end{pmatrix}.
\]
The cyclic amplitude is V_e(s,p)/56 and its exact angle is twiceArccosRational of that rational; |V|≤46 gives the bound. The three-wire SymmetryFourSlotPrimitive module supplies C's physical action and these exact angle interfaces ONLY. It does not supply a primitive cyclic SELECT or whole cyclic circuit.

For XOR use \(\chi_s(p)=p\mathbin{\oplus}s\), preserving sector e. Its total weight is \(Z_e(s,p)=M_e[\chi_s(p),p]\), and the complete tables are
\[
 Z_+=\begin{pmatrix}-30&-31&-30&-14\\16&32&15&15\\-1&-1&-2&-1\\0&16&16&0\end{pmatrix},
\quad
 Z_-=\begin{pmatrix}-30&-31&-30&-46\\16&32&17&17\\-1&-1&-2&-1\\0&16&16&0\end{pmatrix}.
\]
The actual XOR coefficient is \(z_e(s,p)=Z_e(s,p)/56\). All32 values are specified and bounded by1, and their angles use twiceArccosRational. These tables are not interchangeable with V: at p=1,s=1 the cyclic weight is16 and XOR weight32. No unspecified cyclic orientation remains.

### A8.2 Physical six-wire construction and proof

The six-wire middle order is pair(q0,q1), sector q2, selector(q3,q4), coefficient q5. The exact middle decoding is
\[
 x\longleftrightarrow (x5,\ (x3+2x4,\ (x2,x0+2x1))).
\]
The inverse writes those bits, so the context/bijection is explicit on all64 states. There is no extra work wire. The five controls q0–q4 select coefficient-target q5 with angle \(2\arccos z_e(s,p)\). The A4 compiler proves the whole block diagonal equals the logical amplitude lift, retaining sector and selector and exact phase0. The coefficient is evaluated at the INPUT p before SELECT.

Physical SELECT is exactly CX(3;0),CX(4;1). On every basis state it sends (e,p) to (e,p⊕s), preserving selector and coefficient. Selector PREPARE P4 is RY(3;π/2),RY(4;π/2); its adjoint reverses and negates those rotations. Its clean-column probability on each of the four physical selector labels is1/4.

The middle chronology is P4, amplitude, SELECT, P4 dagger. For each fixed sector, XOR permutes the four rows exactly once, so its clean block is
\[
 \frac14\sum_{s=0}^3\mathbf1_{r=p\oplus s}Z_e(s,p)/56
 =M_e[r,p]/224.
\]
There is no transition between different sectors in this middle. Full middle unitarity is obtained independently from the unitary preparation, amplitude blocks and permutation SELECT.

Let \(c=1/\sqrt2\) and \(S=\begin{pmatrix}c&-c\\c&c\end{pmatrix}\otimes I_4\), the EXACT standard RY(π/2) on sector. It is not the sign-different Hadamard. The pair-circuit chronology is S dagger, middle, S, hence matrix \(S U_{\rm mid}S^\dagger\). Direct block multiplication gives
\[
 S\,\operatorname{diag}(M_+,M_-)\,S^\dagger
 =\begin{pmatrix}T&K\\K&T\end{pmatrix}.
\]
The full physical chronology is C, S dagger, P4, amplitude, SELECT, P4 dagger, S, C. Each physical C is its own inverse permutation; reindexing the final pair order to the original eight system labels therefore gives the original M/224 block.

The original-index adapter includes the physical first C before the middle decoding. Its flattened original logical index equals the six-bit little-endian index on EVERY basis state, not just clean states. Thus the emitted primitive matrix equals the reindexed logical flat unitary exactly, and the zero-phase PrimitiveProgram has the same equality. Clean inputs and outputs set q3=q4=q5=0 while q0–q2 retain the original system label; their flat index is j. The final physical root is \(\forall i,j\in\mathrm{Fin}8,\ U_{i,j}=M_{ij}/224\) at those explicit clean embeddings, with no caller-supplied PREPARE/SELECT/angle/table hypotheses. The sector q2 remains a system bit throughout the projection.

The aliases warmRobinFourSlotT3FlatUnitary and warmRobinFourSlotPrimitiveVerifiedBlockEncoding point to THIS XOR object. They do not prove the cyclic route from A8.1. The generic conjugation lemma in A9 is conceptually applicable to the signed S step, but no actual XOR import/implementation dependency is inferred merely from that applicability.

## A9. Precisely quantified system-conjugation algebra [N38,N39,RECT-LEFT,RECT-RIGHT]

Let C,S,H be arbitrary types. For defining \(Q_{c_0,s_0}(U)\), no finiteness or decidable-equality instances are required: U is simply a complex entry function on \((C\times(S\times H))^2\), and chosen elements c0∈C,s0∈S define
\[
 Q_{c_0,s_0}(U)_{ij}=U_{(c_0,(s_0,i)),(c_0,(s_0,j))}.
\]
The clean elements need not be zero. Their existence is supplied by these element arguments, not a separate Nonempty premise.

For the following lifts, entries and products, assume exactly Fintype and DecidableEq on EACH of C,S,H. Let V:H×H→ℂ be arbitrary. Define
\[
 L(V)=I_C\otimes(I_S\otimes V),\qquad
 L(V)_{(a,s,i),(b,t,j)}=\mathbf1_{a=b}\mathbf1_{s=t}V_{ij}.
\]
The adjoint entry is the same delta factors times \(\overline{V_{ji}}\). Define \(\mathrm{Conj}(V,U)=L(V)(U L(V)^\dagger)\) for any square U on the full product. No unitarity is assumed in these definitions or entry identities.

The LEFT rectangular lemma additionally has an arbitrary type K with Fintype K but NO DecidableEq K premise; A is a rectangular matrix \((C\times(S\times H))\times K\to\mathbb C\). For every chosen c0∈C,s0∈S,i∈H,k∈K and arbitrary V,
\[
 (L(V)A)_{(c_0,(s_0,i)),k}
 =\sum_{r\in H}V_{ir}A_{(c_0,(s_0,r)),k}.
\]
The RIGHT rectangular lemma instead has an arbitrary type R with Fintype R but NO DecidableEq R premise; A has shape \(R\times(C\times(S\times H))\to\mathbb C\). For every r0∈R and j∈H,
\[
 (A L(V)^\dagger)_{r_0,(c_0,(s_0,j))}
 =\sum_{t\in H}A_{r_0,(c_0,(s_0,t))}\,\overline{V_{jt}}.
\]
The extra finite row/column carrier is retained even though it is not the summation index. Neither lemma assumes V unitary. Expanding the matrix product and summing the C,S Kronecker deltas proves each equation.

Applying the two rectangular formulas yields, for arbitrary V,U,
\[
 Q_{c_0,s_0}(\mathrm{Conj}(V,U))
 =V\bigl(Q_{c_0,s_0}(U)V^\dagger\bigr).
\]
This clean-block identity has NO unitarity hypothesis on either matrix. Separate statements give: if V is unitary, L(V) is unitary; if BOTH V and full U are unitary, \(\mathrm{Conj}(V,U)\) is unitary. Tensor identity factors prove the first, and multiplication of three unitaries proves the second. Finite empty carriers are not excluded by an unstated dimension assumption; the chosen clean elements simply cannot be supplied if C or S is empty. No elementary circuit, oracle, finite-bit or cost construction of an arbitrary V follows.

## A10. Actual certificate fields, witnesses, defaults and resources [N27,N36,N37,F4/XOR suppliers]

### A10.1 Generic schema versus these concrete instances

QueryOperatorTarget holds an operator entry function, a scalar normalizer, source and semantic-contract STRINGS, and freeParameters defaulting to []. The concrete shared target stores A as a complex matrix, scalar56/3 and an empty parameter list. Its source String is "Guseynov-Huang-Liu 2025, fixed N=8 homogeneous Robin instance"; its contract String is "the coefficient=0 and selector=0 clean block equals A/(56/3) exactly". These strings describe intended semantics; they do not prove it.

For systemQubits=n, OperatorBlockEncodingCandidate stores auxiliaryQubits=a; a matrix of size \(2^{n+a}\); the target; a RegisterLayout; a legacy circuit; schedule DEFAULT []; a Resource; the actual equality layoutMatches:layout.signalQubits+layout.pureAncillas=a; and two freely chosen fields isUnitary:Prop and blockContainsTarget:Prop. The schema itself does not enforce that those arbitrary Props have their intended meanings, does not enforce layout.systemQubits=n, and does not tie the legacy circuit/schedule/resource to the stored matrix. LayoutMatches alone is only its stated Nat equality.

VerifiedOperatorBlockEncoding stores that candidate and two terms: unitaryProof:candidate.isUnitary and blockProof:candidate.blockContainsTarget. Its name and arbitrary stored Props alone are not universal semantic certification. These two CONCRETE candidates instantiate the Props with actual complex matrix-unitary-group membership and explicit forall-entry target equations. Their actual witness terms are provided separately by the constructions above; no Bool named proved is used.

PrimitiveRefinement(q) separately stores an actual PrimitiveCircuit, a complex target matrix on B_q, and a term of exact matrix equality. PrimitiveProgramRefinement(q) instead stores the PrimitiveProgram and equality INCLUDING its scalar phase. These are stronger than lossy presentation Strings; neither is replaced by a mere label.

For Figure4 the candidate has n=3,a=6, unitary=the flattened ACTUAL nine-wire program matrix, layout(system3,signal4,pureAncillas2), and blockContainsTarget equal to the explicit A7 equation at clean indices8i,8j. The unitary witness is primitive-program unitarity followed by reindexing; the block witness is A7's contraction and literal target identity. Its program-refinement witness is the exact physical \(P^\dagger B P\) equality from stage composition. Its constructor does not set schedule, so schedule=[] remains the inherited data default; it is not an execution or depth certificate.

For XOR the candidate has n=3,a=3, unitary=the64×64 LOGICAL flat XOR matrix, layout(system3,signal3,pureAncillas0), and blockContainsTarget the explicit clean-entry target equation using original-system indices. Its unitary witness is logical LCU and conjugation unitarity; its block witness is A8's sector/deconjugation equality. The separate PrimitiveRefinement links the emitted six-wire list to that exact flat matrix; a zero-phase program equality is also supplied. Again schedule=[] is the inherited default. These separate proofs/fields are all necessary to describe the actual concrete construction; none is inferred from the projected block alone.

Both legacy presentations map X to oneQubit "X", RY/RZ to rotationY/rotationZ with angle String "exact-angle", and CX to cnot with wire values. They lose actual angle expressions and, for a Program, its scalar phase. They are presentation-only, not the authoritative matrix denotation. The primitive list/program and exact-refinement witnesses own the semantics.

### A10.2 Resource interpretation and exact list arithmetic

Resource has fields oneQubit,cnot,oracleCalls,pureAncilla,depth, each default0, with gates=oneQubit+cnot+oracleCalls. PrimitiveCircuit.resource computes oneQubit as the number of X/RY/RZ instructions, cnot as the number of CX instructions, and sets oracleCalls=0 AND pureAncilla=0. It computes depth by starting every wire at0 and, for each chronological gate, assigning each touched wire \(1+\max\{\text{current depth of all touched wires}\}\); other wires retain their values. The final depth is the maximum wire depth. This is the particular all-to-all logical scheduling convention, not a hardware routing theorem.

PrimitiveProgram.resource is exactly its LIST resource. The separate scalar phase is semantically retained but has no separate resource charge. Primitive resources do not count initialization, table/angle evaluation, state input, measurement, postselection, amplification or finite-bit rotation synthesis.

Consequently Figure4's physical layout pureAncillas=2 is NOT equal to its primitive Resource.pureAncilla=0, and neither value should be silently substituted for the other. The two physical wires q7,q8 must really begin/end clean in the block contract; they are not free because a bookkeeping field is0. XOR has no additional physical work wire, with three signal auxiliary wires; its sector remains system. Auxiliary score data is layout signal+pure ancillas, not the primitive resource's work field.

The literal unsimplified primitive list arithmetic is:
\[
\begin{array}{c|rrrrr}
 &\mathrm{oneQubit}&\mathrm{CX}&\mathrm{depth}&\mathrm{oracleCalls}&\mathrm{Resource.pureAncilla}\\
 \text{seven-selector PREPARE}&7&8&13&0&0\\
 \text{fixed three-bit adder}&55&33&53&0&0\\
 \text{XOR AMPLITUDE ONLY}&32&62&94&0&0\\
 \text{FULL XOR circuit}&38&68&96&0&0\\
 \text{FULL Figure4 program}&427&454&674&0&0
\end{array}
\]
These are author reconstructions by the explicit integer recurrence on the displayed emitted lists, NOT newly executed Lean proof results. For XOR, add4 selector RY,2 sector RY,2 SELECT CX and4 coordinate CX to the amplitude list, giving38RY/68CX (106 gates), not32RY/62CX for the whole circuit.

For Figure4 the two selector lists give14RY/16CX; the indicator and its DAGGER together give144 one-qubit/72CX; bulk+boundary loaders give144RY/284CX; DT access gives57 one-qubit/33CX; D dagger gives68 one-qubit/40CX; register swap gives9CX. Summing gives427 one-qubit/454CX (881 gates), subdivided as204RY,207RZ,16X. Depth uses the actual reversed primitive lists for daggers, not a repeat of forward lists or the empty candidate schedule.

No betterThan ranking, new scoring rule, lower bound, finite-bit/Clifford+T efficiency, hardware connectivity claim, numerical approximation, arbitrary-width resource theorem or source-paper asymptotic theorem is added. Zero abstract queries means every instruction in THIS primitive list is explicit, not that classical data or precision is free.

## A11. Source/proof boundaries and the remaining review [N40,G01–G06 history]

All circuit, table, matrix, predicate, adapter and record definitions above are literal on their declared total carriers. Equiv.ofBijective packages the explicitly specified finite bijection and its inverse; it does not choose an arbitrary quantum representative. No uniqueness fiction, quotient/global-phase identification, default/zero repair or new oracle premise is introduced. Bounds, PREPARE/SELECT/inverse facts, cleanup, reindexing, table identities, full unitarity and actual proof witnesses remain construction dependencies of the closed fixed-target statements, not newly supplied final Anchor hypotheses.

The generic conditional interfaces in A2,A4,A9 preserve their EXACT stated local inputs: six constructor guards versus eight clean guards plus work0; control-to-target inequalities without extra control injectivity; arbitrary finite rectangular carriers and chosen clean elements; unitarity assumptions only on the separate unitarity conclusions. Exact formal signatures and complete source bodies remain pinned in the companion audit proposal. Attributes, namespaces, opens and local maxRecDepth/maxHeartbeats/transparency settings are ambient proof context, not mathematical premises. Existing native-decide proof bodies were read, not run. No fresh compiler/axiom/kernel gate is claimed.

This source supplies concrete content for historical G01–G06/Q07/Q08 rather than retroactively changing the original104 lines or using the late Stage3 no-contradiction report as proof. Independent source-only review must still decide the new source coverage/topology; later source/formal review must decide fidelity to the original formal declarations and full module contracts. Original-paper authentication, arbitrary-width Robin oracle/compiler/resource theorems, the external final paper-seven consumer, whole RobinMatrix review, compilation, main admission, publication and purification remain separate. Graph alternatives are matched only at the projected fixed M/224 target, not full matrices, work layouts or resource equivalence.
