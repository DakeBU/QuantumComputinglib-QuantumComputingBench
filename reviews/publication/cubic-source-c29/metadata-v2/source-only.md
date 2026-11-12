# Cubic grid operators: rational constructions and their semantic boundaries

This is a retrospective mathematical source for a legacy local construction,
not an external paper, a pre-proof statement seal, a new complexity result, or
an independent review. Historical formalizer identity is unknown. The subject
is two different operators and several explicitly conditional construction
routes. An equation about an extracted matrix is not automatically a theorem
about a circuit, its cost, or normalized state preparation.

## S01. Carriers, the two targets, and normalization

Let $n\geq0$, $N=2^n$, and $J=\{0,\ldots,N-1\}$. The original requests
use positive $n$; the formulas below extend to $n=0$ without changing any
denominator, because $N\geq1$. Scalars are exact rationals unless another
scalar carrier is explicitly supplied. Matrices are functions of finite row
and column indices. Products mean finite sums, in column-vector convention:
\[
 (AB)_{ij}=\sum_{k=0}^{m-1}A_{ik}B_{kj}.
\]
The zero matrix and identity have their literal entrywise meanings. Equality
of matrices below means equality at every entry, not equality of a circuit
description. Define
\[
 x_j=j/N,\qquad a_j=x_j^3,\qquad v=(a_j)_{j\in J}.
\]
The first target is the **rank-one operator**
\[
 O_{rc}=\begin{cases}a_r&c=0,\\0&c\ne0.\end{cases}
 \qquad O=|v\rangle\langle0|.
\]
It maps the zero input basis vector to the generally unnormalized vector
$v$, and all other input basis vectors to zero. It is not a state-preparation
unitary. Preparing $v/\|v\|_2$ requires a separate nonzero-norm condition,
normalization, and a first-column state-action certificate. At $n=0$, $v=0$,
so the normalized target is undefined. No normalization convention is inserted
at this endpoint.

The second target is the **diagonal operator**
\[
 D_{rc}=\delta_{rc}a_r.
\]
These are not interchangeable. In particular, multiplying diagonal blocks
does not produce the rank-one operator. A useful linear input is
\[
 X_{rc}=\delta_{rc}x_r.
\]
The chosen conservative scale for $O$ is $\alpha=N$; the chosen scale for
$D$ and $X$ is one. The requested exploratory error tolerance is the exact
rational $10^{-10}$. The target records and descriptive strings encode
intent, not proofs of a unitary, norm inequality, or scalable implementation.

## S02. Elementary range, norm, and path-count facts

Because $0\leq j<N$ and $N>0$, $0\leq x_j<1$. Multiplication by a
nonnegative number proves inductively that $0\leq x\leq1$ implies
$x^k\leq1$ for every natural $k$. Thus $0\leq a_j\leq1$, in fact
$a_j<1$, and $a_j^2=x_j^6\leq1$. The squared norm is the finite rational sum
\[
 s_n=\sum_{j=0}^{N-1}a_j^2=\sum_{j=0}^{N-1}(j/N)^6\leq N\leq N^2.
\]
For the last inequality use $N\geq1$. This certifies a conservative algebraic
scale bound $s_n\leq\alpha^2$. It does not construct a dilation or prove a
gate implementation. The first three exact diagnostics are
\[
 s_1=1/64,\qquad s_2=397/2048,\qquad s_3=46205/65536.
\]
They are finite rational identities; they are not an asymptotic experiment or
a general closed formula for this sum.

The basic counting lemma is: for natural $m,k$ with $k\leq m$, exactly $k$
indices $t\in\{0,\ldots,m-1\}$ satisfy $t<k$. An induction removes the zero
index and shifts the others when $k,m>0$; $k=0$ contributes none. Filtering
the finite enumeration and counting its true predicate give the same number.
Applied to the cubic threshold, $j^3<N^3=2^{3n}$, so
\[
 \#\{0\leq t<2^{3n}:t<j^3\}=j^3.
\]
The weaker non-strict capacity bound suffices for counting; strict capacity
is needed for storing the payload in a finite register. Also
$2^{4n}=N^4$, and rational arithmetic gives
\[
 a_j/N=j^3/N^4.
\]
These facts explain the intended accepted-path ratio but do not prove that a
Hadamard circuit has precisely those accepted paths or phases.

## S03. Rank-one clean-block interface and three unfinished transcripts

