# Finite state action, exact primitive circuits, and reversible address logic

## 1. Carriers and interpretation

For a natural number \(d\), write \([d]=\{0,\ldots,d-1\}\). A finite \(r\times c\) matrix over a scalar carrier \(A\) is a function \([r]\times[c]\to A\); a column vector is a function \([d]\to A\). Matrix rows are output coordinates and columns are input coordinates. A register with \(n\) qubits has dimension \(2^n\), including dimension one when \(n=0\).

When scalar addition and multiplication support finite sums, matrix action is
\[
(Uv)_i=\sum_{j\in[c]}U_{ij}v_j.
\]
For complex matrices, \(U^\dagger\) means conjugate transpose, not entrywise conjugation. A square complex matrix is unitary when its adjoint is its two-sided inverse. No arbitrary supplied matrix is declared unitary merely by assigning it a description.

A separate symbolic coefficient convention, when used in the surrounding matrix language, consists of rational constants, named symbols, sums, products and negatives. An environment assigns a rational number to every symbol. Interpretation replaces constants and symbols by these values and recursively performs rational addition, multiplication and negation. Such an arbitrary environment supplies neither trigonometric identities nor a unitarity certificate. Symbolic matrix products are finite ordered folds before interpretation; a symbolic expression containing zero summands need not be syntactically identical to its simplified value. The results below concerning complex unitarity do not follow from this symbolic interpretation alone.

The finite constructions are literal formulas on their stated carriers, not selections of representatives modulo phase. They impose no blanket positive-dimension assumption. If \(d=0\), vectors have empty domain, matrices with an empty coordinate axis have no entries on that axis, and sums over that axis are zero. Naming a basis index in \([d]\) itself requires an index to exist.

## 2. Basis action and state-preparation evidence

With distinguished scalar values \(0,1\), the basis column at \(j\in[d]\) is
\[
(e_j)_i=\begin{cases}1&i=j,\\0&i\ne j.\end{cases}
\]
The all-zero register column is \(e_0\in A^{[2^n]}\). This is defined even for zero qubits: it is the one-coordinate column with value \(1\).

For a scalar semiring, including the nonassociative version when only the corresponding finite-sum identities are used,
\[
Ue_j=U_{\bullet j},\qquad Ue_0=U_{\bullet0}.
\]
Indeed, the only possibly nonzero summand in row \(i\) is \(U_{ij}1\). For any complex \(r\times c\) matrix, complex scalars \(a,b\), and indices \(j,k\in[c]\), without requiring \(j\ne k\),
\[
U(ae_j+be_k)=aU_{\bullet j}+bU_{\bullet k},
\qquad
\bigl[U(ae_j+be_k)\bigr]_i=aU_{ij}+bU_{ik}.
\]
This follows by distributing the finite sum and factoring each scalar.

A state target consists of an amplitude vector \(v\in A^{[2^n]}\), a specified proposition \(N\) called its normalization condition, and optional source text. The word “normalization” here does not prescribe a norm formula: \(N\) is supplied as part of the target. The first-column contract is
\[
\forall i\in[2^n],\quad U_{i0}=v_i.
\]
By the preceding basis identity, this is equivalent to the vector equation \(Ue_0=v\).

A concrete complex state-preparation certificate consists of a target \((v,N)\), a complex \(2^n\times2^n\) matrix \(U\), proofs of standard matrix unitarity and \(N\), and a proof of \(Ue_0=v\). It supplies exactly this state action. The certificate can be packaged with a presentation circuit, a layer schedule, a resource record, and an auxiliary-qubit count (default zero) into a generic candidate or verified state-preparation record. The candidate's unitarity proposition is then the standard unitarity predicate of \(U\), and the verified record obtains the first-column equation from \(Ue_0=v\).

These extra presentation and resource fields are supplied data. This packaging does not prove that the supplied circuit denotes \(U\), that its schedule is correct, that the auxiliary count describes a physical implementation, or that its resource record measures that implementation. It also does not replace \(N\) by the usual squared-norm-one equation. Reading the preparation equation back from a certificate simply returns its stored proof.

## 3. Signal–system indexing and the clean branch

