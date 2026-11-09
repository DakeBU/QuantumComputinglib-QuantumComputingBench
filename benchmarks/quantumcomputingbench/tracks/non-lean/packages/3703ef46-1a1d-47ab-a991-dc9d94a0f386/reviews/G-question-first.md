# G1/G2 question-first mathematical derivation

Reviewer actual identity: `/root/batch2_review_gram`.
Method: fresh-context AI question-first, source-aware mathematical review.
Phase: 1, sealed before any package answer or rubric exposure.
Worktree base supplied by coordinator: `bb260f4e27360a0d3791b40cb22638af4b086fc9`.
Source commit actually inspected: `86b9e677566498da04faebcf4e5ed57f177c6bb1`.
This is neither a source-blind reconstruction nor human approval nor a Lean run.

## Exposure and source access

The reviewer read only G1/G2 question objects as mathematical task payloads and
the four exact pinned source modules they cite. The module contents were read
with `git show COMMIT:PATH`, not inferred from current files or catalog labels.
Every supplied whole-file and declaration-span hash matched its stated bytes.
Complete module text, including adjacent exact-case proofs and conventions,
was visible. In G2's original metadata, the transfer/run spans were incomplete;
the corrected metadata described below now includes both complete declarations.

Process context read: AGENTS.md, HARNESS.md, shared/CONTRACT.md, the non-Lean
AGENT_GOAL.md, the master/worker skill instructions, and relevant semantic-slot,
independence, statement-seal and evidence-layer sections of the three publication
protocols. The digest helper source was inspected and `qcb_core.digest` used.
An initial broad filename discovery exposed names of historical review files;
a README keyword search exposed generic historical review/status prose. Neither
operation opened a prior answer report. This limited ancillary exposure is
disclosed rather than described as a completely context-free review.

No `qa/` content, reference answer, rubric, coverage plan, author notes, other
question payload, or prior answer report was opened. No author was contacted.
No Lean, installation, model call, GPU, paid API, system package, staging or
commit operation was performed. The short exact-rational Python checks below
are finite diagnostics; the proofs here are independent mathematical arguments.

After this mathematical derivation was first written, but before phase-1 sealing,
the coordinator reported a metadata-only correction to G2. The reviewer compared
the preserved `questions/history/G2-v1.json` with the current `questions/G2.json`.
Only the transfer/run anchor, line endpoints and associated span hashes changed:
transfer now covers lines 86--89 and run lines 93--96. The full mathematical
question, assumptions and conventions are literally unchanged. The old spans
omitted the recursive clauses; full pinned module text had already been read,
so the derivation did not rely on those truncated locators. Both exact question
objects are bound in the companion record. This is a disclosed continuation of
one review, not a new blind review or an author-answer comparison.

The exact sources establish the following bounded context:

* TensorTrainNormEnvironment: real Gram recursion, scalar all-word identity,
  exact square-root norm, and positivity from a nonzero amplitude.
* StoredTensorTrainNorm: cached exact-real two-pass materialization and an
  exact-real cost model; it supplies no finite-grid roundoff certificate.
* TensorTrainCanonical: real row cores, chronological words, scalar boundaries,
  and row orthonormality; transposition gives output-row/input-column maps.
* SequentialBondPreparation: complex column-input action, passive prefixes,
  chronological emitted bits and exact mass preservation with full unitary
  stages. G2's rectangular perturbative maps are a separately stated natural-
  language generalization, not an existing theorem inferred from this source.

## G1: schedule, error propagation and range

Write `l=d_{j-1}`, `m=d_j`, `M=M_j`, and keep `u=2^{-b-1}`.
All maxima exist because every matrix dimension is positive. The first product
has shape `(l by m)(m by m)`, and the second `(l by m)(m by l)`; both dot products
have length `m`, regardless of `l`.

