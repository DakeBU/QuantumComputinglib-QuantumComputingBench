# Sequential primitive assembly on literal physical wires

LOCAL retrospective mathematical source and reusable lesson, version 1.
Author: Codex worker `/root/sequential_assembly_c48_source_author`.
This is a newly authored account of an existing construction, not an original
paper, a pre-proof source, an independent review, or a new synthesis result.
The claims below concern exactly supplied finite instruction lists.

## S0. The question and its boundary

Given a bond register, an initial circuit on it, and one small circuit for each
emitted bit, construct a single chronological instruction list on their final
physical wires. Identify all amplitudes arising from zero data inputs, retain
the initial preparation cost, and expose the reversal needed when the first
emitted bit is interpreted as the most significant data bit. The bond can
change at every stage; previously emitted data bits must not change at later
stages. A wire label remaining fixed does not mean its state is preserved.

The input consists of a natural number q, a natural number n, an actual finite
initial list J on q wires, and a family C_t of actual finite lists on q+1 wires,
indexed by all natural numbers t. Only C_0 through C_(n-1) are used. No promise
about later lists is needed. No target state, tensor core, support promise,
normalization witness, unitary completion algorithm, or cost-free initial
state is supplied. Empty lists and q=0 or n=0 are legal.

## S1. Finite carriers, exact gates, and standing conventions

Let B_m be the set of functions {0,...,m-1} to {0,1}; it has 2^m elements.
B_0 contains the unique empty word. All vectors have complex entries and all
matrices use output rows and input columns. Write a|x for concatenation of
a in B_m with x in B_t, and a·u for appending a bit u to a. The empty word is
the unit for concatenation. Write 0_m for the constant-zero word (also empty
when m=0). Matrix multiplication is (MN)[r,s]=sum_z M[r,z]N[z,s].

An instruction on m wires is one of X_i, RY_i(theta), RZ_i(theta), or
CX_(i,j), with i,j in {0,...,m-1}, i different from j. An angle is a supplied
exact real expression: rational, rational multiple of pi, twice arccos of a
rational in [-1,1], twice arccos of the square root of a rational in [0,1],
an arbitrary real, or an expression obtained by addition, negation and rational
scaling. The inequalities are part of the respective expression's input
interface. No real evaluation or finite representation cost is assumed free
in a computational claim; no such computational claim is made here.

The one-bit matrices, in row/column order 0,1, are

\[
 X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 RY(\theta)=\begin{pmatrix}\cos(\theta/2)&-\sin(\theta/2)\\
 \sin(\theta/2)&\cos(\theta/2)\end{pmatrix},\quad
 RZ(\theta)=\operatorname{diag}(e^{-i\theta/2},e^{i\theta/2}). \tag{1}
\]

A one-bit instruction has zero matrix entry unless every other wire agrees,
and otherwise has the indicated one-bit entry. CX permutes a basis word by
flipping its target exactly when its control is 1. A list is chronological:
if L=[g_0,...,g_(k-1)], define E(L)=E(g_(k-1))...E(g_0); E([])=I.
Consequently E(L++K)=E(K)E(L). These are the standing semantic definitions,
not assumed implementations of an unspecified external gate.

All gates are unitary: X and CX permute an orthonormal basis; the columns of
RY are orthonormal by cos^2+sin^2=1; each diagonal entry of RZ has modulus one.
Finite products are unitary. This observation explains normalization for an
actual basis input but is not a premise required for the algebraic identities
below. No global-phase quotient is taken: all equations are literal complex
amplitude equalities, preserving relative and global phases.

## S2. Padding and physical placement

For a list L on m wires, define pad_t(L) by embedding each existing target
and control as the same integer among m+t wires. It inserts no instructions.
For any complex matrix M on B_m, let P_0(M)=M and let P_(t+1)(M) be P_t(M)
tensored with identity on a new highest wire. Equivalently,

\[
 P_t(M)[a|x,b|y]=[x=y]M[a,b],\qquad
 a,b\in B_m,\ x,y\in B_t. \tag{2}
\]