For any rational scale $\alpha$ and matrix $B\in\mathbb Q^{N\times N}$,
consider the two-part contract
\[
 [\forall r,\ \alpha B_{r0}=a_r]\quad\land\quad
 [\forall r,c\ne0,\ B_{rc}=0].
\]
Splitting on whether $c=0$ proves $\alpha B=O$ pointwise. No nonzero-scale
premise is necessary for that implication: multiplication, not division, is
the conclusion. Supplying the contract remains a mathematical obligation;
the implication does not supply it. The arithmetic-wrapped and counting
routes both specialize the scale to $N$.

The first proposed arithmetic middle block consists of seven **uninterpreted
oracle labels**, in this order: load $j/N$, square a fixed-point value,
multiply by the input value, transduce the resulting amplitude to a signal
rotation, undo multiplication, undo squaring, undo loading. Its declared
layout has $n$ system qubits, one signal qubit, and $3n+p+2$ pure workspace
qubits; $p=40$ is a seed, not a precision theorem. The transcript has seven
unexpanded calls and sequential depth seven in the label-counting model.
There is no proof here that the labels are implemented, that daggers really
are inverses, or that this middle block has the rank-one shape.

The proposed rank-one wrapper adds a zero-input clean filter and output-row
generation before that middle block, then filter cleanup after it. Row
generation is not undone because the generated row is the desired system
output. This adds three labels: ten calls and depth ten, with pure workspace
$4n+p+3$, hence total auxiliary count $4n+p+4$. At $n=2,p=40$ its label
tuple is $(10,10,52,10)$. A declared cleanup name is not a clean-ancilla proof.

The alternative counting transcript has eight labels: compute a zero-input
flag; set a separate reject signal for a nonzero input column; Hadamards on
the row/threshold path registers; XOR the row into the system; cubic threshold
comparison; undo that comparison; Hadamards again; undo the initial flag
computation. Its pure workspace is
$1+4n+(4n+3)=8n+4$, plus one reject signal, so auxiliary count is $8n+5$.
The $4n$ path qubits are distinct from the additional cube/comparator
workspace. The nonzero-column reject signal must survive the flag cleanup:
merely undoing a computed flag can restore a forbidden clean branch. This is
the purpose of the separate reject label, not a proof that the repaired
transcript works. The row XOR is not undone, for the same output-register
reason as above. At $n=2$ the label tuple is $(8,8,21,8)$.

All three transcript resource statements are literal accounting identities.
To reach a rank-one block encoding they still require interpreted oracle
actions, coherent arithmetic and comparisons, Hadamard amplitudes and phases,
unitarity, all nonzero-column rejection, clean-workspace semantics, and the
complete clean-block theorem. To reach normalized state preparation they
additionally require a nonzero accepted branch, its success probability and
any amplification or normalization cost.

## S04. Exact rational eight-dimensional reflection

For $u,v\in\mathbb Q^8$, write
\[
 u\cdot v=\sum_{i=0}^7u_i v_i,
 \qquad e=(1,0,\ldots,0).
\]
Given $v\cdot v=1$ and $v_0\ne1$, let
\[
 w=e-v,\quad d=w\cdot w=2(1-v_0)\ne0,\quad
 H_{ij}=\delta_{ij}-(2/d)w_iw_j.
\]
Expanding $w\cdot w$ proves the formula for $d$. The clean entry is
\[
 H_{00}=1-\frac{2(1-v_0)^2}{2(1-v_0)}=v_0.
\]
For column indices $i,j$, expand their inner product:
\[
 \sum_k H_{ki}H_{kj}
 =\delta_{ij}-c w_iw_j-c w_jw_i+c^2w_iw_jd
 =\delta_{ij},\qquad c=2/d.
\]
The cancellation uses $c^2d=2c$. Symmetry gives the analogous row identity.
Thus both $H^\mathsf TH=I$ and $HH^\mathsf T=I$ hold over the rationals.
Finite-coordinate enumeration, delta-vector inner products, bilinearity, and
translation between an eight-term sum and the finite fold are supporting
identities, not additional physical assumptions.

The underlying formula is total rational arithmetic: division by zero has
the carrier's totalized value. Its stated reflection and clean-entry claims
are restricted to the unit-vector/nontrivial-coordinate locus above. No
off-locus mathematical reflection theorem is asserted by writing the formula.
In particular the nontrivial-coordinate guard is not silently dropped.

## S05. Controlled direct sum, basis order, and finite fibers

