# QuantumComputingBench benchmark card

QuantumComputingBench is a graph-grounded collection of quantum-computing
knowledge, mathematical-reasoning and formal-proof tasks. Its source is
QuantumComputinglib, together with the explicitly cited mathematical sources.
The exercise book, executable task registry and expert atlas describe the same
versioned mathematical contracts.

## Intended use

- Train specialized mathematical models using the inherited `train` examples.
- Assess knowledge, assumptions, counterexamples and mathematical arguments.
- Assess library-aware formal construction and repair with an isolated verifier.
- Give domain experts inspectable question-to-source and question-to-graph maps.

See the [runtime manual](docs/runtime.md) for installation, split-aware exports,
prepared runs, response schemas, scoring, review and portable task environments.
The [shared contract](shared/CONTRACT.md) governs all natural-language and Lean
views. The current distribution is an open public preview with explicitly
qualified reference cohorts; no version rename closes outstanding review gates.

## Data identities and splits

One canonical core represents one mathematical target. Natural-language,
Lean-course and diagnostic views retain their parent source aliases. A view
count is not a count of distinct new mathematical questions. The runtime's
`task-index.json` and `download-manifest.json` report the actual current counts,
version identities and hashes rather than allocating a new split.

`training` export accepts inherited `train` examples only. `evaluation` export
contains question-only inputs from the requested inherited split. References,
rubrics and operator review material are outside the student payload. Public
test questions and public library theorems can already occur in pretraining or
teacher data; report that exposure in any model study. The current public test
split does not become a private or proof-disjoint holdout through prompt hiding.
New evaluation families need separate admission and split reconciliation.

## Task and environment contract

Each task binds an instruction, response schema, source contract, graph anchors,
source revision, view identity and task hash. Prepared runs add exposure mode,
model/operator provenance, resource budget and verifier identity. Exact task
hashes travel with submitted responses and reviewer records.

The natural-language workflow needs Python and can be prepared without Lean or
a model endpoint. Portable tasks separate the agent workspace from reference
solutions and grading inputs. Formal task export preserves the existing proof
protocol; executing model-generated Lean requires an accepted isolated backend.
A trusted local authored reference is evidence about its fixed proof, not a
certificate for executing arbitrary model output.

Packaging follows the useful instruction/environment/solution/verifier
separation documented in [Harbor](https://docs.harborframework.com/tasks/overview).
The runtime manual distinguishes locally tested QCB workflows, task-format
validation and actual container execution. Harbor interoperability is qualified
by the checks performed, rather than inferred from similar filenames.

## Scoring and evidence

Report the dimensions separately:

| Dimension | Decision procedure |
| --- | --- |
| Semantic decision | Exact `holds`/`refuted` decision on the contrasted propositions; complete-pair accuracy is also reported. |
| Mathematical explanation | Task- and response-bound expert criteria, with reviewer provenance. Unreviewed explanations remain ungraded. |
| Formal root | Kernel/axiom evidence for the exact requested target from the accepted verifier. |
| Process and tools | Recorded actions and typed outcomes; legal Lean steps do not automatically receive positive process reward. |
| Resources | Observed model calls, tokens and elapsed time under the recorded harness and budget. |
| Coverage | Actual subject, anchor and task-view coverage, with unsupported and excluded regions visible. |

Missing, abstained, blocked and incorrect outcomes remain distinct. A synthetic
oracle smoke validates engineering behavior; it is labeled synthetic throughout
and supplies no model baseline. Authored reference acceptance establishes its
exact mathematical scope, not learned understanding, calibrated difficulty or
faithfulness of a model's internal reasoning. A later learning study needs
actual student responses and an appropriate matched design.

## Expert inspection

The expert atlas provides a reverse index from exact graph node to question,
the target/support roles of each anchor, typed local neighborhoods and the
source version behind a declaration. Frozen benchmark graph membership is
distinct from current library membership. Imports, ownership and conceptual
links are not claimed as extracted proof-term dependencies. Course obligation
graphs are shown as supplied task structure, with AND joins preserved.

The planned graph can guide new questions but cannot supply compiled evidence
for an unproved result. Every contribution should state its assumptions,
register/scalar conventions, source relation, reference answer, rubric and
available formal evidence before admission.

## Quality, limitations and reporting

Mathematical authoring and review are currently AI-assisted with retained
content-bound review records. Existing records do not imply newly performed
human expert review. Withheld or disputed items remain outside current reader
and scoring exports. Global semantic deduplication, broad fresh editorial
review and whole-library formal-view coverage remain tracked obligations.

Report a mathematical error, missing premise, source mismatch, formatting
error or verifier loophole using the repository's benchmark issue forms. Include
the task/core ID, source revision, expected behavior and a minimal reproduction.
Result submissions should retain the run manifest, task-bound outputs and the
scoring/review artifacts. Maintainers can then distinguish an environment
failure from an incorrect mathematical answer.

## Attribution and maintenance

The project is maintained at
[QuantumComputinglib-QuantumComputingBench](https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench).
Cite the project and exact dataset/task version, and retain per-item contributor
and external-source attribution. The root [citation metadata](../../CITATION.cff)
and [reuse policy](../../LICENSES/REUSE.md) apply. Mathematical source citations
do not imply that those authors endorsed these task formulations.
