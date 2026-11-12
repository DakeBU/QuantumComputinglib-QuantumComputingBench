# Path-sanitized export of immutable phase-1 notes

This is a new export, not the original sealed file. Original notes SHA-256: `be330a1b3b5f30d66dfd9a41a62bc7fdb3ae79d8ceee288c0c0bfb4ae17e0485`. Only the private source-path reference is replaced with `$AUTHOR/source-only.md`; the original content and historical phase-1 state are otherwise retained below. Original phase-1 bytes were not rewritten. The export header is added provenance, not a new mathematical verdict.

# c29 independent source-first review — phase 1

## Identity, scope, and evidence boundary

Reviewer: the actual independently assigned agent `/root/cubic_source_first_review_c29`. This document was written by that agent, not by the source author or a synthetic reviewer. Historical formalizer: UNKNOWN. Source provenance: retrospective local exposition, not an external paper, a pre-proof statement seal, or a novelty claim.

Only mathematical source read: `$AUTHOR/source-only.md`, 507 lines. SHA-256 independently read from its bytes before mathematical review:

`e3e594b40b44bd474a4c98cf61c052b5f2a42ec8082de8d6164bd4f1e1df3dc7`.

The seven allowed governance documents were read completely: AGENTS.md; HARNESS.md; qbe-substantive-worker/SKILL.md; qbe-source-dependency-audit/SKILL.md; theorem-publication-protocol.md; proof-digestion-protocol.md; evidence-routed-memory-protocol.md. A truncated combined tool display was followed by a complete separate read of proof-digestion-protocol.md and a complete line-numbered read of the source. No other project material was read. No Lean, exact formal signatures, author-side supplementary files, coverage/atlas/registry/graph files, previous decoder/review/build/cache/runtime evidence, Git, network, simulator, or subagent was used. This is an independent reconstruction, not approval of an unseen extractor's graph.

Phase-1 conclusion: the substantive algebraic assertions in the pinned source check out under their explicitly stated guards and their deliberately limited semantics. No source-internal mathematical counterexample was found. The source leaves important circuit/resource questions OPEN; these omissions are declared boundaries, not counterexamples to its weaker claims. This is neither formal-source equivalence approval nor Lean/build acceptance. The final formal binder audit, implementation comparison, and exact-signature seal remain UNASSESSED and require separate authorization.

## Independent mathematical derivation

### M01 — targets, endpoints, ranges, and conservative normalization (S01–S02)

Let n be natural, N=2^n>=1, and 0<=j<N. In Q, division by N preserves order, so 0<=x_j=j/N<1. Multiplying nonnegative inequalities gives 0<=x_j^3<1 and x_j^6<=1. For every natural k, the source's weaker x^k<=1 follows from the base x^0=1 and x^(k+1)=x^k*x<=1*x<=1. Therefore

`s_n = sum_j x_j^6 <= sum_j 1 = N <= N*N`.

The second inequality follows from N*(N-1)>=0. Thus the stated alpha=N meets the squared algebraic bound s_n<=alpha^2. This neither chooses a unitary nor asserts a circuit.

The target action is immediate from columns: (Oe_0)_r=a_r, whereas Oe_c=0 for c!=0. D acts as (Dz)_r=a_r z_r. At n=1, O_(1,0)=1/8 but D_(1,0)=0, and O_(1,1)=0 but D_(1,1)=1/8. This is a minimal witness against conflating the two targets. At n=0 all are 1-by-1 zero matrices and v=0; the phrase “rank-one operator” describes the outer-product form, whose actual rank degenerates to zero here. The source explicitly excludes normalized state preparation at this endpoint, so this is a terminological degeneracy, not a hidden normalization repair. For n>=1, j=1 exists and a_1>0, hence s_n>0, but its normalized state still needs a distinct implementation theorem. The O scale N and the D/X scale 1 must never be interchanged without rescaling the actual extracted block.

Exact diagnostic recomputation:

- n=1: (0^6+1^6)/2^6=1/64.
- n=2: (0+1+64+729)/4^6=794/4096=397/2048.
- n=3: (0+1+64+729+4096+15625+46656+117649)/8^6=184820/262144=46205/65536.

All three source numbers are correct; none is evidence of an asymptotic or finite-bit algorithm. The exploratory tolerance is the literal rational 1/10^10, not a derived numerical accuracy guarantee.

### M02 — counting and rank-one conditional contract (S02–S03)

For k<=m, inclusion of {0,...,k-1} into {0,...,m-1} identifies exactly the entries satisfying t<k, giving cardinality k. Strict monotonicity of natural cubes gives j^3<N^3; exponent arithmetic gives N^3=2^(3n), N^4=2^(4n). Applying the counting lemma with k=j^3,m=N^3 yields j^3 accepted threshold indices. In Q, `(j/N)^3/N=j^3/N^4` since N!=0. At n=0 this says 0 accepted indices in a one-element threshold carrier, consistently.

For arbitrary rational alpha, split c=0 versus c!=0. In the first case the supplied column condition gives alpha B_rc=a_r=O_rc; in the second alpha B_rc=alpha*0=0=O_rc. This proves alpha B=O without alpha!=0. At n>=1 the contract cannot actually be inhabited for alpha=0 (j=1 is a witness), but that does not invalidate this implication. Adding alpha!=0 to this implication would be a needless strengthening of its hypotheses.

