# State-preparation frontier and textbook admission audit

Audit date: 29 September 2026. Baseline: `ab8f277c5704b7831c7a5b5ecddce61c760b4ac8`.
This is a source/organization audit and formalization plan, **not a new Lean
certificate, a novelty claim, or a report of improved preparation complexity**.

## Live wiki: coverage, not completion

The live index, its published canonical JSON and all nine route pages returned
HTTP 200 during this audit. Every route page exposed its acceptance tests and
same-model comparison key. The eight requested frontiers plus the envelope
proposal were already present; they should not be duplicated as new chapters.

| Requested frontier | Existing stable route | Essential boundary already visible |
| --- | --- | --- |
| High-dimensional structured functions | `spw-structured` | Rank, coefficient supply, phase and normalization; tensor products can be exponential in dimension |
| Loading without free QRAM | `spw-no-qram` | Build, query, update and readout costs |
| Coherent parameter families | `spw-controlled` | One joint supplier, relative phases and uniform error |
| Ground states | `spw-ground` | Charged trial state, overlap and gap; no generic removal of these barriers |
| Low-temperature Gibbs states | `spw-gibbs` | Stationarity is not a quantitative mixing theorem |
| Fault-tolerant resources | `spw-fault-tolerant` | Finite-bit angle generation, T/Toffoli, depth, workspace and connectivity |
| Preparation with verification | `spw-verification` | Ideal-circuit proof is not hardware fidelity or a statistical guarantee |
| CV–DV/non-Gaussian preparation | `spw-cvdv` | Embedding, energy/cutoff/grid errors and distinct CV/DV resource models |
| Envelope/reference preconditioning | `spw-envelope` | Support domination, constructible reference and ratio, success/amplification |

The missing material was a source-specific Walsh/diagonal teaching and retrieval
path. New routes `spw-walsh` and `spw-diagonal` fill that organizational gap.
They remain research targets, with neither advertised source root formalized.
The existing hardware candidate `2609.08414` is not reverified by this audit;
its unavailable-primary-source classification remains unchanged.

## How the new textbooks fit

