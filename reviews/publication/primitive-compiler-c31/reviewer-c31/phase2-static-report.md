# Primitive compiler c31: phase2 STATIC comparison

## Scope and outcome

The three complete target source modules have been read, including proofs, private helpers, the structure body and all fields, namespaces, imports, opens, and declaration-local options. Their mathematical statements and constructions are consistent, at the static source-reading layer, with the independently frozen phase1 reconstruction. This is not a SourceAgreement verdict or formal/native acceptance. Actual elaboration, generated declarations, axiom closure, kernel/native trust, compilation, decoder comparison, publication, root/main admission and purification have not been checked.

There are concrete metadata corrections and important graph refinements below. No mathematical counterexample to the pinned source identities was found. No production or author file was changed. The original phase1 notes and seal are immutable and retain their original hashes.

Logical paths only are used. `$PROJECT` means the assigned repository. `$AUTHOR/natural` denotes the original three-file natural-source package; `$AUTHOR/effective` denotes the separately authored effective metadata package. These are logical package labels, not assertions that the two host directories are nested. `$REVIEWER` denotes this reviewer's exclusive output package. The original phase1 `$AUTHOR/source-only.md` is the same source now labeled `$AUTHOR/natural/source-only.md`.

Reviewer: `/root/primitive_compiler_source_first_c31`. Original natural author: `/root`. Effective metadata author: `/root/primitive_compiler_metadata_c31`. Historical formalizer: UNKNOWN. No decoder identity or result was read. These identities distinguish the present authoring acts, not an unknown historical implementation author.

## Bound inputs and mechanical checks

| Input | SHA256 |
| --- | --- |
| `$REVIEWER/source-only-notes.md` (unchanged phase1) | `ec1a9cd7054bab38f6ee7bea3f2a8b2ba9ebd8cfa9cd4440cd0838e154b445cc` |
| `$REVIEWER/phase1-seal.json` (unchanged phase1) | `13a68071140ae9cd87b7f520cdf9cf88421e53357bdadcb7b44cdfe5adaf0675` |
| `$AUTHOR/natural/source-only.md` | `5907262565b6202fec61b189c42d942cb84d6215223a0da4211d63b92d3ad168` |
| `$AUTHOR/natural/source-freeze.json` | `b4a2a5e93b834dd703a126dfb91322c5dd9da5dba490f6dcb06c25b09ab1ad86` |
| `$AUTHOR/natural/author-private-coverage.md` | `fc0e1562a93f71f3f45ae594a35d3898e5db9d070e8053bec3f7ae6ad562ff6f` |
| `$AUTHOR/effective/author-formal-context.json` | `a0b798f1e74b084274a44061514f7944ea6b694c13af2b8f718a27ea7b0ac408` |
| `$AUTHOR/effective/outputs-manifest.json` | `3558853cca2a5e0503f5f633d0a7aac441ac79a5d7ce3c87a19f049fd1743d87` |
| `$AUTHOR/effective/supplement-manifest.json` | `8b5926e2b9830d0ca66959eb08c548ac04d34dc54d9fab91bd488cf20a08bdfa` |
| `$AUTHOR/effective/author-binder-definition-audit.json` | `05e6c2bcad39cc286483534dbf8c311847a3639cf0ca0d52b0d52b558bbd713c` |
| `$AUTHOR/effective/author-source-coverage.json` | `09a49591efeccf046200cf8d51b9b11fb7ffaf8befb239e4426e1e44ba0b307b` |
| `$AUTHOR/effective/author-graph-views.json` | `372356de38ac54593e9582c1503d7384ba1ada383ab8d9801e82a4dab154d254` |

The three requested effective-package digests match the authorization. For each target, actual file hash, full text, line count, authored root sequence and every source block were independently compared with the metadata. Results: PrimitiveMacros 638 lines/43 roots; UniformlyControlledRy 422 lines/19 roots; CubicAmplitudePrimitive 230 lines/25 roots. All 87 source blocks match the actual line slices and their author-audit copies. Public/private counts are 79/8. The source-paragraph partition concatenates exactly to the original source, and duplicated binder/definition records agree across the two author JSONs. These are source-byte/lexical checks, not elaboration or semantic approval.

| Whole target actually read | SHA256 |
| --- | --- |
| `$PROJECT/QuantumBlockEncoding/PrimitiveMacros.lean` | `bd5ada5cb61430ea9d32ce1b3adbd84e6b13d8c3fe2c1b6f2758da2a06903664` |
| `$PROJECT/QuantumBlockEncoding/UniformlyControlledRy.lean` | `78d1aed9bb4068bcee138b665bd93a389463bbb591108837758a6d80752a1cf1` |
| `$PROJECT/QuantumBlockEncoding/CubicAmplitudePrimitive.lean` | `48c9a4a1c47c925c93493eede21eb7b492d23d2cb7dadf254782e4485c349cb3` |

## Findings requiring precision or correction

