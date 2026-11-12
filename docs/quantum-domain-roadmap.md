# QuantumComputinglib long-term curriculum and shared Lean-graph roadmap

This document is a **curriculum and architecture plan**, not a second completion
ledger. The machine-readable source registry remains
`website/research/sources.json`; theorem publication/admission remains governed
by `website/research/publications.json`,
`docs/theorem-publication-protocol.md`, the Lean inventory, and the generated
Implementation Map. A planned chapter here is not a formalized theorem.

## 1. Four peer textbook parts, one shared foundation

QuantumComputinglib is organized as four peer textbook parts. Parts I and II
already contain compiled guided chapters; Parts III and IV are source-audited
curricula whose individual chapters remain planned until exact local Lean roots
exist. This status distinction is machine-readable in
`website/curriculum-parts.json`.

### Part I — State Preparation

Chapters 1–4 establish the shared finite-matrix/circuit conventions and then
specialize them to the state-preparation contract

`U |0ⁿ⟩ = |ψ⟩`

The shared chapters physically appear once. Block Encoding reuses the same
matrix, register, unitary and circuit-semantics nodes rather than receiving
parallel copies.

### Part II — Block Encoding

Chapters 5–9 build on those same foundations and study

`‖A − α Π U Π†‖ ≤ ε`

together with LCU/product/sparse/dilation routes, certified cases, resource
accounting and proof-gated search.

The relation between the two parts is **directional and typed**. The
curriculum/mechanism inclusion direction is **State Preparation → Block
Encoding**: State Preparation is a reusable preparation layer inside many
broader block-encoding constructions.

- **State Preparation → Block Encoding (the inclusion-like direction).** A
  verified preparation can supply a PREPARE component, but a complete block
  encoding also needs the matching SELECT/action, inverse or unprepare
  semantics, coefficient/phase convention, register layout and clean-block
  proof.
- **Block Encoding → State Preparation (a downstream consumer path, not the
  inclusion relation).** Applying a clean block to an input can create an
  unnormalized desired branch, but state preparation additionally needs a
  specified input, a nonzero accepted branch, normalization, success
  probability and, where efficiency is claimed, postselection/amplification
  cost.

This is the quantum analogue of a smaller theory/tool layer living inside a
broader construction theory while retaining its own certificate type.
Conceptual graph edges may show both transports; only named Lean theorems may
be shown as formal implication edges.

## 2. Part III — Quantum Information and Representation Theory

