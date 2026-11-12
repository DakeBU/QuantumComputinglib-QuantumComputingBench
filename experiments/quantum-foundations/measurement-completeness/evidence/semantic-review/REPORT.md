# Independent bounded measurement semantic/canonicality review

Actor: `/root/measurement_semantics_c400`. Date: 2026-10-23.
Distinct formalizer: `/root`. Distinct source-blind decoder:
`/root/measurement_blind_c399`.

## Verdict and scope

**Bounded semantic verdict: ACCEPT.** The two actual declarations correctly
express and prove their sealed pure-vector assertions. No signature change,
extra premise, orientation repair, or proof-body repair is required on this
review. This conclusion was reached from the actual implementation, the pinned
upstream source independently retrieved through connected GitHub `fetch_file`,
and the independently frozen decoder reconstruction, not from an author's
acceptance wording or a build outcome.

**Canonicality verdict: no exact duplicate found by the bounded search;
downstream-consumer and purification status remain provisional.** The first
lemma is genuinely consumed by the second lemma. The inspected canary only
repackages these claims; it is not evidence of an independent production
measurement application. This packet does not certify a fully consumed,
integrated or purified foundational API. For that stronger Class-B admission
claim, identify a genuine non-wrapper downstream use or continue to label this
as a preparatory shared library fragment. No extra quantum-state/measurement
wrapper should be introduced merely to manufacture a consumer.

This is not a transitive TCB/axiom audit, Lean/build verdict, publication
admission, proof seal, main-integration decision, upstream build, private task
solution, whole-paper assimilation, or scientific novelty judgement. None of
those statuses is inferred here.

## Exact reviewed input

The actual source was read in full at
`W/measurement-intake-c399/QuantumBlockEncoding/MeasurementProbability.lean`.
Its SHA-256 is
`33c1a01b8f1e752f22acbc12ae47faa503e5dc7ae5f3f4d73dff39eeb9505775`
(2244 bytes). Checks made before, during, and after source inspection agreed.
No candidate change was observed. The two signatures match the statement seal
and formal packet. The exact bound inputs and remote source pins are in
`INPUT_PINS.json`.

The decoder input/report hashes independently match its `FREEZE.json`:
formal packet `22dd3de60cdae81f4af4a009e11e435fb04540145e39e317167819230ea52772`;
report `b2b67cd91461ad95990d8bf07e9305a534bf6420f30adbe78fe903cdbbb46c17`.
Its reconstruction agrees with the actual theorem interfaces, including all
degenerate cases and the absence of density/update/physical conclusions.

## Independent upstream reading and precise correspondence

