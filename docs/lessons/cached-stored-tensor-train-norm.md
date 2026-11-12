# Cached tensor train norms with stored inputs

A tensor train describes a vector by small matrices, one for each physical
bit. Its norm can be computed from those matrices without constructing all
\(2^n\) amplitudes. For an already stored real train of length \(n\), whose
bond dimensions are at most \(D\), the specified cached procedure returns
the exact norm and uses at most
\[
 n(24D^3+25D^2+20D+6)+5D^2+4D+9
\]
charged operations in the extended exact-real word model. This does not
include producing the input cores or implementing exact real arithmetic
with finite bits.

This is a retrospective local mathematical contract for
QuantumBlockEncoding/StoredTensorTrainNorm.lean, not an external-paper
assimilation or a novelty claim. Existing signatures are unchanged;
independent source-blind reconstruction and comparison determine admission.

## Matrices and complete norm

Let the bond dimensions be \(d_0,\ldots,d_n\). At site \(i\), the two real
matrices \(A_i(0),A_i(1)\) have shape \(d_i\times d_{i+1}\). Each core is a
stored nested vector, not an unevaluated function. Its flattened column
address is \(b\,d_{i+1}+j\), with physical bit \(b\in\{0,1\}\) and right
bond label \(j\).

For a bit word \(x=(x_0,\ldots,x_{n-1})\), write
\(M_x=A_0(x_0)\cdots A_{n-1}(x_{n-1})\).
The right Gram environments are
\[
 E_n=I_{d_n},\qquad
 E_i=\sum_{b=0}^1 A_i(b)E_{i+1}A_i(b)^{\mathsf T}.
\]
They satisfy
\[
 E_0=\sum_{x\in\{0,1\}^n} M_xM_x^{\mathsf T}.
\]
All terminal bond labels are included in this matrix identity. No accepted
sector or garbage projection appears. When \(d_0=d_n=1\), the returned
scalar is
\[
 \sqrt{E_0(0,0)}
 =\sqrt{\sum_x M_x(0,0)^2}.
\]
Zero trains require no special nonzero assumption; an empty scalar-boundary
train has norm one. This is the real Euclidean norm, not a complex
conjugate-transpose statement or a state-normalization theorem.

The word order follows the supplied train, with its first physical bit first.
There is no physical little-endian wire adapter here. A quantum consumer must
prove its chosen word-to-register equivalence separately.

## Stored contraction procedure

Compute the tail environment once and retain its stored table. For each bit
\(b\), materialize
\[
 F_b(a,j)=\sum_{t<d_{i+1}} A_i(b)(a,t)E_{i+1}(t,j),
 \qquad
 G_b(a,c)=\sum_{j<d_{i+1}}F_b(a,j)A_i(b)(c,j).
\]
Materialize the sum \(G_0+G_1\). The transpose in the formula is implemented
by exchanged indices of the original core, not by a free dense constructor.
The stored identity initializes the last environment. After the complete
recursion, read the scalar entry and take one square root.

The recurrence is correct entry by entry by finite-sum matrix
multiplication. Induction on the chain then identifies the stored output
with \(E_i\). For the sum identity, expand over the first bit, apply the
tail identity, and distribute matrix products through the finite sum;
\((AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}\) fixes the multiplication
order. With scalar boundary, the single matrix entry is the complete sum
of squares. Thus the exponential word sum occurs in the specification,
not in this stored producer.

## Charged operation model

A run contains a returned value and eight natural counters: field, square
root, angle, trigonometry, comparison, read, write and emitted record.
Composition adds counters. A stored matrix entry costs two reads, one for
its row and one for its scalar. Each multiplication and addition costs a
field operation. A sum over \(m\) terms performs \(m\) multiplications and
\(m\) additions, including adding the final zero.

Materializing an \(l\times r\) matrix charges
\(4(lr+l)\) reads and writes in total, in addition to the entry producers.
Consequently a product with inner size \(m\) has total budget
\[
 B(l,m,r)=6lrm+4(lr+l),
\]
and adding two \(l\times l\) stored matrices has budget
\[
 S(l)=9l^2+4l.
\]
The four products and one sum at a site with bonds \(l,m\) therefore cost
\[
 2B(l,m,m)+2B(l,m,l)+S(l)
 =12lm^2+12l^2m+8lm+17l^2+20l.
\]
Each recursion node adds six charged cache/traversal words. The terminal
identity costs \(5r^2+4r\), with another six words at its node. For all
bonds bounded by \(D\), induction gives
\[
 \operatorname{cost}(\mathrm{gram})
 \le n(24D^3+25D^2+20D+6)+5D^2+4D+6.
\]
The final entry lookup and square root add exactly three operations, giving
the stated norm bound. Per-operation bounds retain the eight counters;
summing them does not turn the model into wall-clock time.

Input construction, integer precision, transcendental implementations,
counter bookkeeping, proof checking, actual allocation/peak live memory
and numerical stability are outside this model. A finite-bit algorithm
must supply its own error and bit-cost analysis. No oracle, gate, depth,
ancilla cleanup, postselection, global-phase quotient or exported circuit
is certified by this scalar supplier.

## Mathematical and formal correspondence

| Mathematical step | Formal definitions and results |
| --- | --- |
| First stored product | firstEntry, firstPass, firstPass_value, firstEntry_cost_le, firstPass_cost_le |
| Second stored product | secondEntry, secondPass, secondPass_value, secondEntry_cost_le, secondPass_cost_le |
| Stored sum | addMatrices, addMatrices_value, addMatrices_cost_le |
| One cached update | update, update_value, productBudget, additionBudget, updateBudget, update_cost_le, update_total_cost_le |
| Complete cached recursion | cacheNode, gram, gram_value, gram_total_cost_le |
| Scalar norm and final lookup | norm, norm_value, norm_eq_sum, norm_cost, norm_total_cost_le |

All names in the table belong to
\(\texttt{QuantumBlockEncoding.StoredTensorTrainNorm}\).
Read the current complete source for exact signatures and proofs; generated
Lean disclosures should extract these source bytes rather than copy proofs.

## Reuse and the four graph views

The source construction graph is the mathematical sequence from two
materialized products per bit to the cached Gram recursion, then scalar
extraction and the charged bound. The Lean graph reuses stored
matrix/chain operations and the complete norm-sum identity from
StoredTensorTrain and TensorTrainNormEnvironment; this packet does not
admit those whole modules transitively.

The compressed quantum spine is **local Gram contraction for normalization**.
A possible transport to complex cores replaces transpose by adjoint, and a
possible cross-Gram transport uses two trains. Both require separate proofs:
they are conceptual Functor Hypergraph candidates, not implications supplied
by this real same-train module. Reader purification and complete scientific
resource closure remain separate from local module admission.
