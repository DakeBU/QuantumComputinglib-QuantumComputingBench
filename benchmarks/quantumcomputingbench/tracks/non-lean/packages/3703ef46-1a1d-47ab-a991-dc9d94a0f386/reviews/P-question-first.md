# P1 and P2: sealed question-first, source-aware derivation

Reviewer: `/root/batch2_review_phase` (actual AI reviewer identity).

Scope: phase 1 only. Base/source commit:
`bb260f4e27360a0d3791b40cb22638af4b086fc9`. The two frozen questions and their
pinned source references were available. Authored answers, rubrics, maps,
coverage plans, QA files, and other review/previous-answer records were not
read. This is question-first and source-aware independent AI derivation, not
source-blind review, a human approval, admission, or a new Lean certificate.
No Lean, installation, paid API, model run, GPU, or administrator access was
used. Small local Python diagnostics were used only as finite checks.

The separate `P-phase1-bindings.json` seals the raw and canonical question
hashes, this derivation's raw SHA-256, exact source access, process-file access,
and prior-exposure declaration. This document is to remain unchanged after
that seal; any later comparison belongs in a separate phase-2 record.

## Frozen inputs and source scope

| Item | Raw SHA-256 | Canonical JSON SHA-256 |
| --- | --- | --- |
| P1 | `1c384256a5d201da125452732e73daa99a3656d1028d455b5039a12b956f1e90` | `9d2ea126a84f030f2cabfb7ca312d75d41766fc6668164ba2078c903e7fa4152` |
| P2 | `ad8ceca7fd82101ed63468510dabdb420444569862044ac92fbd7b297fea669e` | `cc758ec30d0d5d82a233b8b3da843bd993642ef8777a3cf54fc6598de37273b4` |

Canonical JSON here means UTF-8 encoding of Python
`json.dumps(object, ensure_ascii=False, sort_keys=True, separators=(',', ':'))`,
with no added newline. This is an explicitly stated comparison policy, not an
unstated claim to use RFC 8785.

All four mathematical source files were read in full with `git show` at the
specified commit, including their existing proofs. Their byte hashes match
the frozen questions. CRLF/CR normalization does not change these files.

| Pinned source | Raw/LF SHA-256 | Actual mathematical use |
| --- | --- | --- |
| `QuantumBlockEncoding/ModularAdder3.lean` | `3995a7d9068322d7116e6d3852111574c3c94acc09b9927231be931d33d17002` | Exact permutation compiler, clean three-control chain, fixed three-bit little-endian adder, and scope of its resource statements. |
| `QuantumBlockEncoding/PrimitiveSemantics.lean` | `ded83cb43f8d6e79c50ac738bfd4faca5bc5aeb4c564114999a832db25418c62` | Chronological composition, exact phases, reverse-adjoint circuit, and full program inverse. |
| `QuantumBlockEncoding/PrimitiveCircuit.lean` | `d5019ef58ce1ce65664d2a40979cdd652ca691c94743532c59dfe18cf2036d4c` | Exact-angle representation, actual gate set, and distinction between ideal logical and finite-gate compilation costs. |
| `QuantumBlockEncoding/PrimitiveCircuitPerturbation.lean` | `624109564cd82b0584fad717283e7b9116b36f1ef10d60b43a063c0ef2a1fbae` | Induced Euclidean operator norm and a distinct aligned-circuit operator certificate. |

The pinned repository `LICENSE` was also read: MIT, copyright (c) 2026 Quantum
Block Encoding contributors. The exact source hashes and license hash are in
the bindings file. The arbitrary-width carry/count theorem, Fourier catalyst
construction, stability argument, Gram theorem, and sharp unitary witnesses
below are natural-language derivations for the questions. They are not claims
that those statements are already proved by the four source files.

## P1: complete independent solution

### Register action and phase sign

Put `omega = exp(2 pi i / M)` and let `T_q |y> = |y+q mod M>` on Y. Because
addition modulo M permutes the residues, substitution `z = y+q mod M` gives

