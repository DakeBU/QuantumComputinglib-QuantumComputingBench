# C311: allocated polynomial partial-ledger proof candidate

AUTHOR-UNCOMPILED. Exactly two separately authorized C295 roots:
allocatedBudgetEnvelope and allocatedSameRunPartialLedger.
C295 was issued before this proof; exact seal SHA256
8870a4cb0ec474a4b17979f2e4e334ec9b75bb123777d51eb7bf54a99f797d86.
Its three-signature file is copied unchanged; scaleDyadicBound is NOT authored,
imported as a proof, or needed here. Parent-reported C307 acceptance is unused.

Before this author action, C304 freeze6913539e49fa7c72a4d72fc25fadcab26f4e7e6fecf38258e46dc1e540dcb731
and all seven payload hashes were checked unchanged. C304 remains immutable;
its VALUE proof is not a dependency of this cost-only packet.

## Actual source reuse and closed parameter bounds

Set delta=sourceDelta k n epsilon and M=operationScale k n epsilon EXACTLY.
The physical width is n+1. No sourceDelta, desired degree, radius or error
allocation changes. epsilon is every positive rational, including >1.
R is every rational; no R>0/encoding-height/normalization promise is added.

C147 allocated_tailCutoff_le yields actual T=tailCutoff(delta)<=M;
allocated_sourceDegree_le yields actual d<=4M^2+2M+1.
The proof obtains M>=1, n+1<=M, k+1<=M and 2k+1<=M from literal operationScale.
Power monotonicity for base M>=1 is the raw Mathlib pow_le_pow_right' API.
Consequently M<=M^2, d<=7M^2, d+1<=8M^2, L=d+2k+1<=8M^2, L+1<=9M^2.

Original assemblySize_eq gives D=18d+9(2k+1)+45, hence D<=180M^2.
Squaring gives D^2<=32400M^4. The actual P=(n+1)(2D^2+D+1)+2D satisfies
P<=64800M^5+180M^3+M+360M^2<=65341M^5.
Also n+L+34<=43M^2 and L+61<=69M^2. All these are proved LOCAL facts,
not root hypotheses, callback requirements or additional public assumptions.
M>=1 covers n=k=0 and zero cutoff, including arbitrarily large epsilon.

## Literal frontierBudget, not a new resource model

Monotone substitution in all twelve original summands, followed by semiring
normalization, gives the explicit polynomial
2786400M^7+672084M^4+588069M^5+885M^2+10M+59.
Promoting powers using M>=1 bounds this by4047507M^7<=5000000M^7.
The actual selected cap14(n+1)D^2+4D is <=453600M^5+720M^2
<=454320M^5<=500000M^5. These coefficients were independently recalculated
from literal summands; C276/parent comparator numbers are not premises.
Lean gcongr/ring/omega text remains UNCOMPILED, not accepted arithmetic evidence.

For the second root, apply the CLOSED C262 produceExplicitStored_cost_counters
at the SAME actual delta and SAME returned result. Its total/frontier and
quotient/remainder-cap inequalities compose by transitivity with the first root.
There is no new value, Window, correctness, cost, F or normalization premise.
No scale comparison, real-log theorem or VALUE packet is imported.

## Exact consumer and implementation frontier

AllocatedPolynomialLedgerOwnChecks.lean checks both predicate aliases and
their FULL expanded forall/let statements, then prints root axioms, provider
types/axioms and actual parameter/budget definitions. This is a candidate
own consumer, not an executed or accepted one. Parent must select exact
providers and gate source + own consumer; printed source alone is insufficient.

Untested risks: import/provider routing, implicit-let/type elaboration,
gcongr side-goal matching, ring normalization and omega closure/performance.
No actual failure or successful C311 proof gate is asserted. No holes,
new axioms, native_decide, unsafe, trust/cap/linter override or target weakening.
If a gate fails, preserve exact source/output and stop for bounded direction.

Exposure: same earlier Hermite author/probe/failure work, not an independent
reviewer or fresh universal decoder. C276/C295 metadata mention their author's
C264/C273 reviews; those review files and independent cost outputs were NOT
opened. Canonical C262 source was explicitly authorized and read whole.
Mandatory whole skill/protocol intake is retained with matching current pins.
Selected raw hashes are not a complete loader/source-to-binary/clean TCB audit.

Only new C311 files via apply_patch; no compiler, scripts, Python, lake, Git,
network, subagents, review, finite diagnostic or historical/production mutation.
The bound is the literal partial eight-counter ledger and selected quotient/
remainder-call metadata, NOT all integer operations, Rat bitlength/GCD,
ceil/floor/clog/index/evaluator/CPU/allocation/captured sharing, finite-real
implementation, QR/synthesis/angles/gates/depth/cleanup/export or scientific
SPBE ROOT. No publication/main/reader/ProofSeal/purification credit.
Freeze and STOP; parent owns actual verification.
