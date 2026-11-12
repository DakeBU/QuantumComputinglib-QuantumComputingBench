# Lean QA v5

The course adds two public training companions to existing question cores.
Both are D3 construction tasks. The band describes the supplied mathematical
construction, and solver difficulty remains unmeasured.

| Core | Mathematical task | Lean proof structure |
| --- | --- | --- |
| BE011 | Track a sign in the Hamiltonian block formula, show when it changes the matrix, and justify the phase repair. | Establish the diagonal discrepancy, check the repaired block and preserved entries, and combine the clauses under their respective premises. |
| LA019 | Prove Hermitian closure for the tensor construction and exhibit a finite counterexample when one factor lacks Hermiticity. | Combine tensor and identity facts with closure under addition, and join the universal result with a separate counterexample. |

The [v5 plan](curriculum/course-v5.json) records graph anchors, the shared
contract and split, supplied proof topology and construction band. The
[qualification evidence](../../reports/lean-course-hamiltonian-v1/) records
the independent reconstruction and source comparison, authored obligation
checks, fresh whole-root replay, standalone controls, and wrong-target and
forbidden-axiom rejections. These checks cover the stated formal clauses.
The accompanying mathematical explanations and rubrics have their own review.
Full imports expose library facts and possible shorter proof routes.

## Training and evaluation

```sh
python benchmarks/quantumcomputingbench/scripts/lean_course_v5.py audit
python benchmarks/quantumcomputingbench/scripts/lean_course_v5.py export --split train --output course-v5-tasks.json
python benchmarks/quantumcomputingbench/scripts/lean_qa_training.py --output sparse-study-train.json
python benchmarks/quantumcomputingbench/scripts/lean_qa_coverage.py --expanded --output coverage-v5.json
```

The paired train projection combines the previous public corpus and both
Hamiltonian Lean references. It withholds BE101, BE102, BE104 and LA020 across
their views because they teach closely related sparse-access, register and
nonwrapping arithmetic mechanisms. The exact [training profile](assessment-sparse-v1/training-profile.json)
binds the retained rows and records the audit scope. Public library and workbook
exposure is possible. Model pretraining exposure is unknown.

The separate sparse-address assessment has four owner-only propositions in two
balanced contrasts and one shared exposure group. It exercises premise
boundaries and transfers source-level reversible access facts into local
proofs and counterexamples. Each Lean reference establishes the exact
decision polarity of its fixed proposition. The assessment leaves canonical
IDs and splits intact. Four correlated results do not give four independent
measurements.

An operator with the sealed bank uses the same offline workflow for each run.

1. `sparse_assessment.py prepare` takes `--bank`, `--student` and
   `--controller`. Keep the bank, private grader, and answer-free student
   directory disjoint.
2. `freeze --responses ... --output ...` locks the first decisions and
   explanations before review. Keep the original lock.
3. `review-template --locked ... --output ...` prepares private mathematical
   rubrics. `score --locked ... --reviews ... --evidence-kind operator_supplied
   --output ...` reports decision and reviewed argument outcomes over all four
   planned questions. Pass the same three layout arguments to each command.
4. `formal-challenges --locked ... --output ...` prepares exact Lean targets
   selected by the student's recorded belief in a separate directory. Candidate
   proof execution requires an accepted isolated verifier.

The qualification concerns inspected authored references on the pinned local
Lean runtime. No real model was scored. The course and sparse study add
evidence for specific contracts and leave whole-graph coverage and empirical
difficulty open.
