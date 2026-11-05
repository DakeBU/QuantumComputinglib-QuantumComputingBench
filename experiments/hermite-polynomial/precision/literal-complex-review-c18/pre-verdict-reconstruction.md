# Independent c18 pre-verdict reconstruction

This file is frozen before reading result-v1.json, handoff-v1.json, statement-seal-v1.json, author's gates or discriminators. Reviewer: /root/literal_complex_review_c18. Scope: internal exact operator bridge only. No Git or production writes.

The raw producer has carrier Fin(2^width), bit(q,i)=testBit(i,q), flip(q,i)=i xor 2^q. low clears the target bit; high sets it. A rational-angle RY row update is (cos(theta/2)u - sin(theta/2)v, sin(theta/2)u + cos(theta/2)v), including negative angles. CX c t h permutes rows according to target XOR control, with h:c!=t required for involution. The foldl interpreter executes the first list instruction first on every column of an arbitrary input matrix.

Necessary correspondences independently derived from these bodies and the canonical providers:

1. E=primitiveBasisLEEquiv must encode b as sum_q b(q)*2^q. Its recursive value equation b(0)+2E(tail) confirms q0 is LSB; induction on width/testBit proves each coordinate.
2. E^-1(low(q,i)) is splitPrimitiveWire(q)^-1(0,spectators(E^-1 i)); similarly high uses 1. Every other named coordinate is retained, not traced out or restricted to a clean sector.
3. E^-1(cxRow(c,t,i))=cxBasisAction(c,t,E^-1 i). Canonical permutation multiplication uses the inverse row action. The existing cxBasisEquiv inverse is the same action only under h:c!=t. No control/target exchange is licensed.
4. Existing standardRyMatrix(theta)=realRotation(theta/2) has rows (cos,-sin),(sin,cos). Its Kronecker identity over all OtherPrimitiveWires ensures the exact full terminal carrier, arbitrary spectator patterns and arbitrary columns match the producer's row update.
5. The real inclusion into C preserves addition/subtraction/multiplication. For arbitrary real m, namedCast(realStep(g,m))=evalPrimitiveGate(compile(g))*namedCast(m). This is stronger than agreement on identity or a selected basis input.
6. Induction on the chronological list, using associativity, gives namedCast(realWord(word,m))=evalPrimitiveCircuit(compileWord(word))*namedCast(m). Reindex by E gives the advertised arbitrary-input root; m=identity gives the whole matrix root. Consequently arbitrary complex vectors are admissible downstream, even though the input-matrix producer is real.
7. Width zero has one basis coordinate, no valid instruction and therefore only an empty word. Its matrix is 1, not an empty matrix.

Binder audit: width/word/m are typing and literal input data; angle rational and valid wire indices are the existing language contract; CX distinctness is necessary and supplied in each instruction. There is no premise asserting equality, enclosure, normalization or correctness. Definitions compileInstruction/map/cast/reindex are literal transformations; no new carrier, phase quotient, representative choice or fallback is introduced.

Source topology: bit encoding AND target/spectator splitting AND inverse CX action AND signed half-angle RY AND real scalar inclusion => one-instruction operator equality => word induction => identity-input full matrix equality. The existing interval enclosure is a separate upstream dependency consumed only after this exact bridge. Norm bounds, complex stageEta, local-to-global lifts, QR, finite-bit complexity, runtime refinement, scientific X2 and ROOT acceptance remain open. This is not production admission or purification.

Planned independent checks: arbitrary nonidentity real matrix (parametric plus concrete nonsymmetric input); symbolic all-wire spectator equalities; inverse CX direction and reversed-control/target finite witness; negative rational signed off-diagonal; noncommuting order witness; arbitrary complex vector; width zero; both actual root axiom lists. Local allowUnsafeReducibility changes elaborator unfolding of gridSize=2^n; fresh kernel consumers and actual axiom roots must confirm it does not smuggle a premise.
