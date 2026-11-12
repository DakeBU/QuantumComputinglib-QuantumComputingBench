# One-boundary Bernstein contraction for sampled Hermite data

Retrospective local mathematical source and lesson, version 2. Historical
formalizer: UNKNOWN. The construction below is recovered from an existing
implementation. This text is neither a historical pre-proof source nor a
claim of a new algorithm or an earlier paper. It is an AUTHOR/WIP source
awaiting independent source-first review and source-blind reconstruction.

## S1. The exact target

Let \(k,n\in\mathbb N\), allowing zero, and \(L>0\). Put \(d=2k+1\),

\[
a_{k,i}=\sum_{m=0}^{i}\frac{\binom{k+i-m}{k}}{m!},\qquad
A_k(t)=\sum_{i=0}^{k}a_{k,i}t^i,\qquad E_k(t)=(1-t)^{k+1}A_k(t),
\]
\[
P_k(p)=e^{-1}E_k(p+1)+E_k(-p),\qquad
f_k(p)=\begin{cases}e^p&p<-1,\\P_k(p)&-1\le p\le0,\\e^{-p}&p>0.\end{cases}
\]

In particular \(P_k(-1)=e^{-1}\), \(P_k(0)=1\): \(A_k(0)=1\),
\(E_k(0)=1\) and \(E_k(1)=0\). Thus an equivalent strict-middle expression
uses \(P_k\) on \([-1,0)\) and \(e^{-p}\) on \([0,\infty)\). This endpoint
identity, not a change of target, will assign the center sample to the right
branch. No approximation of \(P_k\) is made.

Let \(N=n+1\), \(M=2^n\), \(h=2\pi L/2^N>0\), and

\[
p_j=-\pi L+hj\quad(j\in\mathbb N),\qquad
C=\left\lceil\frac{-1+\pi L}{h}\right\rceil_{\mathbb N}.
\]

The natural ceiling is zero for a nonpositive argument. Then \(p_M=0\) and

\[
0\le C\le M,\quad p_j<-1\iff j<C,\quad p_j<0\iff j<M,
\quad -1\le p_j<0\iff C\le j<M. \tag{1}
\]

Indeed \(j<\lceil x\rceil_{\mathbb N}\iff (j:\mathbb R)<x\) for natural
\(j\), and multiplication by \(h>0\) gives the first strict cut equivalence.
Strict monotonicity and \(p_M=0\) give the second. Were \(C>M\), the first
would give \(p_M<-1\), a contradiction. Algebra also gives

\[
C=\min\left(\left\lceil M-\frac{2^N}{2\pi L}\right\rceil_{\mathbb N},M\right). \tag{2}
\]

This is an exact real ceiling, not a ceiling computed with rounded pi. The
upper clamp is redundant under \(L>0\); the lower clamp is already natural
ceiling. Neither \(\pi L>1\), \(n\ge1\), nor \(k\le n\) is assumed.

## S2. Words, endpoints, and polynomial coordinates

For a Boolean word \(w=b_0\cdots b_{q-1}\), its first bit is most significant:

\[
J(\varnothing)=0,\quad J(bw)=b2^{|w|}+J(w),\qquad 0\le J(w)<2^{|w|}.
\]

Here a Boolean is interpreted as zero or one. Define
\(\phi_b(t)=(b+t)/2\), and
\(\Phi_{\varnothing}(t)=t\), \(\Phi_{bw}(t)=\phi_b(\Phi_w(t))\).
Induction gives \(\Phi_w(0)=J(w)/2^{|w|}\). Notice the nesting order:
the first digit acts on the outside of the suffix coordinate composition.

For a word of length \(N\), the sample index is the finite index \(j=J(w)<2^N\).
The existing flat sample API is indexed by this integer, whose physical
primitive-wire convention has wire zero least significant. Consequently
word position \(t\) corresponds to wire \(N-1-t=n-t\); one does not feed an
MSB-first list to wire-zero-first indexing without reversing positions.
The result here is a scalar flat-index identity, not a gate-level wire swap.

## S3. Literal Bernstein data and restriction