For a scheduled dot product, let `p_i=Q_b(a_i b_i)` and
`z_i=Q_b(z_{i-1}+p_i)`, with `z_0=0`. Introduce the two rounding errors at each
term, both bounded by `u`. Telescoping gives

    |z_q - sum_{i=1}^q a_i b_i| <= 2 q u.

This is valid for every sign pattern and any fixed nearest-grid tie convention.
Since each stored value is on the grid, additions actually incur zero error on
the unbounded grid. Charging them `u` is conservative and retains the constants
the question requests.

For one bit, the first-pass error satisfies

    ||T_hat - A E_hat||_max <= 2 m u.

The second scheduled dot-product error is at most `2 m u`. Multiplication of
the first-pass error by `A^T` adds at most `m M (2 m u)`. Thus

    ||S_hat - A E_hat A^T||_max <= u(2 m^2 M + 2 m).

Sum the two bit contributions and charge the final addition once. For arbitrary
real `F`, without symmetry or positivity assumptions,

    ||sum_t A^t F (A^t)^T||_max <= 2 m^2 M^2 ||F||_max.

Therefore, with the stated `L_j=2 d_j^2 M_j^2` and
`R_j=4 d_j^2 M_j+4 d_j+1`,

    e_n=0,
    e_{j-1} <= L_j e_j + u R_j.

Define the nonnegative, precision-independent constants backwards by

    C_n=0,              C_{j-1}=L_j C_j+R_j.

Induction gives `e_j <= u C_j`. Explicitly,

    C_j = sum_{k=j+1}^n R_k product_{i=j+1}^{k-1} L_i,
    e_0 <= u C_0 = u sum_{k=1}^n R_k product_{i=1}^{k-1} L_i.

The factors belong to earlier cores: an error made in the right-to-left
environment computation is subsequently propagated through the cores to its
left. This ordering differs from the forward error weights in G2.

For range, define exact-environment bounds and stored-environment bounds by

    B_n=1, B_{j-1}=L_j B_j,
    F_j=B_j+u C_j.

Then `||E_j||_max<=B_j`, `||E_hat_j||_max<=F_j`, and
`F_{j-1}=L_j F_j+u R_j`. At stage `j` put

    P_j = m M F_j + 2 m u,
    Z_j = m M P_j + 2 m u.

Every intermediate category has an explicit absolute-value bound:

| Intermediate | Bound |
| --- | --- |
| First-pass raw scalar product | `M F_j` |
| First-pass rounded scalar product | `M F_j+u` |
| First-pass partial sum before its q-th addition is rounded | `q M F_j+(2q-1)u`, `1<=q<=m` |
| First-pass rounded q-term accumulator | `q(M F_j+2u)` |
| Stored first-pass matrix | `P_j` |
| Second-pass raw scalar product | `M P_j` |
| Second-pass rounded scalar product | `M P_j+u` |
| Second-pass partial sum before its q-th addition is rounded | `q M P_j+(2q-1)u` |
| Second-pass rounded q-term accumulator | `q(M P_j+2u)` |
| Stored second-pass matrix | `Z_j` |
| Unrounded sum of the two bit matrices | `2 Z_j` |
| Stored next environment | `2 Z_j+u = F_{j-1}` |

These follow by induction on the accumulator length using the triangle
inequality; no positive-semidefinite invariant is used. Let `K` be the maximum
of `1`, all `M_j`, all `F_j`, and all displayed product, accumulator and final-
sum bounds (it suffices to use `q=m`). If the square-root branch is used, also
include `sqrt(F_0)+u`. This is a finite maximum of finite known quantities.

Choose a nonnegative integer `I` such that `2^I > K+h`. The signed fixed-point
range `[-2^I,2^I-h]` then contains every stored result with margin. Raw products
of two b-fractional-bit values lie on the `2^{-2b}` grid, so the multiplication
temporary must additionally have enough fractional bits to hold that exact
product before rounding (or implement the equivalent scaled-integer product).
The same magnitude bounds give a finite widened integer-product width. This
distinguishes an overflow certificate for intermediates from a bound on only
the final scalar. It asserts no optimal bit width or bit-operation runtime.