Let \(s,r,c\) be arbitrary natural dimensions. In a product-register view, row indices belong to \([s]\times[r]\) and column indices to \([s]\times[c]\). The signal coordinate is high-order; the system coordinate is low-order. The row and column flattenings are respectively
\[
f_r(a,i)=ar+i,\qquad f_c(b,j)=bc+j.
\]
For their indicated indices, \(f_r(a,i)<sr\) and \(f_c(b,j)<sc\). Thus any flat \(sr\times sc\) matrix \(M\) has the product view
\[
\widetilde M_{(a,i),(b,j)}=M_{ar+i,bc+j}.
\]
For a selected signal value \(a\in[s]\), projection means the same signal value at input and output:
\[
(P_aM)_{ij}=\widetilde M_{(a,i),(a,j)}=M_{ar+i,ac+j}.
\]
Hence projection after changing to the product view agrees entry for entry with flat block extraction. The product embedding into a square signal–system space is precisely \((a,i)\mapsto ad+i\); its numerical value agrees with the flattening above. In particular, the rational-matrix clean block defined by restriction along this embedding is the same pointwise matrix as this signal block projection. No register swap is implicit in these identifications.

Now let \(U\) be a square \(sd\times sd\) matrix over a semiring. The amplitude obtained by inputting the clean basis state at \((a,j)\) and reading the clean output at \((a,i)\) is
\[
C_a(U;i,j):=\bigl[Ue_{ad+j}\bigr]_{ad+i}=U_{ad+i,ad+j}=(P_aU)_{ij}.
\]
The middle equality is the basis-column identity. Consequently, for every target \(d\times d\) matrix \(T\),
\[
P_aU=T\ \text{pointwise}
\quad\Longleftrightarrow\quad
\forall i,j\in[d],\ C_a(U;i,j)=T_{ij}.
\]
Both directions substitute the same entry identity; they do not assume unitarity or a normalized failure branch. This is an exact clean-block/action bridge, not a theorem fixing any normalizer or success probability. Other signal outputs, their normalization, ancilla cleanup and physical realization require additional evidence. If \(s=0\), no selected signal index exists; if \(d=0\), the universally indexed clean-action statements are vacuous. The rectangular product-view formulas also allow \(r=0\) or \(c=0\).

## 4. One-qubit rotations and exact angle interpretation

All angles in this section are exact real numbers. An angle expression may denote a rational, a rational multiple of \(\pi\), twice the arccosine of a rational in \([-1,1]\), twice the arccosine of the square root of a rational in \([0,1]\), or an arbitrary given real. Sums, negatives and rational scaling are interpreted by the corresponding real operations. The domain evidence on the two arccosine expression constructors is part of their syntax; arbitrary real expressions do not promise a computable decimal export.

In the ordered basis \(0,1\), set
\[
R(t)=\begin{pmatrix}\cos t&-\sin t\\\sin t&\cos t\end{pmatrix},
\qquad
Y(\theta)=R(\theta/2),
\qquad
X=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]
Thus the physical \(Y\)-rotation uses a half angle and has a negative upper-right entry. The exact identities, for all real \(\alpha,\beta,\theta\), are
\[
Y(0)=I,\qquad Y(\alpha+\beta)=Y(\beta)Y(\alpha),\qquad
Y(-\theta)=Y(\theta)^\dagger,\qquad
XY(\theta)X=Y(-\theta).
\]
The addition identity is obtained by the sine and cosine addition formulas with \((\alpha+\beta)/2=\alpha/2+\beta/2\); negation uses the evenness of cosine and oddness of sine. Multiplying by \(X\) exchanges rows or columns and gives the last identity directly. Since \(\cos^2t+\sin^2t=1\), every \(Y(\theta)\) is unitary.

Complex conjugation fixes \(\cos t\) and \(\sin t\) when \(t\) is real, whether the real argument is first embedded in the complex field or the real result is embedded afterward. In particular,
\[
\overline{\cos(t+0i)}=\cos(t+0i),\quad
\overline{\sin(t+0i)}=\sin(t+0i),\quad
\frac{t+0i}{2}=(t/2)+0i.
\]
The same conjugation identities therefore hold when the complex argument is written as \((t+0i)/2\). These are scalar conjugation identities; the dagger on a matrix also transposes it.

Define the coefficient-loading rotation \(A(c)=R(\arccos c)\). Under the stated coefficient interval \(-1\le c\le1\),
\[
Y(2\arccos c)=A(c).
\]
The displayed matrix equality is just cancellation of the factor two in the angle; its algebra does not use the interval bounds. Those bounds are the intended coefficient domain, and identify the top-left entry with \(c\). They are not a new assumption on arbitrary primitive rotations. The uniform one-bit preparation matrix is
\[
W=\begin{pmatrix}\sqrt2/2&-\sqrt2/2\\\sqrt2/2&\sqrt2/2\end{pmatrix}
=Y(\pi/2).
\]
This fixes the whole matrix, not just its first column; \(W\) is not the usual Hadamard matrix.

