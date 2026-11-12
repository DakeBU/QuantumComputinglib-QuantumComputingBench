# Independent formal-to-mathematics reconstruction: physical TT boundary

Run: `tt-physical-decoder-c26`. Direction: `c26_FORMAL_TT_PHYSICAL_WORD_BOUNDARY`.

This is a reconstruction from the complete actual formal modules `QuantumBlockEncoding/TensorTrainLocalCompiler.lean`, `QuantumBlockEncoding/TensorTrainWord.lean`, and `QuantumBlockEncoding/TensorTrainPrimitivePreparation.lean`, with the bounded provider readings fixed in `formal-input-seal.json`. No natural-language source package, author graph, author desired result, or other review was used. Earlier formal-only provider exposure is disclosed in that seal. At report authorship no author decoder packet or opaque binding had been supplied. This report does not decide source agreement, novelty, publication admission, or whole-repository gate status.

## Common carriers, literal definitions, and logical inputs

All dimension/length/wire parameters below are natural numbers, including zero unless a strict inequality or successor is explicitly written. `Fin d` is the set of integers from 0 through d-1; it is empty when d=0. Matrices have output rows and input columns for circuit action. Real tensor cores use the opposite orientation described next. All matrix products and vector actions are exact finite sums. Real entries embed in complex amplitudes by the injective real-to-complex map, not by discarding signs or taking magnitudes.

Write `Bits m = Fin m -> Fin 2`, `LE_m : Bits m ≃ Fin(2^m)`, and `z_m` for the all-zero bit assignment. The actual alias `gridSize m` is `2^m`. `LE_m(x)` has value `sum_i 2^i x(i)`: wire 0 is least significant. `Fin.snoc b s` appends bit s as the highest wire; `Fin.append x b` places data x on the first low wires and bond b after it. `rev(i)=m-1-i` is the involution on `Fin m`.

A real core `A : Core l r` is an l-by-(2r) matrix whose column is a pair `(s,b)` with s in `Fin 2` and b in `Fin r`. Its slice is `A_s(a,b)=A(a,(s,b))`. A dependent chain has constructors `nil r : Chain 0 r r` and `cons A T : Chain (m+1) l r` for `A : Core l k`, `T : Chain m k r`. Thus every boundary and intermediate bond is part of the type, not an unproved ambient rank promise. A head-first word is `Word 0=Unit`, `Word(m+1)=Fin 2 × Word m`, with its recursive finite instance. Let `M_C(w)` be contraction: `M_nil=I_r`, `M_cons(s,w)=A_s M_T(w)`. The first core consumes the first word symbol. `RightCanonical C` means `A A^T=I_l` at every cons node, with True at nil. `maxBond C` is the maximum of all actual bond dimensions, including both boundaries.