\[
T_q|G_m\rangle
=M^{-1/2}\sum_{z=0}^{M-1}\omega^{(z-q)\bmod M}|z\rangle
=\omega^{-q}|G_m\rangle.
\]

The second equality is exact: an integer representative of `(z-q) mod M`
differs from `z-q` by a multiple of M, and `omega^M=1`. Thus the positive
Fourier exponent produces the required negative kickback phase, including
wraparound.

Let ADD be the clean-scratch circuit constructed below. In chronological
order execute B on X,Q,W, then ADD on Q,Y,A, then the actual inverse B-dagger
on X,Q,W. The operator is

\[
K=(B^\dagger\otimes I_{YA})\,\mathrm{ADD}\,(B\otimes I_{YA}).
\]

For each x its register transcript, in order X,Q,W,Y,A, is

\[
\begin{aligned}
|x,0^m,0^w\rangle|G_m\rangle|0^a\rangle
&\longmapsto |x,q_x,\gamma_x\rangle|G_m\rangle|0^a\rangle\\
&\longmapsto \omega^{-q_x}|x,q_x,\gamma_x\rangle|G_m\rangle|0^a\rangle\\
&\longmapsto \omega^{-q_x}|x,0^m,0^w\rangle|G_m\rangle|0^a\rangle.
\end{aligned}
\]

The adder leaves Q and W unchanged and restores A, so the supplier inverse
receives exactly the supplier output. No condition `gamma_x=0` is used. The
gate list gives a real inverse: reverse its order, using that X, CNOT, and
Toffoli are each self-inverse. Repeating the forward list in the original
order is not generally an inverse.

Linearity now applies to the full registered equality, not merely to
probabilities or phase classes. For normalized
`|psi> = sum_x c_x |x>`, the result is

\[
(D_q|\psi\rangle)_X\otimes|0^m\rangle_Q\otimes|0^w\rangle_W
\otimes|G_m\rangle_Y\otimes|0^a\rangle_A.
\]

It remains true with X entangled with an untouched reference. In particular
Y is exactly separable and reusable. More generally, even for an arbitrary
Y vector g the same compute/add/uncompute circuit acts on the clean work
subspace as

\[
|x,0^m,0^w\rangle|g\rangle|0^a\rangle
\longmapsto |x,0^m,0^w\rangle T_{q_x}|g\rangle|0^a\rangle.
\]

Thus Q,W,A clean up exactly even in the approximate-catalyst subproblem.

### Why discarding the record is a different operation

Before B-dagger, write `|r_x> = |q_x,gamma_x>`. Tracing out Q,W would produce

\[
\rho_X=\sum_{x,x'}c_x\overline{c_{x'}}
\omega^{-q_x+q_{x'}}\langle r_{x'}|r_x\rangle|x\rangle\langle x'|.
\]

For these computational-basis records the overlap is 1 for equal records
and 0 for unequal records. The desired pure state has no such overlap
factor. Distinct records therefore remove the corresponding coherences;
data-dependent garbage alone can do so even when q is constant. For example,
with one data bit, constant q=0, and B copying x into a work bit, discarding
that work bit maps `|+><+|` to `I/2`, while the desired data action is the
identity. If all records coincide, this particular loss of coherence need
not occur, but discarding still does not establish the advertised coherent
zero-return of Q,W. An actual inverse removes the record reversibly by using
the preserved data. Mere forward black-box access supplies neither an inverse
gate list nor permission to erase arbitrary records.

### Arbitrary-width modular adder from the binary carry rule

For fixed j, adding `q_j 2^j` leaves bits below j fixed. If q_j=0 it does
nothing. If q_j=1, adding one to the suffix beginning at j flips bit t exactly
when all lower bits of that suffix, from j through t-1, were 1. Therefore
for each t from m-1 down to j, apply the controlled flip

\[
Y_t\longmapsto Y_t\mathbin{\mathsf{xor}}
\left(Q_j\prod_{r=j}^{t-1}Y_r\right).
\]