The other primitive rotation is
\[
Z(\theta)=\begin{pmatrix}
\cos(\theta/2)-i\sin(\theta/2)&0\\
0&\cos(\theta/2)+i\sin(\theta/2)
\end{pmatrix}.
\]
Each diagonal value has modulus one, by the same trigonometric identity. Hence \(Z(\theta)\) is unitary, and \(Z(-\theta)=Z(\theta)^\dagger\). Both signs and both half angles are part of the exact convention, with no phase quotient.

## 5. Named wires and full-register primitive matrices

For \(n\ge0\), a computational basis assignment is a function \(b:[n]\to[2]\). This description names wires; it does not choose an integer endian flattening of these assignments. For a bit \(q\), define its flip as \(1\) if \(q=0\), and \(0\) otherwise. Flipping twice returns \(q\).

For a target wire \(t\in[n]\), let \(x_t(b)\) change only \(b(t)\) to its flip. Then \(x_t\) is an involution and hence a basis equivalence with itself as inverse. For control and target \(c,t\in[n]\), define
\[
\operatorname{cx}_{c,t}(b)=
\begin{cases}b&b(c)=0,\\x_t(b)&b(c)\ne0.\end{cases}
\]
The action formula itself allows coincident wires, but its involution and equivalence claims require \(c\ne t\). Under this condition, the target flip leaves the control bit unchanged; applying the same conditional action twice therefore returns \(b\). The resulting equivalence evaluates by this formula and is its own inverse.

