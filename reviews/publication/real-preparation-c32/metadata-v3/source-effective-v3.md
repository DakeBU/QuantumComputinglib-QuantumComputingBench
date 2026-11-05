# Exact real amplitude trees and local isometry completion

This is an implementation-informed retrospective mathematical reconstruction. The historical formalizer is UNKNOWN. It is not a historical pre-proof source, an independent account of an external paper, or a claim about a polynomial-time Hermite preparation algorithm. All matrices below have output rows and input columns. Every equality is exact, including its phase.

## A. Registers, lifting, and chronological action

### A1. Named bits and the highest-bit split

Let \(B_n=\{0,1\}^{\{0,\ldots,n-1\}}\), including the singleton empty word at \(n=0\). The all-zero word is \(0_n\). There is a bijection
\[
 B_{n+1}\longleftrightarrow B_n\times\{0,1\},\qquad
 z\longmapsto(z_{<n},z_n),
\]
whose inverse appends the bit. Two words are equal precisely when their restrictions to the first \(n\) wires and their highest bits agree. This convention keeps every old wire number unchanged when a highest wire is added.

For an \(n\)-wire matrix \(M\), define its extension \(L(M)\) by
\[
 L(M)_{(b,v),(a,w)}=\delta_{v,w}M_{b,a}.
\]
It is the tensor product with the identity on the highest bit, expressed in named-wire coordinates. Consequently \(L(I)=I\) and \(L(MN)=L(M)L(N)\): in the latter identity the sum over the intermediate highest bit collapses to \(v=w\), leaving the ordinary matrix product on the low wires.

### A2. Instruction lifting

An instruction on an old wire is lifted to the same numbered wire. This applies to bit flip, real y-rotation, z-rotation, and a controlled bit flip with distinct control and target. If an old target wire is removed from a word, equality of the remaining contexts on \(n+1\) wires means both equality of the old \(n\)-wire contexts and equality of the newly added highest bits. To prove the converse, examine a remaining wire: it is either the highest wire or an old remaining wire. This gives the two cases directly.

For a real angle \(\theta\), the z-rotation named here has the literal matrix
\[
 R_z(\theta)=\operatorname{diag}\!\left(
 \cos(\theta/2)-i\sin(\theta/2),\;
 \cos(\theta/2)+i\sin(\theta/2)\right).
\]
Off-diagonal entries are zero. This is equality of complex matrix entries, not equality up to a global phase; in particular it is not silently replaced by \(\operatorname{diag}(1,e^{i\theta})\). The instruction lift retains this same angle and matrix on the old target wire. The arbitrary one-qubit matrix lifting argument below therefore applies to this matrix as well. This convention adds no z-rotation to the later real RY/CX preparation tree.

The low-wire restriction of a lifted bit flip is the old bit flip. Its highest bit is untouched. The same is true of a lifted controlled flip, separately in the control-zero and control-one cases. For a lifted one-qubit matrix, the context criterion above gives exactly \(L(M)\). Thus the matrix of every lifted instruction is the lift of its old matrix.

An instruction list is executed chronologically: if the first matrix is \(G\) and the remaining-list matrix is \(R\), its matrix is \(RG\). Concatenating first \(c\), then \(d\), gives \(U_dU_c\). Induction using multiplicativity of \(L\) therefore proves that lifting every instruction lifts the matrix of the entire list. Lifting changes neither the number of y-rotations nor the number of controlled flips; check each of the four instruction kinds and add over the list.

## B. Splitting a real pair, including zero and negative entries

### B1. The pair radius

For arbitrary real \(a,b\), set
\[
 r(a,b)=\sqrt{a^2+b^2}.
\]
It is nonnegative and its square is \(a^2+b^2\). If \(r=0\), both entries are zero. Otherwise \(r>0\), and \(-r\le a\le r\), so \(-1\le a/r\le1\).

### B2. The signed split angle