The basis and de Casteljau restriction below are defined for every natural
degree \(d\), independently of word width. The shared-core and free suffix
identities in S4 also allow any \(d\). Source coefficients and source
injections specialize \(d=2k+1\) as in S1. For \(0\le i\le d\), write
\(B_i^d(t)=\binom di t^i(1-t)^{d-i}\). For the Hermite specialization,
define, for every natural \(r\),

\[
\ell_r=\sum_{i=0}^k\sum_{v=0}^{k-i}
 [r=i+v]\,a_{k,i}\frac{\binom{k-i}{v}}{\binom d{i+v}},\qquad
\beta_r=e^{-1}\ell_r+\ell_{d-r}. \tag{3}
\]

Natural subtraction is truncated at zero, including \(d-r\) outside the finite
range. Only entries \(0,\ldots,d\) are used in finite rows. The denominators
in the double sum are nonzero, since \(i+v\le k\le d\). Degree elevation,
obtained by expanding \(1=(t+(1-t))^{k-i}\), gives

\[
\sum_{v=0}^{k-i}\frac{\binom{k-i}{v}}{\binom d{i+v}}B_{i+v}^d(t)
=t^i(1-t)^{k+1}.
\]

Sum over \(i\), then reflect \(B_i^d(1-t)=B_{d-i}^d(t)\), to get

\[
\sum_{i=0}^d\beta_i B_i^d(t)=P_k(t-1)\quad(t\in\mathbb R). \tag{4}
\]

For a natural-index coefficient sequence \(c\), define the de Casteljau
operator \(D_zc(i)=(1-z)c_i+zc_{i+1}\), and

\[
L_z(c)_i=(D_z^ic)_0,\qquad
R_u(c)_i=L_{1-u}(j\mapsto c_{d-j})_{d-i},\qquad
\mathcal R_{u,v}c=L_{(v-u)/(1-u)}(R_uc). \tag{5}
\]

These are literal total formulas for all real parameters and natural indices;
the field convention is \(x/0=0\). This does not give affine-restriction
semantics at \(u=1\). For \(u\ne1\), the actual restriction identity is

\[
\sum_{i=0}^d(\mathcal R_{u,v}c)_iB_i^d(t)
=\sum_{i=0}^dc_iB_i^d(u+(v-u)t). \tag{6}
\]

To prove it, expand \(D_z^q\) by the binomial theorem. Its zeroth entry is
the degree-\(q\) Bernstein sum. Left restriction pulls evaluation back by
\(t\mapsto zt\); reflecting gives right restriction's pullback
\(t\mapsto u+(1-u)t\). Composing cancels \(1-u\) only under \(u\ne1\),
yielding (6). No interval assumption is needed for this equality.

For arbitrary real origin \(a\), step \(g\), and natural first index \(s\),
put \(x(j)=a+gj\). For a suffix of length \(q\), inject the finite row

\[
c^{s,q}_i=(\mathcal R_{1+x(s),\,1+x(s+2^q)}\beta)_i\quad(0\le i\le d). \tag{7}
\]

If \(x(s)\ne0\), contracting this row at coordinate \(\Phi_w(0)\), with
\(|w|=q\), gives \(P_k(x(s+J(w)))\), by (4), (6), and the word coordinate
identity. The excluded endpoint \(s+2^q\), not the last sample, determines
the right restriction endpoint. This distinction is essential.

## S4. Finite shared cores and their orientation

Index finite input rows and output columns by \(0,\ldots,d\). The coefficient
unit vector at finite index \(i\) is the sequence \(E_i(j)=[j=i]\) for all
natural \(j\), hence is zero outside that single index. A shared core entry
is the half-subdivision of this unit vector, evaluated at output index \(j\).
In explicit row-update form these matrices are

\[
S_0(i,j)=\begin{cases}\binom ji/2^j&i\le j,\\0&i>j,\end{cases}\quad
S_1(i,j)=\begin{cases}\binom{d-j}{i-j}/2^{d-j}&j\le i,\\0&j>i.\end{cases} \tag{8}
\]

These are row-update matrices: \(c\) becomes \(cS_b\). They are transposes
of coefficient-column subdivision matrices; in this row convention \(S_0\)
is upper triangular and \(S_1\) is lower triangular. The de Casteljau sums at
one half show that \(cS_0=L_{1/2}c\) and \(cS_1=R_{1/2}c\) on finite entries.
Equivalently,

