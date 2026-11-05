# Author-private whole-source coverage: cubic legacy module

Role: retrospective source author, not source-blind decoder, source-first
reviewer, historical formalizer, compiler witness, or publication approver.
Only the separately frozen `source-only.md` is suitable as the natural-only
first input to an independent source-first reviewer. This file intentionally
contains implementation names and may not be sent in that first phase.

## Scope and inventory method

The entire target `QuantumBlockEncoding/CubicStatePreparation.lean` was read
in consecutive ranges 1–410, 411–830, 831–1230, 1231–1680, 1681–2130,
2131–2580, 2581–3030, 3031–3480, 3481–3930, 3931–4148.
This includes proof bodies, doc comments, all private support declarations,
all namespaces, record fields, opaque predicates and literal candidate data.
The independently recomputed lexical inventory has 319 explicit named source
declarations: 269 public and 50 private. These are source counts, not an
elaborated compiler environment, generated-declaration count, compilation
result, axiom audit or independent review. Comment text beginning `theorem`
or `open` is not a command and is excluded. In particular line 3089 is prose,
not a named theorem. No anonymous theorem/example is present.

The table below enumerates every explicit name, full namespace, declaration
extent and exact source header. Declaration extent ends before the next named
declaration and may include an intervening comment. It is a navigational span,
not a claim that every next comment belongs to the earlier proof. Exact
headers are extracted only after the complete human source reading; the
mathematical source was not produced by counting wrappers.

## Ambient audit

There are exactly two direct imports: the project block-encoding classics
module, and Mathlib's four-squares module. Project import chain is
BlockEncodingClassics → BlockEncoding → Circuit → Resources → Core → Std.
No scoped variable, section variable, local notation, local instance,
set-option override, axiom command, `sorry` or `admit` appears in this target.
This is lexical observation, not a transitive trust/axiom certificate.
The namespaces are QuantumBlockEncoding, its sibling subnamespaces
CubicStatePreparation and CubicDiagonalOracle, and nested namespaces
LinearDiagonalInputBEContract and CubicQSVTExternalSemantics. The latter two
are reopened solely for methods before closing; all names are qualified in
the table. Universes `u` and `v` occur in generic finite-list helpers as
auto-implicit type universes, not as mathematical nonemptiness premises.

All matrix notation is the project function-matrix API, not Mathlib's bundled
linear operator. Scalar Rat has total division. Fin carriers carry their
range certificates; when a register size is `gridSize n`, positivity is proved
from `2^n>0`. Input `n : Nat` is not accompanied by a positivity binder even
when historical descriptive strings say `n positive`. The natural source
explicitly records the n=0 extension and forbids normalizing its zero vector.

## Binder classification rules (applied to each exact table header)

TYPING: natural sizes/dimensions/precision/count parameters; finite indices;
generic carriers and equality/BEq/LawfulBEq infrastructure; matrix/vector/list
data; embeddings and backend/scalar-tier *data* as such. These do not alone
assert a physical register representation or any semantic proposition.

STANDING: exact rational arithmetic, finite column-vector matrix products,
identity entries, finite enumerations and the documented flattening convention.
They are spelled out in S01/S04/S05 rather than hidden typeclass premises.

SOURCE: each explicit logical premise in a *conditional local mathematical
lemma*, or each asserted field in a supplied *interface* (unit norm, nontrivial
coordinate, source coordinate identity, clean-block equality, approximation
bound, circuit-semantic supplier, finite list membership/nodup/support).
SOURCE here means premise of the displayed local conditional source statement,
not an original user premise of the unconditional O/D construction request.
The exact headers below preserve every such premise. Consuming a proved
dependency must remain a dependency, not be smuggled into a final O/D binder.

RULED: none used; no human-approved correction was manufactured.
EXCESS: no final unconditional physical O/D theorem is claimed. Promoting the
conditional clean-block, backend bridge, primitive contract, arbitrary error
relation or QSVT supplier as an unconditional user-target theorem would create
EXCESS premises and is rejected. The present source presents these as
conditional interfaces with explicit missing producers. This author file is
not an accepted binder/Statement Seal for a future stronger target.

## Seven-slot profiles

Every table row has one source region below; that profile supplies the seven
semantic slots and boundary once, avoiding 319 duplicated paragraphs. The
exact header supplies the row-specific parameters and guards. A pure helper
inherits the profile of its actual consumer; no gate/phase claim is inferred
from an arithmetic profile.

| Source region | Target/normalization | Carriers/order | Access/inverses | Ancilla/garbage | Phase | Error/success | Resources/boundary |
|---|---|---|---|---|---|---|---|
| S01 | O=first-column a, D=diag(a), X=diag(x); scales N/1 | Rat, N=2^n, n≥0, column convention | data only | no circuit inferred | exact signed entries | unnormalized O; normalized n=0 excluded | target strings not acceptance |
| S02 | squared norm ≤N≤N² and threshold j³ | finite lists, j<N, m/k with k≤m | enumeration/counting, not an oracle | none claimed | nonnegative exact Rat | exact arithmetic; three finite norm diagnostics | no asymptotic/bit complexity |
| S03 | alpha B=O under both first/off-column clauses | same N; output row distinct input col | 7/10/8 uninterpreted labels; dagger syntax not inverse proof | one signal, explicit pure budgets; persistent nonzero-column reject | Hadamard phases unproved | epsilon target not achieved by transcript | label tuples only; physical denotation OPEN |
| S04 | H00=v0 and H orthogonal | Rat^8, ordered 0..7 | literal H; d≠0 from unit and v0≠1 | matrix 8D support only | exact signed real entries | no approximation | formula/inner-product theorem, not gate synthesis |
| S05 | direct-sum orthogonality and diag(q) clean block | ancilla×system, q=bN+s, quotient/remainder inverse | supplied branch vectors | clean embedding (0,s), three ancilla matrix qubits; no workspace circuit | all branches exact, no label-phase quotient | exact conditional clean block | fiber permutation proofs; branch synthesis OPEN |
| S06 | existence of X/D rational dilation at scale1 | residual N²-j² or N⁶-j⁶, four Nat squares, Rat^8 | noncanonical chosen witness | specific embed clean; generic cleanup Prop is arbitrary | chosen branch signs; no global-phase quotient | exact matrix equality | one oracle label not deterministic producer/gates |
| S07 | X³=D, clean-matrix product; optional supplied QSVT output | finite diagonal products | exact payload forgetting; external supplier AND-tail | product circuit ancillas not constructed | QSVT phases externally unsupplied | exact algebra; only actual-grid bound local | product/QSVT physical/resource theorem OPEN |
| S08 | diag(q) vs D, squared Euclidean induced error | Rat^m, includes m=0 | supplied q/epsilon and optional abstract relation | no physical implementation | signed error squared | epsilon≥0 and all-vector inequality; non-vacuity witness | no producer/complex extension/finitary synthesis |
| S09 | conditional primitive diag(a), scale1 | opaque Rat matrix dimension2^(n+1) | opaque unitary/extraction assumption; no implementation | one signal/no pure layout, propositions unexpanded | none certified by opaque naming | exact only if full supplied contract | one label (1,1,1,1); no gate certificate |
| S10 | clean-input cubic computation and scalar law | arbitrary W or finite payload 2^(3n); arbitrary Scalar | overwrite backend; opaque-route bridge is conclusion-equivalent | finite payload vs symbolic infinite Rat separated | scalar-tier functions not enforced Ry/cos | exact pointwise value law only | declared qubit count alone not representation/cost |
| S11 | modular compute/uncompute and linear value support | finite M=2^(3n) or N, includes M=1 | one inverse direction field, modular add/sub actual formulas | preserves index, restores dirty workspace after compute; readonly signal law incomplete | no superposition/Ry semantics from signal function | exact arithmetic cleanup, no full route | multiplication/adders and readonly composition OPEN |
| S12 | expanded five-conjunct conditional diagonal interface | N and parameterized workspace | transparent compute/angle + opaque cleanup/extraction + target equality | transparent cleanup not opaque cleanup; no unitary field | actual rotation semantics OPEN | extracting target premise not independent root | no family executable/gate resource closure |
| S13 | descriptive policy/claim strings | Nat/List/Bool/Rat data | no mathematical access supplied | declared layouts only | no phase assertion | epsilon ladder/history not success | scorer label accounting; not controller-run evidence |

## Definition audit and expanded bundled contracts

Literal definitions include grid/amplitude/operator/norm formulas, finite
folds, deltas, branch vectors, direct sums, payload readers and modular maps.
Their exact domains and zero-dimensional/zero-denominator behavior are in
S01/S04/S08/S11. `householder8` is a total rational formula whose meaningful
reflection claims require its stated guard; there is no silently canonical
completion off that locus. `ratAbs` is literal sign splitting, not opaque.

Literal proposition aliases and structures are *interface definitions*, not
proved existence of inhabitants. The source expands them, especially:

- `rankOneCleanBlockContract`: scaled first column AND all other columns zero.
- `LinearDiagonalInputBEContract`: U, embed, rational orthogonality; arbitrary
  cleanup Prop/description/proof; equality to X; scale-one equality; Resource;
  arbitrary resource Prop/proof. No injective-embed field, circuit, or
  denotation/resource connection exists in this generic record.
- `LinearDiagonalRationalCompletion` and `CubicDiagonalRationalCompletion`:
  existence of a branch vector family AND unit norm on each branch AND exact
  clean coordinate. These are not efficient algorithms or unique objects.
- `DiagonalRatOperatorNormBridge`: arbitrary ternary error relation plus the
  diagonal-entrywise implication for that relation. The concrete Euclidean
  instance is independently defined and proved by the source argument S08.
- `CubicDiagonalExactBEContract`: exactPayload, orthogonality of payload.U,
  scale-one equality, arbitrary cleanup Prop/proof, Resource, arbitrary
  resource Prop/proof. Generic payload.A is not constrained to D. The specific
  Householder constructor and its separate clean-target theorem do constrain it.
- `CubicQSVTLocalSideConditions`: degree with equality to3; parity Bool with
  equality to true; bound only on input grid spectrum. The labels are not
  certified degree/parity laws of a generic polynomial representation.
- `CubicQSVTExternalSemantics`: certified input; output exact payload;
  orthogonal output.U; output.A equal to X³; arbitrary global admissibility
  Prop/description/proof; arbitrary cleanup Prop/description/proof; Resource
  and arbitrary resource Prop/proof. Its consumer is conditional, not QSVT.
- `primitiveAmplitudeOracleSemanticContract`: opaque unitarity AND exists
  block with opaque extraction AND literal diagonal target entries.
- `StandardRyCleanEntryScalarTier`: arbitrary Scalar/embedding/angle/entry
  functions and range law; descriptive formula strings default to arccos/cos
  but no fields enforce them or injectivity of the rational embedding.
- `ExpandedCubicArithmeticBackend` and `LinearDiagonalValueBackend`: W,
  declared count/equality, zero, reader, compute function. W cardinality and
  invertibility are not fields; symbolic Rat overwrite is not a finite register.
- `expandedArithmeticBackendComputesCubicAmplitude` and linear counterpart:
  count equality AND for every clean system input, output index preserved AND
  reader gives the target value. Nothing asserts dirty-input reversibility.
- Arithmetic/rotation backend bridges: implication from a known backend/scalar
  proposition to the opaque route predicate. Their iff lemmas are normal-form
  reductions, not witnesses of the opaque conclusion.
- `ExpandedControlledRyWorkspaceReadonlyWitness`: backend, transparent angle
  proposition, basis function on j/W/Fin2, preserves j and W; no prescribed
  signal output or amplitude/linearity/unitarity law.
- Cubic and linear clean-uncompute witness structures: backend, clean compute
  proof, computeStep, uncomputeStep, clean-input agreement, both preserve index,
  uncompute-after-compute for all W. No compute-after-uncompute field. Comments
  saying two-sided cleanup must not strengthen that actual signature.
- `expandedAmplitudeOracleCleanBlockContract`: transparent compute AND
  transparent universal angle law AND opaque route cleanup AND opaque
  extraction AND the desired diagonal contract. No unitary field, no mandatory
  readonly witness, no link selecting one common backend between conjuncts.

The two noncomputable Householder package definitions choose representatives
from existence, not unique characterized objects. Their clean blocks are
independent of the chosen residual-square representatives, but no stronger
matrix/circuit invariance is claimed. The noncomputable cubic product package
inherits this chosen input; its product is at the extracted matrix arithmetic
layer only. No quotient construction or representative modulo phase is used.
Opaque matrix/predicate declarations remain unspecified, not literal physical
semantics; no witness is manufactured here.

## Source proof topology and stronger-consumer gaps

The natural source deliberately compresses repeated sum/finite-index proofs.
S04 contains delta/bilinearity/eight-coordinate reasoning for 11 private
reflection helpers; S05 contains all private index/fiber/list permutation and
zero-filter/congruence helpers. S08 independently gives the repeated generic
zero/unique/monotone-fold argument for error transport. S07 covers the three
private diagonal-product leaves. S11 covers the private modular arithmetic
guard split. Every helper has its own name and exact signature in the table,
but no extra claimed quantum primitive is generated for a wrapper.