Label accounting independently agrees: 7 middle labels give depth/call counts 7; adding filter, row generation, and filter cleanup gives 10. Wrapped pure workspace is 4n+p+3, total auxiliary 4n+p+4; n=2,p=40 gives 52. Counting pure workspace is 1+4n+(4n+3)=8n+4, total auxiliary 8n+5, giving 21 at n=2. Its eight listed stages give eight labels/depth. These are exact syntax counts only. Nothing in the counting ratio derives Hadamard phases, rejection, inverse semantics, or the zero/nonzero input-column action. Preserving a separate reject signal is a stated design requirement; the described reject label is not evidence that it is met. Row generation/XOR not being undone is consistent with the desired output row, but still lacks an interpreted quantum transcript.

### M03 — rational reflection (S04)

For e=e_0, unit v and w=e-v,

`d = (e-v) dot (e-v) = 1-2v_0+1 = 2(1-v_0)`.

The guard v_0!=1 makes d!=0. Put c=2/d and H=I-c w w^T. Then

`H_00=1-(2/[2(1-v_0)])(1-v_0)^2=v_0`.

Expanding a column inner product uses sum_k delta_ki delta_kj=delta_ij, sum_k delta_ki w_k=w_i, and sum_k w_k^2=d. Thus

`(H^T H)_ij=delta_ij-2c w_i w_j+c^2 d w_i w_j=delta_ij`,

because c^2 d=4/d=2c. H is symmetric, so the same argument yields HH^T=I. All operations are rational, and no square root is needed. This proof establishes both row and column orthogonality on the stated locus. Literal totalized division defines H outside that locus but does not license these restricted conclusions there. For example v=0 has d=1,H_00=-1, not v_0=0; unit norm cannot be dropped. The source retains v_0!=1 even though a separately proved special v=e branch could extend the result; this review does not silently extend its theorem.

### M04 — flattened direct sum and fibers (S05)

For b<8,s<N, bN+s<8N. Conversely, q<8N has s=q mod N<N and b=floor(q/N)<8; Euclidean division gives q=bN+s. Encoding followed by decoding returns b,s. Consequently s -> 0*N+s is an injective clean embedding, and b -> bN+s is injective on each fiber.

For columns (c,t),(d,u), a summand in U^T U can be nonzero only at a row (b,s) with s=t and s=u. If t!=u every summand vanishes. If t=u, the sum reduces exactly to sum_b H(v_t)_bc H(v_t)_bd=delta_cd by M03. The ambient identity entry is delta_tu delta_cd. The row proof similarly fixes a common system label and invokes HH^T. Flattening is a bijection, so discarding zero summands and permuting the fiber enumeration preserves the finite sum; no term is counted twice. This justifies the source's fiber argument, including both orthogonality directions.

At b=c=0, the block is zero for r!=c, and for r=c it equals H(v_r)_00=q_r, so it is diag(q). Branch unit norm AND the branch nontrivial-coordinate guard AND the coordinate equation are all required for this conclusion via the stated route. For q=x or q=a, M01 supplies the guard. For supplied q it remains an independent condition. The eight-dimensional ancilla is three qubits in this mathematical basis convention; this is not the one-signal transcript's layout.

### M05 — four-square existence and noncanonical witnesses (S06)

External mathematical input: Lagrange's four-square theorem, every natural residual is a sum of four natural squares. This review uses that named classical theorem; it does not pretend to reprove it from first principles or to have checked any formal implementation or citation ledger.

Since j<N, j^2<=N^2 and j^6<=N^6. Thus natural residuals R_2=N^2-j^2 and R_6=N^6-j^6 satisfy j^2+R_2=N^2 and j^6+R_6=N^6. A four-square witness for each residual gives the displayed source equations. Dividing the first sum of squares by N^2 and the second by N^6 proves that each corresponding eight-vector has squared norm one. Its zeroth coordinate is respectively j/N or j^3/N^3=(j/N)^3. The remaining three coordinates are literally zero. Since J is finite, witnesses can be selected for all j to give a branch family; no efficient search claim follows. Apply M03 and M04 with the range guard to obtain an 8N-by-8N rational orthogonal matrix with clean block X or D.

There is no unique choice. For n=0, residual 1 can use four-square witnesses (1,0,0,0) or (0,1,0,0). The associated v=e_1 or e_2 gives different H off the clean block (H_01=1 in the former and 0 in the latter), while H_00=0 in both. This explicitly validates representative dependence of the matrix and independence of the certified target block. Noncanonical representative selection, rather than unique characterization, is the right semantics. No particular quotient carrier is required by the source.

Forgetting fields of a stronger record preserves its stored equality, but cannot create properties absent from the smaller record. In particular arbitrary embeddings in the generic payload are not automatically injective, and arbitrary cleanup/resource proposition fields are not physical cleanup/cost semantics. The explicit chosen Householder embedding is injective by M04, but its “cleanup” field is only the same clean-block equality. A one-label transcript has no denotation link to this matrix. The generic cubic payload need not target D; target=D is an additional assertion of the chosen instance, not a consequence of its generic name.

### M06 — diagonal products and conditional QSVT (S07)