[Leditzky's notes](https://www.felixleditzky.info/teaching/FT25/math595-repth-qit.pdf)
currently identify themselves as the **10 April 2026, 79-page edition**, despite
the FT25 URL. The stable source ID is retained, but its edition/year is corrected.
The relevant foundation is states/measurements/composites/distances before
representation theory, Schur–Weyl and symmetry applications. This supports
shared normalization, subsystem and error conventions; it is not a separate
state-preparation algorithm library. The edition/contents and foundation map
were checked here, not every theorem in all chapters.

[Lin–Wiebe](https://math.berkeley.edu/~linlin/qasc/live_notes_0429.pdf), 29 April
2026, 447 pages, supplies the complementary scientific-algorithm stack. Chapter
9's Definition 9.2 and Eqs. (9.9)–(9.11) explain precisely why a block encoding
is not yet a cheaply prepared normalized state. Chapters 11 and 13 supply
amplification/transformation prerequisites; Chapters 18–21 consume those
interfaces for ground states, linear systems and dynamics. The contents and
relevant block/success/ground-state passages were checked, not all 447 pages.

Keep one shared finite-matrix/state/register layer, as specified in
[the domain roadmap](quantum-domain-roadmap.md). A future adapter must search
local ASPBE, Mathlib, then attributed quantum Lean libraries before adding a
foundation. This planning update adds no new foundational definition, so it
does not pretend an exhaustive external-library API audit has happened.

## Two source routes, shared mechanisms

The authoritative records are the existing source registry, paper queue, atlas
and Wiki JSON. Cards are authored once inside atlas families and reused by the
reader and agent packets. No second theorem-status database is introduced.

```text
explicit coefficients + grid/wire-order convention
  → Walsh characters → commuting diagonal phase supplier
                         ├─ control + interference + nonzero branch → WSL state
                         └─ source dilation + prepared input + branch contract
                              → diagonal-filter state
Every consumer also requires normalization/error and charged resource contracts.
```

This is a conceptual dependency map, not a Lean implication graph. Hyperedges
retain complete AND inputs. The existing generated Lean graph is unchanged;
the new pages only link exact existing declaration identities:

- `QuantumBlockEncoding.ConcreteSemantics.applyVec_zeroKet`: finite matrix
  action on the zero ket. This does not prove Walsh synthesis.
- `QuantumBlockEncoding.CubicDiagonalOracle.cubicN2PrimitiveProgram_cleanEntry`:
  fixed two-data-qubit cubic diagonal witness. This does not prove a general
  diagonal compiler, error bound or asymptotic resource theorem.

The Python Walsh/Gray multiplexor and the Lean UCRY compiler are different
objects from the Walsh Series Loader. Shared terminology is not a proof bridge.

### Walsh Series Loader

Pinned source: [2307.08384v3](https://arxiv.org/abs/2307.08384v3), with
[2502.05193v1](https://arxiv.org/html/2502.05193v1) as its companion implementation
audit. Relevant primary main/appendix passages were read, not merely abstracts.

Use the source convention, writing its small-angle parameter as \(\tau\):

\[
F_S=\operatorname{diag}(f_S(x)),\qquad
v_{\rm acc}=-\frac{i}{2}(I-e^{-i\tau F_S})|+\rangle^{\otimes n},
\qquad
p=\frac1N\sum_x\sin^2(\tau f_S(x)/2).
\]

The limit is proportional to the desired function, but finite \(\tau\) requires
an approximation proof. Theorem 1/Corollary 1, Table I and Appendix B must be
read together: target epsilon is **infidelity**. For a fixed admissible smooth
function, the advertised single-run depth is \(O(\epsilon^{-1/2})\), whereas
success is \(\Theta(\epsilon)\); expected RUS depth is
\(O(\epsilon^{-3/2})\). Function-dependent constants and nonzero mass matter.
Classical coefficient generation and amplified reflections/inverses are not
free. These are source bounds to formalize, not local performance measurements.

The comment's Sections II.2–II.3/Eq. (11)/Fig. 2 explain the constant-mode
hazard. A phase on the whole data state becomes relative when controlled.
For nonzero constant \(f\), dropping that term can turn the accepted branch
into zero. Retain the control phase \(P(-\tau a_0)\); distinguish this
implementation issue from a refutation of the theory.

### Diagonal unitary and non-unitary operators

Pinned source: [2404.02819v4](https://arxiv.org/abs/2404.02819v4). The source audit
covered relevant pp. 3–16 and Appendix B pp. 25–27, not every section.
Read unitary phase synthesis, non-unitary embedding, parallel scheduling and
state-preparation applications as separate claims. Source Table I uses spectral
operator error, not WSL infidelity. For the exact accepted block in the source's normalization,

\[
p=\frac{\|D\psi\|^2}{\alpha_{\rm src}^2d_{\max}^2}.
\]

Our generic block notation uses total scale
\(\alpha_{\rm total}=\alpha_{\rm src}d_{\max}\). This is an explicit notation
adapter, not a change to the source. Exact dilation permits its endpoint
scaling; smooth transformed-angle approximation needs the stronger guard
\(\alpha_{\rm src}>1\). Degenerate all-zero diagonals and zero output branches
need separate treatment. A small operator error can be magnified by subsequent
normalization when the accepted branch is tiny.

The error scale also needs an adapter: source Eq. (18) bounds the error of
the **normalized block**, \(\|D/\alpha_{\rm total}-B\|\le\delta\).
The Lin–Wiebe/local unscaled-operator convention instead reads
\(\|D-\alpha_{\rm total}B\|\le\epsilon\); these match with
\(\epsilon=\alpha_{\rm total}\delta\), not by reusing the same numeric
tolerance. Neither quantity is automatically a state-infidelity bound.

V.1 directly treats **signed real** diagonal entries, not only nonnegative
ones. The source's subsequent complex extension factors
\(D=e^{i\arg D}|D|\): supply the modulus dilation and the phase operator
separately, choose a phase convention at zero entries, and charge phase
synthesis. A generic complex-matrix interface does not discharge this supplier.

The source reader flagged four locations requiring reconciliation before
source-faithful theorem promotion:

| Location | Audit observation | Required next action |
| --- | --- | --- |
| III.2, pp. 7–8 | Ceiling and floor-plus-one expressions for the parallel group parameter disagree at divisible input sizes | Freeze the permitted integer range and literal schedule; test the divisible boundary |
| VIII.1, p. 16 versus Table I | The stated size improvement with parallelism needs reconciliation with total gate accounting | Derive size and depth separately from the schedule; do not silently substitute one for the other |
| Fig. 4 versus Eqs. (19)–(21) | Caption and equations identify different accepted signal values; Eq. (19)'s rejected-branch phase also needs reconciliation with the displayed final H/P gates | Transcribe source circuit and prove both signal blocks and their relative phase before choosing a convention adapter |
| Appendix B1 versus B2 | Initial/accepted signal labels differ from the displayed block projection | Keep source statement, derived circuit action and any proposed repair separate |

These are **source-audit observations**, not independently accepted paper
corrections. None is resolved by changing the source contract in Lean. The first
two prohibit unqualified resource claims; the latter two prohibit advertising a
literal block theorem until the signal convention is reconciled.

A separate source/organization reviewer (`walsh_independent_review`, distinct
from `walsh_source_audit` and the integration author) independently checked the
WSL accepted branch, zero mode and diagonal normalization/error conventions.
It found no blocking issue in the **planned-only admission**, and requested the
scaled-error clarification and full two-branch phase obligation now recorded
above. This is not a source-blind Lean decoder review and accepts no proposed
paper correction or future theorem.

## Bounded formalization and memory plan

1. Prove one parity-string diagonal action, including empty parity and controlled
   constant phase; freeze the wire-order adapter.
2. Prove the exact WSL ancilla-branch action; separately prove the source
   diagonal-dilation blocks. Test constants, one parity, zero entries, sign and
   accepted-sector conventions.
3. Reuse finite-matrix/norm machinery to derive success and normalized-error
   bounds; zero branches fail closed rather than being normalized.
4. Compose truncation/coefficient/angle errors. Only then prove the source
   resource statements under reconciled size/depth/workspace conventions.
5. Before promoting any new production Lean module, require whole-module
   binding, source-blind decoding, distinct anti-anchored review and all existing
   Lean/publication gates. A review of this plan is not that future theorem review.

Retrieve bounded packets with:

```bash
python3 website/scripts/research_atlas.py context --route spw-walsh
python3 website/scripts/research_atlas.py context --route spw-diagonal
```

Both technical cards have `lean_status: obligation`, `lean_decl: []`, explicit
dependencies, failure modes and next acceptance targets. No leaf is invented
merely to draw a populated graph. No change to controller, verifier, benchmark
split, scientific target or historical trial logs is needed for this admission.

## Validation scope

The live audit above describes the pre-change public deployment. New local
pages are not automatically deployed by changing source records. Focused
catalog/card tests, the unchanged Lean proof-input gate and generated-site
checks must be reported separately; a missing or failed full publication gate
must never be replaced by a green placeholder.

Recorded local evidence (working tree based on the baseline above):

- `python website/scripts/run_lean_gate.py`: passed root, Tests and the full
  explicit module inventory. No production Lean source changed in this update.
- `python -m unittest website.scripts.test_research_atlas`: 34 tests passed.
- Combined research/Hermite regression suites: 52 tests passed after the
  publication-copy fix described below.
- Publication admission checker against `origin/main`: no changed production
  modules and no new accepted theorem packets, as expected for planned cards.
- First browser run: 30 theme/viewport combinations and all authored method/
  research-route formula pages passed using installed Edge. Desktop/mobile
  Walsh AND-graph screenshots were additionally inspected for readable labels.

The initial `scripts/build-all.ps1` execution passed its Lean, executable replay
and Blueprint stages, then failed the final reader marker check: the old
Hermite contract survived inside the copyable LaTeX panel even though the
visible paragraph had been enriched. The source contract in
`website/hermite-case.json` is now typeset consistently and says
"Lean-certified", not "new". The resource bound, theorem roots and outstanding
cost obligations are unchanged. `test_hermite_case.py` checks both the formatted
bound and absence of the obsolete sentence. The failing assertion was retained.

Browser installation from the download CDN timed out; the existing Edge
runtime was used through the explicit `--browser-channel msedge` option.
The default CI Chromium choice and all checks remain unchanged; the selected
channel is recorded in the browser report. These are environment/reader
corrections, not changes to proof acceptance. Final website rebuild and browser
results are recorded in the integration handoff rather than treating the first
failed aggregate invocation as a pass.

### Final integration handoff

After the canonical Hermite copy-panel correction:

- `scripts/build-website.ps1 -PythonCommand .venv/Scripts/python.exe` exited
  successfully: 379 HTML pages, 4,524 declaration search entries, 10 diagrams,
  4,524 commit-pinned source links and 563 publication text files checked for
  local-path leakage. The original final reader assertions all passed.
- `python website/scripts/research_atlas.py check-site --root _site` passed
  again against the final generated catalog, including the signed-real versus
  complex-diagonal supplier distinction.
- The combined research/Hermite regression suites passed again: 52 tests.
- The final `test_research_browser.py --root _site --browser-channel msedge`
  run passed all 30 theme/viewport combinations and all authored method/Wiki
  formula pages, with no reported failures. Both new hyperedges retained their
  complete AND-input sets. Evidence: `_out/research-browser/browser-report.json`.
- Both route-specific context commands above returned the planned technical
  cards, pinned source metadata and complete selected hyperedges.

The initial aggregate command still has a failed exit status; it is not
retroactively relabeled successful. Its completed Lean/executable/Blueprint
stages and the successful corrected website/browser reruns are separate
evidence. No production proof inputs changed between those stages.

Authored changes are confined to the roadmap and this audit, the technical-card
README, the paper/source/atlas/Wiki catalogs, technical-card publication and
retrieval, their tests, the optional local browser-channel selector, and the
Hermite source-copy regression fix. The pre-existing Robin export/replay working
tree changes and unrelated images are not part of this admission. Nothing here
changes the controller, Lean verifier, scoring or historical trial logs.

This handoff is locally validated, not a claim of a new public deployment.
Both new paper routes remain queued for formalization; no new paper theorem
has been promoted to the compiled Lean graph.