To lift a one-qubit matrix \(G\) onto wire \(t\), split the basis assignment into its target bit and its restriction to the remaining wires:
\[
S_t(b)=\bigl(b(t),b|_{[n]\setminus\{t\}}\bigr).
\]
This is a bijection: reconstruction uses the first component at \(t\) and the second component elsewhere. Its other-wire component at a wire \(w\ne t\) is exactly \(b(w)\). Transport \(G\otimes I\) back along this bijection. In entries, the resulting matrix \(L_t(G)\) is
\[
L_t(G)_{b',b}=\begin{cases}
G_{b'(t),b(t)}&b'|_{[n]\setminus\{t\}}=b|_{[n]\setminus\{t\}},\\
0&\text{otherwise}.
\end{cases}
\]
Thus every other wire is fixed. If \(G\) is unitary, so is \(L_t(G)\): the tensor factor \(I\) is unitary, tensor products preserve unitarity, and simultaneous reindexing of rows and columns by a bijection preserves it. This is explicitly conditional on the supplied \(G\)'s unitarity, not a certificate for an arbitrary \(G\). Also
\[
L_t(G)^\dagger=L_t(G^\dagger),
\]
as follows by transposing the entry formula and conjugating its sole nonzero factor.

For any equivalence \(\sigma\) of a finite basis set, write its permutation matrix as
\[
(Q_\sigma)_{b',b}=\begin{cases}1&b'=\sigma(b),\\0&\text{otherwise}.\end{cases}
\]
It sends input basis vector \(e_b\) to \(e_{\sigma(b)}\), is unitary, and satisfies \(Q_\sigma^\dagger=Q_{\sigma^{-1}}\). The latter identity is the equivalence of \(b=\sigma(b')\) and \(b'=\sigma^{-1}(b)\), after conjugating zero or one.

There are exactly four primitive instruction forms: target-bit flip, target \(Y\)-rotation with an exact angle expression, target \(Z\)-rotation with an exact angle expression, and controlled bit flip with distinct control and target. Their full-register matrices are respectively
\[
Q_{x_t},\quad L_t(Y(\theta)),\quad L_t(Z(\theta)),\quad Q_{\operatorname{cx}_{c,t}},
\]
where \(\theta\) is the angle expression's real interpretation. Every such matrix is unitary. Instruction adjoint keeps the two bit-flip forms and negates each rotation expression. Its denotation is exactly the matrix dagger, by involutivity for the permutations and the negation and lifting identities for rotations.

## 6. Chronological circuits, global phase, and exact refinement

A primitive circuit is a finite instruction list in execution order. Its matrix \(E\) is defined by
\[
E([])=I,\qquad E(g::C)=E(C)E(g).
\]
Later instructions multiply on the left. Induction on the list proves unitarity and the concatenation rule
\[
E(C\mathbin{+\!+}D)=E(D)E(C).
\]
The induction step reassociates matrix products; the empty case uses identity. Reversing the instruction list and replacing each instruction by its adjoint gives
\[
E(C^\dagger)=E(C)^\dagger,
\]
by the instruction adjoint law and reversal of the product order under dagger.

For an exact angle expression of real value \(\phi\), define the global phase \(p(\phi)=\exp(i\phi)\). It has unit modulus: its conjugate is \(\exp(-i\phi)\), and the product in either order is \(\exp(0)=1\). In particular, \(p(-\phi)=\overline{p(\phi)}\).

A program consists of a circuit \(C\) and its declared global-phase angle \(\phi\); its matrix is
\[
F(C,\phi)=p(\phi)E(C).
\]
The identity program has empty circuit and zero phase, hence denotes \(I\). Sequential composition executes the first circuit and then the second, and adds their phases. Since \(\exp(i(\phi+\psi))=\exp(i\phi)\exp(i\psi)\), scalar commutativity and the concatenation law give
\[
F(P;Q)=F(Q)F(P).
\]
Every program is unitary, since it is a unitary matrix scaled by a unit-modulus scalar. Its adjoint program reverses and adjoints the instructions and negates the phase; thus
\[
F(P^\dagger)=F(P)^\dagger.
\]
No declared global phase is discarded in these equalities. A circuit refinement consists of a circuit \(C\), a target matrix \(T\) on the same basis assignments, and evidence of \(E(C)=T\). This is literal equality, not equality up to phase. A circuit refinement does not automatically supply a refinement for an arbitrarily phased program.

When \(n=0\), there is exactly one empty basis assignment and no target wire. Consequently no primitive instruction can be formed; the empty circuit denotes the one-dimensional identity. A zero-wire program may still carry a global phase and denotes that scalar times the one-dimensional identity. For \(n=1\), the remaining-wire assignment set in a one-wire lift has one element, so the identity tensor factor has dimension one. Distinct-wire requirements prevent controlled flips on fewer than two wires.

## 7. Reversible classical proof instructions

A separate reversible classical intermediate language contains bit flips, distinct-wire controlled flips, and a doubly controlled flip with three pairwise distinct wire operands. It is a proof language for classical address and indicator logic, not an extension of the final four-form primitive instruction language.

For control wires \(c_0,c_1\) and target \(t\), define the basis action
\[
\operatorname{ccx}_{c_0,c_1;t}(b)=
\begin{cases}x_t(b)&b(c_0)=1\ \text{and}\ b(c_1)=1,\\
b&\text{otherwise}.\end{cases}
\]
The action formula imposes no distinctness condition by itself. If \(c_0\ne t\) and \(c_1\ne t\), then it is an involution: the active case flips the target while preserving both controls, so it remains active for the second application and the two flips cancel; in the inactive case the assignment never changes. This proof and the corresponding basis equivalence do not require \(c_0\ne c_1\). The instruction constructor nevertheless requires all three pairwise inequalities. Its semantic equivalence ignores only the redundant control–control distinction proof, not either control–target distinction.

Each reversible instruction denotes the appropriate basis equivalence: the single- and double-wire forms use the actions of Section 5, and the triple-wire form uses the preceding action. An empty reversible program denotes the identity equivalence. A nonempty program applies its head instruction and then its tail program. Thus for a chronological list \([h_1,\ldots,h_m]\), its action is
\[
b\longmapsto h_m(\cdots h_2(h_1(b))\cdots).
\]
This specifies classical basis execution, with reversibility supplied by composition of equivalences. It is not a theorem compiling the doubly controlled operation into the primitive four-form language. Three pairwise distinct operands cannot exist on fewer than three wires; on zero wires the empty program is the only program.

## 8. Scope of the mathematical evidence

All equalities above are exact finite-dimensional statements. No approximation norm, finite-bit angle precision, synthesis error, measurement protocol, postselection probability, or amplification bound is introduced. The semantics preserve exact global and relative phases; they do not establish ancilla cleanup for an unspecified implementation. The reusable matrix lift assumes unitarity of its input matrix, whereas the four specified primitive instructions and their circuits and programs derive unitarity from their explicit semantics.

These statements give no runtime for evaluating real expressions, no Clifford+T compilation cost, connectivity or hardware-depth bound, and no preprocessing, oracle-construction or readout cost. Supplied state-preparation resource metadata is not a cost theorem. The reversible proof language likewise supplies no charged cost for its doubly controlled flip and no final-instruction synthesis certificate. Such costs and compilation bridges remain separate requirements.
