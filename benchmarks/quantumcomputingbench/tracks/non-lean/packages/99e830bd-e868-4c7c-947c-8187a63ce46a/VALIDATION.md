# Validation evidence and limits

The required checks ran with Python **3.11.17** in an isolated Python environment,
using the repository's declared `jsonschema==4.26.0`. No Lean installation or
execution was needed. Final unit reruns included all twelve additive proposal
wrappers. Logs and exact command/executable/environment/timing records are retained.

| Command or check | Observed result | Evidence |
| --- | --- | --- |
| `python -m unittest discover -s benchmarks/quantumcomputingbench/tests -v` | 317 tests passed, exit 0; final rerun 220.875 seconds wall time | `evidence/final-benchmark-unittests.log`, `evidence/final-unittests.json` |
| `python -m unittest website.scripts.test_quantumcomputingbench -v` | 25 tests passed, exit 0; final rerun 54.138 seconds wall time | `evidence/final-website-unittests.log`, `evidence/final-unittests.json` |
| `python benchmarks/quantumcomputingbench/scripts/curriculum.py validate` | Exit 0; current 198-core registry and reserved identities retained | `evidence/curriculum-validate.log`, `evidence/integration-checks.json` |
| Current registry export | Byte-identical to baseline; SHA-256 `04bd3535f58758587ee742c54caa7af45481340634991cc2079a994898ed3096` | `evidence/integration-checks.json` |
| Current reader export | Byte-identical to baseline; SHA-256 `e5fc1a5673670168eaa2d980612cb38e3aa6277fe71f4a095ebc03fa4b8d1923` | `evidence/integration-checks.json` |
| Cohort integrity/compatibility | Passed; 12 proposed packets checked, zero new cores admitted | `evidence/package-integrity.json`, `evidence/package-integrity.log`; final manifest binding repeated in delivery receipt |
| Changed-path preservation and patch application | Exact changed paths and delivery-time application result recorded separately | `evidence/preservation.json`, delivery-level `DELIVERY.json` |
| Git whitespace check | One retained warning in the original failed-test raw log; non-log contribution files pass | Delivery receipt preserves the exact full-check result; raw execution evidence is not reformatted |

The exact integration export commands, including their temporary output paths,
are in `evidence/integration-checks.json`. Final wrappers bind the three real
comparison reports and all twelve final payload digests. Current reader output
was regenerated outside the repository; no canonical export was replaced.

## Retained environmental failure

The first benchmark run reported one failure and fourteen errors because Python's
temporary-directory fallback landed inside the repository under this sandbox.
The unchanged runtime correctly rejected raw fixture outputs there. That original
log and result are retained as `benchmark-unittests-initial.log` and
`required-tests-initial.json`; they are not recast as a pass. A writable external
`TMPDIR=/workspace/scratch/f6570265c32b/qcb-test-temp` fixed the execution environment.
The corrected initial rerun and the final post-proposal rerun both passed.
No validator or test was weakened. Existing evaluator tests use their mock/fixture
paths; no model inference, training, container or paid API run occurred.

The retained initial log has one trailing space on the interrupted test-progress
line 85. The full Git whitespace check reports that fact. Its bytes are preserved
as execution evidence; the warning is not relabelled as a pass. The generated
Markdown's extra final blank line was corrected in the renderer, and the remaining
non-log contribution files pass the whitespace check. Neither change alters any
mathematical payload or repository validator.

## What the checks establish

The repository checks establish compatibility with the current formats and
policy-resolved registry. The package checker additionally verifies file hashes,
source bytes, graph membership, preserved existing contracts, candidate shape,
rubric totals, reasoning-step references, question-freeze continuity and actual
review content bindings. It invokes the repository's source-binding validator.
These checks do not prove the answers or grade their usefulness. Mathematical
findings and their limitations belong to the substantive review reports.

All required Python commands were available and executed. A new Lean/kernel
check, complete paper-source seal, browser/deployment check, stable-release gate,
model evaluation, empirical difficulty/rubric calibration and human approval were
not run or claimed. Push/PR access was unavailable (`push: false`), so the
requested archive-and-patch fallback is used. No hosted Goal API was exposed.