Here [p] equals 1 if p is true and 0 otherwise. Formula (2) follows by
induction on t: for the last new bit, the tensor identity supplies its equality
indicator; multiply that indicator by the prefix equality indicator. For t=0
the equality of the two empty words is automatic. Embedding a single gate
gives E(pad_t([g]))=P_t(E(g)) directly from (1) and the untouched-coordinate
conditions (or the CX basis permutation). Multiplication of padded matrices
preserves products because the intermediate passive word is forced to agree.
Thus induction on the list gives E(pad_t(L))=P_t(E(L)).

More generally, let e be a bijection from m old wire names to m' new wire
names. Replace every target and control in L by its image under e; call this
list e_*L. Both boundary basis labels change:

\[
 E(e_*L)[r,s]=E(L)[r\circ e,s\circ e]. \tag{3}
\]

To prove (3), first consider one instruction. The touched bits agree under e,
the untouched equality conditions correspond bijectively, and injectivity
preserves distinct CX wires. Therefore the gate entries agree. For a product,
the substitution z -> z composed with e is a bijection of the intermediate
basis set, so finite matrix multiplication preserves the equality. Induction
on L, starting from identity, proves (3). This is a placement construction
for the entire program, not a physical state-permutation instruction added to
an already fixed program. It supplies no uncharged routing between fixed
hardware locations. All-to-all named-wire instructions are the model.

For any list L, define R(L) as its number of RY instructions, C(L) as its
number of CX instructions, and G(L) as its length. Padding and placement
preserve all three: they replace each instruction by exactly one of the same
kind, with the same angle. Counts add under concatenation. X and RZ contribute
to G but not to R+C.

## S3. Where one stage acts

Before stage t the growing register has order bond (q wires), old data (t
wires). The local list C_t expects bond on its first q wires and a fresh bit
on its last wire. First pad C_t by t wires; its temporary order is bond,
fresh, old data. Define the bijection p_(q,t) by the following exhaustive cases:

\[
 i\mapsto i\ (0\le i<q),\qquad q\mapsto q+t,\qquad
 q+1+j\mapsto q+j\ (0\le j<t). \tag{4}
\]

Its inverse sends the first q indices to themselves, each q+j with j<t to
q+1+j, and q+t to q. These cases are disjoint and cover both index sets,
including empty ranges. Define T_t(L)=p_(q,t)*pad_t(L), a list on q+t+1
wires. Define its matrix version Q_t(M) by the same padding and reindexing.
The basis pullback is

\[
 (a|x)\mathbin{\cdot}u\ \circ p_{q,t}=(a\mathbin{\cdot}u)|x. \tag{5}
\]

Checking (5) in the three cases of (4), then applying (2) and (3), proves

\[
 E(T_t(L))=Q_t(E(L)),\qquad
 Q_t(M)[(a|x)\mathbin{\cdot}u,(b|y)\mathbin{\cdot}v]
 =[x=y]M[a\mathbin{\cdot}u,b\mathbin{\cdot}v]. \tag{6}
\]

Every old data coordinate is therefore preserved by the stage, whereas the
bond and new bit can change. Bond wire *positions* are preserved by (4), not
bond amplitudes by the stage. The fresh wire is exactly q+t. The instruction
counts R,C,G of T_t(L) equal those of L. For example, q=2,t=3 gives images
(0,1,5,2,3,4); this is a placement example, not a SWAP circuit.

## S4. The flattened list and its full matrix definition

Define A_0=[] on q wires. Recursively define

\[
 A_{t+1}=\operatorname{pad}_1(A_t)\mathbin{++}T_t(C_t),\qquad
 F_0=I_{B_q},\quad F_{t+1}=Q_t(E(C_t))P_1(F_t). \tag{7}
\]

At a fixed final width q+n, the lifting of earlier lists changes only their
types: all their numerical wire labels remain unchanged. By induction, using
chronological concatenation and (6), E(A_n)=F_n as complete matrices. This
complete matrix identity has no clean-input restriction; F_n is defined by
the actual supplied stage matrices, including all dirty-input columns. It is
not a claim that a smaller collection of clean columns determines an arbitrary
unitary operator.

## S5. Accumulation on the clean data-input sector

