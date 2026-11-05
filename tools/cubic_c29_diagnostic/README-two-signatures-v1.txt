WIP two-signature-only changed-fingerprint supplement; no local Lean run.

Prerequisite: frozen CI3 runtime successor packet
11fd328975b6309685d82335b66e756d95e1a8fd299548fd9c1c92a20f975819
seal c16a18a1266dc5e601be42485b330349c9d464e0f7d0b081cbe5764919ebea09.

Actual CI3 produced U+22EF omissions in binder/data/RHS positions of exactly
two generated thmInfo signatures. This package reads only those actual names,
using the exact same fresh namespace/olean AFTER successful Probe-v5 validation.
It does not recompile the target or print ordinary generated values.

Options supported by installed Lean4.33 source: pp.deepTerms true,
pp.maxSteps 2000000 (finite), maxRecDepth 10000 (finite). Existing explicit/proof/
universe/name settings are retained. Those increased budgets are candidates,
not a claim they suffice. Any remaining U+22EF/U+2026/ASCII ellipsis, wrong fresh
path, missing/duplicate/wrong record, or nonzero exit fails closed with original
raw streams/PID/argv/UTC/wall/exit preserved by the existing native wrapper.
The supplement has no mathematical acceptance or axiom allowlist.

Files: SupplementalTypes-v1.lean, supplemental_types_v1.py,
test_supplemental_types_v1.py, supplemental-pins-v1.json; runner-append-v1.patch
is an unexecuted parent-review integration patch. It adds one serial subprocess
after the existing v5 validation and before inherited provider post-run pins.
No existing driver or validator is edited. No workflow, target, verifier or
scoring change is proposed. The parent owns integration/Git/actual CI.
Existing always-public export automatically sanitizes the new stage logs, with
raw SHA receipts and private original logs retained. No acceptance fields change.

Even a later successful supplement only closes the two captured-text holes;
native compiler/evaluator trust policy, ordinary pretty-value omissions,
provider/loadtrace limits and natural-source/opaque binding remain unresolved.
