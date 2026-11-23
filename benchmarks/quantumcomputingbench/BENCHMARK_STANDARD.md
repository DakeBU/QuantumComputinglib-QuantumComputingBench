# Benchmark design, release gates and coverage roadmap

QuantumComputingBench measures knowledge and mathematical reasoning in quantum
computing, with an additional tool-assisted setting for formal proof. Its
scientific unit is a mathematical core: a question, exact assumptions and
requested conclusion anchored to the QuantumComputinglib graph. Natural-language
and Lean views of that core share family and split identifiers. Graph reasoning
belongs in both tracks; supplying a graph slice is an optional experimental
information condition, not a third independent benchmark or new core count.
The current formal course's `root_only` and `proof_dag` modes differ in
submission rules, not graph visibility: both expose the supplied obligation
graph. A graph-provided versus graph-withheld autonomous planning diagnostic
must be implemented and scored as a separate controlled information condition.

## Design precedents

The following primary research sources inform the standard; they do not imply
interoperability, endorsements or comparable benchmark scores.

| Precedent | Adopted design principle |
| --- | --- |
| [Terminal-Bench (Merrill et al., arXiv:2601.11868)](https://arxiv.org/abs/2601.11868), [official tasks](https://github.com/harbor-framework/terminal-bench) | Treat every agent task as a reproducible contract with an environment, instruction, reference solution and independent verifier; verify solvability and rejection of incomplete solutions. |
| [MATH (Hendrycks et al., NeurIPS 2021)](https://arxiv.org/abs/2103.03874) | Provide substantial worked mathematical solutions, useful for both learning and evaluation, rather than final labels alone. |
| [miniF2F (Zheng et al., ICLR 2022)](https://arxiv.org/abs/2109.00110) | Freeze exact formal statements and make proof success reproducible. |
| [LeanDojo (Yang et al., NeurIPS 2023)](https://arxiv.org/abs/2306.15626) | Expose a reproducible proof environment and premise access; test transfer beyond seen solution families. |

Terminal-Bench-style packaging is an engineering target. QCB's existing
[runtime](docs/runtime.md), [benchmark card](BENCHMARK_CARD.md) and evaluation
interfaces have their own formats. A Harbor-compatible isolated adapter is not
asserted merely because a task can be exported or locally replayed.

## Release acceptance checklist

| Gate | Required evidence |
| --- | --- |
| Mathematical contract | Fixed assumptions, dimensions, basis/register convention, requested result; original readable question and full worked solution; answer-equivalent alternatives or content rubric. |
| Source and graph | Pinned graph snapshot, exact declaration or reviewed source anchors, typed mathematical support with complete AND premises and alternatives; explicit planned/partial status. |
| Identity and exposure | Stable shared core ID, family, split, content hashes, source and answer access policy; reconcile duplicates and related mechanisms before pooling. |
| Reproducible task | Machine-readable answer-free input, environment/toolchain and imports, resource budget, response schema, separate train references and evaluator material. |
| Right-answer evidence | A distinct mathematical/semantic review. For Lean, authored reference proof and fresh exact-root replay, fixed assumptions, transitive axiom policy and no sorryAx. |
| Grading robustness | Positive, incorrect, incomplete and boundary controls; accept mathematically valid alternatives; typed unavailable/time-out outcomes. Legal tactics are not necessarily progress, and a formally valid statement is not an automatically correct explanation. |
| Measured capability | Only actual model runs under the accepted execution/access contract may populate results. Record checkpoint, input/output tokens, elapsed time, calls, task mode, exposure and denominators. |
| Release and maintenance | Version manifest, exact task and proof identities, test reports, reproducible commands, contribution and issue workflow, citation and license/source provenance; no promotion of a candidate by assertion. |

Authored Lean verification can run locally on reviewed trusted reference code;
untrusted model-generated Lean requires the accepted isolated verifier profile.
Missing isolation is a visible environment limitation, not a negative proof
result or a reason to bypass the execution policy. Public test inputs and
references are reproducible open data, not a claim of contamination-free testing.
Owner-only assessment remains separately sealed.

## What complete coverage means

Build a versioned matrix across subject, mechanism, exact source status, skill,
provisional construction band, support relationship and independent family/split.
For each mathematical mechanism, select meaningful knowledge/local-reasoning,
composition and assumption-sensitive tasks where the mathematics supports them.
Each remaining source region must have an explicit coverage disposition: covered,
candidate, not useful as a student task, or blocked by missing reviewed evidence.
Do not demand one question per helper or enumerate arbitrary paths. A module
import is not an implication, graph anchor count is not reasoning depth, and
the number of tasks does not certify that a trained model mastered a domain.

### Starting checkpoint — 21 November 2026

The current canonical catalog at `62d9a4f` has 198 retained mathematical cores,
74 train, 21 dev and 103 public test. The separate 24-item natural-language
workbook contains four same-core expositions and 20 unassigned candidates; it
adds no formally admitted cores or scored split rows. Fifteen historical core
contracts remain withheld. The v6 Lean course has 25 overlapping shared cores,
16 train, 4 dev and 5 public test (D1=1, D2=9, D3=10, D4=5). These are provisional
route difficulties, not measured model calibration.

| Subject | Train | Dev | Public test | v6 Lean core companions |
| --- | ---: | ---: | ---: | ---: |
| Foundations | 39 | 9 | 10 | 3 |
| State Preparation | 18 | 7 | 6 | 10 |
| Block Encoding | 16 | 5 | 2 | 11 |
| Quantum Information | 0 | 0 | 53 | 0 |
| Quantum Scientific Computing | 1 | 0 | 32 | 1 |

Eighty-five source-only planned-topic cores are public test. Do not move those
answers into training, or admit them as locally Lean-certified. Design new
source-supported, family-reconciled training and evaluation cohorts. In the
frozen graph inventory, 350 of 3,548 declarations labeled Compiled are directly
anchored by current canonical cores; the public workbook union reaches 398.
This is an anchor statistic, not a semantic or proof-term coverage percentage.

The [v7 circuit-foundations checkpoint](tracks/lean/COURSE_V7.md) extends the
course to 29 of those same cores: 18 train, 5 dev and 6 public test. It adds
register order, two-term linearity and reversible bit actions, including a
concrete counterexample to an invalid control configuration. The cumulative
route bands are D1=2, D2=12, D3=10 and D4=5. The 91 distinct source anchors
recorded by the supplied tasks are not a denominator for model mastery. The
canonical inventory, workbook and family splits are unchanged; no new graph
declaration or canonical formal admission is inferred from a course view.

### Priority queue

1. Basics and circuit semantics: inspect `TextbookStatePreparation`,
   `PrimitiveSemantics`, `PrimitiveBasisLE`, `PrimitiveCircuit` and
   `ConcreteSemantics`; pair basic mathematical understanding with exact local
   formal views. Preserve bit order, phases, dimensions and exact action.
2. Reversible operations and construction boundaries: controlled bit action,
   composition, inverses and collision witnesses, then conditional clean-block
   and state-action interfaces. Existing phase-cycle and rotation workbook
   overlaps must be reconciled, never counted twice.
3. Concrete construction families: `StatePreparationPrimitiveRoutes`,
   `CubicStatePreparation`, `MainCase`, `HermiteBoundaryInjection`, `Resources`
   and missing interfaces in `BlockEncodingClassics`. Prioritize missing
   public-test mechanisms in block encoding and compiled source validity.
4. QIT/scientific computing: preserve source-only questions and distinguish
   actual current anchors from plans. Admit qualified formal counterparts
   only when source semantics and local compiled interfaces support them.

Contributors should reconcile the 20 pending workbook candidates and 15
withheld contracts before counting their recovery; prioritize meaningful
uncovered mechanisms rather than repeating existing examples. The next local
Lean course selects existing exact contracts in priority 1–2 before broader
algorithm families. Each new cohort must state its coverage delta, preserve
earlier manifests and publish the highest actually qualified frontier.

## Citation and result reporting

Cite the project via [CITATION.cff](../../CITATION.cff) and identify the exact
benchmark commit, course/release ID, graph snapshot, split, access setting,
task count, grader/verifier version and budget. Cite underlying mathematics and
contributors through each task's source record. Do not compare scores from
different information conditions as though they were the same benchmark.
Until these release gates and actual measurements are complete, describe the
project as an open development benchmark with qualified subsets.
