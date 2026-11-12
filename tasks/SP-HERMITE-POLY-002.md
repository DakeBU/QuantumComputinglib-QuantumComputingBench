# Structure-exploiting polynomial-resource Hermite state preparation

Task id: `SP-HERMITE-POLY-002`
Kind: `statePreparation`
Mode: `exploratoryConstruction`
Evaluation mode: `full-abeis`
Status: `exact-real polynomial quantum-gate root compiled; classical compiler cost and uniform finite-precision export remain open`
Parent baseline: `SP-HERMITE-001`, public commit `129bc2ad38c8e82d259459607ef0aae601af3212`.

## Frozen scientific and resource target

Preserve the exact function, normalization and little-endian output of
`QuantumBlockEncoding.HermiteStatePreparation`:

$$
p_j=-\pi L+2\pi L j/2^n,\qquad
|\psi_{k,n,L}\rangle=Z^{-1/2}\sum_{j=0}^{2^n-1}g_k(p_j)|j\rangle,
\quad Z=\sum_j g_k(p_j)^2.
$$

Here `k` is natural, the physical family has `n >= 1` and `L > 0`, and
`g_k` is `exp(p)` for `p < -1`, the source's degree-at-most `2*k+1`
Hermite polynomial on `[-1,0]`, and `exp(-p)` for `p > 0`. The amplitudes
are function values, not their square roots. `q0` remains the least
significant output bit even if an implementation processes bits in another order.

The new objective is an explicit, deterministic gate family whose gate count,
depth, clean ancillary space and classical construction work are polynomial
in `n`, with all dependence on `k`, `L` and precision separately exposed.
An `O(2^n)` algorithm is correctness evidence only, not a search success.
Prove the family and resource bound; fitting finite resource points is not
an asymptotic certificate. No claim of optimality is requested.

Primary tier: exact ideal real-angle circuit semantics, with zero final
ancilla garbage and no postselection or unresolved preparation/value oracle.
Separately account for how the real parameters are obtained. A polynomial
real-arithmetic count is not automatically polynomial bit complexity.

Approximate variants remain separate proposals until a tolerance rung is
explicitly recorded. Their target stays the same state; report Euclidean
state error at most `epsilon`, all rounding/truncation/normalization errors,
gate-synthesis error, and the input representation of `L`. A small finite
floating-point error never authorizes an exact or uniform-error claim.

## Highest certified frontier and rejection rules

The new exact-real quantum tier is now proved by
`QuantumBlockEncoding.HermitePolynomialPreparation.exists_polynomial_preparation`:
for `n >= 1`, all `k` and `L > 0`, an actual primitive circuit has at most
`48*n*(2*k+6)^3` instructions, `ceil(log2(2*k+6))` reusable clean bond wires,
zero oracle calls, and the literal normalized target in the public
little-endian order. Every nonzero output bond sector is proved zero.
This is not acceptance of the full classical/finite-precision task.
`ConstructiveHermitePreparation.prepare_spec` now certifies a named
deterministic producer of this same circuit contract. See the
[cycle-03 result and remaining costs](../experiments/hermite-polynomial/CYCLE03-RESULT.md);
the earlier existence-result snapshot is retained separately.

`HermiteFiniteNorm.localSampleNorm_eq_sampleNorm` additionally supplies the
normalizer by local Gram contraction; no full amplitude table is needed for
this supplier. Its stated add/multiply schedule is bounded by `9*n*(2*k+6)^3`,
plus one square root. Computing core entries, basis choices and real angles
still requires separate classical cost accounting.

The reference circuit has `2^n-1` RY gates and `2*(2^n-1-n)` CX gates,
zero ancillas and zero oracle calls. Its exact root is
`QuantumBlockEncoding.HermiteStatePreparation.hermiteStatePreparation_complete`.
It is retained unchanged. Its proof of correctness does not meet this task's
new resource objective.

Reject as a polynomial construction: a hidden full amplitude/angle table;
a dense `2^n`-dimensional SVD/unitary completion; an uncharged arbitrary
controlled rotation; exponential offline preprocessing; a free oracle;
unaccounted postselection/amplification; dirty discarded workspace; or
relabeling numerical rank as an exact rank theorem.

## Cycle 1 independent forks

1. `MPS-01`: explicit finite-state/low-rank representation of piecewise
   polynomial and exponential samples; sequential isometries; small-register
   primitive compilation. No dense-vector input to the construction algorithm.
2. `MASS-01`: closed-form prefix interval masses from polynomial power sums
   and geometric tails; coherent arithmetic, rotations and uncompute.
3. `AUDIT-01`: exact-signature library retrieval and independent accounting of
   hidden exponential work, evidence stages and integration obligations.

These are insight-pool proposals, not certified parents or accepted solutions.
Recombination requires a named shared interface and explicit source lineage.
Read the candidate ledger and proof frontier before launching a successor.

## Evidence gates

- Source/formula agreement and basis/register convention.
- Finite discriminators over multiple `n,k,L`, used only for screening.
- Named Lean state-action, unitarity, cleanup and resource roots, followed by
  `lake build && lake build Tests` and complete-module publication checks.
- Executable construction without dense fallback, with independently saved
  QASM replay and precise resource/precision accounting.
- Classical scaling probes beyond statevector-simulable `n`, separately from
  the finite statevector correctness set.
- Website promotion only after the documentation gate; do not replace the
  public baseline with an unproved efficient claim.

## Durable search memory

- Population: `candidate-populations/SP-HERMITE-POLY-002.md`.
- Frontier: `proof-obligations/SP-HERMITE-POLY-002.md`.
- Raw cycles, worker packets and metrics: task-scoped `runs/` records.
- Append substantive attempts through `tools/qbe.py trial-log`; do not edit
  historical trial rows or acceptance records.

No-progress policy: one unchanged failed route is classified; a second attempt
must change a concrete mechanism or test a new discriminator. Repeated
controller-only cycles cannot count as mathematical advances. The master
reallocates work to a distinct unresolved interface instead of enlarging the
same prompt or introducing another orchestration layer.

## Uniform scalar completeness and saved rounding

