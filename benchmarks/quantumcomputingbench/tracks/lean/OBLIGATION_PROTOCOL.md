# Experimental Lean proof-obligation protocol

This is a local engineering slice for Lean-enabled QuantumComputingBench. It
implements task-scoped declaration search, fixed-target obligation checks,
retained failed attempts, repair, and fresh final-root replay. It does not start
a proving model. The default verifier is blocked. The only executable backend
in this slice accepts inspected, exact-hash authored fixtures; it does not run
arbitrary model output on the host.

## Mathematical scope

The fixed cohort reuses `qcb-core-sp-005` and `qcb-core-la-102`, preserving their
canonical question contracts, families, public-test splits and native Lean root
types. They remain two mathematical cores across all views and conditions.

| Core | Provided proof obligations | Mathematical mechanism |
| --- | --- | --- |
| sp-005 | Pair-square identity, last-bit sum partition, marginal specialization, unchanged root | Nonnegative sum of squares and finite-basis reindexing preserve squared norm |
| la-102 | Repeated rows, row-swap sign, two-row determinant mixing, rotation/update alignment, unit factor, unchanged root | Alternation and multilinearity with the RY half-angle convention preserve determinant |

No amplitude positivity or normalization is added to sp-005. No invertibility,
orthogonality, adjacency or ordering premise is added to la-102; distinct row
indices remain required. The marginal specialization, rotation/update alignment
and trigonometric specialization include bookkeeping. Their node counts are not
a count of independent reasoning insights.

The root types already have native alignment evidence. The new decomposition
and intermediate obligations are **experimental evaluator-provided fixtures**,
not new formal-view admissions. Source-aware engineering review does not replace
an independent semantic admission process. Existing source hashes and exact
contract/split bindings are checked before export or replay. Planned graph nodes
do not enter this checked cohort.

## Agent-visible protocol

The evaluator fixes the task, imports, library revision, root, complete AND
dependency DAG, declaration corpus, axiom policy, exposure and ceilings. Each
action carries the current `state_id` and exactly its documented fields:

| Action | Fields in addition to `kind`, `state_id` | Result |
| --- | --- | --- |
| `search` | `query` | At most six scoped declaration names/types/source IDs; no proof bodies |
| `submit` | `node_id`, `proof` | A complete proof of that fixed obligation; status and bounded diagnostics |
| `explain` | `answer` | Recorded NL explanation; semantic score remains null pending independent grading |
| `finish` | None | A fresh process reconstructs and checks the same root and its accepted ancestors |

The state is an obligation frontier, **not a Lean tactic state**. No half-written
`case` or cross-round parser context exists. All accepted predecessor obligations
are re-declared when a dependent proof is checked. Final replay rebuilds the
complete root context from saved proof bodies, rather than accepting a saved
boolean or a zero-goal marker. Every actual checked theorem has a transitive
axiom audit; only `propext`, `Classical.choice` and `Quot.sound` are allowed.

`proof_dag` requires the provided predecessor obligations before a node can be
submitted. `root_only` accepts the whole root without requiring these artificial
submissions. Both conditions see the same provided decomposition and allow
repeated attempts within the same ceilings. **Root-only is not a one-attempt,
planning-blind ablation.** Existing original root lemmas remain imported and
callable in every condition; this is not a shortcut-free proof-synthesis test.

`approved_interface` enables the task-scoped search tool. `closed_book` disables
that tool. These names describe retrieval exposure, not a restriction on Lean's
imported namespace. The pilot does not expose repository browsing or internet
search. Interface search is a deterministic lexical tool, not a learned ranker;
search success is not mathematical credit or a premise-recall benchmark score.

## Bounds and failure classes

Default session ceilings are 32 actions, 12 verifier calls, eight searches,
16,000 proof characters, 512 query characters, a 24,000-character complete tool
reply, 180 wall seconds and 45 seconds per check. These are protocol ceilings,
not aggregate resource isolation. Feedback may be explicitly truncated; exact
attempt evidence stays in evaluator-owned reports. Session actions are
serialized. An authored native worker must finish timeout cleanup before the
session accepts another check.

Compilation/type failures are `IMPLEMENTATION_FAILED`. They do not prove the
mathematical statement false. Stale state, malformed fields or unbound verifier
evidence are `API_BLOCKED`. Runtime/toolchain/timeouts are `ENV_BLOCKED`; exhausted
ceilings are `BUDGET_EXHAUSTED`. Accepted execution, usefulness to a proof, formal
root correctness and semantic correctness of an NL explanation remain separate.
No accepted step is automatically a positive PRM training label.

The report records exact actions, responses, attempt evidence, task/contract and
pipeline identities, execution IDs, proof/source hashes, actual compiler and
checkout, axioms, elapsed time, calls and repair counts. Model token usage is
null because this smoke uses no model. Equal declared ceilings do not establish
equal realized compute; no feedback-timing causal effect is claimed.

## Local commands

From repository root, export proof-free public pilot inputs:

```sh
python benchmarks/quantumcomputingbench/scripts/proof_session.py export-pilot \
  --output _out/obligation-agent-inputs.json
```

The export excludes reference bodies, negative-control answers, knowledge
rubrics and the operator fixture metadata. Search interfaces are supplied only
through the scoped tool. References are nevertheless present publicly in this
repository: field projection does not make the cohort blind or contamination
free. The old baseline runner does not automatically consume this schema.

After inspecting the fixed fixture and matching the installed, already-built
Lean checkout, run the explicit authored-only smoke:

```sh
python benchmarks/quantumcomputingbench/scripts/proof_session.py smoke \
  --trusted-local-reference --build-root PATH_TO_MATCHING_BUILT_CHECKOUT \
  --output _out/obligation-smoke.json
```

Outputs require fresh paths. The runtime checkout must have the exact pinned
commit, matching production proof-input digest and a complete passing Lean gate.
The CLI has no custom candidate file or custom allowlist option. Unknown proof
hashes are rejected before a compiler or filesystem operation is reached.

The authored smoke uses a separately labelled **300-second session ceiling**
for every condition, leaving the default protocol's 180 seconds unchanged.
On the inspected Windows installation, Lean startup/checks take about 25 seconds
each; the first 180-second row-rotation DAG run checked all obligations but timed
out during final replay. That failed run remains evidence, not a successful root
certificate. Per-check and call/action ceilings remain unchanged.

Each core runs three authored engineering conditions: original library
application, a self-contained whole-root construction, and the provided DAG with
one deliberately ill-typed attempt followed by the fixed repair. These test
protocol plumbing and actual Lean compatibility. They are not model-generated
trajectories or comparative model accuracy. The authored-error repair costs are
recorded, rather than retrospectively removed from the budget.

## Next model-evaluation gates

Connect a separately accepted isolated candidate verifier without changing this
authored backend into an arbitrary-code runner. Add a model adapter with actual
token accounting and frozen model/template identities. Review semantic
decompositions and premise-route relevance independently before claiming those
scores. Admit new/source-supported targets and private evaluation instances
through the existing shared-core process; preserve dependency-aware splits and
all AND premises. Add genuine tactic-state execution only as a separately tested
condition. Knowledge/assumption rubrics remain evaluator-side and must receive
real semantic grading; a formal subproof does not certify the full NL answer.

No administrator contact, Cosmos3 privileges, GPU training, long model run,
website deployment or stable-release promotion is part of this checkpoint.