All source routes and OPEN stronger-consumer nodes are explicit in S12.
Physical alternatives are OR routes with full AND tails, not independently
sufficient arrows from an isolated coefficient/norm/cleanup leaf. Source
topology here is AUTHOR-PROVISIONAL; a fresh source-first reviewer must
derive and freeze its own natural-only topology before formal comparison.
No theorem-dependency extractor or independently reviewed graph is claimed.

## Observed prose/source drift and exclusions

The current task prose describes a five-rung decade ladder, but the actual
module defines three rungs [1e-10,1e-8,1e-6]. S13 describes the module literally
and does not silently reconcile or rewrite either original. Several comments
near the four-square support still call it external/open despite the later
unconditional imported-theorem existence proof. The current source of truth
for that mathematical existence is the actual proof, while its algorithmic
cost is still open. Strong words such as `complete`, `unitary`, `two-sided`,
`QSVT` and `resource` in names/comments do not strengthen actual definitions.
The natural source corrects overinterpretation without changing the code or
the frozen scientific task.

Task IDs, policy schedules, expected phase and construction-claim strings are
NODEs in S13 as historical data, EXCLUDED from scientific-success evidence.
Imported unrelated sparse/permutation/Chebyshev primitives are not attributed
as cubic theorem dependencies merely because they share a module import.
No historical decoder/reviewer artifact was sought or read; the task and
conversion-window text include workflow instructions and old status prose,
which were not accepted as independent verdicts or build evidence. A combined
conversion-window read exceeded the output limit, so it is recorded as partial,
not whole-source reading of either window. The natural task target sections
were subsequently read in bounded calls. Two shell glob searches for provider
locations were rejected by Windows rg path handling; direct known-file reads
then supplied the actual provider definitions. Neither diagnostic executed Lean
or altered any source.

## Per-declaration lossless table