### F1. Two actual dependent function signatures are absent from the author binder lists

For C31-055 `compileUniformlyControlledRy` and C31-056 `uniformlyControlledRyMatrix`, the author `binder_audit` lists only `{qubits : Nat}`. Their actual definitions have, after the colon, the dependent function inputs

    (controls : Nat) -> (wires : Fin controls -> Fin qubits) ->
    (target : Fin qubits) -> (forall control, wires control != target) ->
    (PrimitiveBasis controls -> ExactAngle) -> result.

The compiler returns `PrimitiveCircuit qubits`; the recursive matrix returns a complex square matrix on `PrimitiveBasis qubits`. Controls, wires, target and angle-table data are source-specified data with typing roles; the target-avoidance proof is a SOURCE guard. The exact-angle evaluation convention is STANDING source semantics, not free computational access. No injectivity premise exists. The omitted guard must not disappear from the audit simply because it is inside the result's Pi type.

The limited producer inspection explains the omission: `$AUTHOR/effective/author-package-build.py`, lines 57–85, scans only leading bracketed groups and stops at the colon. Its lexical proof-test is a regex, not type elaboration. This is an audit-extractor omission, not a missing guard in Lean. The raw full definitions are intact, and later theorems C31-057–062 spell the guard explicitly. A successor metadata audit should recursively inspect Pi inputs or enumerate these inputs explicitly. No original sealed artifact is edited by this report.

### F2. Whole-source coverage exists, but its per-declaration source links are coarse

All 43 macro roots are linked to the same S2/S3/S4 paragraph set; all 19 multiplexor roots to the same S5/S6/S7 set; all 25 cubic roots to the same S8/S9 set. For example C31-009/010 implement S1 lifting, although the generated row points to S2–S4. The 34 paragraph records do retain every substantive source region, but repeating an entire module's regions for every declaration does not establish precise theorem-level proof edges. The 87-row reviewer table below supplies narrower source identities from the untouched phase1 inventory. Source-faithful completeness must not be inferred from the count 87 alone.

The old private coverage is explicitly lexical and several headers are truncated at `:=` within a let/recursive body. For example `hadamardMatrix_apply` ends at `let scale : C` in its old header and both recursive definitions include early body material. Actual full source, not those strings, is the statement authority. The new metadata preserves that full source; no formal signature digest has been inferred from the lexical headers.

### F3. Coarse graph bundles must not be mistaken for actual theorem dependencies

The author source graph correctly separates the three different targets, retains conditional context cases, and does not introduce a CCX-to-cubic prerequisite. Its `verified-finite-wrapper` source edge includes exponential reference cost, while the conceptual transport to the same head does not. The actual verified-wrapper definition uses unitarity and clean-entry proofs, not the count theorem. The cost/presentation portion is separate data. Likewise flat-unitarity itself is independent of clean-entry correctness, even though the author graph bundles unitarity and transported clean entries under `flat-unitary`.

These bundles can be reader navigation, but cannot be exact proof implication edges without distinguishing their subclaims. Correct complete tails are given below. The author graph's `guarded_OR_cases` are exhaustive proof case splits; both branches must be proved to obtain a uniform theorem. They are not independently sufficient alternative constructions for the same unguarded target. Conversely the source explicitly allows the eight-bit-case proof OR XOR expansion for E=4abt; this local proof OR is not shown in `alternative_sufficient_routes: []`. That empty list can mean no alternative full compiler, but must not erase the local alternative proof described in S4.

### F4. Generic certificate names carry weaker authority than their concrete instance

The actual generic `OperatorBlockEncodingCandidate` stores arbitrary `isUnitary : Prop` and `blockContainsTarget : Prop`; `layoutMatches` proves only a count equality. `VerifiedOperatorBlockEncoding` supplies proofs of those stored Props. The generic type name therefore does not force physical unitarity or a clean-block formula. The current cubic candidate, however, literally instantiates the first Prop by membership of its explicit matrix in `Matrix.unitaryGroup` and the second by the exact clean-entry/normalizer equation. The verified definition then supplies the actual named unitary and clean-block theorems. This instance is not a Boolean-only certificate and does not merely prove `True`.

This resolves the concrete field concern statically, while retaining the generic API boundary. The strings `source` and `semanticContract` have no proof authority. The presentation circuit is not tied by these generic types to an angle-complete executable semantics; here its rotations intentionally discard the angle and store `exact-angle`. Comments saying that an executable semantic route is closed, or that a resource row is accepted, cannot upgrade that presentation into executable-family acceptance.

### F5. Native proof scripts are visible, but their acceptance and trust are not inspected

The cubic bound, encoded-index identity and context-iff identity contain `native_decide +revert`; the LE provider also contains native finite proofs. No such command was run. The independent rational and encoding arguments in phase1 remain the mathematical checks. No runtime output, compiled artifacts, generated axiom listing, or kernel acceptance was read. Absence of visible `sorry` or an explicit axiom declaration in the three targets is not an audit of transitive axiom closure or the actual generated proof terms.