For each t define a local square matrix on {0,1} x B_q by

\[
 U_t[(u,b),(v,a)]=E(C_t)[b\mathbin{\cdot}u,a\mathbin{\cdot}v]. \tag{8}
\]

For arbitrary complex boundary v:B_q -> C, define a state R_t(v) on B_t x B_q
by

\[
 R_0(v)[\varnothing,b]=v[b],\qquad
 R_{t+1}(v)[x\mathbin{\cdot}u,b]
 =\sum_{c\in B_q} U_t[(u,b),(0,c)]R_t(v)[x,c]. \tag{9}
\]

This recurrence is precisely: append a new bit in zero, act with U_t on
fresh-bit and bond, leave the old-data prefix untouched, then regroup the
basis to put the new bit last in the emitted word. It is ordinary linear
action, not measurement. Writing the full finite sum gives a passive-word
indicator [x=y] and a fresh-input indicator [v=0]; both sums collapse to (9).
The boundary need not be normalized, nonzero, real, or positive.

For every a,b in B_q and x in B_n, with no restrictions on the C_t,

\[
 F_n[b|x,a|0_n]=R_n(\delta_a)[x,b],\qquad
 \delta_a[c]=[c=a]. \tag{10}
\]

Proof: for n=0, the left side is the identity entry [b=a] and the right side
is delta_a[b]. At the successor, write x·u for the output word and expand
(7) over an intermediate basis (c|y)·v. The lifted F_n forces v=0 by (2);
the placed stage forces y=x by (6). Exactly

\[
 \sum_{c\in B_q}E(C_n)[b\mathbin{\cdot}u,c\mathbin{\cdot}0]
 F_n[c|x,a|0_n] \tag{11}
\]

remains. Substitute the induction hypothesis and (8); (9) proves (10).
Since E(A_n)=F_n, (10) also identifies the actual flattened list's column.
Every x and every b occurs, including nonzero bond labels. No off-sector
amplitude is ignored, but it has not been shown zero merely by being named.

The recurrence is linear in its boundary, with the explicit formula

\[
 R_n(v)[x,b]=\sum_{a\in B_q}R_n(\delta_a)[x,b]v[a]. \tag{12}
\]

For n=0 the delta sum equals v[b]. If (12) holds at n, substitute it into
(9), distribute multiplication, and interchange the two finite sums. The
inner sum is R_(n+1)(delta_a), proving (12). No convergence or division is
involved.

## S6. The initial bond is not free

Define W_n=pad_n(J)++A_n. The input bond basis label a can be any element of
B_q, not only zero. Put v_a[c]=E(J)[c,a]. For every b and x,

\[
 E(W_n)[b|x,a|0_n]=R_n(v_a)[x,b]. \tag{13}
\]

Expand the product E(A_n)P_n(E(J)). Formula (2) forces the intermediate
data word to 0_n; the remaining sum over c is
sum_c R_n(delta_c)[x,b]E(J)[c,a], by (10). Formula (12) gives (13).
An arbitrary externally supplied v is useful for (9) and (12), but (13)
uses the column of an actual initial circuit and does not manufacture a
circuit for an arbitrary v. For an all-zero physical input choose a=0_q.

## S7. Actual list counts and the exact model boundary

For D equal to R or C, all q,n and supplied lists satisfy

\[
 D(A_n)=\sum_{t=0}^{n-1}D(C_t),\qquad
 D(W_n)=D(J)+\sum_{t=0}^{n-1}D(C_t). \tag{14}
\]

Proof: the empty list has count zero; (7) and the count invariance of padding
and placement add exactly D(C_t) at the successor. Adding the initial padded
list proves the second equality. Padding and single-stage placement also
preserve G, as established in S2-S3. Equation (14) is a selected-kind count,
not a blanket total gate or depth certificate.

Let h be a supplied natural bound such that, for every natural t<n,
R(C_t)+C(C_t) <= h. Then

\[
 R(W_n)+C(W_n)\le R(J)+C(J)+nh. \tag{15}
\]

Sum each of the n inequalities, use (14), and collect the initial counts.
There is no assumption on t>=n. At n=0 the sum is empty and the bound is
equality, irrespective of h. This hypothesis is a real input promise for
the conditional bound; it is not proved for arbitrary supplied lists.

