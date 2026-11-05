# Finite real thin LQ factorization

A real matrix can be reconstructed from orthonormal row directions even when its rows are dependent or zero. The result below guarantees a factorization, not a fast algorithm or a triangular factor. It is a retrospective local mathematical contract for the existing ThinLQ module, not a claim of new mathematics or faithful reproduction of an external paper.

## Statement

Let \(m,n\) be nonnegative integers, let \(A\in\mathbb R^{m\times n}\), and put \(r=\min(m,n)\). There exist
\[
R\in\mathbb R^{m\times r},\qquad Q\in\mathbb R^{r\times n},
\qquad A=RQ,\qquad QQ^{\mathsf T}=I_r.
\]
The rows of \(Q\) are orthonormal. No full-rank, linear-independence, positivity or nonzero-row premise is needed. The row count is \(r\), not necessarily the rank of \(A\). If \(r=0\), the orthogonality equation is an equality of empty matrices.

The scalar field is real; transposition is ordinary transpose, not a complex adjoint. No quantum registers, oracles, ancillas, phases, approximation, success probability or resource claim occurs in this contract.

## Removing zero terms from a sum

For \(m\le n\), a function \(f:\{0,\ldots,n-1\}\to M\) into an additive commutative monoid satisfies
\[
\sum_{i=0}^{m-1} f(i)=\sum_{j=0}^{n-1}f(j)
\]
whenever \(f(j)=0\) for \(j\ge m\). Embed the prefix into the full index set. The embedding is injective, so it neither duplicates nor changes terms; every term in the complementary set is zero. This argument also covers an empty prefix.

Lean declaration: `QuantumBlockEncoding.ThinLQ.sum_prefix_of_zero`. Its additive commutative monoid interface is more general than the real-coordinate instance used below.

## Wide matrices

Assume \(m\le n\). Extend the list of rows of \(A\) to a list \(f_0,\ldots,f_{n-1}\) of vectors in \(\mathbb R^n\) by appending zero vectors. Use a full orthonormal basis \(b_0,\ldots,b_{n-1}\) produced by ordered Gram–Schmidt with orthonormal completion. Completion, rather than division by the norm of every input row, is essential for dependent rows.

The ordered-basis property needed here is
\[
\langle b_k,f_i\rangle=0\quad\text{when }i<k.
\]
Together with expansion in a full orthonormal basis, it implies, for each \(i<m\),
\[
f_i=\sum_{k=0}^{n-1}\langle b_k,f_i\rangle b_k
    =\sum_{k=0}^{m-1}\langle b_k,f_i\rangle b_k.
\]
The second equality uses the prefix-sum result: every removed index satisfies \(k\ge m>i\).

Define \(R_{ik}=\langle b_k,f_i\rangle\) and \(Q_{kj}=(b_k)_j\), retaining the first \(m\) basis vectors. Taking coordinate \(j\) in the displayed expansion gives
\[
A_{ij}=\sum_{k=0}^{m-1}R_{ik}Q_{kj}=(RQ)_{ij}.
\]
For any \(i,k<m\), orthonormality of the full basis gives
\[
(QQ^{\mathsf T})_{ik}=\sum_{j=0}^{n-1}(b_i)_j(b_k)_j
                      =\langle b_i,b_k\rangle=\delta_{ik}.
\]
This constructs the two required factors without assuming independence of the input rows.

Lean declaration: `QuantumBlockEncoding.ThinLQ.exists_factor_of_le`. The imported Mathlib provider is `gramSchmidtOrthonormalBasis`; the vanishing-coordinate property is `gramSchmidtOrthonormalBasis_inv_triangular'`. `OrthonormalBasis.sum_repr` supplies expansion, and `OrthonormalBasis.inner_eq_ite` supplies orthogonality. These are formal dependencies, not external oracle assumptions.

## All shapes

If \(m\le n\), apply the wide-matrix construction and substitute \(r=m\). If \(m>n\), take \(R=A\) and \(Q=I_n\); then \(A=AI_n\), \(I_nI_n^{\mathsf T}=I_n\), and \(r=n\). The same argument includes \(n=0\).

Lean declaration: `QuantumBlockEncoding.ThinLQ.exists_thin_lq`.

## Formal context and boundary

The authoritative source is [ThinLQ.lean](../../QuantumBlockEncoding/ThinLQ.lean). Its current source, rather than a copied proof, supplies the Lean disclosures when this lesson is admitted into the generated textbook. Module imports are `Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho` and `Mathlib.Data.Matrix.Basic`.

The conceptual move is orthonormal completion followed by coordinate reconstruction. It can support tensor-train factorization mathematics, but it does not produce stored factors, pivot instructions, rotations or runtime bounds. Those require the distinct constructive and stored suppliers. Neither existence nor a matrix's output dimensions certifies an efficient state-preparation compiler.

The current whole-module admission status is recorded in `website/research/publications.json`, with independently bound evidence under `reviews/publication/thin-lq/`. This lesson does not close other changed-module publication obligations or promote the Hermite root.