The finite negative-exponential supplier now has a sufficient active degree
`4*T^2+2*T+1`, where `T` is its precision-dependent tail cutoff. Its checked
enclosure succeeds for every rational `q <= 0` and positive scalar tolerance.
This removes the previous unproved degree-allocation edge; it is neither an
optimal allocation nor a finite-bit runtime theorem.

The literal signed outward-rounding supplier also encloses chronological RY
updates on one fixed row pair and bounds the midpoint taken only at the end.
Both internal providers have distinct scoped review. Changing physical row
pairs, CX-interleaved full stages, dimension-aware operator transport, source
normalization and total finite-bit costs remain open.

The complete stored Gram module has an accepted source-blind decoder and a
distinct source-first reviewer. Its charged exact-real stored-data model does
not certify input production, machine caching, peak RAM or physical gates.
[Evidence and remaining obligations](../experiments/hermite-polynomial/precision/cycle15-staging-result.json).
No new certified population winner, full scientific root or main admission is
claimed. The efficient branch uses Lean 4.33.0; main migration still requires
the remaining changed-module, integration and reader gates.


## 18 October 2026 integration and finite-bit frontier

The contribution checkpoint `67b750fcf30ac988df0a66d7af8f27e51a0fb74d`
uses Lean 4.33.0. Fetched main remains
`af585d9cbbb299c1c8c48647627a2cb820ef536a`, Lean 4.29.1. Fifty current
whole-module source-correspondence records validate; RobinMatrix remains a
separately identified experimental-policy/integration obligation. This is not
main admission, deployment, or completion of the frozen scientific target.
See the [actual current evidence](../reports/lean-433-migration/c142-independent-freezes-and-async-cost-frontier.json).

The next Hermite work is actual consumption of the independently reviewed C23
source-coefficient cache in C22, and an explicit data-width bound for the
precision-dependent source degree. Both are unproved successor work at this
snapshot. Keep the C23 scalar/word bound distinct from rational bitlength/GCD,
full preprocessing, normalized error composition, circuit synthesis and the
independent executable-family gate. No new resource winner is selected.


### Subsequent local parameter proof and current full gate

The C147 allocated Taylor-index root subsequently compiled under Lean4.33.0
(31.844s), with its exact own-output definition/type/axiom audit passing
(23.328s). All4 new roots report only the ordinary3 axioms. This is
proved_locally, not the complete finite-bit resource/root certificate.
[Exact scope and evidence](../experiments/hermite-polynomial/precision/allocated-degree-budget-c147/README.md).

The PR merge snapshot b95220ce6ebe9b6b7a965b4437f43b26fb673c03 also completed
full library/Tests and original Hermite executable replay successfully; its
selected proof/replay Git inputs equal contribution67b750f. This is a real
current PR integration gate, not main merge, clean TCB, new finite-bit poly-SP
executable acceptance or resolution of the experimental publication conflict.
[Source association](../reports/lean-433-migration/c153-current-PRmerge-full-gate-association.json).


### Independent scalar review and actual cached-supplier type probe

The C147 arithmetic provider now has a separately frozen C151 independent
source-first mathematical/binder/definition review and C154 subsequent actual
runtime association review. Both support their bounded internal claims, with
inherited/dirty/transitive provenance limitations retained; neither grants
source-publication, clean-TCB or scientific ROOT credit.

C150 actual cache -> signed middle -> five-branch right table -> existing
stored-chain definitions typechecked in C155: three modules plus seventeen
candidate propositions, all exit0. Type formation is not a proof. C156 seals
their exact bodies/signatures before subsequent bounded proof search. The
400/816 proposed bounds and final cached same-run refinement remain OPEN.
Subsequently C159 actually compiled seven C157 primitive/right roots, including
rightEntry partial counter<=11, and a fresh-own-output exact-type/axiom consumer
(25.578s/24.531s), all seven ordinary-three axioms. This is proved_locally with
independent static review pending, not full producer/runtime/root acceptance.
[Exact compiled primitives](../experiments/hermite-polynomial/precision/cached-primitives-c157/README.md).
Kernel/left and captured-block setup/native/bit/GCD costs remain unaccounted.
[Exact original stages](../reviews/publication/migration-checkpoints-c158/README.md).

The asynchronous policy retains human choice for material unapproved trade-offs,
autonomous bounded same-contract work, typed immutable evidence, matched
acceptance endpoints and all observed failed/cancelled/stale cost. No measured
quantum proof-first/screen-first/dual-lane efficiency winner or production
scheduler change is claimed. Original finite-bit Hermite ROOT remains OPEN.


### Actual cached setup and signed-middle VALUE certificates

C168 closes the actual setup-value conjunction after an exact two-block proof-only
repair of C165's rejected dependent-Decidable rewrite attempt. Four cuts, the
full factorial-reciprocal tail, clipped value and midpoint match the unchanged
source, including R/delta zero/negative and T0/T1. Source/own-output type+axiom
gates pass (30.000s/22.406s); original exit1, recovery sorryAx rejection and all
warnings are retained. No executable body or public type was changed.
[Setup certificate](../experiments/hermite-polynomial/precision/cached-setup-c166/README.md).

C174 closes generic signed middle entries and actual C23 cache substitution to
C21 middleCoeffQ (24.688s/25.062s exact source/own-output gates). Both roots use
only the ordinary3 axioms, no added correctness premise. Independent C178
static review is a separate pending stage at this checkpoint preparation.
[Middle certificates](../experiments/hermite-polynomial/precision/cached-middle-values-c167/README.md).

Complementary C172 executable screening passed1456 exact rational entries in a
25.906s parent subprocess while symbolic authoring continued. The result was
withheld until author freeze. It is finite discriminator evidence, not theorem,
SP state/export acceptance or matched-endpoint strategy comparison. Unknown
CPU/model/tokens/peak-memory remain unknown.
[Finite evidence](../experiments/hermite-polynomial/precision/cached-middle-finite-c172/README.md).

C161/C164 primitive and C169/C173 setup static-then-runtime internal reviews are
now preserved in13 exact original members. No source-publication, ProofSeal,
clean-TCB/native-cost or scientific ROOT promotion. Cost400, cached whole-data/
chain/source integration and816 are next obligations, not silently accepted.
Kernel/left/captured setup, native/bit/GCD/synthesis and finite-bit ROOT remain OPEN.