\[
\sum_{j=0}^dS_b(i,j)B_j^d(t)=B_i^d(\phi_b(t)). \tag{9}
\]

Let \(e_0(i)=[i=0]\). The backward suffix contraction is
\(Q_{\varnothing}=e_0\), \(Q_{bw}(i)=\sum_jS_b(i,j)Q_w(j)\).
Induction using (9) gives

\[
Q_w(i)=B_i^d(\Phi_w(0)),\qquad c^{s,|w|}Q_w=P_k(x(s+J(w)))\quad(x(s)\ne0). \tag{10}
\]

Every sum has \(d+1\) terms. This proves the finite matrix adapter rather
than assuming a polynomial/core equality as a hypothesis.

## S5. Interval traversal and its one-boundary schedule

For arbitrary natural \(l,u,s,m\), use the literal predicates

\[
F(l,u,s,m): l\le s\ \land\ s+m\le u,\qquad
O(l,u,s,m): s+m\le l\ \lor\ u\le s,\qquad
T=\neg F\land\neg O. \tag{11}
\]

They are defined even for reversed endpoints or zero size; we do not assume
they are then the usual disjoint interval trichotomy. All traversed sizes are
positive powers of two. At a node \((s,w)\), inspect \(F(l,u,s,2^{|w|})\)
first. If full, return the row readout (7)-(10). If not full but outside,
return zero. Otherwise, on \(w=bv\), continue at \(s+b2^{|v|}\) with suffix
\(v\); at an empty suffix return zero. Call the resulting scalar \(H(s,w)\).
For every arbitrary real affine coordinate with

\[
\forall j,\quad l\le j<u\ \Longrightarrow\ x(j)\ne0, \tag{12}
\]

induction on the word proves

\[
H(s,w)=[l\le s+J(w)<u]P_k(x(s+J(w))). \tag{13}
\]

For a full node its first point satisfies (12), so (10) applies, and the word
bound keeps the queried point in the node. An outside node cannot contain
that point. In the remaining case the child recursion preserves the queried
integer. At size one a node cannot be partial: if its integer point is
inside it is full; otherwise it is outside. This also resolves the base case.

To store only one unresolved scalar, let a schedule \(s_r\in\mathbb N\)
select the proposed boundary node of size \(2^r\), and put
\(j_{r,b}=s_{r+1}+b2^r\). The precise validity condition at width \(q\) is

\[
\forall r<q\ \forall b,\quad T(l,u,j_{r,b},2^r)\Longrightarrow s_r=j_{r,b}. \tag{14}
\]

This is a conditional interface, not an assumed target/core identity. On bond
\(\{\partial\}\sqcup\{0,\ldots,d\}\), set

\[
K_{r,b}=\begin{pmatrix}
[T(l,u,j_{r,b},2^r)]&[F(l,u,j_{r,b},2^r)]c^{j_{r,b},r}\\
0&S_b
\end{pmatrix},\qquad \tau=(0,e_0)^T. \tag{15}
\]

There is no return from a coefficient state to the boundary. Starting from
a coefficient state therefore gives \(Q_w\). Starting from the boundary
gives \(H(s_q,w)\), provided BOTH (14) and \(T(l,u,s_q,2^q)\) hold. For the
proof, inspect the selected child: full injects (10); outside has zero row;
partial leaves only the unresolved scalar and (14) identifies its next start.
The empty-word partial case is impossible. These statements do not require
(12) until (13) is applied.

The actual schedule is not a list of all prefixes:

\[
s_r=2^r\left\lfloor C/2^r\right\rfloor. \tag{16}
\]

For an aligned upper endpoint \(MB\), a partial size-\(M\) block beginning
at \(Mx\) satisfies \(Mx<l<M(x+1)\): its aligned upper endpoint is at most
the target's upper endpoint, and failure of fullness forces the lower cut
inside. Hence \(x=\lfloor l/M\rfloor\), proving uniqueness. For a prefix
interval \([0,u)\), partiality instead gives \(Mx<u<M(x+1)\), so
\(x=\lfloor u/M\rfloor\). Applied to (16), these prove (14) for \([C,2^n)\)
at width \(n+1\), and for \([0,C)\) at any width, respectively. The quotient
schedule identity for children is

