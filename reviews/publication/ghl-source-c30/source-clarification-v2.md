## M14. Canonical bulk guard clarification — source-bound successor v2

This supplement clarifies the historical row-dependent candidate in M4. It does not rewrite the original frozen source or any implementation. In that section, “bulk” means exactly the canonical n-only predicate 2 ≤ r ≤ N−3, where N=2^n and subtraction is natural-number subtraction. It is not the arbitrary-parameter interval [K₁,K₂] used by the generic classifier discussion in M1/M2.

The forward candidate tests the canonical bulk predicate first, then row 0, then row 1, then row N−2, then row N−1, then its fallback. Within those regions its slot bounds are respectively 5,3,4,4,3; an unused slot returns the input row.

The reverse candidate tests row 0 first, row 1 second, then the canonical bulk predicate, then row N−2, then row N−1, then its fallback. Its outputs in that order are target, target, target+2−row, target−(N−4), target−(N−3), and target. This actual precedence matters on the total natural-number carrier, especially at small grids.

The recovered forward/reverse roundtrip is only the stated canonical-family result for n≥3, sparse index s<8, and input row i<N. No arbitrary K₁,K₂ version is claimed. These are the existing local formula and theorem guards, not added paper assumptions or a repaired Lean target.

Provenance: after the original source-only freeze, the parent supplied one explicitly authorized limited independent-phase clarification request concerning the meaning of bulk. The author received that specific feedback but read no reviewer/decoder file or other independent result. The two implementation definitions and the roundtrip header were directly rechecked before writing this supplement. The original source SHA-256 remains c774ecaf66c3d3c9586c41f7441b416ee77bfd54a3314e1d9ee66ff7151db6f5; the prospective lesson appends this visibly versioned supplement rather than pretending it was present initially.
