# Source-first construction topology

Reconstructed before Lean proof search; independent approval pending.
Scope: complete printed pages 141-143 of section 9.1. Stable node prefix
`lin-wiebe-2026-qasc:ch9:`. Source and implementation graphs are separate.

| Source region | Disposition |
| --- | --- |
| p141 chapter overview, three paragraphs | EXCLUDED: input-model motivation, efficient construction and composition promises outside this exact consumer |
| p141 first block-matrix display and initial assumptions | NODE exact-block, SOURCE input U unitary with prescribed top-left block |
| p141 (9.1) | NODE clean-input, ancilla-first b/zero injection |
| p141 (9.2) | NODE clean-action, clean output Ab and other-sector residual |
| p142 first paragraph and (9.3) | NODE orthogonal-residual, other sector rejected; full residual-vector theorem outside chosen endpoint |
| p142 measurement paragraph and Figure9.1 caption | NODE postselect, accept zero and normalize accepted system vector |
| p142 normalization paragraph and (9.4) | NODE born-weight, square norm of accepted vector; expectation-value equality EXCLUDED in this slice |
| p142 independence of unspecified U entries | NODE independence, clean branch depends only on exact clean block |
| p142 Example9.1, (9.5), circuit, (9.6), verification sentence | EXCLUDED: separate concrete Ry/CNOT synthesis, not input consumer |
| p143 generalization paragraph, (9.7) | NODE multiple-ancillas, 2^m block rows, first clean sector |
| p143 Definition2.25 reference and (9.8) | NODE partial-application, bra/ket contraction equals clean block |
| p143 Exercise9.1 and necessary-condition paragraph | EXCLUDED: matrix operator-norm contraction, not probability calculation |
| p143 (9.9) | NODE alpha-block, A/alpha equals clean block |
| p143 normalized-state paragraph and (9.10) | NODE scaled-consumer, alpha scaling, weight and conditional normalization |
| p143 warning that large alpha suppresses probability | NODE alpha-warning, consequence of exact weight formula; no efficiency guarantee |
| p143 approximation paragraph, Definition9.2, (9.11) | EXCLUDED: approximate operator-norm frontier; no substitution of vector/Frobenius norm |
| p143 precision paragraph and exact shorthand | EXCLUDED: finite-precision models and notation not a certified finite-bit theorem |
| p143 (9.12) and superposition paragraph | NODE basis-to-vector, entrywise block check extends by linearity |
| p143 U=UB UC paragraph and (9.13) | EXCLUDED: alternative block-verification inner-product route |

AND route to scaled-consumer: alpha-block + clean-input + basis-to-vector +
born-weight + positive-real-alpha. Conditional normalized output additionally
needs nonzero accepted branch, derived from Ab!=0, not promised uniformly.
The exact-unitary normalized-input assumptions permit interpretation as Born
probability; this slice does not certify a physical measurement instrument.

OR routes for supplying the exact block: direct entries (9.12) OR factored
inner products (9.13) OR a separately certified construction from later
sections. They are not all prerequisites of the consumer. Other U sectors
and circuit construction are intentionally opaque here.

Referenced standing convention: printed p37 (PDF zero-based36) was also
rendered and read. Definition2.25/(2.53) is the NODE for forward partial
application; (2.54) is EXCLUDED because this slice does not use the dual row map.
Example2.26/(2.55)-(2.58) is the NODE for computational-basis row/column/block
selection. The staged adapter specializes these formulas to the existing finite
coordinate indexing; it does not certify a general abstract tensor-product API.
Example2.24 at the top of that page is EXCLUDED (matrix reshaping not needed).

SOURCE_GAP/nonzero-boundary: the source writes Ab/||Ab|| without spelling out
Ab!=0. The staged theorem exposes the boundary rather than supplying a false
normalization at zero. This is an implicit validity condition on the conclusion,
not a reviewed repair to the source statement. SOURCE_GAP resource boundary:
success formula alone supplies neither amplification nor gate costs.