Use the flattened basis $(b,s)\mapsto bN+s$, with ancilla $b\in\{0,\ldots,7\}$
first and system $s\in J$ second. The inverse decodes a full index $q<8N$
as $s=q\bmod N$, $b=\lfloor q/N\rfloor$. Positivity of $N$ justifies both
ranges, and quotient/remainder reconstruction proves the two encodings are
inverse. The clean embedding is $s\mapsto(0,s)$, numerically the index $s$.
This is a three-qubit ancilla matrix construction, not the earlier one-signal
oracle layout; no hardware wire endianness is inferred beyond this flattening.

For a supplied branch family $v_s\in\mathbb Q^8$, define
\[
 U_{(b,s),(c,t)}=\begin{cases}H(v_s)_{bc}&s=t,\\0&s\ne t.\end{cases}
\]
If every branch is unit and has $v_{s,0}\ne1$, then $U$ is rational
orthogonal. For different system branches every inner-product summand is
zero. For the same branch, only the fiber
\[
 F_s=\{bN+s:0\leq b<8\}
\]
contributes; the full sum reduces to the eight-term branch inner product.
To justify this reduction rigorously, discard only summands proved zero;
the filtered full enumeration and $F_s$ have equal membership and no
duplicates, hence are permutations; finite addition is permutation invariant.
The map $b\mapsto bN+s$ is injective, by decoding the ancilla. Reindexing the
fiber gives exactly the branch row or column sum, and reconstruction shows the
ambient identity entry is the same branch identity entry. This proves both
row and column orthogonality, not only one direction.

If in addition $v_{s,0}=q_s$, its clean block is
\[
 U_{(0,r),(0,c)}=\delta_{rc}q_r.
\]
Taking $q_s=x_s$ gives $X$; taking $q_s=a_s$ gives $D$. For the first
case, $x_s<1$ supplies the nontrivial guard. For the second, $a_s<1$ does.
In a general supplied-value case the guard remains a separate premise.

## S06. Four squares, existence, and chosen matrix witnesses

The number-theoretic input is Lagrange's theorem: every natural $m$ is a sum
of four natural squares. Apply it separately to each nonnegative residual.
For the linear target choose $a,b,c,d\in\mathbb N$ with
\[
 N^2=j^2+a^2+b^2+c^2+d^2,
\]
and use the literal vector
\[
 v_j=(j/N,a/N,b/N,c/N,d/N,0,0,0).
\]
Its squared norm is one by dividing the displayed identity by $N^2\ne0$;
its zeroth coordinate is $x_j$. For the cubic target use
\[
 N^6=j^6+a^2+b^2+c^2+d^2,
 \qquad
 v_j=(j^3/N^3,a/N^3,b/N^3,c/N^3,d/N^3,0,0,0).
\]
The same calculation gives unit norm and zeroth coordinate $a_j$. Residual
subtraction is natural subtraction, justified by $j^2\leq N^2$ or
$j^6\leq N^6$; it is not a truncated-negative shortcut.

These constructions establish existence of a whole rational branch family
and therefore an $8N\times8N$ rational orthogonal matrix whose clean block
is $X$, or respectively $D$, at scale one. Selecting a family from an
existence proof is a noncanonical representative choice. The chosen matrix
may depend on the selected four-square witnesses; the certified clean block
does not. No uniqueness, efficient search for witnesses, uniform gate
synthesis, or polynomial classical preprocessing follows from this choice.

A matrix-level input package for $X$ contains a matrix, an arbitrary
embedding of the system basis, rational orthogonality, clean-block equality,
scale-one equality, and declared cleanup/resource propositions with proofs.
It can forget the extra fields to expose an exact-clean-block package. Such
a smaller package means only a matrix, target, embedding and equality; it
does not itself mean orthogonality or an injective physical clean embedding.

The chosen Householder instance uses the explicit clean embedding above.
Its declared cleanup proposition is the very same clean-block equality,
described as system-index preservation with no workspace. Its resource is
one oracle label with a label-count equality. Those are exact facts about
this package, but there is no matrix-denotation link from the label to $U$
and no elementary-gate expansion. A generic cubic exact package similarly
stores an exact-clean-block payload plus orthogonality, scale-one and arbitrary
cleanup/resource propositions. In that generic type the payload's target is
not constrained to be $D$; the specific chosen instance sets it to $D$
and separately proves the target equality. The choice of a one-label resource
for that instance must not be read as one elementary gate.

## S07. Product arithmetic and the separate QSVT boundary

