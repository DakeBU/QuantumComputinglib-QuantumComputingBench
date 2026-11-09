# E1/E2 question-first independent mathematical derivation

Reviewer actual identity: `/root/batch2_review_composition`.

This is an AI, source-aware, question-first mathematical review. It is not a
source-blind decoder, a human approval, a Lean proof run, or a review of an
author answer. The derivations below were developed from the original E1/E2
question packets, their exact cited source files, and repository process
guidance before exposure to answers or rubrics. Hashes, chronology, notation
revision checks, and the final phase-1 seal are in `E-phase1-bindings.json`.

## E1 — complete independent answer

### Residual propagation and certified raw mass

Set

\[
D_j=\bar E_j-E_j,\qquad
R_j=\bar E_{j-1}-T_j(\bar E_j).
\]

Then \(D_n=0\), and linearity gives

\[
D_{j-1}=R_j+T_j(D_j).
\]

For an arbitrary real square matrix \(Z\), without a symmetry or positivity
assumption,

\[
\begin{aligned}
\|T_j(Z)\|
&\le\sum_{t=0}^1\|A_j^t Z(A_j^t)^T\|\\
&\le\sum_t\|A_j^t\|^2\|Z\|
\le L_j\|Z\|.
\end{aligned}
\]

Here the transpose has the same induced Euclidean norm, including the
zero-dimensional cases. Therefore

\[
\|D_{j-1}\|\le\varepsilon_j+L_j\|D_j\|,
\qquad
\boxed{\beta=\sum_{j=1}^n\varepsilon_j\prod_{i=1}^{j-1}L_i}.
\]

Unrolling the recurrence from \(D_n=0\) proves \(\|D_0\|\le\beta\).
The boundary space is one-dimensional, so the supplied Gram identity yields

\[
\boxed{\left|\bar E_0(1,1)-\|x\|^2\right|\le\beta},
\qquad m=\bar E_0(1,1)-\beta\le\|x\|^2.
\]

For \(n=0\), there are no transfers or residuals: the empty sum is
\(\beta=0\), \(\bar E_0=E_0=I_1\), and \(x=(1)\), so \(m=1\).
The propagation uses **preceding**, not following, cores because an error
inserted at level \(j-1\) passes through \(T_{j-1},\ldots,T_1\) to reach
level zero. No contractivity of those maps was assumed.

An explicit scalar-bond witness is \(n=2\), with every bond dimension equal
to one, \(A_1^0=2\), \(A_1^1=0\), and \(A_2^0=A_2^1=0\). The raw vector is
zero. Choose

\[
(\bar E_0,\bar E_1,\bar E_2)=(4,1,1),\quad
(\varepsilon_1,\varepsilon_2)=(0,1),\quad (L_1,L_2)=(4,0).
\]

These are valid residual and transfer certificates. The correct bound is
\(\beta=4\) and gives \(m=0\). Replacing it by
\(\varepsilon_1+\varepsilon_2=1\) gives the false positive lower bound
\(4-1=3\) on the mass of the zero vector. This witness belongs outside the
subsequent \(m>0\) branch.

### Nonzero vectors before normalization

Now impose the question's additional premises \(m>0\) and
\(0\le\delta<\sqrt m\). The already established lower bound gives

\[
\|x\|\ge\sqrt m>0,\qquad
\|y\|\ge\|x\|-\|x-y\|\ge\sqrt m-\delta>0.
\]

Only now define \(\psi=x/\|x\|\) and \(\phi=y/\|y\|\). They are unit
vectors, and the supplied inequality implies

\[
\|\psi-\phi\|\le\frac{2\|x-y\|}{\|x\|}
\le\frac{2\delta}{\sqrt m}.
\]

The strict margin is substantive: at the excluded endpoint
\(x=(1),m=1,\delta=1,y=0\), the raw error bound holds but \(\phi\) cannot
be defined. A positive mass for \(x\) alone is not a substitute for the
separate nonzero guarantee for \(y\).

