# OpenAI Math assimilation protocol for QuantumComputinglib / ASPBE

Status: active intake protocol, 2026-10-07.

This protocol governs how results from `openai/math` enter the
QuantumComputinglib / ASPBE Lean graph. It supplements the existing source
fidelity, statement seal, semantic reconstruction, proof-DAG, purification, and
publication requirements.

## 1. Pinned upstream

Reviewed snapshot:

- repository: `openai/math`;
- commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`;
- release date: 2026-10-06;
- upstream formalization license: Apache-2.0.

Never depend on a floating `main` when making a mathematical claim. Every
promoted item records upstream commit + path + relevant SHA + source/preprint
anchor + attribution.

The default relation to OpenAI Math is **audited source/adaptor input**, not
automatic package dependency.

## 2. Admission classes

Each upstream cluster or declaration receives exactly one initial class:

- `canonical-leaf`: a definition-independent linear algebra / matrix / finite
  probability / circuit fact that should become a shared local primitive;
- `adapter-backed`: valuable theorem family whose state/channel/circuit model
  differs from ASPBE and therefore needs a semantic adapter;
- `source-route`: source-specific theorem family exposed as a new quantum
  computing / information route;
- `benchmark-only`: useful formal benchmark or comparison target, not a local
  proof claim;
- `out-of-scope`: similarity is lexical or too remote to justify graph growth.

Default: `benchmark-only`.

## 3. Foundational anti-duplication rule

Before adding any quantum state, density operator, channel, Kraus map, POVM,
measurement, trace norm, partial trace, tensor-system, unitary/circuit, or
query-complexity definition:

1. search existing `QuantumBlockEncoding/`;
2. search Mathlib;
3. search the already-audited external quantum Lean libraries named in
   `AGENTS.md`;
4. inspect the OpenAI definition;
5. choose one canonical local object and write the smallest adapter.

Do not create a second quantum foundation merely because an OpenAI theorem is
conveniently stated in a matrix model.

A successful adapter must state what it preserves: positivity, trace,
unitarity, composition order, tensor ordering, Born probabilities, support,
depth, ancilla convention, or other relevant semantics.

## 4. Mandatory semantic round trip

For every source-facing OpenAI result, preserve separately:

1. source/preprint statement;
2. exact upstream Lean statement;
3. proposed local statement;
4. source-blind reconstruction of the local statement;
5. independent anti-anchored comparison.

Audit at least:

- finite index types / basis convention;
- little- versus big-endian bit order where applicable;
- matrix multiplication / chronological gate order;
- global phase and exact versus approximate equality;
- input ancilla initialization;
- clean versus garbage output registers;
- projective versus general POVM measurement;
- postselection or conditioning;
- gate set and arity;
- support disjointness and depth accounting;
- error norm/probability;
- asymptotic size, depth, and ancilla quantifiers.

The invariant remains: a proof ingredient is a dependency edge; it cannot be
turned into an extra source-facing hypothesis.

## 5. Priority A: quantum circuits and parity

First intake cluster:
`lean/OAI/InformationTheory/QuantumCircuit`, upstream tree SHA
`44b141f8943100e08320bea56569203443e40d5d`.

This cluster is especially valuable because it spans both physical circuit
semantics and a nontrivial lower-bound proof. It should be split into layers
rather than copied as one namespace.

### 5.1 Semantic layer

The upstream model uses:

- `Word N = Fin N -> Fin 2`;
- matrix operators in the computational basis;
- single-qubit local unitaries;
- unbounded-arity Toffoli gates;
- physical layers with pairwise-disjoint gate supports;
- chronological circuit matrices;
- zero-initialized non-input qubits;
- a measured output bit with all final garbage summed out.

Before reuse, map these to:

- `QuantumBlockEncoding/Circuit.lean`;
- `CircuitSemantics.lean`;
- `ConcreteSemantics.lean`;
- `PrimitiveCircuit.lean` and `PrimitiveSemantics.lean`;
- `ReversibleClassical.lean`;
- existing resource/depth declarations.

No parity result may be ported until the Born-probability and gate-composition
adapter is explicit.

### 5.2 Physical-to-abstract bridge

The upstream `Physical.lean` proves a particularly useful style of bridge:
local gates and Toffoli gates are normalized into an abstract reflection/local
circuit representation while preserving supports and depth. Treat this as a
candidate pattern for ASPBE's own “printed/physical circuit -> semantic
operator -> resource certificate” chain.

Port the **mechanism**, not necessarily the upstream intermediate type. If the
local circuit representation can express the same theorem more canonically,
prove an adapter theorem there.

### 5.3 Lower-bound route

The source-facing endpoint is a constant-depth, polynomial-total-qubit parity
lower bound: eventually, every such measured-output physical circuit has an
input on which success is below the target threshold.

This belongs in a **circuit complexity / lower bounds** branch. It is not
evidence that ASPBE synthesized a block encoding or state preparation, and it
must not change existing ASPBE success badges.

Build its Source Proof Graph around:

- Pauli / product-state expansions;
- degree and low-degree propagation;
- regularity and retained mass/mean;
- localization/pruning;
- approximation budgets;
- physical-circuit normalization;
- measured-output parity conclusion.

## 6. Priority B: quantum channel and information primitives

### 6.1 Generalized amplitude damping

Cluster:
`OAI/InformationTheory/AmplitudeDamping`, tree SHA
`bc0bdc6cc56981a86a465da8c75d1fb003bd29cf`.

High-value ingredients include:

- finite density/state predicates;
- Kraus operators and tensor-product channels;
- spectral/von-Neumann entropy interfaces;
- Holevo information;
- Naimark-style measurement tools;
- pinching and typical-projector arguments;
- coding achievability/converse;
- operational capacity;
- explicit phase-product ensembles.

The source-specific endpoint identifies the operational unassisted classical
capacity with the one-shot Holevo quantity for the channel and proves the
associated additivity/attainment statements.

This is a new **quantum information** route, not part of the core block-encoding
claim. Shared primitives should be canonicalized only when they also help
state-preparation, block encoding, quantum algorithms, or a second QIT route.

### 6.2 Entanglement infrastructure

Cluster:
`OAI/InformationTheory/Entanglement`, tree SHA
`6f9299728d0056a72fe68755c3bac32237776203`.

This is a large foundational graph containing, among other things, trace norms,
matrix measures, completely-positive/instrument/channel interfaces, Choi
transfer, fidelity, POVMs, purification, tensor constructions, conditioning,
and adaptive/causal protocol semantics.

It must **not** be bulk-copied. Intake is declaration-by-declaration:

1. identify a real local consumer;
2. compare with local/Mathlib/external-QIT definitions;
3. select the canonical representation;
4. prove adapter/equivalence;
5. only then port downstream theorems.

This cluster is a strong candidate source for a future canonical QIT spine if
the audit shows it reduces duplication across several routes.

## 7. Priority C: photon-number, secret-key, and classical-information routes

### PhotonNumber

`OAI/InformationTheory/PhotonNumber` (tree SHA
`563feea512b18ed1fa7b0214654aa4f6ebb1ef9a`) supplies a coherent quantum-optics
route: Fock/number basis, entropy, Gibbs/thermal states, beam operations,
continuity, finite-energy approximations, and entropy photon-number inequalities.
Treat as a later QIT/quantum-optics textbook branch.

### SecretKey

`OAI/InformationTheory/SecretKey` (tree SHA
`8c5dee25a15f569311261890e18643c15a392d89`) includes CP/PPT maps,
purification, Choi transfer, key-rate and explicit zero-key constructions. It is
advanced QIT and should enter only after the foundational state/channel/trace
adapters are stable.

### SoftChannel and BooleanNoise

`OAI/InformationTheory/SoftChannel` (tree SHA
`c7f7510180d65e41f89381b748205e60cb423039`) and Boolean-noise results are
primarily classical information theory. They are useful shared mathematical
substrates for entropy/noise contraction and can also be consumed by BanditRLlib.
Do not label them quantum merely because they live under InformationTheory.

## 8. Other quantum OpenAI results

Preprints/results such as exact factoring over a fixed finite gate set,
randomized-versus-quantum query separations, entangled games, and other quantum
information results are `benchmark-only` until a precise Lean cluster,
statement boundary, and local consumer have been audited.

“Interesting for quantum computing” is not sufficient for a solid graph edge.

## 9. Graph design

Use four visibly different relations:

- solid local Lean dependency: local compiler-checked theorem dependency;
- adapter edge: locally proved semantic correspondence;
- source correspondence: theorem-to-paper identity;
- dashed conceptual bridge: mathematical mechanism without formal implication.

Candidate conceptual families from this intake:

- `family:physical-circuit-to-operator`;
- `family:circuit-normalization-and-pruning`;
- `family:low-degree-propagation-lower-bound`;
- `family:kraus-channel-semantics`;
- `family:operational-capacity-via-information`;
- `family:trace-distance-contractivity`;
- `family:purification-and-measurement-dilation`.

Keep full AND tails and OR routes. Imports are not theorem implications.

## 10. Cross-library ownership

For quantum-bandit or quantum-RL work, ASPBE/QuantumComputinglib owns the quantum
semantics. BanditRLlib should consume a reviewed adapter/certificate rather than
redefine states, channels, or measurements.

Conversely, classical online-decision machinery belongs in BanditRLlib even if a
quantum application consumes it.

Samplinglib may share generic matrix/probability lemmas only through a genuinely
source-independent canonical leaf, not by importing a quantum source route.

## 11. CI and publication gate

Before an OpenAI-derived item is promoted from candidate to local truth, require:

- pinned upstream commit/path/SHA and attribution;
- exact source/preprint anchor;
- exact upstream theorem/definition seal;
- local semantic map;
- explicit convention audit;
- Mathlib/local/external-library reuse search;
- local Lean build/test evidence;
- no `sorry`/axiom/fake-wrapper closure;
- source-blind reconstruction;
- independent source review;
- graph delta;
- reader-facing source / natural-language / Lean correspondence;
- purification pass eliminating duplicate definitions and wrapper-only clutter.

A source theorem may remain a valuable graph node even when its local port is
blocked; mark the obstruction honestly.

## 12. Upstream updates

Advance the OpenAI commit pin only through a reviewed diff. For each already
admitted closure, classify upstream changes as semantic, proof-only,
organizational, or deleted. Semantic changes re-open the local statement and
adapter audit before publication status can remain green.

## Upstream verification-status gate

OpenAI Math contains manuscripts at different verification stages. A directory
under `lean/OAI` is not by itself a formalization-status claim. Before
promotion, inspect `lean/formalization.yaml`, the Comparator config/challenge
when present, and the exact solution declaration.

At the pinned snapshot, the shallow-circuit parity endpoint is comparator-backed
as `OAI.QAC.parity_lower_bound_polynomial_size` through
`ComparatorChallenges/RegularParity.json`; the generalized-amplitude-damping
endpoint is comparator-backed as `OAI.GAD.main`. Other QIT subtrees still need
declaration-level status recording before we present them as source-complete.

## Additional audited quantum-computing routes

The catalog sweep promotes the following from generic “other quantum results” to
named routes:

- `OAI/Computability/QuantumFactoring`: comparator-backed exact quantum
  factoring. This is a very large end-to-end route covering arithmetic,
  reversible/quantum circuit construction, compiler/emission semantics, oracle
  use, algorithmic control flow, and resource bounds. It is Priority A because
  its compiler and circuit-resource spine can share directly with ASPBE. Mine
  shared primitives first; do not copy the 500+ file closure wholesale.
- `OAI/Probability/EntangledGames`: comparator-backed threshold parallel
  repetition for finite-dimensional entangled games. It is a valuable consumer
  of state, measurement, purification, entropy, resampling and correlated
  sampling APIs, but requires canonical QIT adapters before reuse.
- `OAI/Analysis/Quantum/DimensionTen`: comparator-backed quantum-channel
  existence/geometry route.
- `OAI/InformationTheory/PhotonNumber`: its entropy photon-number endpoint is
  comparator-backed and should anchor the quantum-optics/entropy route.

Two October 5 results—randomized-versus-quantum query separation and
Boolean-oracle unitary synthesis—are recorded as benchmark/manuscript routes in
the current audit. They are mathematically central to a future quantum-query and
synthesis textbook branch, but must not be labelled locally formalized until an
exact OpenAI formalization/comparator mapping is established.

This changes the recommended first-wave order to:
`QuantumCircuit -> QuantumFactoring -> AmplitudeDamping -> foundational QIT
adapters -> EntangledGames/PhotonNumber`.

## Full-tree reconciliation for the quantum curriculum

The 2026-10-07 reconciliation inspects the complete tree at the pinned commit,
not only paths already named by the first intake. It adds these scoped routes to
`research-wiki/openai-math-2026-intake.json`:

- `Computability/FourierCircuit`: a Comparator-backed exact Fourier-circuit and
  resource route for the scientific-computing Fourier/QPE chapter. It is a
  possible circuit supplier, not by itself a QPE, state-preparation or
  block-encoding certificate.
- `Analysis/Quantum/PPTSquare` and the companion
  `InformationTheory/DimensionTen`: advanced channel, entanglement-breaking,
  Choi and secret-key consumers for the QIT extended chapters. They sit above a
  canonical state/channel adapter layer.
- the scoped `RepresentationTheory/Young`, `YoungSymmetry` and `FiniteUnitary`
  subtrees: candidate ingredients for representation theory and Schur--Weyl.
  Manuscript-specific namespaces and assumptions must be purified first.
- the Comparator-backed `Saxl` and `FoulkesHowe` routes: advanced representation
  theory extensions, not prerequisites of the basic QIT spine.
- `Analysis/Laughlin`: a Comparator-backed mathematical-physics target for an
  extended many-body-model chapter, not a quantum-algorithm certificate.

The same reconciliation records a lexical rejection: `OAI.Analysis.Naimark`
concerns the C*-algebra Naimark problem, not Naimark dilation of POVMs. It
therefore creates no measurement-theory edge.

### Exact toolchain boundary

The pinned OpenAI Math snapshot declares `leanprover/lean4:v4.34.1`; this
project declares `leanprover/lean4:v4.33.0`. OpenAI Math therefore remains a
pinned source/adapter corpus and is not a direct Lake dependency. A result may
enter local proof memory only after its exact declaration has been ported or
adapted and compiled under local Lean 4.33.0. The intake JSON and tests enforce
this boundary.

### Textbook placement is not theorem admission

Every admitted intake cluster names one or more curriculum consumers. Placement
gives agents a retrieval address and helps the Functor Hypergraph avoid
duplicated foundations; it does not create a solid Lean edge. The four peer
textbook parts are defined in `website/curriculum-parts.json`, which separates
compiled chapters, partial routes and planned/extended chapters.