For diagonal A=diag(f),B=diag(g), `(AB)_rc=sum_k delta_rk f_r delta_kc g_k`. Only k=r survives, leaving delta_rc f_r g_r. Applying twice yields X^3=diag(x^3)=D. If an extracted clean matrix B equals X, substitution into finite sums gives B^3=D. Normalizer products and term-count metadata do not change the type of this conclusion: it is a product of extracted matrices.

A clean-block product is not the clean block of a physical product. For a concrete rational witness take the symmetric 2-by-2 orthogonal matrix U=[[3/5,4/5],[4/5,-3/5]], with its first coordinate as clean. U^2=I, hence U^3=U and clean(U^3)=3/5, whereas clean(U)^3=27/125. This directly corroborates the source's warning. Fresh ancilla/projector composition must be supplied separately.

For P(x)=x^3, M01 gives |P(x_j)|<=1. A degree field assigned 3 and a Boolean field assigned true are record values, not a phase list or a synthesis theorem. The external supplier is a full AND: certified linear input, output payload, output orthogonality, output target=X^3, and inhabited global-admissibility, cleanup, resource propositions. Substitution of X^3=D then identifies the supplied output target with D. Without specific meanings for the propositions, this is conditional record transport, not validation of physical QSVT. The source supplies no such unconditional external supplier and this review invents none.

### M07 — diagonal approximation and error predicate (S08)

The piecewise rational absolute value has |u|>=0 and |u|^2=u^2. For diagonal A,B let d_r=A_rr-B_rr. Finite-sum collapse gives `((A-B)z)_r=d_r z_r`. If |d_r|<=epsilon and epsilon>=0 then squaring nonnegative sides gives d_r^2<=epsilon^2; multiply by z_r^2>=0 and sum to obtain precisely E_epsilon(A,B). In dimension zero the universal inequality is 0<=0, so the predicate reduces exactly to epsilon>=0. In dimension one, A=I,B=0,epsilon=0,z=(1) yields the false inequality 1<=0: the relation is non-vacuous.

For A_q and D all off-diagonal entries are zero, so the scalar hypotheses give all-entry absolute error and E directly, with no dimension factor. Conversely, testing z=e_r recovers the diagonal squared bound; this confirms the source is not disguising a vacuous relation. Nothing here chooses q, proves accuracy of a numerical producer, or extends the quantification from Q to C. A supplied rational pair q_j,r_j with q_j^2+r_j^2=1 gives a unit eight-vector (q_j,r_j,0,...); with q_j!=1, M03–M04 realize diag(q). Approximation and rational unit-circle existence are distinct inputs. For instance q=1/8 has 1-q^2=63/64, not a rational square, so a two-coordinate rational branch is not available for every exact cubic value. This does not refute the four-square eight-coordinate route or the conditional statement.

### M08 — opaque primitive interface and scalar tier (S09–S10)

From `P(U) AND exists B, Extract(U,B) AND B=D`, conjunction projection and existential elimination yield exactly the stored unitarity proposition P(U) and a supplied extracted target. No fact of rational orthogonality follows from an unspecified P. Taking P constantly false prevents inhabitants; taking P constantly true does not force orthogonality. Either example is permitted by the abstract predicate vocabulary, showing why the source correctly refrains from a physical theorem. The one-signal layout and label tuple (1,1,1,1) are separate data and do not connect the label to U.

For a supplied scalar tier, apply its sole law at a=a_j using M01. This establishes `C(Theta(iota(a_j)))=iota(a_j)` for each tier; it does not construct a tier. A singleton scalar carrier with constant maps satisfies the law and need not encode distinguishable amplitudes. Thus the source's explicit absence of injectivity, trigonometric equations, and physical R_y semantics is material, not cosmetic. Workspace size is unused in this scalar statement.

### M09 — clean computation and bridge normal form (S10)

The symbolic backend is F(j,w)=(j,a_j), W=Q, readout identity. Clean correctness is immediate for w=0. W is infinite, irrespective of a declared qubit count. For n>=1 this F is not injective in w, hence cannot itself be a reversible quantum workspace transformation.

The finite backend uses M=2^(3n)=N^3 and F(j,w)=(j,j^3). Strict j^3<M makes the payload a member of Fin M, and readout j^3/M=(j/N)^3=a_j proves clean correctness. Fin M has exactly 2^(3n) elements, supporting a 3n-bit carrier interpretation, but not a circuit. For n>=1, M>1 and F(j,0)=F(j,1), again refuting reversibility of overwrite; at n=0 M=1 and this objection degenerates, without invalidating any source statement.

With known h:C and arbitrary proposition P, `(C -> P) -> P` applies the implication to h. Conversely P implies C->P by a constant function. Hence `(C -> P) iff P` in this known-premise context. This proves the source's symbolic/finite computation bridge equivalences, and the same argument handles the known scalar law to opaque-angle bridge. It does not prove P; adding the bridge as an unexplained public premise would simply move the unresolved goal into a binder.

### M10 — modular lift, one-sided generic cleanup, readonly rotation (S11)