### Actual cached same-returned-data chain and partial middle-cost certificate

C193 verifies five unchanged C156 VALUE roots: all actual right coordinates,
whole returned RationalData, Window, same cast/ofTable dependent chain and
literal original piecewise grid source. Source/own-output gates pass34.016s/
26.672s; five typed consumers and all five ordinary-axiom reports pass. Parent
read the five actual types and seven printed loaded bodies, not every proof
term. Independent C188 source-first review is frozen; C196 static comparison is
separate, not inferred from compilation.
[Same-chain values](../experiments/hermite-polynomial/precision/cached-chain-values-c187/README.md).

C189 verifies actual middleFromCache partial total<=400*(k+1)^2 with no new
public assumption (24.922s/23.093s source/own-output exact type+ordinary axioms).
All generated factorial/sign/guarded-sum/collect work in that eight-counter
annotation is retained. Independent C194 source derivation is frozen separately;
comparison to the actual proof is pending, not self-approved.
[Partial cost](../experiments/hermite-polynomial/precision/cached-middle-cost-c183/README.md).

C178/C184 middle static-then-runtime internal reviews retain six exact original
members. Source first and later runtime exposure are separate freezes, with
inherited/dirty-TCB and direct-dependency-not-loader limits unchanged.
[Independent stages](../reviews/publication/migration-checkpoints-c190/README.md).

Failures remain exact: rejected Sum/implicit-index proof attempts, precompiler
memory deferral, low-cap interpreter exhaustion, and rejected cost normalization
attempt. Four failed compiler processes consumed129.299 observed subprocess
seconds; this is not total workflow/model/CPU time. Unknown calls/tokens/CPU/peak
memory stay unknown. Fin-index repair changed only proof; final run used actual
restored headroom and original3GiB cap plus2GiB reserve. No finite-screen/family
endpoint substitution or universal efficiency winner is claimed.

Previous ba2afcc1 full CI39075097319 succeeded (library/Tests and original15-test
finite replay), not a new finite-bit family acceptance. New checkpoint CI is
unverified. Cost816/same-run, kernel/left/captured setup, native/bit/GCD/finite-bit
synthesis/export and scientific ROOT remain OPEN; four textbook final admissions
and main4.33 migration are still OPEN. Robin publication policy is unchanged.


### Same-returned-run conjunction and bounded asynchronous decisions

C211 now proves the exact last C156 internal statement: the SAME returned
producer value refines the original chain AND its SAME annotated cost obeys
the unchanged816-plus-actual-setup/traffic/ofTable bound. Source32.953s and
fresh own-output exact-type/ordinary-axiom consumer28.047s pass. No new public
premise, weakened contract or increased proof budget was introduced. This is
an internal partial-cost result, not physical one-evaluation/sharing or full
finite-bit/poly(n_p) preparation.
[Exact proof and preserved failure](../experiments/hermite-polynomial/precision/cached-same-run-c208/README.md).

Ten original members preserve C199/C208 and rejected C207 exit1/47.563s;
no failed olean or zero-row axiom report is promoted. Eighteen further original
review members preserve six separately frozen source/static/runtime stages
for prerequisite same-chain values and middle cost. Those prerequisite reviews
are not an independent review of this new conjunction or a clean TCB rerun.
[Independent stages](../reviews/publication/migration-checkpoints-c205/README.md).

HARNESS section8a now routes to the existing asynchronous policy: autonomously
select bounded same-contract methods; ask asynchronously for material target,
error/success/oracle/budget/application trade-offs; continue unaffected work.
Proof and finite screens may run concurrently with immutable bindings and
source-blind release barriers. Compare all three methods only at matched
acceptance endpoints, retaining failed/censored work and unknown telemetry.
No new production event scheduler, scoring or measured strategy advantage.

Actual setup cost remains OPEN: C210 source failed29.094s; C216 proof-only
successor failed22.5s at no-progress simp, zero roots/no accepted output. C217
is authored, not proved. C219's precompiler check rejected the changed HARNESS
context; no compiler started. This is documented context drift caused by this
policy entry, not mathematical refutation, and no pin was waived or rewritten.
The new context must be explicitly bound before further proof validation.

Priorc913 fullHermiteCI39076442370/job117524465547 succeeded: actual fullTests
3460jobs and original15-test saved executable replay; this is not a new
finite-bit family acceptance. New checkpoint fullCI is unverified. Robin source
publication conflict still blocks main4.33 admission; no policy approval/change,
mainmerge, deployment, branchdelete, scientificROOT or textbookfinaladmission.


### Closed setup annotation and first Gaussian integer invariant

C223 closes the exact C202 partial setup target, with no public premise:
total(rightSetup n R delta).cost<=81*(d+1)^2+8*(d+1)+n+T+22,
d=sourceDegree(delta),T=tailCutoff(delta). Actual source27.422s, exact own-output
type/ordinary-axiom consumer24.969s, loaded-definition audit24.687s all pass.
Parent read actual type/axioms and loaded definitions, not every expanded root
proof or private recursive body.26 original seal/author/failure/preparer members
remain exact. C222->C224 is explicitly reviewed process-context succession with
the linked async policy additionally pinned, not a scientific/policy exception.
[Setup proof](../experiments/hermite-polynomial/precision/cached-setup-cost-c217/README.md).

The fixed Gaussian witness now has actual typed integer definitions and
independent source-first/static/successor-static review freezes. C225 original
Decidable failure remains; C227 adds only an explicit local constructive domain
decision, C228 types all31 names using its own table/core outputs. The final
literal1024 words and81local/eightsigned input diagnostics are parent-replayed,
not a uniform error/circuit proof. Apache-2.0/NOTICE and exact ancestry accompany it.
[Fixed model](../experiments/uncompute-2610-22367/gaussian-integer-model-c206/README.md).

C240 proves the exact C229 sealed all-D aligned128-block constancy theorem for
the actual integer model (source12.265s/own-output consumer9.859s, ordinary
axioms). It preserves six signed truncated middle rows, modular stored slope,
nine biased final rows and the special top-row drop. This is a symbolic integer
supplier, not finite screening or a replacement floor(full product), and not
Gaussian real-exp/f64 error, coherent circuit/cleanup/resource or SP/BE closure.
[Constancy proof](../experiments/uncompute-2610-22367/gaussian-constancy-c230/README.md).