Finite-sum collapse proves that two diagonal matrices multiply entrywise on
the diagonal: for a fixed output row only the equal summation index survives.
Applying this twice gives
\[
 X^3_{rc}=\delta_{rc}x_r^3=D_{rc}.
\]
Extract the already known clean matrix of the linear Householder construction,
and multiply that clean matrix three times. Equality propagates through
finite matrix multiplication, so the resulting **algebraic clean-matrix
certificate** has target $D$. It records products of normalizers and term
counts as arithmetic metadata. It does not supply a larger unitary, the
ancillas that isolate intermediate clean blocks, a composed circuit, or its
orthogonality/resource theorem. The generic fact that the clean block of
$U^3$ need not equal the cube of the clean block is not bypassed.

An optional QSVT-facing route chooses $P(x)=x^3$. On the actual grid spectrum,
$|P(x_j)|\leq1$. A local side-condition record contains a natural degree set
to three, a Boolean parity label set to true, and this spectral bound. The
degree/parity equalities are labels in that record; they do not establish a
full polynomial phase-synthesis theorem or all global QSVT admissibility.

A stronger external supplier must provide: a certified linear input package;
an output exact-clean-block package; output orthogonality; equality of the
output target to $X^3$; and explicit global-admissibility, cleanup and
resource propositions with proofs. The target equality then identifies the
output with $D$. A generic consumer package retains the input payload,
the description of $P$, local side-condition inhabitation together with the
supplied global proposition, and the proved output-target equality. These
are conditional extraction/transport operations, not an implementation of
QSVT. In particular arbitrary proof-carrying proposition fields are not
substitutes for actual phase, circuit, cleanup, or cost semantics.

## S08. Supplied diagonal approximations and a non-vacuous error bound

For any supplied $q:J\to\mathbb Q$, set $A_q=\operatorname{diag}(q)$.
Define rational absolute value literally by $|z|=z$ for $z\geq0$, and
$|z|=-z$ otherwise. Let
\[
 E_\epsilon(A,B):\quad\epsilon\geq0\quad\land\quad
 \forall z\in\mathbb Q^m,
 \sum_r\left(\sum_c(A_{rc}-B_{rc})z_c\right)^2
 \leq\sum_r(\epsilon z_r)^2.
\]
This is a squared Euclidean induced-error predicate on rational vectors,
with no square-root, completion, real/complex-vector extension or physical
gate approximation silently added. It also handles $m=0$: the sums are
empty and only the nonnegative-error condition remains.

If $A,B$ are diagonal, the action of their difference at row $r$ is
$(A_{rr}-B_{rr})z_r$: all other summands vanish, and each finite index occurs
exactly once. If $|A_{rr}-B_{rr}|\leq\epsilon$ and $\epsilon\geq0$, then
\[
 ((A_{rr}-B_{rr})z_r)^2\leq(\epsilon z_r)^2.
\]
Indeed $u^2=|u|^2\leq\epsilon^2$, multiply by $z_r^2\geq0$, then sum.
Monotonicity of a finite additive fold proves $E_\epsilon(A,B)$. A
dimension-parametrized bridge may abstract this implication to another
supplied error relation; the concrete relation above genuinely satisfies it.
It is non-vacuous: in dimension one, identity versus zero at error zero fails
on the vector with entry one.

Consequently, the supplied scalar bounds
\[
 \forall j,\quad |q_j-a_j|\leq\epsilon,\qquad\epsilon\geq0
\]
imply both all-entry error bounds and $E_\epsilon(A_q,D)$. Off-diagonal
entries are zero, which is why this does not lose an $N$ factor. The result
does not choose $q$, prove such bounds for a numerical producer, or certify
a dilation of $A_q$. A simple supplied branch construction uses
$(q_j,r_j,0,\ldots,0)$ with $q_j^2+r_j^2=1$; with a separate $q_j\ne1$
guard, the direct-sum construction realizes $A_q$ exactly. Rational
unit-circle witnesses and approximation quality are distinct prerequisites.

## S09. Primitive oracle contracts are conditional, not realizations

The one-signal primitive diagonal route declares a matrix of dimension
$2^{n+1}$, an unspecified unitarity predicate on such matrices, and an
unspecified extraction predicate relating it to an $N\times N$ block. The
semantic assumption is the **conjunction** of that unitarity proposition and
existence of an extracted block equal entrywise to $D$. From this assumption
one may obtain the unitarity field and a block-target equality, then package a
verified-candidate record whose propositions are precisely these supplied
ones. No unconditional witness of that assumption is given here. The opaque
predicate named unitarity is not definitionally the rational orthogonality
predicate used in the Householder route.