### Actual circuit action and full-output estimate

Write \(z=|0^{a+n}\rangle\). The given isometry has \(J^\dagger J=I\),
and \(P=JJ^\dagger\) is the orthogonal projector onto the complete clean
workspace subspace in the stated order \(K\otimes H\). The exact preparation
action and the supplied actual-list bound give

\[
\begin{aligned}
\|\Omega-J\psi\|
&=\|Vz-J\psi\|\\
&\le\|(V-U)z\|+\|J\phi-J\psi\|\\
&\le\gamma+2\delta/\sqrt m=\tau.
\end{aligned}
\]

This compares the complete outputs and their exact representatives, including
workspace and phase. The gate bound is conditional on positional alignment,
physical targets, actual half-angle rotations and their supplied angle-error
certificates; it is not a consequence of a gate count alone. Unitarity of
\(V\) gives \(\|\Omega\|=1\), while \(\|J\psi\|=1\).

### Accepted branch and the exact-representative estimate

Let

\[
b=J^\dagger\Omega,\qquad
\chi=(I-P)\Omega,\qquad
\Omega=Jb+\chi.
\]

The terms are orthogonal, \(J^\dagger\chi=0\), and

\[
p=\|b\|^2,\quad 1-p=\|\chi\|^2,\quad 0\le p\le1.
\]

Set \(s=\|\Omega-J\psi\|\) and
\(c=\operatorname{Re}\langle\psi,b\rangle\). Using both unit norms,

\[
s^2=2-2c,\qquad
c=1-s^2/2\ge1-\tau^2/2>0
\]

under the stated \(\tau<1\). Cauchy–Schwarz gives
\(c\le|\langle\psi,b\rangle|\le\|b\|\). Thus \(b\ne0\), and squaring
nonnegative quantities proves

\[
\boxed{p\ge(1-\tau^2/2)^2}.
\]

Define \(q=\|b\|\in(0,1]\) and \(\psi_{\rm acc}=b/q\). Then

\[
\begin{aligned}
\|\psi_{\rm acc}-\psi\|^2
&=2-2\operatorname{Re}\langle\psi,b\rangle/q\\
&\le2-2c=s^2\le\tau^2,
\end{aligned}
\]

because \(c>0\) and \(q\le1\). Hence
\(\boxed{\|\psi_{\rm acc}-\psi\|\le\tau}\). No phase is optimized or
discarded: the proof uses the real part of the inner product of the exact
representatives. If \(p<1\), one may additionally write

\[
\Omega=\sqrt p\,J\psi_{\rm acc}+\sqrt{1-p}\,\chi_{\rm rej},
\qquad \chi_{\rm rej}=\chi/\sqrt{1-p}.
\]

For \(p=1\), the rejected vector is zero and no normalized rejected vector
needs to be defined.

The proof actually works for the larger sufficient range \(\tau<\sqrt2\).
Thus \(\tau<1\) is a convenient sufficient threshold, not a sharp claim.
At full-output distance \(\sqrt2\), zero clean success is possible: use
\(n=0,a=1,x=y=(1)\), \(U=R(0)=I\), and \(V=R(\pi)\) on the workspace.
Then the target is \(|0\rangle\), the actual output is \(|1\rangle\),
and \(p=0\). These are even aligned one-rotation lists, with the valid
budget \(\gamma=\pi/2\); this diagnostic does not satisfy \(\tau<1\).

The full-output unit norm is essential for the stronger conditional bound.
If one drops it, take a clean target \((1,0)\) and an unnormalized full
output \((1/2,1/2)\). Its squared distance is \(1/2\), whereas the squared
distance after normalizing its accepted branch is \(2-\sqrt2>1/2\). This is
a counterexample to the weakened premise set, not to the unitary question.

### E1 boundary cases and complete AND inputs