## G1: positivity before normalization

The normalization branch alone assumes a true independent certificate
`rho=||x||_2 >= mu > 0`. Set `delta=u C_0`. If `delta<mu^2`, then

    s_hat >= rho^2-delta >= mu^2-delta > 0.

Only now define `q=sqrt(s_hat)`. The difference-of-squares identity gives

    |q-rho| <= delta/(mu+sqrt(mu^2-delta)) <= delta/mu.

After the single correctly rounded square root,

    |r_hat-rho| <= tau,
    tau := u + delta/mu = u(1+C_0/mu).

If additionally `tau<mu`, then `r_hat>=mu-tau>0`. The exact divided-vector
error is

    ||x/r_hat-x/rho||_2
      = rho |1/r_hat-1/rho|
      = |rho-r_hat|/r_hat
      <= tau/(mu-tau).

A sharper optional `tau` is
`u+delta/(mu+sqrt(mu^2-delta))`, with the same final denominator argument.

For a requested `epsilon>0`, define

    alpha = min(1/2, epsilon/(1+epsilon)),
    U = mu alpha/(1+C_0/mu) > 0.

The single sufficient inequality `u<=U` implies `tau<=mu/2` and
`delta<=mu tau<=mu^2/2`; thus it proves both strict positivity facts before
invoking the square root or division. It also gives
`tau/(mu-tau)<=epsilon`. An explicit legal integer choice is

    b = max(0, b_in, ceil(log_2(1/(2U)))).

Here `b_in` is integral; including `0` ensures the unit constant is on the grid.
The premise already says that 1 is represented exactly. There is no dependence
of `C_0` on the chosen precision, so this is not circular. The computed vector
has norm `rho/r_hat`, which is generally close to, but not exactly, one. Its
numerator and divisions remain exact mathematical quantities; no coordinate
rounding is hidden in this estimate.

## G1: boundary and falsification checks

* Empty chain: retain the raw premises with `n=0`. There is one empty amplitude,
  `x_empty=1`, `E_0=E_hat_0=[1]`, `C_0=0`. The exactly represented square root
  of 1 is 1, so normalization is exactly correct. A valid independent lower
  certificate in this case must have `0<mu<=1`.
* Zero core: if both slices of any whole core are zero, all exact amplitudes
  vanish. That update produces the zero rounded environment exactly, and every
  earlier update stays exactly zero. This retains the raw premises and excludes
  the normalization branch's `mu>0` certificate. One zero slice alone does not
  imply zero mass.
* Zero mass without a zero core: real squares imply every `x_s=0`; the raw
  certificate gives `|s_hat|<=u C_0`. It does not authorize division by the true
  norm. It is unnecessary to assume that arbitrary rounded environments retain
  symmetry or positivity, or that cancellation-induced zero mass is preserved
  exactly by the schedule.
* For every fixed integer `b>=2`, take one scalar-bond core with
  `A_1^0=h=2^{-b}`, `A_1^1=0`, `b_in=b`, and `M_1=h`. Its nonzero exact mass is
  `h^2`. The first product is exactly `h`, but the second rounds `h^2` to zero
  because `h^2<h/2`. There is no tie, so every tie convention gives `s_hat=0`.
  A true lower mass exists, but that fact alone without a compatible precision
  margin does not guarantee a positive computed mass.

The exact-real Gram identity proves the target algebraic identity, and the
exact-real operation count describes another arithmetic model. Neither controls
this schedule's rounding, intermediate overflow or normalizer denominator.

