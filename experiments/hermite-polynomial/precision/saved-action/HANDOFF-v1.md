# Same actual saved action, full terminal bond: cycle13 handoff

Objective / frontier node: execute the previously DESIGN_ONLY same-return
saved-action frontier, with the full terminal bond retained and no dense
constructor/checker input. Direction fingerprint:
`same-actual-plan-full-garbage-saved-action-compact-TT-diagnostic`.

Mathematical/executable delta: an actual frozen OffsetSource `n=3,k=1,L=1`
raw TT C is passed once to `certify_scaled_canonicalize`, and its SAME returned
D is passed to ONE actual `compile_mps(D)` plan. The plan's real saved QASM2
contains 456 RY/CX instructions, stage counts 184/168/104, and two bond wires
(`B=4`). Repeated legacy QR/pruning/completion/atan2 are observed, not assumed
to preserve D. Actual C/D bytes remain unchanged by compilation. A separately
validated exact-rational local matrix chain follows those saved decimals in
chronological order and appends two deterministic readout cores. All 32
physical coordinates, including every terminal bond label, are included in
the residual. The target is literal signed E(D), not normalize(D).

The exact three-pass Gram residual has directed `r≈3.1592406234e-16`.
Interval dependency growth makes the conservative nonunitary product budget
`sigma≈1.1783693583e-13`, yielding `sigma+r≈1.1815285989e-13` as a candidate
bound to literal D under the still-open interpreter/primitive bridges. The
formula is `product(1+eta_i)-1`, not an unjustified sum. The same-return QR
candidate is separately composed against normalized stored C; ideal Hermite
source error is not supplied.

Named evidence: `result-v1.json`, SHA256
`c6ec9a792ceee64d17d8a419562aea473a8f1ec8c7f9a66511cedd53349c9e6a`,
binds source, preimplementation seals and actual runtime-generated fixture
bytes. `fixture-n3-k1-L1/saved.qasm` SHA256
`cc78a8231cddfa64be885704924fdb383b39968504ecbd24f22cb9f4194ccaf0`.
Fifteen focused tests passed. A fresh normal-producer fixture exactly matched
all six saved file hashes. The independent tiny Qiskit saved-file replay
(binary64 parser semantics, separate from primary decimal semantics) measured
Euclidean error to literal D about`2.0061325122e-15`, and garbage norm
about `1.8541264657e-16`. This replay is diagnostic only; no phase alignment.

Commands actually executed (repository-relative):

```
.venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-action/generate_fixture.py experiments/hermite-polynomial/precision/saved-action/fixture-n3-k1-L1
.venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-action/test_saved_action.py
.venv/Scripts/python.exe experiments/hermite-polynomial/precision/saved-action/freeze_result.py
```

Final results: generator exit 0; 15 tests PASS exit 0; freeze runner exit 0. The
result records exact commands, successful test output and measured run time.
All live handles are closed. Per-worker token use is unknown. No worker git
mutation was performed. Parent owns trial recording, checkpoint/push,
distinct review and repository build/publication gates.

Assumptions/conventions: physical q0 is LSB. TT word order is data n-1..0,
then bond a-1..0. Its explicit coordinate map is `j+2^n*b`, not generic
global-MSB ordering. Exact saved text angles are primary; original float
hex and parser dyadics are separately compared. No global phase quotient,
postselection, active-bond truncation or discarded garbage. Caps `n<=3`,
`B<=16`, 50000 saved primitives and bounded Taylor/text/operand precision are
operational limits, not restrictions on the scientific family.

Finite trig supplier: the separate worker's frozen `HermiteFiniteTrig`
proves unconditional all-rational Taylor membership with radius
`|q|^(m+1)/(m+1)!`; no free trig oracle or membership premise. This consumer
uses measured fixed-degree 96 recurrence and outward dyadic rounding, and
exactly crosschecks all 26 actual halfangles against that supplier's separately
frozen Python formulas. Membership proof does not prove this Python program,
parser, rounding or local quantum-stage adapter. Those bridges stay OPEN.

Work/evidence: 7 NumPy QR calls, 3 completion calls and 57 atan2 calls, with actual
shape/hash traces. The result retains rational field counts, decoded scalar
counts, stage row/permutation/output copies, endpoint comparisons, integer
grid/floor/ceil operations, numerator/denominator and pre-GCD bit maxima,
three-pass contraction budget and exact directed sqrt operands. Frozen
source/QR work is separately retained. Internal Fraction GCD steps, BLAS,
all scalar object allocation and full integer runtime are not instrumented;
no total finite-bit runtime theorem is inferred.

Adversaries: missing/extra files, corrupt hashes, malformed/altered angles,
missing/extra instructions, bad spans, cross-stage and reused-data wires
reject. Valid angle/sign/whole-stage order mutations change the residual.
An actual terminal-bond excitation yields residual above 1.4 and garbage
weight above 0.99. A dimension-valid readout-endian swap discriminates. Zero,
deficient/tall and empty-stage/no-ancilla cases, signed and unnormalized
targets, sqrt zero/tie/non-square and full readout labels pass. Early test
authoring mistakes (wrong stage-count expectation, commuting adjacent swap,
malformed adversarial nested-list index) were corrected without changing
producer fixtures; these do not refute a mathematical route.

Files changed: only new `precision/saved-action/` subtree. The original
design SHA and every frozen old source binding were verified before actual
generation. Frozen parent sources, previously failed tinyL/cutoff routes,
production/config/tests/registries and user files were not edited.

Failure class: NONE after local test-construction repairs. Salvage: the full
saved-action consumer, primitive interval schedule, literal pair residual and
readout discriminators are reusable experimental fragments; no production
promotion. Process memory: protocol plus source-specific retained design and
task packet; no unrelated negative-memory route consulted. Parallelism was
explicitly human-admitted for distinct uncertainties: this executable path,
the finite-trig mathematical producer and the nonunitary telescope lemma.
Common-blind-spot / source-blind review is pending, not claimed.

Effect on root: previously only designed full-garbage saved action is now an
actually replayed bounded finite candidate. `formalGate` and `executableRoot`
remain OPEN. Remaining: decoded Python/rational/parser/primitive refinement,
entry-to-operator and local-stage-to-chain refinement, readout bijection proof,
uniform ideal-source-to-C error/norm floor and total finite-bit cost.
PURIFICATION and Exposition Seal are pending; no ROOT, PUBLISHED or PURIFIED
claim. Recommended next fork: a distinct review of the pinned saved-action
packet, then a bounded formal local-stage/readout bridge on this same saved
word interface. Do not promote floating completion residual as circuit action.
