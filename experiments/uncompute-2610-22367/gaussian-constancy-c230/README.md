# A symbolic128-block certificate for the fixed integer model

C240 proves the exact C229 preproof-sealed statement, not a sample check:

    forall j D, j<1024 -> D<2^25 ->
      localIncrement j D = localIncrement j (128*(D/128)).

For e>=7, dividing D by2^e is unchanged by rounding D down to a multiple of128.
Hence middle U=D/2^14 is unchanged, as are its six SIGNED separately truncated
rows and the actual modular19-bit slope fold. Every data quotient in the nine
retained final rows has exponent>=7, including index10's special drop. Those
rows keep sign and active-row bias. Congruence on exactly List.range9 preserves
the final sum, so the actual fixed model increment is constant on each block.
No word table is unfolded, no unbounded slope substituted, no full-product
floor introduced, and no nonwrapping/positive-output hypothesis is added.

Actual source12.265s and own-output exact-type/typed-example/axiom consumer
9.859s both exit0; one root has only propext, Classical.choice and Quot.sound.
The parent read the full source/derivation/manifest and actual root type/axioms.
The same author wrote the consumer; independent proof review remains pending.
Five original author members retain their historical uncompiled status. Exact
core/table providers come from the separately typed Gaussian model checkpoint;
the original preproof seal is in its constancy-preproof-seal archive.

This is a genuine all-D INTEGER supplier for a later endpoint-envelope proof.
It does NOT prove any Gaussian real-exp/f64 error bound between endpoints,
source circuit/gadget refinement, phases, cleanup, gate/qubit counts, amplitude
transduction, normalized state quality or an SP/BE resource improvement.128 is
not asserted minimal. Full source/publication/main/PURIFIED gates remain open.
