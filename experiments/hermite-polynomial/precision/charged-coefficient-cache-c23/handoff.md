# C23 actual charged source-coefficient cache

Status: proved locally, awaiting independent review and parent integration gates.
No original source admission, scientific ROOT, full C22 runtime or finite-bit
claim is made. The formalizer has not fabricated an independent identity.

## Objective and mathematical delta

This bounded prerequisite returns one computable `Run (Vector Rat (k+1))`.
Every entry of that same returned vector is exactly the existing C21
`sourceCoefficientQ k i`, hence the actual `coefficientQ k i` for `i<=k`.
The same run has, for every ordinary operation category, cost at most
`52*(k+1)^2`, and total ordinary count at most `416*(k+1)^2`.
There is no desired-vector, desired-cost, oracle or correctness hypothesis.

Direction fingerprint: `C23_ACTUAL_CHARGED_SOURCE_COEFFICIENT_CACHE`.
Expected gain: replace repeated nonconstant source-coefficient formula evaluation
in the C22 scalar prerequisite with one stored polynomially bounded producer.
The cache is not yet installed into C22's middle/right-boundary evaluation.

## Construction and proof

Write `W=k+1`. Generate factorials through `2k+1` exactly once. At each extension,
read the last stored factorial, multiply by the stored next multiplier, add one
to that multiplier, and fully copy the vector with a charged comparison and
stored read at each copied entry. Initialization uses only the literal one.
Induction proves every table entry is its index factorial and the next multiplier
is the next natural number embedded in the rationals. There is no runtime call
to the specification's `Nat.factorial`.

For each `i` in `0..k`, sum the terms indexed by `r` in `0..i`.
Use three cached factorial reads and charged multiplication/division to obtain
`choose(k+i-r,k)` from the factorial quotient. The index inequalities follow
from the finite types; `Nat.cast_choose` proves the exact quotient identity.
Read the cached `r!`, divide by it, and perform a charged summation addition.
The finite-sum theorem returns precisely

`sum r in range(i+1), choose(k+i-r,k)/r!`.

Finally materialize all `W` source entries with inherited `collect`, whose two
passes charge two reads and two writes per result. The factorial cost is bounded
by `10*(2k+2)^2=40*W^2` per category. Each sum term has four stored reads and four
field operations including its summation addition, so the coefficient pass is
bounded by `12*W^2` per category, including collection. Adding the actual composed
counters proves `52*W^2`; summing the eight inherited categories gives `416*W^2`.
These bounds count actual rational operations, not arbitrary callback prices or
an unrelated output-size sum.

## Reuse and exact consumers

This is the small rational refinement of the existing
`StoredHermiteCoefficients.factorials/chooseFrom/sourceEntry/sources` mechanism.
Those APIs are monomorphic noncomputable real producers and cannot directly
provide a computable rational vector. `Run`, `tick`, `read`, `collect`, and the
exact factorial quotient theorem are reused. No second quantum representation,
MPS convention or complete source-cache API is introduced.

`produceSourceCache_real_sources` proves entrywise rational-to-real equality to
the ACTUAL existing real `sources` run supplied with the ACTUAL existing
`factorials` return. It does not compare to the Bernstein `compile` output and
does not pretend to transport its exponential primitive. The C21 actual
coefficient bridge remains a separately inherited dependency.

Primary roots in `ChargedSourceCache.lean`: `factorials_value`,
`factorials_cost_le`, `chooseFrom_value`, `sourceEntry_value`,
`produceSourceCache_entry`, `produceSourceCache_cost_le`.
Consumer roots in `CacheConsumerChecks.lean`: `produceSourceCache_actual`,
`produceSourceCache_real_sources`, `produceSourceCache_total_le`,
`same_cache_contract`.
All ten printed symbolic roots have only the ordinary logical axioms.
Native finite examples for `k=0,1,2,3` are supporting diagnostics, not the
parametric certificate and not included as claims of ordinary-axiom proofs.

## Evidence and failure discipline