## Static mathematical comparison, path by path

### Macros and monomial/CCX path

The actual H body is `I` times `standardRyMatrix(pi/2) * standardRzMatrix(pi)`; H's literal circuit lists Rz then Ry with phase pi/2. T/inverse-T phases are pi/8 and -pi/8 with Rz angles pi/4 and -pi/4. Provider evaluation uses exp(i phi) and later list instructions multiply on the left. This exactly matches phase1, including the signs and chronology.

The monomial definition tests output row against the permutation of the input column. Its multiplication theorem evaluates the right program's phase at the left permutation and composes `leftPerm.trans rightPerm`. No modulus-one premise is present. `MonomialProgram.exact` is an actual matrix equality proof field; sequential construction invokes both input equalities and the multiplication theorem. Those equalities are internal dependencies, not extra hypotheses of the final CCX theorem.

The 13-step middle list is the literal S4 network, with six CX gates, four T macros and three inverse-T macros. Its source proof restores the permutation and then checks the eight phase cases. The stored middle global phase evaluates to pi/8; adding the two H phases gives 9*pi/8 for the whole CCX program, while the full program matrix is exactly the phase-free CCX permutation. Thus a nonzero stored phase must not be misreported as an unwanted residual matrix phase. The raw elementary list has eleven one-qubit gates and six CX gates, independently derived from the source constructors, not asserted as a new compiled resource theorem.

The final network and refinement have all three distinctness binders. `cczMatrix_eq_blockDiagonal`, `equivPermutationMatrix_ccx_eq_blockDiagonal`, and `hadamard_conjugates_ccz` require only a!=target and b!=target; a and b may coincide there. The actual reversible provider's `ccxBasisEquiv` has the same weaker pair of guards. The actual `PrimitiveGate.cx` constructor carries control!=target, eliminating the invalid same-wire operation highlighted in phase1.

### Controlled-Ry path

The independent block matrix selects the table with `primitiveControlAssignment` on the complete non-target context, not with a separate arbitrary control register that could access inconsistent repeated-wire tuples. Its entry theorem uses row context; equality of contexts makes the selected tuple identical on either side. No injection premise appears anywhere in the actual target. Empty controls select the unique empty tuple and emit one Ry.

The three private angle helpers are exactly prepend, half-add and half-sub. The provider defines ExactAngle addition, negation, rational scaling and their evaluation rules; `.real` also admits an arbitrary mathematical real without a decimal export promise. Thus the generic source table's real-valued scope is not silently reduced to rational multiples of pi. The compiler recurses on tail wires, appending alpha, CX, delta, CX. The recursive matrix definition uses the reverse chronological matrix product as expected.

Crucially C31-058 proves the independent specification by its own induction; it does NOT call C31-057. Both base and successor cases read correctly against the phase1 derivation: zero-control block, CX context block, exact half-angle evaluations, context-local Ry addition, X conjugation, and explicit head zero/one assignment equalities. Correlation between head and tail controls never invalidates this proof, since every gate preserves the complete context. No untracked phase or garbage register is introduced.

The two count proofs are separate inductions on the emitted list and match 2^n and 2(2^n-1). The five-control conjunction specializes them. Zero opaque oracle calls comes from the primitive resource definition, not an efficient arithmetic provider. With duplicated wires the counts still refer to control positions, not the smaller number of independent physical bits.

### Finite cubic and LE clean-block path

The actual provider definitions used are `gridSize n=2^n`, `gridPoint n j=j/2^n`, `cubicAmplitude=(gridPoint)^3`, and `cubicDiagonalOperator` with row=column diagonal condition. The unrelated rank-one `cubicOperator` exists in the imported provider but is not the chosen target. The target module fixes controls 0 and 1, signal 2, and the index b0+2b1. It derives the finite bound before constructing `.twiceArccosRational`. No bound or compiler-correctness proof is assumed as a final cubic theorem binder.

Program phase is literally rational zero. The full evaluated program theorem is equality to the independent block matrix; the clean-entry proof then uses the encoded-index and context-iff facts, the standard half-angle bridge, and the arccos clean-entry identity. The actual standard-Ry bridge theorem has domain binders -1<=d<=1 although its equality to `amplitudeRotation` is definitional; the domain is substantively used by the latter's clean-entry theorem. Those bounds are supplied internally by the finite producer, not moved into the public clean-entry statement.

`cubicN2EncodeBits` is exactly the source encoding for arbitrary signal and system indices. The LE provider's recursive value equation is bit0+2*tail, so unfolding three times yields j+4s on this encoding. The actual flat matrix uses reindexing along `primitiveBasisLEEquiv 3` in the forward direction; its entries are evaluated at inverse images. `cubicN2PrimitiveCleanIndex` is the forward image of the signal-zero encoding, so the inverse laws give precisely the named-wire clean entry. There is no convention swap.