Finite diagnostic only: Python `Fraction` arithmetic and nearest-even rounding
at `b=2` were applied to dimensions `(1,2,1)`, with
`A_1^0=(1/4,-1/2)`, `A_1^1=(3/4,1/4)`,
`A_2^0=(1/4,1/2)^T`, `A_2^1=(-1/4,3/4)^T`. The exact right environment was
`[[1/8,-1/16],[-1/16,13/16]]`, whereas the rounded one was
`[[0,-1/4],[-1/4,3/4]]`; its error was `3/16<=1=u C_1`.
The final exact mass was `83/256`, the rounded mass `1/4`, and the error
`19/256<=57/8=u C_0`. In particular the rounded intermediate has determinant
`-1/16`, so positivity cannot be presumed. The one-core erasure was also checked
for `b=2,...,6`. These finite checks corroborate examples, not the all-parameter
proof or a bit-runtime claim.

## G2: passive factors, mass products and sharp endpoints

For one stage set `D=V^dagger V-I`, a Hermitian operator satisfying
`||D||_op<=eta`. Hence, for every bond vector `w`,

    (1-eta)||w||^2 <= ||Vw||^2 <= (1+eta)||w||^2.

For an arbitrary passive space with orthonormal basis `(e_p)`, write the whole
vector uniquely as `z=sum_p e_p tensor z_p`. This is a decomposition of every
vector, including entangled ones; no product-state assumption is made.
Orthogonality of the passive basis gives

    ||z||^2=sum_p ||z_p||^2,
    ||(I tensor V)z||^2=sum_p ||V z_p||^2.

Summing the bond inequalities proves the one-step bound on the entire space.
The specified regrouping preserves norms and places the new bit after the
previous bits, with the bond last. The maps have domain dimension
`2^{j-1} d_{j-1}` and output dimension `2^j d_j`.

Apply this to `z=T_{j-1}v` repeatedly. With

    L=product_{j=1}^n(1-eta_j),
    U=product_{j=1}^n(1+eta_j),

one obtains `L||v||^2 <= ||T_n v||^2 <= U||v||^2`. Equivalently,
`L I <= T_n^dagger T_n <= U I`, so

    ||T_n^dagger T_n-I||_op <= max(1-L,U-1).

In fact this maximum is `U-1`: expansion of `U+L` contains twice the empty
product and nonnegative even-degree products, so `U+L>=2`. Keeping the maximum
form is also valid. Since the chain is finite and every `eta_j<1`, `L>0`.
The local premise itself forces injectivity and `d_{j-1}<=2d_j`; no additional
dimension assumption is silently needed to obtain that consequence.

Each mass endpoint is attained by legal scalar-bond trains: take all `d_j=1`
and `V_j z=sqrt(1+eta_j) z |0>` for the upper endpoint, or use
`sqrt(1-eta_j)` throughout for the lower one. The local Gram defects have
exactly the allowed magnitudes and the squared output norms are the products.

For two positive defects the upper product is
`1+eta_1+eta_2+eta_1 eta_2`, so an upper bound `1+sum eta_j` is false in general.
The weaker lower bound `product(1-eta_j)>=1-sum eta_j` is valid: induct on
`1-product(1-eta_j)` and use that each partial product is in `[0,1]`. It is not
an equality in general and cannot replace the sharp two-sided product claim.

## G2: target fidelity and forward error propagation

Zero Gram defect does not identify a target. The one-stage scalar-bond maps
`V z=z|0>` and `W z=z|1>` both have zero defect, but their outputs from 1 are
orthogonal unit vectors. Gram control certifies distortion of input Euclidean
mass (and, by the Gram operator, inner products), including preservation when
the defects vanish. It supplies no prescribed output amplitudes, directions,
relative phases, chronological target action or terminal-bond support. Even
a scalar phase change leaves a Gram matrix unchanged; the orthogonal witness
shows a failure stronger than a global-phase ambiguity.

For the separate comparison branch put
`A_j=I tensor V_j`, `B_j=I tensor W_j`, including the prescribed isometric
regrouping. The passive-factor argument implies
`||A_j||<=g_j=sqrt(1+eta_j)` and `||A_j-B_j||<=epsilon_j`.
The `B_j` are isometries, so `||S_{j-1}v||=1` for unit input. The exact identity

    T_jv-S_jv = A_j(T_{j-1}v-S_{j-1}v) + (A_j-B_j)S_{j-1}v

