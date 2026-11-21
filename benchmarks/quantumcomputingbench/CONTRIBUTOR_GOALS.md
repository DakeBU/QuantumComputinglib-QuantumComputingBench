# QuantumComputingBench: three complementary evaluation modes

The scientific objective is to determine which quantum mathematics a model can
understand, derive and apply, how well it can use Lean to solve mathematical
problems, and whether it understands the structure connecting mathematical ideas.
The three modes share one mathematical core registry. A view is an evaluation
condition or answer format, not another independent question.

| Mode | Student receives | Main evidence of success |
| --- | --- | --- |
| Non-agentic Mathematical QA | A complete question with stated definitions, assumptions and notation; no tools or retrieval | Correct answer and independently reviewed mathematical derivation, including boundaries |
| Agentic Lean-assisted QA | A fixed mathematical target, approved imports/interfaces and a specified feedback environment | Fresh replay of the unchanged Lean root under the approved axiom policy, plus separately scored reasoning and resource use |
| Structured Graph QA | A versioned graph slice or explicitly closed-book graph question, with a defined relation vocabulary | Correct dependency choices, complete AND premises, feasible derivation plans and mathematically justified explanations |

The first two modes have existing curricula, reference evidence and interfaces.
Structured Graph QA is a proposed scored track; the existing expert atlas and
reasoning graph guide provide its starting point, not an already qualified graph
test suite. Mode-level scores must remain separate. Match the shared core,
information access and budgets where a comparison needs paired tasks.

## Shared operating contract for every goal

Append the following block to exactly one of the role objectives below when
starting an AI agent's persistent goal. Work in English. The agent should deliver
bounded, reviewed batches and a coverage delta, then resume from the next gap.

```text
Work in DakeBU/QuantumComputinglib-QuantumComputingBench. Start from current main;
record its commit, graph snapshot ID/hash and current curriculum registry.
Read AGENTS.md, HARNESS.md, benchmarks/quantumcomputingbench/AGENT_GOAL.md,
shared/CONTRACT.md, the applicable track goal and publication protocols.
Run `python benchmarks/quantumcomputingbench/scripts/curriculum.py export
--output <fresh-output.json>` on one command line and inspect existing cores,
proposals, withheld contracts and accessible collaborator work before writing.
Reserve mathematically meaningful task families by topic, exact target and exposure;
do not duplicate paraphrases, Lean translations or graph views as new cores.

Prioritize coverage gaps in definitions, local derivation, multi-node composition,
hypothesis sensitivity, counterexamples and cross-topic transfer. Work from easy
to difficult. Report provisional difficulty D1-D4, support node count, relation
types and meaningful inference steps separately; do not manufacture graph depth.
Represent all required premises; distinguish module imports, declaration ownership,
checked proof-term dependencies, reviewed mathematical links, conceptual
transports and planned nodes. Planned/source-only work must be visibly qualified.
Do not use unproven graph edges as logical implications.

Every candidate has a stable existing core ID or candidate:<UUID>, contract
hash, snapshot and source/version anchors, family, split, exposure profile,
question, complete reference answer/derivation, acceptable-alternative rubric,
assumptions, dimensions, notation, semantic step-to-node map and limitations.
Keep equivalent views and solution-revealing aliases in the same family/split.
Propose new families with train/dev/test allocation before generating variants;
reserve disjoint withheld families or parameter regimes for meaningful transfer.
Never move frozen test material to train. Public evaluation is not blind testing.
Source review, independent answer review, Lean qualification and measured model
performance are separate evidence. Do not promote drafts or fabricate reviews.

For each accepted candidate, reconstruct the solution from the question first,
then have a distinct reviewer check actual mathematics, exact assumptions,
boundary cases, relevance, possible shortcuts and overlapping solution families.
Use original prose and licensed sources. Write concise textbook English:
definitions and assumptions first, question next, essential derivation and
physical/mathematical meaning, then folded evidence and implementation details.
Use standard LaTeX and explicit dimensions and conventions.

Use UUID proposals, not edits to frozen data or someone else's branch. Run the
existing validators and relevant tests; report exact commands/results, graph and
split coverage, duplicate/blocked dispositions and review limitations. Provide
answer-free task inputs and separate reference/rubric artifacts. Train exports
contain train-family references only. Keep any genuinely private test gold in
an owner-only archive outside the public repository and public ZIP. No paid
inference, real-model training, long GPU jobs or untrusted Lean execution on
the host is authorized. Do not manufacture model scores. If you can push,
submit an independent reviewed branch/PR; otherwise deliver a ZIP of proposals,
manifest with hashes and provenance, tests/review report, and a README explaining
how to integrate it. Do not require changes to other tracks or website internals;
use existing publication section conventions and let the maintainer integrate.
Continue until the agreed batch is qualified or each remaining item has an
explicit evidence gap and actionable next step. Do not claim whole-domain mastery.
```

## Goal A — Collaborator without Lean: Non-agentic Mathematical QA

