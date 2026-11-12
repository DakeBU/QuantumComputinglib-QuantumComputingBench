# c26r independent static source/formal/metadata comparison

Run: `tt-physical-source-review-c26r`, continuing the same reviewer who authored the original source-only notes. Status: `STATIC_PASS_PENDING_DECODER_AND_COMPILE`. This is not a final accepted publication review.

## Frozen inputs and chronology

The source-only notes (`source-only-notes.md`, SHA256 `fc3dfacf6ad4deb486bcc0fa22ccb3ff82f218ad0f1393329ed6bbfa84f664c3`) were frozen before actual formal/provider delivery. The original private phase-one seal is retained unchanged, bound by its later public transport companion (`phase1-public-transport-seal.json`, SHA256 `42f8748552b6ea71816230f8974b0e2a4ce32563a7f5bab64dfea8f8e1c2bae9`). This second phase does not rewrite those earlier artifacts or claim pre-proof chronology.

The parent separately authorized static formal and author-metadata exposure through `reviews/publication/finite-real-tt-physical/static-review-inputs-c26r.json`, SHA256 `bf51e531930af580a2fc1dbc685fadbca51087e3208df0e1ccfd461588e361b0`. I verified all 26 listed input hashes and all 41 provider-index hashes against actual files before using the providers. All matched. The 41-provider list is an import closure, NOT an assertion that I semantically audited all 41 modules or extracted their elaborated proof dependencies.

I completely read the actual three target modules, not only the author's embedded copies. The embedded `full_source_lines` concatenate exactly to the actual target texts. Target hashes:

| Module | SHA256 |
| --- | --- |
| `QuantumBlockEncoding/TensorTrainLocalCompiler.lean` | `ba397af87d9faf52be581f4d87e414c50821fa438541f7fbc6ef801e6acb88e2` |
| `QuantumBlockEncoding/TensorTrainWord.lean` | `2b7d16226ae2ebf09f5ead27572af52d75f37b0e1e7a8133bd2f0ee42d3a82e4` |
| `QuantumBlockEncoding/TensorTrainPrimitivePreparation.lean` | `3b9c745db873f678b80bc7ddc3200eb9ed9d4ba14587f7ad9edeb01251131000` |

The source/lesson has its original SHA256 `d71f16da026938debcd024d6f2fa9fa9268ade2096b5854a030d2065828b315d`. I reviewed author coverage and graph content only AFTER my independent source seal. Their stated earlier-reviewer provenance remains their provenance; no old reviewer file was opened and their graph is not relabelled as my independently extracted graph. The source is retrospective local exposition; the historical formalizer is still UNKNOWN.

No decoder reconstruction, decoder native evidence, compile output, or old review verdict was read. `author-decoder-packet.json` was read only as an authorized formal-only input descriptor; it contains no decoder reconstruction. No Git, Lean, simulator, cache, or main-repository write was performed. I did not execute the author selftest, publication validator, or binding-digest replay that would traverse additional production/test files. Those author claims remain claims, not my execution evidence.

## Necessary provider inspection

Completely read after hash verification: `TensorTrainCanonical.lean`, `TensorTrainSchedule.lean`, `ThinLQ.lean`, `RealIsometryCompletion.lean`, `GrayGivensCompiler.lean`, `GrayBasis.lean`, `SequentialPrimitiveAssembly.lean`, `PrimitiveWireRename.lean`, and `PrimitiveCircuit.lean`, all under `QuantumBlockEncoding/`.

Bounded necessary definitions/signatures/proof regions read after hash verification:

- `PrimitiveSemantics.lean`: RY/RZ signs, named-wire basis and X/CNOT actions, lift semantics, primitive/list evaluation, full-space unitarity and chronological append.
- `SequentialBondPreparation.lean`: finite Core/Stage/BondState, fresh-zero/lift/step/run/transfer, local basis reindexing and circuitStage, support and mass interfaces. Not an audit of every theorem in that provider.
- `AdjacentGivens.lean`: ordered plane definitions, elimination angle/pair/zero behavior, Step, sweep/final determinant and reverse-inverse decomposition interfaces/count. Not a fresh check of every intervening sweep proof.
- `UniformlyControlledRy.lean`: half-sum/difference tables, block specification, actual recursive compiler, exact evaluation interfaces and RY/CNOT counts.
- `SelectedRyPlane.lean`: exact selected-plane block, full-control context equivalence, actual list realization, length and cubic-bound proofs.
- `RealAmplitudePreparation.lean`: last-wire basis, liftGate/liftLastMatrix/evaluation, pairNorm/signed splitAngle and its complete first-column proof.
- `PrimitiveBasisLE.lean`: general-width equivalence and recurrence, including width zero.
- `HermiteBoundaryInjection.lean`: only wordValue, its finite bound, and wordSampleIndex with exact length carrier. No scientific target theorem is borrowed from that provider's name.
- `Resources.lean`: Resource and ofCountsWithDepth; `Core.lean`: gridSize; `Robin/ComplexLCU.lean`: rotation and permutation matrix definitions needed to expand primitive semantics.