No separate target-module theorem explicitly spells out `cubicN2PrimitiveCleanIndex j=j`; it follows mathematically from the inspected equivalence and encoding definitions. Similarly the positive square-root signal-one column and the specialized 4/6 counts are consequences of inspected definitions/generic results, not additional named target theorems. Static consequence is not a freshly compiled formal root.

The flat-unitarity proof calls primitive-program unitarity plus reindex preservation. The candidate has auxiliary=1, system=2, signal=1, pure=0, normalizer=1 and default empty schedule/free-parameter list. Its actual Props and proof suppliers match those numbers. The stored resource is definitionally the program's circuit resource. The primitive schedule tracks the maximum current touched-wire layer; all ten emitted instructions touch signal 2, so its mathematical reference depth is ten as well as counts 4/6, oracle0, pure0. This is not a hardware scheduling, connectivity, finite-bit or general preprocessing theorem.

The source's state-normalization and success exclusions remain essential: the clean diagonal has rank three and norm 27/64; its coefficient vector has squared norm 397/2048; signal-zero success can be zero. The wrapper does not become normalized cubic state preparation, rank-one loading, scalable Hermite SP, or a general-n efficient arithmetic compiler.

## Complete 87-root reviewer coverage

Names in the first two tables are prefixed `QuantumBlockEncoding.`; names in the third are prefixed `QuantumBlockEncoding.CubicDiagonalOracle.`. Private names below are source-authored lexical identities, not a claim about compiler-mangled declarations. `Nxx` refers to the original untouched phase1 inventory. Each row's full source body was actually read, and each literal definition or proof was compared to its listed phase1 obligation. Whole source includes the commands between declarations; end-line spans may therefore include namespace/option commands.

### PrimitiveMacros: C31-001–043, all public

| ID | Source name | Lines | Phase1 obligations |
| --- | --- | --- | --- |
| 001 | hadamardMatrix | 15–18 | N02,N04 |
| 002 | phaseMatrix | 19–23 | N02,N04 |
| 003 | hadamardMatrix_apply | 24–40 | N04 |
| 004 | phaseMatrix_apply | 41–75 | N04 |
| 005 | primitiveHProgram | 76–81 | N05 |
| 006 | primitiveTProgram | 82–86 | N05 |
| 007 | primitiveTdgProgram | 87–91 | N05 |
| 008 | evalGlobalPhase_pi_div_two | 92–97 | N01,N05 |
| 009 | liftPrimitiveOneQubit_mul | 98–107 | N03 |
| 010 | smul_liftPrimitiveOneQubit | 108–116 | N03 |
| 011 | primitiveHProgram_eval | 117–131 | N03,N04,N05 |
| 012 | primitiveTProgram_eval | 132–151 | N03,N04,N05 |
| 013 | primitiveTdgProgram_eval | 152–173 | N03,N04,N05 |
| 014 | phasePermutationMatrix | 174–179 | N06 |
| 015 | phasePermutationMatrix_mul | 180–198 | N07 |
| 016 | evalPrimitiveCx_eq_phasePermutationMatrix | 199–206 | N08 |
| 017 | liftPhaseMatrix_eq_phasePermutationMatrix | 207–230 | N03,N08 |
| 018 | primitiveCxProgram | 231–235 | N01,N08 |
| 019 | primitiveCxProgram_eval | 236–247 | N08 |
| 020 | primitiveTProgram_eval_monomial | 248–256 | N05,N08 |
| 021 | primitiveTdgProgram_eval_monomial | 257–265 | N05,N08 |
| 022 | MonomialProgram (all four fields) | 266–274 | N08 |
| 023 | MonomialProgram.seq | 275–283 | N07,N08 |
| 024 | MonomialProgram.cx | 284–290 | N08 |
| 025 | MonomialProgram.t | 291–297 | N05,N08 |
| 026 | MonomialProgram.tdg | 298–307 | N05,N08 |
| 027 | primitiveCCXMiddle | 308–328 | N09 |
| 028 | primitiveCCXProgram | 329–337 | N12 |
| 029 | primitiveCCXMiddle_permutation_eq_refl | 338–362 | N10 |
| 030 | primitiveCCXMiddle_phase_eq_ccz | 363–384 | N10,N11 |
| 031 | cczMatrix | 385–392 | N11 |
| 032 | primitiveCCXMiddle_eval | 393–407 | N08,N10,N11 |
| 033 | zMatrix | 408–410 | N12 |
| 034 | hadamard_mul_hadamard | 411–419 | N12 |
| 035 | hadamard_mul_z_mul_hadamard | 420–430 | N12 |
| 036 | liftPrimitiveOneQubit_eq_blockDiagonal | 431–440 | N03,N12 |
| 037 | cczTargetBlock | 441–448 | N12,N13 |
| 038 | cczMatrix_eq_blockDiagonal | 449–504 | N12,N13 |
| 039 | ccxTargetBlock | 505–512 | N12,N13 |
| 040 | equivPermutationMatrix_ccx_eq_blockDiagonal | 513–584 | N12,N13 |
| 041 | hadamard_conjugates_ccz | 585–615 | N12,N13 |
| 042 | primitiveCCXProgram_eval | 616–628 | N12,N13 |
| 043 | primitiveCCXProgramRefinement | 629–638 | N08,N12,N13 |

