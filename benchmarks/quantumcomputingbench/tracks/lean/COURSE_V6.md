# Lean course v6: orientation and wire order

Course v6 adds two train companions to the cumulative v5 course, bringing it
to **25 existing mathematical cores**. Their natural-language questions,
contracts, core IDs and splits are unchanged. They add formal training views,
not new mathematical cores or canonical formal admissions.

[Read the mathematics](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/lean/orientation-and-wires/) ·
[Download the cumulative course](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/run/course-v6/)

## What the new tasks test

| Core | Mathematical request | Supplied proof route |
| --- | --- | --- |
| LA006 | Extend prescribed orthonormal real columns to determinant +1; explain the fully prescribed obstruction. | Determinant classification and an unused column feed a sign-flip repair; join the positive result with a reflection witness and the empty-matrix boundary. |
| LA013 | Rename every wire consistently and prove exact circuit conjugation; diagnose output-only and unrelated-basis changes. | Connect reindexing to permutation matrices, compose gates in chronological order, and join the result with small-width and explicit counterexample branches. |

Both have provisional **D3** construction levels. LA006 supplies 7
obligations and LA013 supplies 9. Their longest supplied obligation chains
have 3 and 4 nodes respectively. These are evaluator-supplied AND graphs,
not extracted Lean proof-term graphs, measured model reasoning depths or
counts of independent questions.

The library offers shortcuts for individual subclaims. The complete roots
also require the requested boundary statements and counterexamples. The
constructed reference route and library-assisted control are disclosed under
the same proposition; a theorem call is not automatically a process-reward
label or evidence that the model can explain the construction.

## Use the cumulative training and evaluation interfaces

Run from the repository root. Choose fresh output paths.

```sh
python benchmarks/quantumcomputingbench/scripts/lean_course_v6.py audit
python benchmarks/quantumcomputingbench/scripts/lean_course_v6.py export --help
python benchmarks/quantumcomputingbench/scripts/lean_training_v6.py --output course-v6-train.json
python benchmarks/quantumcomputingbench/scripts/evaluate_course_v6.py --help
```

The course exporter selects a split, construction band, `root_only` or
`proof_dag` mode, and `closed_book` or `approved_interface` exposure. It
projects questions and formal obligations without reference proofs.
`lean_training_v6.py` exports whole-root references for the 16 train cores
only. The remaining 4 dev and 5 public-test cores retain their old splits.

`evaluate_course_v6.py` fixes selection to the qualified v6 registry. Use
`plan` before a bounded `run`; real formal proof evaluation requires an
accepted isolated verifier and explicit model authorization. `run-fixture`
checks the protocol using synthetic responses and does not count as a
successful mathematical proof or model result. Public documentation does not
authorize running arbitrary generated Lean on the host.

Historical course v4, course v5 and assessment-study fingerprints remain
unchanged. The new v6 registry has its own identity. It is **not** the
family-withheld sparse-address or assessment-v3 training profile.

## Mathematical and exposure boundaries

- For LA006, `r < N` guarantees a repair for every prescribed frame. It is
  not necessary when the full frame already has determinant +1. The
  positive-dimensional reflection counterexample does not apply to the
  empty matrix, whose determinant is 1.
- For LA013, zero wires have one basis state. The induced permutation acts
  on both matrix indices; a wire relabeling is not a physical SWAP network.
  At the chosen angle pi, the one-qubit counterexample is an exact matrix
  inequality between matrices differing by a global sign. No physical
  distinguishability modulo global phase is claimed.
- LA006 overlaps public frame-completion and orientation tasks. LA013 shares
  reindexing/permutation mechanisms with public BE111 and LA014 and with
  publicly identified assessment source groups. Report these as related
  mechanism transfer, not unseen-family generalization. No private owner
  questions, references or graders were opened for this review.
- The mathematical explanation, its agreement with the formal statement,
  authored kernel-checked references, and isolated model evaluation are
  separate evidence. No model performance or whole-domain mastery is
  established by this release.

The [exposure review](../../reports/lean-course-linear-circuit-v1/exposure-review.json)
records the public relationships. The
[semantic comparison](../../reports/lean-course-linear-circuit-v1/comparison.json)
binds the actual canonical questions, anonymous formal reconstruction and
retrieval interfaces. The
[reference replay](../../reports/lean-course-linear-circuit-v1/reference-checks.json)
binds exact committed pipeline bytes, targets, proofs and runtime identity.
Author-time `pending` fields in the fixture record its preparation stage;
the separate qualified receipts determine admission to this course.

## Continue the curriculum

Choose new tasks by mathematical skill and source relationship, not by
enumerating arbitrary graph paths. Preserve the shared NL/Lean core contract
and family exposure labels. Explain dimensions, premises and counterexamples
before exposing implementation details.

The current 53 Quantum Information cores are anchored to planned concept
nodes rather than admitted compiled declaration anchors in this snapshot.
They guide a future library and snapshot extension; they cannot be relabeled
as checked Lean course tasks by adding metadata. This is an admission gap,
not a mathematical refutation of those questions.
