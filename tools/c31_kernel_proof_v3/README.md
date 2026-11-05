# C31 kernel proof v3 — shadow-helper fix proposal

This is an ENV/instrumentation successor, not a mathematical verdict. No Lean was run locally; the candidate did not compile in the inspected failed attempt. All acceptance fields remain false/null. The immutable v1 19 files and v2 9 files stay unchanged.

## Actual first failure

`actual-first-failure.json` independently binds the authorized ZIP `7c395ab385ffb36a60b569b8688085155c54e50f3a7acc474e80c24b98ecf732`, all 26 members and 25 public derivative hashes. Actual help PID 12347 and prefix PID 12350 exited 0. `result.json` reports a missing `$CANDIDATE_WORKSPACE/tools/cubic_c29_diagnostic/runner.py`. These members contain no target/collector receipts; this is not a claim about unuploaded filesystem state. Parent-provided job/run labels are 117272066142 / 38990641927, not independently fetched API metadata or an executed-checkout attestation.

The earlier temporary `load_shared` callback fixed execution origin only. It did not satisfy the unchanged base runner's shadow `verify_pins`. That scope gap is retained, not retroactively reclassified as a mathematical failure.

## Exact delta

`entry.py` forks the small v2 guard rather than importing its `run`. Its actual `__file__`, argv0, `__main__.__file__`, current SHA and the same three actual loaded v1 module objects/paths/SHAs remain checked. The new hook calls byte-unchanged v1 `prepare`, then exclusively copies only the fixed shared helper from the original project into the identical shadow relative path. Both sides must equal SHA `61733fc92f5e99672e0ce0260ff397e07c94a349e98e12c48dd6a3171d5a75d9`; unexpected paths, preexisting destinations and drift fail closed. It records UTC, wrapper PID, bytes, actual source/destination and before/after hashes in `shared-helper-copy.json`. The copied helper is data, not imported or executed. The original pinned API remains the execution source.

The typed copy row is appended to the existing recheck vector (the legacy enclosing key is `providerSeedCopies`; this extra row explicitly says it is NOT a provider artifact). Existing `revalidate` checks both endpoints before/after every child through unchanged `base.recheck_rows`; unchanged `base.run` also checks the shadow helper pin. No old pin check is removed.

Candidate bytes, raw87 profile, collector, baseline/comparison, actual-generated discovery, finite CI4 Linux gate 5120+2048 MiB, threads1, no fallback and whole 2100-second boundary are unchanged. Source-file/object checks are observations, not OS/code-object attestation.

## Parent installation and rollback

After full parent review only, install this package at `tools/c31_kernel_proof_v3/` alongside the unchanged full v1 package and existing runtime packages. The sole optional execution-command delta is from `tools/c31_kernel_proof_v2_guard/entry.py --project .` to `tools/c31_kernel_proof_v3/entry.py --project .`, under the same existing `lake env python` invocation. No workflow file is supplied or changed here. The public artifact path stays `_out/c31-kernel-proof-v1/public`; raw receipts/host paths stay private. The old exporter creates separately hashed logical-path derivatives. The new receipt uses existing `$PROJECT` / `$CANDIDATE_WORKSPACE` redaction without altering raw hashes.

Rollback is that one execution-command reversal; hooks also restore in `finally`. Do not delete/reuse old failed outputs; runtime output remains exclusive, so a next actual job needs a fresh checkout/output. Reversal restores the known old failure, not success.

## Reproduction and remaining boundary

`build_profile.py BASE_V1 PREVIOUS_V2` writes a new profile only. `verify_failure.py AUTHORIZED_ZIP` writes the bounded failure analysis. `freeze.py BASE_V1 PREVIOUS_V2 PROJECT` runs Python tests, records the actual Python PID/exit/timeout/output digest, rechecks old files and freezes this allowlist. Fixtures are exclusive temporary files. One test exercises real old 31-input prepare and collector copy, with provider binary seeding explicitly stubbed. No native-call test or Lean compilation is claimed. Remaining risk is unexecuted Linux/Lean integration, candidate proof compilation and actual generated comparison.

All seal-allowlisted files are public-safe technical source/derivatives with logical paths. No author natural source, reviewer report, registry or other decoder mathematics was read for this fix. The immutable v1 candidate transport contract is unchanged: its private-review label was scope isolation, not confidentiality.
