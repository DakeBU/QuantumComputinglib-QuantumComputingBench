# C305: syntax-only successor to preserved C298/C303 failure

Objective/root: unchanged C280 primitiveRepresentation : PrimitiveRepresentationSpec.
C303 actual source gate exited1 in17.859s, zero accepted own roots, consumer not
run. Whole released feedback reports invalid dot notation in hpair line15,
followed by the unsolved goal containing parser-recovery sorry. That recovery
is not an accepted proof or mathematical counterexample; no own output exists.

Raw API check: Mathlib/Data/Rat/Defs.lean lines1-30 explicitly documents
Rat.divInt n d as the rational n/d and `/.` as its notation. Lines244-247
define intCast_div_eq_divInt using that same operation (retained prior read).
The ONLY source delta is the hpair expression:
`w.numerator /. (w.denominator : ℤ)` ->
`Rat.divInt w.numerator (w.denominator : ℤ)`.
All imports, public/private signatures, helper premises and tactics unchanged.
ExactChecks.lean is byte-identical to C298. EXACT_DIFF.patch records the line.

Mathematics remains the C298 canonical divisor/magnitude reduction and actual
four-operation witness equality, including signed and zero-divisor branches.
Source graph and Lean graph are unchanged; this repairs parsing only. It does
not prove primitiveWidth, producer/Sites coverage, native/GCD/scratch/runtime,
physical sharing, finite-SP or scientific ROOT claims. No new axiom or premise.

Evidence audit: whole released C303 feedback/result and whole own C298 proof,
consumer/manifest read; raw Rat.Defs1-75 reread. No review/cost/other-worker
packet or runtime archive opened. Exact string replacement and consumer hash
identity checked; all input/output pins separately bound in manifest/freeze.
No compiler/lake/scripts/Python/Git/network/subagent execution or new proof search.

qbe-substantive-worker handoff: direction C280_THIRD_SYNTAX_ONLY_DIVINT;
failure class IMPLEMENTATION_FAILED applies to preserved C303 parser failure,
not refutation. Salvage: entire original candidate retained with one explicit
API spelling repair; no discarded or weakened clauses. Remaining uncertainty:
parent compiler/elaboration and own-output exact type/axiom/dependency gate.
No accepted result asserted; parent must test this exact new source and consume
its NEW own output, not the failed predecessor. Full protocol intake and
LOW-TOKEN-CONTROL-PLANE / VERIFIER-SEMANTIC-LEVEL retained; no parallel route.
Purification/Exposition-Seal NOT_STARTED. Freeze and STOP.