Use the physical rotation convention
\[
 R_y(\theta)=
 \begin{pmatrix}\cos(\theta/2)&-\sin(\theta/2)\\
 \sin(\theta/2)&\cos(\theta/2)\end{pmatrix}.
\]
Define the angle by
\[
 \theta(a,b)=
 \begin{cases}
 0,&r(a,b)=0,\\
 -2\arccos(a/r(a,b)),&r(a,b)>0\text{ and }b<0,\\
 2\arccos(a/r(a,b)),&r(a,b)>0\text{ and }b\ge0.
 \end{cases}
\]
Then, for either output bit \(v\),
\[
 R_y(\theta(a,b))_{v,0}\,r(a,b)
 =\begin{cases}a,&v=0,\\b,&v=1.\end{cases}                 \tag{B2}
\]
When \(r=0\), both sides vanish. In the other case put \(\alpha=\arccos(a/r)\). The cosine identity gives \(r\cos\alpha=a\). Since \(\alpha\in[0,\pi]\), the number \(s=r\sin\alpha\) is nonnegative. Multiplying \(\sin^2\alpha+\cos^2\alpha=1\) by \(r^2\) gives \(s^2=b^2\). Hence \(s=b\) when \(b\ge0\), and \(-s=b\) when \(b<0\). Cosine is even and sine is odd, proving both rows of (B2). No unverified two-argument numerical arctangent is needed.

This pair identity allows signed entries. The preparation statement in Section D has a separate nonnegativity premise; the pair lemma alone must not be advertised as that stronger preparation theorem.

## C. Marginals, controlled rotations, and the recursive tree

### C1. Marginal table and squared norm

For \(f:B_{n+1}\to\mathbb R\), let
\[
 m_f(b)=r(f(b,0),f(b,1)),\qquad
 S(f)=\sum_{z\in B_n}f(z)^2
\]
when \(f\) is an \(n\)-wire table. Every marginal entry and every squared norm is nonnegative. The highest-bit bijection and the radius-square identity give
\[
 S(m_f)=\sum_{b\in B_n}\bigl(f(b,0)^2+f(b,1)^2\bigr)=S(f).       \tag{C1}
\]
The same bijection is used in the proof, not an implicit reshuffling of tensor factors.

### C2. A controlled rotation on the highest wire

Given an angle table \(\vartheta:B_n\to\mathbb R\), define the block matrix
\[
 D(\vartheta)_{(b,v),(a,w)}=\delta_{b,a}R_y(\vartheta(b))_{v,w}.
\]
Removing the highest wire leaves exactly the low-wire word. Therefore the context-preserving controlled-rotation specification is this block matrix. For any \(M\), matrix multiplication gives
\[
 [D(\vartheta)L(M)]_{(b,v),(0_n,0)}
   =R_y(\vartheta(b))_{v,0}M_{b,0_n}.                         \tag{C2}
\]
Indeed the low intermediate word must equal \(b\) and the intermediate highest bit must be zero. All other summands vanish.

The reused reference multiplexor implements \(D(\vartheta)\) with \(n\) controls using \(2^n\) y-rotations and \(2(2^n-1)\) controlled flips. Its elementary recurrence splits the control-angle table into half-sum and half-difference tables: apply the half-sum multiplexor, flip the target conditioned on the head control, apply the half-difference multiplexor, and repeat that controlled flip. In the head-zero block rotations add; in the head-one block conjugation by a bit flip negates the half-difference. These give exactly the two original angles. The chronological matrix order is the reverse of this written instruction order. Counts follow by doubling the smaller multiplexor and adding two controlled flips. No extra workspace wires are introduced.

### C3. Recursive preparation

For a table on zero wires take the empty instruction list. For a table \(f\) on \(n+1\) wires, first prepare the marginal \(m_f\) on the low \(n\) wires, with the highest wire untouched in zero. Then apply the controlled highest-wire rotation with angle table
\[
 b\longmapsto\theta(f(b,0),f(b,1)).                           \tag{C3}
\]
This describes one specific unoptimized binary-tree instruction list. It uses only y-rotations and controlled flips, even though the lifting operation was defined for the larger four-instruction language. Every individual instruction is unitary, and products are unitary; the preparation matrix is unitary for every real input table, without positivity or nonzero-norm assumptions.

