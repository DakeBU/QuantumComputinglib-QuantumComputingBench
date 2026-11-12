# Source-blind mathematical reconstruction

## Input binding and actor

- Input: `W/measurement-intake-c399/FORMAL_PACKET.md`.
- Input SHA-256: `22dd3de60cdae81f4af4a009e11e435fb04540145e39e317167819230ea52772` (read and independently hashed).
- Authoring actor: `/root/measurement_blind_c399`, source-blind mathematical decoder.
- Scope: reconstruct only the supplied signatures and their mathematical consequences. No source, proof, seal, upstream material, external source, build, or repository history was consulted. No subagents were used.
- This is not a verdict on any source implementation, proof, compilation, or publication acceptance.

## Ambient objects and quantifiers

Both declarations universally quantify over types `ι`, `E`, and `F`, a specified finite indexing structure on `ι`, and the displayed normed additive commutative group, complex inner-product space, and completeness structures on `E` and `F`. Thus `E` and `F` are complex Hilbert spaces, possibly infinite-dimensional or the zero space; no finite-dimensionality, separability, dimension equality, or nontriviality is assumed. The finite index type can be empty. The namespace and import do not add a mathematical hypothesis.

For every indexed family of bounded complex-linear maps `M_i : E → F`, assume the bounded-operator identity on `E`

`Σ_{i ∈ ι} M_i* M_i = I_E`.

Here `M_i* : F → E` is the Hilbert adjoint, and each product means first applying `M_i` and then its adjoint. This is a finite, unweighted sum; the identity is on the input space, not the output space. All squared vector norms below are real numbers.

## Literal assertions

1. For every such family satisfying the identity and every vector `ψ ∈ E`, without a normalization assumption,

   `Σ_{i ∈ ι} ‖M_i ψ‖² = ‖ψ‖²`.

2. For every such family satisfying the identity, every vector `ψ ∈ E` with exactly `‖ψ‖ = 1`, and every index `i ∈ ι`,

   `0 ≤ ‖M_i ψ‖² ≤ 1`.

The second conclusion is membership in the closed real interval `[0, 1]`; neither inequality is strict.

## Consequences and mathematical meaning

Taking the quadratic form of the operator identity at `ψ` yields the first equality: each term is `‖M_i ψ‖²`. Every summand is nonnegative, so any one term is at most their sum. Consequently `0 ≤ ‖M_i ψ‖² ≤ ‖ψ‖²` for arbitrary `ψ`; under unit normalization the finite numbers `p_i = ‖M_i ψ‖²` sum to one and each lies in `[0, 1]`. In particular, each `M_i` is norm-nonincreasing. These are mathematical implications of the packet, not checks of a supplied formal proof.

Zero outcome weights and weights equal to one are allowed. An individual map may be zero. For a unit vector, a weight is one precisely when every other outcome weight is zero. No positivity away from zero is asserted.

## Empty and zero cases

- If `ψ = 0`, every output and every weight is zero, and the first equality is `0 = 0`. This vector cannot meet the unit-norm hypothesis of the second assertion.
- If `E` is the zero space, all maps out of it are zero and `I_E` is also the zero map. Hence the operator identity holds for every family, including an empty one; the first assertion remains `0 = 0`. There is no unit vector, so the second assertion has no applicable state.
- If `ι` is empty, the operator sum is zero. Its equality with `I_E` forces `E` to be the zero space; conversely the identity holds for an empty family when `E` is the zero space. The first assertion then reads `0 = 0`. The second has no index to instantiate and also no unit vector compatible with the identity. With nonzero `E`, no empty family satisfies the premise.
- If `F` is the zero space, every `M_i` is zero, so the operator identity again forces `E` to be the zero space. A zero output space and nonzero input space cannot satisfy the premise.
- None of these premises guarantees a family exists for arbitrary chosen spaces. A unit vector, if supplied, entails nonzero `E`, nonempty `ι`, and nonzero `F` under the operator identity.

## Scope not established

The assertions do not assume or establish that individual maps are projections, mutually orthogonal, unitary, or isometries, nor that `M_i M_i* = I_F`. There is no assertion that different outcome images are orthogonal. No distinctness or nonzeroness of maps or weights is required. Without unit normalization, the weights sum to `‖ψ‖²`, not necessarily one, and the upper bound one is not generally available.

Only finite-outcome, pure-vector squared-norm statements over the complex numbers are covered. The packet specifies no physical measurement implementation, state-update rule, normalized conditional output, density-operator formulation, infinite-outcome extension, or convergence claim. It supplies proposed theorem signatures, not their proofs; this reconstruction establishes no fact about a corresponding source file or its compilation.