Main migration diagnostic C234 actually compiles unmodified main Robin against
the4.33 context: exit1/86.344s, seven type/recursion errors, no accepted output.
Thus simply keeping that old file does not solve migration in this context.
No production source was changed. The separate experimental/source-publication
conflict remains; human approval for maintenance-rule design/review is pending.

Previous268522fc fullHermiteCI39078495808/job117530481115 terminalSUCCESS:
actual Tests3460jobs and original15-test finite replay. This is not the new
experimental proof set or a uniform finite-bit family acceptance. Current
checkpoint CI remains unverified; main4.29.1/fullHermitefinitebitROOT and four
bounded textbook final admissions are OPEN. Kernel/left/capturedsetup/native
bit/GCD/evaluator/synthesis/cleanup/export remain missing; C237 now designs the
literal fully costed kernel/left producer, not a return to the old2k+6 layout.


### Explicit five-block producer: typed sealed frontier, not a cost proof

C243 replaces the previously unaccounted kernel/left scalar callbacks with
literal comparison, factorial-binomial, charged powers/products and complete
materialization. Numerical loop dimensions use the actual second charged
cutoff result. The five-sum index, reflected signs, actual right boundary and
same returned data/cast/ofTable are retained; no canonical2k+6 layout replaces D.
C246 fails one dependent cast (exit1/28.671s), preserved unchanged. C248 changes
only that cast. C249 types source24.750s and own-output consumer24.063s; eight
Prop formations are NOT eight proofs. C250 seals exact bodies/statements BEFORE
new value/cost authoring. No new proved root or complete budget is claimed.
[Exact typed checkpoint](../experiments/hermite-polynomial/precision/explicit-five-block-c243/README.md).

C245 independent original-source baseline precedes C247 static comparison;
parent whole-read,31/40 raw pins respectively verified. This supports literal
semantics and branch-local ledgers, not full budget, proof/runtime association
or universal source-publication admission. Six original review members remain
frozen. C248 successor review and C252/C253 value/cost proofs are separate work.
[Review scope](../reviews/publication/migration-checkpoints-c254/README.md).

C244 isolates Gaussian's ACTUAL math.exp/half-away/centered429 reference. Negative
fold partners require the inclusive magnitude endpoint2^35 via valid xs=-2^35.
The compressed uniform route still needs119,275,520 quadratic blocks and an
operational monotonicity/enclosure supplier; sparse/NumPy scans are not enough.
The four-point/capped preflights are proposed, not executed. No refit/recenter,
source-target swap or uniform/circuit/error/resource/SPBE acceptance occurred.
[Operational reference audit](../experiments/uncompute-2610-22367/gaussian-error-reference-c244/README.md).

Priorc661 fullHermiteCI39079883741/job117534493326 now terminalSUCCESS: parent
actual logs read, Tests3460jobs23:57:45UTC, prooftrust0holes/axioms23:57:46,
15original finite replay tests23:58:02. This is the production frontier/baseline,
not the new experimental supplier or a uniform finite-bit family certificate.
Current checkpoint fullCI remains unverified; main4.29.1/Robin publication
conflict, fullHermitefinitebitROOT and four textbook final admissions stay OPEN.
No verifier/scoring/target/publication-policy/history/user-file/branch mutation.


### Same-return explicit cost checkpoint and asynchronous choice boundary

C263 actually closes the C250-sealed cost/counter projection for the SAME
explicit five-block result: source44.391s, separate exact-statement own-output
consumer26.968s, one public root, ordinary propext/Classical.choice/Quot.sound.
Actual selected quotient/remainder counts each <=14(n+1)D^2+4D and the full
named finite-operation frontierBudget are proved without added cache/F/value/
cost promises. C256/C259 normalization failures and C253/C258/C262 exact
source lineage remain immutable. Independent proof review is still PENDING;
source-only transport review C251 is not retroactive review of this new proof.
[Focused cost certificate](../experiments/hermite-polynomial/precision/explicit-five-block-cost-c262/README.md).

C257 gives separate source-derived canonical Rat data/working/raw-witness
height envelopes, with actual signed suffix/common-denominator invariants.
Parent whole-read and21direct+40retained hash checks match. Exact primitive
Sites coverage, Statement Seal and Lean height proofs are NOT supplied.
Native GCD/bigint scratch/control/evaluator/allocation, radius encoding, QR,
angles/gates/cleanup and full finite-bit SP remain OPEN.
[Bit-growth design, not proof](../experiments/hermite-polynomial/precision/rational-bit-growth-c257/README.md).

The value lane is separate: C260 scalar exit1/28.078s, C261 normalization then
C266 scalar exit1/28.672s; current remaining error is nested inverse-equivalence
normalization. Compiler recovery sorryAx is REJECTED, no accepted own value
supplier/root. C265 parent-wrapper schema failure occurred BEFORE any compiler,
was preserved, and C266 uses the original frozen root list with unchanged
consumer/signatures/caps. These are implementation failures, not mathematical
refutations. No old cached cost ledger is substituted for this new producer.

The human's asynchronous method-choice policy is already in HARNESS8a and
the bounded asynchronous design: autonomously choose bounded discriminators
inside the fixed contract, ask asynchronously for changed target/error/success/
oracle/budget or incomparable application trade-offs, and continue only
unaffected authorized work while waiting. Compare proof-first, screen-then-proof
and dual-lane at the SAME evidence endpoint with failures/censoring and TOTAL
cost. The14 isolated timing tests pass again; they establish no quantum-search
efficiency winner. No production event scheduler or score change was made.

C254 actual fullHermiteCI39081435433/job117538996204 is terminalSUCCESS:
Tests3460jobs00:22:37UTC, prooftrust0holes/axioms00:22:38,15original baseline
finite export tests00:22:53. This is not acceptance of the new experimental
cost proof or uniform finite-bit family. Research-publication CI still fails
on Robin alone; main stays4.29.1 and maintenance-rule human choice is pending.
Current new-head full CI remains unverified. No merge/deploy/branch deletion,
verifier/scoring/target/publication-policy/history or user-file mutation.