## D. Exact state action, normalization, and scope

### D1. First-column theorem

Let \(f:B_n\to\mathbb R\) satisfy
\[
 f(b)\ge0\quad\text{for all }b,\qquad S(f)>0.
\]
The specific tree matrix \(P_f\) then satisfies
\[
 (P_f)_{b,0_n}=\frac{f(b)}{\sqrt{S(f)}}\quad(b\in B_n).        \tag{D1}
\]
The real number on the right is embedded in the complex scalars of circuit matrices, with no phase quotient.

Proof is by the number of wires. At zero wires there is one word. Nonnegativity and positive squared norm force its amplitude to be strictly positive. Thus \(\sqrt{f^2}=f\), the normalized amplitude is one, and the empty list has the required one-by-one identity matrix. For the induction step, \(m_f\) is nonnegative and has the same positive squared norm by (C1), so the induction hypothesis applies to it. Equation (C2) expresses the new first column as
\[
 R_y(\theta(f(b,0),f(b,1)))_{v,0}
 \frac{m_f(b)}{\sqrt{S(f)}}.
\]
Equation (B2) reduces this expression to \(f(b,v)/\sqrt{S(f)}\). Appending the low restriction and the highest bit recovers the original word, so all entries have the promised order.

The table that is identically zero is outside (D1): it has no normalized target state. For it, the construction is still a unitary instruction list, but that does not make zero a unit vector. At zero wires the singleton table \(f=-1\) would request the scalar \(-1\), whereas this construction returns the identity scalar \(+1\); consequently dropping nonnegativity from the all-width statement would be false. Equality up to global phase would be a different contract. No such relaxation is used here. For positive width a stronger signed-table result may be possible, but is not part of the statement recovered here.

### D2. Normalization

For every real table with \(S(f)>0\), regardless of signs,
\[
 \sum_b\left(\frac{f(b)}{\sqrt{S(f)}}\right)^2=1.              \tag{D2}
\]
Move the common squared denominator outside the finite sum. The denominator is \(S(f)\), by the nonnegative square-root identity, and positivity permits cancellation. If every table entry is strictly positive, then every squared entry is positive and the finite nonempty sum is positive. Strict positivity is a sufficient condition, not equivalent to nonzero norm.

### D3. Exact reference resources

Lifting preserves counts. If \(Y_n\) and \(X_n\) denote y-rotation and controlled-flip counts, the multiplexor recurrence gives
\[
 Y_0=X_0=0,\quad Y_{n+1}=Y_n+2^n,\quad
 X_{n+1}=X_n+2(2^n-1).
\]
Induction yields the exact counts
\[
 Y_n=2^n-1,\qquad X_n=2(2^n-1-n).                            \tag{D3}
\]
These include \(n=0\) and \(n=1\). There are no oracle instructions; the recorded oracle count is zero by the instruction-language resource definition. This does not give free access to the input table, free classical preprocessing, or an oracle that computes its entries. It is a count of the generated exact-real circuit, not a runtime bound. The construction is exponential in the number of wires and linear-scale in the size of an explicitly listed arbitrary amplitude table. It does not establish a polynomial-in-wire-count Hermite construction.

### D4. Flat little-endian coordinates

Define
\[
 \ell_n(b)=\sum_{j=0}^{n-1}2^j b_j\in\{0,\ldots,2^n-1\}.
\]
Its recursion is \(\ell_{n+1}(b)=b_0+2\ell_n(b_1,\ldots,b_n)\). It maps the all-zero word to index zero, and its inverse maps zero back to that word. Reindexing both matrix axes by \(\ell_n\) preserves unitarity. Reindexing a table preserves its sum of squares because this is a bijection.

