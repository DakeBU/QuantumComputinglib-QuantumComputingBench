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

Two candidate areas for the next tranche are the phase conventions and
Hermitian structure of the Hamiltonian construction, and the scope of
reversible banded sparse address access. The audit records their compiled
source declarations and existing coverage. The admission decision also
depends on exact statement alignment, replay evidence and the overlap of
assessed reasoning with available training examples.