Exact provider path/hash authority is the frozen `author-formal-context.json` (SHA256 `6a056581661325754ed0a72e6fa8e092b2fd265df034ec97471f4c1738753232`). No hidden conclusion about the entire unrelated Robin/GHL/Hermite import closure follows from these bounded reads.

## Whole-module scope and inventory

There are exactly 10 + 12 + 15 = 37 public named declarations, matching the formal context's names, kinds, and actual one-based declaration lines. The actual whole files have no extra named instance, private declaration, opaque/axiom declaration, ambient variable binder, sorry or admit. Full scope includes imports, namespace/open commands, simp attributes and proof-local definitions. The scoped `backward.isDefEq.respectTransparency false` affects elaboration of `run_circuits_clean`; it does not add a mathematical premise or axiom. Exact elaborated types/axiom reports are intentionally deferred to the separately authorized compiler/decoder stage.

Below, LC/TW/TP are author inventory IDs used solely to identify the 37 exact declarations. Source references C1, W1, etc. are MY previously frozen source-only nodes. Implicit natural dimensions, finite matrix/vector/chain data and ordinary Fintype/DecidableEq instances are TYPING. Logical assumptions are SOURCE as listed. There is no RULED correction, new STANDING access assumption, or EXCESS logical premise in these lexical interfaces. Injections/bijections have genuine SOURCE mathematical content, even though their carrier/type components are TYPING.

| ID / declaration suffix | Actual line | Logical source inputs; result/definition audit | My source nodes |
| --- | --- | --- | --- |
| LC-01 `exists_SO_named` | 12 | strict r<card(I), injected positions e, V^T V=I; ONE U produces orthogonality AND det=1 AND all prescribed columns | E1,E2 |
| LC-02 `localIndex` | 36 | no logical premise; literal last-bit/LE-bond equivalence | W1 |
| LC-03 `localIndex_snoc` | 39 | no logical premise; all labels obey that coordinate equation | W1 |
| LC-04 `paddedAt_real` | 44 | no canonicality/site/bond premise; real embedding equality for every time | C2,C3 |
| LC-05 `paddedAt_im_zero` | 56 | no logical premise; imaginary part zero for every time | C3 |
| LC-06 `activePositions` | 61 | l<=2^q; literal fresh-zero embedding with injection proof | W1 |
| LC-07 `activeColumns` | 69 | maxBond<=2^q; literal real padded columns with bound-based cast | C2,C3,L1 |
| LC-08 `activeColumns_isometry` | 77 | canonicality AND maxBond<=2^q AND t<n; produces Gram=I | C3,L1 |
| LC-09 `exists_local_circuit_with_resources` | 99 | same three SOURCE premises; ONE actual list produces bound AND zero-oracle AND full-output active-input columns | L1–L4 |
| LC-10 `exists_local_circuit` | 139 | same premises; projection of LC-09 forgetting only zero-oracle field | L3 |
| TW-01 `toBasis` | 10 | literal recursive first-coordinate word map, no logical premise | I1 |
| TW-02 `toBasis_wordOfBasis` | 14 | no logical premise, basis inverse including n=0 | I1 |
| TW-03 `wordOfBasis_toBasis` | 20 | no logical premise, word inverse including n=0 | I1 |
| TW-04 `basisEquiv` | 26 | literal equivalence with those two inverse proofs | I1 |
| TW-05 `reverseBasis` | 32 | literal coordinate rev, with involutive inverse | I1 |
| TW-06 `sampleEquiv` | 38 | literal basis THEN reversal THEN LE; gridSize n=2^n | I2 |
| TW-07 `toBits` | 41 | literal empty/cons Boolean-list map from Fin 2 | I1 |
| TW-08 `toBits_length` | 45 | no logical premise, produced exact length | I1 |
| TW-09 `primitive_snoc_value` | 50 | no logical premise, exact append LE arithmetic | I3 |
| TW-10 `sampleEquiv_value` | 73 | no logical premise, sample value equals MSB-first wordValue | I2,I3 |
| TW-11 `wordSampleIndex_eq` | 90 | positive width n+1 in data type; length proof is produced, not assumed | I3 |
| TW-12 `sampleEquiv_public` | 96 | no logical premise, double-reversal index cancellation | I4 |
| TP-01 `boundaryRow` | 22 | literal one-row matrix from arbitrary u | B1 |
| TP-02 `boundaryRow_isometry` | 24 | mass(u)=1 produces row-isometry | B1 |
| TP-03 `boundaryCore_isometry` | 32 | mass(u)=1 AND A*A^T=I produce absorbed row-isometry | B1 |
| TP-04 `boundaryCore_contract` | 41 | no norm/canonicality premise, entire terminal matrix equality | B2 |
| TP-05 `exists_unitBoundary_canonical` | 51 | maxBond<=B AND original complete squared mass=1; nonempty Chain(n+1,1,1) carrier; produces canonical scalar D, bound and pointwise signed amplitudes | F1,B3 |
| TP-06 `transportStage` | 70 | supplied equivalence e; literal two-bond-index reindex, no finiteness assumption needed for this definition alone | T1 |
| TP-07 `run_transport` | 73 | supplied finite bond equivalence e; no unitarity/norm/state-action premise, arbitrary complex boundary/matrices | T1 |
| TP-08 `bondIndex_zero` | 87 | no logical premise, all-zero LE label | Z1 |
| TP-09 `bondIndex_zero_iff` | 94 | no logical premise, exact iff at all q including 0 | Z1 |
| TP-10 `initial_padding` | 104 | no logical premise, literal padded singleton equals EMPTY circuit's zero-input column | Z1 |
| TP-11 `run_circuits_clean` | 120 | maxBond<=2^q AND only t<n occupied fresh-zero column equations; produces full-state sequential action/cleanup for every output | A1,A2,A0,T1,Z1 |
| TP-12 `publicCircuit_clean` | 153 | same conditional SOURCE premises; actual public list action at every x,b with reversed data word | P1–P3 |
| TP-13 `assemble_gateCount` | 169 | no logical premise; exact list-length sum for arbitrary supplied stages including N=0 | K1 |
| TP-14 `publicCircuit_gateCount_bound` | 183 | executed-stage list length <= bound; produces total <=n*bound | K1 |
| TP-15 `exists_primitive_preparation` | 205 | ONLY maxBond<=2^q AND original complete squared scalar mass=1 on Chain(n+1,1,1); ONE circuit produces list bound, no oracles, full-space unitarity and exact signed all-output zero-input state | R1–R3,R0 |

