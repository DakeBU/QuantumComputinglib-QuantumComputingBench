# Source freeze — author private / routing only

Date: 2026-10-17. Role: retrospective source AUTHOR-curator.
Historical formalizer: UNKNOWN. Source-first disclosure is `source-only.md`;
do not send this binding/routing file or author-private coverage to its initial
independent mathematical reader. There is no reviewer verdict in this packet.

Parent-supplied checkout context (not rechecked by Git in this worker):
HEAD `87072cc8c2f8ee41941bc451b47667816225c569`;
origin/main `f2cba045611a0d11c5995c29607569726bf1d6c5`.
Actual inspected toolchain text: `leanprover/lean4:v4.33.0`.
The parent reports the main toolchain as 4.29.1; this does not substitute for
checking either environment. No toolchain compatibility/build claim is made.

All hashes are SHA-256 of actual raw file bytes, case-insensitive hexadecimal.
Repository-relative paths below intentionally contain no local absolute paths.

Authored mathematical source version 1:
`source-only.md` SHA-256
`B971E269CCF4F89DDE39BA87EB385A9C6D200ACB97D570738F2B5BBAC85784FD`.
The other three files are private routing/coverage artifacts, not part of the
initial source-first mathematics packet. The author checked 14 source sections
and 75 declaration coverage rows; lexical checks found no Lean module/name,
local absolute path or old verdict in that mathematics file.

| Whole production module | SHA-256 | Lines / nonblank | Public / private lexical declarations |
| --- | --- | --- | --- |
| QuantumBlockEncoding/HermiteSmoothness.lean | FD345E839442CB2355A475D2DFA8A16E50CD33D59A1E7E05ACBBBA228F813004 | 151 / 133 | 12 / 0 |
| QuantumBlockEncoding/HermiteTransferCores.lean | BDCDDE7754A59D67870A5B0D9E169D9EF20B7FBE161E2CE719B310CDB6A938EC | 91 / 75 | 10 / 0 |
| QuantumBlockEncoding/HermiteBinaryCutoff.lean | 728F7AFA19181BBD3FE6E8D2D3EB66EA1862B01932AFEF0BE8A50CD557A7A212 | 130 / 113 | 9 / 3 |
| QuantumBlockEncoding/StoredHermiteChildGeometry.lean | 8315B9E37FD060DECF3B8BA41EF4101A9B4E21BAAFC35B61B0FE6BDDEB7588F2 | 249 / 222 | 24 / 0 |
| QuantumBlockEncoding/StoredHermiteKernelTable.lean | A0FD513ED0E1D7A826080660871103B492329C6577E7AEC6D0CFEDFC2D49BC12 | 204 / 182 | 16 / 1 |

| Context | SHA-256 |
| --- | --- |
| lean-toolchain | 302CD63C54178885B89E669F33B38F12F4DD7AE7E5CAC537B3203E3768D8FB2B |
| lake-manifest.json | 510171E8214A2AC5E00F16C1BF92AD474D2DE42C4CD2DC2B3D411272F7B58763 |

The following are hash-bound consulted providers/lessons, not a new
whole-provider publication scope and not compiler-extracted proof dependencies.

| Consulted file | SHA-256 |
| --- | --- |
| QuantumBlockEncoding/HermitePolynomial.lean | F8A3E1D5F29AED1228B6EDE3577A9AF1E76301559172EE67A266FCB0D56FEE1E |
| QuantumBlockEncoding/HermiteBoundaryInjection.lean | 7B16E1EE4B88B9E775CEE1A63482C60DF2121CE88AD43F10E72CA2E88C6D472C |
| QuantumBlockEncoding/HermiteBernstein.lean | 661618D9C10826491EE293C7C411AC2D55056426739F4BBFD3E7C410C05E4BFF |
| QuantumBlockEncoding/HermiteExplicitBond.lean | F6E1B0099D451C77C5FE479A7591BCB204910675838109074C2E49867A1D5031 |
| QuantumBlockEncoding/StoredGivens.lean | C2A524772ADB32A4CCAD236DAB347633DC865B0BEFB16ADCBF6DC08FBDF3301D |
| QuantumBlockEncoding/StoredBinaryCoordinates.lean | 247805A31B94A5DFC2D78B46FBE139CD0AFF24DC5E23CB2E73F2F55A417EA00C |
| QuantumBlockEncoding/StoredHermiteGeometry.lean | 167B4FA79EAA7C8629F6C3E246C9CDA4D64D678BFC99F8AA7C5820A68A1F4739 |
| QuantumBlockEncoding/StoredThinLQ.lean | ED08EF278A93268F7D9620CB2DDAFC2E3468FCC4F2543923251A3CE4E057177A |
| QuantumBlockEncoding/StoredTensorTrain.lean | A9E5B0C2B00261D6F100A431FA95725C1BEAD82A4B87C41D54B59F0B084FEAE4 |
| docs/hermite-polynomial-proof.md | 334EE2E6C6F6515BAC1A85C6CE17189D2394A72314ACF8C680DCA39F683B71EB |
| docs/lessons/hermite-affine-cut-separation.md | AE108F8933C49B0EE51D4523E7F33BF2000D6B77201FBC348104A22B60EF35D2 |
| docs/hermite-state-preparation.tex | F1C4659F892B91EEC720A272E225E91A4FEDA5A4B01D045B17CEE9C380BBE7ED |

The exact dependency manifest binds the dependency checkout pins; selected
Mathlib source definitions were additionally inspected for finSuccEquiv,
finSumFinEquiv and finProdFinEquiv. This is not an elaborated proof-term export.

Freeze discipline: any changed whole-module bytes, including imports/private
helpers/ambient scope/comments, invalidate this binding for a future formal
round trip. A substantive edit to `source-only.md` requires a successor source
version and new source-first evidence as appropriate. None of the old source
or review artifacts were rewritten. No production compile gate, public metadata,
graph publication, canonical registry or large completion ledger is created.