### UniformlyControlledRy: C31-044–062

| ID | Source name | Lines | Phase1 obligations / visibility |
| --- | --- | --- | --- |
| 044 | prependControlBit | 16–19 | N16,N30; private |
| 045 | halfAddAngles | 20–26 | N16,N30; private |
| 046 | halfSubAngles | 27–33 | N16,N30; private |
| 047 | primitiveControlAssignment | 34–41 | N14,N15; public |
| 048 | controlledRyBlockMatrix | 42–50 | N14; public |
| 049 | controlledRyBlockMatrix_apply | 51–66 | N14,N15; public |
| 050 | kronecker_one_eq_blockDiagonal | 67–77 | N03,N15,N30; private |
| 051 | evalPrimitiveRy_eq_controlledRyBlockMatrix_zero | 78–91 | N15,N30; private |
| 052 | controlledXBlock | 92–96 | N15,N30; private |
| 053 | xMatrix_flipBit | 97–100 | N15,N30; private |
| 054 | evalPrimitiveCx_eq_controlledXBlock | 101–192 | N15,N30; private |
| 055 | compileUniformlyControlledRy | 193–217 | N16; public; binder-list correction F1 |
| 056 | uniformlyControlledRyMatrix | 218–240 | N17; public; binder-list correction F1 |
| 057 | compileUniformlyControlledRy_eval | 241–259 | N17; public |
| 058 | compileUniformlyControlledRy_eval_controlledRyBlockMatrix | 260–370 | N18; public |
| 059 | compileUniformlyControlledRy_ryCount | 371–386 | N19; public |
| 060 | compileUniformlyControlledRy_cxCount | 387–403 | N19; public |
| 061 | compileUniformlyControlledRy_oracleCalls_eq_zero | 404–411 | N20; public |
| 062 | compileUniformlyControlledRy_five_control_counts | 412–422 | N19,N20; public |

### CubicAmplitudePrimitive: C31-063–087, all public

| ID | Source name | Lines | Phase1 obligations |
| --- | --- | --- | --- |
| 063 | cubicN2ControlWires | 22–25 | N21,N22 |
| 064 | cubicN2ControlWires_ne_signal | 26–30 | N22 |
| 065 | cubicN2ControlIndex | 31–33 | N21,N24 |
| 066 | cubicN2Amplitude_abs_le_one | 34–43 | N21,N24 |
| 067 | cubicN2Angle | 44–49 | N22,N23 |
| 068 | cubicN2PrimitiveCircuit | 50–53 | N22 |
| 069 | cubicN2PrimitiveProgram | 54–58 | N22 |
| 070 | cubicN2PrimitiveCircuit_eval | 59–65 | N23 |
| 071 | cubicN2PrimitiveProgram_eval | 66–76 | N23 |
| 072 | cubicN2EncodeBits | 77–81 | N25 |
| 073 | cubicN2EncodeBits_signal | 82–85 | N25 |
| 074 | cubicN2ControlIndex_encode | 86–94 | N25 |
| 075 | cubicN2EncodeBits_context_eq_iff | 95–102 | N25 |
| 076 | cubicN2PrimitiveProgram_cleanEntry | 103–144 | N23,N25 |
| 077 | cubicN2PrimitiveFlatUnitary | 145–149 | N26,N27 |
| 078 | cubicN2PrimitiveFlatUnitary_unitary | 150–155 | N26,N27 |
| 079 | cubicN2PrimitiveCleanIndex | 156–158 | N25,N27 |
| 080 | cubicN2PrimitiveFlatUnitary_cleanBlock | 159–169 | N25,N27 |
| 081 | cubicN2ComplexTarget | 170–176 | N25,N27 |
| 082 | cubicN2PrimitivePresentation | 177–184 | N28 |
| 083 | cubicN2PrimitiveResource | 185–187 | N28 |
| 084 | cubicN2PrimitiveOperatorCandidate | 188–210 | N27,N28 |
| 085 | cubicN2PrimitiveVerifiedBlockEncoding | 211–220 | N27 |
| 086 | cubicN2Primitive_oracleCalls_eq_zero | 221–225 | N28 |
| 087 | cubicN2Primitive_resource_faithful | 226–230 | N28 |

N01–N03 are additionally instantiated by the actual semantics providers. N29–N31 remain source-topology/helper classification and open-consumer boundaries, not hidden extra target declarations. X00/X01/X02 from phase1 are unchanged. None of the 87 roots is silently excluded; private helpers are internal providers without invented external source credit. The eight private roots are exactly 044/045/046/050/051/052/053/054. Generated constructors, fields, recursors, equation lemmas, implicit universes and synthesized typeclass instances have not been inventoried by Lean.