For t=j the empty product is 1, so this is CNOT from Q_j to Y_j. Descending
target order is essential: all lower control bits still have their values
from the start of this suffix increment. To see the carry formula directly,
if the suffix has a first zero at t0, precisely bits j through t0 flip; if
it consists entirely of ones, all its bits flip and its carry out is
discarded. These are exactly increment modulo `2^(m-j)`. The expression
therefore proves the increment for every word, including overflow.

Run these increments for j=0,...,m-1. Each preserves every Q bit. Since the
j-th increment adds `q_j 2^j` to the current Y value modulo M, composition
gives

\[
Y\longmapsto Y+\sum_{j=0}^{m-1}q_j2^j=Y+q\pmod M.
\]

This is a reversible basis permutation. The same exact action on arbitrary
superpositions follows with no relative phase because all emitted gates are
the specified exact classical permutation gates.

### Multi-control expansion, cleanup, and counts

For a target t with k distinct controls c1,...,ck:

* k=1 is one CNOT, with no scratch.
* k=2 is one Toffoli, with no scratch.
* k>=3 uses k-2 fresh clean bits a1,...,a_(k-2). Compute
  `a1=c1 c2`, `a2=a1 c3`, ..., `a_(k-2)=a_(k-3)c_(k-1)` by k-2
  Toffolis. Flip t with a Toffoli controlled by `a_(k-2),ck`. Reverse
  the k-2 computing Toffolis.

The invariant after the r-th computing Toffoli is
`a_r = c1 ... c_(r+1)`. The target flip is therefore controlled by all k
original controls. It changes neither these controls nor the chain bits, so
the reversed computing list restores every chain bit to zero. This proves
both action and cleanup for each control word and target value. The count
for k>=2 is `2(k-2)+1=2k-3` Toffolis and k-2 clean scratch. This is the usual
clean conjunction chain whose final conjunction is applied directly to the
target; no unnecessary extra work bit is computed for the full conjunction.

In the suffix circuit, a target at displacement `d=t-j>=1` has `k=d+1`
controls and costs `2d-1` Toffolis. Thus

\[
\begin{aligned}
C_{\mathrm{CX}}(m)&=m,\\
C_{\mathrm{CCX}}(m)
&=\sum_{j=0}^{m-1}\sum_{d=1}^{m-1-j}(2d-1)
=\sum_{r=0}^{m-1}r^2
=\frac{m(m-1)(2m-1)}6,\\
a_m&=\max\{m-2,0\},\qquad C_X(m)=0.
\end{aligned}
\]

All flips execute sequentially and each returns its chain to zero, so the
same a_m scratch bits suffice throughout. This is the maximum simultaneous
scratch of this construction, not a lower bound over all modular adders.
The largest control set occurs at j=0,t=m-1. Q cannot be destroyed and W
may contain arbitrary supplier garbage during the adder, so neither is
silently borrowed as clean chain scratch.

At m=3 the route has 5 Toffolis, 3 CNOTs, and one clean bit. The pinned
three-bit source uses wires `a0,a1,a2,b0,b1,b2,work`, overwrites a, and
preserves b. Its relation to this question is `a=Y`, `b=Q`; one must not
identify its printed wire order with the question's Q,Y order unchanged.
That source also compiles macros to its own X,RY,RZ,CX primitive basis, so
its primitive counts are not these logical Toffoli counts.

### Product preparation and complete logical ledgers

For physical bit j define

\[
\theta_j=\frac{2\pi 2^j}{2^m},\qquad
F_m=\bigotimes_{j=0}^{m-1}\bigl(P(\theta_j)H\bigr),
\]

where each factor is assigned to its named little-endian bit; chronological
order on each bit is H then P. The amplitude of word y is

\[
2^{-m/2}\prod_j e^{i\theta_j y_j}
=M^{-1/2}e^{2\pi i y/M}.
\]

Hence F_m prepares exactly G_m using m Hadamards and m allowed dyadic phase
gates, without additional scratch. Its actual inverse applies
`P(-theta_j)` and then H on every bit, and maps G_m exactly to zero.

Let `C_m=m(m-1)(2m-1)/6`. For L uses, excluding any separately chosen
interleaving data unitaries, the complete gate vector is:

