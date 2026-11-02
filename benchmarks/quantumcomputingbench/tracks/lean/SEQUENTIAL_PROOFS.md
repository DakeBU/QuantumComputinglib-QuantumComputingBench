# Sequential State Preparation proof companions

This experimental sidecar develops two views of existing cores. Canonical
questions, splits, frozen releases and the non-Lean track stay unchanged. UUID
records under `proposals/` remain uncounted formal-companion candidates.

| Core | Exact formal conclusion | Substantive assumptions |
| --- | --- | --- |
| SP007 | Full word/final-bond amplitudes equal the chronological transfer product applied to an arbitrary complex boundary | Only local fresh-input-bit-zero column equality with the cores |
| SP008 | Real sum of `Complex.normSq` over the full word × bond basis equals one at every length | Full unitary stages and an initial bond basis label |

SP007 includes length zero and newest-factor-on-the-left order. Its boundary
need not be real or normalized; unitarity is not added. Input-bit-one columns
never enter its step action. SP008 retains the final bond and does not imply
cleanup, separability or physical-bit-only purity. Neither target establishes
completion existence, flattened circuit execution, synthesis or resource bounds.

## Evidence and boundaries

SP007 combines a one-step finite-sum collapse with all-length induction. SP008
uses an explicit real-part-to-real-probability bridge, padding/lifted-unitary
step mass, all-length mass induction and basis-boundary evaluation. These are
provided obligations, not autonomous planning or measured proof-term depth.

The original SP007 root is a one-call control. SP008's same-target control uses
the complex-mass theorem **plus an explicit real bridge**. The complex theorem
alone has the wrong type; it is a negative control. A basis-boundary
specialization likewise cannot replace SP007's arbitrary-boundary target.
Rejections are implementation/type failures, not mathematical refutations.

The [source-blind decoder](../../reports/lean-agentic-sequential-v1/decoder.json)
saw anonymous types and definition displays. A
[distinct source-aware comparison](../../reports/lean-agentic-sequential-v1/comparison.json)
accepts both exact root alignments while keeping whole-question exposition
coverage partial. Root checking does not grade whether a respondent explains
induction, irrelevant columns, coherence or padding; those retain the complete
canonical NL rubric.

Displays are normalized reconstructions, not byte-literal source extractions.
The [context audit](../../reports/lean-agentic-sequential-v1/source-context-audit.json)
records qualification, wrappers, universes and equalities against actual imports.
The raw S2 display mentions universe `v` without declaring it in its preamble;
the audit supplies `u v`. This display-only caveat remains visible: the packet
is not advertised as executable verbatim. Both root targets use declared `u`.

The inspected [standalone context-audit source](fixtures/SequentialContextAudit.lean)
is included for reproduction. Its LF hash matches the author's compiled audit
file named in the source-context record. It uses an audit namespace and
explicit `u v` declarations, rather than redeclaring the imported definitions.

Protocol v2 carries a bounded list of universe identifiers as evaluator-owned
data, bound into task, request and reference source. It accepts no arbitrary
source preamble. Existing v1 tasks remain supported.

## Local commands

Export proof-free inputs:

```sh
python benchmarks/quantumcomputingbench/scripts/sequential_proofs.py export \
  --output _out/sequential-agent-inputs.json
```

Replay inspected authored references in an installed matching built checkout:

```sh
python benchmarks/quantumcomputingbench/scripts/sequential_proofs.py check-references \
  --trusted-local-reference --build-root PATH_TO_MATCHING_BUILT_CHECKOUT \
  --output _out/sequential-session-replay.json
```

Fresh outputs are mandatory. Both candidates and all conditions use a declared
300-second authored session ceiling with actual calls/time retained. Empty or
incomplete cohorts are rejected. Unknown proof hashes are never executed.
Final roots are independently rebuilt in fresh processes with an axiom allowlist.

Exports omit references, controls, operator rubrics and review verdicts. Existing
public references still make this a non-blind cohort. Model-generated execution
requires a separately accepted isolated verifier. Fixed replay is engineering
evidence and does not create model scores or canonical formal admissions.

The [qualified local execution record](../../reports/lean-agentic-capabilities-v1/sequential-execution.json)
records the frozen pipeline, actual compiler/checkout, 16 verified checks,
two expected rejections, six final root replays and the fresh repository gate.