## Binder and definition audit after reading actual source

There is no target-level `variable`, `universe`, local notation, section-wide typeclass or explicit instance command. The ambient commands are the observed namespaces/opens/imports and the two declaration-local maxHeartbeats settings. Imports remain a transitive trust boundary. The only explicit typeclass binders on target-local generic matrix lemmas are finite enumeration/decidable equality; their finite-type carrier roles are appropriate.

Visible logical guards are exactly source-described wire inequalities. In the final CCX program they are three pairwise inequalities; in intermediate context identities only two target inequalities; in the compiler every selected wire differs from target, with no control-control injection. No final cubic root adds bounds, normalization, PREPARE/SELECT, unitary or clean-entry premises. Counts are conclusions, not hypotheses. No RULED correction is authorized. No EXCESS hypothesis is found in the visible target source signatures; actual elaborated EXCESS status remains unverified.

Internal `MonomialProgram`, `PrimitiveRefinement`, and `PrimitiveProgramRefinement` carry real evaluation equalities. Their input proof fields are internal provider evidence, not logical premises of the final source Anchor. The author marks such fields SOURCE; that label must be read together with its internal-evidence policy, not as permission to expose producer results as public source hypotheses. The same applies to proof fields of the verified cubic wrapper. The constructor proof carried by `.twiceArccosRational` is supplied by C31-066; it does not add a bound premise to C31-076 or C31-085.

Literal definition classification is appropriate for the actual target definitions: no choice-based unique characterization, quotient, zero fallback or off-carrier invention was observed. The `.real` angle constructor is intentionally mathematical/non-numeric. The two arccos constructors include domain proofs, and the needed evaluator and half-add/sub identities are explicitly provided. No unique unitary dilation is claimed or required. Exact matrix representatives are fixed; no global-phase quotient is used. Presentation strings and arbitrary generic Props have their weaker roles as described in F4.

## Source topology versus actual static proof structure

The original phase1 source graph is preserved verbatim. The following are separately recorded source-code proof traces, not an elaborated dependency graph. Each brace is one complete AND tail. Calls visible inside the actual bodies and direct definitional reductions are distinguished from local induction hypotheses. These lists do not claim transitive kernel proof-term completeness.

    {literal H/T/Tdg lists, angle evaluator, phase evaluator,
     lift multiplication/scalar transport, local 2x2 identities}
       -> exact macro equalities C31-011/012/013.

    {finite monomial sum identity C31-015, program seq law,
     both input MonomialProgram.exact proofs}
       -> C31-023's produced exact equality.

    {literal middle C31-027, produced monomial equality,
     permutation identity C31-029, phase identity C31-030,
     ccz definition C31-031}
       -> C31-032.

    {H block lift C31-036, CCZ block C31-038,
     CCX block C31-040, H^2 C31-034, HZH C31-035,
     reindex/blockDiagonal multiplication, context activity cases}
       -> C31-041.

    {C31-028 literal composition, program seq semantics,
     C31-011, C31-032, C31-041}
       -> C31-042 -> produced refinement C31-043.

For the phase identity the implementation uses eight cases; phase1 also reconstructed the source-authorized XOR proof OR route. Both are sufficient local arithmetic proofs, not two independently verified compiler implementations.

    {literal compiler C31-055, recursive matrix C31-056,
     circuit append/evaluation law, base evaluation,
     two recursive evaluation induction hypotheses}
       -> C31-057.

    {independent spec C31-048, compiler C31-055,
     zero-control block C31-051,
     CX context block C31-054, exact half-angle helpers C31-044/045/046,
     exact-angle evaluator rules, Ry addition, X-Ry-X identity,
     reindex/block product laws, assignment reconstruction,
     two tail semantic induction hypotheses, both head-bit cases}
       -> C31-058 directly, without C31-057.

This direct implementation proof is a separate route from factoring first through C31-057 and a recursive-formula-to-spec theorem. The natural source describes both layers, and their narrative order is not evidence that the implementation invokes one inside the other.

    {literal compiler C31-055, list count definitions/additivity,
     base counts, two tail count induction hypotheses, elementary arithmetic}
       -> C31-059/C31-060 -> five-control conjunction C31-062.

    {primitive resource definition with oracle field zero}
       -> C31-061; no semantic or efficiency theorem is needed.

    {finite amplitude bound C31-066, literal arccos angle C31-067,
     literal controls/circuit C31-063/064/068,
     compiler spec theorem C31-058}
       -> C31-070; with zero global-phase evaluation -> C31-071.

    {C31-071, independent spec entry C31-049,
     signal encoding C31-072/073, decoded index C31-074,
     context iff C31-075, internally supplied finite bound,
     Ry-to-amplitudeRotation bridge, arccos clean entry,
     rational/real/complex casts, literal diagonal target}
       -> C31-076.

    {literal flat reindex C31-077, primitive-program unitary theorem,
     reindex_unitary provider}
       -> C31-078, independently of C31-076/C31-080.

    {literal flat reindex C31-077, clean index C31-079,
     explicit LE equivalence inverse laws, C31-076}
       -> C31-080.

    {literal candidate C31-084 with actual predicates,
     target C31-081 and normalizer=1, unitary theorem C31-078,
     flat clean-entry theorem C31-080}
       -> C31-085, with the full AND tail retained.

    {resource definition C31-083, program-resource definition}
       -> C31-087 by definitional equality.
    {primitive resource oracle-zero definition}
       -> C31-086.

