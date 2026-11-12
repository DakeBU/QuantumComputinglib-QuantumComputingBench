# Lean QA coverage audit

Run the audit from a full repository checkout. The output binds the current
reader catalog, frozen graph snapshot, course index and public assessment
seals.

```sh
python benchmarks/quantumcomputingbench/scripts/lean_qa_coverage.py \
  --output lean-qa-coverage.json
```

The baseline at `53415ae` has 198 canonical mathematics cores. The 21 course
cores and three native Lean views together cover 21 distinct cores. Ten course
cores are in state preparation, ten in block encoding and one in foundations.
Public diagnostics and the owner-sealed assessment contain 16 and 18
propositions respectively. Several propositions can share one mathematical
core or source group.

The snapshot lists 3,548 closed compiled declarations. For each source file,
the audit counts citations from the course, public diagnostics, sealed
assessment and natural-language workbook. It also lists nearby canonical
cores by exact graph identity. Use these counts to locate areas for review.
An anchor records a relationship between a task and its source. The
mathematical operation required by the task and the sufficiency of its
premises require separate review.

Course v5 adds Hamiltonian phase conventions and Hermitian structure. The
owner-sealed sparse-address study adds a separate evaluation group. Use
`--expanded` to require both qualifications and map the updated public
coverage. An owner can additionally supply `--owner-bank` and write to a
private output path to count the sparse study's compiled citations.

Use the uncovered declaration counts to shortlist modules, then look for
uncovered skills and relationships inside each module. A useful next round
could pair a direct interface task with a composition or counterexample in
quantum information or quantum scientific computing. The inventory includes
reusable support facts, so it supplies no estimate of unique valid questions.
