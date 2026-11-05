# Public display-only derivation

This is `PUBLIC_REPORT.md`, a separate public-safe display derivation of `REPORT.md`. The original `REPORT.md` and `FREEZE.json` remain unchanged. The original report body below is reproduced in full, with only private input/output path spellings replaced by the logical artifact names `FORMAL_PACKET-v1.md`, `REPORT.md`, and `FREEZE.json` where applicable. No private spelling is reproduced in a mapping.

Original input `FORMAL_PACKET-v1.md` SHA-256: `2a1af6af46029820d070b3818a787b74414a28224acc976bf01265f88342aa79`.

Original `REPORT.md` SHA-256: `bd7aa0f9d585fa2f1207088b3fb3c035ba206793ca325eff1f1b0782b324d36c`.

Original `FREEZE.json` SHA-256: `43bda5da6243ace0d6710cf7fd4423634728c0116c078a3f0645b0b0fe1b4265`.

This is display-only path removal, not a new independent run, new reconstruction, additional independent review, or new verdict. The full mathematics and real canonical agent identity `/root/finite_branch_blind_c404` are preserved. That identity is a task name, not a local filesystem path. Historical scope and provenance statements in the reproduced body refer to the original reconstruction. Only this agent's already generated artifacts were read to prepare this display derivation; no extra source, repository, implementation, or network material was read.

---

# Source-blind reconstruction of the supplied finite-branch contract

## Provenance and scope

Decoder identity: `/root/finite_branch_blind_c404`, in its current delegated run. No separate runtime run identifier was exposed to this agent, so none is invented here. This report was authored by that agent; it does not represent an additional review by another person or agent.

The sole pre-existing input read was:

`FORMAL_PACKET-v1.md`

Its actual byte-level SHA-256, computed before reconstruction, is:

`2a1af6af46029820d070b3818a787b74414a28224acc976bf01265f88342aa79`

This equals the expected input hash supplied in the assignment. The input was read in full. No sibling seal, implementation, prior report, repository file, source paper, or network resource was read. No compilation or Git operation was performed. The mathematical discussion below is a reconstruction of the supplied interfaces, not a source-correspondence, build, or admission verdict.

## 1. Common ambient objects and quantifiers

Both namespaces quantify over an arbitrary finite index type `ι`, equipped with `Fintype ι`, and arbitrary complex Hilbert spaces `E` and `F`. More explicitly, each space has a normed additive commutative group structure, a complex inner-product-space structure, and completeness. There is no finite-dimensionality assumption on either space, no requirement that they coincide, and no nonzero-space assumption. The finite index type need not be inhabited.

Every declaration involving `M` takes an arbitrary family of bounded complex-linear maps

`M_i : E -> F`, for every `i` in `ι`.

Thus, for all complex scalars `a, b` and all `ψ, φ` in `E`, each branch satisfies

`M_i(a ψ + b φ) = a M_i ψ + b M_i φ`.

Its Hilbert adjoint has the reverse type, `M_i* : F -> E`. The composition `M_i*.comp M_i` sends an input `x` first through `M_i` and then through `M_i*`; it is the endomorphism `M_i* M_i` of `E`, not `M_i M_i*` of `F`.

All four declarations take the same explicit hypothesis, denoted here by `hM`:

`sum over i in ι of M_i* M_i = I_E`.

This is equality of bounded complex-linear endomorphisms of the input space. In particular, for every `x` in `E`, it asserts `sum_i M_i*(M_i x) = x`. The finite sum includes every element of `ι`; it is neither a selected subset nor an infinite series. The symbol `1` is the identity of `E`, not a scalar, an identity of `F`, or an identity on the output product.

The family and this operator identity are supplied assumptions. The declarations do not construct such a family from dimensions or assert that every family satisfies the identity. The state vectors that occur below are universally quantified and are not assumed to be unit vectors, nonzero, or mutually orthogonal.

The namespaces organize names only. The notation scope and imports do not add mathematical hypotheses. The `[simp]` annotation on the application theorem marks a simplification rule; it does not change its mathematical assertion.

## 2. The complex inner-product convention

Write the inner product as `<x,y>`. It is conjugate-linear in the first argument and linear in the second:

`<a x,b y> = conjugate(a) b <x,y>`.

In particular, `<x,x> = ||x||^2`, viewed as a real nonnegative number embedded in the complex numbers when necessary. With this convention the adjoint relation can be written

`<M_i x,y>_F = <x,M_i* y>_E`.

Consequently the supplied operator identity yields, for arbitrary `ψ, φ`,

`sum_i <M_i ψ,M_i φ>_F = <ψ,(sum_i M_i* M_i) φ>_E = <ψ,φ>_E`.