Append-only privacy clarification for C254's historical shorthand: its public
inventory is30 EXACT original archive members PLUS1 explicitly path-redacted
diagnostic member, not31 byte-identical originals. Original private receipts
are preserved, and source-binding/report record the exact redaction and hashes.


### Canonical height foundation proved locally; explicit cost independently reviewed

C278 actually types the exact canonical Rat height/unreduced-witness definitions
and four closed targets (12.094s+12.281s). C280 freezes exact bodies/statements
BEFORE C282 first-root proof authoring. C285 source0/11.781s and separate exact
expanded own-output consumer0/12.156s close ONE root, heightBound: h(q)<=B iff
1<=B AND abs(q.num)<2^B AND q.den<2^B, for all q/B including zero and signs.
Actual consumer selects the fresh own output and prints ordinary3axioms for
root and expanded assignment. Source zero axiom rows are not an empty proof.
Common-denominator/primitive-representation/primitive-width targets remain OPEN,
as do actual suffix/Sites coverage, producer-wide bit height and native costs.
Independent source-first height review C288 is separately frozen; not yet
author/runtime-associated or public-admitted. This is proved_locally, not ROOT.
[Exact height checkpoint](../experiments/hermite-polynomial/precision/rational-height-c269/README.md).

C264 independent actual-operation derivation froze BEFORE reading C262 proof;
parent whole-read,44raw/retainedlength/hashchecks match. C273 subsequently binds
that exact source to C263 own output/exact consumer/type/ordinary root axioms
and actual selected directdeps; parent whole-read,34direct+10private member
pins match. No concrete omission/association mismatch found. This completes
scoped internal static review+recorded-runtime association, NOT universal
source publication, independent rerun, complete loader/cleanTCB or fullSPBE.
Historical C263 receipt is not rewritten to upgrade its old review status.
[Separate freezes and limits](../reviews/publication/migration-checkpoints-c287/README.md).

The value lane remains REJECTED: C270 scalar exit1/28.015s; C272 explicit
instantiation reaches first inr but rw cannot see the term under its match.
C275 isolates a probe; C279 exit1/27.938s. C281 adds only rfl; C284 probe
exit1/27.016s explicitly rejects definitional equality despite apparently
matching ordinary print. The prior alpha-only explanation is NOT accepted.
No probe-own-consumer/scalar/chain ran after probe failures; zero accepted own
VALUE roots. All frozen authors and actual failures are retained in68members.
Full explicit-type diagnostics are separate work; this is implementation
failure, NOT a mathematical route obstruction or compiler-bug conclusion.
[Recoverable value/failure checkpoint](../experiments/hermite-polynomial/precision/explicit-five-block-values-c252/README.md).

Prior6c33fullHermiteCI39083056338/job117543833064 is terminalSUCCESS: actual
complete logs read, Tests3460jobs00:46:00UTC, prooftrust0holes/axioms00:46:01,
15ORIGINAL finite baseline tests00:46:13. This does NOT accept new experiments
or a uniform finitebit family. PublicationCI39083056333/job117543833032 still
fails only missing Robin record;50valid/51changedproductionmodules, main4.29.1,
human compatibility-maintenance choice pending. Current new-head CI unverified.
No verifier/scoring/target/policy/history/user-file change, merge/deploy or
branch deletion. Full Hermite finitebit ROOT, four textbook final admissions
and Gaussian operational/circuit/resource/SPBE ROOT stay OPEN. Async matched
three-arm strategy superiority remains unmeasured; ordinary fixed-contract
method choices autonomous, material assumption/budget choices ask the user.


### Common-denominator foundation locally proved; independent first-height review completed

C296 closes the second C280 rational foundation commonDenominator against the
exact signed/zero canonical Rat and unreduced commonWitness definitions.
Actual source0/13.172s -> own proof15c8671c... -> exact expanded own-output
consumer0/12.188s, two ordinary3axiom rows (root plus assignment, ONE root).
The local conditions Q>0, den(q) divides Q, abs(q)<=M are witness bridges,
not new scientific-target premises. Primitive representation/width, actual
suffix invariants, complete Sites coverage and producer-wide nativebit/GCD/
allocator/CPU bounds remain OPEN. Independent common-denominator review is
separate; this new root is proved_locally, not source-publication or fullSP.
[Exact proof and immutable original receipts](../experiments/hermite-polynomial/precision/common-denominator-c293/README.md).

C288 source-first -> C290 author/static comparison -> C291 recorded-runtime
association are separate immutable freezes for the earlier heightBound root.
Parent whole-read and rehashes match13/19/31direct input bindings respectively,
plus10private C291 runtime members. No concrete focused mismatch was found;
not an independent rerun, fresh universal decoder, complete loader/cleanTCB
or main/publication admission. Old pending-review receipts remain historical.
[Scoped height review](../reviews/publication/height-foundation-checkpoint-c300/README.md).

C283 actually forms three unchanged allocated partial-ledger targets in
27.968s+27.859s. C295 exact preproof seal then freezes them before any proof
authorization. M=n+1+2k+tailCutoff(eps/(4(k+1)^2)); proposed 5e6*M^7 operation
and5e5*M^5 selected-index bounds are NOT proved. Types/manual coefficients
are not nativebit/quantum-resource/value/root certificates.
[Typed and sealed, zero proofs](../experiments/hermite-polynomial/precision/allocated-polynomial-interface-c276/README.md).

The bounded asynchronous organization remains fixed-contract autonomy plus
user choice for material scientific/oracle/error/success/budget trade-offs.
Proof and finite screening may run concurrently for distinct uncertainties;
matching contract/revision/evidence endpoints and TOTAL consumed cost are
required for comparisons. No three-arm quantum strategy winner is measured,
and no production scheduler/scoring/verifier change is installed.

Current c221 publicationCI39084745643/job117548849697 actual complete logs
read: changed-module gate fails only missing RobinMatrix reviewed record.
Stateprep smoke39084745652 and fastwebsite39084745615 pass. FullHermite
run39084745630/job117548849683 was still compiling when this note was formed;
completion is separately required before pushing the same ref. Main remains
Lean4.29.1; contribution4.33.0. Compatibility-maintenance policy choice remains
unanswered; no waiver or false source record. No mainmerge/deploy/branchdelete.
Hermite finitebit ROOT, four textbook admissions and Gaussian operational
error/circuit/phase/cleanup/resources/SPBE root remain OPEN.