The author coverage's SOURCE/TYPING classifications are compatible with this audit when read together: e.g. e in LC-01 is described among data/type binders AND independently has its injection content classified SOURCE. This is not silently treating injection as a vacuous typing assumption. No bundled original canonicality or desired action is hidden by the actual target scope.

## Expanded definition and producer audit

Core is literally a real matrix with left rows and (bit,right) columns. Chain indices enforce matching bonds and explicit boundaries. Word is Unit at zero and Fin 2 times the tail otherwise; contract is I_r on nil and slice(head)*contract(tail) otherwise. RightCanonical recursively means each A*A^T=I; maxBond includes both endpoints. rankAt remains terminal beyond the end; paddedAt is deliberately zero beyond the end. These definitions agree on their whole public carriers, including natural zero dimensions. The after-schedule zero is source-defined literal semantics, not a fake isometry fallback.

`mass u` is sum u_i^2. `exists_normalized_state` derives unit residual mass using the entire word-and-terminal mass, not by selecting a terminal sector. ThinLQ admits rank-deficient/empty matrices, uses exactly min(m,n) orthonormal rows, and its tail-first caller absorbs the tail residual before factoring the head. `exists_unitBoundary_canonical` absorbs the SIGNED u into an actual first core; original boundary one gives the new boundary bound. No absolute value, global-phase quotient, free state preparation or full-rank premise is introduced.

`PrimitiveCircuit k` is literally List(PrimitiveGate k); `gateCount` is list.length. PrimitiveGate constructors are X, RY, RZ, and distinct-control-target CX, with arbitrary exact real angles supported by ExactAngle.real. Evaluation of gate::rest is eval(rest)*eval(gate); empty is identity. The matrix unitaryGroup conclusion is the full named-basis matrix property, not unit mass of a single column. Resource.oracleCalls=0 is definitionally true in this oracle-free language, not a statement that input-angle acquisition was free.

