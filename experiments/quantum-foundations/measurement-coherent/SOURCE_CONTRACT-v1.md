# Original mathematical interface: finite coherent branch map

This is a comparison view of the mathematical contract already frozen in
STATEMENT_SEAL-v1.md (SHA-256
dfeff3145f5f0bf3010b4ad211e80bbc679551607635f2da2e24138e919661e3),
not a new statement freeze or an external-paper equivalence claim.

Let the outcome type be finite, possibly empty. Let the input and output be
complex Hilbert spaces, possibly zero, infinite-dimensional, and different.
For a family of bounded complex-linear maps $M_i:E\to F$, assume exactly
$\sum_i M_i^\dagger M_i=I_E$. Construct the literal finite Hilbert-product map

$$
V_M:E\longrightarrow \bigoplus_{i\in\iota}^{\ell^2}F,
\qquad (V_M\psi)_i=M_i\psi,
$$

as a complex-linear isometry using the existing Hilbert-product and isometry
interfaces. Prove the stated coordinate action and derive, through the
assembled isometry, the equality of full complex overlaps

$$
\sum_i\langle M_i\psi,M_i\phi\rangle=\langle\psi,\phi\rangle
$$

for arbitrary input vectors. There are no normalization, nonzero-branch,
nonempty-outcome, nontrivial-space, finite-dimensionality or equal-dimension
premises. The product stores the whole finite tuple of branch amplitudes; it
is not their sum in $F$. The inner product is conjugate-linear in its first
argument and linear in its second.

The desired mathematical use is coherent branch bookkeeping before forgetting
outcomes: retain superpositions and full overlaps, not only probabilities.
This contract does not specify tensor/register identifications, a surjective
unitary or dilation, an instrument/channel, density/trace semantics, branch
normalization, a physical circuit, oracle access, ancilla cleanup, resource
counts or a finite-bit algorithm. None of those follows merely from its name.