Let p<M and w<M. These imply M>=1 and w+p<2M. If w+p<M then T_p(w)=w+p and `(T_p(w)+M-p) mod M=(w+M) mod M=w`. If w+p>=M then T_p(w)=w+p-M, and its sum with M-p equals w, so reducing modulo M again gives w. The natural subtraction equalities are legitimate because p<=M and, in the second case, M<=w+p. This proves S_p(T_p(w))=w for all dirty workspace inputs, not merely zero. On w=0, T_p(0)=p because p<M. The pair transformation keeps j unchanged. Plugging in p=j^3,M=N^3 or p=j,M=N proves both concrete value-cleanup statements, including n=0,M=1,p=w=0. This gives a reversible finite permutation mathematically, not a multiplication/adder gate expansion or cost theorem.

The generic witness stores only uncompute-after-compute=id. Without a finite-carrier axiom, it need not have the reverse law. Example with W=N, compute(w)=w+1, uncompute(w)=max(w-1,0): uncompute(compute(w))=w, but compute(uncompute(0))=1. One may set zero=0, amplitude readout constant a_j for a single-system example, and the clean backend output to 1 so all relevant generic fields can be met. The source correctly declines to promote every generic witness to two-sided cleanup. The particular finite modular maps do have inverses, which does not add a field to the generic interface.

Readonly simply says `(j,w,sigma) -> (j,w,f(j,w,sigma))`; choosing f=0 preserves j,w but is noninjective on the signal. Even a signal permutation would only be a basis permutation unless a linear amplitude semantics were supplied. Thus readonly is insufficient to prove a nontrivial R_y matrix, its angles, or coherent composition with the arithmetic backend. Backend identity and register agreement must be checked when composing any future witnesses.

### M11 — expanded conjunction and process/resource limits (S12–S13)

The five items in S12 are jointly required, not alternatives: (1) computation existence, (2) universal supplied-tier scalar law, (3) opaque cleanup, (4) opaque extraction, (5) literal diagonal target equality. M09 and M08 supply only the first two at size 3n. The transparent witness M10 is not definitionally item 3. Nothing in this conjunction is a unitarity proposition. Selecting its target-equality conjunct only recovers what was assumed. This is a valid conditional interface, not an unconditional block encoding.

Resource syntax adds one-qubit, CNOT, oracle counts for the score's gate field, sums sequential depth, and computes auxiliary count from declared signal plus workspace. A primitive label may contribute 0 elementary gates but 1 oracle call and 1 scored gate. This is internally consistent label accounting. No polynomial string is an asymptotic bound and no qubit count proves enough physical workspace. The three error ladder entries satisfy 10^-10<10^-8<10^-6: accepting either relaxed entry need not meet the original tolerance. Iteration/agent/schedule constants are process data and have no theorem-closing force. Their historical accuracy cannot be independently checked without forbidden artifacts; this review makes no such historical certification.

## Definition audit

| Source object | Kind and independent finding |
| --- | --- |
| N,J,x,a,v,O,D,X; matrix sums; zero/identity | LITERAL on the finite natural/rational carrier, including n=0. No normalized v is defined there. |
| s_n, threshold sets, rank-one two-part contract | LITERAL; finite sums/predicates, no hidden square-root or division by alpha. |
| H(v), dot, w,d | LITERAL total rational arithmetic; reflection/entry theorems guarded by unit norm AND v_0!=1. No fabricated default reflection. |
| flatten/decode, clean embedding, fibers, U | LITERAL; inverse identities derived, not extra assumed identifications. |
| four-square vectors for supplied witnesses | LITERAL conditional on those witnesses satisfying the displayed sum identity. |
| selected branch family and selected U | CHOICE/REPRESENTATIVE, not uniquely characterized. Equivalence for the stated downstream observation is equal clean block (and the construction supplies orthogonality); matrices need not be equal. No quotient type or canonicality asserted. |
| exact-clean payload, stronger input/cubic/QSVT/candidate packages | LITERAL record specifications, with only the enumerated fields. Arbitrary propositions retain their exact opaque meanings; names do not strengthen them. |
| product clean-matrix certificate; P(x)=x^3 and local labels | LITERAL algebraic certificate/metadata, not characterized physical circuit. |
| rational abs; E_epsilon; A_q | LITERAL, including dimension zero and epsilon>=0. |
| scalar-tier maps and law | SUPPLIED interface, not a uniquely characterized trigonometric object; no existence or injectivity follows. |
| symbolic/finite overwrite backends, modular maps | LITERAL, respectively infinite/finite carriers. Known clean correctness is proved rather than hidden in a producer binder. |
| generic cleanup/readonly/expanded interfaces | LITERAL field specifications; no reverse-inverse, amplitude, or unitarity fields are invented. |
| resource/policy/description fields | LITERAL metadata only; no physical denotation supplied. |

No source object is a uniquely CHARACTERIZED definition requiring an exists-unique theorem before choice. Existential four-square witnesses emphatically are not unique. There is no normalized-state quotient or global-phase quotient in the stated source. Any formal implementation introducing one would require a separate definition audit; phase-1 has not inspected one.

## Expected binder audit before formal comparison

These are source-derived expectations, NOT exact Lean signatures or an audit of unseen binders. Every project-owned formal structure/Prop alias must later be expanded recursively.