The provider's `RankReduced C D` preserves terminal dimension and recursively replaces each left dimension l by `min(l,2*k')`, where k' is the already reduced next dimension. It is a dimension relation with its recursive tail premise; it is not a numerical matrix-rank equality. Its producer proves full all-word matrix action through a residual, and never increases maxBond. `mass u=sum_a u(a)^2`. In particular, the producer `exists_normalized_state` returns a canonical D, a signed real u with mass 1, the dimension relation, and the equality `M_C(w)(0,0)=sum_a u(a) M_D(w)(a,0)` for every complete word, from only the input train and its squared-amplitude normalization.

For a chain C with bonds d_0,...,d_m, `rankAt C t=d_t` for t<=m and equals d_m thereafter. For a physical padded bond S, `paddedAt C t((s,b),a)` is the complex cast of the t-th real core entry if t<m, a<d_t and b<d_(t+1), and zero otherwise; after the chain it is zero. `padVector v b` returns v(b) if b is within its active dimension and zero otherwise. Without a dimension inequality it can truncate, but the maxBond<=S hypotheses in the relevant roots bound every input and output active bond and prevent this truncation.

A sequential `Stage B` is a square complex matrix on `Fin 2 × B`. A state at length m is a function on `Bits m × B`. `run(U,v,0)(x,b)=v(b)` and

`run(U,v,m+1)(x,b) = sum_a U_m((x(last m),b),(0,a)) run(U,v,m)(init x,a)`.

Every step adds the new bit in zero; prior emitted bits are passive. The chronological transfer multiplies the last local slice on the left. `circuitStage c((s,b),(s',a)) = E(c)(snoc b s,snoc a s')`.

`PrimitiveCircuit m` is an actual finite list of typed `PrimitiveGate m` instructions X, RY, RZ or CX, with distinct CX endpoints. The angle language includes arbitrary exact real values, rational values, rational multiples of pi, special arccos expressions, sums, negatives and rational scaling. RY(theta) has the standard half-angle block `[[cos(theta/2),-sin(theta/2)],[sin(theta/2),cos(theta/2)]]`. Circuit evaluation E is a complex matrix, `E([])=I`, `E(g::rest)=E(rest)E(g)`: later instructions act on the left. Its unitary-group membership expands to both `E†E=I` and `EE†=I`. `gateCount` is literal list length, including identity-angle instructions if present. The circuit resource record assigns oracleCalls=0 and pureAncilla=0 to every primitive list by definition; this bookkeeping is not an input-evaluation/runtime theorem, nor an assertion that the explicit bond register is absent.

There are no target-wide section variables, named instances or private declarations. The modules have respectively 10, 12 and 15 public source roots. Their exact complete lexical headers, imports, attributes and scopes are in the initial seal; fresh elaborated types are separate probe evidence. The only local target option is `backward.isDefEq.respectTransparency false` on `run_circuits_clean`, an elaboration transparency setting and not a mathematical premise. Statements below distinguish typing data from logical hypotheses. No SOURCE/STANDING/EXCESS comparison is asserted without the withheld natural-language source.

## TensorTrainLocalCompiler: all ten roots

1. `exists_SO_named`. For any type I with finite enumeration and decidable equality, natural r, strict `r < card I`, real matrix V on `I × Fin r`, injection `e : Fin r ↪ I`, and `V^T V=I_r`, there exists a real square matrix U on I with `U^T U=I_I`, `det U=1`, and `U(i,e(a))=V(i,a)` for every i,a. The finite/decidable instances supply index and finite-sum typing; strict dimension and orthonormality are genuine logical hypotheses. I need not be a canonical numeric basis, and e need not be a prefix injection.

   The proof reindexes to `Fin(card I)`, extends the orthonormal columns to an orthogonal basis, and corrects orientation at a genuinely unused column when determinant is -1. The prescribed columns are unchanged. Strict spare dimension matters: if all columns were prescribed, their orientation could already be -1. The witness is classical and non-unique. r=0 is allowed if I is nonempty; empty I cannot satisfy the strict inequality.

2. `localIndex(q)` is the equivalence `Bits(q+1) ≃ Fin 2 × Fin(2^q)` sending x to `(x(q),LE_q(init x))`. The fresh local bit is the highest wire; the q bond wires are low.

3. `localIndex_snoc`. For every q, b in Bits q, and s in Fin 2, `localIndex(q)(snoc b s)=(s,LE_q(b))`.

4. `paddedAt_real`. For every chain C of any dimensions/length, any natural t, padded bond dimension B, output `(s,b)` and input a in Fin B, the complex cast of the real part of `paddedAt C t((s,b),a)` equals that original complex entry. No canonicality, maxBond bound, or `t<length` is assumed; out-of-schedule entries are zero.

5. `paddedAt_im_zero`. Under the same unrestricted data, the imaginary part of that entry is zero. This is real-amplitude structure, not an assumption about the eventual completion's unused columns.

6. `activePositions`. Given q,l and `hl:l<=2^q`, this is the injection from Fin l to Bits(q+1) sending a to `localIndex(q)^-1(0,castLE(hl,a))`. These are the clean-fresh-bit physical column labels, not an arbitrary initial state or a contiguous prefix in every external coordinate system.

7. `activeColumns`. Given C:Chain m l r, natural t,q and `hB:maxBond C<=2^q`, this is the real matrix with rows in Bits(q+1) and columns in Fin(rankAt C t), entry

   `V_t(row,a)=Re(paddedAt C t(localIndex(q)(row),castLE(rankAt<=maxBond<=2^q,a)))`.

   The bound is required to type the finite-index embedding. The definition exists for all t and does not require canonicality; after the end the entries are zero even though rankAt remains terminal rank.

8. `activeColumns_isometry`. Add `RightCanonical C` and `t<m`. Then `V_t^T V_t=I_(rankAt C t)`. The proof takes real parts of the provider's full padded active-column isometry and sums through localIndex. The canonicality and actual-stage premise are necessary logical inputs; this theorem does not assert an isometry of the zero schedule after its end.

9. `exists_local_circuit_with_resources`. Under exactly C, canonicality, hB and `t<m` above, there exists `c:PrimitiveCircuit(q+1)` with `length c<=6*(2^q)^3`, `c.resource.oracleCalls=0`, and, for every s in Fin 2 and b,a in Bits q whose numeric input bond `LE_q(a)<rankAt C t`,

   `E(c)(snoc b s,snoc a 0)=paddedAt C t((s,LE_q(b)),LE_q(a))`.

   The equality covers every output b,s, including inactive output sectors, but only active input bonds with fresh bit zero. It does not prescribe inactive-input or fresh-bit-one columns. The completion supplies these other columns, and the primitive evaluator makes the entire matrix unitary.

   With S=2^q>=1, the active rank is <=S, while the full local basis has size 2S. Thus active rank <2S, giving an unused orientation column even at q=0. The proof chooses an SO completion, compiles its exact named-wire matrix by the Gray/Givens backend, and transfers the prescribed real columns back to complex amplitudes. It assumes neither an SO matrix nor a desired circuit action from the caller.

   The inherited compiler proves a chronological list of `N*(N-1)/2` adjacent real RY planes for an SO(N) matrix, N=2S, including harmless zero-pivot rotations. Binary-reflected Gray labels turn adjacent indices into a one-wire flip. A reversed target-bit orientation negates the plane angle. Each selected plane controls every other local wire and compiles by the proved recursive multiplexor into S RY and `2*(S-1)` CX, so actual primitive list length is `N*(N-1)/2 * (S+2*(S-1)) <=6S^3`. Gray order is internal; final matrix equality is in the original named-wire basis, not a silently permuted external state. This is the checked recursive selected-RY backend, not an assertion about a numerical Walsh/Gray exporter.

10. `exists_local_circuit` has the identical chain/canonicality/bond/stage premises, witness type, literal length bound, and all active-clean-column equations, but omits the oracleCalls conjunct. It is the weaker projection of root 9, not an additional synthesis assumption.

## TensorTrainWord: all twelve roots

Let a word w of length m have head-first digits s_0,...,s_(m-1). Its Boolean list tests each Fin 2 digit for equality to 1.

1. `toBasis` recursively converts the empty Unit word to the unique empty function and `(s,w)` to `Fin.cons s (toBasis w)`. It sends the head to wire 0, so direct LE indexing of this basis would make the head least significant.

2. `toBasis_wordOfBasis`: for every x:Bits m, `toBasis(wordOfBasis x)=x`.

3. `wordOfBasis_toBasis`: for every w:Word m, `wordOfBasis(toBasis w)=w`.

4. `basisEquiv(m)` is the full finite-carrier equivalence Word m ≃ Bits m with those forward and inverse maps, not only an injection on nonzero amplitudes.

5. `reverseBasis(m)` is the involutive equivalence x -> `(i -> x(rev i))`, with the same inverse.

6. `sampleEquiv(m)` is the composite `basisEquiv(m)`, then reverseBasis(m), then LE_m. Consequently the head-first word is interpreted most-significant-first at the public numeric sample index. The reversal is part of the stated definition, not an uncharged state-moving operation.

7. `toBits` maps empty word to [] and `(s,w)` to `decide(s=1)::toBits(w)`.

8. `toBits_length`: its Boolean list has length exactly m for every w:Word m.

9. `primitive_snoc_value`: for every m,x:Bits m and s:Fin 2, `LE_(m+1)(snoc x s).val=LE_m(x).val+2^m*s.val`. The newly appended high wire has its actual little-endian weight.

10. `sampleEquiv_value`: for every w:Word m, `sampleEquiv(m)(w).val=HermiteBoundaryInjection.wordValue(toBits w)`. Here wordValue([])=0 and wordValue(bit::tail) is `(if bit then 2^(length tail) else 0)+wordValue(tail)`, i.e. `sum_i 2^(m-1-i)*s_i`. Its total domain is every Boolean list, with value <2^(list length).

11. `wordSampleIndex_eq`: for any natural n and w:Word(n+1), the provider's finite index `wordSampleIndex n (toBits w) (toBits_length w)` equals `sampleEquiv(n+1)(w)`. `wordSampleIndex` is literally wordValue with its proof that the value lies in Fin(gridSize(n+1)); the width equality is supplied by the length theorem. This root concerns positive widths n+1 only.

12. `sampleEquiv_public`: for every x:Bits m, `sampleEquiv(m)(wordOfBasis(i -> x(rev i)))=LE_m(x)`. The two reversals cancel. This is the exact adapter between public low-data little-endian wires and the reversed head-first word occurring in the physical preparation theorem.

All these roots are unconditional finite-index statements; no amplitudes, polynomial, normalization, cutoff, positivity of a real parameter, circuit or oracle is assumed. Empty words/bases at m=0 map to the unique numeric index in Fin 1. The module imports HermiteBoundaryInjection for its two indexing definitions, but does not assert Hermite sample amplitudes or state preparation by itself.

## TensorTrainPrimitivePreparation: all fifteen roots

1. `boundaryRow(u)` is the real 1-by-l matrix `R(0,a)=u(a)` for any u:Fin l -> R. There is no default normalization or discarded sign.

2. `boundaryRow_isometry`: given mass(u)=1, `R R^T=I_1`. For l=0 the hypothesis is impossible (mass is zero); it is not silently supplied by a typeclass.

3. `boundaryCore_isometry`: for u as above, A:Core l r and `A A^T=I_l`, `(R A)(R A)^T=I_1`. Thus multiplying the signed residual into the first row-isometric core preserves the required row-isometry.

4. `boundaryCore_contract`: for arbitrary u, A:Core l k, T:Chain m k r and w:Word(m+1), `M_cons(RA,T)(w)=R M_cons(A,T)(w)`. Neither u normalization nor canonicality is needed for this associativity identity. It is equality of the entire 1-by-r matrix, not only a scalar terminal entry.

5. `exists_unitBoundary_canonical`: for C:Chain(n+1) 1 1, natural B, `maxBond C<=B` and `sum_w M_C(w)(0,0)^2=1`, there exists D:Chain(n+1) 1 1 such that `RightCanonical D`, `maxBond D<=B` and `M_D(w)(0,0)=M_C(w)(0,0)` for every w. No canonicality of C, nonnegative amplitudes, full-rank hypothesis, residual vector, or free state-preparation oracle is assumed.

   The proof first gets the producer's signed normalized u and canonical chain with possibly changed left boundary, then absorbs u into its first core by roots 1-4. It uses nonemptiness to have that first core. The original left dimension 1 also proves 1<=B; interior maxima do not increase. This root returns no RankReduced relation for the final boundary-absorbed D, and does not assert an efficient algorithm to compute it.

6. `transportStage(e,U)`, for any equivalence e:B≃C and Stage C matrix U, is the Stage B matrix `transportStage(e,U)((s,b),(s',a))=U((s,e(b)),(s',e(a)))`. Only bond labels are reindexed, not emitted bits.

7. `run_transport`: let B,C be finite types with decidable equality, e:B≃C, arbitrary sequence U of Stage C matrices, arbitrary complex boundary v:B->ℂ, natural m, x:Bits m and b:C. Then

   `run(U,c -> v(e^-1(c)),m)(x,b) = run(t -> transportStage(e,U_t),v,m)(x,e^-1(b))`.

   There is no unitarity, normalization or active-column hypothesis here. The exact finite sum is reindexed through e; it is not an implementation of a free physical permutation.

8. `bondIndex_zero(q)`: `LE_q(z_q).val=0`.

9. `bondIndex_zero_iff`: for all b:Bits q, `LE_q(b).val=0` iff b=z_q. This remains valid at q=0, where the basis has one element.

10. `initial_padding`: for all q and b:Bits q, padding the one-entry vector (1:C) to the numeric bond label LE_q(b) equals `E([]:PrimitiveCircuit q)(b,z_q)`. Thus the initial padded unit boundary is genuinely the zero-gate identity-circuit column of a computational-zero bond. It is not a general signed boundary vector prepared for free.

11. `run_circuits_clean`: let D:Chain m 1 1, q natural, `maxBond D<=2^q`, and stages t:PrimitiveCircuit(q+1) for every natural t. Suppose for every t<m, bit s and b,a:Bits q with LE_q(a)<rankAt D t, the actual evaluator columns satisfy

   `E(stages_t)(snoc b s,snoc a 0)=paddedAt D t((s,LE_q(b)),LE_q(a))`.

   Then for every x:Bits m,b:Bits q,

   `run(t -> circuitStage(stages_t),c -> E([])(c,z_q),m)(x,b)`

   equals `(M_D(wordOfBasis x)(0,0):C)` if b=z_q and 0 otherwise. Canonicality and normalized mass are NOT premises of this bridge: exact columns and the bond bound suffice. It uses finite bond transport, padded run semantics and terminal dimension 1 to cover every padded bond output, not only a postselected component. No columns are requested after m.

12. `publicCircuit_clean`: with exactly the same D,q,bond bound, stage family and active-column hypothesis, for every x:Bits m and b:Bits q,

   `E(publicCircuit([],stages,m))(append x b,z_(m+q))`

   equals `(M_D(wordOfBasis(i -> x(rev i)))(0,0):C)` if b=z_q, otherwise zero. The output carrier is the entire Bits(m+q), equivalently all pairs (x,b), since append is a bijection. Input is the one all-zero computational basis vector. This is a complete column of one actual primitive list, not merely recursive matrix semantics or a projected block.

   Assembly starts with low bond wires 0,...,q-1 and emits bit t on wire q+t, preserving previous outputs. It lifts previous instructions and places the new stage on its actual final wires. Public output renaming sends old bond wire i to m+i and old data wire q+t to m-1-t, yielding low little-endian data and high bond. Each gate's endpoints are renamed in the list. This is not an extra physical SWAP network applied for free to an already-prepared state; unrestricted endpoint placement is the operation model. No hardware connectivity cost is claimed.

13. `assemble_gateCount`: for all q, stage lists and natural m, the literal list length of `SequentialPrimitiveAssembly.assemble q stages m` is `sum_(t in range m) length(stages_t)`. The assembly recursion is [] at m=0 and `(assemble m).map(liftGate) ++ placeStage(m,stages_m)` at the successor. Padding, liftGate and endpoint renaming preserve list length.

14. `publicCircuit_gateCount_bound`: given q, any stage family, natural m,L and `length(stages_t)<=L` for every t<m, the actual publicCircuit with [] initialization has length <=m*L. Neither canonicality nor correct action is needed for this counting lemma. Initial empty circuit has exactly zero cost, and public renaming costs no new instructions in this syntax. m=0 gives zero length irrespective of the unused stages.

15. `exists_primitive_preparation`: for C:Chain(n+1) 1 1 and q natural, the only logical premises are `maxBond C<=2^q` and `sum_(w:Word(n+1)) M_C(w)(0,0)^2=1`. There exists one list `circuit:PrimitiveCircuit((n+1)+q)` with all of:

   - literal length <=`(n+1)*(6*(2^q)^3)`;
   - resource.oracleCalls=0;
   - E(circuit) is a unitary matrix on the complete Bits((n+1)+q) complex carrier;
   - for every x:Bits(n+1) and b:Bits q, its entry from z_((n+1)+q) to append(x,b) is the exact complex cast of `M_C(wordOfBasis(i -> x(rev i)))(0,0)` when b=z_q and exactly zero otherwise.

   The proof constructs the bounded canonical unit-boundary D from root 5, obtains actual local primitive stages from TensorTrainLocalCompiler on each used t, chooses [] for unused t, and applies roots 12 and 14. The caller supplies no completed matrices, stage circuits, normalization proof ingredients beyond the stated source normalization, global-action theorem, or already-prepared residual. Exact input signs and relative phases survive boundary absorption; there is no global-phase quotient or arbitrary ± ambiguity. Global unitarity comes from the primitive circuit evaluator, and whole-bond cleanup comes from the terminal dimension-one semantics. Thus this downstream root really does close an actual flattened primitive-list preparation interface, even where upstream provider comments separately list synthesis/placement as obligations.

## Degenerate and off-schedule scope

Definitions and intermediate clean-run/public-circuit/counting roots accept m=0. A typed Chain 0 1 1 has only the nil 1 constructor, contraction I_1 and scalar amplitude +1; its zero-stage assembly and empty initialization are identity. The final existence root and boundary-absorption root deliberately quantify successor length n+1, not arbitrary m. Their n=0 case therefore means ONE emitted data qubit, not an empty train. This report does not silently widen those signatures to length zero, nor claim that empty length is mathematically impossible. No separate fresh theorem adding that case was authored.

q=0 is allowed: S=1, a local circuit still has one fresh/output wire, and the final bond register is Bits 0 with one basis label. The local completion still has dimension 2 and at least one spare column. Generic dependent-chain definitions permit zero bonds; stage isometry may then have zero active columns. But a scalar-boundary normalized chain cannot have an interior zero bond (all full-word amplitudes would vanish), so final normalization eliminates that obstruction rather than a hidden positivity/full-rank binder. Active columns outside used t are not assumed orthonormal or implemented. Inactive input columns of U may be nonzero and need not equal zero-padded K: they never acquire support in the proved clean-input run.

## Seven quantum-semantic slots and remaining boundaries

1. Target/normalization: the final target is the EXACT real scalar-boundary train amplitude for every full word, embedded in complex amplitudes. Squared mass is exactly one; no supplied target vector or source oracle is identified by a further unproved equality here. The word module's grid adapter identifies sample labels, not a particular Hermite amplitude family.

2. Dimensions/order/basis: all dependent bonds and full output carrier are explicit; local q-low bond plus highest fresh bit, internal chronological emitted order, head-first words, final reversed public LE data order and high clean bond are distinct and connected by actual equivalences/list placement.

3. Oracle/access: local and final outputs are lists in an oracle-free syntax; oracleCalls=0 follows by the resource definition. This does not charge evaluation of arbitrary real input core entries, discovery of a normalized train from another data source, coherent parameter loading, inverse/control construction for an additional external API, or classical preprocessing.

4. Ancillas/garbage: input data and bond wires are computational zero. All output bond labels except the unique all-zero label have zero amplitude. No measurement, postselection or untracked garbage sector remains for the prepared column. q is an explicit workspace size, not proved minimal; the resource record's pureAncilla=0 is not a claim of no workspace.

5. Phases: the signed boundary is multiplied into the first core, orientation correction uses an unused completion column, and Gray target reversal negates physical angles. Exact complex amplitude equality is asserted, stronger than equality up to phase or probabilities. Unspecified completion columns are not additional freedom in the target column.

6. Error/success: there is no approximation parameter, norm-error tolerance, finite-shot probability or postselection success variable. The complete zero-input column is deterministic ideal-unitary action, with cleaned bond; the report does not infer hardware or numerical fidelity.

7. Resources/model: final instruction-list bound is `(n+1)*6*(2^q)^3`, not merely a proxy number of abstract planes. The inherited compiler has exact-real RY/CX lists; the public syntax also admits X/RZ. This is an exact-real logical-gate existence statement. Arbitrary real angle evaluation/export, finite-bit precision, Clifford+T compilation, finite error accumulation, arithmetic runtime/cost of canonicalization/completion/Gray/Givens extraction, input storage/evaluation, connectivity routing, physical depth/noise and readout are not supplied. Classical choices in SO completion and stage selection are not an executable preprocessing-cost certificate. Conversely, these omissions do not negate the already proved exact list action or literal gate-list bound.

## Evidence and handoff boundary

This report was written before the bounded target compiler/probe stage. `formal-input-seal.json` records exact source headers and full-file digests; later `signatures.json`, probe outputs and `evidence.json` must say which actual sources were freshly compiled and which providers were inherited. A cached target check is not fresh source compilation. No production/Git/cache writes, natural-language agreement judgement, all-library/Tests gate, source coverage graph, publication admission or Exposition Seal is performed by this run. Parent integration/review remain separate. Unknown token/currency costs are not invented.