For a strictly positive flat table \(g\), the reindexed preparation matrix \(Q_g\) therefore obeys
\[
 (Q_g)_{j,0}=g(j)/\sqrt{\sum_i g(i)^2},\qquad
 \sum_j(g(j)/\sqrt{\sum_i g(i)^2})^2=1.                       \tag{D4}
\]
The strict positivity premise here is stronger than the nonnegative positive-norm premise of (D1); do not erase this interface distinction. The proof transports (D1) and (D2), using strict positivity to obtain the norm premise.

## E. Prescribed columns: classical orthogonal existence

### E1. Arbitrary positions

Let \(V\in\mathbb R^{N\times r}\), let \(e:\{0,\ldots,r-1\}\hookrightarrow\{0,\ldots,N-1\}\) be injective, and assume \(V^TV=I_r\). There exists \(U\in\mathbb R^{N\times N}\) such that
\[
 U^TU=I_N,\qquad U_{i,e(a)}=V_{i,a}\quad\text{for all }i,a.   \tag{E1}
\]
Each column of \(V\) is a vector in Euclidean \(N\)-space. The matrix equation says their inner products are the Kronecker delta. Assign these vectors to the labels in the image of \(e\); injection makes the assignment unambiguous. Extend this orthonormal subfamily to an orthonormal basis indexed by all \(N\) physical labels. Taking these basis vectors as the columns gives (E1). A temporary zero value outside the specified image is only a way to present the restricted family to the extension theorem; it does not prescribe any output column or a unique completion. This is an application of finite-dimensional orthonormal-basis extension, not a new proof of that foundation.

Neither a prefix-position assumption nor \(r<N\) is needed for (E1). Empty dimensions are permitted. The injection and orthonormality already impose the compatible dimensional restrictions.

### E2. A one-column sign flip

For a chosen physical index \(j\), let \(F_j\) be diagonal with entry \(-1\) at \(j\) and \(+1\) elsewhere. Then \(F_j^TF_j=I\), because each diagonal entry squares to one, and \(\det F_j=-1\), because exactly one factor in the diagonal product is negative. Right multiplication flips column \(j\) and leaves every other column unchanged:
\[
 (UF_j)_{i,a}=U_{i,a}\quad(a\ne j).                          \tag{E2}
\]
The presence of \(j\) entails \(N>0\); this formula does not invent a column in the empty matrix.

### E3. Special-orthogonal existence and its spare-column boundary

Under the hypotheses of (E1), suppose additionally that a physical column \(j\) is unused: \(e(a)\ne j\) for every active label. A completion with determinant \(+1\) exists. Indeed, taking determinants of \(U^TU=I\) shows \((\det U)^2=1\), so \(\det U\) is \(+1\) or \(-1\). Keep \(U\) in the former case; replace it by \(UF_j\) in the latter. Orthogonality is preserved, determinants multiply to \(+1\), and (E2) preserves every prescribed column. Thus
\[
 U\in SO(N),\qquad U_{i,e(a)}=V_{i,a}.                       \tag{E3}
\]
The condition \(r<N\) supplies such an unused column: a surjection from \(r\) labels onto \(N\) labels would imply \(N\le r\), a contradiction. This produces the strict-dimension version of (E3).

The spare-column condition is substantive. If all columns are prescribed, an orientation-reversing orthogonal matrix cannot be changed without altering them; for example \(N=r=1\), identity placement, and \(V=(-1)\). Orthogonal completion exists but special-orthogonal completion preserving the data does not. The existence argument uses basis extension and choices, does not select a canonical completion, and provides neither an elimination trace nor a deterministic arithmetic cost bound.

## F. A distinct explicit real completion route

### F1. Supplied exact-real producer

For interpreting the local construction below, reuse a different, explicit finite producer. Given an isometry \(V\) with \(r<N\), sweep its columns from left to right. For column \(k\), eliminate entries bottom-up using adjacent row planes \((i,i+1)\), with angle \(-\theta(x,y)\) for the current pair. The pair calculation in Section B shows that this changes \((x,y)\) into \((r(x,y),0)\); a zero pair gives angle zero and the identity step.

