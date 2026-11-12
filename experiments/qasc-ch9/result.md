# Bounded result and integration handoff

Status: **PROVED_LOCAL (staging)**. No production/publication or canonical
completion ledger changed. Independent decoder, source reviewer, topology
review, repository aggregate gates, publication and Exposition Seal pending.

## Certified delta

Namespace `QuantumBlockEncoding.QASCChapter9` in `ExactConsumer.lean`:

| Source obligation | Checked declaration |
| --- | --- |
| (9.12) superposition extends basis block entries to arbitrary b | cleanOutput_eq_blockAction |
| (9.2),(9.9) exact clean action with real scale alpha | scaled_cleanOutput |
| (9.10) accepted Born weight is image weight / alpha squared | exact_weight |
| Meaningful successful branch iff Ab is nonzero | positive_weight_iff |
| Positive alpha cancels in conditional normalized output | normalized_cleanOutput |
| Explicit normalized coordinates have weight exactly one | normalized_vector_weight |
| Qubit-dimensional, zero-ancilla-sector source consumer | exactConsumer |

The actual algebra: expand the clean input as a superposition of the existing
clean basis kets. Matrix-vector linearity selects each clean matrix entry, so
the clean output is B b. The exact block assumption A=alpha B gives
alpha c=A b. Taking complex normSq coordinatewise and summing gives
alpha^2 weight(c)=weight(A b). Each summand is nonnegative and vanishes exactly
at a zero coordinate, so success is positive exactly for Ab!=0. Positive-alpha
square-root scaling gives sqrt(weight(Ab))=alpha sqrt(weight(c)); cancelling
alpha proves equality of the two normalized vectors. Separately their weight
is one because the common nonzero denominator squared is the image weight.

The full orthogonal residual-vector decomposition (9.3), expectation-value
form of (9.4)/(9.10), probability upper bound, physical measurement instrument,
operator-norm approximation Definition9.2, Exercise9.1, Example9.1 circuit,
LCU/addition/multiplication/sparse/Hermitian/general-basis constructions and
all query/gate/finite-bit/amplification/readout costs remain unproved here.
This is not full section or chapter closure.

## Evidence binding

- Source id: lin-wiebe-2026-qasc; printed date 29 April 2026; 447 pages.
- Primary URL: https://math.berkeley.edu/~linlin/qasc/live_notes_0429.pdf
- Source SHA256: `56825000d53025dea4c2998dd6a061592b8fb2b9a446c3194c5f408183327599`.
- Relevant complete rendered pages visually inspected: printed141,142,143,37.
- Lean source SHA256: `cc07aed9366c36ff665e5d52d9d0b97baab399a90fcc7e681884d4a9d984e412`.
- Statement signature SHA256: `5dc1f10a7727f21feec727bbb3b30f12ff30477e7de15aa59fced87387cf37a4`.
- lean-toolchain: leanprover/lean4:v4.33.0; SHA256
  `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b`.
- lake-manifest.json SHA256:
  `510171e8214a2ac5e00f16c1bf92ad474d2de42c4cd2dc2b3d411272f7b58763`.
- Actual focused gate: `lake env lean experiments/qasc-ch9/ExactConsumer.lean`,
  final completed exit0. Imported checkout warning: Verso has local changes;
  no dependency edits by this worker.
- `#print axioms exactConsumer` and `#print axioms normalized_vector_weight`:
  exactly propext, Classical.choice, Quot.sound. No sorryAx.
- No sorry/admit/unsafe/new axiom in this module.
- Four checked examples: zero target gives impossible positive success;
  empty algebraic system has zero accepted weight; identity preserves imaginary
  amplitudes; source root at m=n=0 identity with normalized input gives positive
  success. Examples use the same compiler gate, not a numerical simulator.
- PDF/render caches are ignored by the directory-owned .gitignore, verified
  with git check-ignore. They are local source-inspection aids, not deliverables.

## Trust, assumptions and four graph views

Binder audit: source exact-block and positive-alpha assumptions, source unitary
matrix, standing normalized input, typing dimensions/scalars; EXCESS none.
Expanded physical interpretation assumptions are not hidden inside generic
candidate Prop fields. Unitarity and input normalization are unnecessary for the
stronger algebraic provider conclusions; their presence in the source root
does not by itself certify a measurement process or probability upper bound.
No public nonzero-branch premise was added: the criterion is proved and
normalization is conditional inside the conclusion.

Source graph: source-topology.md; complete AND route preserved, construction
providers remain OR alternatives, implicit nonzero validity/source gaps exposed.
Lean dependency graph: existing shared finite coordinates + Mathlib linearity,
complex normSq and real square-root facts + new consumer providers. Module
imports are not advertised as elaborated per-theorem dependency extraction.
Compressed spine: shared BE clean projection -> arbitrary-state action ->
postselection weight/nonzero boundary -> conditional normalization.
Functor hypergraph: BE + prepared normalized input + nonzero image supports
conditional output preparation; amplification and all costs remain boundary
nodes. This is not a categorical functor certificate or automatic synthesis.

## Worker handoff fields

- Objective/frontier: bounded shared Chapter9 exact BE consumer.
- Failure class: NONE for final sealed target. A few compilation iterations
  were implementation/API corrections, not mathematical counterexamples.
- Salvage: all successful providers are reachable from source root or its
  explicit normalization interpretation; no abandoned proof declaration.
- Process-memory consulted: QBE-PM-LOW-TOKEN-CONTROL-PLANE; no entry supplies
  a mathematical premise.
- Fingerprint: scientific-textbook-shared-BE-consumer.
- Expected information gain: establish exact source-to-existing-BE consumer
  reuse without a second scientific-computing foundational API.
- Parallel admission: assigned independent of state/channel and stored-SO
  workers by root; no subagents spawned here. Common-blind-spot review pending
  if multiple serious routes to this same anchor are later compared.
- Default verified route: direct shared finite clean block + superposition;
  small, exact, phase-preserving. Factored-inner-product/construction suppliers
  are alternatives, not duplicate downstream proofs.
- Purification: staged local dead-code/import/duplicate audit completed;
  reader-facing PURIFIED and independent Exposition Seal not asserted.
- Recommended merge: review this complete directory packet, promote only the
  exact consumer and internal providers if useful; do not vendor PDF/renders.
  Root owns integration and full lake build/Tests/site gates.
- Next dependency-ready objective: accepted-sector probability upper bound from
  standard unitarity and input normalization, followed by a separately sealed
  genuine operator-norm approximation consumer. Neither is silently included.
