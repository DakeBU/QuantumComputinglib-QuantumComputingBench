# Source v2 clarification review, sealed before formal exposure

Source v2 SHA-256:
`91c442f1f8002be9d082257fbba0a79d551df3cdda499c6d1a2f539a686e0fd3`.
Proposal SHA-256:
`d91e7a2f355c3eb4b81d01a70d8763f7aa93207c9ec7c80a924b27a18ad5412c`.

This is a new natural-source-only supplement to immutable phase1. No formal
packet, decoder, author coverage, publication candidate, or other natural
review has been read at this point. The retrospective implementation-informed
provenance remains essential; this is not a pre-proof source or historical
paper correction.

## Independent principal-arccos derivation

Put rho=sqrt(x^2+y^2). If rho=0 then x=y=0 and alpha=theta=0 gives the
identity action on this pair. Otherwise rho>0. Since rho^2-x^2=y^2>=0,
|x|<=rho. Thus a=x/rho is in [-1,1], and beta=arccos(a) is well-defined
in [0,pi]. Its cosine is a and its sine is nonnegative. Also

    sin(beta)^2 = 1-a^2 = y^2/rho^2,
    sin(beta) = |y|/rho.

If y<0, alpha/2=-beta, so its cosine is x/rho and its sine is
-|y|/rho=y/rho. If y>=0, alpha/2=beta and the sine is |y|/rho=y/rho.
Consequently for theta=-alpha the source's block gives

    new x = (x/rho)x - (-y/rho)y = rho,
    new y = (-y/rho)x + (x/rho)y = 0.

For y=0,x>0, beta=0 and theta=0. For y=0,x<0, beta=pi and
theta=-2pi, whose half-angle block is -I on the selected two rows. This
is not a deletable zero-angle rotation. For x=0,y>0 the parameter is -pi;
for x=0,y<0 it is +pi. The signed preparation angle is now an actual
real-valued function, not merely a class modulo 4pi. This removes phase1 F2
for comparisons to precisely this representative.

## Partial interval and preservation

The descending sweep over t adjacent pairs guarantees zeros at
lo<i<=lo+t and leaves every row outside [lo,lo+t] unchanged. This follows
from the pair-zeroing result and the fact that later pairs lie strictly
above an already eliminated row. The prior N=3 partial-interval counterexample
is now correctly outside the guaranteed zero range. Older columns that are
zero throughout the interval remain zero there because each block acts on a
zero pair, with no dependence on that column's own angles.

The phrase "exactly the guaranteed rows" is read as specifying the guarantee's
range, not as asserting that entries elsewhere are nonzero. An iff assertion
about the zero set would be false for the all-zero matrix and is neither
needed nor warranted by this wording. No such nonzero assertion is accepted.

## Necessity, sufficiency, and minimality

F1 needs an interval qualification if the supplier accepts partial intervals;
the old global reading was false. The new qualification plus untouched-outside
rule is sufficient and changes no full sweep, because S2 always uses
lo=k,t=N-1-k. It is the smallest semantic correction: it does not alter the
visited pairs or add a premise to A.

F2 needs a fixed deterministic representative only if literal angle-record
equality is in scope. A principal-arccos representative is not the uniquely
necessary mathematical choice; any explicitly fixed compatible function could
serve the matrix theorem. The proposed two sign branches and origin branch
are sufficient, deterministic, and conservative, and resolve exact-record
underdetermination without modifying matrix action. The extra axis example
states a consequence rather than imposing a new condition.

Versioned provenance is necessary to prevent overwriting the prior findings
or implying a historical/pre-proof source. It changes no mathematics.

The S2-S7 recurrences, Prefix definition, actual-list action, strict lower
zeros, N*M list bound, arbitrary-list orthogonality and determinant, recovery
AND tails, and exact-real/non-runtime boundary remain unchanged. N,M may still
be zero; rank, nonzero pivot, isometry, normalization, and positive diagonal
are NOT added. In particular a terminal one-row sweep still leaves its
possibly negative entry unchanged, and zero-angle records remain counted.

The phase1 independent proofs therefore extend with the explicit angle
derivation above. All old source graph nodes retain their role. F1 and F2
are discharged as natural-source clarification issues only; actual formal
definitions and supplier certificates still need separate comparison.

Verdict: ACCEPTED as a necessary-in-purpose, sufficient and minimal/conservative
clarification of the retrospective source. This accepts the proposal's
precision, not a publication wrapper, unread implementation, compiled proof,
finite-bit resource theorem, or a uniquely mandated angle convention.