### Actual primitive representation and allocated dyadic-scale roots; chain remains open

C309 accepts the unchanged C280 primitiveRepresentation target, including all
signed/zero/add/sub/mul/div actual raw witnesses. Source0/18.531s -> own
ebf25188... -> exact expanded own-output consumer0/16.625s; root+assignment
ordinary3axioms. C303 parser failure0acceptedroots is preserved; C305 changes
only notation to explicit Rat.divInt, consumer byte-identical. This does NOT
prove primitiveWidth, actual suffix/Sites coverage or producer-wide nativebits.
[Actual representation proof and preserved failure](../experiments/hermite-polynomial/precision/primitive-representation-c305/README.md).

C307 accepts C295's FIRST exact scale target: with n_p=n+1 and the original
M=n+1+2k+tailCutoff(eps/(4(k+1)^2)), M<=n_p+4k+2+tailCutoff eps for all k,n
and positive rational eps, including eps>1. Actual source0/43.234s -> own
6e7f984f... -> operationScale-expanded exact ownconsumer0/40.562s ordinary3.
Original unused/unreachable/sequencing/defProp warnings retained. Two other
C295 polynomial budget/same-run roots are NOT proved by this packet. Native
Rat/GCD/CPU/allocator, finite-angle/quantum gates/cleanup/export remain OPEN.
[Exact scale proof](../experiments/hermite-polynomial/precision/allocated-dyadic-scale-c306/README.md).

C299 independently reconstructs CommonDenominator before C293 proof release;
C302 then compares author source; C308 later associates C296 raw runtime.
Parent whole-read23/24/43direct inputs+10private raw members and payloads MATCH.
No concrete scoped source/type/axiom mismatch. Recorded association is NOT
independent rerun, clean loader/TCB or source-publication admission. Init path
vs prefix provenance limitation and defProp warning remain. Old receipts
are not rewritten. [Separate review freezes](../reviews/publication/common-denominator-checkpoint-c314/README.md).

Value progress is precise: C301 closes probe/own-consumer and THREE scalar
roots (decode/comparison/actual factorial translation), using the unchanged
C275/C281 scalar that earlier failed probes had prevented from running.
C301 chain fails3interfaces. C304 proof-only successor clears the right-index
transport goal, but C313 source exit1/57.734s rejects two remaining interfaces:
column rewrite fails under implicit transparency because assemblySize/fiveSize
carrier types differ syntactically; final dependent cutoff/degree carrier
normalization still fails. No accepted C313 own chain, no final consumer run,
compiler-recovery sorryAx rejected. Keep prior THREE scalar roots, not seven.
This is implementation failure, not scientific impossibility/compiler bug.
[Exact success/failure boundary](../experiments/hermite-polynomial/precision/explicit-value-refinement-c313/README.md).

Current ee6a publicationCI39085996428/job117552571755 actual complete logs read:
fails only RobinMatrix missing reviewed record.50valid/51changedproduction
modules, main4.29.1, contribution4.33.0. FullHermite39085996387/job117552571580
is live at preparation; do not cancel it with premature same-ref push. No
maintenance-policy approval, waiver, mainmerge/deploy/branchdelete or production
behavior/target/scoring/verifier/history/user-file change. Hermite finitebit
ROOT, four textbook admissions and Gaussian operational/circuit/resource/SPBE
ROOT remain OPEN; async strategy superiority remains unmeasured.


### Actual polynomial partial-ledger envelopes and all raw primitive widths locally proved

C316 closes BOTH remaining C295 targets against the unchanged actual sourceDelta
and SAME returned produceExplicitStored result. Source0/43.875s -> ownab75d04e...
-> exactownconsumer0/36.391s ownc5a4d475..., ordinary3axioms on2root+3provider
rows. For M=n+1+2k+tailCutoff(eps/(4(k+1)^2)), total partial ledger<=5e6*M^7
and selected quotient/remainder calls each<=5e5*M^5, allk/n,positiveRat eps,
allRat R. Intermediate facts are proved, not public assumptions. Combined
with prior scaleDyadicBound, all3C295 local suppliers now pass focused gates.
[Exact allocated ledger proof](../experiments/hermite-polynomial/precision/allocated-polynomial-ledger-c311/README.md).

C325 closes primitiveWidth, the FOURTH C280 local foundation: source0/21.312s
own05ceefc5... -> original expandedexactownconsumer0/17.375s own83bdc961...,
root+assignmentordinary3. All listed raw intermediates retained, signed/zero
division and add/sub carry1 unchanged. C318 membership endpointfailure and
C322 localwidth unfoldingfailure are preserved; C324 changes only4finalsimp
calls after C321's4membershiplists. C323 separately discloses C321 inherited
ancestor outputs metadata; current authorfreezepayloads/stagesource, not that
array, bind actual source. C324 fresh outputs correct and all old bytes stay.
[Exact width proof and failure lineage](../experiments/hermite-polynomial/precision/primitive-width-c324/README.md).

These are THREE new locally proved suppliers, NOT all native/quantum resource
costs or full state preparation. Actual source-suffix denominator/magnitude
invariants, complete primitive Sites coverage and producer-wide bit heights
remain OPEN. Rational epsilon input height can grow with fixed cutoff (e.g.
(2^B+1)/2^B>1), so native input/GCD/ceil/clog/index/allocator/CPU work cannot
be inferred from M counters. Radius height, finite QR/angle synthesis/gates/
depth/cleanup/export and global normalized-state/error acceptance remain OPEN.
Independent reviews/source-publication/main/reader/PURIFIED not claimed.

C315 exactC313 carrierforensics parentwhole-read31inputs+6private members+
2payloadsMATCH: hidden assemblySize/fiveSize product widths and whole dependent
QData cutoff/degree carriers need synchronized typing, not a new mathematical
premise. Prior THREE scalar VALUE roots remain; no accepted chain. C319 new
two-carrier author checkpoint is frozen but actual gate PENDING; not success.
[Forensic evidence, not a repair certificate](../reviews/publication/chain-carrier-forensics-c326/README.md).