This is equality of complex numbers, including imaginary parts, rather than only equality of real parts or absolute values.

## 3. Reconstruction of every supplied declaration

### `MeasurementProbability.sum_norm_sq_eq`

For every choice of the ambient types and structures, every family `M`, every witness `hM` of the input-space operator identity, and every `ψ` in `E`,

`sum_i ||M_i ψ||^2 = ||ψ||^2`.

This is equality in the real numbers. It is not restricted to normalized inputs. For a unit input, the nonnegative weights `p_i = ||M_i ψ||^2` sum to one and therefore form a finite probability distribution. For an arbitrary input their total is the squared input norm. For the zero input all weights are zero. A conditional normalization by `||ψ||^2` is meaningful only when `ψ` is nonzero; no such division is part of the declaration.

No individual probability function, sampling process, state-update rule, or normalized post-measurement vector is defined here. The namespace name alone supplies none of those objects.

### `MeasurementCoherent.branchIsometry`

For every family `M` and witness `hM`, this definition supplies a bundled complex-linear norm-preserving map

`V = branchIsometry M hM : E -> H`,

where `H = PiLp 2 (fun _ : ι => F)` is the finite Hilbert product of copies of `F`, indexed by `ι`. An element of `H` is a tuple `x = (x_i)`, with

`||x||_H^2 = sum_i ||x_i||_F^2`

and

`<x,y>_H = sum_i <x_i,y_i>_F`.

The bundled type states both complex linearity and norm preservation:

`V(a ψ + b φ) = a Vψ + b Vφ`, and `||Vψ||_H = ||ψ||_E`.

It follows that `V` preserves distances and is injective. These are properties of the single map into the full product. The type does not assert that `V` is surjective, and it is not the type of a surjective linear isometric equivalence.

The `noncomputable` modifier does not weaken these mathematical properties or make the output multivalued. It does not supply an executable algorithm or an efficiency bound.

### `MeasurementCoherent.branchIsometry_apply`

For every `M`, every witness `hM`, every `ψ` in `E`, and every `i` in `ι`,

`(branchIsometry M hM ψ)_i = M_i ψ`.

This equality is an equality of vectors of `F`, identifying one coordinate of the product output. Together for all coordinates, it characterizes the entire output as

`Vψ = (M_i ψ)_(i in ι)`.

It does not say `Vψ = M_i ψ`, which would generally have mismatched ambient spaces. It also does not say that the coordinate map `M_i` is an isometry, or that different branch outputs are equal. The proof witness `hM` introduces no additional choice of branch phase: any two witnesses for the same `M` give the same coordinate values and hence the same map extensionally.

### `MeasurementCoherent.sum_inner_eq`

For every `M`, every witness `hM`, and every pair of vectors `ψ, φ` in `E`,

`sum_i <M_i ψ,M_i φ>_F = <ψ,φ>_E`.

Equivalently, with the map and product above, `<Vψ,Vφ>_H = <ψ,φ>_E`. The two input vectors are independent universal variables; the theorem is not only the diagonal case `ψ = φ`. It preserves complex overlaps, not just the squared norm of each input separately. Setting `φ = ψ` recovers the squared-norm identity after identifying real squared norms with their complex embeddings.

## 4. What linearity and phase preservation mean here

For the fixed supplied family `M`, the coherent output is a tuple of actual vectors, not a tuple of their norms or probabilities. For any finite superposition, applying `V` distributes with the original complex coefficients. For example,

`V(a ψ + b φ) = (a M_i ψ + b M_i φ)_i`.

Therefore this contract does not discard input relative phase before forming the output. In each branch the interference expression is

`||a M_i ψ + b M_i φ||^2`

`= |a|^2 ||M_i ψ||^2 + |b|^2 ||M_i φ||^2 + 2 Re(conjugate(a) b <M_i ψ,M_i φ>)`.

Summing over branches replaces the branch overlap sum by `<ψ,φ>`. This explicitly preserves the dependence on the relative complex coefficients. Also `V(a ψ) = a Vψ`, so a global phase is carried along as a global phase of the full tuple.

This does not mean that the weights `||M_i ψ||^2` alone determine the coherent tuple, that the operator identity fixes all branch phases, or that each individual branch preserves the input overlap. For example, replacing each branch by `N_i = u_i M_i` with `|u_i| = 1` leaves every `M_i* M_i` and every branch squared norm unchanged. It can nevertheless change the relative phase between nonzero coordinates of the coherent output. The application theorem fixes the output for a given `M`; it does not identify these different families.

