# Active-walk branch-recovery composition: local proof checkpoint

Status: PROVED_LOCALLY in an isolated Lean 4.33.0 context; independent review
of this new composition is in progress. Not locally admitted, not a whole-paper
formalization, not a finite-width circuit or resource certificate, and not
PURIFIED. No production Lean source or publication record changes.

## The new bounded interface

`ASPBE.Uncompute.recover_zWalk_active` supplies all reachable-state invariants
internally and recovers BOTH the swap flag and incoming parity from the actual
next walk state. Its only logical premises are odd p and current g nonzero.
It handles swap, terminating nonswap, nonnegative-counter nonswap and the
residual negative-counter case together. The decoder uses the author's
determinant-ladder formula only in that last branch. The function's arbitrary
off-domain extension is not attributed to the paper.

The pre-proof statement is retained unchanged. An initial proof attempt failed
because unrestricted simplification rewrote a guard and left a goal unsolved;
it is preserved, not counted as a proved theorem. A successor changed only the
proof to use explicit guarded rewrites. Actual compilation exited0 and the
printed root axiom set is exactly propext, Classical.choice and Quot.sound.
No successful sorryAx claim is made from the failed elaboration.

This is an ASPBE integration of author-proved ingredients, not discovery of
the branch-recovery method. The mathematics belongs to
[Gu, Kemeny, Yelin and Lukin, arXiv:2610.22367v1](https://arxiv.org/abs/2610.22367v1)
and the fixed
[author code](https://github.com/andigu/uncompute/tree/64b5a13aa249f1360846657392e6c66817b26d0f).
Original sources and licenses are in the parent checkpoint's upstream archive.

## Separate independent evidence

The original source-first extraction was independently checked directly
against the full Appendix A. Its complete local topology and76 dispositions
were accepted with explicit unclosed Wuille-bound/primality tails. This is
source-topology evidence only, not compiler or circuit evidence.

For the original upstream Recovery module, a source-first reviewer froze a
whole-target interpretation before reading the actual source-blind decoder.
Their subsequent comparison found substantive mathematical agreement and
exact59-command/header/body/binder capture, but an ambient-context metadata
ambiguity: namespace and ambient-variable fields were static file-level
references even before those commands took effect. Original packets, the
finding, and all seals are preserved. The decoder actor supplied a separately
sealed context overlay, with distinct before/after scopes and unchanged old
values; independent verification of that successor remains pending. No final
module admission is inferred.

A fresh source-blind decoder and a distinct source-first reviewer are examining
the NEW small composition. Their in-progress work is not an acceptance record
and is not included here as one.

## Reproduction and remaining work

Extract the parent checkpoint's fixed upstream source archive; compile Defs,
NumberTheory and Recovery against the recorded Lean/Mathlib4.33.0 context in
dependency order, as described in the parent README. Add that isolated source
directory to the local import search path and compile `WalkRecovery.lean` with
`lake env lean -M1536 -j1`, keeping all outputs outside production sources.
The observation records exact raw inputs, host configuration hashes, actual
compiler version, timing, memory limit/reserve and stdout/stderr digests.
Path-bearing raw logs are private; the published type/axiom text is the
path-free actual successful stdout, not a newly simulated result.

Run `python -m unittest discover -s experiments/uncompute-2610-22367 -p 'test*.py'`
and this directory's corresponding discovery command from the repository root.
These are evidence-integrity tests, not a fresh Lean execution.

Still open: independent admission of this composition and whole source modules,
source EqA6's inverse-power supplier, the indexed A13 history theorem,
independent external590/primality admission, finite signed-register overflow,
coherent reversible implementation, phases/measurement feedback, cleanup and
actual gate/qubit/bit costs. The533-step failure-budget circuit is a separate
contract. Hermite's finite-bit root and the rest of the paper remain open.

The asynchronous SP/BE design in `paper-notes/system-comparisons/` separates
user-owned trade-offs, independent proof/experiment lanes and trustworthy cost
measurements. It does not install a new production scheduler or change scoring.