- Zero certified residual budgets give \(\beta=0\) and exact Gram mass.
  Actual residuals being zero also imply exact environments by backward
  induction, though unnecessarily positive supplied budgets may produce a
  conservative \(\beta>0\).
- Zero data and gate budgets give \(x=y\), \(\gamma=\tau=0\),
  \(\Omega=J\psi\), \(p=1\), and exact accepted output whenever the
  normalization branch is active.
- For \(n=0\), \(x=(1),m=1\). Since \(y\) is a real scalar and
  \(|1-y|\le\delta<1\), it is positive, so in fact \(\phi=\psi=(1)\).
  The general estimates remain valid and may be conservative.
- For \(a=0\), \(J=I\) and \(P=I\): there is no rejected sector,
  \(p=1\), and the conditional vector is the full output.
- Any internal zero bond forces every word contraction through a zero
  intermediate space to vanish. Therefore \(x=0\), and a valid residual
  certificate always has \(m\le0\). This case tests the raw theorem and is
  incompatible with the active \(m>0\) normalization theorem. In
  particular, a zero transfer factor kills downstream error contributions.
- The mass estimate uses the TT definition, exact terminal environment,
  Gram identity, certified local residuals, certified transfer bounds and
  the chosen induced norm. It does not use \(y,U,V\).
- Nonzero normalized vectors and their distance additionally require the
  positive certified mass and the raw-data error with its strict margin.
- The full-output estimate additionally requires actual aligned unitary
  lists, their angle budgets, exact phases/physical targets, and the exact
  complete preparation action. A prepared abstract vector is insufficient.
- Conditional success and the stated conditional-vector estimate additionally
  use the complete-workspace orthogonal projection, full-output unit norm,
  and the imposed small-error threshold. These are AND inputs to the
  composition, not independently sufficient alternative arrows.

The result is conditional analytic error propagation. It supplies no
floating-point residual certifier, numerical angle supplier, data loader,
unitary-preparation algorithm, finite-gate-set compiler, finite-bit rounding
analysis, or runtime bound. The existence of an exact Gram identity or of a
stored exact-real denotation theorem does not supply those missing layers.

## E2 — complete independent answer

### Clean-column sandwich and ideal coefficients

The nonzero coefficient assumption implies \(\alpha>0\). From the stated
definitions, including the zero-coefficient convention,

\[
\|l\|^2=\|r\|^2=\sum_j|c_j|/\alpha=1,
\quad \overline{l_j}r_j=c_j/\alpha.
\]

Unitarity of \(Q_L,Q_R\) gives \(\|\widetilde l\|=\|\widetilde r\|=1\).
For any selector vector \(z\), let \(C_z:H\to K\otimes H\) be
\(C_zv=z\otimes v\). Then \(\|C_z\|=\|z\|\),
\(C_z^\dagger=\langle z|\otimes I\), and a unit \(z\) makes \(C_z\)
an isometry. In particular,

\[
(Q_R\otimes I)J=C_{\widetilde r},\qquad
J^\dagger(Q_L^\dagger\otimes I)=C_{\widetilde l}^\dagger.
\]

Thus the actual block is exactly

\[
\boxed{\widetilde B
=(\langle\widetilde l|\otimes I)\widetilde S
 (|\widetilde r\rangle\otimes I)
=C_{\widetilde l}^\dagger\widetilde S C_{\widetilde r}}.
\]

No approximation of any off-clean column occurs in this identity. The actual
adjoint in the question is essential: its clean row is exactly the adjoint
of the actual clean column, not an independently prepared vector or a
transpose.

The orthogonal selector projectors \(P_j=|j\rangle\langle j|\) satisfy
\(P_jP_k=0\) for \(j\ne k\) and \(\sum_jP_j=I\). Hence

\[
S^\dagger S=\sum_jP_j\otimes U_j^\dagger U_j=I,
\qquad SS^\dagger=I.
\]

So \(S\) is unitary. The ideal sandwich is

