# First bounded timing observation

The frozen plan was executed with Python 3.12.14 on Windows. All four arms
completed. In launch-order collection, the fast second child's work-finish
sample preceded parent observation by 656 and 671 ms. In ready-first collection,
that interval was 16 ms in both repetitions. These intervals include process
serialization/exit and polling, not only avoidable observation delay.

The whole pair still took 844–859 ms in every arm. This experiment supports
fixing measurement provenance and making completed results available earlier;
it does **not** show less total work, faster mathematical proofs or improved
SP/BE synthesis. The runtime clock reports a 15.625-ms resolution. Sub-tick
claims, full-process CPU claims and a quantum-search speedup are not supported.

The 14 focused tests passed. An initial test incorrectly required killing an
already-exited child on interruption; that expectation was corrected to drain
every owned child and kill only those still running. Production code was not
changed. See `pre-execution-freeze.json` and the additive `observation-1.json`
for exact source/plan binding, timings, unknowns and remaining limitations.

Next decision: retain the existing trusted acceptance boundary. Before any
production adapter, test faithful command/logging compatibility and instrument
completion versus observation separately. Then compare proof-first,
experiment-first and bounded dual-lane execution on matched quantum obligations,
with total work and equivalent evidence strength. A lower-semantic finite
screen must not win merely because it is cheaper than a symbolic certificate.