Let \(T\) be the chronological product of these actual row rotations. Each plane is orthogonal and has determinant one, so \(T\in SO(N)\). The transformed table is \(TV\). Previously fixed columns remain standard basis columns because each later plane touches only positions where those columns are zero. Orthogonality with those earlier columns forces the new column's entries above its pivot to vanish. The sweep zeros all entries below it. Its remaining pivot has square one, and is nonnegative after at least one adjacent elimination, so the pivot is \(+1\). The strict inequality \(r<N\) guarantees at least one available elimination step even for the last active column. Consequently \(TV\) has the first \(r\) standard coordinate columns. Therefore \(T^T\) is an explicit determinant-one prefix completion: multiplying back gives each original column of \(V\).

To place these columns at an arbitrary injection \(e\), extend the prefix assignment deterministically by greedy swaps. Beginning with the identity permutation, at step \(k\) swap the current image of coordinate \(k\) with \(e(k)\). Injection ensures previous images are untouched. At the end a permutation \(p\) satisfies \(p(a)=e(a)\) for all active \(a\). The image \(p(r)\) is unused. Permute the completion's columns so original column \(a\) goes to physical column \(p(a)\). Its determinant changes by the sign of \(p\). If that sign is negative, flip only column \(p(r)\). The result is special orthogonal and preserves all prescribed columns. This orientation step uses finite permutation parity, not a determinant comparison of a chosen existential completion.

An explicitly supplied bijection from a named physical basis to numerical coordinates transports both matrix axes, the input columns, and the placement injection. It is not an unspecified enumeration. This exact-real producer is a reused dependency of the local route, not a theorem established by merely packaging its desired conclusion as an input.

### F2. What this does not settle

The formulas select definite real angles, rotations, and permutations. That is stronger than existence alone. It is not yet a stored finite-bit program with a certified evaluation cost. Exact square roots, inverse cosine, sign comparisons, arbitrary input-entry access, intermediate storage and copying all need a cost/precision model. The use of real-valued definitions is neither a proof of efficiency nor a proof of inefficiency. Replacing this producer by the existence route of Section E is an alternative mathematical route, not an interchangeable algorithm certificate.

## G. Local tensor-train columns at actual physical positions

### G1. Chain data and canonicality

A real core from left rank \(l\) to right rank \(m\) is a table \(A_{a,(v,b)}\), with \(a<l\), \(v\in\{0,1\}\), and \(b<m\). A length-\(n\) chain has dependent intervening ranks and explicit initial and terminal ranks. Its emitted-word contraction is the ordered product of its bit slices; the first core emits the first bit. A chain is right-canonical when every core satisfies \(AA^T=I\). This is actual local row orthonormality, not a Boolean flag or a hypothesis of already-correct whole-state action.

Let \(r_t\) be the rank before stage \(t\), remaining at the terminal rank after the end. Let \(M\) be the largest actual rank, including both boundaries. Then \(r_t\le M\) for every \(t\). Choose \(q\) with \(M\le B=2^q\). The padded core at an existing stage is
\[
 K_t((v,b),a)=
 \begin{cases}
 A^{(t)}_{a,(v,b)},&a<r_t,\ b<r_{t+1},\\
 0,&\text{otherwise},
 \end{cases}                                                \tag{G1}
\]
viewed as complex numbers with zero imaginary part. After the length of the chain its scheduled core is zero; no local active-isometry theorem is asserted for those later stages. Right-canonicality implies that the occupied columns \(a<r_t\) of \(K_t\) are orthonormal, for \(t<n\): restrict the padded finite sum to the actual next-rank labels and use \(AA^T=I\). Taking real parts recovers a real isometry, since every imaginary part is zero.

### G2. Explicit physical coordinates and clean-input positions