Current fef8 publicationCI39087045546/job117555679611 actual complete logs read:
fails only missing RobinMatrix record,50valid/51changedproductionmodules.
Main4.29.1 vs contribution4.33.0; maintenancechoicepending, no policy waiver.
FullHermite39087045543/job117555679666 live at preparation. No premature
same-refpush/mainmerge/deploy/branchdelete; no verifier/scoring/scientifictarget/
productionbehavior/history/userfile change. Hermite finitebitROOT, fourtextbook
finaladmissions, Gaussianoperationalerror/circuit/resource/SPBEroot stayOPEN;
matched async strategy superiority unmeasured. Full Goal stays ACTIVE.


### Actual producer VALUE chain and same-result partial-cost composition locally closed

C329 now closes the EXACT seven C250 VALUE interfaces. C319 source0/62.265s
-> own d515494b... -> unchanged full exact own-output consumer0/37.437s
own bd6fd1d9.... Nine private helper and seven public rows have only ordinary
axioms (comparison needs propext/Quot.sound, others ordinary3). Three scalar
roots were already accepted; FOUR chain VALUE interfaces newly close, not
seven new algorithms. Only two proof-body carrier conversions change from
C304; all sealed statements, executable definitions and scalar/consumer bytes
stay fixed. This closes actual QData equality, table window, chain refinement
and the rational-grid source action with its original R>0 premise.
[Exact VALUE refinement](../experiments/hermite-polynomial/precision/explicit-value-chain-c319/README.md).

C337 then closes the EIGHTH original C250 same_run proposition: correctness
and partial total/quotient/remainder bounds for the SAME literal returned
result. Unchanged C332 source uses And.intro of the accepted VALUE and cost
suppliers. Source0/37.563s own c41a071c... -> exact own-output consumer0/39.735s
own e7607a8f..., one source/four root-consumer-provider rows ordinary3.
C335's first attempt failed24.719s on missing transitive CachedMiddleCostProof
BEFORE theorem checking, zero accepted output/consumer not run. C337 adds the
pinned prior C263 cost path after the value path and verifies the cost context;
no source, target, cost, scoring, verifier or resource-cap change. Original
failed plan/result retained; raw feedback with an inherited local search path
stays private, and a separately hash-bound sanitized public derivative is used.
[Same actual result, not physical runtime](../experiments/hermite-polynomial/precision/explicit-same-run-c332/README.md).

This adds FIVE closed local interfaces (four VALUE plus one composition) on
the prior frontier, not a new algorithm or full poly(n_p) finite-bit result.
All8C250 and all3C295 local suppliers now compile with exact own consumers.
Partial M^7 operation/counter bounds still do NOT supply producer-wide operand
bits/common-denominator/magnitude/Sites coverage, native GCD/floor/ceil/clog/
index/CPU/allocator or physical once-only evaluation/sharing. Normalized-state
error, finite QR/angles, synthesized gates/depth, phase/clean-workspace and
independent family executable acceptance remain OPEN. New chain/same-run
independent review, clean transitive TCB, source-publication and PURIFIED remain
separate. Earlier failed receipts are immutable, not overwritten by success.

Two existing foundations now have scoped independent internal reviews:
C317 source-first -> C327 static -> C331 recorded association for dyadic scale;
C320 source-first -> C330 static -> C334 recorded association for primitive
representation. Parent whole-read and exact pins+10private runtime members
per root MATCH. Separate source/proof/runtime releases preserve anti-anchoring
barriers, with all previous authorship/partial-source exposures disclosed.
These are NOT fresh universal decoders, independent reruns or full loader/TCB
attestations. Old pending-review receipts remain historical.
[Scale review](../reviews/publication/dyadic-scale-review-c340/README.md) /
[Representation review](../reviews/publication/primitive-representation-review-c340/README.md).

Current de7b full Hermite CI39087980863/job117558461294 terminalSUCCESS;
actual complete logs obtained, relevant build/trust/finite sections read:
3460jobs at2026-10-18T02:06:07.5940969UTC; zero unapproved holes/source axioms
02:06:08.4306813;15ORIGINALfinite export tests02:06:20.4638003, independent
finite replay(k1,n3,L1)passed, lean_certificate_claimed=false. NOT new C340
or uniform finite-bit family acceptance. Current complete publication logs
39087980753/job117558460730 still fail missing RobinMatrix reviewed record
only:50valid/51changedproductionmodules. Main actual4.29.1, contribution4.33.0;
maintenance choice unresolved, no waiver/merge/deploy/branch deletion.
FullHermitefinitebitROOT,four textbook admissions,Gaussian operational error/
circuit/phase/cleanup/resources/SPBE ROOT remain OPEN. Matched asynchronous
strategy superiority remains unmeasured. Full Goal unchanged ACTIVE.


### Actual suffix targets typed/sealed; source input-height and normalized-error analysis

Recoverable WIP checkpoint, ZERO newly accepted mathematical roots. C338
inspects the literal producer's internal suffixes, k! common-denominator
strategy, signed middle denominator and radius/epsilon input bit heights.
Its proposed global bit-height envelope remains UNPROVED; hand-derived
stress families are not executed or Lean-certified evidence.
[Actual producer height strategy](../experiments/hermite-polynomial/precision/producer-height-analysis-c338/README.md).

C342 fixes the actual C23 factorial table and original recursive sumEntries
observations, including every dropped offset, next-tail connection and the
empty k=i=0 boundaries. C344 actually forms all3closedProps in39.610s+39.578s,
own f7e5fc3d... -> exact type consumer own62a9f346.... C345 then issues the
exact preproof Statement Seal. No mathematical proof follows merely from
Prop formation. Two distinct author proof branches are successor work,
not accepted by this checkpoint. No producer or resource model changed.
[Typed, sealed, unproved targets](../experiments/hermite-polynomial/precision/source-suffix-interface-c342/README.md).

