# Current-main validation

These commands actually ran on isolated branch
`codex/nonlean-followup-20261104`, based on
`abfd4f5b8b52de29ed0e23f15d355e46f21748df`, with the original contribution patch
applied unchanged. Python was 3.11.17, with the repository's declared
`jsonschema==4.26.0`. A writable external TMPDIR was used.

| Command | Result | Exact evidence |
| --- | --- | --- |
| `python -m unittest discover -s benchmarks/quantumcomputingbench/tests -v` | 367 tests passed; exit 0 | `evidence/benchmark-tests.log`, `evidence/required-tests.json` |
| `python -m unittest website.scripts.test_quantumcomputingbench -v` | 25 tests passed; exit 0 | `evidence/website-tests.log`, `evidence/required-tests.json` |
| `python benchmarks/quantumcomputingbench/scripts/curriculum.py validate` | Passed; 198 retained and 15 reserved cores | `evidence/compatibility.json` |
| Original cohort `verify_package.py` | Passed, including exact source/review/contract bindings and all twelve proposed packets | `evidence/compatibility.json` |
| Original patch applicability on the new base | `git apply --check` and actual application succeeded | Delivery receipt; one known historical raw-log whitespace warning is preserved |
| Nineteen indexed first-cohort source/evidence files | All exact SHA-256 hashes unchanged | `evidence/compatibility.json` |

The newly added upstream test modules were inspected before execution: their
verifier/model branches use mocks or fixtures. No new Lean check, inference,
training, container or paid API was launched. The upstream diagnostic report's
own historical Lean receipts are not represented as execution by this checkpoint.

Original first-cohort logs and manifests remain unchanged and tied to their old
base. The fresh results above are separate. Validation establishes compatibility
and recorded artifact agreement, not mathematical approval, global deduplication,
split clearance, stable-release readiness or empirical model difficulty.