All ten target definitions are literal compositions/entries, not unique-characterized or quotient choices. Precisely the target defs are LC localIndex/activePositions/activeColumns (3), TW toBasis/basisEquiv/reverseBasis/sampleEquiv/toBits (5), TP boundaryRow/transportStage (2): ten definitions and twenty-seven theorems. There is no exists-unique-based definition to justify. Nonunique choices occur inside proofs/providers: orthogonal extensions, thin factors, angles/control enumerations and stage circuits. Existence is proved before use of choice; no uniqueness, canonical representative, deterministic producer, or preprocessing cost follows. Arbitrary off-occupied columns are allowed, while every downstream amplitude claim is independent of those choices by support induction.

The full circuit list is constructed with empty initialization, lift/place/append and bijective instruction renaming. Internal q-low bond wires become public high wires N+a; chronological output q+t becomes N-1-t. This is gate placement, not a free physical permutation of an already prepared state. General placement/action helpers include all N=0 cases. The root remains strictly positive length by its n+1 carrier.

## Seven-slot source-versus-actual comparison

| Publication semantic slot | Static comparison result |
| --- | --- |
| target | MATCH. The TP-15 result is the original C contraction, embedded in complex amplitudes, at wordOfBasis(x composed with rev). It is not a Hermite/sampled-data theorem and does not prescribe every input column. |
| normalization | MATCH. hNorm is the full real squared scalar-amplitude sum; signed residual normalization is derived. Conditional TP-04/07/11/12 carry no unnecessary normalization/canonicality premise. |
| registers | MATCH. Fin k -> Fin 2 carriers; local snoc bond/fresh-bit order; public append(data,bond); q=0 allowed; root N=n+1>0; after-schedule columns unused. Word/basis/Boolean/LE maps are explicit and width-correct. |
| oracles | MATCH. Actual instructions have no oracle constructor. No data-oracle, coherent parameter access, inverse/control whole-family interface or SELECT oracle is assumed or concluded. |
| ancillas_phases | MATCH. Same q bond wires, initially/finally zero; no extra work wire; all output amplitudes included. Exact original signed amplitudes, not merely probabilities or unspecified phase. Unused orientation column and Gray endpoint angle sign are internal produced choices. |
| error_success | MATCH. Exact ideal action and full-space unitarity; no postselection, accepted sector, probability parameter, error norm or finite-precision claim. |
| resources | MATCH. Same witness actual list has <=(n+1)*6*(2^q)^3 instructions and no oracle calls. TP-13/14 use list.length including X/RZ if supplied to generic helpers. Existential exact-angle choices are not costed input access, arithmetic, storage, synthesis, routing, depth or external scientific scaling. |

All matches are static source/formal judgments, not a substituted decoder or compiler result.

## Source topology versus actual route and author graph

My source-only graph has a single complete root route and explicit AND tails. The actual proof follows that route: TP-05 canonicalizes/absorbs; LC-09 obtains the SO extension and Gray/Givens list on its occupied fresh-zero columns; TP-11 supplies support/transfer transport and terminal cleanup; TP-12 places the actual list in public order; TP-13/14 add actual lengths; TP-15 chooses stages only where t<N and combines action, length, no-oracle and unitarity for ONE c.

The source diagram is not inferred from these Lean calls: it was already frozen in my notes. The author's 32-edge transcription agrees in mathematical content, with the following crosswalk (my source IDs remain distinct from author IDs):

| Author graph edges | My frozen source nodes / obligations |
| --- | --- |
| P01–P04 | C1–C3,W1: carriers, padding/support, actual-site isometry, LE local coordinates |
| P05–P06 | E1,E2: prescribed full columns, unused-column orientation correction/nonuniqueness |
| P07–P12 | G1–G5: primitive semantics, adjacent sweeps, reversed inverse list, Gray sign/transport, recursive selected lists and count |
| P13–P14 | L1–L4: real occupied-column extraction and produced local circuits |
| P15–P18 | B1,B2,F1,B3: unrestricted contraction identity, normalized row-isometry, tail-first supplier, positive-length signed absorption |
| P19–P23 | Z1,T1,A1,A2,A0: actual empty zero initialization, bond covariance, support induction, terminal cleanup and empty helper |
| P24–P27 | I1–I4: word/basis/list maps, reversal and public sample cancellation |
| P28–P31 | P1–P3,K1: actual internal list semantics, public placement, exact sum and N*K bound |
| P32 | R1–R3,R0: complete same-witness AND conclusion and positive/zero length distinction |

All 74 author paragraphs concatenate byte-for-byte to 21,210 source bytes; every paragraph hash and byte offset matched. Only title/section headings are EXCLUDED. Substantive scope/frontier paragraphs are NODEs, and their gap links are diagnostic/boundary links, not proof implication. The source graph's primitive support/output/rank and phase/order/resource paragraphs are not lost behind the target inventory.

