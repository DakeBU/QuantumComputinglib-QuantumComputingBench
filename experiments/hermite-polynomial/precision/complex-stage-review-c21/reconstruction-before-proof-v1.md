# C21 independent pre-proof reconstruction

Reviewer identity: /root/complex_transport_review_c21. This record was written after reading the frozen interfaces and original SP-HERMITE-POLY-002 contract but BEFORE reading ComplexStageTransport.lean or its proof bodies. No source-blind public review credit is asserted.

For width w let N=2^w, with q0 the least significant bit. The whole terminal carrier is C^N, not the clean sector. A saved instruction list is chronological. RY(theta) acts by [[cos(theta/2),-sin(theta/2)],[sin(theta/2),cos(theta/2)]] on each target-bit pair and preserves every spectator pattern. CX(control,target) maps x to x xor 2^target when control is set. These are the literal existing primitive gates, without a global-phase quotient. The empty width-zero circuit is the identity on C^1.

Run the actual interval word from intervalIdentity, taking each final midpoint only after the complete stage. Let A be that rational midpoint matrix cast to real then complex and reindexed by the existing primitiveBasisLEEquiv. Let U be literal evalPrimitiveCircuit(compileWord word). Every complex entry A-U has imaginary part zero and absolute value bounded by the corresponding actual interval radius, hence by r=maxRadius of the whole final interval matrix. The actual stage eta is N*r, not a replacement error witness.

For arbitrary complex x (including independently nonzero real and imaginary coordinates), triangle inequality and real Cauchy-Schwarz give |((A-U)x)_i| <= r sum_j |x_j| <= r sqrt(N) ||x||. Summing N row squares yields ||(A-U)x||^2 <= N^2 r^2 ||x||^2; r>=0 then gives induced Euclidean operator norm <= N*r. This is the Frobenius-style dimension-aware estimate; an entry radius alone is not an operator bound.

U is unitary because it is the literal product of existing RY/CX primitives, so ||U||<=1. Interval enclosure implies eta>=0. Consequently actualComplexStage(stageCenter,stageEta) must derive NonunitaryTransport.Valid internally from eta nonnegativity, contraction and actual operator error. No supplied Valid, error bound, contraction, inverse, real-input-only or clean-ancilla assumption is allowed at the actual-stage roots.

For chronological stages U1,...,Um the literal flattened circuit is Um...U1. The midpoint product follows the same later-left chronology. Applying the nonunitary product recurrence gives ||Am...A1-Um...U1|| <= product_s(1+eta_s)-1. On arbitrary complex x this multiplies ||x||. Empty stages and width zero remain included.

Required adversarial finite screens: non-real complex inputs; negative theta where sine sign matters; all ordered distinct CX wires and every spectator pattern; reversed CX direction must differ somewhere; noncommuting chronological stage reversal must differ; width-zero identity. These are finite diagnostics, not uniform symbolic evidence.

The original scientific target remains normalized sampled g_k at p_j=-pi L+2 pi L j/2^n, not midpoint circuit action by definition. This internal transport alone does not prove angle/input production, physical stage lifting, uniform family epsilon/resource allocation, finite-bit runtime, full QR, ROOT closure, production admission or PURIFIED reader state.