| Claim/interface | Allowed source input; produced dependency/conclusion |
| --- | --- |
| Grid range, scale, counting, diagnostic theorems | TYPING n:N; finite indices and their ranges. N=2^n and rational arithmetic are STANDING conventions. Range, capacity, count and norm bounds are PRODUCED, not new SOURCE hypotheses. |
| Rank-one conditional implication | SOURCE rational alpha, matrix B and exactly its two contract conjuncts. alpha!=0 is not required. O is fixed literally, not an arbitrary target whose equality to O is assumed. |
| Reflection theorem | TYPING v:Q^8; SOURCE unit norm AND v_0!=1. d!=0, clean entry and both orthogonality identities are PRODUCED. |
| Supplied-family direct sum | SOURCE every branch unit AND nontrivial; for diag(q), coordinate equality. Flattening validity/fiber identities are PRODUCED. |
| X/D matrix existence by four squares | Only grid/type conventions publicly required; four-square existence, branch family, normalization, guards, orthogonality and target equality must be dependency-produced. A witness may be an input to an auxiliary vector lemma, but not an extra premise of the source's unconditional existence conclusion. |
| Generic package projection | SOURCE that exact stronger package, including the field proofs it stores. The smaller package gains no extra properties. |
| Chosen cubic instance | Target=D is PRODUCED for this instance, not a generic consequence or a circular public premise. |
| Diagonal product | SOURCE matrices diagonal or literally X; target X^3=D is PRODUCED. Circuit composition or normalized-state claims are EXCESS if inferred only from this arithmetic. |
| Conditional QSVT transport | SOURCE full external supplier including input/output payloads, output orthogonality, target=X^3, and global-admissibility/cleanup/resource proposition proofs. These premises are legitimate for the explicitly conditional consumer, not grounds for claiming an unconditional QSVT construction. |
| Error transport | SOURCE supplied q, epsilon>=0 and pointwise abs error; diagonality literal or SOURCE for the generic lemma. E and all-entry error are PRODUCED; adding E itself to their premises would be EXCESS. |
| Supplied unit-circle realization | SOURCE q,r, unit-circle equality AND q!=1; approximation is separately SOURCE if claimed. |
| Primitive candidate | SOURCE opaque unitarity AND existence of extracted B with extraction relation AND B=D. Conclusions are only projections/repackaging. No unconditional physical theorem is licensed. |
| Scalar statement | SOURCE supplied tier including its law; grid range PRODUCED. Its carrier/map/functions are TYPING/interface data, not assumed real trigonometry. Unused workspace parameter does not restrict the tier. |
| Transparent computation existence | TYPING n and declared-size parameter; backends/clean correctness for the constructed instances are PRODUCED. Infinite W cannot acquire a finite-cardinality premise by its count label. |
| Opaque bridge equivalence | SOURCE arbitrary opaque proposition and known transparent premise; bridge is an object equivalent to that proposition, not a theorem producing it. |
| Modular cancellation | SOURCE naturals p,M,w with p<M,w<M; M>0 and subtraction legitimacy PRODUCED. Cubic/linear instantiations derive these bounds from grid conventions. |
| Generic cleanup/readonly projections | SOURCE those explicitly defined witness fields only; reverse inverse, coherent unitary action and actual R_y law are not fields. |
| Expanded contract projection | SOURCE exactly the five-item conjunction (or its existential package); do not omit any AND tail or invent unitarity. For any future unconditional expanded route, opaque cleanup/extraction/target must instead be genuinely discharged dependencies. |

No RULED correction was supplied or needed for these source claims. An exact formal binder audit is PENDING. Future formal premises that assume produced range/normalization/orthogonality/target-action facts for an advertised unconditional anchor would be EXCESS; the same facts may legitimately occur as SOURCE premises of the explicitly conditional auxiliary interfaces. Source and conditional interface levels must not be conflated.

## Source Construction Graph: independent nodes, exhaustive region disposition

Line anchors below refer only to the pinned 507-line source. Formatting-only blank lines and section headings inherit the following region's disposition; all substantive text/formulas/citations are covered. NODE records can be limitations/metadata, not necessarily theorem successes. EXCLUDED is exclusion from mathematical success, not concealment from the inventory.