| Gate type | Catalyst prepared once, returned as G_m | Catalyst prepared once, finally reset by F_m-dagger |
| --- | --- | --- |
| X | `2 L b_X` | `2 L b_X` |
| CNOT | `L(2 b_CX + m)` | `L(2 b_CX + m)` |
| Toffoli | `L(2 b_CCX + C_m)` | `L(2 b_CCX + C_m)` |
| H | `m` | `2m` |
| P | `m` | `2m` |
| Supplier calls | L forward and L actual inverse | L forward and L actual inverse |

Total logical gates are respectively
`2L(b_X+b_CX+b_CCX)+L(m+C_m)+2m` and the same expression with `+4m`.
The inverse supplier has the same gate vector as B because each of its
specified gates is self-inverse. It is charged on every use, while catalyst
preparation is charged once. If interleaving data circuits are requested,
their actual counts must be added; the question supplies no values for them.

For the one n-qubit data register specified in the question, peak live
qubits are

\[
n+2m+w+a_m.
\]

The ancilla overhead is `m+w+m+a_m` for Q,W,Y,A. Reuse of clean Q,W,A
between sequential calls avoids an L multiplier in this workspace. On
return, Q,W,A are zero and Y is G_m; following final inverse preparation Y
is also zero. A physical allocation may still contain all these wires, but
clean zero wires can then be released or reused. If L different data
registers are all live, their total data size replaces n, e.g. Ln for L
disjoint n-qubit inputs. Arbitrary data/reference qubits do not disappear
from the live-qubit ledger.

There is no promised polynomial cost for constructing or running B as a
function of n,m; its given vector is retained exactly. This cubic adder
bound is only a logical gate count for the requested route. It is not a
depth, connectivity, optimality, Clifford+T, or fixed-finite-gate synthesis
bound. Exact dyadic P gates are permitted by the question's ideal logical
model, which deliberately differs from the source primitive gate set.

### Approximate preparation with one shared catalyst

Let `|g> = tilde F_m |0^m>` and let
`delta=||g-G_m|| <= eta`. Here tilde F_m is the actual unitary on Y and its
actual adjoint is available, as explicitly assumed. Let C be the whole
exact unitary comprising the L compute/add/uncompute uses and any data-only
interleavings. Let A_data denote the corresponding ideal data unitary.
The clean-work action gives

\[
C(|\psi\rangle|G_m\rangle)
=A_{\rm data}|\psi\rangle|G_m\rangle.
\]

All Q,W,A zeros can be included in both sides. The same C is applied to
the two initial vectors, so preservation of Euclidean norm gives the exact
identity

\[
\left\|C(|\psi\rangle|g\rangle)
-A_{\rm data}|\psi\rangle|G_m\rangle\right\|=\delta\le\eta.
\]

This holds for normalized inputs entangled with an untouched reference as
well. It is not a per-use triangle estimate: there is only one preparation
perturbation at the beginning. No unavoidable factor L follows from this
error alone. Applying the actual tilde F_m-dagger at the end gives

\[
\begin{aligned}
&\left\|(I\otimes\widetilde F_m^\dagger)C(|\psi\rangle|g\rangle)
-A_{\rm data}|\psi\rangle|0^m\rangle\right\|\\
&\quad=\left\|C(|\psi\rangle|g\rangle)
-A_{\rm data}|\psi\rangle|g\rangle\right\|\\
&\quad\le \delta+\delta=2\delta\le 2\eta.
\end{aligned}
\]

The trivial distance cap is 2, so safe reported bounds are
`min(eta,2)` before reset and `min(2eta,2)` after reset. Q,W,A are still
exactly zero; the latter inequality is a full output vector bound relative
to ideal data with *all* work, including Y, zero, not an assertion of exact
Y cleanup or a standalone success probability. It also is not an operator
approximation for tilde F_m on inputs other than zero.

For a useful sharper observation, write
`g = alpha G_m + h` with `h` perpendicular to G_m. Since C has the stated
ideal action on the entire data tensor G_m subspace, the component parallel
to G_m cancels in the last displayed difference. The reset error is at
most `2||h||=2 sqrt(1-|alpha|^2)`, still at most `2delta`. The simpler
2eta estimate suffices for the question and has the correct small-error
scale without an L factor.

