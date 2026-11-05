# Actual cached middle: partial scalar/word cost

Status: proved_locally under Lean4.33.0, independent review and admission pending.
The exact sealed theorem bounds actual middleFromCache cost by400*(k+1)^2 for
all natural k and arbitrary signed rational e/coefficient vector a, without a
new public assumption. Source compile24.922s and exact own-output type/axiom
consumer23.093s passed; the root uses only propext,Classical.choice,Quot.sound.
These are recorded subprocess times, not total workflow time or peak memory.

Writing W=k+1, actual factorial generation contributes <=320W^2, weighted sign
and coefficient work <=14W^2, both guarded convolution sums and stored output
<=50W^2. Their composition <=384W^2 implies the unchanged400W^2 bound.
Each sum includes its final addition to zero, and collect retains4n traffic.

The first C176/C182 attempt failed three proof-normalization obligations in
27.797s. The ten original author/failure/repair members are preserved exactly.
The successor selects dependent guards before broad simplification and matches
the same table callback normalization before arithmetic. It changes no producer,
target, guard, budget or public premise. Three original linter warnings remain.

This is ONLY the eight-counter annotation, not native Rat bit/GCD/CPU costs,
physical gates, complete classical work, sharing or a complete SP certificate.
Outer source-cache, actual rightSetup and the same returned full-chain cost
remain separate obligations. Kernel/left AND captured actualBlocksQ setup remain
unaccounted; full finite-bit/synthesis/executable scientific ROOT remains OPEN.
No clean transitive TCB, independent rerun, ProofSeal or main admission follows.
Resolve providers from the pinned C150/C155/C156/C157/C159 context; no production
lake target or production controller/scoring/verifier has been changed.