gives `D_j<=g_j D_{j-1}+epsilon_j`, where `D_0=0`. Induction yields

    ||T_n v-S_n v||
      <= sum_{k=1}^n epsilon_k product_{j=k+1}^n sqrt(1+eta_j).

Equivalently each hybrid term has the inserted difference at stage `k`, ideal
isometries before it and actual maps after it. Only later actual maps can
amplify that inserted discrepancy, which explains the product indices.

For a counterexample to the unweighted sum take two scalar-bond stages with
`W_j z=z|0>` and `V_j z=(5/4)z|0>`, for `j=1,2`. Choose
`eta_1=eta_2=9/16<1`, `epsilon_1=epsilon_2=1/4`, and unit input 1. All premises
hold exactly. The outputs are `(25/16)|00>` and `|00>`, so their difference has
norm `9/16>1/2=epsilon_1+epsilon_2`. The requested weighted bound is exactly
`(1/4)(5/4)+1/4=9/16`. The rational values were independently verified by a
short Python `Fraction` calculation; the displayed algebra proves the witness.
No normalization or postselection is used.

## G2: boundaries, phase, physical implementation and cleanup

* Empty chain: retaining the main premises, `T_0=I`, both mass products are one,
  and the global defect is zero. In the comparison branch `S_0=I` and the error
  sum is empty, hence zero. The original bond remains; no emitted bit or cleanup
  occurs.
* Zero input: retaining the main premises yields both sides of the mass bounds
  equal to zero. Zero input does not satisfy the comparison branch's unit-input
  premise. If that premise is replaced by arbitrary input, homogeneity gives
  the displayed comparison bound multiplied by `||v||`, including zero.
* Exact local isometries: set all `eta_j=0`, retaining the comparison branch
  only when its extra `W_j`/`epsilon_j` premises are supplied. Then
  `T_n^dagger T_n=I`; the comparison weights are one and its error is at most
  `sum epsilon_j`. If all comparison discrepancies also vanish, `T_n=S_n`.
  Zero defects alone still do not imply the specified target action.
* Non-strict endpoint: replace the strict condition by `eta_1=1`. With
  `n=1`, `d_0=d_1=1`, `V_1=0` and input 1, the defect is exactly one and output
  mass is zero. This explicitly leaves the original `eta_j<1` domain; no
  positive lower mass can then be inferred.
* Cleanup counterexample within the strict domain: let `n=1`, `H_0=C`,
  `H_1=C^2`, and `V_1(1)=(|0> tensor |0>+|1> tensor |1>)/sqrt(2)`. This is an
  exact isometry, yet its terminal bond is entangled with the emitted bit,
  rather than fixed to a clean label. Thus a cleanup or terminal-support premise
  is genuinely additional.

Approximate linear maps can increase or decrease mass; they are not thereby
physical probability-preserving channels or unitary circuit stages. Even where
exact isometries admit abstract finite-dimensional completions, these estimates
do not construct gates, give synthesis cost, prove a wire-placement bridge, or
clean a terminal bond. Gram defects are phase-insensitive; the comparison
operator norm is a phase-sensitive vector comparison exactly as stated.

## Phase-1 disposition and remaining uncertainty

Both questions are coherent on their explicitly scoped premises. No
question-contract correction is required by this derivation. The supplied
constants in G1 are safe; symmetry/positivity shortcuts would be unsound.
G1's normalization branch needs its independent lower certificate and a
precision margin. G2's entangled-input step and later-stage growth weights
follow from full operator control, not basis-only checks.

Confidence is high in the independent natural-language mathematics. The review
does not establish formal closure, machine bit-runtime, circuit synthesis,
novelty, admission, or correctness of an unseen answer/rubric. Phase 2 remains
unperformed pending the coordinator's authorization. The companion binding
record seals this file's exact bytes and the exact question/source inputs.