\[
C_l^\dagger SC_r
=\sum_j\overline{l_j}r_jU_j
=\sum_j(c_j/\alpha)U_j=A/\alpha=:T.
\]

The tensor lifts of \(Q_L^\dagger,Q_R\) and the supplied
\(\widetilde S\) are unitary, so their product \(\widetilde W\) is
unitary. Consequently \(\|\widetilde W\|=1\), \(\|J\|=\|J^\dagger\|=1\),
and \(\|\widetilde B\|\le1\). Also \(\|T\|\le1\) by the ideal isometry
sandwich; equivalently, \(\|A\|\le\sum_j|c_j|\|U_j\|=\alpha\).
None of these conclusions requires \(\widetilde S\) to preserve the selector.

### Direct perturbation proof and the cap at two

Use the exact telescoping identity

\[
\begin{aligned}
\widetilde B-T
={}&(C_{\widetilde l}^\dagger-C_l^\dagger)
       \widetilde S C_{\widetilde r}\\
&+C_l^\dagger(\widetilde S-S)C_{\widetilde r}\\
&+C_l^\dagger S(C_{\widetilde r}-C_r).
\end{aligned}
\]

All unchanged isometry/coisometry or unitary factors have norm one. The three
terms therefore have norms at most \(\delta_L,\eta,\delta_R\), respectively.
Writing \(e=\delta_L+\delta_R+\eta\),

\[
\|\widetilde B-T\|\le e,
\qquad
\|\widetilde B-T\|\le\|\widetilde B\|+\|T\|\le2.
\]

Since \(\alpha>0\), this proves the requested guarantee

\[
\boxed{\|A-\alpha\widetilde B\|
\le\alpha\min\{2,\delta_L+\delta_R+\eta\}}.
\]

There is no need to select ideal full PREPARE unitaries or compare actual
ones to them in operator norm. Only their clean columns enter the sandwich.

### Coefficient route as an alternative proof

With ideal \(S\) in the middle, the implemented coefficient of \(U_j\) is
\(a_j=\overline{\widetilde l_j}\widetilde r_j\). Split its deviation as

\[
a_j-c_j/\alpha
=\overline{(\widetilde l_j-l_j)}\widetilde r_j
 +\overline{l_j}(\widetilde r_j-r_j).
\]

The triangle inequality followed by scalar Cauchy–Schwarz gives

\[
\begin{aligned}
\sum_j|a_j-c_j/\alpha|
&\le\|\widetilde l-l\|\,\|\widetilde r\|
 +\|l\|\,\|\widetilde r-r\|\\
&\le\delta_L+\delta_R.
\end{aligned}
\]

Thus the norm of the corresponding linear combination error is at most that
same quantity, because every \(U_j\) has norm one. Replacing \(S\) by
\(\widetilde S\) contributes at most \(\eta\) through the unit-column
sandwich; the contraction cap is unchanged. The coefficient proof and direct
sandwich proof are alternative sufficient derivations from the same premises.
They are not two jointly necessary hypotheses and do not introduce an
additional promise on the supplied data.

### Separate preparation phases

Under the replacement assumptions, let

\[
l_\theta=e^{i\theta_L}l,\quad r_\theta=e^{i\theta_R}r,
\quad\Delta=\theta_R-\theta_L,\quad\zeta=e^{i\Delta}.
\]

The conjugate-linear bra produces the target

\[
C_{l_\theta}^\dagger SC_{r_\theta}=\zeta A/\alpha.
\]

Repeating the preceding proof around those unit representatives gives

\[
\|\alpha\widetilde B-\zeta A\|\le\alpha\min\{2,e\}.
\]

A bound relative to the original exact target, including the phase mismatch,
is

\[
\boxed{
\|A-\alpha\widetilde B\|
\le\alpha\min\left\{2,
e+|1-\zeta|\frac{\|A\|}{\alpha}\right\}
\le\alpha\min\{2,e+2|\sin(\Delta/2)|\}.}
\]