`statement-seal-v1.json` freezes the initial Pascal mechanism; V2 freezes the
quadratic local-reuse mechanism before its proof search. Both have no EXCESS
binders. V1's source text is preserved as `attempt-pascal-v1.lean.txt`.
`negative-evidence-v1.json` records the warning-as-error launcher failure,
classified ENV_BLOCKED before Lean. `negative-evidence-v2.json` preserves the
first factorial elaboration failure, classified IMPLEMENTATION_FAILED and
explicitly discloses the missing failure-time source snapshot. Neither failure
retires mathematics; no failed sorryAx-bearing elaboration is admitted.
`negative-evidence-v3.json` and `negative-evidence-v4.json` preserve the two
verification-only cache-priority/namespace-root findings as ENV_BLOCKED; their
prior runner, input bindings and actual selections are retained.

`replay-v3.py` performs a bounded fresh-source gate in a unique private cache:
StoredGivens, Mathlib Choose.Cast, C21 ActualCoefficients, existing real
StoredHermiteCoefficients and both C23 modules. It records selected direct-import
cache paths/hashes and checks inherited C19/C20/C21 cache/source bindings before
and after. It does not rebuild the entire transitive graph. The C21
finite-middle `ConsumerChecks` cache takes precedence over the duplicate C20
module. Existing frozen caches and receipts are not overwritten.

The initial `replay.py` gate exposed lake's package-path precedence for namespaced
modules; its exact chosen imports are preserved, not relabeled fresh. V2 uses the
exact toolchain binary directly, but its incomplete project namespace was caught
before compilation because Lean resolves namespace roots. V3 supplies a complete
copied project namespace before the selected fresh provider compilations, pins
selected import companions pre/post, and asserts that the intended fresh project
providers really are selected. Mathlib Choose.Cast is freshly source-gated in
isolation; its consumer cache remains explicitly inherited. The mathematical V2
source is unchanged by either verification correction.

Source/provider, cache, seal, toolchain, manifest, frozen task, failed receipt and
successful receipt hashes are in `final-binding-manifest.json`,
`pre-gate-bindings-v3.json` and `focused-verification-v3.json`.
Private raw receipt hashes are separately recorded; public paths are relative.

## Frontier and preserved boundary

Resource tier: exact rational scalar/word operation counters. Rational addition,
multiplication and division, numeric table access, full-copy collection, and
extension comparisons are charged. Natural-index arithmetic, loop control,
fixed record projections and counter metadata remain outside this model.
Integer bitlength, rational GCD/reduction work, allocator implementation,
finite-bit accuracy and physical circuit synthesis remain open.

Also open: middleCoeffQ generation, expMidpoint/sourceDelta setup, translation
tables, cutoff/index setup, all actual local-entry/boundary arithmetic, cache
consumption traffic, full classical runtime, source error plus normalization,
canonicalization/isometries, sequential preparation and the original scientific
ROOT. q0LSB and the full signed Hermite source are unchanged.

Failure class for the final bounded mathematical slice: NONE.
Salvage: accepted local factorial/source/cost roots; rejected logs retained;
V1 Pascal text is evidence only, not reusable proof memory.
Process-memory IDs: QBE-PM-LOW-TOKEN-CONTROL-PLANE and
QBE-PM-VERIFIER-SEMANTIC-LEVEL. No new process-memory authority is inferred.
Parallel admission: parent-issued disjoint prerequisite; no subagents spawned.
Only one final verified mechanism survives, so no internal multi-route comparator
or common-blind-spot acceptance is fabricated. Default route is the quadratic
factorial cache because it reuses the existing mechanism and avoids the V1
cubic Pascal table. Alternatives are not mathematically refuted.

Purification: locally bounded, imports minimized, abandoned route kept only as
an explicitly rejected text artifact. Source/Lean expansion nodes are the exact
C21 source formula/actual bridge, inherited factorial quotient identity,
StoredGivens materialization and the ten roots above. Independent source-blind
review, full repository/site gates, global purification and Exposition Seal are
PENDING and belong to parent integration. No canonical ledger, production module,
Git state, task contract or old receipt was changed. No successor is opened.