The following mechanically transcribed rows are subordinate to the manual
source/binder/definition analysis above. They do not self-approve a publication.
| # | Qualified source name | Visibility/kind | Source lines | Natural region | Exact source header (binder data) |
|---|---|---|---|---|---|
| 1 | `QuantumBlockEncoding.CubicStatePreparation.taskId` | public def | 25–27 | S01 | `def taskId : String` |
| 2 | `QuantumBlockEncoding.CubicStatePreparation.requestedEpsilon` | public def | 28–30 | S01 | `def requestedEpsilon : Rat` |
| 3 | `QuantumBlockEncoding.CubicStatePreparation.gridPoint` | public def | 31–34 | S01 | `def gridPoint (n : Nat) (j : Fin (gridSize n)) : Rat` |
| 4 | `QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude` | public def | 35–42 | S01 | `def cubicAmplitude (n : Nat) (j : Fin (gridSize n)) : Rat` |
| 5 | `QuantumBlockEncoding.CubicStatePreparation.cubicOperator` | public def | 43–50 | S01 | `def cubicOperator (n : Nat) : Matrix (gridSize n) (gridSize n) Rat` |
| 6 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq` | public def | 51–59 | S01 | `def cubicNormSq (n : Nat) : Rat` |
| 7 | `QuantumBlockEncoding.CubicStatePreparation.conservativeNormalizer` | public def | 60–63 | S01 | `def conservativeNormalizer (n : Nat) : Rat` |
| 8 | `QuantumBlockEncoding.CubicStatePreparation.cubicTarget` | public def | 64–76 | S01 | `def cubicTarget (n : Nat) : QueryOperatorTarget Rat (gridSize n) (gridSize n)` |
| 9 | `QuantumBlockEncoding.CubicStatePreparation.defaultRequiredCost` | public def | 77–88 | S13 | `def defaultRequiredCost : BlockEncodingCost` |
| 10 | `QuantumBlockEncoding.CubicStatePreparation.defaultPolicy` | public def | 89–99 | S13 | `def defaultPolicy : AdaptiveBlockEncodingPolicy Rat` |
| 11 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicDefaultPrecision` | public def | 100–109 | S03 | `def arithmeticCubicDefaultPrecision : Nat` |
| 12 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicLayout` | public def | 110–121 | S03 | `def arithmeticCubicLayout (n precision : Nat) : RegisterLayout` |
| 13 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicCircuit` | public def | 122–132 | S03 | `def arithmeticCubicCircuit (_n _precision : Nat) : Circuit` |
| 14 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResource` | public def | 133–136 | S03 | `def arithmeticCubicResource (n precision : Nat) : Resource` |
| 15 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicNormalizer` | public def | 137–140 | S03 | `def arithmeticCubicNormalizer (n : Nat) : Rat` |
| 16 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicCost` | public def | 141–146 | S03 | `def arithmeticCubicCost (n precision : Nat) : BlockEncodingCost` |
| 17 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResourceTuple` | public def | 147–154 | S03 | `def arithmeticCubicResourceTuple (n precision : Nat) : Nat × Nat × Nat × Nat` |
| 18 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResource_eq` | public theorem | 155–160 | S03 | `theorem arithmeticCubicResource_eq (n precision : Nat) : arithmeticCubicResource n precision = Resource.ofCountsWithDepth 0 0 7 0 7` |
| 19 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicLayout_auxiliaryQubits` | public theorem | 161–169 | S03 | `theorem arithmeticCubicLayout_auxiliaryQubits (n precision : Nat) : (arithmeticCubicLayout n precision).auxiliaryQubits = 1 + (3 * n + precision + 2)` |
| 20 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicClaim` | public def | 170–191 | S03 | `def arithmeticCubicClaim : ConstructionClaim` |
| 21 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicLayout` | public def | 192–205 | S03 | `def arithmeticRankOneCubicLayout (n precision : Nat) : RegisterLayout` |
| 22 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCircuit` | public def | 206–213 | S03 | `def arithmeticRankOneCubicCircuit (n precision : Nat) : Circuit` |
| 23 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResource` | public def | 214–217 | S03 | `def arithmeticRankOneCubicResource (n precision : Nat) : Resource` |
| 24 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicNormalizer` | public def | 218–221 | S03 | `def arithmeticRankOneCubicNormalizer (n : Nat) : Rat` |
| 25 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCost` | public def | 222–227 | S03 | `def arithmeticRankOneCubicCost (n precision : Nat) : BlockEncodingCost` |
| 26 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResourceTuple` | public def | 228–236 | S03 | `def arithmeticRankOneCubicResourceTuple (n precision : Nat) : Nat × Nat × Nat × Nat` |
| 27 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResource_eq` | public theorem | 237–242 | S03 | `theorem arithmeticRankOneCubicResource_eq (n precision : Nat) : arithmeticRankOneCubicResource n precision = Resource.ofCountsWithDepth 0 0 10 0 10` |
| 28 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicLayout_auxiliaryQubits` | public theorem | 243–248 | S03 | `theorem arithmeticRankOneCubicLayout_auxiliaryQubits (n precision : Nat) : (arithmeticRankOneCubicLayout n precision).auxiliaryQubits = 1 + ((arithmeticCubicLayout n precision).pureAncillas + n + 1)` |
| 29 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResourceTuple_n2_default` | public theorem | 249–257 | S03 | `theorem arithmeticRankOneCubicResourceTuple_n2_default : arithmeticRankOneCubicResourceTuple 2 arithmeticCubicDefaultPrecision = (10, 10, 52, 10)` |
| 30 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicClaim` | public def | 258–279 | S03 | `def arithmeticRankOneCubicClaim : ConstructionClaim` |
| 31 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicWorkspace` | public def | 280–290 | S03 | `def hadamardCountingCubicWorkspace (n : Nat) : Nat` |
| 32 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicLayout` | public def | 291–304 | S03 | `def hadamardCountingCubicLayout (n : Nat) : RegisterLayout` |
| 33 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCircuit` | public def | 305–321 | S03 | `def hadamardCountingCubicCircuit (_n : Nat) : Circuit` |
| 34 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCircuit_rejectSignalRepair` | public theorem | 322–335 | S03 | `theorem hadamardCountingCubicCircuit_rejectSignalRepair (n : Nat) : hadamardCountingCubicCircuit n = [ Gate.oracleCall "hcount-zero-input-flag" , Gate.oracleCall "hcount-nonzero-column-reject" , Gate.oracleCall "hcount-path-H-on-R-T" , Gate.oracleCall "hcount-row-xor-R-into-system" , Gate.oracleCall "hcount-cubic-threshold-compare" , Gate.oracleCall "(hcount-cubic-threshold-compare)^dagger" , Gate.oracleCall "hcount-path-H-on-R-T" , Gate.oracleCall "(hcount-zero-input-flag)^dagger" ]` |
| 35 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResource` | public def | 336–339 | S03 | `def hadamardCountingCubicResource (n : Nat) : Resource` |
| 36 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicNormalizer` | public def | 340–343 | S03 | `def hadamardCountingCubicNormalizer (n : Nat) : Rat` |
| 37 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCost` | public def | 344–349 | S03 | `def hadamardCountingCubicCost (n : Nat) : BlockEncodingCost` |
| 38 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResourceTuple` | public def | 350–357 | S03 | `def hadamardCountingCubicResourceTuple (n : Nat) : Nat × Nat × Nat × Nat` |
| 39 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResource_eq` | public theorem | 358–363 | S03 | `theorem hadamardCountingCubicResource_eq (n : Nat) : hadamardCountingCubicResource n = Resource.ofCountsWithDepth 0 0 8 0 8` |
| 40 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicLayout_auxiliaryQubits` | public theorem | 364–369 | S03 | `theorem hadamardCountingCubicLayout_auxiliaryQubits (n : Nat) : (hadamardCountingCubicLayout n).auxiliaryQubits = 1 + (1 + 4 * n + hadamardCountingCubicWorkspace n)` |
| 41 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResourceTuple_n2` | public theorem | 370–377 | S03 | `theorem hadamardCountingCubicResourceTuple_n2 : hadamardCountingCubicResourceTuple 2 = (8, 8, 21, 8)` |
| 42 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicClaim` | public def | 378–400 | S03 | `def hadamardCountingCubicClaim : ConstructionClaim` |
| 43 | `QuantumBlockEncoding.CubicStatePreparation.hardModeUpperAgentSchedule` | public def | 401–402 | S13 | `def hardModeUpperAgentSchedule : List Nat` |
| 44 | `QuantumBlockEncoding.CubicStatePreparation.hardModeMiddleAgentSchedule` | public def | 403–404 | S13 | `def hardModeMiddleAgentSchedule : List Nat` |
| 45 | `QuantumBlockEncoding.CubicStatePreparation.hardModeLowerAgentSchedule` | public def | 405–407 | S13 | `def hardModeLowerAgentSchedule : List Nat` |
| 46 | `QuantumBlockEncoding.CubicStatePreparation.hardModeExactStallWindow` | public def | 408–413 | S13 | `def hardModeExactStallWindow : Nat` |
| 47 | `QuantumBlockEncoding.CubicStatePreparation.hardModeConstructionStallWindow` | public def | 414–416 | S13 | `def hardModeConstructionStallWindow : Nat` |
| 48 | `QuantumBlockEncoding.CubicStatePreparation.hardModeLevelCycleBudget` | public def | 417–424 | S13 | `def hardModeLevelCycleBudget : List Nat` |
| 49 | `QuantumBlockEncoding.CubicStatePreparation.relaxedEpsilonLadder` | public def | 425–427 | S13 | `def relaxedEpsilonLadder : List Rat` |
| 50 | `QuantumBlockEncoding.CubicStatePreparation.relaxedEpsilonLadder_startsWithRequested` | public theorem | 428–431 | S13 | `theorem relaxedEpsilonLadder_startsWithRequested : relaxedEpsilonLadder.head? = some requestedEpsilon` |
| 51 | `QuantumBlockEncoding.CubicStatePreparation.hardModeSchedules_have_four_levels` | public theorem | 432–438 | S13 | `theorem hardModeSchedules_have_four_levels : hardModeUpperAgentSchedule.length = 4 ∧ hardModeMiddleAgentSchedule.length = 4 ∧ hardModeLowerAgentSchedule.length = 4 ∧ hardModeLevelCycleBudget.length = 4` |
| 52 | `QuantumBlockEncoding.CubicStatePreparation.hardModeLowerAgentSchedule_final` | public theorem | 439–447 | S13 | `theorem hardModeLowerAgentSchedule_final : hardModeLowerAgentSchedule.getLast? = some 6` |
| 53 | `QuantumBlockEncoding.CubicStatePreparation.initialExpectedPhase` | public def | 448–450 | S13 | `def initialExpectedPhase : BlockEncodingSearchPhase` |
| 54 | `QuantumBlockEncoding.CubicStatePreparation.gridSize_pos` | public theorem | 451–453 | S01 | `theorem gridSize_pos (n : Nat) : 0 < gridSize n` |
| 55 | `QuantumBlockEncoding.CubicStatePreparation.cubicOperator_first_column` | public theorem | 454–457 | S01 | `theorem cubicOperator_first_column (n : Nat) (row : Fin (gridSize n)) : cubicOperator n row ⟨0, gridSize_pos n⟩ = cubicAmplitude n row` |
| 56 | `QuantumBlockEncoding.CubicStatePreparation.cubicOperator_only_first_column` | public theorem | 458–470 | S01 | `theorem cubicOperator_only_first_column (n : Nat) (row col : Fin (gridSize n)) (h : col.val ≠ 0) : cubicOperator n row col = 0` |
| 57 | `QuantumBlockEncoding.CubicStatePreparation.rankOneCleanBlockContract` | public def | 471–477 | S03 | `def rankOneCleanBlockContract (n : Nat) (alpha : Rat) (block : Matrix (gridSize n) (gridSize n) Rat) : Prop` |
| 58 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCleanBlockContract` | public def | 478–485 | S03 | `def arithmeticRankOneCubicCleanBlockContract (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) : Prop` |
| 59 | `QuantumBlockEncoding.CubicStatePreparation.rankOneCleanBlockContract_pointwise_eq` | public theorem | 486–505 | S03 | `theorem rankOneCleanBlockContract_pointwise_eq {n : Nat} {alpha : Rat} {block : Matrix (gridSize n) (gridSize n) Rat} (h : rankOneCleanBlockContract n alpha block) : Matrix.PointwiseEq (fun row col => alpha * block row col) (cubicOperator n)` |
| 60 | `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCleanBlockContract_pointwise_eq` | public theorem | 506–514 | S03 | `theorem arithmeticRankOneCubicCleanBlockContract_pointwise_eq {n : Nat} {block : Matrix (gridSize n) (gridSize n) Rat} (h : arithmeticRankOneCubicCleanBlockContract n block) : Matrix.PointwiseEq (fun row col => arithmeticRankOneCubicNormalizer n * block row col) (cubicOperator n)` |
| 61 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCleanBlockContract` | public def | 515–522 | S03 | `def hadamardCountingCubicCleanBlockContract (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) : Prop` |
| 62 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCleanBlockContract_pointwise_eq` | public theorem | 523–530 | S03 | `theorem hadamardCountingCubicCleanBlockContract_pointwise_eq {n : Nat} {block : Matrix (gridSize n) (gridSize n) Rat} (h : hadamardCountingCubicCleanBlockContract n block) : Matrix.PointwiseEq (fun row col => hadamardCountingCubicNormalizer n * block row col) (cubicOperator n)` |
| 63 | `QuantumBlockEncoding.CubicStatePreparation.rat_cube_sq_eq_sixth` | public theorem | 531–537 | S02 | `theorem rat_cube_sq_eq_sixth (x : Rat) : (x ^ 3) ^ 2 = x ^ 6` |
| 64 | `QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_sq_eq_gridPoint_sixth` | public theorem | 538–542 | S02 | `theorem cubicAmplitude_sq_eq_gridPoint_sixth (n : Nat) (j : Fin (gridSize n)) : cubicAmplitude n j ^ 2 = gridPoint n j ^ 6` |
| 65 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_sixthPowerFold` | public theorem | 543–549 | S02 | `theorem cubicNormSq_sixthPowerFold (n : Nat) : cubicNormSq n = (List.finRange (gridSize n)).foldl (fun acc j => acc + gridPoint n j ^ 6) 0` |
| 66 | `QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_ne_zero` | public theorem | 550–554 | S02 | `theorem gridSize_rat_ne_zero (n : Nat) : (gridSize n : Rat) ≠ 0` |
| 67 | `QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_pos` | public theorem | 555–559 | S02 | `theorem gridSize_rat_pos (n : Nat) : (0 : Rat) < (gridSize n : Rat)` |
| 68 | `QuantumBlockEncoding.CubicStatePreparation.rat_div_cube_div_eq` | public theorem | 560–570 | S02 | `theorem rat_div_cube_div_eq (a b : Rat) : (a / b) ^ 3 / b = a ^ 3 / b ^ 4` |
| 69 | `QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_div_conservativeNormalizer_eq` | public theorem | 571–578 | S02 | `theorem cubicAmplitude_div_conservativeNormalizer_eq (n : Nat) (j : Fin (gridSize n)) : cubicAmplitude n j / conservativeNormalizer n = (j.val : Rat) ^ 3 / (gridSize n : Rat) ^ 4` |
| 70 | `QuantumBlockEncoding.CubicStatePreparation.gridSize_three_mul_eq_cube` | public theorem | 579–584 | S02 | `theorem gridSize_three_mul_eq_cube (n : Nat) : gridSize (3 * n) = gridSize n ^ 3` |
| 71 | `QuantumBlockEncoding.CubicStatePreparation.gridSize_four_mul_eq_fourth` | public theorem | 585–595 | S02 | `theorem gridSize_four_mul_eq_fourth (n : Nat) : gridSize (4 * n) = gridSize n ^ 4` |
| 72 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdCountP_finRange` | public theorem | 596–624 | S02 | `theorem hadamardCountingCubic_thresholdCountP_finRange (m k : Nat) (hk : k ≤ m) : List.countP (fun t : Fin m => t.val < k) (List.finRange m) = k` |
| 73 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdFilterLength` | public theorem | 625–631 | S02 | `theorem hadamardCountingCubic_thresholdFilterLength (m k : Nat) (hk : k ≤ m) : ((List.finRange m).filter (fun t => t.val < k)).length = k` |
| 74 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_threshold_le_pathCapacity` | public theorem | 632–644 | S02 | `theorem hadamardCountingCubic_threshold_le_pathCapacity (n : Nat) (j : Fin (gridSize n)) : j.val ^ 3 <= gridSize (3 * n)` |
| 75 | `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdPathCount` | public theorem | 645–652 | S02 | `theorem hadamardCountingCubic_thresholdPathCount (n : Nat) (j : Fin (gridSize n)) : ((List.finRange (gridSize (3 * n))).filter (fun t => t.val < j.val ^ 3)).length = j.val ^ 3` |
| 76 | `QuantumBlockEncoding.CubicStatePreparation.gridPoint_nonneg` | public theorem | 653–661 | S02 | `theorem gridPoint_nonneg (n : Nat) (j : Fin (gridSize n)) : (0 : Rat) ≤ gridPoint n j` |
| 77 | `QuantumBlockEncoding.CubicStatePreparation.gridPoint_lt_one` | public theorem | 662–668 | S02 | `theorem gridPoint_lt_one (n : Nat) (j : Fin (gridSize n)) : gridPoint n j < 1` |
| 78 | `QuantumBlockEncoding.CubicStatePreparation.gridPoint_le_one` | public theorem | 669–672 | S02 | `theorem gridPoint_le_one (n : Nat) (j : Fin (gridSize n)) : gridPoint n j ≤ 1` |
| 79 | `QuantumBlockEncoding.CubicStatePreparation.rat_pow_le_one_of_nonneg_le_one` | public theorem | 673–686 | S02 | `theorem rat_pow_le_one_of_nonneg_le_one (x : Rat) (k : Nat) (hx0 : 0 ≤ x) (hx1 : x ≤ 1) : x ^ k ≤ 1` |
| 80 | `QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_sq_le_one` | public theorem | 687–692 | S02 | `theorem cubicAmplitude_sq_le_one (n : Nat) (j : Fin (gridSize n)) : cubicAmplitude n j ^ 2 ≤ 1` |
| 81 | `QuantumBlockEncoding.CubicStatePreparation.foldl_add_le_add_length` | public theorem | 693–718 | S02 | `theorem foldl_add_le_add_length {α : Type u} (xs : List α) (f : α → Rat) (h : ∀ x, x ∈ xs → f x ≤ 1) (acc : Rat) : xs.foldl (fun acc x => acc + f x) acc ≤ acc + (xs.length : Rat)` |
| 82 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_gridSize` | public theorem | 719–730 | S02 | `theorem cubicNormSq_le_gridSize (n : Nat) : cubicNormSq n ≤ (gridSize n : Rat)` |
| 83 | `QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_le_sq` | public theorem | 731–742 | S02 | `theorem gridSize_rat_le_sq (n : Nat) : (gridSize n : Rat) ≤ (gridSize n : Rat) ^ 2` |
| 84 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_conservativeNormalizer_sq` | public theorem | 743–753 | S02 | `theorem cubicNormSq_le_conservativeNormalizer_sq (n : Nat) : cubicNormSq n ≤ conservativeNormalizer n ^ 2` |
| 85 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_arithmeticCubicNormalizer_sq` | public theorem | 754–763 | S02 | `theorem cubicNormSq_le_arithmeticCubicNormalizer_sq (n : Nat) : cubicNormSq n ≤ arithmeticCubicNormalizer n ^ 2` |
| 86 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_hadamardCountingCubicNormalizer_sq` | public theorem | 764–768 | S02 | `theorem cubicNormSq_le_hadamardCountingCubicNormalizer_sq (n : Nat) : cubicNormSq n ≤ hadamardCountingCubicNormalizer n ^ 2` |
| 87 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n1` | public theorem | 769–772 | S02 | `theorem cubicNormSq_n1 : cubicNormSq 1 = (1 : Rat) / 64` |
| 88 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n2` | public theorem | 773–776 | S02 | `theorem cubicNormSq_n2 : cubicNormSq 2 = (397 : Rat) / 2048` |
| 89 | `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n3` | public theorem | 777–785 | S02 | `theorem cubicNormSq_n3 : cubicNormSq 3 = (46205 : Rat) / 65536` |
| 90 | `QuantumBlockEncoding.CubicDiagonalOracle.taskId` | public def | 786–788 | S01 | `def taskId : String` |
| 91 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalOperator` | public def | 789–794 | S01 | `def cubicDiagonalOperator (n : Nat) : Matrix (gridSize n) (gridSize n) Rat` |
| 92 | `QuantumBlockEncoding.CubicDiagonalOracle.exactNormalizer` | public def | 795–797 | S01 | `def exactNormalizer (_n : Nat) : Rat` |
| 93 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalTarget` | public def | 798–818 | S01 | `def cubicDiagonalTarget (n : Nat) : QueryOperatorTarget Rat (gridSize n) (gridSize n)` |
| 94 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalOperator` | public def | 819–824 | S01 | `def linearDiagonalOperator (n : Nat) : Matrix (gridSize n) (gridSize n) Rat` |
| 95 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalTarget` | public def | 825–839 | S01 | `def linearDiagonalTarget (n : Nat) : QueryOperatorTarget Rat (gridSize n) (gridSize n)` |
| 96 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlockContract` | public def | 840–845 | S06 | `def linearDiagonalCleanBlockContract (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) : Prop` |
| 97 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlockContract_pointwise_eq` | public theorem | 846–852 | S06 | `theorem linearDiagonalCleanBlockContract_pointwise_eq (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) (h : linearDiagonalCleanBlockContract n block) : Matrix.PointwiseEq block (linearDiagonalOperator n)` |
| 98 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlock_eq_target` | public theorem | 853–866 | S06 | `theorem linearDiagonalCleanBlock_eq_target (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) (h : linearDiagonalCleanBlockContract n block) : Matrix.PointwiseEq block (linearDiagonalTarget n).operator` |
| 99 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalExactCleanBlockFromPointwise` | public def | 867–880 | S06 | `def linearDiagonalExactCleanBlockFromPointwise {n total : Nat} (U : Matrix total total Rat) (embed : Fin (gridSize n) -> Fin total) (h : Matrix.PointwiseEq (BlockEncodingClassics.cleanBlockBy embed U) (linearDiagonalOperator n)) : BlockEncodingClassics.ExactCleanBlock (gridSize n) total` |
| 100 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalExactCleanBlockFromPointwise_clean_eq_target` | public theorem | 881–903 | S06 | `theorem linearDiagonalExactCleanBlockFromPointwise_clean_eq_target {n total : Nat} (U : Matrix total total Rat) (embed : Fin (gridSize n) -> Fin total) (h : Matrix.PointwiseEq (BlockEncodingClassics.cleanBlockBy embed U) (linearDiagonalOperator n)) : Matrix.PointwiseEq (BlockEncodingClassics.ExactCleanBlock.clean (linearDiagonalExactCleanBlockFromPointwise U embed h)) (linearDiagonalTarget n).operator` |
| 101 | `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract` | public structure | 904–925 | S06 | `structure LinearDiagonalInputBEContract (n total : Nat)` |
| 102 | `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract.exactPayload` | public def | 926–931 | S06 | `def exactPayload {n total : Nat} (cert : LinearDiagonalInputBEContract n total) : BlockEncodingClassics.ExactCleanBlock (gridSize n) total` |
| 103 | `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract.clean_eq_target` | public theorem | 932–943 | S06 | `theorem clean_eq_target {n total : Nat} (cert : LinearDiagonalInputBEContract n total) : Matrix.PointwiseEq (BlockEncodingClassics.ExactCleanBlock.clean cert.exactPayload) (linearDiagonalTarget n).operator` |
| 104 | `QuantumBlockEncoding.CubicDiagonalOracle.householderZero` | public def | 944–946 | S04 | `def householderZero : Fin 8` |
| 105 | `QuantumBlockEncoding.CubicDiagonalOracle.dot8` | public def | 947–951 | S04 | `def dot8 (u v : Fin 8 -> Rat) : Rat` |
| 106 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus` | public def | 952–960 | S04 | `def householder8E0Minus (v : Fin 8 -> Rat) : Fin 8 -> Rat` |
| 107 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8` | public def | 961–967 | S04 | `def householder8 (v : Fin 8 -> Rat) : Matrix 8 8 Rat` |
| 108 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus_normSq` | public theorem | 968–976 | S04 | `theorem householder8E0Minus_normSq (v : Fin 8 -> Rat) (hunit : dot8 v v = 1) : dot8 (householder8E0Minus v) (householder8E0Minus v) = 2 * (1 - v householderZero)` |
| 109 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus_normSq_ne_zero` | public theorem | 977–988 | S04 | `theorem householder8E0Minus_normSq_ne_zero (v : Fin 8 -> Rat) (hunit : dot8 v v = 1) (hnot : v householderZero ≠ 1) : dot8 (householder8E0Minus v) (householder8E0Minus v) ≠ 0` |
| 110 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8_clean_entry` | public theorem | 989–1000 | S04 | `theorem householder8_clean_entry (v : Fin 8 -> Rat) (hunit : dot8 v v = 1) (hnot : v householderZero ≠ 1) : householder8 v householderZero householderZero = v householderZero` |
| 111 | `QuantumBlockEncoding.CubicDiagonalOracle.delta8` | private def | 1001–1003 | S04 | `private def delta8 (i : Fin 8) : Fin 8 -> Rat` |
| 112 | `QuantumBlockEncoding.CubicDiagonalOracle.fin8_exhaust` | private theorem | 1004–1034 | S04 | `private theorem fin8_exhaust (i : Fin 8) : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7` |
| 113 | `QuantumBlockEncoding.CubicDiagonalOracle.dot8_delta_delta` | private theorem | 1035–1041 | S04 | `private theorem dot8_delta_delta (i j : Fin 8) : dot8 (delta8 i) (delta8 j) = Matrix.identity 8 Rat i j` |
| 114 | `QuantumBlockEncoding.CubicDiagonalOracle.dot8_delta_left` | private theorem | 1042–1047 | S04 | `private theorem dot8_delta_left (i : Fin 8) (w : Fin 8 -> Rat) : dot8 (delta8 i) w = w i` |
| 115 | `QuantumBlockEncoding.CubicDiagonalOracle.dot8_delta_right` | private theorem | 1048–1053 | S04 | `private theorem dot8_delta_right (u : Fin 8 -> Rat) (j : Fin 8) : dot8 u (delta8 j) = u j` |
| 116 | `QuantumBlockEncoding.CubicDiagonalOracle.dot8_sub_sub` | private theorem | 1054–1060 | S04 | `private theorem dot8_sub_sub (a b u v : Fin 8 -> Rat) (c x y : Rat) : dot8 (fun k => a k - c * u k * x) (fun k => b k - c * v k * y) = dot8 a b - c * x * dot8 u b - c * y * dot8 a v + c * c * x * y * dot8 u v` |
| 117 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8_columnDot` | private theorem | 1061–1092 | S04 | `private theorem householder8_columnDot (v : Fin 8 -> Rat) (hunit : dot8 v v = 1) (hnot : v householderZero ≠ 1) : ∀ i j : Fin 8, dot8 (fun k => householder8 v k i) (fun k => householder8 v k j) = Matrix.identity 8 Rat i j` |
| 118 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8_symm` | private theorem | 1093–1097 | S04 | `private theorem householder8_symm (v : Fin 8 -> Rat) (i j : Fin 8) : householder8 v i j = householder8 v j i` |
| 119 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8_rowDot` | private theorem | 1098–1114 | S04 | `private theorem householder8_rowDot (v : Fin 8 -> Rat) (hunit : dot8 v v = 1) (hnot : v householderZero ≠ 1) : ∀ i j : Fin 8, dot8 (fun k => householder8 v i k) (fun k => householder8 v j k) = Matrix.identity 8 Rat i j` |
| 120 | `QuantumBlockEncoding.CubicDiagonalOracle.columnInner_eq_dot8` | private theorem | 1115–1120 | S04 | `private theorem columnInner_eq_dot8 (U : Matrix 8 8 Rat) (i j : Fin 8) : BlockEncodingClassics.columnInner U i j = dot8 (fun k => U k i) (fun k => U k j)` |
| 121 | `QuantumBlockEncoding.CubicDiagonalOracle.rowInner_eq_dot8` | private theorem | 1121–1131 | S04 | `private theorem rowInner_eq_dot8 (U : Matrix 8 8 Rat) (i j : Fin 8) : BlockEncodingClassics.rowInner U i j = dot8 (fun k => U i k) (fun k => U j k)` |
| 122 | `QuantumBlockEncoding.CubicDiagonalOracle.householder8_isRationalOrthogonal` | public theorem | 1132–1145 | S04 | `theorem householder8_isRationalOrthogonal (v : Fin 8 -> Rat) (hunit : dot8 v v = 1) (hnot : v householderZero ≠ 1) : BlockEncodingClassics.IsRationalOrthogonal (householder8 v)` |
| 123 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8SystemIndex` | public def | 1146–1150 | S05 | `def controlledHouseholder8SystemIndex (n : Nat) (idx : Fin (8 * gridSize n)) : Fin (gridSize n)` |
| 124 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8AncillaIndex` | public def | 1151–1159 | S05 | `def controlledHouseholder8AncillaIndex (n : Nat) (idx : Fin (8 * gridSize n)) : Fin 8` |
| 125 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8Embed` | public def | 1160–1164 | S05 | `def controlledHouseholder8Embed (n : Nat) : Fin (gridSize n) -> Fin (8 * gridSize n)` |
| 126 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum` | public def | 1165–1175 | S05 | `def controlledHouseholder8DirectSum (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) : Matrix (8 * gridSize n) (8 * gridSize n) Rat` |
| 127 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8Embed_val` | private theorem | 1176–1181 | S05 | `private theorem controlledHouseholder8Embed_val (n : Nat) (j : Fin (gridSize n)) : (controlledHouseholder8Embed n j).val = j.val` |
| 128 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8SystemIndex_embed` | private theorem | 1182–1188 | S05 | `private theorem controlledHouseholder8SystemIndex_embed (n : Nat) (j : Fin (gridSize n)) : controlledHouseholder8SystemIndex n (controlledHouseholder8Embed n j) = j` |
| 129 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8AncillaIndex_embed` | private theorem | 1189–1196 | S05 | `private theorem controlledHouseholder8AncillaIndex_embed (n : Nat) (j : Fin (gridSize n)) : controlledHouseholder8AncillaIndex n (controlledHouseholder8Embed n j) = householderZero` |
| 130 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8SystemIndex_productIndex` | private theorem | 1197–1204 | S05 | `private theorem controlledHouseholder8SystemIndex_productIndex (n : Nat) (a : Fin 8) (s : Fin (gridSize n)) : controlledHouseholder8SystemIndex n (BlockEncodingClassics.productIndex a s) = s` |
| 131 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8AncillaIndex_productIndex` | private theorem | 1205–1217 | S05 | `private theorem controlledHouseholder8AncillaIndex_productIndex (n : Nat) (a : Fin 8) (s : Fin (gridSize n)) : controlledHouseholder8AncillaIndex n (BlockEncodingClassics.productIndex a s) = a` |
| 132 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_productIndex_eta` | private theorem | 1218–1232 | S05 | `private theorem controlledHouseholder8_productIndex_eta (n : Nat) (idx : Fin (8 * gridSize n)) : BlockEncodingClassics.productIndex (controlledHouseholder8AncillaIndex n idx) (controlledHouseholder8SystemIndex n idx) = idx` |
| 133 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_identity_same_branch` | private theorem | 1233–1267 | S05 | `private theorem controlledHouseholder8_identity_same_branch (n : Nat) (i j : Fin (8 * gridSize n)) (hsys : controlledHouseholder8SystemIndex n i = controlledHouseholder8SystemIndex n j) : Matrix.identity (8 * gridSize n) Rat i j = Matrix.identity 8 Rat (controlledHouseholder8AncillaIndex n i) (controlledHouseholder8AncillaIndex n j)` |
| 134 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_branchNontrivial_of_clean` | public theorem | 1268–1285 | S05 | `theorem controlledHouseholder8_branchNontrivial_of_clean (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (branchClean : forall j : Fin (gridSize n), v j householderZero = CubicStatePreparation.gridPoint n j) : forall j : Fin (gridSize n), v j householderZero ≠ 1` |
| 135 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_clean_entry` | public theorem | 1286–1332 | S05 | `theorem controlledHouseholder8DirectSum_clean_entry (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (branchUnit : forall j : Fin (gridSize n), dot8 (v j) (v j) = 1) (branchClean : forall j : Fin (gridSize n), v j householderZero = CubicStatePreparation.gridPoint n j) (branchNontrivial : forall j : Fin (gridSize n), v j householderZero ≠ 1) : Matrix.PointwiseEq (BlockEncodingClassics.cleanBlockBy (controlledHouseholder8Embed n) (controlledHouseholder8DirectSum n v)) (linearDiagonalOperator n)` |
| 136 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_zero_of_all_zero` | private theorem | 1333–1359 | S05 | `private theorem linearDiagonal_foldl_add_zero_of_all_zero {β : Type u} (ks : List β) (f : β -> Rat) (acc : Rat) (hzero : ∀ k, k ∈ ks -> f k = 0) : ks.foldl (fun acc k => acc + f k) acc = acc` |
| 137 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_eq_identity_of_system_ne` | public theorem | 1360–1394 | S05 | `theorem controlledHouseholder8DirectSum_columnInner_eq_identity_of_system_ne (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (i j : Fin (8 * gridSize n)) (hsys : controlledHouseholder8SystemIndex n i ≠ controlledHouseholder8SystemIndex n j) : BlockEncodingClassics.columnInner (controlledHouseholder8DirectSum n v) i j = Matrix.identity (8 * gridSize n) Rat i j` |
| 138 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_column_off_branch_summand_zero` | private theorem | 1395–1410 | S05 | `private theorem controlledHouseholder8DirectSum_column_off_branch_summand_zero (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (s : Fin (gridSize n)) (i j k : Fin (8 * gridSize n)) (hi : controlledHouseholder8SystemIndex n i = s) (_hj : controlledHouseholder8SystemIndex n j = s) (hk : controlledHouseholder8SystemIndex n k ≠ s) : controlledHouseholder8DirectSum n v k i * controlledHouseholder8DirectSum n v k j = 0` |
| 139 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_column_summand_productIndex` | private theorem | 1411–1426 | S05 | `private theorem controlledHouseholder8DirectSum_column_summand_productIndex (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (s : Fin (gridSize n)) (a ai aj : Fin 8) : controlledHouseholder8DirectSum n v (BlockEncodingClassics.productIndex a s) (BlockEncodingClassics.productIndex ai s) * controlledHouseholder8DirectSum n v (BlockEncodingClassics.productIndex a s) (BlockEncodingClassics.productIndex aj s) = householder8 (v s) a ai * householder8 (v s) a aj` |
| 140 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_row_off_branch_summand_zero` | private theorem | 1427–1442 | S05 | `private theorem controlledHouseholder8DirectSum_row_off_branch_summand_zero (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (s : Fin (gridSize n)) (i j k : Fin (8 * gridSize n)) (hi : controlledHouseholder8SystemIndex n i = s) (_hj : controlledHouseholder8SystemIndex n j = s) (hk : controlledHouseholder8SystemIndex n k ≠ s) : controlledHouseholder8DirectSum n v i k * controlledHouseholder8DirectSum n v j k = 0` |
| 141 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_row_summand_productIndex` | private theorem | 1443–1458 | S05 | `private theorem controlledHouseholder8DirectSum_row_summand_productIndex (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (s : Fin (gridSize n)) (a ai aj : Fin 8) : controlledHouseholder8DirectSum n v (BlockEncodingClassics.productIndex ai s) (BlockEncodingClassics.productIndex a s) * controlledHouseholder8DirectSum n v (BlockEncodingClassics.productIndex aj s) (BlockEncodingClassics.productIndex a s) = householder8 (v s) ai a * householder8 (v s) aj a` |
| 142 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8BranchFiber` | private def | 1459–1464 | S05 | `private def controlledHouseholder8BranchFiber (n : Nat) (s : Fin (gridSize n)) : List (Fin (8 * gridSize n))` |
| 143 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_productIndex_left_injective` | private theorem | 1465–1473 | S05 | `private theorem controlledHouseholder8_productIndex_left_injective (n : Nat) (s : Fin (gridSize n)) : Function.Injective (fun a : Fin 8 => BlockEncodingClassics.productIndex a s)` |
| 144 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8BranchFiber_mem_iff` | private theorem | 1474–1488 | S05 | `private theorem controlledHouseholder8BranchFiber_mem_iff (n : Nat) (s : Fin (gridSize n)) (k : Fin (8 * gridSize n)) : k ∈ controlledHouseholder8BranchFiber n s ↔ controlledHouseholder8SystemIndex n k = s` |
| 145 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_unique_of_nodup` | private theorem | 1489–1533 | S05 | `private theorem linearDiagonal_foldl_add_unique_of_nodup {β : Type u} [DecidableEq β] (ks : List β) (f : β -> Rat) (k0 : β) (hnodup : ks.Nodup) (hmem : k0 ∈ ks) (hzero : ∀ k, k ∈ ks -> k ≠ k0 -> f k = 0) : ks.foldl (fun acc k => acc + f k) 0 = f k0` |
| 146 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_nodup_map_of_injective` | private theorem | 1534–1552 | S05 | `private theorem linearDiagonal_nodup_map_of_injective {α : Type u} {β : Type v} [DecidableEq β] {f : α -> β} (hf : Function.Injective f) {xs : List α} (hxs : xs.Nodup) : (xs.map f).Nodup` |
| 147 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_finRange_nodup` | private theorem | 1553–1570 | S05 | `private theorem linearDiagonal_finRange_nodup (n : Nat) : (List.finRange n).Nodup` |
| 148 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8BranchFiber_nodup` | private theorem | 1571–1577 | S05 | `private theorem controlledHouseholder8BranchFiber_nodup (n : Nat) (s : Fin (gridSize n)) : (controlledHouseholder8BranchFiber n s).Nodup` |
| 149 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_perm_cons_erase_of_mem` | private theorem | 1578–1599 | S05 | `private theorem linearDiagonal_perm_cons_erase_of_mem {α : Type u} [BEq α] [LawfulBEq α] (x : α) : ∀ {ys : List α}, x ∈ ys -> ys.Perm (x :: ys.erase x) &#124; [], h => by cases h &#124; y :: ys, h => by by_cases hy : y = x · subst y simp [List.erase_cons_head] · have htail : x ∈ ys` |
| 150 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_perm_of_nodup_mem_iff` | private theorem | 1600–1640 | S05 | `private theorem linearDiagonal_perm_of_nodup_mem_iff {α : Type u} [BEq α] [LawfulBEq α] {xs ys : List α} (hxs : xs.Nodup) (hys : ys.Nodup) (hmem : ∀ x, x ∈ xs ↔ x ∈ ys) : xs.Perm ys` |
| 151 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_perm` | private theorem | 1641–1650 | S05 | `private theorem linearDiagonal_foldl_add_perm {β : Type u} (xs ys : List β) (f : β -> Rat) (hperm : xs.Perm ys) : xs.foldl (fun acc x => acc + f x) 0 = ys.foldl (fun acc x => acc + f x) 0` |
| 152 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_filter_of_zero_acc` | private theorem | 1651–1669 | S05 | `private theorem linearDiagonal_foldl_add_filter_of_zero_acc {β : Type u} (xs : List β) (p : β -> Bool) (f : β -> Rat) (acc : Rat) (hzero : ∀ x, x ∈ xs -> p x = false -> f x = 0) : xs.foldl (fun acc x => acc + f x) acc = (xs.filter p).foldl (fun acc x => acc + f x) acc` |
| 153 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_filter_of_zero` | private theorem | 1670–1676 | S05 | `private theorem linearDiagonal_foldl_add_filter_of_zero {β : Type u} (xs : List β) (p : β -> Bool) (f : β -> Rat) (hzero : ∀ x, x ∈ xs -> p x = false -> f x = 0) : xs.foldl (fun acc x => acc + f x) 0 = (xs.filter p).foldl (fun acc x => acc + f x) 0` |
| 154 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_congr_acc` | private theorem | 1677–1692 | S05 | `private theorem linearDiagonal_foldl_add_congr_acc {β : Type u} (xs : List β) (f g : β -> Rat) (acc : Rat) (hfg : ∀ x, x ∈ xs -> f x = g x) : xs.foldl (fun acc x => acc + f x) acc = xs.foldl (fun acc x => acc + g x) acc` |
| 155 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_congr` | private theorem | 1693–1699 | S05 | `private theorem linearDiagonal_foldl_add_congr {β : Type u} (xs : List β) (f g : β -> Rat) (hfg : ∀ x, x ∈ xs -> f x = g x) : xs.foldl (fun acc x => acc + f x) 0 = xs.foldl (fun acc x => acc + g x) 0` |
| 156 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8BranchFiber_filter_perm` | private theorem | 1700–1725 | S05 | `private theorem controlledHouseholder8BranchFiber_filter_perm (n : Nat) (s : Fin (gridSize n)) : ((List.finRange (8 * gridSize n)).filter (fun k : Fin (8 * gridSize n) => decide (controlledHouseholder8SystemIndex n k = s))).Perm (controlledHouseholder8BranchFiber n s)` |
| 157 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_productIndex` | private theorem | 1726–1798 | S05 | `private theorem controlledHouseholder8DirectSum_columnInner_productIndex (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (s : Fin (gridSize n)) (ai aj : Fin 8) : BlockEncodingClassics.columnInner (controlledHouseholder8DirectSum n v) (BlockEncodingClassics.productIndex ai s) (BlockEncodingClassics.productIndex aj s) = BlockEncodingClassics.columnInner (householder8 (v s)) ai aj` |
| 158 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_eq_branch` | public theorem | 1799–1844 | S05 | `theorem controlledHouseholder8DirectSum_columnInner_eq_branch (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (i j : Fin (8 * gridSize n)) (hsys : controlledHouseholder8SystemIndex n i = controlledHouseholder8SystemIndex n j) : BlockEncodingClassics.columnInner (controlledHouseholder8DirectSum n v) i j = BlockEncodingClassics.columnInner (householder8 (v (controlledHouseholder8SystemIndex n i))) (controlledHouseholder8AncillaIndex n i) (controlledHouseholder8AncillaIndex n j)` |
| 159 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_productIndex` | private theorem | 1845–1917 | S05 | `private theorem controlledHouseholder8DirectSum_rowInner_productIndex (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (s : Fin (gridSize n)) (ai aj : Fin 8) : BlockEncodingClassics.rowInner (controlledHouseholder8DirectSum n v) (BlockEncodingClassics.productIndex ai s) (BlockEncodingClassics.productIndex aj s) = BlockEncodingClassics.rowInner (householder8 (v s)) ai aj` |
| 160 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_eq_branch` | public theorem | 1918–1971 | S05 | `theorem controlledHouseholder8DirectSum_rowInner_eq_branch (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (i j : Fin (8 * gridSize n)) (hsys : controlledHouseholder8SystemIndex n i = controlledHouseholder8SystemIndex n j) : BlockEncodingClassics.rowInner (controlledHouseholder8DirectSum n v) i j = BlockEncodingClassics.rowInner (householder8 (v (controlledHouseholder8SystemIndex n i))) (controlledHouseholder8AncillaIndex n i) (controlledHouseholder8AncillaIndex n j)` |
| 161 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_eq_identity_of_system_ne` | public theorem | 1972–2011 | S05 | `theorem controlledHouseholder8DirectSum_rowInner_eq_identity_of_system_ne (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (i j : Fin (8 * gridSize n)) (hsys : controlledHouseholder8SystemIndex n i ≠ controlledHouseholder8SystemIndex n j) : BlockEncodingClassics.rowInner (controlledHouseholder8DirectSum n v) i j = Matrix.identity (8 * gridSize n) Rat i j` |
| 162 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_isRationalOrthogonal` | public theorem | 2012–2060 | S05 | `theorem controlledHouseholder8DirectSum_isRationalOrthogonal (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (branchUnit : forall j : Fin (gridSize n), dot8 (v j) (v j) = 1) (branchNontrivial : forall j : Fin (gridSize n), v j householderZero ≠ 1) : BlockEncodingClassics.IsRationalOrthogonal (controlledHouseholder8DirectSum n v)` |
| 163 | `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalRationalCompletion` | public def | 2061–2073 | S06 | `def LinearDiagonalRationalCompletion (n : Nat) : Prop` |
| 164 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector` | public def | 2074–2083 | S06 | `def linearDiagonalFourSquareBranchVector (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) : Fin 8 -> Rat` |
| 165 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_clean` | public theorem | 2084–2090 | S06 | `theorem linearDiagonalFourSquareBranchVector_clean (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) : linearDiagonalFourSquareBranchVector n j a b c d householderZero = CubicStatePreparation.gridPoint n j` |
| 166 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_unit` | public theorem | 2091–2113 | S06 | `theorem linearDiagonalFourSquareBranchVector_unit (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) (hsq : gridSize n ^ 2 = j.val ^ 2 + a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) : dot8 (linearDiagonalFourSquareBranchVector n j a b c d) (linearDiagonalFourSquareBranchVector n j a b c d) = 1` |
| 167 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_of_fourSquareWitnesses` | public theorem | 2114–2133 | S06 | `theorem linearDiagonalRationalCompletion_of_fourSquareWitnesses (n : Nat) (a b c d : Fin (gridSize n) -> Nat) (hsq : forall j : Fin (gridSize n), gridSize n ^ 2 = j.val ^ 2 + a j ^ 2 + b j ^ 2 + c j ^ 2 + d j ^ 2) : LinearDiagonalRationalCompletion n` |
| 168 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_exists` | public theorem | 2134–2155 | S06 | `theorem linearDiagonalRationalCompletion_exists (n : Nat) : LinearDiagonalRationalCompletion n` |
| 169 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_branchData` | public theorem | 2156–2175 | S06 | `theorem linearDiagonalRationalCompletion_branchData (n : Nat) (h : LinearDiagonalRationalCompletion n) : exists v : Fin (gridSize n) -> Fin 8 -> Rat, (forall j : Fin (gridSize n), dot8 (v j) (v j) = 1) ∧ (forall j : Fin (gridSize n), v j householderZero = CubicStatePreparation.gridPoint n j) ∧ (forall j : Fin (gridSize n), v j householderZero ≠ 1)` |
| 170 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_backendSupport` | public theorem | 2176–2197 | S06 | `theorem linearDiagonalRationalCompletion_backendSupport (n : Nat) (h : LinearDiagonalRationalCompletion n) : exists v : Fin (gridSize n) -> Fin 8 -> Rat, Matrix.PointwiseEq (BlockEncodingClassics.cleanBlockBy (controlledHouseholder8Embed n) (controlledHouseholder8DirectSum n v)) (linearDiagonalOperator n) ∧ BlockEncodingClassics.IsRationalOrthogonal (controlledHouseholder8DirectSum n v)` |
| 171 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderCircuit` | public def | 2198–2200 | S06 | `def linearDiagonalHouseholderCircuit (_n : Nat) : Circuit` |
| 172 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderResource` | public def | 2201–2203 | S06 | `def linearDiagonalHouseholderResource (n : Nat) : Resource` |
| 173 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderResource_eq` | public theorem | 2204–2216 | S06 | `theorem linearDiagonalHouseholderResource_eq (n : Nat) : linearDiagonalHouseholderResource n = Resource.ofCountsWithDepth 0 0 1 0 1` |
| 174 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract` | public noncomputable def | 2217–2247 | S06 | `noncomputable def linearDiagonalHouseholderInputBEContract (n : Nat) : LinearDiagonalInputBEContract n (8 * gridSize n)` |
| 175 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract_clean_eq_target` | public theorem | 2248–2260 | S06 | `theorem linearDiagonalHouseholderInputBEContract_clean_eq_target (n : Nat) : Matrix.PointwiseEq (BlockEncodingClassics.ExactCleanBlock.clean (linearDiagonalHouseholderInputBEContract n).exactPayload) (linearDiagonalTarget n).operator` |
| 176 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract_complete` | public theorem | 2261–2283 | S06 | `theorem linearDiagonalHouseholderInputBEContract_complete (n : Nat) : BlockEncodingClassics.IsRationalOrthogonal (linearDiagonalHouseholderInputBEContract n).U ∧ Matrix.PointwiseEq (BlockEncodingClassics.cleanBlockBy (linearDiagonalHouseholderInputBEContract n).embed (linearDiagonalHouseholderInputBEContract n).U) (linearDiagonalTarget n).operator ∧ (linearDiagonalTarget n).normalizer = 1 ∧ (linearDiagonalHouseholderInputBEContract n).resource = Resource.ofCountsWithDepth 0 0 1 0 1` |
| 177 | `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator` | public def | 2284–2288 | S08 | `def approxDiagonalOperator (n : Nat) (q : Fin (gridSize n) -> Rat) : Matrix (gridSize n) (gridSize n) Rat` |
| 178 | `QuantumBlockEncoding.CubicDiagonalOracle.ratAbs` | public def | 2289–2291 | S08 | `def ratAbs (x : Rat) : Rat` |
| 179 | `QuantumBlockEncoding.CubicDiagonalOracle.IsDiagonalRatMatrix` | public def | 2292–2302 | S08 | `def IsDiagonalRatMatrix (dim : Nat) (A : Matrix dim dim Rat) : Prop` |
| 180 | `QuantumBlockEncoding.CubicDiagonalOracle.DiagonalRatOperatorNormBridge` | public structure | 2303–2313 | S08 | `structure DiagonalRatOperatorNormBridge (dim : Nat)` |
| 181 | `QuantumBlockEncoding.CubicDiagonalOracle.ratSquaredEuclideanNorm` | public def | 2314–2317 | S08 | `def ratSquaredEuclideanNorm {dim : Nat} (v : Fin dim -> Rat) : Rat` |
| 182 | `QuantumBlockEncoding.CubicDiagonalOracle.ratMatrixErrorAction` | public def | 2318–2330 | S08 | `def ratMatrixErrorAction {dim : Nat} (A B : Matrix dim dim Rat) (v : Fin dim -> Rat) : Fin dim -> Rat` |
| 183 | `QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanOperatorNormErrorAtMost` | public def | 2331–2337 | S08 | `def ratEuclideanOperatorNormErrorAtMost {dim : Nat} (A B : Matrix dim dim Rat) (epsilon : Rat) : Prop` |
| 184 | `QuantumBlockEncoding.CubicDiagonalOracle.diagonalFoldlAddZero` | private theorem | 2338–2355 | S08 | `private theorem diagonalFoldlAddZero {β : Type u} (xs : List β) (f : β -> Rat) (acc : Rat) (hzero : ∀ x, x ∈ xs -> f x = 0) : xs.foldl (fun total x => total + f x) acc = acc` |
| 185 | `QuantumBlockEncoding.CubicDiagonalOracle.diagonalFoldlAddUnique` | private theorem | 2356–2397 | S08 | `private theorem diagonalFoldlAddUnique {β : Type u} [DecidableEq β] (xs : List β) (f : β -> Rat) (x0 : β) (hnodup : xs.Nodup) (hmem : x0 ∈ xs) (hzero : ∀ x, x ∈ xs -> x ≠ x0 -> f x = 0) : xs.foldl (fun total x => total + f x) 0 = f x0` |
| 186 | `QuantumBlockEncoding.CubicDiagonalOracle.diagonalNodupMapOfInjective` | private theorem | 2398–2415 | S08 | `private theorem diagonalNodupMapOfInjective {α : Type u} {β : Type v} [DecidableEq β] {f : α -> β} (hf : Function.Injective f) {xs : List α} (hxs : xs.Nodup) : (xs.map f).Nodup` |
| 187 | `QuantumBlockEncoding.CubicDiagonalOracle.diagonalFinRangeNodup` | private theorem | 2416–2432 | S08 | `private theorem diagonalFinRangeNodup (dim : Nat) : (List.finRange dim).Nodup` |
| 188 | `QuantumBlockEncoding.CubicDiagonalOracle.diagonalFoldlAddLe` | private theorem | 2433–2452 | S08 | `private theorem diagonalFoldlAddLe {β : Type u} (xs : List β) (f g : β -> Rat) (hpoint : ∀ x, x ∈ xs -> f x ≤ g x) (left right : Rat) (hacc : left ≤ right) : xs.foldl (fun acc x => acc + f x) left ≤ xs.foldl (fun acc x => acc + g x) right` |
| 189 | `QuantumBlockEncoding.CubicDiagonalOracle.ratMatrixErrorAction_eq_diagonal` | public theorem | 2453–2467 | S08 | `theorem ratMatrixErrorAction_eq_diagonal {dim : Nat} (A B : Matrix dim dim Rat) (v : Fin dim -> Rat) (row : Fin dim) (hA : IsDiagonalRatMatrix dim A) (hB : IsDiagonalRatMatrix dim B) : ratMatrixErrorAction A B v row = (A row row - B row row) * v row` |
| 190 | `QuantumBlockEncoding.CubicDiagonalOracle.ratAbs_nonneg` | public theorem | 2468–2471 | S08 | `theorem ratAbs_nonneg (x : Rat) : 0 ≤ ratAbs x` |
| 191 | `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_eq_ratAbs_mul_self` | public theorem | 2472–2476 | S08 | `theorem rat_mul_self_eq_ratAbs_mul_self (x : Rat) : x * x = ratAbs x * ratAbs x` |
| 192 | `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_nonneg` | public theorem | 2477–2480 | S08 | `theorem rat_mul_self_nonneg (x : Rat) : 0 ≤ x * x` |
| 193 | `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_le_of_abs_le` | public theorem | 2481–2490 | S08 | `theorem rat_mul_self_le_of_abs_le (x epsilon : Rat) (hepsilon : 0 ≤ epsilon) (habs : ratAbs x ≤ epsilon) : x * x ≤ epsilon * epsilon` |
| 194 | `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_product_self` | private theorem | 2491–2498 | S08 | `private theorem rat_mul_product_self (a b : Rat) : (a * b) * (a * b) = (a * a) * (b * b)` |
| 195 | `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_vector_le_of_abs_le` | public theorem | 2499–2508 | S08 | `theorem rat_mul_self_vector_le_of_abs_le (x epsilon value : Rat) (hepsilon : 0 ≤ epsilon) (habs : ratAbs x ≤ epsilon) : (x * value) * (x * value) ≤ (epsilon * value) * (epsilon * value)` |
| 196 | `QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanDiagonalOperatorNormBridge` | public def | 2509–2524 | S08 | `def ratEuclideanDiagonalOperatorNormBridge (dim : Nat) : DiagonalRatOperatorNormBridge dim` |
| 197 | `QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanOperatorNormErrorAtMost_not_vacuous` | public theorem | 2525–2538 | S08 | `theorem ratEuclideanOperatorNormErrorAtMost_not_vacuous : ¬ ratEuclideanOperatorNormErrorAtMost (Matrix.identity 1 Rat) (Matrix.zero 1 1 Rat) 0` |
| 198 | `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_isDiagonal` | public theorem | 2539–2545 | S08 | `theorem approxDiagonalOperator_isDiagonal (n : Nat) (q : Fin (gridSize n) -> Rat) : IsDiagonalRatMatrix (gridSize n) (approxDiagonalOperator n q)` |
| 199 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalOperator_isDiagonal` | public theorem | 2546–2557 | S08 | `theorem cubicDiagonalOperator_isDiagonal (n : Nat) : IsDiagonalRatMatrix (gridSize n) (cubicDiagonalOperator n)` |
| 200 | `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalEntrywiseErrorAtMost` | public def | 2558–2569 | S08 | `def approxDiagonalEntrywiseErrorAtMost (n : Nat) (q : Fin (gridSize n) -> Rat) (epsilon : Rat) : Prop` |
| 201 | `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_entrywise_error` | public theorem | 2570–2596 | S08 | `theorem approxDiagonalOperator_entrywise_error (n : Nat) (q : Fin (gridSize n) -> Rat) (epsilon : Rat) (hdiag : approxDiagonalEntrywiseErrorAtMost n q epsilon) (hepsilon : 0 ≤ epsilon) : ∀ row col : Fin (gridSize n), ratAbs (approxDiagonalOperator n q row col - cubicDiagonalOperator n row col) ≤ epsilon` |
| 202 | `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_operatorNorm_error_of_contract` | public theorem | 2597–2618 | S08 | `theorem approxDiagonalOperator_operatorNorm_error_of_contract (n : Nat) (q : Fin (gridSize n) -> Rat) (epsilon : Rat) (bridge : DiagonalRatOperatorNormBridge (gridSize n)) (hdiag : approxDiagonalEntrywiseErrorAtMost n q epsilon) (hepsilon : 0 ≤ epsilon) : bridge.opNormErrorAtMost (approxDiagonalOperator n q) (cubicDiagonalOperator n) epsilon` |
| 203 | `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_operatorNorm_error` | public theorem | 2619–2634 | S08 | `theorem approxDiagonalOperator_operatorNorm_error (n : Nat) (q : Fin (gridSize n) -> Rat) (epsilon : Rat) (hdiag : approxDiagonalEntrywiseErrorAtMost n q epsilon) (hepsilon : 0 ≤ epsilon) : ratEuclideanOperatorNormErrorAtMost (approxDiagonalOperator n q) (cubicDiagonalOperator n) epsilon` |
| 204 | `QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector` | public def | 2635–2640 | S08 | `def rationalCircleBranchVector (q r : Rat) : Fin 8 -> Rat` |
| 205 | `QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector_clean` | public theorem | 2641–2644 | S08 | `theorem rationalCircleBranchVector_clean (q r : Rat) : rationalCircleBranchVector q r householderZero = q` |
| 206 | `QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector_unit` | public theorem | 2645–2660 | S08 | `theorem rationalCircleBranchVector_unit (q r : Rat) (hcircle : q ^ 2 + r ^ 2 = 1) : dot8 (rationalCircleBranchVector q r) (rationalCircleBranchVector q r) = 1` |
| 207 | `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_clean_entry_of_branchValue` | public theorem | 2661–2708 | S08 | `theorem controlledHouseholder8DirectSum_clean_entry_of_branchValue (n : Nat) (q : Fin (gridSize n) -> Rat) (v : Fin (gridSize n) -> Fin 8 -> Rat) (branchUnit : forall j : Fin (gridSize n), dot8 (v j) (v j) = 1) (branchClean : forall j : Fin (gridSize n), v j householderZero = q j) (branchNontrivial : forall j : Fin (gridSize n), v j householderZero ≠ 1) : Matrix.PointwiseEq (BlockEncodingClassics.cleanBlockBy (controlledHouseholder8Embed n) (controlledHouseholder8DirectSum n v)) (approxDiagonalOperator n q)` |
| 208 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector` | public def | 2709–2718 | S06 | `def cubicDiagonalFourSquareBranchVector (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) : Fin 8 -> Rat` |
| 209 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_clean` | public theorem | 2719–2727 | S06 | `theorem cubicDiagonalFourSquareBranchVector_clean (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) : cubicDiagonalFourSquareBranchVector n j a b c d householderZero = CubicStatePreparation.cubicAmplitude n j` |
| 210 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_unit` | public theorem | 2728–2745 | S06 | `theorem cubicDiagonalFourSquareBranchVector_unit (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) (hsq : gridSize n ^ 6 = j.val ^ 6 + a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) : dot8 (cubicDiagonalFourSquareBranchVector n j a b c d) (cubicDiagonalFourSquareBranchVector n j a b c d) = 1` |
| 211 | `QuantumBlockEncoding.CubicDiagonalOracle.CubicDiagonalRationalCompletion` | public def | 2746–2751 | S06 | `def CubicDiagonalRationalCompletion (n : Nat) : Prop` |
| 212 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_of_fourSquareWitnesses` | public theorem | 2752–2766 | S06 | `theorem cubicDiagonalRationalCompletion_of_fourSquareWitnesses (n : Nat) (a b c d : Fin (gridSize n) -> Nat) (hsq : forall j : Fin (gridSize n), gridSize n ^ 6 = j.val ^ 6 + a j ^ 2 + b j ^ 2 + c j ^ 2 + d j ^ 2) : CubicDiagonalRationalCompletion n` |
| 213 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_exists` | public theorem | 2767–2783 | S06 | `theorem cubicDiagonalRationalCompletion_exists (n : Nat) : CubicDiagonalRationalCompletion n` |
| 214 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_lt_one` | public theorem | 2784–2799 | S06 | `theorem cubicAmplitude_lt_one (n : Nat) (j : Fin (gridSize n)) : CubicStatePreparation.cubicAmplitude n j < 1` |
| 215 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_backendSupport` | public theorem | 2800–2827 | S06 | `theorem cubicDiagonalRationalCompletion_backendSupport (n : Nat) : exists v : Fin (gridSize n) -> Fin 8 -> Rat, Matrix.PointwiseEq (BlockEncodingClassics.cleanBlockBy (controlledHouseholder8Embed n) (controlledHouseholder8DirectSum n v)) (cubicDiagonalOperator n) ∧ BlockEncodingClassics.IsRationalOrthogonal (controlledHouseholder8DirectSum n v)` |
| 216 | `QuantumBlockEncoding.CubicDiagonalOracle.CubicDiagonalExactBEContract` | public structure | 2828–2837 | S06 | `structure CubicDiagonalExactBEContract (n total : Nat)` |
| 217 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract` | public noncomputable def | 2838–2866 | S06 | `noncomputable def cubicDiagonalHouseholderExactBEContract (n : Nat) : CubicDiagonalExactBEContract n (8 * gridSize n)` |
| 218 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract_clean_eq_target` | public theorem | 2867–2878 | S06 | `theorem cubicDiagonalHouseholderExactBEContract_clean_eq_target (n : Nat) : Matrix.PointwiseEq (cubicDiagonalHouseholderExactBEContract n).exactPayload.clean (cubicDiagonalTarget n).operator` |
| 219 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract_complete` | public theorem | 2879–2894 | S06 | `theorem cubicDiagonalHouseholderExactBEContract_complete (n : Nat) : BlockEncodingClassics.IsRationalOrthogonal (cubicDiagonalHouseholderExactBEContract n).exactPayload.U ∧ Matrix.PointwiseEq (cubicDiagonalHouseholderExactBEContract n).exactPayload.clean (cubicDiagonalTarget n).operator ∧ (cubicDiagonalTarget n).normalizer = 1 ∧ (cubicDiagonalHouseholderExactBEContract n).resource = Resource.ofCountsWithDepth 0 0 1 0 1` |
| 220 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_unique_finRange` | private theorem | 2895–2904 | S07 | `private theorem linearDiagonal_foldl_add_unique_finRange {n : Nat} (f : Fin n -> Rat) (k0 : Fin n) (hzero : ∀ k : Fin n, k ≠ k0 -> f k = 0) : (List.finRange n).foldl (fun acc k => acc + f k) 0 = f k0` |
| 221 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_mul_entry` | private theorem | 2905–2940 | S07 | `private theorem linearDiagonal_mul_entry (n : Nat) (row col : Fin (gridSize n)) : Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n) row col = if row = col then CubicStatePreparation.gridPoint n row * CubicStatePreparation.gridPoint n row else 0` |
| 222 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_square_mul_entry` | private theorem | 2941–3000 | S07 | `private theorem linearDiagonal_square_mul_entry (n : Nat) (row col : Fin (gridSize n)) : Matrix.mul (Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n)) (linearDiagonalOperator n) row col = if row = col then (CubicStatePreparation.gridPoint n row * CubicStatePreparation.gridPoint n row) * CubicStatePreparation.gridPoint n row else 0` |
| 223 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_cube_eq_cubicDiagonalOperator` | public theorem | 3001–3021 | S07 | `theorem linearDiagonal_cube_eq_cubicDiagonalOperator (n : Nat) : Matrix.PointwiseEq (Matrix.mul (Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n)) (linearDiagonalOperator n)) (cubicDiagonalOperator n)` |
| 224 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate` | public noncomputable def | 3022–3029 | S07 | `noncomputable def linearDiagonalCubicProductCertificate (n : Nat) : BlockEncodingClassics.LCUCertificate (gridSize n)` |
| 225 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate_target_eq` | public theorem | 3030–3039 | S07 | `theorem linearDiagonalCubicProductCertificate_target_eq (n : Nat) : Matrix.PointwiseEq (linearDiagonalCubicProductCertificate n).target (cubicDiagonalTarget n).operator` |
| 226 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate_clean_eq_target` | public theorem | 3040–3049 | S07 | `theorem linearDiagonalCubicProductCertificate_clean_eq_target (n : Nat) : Matrix.PointwiseEq (linearDiagonalCubicProductCertificate n).cleanBlock (cubicDiagonalTarget n).operator` |
| 227 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTPolynomial` | public def | 3050–3052 | S07 | `def cubicQSVTPolynomial (x : Rat) : Rat` |
| 228 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTPolynomial_gridPoint_abs_le_one` | public theorem | 3053–3063 | S07 | `theorem cubicQSVTPolynomial_gridPoint_abs_le_one (n : Nat) (j : Fin (gridSize n)) : Rat.abs (cubicQSVTPolynomial (CubicStatePreparation.gridPoint n j)) ≤ 1` |
| 229 | `QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTLocalSideConditions` | public structure | 3064–3072 | S07 | `structure CubicQSVTLocalSideConditions (n : Nat)` |
| 230 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTLocalSideConditions` | public def | 3073–3090 | S07 | `def cubicQSVTLocalSideConditions (n : Nat) : CubicQSVTLocalSideConditions n` |
| 231 | `QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics` | public structure | 3091–3111 | S07 | `structure CubicQSVTExternalSemantics (n inputTotal outputTotal : Nat)` |
| 232 | `QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics.output_eq_cubic_target` | public theorem | 3112–3119 | S07 | `theorem output_eq_cubic_target {n inputTotal outputTotal : Nat} (semantics : CubicQSVTExternalSemantics n inputTotal outputTotal) : Matrix.PointwiseEq semantics.output.A (cubicDiagonalTarget n).operator` |
| 233 | `QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics.consumerContract` | public def | 3120–3137 | S07 | `def consumerContract {n inputTotal outputTotal : Nat} (semantics : CubicQSVTExternalSemantics n inputTotal outputTotal) : BlockEncodingClassics.QSVTConsumerContract (gridSize n) inputTotal` |
| 234 | `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleLayout` | public def | 3138–3143 | S09 | `def amplitudeOracleLayout (n : Nat) : RegisterLayout` |
| 235 | `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleCircuit` | public def | 3144–3147 | S09 | `def amplitudeOracleCircuit (_n : Nat) : Circuit` |
| 236 | `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResource` | public def | 3148–3151 | S09 | `def amplitudeOracleResource (n : Nat) : Resource` |
| 237 | `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleCost` | public def | 3152–3156 | S09 | `def amplitudeOracleCost (n : Nat) : BlockEncodingCost` |
| 238 | `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResourceTuple` | public def | 3157–3163 | S09 | `def amplitudeOracleResourceTuple (n : Nat) : Nat × Nat × Nat × Nat` |
| 239 | `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResource_eq` | public theorem | 3164–3167 | S09 | `theorem amplitudeOracleResource_eq (n : Nat) : amplitudeOracleResource n = Resource.ofCountsWithDepth 0 0 1 0 1` |
| 240 | `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResourceTuple_eq` | public theorem | 3168–3174 | S09 | `theorem amplitudeOracleResourceTuple_eq (n : Nat) : amplitudeOracleResourceTuple n = (1, 1, 1, 1)` |
| 241 | `QuantumBlockEncoding.CubicDiagonalOracle.diagonalCleanBlockContract` | public def | 3175–3180 | S09 | `def diagonalCleanBlockContract (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) : Prop` |
| 242 | `QuantumBlockEncoding.CubicDiagonalOracle.diagonalCleanBlockContract_pointwise_eq` | public theorem | 3181–3187 | S09 | `theorem diagonalCleanBlockContract_pointwise_eq (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) (h : diagonalCleanBlockContract n block) : Matrix.PointwiseEq block (cubicDiagonalOperator n)` |
| 243 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveOracleCleanBlock_eq_target` | public theorem | 3188–3195 | S09 | `theorem primitiveOracleCleanBlock_eq_target (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) (h : diagonalCleanBlockContract n block) : Matrix.PointwiseEq block (cubicDiagonalTarget n).operator` |
| 244 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_le_one` | public theorem | 3196–3202 | S02 | `theorem cubicAmplitude_le_one (n : Nat) (j : Fin (gridSize n)) : CubicStatePreparation.cubicAmplitude n j ≤ 1` |
| 245 | `QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_nonneg` | public theorem | 3203–3209 | S02 | `theorem cubicAmplitude_nonneg (n : Nat) (j : Fin (gridSize n)) : 0 ≤ CubicStatePreparation.cubicAmplitude n j` |
| 246 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleDimension` | public def | 3210–3218 | S09 | `def primitiveAmplitudeOracleDimension (n : Nat) : Nat` |
| 247 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleUnitary` | public opaque | 3219–3223 | S09 | `opaque primitiveAmplitudeOracleUnitary (n : Nat) : Matrix (primitiveAmplitudeOracleDimension n) (primitiveAmplitudeOracleDimension n) Rat` |
| 248 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleIsUnitary` | public opaque | 3224–3228 | S09 | `opaque primitiveAmplitudeOracleIsUnitary (n : Nat) (unitary : Matrix (primitiveAmplitudeOracleDimension n) (primitiveAmplitudeOracleDimension n) Rat) : Prop` |
| 249 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCleanBlockExtracts` | public opaque | 3229–3240 | S09 | `opaque primitiveAmplitudeOracleCleanBlockExtracts (n : Nat) (unitary : Matrix (primitiveAmplitudeOracleDimension n) (primitiveAmplitudeOracleDimension n) Rat) (block : Matrix (gridSize n) (gridSize n) Rat) : Prop` |
| 250 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract` | public def | 3241–3247 | S09 | `def primitiveAmplitudeOracleSemanticContract (n : Nat) : Prop` |
| 251 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract_unitary` | public theorem | 3248–3252 | S09 | `theorem primitiveAmplitudeOracleSemanticContract_unitary (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) : primitiveAmplitudeOracleIsUnitary n (primitiveAmplitudeOracleUnitary n)` |
| 252 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract_cleanBlock_eq_target` | public theorem | 3253–3267 | S09 | `theorem primitiveAmplitudeOracleSemanticContract_cleanBlock_eq_target (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) : ∃ block : Matrix (gridSize n) (gridSize n) Rat, primitiveAmplitudeOracleCleanBlockExtracts n (primitiveAmplitudeOracleUnitary n) block ∧ Matrix.PointwiseEq block (cubicDiagonalTarget n).operator` |
| 253 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleLayout` | public def | 3268–3272 | S12 | `def expandedAmplitudeOracleLayout (n workspaceQubits : Nat) : RegisterLayout` |
| 254 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleLayout_auxiliaryQubits` | public theorem | 3273–3279 | S12 | `theorem expandedAmplitudeOracleLayout_auxiliaryQubits (n workspaceQubits : Nat) : (expandedAmplitudeOracleLayout n workspaceQubits).auxiliaryQubits = 1 + workspaceQubits` |
| 255 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleNormalizer_eq` | public theorem | 3280–3292 | S12 | `theorem expandedAmplitudeOracleNormalizer_eq (n _workspaceQubits : Nat) : exactNormalizer n = 1` |
| 256 | `QuantumBlockEncoding.CubicDiagonalOracle.StandardRyCleanEntryScalarTier` | public structure | 3293–3307 | S10 | `structure StandardRyCleanEntryScalarTier` |
| 257 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedRyCleanEntryForCubicAmplitudes` | public def | 3308–3320 | S10 | `def expandedRyCleanEntryForCubicAmplitudes (tier : StandardRyCleanEntryScalarTier) (n : Nat) : Prop` |
| 258 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedRyCleanEntryForCubicAmplitudes_of_standardTier` | public theorem | 3321–3333 | S10 | `theorem expandedRyCleanEntryForCubicAmplitudes_of_standardTier (tier : StandardRyCleanEntryScalarTier) (n : Nat) : expandedRyCleanEntryForCubicAmplitudes tier n` |
| 259 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude` | public opaque | 3334–3345 | S10 | `opaque expandedArithmeticComputesCubicAmplitude (n workspaceQubits : Nat) : Prop` |
| 260 | `QuantumBlockEncoding.CubicDiagonalOracle.ExpandedCubicArithmeticBackend` | public structure | 3346–3360 | S10 | `structure ExpandedCubicArithmeticBackend (n workspaceQubits : Nat)` |
| 261 | `QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend` | public def | 3361–3376 | S10 | `def symbolicExpandedCubicArithmeticBackend (n workspaceQubits : Nat) : ExpandedCubicArithmeticBackend n workspaceQubits` |
| 262 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendComputesCubicAmplitude` | public def | 3377–3390 | S10 | `def expandedArithmeticBackendComputesCubicAmplitude {n workspaceQubits : Nat} (backend : ExpandedCubicArithmeticBackend n workspaceQubits) : Prop` |
| 263 | `QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend_computes` | public theorem | 3391–3405 | S10 | `theorem symbolicExpandedCubicArithmeticBackend_computes (n workspaceQubits : Nat) : expandedArithmeticBackendComputesCubicAmplitude (symbolicExpandedCubicArithmeticBackend n workspaceQubits)` |
| 264 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendBridge` | public def | 3406–3411 | S10 | `def expandedArithmeticBackendBridge {n workspaceQubits : Nat} (backend : ExpandedCubicArithmeticBackend n workspaceQubits) : Prop` |
| 265 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude_of_backendBridge` | public theorem | 3412–3426 | S10 | `theorem expandedArithmeticComputesCubicAmplitude_of_backendBridge {n workspaceQubits : Nat} (backend : ExpandedCubicArithmeticBackend n workspaceQubits) (hBackend : expandedArithmeticBackendComputesCubicAmplitude backend) (hBridge : expandedArithmeticBackendBridge backend) : expandedArithmeticComputesCubicAmplitude n workspaceQubits` |
| 266 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendBridge_iff_of_computes` | public theorem | 3427–3447 | S10 | `theorem expandedArithmeticBackendBridge_iff_of_computes {n workspaceQubits : Nat} (backend : ExpandedCubicArithmeticBackend n workspaceQubits) (hBackend : expandedArithmeticBackendComputesCubicAmplitude backend) : expandedArithmeticBackendBridge backend ↔ expandedArithmeticComputesCubicAmplitude n workspaceQubits` |
| 267 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude_of_symbolicBackendBridge` | public theorem | 3448–3467 | S10 | `theorem expandedArithmeticComputesCubicAmplitude_of_symbolicBackendBridge (n workspaceQubits : Nat) (hBridge : expandedArithmeticBackendBridge (symbolicExpandedCubicArithmeticBackend n workspaceQubits)) : expandedArithmeticComputesCubicAmplitude n workspaceQubits` |
| 268 | `QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend_bridge_iff` | public theorem | 3468–3480 | S10 | `theorem symbolicExpandedCubicArithmeticBackend_bridge_iff (n workspaceQubits : Nat) : expandedArithmeticBackendBridge (symbolicExpandedCubicArithmeticBackend n workspaceQubits) ↔ expandedArithmeticComputesCubicAmplitude n workspaceQubits` |
| 269 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicPayload_lt_capacity` | public theorem | 3481–3492 | S10 | `theorem fixedDenomCubicPayload_lt_capacity (n : Nat) (j : Fin (gridSize n)) : j.val ^ 3 < gridSize (3 * n)` |
| 270 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicAmplitude_eq` | public theorem | 3493–3508 | S10 | `theorem fixedDenomCubicAmplitude_eq (n : Nat) (j : Fin (gridSize n)) : (j.val : Rat) ^ 3 / (gridSize (3 * n) : Rat) = CubicStatePreparation.cubicAmplitude n j` |
| 271 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend` | public def | 3509–3526 | S10 | `def fixedDenomCubicArithmeticBackend (n : Nat) : ExpandedCubicArithmeticBackend n (3 * n)` |
| 272 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend_computes` | public theorem | 3527–3545 | S10 | `theorem fixedDenomCubicArithmeticBackend_computes (n : Nat) : expandedArithmeticBackendComputesCubicAmplitude (fixedDenomCubicArithmeticBackend n)` |
| 273 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitudeTransparent` | public def | 3546–3557 | S10 | `def expandedArithmeticComputesCubicAmplitudeTransparent (n workspaceQubits : Nat) : Prop` |
| 274 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticRouteTransparent` | public theorem | 3558–3571 | S10 | `theorem fixedDenomCubicArithmeticRouteTransparent (n : Nat) : expandedArithmeticComputesCubicAmplitudeTransparent n (3 * n)` |
| 275 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend_bridge_iff` | public theorem | 3572–3585 | S10 | `theorem fixedDenomCubicArithmeticBackend_bridge_iff (n : Nat) : expandedArithmeticBackendBridge (fixedDenomCubicArithmeticBackend n) ↔ expandedArithmeticComputesCubicAmplitude n (3 * n)` |
| 276 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngle` | public opaque | 3586–3596 | S10 | `opaque expandedControlledRyUsesCubicAngle (n workspaceQubits : Nat) : Prop` |
| 277 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngleTransparent` | public def | 3597–3607 | S10 | `def expandedControlledRyUsesCubicAngleTransparent (n _workspaceQubits : Nat) : Prop` |
| 278 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomControlledRyRouteTransparent` | public theorem | 3608–3621 | S10 | `theorem fixedDenomControlledRyRouteTransparent (n : Nat) : expandedControlledRyUsesCubicAngleTransparent n (3 * n)` |
| 279 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyBackendBridge` | public def | 3622–3627 | S10 | `def expandedControlledRyBackendBridge (tier : StandardRyCleanEntryScalarTier) (n workspaceQubits : Nat) : Prop` |
| 280 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngle_of_backendBridge` | public theorem | 3628–3643 | S10 | `theorem expandedControlledRyUsesCubicAngle_of_backendBridge (tier : StandardRyCleanEntryScalarTier) (n workspaceQubits : Nat) (hBridge : expandedControlledRyBackendBridge tier n workspaceQubits) : expandedControlledRyUsesCubicAngle n workspaceQubits` |
| 281 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyBackendBridge_iff_of_standardTier` | public theorem | 3644–3665 | S10 | `theorem expandedControlledRyBackendBridge_iff_of_standardTier (tier : StandardRyCleanEntryScalarTier) (n workspaceQubits : Nat) : expandedControlledRyBackendBridge tier n workspaceQubits ↔ expandedControlledRyUsesCubicAngle n workspaceQubits` |
| 282 | `QuantumBlockEncoding.CubicDiagonalOracle.ExpandedControlledRyWorkspaceReadonlyWitness` | public structure | 3666–3685 | S11 | `structure ExpandedControlledRyWorkspaceReadonlyWitness (n workspaceQubits : Nat)` |
| 283 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyWorkspaceReadonlyTransparent` | public def | 3686–3690 | S11 | `def expandedControlledRyWorkspaceReadonlyTransparent (n workspaceQubits : Nat) : Prop` |
| 284 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputed` | public opaque | 3691–3702 | S11 | `opaque expandedWorkspaceCleanUncomputed (n workspaceQubits : Nat) : Prop` |
| 285 | `QuantumBlockEncoding.CubicDiagonalOracle.ExpandedArithmeticCleanUncomputeWitness` | public structure | 3703–3730 | S11 | `structure ExpandedArithmeticCleanUncomputeWitness (n workspaceQubits : Nat)` |
| 286 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputedTransparent` | public def | 3731–3734 | S11 | `def expandedWorkspaceCleanUncomputedTransparent (n workspaceQubits : Nat) : Prop` |
| 287 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputedTransparent_of_witness` | public theorem | 3735–3740 | S11 | `theorem expandedWorkspaceCleanUncomputedTransparent_of_witness {n workspaceQubits : Nat} (w : ExpandedArithmeticCleanUncomputeWitness n workspaceQubits) : expandedWorkspaceCleanUncomputedTransparent n workspaceQubits` |
| 288 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicModAddSub_eq_self` | private theorem | 3741–3782 | S11 | `private theorem fixedDenomCubicModAddSub_eq_self {modulus workspace payload : Nat} (hWorkspace : workspace < modulus) (hPayload : payload < modulus) : ((workspace + payload) % modulus + modulus - payload) % modulus = workspace` |
| 289 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicComputeStep` | public def | 3783–3790 | S11 | `def fixedDenomCubicComputeStep (n : Nat) : Fin (gridSize n) -> (fixedDenomCubicArithmeticBackend n).Workspace -> Prod (Fin (gridSize n)) (fixedDenomCubicArithmeticBackend n).Workspace` |
| 290 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicUncomputeStep` | public def | 3791–3797 | S11 | `def fixedDenomCubicUncomputeStep (n : Nat) : Fin (gridSize n) -> (fixedDenomCubicArithmeticBackend n).Workspace -> Prod (Fin (gridSize n)) (fixedDenomCubicArithmeticBackend n).Workspace` |
| 291 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicComputeStep_matches_backend_on_clean` | public theorem | 3798–3806 | S11 | `theorem fixedDenomCubicComputeStep_matches_backend_on_clean (n : Nat) (j : Fin (gridSize n)) : fixedDenomCubicComputeStep n j (fixedDenomCubicArithmeticBackend n).zeroWorkspace = (fixedDenomCubicArithmeticBackend n).compute j (fixedDenomCubicArithmeticBackend n).zeroWorkspace` |
| 292 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicUncomputeStep_after_compute` | public theorem | 3807–3826 | S11 | `theorem fixedDenomCubicUncomputeStep_after_compute (n : Nat) (j : Fin (gridSize n)) (workspace : (fixedDenomCubicArithmeticBackend n).Workspace) : fixedDenomCubicUncomputeStep n j (fixedDenomCubicComputeStep n j workspace).2 = (j, workspace)` |
| 293 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomExpandedArithmeticCleanUncomputeWitness` | public def | 3827–3845 | S11 | `def fixedDenomExpandedArithmeticCleanUncomputeWitness (n : Nat) : ExpandedArithmeticCleanUncomputeWitness n (3 * n)` |
| 294 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomWorkspaceCleanUncomputedTransparent` | public theorem | 3846–3859 | S11 | `theorem fixedDenomWorkspaceCleanUncomputedTransparent (n : Nat) : expandedWorkspaceCleanUncomputedTransparent n (3 * n)` |
| 295 | `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalValueBackend` | public structure | 3860–3873 | S11 | `structure LinearDiagonalValueBackend (n workspaceQubits : Nat)` |
| 296 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalValueBackendComputesGridPoint` | public def | 3874–3888 | S11 | `def linearDiagonalValueBackendComputesGridPoint {n workspaceQubits : Nat} (backend : LinearDiagonalValueBackend n workspaceQubits) : Prop` |
| 297 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalValueBackend` | public def | 3889–3900 | S11 | `def fixedDenomLinearDiagonalValueBackend (n : Nat) : LinearDiagonalValueBackend n n` |
| 298 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalValueBackend_computes` | public theorem | 3901–3918 | S11 | `theorem fixedDenomLinearDiagonalValueBackend_computes (n : Nat) : linearDiagonalValueBackendComputesGridPoint (fixedDenomLinearDiagonalValueBackend n)` |
| 299 | `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalValueCleanUncomputeWitness` | public structure | 3919–3940 | S11 | `structure LinearDiagonalValueCleanUncomputeWitness (n workspaceQubits : Nat)` |
| 300 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalWorkspaceCleanUncomputedTransparent` | public def | 3941–3944 | S11 | `def linearDiagonalWorkspaceCleanUncomputedTransparent (n workspaceQubits : Nat) : Prop` |
| 301 | `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalWorkspaceCleanUncomputedTransparent_of_witness` | public theorem | 3945–3951 | S11 | `theorem linearDiagonalWorkspaceCleanUncomputedTransparent_of_witness {n workspaceQubits : Nat} (w : LinearDiagonalValueCleanUncomputeWitness n workspaceQubits) : linearDiagonalWorkspaceCleanUncomputedTransparent n workspaceQubits` |
| 302 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalComputeStep` | public def | 3952–3959 | S11 | `def fixedDenomLinearDiagonalComputeStep (n : Nat) : Fin (gridSize n) -> (fixedDenomLinearDiagonalValueBackend n).Workspace -> Prod (Fin (gridSize n)) (fixedDenomLinearDiagonalValueBackend n).Workspace` |
| 303 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalUncomputeStep` | public def | 3960–3966 | S11 | `def fixedDenomLinearDiagonalUncomputeStep (n : Nat) : Fin (gridSize n) -> (fixedDenomLinearDiagonalValueBackend n).Workspace -> Prod (Fin (gridSize n)) (fixedDenomLinearDiagonalValueBackend n).Workspace` |
| 304 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalComputeStep_matches_backend_on_clean` | public theorem | 3967–3975 | S11 | `theorem fixedDenomLinearDiagonalComputeStep_matches_backend_on_clean (n : Nat) (j : Fin (gridSize n)) : fixedDenomLinearDiagonalComputeStep n j (fixedDenomLinearDiagonalValueBackend n).zeroWorkspace = (fixedDenomLinearDiagonalValueBackend n).compute j (fixedDenomLinearDiagonalValueBackend n).zeroWorkspace` |
| 305 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalUncomputeStep_after_compute` | public theorem | 3976–3996 | S11 | `theorem fixedDenomLinearDiagonalUncomputeStep_after_compute (n : Nat) (j : Fin (gridSize n)) (workspace : (fixedDenomLinearDiagonalValueBackend n).Workspace) : fixedDenomLinearDiagonalUncomputeStep n j (fixedDenomLinearDiagonalComputeStep n j workspace).2 = (j, workspace)` |
| 306 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalCleanUncomputeWitness` | public def | 3997–4015 | S11 | `def fixedDenomLinearDiagonalCleanUncomputeWitness (n : Nat) : LinearDiagonalValueCleanUncomputeWitness n n` |
| 307 | `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalWorkspaceCleanUncomputedTransparent` | public theorem | 4016–4022 | S11 | `theorem fixedDenomLinearDiagonalWorkspaceCleanUncomputedTransparent (n : Nat) : linearDiagonalWorkspaceCleanUncomputedTransparent n n` |
| 308 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockExtracts` | public opaque | 4023–4034 | S12 | `opaque expandedAmplitudeOracleCleanBlockExtracts (n workspaceQubits : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) : Prop` |
| 309 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract` | public def | 4035–4043 | S12 | `def expandedAmplitudeOracleCleanBlockContract (n workspaceQubits : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) : Prop` |
| 310 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract_diagonal` | public theorem | 4044–4050 | S12 | `theorem expandedAmplitudeOracleCleanBlockContract_diagonal (n workspaceQubits : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) (h : expandedAmplitudeOracleCleanBlockContract n workspaceQubits block) : diagonalCleanBlockContract n block` |
| 311 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract_eq_target` | public theorem | 4051–4062 | S12 | `theorem expandedAmplitudeOracleCleanBlockContract_eq_target (n workspaceQubits : Nat) (block : Matrix (gridSize n) (gridSize n) Rat) (h : expandedAmplitudeOracleCleanBlockContract n workspaceQubits block) : Matrix.PointwiseEq block (cubicDiagonalTarget n).operator` |
| 312 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleSemanticContract` | public def | 4063–4067 | S12 | `def expandedAmplitudeOracleSemanticContract (n workspaceQubits : Nat) : Prop` |
| 313 | `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleSemanticContract_cleanBlock_eq_target` | public theorem | 4068–4079 | S12 | `theorem expandedAmplitudeOracleSemanticContract_cleanBlock_eq_target (n workspaceQubits : Nat) (h : expandedAmplitudeOracleSemanticContract n workspaceQubits) : ∃ block : Matrix (gridSize n) (gridSize n) Rat, expandedAmplitudeOracleCleanBlockExtracts n workspaceQubits block ∧ Matrix.PointwiseEq block (cubicDiagonalTarget n).operator` |
| 314 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate` | public def | 4080–4096 | S09 | `def primitiveAmplitudeOracleCandidate (n : Nat) : OperatorBlockEncodingCandidate Rat n` |
| 315 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_costTuple_eq` | public theorem | 4097–4107 | S09 | `theorem primitiveAmplitudeOracleCandidate_costTuple_eq (n : Nat) : ( (primitiveAmplitudeOracleCandidate n).cost.gateCount , (primitiveAmplitudeOracleCandidate n).cost.depth , (primitiveAmplitudeOracleCandidate n).cost.auxiliaryQubits , (primitiveAmplitudeOracleCandidate n).cost.oracleCalls ) = (1, 1, 1, 1)` |
| 316 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_unitary_from_contract` | public theorem | 4108–4113 | S09 | `theorem primitiveAmplitudeOracleCandidate_unitary_from_contract (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) : (primitiveAmplitudeOracleCandidate n).isUnitary` |
| 317 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_block_from_contract` | public theorem | 4114–4127 | S09 | `theorem primitiveAmplitudeOracleCandidate_block_from_contract (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) : (primitiveAmplitudeOracleCandidate n).blockContainsTarget` |
| 318 | `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleVerified` | public def | 4128–4135 | S09 | `def primitiveAmplitudeOracleVerified (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) : VerifiedOperatorBlockEncoding Rat n` |
| 319 | `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleClaim` | public def | 4136–4148 | S09 | `def amplitudeOracleClaim : ConstructionClaim` |
