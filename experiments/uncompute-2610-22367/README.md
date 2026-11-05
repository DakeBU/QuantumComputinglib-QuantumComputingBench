# Uncompute: first proof-digestion checkpoint

Status: compiled external assets plus independently frozen source mathematics.
This is not local source/formal admission, a new ASPBE theorem, a whole-paper
formalization, a circuit certificate, or PURIFIED exposition.

The author work is Gu, Kemeny, Yelin and Lukin,
[arXiv:2610.22367v1](https://arxiv.org/abs/2610.22367v1).
All upstream inputs are pinned to
[`64b5a13`](https://github.com/andigu/uncompute/tree/64b5a13aa249f1360846657392e6c66817b26d0f).
The original Apache-2.0 license and the MIT safegcd-bounds attribution are
retained in the source archive. No mathematical authorship is reassigned.

## What actually ran

The original `Defs`, `NumberTheory` and `Recovery` Git blobs were compiled,
without source edits, against the installed ASPBE Lean 4.33.0 / Mathlib 4.33.0
context. `Audit.lean` then checked four interfaces and printed their axioms.
The actual type/axiom output and input/compiler-context hashes are retained.
The four reported axiom sets contain `propext`, `Classical.choice` and
`Quot.sound`. This is not a transitive loader or independent proof-term audit.

The first attempt passed `Defs` but stopped at a 1024 MiB interpreter memory
limit in `NumberTheory`. It is retained as environment evidence. The successor
used one thread, a 1536 MiB cap and at least 2048 MiB measured spare-memory
reserve. All three modules and the audit command passed. One upstream `haveI`
style warning was left visible; no linter suppression or theorem edit was used.

## Reproduction

Use the source archive's three files under `lean/divsteps/`, retain both
licenses, and use the exact compiler context hashes in the observation. Put
that source directory on `LEAN_PATH`, then run the installed 4.33.0 compiler
in dependency order with `lake env lean -M1536 -j1`: `Defs`, `NumberTheory`,
`Recovery`, and the supplied `Audit.lean`, writing each module's `.olean` in
the isolated source tree. Do not update the production dependency manifest.
No `.olean` or path-bearing raw compiler log is published in this checkpoint.

Run the evidence regression tests from the ASPBE root:

```sh
python -m unittest discover -s experiments/uncompute-2610-22367 -p 'test*.py'
```

## Reading and remaining gates

The source-first archive covers Appendix A before implementation access.
Its dependency graph is a pending independent-review proposal, not self-approved
topology. The source-first reviewer and a distinct source-blind formal decoder
are now reading the actual formal context independently.

Next: reconcile the literal source, complete formal interfaces and definition
expansions; independently review source topology; build the finite-register,
phase and cleanup bridge to the emitted circuit; charge actual resources.
DQI's separate 4.33.1 artifact, statistical inference, numerical instances and
the native 590-step certificate were not built by this probe.

The full paper remains the target, not just its first decoder batch. The public
[layered research route](https://dakebu.github.io/Quantum-Computing-Block-Encoding/state-preparation-wiki/spw-uncompute/index.html)
keeps the remaining case studies and acceptance layers explicit.
