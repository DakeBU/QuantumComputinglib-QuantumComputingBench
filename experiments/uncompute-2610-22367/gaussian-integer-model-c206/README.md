# Gaussian witness: exact integer model, not a circuit certificate

This packet follows the fixed upstream64b5a13 witness, not a new fit/search.
Read the scalar spine before the files:

    signed39-bit promise -> fold negative X to-X-1 -> literal55-bit table
    -> six signed, separately truncated middle rows, modulo stored19bits
    -> nine separately truncated/bias final rows ->(k+128*A-P)mod2^39.

Every one of1024 reachable words matches the fixed source:514 literal cases,
then510 zero words. Correction is signed11-bit times256, not E padded with0.
Negative shifts floor; row biases survive below data cutoff; the final row
has a different drop. Replacing these rows by a full-product floor is wrong.
The two source-level warnings are about schematic README equations/wording,
not newly found implementation bugs or evidence against the quantum method.

C228 actually typechecks table2.641s, core5.578s and own-output checks5.343s
under Lean4.33.0.31 named types and six loaded definitions were inspected.
These are DEFINITIONS ONLY: no theorem closure or axiom-clean root is claimed.
C225's original missing-Decidable failure remains exact. The successor adds
only a local constructive decision for the unchanged two integer inequalities,
not classical choice, a new global instance or an oracle/hypothesis.

Three independent freezes remain separate: C213 source-first before author
exposure; C221 original code/table static comparison before diagnostics;
C231 successor-only static comparison before runtime exposure. Neither static
review claims compilation or successor import-provider inspection. The parent
owns actual type checks; this does not fabricate an independent runtime review.

The author's81 local pairs/eight signed inputs/arbitrary-k boundary diagnostic
is parent-replayed exactly. It has no floats/exp/circuit tests and is NOT a
uniform error proof. Two full-product substitutions fail; negative fold seams
are retained. C229 seals an exact128-aligned-block constancy proposition before
any proof search; its original type probe is saved, not a proved theorem.

Still OPEN: formal row/lookup/circuit refinement; Gaussian real-exp and original
operational-f64 reference/rounding error; phases for every measurement record;
workspace/alias cleanup; emitted operations/Toffoli/qubits; amplitude conversion,
normalization/success/amplification and SP/BE integration. Author1583/139 counts
are not local certificates. See original MODEL in the immutable author archive
for the complete dependency map and its historical pre-typecheck status.

Apache-2.0 LICENSE and NOTICE accompany transported literal data and modified
scalar transcriptions. No upstream fitting, recenter search or simulator runs
were executed. This is a WIP experimental checkpoint, not production or main
publication/ProofSeal/PURIFIED status or a new resource-record claim.