The outer cap at two follows independently from contraction, so it remains
valid even when the phase contribution and error budgets are large. A
sufficient relation restoring the previous guarantee is
\(\theta_R-\theta_L\in2\pi\mathbb Z\). If \(A=0\), phase mismatch has no
effect on the target; phase agreement is sufficient rather than necessary
for every individual instance.

For a concrete perfect-fidelity failure, take \(r=d=1,c_1=1,U_1=1\),
\(Q_L=1,Q_R=-1\), and \(\widetilde S=S=1\). Both prepared state fidelities
with their desired one-dimensional unit states equal one. Nevertheless
\(\widetilde B=-1\), while \(A/\alpha=1\), giving exact block error two.
The phase-referenced errors vanish with \(\theta_L=0,\theta_R=\pi\).
This is not a counterexample to the exact-representative hypothesis: there,
the right-column distance is two rather than zero.

### Completion invariance and boundary cases

If another unitary \(Q_L'\) has the same clean column, then its projected
adjoint row is also the same. If \(Q_R'\) has the same clean column, its
clean-input action is the same. The sandwich formula therefore makes
\(\widetilde B\) invariant under either completion change for every fixed
\(\widetilde S\), even one that mixes selector sectors.

For an explicit pair in dimension two, take

\[
Q=I_2,\qquad Q'=\operatorname{diag}(1,-1).
\]

They have clean column \((1,0)^T\), yet \(\|Q-Q'\|=2\). More generally,
right-multiplying any completion by \(\operatorname{diag}(1,-1,1,\ldots)\)
preserves its clean column and produces a completion at operator distance two. Thus even
zero column error places no small-distance requirement on the completion.

- Zero coefficients give \(l_j=r_j=0\), so their chosen \(\omega_j=1\)
  makes no contribution. Actual approximate columns can leak into such
  coordinates; the proved coefficient and sandwich bounds cover that leakage.
- For \(r=1\), both preparation unitaries are scalar phases, there are no
  off-clean columns, and the same formulas hold. Selector projection is then
  the identity and succeeds deterministically. Its exact block can still
  have the phase failure displayed above.
- If \(\delta_L=\delta_R=\eta=0\) in the exact-representative branch, then
  \(\widetilde B=A/\alpha\) exactly. The completions need not be close to
  any chosen ideal completions.
- If all coefficients vanish, then \(\alpha=0\) and the stated definitions
  of \(l,r,A/\alpha\) are unavailable. That case is excluded; no zero
  normalization fallback is introduced.
- For any unit system input \(v\), the complete output decomposes into
  \(J\widetilde Bv\) and an orthogonal rejected component, so the clean
  success probability is \(\|\widetilde Bv\|^2\), not automatically one.
  For example, take \(r=2,d=1,c_1=c_2=1,U_1=1,U_2=-1\), both PREPAREs
  equal to the Hadamard matrix, and ideal SELECT \(S=\operatorname{diag}(1,-1)\).
  Then \(\alpha=2\), \(A=0\), the full composite is the selector Pauli X,
  and its clean block and success probability are zero, despite exact inputs.

The analytic implication requires all of: nonzero coefficient mass; the
unitary \(U_j\); actual \(Q_L,Q_R,\widetilde S\); their exact column/error
certificates; the actual adjoint \(Q_L^\dagger\); fixed tensor order; and
complete clean-work semantics. Abstract availability of normalized vectors
does not supply an executable adjoint or a controlled, coherent SELECT. An
existential unitary completion is not a construction or cost theorem.
Unmodelled garbage can change the projected block. No gate counts, inverse
access costs, state-loading costs, residual/angle precision supplier,
finite-gate-set synthesis, finite-bit bound, or runtime follows from this
mathematical interface. A nonzero accepted branch would be an additional
premise before normalizing an output state; E2 does not assert one.

## Source scope, independent search, and review conclusion

After completing these independent derivations and diagnostics, I compared
the byte-preserved original packets with the final notation packets. Only
the `question` field changed in each. I checked the dimensions, quantifiers,
matrix order, transpose/adjoint, terminal condition, nonnegative error bounds,
strict margins, supplied interfaces, phase directions, requested bounds,
boundary cases, and resource exclusions. The revisions only convert the
same mathematics to inline/display LaTeX; no semantic drift was found.
E1's original approximate-environment symbol is written as
\(\widehat E\) in the revised question and \(\bar E\) in this derivation;
both denote exactly the same supplied matrices. This is an explicit
pre-comparison notation review, not a new blind-review claim. Both question
versions and the timing are bound separately.

All seven cited whole-file SHA-256 digests were checked and match the question
packets. The E1 Gram recurrence and scalar identity are the exact cited
interfaces. `StoredTensorTrainNorm.gram_value` and `norm_eq_sum` connect a
stored exact-real producer's denotation to that identity; they do not certify
floating-point residual estimates. `ConcreteSemantics` defines clean product
register projection and its basis-action equivalence; it does not by itself
prove the new conditional-state estimate.

The cited `PrimitiveCircuitPerturbation.aligned_eval_distance_le` is stated
with a uniform \(\delta\) and all-list-length budget
\(\mathrm{length}\cdot\delta/2\), whereas E1 explicitly supplies the sharper
per-rotation sum \(\gamma=\frac12\sum_kd_k\). The latter is a valid
telescoping variant in the question's given interface; it must not be reported
as the literal signature of that existing declaration. The residual,
positive-margin, and conditional-projection chain is independently derived
here, not attributed wholesale to one cited theorem.

The E2 clean-entry source uses one PREPARE, a coefficient register, controlled
amplitude matrices, and permutation SELECT. Its clean-column and adjoint-row
identities support the sandwich mechanism. E2's two different preparations,
arbitrary system unitaries, selector-mixing approximate middle, and analytic
norm estimate are a separately derived extension of that mechanism, not a
literal restatement of the existing source theorem. The named source theorem
at lines 172–219 actually ends at line 220; the complete declaration through
line 220 was inspected after a coordinator locator-only notice. The question
packet's whole-file digest is exact, and no mathematical premise changed.

`ApproximateOperatorBlockEncodingCandidate` has an
`approximationBound : Prop` field. The surrounding comment gives the intended
scaled norm interpretation. Merely constructing or locating that record type
does not establish the inequality, supply its proof, certify arbitrary
non-qubit dimensions, or construct a runtime/finite-bit implementation.
These source-scope distinctions are provenance boundaries, not defects in the
explicitly posed analytic questions.

The independent script `E-finite-diagnostics.py` performed 14,400 exact
rational scalar residual checks for chains of lengths two and three. It found
the unweighted false-positive examples and no violation of the weighted
bound. It also checked 11,025 finite vector geometries, including 4,600 with
full distance below \(\sqrt2\), and 180 small complex LCU instances
(selector dimensions one through three, system dimensions one and two,
largest matrix six by six), including selector-mixing unitary perturbations,
zero coefficients, completion changes and phase changes. Every LCU instance
had an uncapped error budget below two. Matrix/vector checks used ordinary
floating point; the largest measured unitarity defect was below
\(7.1\times10^{-15}\). These checks are diagnostics only. They are not
certified residual computation, an arbitrary-dimension proof, a benchmark
evaluation, or Lean compilation.

The symbolic proofs and explicit witnesses above found no mathematical
counterexample to either original question under its complete stated
premises. The strongest issues to preserve in later answer/rubric review are
the preceding-core residual factors; both nonzero raw-vector proofs; the
full-output unit norm and real-part argument; actual adjoint and phase
direction; contraction cap; alternative rather than jointly assumed proof
routes; and honest source/resource boundaries. Author answer and rubric
correctness remain unassessed until separately authorized phase 2.