A future Quantum Information part will use Felix Leditzky's
[Representation-theoretic methods in quantum information theory](https://www.felixleditzky.info/teaching/FT25/math595-repth-qit.pdf)
as a principal curriculum anchor, while reusing external Lean libraries through
reviewed adapters rather than copying incompatible foundations.

The intended progression is:

1. finite-dimensional quantum states, density operators and measurements;
2. composite systems, partial trace, Schmidt decomposition, purification and
   entanglement;
3. state/channel distances and operational interpretations;
4. finite-group/unitary-group representation theory needed by QIT;
5. Schur–Weyl duality, Young diagrams/tableaux and the quantum method of types;
6. invariant families such as Werner/isotropic states;
7. de Finetti reductions and symmetry-based compression;
8. approximate cloning, spectrum estimation and weak Schur sampling;
9. advanced capacity, secret-key, entangled-game and quantum-optics routes;
10. channel counterexamples and representation-theory extensions.

The order is intentionally graph-driven: quantum states, tensor products,
partial trace, positive operators and channel semantics become **shared
foundation nodes** consumed both by QIT chapters and by later scientific
algorithms. Representation-theoretic nodes sit above that shared layer and are
not baked into the lower circuit model.

The pinned OpenAI Math audit contributes only scoped candidates here:

- `InformationTheory/Entanglement` and `Analysis/Quantum/PPTSquare` can inform
  the shared state/channel/Choi layer, but only declaration by declaration;
- `RepresentationTheory/Young`, `YoungSymmetry` and `FiniteUnitary` are
  candidate prerequisites after manuscript-specific namespaces are purified;
- Saxl and Foulkes--Howe belong to an advanced extension, not the core
  Schur--Weyl dependency chain;
- `InformationTheory/DimensionTen`, PhotonNumber, SecretKey and EntangledGames
  are downstream consumers and must not dictate the foundational API.

`OAI.Analysis.Naimark` is explicitly excluded from the measurement chapter: it
formalizes the C*-algebra Naimark problem, not POVM dilation.

## 3. Part IV — Quantum Algorithms for Scientific Computation

A second long-term anchor is Lin Lin and Nathan Wiebe,
[Quantum Algorithms for Scientific Computation, 29 April 2026 edition](https://math.berkeley.edu/~linlin/qasc/live_notes_0429.pdf).

The user-supplied copy of this edition is not vendored into the repository:
the same titled and dated 447-page edition is publicly hosted by the authors, so
the source registry stores the public reference instead of introducing a large
binary snapshot. If a future required appendix/edition is not publicly
available, it may be stored under a source-evidence path with provenance and
license/reuse review; it must not silently become proof memory.

The supplied 447-page copy exposes four source parts and 21 chapters. The
formalization map should preserve that source organization while deduplicating
objects that QuantumComputinglib already owns:

| Source part | Source chapters | QuantumComputinglib treatment |
| --- | --- | --- |
| **Part I · Background** | Ch. 1 quantum advantage; Ch. 2 elements of quantum computation, including density operators and circuits | reuse/extend the shared quantum-object and circuit foundations; no second ket/unitary/register API |
| **Part II · Foundation** | Ch. 3 probability, quantum channels and distances; Ch. 4 universality; Ch. 5 reversible classical processing; Ch. 6 query complexity; Ch. 7 perturbation theory; Ch. 8 statistical estimates | build the shared QIT/scientific-computing substrate, preferably through existing Mathlib/external quantum-Lean adapters |
| **Part III · Algorithm** | Ch. 9 block encoding; Ch. 10 qubitization; Ch. 11 amplitude amplification; Ch. 12 QSP; Ch. 13 QSVT; Ch. 14–15 Hamiltonian simulation; Ch. 16 QPE/Fourier/amplitude estimation | map Ch. 9 onto the existing Block Encoding part; add only the genuinely new transforms above it |
| **Part IV · Application** | Ch. 17 quantum walks; Ch. 18 eigenvalue/ground-state problems; Ch. 19 linear systems; Ch. 20 linear differential equations; Ch. 21 open quantum systems | consume the common graph and expose full input/query/success/output-cost contracts rather than application-local copies |

Block Encoding is therefore not duplicated as a later textbook chapter. The
scientific-computing part points back to the existing certified Block Encoding
nodes and adds only genuinely new transforms and application theorems. The same
deduplication applies to Ch. 2–3 objects that will also be consumed by the
Leditzky QIT route.

The pinned OpenAI Math tree adds three carefully bounded extensions:

- `Computability/FourierCircuit` supplies a Comparator-backed exact Fourier
  circuit/resource theorem to the Fourier and phase-estimation chapter after a
  circuit-model adapter; it does not close QPE itself;
- `Computability/QuantumFactoring` is a source of compiler and resource
  patterns for an extended synthesis chapter, not a core prerequisite;
- `Analysis/Laughlin` is placed in an extended many-body-model chapter as
  mathematical substrate, never as a claimed quantum simulation result.

The Walsh-series and space--time--accuracy diagonal-operator papers remain
respectively in Part I and Parts I--II. Their placement cards expose the phase
supplier, accepted branch, finite-precision and success-cost obligations; no
paper citation is promoted into a compiled theorem.

## 4. One graph, minimal duplicated nodes

The target architecture is a single shared proof graph.

```text
L0  finite linear algebra / finite sums / norms / permutations
      ↓
L1  quantum objects
    normalized vectors · density operators · tensor systems · projectors
    partial trace · isometries · unitaries · positive operators
      ↓
L2  operational semantics
    measurements · channels · circuits · registers · classical reversible maps
    oracle/query contracts · resource/cost records
      ↓
L3  construction interfaces
    state preparation · PREPARE/SELECT · block encoding · LCU · sparse access
    dilation · amplification
      ↓
L4  transforms / algorithms
    QSP · QSVT · qubitization · Hamiltonian simulation · phase estimation
    symmetry / Schur-Weyl transforms
      ↓
L5  scientific and information-theoretic applications
```

A new theorem should reuse the lowest compatible node. A domain chapter must
not introduce its own second definition of a density matrix, partial trace,
unitary circuit, trace distance, query oracle or block encoding merely because
the source textbook uses different notation.

### Node-reuse gate

Before adding a foundational declaration:

1. search ASPBE/QuantumComputinglib;
2. search Mathlib under the pinned toolchain;
3. search the attributed quantum Lean references;
4. if an external result is suitable, write a **narrow adapter contract** and
   preserve its source/toolchain/license boundary;
5. only then add a new local node, with a written reason why reuse/adaptation
   was insufficient.

The goal is not literally the fewest declarations. It is the fewest
**semantically duplicated** nodes consistent with readable APIs, stable
toolchains and proof locality.

## 5. External quantum Lean references in the bigger picture

These projects are references or adapter candidates; the label is not a claim
that ASPBE imports or owns their theorems.

| Upstream | Planned use in the shared graph | Boundary |
| --- | --- | --- |
| [duckki/quantum-computing-lean](https://github.com/duckki/quantum-computing-lean) | finite states, gates, projectors, small circuit identities and organizational patterns | reference atlas unless an explicit adapter is compiled |
| [Timeroot/Lean-QuantumInfo](https://github.com/Timeroot/Lean-QuantumInfo) | finite-dimensional quantum/classical information, channels, distributions, entropy/capacity APIs | reference/adapter candidate; local theorem claims require a checked boundary |
| [Hayata-Yamasaki-Group/lean-quantum](https://github.com/Hayata-Yamasaki-Group/lean-quantum) | states, qudits, channels, partial trace, entropy, trace inequalities and operator conventions | reference/adapter candidate; do not duplicate higher-level QIT foundations without an audit |
| [QudeLeap/Lean-QuantumAlg-Bench](https://github.com/QudeLeap/Lean-QuantumAlg-Bench) | benchmark statements for quantum algorithms | benchmark targets are not proof memory |
| [QuAIR/Lean-QIT-Bench](https://github.com/QuAIR/Lean-QIT-Bench) | benchmark statements for quantum information | unresolved statements remain tests/targets, not certified upstream lemmas |
| ATLAS v1 / Mathlib | general algebra, matrix analysis, probability and analysis leaves | preserve their existing license/toolchain/admission rules |

For each external library we prefer a small compatibility layer over wholesale
API duplication. Toolchain mismatch is an explicit frontier, never hidden by
copy-pasting theorem statements.

## 6. Protocol for adding a future textbook section

Every future section must move through the same gates as current ASPBE work.

1. **Source freeze.** Pin edition/version, exact statement/definition anchors,
   notation and any referenced prerequisites.
2. **Mechanism placement.** Identify which existing graph nodes are reused and
   which new node/hyperedge is genuinely needed.
3. **Mathematical authoring.** Give the natural-language statement, equations,
   proof and hidden assumptions once.
4. **Lean formalization.** Add or adapt only the required declarations.
5. **Encoder–denoiser review.** Run the source-blind reconstruction and a
   distinct anti-anchored reviewer as required by the publication protocol.
6. **Truth-layer update.** Update conceptual graph, actual module/import graph,
   and theorem-dependency evidence without turning conceptual relations into
   Lean implications.
7. **Reader publication.** Only after the required Lean/integration/site gates
   pass may a planned item become a positive theorem card.

For new quantum-information material the semantic checklist additionally
includes positivity/complete positivity, subsystem order, partial traces,
normalization, support conditions and metric conventions. For scientific
algorithms it additionally includes input-state cost, query model, precision,
success probability, output/readout cost and the distinction between
mathematical oracle complexity and an explicit gate implementation.

## 7. Immediate next steps

The September source/frontier admission is recorded in
[the state-preparation audit](state-preparation-frontier-audit-20260929.md).
It adds the Walsh Series Loader and diagonal space–time–accuracy papers to the
planned queue, with shared phase/accepted-branch mechanisms, not a duplicate
foundation. The canonical cards and routes remain in the research JSON.
The Leditzky public PDF currently carries a 10 April 2026 edition date; FT25
in its URL is not the edition date. These additions are not source-root closure.

The near-term order is deliberately conservative:

1. publish all four peer parts in the teaching surface while marking Parts III
   and IV, and the Walsh/diagonal additions, as planned rather than compiled;
2. finish source-faithful Vandaele comparator/adder formalization before using
   its arithmetic circuits as generic memory;
3. build the QIT shared foundations that are simultaneously useful to
   Leditzky's notes and Lin–Wiebe (density operators, channels, distances,
   subsystem operations), preferring reviewed external adapters;
4. let the Lin–Wiebe scientific-computing route reuse current block-encoding
   nodes instead of re-formalizing Chapter 9 under a second API;
5. only after those shared interfaces stabilize, expand into
   representation-theoretic QIT and later scientific-application chapters.