\[
j_{r,b}=2^r\left(2\lfloor C/2^{r+1}\rfloor+b\right).
\]

Middle schedule validity holds for every natural cut \(C\), even without
\(C\le M\); that bound is used for the root-start identity. For any natural
lower endpoint, the node \([0,2^{n+1})\) is never full in
\([\mathrm{lower},2^n)\), and is partial if \(\mathrm{lower}<2^n\).
Since the actual \(C\le M\), \(s_{n+1}=0\); if \(C<M\), the middle root is
partial. If \(C=M\), disable the entire middle branch
instead of asserting partiality of an empty interval. For a fully included
middle block of positive size, (1) and strict monotonicity prove

\[
0\le1+p_s<1+p_{s+m}\le1. \tag{17}
\]

In particular \(p_s<0\), supplying (12) and the nonzero denominator condition.
Its excluded endpoint may be the center, where the right parameter equals one.

## S6. Scalar boundary mechanism and stable tails

For any scalar injection \(I(s,r)\) and free factor \(\gamma(r,b)\), let
\(U(\varnothing)=1\), \(U(bw)=\gamma(|w|,b)U(w)\). Replace the coefficient block
in (15) by one free state, its lower-right entry by \(\gamma(r,b)\), its injected
row by \([F(l,u,j_{r,b},2^r)]I(j_{r,b},r)\), and terminal by \((0,1)^T\).
The same full/outside/partial proof equates its boundary contraction to the
scalar interval traversal under (14) AND root partiality. If, additionally,

\[
I(s,|w|)U(w)=z(s+J(w))\quad\text{for all }s,w, \tag{18}
\]

that traversal is the masked target \([l\le s+J(w)<u]z(s+J(w))\).
Equation (18) is a genuine premise of this generic conditional lemma; it is
proved, not assumed, for the following left tail.

For the left branch use \(l=0,u=C\) and (16), with

\[
F_\ell(r,1)=1,\quad F_\ell(r,0)=e^{-h2^r},\qquad
I_\ell(s,r)=e^{p_s+h(2^r-1)}=e^{p_{s+2^r-1}}. \tag{19}
\]

The final equality uses positive integer \(2^r\), so the natural subtraction
at the last included index is legitimate. Induction and exponential addition
give \(U_\ell(w)=e^{-h(2^{|w|}-1-J(w))}\); multiplication by (19) gives
(18) with \(z(j)=e^{p_j}\). If \(C>0\), the width-\(N\) root is partial;
if \(C=0\), initialize this boundary state with zero. Thus its readout is
\([J(w)<C]e^{p_{J(w)}}\). For \(h\ge0\), every free factor lies in \([0,1]\).
For a full left block, its last point has \(p<-1\), so its injection also
lies in \([0,1]\). These boundedness claims have their stated sign/fullness
hypotheses and are not required as root premises.

For the right branch only one state is needed. Define

\[
F_r(r,0)=1,\quad F_r(r,1)=e^{-h2^r},\qquad
G(r,b)=\begin{cases}b&r=n,\\F_r(r,b)&r\ne n.\end{cases} \tag{20}
\]

Its free suffix product is \(e^{-hJ(w)}\). For a word of length at most \(n\),
all free levels have \(r<n\), so \(G\) agrees with \(F_r\) throughout that
suffix. For a full word \(bw\) of length \(N\), the first level is \(n\).
If \(b=0\), the product is zero. If \(b=1\), \(J(bw)=M+J(w)\), and
\(p_{M+J(w)}=hJ(w)\), giving \(e^{-p_{J(bw)}}\). This identity itself holds
for arbitrary real \(L\); identifying its support with the public branch
uses \(L>0\). Its factors are in \([0,1]\) when \(h\ge0\).

## S7. Direct sum, exact readout, and storage

Use the ordered tagged disjoint union of left boundary/free, middle
boundary/coefficient, and right states:

\[
\mathcal B=(\{\partial_\ell\}\sqcup\{\ell\})\sqcup
 ((\{\partial_m\}\sqcup\{0,\ldots,d\})\sqcup\{r\}).
\]

Let the full core be the block diagonal sum of the left two-state core, the
middle core (15), and the one-state right core (20). All cross-branch entries
are zero. The initial row has boundary entries \([C\ne0]\), \([C\ne M]\),
right entry one, and all free/coefficient entries zero. The terminal column
has entries \((0,1)\), \((0,e_0)\), and one on those three branches.
For any finite bond and terminal column \(v\), define backward contraction

\[
V(\varnothing,i)=v_i,\qquad
V(bw,i)=\sum_{j\in\mathcal B}K_{|w|,b}(i,j)V(w,j),\qquad
\mathcal A(w)=\sum_i\lambda_iV(w,i). \tag{21}
\]

This definition is total for every word length, every real \(L\), and every
supplied kernel. The Hermite identification asserts the following only at
length \(N=n+1\) and \(L>0\):

\[
\boxed{\mathcal A(w)=f_k(p_{J(w)})\qquad(|w|=n+1).} \tag{22}
\]

Indeed block diagonality splits (21) into a sum of the three branch readouts;
this follows by induction, since every cross-block summand is zero. Their
values are the left, middle and right samples masked by \(j<C\),
\(C\le j<M\), and \(M\le j\), respectively. Since \(C\le M\), exactly one
mask holds for each natural \(j\). Equations (1), (13), (18)-(20), and the
endpoint identity in S1 identify that sum with the literal sample, with no
cancellation between large out-of-support values.

The middle bond has \(1+(d+1)=2k+3\) states. The left and right bonds have
two and one, so \(|\mathcal B|=2k+6\). An alternative written middle carrier
\(\{\partial\}\sqcup\{0,\ldots,2k+1\}\) has the same cardinality; the
count alone would not prove (22). The actual dense two-slice core address
space consists of a stage \(t\in\{0,\ldots,n\}\), a Boolean bit, an input
bond and an output bond. Its cardinality is exactly

\[
2(n+1)(2k+6)^2,\qquad\text{entry}(t,b,i,j)=K_{n-t,b}(i,j). \tag{23}
\]

The subtraction in the total entry formula is natural subtraction; the stated
finite stage range makes \(n-t\ge0\). This is a dense address count in real
scalars, not a minimal sparse count, evaluation runtime, allocation algorithm,
integer-word size theorem, or finite-bit storage bound.

## S8. Totality, degenerate inputs, and remaining boundary

All coefficient and kernel definitions are literal formulas, with finite sums,
tagged cases, total real division and recursion decreasing word length. There
is no choice of an existentially characterized kernel, no quotient, and no
arbitrary representative. Empty contractions return their explicit terminals;
an unresolved boundary has terminal value zero. Arbitrary supplied schedules
and arbitrary real grid parameters define numbers but need not satisfy (22).
Generic traversal theorems use exactly (12); generic contraction adapters use
exactly (14) AND root partiality; the scalar target adapter uses (18).
Do not conjoin all three as new hypotheses of (22): the actual grid and
formula-derived branches provide each when needed.

The exact theorem includes \(n=0\) \(one digit\), \(k=0\), \(C=0\) \(empty left
tail\), and \(C=M\) \(empty middle\). It makes no public-sample claim for an
incorrect word length, \(L\le0\), or an arbitrary scientific target. No
normalizer divides (22). A separate normalized-state construction would have
to supply the true norm of the complete sample, not the norm of one branch.

There is no certified unitary/isometry, primitive circuit, clean-workspace
action, coherent oracle, postselection probability, amplification bound,
QR step, finite-precision stability, numerical error tolerance, classical
preprocessing runtime, gate count, depth, connectivity or readout cost in
this source. In particular (23) cannot close a polynomial resource claim in
\(n\) and \(\log(1/\epsilon)\): selecting and bounding \(k,L\), normalization,
finite-bit evaluation and error propagation remain separate obligations.
No alternative algorithmic OR-route is asserted here. Full/outside/partial
are cases within one proof, and the three branch outputs form a required
sum, not three independently sufficient preparations.