| Region | Disposition / source node |
| --- | --- |
| 1–8 | EXCLUDED(PROVENANCE): title, retrospective status, UNKNOWN historical formalizer, distinction of evidence layers; retained as review scope. |
| 10–25 | NODE C01: carriers, natural endpoint, rational matrix multiplication and grid definitions. |
| 26–36 | NODE C02: O entries/action; normalized-state boundary and zero endpoint. |
| 38–46 | NODE C03: D and X definitions and distinction from O. |
| 47–50 | NODE C04: selected scales/tolerance and intent-only warning. |
| 52–62 | NODE C05: range/power/norm/scale inequalities. |
| 63–68 | NODE C06: three exact norm diagnostics, restricted evidence class. |
| 70–79 | NODE C07: initial-segment counting, cubic capacity, strict-storage distinction. |
| 80–85 | NODE C08: exponent arithmetic and accepted-path ratio; phase/transcript nonimplication. |
| 87–99 | NODE C09: two-part rank-one contract implies alpha B=O. |
| 101–109 | NODE C10: seven arithmetic labels/layout/accounting; denotation/inverse gap. |
| 111–116 | NODE C11: wrapper ordering, kept row output, auxiliary and tuple counts. |
| 118–129 | NODE C12: eight-label counting ordering, separate reject flag, kept row XOR and counts. |
| 131–137 | NODE C13: required rank-one semantic AND tail and separate normalized-SP tail. |
| 139–150 | NODE C14: dot/e/w/d/H formulas and unit/nontrivial guards. |
| 151–154 | NODE C15: d identity/nonzero and clean entry calculation. |
| 155–162 | NODE C16: expanded column inner products, row symmetry, rational orthogonality. |
| 163–171 | NODE C17: finite-fold support identities; totalized off-locus boundary. |
| 173–181 | NODE C18: flatten/decode inverse, clean embedding and layout distinction. |
| 183–192 | NODE C19: controlled-direct-sum formula and support fibers. |
| 193–200 | NODE C20: zero-support filtering, permutation/injectivity/reindex and both orthogonality directions. |
| 202–208 | NODE C21: clean diag(q), X/D instances and supplied-value guard. |
| 210–213 | NODE C22: EXTERNAL_CITED_RESULT Lagrange four-square theorem, all natural residuals. No implementation/cost presumed. |
| 214–223 | NODE C23: linear residual equation/vector, norm and zeroth-coordinate proof. |
| 224–231 | NODE C24: cubic residual equation/vector, norm and legitimate natural subtraction. |
| 233–239 | NODE C25: finite-family choice, orthogonal matrix existence, representative dependence and cost/uniqueness boundaries. |
| 241–246 | NODE C26: input-package fields and forgetful exact-payload projection; embedding/orthogonality limitations. |
| 248–258 | NODE C27: chosen embedding, weak cleanup field, unlinked label resource, generic cubic target freedom and specific target equality. |
| 260–267 | NODE C28: diagonal multiplication and X^3=D. |
| 268–275 | NODE C29: product clean-matrix certificate and physical-product nonimplication. |
| 277–281 | NODE C30: P=x^3, grid bound, degree/parity record limitations. |
| 283–292 | NODE C31: full conditional QSVT supplier/consumer tail and target substitution. |
| 294–308 | NODE C32: diag(q), literal rational abs and E, dimension-zero/scalar boundary. |
| 310–321 | NODE C33: diagonal action, pointwise-square and finite-sum proof, abstract bridge and non-vacuity. |
| 323–333 | NODE C34: approximation transport with no N loss; separate guarded unit-circle realization and producer gap. |
| 335–346 | NODE C35: primitive opaque-unitarity AND extracted-target contract and candidate projection; no unconditional witness. |
| 348–355 | NODE C36: one-signal label/layout/resources, separate fields and absent denotation/rational-rotation guarantee. |
| 357–371 | NODE C37: supplied scalar law, descriptions versus actual functions, range specialization and unused workspace. |
| 373–383 | NODE C38: arbitrary W backend/clean contract and symbolic overwrite, cardinality/dirty/inverse limits. |
| 385–390 | NODE C39: finite fixed-denominator overwrite backend, payload capacity and exact readout. |
| 392–400 | NODE C40: known-premise implication equivalences for opaque computation/angle and unresolved meaning. |
| 402–413 | NODE C41: modular compute/uncompute formulas, two-case cancellation and natural-subtraction guards. |
| 415–422 | NODE C42: cubic/linear instantiations, dirty preservation, zero agreement/cleanup and n=0; no gate/cost claim. |
| 424–431 | NODE C43: generic cleanup fields, one-sided inverse distinction. |
| 433–439 | NODE C44: readonly rotation fields, unchanged j,w and missing signal/linear/unitary semantics. |
| 441–450 | NODE C45: expanded five-conjunct diagonal contract, no alternatives among them. |
| 452–458 | NODE C46: first-two supply, transparent/opaque distinction, readonly not a conjunct, circular extraction and no unitarity. |
| 460–472 | NODE C47: guarded construction route summary with full AND/OR distinctions. |
| 474–481 | NODE C48: enumerated stronger-consumer gaps and evidence-tier exclusions. |
| 483–491 | NODE C49: resource syntax/score/depth/layout accounting and absence of asymptotic semantics. |
| 493–502 | EXCLUDED(PROCESS_METADATA) C50: iteration, agent, schedule, budget, stall, error-ladder and planning labels; literal values retained but historical controller execution not verified. |
| 504–507 | EXCLUDED(PROCESS_NOT_CLOSURE) C51: metadata exclusion and prohibition on substituting it for guarded evidence. |

SOURCE_GAP nodes (explicitly OPEN, not a false theorem asserted by source):

- G01: interpreted coherent arithmetic-middle and wrapper transcript, including true inverses, row generation and every column action.
- G02: interpreted counting transcript, coherent cube/comparator actions, and correct register behavior.
- G03: complete rejection of all nonzero input columns plus clean workspace/flag behavior.
- G04: Hadamard amplitudes, phases and accepted-path normalization through the counting transcript.
- G05: normalized-SP first-column action, nonzero accepted branch, success probability, normalization/amplification and associated cost.
- G06: efficient deterministic four-square data producer, storage/input evaluation contract and classical preprocessing cost.
- G07: uniform controlled-matrix/gate realization, label-to-matrix denotation, precision, gate set and resources for chosen matrices.
- G08: physical product-block isolation/composition, fresh ancilla/projector semantics, composed unitary and cost.
- G09: actual QSVT global-admissibility/phase synthesis, circuit semantics, cleanup and resource supplier.
- G10: approximation producer with error proof; optional scalar extension from Q and a certified dilation.
- G11: actual rotation/linear-amplitude semantics and coherent common-backend/register composition with arithmetic.
- G12: transparent-cleanup-to-opaque-cleanup bridge and route-level computation/angle bridges with genuine semantics.
- G13: physical extraction and unitarity for the expanded route, not merely its literal block-target equality.
- G14: finite-bit gate/resource refinement and executable family acceptance, including saved-circuit/target correspondence.