Its layout is one signal and no pure workspace; the circuit is one oracle
label, whose resource tuple is $(1,1,1,1)$. Candidate target, matrix, layout,
transcript and resource are separate record fields. The fact that the layout
has the expected number of auxiliaries does not prove that the transcript
denotes the matrix. The generic verified-candidate packaging requires proof
of the chosen propositions, not a hidden theorem about every such record.
No claim that a standard rational two-dimensional rotation realizes every
cubic amplitude follows from this conditional package.

## S10. Scalar rotation interface and transparent computation

A supplied scalar-tier interface consists of a scalar carrier, a map from
rational amplitudes, an angle-producing function, a clean-entry function and
the law
\[
 0\leq a\leq1\ \Longrightarrow\ C(\Theta(\iota(a)))=\iota(a).
\]
Descriptive strings suggest $\Theta(a)=2\arccos a$ and
$C(\theta)=\cos(\theta/2)$. The interface does not enforce these formulas,
injectivity of the amplitude map, or actual trigonometric/matrix semantics.
The range theorem in S02 specializes its law to every cubic grid amplitude.
Universal quantification over every such tier is a transparent scalar
bookkeeping statement, not existence of a physical rotation backend. The
workspace-size parameter is unused in this angle statement.

A value-computation backend has an arbitrary workspace carrier $W$, a
declared qubit count, a zero workspace, an amplitude-reading function
$a:W\to\mathbb Q$, and a function $F:J\times W\to J\times W$. Its clean
input contract says the declared count equals the parameter and
\[
 F(j,0_W)=(j,w_j),\qquad a(w_j)=a_j.
\]
This does not constrain dirty-input behavior, invertibility, or the cardinality
of $W$. A symbolic instance takes $W=\mathbb Q$, reads the identity, and
overwrites any workspace with the exact cubic amplitude; its declared finite
qubit count does not make the rational carrier a finite register.

The finite fixed-denominator instance instead takes
$W=\{0,\ldots,M-1\}$, $M=2^{3n}=N^3$, zero payload zero, reads $w/M$, and
overwrites the payload with $j^3$. Since $j^3<M$ and
$j^3/M=(j/N)^3$, it meets the clean-input computation contract with a
$3n$-bit carrier. Existence of such a backend yields the transparent
computation proposition; the overwrite function itself is not reversible.

An opaque route-level arithmetic proposition is separately declared. A
backend bridge is the implication from its clean-input computation contract
to that opaque proposition. Once the computation premise is known, this
bridge is logically equivalent to the opaque proposition itself: apply the
bridge in one direction and use a constant implication in the other. The
same applies to the symbolic and finite fixed-denominator instances. These
equivalences identify an unresolved semantic obligation; they do not solve it.
The corresponding opaque controlled-angle proposition and its bridge from a
known scalar-tier law have the same logical normal form.

## S11. Modular reversible lifts and the readonly-rotation boundary

An honest reversible lift replaces overwrite by modular addition. Fix a
payload $p<M$ and workspace $w<M$, and define
\[
 T_p(w)=(w+p)\bmod M,\qquad
 S_p(w)=(w+M-p)\bmod M.
\]
Then $S_p(T_p(w))=w$. If $w+p<M$, reduce the inner modulo and cancel $p$;
otherwise $M\leq w+p<2M$, so the inner remainder is $w+p-M$, and adding
$M-p$ recovers $w$. All subtractions are natural subtractions, with the
displayed range inequalities ensuring the cancellations are legitimate.

For the cubic lift use $p=j^3$ and $M=2^{3n}$; for the linear-value lift
use $p=j$ and $M=N$. Both keep $j$ unchanged for all dirty workspace
inputs. On zero workspace their compute step matches the overwrite backend,
and compute followed by the stated uncompute restores every workspace value.
This supplies transparent cleanup witnesses for both the cubic and linear
value-computation interfaces. At $n=0$, $M=1,p=0,w=0$, so the same statements
remain valid. No multiplication circuit, adder gate sequence, depth bound,
or cost of forming $p$ is certified by the modular formulas.

