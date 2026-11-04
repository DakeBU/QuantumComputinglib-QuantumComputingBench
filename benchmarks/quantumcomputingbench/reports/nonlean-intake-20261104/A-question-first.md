# A1–A4 question-first mathematical reconstruction

Reviewer identity: `/root/nonlean_audit_normalization`. Scope: four questions, not formal verification or benchmark admission. Written before opening the delivered QA answer, rubric, or reasoning-map fields. The protocol and source context are not blind: the question-only packets themselves include source theorem signatures and proof descriptions, and the permitted repository sources contain proofs. Independence here means an answer-first payload comparison was avoided, not that the reviewer was source-blind.

Actual exposure before this artifact: repository `AGENTS.md`, `HARNESS.md`, substantive-worker skill, theorem-publication/proof-digestion/evidence-routed-memory protocols; `_out/cohort-question-only/A1.json` through `A4.json`; Git source of the five cited Lean modules at `86b9e677566498da04faebcf4e5ed57f177c6bb1`; relevant rotation definitions in `PrimitiveSemantics.lean` and `Robin/ComplexLCU.lean`; the existing release-v3 snapshot's `transport:be-to-sp`; filtered current `nl-v12/core-registry.json` statement summaries. An initial broad core-summary filter emitted a truncated large result because split-group text matched many entries; it exposed registry summaries and status metadata, not QA payload answer/rubric/maps. A narrow projection was then used. No colleague QA payload, review report, or verdict was opened.

Source binding: all five cited Lean file SHA256 values agree exactly with `git show 86b9e677…:<path>`. The snapshot file is not itself present at that Git commit (the attempted `git show` failed); the current archived release-v3 snapshot has the exact supplied digest `71a08777e01af1b6e5bd3dd88ba6443efe9aea41240c09303d4bcc0a7cd8058b`, declares that commit, and says `compiled_this_run=false`. This is a later stored graph artifact describing the frozen source, not a file claimed to exist inside that source commit.

## A1

Set S = sum_b f(b)^2. Each square is nonnegative, so S >= 0 without a strict-positivity assumption. Since S > 0, sqrt(S) > 0 and S != 0. Finite summation and division by a common nonzero denominator give

    sum_b (f(b)/sqrt(S))^2
      = (sum_b f(b)^2)/(sqrt(S))^2
      = S/S = 1.

The square-root squaring identity requires S >= 0. Strict positivity supplies the nonzero denominator and the final cancellation; it is not needed to prove nonnegativity. If S=0 every entry vanishes. In ordinary arithmetic normalization is undefined; in Lean's totalized division by zero the displayed sum is 0, not 1. Signed real entries are allowed by `normalized_sum_sq`. The separate `prepareCircuit_firstColumn` source theorem additionally assumes pointwise nonnegativity, including its zero-qubit boundary, and must not be conflated with this algebraic normalization theorem. No circuit is proved by the identity alone.

## A2

Write r=||x||>0 and q=||y||>0. For arbitrary nonzero x,y, insert y/r:

    ||x/r-y/q|| <= ||(x-y)/r|| + ||y/r-y/q||
                   = ||x-y||/r + |q-r|/r
                   <= 2||x-y||/r.

The last step is the reverse triangle inequality. This argument is valid over R and C because the scale factors r,q are positive reals; no phase minimization occurs. Both normalized vectors have norm one, giving the independent upper bound 2.

For initially arbitrary y with ||x-y|| <= delta < r and delta >= 0, reverse triangle first gives ||y|| >= r-delta > 0. Only now is N(y) legal. The previous estimate gives the requested min(2,2 delta/r). If r>=m>0 and delta<m, this implies min(2,2 delta/m); in this regime the second bound is below 2. This uniform result requires a fixed positive lower norm bound.

An explicit strict-margin counterexample to absolute-error continuity uniform near zero is x_t=(t,0), y_t=(t/2,t/2), t>0. Both are nonzero, ||x_t-y_t||=t/sqrt(2)<t=||x_t||, and the normalized distance is sqrt(2-sqrt(2)), independent of t. As t decreases to zero, the absolute error decreases to zero. Therefore any bound depending only on delta and vanishing with delta fails uniformly over such shrinking reference norms.

At delta=0, y=x and the distance is zero. At delta=r, y=0 is permitted, so automatic nonvanishing fails (the reusable estimate still holds if y is separately nonzero). At x=0 the normalization N(x) is outside its domain; dimension zero contains only zero and has no admissible nonzero reference. The theorem provides a conditional analytic perturbation estimate. It produces neither a state-preparation circuit nor a numerical norm/angle algorithm, finite-bit error budget, or resource bound.

The real normalization identity is an appropriate source anchor, but the cited Lean source does not state this general complex perturbation theorem. `StateVector` is a function abbreviation and `ApproximateStatePreparationCandidate.approximationBound` is a backend-chosen proposition, not an automatically enforced Euclidean metric.

## A3

Since J is an isometry, J†J=I, P=JJ† is an orthogonal projector, and UJpsi has norm one. With eta=(I-P)UJpsi,

    UJpsi = JBpsi + eta = |0^m> tensor Bpsi + eta,
    P eta=0, J†eta=0, ||eta||^2=1-||Bpsi||^2.