### Graph edges: complete AND tails, typed heads, guarded OR routes

Notation `AND{...} -> H` means every listed tail is needed. OR alternatives are stated only for a matched head; no individual AND input is claimed sufficient.

1. `AND{C01,C03} -> C05`; `AND{C01,C05} -> C06,C07,C08`. The diagnostic identities are separate exact computations, not consequences of a loose inequality alone.
2. `AND{C01,C02,C09.contract} -> C09.conclusion(alpha B=O)`. The contract is an explicit conditional premise, not an output of merely naming a transcript.
3. `AND{C14.unit,C14.guard,C14.formula,C17.finite-sum identities} -> C15,C16`. No off-locus edge exists.
4. `AND{C18.bijection,C19.formula,C19.all-unit,C19.all-guards,C16,C20.fiber proof} -> U orthogonal`.
5. `AND{C18,C19,C15,all branch coordinate equations} -> C21.clean diag(q)`; the guard and unit inputs needed by C15 remain in the transitive tail.
6. `AND{C01,C05.residual bounds,C22,C23} -> linear branch existence`; `AND{C01,C05.residual bounds,C22,C24} -> cubic branch existence`.
7. `AND{linear branch existence,C05.guard,C18,C19,C20,C21} -> C25.X orthogonal matrix existence`; parallel cubic branch tail gives `C25.D orthogonal matrix existence`. This head has fixed dimension 8N, explicit clean embedding, scale 1, not a circuit/cost head.
8. `AND{C26.strong package} -> C26.weak exact payload`; forgetting is not an edge in the opposite direction. `AND{C25,explicit chosen embedding,stored target definition} -> C27.chosen instance properties` with the literal weak cleanup/resource fields; G07 remains OPEN.
9. `AND{C01,C03,C28.diagonal finite-sum calculation} -> X^3=D`; `AND{C26.extracted clean matrix=X,C28,finite product congruence} -> C29.clean-matrix cube=D`. G08 is necessary before any physical-product head.
10. `AND{C05,C30.P formula} -> local grid bound`; degree/parity labels are independent record fields. `AND{certified linear input,output exact payload,output orthogonality,output target=X^3,global-admissibility proof,cleanup proof,resource proof,C28} -> C31.supplied output target=D`. This retains the complete supplier AND tail, including the output object, not merely P's grid bound. G09 prevents any unconditional synthesis inference.
11. `AND{C32.literal E,C33.diagonal action,epsilon>=0,all diagonal abs bounds} -> C33.E theorem`; `AND{C34.supplied q,epsilon>=0,all |q-a|<=epsilon,C32,C33} -> C34.entry and E errors`. Optional realization uses `AND{all rational unit-circle witnesses,all q!=1,C18,C14-C21} -> orthogonal matrix with clean diag(q)`; only AND with the error tail yields both realization and error. G10 is not supplied by either tail.
12. `AND{C35.opaque unitarity,exists B (opaque Extract(U,B) AND B=D)} -> C35.candidate projections`. C36 counts do not discharge either premise.
13. `AND{C37.supplied tier law,C05.range} -> C37.grid law`; `AND{C38.symbolic definition} -> symbolic clean computation`; `AND{C01,C07.strict capacity,C39.finite definition,C08.rational arithmetic} -> finite clean computation`.
14. `AND{known clean computation,C40.bridge} -> opaque computation`, and conversely opaque computation supplies a constant bridge. Same known-premise equivalence for C37 and opaque angle. Neither direction manufactures the opaque proposition from nothing.
15. `AND{C41.definitions,p<M,w<M} -> C41.left cancellation`; `AND{C01,C07.capacity,C39,C41} -> C42.cubic cleanup`; with p=j,M=N and its linear readout backend the analogous tail gives linear cleanup. `C43.generic fields` only imply their stated one-sided law. `C44.readonly` does not imply G11.
16. `AND{exists cubic backend clean at declared workspace,universal supplied-tier angle law,opaque route-cleanup,opaque Extract(B),B=D} -> C45.expanded contract`. C38/C39 and C37 at 3n supply only the first two. C42 is not automatically the third. Neither readonly nor unitarity is one of these five items; G11–G14 are required for a future stronger circuit acceptance head.
17. `AND{C49.resource grammar,explicit label list,declared layout} -> literal tuples in C10-C12,C27,C36`. This edge ends at metadata; no edge to physical synthesis follows. C50/C51 are not mathematical dependencies.

Guarded OR structure:

