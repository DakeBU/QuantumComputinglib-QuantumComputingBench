# Parent review handoff

Only a new C staging proposal. Read POLICY-RATIONALE.md, resource-contract.delta.patch, resource_gate_v4.py and runner_v4.py completely. Verify ci4-bindings.json and ci4-seal.json against every allowlisted byte, then run test_ci4.py with C31_TEST_PROJECT pointing at the repository. No raw CI metadata is required or authorized.

Prior actual failure: self reserved-init readlink succeeded; PID1 access failed; no native child or complete gate. PID1 is removed from the new mandatory contract because task self reserved-init fingerprint already identifies initial cgroup namespace in the explicitly recognized upstream implementation, not because a permission failure is acceptable evidence. CI4 does not read, infer or fabricate PID1's namespace. The implementation/OS trust residual is unchanged and documented, not silently upgraded to a proof of the deployed kernel.

Budget and all inherited formal collection boundaries remain. Exact executed checkout SHA is unasserted: artifact context SHA and parent-reported official API head are distinct attributed observations. The 31 source/config hashes are verified independently.

No tools/workflow/production/canonical installation or edit, Git, Lean, push, CI trigger, or extra filesystem read outside authorization was performed. Parent owns review, installation and any next execution. STOP after this freeze.