Different coordinates are orthogonal coordinate subspaces in the product Hilbert space. The product inner product sums only equal-index terms. It does not assert that `M_i ψ` and `M_j φ`, regarded inside the same space `F`, are orthogonal when `i != j`. Nor does it require `M_i* M_j = 0`. Coherently summing the vectors in `F`, `sum_i M_i ψ`, is a different operation from storing the tuple in `H`; no norm identity for that sum is supplied.

## 5. Combined isometry versus individual branches and unitary maps

Every branch is a contraction: `||M_i ψ||^2 <= sum_j ||M_j ψ||^2 = ||ψ||^2`. Equality for an individual branch is not required. Branches may be zero, noninjective, or overlapping in their ranges.

For a concrete two-branch example on a nonzero Hilbert space with `E = F`, take both branches to be `(1/sqrt(2)) I`. The hypothesis holds, and the coherent map is `ψ -> (ψ/sqrt(2), ψ/sqrt(2))`. Neither branch is norm preserving, and the coherent range is only a proper subspace of `E x E`. Thus the combined map is an isometry but is not surjective.

A different permitted two-branch example is `M_0 = I`, `M_1 = 0`, yielding `Vψ = (ψ,0)`. This also has a proper range when `E = F` is nonzero. These examples show why pointwise coordinate equality must not be read as branch-wise isometry or as a surjective unitary claim.

The input identity is not an output identity. In particular, the packet does not assume or conclude that `sum_i M_i M_i* = I_F`, that each branch is invertible, or that `V V* = I_H`. A surjective unitary from `E` to `H` would require surjectivity in addition to the supplied complex-linear isometry. Surjectivity is not a field of the declared result.

## 6. Empty, zero, infinite-dimensional, and rectangular cases

**Empty index type.** The finite sum is zero and the target product has exactly one element, its zero vector. The hypothesis becomes `0 = I_E`. Applying it to any `x` forces `x = 0`, so it can hold only when `E` is the zero space. In that case both norm and inner-product identities have zero sides, the coordinate theorem is vacuous, and the unique map from the zero source to the zero product is surjective. If `E` is nonzero, there is no witness `hM` for an empty index type. The interfaces do not silently posit such a witness.

**Zero input vector.** In any permitted spaces and family, all `M_i 0` and `V0` are zero. The identities remain valid without normalization. The zero vector is not thereby turned into a unit state or a probability distribution of total one.

**Zero source space.** For any finite index type and any `F`, every branch out of the zero space is the zero map, and the operator identity is satisfied because its identity endomorphism is also zero. The resulting coherent map is the unique zero-source isometry. It is surjective exactly when the product target is itself zero, not in general.

**Zero branch space.** If `F` is zero, the product is zero and every branch is zero. The hypothesis forces `E` to be zero as well. More generally, any all-zero family forces a zero source, regardless of `F` or the size of `ι`.

**Singleton index type.** The hypothesis reduces to `M* M = I_E`; the coherent map is that isometric embedding into a single copy of `F`. It need not be onto. Even if `E = F` is infinite-dimensional, a proper isometric embedding is possible; the right shift on complex square-summable sequences is an example.

**Infinite-dimensional spaces.** Arbitrary complete complex inner-product spaces are allowed. The number of branches remains finite. No finite-dimensional matrix theorem, convergence of an infinite branch sum, compactness, trace formula, or dimension-equality argument is assumed. The contract neither extends its index quantifier to infinite `ι` nor asserts an infinite-sum analogue.

**Rectangular maps.** `E` and `F` are independent spaces, so each branch can have different input and output dimensions. For example, take `E = C^2`, `F = C`, and two coordinate projections. The two adjoint-products sum to the identity of `C^2`; the full tuple map is an isometry (in this example onto `C^2`), although neither scalar-valued branch is injective. In finite dimensions, injectivity of the full map implies `dim(E) <= |ι| dim(F)`, not in general `dim(E) <= dim(F)`. This dimension restriction is a consequence under extra finite-dimensional assumptions, not an assumption in the packet. No construction is asserted for dimensions where the hypothesis is impossible.

## 7. Limits of the contract

The interfaces do not supply a unitary extension on an enlarged space, a circuit or implementation of `V`, an output-surjectivity theorem, a reversible operation acting on every vector of the output product, a branch-wise isometry theorem, or equality between distinct branch families with the same probabilities. Inverting `V` on its image is mathematically different from asserting that every output tuple has a preimage.

They also do not define a classical measurement record, mixed-state channel, density-operator evolution, postselection success protocol, normalization of a selected branch, or behavior of a measurement apparatus. Such structures or interpretations need additional definitions. The supplied assertions concern a finite family of bounded complex-linear maps satisfying one operator identity, the resulting norm and overlap equalities, and a precisely characterized complex-linear isometric embedding into a finite Hilbert product.
