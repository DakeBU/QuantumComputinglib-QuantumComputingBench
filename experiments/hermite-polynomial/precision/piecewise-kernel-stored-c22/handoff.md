# C22 same-object stored supplier

This checkpoint materializes the exact C21 five-component source kernel. `actualBlocksQ` is a computable rational counterpart of C21's full object; its entry and both boundaries cast exactly to C21's `actualBlocks` through the same explicit `fullEquiv`.

`produceQData` constructs that rational block once, then generates only width-many local D-by-2D rational tables and two D boundary vectors. These are actual stored nested vectors, not an abstract input table or all-word amplitude callback. `castData` reads and materializes those vectors into real stored tables. `produceData_window` proves their finite-window specification unconditionally. `produceStored` passes those actual tables and boundaries to canonical `StoredMatrixProductChain.ofTable`.

`produceStored_refines` identifies the same returned chain with C21 `actualChain`, for all rational R/delta without any supplied Window, mask, coefficient, refinement, or rank premise. Exact source action, bond bound, and scalar-address envelope transfer to that same value. `allocated_stored_source` directly uses the actual allocatedRadius/sourceDelta inputs and obtains positive radius from the inherited theorem.

The physical bits remain q0 LSB. All original strict/inclusive cuts, zero/full-grid endpoints, T=0/T=1, signed source coefficients, and rationalGrid conventions are inherited unchanged. The dimension is

\[
D=18(d+1)+9(m+1)+18,\quad d=\mathrm{sourceDegree}(\delta),\quad m=2k+1.
\]

## Partial accounting, not full runtime

The new accounting proves real container work on the actual generated data. Put

\[
A=(n+1)(2D^2+D+1)+2D.
\]

Rational collection incurs \(2A\) reads and \(2A\) writes. Casting the stored rational vectors adds \(3A\) reads and \(2A\) writes, including explicit source-table/row/scalar reads and new materialization. Canonical ofTable charges its actual boundary absorption, copied core references, nodes, and local arithmetic. Thus the same returned run has the *accounted partial ledger* bound

\[
9A+20D^2+30D+5n^2+7n+31.
\]

This is emphatically not full producer runtime. Rational scalar callbacks currently cross an explicitly unaccounted arithmetic boundary (`pure` after literal formula evaluation). No choose/factorial/power/expMidpoint/source evaluation is assumed O(1). Entry indexing and source preprocessing are also open. Coefficient caches have not yet been implemented/charged; repeated boundary coefficient production must be charged or replaced by a proved stored cache.

Pinned Mathlib source shows logical choose recursion branches, but `choose_eq_fast_choose` is a compiler-simplification theorem redirecting execution to descending-product/factorial quotient. Factorial and descending-product code also use proved binary-splitting replacements. This is implementation inspection, not a cost certificate; it does not justify treating those calls as free or announcing finite-bit polynomial runtime.

The exact remaining scalar interface is tied to this prepared BlockQ object: setup plus \(2(n+1)D^2\) actual local kernel evaluations and \(D\) left/\(D\) right boundary evaluations. An eventual complete ledger must produce, rather than assume,

\[
C_{\rm setup}+\sum_{q,a,j}C_{\rm entry}(q,a,j)
 +\sum_a(C_{\rm left}(a)+C_{\rm right}(a)),
\]

alongside the proved traffic/assembly contribution. The charged source-specific evaluator must include cuts, powers, binomials, factorials, midpoint/tail production, source coefficients and caches/copies, comparator/product/directsum arithmetic, and finite-index quotient/remainder operations. Integer bitlength, rational GCD and real-representation costs remain separate named obligations.

## Evidence and lifecycle

New C22 sources and consumer receive a fresh private-cache gate, with canonical storage suppliers rebuilt and all C19/C20/C21 bytes checked pre/post. The selected logical ConsumerChecks is C21's cached actual finite-middle module, not C20's same-named consumer. Final source/cache hashes, ordered environment, native-log provenance and sanitized public derivatives are bound in the final manifest. Earlier frozen ENV_BLOCKED/stale receipts stay unchanged.

This is PROVED_LOCAL, not independent source/publication admission, PURIFIED, or full scientific ROOT. No Git, production, task, registry or historical files were written. The user requested pausing goal expansion for textbook publication; after sealing this already-started bounded slice, no successor work begins.