Exact catalyst factorization does not follow from small nonzero error.
For m=1, G_1 is `|->`; take a supplier of q_x=x, and
`g=cos(theta)|->+sin(theta)|+>`, with `0<theta<pi/2` small. On data `|+>`
the cleaned circuit gives

\[
\cos\theta\,|-\rangle_X|-\rangle_Y
+\sin\theta\,|+\rangle_X|+\rangle_Y,
\]

which has Schmidt rank two. No Y-only inverse preparation can turn this
into an exactly separable ideal data output and zero Y. Even on the basis
input x=1, reset need not be exact: before reset the actual vector is
`|1>(-cos(theta)|->+sin(theta)|+>)`, whereas ideal data tensored with g
is `-|1>(cos(theta)|->+sin(theta)|+>)`. Their distance is `2sin(theta)`,
while the preparation error is `2sin(theta/2)`. This supplies a concrete
nonzero reset error and shows the factor 2 bound has the correct
small-error behavior. Special preparations can still factorize; the claim
is absence of a general exact-factorization guarantee.

Nothing in `||tilde F_m|0>-G_m||<=eta` specifies how to synthesize tilde
F_m, its gate count, or a uniform operator error for it. Any actual
approximate preparation/inverse gate list must be charged separately by
its own supplied cost. Additional per-use gate errors would be a different
model and could require a telescoping error bound.

### Endpoints

At m=1, M=2 and G_1=`|->`. The adder is one CNOT from Q_0 to Y_0,
with zero Toffolis and zero A scratch; F_1 is H then P(pi), and kickback is
`(-1)^(q_x)`. All ledgers and stability claims above still hold.

For the optional m=0 extension, M=1, Q and Y are empty, q_x=0, G_0 is the
unique empty-register basis vector, D_q=I, ADD and F_0 are empty, and A
has size zero. Define all adder counts as zero rather than using a negative
scratch number. The literal supplier route is B followed by B-dagger and
still costs 2g_B per use if executed, with n+w live qubits; because the
target is known to be identity, an explicitly optimized implementation may
instead omit both supplier calls and allocate no supplier work. These are
different ledgers, not an uncharged inverse. On a zero-qubit catalyst an
actual unitary can at most add a scalar phase. Its actual inverse cancels
that phase exactly at reset, so there is no nontrivial entanglement or
reset error in this extension.

## P2: complete independent solution

### Gram form and universal bound

For `a=(a_0,...,a_(N-1))` with sum `|a_j|^2=1`, define `e_j'=E e_j`.
The stated conjugate-linear-first inner product gives

\[
\|Ea\|_2^2
=\left\langle\sum_j a_je_j',\sum_k a_ke_k'\right\rangle
=\sum_{j,k}\overline{a_j}G_{jk}a_k
=a^\dagger G a.
\]

In particular G=E-dagger E is Hermitian positive semidefinite, and

\[
\|E\|^2=\max_{\|a\|=1}a^\dagger Ga
=\lambda_{\max}(G),\qquad
G_{jj}=\|Ee_j\|^2\le\varepsilon_j^2.
\]

For a positive semidefinite matrix, its largest eigenvalue is at most its
trace. Writing `S=(sum_j epsilon_j^2)^(1/2)`, this yields `||E||<=S`.
Equivalently,
`||sum_j a_j Ee_j|| <= sum_j |a_j| epsilon_j <= S` by Cauchy-Schwarz.
Since U,V are isometries, `||U||=||V||=1`, and therefore

\[
\boxed{\|V-U\|\le\min\left\{2,\sqrt{\sum_j\varepsilon_j^2}\right\}.}
\]

Off-diagonal entries of G are not controlled to be zero by the column
promises. Their coherent accumulation prevents a general replacement of S
by `max_j epsilon_j`.

### Sharpness for every nonnegative tolerance vector