The local register has \(q\) low bond wires and one highest emitted-bit wire. For a bond word \(b\in B_q\) and highest bit \(v\), its coordinate pair is \((v,\ell_q(b))\). The explicit flattened coordinate is
\[
 c(b,v)=v\,2^q+\ell_q(b)\in\{0,\ldots,2\cdot2^q-1\}.        \tag{G2}
\]
For an active numerical bond label \(a<r\le2^q\), the prescribed physical input column is the named word \((\ell_q^{-1}(a),0)\). These columns are distinct: applying the coordinate map recovers \(a\). They are precisely active bond labels with a fresh highest bit in zero. This is a prefix in the specified numerical coordinates; an unspecified named-basis enumeration is not allowed to replace that assertion.

Let \(W\) be any real matrix with \(2\cdot2^q\) named rows and \(r\) active columns. Feed \(W\), these physical positions, and (G2) into the explicit completion route of Section F. This defines a particular full local matrix even when \(W\) is not an isometry. If \(W^TW=I_r\), the returned matrix \(U\) is orthogonal, has determinant one, and satisfies every prescribed entry exactly. The needed spare dimension follows from
\[
 r\le2^q<2\cdot2^q.
\]
At \(q=0\) the bond has one label and the local register has two states, so a spare column still exists. At \(r=0\) the prescribed-column requirement is vacuous, not a missing supplier of nonzero data.

### G3. Actual stage completion

For a chain and \(M\le2^q\), form the real occupied-column table
\[
 W_t(z,a)=\operatorname{Re}K_t\bigl((z_q,\ell_q(z_{<q})),a\bigr),
 \qquad a<r_t.                                             \tag{G3}
\]
Apply the preceding local completion to obtain \(U_t\). If the chain is right-canonical and \(t<n\), its occupied-column isometry supplies \(W_t^TW_t=I\). Thus
\[
 U_t^TU_t=I,\qquad\det U_t=1,
\]
and for every output bit \(v\) and bond words \(b,a\in B_q\),
\[
 \ell_q(a)<r_t\quad\Longrightarrow\quad
 U_t((b,v),(a,0))=K_t((v,\ell_q(b)),\ell_q(a)).               \tag{G4}
\]
The real matrix entry on the left is embedded into complex scalars. To prove (G4), regard \(\ell_q(a)\) as an active label. Its prescribed column is exactly \((a,0)\), by the explicit coordinate map. The completion theorem gives the corresponding entry of \(W_t\); (G3) and the zero imaginary part identify that entry with \(K_t\). These steps also explain why one must not replace occupied clean columns by an arbitrary prefix convention with a different endian order.

## H. Composition contracts and remaining suppliers

The local matrix \(U_t\) in (G4) uses named bond-first pairs \((b,v)\), whereas the sequential recurrence below uses bit-first numerical pairs. Put \(B=2^q\) and let \(\ell_q^{-1}:\operatorname{Fin}(B)\to B_q\) be the inverse little-endian coordinate bijection. Define the transported kernel by
\[
 \mathcal U_t((v,b),(w,a))
 =U_t((\ell_q^{-1}(b),v),(\ell_q^{-1}(a),w)),
 \quad a,b\in\operatorname{Fin}(B),\quad v,w\in\{0,1\}.       \tag{H0}
\]
The map \((v,b)\mapsto(\ell_q^{-1}(b),v)\) is a bijection onto the named words of width \(q+1\). Thus (H0) is simultaneous row/column coordinate transport of one matrix, not a physical SWAP instruction or an assertion of free wire routing. Bijection reindexing preserves matrix products and orthogonality; its permutation conjugation also preserves determinant. Substituting \(w=0\) in (H0), (G4) gives the exact occupied-column identity for numerical input \(a<r_t\) and every numerical output bond \(b<B\). No sign, phase, transposition or new mathematical premise is added.

