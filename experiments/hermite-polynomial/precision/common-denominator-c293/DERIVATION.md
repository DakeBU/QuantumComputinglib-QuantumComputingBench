# C293: literal common-denominator bridge, uncompiled candidate

Objective: exact C280 commonDenominator : CommonDenominatorSpec, separately
authorized after C285 heightBound. Primitive representation/width not authorized.

Let d=q.den>0, t=Q/d. Assumptions are exactly Q>0, d divides Q and |q|<=M.
Divisibility gives t*d=Q and d<=Q. Canonical abs_def gives |q|=abs(q.num)/d.
Multiplying the magnitude bound by positive d gives abs(q.num)<=M*d.
Nat casts reflect this order; no sign condition on q.num is required.

The actual witness numerator is q.num*t, denominator Q, with no replacement
witness. Canonical q*d=q.num and t*d=Q yield cast(q.num*t)=q*Q, hence
cast(q.num*t)/Q=q, using Q!=0. Denominator positivity is precisely Q>0.
natAbs_mul gives abs(q.num*t)=abs(q.num)*t <= M*d*t=M*Q.
Separately abs(q.num)<=M*d<=M*Q, and d<=Q. Nat.size monotonicity gives the
two canonical field-size caps. Applying C285 heightBound converts these caps
to its strict powers-of-two characterization; the outer maximum also ensures
the required lower bound1. The conjunction is returned in literal sealed order.

Boundary analysis, not executed diagnostics: q=0,M=0,Q>0 has witness0/Q and
height1; signed q changes no natAbs estimate. For q=-1/2,Q=6,M=1 the actual
witness is -3/6, magnitude3<=6 and canonical height2<=max(1,size6,size6)=3.
Q=1 forces d=1; no division truncation occurs because d divides Q. Q=0 is
outside the exact original premise, not silently assigned a valid witness.
Magnitude caps are nonstrict; the reused height equivalence remains strict
at powers of two. No counterexample to these sealed local conditions found.

Source graph: canonical positive denominator/absolute value -> integral
numerator bound -> actual common witness identity and magnitude -> field-size
caps. Lean graph additionally reuses HeightBoundProof.heightBound. This is a
foundational supplier, not actual suffix closure or a producer observation trace.
Q/M conditions are LOCAL bridge assumptions, not new producer/root premises.

Raw read audit: C280 all three files read whole, prior C269 literal definitions
retained; C282 HeightBoundProof read whole, no independent review read. Mathlib
Rat.Defs and Order.Ring.Unbundled.Rat read whole; Rat.Lemmas1-174, Ring.Rat1-105,
Field.Rat1-65, Nat.Cast.Order.Basic1-84 and Ring1-66, Order.Ring.Nat whole;
Nat.Size76-111; Order.GroupWithZero.Basic1125-1155; Int.NatAbs1-33 inspected.
Narrow raw-source name searches located div_eq_iff, cast/abs/divisibility APIs.
No C264/C273/value packets/current runtime/other new root proof exposed.

Evidence: one CommonDenominatorProof candidate, exact CLOSED fully expanded
consumer assignment, root and consumer type/axiom queries; no proof holes,
new axiom, altered producer, alternate desired-output definition or budget change.
Parent must compile against actual selected C285 HeightBoundProof and sealed
Definitions, then compile consumer against NEW own C293 output and check --deps.
No author compiler run or accepted root/axiom inventory claimed. API/elaboration
acceptance remains pending; preserve any failure as an implementation obligation.

qbe-substantive-worker handoff: C280_SECOND_COMMON_DENOMINATOR_ONLY; no competing
route or parallel worker; direct positive-denominator calculation is default.
Process memory: LOW-TOKEN-CONTROL-PLANE, VERIFIER-SEMANTIC-LEVEL; protocol intake
retained. Failure class NONE at mathematical design layer, compile pending by
task authority. Salvage: complete candidate pending gate, nothing weakened.
Purification/Exposition-Seal NOT_STARTED. No publication/root completion claim.
Canonical common witness is not GCD scratch/native allocation/runtime evidence.
Actual C23 suffix denominator/magnitude invariants and Sites coverage remain open,
as do full producer/native/evaluator/physical sharing/finite-SP/scientific ROOT.
Only new proof/consumer/derivation/manifest/freeze; all predecessor files preserved.
No compiler/scripts/Python/lake/Git/network/subagent execution. Freeze and STOP.
