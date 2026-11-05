# Saved rational RY interval provider — internal only

Objective / frontier node: actual signed RY/CX primitive semantics in the frozen
saved-action diagnostic, before parser/program/readout refinement.

Mathematical delta: for every exact rational physical angle theta and every
natural Taylor degree n, define q=theta/2 and the exact rational matrix
S=[[cosPoly(q,n),-sinPoly(q,n)],[sinPoly(q,n),cosPoly(q,n)]]. Its complex cast
has entry error at most delta=radius(q,n) against the existing standard RY.
The Euclidean induced operator error is at most 2*delta. The identical bound
holds for every named physical target and every spectator register size.
The explicit Euclidean continuous-linear-map bound supplies error at most
2*delta*norm(v) on every complex state vector. The surrogate is not assumed
unitary or normalized. All phases/signs remain literal.

Proof: S-RY(theta)=a*RY(0)+b*RY(pi), where a and b are the finite cosine/sine
errors at the actual half angle. FiniteTrig's unconditional Taylor theorem
bounds abs(a),abs(b) by delta. The existing PrimitiveSemantics matrices and
their named-wire lifts are unitary, so triangle inequality gives 2*delta.
This is not the false dimension-free entry-to-operator implication: the
local 2x2 factor is explicit. The spectator lift keeps the stronger same
bound because its exact error decomposition is retained.

Effect on root frontier: scalar trigonometric membership now reaches a literal
standard RY matrix and its actual named-wire gate semantics. This does NOT
identify the saved Python stage midpoint with S or close saved-plan action.

Named evidence: SavedRyInterval.lean (namespace HermiteSavedRyInterval),
ConsumerChecks.lean, test_saved_ry_interval.py; result-v2.json binds exact
source/dependency hashes and gate logs. The kernel regressions cover arbitrary
degree zero angle, theta sign, half angle, q0/q1/q2, a spectator mismatch and
the exact CX0->1 basis permutation. Actual first textual angle
-0.86958955523179937 is instantiated at the saved default degree 96.

Assumptions and conventions: theta,n are data; target and dimension binders
are typing-only. There is no Valid input, desired operator-error hypothesis,
clean-ancilla hypothesis, or phase quotient. Fin 2 is ordered 0,1; the
three-wire discriminators use existing primitiveBits3LE indices1,2,4.
CX uses existing cxBasisAction only in kernel diagnostics, not a new semantic
bridge or mathematical advance; the tautological zero-error helper is removed.
Existing unitary proof ingredients are dependencies, not inputs.

Files changed: only this new internal experiment directory; .lake compiler
outputs are local generated caches. No production or frozen packet edited.
No Git mutation by this worker.

Reusable cross-layer insight: the signed RY error structure avoids an
exponential spectator dimension factor while allowing nonunitary midpoints.
The executable exact test compares every distinct saved RY token's finite
Taylor supplier to saved_action's actual degree96 outward endpoints, without
silently erasing the rounding difference.

Failure class: NONE after focused stabilization. Early Complex coercion
simplification and Fin-case elaboration failures were IMPLEMENTATION_FAILED,
not REFUTED mathematics. A consumer invoked before a supplier olean existed
was dependency/environment evidence, not a theorem counterexample.
Salvage audit: the actual matrix/lift/CLM/vector roots are retained and
reachable; no failed theorem source, sorry or new axiom retained.
Process-memory IDs consulted: none applicable to this new primitive bridge.
Direction fingerprint: literal-rational-half-angle-to-signed-rotation-matrix-
linear-unitary-decomposition; expected information gain: replace missing
concrete operator supplier instead of restating a generic conditional bound.
Parallel admission: parent-assigned disjoint ownership; no child delegation.
Common-blind-spot audit: not performed; no independent reviewer claimed.
Default verified route: direct exact unitary decomposition, preserving the
actual signed scalar errors and named-wire semantics.
Purification / Exposition Seal: internal helpers have compiled consumers;
public purification and independent Exposition Seal are NOT claimed.

Remaining boundary: Python decoder/parser refinement, exact outward interval
operations and their primitive center, saved stage midpoint after ordered
gate chronology, full tensor/readout and saved-plan refinement, uniform
Hermite family, finite-bit cost and operation cost. The midpoint after the
entire interval stage is not the product of the raw Taylor midpoints.

Residual risk: focused evidence certifies exactly the formal primitive bridge;
it is not a scientific-root gate. Full repository build/Tests, source review,
integration and publication remain parent-owned obligations.
Recommended next independent fork: prove outward interval arithmetic and
the actual sequential row updates, then derive each stage midpoint error
from its full matrix entry enclosure before applying nonunitary transport.
Context digest: result-v2.json has exact hashes, toolchain, current read-only
HEAD, logs, namespace and remaining boundary. Re-run replay.ps1 or
freeze_result.py without changing the old saved-action packet.

Privacy chronology: unpublished initial result-v1/logs finished just before
the parent privacy warning. They were moved to ignored .private/run-v1,
recoverable locally and not staged. The safe v2 successor reruns all focused
gates with repository-relative commands and sanitizes ambient paths in logs.