C341 source analysis identifies the existing positive-Rat L/epsilon
normalized_original_error <=epsilon/2 and a necessary direct public-LE
adapter: wordIndex is LSB-first while sampleEquiv adds reversal. Reuse the
old error theorem rather than duplicate it or import the old exact chain's
bond/cost bound. IMPORTANT EXPLICIT CORRECTION: C341 incorrectly describes
the exponential argument as -p^2. Actual tails are exp(p) for p<-1 and
exp(-p) for p>0; middle uses exp(-1). Parent directly re-read the literal
definitions/proof. Inputs are still nonpositive, so enclosure domain and
existing error allocation are unchanged. Original erroneous bytes/hashes
are preserved together with a separate correction; hash integrity is not
semantic accuracy. No Gaussian target substitution is authorized.
[Source bridge analysis and explicit correction](../experiments/hermite-polynomial/precision/normalized-source-analysis-c341/README.md).

Producer-wide middle/Sites/operand heights, native integer/GCD/floor/ceil/
clog/index/CPU/allocation/sharing, original arbitrary-Real-L representation,
actual rounding/QR/angles/synthesis/phase/cleanup and independent family
acceptance remain OPEN. No scientific ROOT, new source publication, reader
seal or PURIFIED status. Four textbook admissions and Gaussian operational
error/circuit/resources/SPBE ROOT also remain OPEN.

Prior836b actual full HermiteCI39089118282/job117561835681 now terminalSUCCESS:
3460jobs2026-10-18T02:27:58.5312687UTC; proof trust0unapprovedholes/0sourceaxioms
02:27:59.5935468;15ORIGINALfiniteexporttests02:28:18.4866912; independent
finite replay(k1,n3,L1)passes with lean_certificate_claimed=false. Actual
complete logs obtained, relevant sections read; NOT new checkpoint build or
poly(n_p) finite-bit family acceptance. Current publication39089118289/
job117561835817 still fails ONLY missing RobinMatrix whole-module reviewed
record. Main actual4.29.1, contribution4.33.0,50valid/51changedmodules.
Maintenance policy choice unresolved; no waiver, main merge, deploy or
branch deletion. Async proof/screen policy retains fixed-contract autonomy,
material-choice user approval, exact event bindings and matched acceptance
endpoints/total-work comparison; no measured strategy superiority claimed.


### Two exact internal suffix roots locally proved; returned-cache join uncompiled

C352 fresh parent gate closes original C345 actualSuffix: literal actual
factorial table, every dropped sum=Ico, actual recursive tail=next offset,
zero offset=original sourceEntry, explicit empty branch. Source0/40.734s
own5c7a7631... -> complete expanded own consumer0/30.875s ownc84e4d26...;
source and two consumer rows ordinary3. C346 author first attempt failed
41.125s on two Fin/reindex elaborations; no own output or failed import.
Original source/plan/result and full private streams retained. Successful
author attempt and fresh parent run are separate; proof-only repair never
changes sealed targets/definitions. Public failure feedback is a separately
hash-bound privacy derivative, not a rewritten original.
[Actual recursive binding](../experiments/hermite-polynomial/precision/source-suffix-binding-c346/README.md).

C351 closes original suffixEnvelope, all k/i/s including empty and k=i=0:
canonical denominator divides SAME k!, nonnegative, precise remaining-count
bound(i+1-s)*2^(2k). Source0/39.609s ownbed2da08... -> complete expanded own
consumer0/36.547s ownbe0a7530..., ordinary3. Factorial/choose/finite-sum
facts are internal proof dependencies, not new source assumptions.
[Shared denominator and magnitude](../experiments/hermite-polynomial/precision/source-suffix-envelope-c347/README.md).
These are TWO new local suppliers, not a whole-producer bit/CPU theorem.

C353 third C345 returnedCache AND-join is authored but UNCOMPILED. C358
available3927MiB<3072+2048 reserve deferred BEFORE any Lean invocation.
C359 unchanged source/consumer/target lowered cap to1536 but kept2048
reserve; available3532<3584 again deferred BEFORE compiler/consumer. Zero
Lean attempts, not proof/API failure or mathematical obstruction. Both
original plans/results retained; no repeated cap-lowering loop, no user
application killed. The two accepted suppliers do not prove this WIP join.
[Uncompiled same returned-cache join](../experiments/hermite-polynomial/precision/returned-source-cache-c353/README.md).

C349 direct public-LE producer vector interfaces now actually typecheck in
C35439.703s+30.797s, ownb2a7b205... -> exact type ownconsumerae6fa88c....
C356 preproof seal follows: wordIndex direct-LE, actual returned chain's
Euclidean vector=finiteVector, existing allocated error<=epsilon/2 for
positive rationalL/epsilon. Eq.refl only checks Prop expansion: ZERO proofs
of these3targets. No reversal, dense executable table, source oracle or new
error allocation. Unused-k warning retained, no linter disabled. C357 new
proof chain is successor work, not accepted by this checkpoint.
[Typed and sealed direct-LE bridge](../experiments/hermite-polynomial/precision/public-le-producer-interface-c349/README.md).

Complete primitive Sites, signed middle/producer-wide operand heights,
native integer/GCD/floor/ceil/clog/index/CPU/memory/physical-sharing costs,
original arbitrary-Real-L input, actual finite rounding/norm/QR/angles/
synthesis/phase/cleanworkspace/export and independent family acceptance
remain OPEN. Internal focused proofs are not independent source review,
clean transitive TCB, source-publication/main/reader/PURIFIED or ROOT.
Four textbook admissions and Gaussian operational-error/circuit/resources/
SPBE ROOT remain OPEN. Fixed-contract async policy unchanged; strategy
superiority unmeasured, no verifier/scoring/runtime policy change.

Prior7f7297b fullHermiteCI39090933770/job117567343869 terminalSUCCESS;
complete logs obtained,relevant build/trust/finite sections read:3460jobs
2026-10-18T02:58:02.3702520UTC;prooftrust0unapprovedholes/0sourceaxioms
02:58:03.4198684;15ORIGINALfiniteexporttests02:58:19.4768695;
independentfinite replay(k1,n3,L1)passed,lean_certificate_claimed=false.
This is NOT new C355/fullfinitebitfamily acceptance. Current publication
39090933990/job117567344631 actualcomplete logs still fail missing
RobinMatrix whole-module reviewed record only,50valid/51changedmodules.
Main af585d9... actualLean4.29.1, contribution4.33.0. Maintenance policy
choice unanswered; no waiver, main merge/deploy or branch deletion.