If a sequence of full stages acts on a fresh zero bit at each step, then only their clean-input columns affect the evolving state. Previously emitted bits are passive. With bond boundary \(u\), expressed in these numerical bond coordinates, the single-step identity is
\[
 \psi_{t+1}(x,b)=\sum_{a<B}\mathcal U_t((x_t,b),(0,a))\psi_t(x_{<t},a).
\]
Here (H0) is a natural mathematical coordinate definition. Its agreement with any actual implementation adapter and the physical global placement remain separate audit obligations; this source clarification is not an implementation certificate.
If the boundary vanishes outside rank \(r_0\), the padded cores vanish outside each next rank, and every used stage matches the occupied clean columns as in (G4), induction gives exactly the contraction of the original cores, zero-padded in the final bond. For terminal rank one, every final bond label except zero has amplitude zero. This is a reused sequential-composition fact, not an extra premise of the local completion theorem and not newly proved whole-circuit synthesis here.

The local theorem supplies a specific matrix from supplied real chain data. It does not by itself supply a primitive gate list for that matrix, a global wire-placement theorem, an initial-boundary preparation circuit, a chain for any specific function, a deterministic canonicalization algorithm for an arbitrary chain, or finite-bit resource guarantees. Conditional assembly theorems that take local stages as premises remain consumers until actual suppliers discharge those premises. A supplied-stage certificate is not a supplier merely because its conclusion sounds like preparation.

## I. Dependency topology, alternatives, and finite-bit boundary

The recovered mathematical construction has the following complete conjunctive dependencies. The amplitude-state conclusion needs the table, its stated nonnegativity, positive squared norm, the pair-split identity, marginal norm preservation, lifting/chronological semantics, and the controlled-rotation compiler. Its normalization theorem needs only positive squared norm. Its exact gate counts need the particular reference multiplexor recurrence, not state positivity. The special-orthogonal existence conclusion needs orthonormal prescribed columns, their injective placement, and an unused physical column; the strict dimension condition is a sufficient supplier of the last input. The local stage conclusion needs actual real chain data, local canonicality, the maximum-rank bound, a stage within the chain, the padded-column isometry, explicit physical coordinates/placement, and the explicit completion producer. No one member of these conjunctions is separately sufficient.

Classical basis extension with an unused-column determinant correction and explicit adjacent-row elimination with permutation-parity correction are alternative routes to a matched completion specification. They are not a single conjunction requiring both methods. Their algorithmic evidence differs. The full-table amplitude tree and a structured tensor route are also alternatives only after the structured route supplies a chain, its boundary, local circuits and global assembly under the same target, normalization, register and error contract; the present local completion result alone does not establish that alternative's full closure.

No external paper's omitted argument has been silently supplied. The signed all-width strengthening with the unchanged zero-wire exact-phase tree is REFUTED, not an open supplier: at n=0 and singleton f=-1, the empty tree returns +1 whereas the normalized target is -1, as already stated in D1. This does not refute the original nonnegative theorem or establish a mathematical obstruction to positive-width signed preparation. Open bridges for stronger public claims are: less restrictive flat-table premises; efficient function-to-chain extraction; bounded-rank approximation and its normalization/error analysis; deterministic finite-bit canonicalization; numerical angle evaluation and rounding robustness; primitive local compilation and physical global placement for the chosen producer; initial-boundary loading; and preprocessing, depth, connectivity and compiled-gate costs. The source-level H0 coordinate definition additionally requires an implementation-adapter audit. These are explicitly separate obligations, not consequences of an oracle count of zero or of exact matrix existence.

In particular, the exact-real resources here exclude numerical representation length, transcendental evaluation, conditioning near zero pivots, finite-bit zero/sign decisions, synthesis into a discrete universal gate set, approximation-error accumulation, memory access, classical copying and output/readout. There is no postselection or success-probability loss in the exact amplitude tree or the stated local matrix action. No arbitrary matrix block-encoding follows from a prepared state: selection, unpreparation, coefficient/phase conventions and their costs would be additional conjunctive inputs. Conversely an operator-to-state construction would need its input state, a nonzero accepted branch, normalization and any postselection/amplification costs. Neither transport is certified by the present three results.