Independently retrieved [AxQM Measurement.lean](https://github.com/Axiomatic-AI/AxQM/blob/2ccf167efca86eb5164f1df8cedb72b84626b479/AxQM/Basic/Measurement.lean)
at commit `2ccf167efca86eb5164f1df8cedb72b84626b479`.
The fetched Git blob is exactly
`1a078f8cd71d6b41c3e87bb70c763c3a2a628aa0`. Independently computing Git's blob
hash from the returned UTF-8 content reproduced that blob; its content SHA-256
is `17e039db7edde642e3dcabc4b423ba4a490ce82678fe8fafdec143c41188091c`.
Also retrieved `AxQM/Basic/StateSpace.lean` and `AxQM/Basic/QSystem.lean` at the
same commit to expand the actual state/system binders.

Upstream `QSystem` bundles a finite-dimensional complex inner-product space.
`Measurement ι S` has finite outcomes and endomorphisms `S ->L[ℂ] S`, together
with `sum_i M_i* M_i = I_S`. Its `State S` is a positive trace-one operator.
`bornProb` is defined via the induced POVM's density-operator probability;
normalization is proved using the density predicate. The file also constructs
orthonormal-basis measurements and defines a normalized density update when
the selected Born probability is nonzero. `PureState` is a unit vector and
`toState` is its rank-one density operator, but the local module does not use
or bridge that conversion.

The local theorems instead concern bounded maps `M_i : E ->L[ℂ] F`, with `E`
and `F` arbitrary complex Hilbert spaces, and vector weights `||M_i ψ||²`.
Rectangular codomain and possibly infinite dimensions are deliberate
generalizations of the operator substrate, not equivalence to all upstream
measurement semantics. In the finite endomorphism setting an explicit
rank-one/trace adapter would still be needed to identify these weights with
AxQM's `bornProb`. No such adapter is present or certified here. No mixed-state
normalization, complete positivity, instrument/dilation, collapse, or circuit
implementation follows as an admitted local result from this review.

Upstream attribution is retained: Axiomatic AI, Winston Yin and Frank Koppens,
Apache-2.0. The book reference in upstream comments is not a fresh inspection
of Nielsen-Chuang or a claim to have checked its exercises. No private task
file was consulted.

## All binders and dependency/premise separation

The implicit types `ι`, `E`, and `F` and their listed structures are universal.
`Fintype ι` supplies a finite unweighted sum and allows an empty carrier.
The normed additive group and complex inner-product structures are typing;
`CompleteSpace E` and `CompleteSpace F` are the Hilbert-adjoint API's typing
conditions for this generalized contract. No finite-dimensionality,
nontriviality, separability, equal-dimension, or nonempty-outcome hypothesis is
hidden in a project alias: there are no project-owned contract aliases here.

`M`, `ψ`, and, for the second theorem, `i`, are ordinary data. `hM` is exactly
the chosen local completeness premise; it corresponds to upstream's
`Measurement.complete` field, not to an auxiliary proof convenience. `hψ` is
the exact unit-vector premise in the local probability theorem (consistent
with the upstream pure-state convention, but not a replacement proof of the
density theorem). The first theorem needs no normalization premise. Relative
to this bounded Class-B contract, no EXCESS logical premise was found.

Adjoint quadratic-form identities, finite sum evaluation/additivity, norm-square
nonnegativity and single-term-versus-sum order are proof dependencies, not
additional theorem premises. In particular, neither positivity of each
effect, an effect contraction bound, normalized outputs, branch nonzeroness,
nor a supplied total-probability identity is smuggled into the signatures.
There are no choice/default/quotient definitions to audit in this module.

## Mathematical and actual-proof check

For every index, the exact Mathlib dependency
`ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left` gives
`||M_i ψ||² = Re <M_i* M_i ψ, ψ>`. The implementation sums this identity,
uses finite additivity of the inner product and real part, then substitutes
`hM` and the identity action. This yields the stated equality for arbitrary
`ψ`, without dividing by its norm. The complex first-slot convention causes
no problem: that slot is additive, and no scalar-conjugation shortcut occurs.

For the second theorem, the implementation derives a sum of one from the
first theorem and `hψ`. Every real square is nonnegative. The selected term is
therefore at most the finite sum, exactly as used by `Finset.single_le_sum`.
The conclusion is the closed interval `[0,1]`, not strict positivity. Thus
`p_i = ||M_i ψ||²` is a normalized finite probability family for unit inputs,
as a mathematical consequence; no packaged PMF or post-state is constructed.

The completeness identity is on the input space and composes `M_i` first,
then `M_i*`. It is not `sum_i M_i M_i* = I_F`. These orientations cannot be
swapped: the coordinate projection from `ℂ²` to `ℂ` is a coisometry but kills
the second unit basis vector, so output-side completeness would not imply
the asserted input-norm identity. Nor does the actual premise require
orthogonality, projections or individually isometric maps; two identical
copies of `I/sqrt(2)` already satisfy completeness in the endomorphism case.
These examples are mathematical discriminators, not executed finite tests.

## Degenerate and zero cases

- For `ψ = 0`, all weights are zero and the first theorem is `0 = 0`; the
  second theorem's unit norm cannot hold.
- If `E` is the zero space, every map out of it and `I_E` are zero. Any family,
  including the empty family, satisfies completeness; no unit input exists.
- If `ι` is empty, completeness is `0 = I_E` and forces `E` to be the zero
  space. There is neither an applicable unit input nor an outcome index.
- If `F` is the zero space, all `M_i` vanish; completeness again forces `E`
  to be the zero space. It does not permit loss of mass from a nonzero input.
- An individual outcome can have weight zero or one. The claims never divide
  by a probability, and they do not certify a normalized conditional output
  for a zero-probability branch.

The operator equation is a premise, not an existence theorem for arbitrary
chosen spaces or family sizes. Without `hψ`, total weight is `||ψ||²`, not
one. No nonempty probability distribution is falsely asserted on the empty
carrier.

## Bounded canonicality and ownership audit

Read-only searches were made over `R/QuantumBlockEncoding` and the same
directory in main commit `8d7ba4cd5b786706796df15777bcb5a5403723d0` and contribution
commit `ea0d8727f9d225f5af52e4bd5b62d02fe5d35cde`. Searches for measurement,
POVM/Kraus, the proposed theorem names and the adjoint quadratic identity did
not reveal an existing finite-family completeness implementation. Incidental
prose saying a construction has no measurement is not such a declaration.

Targeted searches of Mathlib's `Analysis/InnerProductSpace` and
`Analysis/CStarAlgebra` for measurement/POVM/Kraus, squared-norm sums, and
finite adjoint/star sums found the expected analytic substrate but no exact
general finite-family completeness-to-total-squared-norm theorem. The local
module directly reuses the existing adjoint API rather than defining parallel
operators or states. This is bounded retrieval, not ecosystem-wide
nonexistence or novelty evidence.

The existing `contrib/effect-probability-stability` branch resolves to
`0bf8979ab4600d458288aa2c19eb95b065e2799a`. Its `BornStability.lean` was read in
full; relevant `CircuitEffectStability.lean` declarations were searched. Its
finite-matrix effect probability has supplied positivity/order and unitary
premises and proves effect/Born stability and an effect `[0,1]` bound. Those
are prior, distinct results, not this formalizer's new contribution. The
present family-completeness theorem does not recreate that probability
definition or stability API. A future effect-measurement connection must
reuse it through a reviewed adapter rather than duplicate its semantics.

The first local lemma has a non-wrapper internal consumer in the second.
`W/measurement-intake-c399/Canary.lean` was inspected but not run: its
`normalized_total` and conjunction are interface smoke/repackaging consumers,
not a downstream source theorem or measurement construction. Genuine external
consumer closure and final purification are therefore not certified here.

## Required changes and retained boundaries

No core signature or proof change is required for the bounded semantic pass.
Any later source edit invalidates this binding. For stronger admission claims,
retain the exact source, formal packet and independent role bindings; exhibit
a genuine non-wrapper application or keep the preparatory-fragment label;
preserve prior-branch ownership; and keep the density/trace, state-update,
physical/circuit/resource and final purification boundaries visible. These
are not extra hypotheses to add to either theorem.

No implementation, build, Git write, production-tree edit, or subagent was
performed. Only this new output directory was written. Publication/TCB and
full integration remain NOT_EVALUATED by this actor. STOP after freeze.