C31-059/060 are not mathematical proof inputs to C31-085. The candidate does store presentation/resource values, but a count theorem is not a proof binder of the verified wrapper. CCX is nowhere a prerequisite of this finite cubic chain. The broader author import/ownership graph is only module-level source information; its absence of elaborated theorem edges is correctly disclosed. The compressed spine remains unpurified navigation, and all three conceptual transports remain non-certified. This review does not promote any of them to certified functors.

## Phase1 SOURCE_GAP reconciliation

| Original gap | What actual static reading establishes | What remains unverified |
| --- | --- | --- |
| SG1 exact angles | Actual constructors include rational/pi-rational/arccos/real/add/neg/scale; eval and half-add/sub lemmas have the required meanings. | Elaboration/axiom acceptance; numeric algorithm, precision, runtime and serialization are not supplied. |
| SG2 generic primitive unitary validity | CX carries a distinctness proof; basis actions/equivalences, unitary primitive evaluation, list composition and phase-unitary proofs are present and mathematically match. | Actual kernel/generated axiom closure and all transitive providers. |
| SG3 detailed LE encoding | Target encodings and context/index lemmas match; actual LE equivalence has the right forward/inverse direction and low-bit recurrence. | Native proof acceptance; no new compiled theorem of literal j+4s was produced in this review. |
| SG4 proof-carrying wrappers | Actual equality fields and concrete unitary/clean predicates are read, with theorem suppliers present. Generic Prop-data weakness retained. | Elaborated field types, generated names, actual proof terms/axioms and formal acceptance. |
| SG5 resource/presentation | Actual program resource ignores the global phase as expected; circuit resource is counts/oracle0/pure0/named-wire depth. Actual presentation drops angle data. | Executable refinement of presentation, angle-complete emitter, finite-bit preprocessing/synthesis and complete hardware costs. |

The broader open consumers N31 remain open, not refuted. Availability of provider sources is not evidence of a clean rebuild or transitive admission.

## Seven semantic slots after actual-source comparison

| Slot | Static source comparison | Boundary retained |
| --- | --- | --- |
| Target/normalization | H/T/Tdg/CCX exact; general controlled-Ry full matrix; finite D2 diagonal, normalizer 1. | No rank-one state loader or normalized cubic vector certificate. |
| Dimensions/scalars/basis | Complex finite matrices; real evaluated angles; named wires generic; 2 system + 1 signal and j+4s LE in finite cubic. | No implicit generic endianness or arbitrary-width cubic generalization. |
| Access/controls/inverses | Actual typed X/Ry/Rz/CX; exact inverse-T; target avoidance only for multiplexor; repeated controls allowed. | No free coherent arithmetic lookup or independent inconsistent tuple access. |
| Ancillas/workspace | Context bits preserved; signal wire2; zero extra pure ancillas; explicit clean-sector extraction. | Signal is not necessarily returned zero; no deterministic success claim. |
| Phase | Actual exp(i phi) program denotation and reverse chronological products; exact stored macro phases; cubic phase0. | No quotient-by-phase or truth-table-only certification. |
| Error/success | Exact symbolic equality/entries; ideal real arithmetic. | No numerical error budget, success/amplification or prepared-state normalization theorem. |
| Resources | Exact emitted-list exponential counts, zero opaque calls, concrete resource ownership; reference depth field exists. | No finite-bit/T synthesis, efficient preprocessing/storage, hardware routing or scalable Hermite/executable-family acceptance. |

## Actual reading and trust scope

Whole providers read in addition to the three targets:

- `$PROJECT/QuantumBlockEncoding/PrimitiveCircuit.lean`: all angle constructors/evaluators, typed gate validity, program constructors, counters and resource/depth definitions.
- `$PROJECT/QuantumBlockEncoding/PrimitiveSemantics.lean`: all primitive matrices, target/context splitting, evaluation laws, phase/unitarity/refinement definitions and proofs.
- `$PROJECT/QuantumBlockEncoding/PrimitiveRefinement.lean`: whole refinement type and resource interface.
- `$PROJECT/QuantumBlockEncoding/ReversibleClassical.lean`: whole CCX semantics and weaker guarded equivalence.
- `$PROJECT/QuantumBlockEncoding/PrimitiveBasisLE.lean`: whole LE equivalence, recursive formula and fixed-width helpers/proofs.
- `$PROJECT/QuantumBlockEncoding/Resources.lean`, `Circuit.lean`, `BlockEncoding.lean`: whole resource/presentation/certificate definitions, including arbitrary Prop fields and proof fields.

