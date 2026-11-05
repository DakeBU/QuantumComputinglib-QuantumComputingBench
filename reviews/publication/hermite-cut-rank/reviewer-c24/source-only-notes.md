# HCR c24: independent source-only reconstruction

Fingerprint: `HCR_SOURCE_THRESHOLD_ENDPOINT_WIDTH_AND_RANK_BOUNDARY`.
Source packet: `hcr-source-c24.md`, raw SHA-256 `ae108f8933c49b0ee51d4523e7f33bf2000d6b77201fbc348104a22b60ef35d2`.

These notes precede any HCR Lean target/provider, formal context, author graph, existing evaluation or decoder read. Only the assigned source and repository process instructions were read. The live review agent also performed an earlier unrelated CTT review; that evidence was not used to infer any HCR implementation. This is a retrospective local exposition, not an external paper, historical Statement Seal or novelty claim; the historical formalizer is unknown. Formal-source agreement and whole-module publication acceptance have not been evaluated.

## Independent mathematics

An I-separation is an existential entrywise factorization through a finite real coordinate space. X and Y need not be finite. With finite Y, the column map factors through the |I|-dimensional space of I-coordinates, so its image has dimension at most |I|. Finite X is unnecessary. Empty I forces the zero matrix; empty X or Y is permitted. Witness width does not assert exact or minimal rank.

For a polynomial p(z)=sum_j c_j z^j of degree at most d, use left factor at index i equal to `sum_(j=i..d) c_j choose(j,i) u(x)^(j-i)` and right factor `v(y)^i`. The binomial theorem proves exact equality with d+1 terms, including the zero and constant polynomials. This is an algebraic finite Taylor expansion, not an analytic approximation.

The displayed Hermite polynomial is fixed, not an arbitrary oracle satisfying a degree promise. Its A_k has degree at most k and A_k(0)=1. Both summands defining P_k therefore have degree at most 2k+1, and substitution p=0, t=1 gives P_k(0)=1 because k+1 is positive. Thus polynomial separation has width 2k+2, and the finite-column rank consequence follows. The source reuses these polynomial prerequisites; their formal providers and production costs remain unchecked in this phase.

The witness algebra preserves exact functions: sum uses disjoint union, negation changes the left factor, and Hadamard product uses Cartesian product plus commutativity of real multiplication. Product of scalar functions and exponential of an additive scalar split each have singleton width. Hadamard multiplication must not be mistaken for matrix multiplication.

For each actual column, v(y)<M implies M>0. Quotient/remainder arithmetic then partitions the strict integer cut into all earlier rows and the possibly partial boundary row. Their indicator terms are disjoint. The complement uses `(1-earlier, -boundary)` as left factors with the same right factors `(1, suffix_indicator)`, still width two. For empty Y no actual column exists and M may be zero; the statements remain vacuous entrywise. T=0 gives the zero cut, and a threshold divisible by M has empty partial boundary. No injectivity or complete bitstring grid is needed.

With h>0, divide the real inequality to obtain j<(t-a)/h. For natural j this is equivalent to j<ceil_N((t-a)/h), including negative arguments clamped to zero and exact integer arguments. Floor, non-strict ceiling comparison, or an extra +1 would change endpoint samples.

Let z=a+h*(M*u(x)+v(y)). The left indicator is exactly 1[z<-1] and the right exactly 1[z<0]. The left cut is nested in the right. Therefore the three masks select respectively z<-1, -1<=z<0, and z>=0. At z=-1 the middle mask is one; at z=0 the right mask is one and exp(-z)=1=P_k(0), so the original inclusive polynomial definition is unchanged. No identity P_k(-1)=exp(-1), continuity, differentiability or endpoint deletion is required for this switching proof.

The affine split `row=a+h*M*u` and `col=h*v` equals z by real distributivity and natural-to-real cast compatibility. The first masked exponential has width 2*1. The middle mask is H_right+(-H_left), width 2+2, and the polynomial width is 2k+2, so its Hadamard product has width 4(2k+2). The last term uses the direct width-two complement and exp(-row)exp(-col), width 2*1. Concatenate with the displayed parentheses and tags to obtain the literal index type and width 8k+12. This is one construction with three simultaneously required terms, not three alternative OR routes. In particular replacing the direct complement by the generic width-three expression `1+(-H_right)` would not reproduce the literal stated supplier width without another compression argument.

Finite Y is needed only for rank conclusions, not for the separation construction. Scalar multiplication by any real c scales a left factor, preserving the same width; c need not be positive or nonzero, and no normalization follows.

## Obligations to retain for phase 2

The source provides only the grouped heading S3-S5, not an individual label for every polynomial subclaim. The seal records an explicit independent atomization and covers every subclaim, rather than pretending the source uniquely fixes declaration numbering. S18 explicitly uses S3 for the generic polynomial mechanism.

Potential mismatches to test later are: extra finite-X, M>0, nonempty, positivity or rank premises; replacement of the fixed P_k by a conditional oracle; flipped quotient/remainder order; incorrect strict threshold at a junction; different piecewise function at zero; matrix instead of entrywise multiplication; wrong tagged index parentheses/cardinality; equality or optimality of rank instead of an upper bound; normalization or executable/quantum cost claims smuggled through the word "certificate". None is alleged to occur in an unseen implementation.

No internal mathematical gap was found in the source-only derivation. Reused formal prerequisites and every implementation correspondence remain unverified. Separate open consumer bridges are the actual scientific grid and parameter mapping, normalization, complete tensor-train construction, physical word/register embedding and isometry realization, full cleanup and circuit action, and uniform accuracy/finite-bit/stability/input/storage/resource bounds. There is no epsilon, L or n_p parameter in this contract, hence no poly(n_p) conclusion.

The source graph is independently reconstructible, but the Lean dependency graph cannot be reconstructed from prose alone. A compressed spine can only present exact polynomial/exponential separation, two-term threshold masks, endpoint-safe affine composition and finite-column rank consumption. Any proposed state-preparation transport needs all additional consumer inputs, not a lone rank arrow. No certified functor, fresh compilation, whole-module round-trip verdict, integration, main admission, ROOT closure or PURIFIED/Exposition Seal is claimed.

Phase 1 stops after freezing these notes and the source-only seal. Phase 2 requires a new explicit authorization.