A generic cleanup witness contains a backend and its clean-input computation
proof, separate compute/uncompute functions, agreement with the backend only
on the clean input, preservation of the system index for both functions, and
the law uncompute-after-compute for every workspace. Although a comment may
call this two-sided cleanup, the actual requested law is only this direction;
the reverse composite is not a field. The fixed finite modular maps have
the displayed cancellation property; no unlisted inverse law is silently
added to every generic witness.

A separate readonly-rotation witness contains a backend, the transparent
angle convention, and a function on $(j,w,\sigma)$, where $\sigma\in\{0,1\}$,
that preserves $j,w$. It does not prescribe the output signal, amplitudes,
unitarity or a linear action on superpositions. In particular a basis-state
function on a two-element signal carrier is not by itself a nontrivial
$R_y$ matrix. The readonly condition would be needed to compose cleanup
around an actual signal rotation, but the interface alone does not do so.

## S12. Remaining expanded conjunction and precise open source gaps

An expanded diagonal route uses one signal qubit and a parameterized number
of pure workspace qubits. Its proposed clean-block contract requires all five:

1. existence of a clean-input cubic computation backend;
2. the transparent scalar-angle statement for every supplied scalar tier;
3. an **opaque route-level clean-uncompute proposition**;
4. an **opaque extraction relation** for the chosen block;
5. the literal diagonal target equality for that block.

The first two have the witnesses described above at workspace size $3n$.
The transparent modular-cleanup witness in S11 is not automatically the third
opaque proposition. The readonly interface is not a conjunct of this contract.
The fifth item already contains the desired target entries; extracting it or
repackaging an existential block does not independently prove a circuit.
There is no unitarity field in this expanded conjunction. It is therefore a
conditional interface, not an expanded block-encoding acceptance theorem.

The construction graph has the following guarded routes. S01 AND S02 give
safe scales and target arithmetic. S02 AND an interpreted coherent counting
transcript AND complete rejection/cleanup AND Hadamard phase analysis could
give the rank-one clean block; the latter three are OPEN. S04 AND S05 AND
S06 give exact rational orthogonal **matrix existence** for each diagonal
target. This is an alternative to a gate-expanded arithmetic route, not a
shortcut that closes its cost. S06 AND the clean-matrix product arithmetic in
S07 give a cubic clean-matrix equality, not the physical product circuit. A
QSVT supplier is an alternative external route, retaining its full AND tail.
S08 transports supplied diagonal entry errors to rational Euclidean action
errors. S10 AND S11 provide value/cleanup subinterfaces, while a real rotation
semantics, common-backend composition, opaque-cleanup bridge, extraction,
unitarity and resource refinement remain OPEN for S12.

The explicit stronger-consumer gaps are: normalized state preparation and
success/amplification; rank-one transcript denotation; efficient deterministic
four-square data production and storage; uniform controlled-matrix/gate
synthesis with bit precision; physical composition of product clean blocks;
QSVT global phase/semantic/resource supply; approximation producer and scalar
extension; coherent arithmetic/rotation/cleanup composition; and executable
family acceptance. No finite diagnostic, output-size bound, exact-rational
operation count, oracle label, or existence witness is a substitute for them.

## S13. Accounting and process metadata are not mathematical closure

The local resource vocabulary counts one-qubit, CNOT and unexpanded oracle
calls separately; its score's gate field is their sum. Sequential composition
adds depths. Thus a label can have zero local elementary cost but still add
one oracle call and one scored gate. The auxiliary score comes from signal
plus pure layout qubits, not from a proof that those qubits suffice physically.
Symbolic polynomial or rotation-synthesis cost expressions are descriptive
syntax, not asymptotic inequalities with certified constants.

The historical policy data sets the exact-iteration limit to two, exact-stall
window to one, target auxiliary floor to four with zero gate/depth/query
fields, and maximum agent counts to four/five/eight. A separate four-level
schedule is $[1,2,3,4]$ for the upper and middle coordination slots and
$[3,4,5,6]$ for lower work; its per-level budgets are $[1,1,1,1]$, with
stall windows one. The encoded exploratory error ladder is
$[10^{-10},10^{-8},10^{-6}]$, beginning with the requested tolerance. Its
relaxed entries do not satisfy the original tolerance automatically. A
planning phase label starts relaxed approximate search; it is not a theorem
that exact synthesis is impossible or that the controller actually ran.

These process records, task strings, construction-claim descriptions and
constant-value checks are retained for whole-source completeness, but excluded
from mathematical success claims. They cannot replace any guarded dependency
or authorize changing the target, verifier, score, or historical evidence.