- Prospective rank-one physical block: arithmetic-wrapper route OR counting route, each with its own full AND of interpreted denotation, unitarity, rejection, workspace cleanup and clean-block proof. Counting additionally retains G04 and C07/C08; arithmetic retains actual rotation/compute/inverse semantics G01/G11. Both are OPEN. They are not an AND requiring both circuits and neither route is currently delivered.
- Exact cubic *target-matrix equality* can come from direct cubic four-square construction OR algebraic cube of the linear clean matrix OR a fully supplied QSVT output plus X^3=D. Their conclusion types differ in strength: the direct route additionally supplies an 8N orthogonal matrix; the clean-product route supplies only an algebraic certificate; the QSVT route is conditional and does not fix the same dimension/embedding. These are not unguarded OR-proofs of one common physical/unitary/resource theorem.
- Prospective diagonal physical realization may use the Householder matrix plus G06/G07 OR a gate-expanded arithmetic route plus G11–G14 OR the fully semantic QSVT supplier. The primitive supplied contract is only a conditional route, and S12 alone is not sufficient because it lacks unitarity. No alternative is asserted as a verified gate-level winner.
- Scalar approximation error has one sufficient diagonal argument. A unit-circle matrix realization is an independent optional AND prerequisite when realization is also desired, not a replacement for the error proof or an alternative error bound.

No source graph edge here is claimed to be a Lean dependency. No graph topology or number of nodes constitutes novelty, compilation, or publication evidence.

## Seven quantum semantic slots

| Slot | Phase-1 source-derived contract and remaining boundary |
| --- | --- |
| target | Separate O=|v><0| and D=diag((j/N)^3), with X=diag(j/N). O maps e_0 to unnormalized v; diagonal products/QSVT target D, not O. Generic exact cubic payload is not inherently fixed to D. |
| normalization | O's chosen scale N satisfies sum a_j^2<=N^2. D/X scales 1; Householder clean block exact. alpha B=O uses multiplication, so no alpha!=0 binder. Normalized v undefined at n=0 and not implemented for n>0 by these assertions alone. |
| registers | J=Fin(2^n). Householder total dimension 8N, ancilla-first flatten bN+s, clean b=0. Arithmetic/primitive/expanded layouts use one signal and their own workspace declarations; do not identify these layouts. Fixed cubic payload is Fin(2^(3n)); symbolic Q workspace is not a finite register. Hardware endianness unspecified beyond flattening. |
| oracles | Seven/ten/eight/one labels are uninterpreted transcript metadata. Coherent controls, inverse denotations and arithmetic/comparison gates not supplied. Primitive extraction/unitarity and expanded opaque propositions remain precisely supplied assumptions. No zero-cost random access, witness search, or backend synthesis inferred. |
| ancillas_phases | Householder supplies exact rational row/column orthogonality and clean projection, not return of all ancilla amplitude to clean zero. “Cleanup” package fields may mean only block equality. Concrete modular maps restore dirty workspaces; generic witness only has one inverse direction. Readonly preserves j,w but lacks signal amplitudes. Rank-one reject flag and Hadamard relative phases are OPEN; no quotient/global-phase exemption or coherent-label phase loss is allowed. |
| error_success | Exact rational equalities for algebraic routes; supplied q error is E over Q vectors and nonnegative epsilon, including m=0. No numerical q producer, real/complex extension, gate approximation or precision proof. Exploratory 10^-10 distinct from relaxed 10^-8/10^-6. No certified success probability, postselection cost, amplification or normalized state-action theorem. |
| resources | Literal count/depth/layout tuples only; one label not one elementary gate. Orthogonal matrix existence and finite carrier size do not prove efficient preprocessing/gate synthesis. Gate set, exact-real versus finite-bit compiler costs, phase synthesis, readout, connectivity/depth and executable uniform-family acceptance remain OPEN. |

## Counterexample/necessity register and reviewer outcome

Explicit independent witnesses above separate potential false stronger claims from actual source claims: n=1 distinguishes O/D; n=0 kills normalized v; v=0 invalidates off-unit H_00=v_0; two four-square choices give different matrices with the same clean block; the 3/5–4/5 reflection disproves clean(U^3)=clean(U)^3; identity-versus-zero disproves error-zero vacuity; q=1/8 excludes a universal rational two-coordinate rotation; overwrite on two workspace inputs is noninjective; a singleton scalar tier shows the law need not be a faithful amplitude embedding; shift/predecessor shows generic left cleanup need not be two-sided; constant signal output shows readonly need not be unitary. None contradicts the source as written, which expressly avoids those strengthened conclusions.

Failure class: NONE for the reviewed algebraic and explicitly conditional source claims. Stronger-consumer G01–G14 remain unresolved source boundaries, not REFUTED mathematics, not ENV_BLOCKED/API_BLOCKED, and not an implementation failure claim. Salvage: the independently checked algebraic identities/obstruction examples are retained here as natural-mathematics evidence only; no fragment is labelled compiled or promoted to a canonical Lean node. Curated process-memory entries consulted: none (scope intentionally forbids additional records). Direction fingerprint: independent raw-source-first rational algebra/conditional-contract audit, no implementation exposure. Expected information gain: detect false mathematics, lost guards/AND tails and semantic overclaims before formal comparison. Parallel/common-blind-spot/comparator: no subagents or multi-route winner selection performed; no separate topology review was fabricated. Purification/Exposition Seal: NOT ASSESSED; this source-only review is not a production publication or purification gate.

Phase 1 stops after hashing this notes file and the source into a separate seal. This file's bytes must not be amended after sealing. The exact formal signature, expanded binder audit, actual Lean graph, formalizer/decoder/reviewer identity checks, Lean/build status and equivalence verdict remain PENDING separate formal authorization.