If S=0 take U=V=I_N. Otherwise choose the unit vector
`v_j=epsilon_j/S`, put `t=min(S,2)`, and choose a unit-modulus scalar z
with `|z-1|=t`, for example

\[
z=e^{2i\arcsin(t/2)}
=1-\frac{t^2}{2}+it\sqrt{1-\frac{t^2}{4}}.
\]

Let `P=|v><v|` and define square matrices

\[
U=I_N,\qquad V=I_N+(z-1)P=(I_N-P)+zP.
\]

Because P and I-P are orthogonal projections and `|z|=1`, V is unitary.
Its eigenvalue on v is z and on the orthogonal complement is 1. Thus

\[
E=(z-1)P,\qquad
\|E\|=|z-1|=t,\qquad
\|Ee_j\|=t|v_j|=\frac{t}{S}\varepsilon_j\le\varepsilon_j.
\]

This attains the asserted universal bound using genuine unitaries for
every tolerance vector, not an arbitrary error matrix. If S<=2 all
column inequalities are saturated. If S>=2 take z=-1, and the bound 2 is
attained while some column promises can be loose. A zero tolerance makes
the corresponding v_j zero and that column exactly unchanged. There is
no hidden assumption that every tolerance is positive or at most 2.

For uniform tolerance epsilon the exact universal answer is
`min(2,sqrt(N) epsilon)`. The isometry cap takes over when
`epsilon>=2/sqrt(N)`, with equality of the two expressions at the
threshold. For N=1 this reduces to `min(2,epsilon_0)` and is attained by
scalar phases. If all tolerances vanish, every column agrees, so E=0 and
U=V on the whole input by linearity. If actual columns agree exactly even
when the advertised tolerances are loose, the same conclusion holds for
those particular isometries.

### Small basis errors with maximal coherent operator distance

For N>=2 take

\[
s_N=\frac1{\sqrt N}\sum_{j=0}^{N-1}e_j,\qquad
U_N=I_N,\qquad V_N=I_N-2|s_N\rangle\langle s_N|.
\]

Each column error is `2/sqrt(N)`, tending to zero with N, whereas
`E_N s_N=-2s_N` gives `||E_N||=2`. This also refutes the purported
dimension-free max-column bound for every N>1. The vector s_N itself is
not an operational state-distinguishing witness: its two outputs are
s_N and -s_N, whose Euclidean vector distance is 2 but whose density
operators coincide, so their trace distance is 0 and no measurement
distinguishes them.

Let `r=(e_0-e_1)/sqrt(2)`, so r is normalized and orthogonal to s_N.
Use the normalized input

\[
\psi=\frac{s_N+r}{\sqrt2}.
\]

The two outputs are

\[
\phi=U_N\psi=\frac{s_N+r}{\sqrt2},\qquad
\chi=V_N\psi=\frac{-s_N+r}{\sqrt2}.
\]

Their inner product is zero. Their Euclidean vector distance is sqrt(2),
and the trace distance of the two pure-state density operators is 1:
their difference has eigenvalues 1,-1 on their span, giving trace norm 2.
The explicitly specified two-outcome projective measurement
`{ |phi><phi|, I-|phi><phi| }` returns the first outcome with probability
one for the intended output and zero for the actual output. Thus this
second input gives perfect operational discrimination, separately from
the phase-sensitive norm-saturating input.

### Error geometry that does give a dimension-free conclusion

A sufficient additional condition is pairwise orthogonality of the full
error columns:

\[
\langle Ee_j,Ee_k\rangle=0\quad(j\ne k).
\]

Then G is diagonal, so

\[
\|E\|^2=\max_jG_{jj}
=\max_j\|Ee_j\|^2\le\max_j\varepsilon_j^2.
\]

This condition has to concern the errors, not just the original columns
of U and V separately. Their individual isometry conditions do not force
cross-errors to be orthogonal; the rank-one examples above demonstrate
that distinction.

