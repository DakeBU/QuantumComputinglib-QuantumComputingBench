# OpenAI Math quantum-curriculum reconciliation

Date: 2026-10-07

Local target toolchain: Lean 4.33.0

Audited upstream: [openai/math at the fixed snapshot](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a)

## Executive conclusion

Commit `c681192368c2fed4e055928480cefe8544cf30f1` established the correct
proof-digestion, encoder--denoiser and Functor-Hypergraph boundary, but its first
intake did not exhaust the fixed upstream tree. The missing high-value material
is not another state-preparation or block-encoding foundation. It is a set of
scoped suppliers and advanced consumers for the new Quantum Information /
Representation Theory and Quantum Algorithms for Scientific Computation parts.

The most important additions are the exact Fourier-circuit resource route,
PPT-square and DimensionTen companion channel constructions, Young/Specht and
finite-unitary representation infrastructure, the advanced Saxl and
Foulkes--Howe routes, and the Laughlin mathematical-physics target. None is a
local theorem until a named declaration is adapted and compiled under Lean
4.33.0.

## Evidence and method

The audit used the complete Git tree at the pinned commit and then inspected
the relevant source subtrees, exact Comparator configurations and
`lean/formalization.yaml`. It did not infer coverage from the repository README
or from directory names alone.

The [formalization map](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/formalization.yaml)
and [upstream toolchain](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/lean-toolchain)
are pinned evidence. Comparator-backed means a matching upstream configuration
was found; it does not report a local rerun of that comparator or establish
that every supporting declaration is reusable. The tree-level candidate scan
is not an exhaustive semantic audit of every upstream proof body.

Machine-readable evidence lives in:

- `research-wiki/openai-math-2026-intake.json`: path, tree SHA, verification
  status, curriculum consumers and hard guards;
- `website/curriculum-parts.json`: the four peer textbook parts and chapter
  placement;
- `docs/openai-math-assimilation-protocol.md`: admission and toolchain rules.

## Reconciliation table

| Upstream cluster | What it actually supplies | Placement | Admission decision |
| --- | --- | --- | --- |
| `Computability/FourierCircuit` | Exact Fourier circuit plus a stated resource model | Part IV Fourier/QPE; Part II supplier extension | Source route after circuit/cost adapter |
| `Analysis/Quantum/PPTSquare` | CP/PPT/TP/entanglement-breaking and explicit channel geometry | Part III channels and counterexamples | Adapter-backed; not a foundational API |
| `InformationTheory/DimensionTen` | Density-state, entanglement, Choi-transfer and readout/key companion construction | Part III secret-key/entanglement extension | Downstream source route |
| `RepresentationTheory/{Young,YoungSymmetry,FiniteUnitary}` | Young/Specht and finite-unitary ingredients | Part III representation foundations and Schur--Weyl | Declaration-level admission after namespace purification |
| `RepresentationTheory/Saxl` | Advanced symmetric-group/Specht route | Part III extended representation theory | Comparator-backed source route, not prerequisite |
| `RepresentationTheory/FoulkesHowe` | Advanced plethysm route | Part III extended representation theory | Comparator-backed source route, not prerequisite |
| `Analysis/Laughlin` | Many-body mathematical target | Part IV extended models | Comparator-backed source route, not an algorithm claim |

## Explicit non-match

`OAI.Analysis.Naimark` is about the C*-algebra Naimark problem. It is not a
formalization of Naimark dilation for quantum measurements. The shared QIT
measurement chapter must not retrieve it merely because the names coincide.

Likewise, a preprint title containing “quantum”, “many-body” or field-theory
terminology does not imply a quantum-algorithm contract. Such items remain out
of the core curriculum unless an exact theorem, semantic consumer and
verification status are identified.

## Toolchain result

The pinned upstream snapshot declares Lean 4.34.1; QuantumComputinglib is
locked to Lean 4.33.0. Direct package import is therefore rejected for this
snapshot. The safe route is source mining followed by a narrow local adapter or
port, compiled and tested under 4.33.0. This is intentionally stricter than
copying a statement into proof memory.

## Curriculum consequences

State Preparation and Block Encoding remain Parts I and II. Walsh-series state
preparation and space--time--accuracy diagonal operators are planned chapters
inside those parts, not separate foundations. Representation Theory/QIT and
Quantum Algorithms for Scientific Computation become Parts III and IV at the
same navigation level, with honest planned status.

The Functor Hypergraph should share the lowest compatible objects--finite
linear algebra, states, channels, measurements, tensor order, circuits and
resource records--while keeping these relations distinct:

1. compiled local Lean dependencies;
2. locally proved semantic adapters;
3. source correspondences;
4. conceptual curriculum bridges.

This audit changes retrieval and chapter placement. It does not claim any new
local mathematical closure.
