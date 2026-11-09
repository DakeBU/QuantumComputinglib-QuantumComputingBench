# Validation and reproducibility record

Recorded base: `bb260f4e27360a0d3791b40cb22638af4b086fc9`. The supported interpreter was Python 3.11.17; `jsonschema` was available. Exact timestamps, executable paths and wall times are in the JSON records beside each raw log.

| Command | Actual result | Evidence |
|---|---|---|
| `python -m unittest discover -s benchmarks/quantumcomputingbench/tests -v` | 468 tests passed; 636.835 seconds; exit 0 | [benchmark-tests.log](evidence/benchmark-tests.log) |
| `python -m unittest website.scripts.test_quantumcomputingbench -v` | 25 tests passed; 547.946 seconds; exit 0 | [website-tests.log](evidence/website-tests.log) |
| `python benchmarks/quantumcomputingbench/scripts/curriculum.py validate` | Passed; exit 0; retained catalog hash unchanged; 198 retained cores and 15 withheld identities | [curriculum-validate.log](evidence/curriculum-validate.log) |

The registry and resolved reader were exported before authoring using the exact requested commands. Both succeeded; command lines, output hashes and the reader-policy identity are in `evidence/baseline.json`. These reproducible `_out` exports are not copied into the contribution ZIP. The compact current-question inventory is included.

The 468-test benchmark run started before the six final proposals were assembled; it tests the unchanged repository implementation and its synthetic/mocked fixtures. Final `curriculum.py validate` ran after all six proposals and exact review records were assembled, traversing both tracks' proposal directories. No validator or production implementation was modified. The 25 reader/renderer tests use mock writers and temporary publisher output; they do not deploy or overwrite the repository's generated website.

`curriculum.py validate` checks graph IDs, UUID and contract compatibility. It reports the existing stable-readiness state as false: withheld cores, publication/browser gates and cross-cohort reconciliation remain unresolved. This expected status is not a validation failure and was not changed to obtain a pass. Candidate proposals add zero admitted cores.

## Package-specific integrity checks

`verify_package.py` is read-only. It checks manifest closure and raw hashes; current question/reference separation; exact frozen mathematical fields; full-payload review digests and preserved phase-one seals; source hashes and repository source-binding checks; proposal contracts; frozen node membership; declared map-identifier topology; the prior cohort's 103 bound files; and absence of tracked changes outside this package and its six proposals. Its stdout is saved in `evidence/package-integrity.log` after assembly.

The assembly script is then rerun to bind the validation record itself into the final manifest. The final immutable package is rechecked, committed, replayed from the exact base in a separate checkout, and checked for identical repository-relative bytes. The outer `DELIVERY.json` records the final replay/check results and commit/patch identities; it sits outside the self-hashing package to avoid circular digests.

Author/reviewer finite diagnostics are supporting examples, not exhaustive mathematical tests: they cover the grid witnesses, small modular adders, residual amplification, normalized projection geometry and LCU counterexamples described in their individual evidence records. Their original hashes and scopes are preserved, including the old P2 payload binding before the bounded rubric/map repair.

## Checks not performed

- No Lean installation, execution, kernel replay or new compiled-library verification.
- No model-response collection, scoring experiment, inference/training job or measured-difficulty calibration.
- No browser publication acceptance, website deployment, container, administrator action or stable-release declaration.
- No human expert approval, private-assessment question comparison or global semantic/split admission audit.

Schema and hash checks establish integrity and compatibility, not mathematical truth, reviewer independence, novelty, hidden-evaluation status or admission. All remaining decisions are listed in REVIEW_REQUESTS.md.
