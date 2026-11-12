# Temporary AND: exact branch cleanup, isolated local proof

Status: `PROVED_LOCALLY_ISOLATED_NOT_ADMITTED`. On Lean 4.33.0 the actual
component roots compile and report only `propext`, `Classical.choice` and
`Quot.sound`. No production Lean module, verifier, scoring, target or frozen
historical record is changed. Independent source/formal review is pending.

The source is Methods Eq. (12), physical page 9 of
[Gu, Kemeny, Yelin and Lukin](https://arxiv.org/html/2610.22367v1), who credit
[Gidney, *Halving the cost of quantum addition*](https://arxiv.org/abs/1709.06648).
This is a formalization of the displayed cleanup algebra, not a new MBU method.
The Gidney citation is bibliographic provenance from reference [29]; its full
paper has not been audited in this packet. Source pages/figures are not copied.

`SOURCE.md` and `STATEMENT_SEAL.json` are the unchanged pre-proof contract.
`TemporaryAnd.lean` reuses ASPBE's actual `hadamardMatrix` and proves:

- Exact corrected branch amplitudes for either measurement outcome, arbitrary
  complex amplitudes and an arbitrary retained reference carrier.
- A reset output coordinate equal to zero on every nonzero-amplitude branch.
- Branch squared mass equal to half the input mass; normalized input gives
  outcome weight one half, and both weights sum to the input mass.

The unnormalized branch factor sqrt(2)/2 is retained explicitly. This is a
finite-amplitude calculation of a measurement bra/reset and conditional CZ,
not a new global channel API or an emitted hardware-gadget verification.
The input embedding already places the measured wire at the CURRENT AND of
the retained controls. The theorem does not clear arbitrary garbage after
those controls, the coefficient function or the live workspace have changed.

Both recorded attempts compiled. The first contained a redundant trailing
`ring` tactic and emitted unused/unreachable-tactic warnings. The second only
removed that dead tactic and compiled without those warnings. Their exact
sources, hashes, elapsed times and axiom observations remain separate.
Inherited dependency caches were used; no clean transitive rebuild is claimed.
No finite simulator experiment is substituted for the symbolic theorem.

The source graph's inverse-Toffoli alternative remains visible. No Toffoli,
depth, qubit, feed-forward, physical-reset or finite-bit resource theorem is
proved here. Gaussian lookup/modified-coefficient phase correction, its full
all-record cleanup/liveness and numerical error, the paper's reported resource
point, SP/BE consumers and Hermite's finite-bit root all remain OPEN.

Run the integrity/finite regression tests with `python -B -m unittest discover`
in this directory. To compile the isolated Lean file, use the existing project
Lean 4.33 environment and a NEW output directory; record the real command,
input hashes, exit, type and axiom output. Do not import it as an admitted
canonical library primitive until its independent and integration gates pass.

Rollback: remove this isolated package and its new references. Production
behavior remains unchanged; preserve these observations as historical evidence.
