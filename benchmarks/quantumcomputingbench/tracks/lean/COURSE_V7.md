# Lean course v7: circuit foundations

Course v7 extends [course v6](COURSE_V6.md) with four existing mathematical
cores. Their question contracts, IDs, family labels and splits remain fixed.
The cumulative course contains 29 cores: 18 train, 5 dev and 6 public test.
No canonical core or native Lean admission is added by these companions.

[Explore circuit foundations](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/lean/circuit-foundations/) ·
[Download the cumulative course](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/run/course-v7/)

## Mathematical learning objectives

| Core | Split | Level | What the task asks |
| --- | --- | --- | --- |
| LA004 | Public test | D1 | Derive joint-register dimensions, ordered indexing and the equivalence of two projection representations at an arbitrary selected signal branch. |
| LA007 | Dev | D2 | Derive matrix action on a two-term state and the single-coordinate formula; establish exactly which columns or entries suffice. |
| LA017 | Train | D2 | Show the raw controlled bit action is involutive with target-control separation; handle repeated controls. |
| LA018 | Train | D2 | Construct a concrete invalid-control collision and show failure of injectivity and involution. |

These levels describe one authored proof construction, not measured model
difficulty. Available imported lemmas can substantially shorten tasks. For
LA018, the raw basis action is defined even when the target is reused as a
control; this is not a claim about a well-formed reversible gate constructor.
LA007 is about the stated sparse input, not a universal cost bound. LA004
does not require the selected signal value to be zero.

## Training and evaluation interfaces

From the repository root, choose fresh outputs:

```sh
python benchmarks/quantumcomputingbench/scripts/lean_course_v7.py audit
python benchmarks/quantumcomputingbench/scripts/lean_course_v7.py export --split test_public --output course-v7-test.json
python benchmarks/quantumcomputingbench/scripts/lean_training_v7.py --output course-v7-train-references.json
python benchmarks/quantumcomputingbench/scripts/course_task_v7.py package --view qcb-course-la-004-v1 --mode root_only --output la004-task.json
python benchmarks/quantumcomputingbench/scripts/course_task_v7.py verify --input la004-task.json
python benchmarks/quantumcomputingbench/scripts/evaluate_course_v7.py run-fixture --view qcb-course-la-017-v1 --episode-dir course-v7-fixture
python benchmarks/quantumcomputingbench/scripts/evaluate_course_v7.py --help
```

The exporter separates the train, dev and public-test inputs. It also selects
construction band, `root_only` or `proof_dag` mode, and `closed_book` or
`approved_interface` exposure. The distinct train-reference exporter projects
only authorized train cores. The v7 selection and registry are versioned;
earlier courses and sealed assessment profiles remain unchanged.

The single-task package binds the exact question, library revision, toolchain,
proof-input digest, observation/response condition, limits and scoring
contract. This is a portable task specification, not a running verifier
container or an assertion of Harbor compatibility.

`run-fixture` exercises the evaluation protocol using a synthetic provider;
it is neither a Lean proof nor a model performance result. Real model proof
evaluation requires explicit operator authorization and an accepted isolated
verifier profile; this document does not authorize execution of arbitrary
model-generated Lean on the host.

## Evidence and exposure

The [independent source and public-exposure review](../../reports/lean-course-circuit-basics-v1/source-and-exposure-review.json)
reconstructs the mathematical requests and identifies related public families.
The [source-aware comparison](../../reports/lean-course-circuit-basics-v1/comparison.json)
binds an independently decoded exact formal context to the canonical
mathematical requirements. The [authored reference receipt](../../reports/lean-course-circuit-basics-v1/reference-checks.json)
binds the exact pipeline, positive proofs, independent whole-root replays,
wrong-target and incomplete-proof rejection controls, toolchain and axioms.
The [course manifest](curriculum/course-v7.json) records exact anchors and
evaluator-supplied proof DAGs. Its graph lengths are not observed reasoning
depths.

The course is public: related mechanisms and source proofs, including the
LA004 and LA007 target families, are exposed. LA017 and LA018 belong to a
related train mechanism. Public test is not a secret or unseen-family test;
use the separate owner-sealed profiles when appropriate. No human expert
approval or model mastery claim follows from these agent reviews and Lean
checks. Mathematical explanation quality remains separately assessed.

## Next coverage checkpoint

Follow [the benchmark standard](../../BENCHMARK_STANDARD.md), using graph
mechanisms rather than treating every declaration or import edge as a question.
The next candidate group should audit LA008 (clean-block representation
equivalence), LA009/LA010 (isometry dimensions and padded embedding), and
LA015/LA016 (rotation distance and phase boundaries). These are existing cores,
not admissions. Check family overlap with prior courses, workbook and owner
assessment metadata before selecting tasks. Reuse shared basis/circuit
semantics, then connect to actual preparation and controlled-block interfaces.
The wider quantum-information and scientific-computing areas still require
source-supported train/dev/test families and formal adapters where needed.