Thus 0<=p=||Bpsi||^2<=1 and the success branch is JBpsi. Put x=Apsi, y=alpha Bpsi, and q=||y||. The operator error and unit input give ||x-y||<=epsilon and |q-s|<=epsilon. Since s>epsilon>=0, x!=0, q>=s-epsilon>0, y!=0, and Bpsi!=0. Hence success has positive probability and conditional output is

    J(Bpsi/||Bpsi||), with system representative Bpsi/||Bpsi||.

If p<1, write eta=sqrt(1-p) eta_hat for a normalized rejected vector; if p=1 then eta=0 and no normalized rejected vector need be defined. This branch distinction avoids dividing by zero.

Because alpha>0, (s-epsilon)/alpha <= ||Bpsi|| <= (s+epsilon)/alpha. Squaring nonnegative quantities and using p<=1 gives the claimed probability interval. Applying the supplied normalization estimate to x,y after proving nonvanishing gives the state error <=2 epsilon/s, while unit-norm geometry gives <=2. The positive scale alpha cancels from the normalized y exactly, including its phase convention.

For the probability error,

    |p-s^2/alpha^2| = |q^2-s^2|/alpha^2
      = |q-s|(q+s)/alpha^2
      <= epsilon(2s+epsilon)/alpha^2.

The nominal s^2/alpha^2 can exceed 1: take U=I, B=I, alpha=1, A=(1+epsilon)I and epsilon>0. All promises hold but the nominal value is (1+epsilon)^2. The actual probability remains 1. Conversely, for a genuinely dirty branch one may take m=1, U=R(theta) on the ancilla tensor I, 0<theta<pi, and A=alpha cos(theta/2) I, epsilon=0. Projection is clean, but the full output has a nonzero ancilla-one branch.

Independent fresh trials have geometric waiting time T: P(T=k)=(1-p)^(k-1)p and E[T]=1/p. Each charged operation occurs once per trial, so each expectation is 1/p <= alpha^2/(s-epsilon)^2; the expected sum of the three operation counts is 3/p. This charges preparation and success testing as well as U. No inverse/reflection/control or amplitude-amplification conclusion follows.

For epsilon=0 and s>0 the success probability is exactly s^2/alpha^2 and the accepted state is exactly Apsi/s. For s=0 the target is undefined; if epsilon=0 then p=0, whereas for epsilon>0 a small spurious accepted branch is possible. At s=epsilon>0 nonvanishing fails: let m=1, U=X tensor I, B=0, A=epsilon I, and any unit psi. The operator error is epsilon, s=epsilon, but p=0. This is an admissible unitary witness and works even for n=0. If m=0, J=I, P=I, B=U, p=1 and the rejected branch vanishes; |s-alpha|<=epsilon. If n=0 the system is the one-dimensional complex space, not the zero vector space, so unit scalar representatives and their phases remain meaningful. None of these arguments proves that every possible method for preparing the same target must use postselection.

Source scope: the concrete source identifies a clean block entry with the clean basis-action amplitude; linearity supplies arbitrary input action. The approximate block source states the intended norm inequality in comments but stores an arbitrary proposition in the candidate. The snapshot transport is a proposal with independent review pending and no Lean refs. Its full tail list is block-encoding + spectral-filter + state-action, and its generic hypothesis map also mentions inverses/controls. This question's direct measurement/repetition specialization does not need spectral filtering, inverses, or controls. It must be described as a separately stated analytic composition, not as a new certified interpretation of that whole generic transport hyperedge.

## A4

For the specified half-angle convention, trigonometric addition/subtraction identities give the signed operator identity

    R(a)-R(b) = 2 sin((a-b)/4) R((a+b)/2+pi).

The final factor is unitary over C (orthogonal over R), so its Euclidean induced operator norm is 1 and

    ||R(a)-R(b)|| = 2|sin((a-b)/4)| <= |a-b|/2.

The signed factor is essential for the exact matrix identity; taking an absolute value belongs only in the norm. Tensoring the difference with an untouched identity gives the same scalar times a unitary on a nonzero space, whose operator norm remains 1. Equivalently, decompose any vector into orthogonal spectator sectors and apply the same local bound in each sector, with equality attained on a product input. A common fixed wire/basis reindexing is unitary conjugation and preserves the norm. There is no dimension factor. Zero spectator qubits are allowed; zero total qubits have no physical target wire, as the source type `target : Fin qubits` records. The inspected source states exactly this norm and uses the L2 operator norm scope. No fresh compilation or numerical angle evaluation is asserted.

## Existing-target overlap and scope

A1 matches the mathematical core `qcb-core-sp-006` (normalization identity); it is an additional exposition, not a distinct scored core. A4's question is verbatim the `qcb-core-la-015` registry summary and has the same target. A2 shares the normalization substrate but adds a perturbation theorem and a near-zero obstruction not present in that source declaration. A3 overlaps `qcb-core-be-007` (postselection success) and `qcb-core-be-001` (projected-block contract), while adding approximate-error normalization and strict-margin analysis. Candidate status and split reconciliation are the integrator's decisions. Neither graph adjacency nor this review establishes novelty, Lean closure, or benchmark admission.