Selected provider ranges, not whole-provider mathematical review:

- `$PROJECT/QuantumBlockEncoding/Robin/ComplexLCU.lean`, lines 1–140 and 148–166: imports/context, explicit real rotation matrices and their unitary proofs, amplitudeRotation and clean-entry theorem, complete reindex_unitary proof, plus actual permutation-matrix definition/unitarity proof. The end of the first slice enters an unrelated blockDiagonal proof; its remainder is not claimed reviewed.
- `$PROJECT/QuantumBlockEncoding/CubicStatePreparation.lean`, lines 1–65 and 776–815: gridPoint/cubicAmplitude and nearby rank-one distinction; diagonal operator/exact normalizer/target definitions and namespace context. No whole-module or unrelated algorithm claim.
- `$PROJECT/QuantumBlockEncoding/Core.lean`, lines 1–65: finite matrix carrier and gridSize definitions/context; no claim to have reviewed the partial theorem that begins at the slice end or the rest of Core.

For all 25 author provider-index files, a mechanical byte read checked actual hashes and exact stored full-source copies; all match. This does not mean the reviewer semantically read all 25 or trusts their transitive proofs. The 11 providers above received whole/selected semantic reading. The other 14 provider files received only mechanical equality checks and necessary import/name scans where noted. External Mathlib source/trust, .lake contents, compiled artifacts and toolchain installation were not inspected.

Configuration whole reads: `$PROJECT/lean-toolchain`, `lakefile.lean`, `lake-manifest.json`. They prescribe Lean 4.33.0 and pinned dependencies, but have not been executed or independently matched to installed packages. Whole checker source read: `$PROJECT/website/scripts/check_research_publications.py`, hash `f8f6d7232376b5bc19a480b7e0ef549a5fafa8d66017e07482f7e6999962f8ad`, matching the metadata pin. Its source describes integrity/identity/path/binding checks, not mathematical equivalence. It was not run; its registry, source catalog and generated inventory inputs were not opened.

Metadata semantic reads: complete original private coverage and source freeze; all 87 effective binder/definition rows, recursively expanded bundle fields/manual policies, all 34 source paragraph dispositions and all 87 coverage link projections, all source AND/guarded-case records, and all four graph views. Repeated exact source blocks were byte-compared to already-read actual modules instead of redundantly treated as independent evidence. Effective formal context was parsed for targets/87 inventory/ambient scope/provider index/config context and exact source-copy equality; embedded provider text outside the read scope above is not claimed cognitively reviewed. Metadata-freeze, output-manifest and supplement were used only for scoped pins/schema, not for accepting claims about other artifacts. Producer source slices actually read were lines 57–87 and 126–147, plus lexical-search hits for binder/header/field extraction, to diagnose F1 and field-extraction precision; no whole-producer reading, producer execution or verifier execution is claimed.

No handoff, verifier selftest, author decoder packet, decoder output, other reviewer or sibling result, CI/build/cache/runtime/native evidence, .lake package source, other chats, registry or source catalog content was read. No Lean, Git, network, subagents, canonical writes or checker admission was performed. The earlier parent report that its verifier exited zero is not semantic evidence in this review. Hash checks and JSON/source-text inspection are the only mechanical actions used.

## Handoff and mandatory stop

Static result: source identities reconstructed in phase1 remain mathematically matched by the read target text, with F1/F2 audit precision corrections, F3 graph granularity refinements, and F4/F5 trust boundaries. This is an inspection report, not an accepted source/formal round trip. No source theorem or implementation has been repaired, weakened, admitted or retired. Failure class NONE for the abstract mathematics; metadata audit omissions are recorded, and formal evidence remains pending.

Salvage: existing phase1 macro/monomial/context/count/encoding derivations and this narrower source mapping are candidate reusable evidence, not admitted library fragments. Process-memory IDs: none. Direction fingerprint: original-phase1-preserving whole-target static semantic/binder/definition/topology comparison, with bounded provider reads. Children: none. Common-blind-spot/decoder comparison: not performed. Verified default route: none selected. Purification/Exposition Seal: not performed.

Only new files `$REVIEWER/phase2-static-report.md`, `phase2-publicsafe-allowlist.json`, and `phase2-static-seal.json` are written. The allowlist classifies permitted report artifacts for a possible later export; it is not publication authorization. Hash them, verify original phase1/source pins again, and STOP. Any later actual formal comparison, decoder bridge, generated-signature/axiom inspection, compilation, native check, admission or publication requires a separate grant.
