# Apache 2.0 and reuse entry: documentation verification

Base: `4e2c5b2` (main, 2026-10-23). Branch: `docs/apache-reuse-20261103`. Canonical public project: QuantumComputinglib-QuantumComputingBench. No Lean source, benchmark answers or mathematical completion status changes are included.

- LICENSE is the unchanged Apache Software Foundation LICENSE-2.0.txt from https://www.apache.org/licenses/LICENSE-2.0.txt. SHA-256: `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` (11,358 bytes).
- LICENSE-MIT retains the previous root license. NOTICE and LICENSE_SCOPE.md distinguish project-owned distribution, retained MIT contributions, external content and their respective reuse conditions. Current dataset cards and contributor policy are synchronized. Historical frozen release evidence remains unchanged.
- Renderer compilation passed. Focused checks verified the standard license digest, retained MIT text, every scope paragraph and actual attribution-section rendering.
- `python -m unittest website.scripts.test_site_contracts`: 54 tests passed.
- The full website command `python website/scripts/build_site.py` correctly refused publication because this fresh workspace has no `_out/lean-gate.json` certifying its current checkout. No report was fabricated or borrowed from the research checkpoint.
- A documentation-only preview of the actual attribution-section output was inspected in headless Edge at 1440 and 390 pixel widths. It is readable with no document horizontal overflow. This preview stubs the common template; it does not certify full-site layout, links, Lean verification or deployment.
- `git diff --check` passed.

The complete `lake build`, `lake build Tests` and `bash scripts/build-all.sh` remain pre-merge gates. This increment is a reviewable documentation branch, not a main release. All prior benchmark admission, source-rights, answer-review and formal-verification boundaries remain intact. No license change certifies an answer or imports external source text into the Apache grant.