For a controlled branch map whose full intended and actual outputs on
branch j are `|j> tensor u_j` and `|j> tensor v_j`, their error is
`|j> tensor (v_j-u_j)`. Retaining the orthogonal label j makes errors
from distinct branches orthogonal and supplies the required Gram geometry.
More generally, a direct sum of controlled branch error operators has
operator norm the maximum branch operator norm, when each branch promise
is itself a uniform operator bound on that branch's input space. A bound
for just one vector per branch must not be upgraded to that stronger
within-branch promise without proof. Linearity alone instead allows the
error vectors to point in a common output direction, as in the reflection
example, and supplies no orthogonal label. No trace-out or measurement
appears in this argument.

The entire result concerns the specified full-output representatives and
induced Euclidean norm. Per-input measurement probabilities, equality of
individual rays after separate phase choices, or entrywise matrix bounds
are different premises. For example, diagonal phases preserve each basis
ray while changing relative phases of coherent superpositions. The
question's exact representative-wise column promise is not weakened to
any of those alternatives.

## Finite diagnostics and their limits

A self-contained standard-library Python check generated the elementary
CNOT/Toffoli lists by the chain rule above and tested every clean-scratch
basis input (q,y) at m=1,...,7. It verified preservation of q, the modular
y output, and zero final scratch. In all, 21,844 basis pairs passed. The
measured logical ledgers were:

| m | Basis pairs | CNOT | Toffoli | Peak clean chain bits |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 0 | 0 |
| 2 | 16 | 2 | 1 | 0 |
| 3 | 64 | 3 | 5 | 1 |
| 4 | 256 | 4 | 14 | 2 |
| 5 | 1,024 | 5 | 30 | 3 |
| 6 | 4,096 | 6 | 55 | 4 |
| 7 | 16,384 | 7 | 91 | 5 |

A separate wrong-order discriminator replaced descending targets by
ascending targets. At m=2,q=1,y=1 it produced y=0 rather than the required
y=2. This is a real order failure, not a change of Fourier convention.
The phase reindexing identity checked numerically over m=1,...,7 had
maximum floating residual below 4.1e-15; the symbolic proof above supplies
the arbitrary-width, exact claim.

A two-qubit catalyst/data diagnostic used m=1, q_x=x, nonzero catalyst
mixing angle 0.13, and H on the data between uses. For L=1,2,7,31 the
initial vector error was approximately 0.1299084776695651 and the full
output error remained that value to floating precision. The actual-inverse
clean-zero comparison error was approximately 0.1833303626393804, below
twice the preparation error. This supports the distinction between exact
shared-unitary error preservation and approximate final cleanup; it does
not replace the L-independent unitary proof.

For P2, 13 tolerance vectors, including zero, N=1, nonuniform zeros, the
cap boundary, and above-cap cases, were checked with the square-unitary
construction. Column bounds held; maximum unitarity residual was below
4.5e-16 and maximum saturation residual below 4.5e-16. Again these are
finite diagnostics, not certification of the quantified theorem.

## Phase-1 assessment and handoff

Both frozen questions are mathematically well-posed under their stated
models, and the derivations above discharge their requested conclusions.
No question-contract change is proposed. The clean-chain count used here
is the standard k-2-work construction whose final Toffoli applies the last
conjunction to the target; counts are route-specific, not optimality
claims. In phase 2, the answer and rubric must preserve this explicit
implementation convention and not mix a different chain's resource count
with this circuit.

The principal checks for the later comparison are: negative Fourier
kickback under modular wrap; actual reverse supplier and retention of W;
descending carry order; cubic exact adder count and reusable scratch;
one-time preparation versus per-use supplier charges; no obligatory L
factor from one catalyst input error; no exact factorization inferred from
approximation; full clean-zero vector error after the actual inverse;
Gram off-diagonal contributions; sharp nonuniform bound with genuine
unitaries; distinction between a sign-only norm witness and physically
orthogonal outputs; and the retained-label error geometry.

Failure class: NONE for the two question contracts. The erroneous
ascending-target implementation is REFUTED by the displayed witness.
Finite code is diagnostic evidence only. No new local formal closure,
admission, stable release, universal novelty, or human approval is claimed.
The source records provide a fixed-width/semantic substrate, not proofs of
all new general statements. Phase 2 remains unauthorized at this seal.