There are zero oracle instructions: the instruction grammar has none. This
does not say that producing the lists or their real angles is cost-free.
No bound on X/RZ counts, synthesis precision, Clifford+T cost, classical
precomputation, depth, hardware connectivity, readout, or runtime follows
from (15). For example, a list containing only many X instructions has R+C=0
and large G. All equations are exact-real mathematical semantics; there is
no numerical tolerance, postselection, approximation probability, or hidden
amplification cost.

## S8. Public low-data-wire convention and the MSB/LE adapter

The growing circuit order has bond first and data in emission order. Place
the *entire* W_n list by the bijection o_(q,n) from q+n wires to n+q wires:

\[
 i\mapsto n+i\quad(0\le i<q),\qquad
 q+t\mapsto n-1-t\quad(0\le t<n). \tag{16}
\]

The inverse sends data position j<n to q+(n-1-j), and bond position n+i to i.
For x in B_n let rev(x)[t]=x[n-1-t]. For n=0 this is the unique empty
function; no invalid index is evaluated. Direct substitution proves

\[
 (x|b)\circ o_{q,n}=b|\operatorname{rev}(x). \tag{17}
\]

Define V_n=o_(q,n)*W_n. Applying (3), (17), and (13) proves the public column
identity, for every a,b,x:

\[
 E(V_n)[x|b,0_n|a]=R_n(v_a)[\operatorname{rev}(x),b]. \tag{18}
\]

Low data wires use the little-endian value sum_(j<n) 2^j x[j]. If one
interprets the emitted word w as most-significant-first, its value is
sum_(t<n)2^(n-1-t)w[t]; substituting w=rev(x) makes these integers equal.
Thus stage zero is placed at the highest data wire and the bond follows all
data wires. Example q=2,n=3 gives images (3,4,2,1,0). Both input and output
labels are reindexed; no operation permutes a previously prepared physical
state for free. All R,C,G counts are preserved by this placement, so (15)
holds for V_n with the same right side. Although these following bond wires
are often intended as clean workspace in applications, (18) alone does not
assert that their output is zero.

## S9. Degenerate cases and what a stronger claim must supply

When q=0 the bond carrier B_q is a singleton, not an empty state space.
There is still a fresh one-bit stage, and every bond sum in (9)-(13) has one
term. An initial circuit on zero wires must be empty since no gate target
exists. The stage placement still inserts the new bit at t, with all old
data passive. When n=0, A_0 is the empty circuit, W_0=J, o_(q,0) fixes the
bond coordinates, and (18) reduces to E(J)[b,a]=v_a[b]. When q=n=0 every
assembled, initial and public circuit matrix is the 1 by 1 identity. When any C_t is empty its matrix is identity;
that stage leaves the bond unchanged and emits a zero bit. These conclusions
follow by substituting the empty-word and identity definitions above, without
positivity/rank assumptions or a default chosen output.

To conclude a particular tensor contraction, an application must identify
the occupied local clean columns E(C_t)[b·u,c·0] with its tensor core, and
justify the initial boundary. If the identification holds only on an active
bond set, an initial-support invariant and preservation of that support are
additional obligations. To conclude terminal clean bond, it must prove
R_n(v_a)[x,b]=0 for every non-clean b, and identify the remaining amplitudes.
This is not implied by old data being passive. A terminal prescription on
all padded input columns may even be incompatible with unitarity; restrict
it to a justified occupied subspace when necessary.

To replace the clean-sector identity by a target full-operator equality, an
application must additionally specify and verify all nonzero-data-input
columns (or a sufficient independent full-operator argument). A phase-exact
full-matrix example is diag(1,1) versus
diag(1,-1): their first columns coincide and their second columns do not.
These matrix examples distinguish information content, not an additional
instruction constructor.

Finally, no Hermite formula, parameter-dependent rank bound, source core
generator, small-unitary compiler, terminal cleanup proof, finite-bit
algorithm, or hardware routing has been constructed by this lesson. Those
are separate AND-prerequisites for those stronger application claims.