```text
Extend the non-agentic Mathematical QA curriculum, using the current frozen
QuantumComputinglib graph and reviewed planned curriculum to build original
closed-book quantum-mathematics questions. Reuse the shared core registry;
write under tracks/non-lean/proposals with the existing proposal protocol.
Prioritize gaps not already covered by the natural-language workbook; avoid
rephrasing existing definitions or varying only numbers. Build small families
that progress from explaining a definition or exact theorem to deriving a result,
choosing a lemma with all premises, composing different results and detecting or
correcting false claims. Include exact worked derivations and counterexamples,
not just final answers. Cover State Preparation, Block Encoding, foundations and
source-supported planned QIT/scientific computing in proportion to actual gaps.
Assess mathematical knowledge and reasoning without giving Lean identifiers,
retrieval snippets or answer hints as shortcuts in closed-book input. Provide
separate source cards and expert references for grading. A planned result can
have a reviewed NL reference but cannot be called locally Lean-certified.
You do not need Lean installed; do not claim kernel execution or manufacture
formal evidence. Deliver one coherent 12–20 candidate batch across at least two
distinct mechanisms, with independent mathematical/semantic review and explicit
family/exposure reconciliation. Smaller qualified batches are preferable to
filling a quota with redundant or unsupported questions. Include public review
and train proposals, public test proposals clearly labeled, and any owner-only
holdout separately if the maintainer has explicitly allocated that family.
```

## Goal B — Local or Lean-equipped collaborator: Agentic Lean-assisted QA

```text
Extend the current cumulative Lean QA course (v6 is the starting checkpoint;
inspect main for a newer course), prioritizing existing source-supported cores
whose full mathematical contracts lack an exact formal companion. Use
tracks/lean/proposals and the existing versioned curriculum/qualification
pipeline. Choose a small coherent cohort from documented graph gaps; do not
promote planned nodes until a reviewed compiled source/snapshot supports them.
Include a local proof, a multi-premise composition and, where justified, a
counterexample or repair task. Record how the supplied proof-obligation DAG
relates to actual checked dependencies and any imported theorem shortcuts.

For each task freeze the full root, context/imports, assumptions, allowed axioms,
and permitted retrieval. Provide a natural-language mathematical proof,
source-blind reconstruction of the formal statement and distinct source-aware
semantic comparison. Compile independently authored reference proofs at the
pinned toolchain; verify the exact unchanged root in a fresh process, inspect
transitive axioms and reject wrong-target/incomplete/unapproved-axiom controls.
Check separate explanation obligations wherever a root does not encode a method
or physical interpretation. Distinguish a one-call library application from
new proof synthesis, and accepted proof steps from demonstrated progress.

Provide answer-free exports for both whole-root and supplied-obligation modes;
preserve closed-book/approved-interface/full-library exposure labels. Enable
incremental tactic or asynchronous NL/Lean feedback only through a supported,
accepted isolated verifier. Compare feedback timing only under matched tasks,
model, available source and token/time/tool budget. If isolation is unavailable,
perform trusted authored reference checks and synthetic protocol checks only;
leave real generated-proof execution blocked and performance unmeasured.
Deliver 2–4 substantive qualified companions (or fewer when evidence requires),
separate train-only references, versioned benchmark entry points, preserved prior
course fingerprints, and tested English hierarchical reader pages with exact
graph/source links. Run applicable Lean, benchmark, publication and browser gates.
```

## Goal C — Graph specialist (Lean optional): Structured Graph QA

```text
Establish the first evidence-qualified Structured Graph QA pilot, using versioned
Lean Graph and Functor Hypergraph slices. Read the graph exporter and actual
relation schemas; inspect the existing expert atlas and reasoning guide. Work
in tracks/structured-graph/proposals using the draft packet contract in that
track's README. Do not claim a registered score until a reviewed scorer and
admission protocol exist. Reuse the mathematical core ID when a graph query
examines the same target; a new mathematical question needs a candidate UUID.

Design graph-given tasks (provide only the selected nodes, typed edges, statements
and necessary assumptions) separately from closed-book tasks. Ask the model to
select sufficient prerequisites, complete an AND-tail, order a proof DAG,
distinguish alternative valid routes, find a missing condition or invalid edge,
or transfer a mathematical mechanism across subjects under an explicit interface.
Include graph-negative pairs: import proximity without implication, incomplete
AND-tails, reversed dependencies or omitted representation assumptions. Test
mathematical applicability and explanations, not memorized node names or arbitrary
path lengths. Randomize presentation order without changing the graph. Record
whether the answer needs graph structure, mathematical content or both.

Begin with 8–12 original reviewed tasks spanning at least three distinct graph
motifs and two quantum mechanisms; choose train/dev/test families before writing.
Save typed answer keys with all acceptable equivalent solution structures where
known, exact constraints for ordering/set/edge questions, and reviewed NL reasons.
For open proof-plan responses use a content rubric and accept alternative valid
plans; do not force one reference traversal. Record graph-level scoring separately
from mathematical validity. Build a small deterministic input/export/scorer pilot
only for well-defined structured answers, with positive, equivalent-alternative,
missing-premise, wrong-edge, invalid-order and unsupported-claim controls. Do not
claim automatic scoring of arbitrary mathematical explanations. If Lean is not
installed, use pinned existing evidence and request a maintainer's replay for
any new formal claim; keep source-only graph evidence labeled appropriately.
Deliver evidence-bound packets and reviewed coverage/exposure ledger; do not
modify canonical registry/splits or admit a new task kind yourself.
```

## Integration order

The maintainer reconciles family overlaps and exact contracts before admitting
the proposals. First qualify the mathematical question; then attach the supported
views. Record new core counts separately from additional mode/view counts and
benchmark protocol versions. For paired experiments, choose matched cores and
report each capability with its own denominator. Library retrieval can establish
application skill, but a publicly retrievable complete proof is not evidence of
unseen theorem discovery. Coverage is a map of tested capabilities, not proof
that a model understands the entire domain.