The author graph explicitly retains determinant +/- and zero/nonzero pair guarded alternatives. Its P10 ordered-endpoint-sign ingredient contains the target-bit orientation conditional; my notes spell both sign guards out. Neither depiction creates two independently sufficient root constructions. P32 retains all canonicalization, stage synthesis, initialization, transport, terminal cleanup, placement, length and primitive-unitarity tails. Canonicality/columns/cleanup/count are outputs inside the root, not newly promoted source binders. P23's zero-length helper is not a route to arbitrary signed zero-wire state preparation.

There is no new internal SOURCE_GAP revealed by static comparison. Source proof obligations now have actual named candidate providers, but compiler verification remains withheld. The author's six stronger-consumer gap categories preserve my DATA_REPRESENTATION, DETERMINISTIC_REFINEMENT, FINITE_PRECISION, HARDWARE_RESOURCES, COHERENT_TRANSPORT/BE_TRANSPORT and EXTERNAL_POLYNOMIALITY boundaries; the last two coherent/BE categories are grouped in its one oracle/BE gap. My EMPTY_SIGNED_TARGET boundary is separately retained by source P23/P32 and actual n+1 root typing. These consumer gaps do not negate the narrower exact-real theorem and cannot be closed by the word index bridge or instruction count.

The Lean view labels import and ownership edges honestly and leaves elaborated theorem dependencies empty. The compressed spine remains navigation-only/pending purification with drill-down. The functor view has no certified implication hyperedges or categorical claim. Diagnostic IDs in the source graph are labels, not reviewed execution evidence; I saw no simulator/tests in this static packet and do not promote them as proof.

## Joint author-metadata judgment and remaining gates

The lesson is exactly the pinned natural source. Author rows/coverage, formal context, frozen formal-only packet, source graph, binding bridge proposal and candidate records retain retrospective/WIP status. All 37 declarations are mapped as proof edges or prerequisites. The three parent c26r proposals preserve the public checker's eleven binding-selected fields from their author candidates, preserve the same claimed public binding digests, and change the review-routing/continuity metadata to this actual run with FUTURE reviewer evidence. I did not infer acceptance from any author status or parent assertion that decoder evidence exists.

Claimed publication bindings, NOT freshly replayed by this reviewer over the checker's wider production/test closure:

- local compiler: `76cb8091e361a7f31bc99aed73db73816b0000457b45d9a8cd7f8d34078b587d`;
- word adapter: `2c9e0d3aa865534e15a4b9c987ac7ea0117acc4612b973e847886a15110f2c8d`;
- primitive preparation: `3524f3ed0dd02245af190769a6920ce8355fa7888aa4ed1401f48d4bf7bacc2f`.

The parent proposals explicitly distinguish the old run, absent old final joint seal, this fresh source review and the original author graph provenance. I neither impersonate the old reviewer nor attest its unobserved exposure history. Historical formalizer UNKNOWN is not resolved by a mechanically distinct author-curator identity string.

Toolchain is Lean 4.33.0; manifest pins Mathlib to `db584cd6d46c92f209a44c0f1c829460d327499d`. The lakefile and checker hashes are among the verified 26 inputs; lakefile isn't silently treated as a field bound by a publication digest that omits it. The checkpoint/base/head strings are metadata, not a new Git check by this reviewer.

One nonblocking editorial observation: `publication-freeze.json`'s binding_recipe says “twelve selected record fields”, but the actual frozen checker's tuple selects ELEVEN fields. I compared exactly those eleven fields. This wording does not alter the algorithm or current field equality and does not require a mathematical repair or invalidate static semantic comparison. No file was edited to conceal or repair it.

Verdict: no blocking mathematical, lexical-interface, definition, source-topology, seven-slot or author-metadata mismatch found. Failure class NONE for this static objective. Status remains `STATIC_PASS_PENDING_DECODER_AND_COMPILE`, not accepted/PROOF_SEALED/main-admitted/PURIFIED/scientific_ROOT. Source-faithful signatures have not yet been checked against independently elaborated #check output, kernel/build/axiom evidence, or a source-blind decoder's reconstruction. Exact public binding replay/late decoder binding and final reviewer evidence must be checked at the authorized final stage, without redoing unchanged source mathematics or fabricating historical chronology.

No final `*-evidence.json` is authored in this phase. The next step is parent delivery of the bounded decoder/compilation packet under separate authorization; until then those inputs remain unread. All earlier source-only artifacts are preserved unchanged.
