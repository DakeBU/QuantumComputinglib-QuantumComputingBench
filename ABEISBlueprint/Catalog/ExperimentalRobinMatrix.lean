import QuantumBlockEncoding
import QuantumBlockEncoding.RobinMatrix
import Verso
import VersoManual
import VersoBlueprint

open Verso.Genre
open Verso.Genre.Manual
open Informal

set_option linter.hashCommand false
set_option linter.style.longLine false
set_option verso.blueprint.externalCode.strictResolve true

#doc (Manual) "Declaration catalog: ExperimentalRobinMatrix" =>
%%%
file := "catalog-experimental-robin-matrix"
%%%

This chapter is generated from the Lean source. Every node denotes one explicit public
declaration, and every Lean link is checked during the Blueprint build. Definitions appear
in source order before later results whenever the source module does so.

Reader orientation: Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts. Each card separates an accessible
reading cue from formal status, the source docstring, and the authoritative Lean panel.
The standalone Library Explorer adds full-text search and filters across every chapter.

*Research-module status.* RobinMatrix.lean is compiled by the full ASPBE gate
with zero proof holes. Its declarations include proved helper lemmas, explicit
counterexamples, and typed external contracts. A compiled local declaration does
not by itself certify the complete paper construction.

# QuantumBlockEncoding/RobinMatrix.lean

395 explicit public declarations, in source order.

:::definition "QuantumBlockEncoding.stencilRowCoeff" (lean := "QuantumBlockEncoding.stencilRowCoeff")
*Plain-English reading.* This definition gives the library's named construction or computation for “stencil row coeff”. Coefficient at column 'colIdx' when the stencil 'entries' is applied at row 'rowIdx'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Coefficient at column 'colIdx' when the stencil 'entries' is applied at row 'rowIdx'. Only entries whose offset lands on 'colIdx' contribute; the result is the sum of all matching coefficients. Returns bare 'Coeff' (no zero-wrapping) when exactly one entry matches.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-stencilrowcoeff). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.robinRowEntries" (lean := "QuantumBlockEncoding.robinRowEntries")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin row entries”. Select the stencil entry list for row 'i': - rows 'i < w.lower' use left boundary rows, - rows 'i > w.upper' use right boundary rows, - all others use the bulk stencil.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Select the stencil entry list for row 'i': - rows 'i < w.lower' use left boundary rows, - rows 'i > w.upper' use right boundary rows, - all others use the bulk stencil. Falls back to the empty list if a boundary row is missing from the supplied data, so the definition is total and does not need index proofs.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:37](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-robinrowentries). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.buildRobinMatrix" (lean := "QuantumBlockEncoding.buildRobinMatrix")
*Plain-English reading.* This definition gives the library's named construction or computation for “build robin matrix”. Build the full Robin derivative matrix of size 'gridSize n × gridSize n'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Build the full Robin derivative matrix of size 'gridSize n × gridSize n'. The boundary rows come from 'leftRows' and 'rightRows'; the interior uses 'bulkEntries'. The 'BulkWindow w' records where the interior starts and ends.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:56](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-buildrobinmatrix). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeMatrix" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeMatrix")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin derivative matrix”. The concrete Robin derivative matrix for the fourth-order central second-derivative stencil.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The concrete Robin derivative matrix for the fourth-order central second-derivative stencil.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:68](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinderivativematrix). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinAkMatrix" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinAkMatrix")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin ak matrix”. The one-term Robin theorem target $A\_k$.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The one-term Robin theorem target $A\_k$. Theorem '1 term robin' block-encodes the row-scaled operator 'A\_k ~ f(x) d^m/dx^m'; Eq. 'ROBIN clarified' carries entries 'f(x\_i) D\_\{ij\}' in the 'gamma3' branch.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:81](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinakmatrix). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinAkMatrix_apply" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinAkMatrix_apply")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin ak matrix apply”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:84](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinakmatrix-apply). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.matrixRowAbsSum" (lean := "QuantumBlockEncoding.matrixRowAbsSum")
*Plain-English reading.* This definition gives the library's named construction or computation for “matrix row abs sum”. Absolute-row-sum for row 'i' of a 'Coeff'-valued matrix, given a symbol environment 'env'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Absolute-row-sum for row 'i' of a 'Coeff'-valued matrix, given a symbol environment 'env'. This is the building block for the induced 1-norm.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:96](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-matrixrowabssum). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.matrixOneNorm" (lean := "QuantumBlockEncoding.matrixOneNorm")
*Plain-English reading.* This definition gives the library's named construction or computation for “matrix one norm”. Induced matrix 1-norm: the maximum absolute row sum.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Induced matrix 1-norm: the maximum absolute row sum. Uses 'evalWith env' to convert symbolic 'Coeff' entries to concrete 'Rat' values.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:106](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-matrixonenorm). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeNorm" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeNorm")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin derivative norm”. Numeric 1-norm of the Robin derivative matrix under a symbol environment.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Numeric 1-norm of the Robin derivative matrix under a symbol environment. Returns the maximum absolute row sum as a concrete 'Rat'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:117](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinderivativenorm). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinNumericNormalizer" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinNumericNormalizer")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin numeric normalizer”. Numeric normalizer α = N\_D · N\_f · κ for the one-term Robin construction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Numeric normalizer α = N\_D · N\_f · κ for the one-term Robin construction. 'nD' is the derivative-stencil normalization (1-norm of the Robin derivative matrix), 'nF' is the function-oracle normalization, and 'k' is the Robin-condition bound.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:125](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinnumericnormalizer). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinNormalizerBound" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinNormalizerBound")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin normalizer bound”. Proposition: the numeric normalizer α is at least the induced 1-norm of the Robin derivative matrix, i.e.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Proposition: the numeric normalizer α is at least the induced 1-norm of the Robin derivative matrix, i.e. α ≥ ∥D\_Robin∥₁. Stated via a 'Decidable' check so 'native\_decide' can close concrete instances.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:133](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinnormalizerbound). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinNumericNormalizer_eq_eval" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinNumericNormalizer_eq_eval")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin numeric normalizer eq eval”; its local proof does not by itself complete the broader paper route. Connecting the numeric normalizer to the symbolic GHL2025 normalizer via a concrete environment mapping the three symbols to their numeric values.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Connecting the numeric normalizer to the symbolic GHL2025 normalizer via a concrete environment mapping the three symbols to their numeric values.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:139](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinnumericnormalizer-eq-eval). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinBlockEncodingSpec" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinBlockEncodingSpec")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin block encoding spec”. Concrete BlockEncodingSpec wiring the Robin derivative matrix into the one-term Robin block encoding framework.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete BlockEncodingSpec wiring the Robin derivative matrix into the one-term Robin block encoding framework. Uses the fourth-order central stencil with Robin boundary corrections.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:149](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinblockencodingspec). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.robinBlockEncodingSpec_pureAncilla" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinBlockEncodingSpec_pureAncilla")
*Plain-English reading.* Lean checks the research-module proposition indexed as “robin block encoding spec pure ancilla”; its local proof does not by itself complete the broader paper route. The spec's resource pureAncilla matches 2n.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The spec's resource pureAncilla matches 2n.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:158](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinblockencodingspec-pureancilla). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeOracleResource" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeOracleResource")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin derivative oracle resource”. Concrete derivative oracle resource for the fourth-order Robin stencil.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete derivative oracle resource for the fourth-order Robin stencil. Uses half-bandwidth l = leftRadius = 2.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:163](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinderivativeoracleresource). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeOracleResource_eq" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeOracleResource_eq")
*Plain-English reading.* Lean checks the research-module proposition indexed as “robin derivative oracle resource eq”; its local proof does not by itself complete the broader paper route. The Robin derivative oracle resource equals bandedSparseAccessResource n 2.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The Robin derivative oracle resource equals bandedSparseAccessResource n 2.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:167](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinderivativeoracleresource-eq). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeOracleResource_pureAncilla" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinDerivativeOracleResource_pureAncilla")
*Plain-English reading.* Lean checks the research-module proposition indexed as “robin derivative oracle resource pure ancilla”; its local proof does not by itself complete the broader paper route. The Robin derivative oracle uses n - 1 pure ancillas (from Lemma 1).

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The Robin derivative oracle uses n - 1 pure ancillas (from Lemma 1).

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:171](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinderivativeoracleresource-pureancilla). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinBlockEncodingPredicate" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinBlockEncodingPredicate")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin block encoding predicate”. PO-6: Block-extraction equation for the Robin derivative block encoding.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* PO-6: Block-extraction equation for the Robin derivative block encoding. Records the structural preconditions that are checkable now (normalizer bound, ancilla count, zero error) and reserves the full equation ⟨0^a| ⊗ I) U (|0^a⟩ ⊗ I) = A / α as an abstract component pending unitary semantics.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:181](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinblockencodingpredicate). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinResourceBoundHolds" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinResourceBoundHolds")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin resource bound holds”. PO-7: Resource bound holds for the Robin block encoding.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* PO-7: Resource bound holds for the Robin block encoding. Concrete decidable check: pureAncilla = 2n and gate count ≤ paper's formula.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:188](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinresourceboundholds). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinResourceConsistent" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinResourceConsistent")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin resource consistent”. PO-9: The concrete resource is consistent with the symbolic expression.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* PO-9: The concrete resource is consistent with the symbolic expression. Checks the decidable part: pureAncilla = 2n.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:195](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinresourceconsistent). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.RobinOracleComposition" (lean := "QuantumBlockEncoding.Examples.RobinHeat.RobinOracleComposition")
*Plain-English reading.* This record groups the data and proof fields needed for “robin oracle composition”. A proposition-valued field is a requirement until a constructor supplies it. Bundle of oracle contracts and LCU composition obligation for the one-term Robin construction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Bundle of oracle contracts and LCU composition obligation for the one-term Robin construction. Contains: - derivative oracle O\_D (sparse-access for the banded stencil matrix), - function oracle O\_f (amplitude oracle for the coefficient function), - LCU composition Prop (PO-15: linear combination of unitaries correctness), - matrix coherence (the oracle's matrix equals the Robin derivative matrix).

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:204](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinoraclecomposition). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin oracle composition”. PO-13/14/15: Concrete oracle composition for the Robin derivative block encoding.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* PO-13/14/15: Concrete oracle composition for the Robin derivative block encoding. Instantiates the derivative oracle with the fourth-order stencil, the function oracle with one piece, and records the LCU composition Prop as an abstract claim.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:215](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinoraclecomposition). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition_bandwidth" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition_bandwidth")
*Plain-English reading.* Lean checks the research-module proposition indexed as “robin oracle composition bandwidth”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:231](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinoraclecomposition-bandwidth). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition_functionPieces" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition_functionPieces")
*Plain-English reading.* Lean checks the research-module proposition indexed as “robin oracle composition function pieces”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:234](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinoraclecomposition-functionpieces). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition_matrix" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition_matrix")
*Plain-English reading.* Lean checks the research-module proposition indexed as “robin oracle composition matrix”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:237](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinoraclecomposition-matrix). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.robinProofObligations" (lean := "QuantumBlockEncoding.Examples.RobinHeat.robinProofObligations")
*Plain-English reading.* This definition gives the library's named construction or computation for “robin proof obligations”. Default proof-obligation bundle for the one-term Robin construction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Default proof-obligation bundle for the one-term Robin construction. All obligations are unproved. main.tex:1131-1136 -

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:242](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-robinproofobligations). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinCircuitSemantics" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinCircuitSemantics")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin circuit semantics”. CircuitMatrixSemantics for the one-term Robin circuit using honest gate matrices.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* CircuitMatrixSemantics for the one-term Robin circuit using honest gate matrices. The full-space matrix is the product of the 7 honest gate matrices computed by 'evalGateMatrices'. Unproved gate claims remain in their own 'SemanticObligation' records. figure:1\_term\_ROBIN -

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:252](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobincircuitsemantics). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinCircuitDimCompat" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinCircuitDimCompat")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin circuit dim compat”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:275](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobincircuitdimcompat). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockExtractionTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockExtractionTarget")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin block extraction target”. Block-extraction target for the one-term Robin block encoding.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Block-extraction target for the one-term Robin block encoding. States that the '(0, 0)' block of the circuit matrix should equal 'A\_k / (N\_D \* N\_f \* kappa)'. The 'unitaryMatrix' and 'blockMatrix' are derived from the real circuit matrix product computed by 'evalGateMatrices' over all 7 honest gate matrices. Block correctness remains unproved. The 'signalDim' is 'qubitDim effectiveRobinSignalQubits' where 'effectiveRobinSignalQubits' counts all non-system qubits. 'systemDim' is 'gridSize n'. figure:1\_term\_ROBIN, main.tex:1131-1136 -

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:296](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockextractiontarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinCircuitBlockClaim" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinCircuitBlockClaim")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin circuit block claim”. Circuit block encoding claim for the one-term Robin construction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Circuit block encoding claim for the one-term Robin construction. Connects the circuit matrix semantics to the block extraction target and records the dimension compatibility as a parameter. The caller must supply 'hDim' proving that the total circuit Hilbert space decomposes as signalDim × systemDim. For concrete 'n' (e.g. n = 3) this is provable by 'native\_decide'. figure:1\_term\_ROBIN, main.tex:1131-1136 -

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:323](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobincircuitblockclaim). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.defaultOneTermRobinCircuitBlockClaim" (lean := "QuantumBlockEncoding.Examples.RobinHeat.defaultOneTermRobinCircuitBlockClaim")
*Plain-English reading.* This definition gives the library's named construction or computation for “default one term robin circuit block claim”. Default one-term Robin circuit block claim using the reusable dimension compatibility theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Default one-term Robin circuit block claim using the reusable dimension compatibility theorem. The block-correctness obligation remains unproved.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:344](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-defaultonetermrobincircuitblockclaim). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinFiniteBlockCompositionContract" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinFiniteBlockCompositionContract")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin finite block composition contract”. Contract-only finite-dimensional LCU/block-composition dependency for the one-term Robin theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Contract-only finite-dimensional LCU/block-composition dependency for the one-term Robin theorem. This records the exact circuit claim, target matrix, normalizer, and open matrix obligations that a future finite-dimensional composition theorem must close. It does not promote the current LCU, projection, or extraction flags.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:359](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinfiniteblockcompositioncontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinFiniteBlockCompositionContract_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinFiniteBlockCompositionContract_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin finite block composition contract transcript”; its local proof does not by itself complete the broader paper route. The finite block-composition contract is wired to the concrete target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The finite block-composition contract is wired to the concrete target.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:404](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinfiniteblockcompositioncontract-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinFiniteCompositionExactTheoremObligation" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinFiniteCompositionExactTheoremObligation")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin finite composition exact theorem obligation”. Contract-only interface for the exact finite composition theorem still needed to close the GHL2025 one-term Robin block encoding.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Contract-only interface for the exact finite composition theorem still needed to close the GHL2025 one-term Robin block encoding. This names the missing theorem-facing step without asserting it: the seven-gate matrix product, projected in the Definition 'def:block-encoding' signal-zero convention, must realize the Eq. 'ROBIN clarified' target block 'oneTermRobinAkMatrix n / (N\_D N\_f kappa)'. The proof flag stays false until that exact finite-dimensional theorem is build-tested.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:441](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinfinitecompositionexacttheoremobligation). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinFiniteCompositionExactTheoremObligation_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinFiniteCompositionExactTheoremObligation_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin finite composition exact theorem obligation transcript”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:449](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinfinitecompositionexacttheoremobligation-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinBlockEncodingProofRoute" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinBlockEncodingProofRoute")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin block encoding proof route”. A proposition-valued field is a requirement until a constructor supplies it. Phase 1 proof-route contract for the GHL2025 one-term Robin theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Phase 1 proof-route contract for the GHL2025 one-term Robin theorem. This record ties the theorem tuple, circuit-matrix semantics, block-projection target, active oracle contracts, and source-route blockers into one Lean object. It is a transcript and obligation map, not a proof that the block encoding is correct.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:467](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin block encoding proof route”. Default theorem-level proof route for the one-term Robin block encoding.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Default theorem-level proof route for the one-term Robin block encoding. All unproved semantic obligations are deliberately kept false. The route uses the active seven-gate circuit product, the global-slot 'O\_D^BS' cleanup-scope decision, and the external-source transcript for 'O\_f'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:531](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_normalizer" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_normalizer")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route normalizer”; its local proof does not by itself complete the broader paper route. The proof-route contract links the theorem normalizer to the block target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The proof-route contract links the theorem normalizer to the block target.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:573](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-normalizer). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_blockTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_blockTarget")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route block target”; its local proof does not by itself complete the broader paper route. The theorem-level route pins the block target used for the one-term theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route pins the block target used for the one-term theorem. This is only a structural guard: it records the signal-index-zero convention, the Robin target matrix, and the shared circuit semantics object. It does not prove the extracted block equation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:586](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-blocktarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_blockProjectionNormalizerAudit" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_blockProjectionNormalizerAudit")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route block projection normalizer audit”; its local proof does not by itself complete the broader paper route. The theorem-level route uses the same block-projection target, normalizer, and open flags as the concrete circuit matrix target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route uses the same block-projection target, normalizer, and open flags as the concrete circuit matrix target. This is a route guard for the final block-extraction statement. It records the cast circuit product, the signal-index-zero projection API, the Robin target matrix, and the normalizer 'N\_D \* N\_f \* kappa', while keeping the block and LCU obligations false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:610](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-blockprojectionnormalizeraudit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_circuitProduct" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_circuitProduct")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route circuit product”; its local proof does not by itself complete the broader paper route. The theorem-level route uses the active seven-gate circuit product.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route uses the active seven-gate circuit product. This is a structural guard for Phase 1: it records that the route still points to 'oneTermRobinCircuitSemantics', whose matrix is the ordered product computed by 'evalGateMatrices' over 'oneTermRobinGateMatrixPlaceholders'. It does not prove any gate unitarity or block-extraction equation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:680](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-circuitproduct). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gateUnitaryFlags" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gateUnitaryFlags")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gate unitary flags”; its local proof does not by itself complete the broader paper route. The theorem route uses the active seven-gate matrix product with the current gate-level proof flags frozen.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route uses the active seven-gate matrix product with the current gate-level proof flags frozen. Only 'U\_indic' and SWAP are locally marked proved. The paper-oracle gates 'O\_DT^S', 'Ry\_boundary', 'O\_D^BS', 'O\_f', and '(O\_D^BS)^dagger' remain in obligation mode, and the O\_D^BS cleanup scope is still restricted to the active global sparse-slot source.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:712](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gateunitaryflags). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gateListAndFlags" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gateListAndFlags")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gate list and flags”; its local proof does not by itself complete the broader paper route. The theorem route keeps the Fig.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route keeps the Fig. 1-term Robin gate order and the current gate-level proof flags synchronized. This guard packages the gate-list freeze with the seven-gate flag freeze. It does not prove any of the paper-oracle gates unitary and keeps the O\_D^BS active global-source cleanup scope in obligation mode.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:740](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gatelistandflags). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gateProjectionFreeze" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gateProjectionFreeze")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gate projection freeze”; its local proof does not by itself complete the broader paper route. The theorem route keeps the seven-gate order and projection target frozen together.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route keeps the seven-gate order and projection target frozen together. This is a reviewer-facing proof-DAG wrapper over the gate-list guard and the block-projection normalizer audit. It records the active Fig. 1-term Robin gate order, the current proof-state vector, the signal-index-zero target, and the final false flags. It does not prove a block equation or change any oracle matrix.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:780](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gateprojectionfreeze). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_layoutProjectionAudit" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_layoutProjectionAudit")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route layout projection audit”; its local proof does not by itself complete the broader paper route. The theorem-level signal and pure-ancilla counts are wired separately from the circuit-level projection dimension.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level signal and pure-ancilla counts are wired separately from the circuit-level projection dimension. The paper theorem states the block-encoding tuple with 'oneTermRobinLayout.signalQubits' and '2n' pure ancillas. The matrix backend uses 'effectiveRobinSignalQubits' because the block projection zeros every non-system wire in the concrete register partition. This guard records both counts and keeps resource cleanup plus block extraction in obligation mode.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:823](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-layoutprojectionaudit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockExtractionTarget_signalZeroBlockIndices" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockExtractionTarget_signalZeroBlockIndices")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block extraction target signal zero block indices”; its local proof does not by itself complete the broader paper route. The signal-index-zero Robin target uses the unshifted system row and column indices.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The signal-index-zero Robin target uses the unshifted system row and column indices. This is an index-convention guard for the block-projection route, not a proof of the extracted block equation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:862](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockextractiontarget-signalzeroblockindices). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_signalZeroBlockIndices" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_signalZeroBlockIndices")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route signal zero block indices”; its local proof does not by itself complete the broader paper route. The theorem-level route inherits the signal-index-zero block index convention from 'oneTermRobinBlockExtractionTarget'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route inherits the signal-index-zero block index convention from 'oneTermRobinBlockExtractionTarget'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:876](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-signalzeroblockindices). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_claimBlockCorrectFalse" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_claimBlockCorrectFalse")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route claim block correct false”; its local proof does not by itself complete the broader paper route. The theorem-level route keeps the circuit-claim block obligation open.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route keeps the circuit-claim block obligation open. 'CircuitBlockEncodingClaim.blockCorrect' is separate from the target-level 'blockCorrect' field. This guard prevents the route from silently promoting the theorem claim while the paper-level oracle and composition blockers remain open.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:899](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-claimblockcorrectfalse). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_flags_false" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_flags_false")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route flags false”; its local proof does not by itself complete the broader paper route. The theorem-level route keeps all semantic blockers in obligation mode.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route keeps all semantic blockers in obligation mode. This theorem is the acceptance guard for the Phase 1 contract: it records the current false flags without using them as proofs.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:917](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-flags-false). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_ofExternalSourceAndFlags" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_ofExternalSourceAndFlags")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route of external source and flags”; its local proof does not by itself complete the broader paper route. The theorem route exposes the 'O\_f' external-source transcript and false flags.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route exposes the 'O\_f' external-source transcript and false flags. This is a Phase 1 bridge from the per-column 'functionOracleAmplitudeProofRoute\_externalSourceAndFlags' guard to 'oneTermRobinBlockEncodingProofRoute'. It records that the route still points to the cited GHL2025/GL2024 source contract and keeps the 'N\_f', orthogonal completion, gate-unitarity, LCU, projection, and block-correctness obligations false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:969](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-ofexternalsourceandflags). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_ofCleanFunctionOracleEntry" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_ofCleanFunctionOracleEntry")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route of clean function oracle entry”; its local proof does not by itself complete the broader paper route. The route-level 'O\_f' gate exposes the clean-workspace paper branch entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The route-level 'O\_f' gate exposes the clean-workspace paper branch entry. This is a narrow bridge from gate slot 4 of Fig. 1-term Robin to the per-column 'functionOracleAmplitudeProofRoute'. It proves only the matrix entry selected by the clean 'm\_f' branch; the theorem-level function-oracle, LCU, projection, block-correctness, and final extraction flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1076](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-ofcleanfunctionoracleentry). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_derivativeBoundaryContractMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_derivativeBoundaryContractMap")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route derivative boundary contract map”; its local proof does not by itself complete the broader paper route. The theorem route exposes the derivative-amplitude and boundary-rotation contracts that share the paper normalizer 'N\_D'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route exposes the derivative-amplitude and boundary-rotation contracts that share the paper normalizer 'N\_D'. This guard connects GHL2025 Lemma 3, Eq. (20), Eq. 'angles for Ry', and Fig. 1-term Robin to 'oneTermRobinBlockEncodingProofRoute'. It packages the existing source-bound bridge for 'O\_DT^S' and 'Ry\_boundary', checks that those gates occur in the active seven-gate route, and keeps all analytic, gate-level, LCU, projection, and final extraction flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1176](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-derivativeboundarycontractmap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odtsKetZeroEntry" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odtsKetZeroEntry")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odts ket zero entry”; its local proof does not by itself complete the broader paper route. The route-level 'O\_DT^S' gate exposes the Eq.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The route-level 'O\_DT^S' gate exposes the Eq. (20) ket-zero entry. This is the local matrix-entry bridge for the derivative-amplitude factor in Eq. 'ROBIN clarified'. Under the paper-register hypotheses selecting an indicator-1, ancilla-0 column and the ancilla-0 row with matching non-ancilla bits, gate slot 1 of the Fig. 1-term Robin route has the symbolic ket-zero entry recorded by 'sparseAmplitudeOracleDTCoefficientNormalizerProofRoute'. It does not prove the division semantics, normalizer bound, two-by-two unitarity, LCU composition, projection, or final block extraction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1322](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odtsketzeroentry). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_boundaryKetZeroEntry" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_boundaryKetZeroEntry")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route boundary ket zero entry”; its local proof does not by itself complete the broader paper route. The route-level 'Ry\_boundary' gate exposes the boundary ket-zero entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The route-level 'Ry\_boundary' gate exposes the boundary ket-zero entry. This is the local matrix-entry bridge for the boundary rotation factor in Eq. 'angles for Ry' and Eq. 'ROBIN clarified'. Under the paper-register hypotheses selecting an indicator-0, ancilla-0 column and the ancilla-0 row with matching non-ancilla bits, gate slot 2 of the Fig. 1-term Robin route has the symbolic cosine half-angle entry recorded by 'boundaryRotationAngleNormalizerProofRoute'. It does not prove the arccos semantics, half-angle identities, two-by-two unitarity, LCU composition, projection, or final block extraction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1441](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-boundaryketzeroentry). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveGlobalSlotBlockers" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveGlobalSlotBlockers")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs active global slot blockers”; its local proof does not by itself complete the broader paper route. The theorem-level route exposes the active global-slot 'O\_D^BS' blockers.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route exposes the active global-slot 'O\_D^BS' blockers. This is the replacement for the retired row-dependent unused-branch route. The active route is the global sparse-slot source together with the restricted dagger-column cleanup interface. Full clean-domain cleanup and full-space unitarity remain obligations.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1614](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbsactiveglobalslotblockers). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_activeOdbsGatePairBlocked" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_activeOdbsGatePairBlocked")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route active odbs gate pair blocked”; its local proof does not by itself complete the broader paper route. The theorem-level route keeps the active 'O\_D^BS' gate pair in obligation mode.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route keeps the active 'O\_D^BS' gate pair in obligation mode. This guard is intentionally weaker than a semantic theorem. It records only that the active forward and dagger matrices remain unproved as unitaries while the paper cleanup and unitary-extension flags stay false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1674](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-activeodbsgatepairblocked). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveScopeKeepsFinalFlagsFalse" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveScopeKeepsFinalFlagsFalse")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs active scope keeps final flags false”; its local proof does not by itself complete the broader paper route. The active-scope blocker propagates to the final theorem flags.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The active-scope blocker propagates to the final theorem flags. The global-slot cleanup interface is currently restricted to 'bandedSparseAccessPaperGlobalSlotSource'. This theorem keeps final composition and block-extraction flags false until a full clean-domain or full-space theorem is accepted.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1699](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbsactivescopekeepsfinalflagsfalse). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_activeOdbsGatePairWiring" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_activeOdbsGatePairWiring")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route active odbs gate pair wiring”; its local proof does not by itself complete the broader paper route. The theorem-level route wires the active 'O\_D^BS' gate pair at the Fig.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route wires the active 'O\_D^BS' gate pair at the Fig. 1-term Robin positions. This is only a circuit-product guard. It records the gate labels and matrices used by the route while preserving the false unitarity flags.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1734](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-activeodbsgatepairwiring). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_activeOdbsGatePairPublicSources" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_activeOdbsGatePairPublicSources")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route active odbs gate pair public sources”; its local proof does not by itself complete the broader paper route. The active 'O\_D^BS' gate pair keeps public source anchors on its obligation records.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The active 'O\_D^BS' gate pair keeps public source anchors on its obligation records.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1772](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-activeodbsgatepairpublicsources). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveGlobalSlotGateFreeze" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveGlobalSlotGateFreeze")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs active global slot gate freeze”; its local proof does not by itself complete the broader paper route. The active global-slot gate freeze combines the active matrices, cleanup-scope blocker, block target, and final false flags.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The active global-slot gate freeze combines the active matrices, cleanup-scope blocker, block target, and final false flags.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1788](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbsactiveglobalslotgatefreeze). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_projectionSourceFreeze" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_projectionSourceFreeze")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route projection source freeze”; its local proof does not by itself complete the broader paper route. The source-gate freeze keeps the projection target and final theorem flags open under the active global-slot cleanup scope.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source-gate freeze keeps the projection target and final theorem flags open under the active global-slot cleanup scope.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1840](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-projectionsourcefreeze). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_rejectedRowDependentCollisionRegression_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_rejectedRowDependentCollisionRegression_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route rejected row dependent collision regression n 3”; its local proof does not by itself complete the broader paper route. The old row-dependent collision remains rejected-model regression memory.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The old row-dependent collision remains rejected-model regression memory. The active global-slot image separates the same two boundary columns, so this theorem must not be used as an active paper-level blocker.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1872](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-rejectedrowdependentcollisionregression-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_encodedOutOfRangeSparseSlot_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_encodedOutOfRangeSparseSlot_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route encoded out of range sparse slot n 3”; its local proof does not by itself complete the broader paper route. The theorem route records encoded sparse value '7' as the first out-of-range clean slot for the one-term 'kappa = 7' source domain.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route records encoded sparse value '7' as the first out-of-range clean slot for the one-term 'kappa = 7' source domain. This guard replaces the retired row-dependent unused-branch blocker in the active route. The source column is clean, but it is not in 'bandedSparseAccessPaperGlobalSlotSource', so any broader cleanup theorem must use a precise full-clean-domain or full-space extension interface.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1903](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-encodedoutofrangesparseslot-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_contractDriftColumn8Blocked_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_contractDriftColumn8Blocked_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route contract drift column 8 blocked n 3”; its local proof does not by itself complete the broader paper route. The theorem route carries the active column-8 'O\_D^BS' contract-drift guard.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route carries the active column-8 'O\_D^BS' contract-drift guard. For 'n = 3', source column '8' maps to the Lemma 1 paper-image row '40' in the route's active 'O\_D^BS' gate. The legacy helper still has a row-'4' entry, so this guard keeps the active/legacy separation visible at the theorem route without proving injectivity, dagger cleanup, or block correctness.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1931](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-contractdriftcolumn8blocked-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_sparseAccessContractIdentity" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_sparseAccessContractIdentity")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route sparse access contract identity”; its local proof does not by itself complete the broader paper route. The theorem-level route uses the default Lemma 1 'O\_D^BS' contract object.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route uses the default Lemma 1 'O\_D^BS' contract object. This guard prevents a later lower packet from swapping in a different sparse-access contract while preserving similar-looking field values. It does not prove the oracle image, dagger cleanup, or unitary extension.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1961](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-sparseaccesscontractidentity). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsPaperContractTranscript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsPaperContractTranscript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs paper contract transcript”; its local proof does not by itself complete the broader paper route. The theorem-level route carries the Lemma 1 'O\_D^BS' paper contract verbatim.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route carries the Lemma 1 'O\_D^BS' paper contract verbatim. This is a source-transcript guard. It pins the padded input/output ket formula and the register widths while keeping all paper-contract semantic flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:1985](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbspapercontracttranscript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsRestrictedDaggerColumnIndicator" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsRestrictedDaggerColumnIndicator")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs restricted dagger column indicator”; its local proof does not by itself complete the broader paper route. The theorem-level route exposes the active-domain 'O\_D^BS' dagger-column indicator.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route exposes the active-domain 'O\_D^BS' dagger-column indicator. For the fixed one-term Robin parameters, this guard routes the compiled global-slot cleanup evidence through 'oneTermRobinBlockEncodingProofRoute'. It is still restricted to rows satisfying 'bandedSparseAccessPaperGlobalSlotSource', and it keeps every theorem-level cleanup, unitarity, LCU, projection, and block-correctness flag false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2034](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbsrestricteddaggercolumnindicator). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsCleanupScopeDecision" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsCleanupScopeDecision")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs cleanup scope decision”; its local proof does not by itself complete the broader paper route. The theorem route selects the active global-source domain as the next 'O\_D^BS' cleanup theorem scope.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route selects the active global-source domain as the next 'O\_D^BS' cleanup theorem scope. This is a proof-search scope guard, not a cleanup proof. It connects the route to the compiled restricted dagger-column indicator and records that full clean-domain cleanup, full-space unitary extension, LCU correctness, and final block-correctness obligations remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2118](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbscleanupscopedecision). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsFullCleanDomainImageRuleBlocked" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsFullCleanDomainImageRuleBlocked")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs full clean domain image rule blocked”; its local proof does not by itself complete the broader paper route. The theorem route keeps the full clean-domain 'O\_D^BS' image-rule slot blocked.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route keeps the full clean-domain 'O\_D^BS' image-rule slot blocked. This is a source-contract guard for the scope decision. The route may use the active global-source cleanup interface, but the full clean-domain wrapper still has no unused-branch image rule and cannot promote cleanup, unitarity, LCU, or block correctness.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2175](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbsfullcleandomainimageruleblocked). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveGlobalSourceCleanupInterface" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveGlobalSourceCleanupInterface")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs active global source cleanup interface”; its local proof does not by itself complete the broader paper route. The theorem-level route exposes the selected active global-source cleanup interface for 'O\_D^BS'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route exposes the selected active global-source cleanup interface for 'O\_D^BS'. This is only an interface wrapper around the compiled active-domain dagger column and the cleanup-scope decision. It does not promote 'daggerCleanup', unitarity, LCU correctness, block projection, block correctness, or final block extraction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2235](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbsactiveglobalsourcecleanupinterface). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveGlobalSourceCleanupContractMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_odbsActiveGlobalSourceCleanupContractMap")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route odbs active global source cleanup contract map”; its local proof does not by itself complete the broader paper route. The theorem-level route exposes the active global-source cleanup contract map.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-level route exposes the active global-source cleanup contract map. This guard packages the current proof-DAG block for post-SWAP inverse evidence: the named candidate is an active global-source preimage of the post-SWAP target, it is unique among active global-source rows, and the transpose-style dagger entry is '1'. The statement is still restricted to 'bandedSparseAccessPaperGlobalSlotSource'; it does not promote paper-contract cleanup, full clean-domain cleanup, full-space unitarity, LCU correctness, or block extraction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2325](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-odbsactiveglobalsourcecleanupcontractmap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_theoremTranscriptDependencies" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_theoremTranscriptDependencies")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route theorem transcript dependencies”; its local proof does not by itself complete the broader paper route. The theorem route exposes the source transcript dependencies for Theorem '1 term robin'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route exposes the source transcript dependencies for Theorem '1 term robin'. This is a guard-only Phase 1 declaration. It ties the theorem source anchor, normalizer, gate order, active 'O\_D^BS' global-source scope, 'O\_f' external source, signal-index-zero target, and current false proof flags into one reviewer-facing checkpoint. It does not prove cleanup, unitarity, LCU correctness, block projection, block correctness, or final block extraction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2422](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-theoremtranscriptdependencies). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_theoremTranscriptActiveCleanupMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_theoremTranscriptActiveCleanupMap")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route theorem transcript active cleanup map”; its local proof does not by itself complete the broader paper route. The theorem transcript consumes the active global-source cleanup map.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem transcript consumes the active global-source cleanup map. This is the next guard-only proof-DAG bridge after the cleanup contract map: it exposes the active-source post-SWAP preimage data while also pinning the one-term theorem source, normalizer, circuit order, sparse-access formula, and 'O\_f' source transcript. The bridge remains restricted to 'bandedSparseAccessPaperGlobalSlotSource' and does not promote semantic cleanup, unitarity, LCU correctness, block projection, block correctness, or final block extraction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2527](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-theoremtranscriptactivecleanupmap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_robinClarifiedGammaTranscript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_robinClarifiedGammaTranscript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route robin clarified gamma transcript”; its local proof does not by itself complete the broader paper route. The theorem transcript exposes the Eq.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem transcript exposes the Eq. ROBIN clarified gamma decomposition. This guard ties 'defaultRobinWavefunctionDecomposition' to the one-term theorem route, the active global-source cleanup map, and the external 'O\_f' source record. It records the three gamma normalizers and keeps the final semantic flags false; it is not a block-extraction proof.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2617](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-robinclarifiedgammatranscript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_blockProjectionDependencyMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_blockProjectionDependencyMap")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route block projection dependency map”; its local proof does not by itself complete the broader paper route. The theorem transcript exposes the dependency map for the final block projection.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem transcript exposes the dependency map for the final block projection. This is a contract-only Phase 1 map. It packages the Eq. ROBIN gamma transcript, active-source 'O\_D^BS' cleanup evidence, the 'CircuitBlockEncodingClaim' projection target, the full clean-domain blocker, and the external 'O\_f' source contract. It does not prove the signal block equation or promote LCU, cleanup, unitarity, projection, block-correctness, or final extraction flags.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2711](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-blockprojectiondependencymap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_fullGateContractLedger" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_fullGateContractLedger")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route full gate contract ledger”; its local proof does not by itself complete the broader paper route. The theorem route exposes one ledger for all Fig.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route exposes one ledger for all Fig. 1-term Robin gate contracts. This is a guard-only aggregation step for Phase 1. It consumes the compiled 'O\_DT^S'/'Ry\_boundary' bridge, the active-source 'O\_D^BS' cleanup map, and the external 'O\_f' source transcript. It freezes the seven gate slots and keeps all paper-oracle, LCU, projection, and final block-extraction flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:2829](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-fullgatecontractledger). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_theoremTranscriptClosurePacket" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_theoremTranscriptClosurePacket")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route theorem transcript closure packet”; its local proof does not by itself complete the broader paper route. The theorem-transcript closure packet consumes the current Phase 1 guards.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem-transcript closure packet consumes the current Phase 1 guards. This is the middle-agent checkpoint for Theorem '1 term robin': it combines the source transcript dependencies, layout/projection audit, block-projection dependency map, and full Fig. 1-term Robin gate-contract ledger into one reviewer-facing statement. It records the exact false-obligation ledger and does not promote cleanup, unitarity, LCU correctness, projection, block-correctness, resource-bound, ancilla-cleanup, or final extraction flags.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3043](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-theoremtranscriptclosurepacket). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_finiteBlockCompositionContractMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_finiteBlockCompositionContractMap")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route finite block composition contract map”; its local proof does not by itself complete the broader paper route. The theorem route now has a typed finite LCU/block-composition contract.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route now has a typed finite LCU/block-composition contract. This guard consumes the Phase 1 closure packet and exposes the exact remaining finite-dimensional composition obligations. It keeps the route-level LCU, circuit-unitary, block-projection, block-correctness, and final-extraction flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3197](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-finiteblockcompositioncontractmap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_finiteCompositionExactTheoremInterface" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_finiteCompositionExactTheoremInterface")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route finite composition exact theorem interface”; its local proof does not by itself complete the broader paper route. The theorem route exposes the exact finite composition theorem interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The theorem route exposes the exact finite composition theorem interface. This consumes the finite block-composition contract map and names the precise matrix objects that a future theorem must relate: the route circuit semantics, the signal-zero block projection, the row-scaled Robin target matrix, and the normalizer 'N\_D \* N\_f \* kappa'. It is contract-only; all finite composition, route LCU, resource, cleanup, projection, block-correctness, and extraction flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3283](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-finitecompositionexacttheoreminterface). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SignalBlockEntryObligation" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SignalBlockEntryObligation")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 signal block entry obligation”. Contract-only entry obligation connecting Eq.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Contract-only entry obligation connecting Eq. 'ROBIN clarified' to the signal-zero block matrix. The future theorem must show, entry by entry, that the signal-zero projection of the Fig. 1-term Robin gate product realizes the 'gamma3' clean branch and therefore the row-scaled Robin target normalized by 'N\_D \* N\_f \* kappa'. This declaration only names that missing theorem-facing step.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3422](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3signalblockentryobligation). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SignalBlockEntryObligation_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SignalBlockEntryObligation_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 signal block entry obligation transcript”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3430](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3signalblockentryobligation-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3SignalBlockEntryObligationMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3SignalBlockEntryObligationMap")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 signal block entry obligation map”; its local proof does not by itself complete the broader paper route. The exact finite-composition interface is refined to the gamma3 entry target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The exact finite-composition interface is refined to the gamma3 entry target. This is still a Phase 1 transcript guard. It consumes the exact finite theorem interface, exposes the 'gamma3' normalizer, the concrete signal-projection entry, the target matrix, and the false final flags. It does not prove that the entry equals the paper coefficient, nor does it promote LCU, projection, block-correctness, resource, cleanup, or extraction obligations.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3447](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3signalblockentryobligationmap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3TargetEntryData" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3TargetEntryData")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 target entry data”; its local proof does not by itself complete the broader paper route. The gamma3 entry obligation also exposes the concrete target entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The gamma3 entry obligation also exposes the concrete target entry. This is the RHS data for the future entry theorem: the same fixed system indices 'i, j' point to 'f(x\_i) D\_\{ij\}', with normalizer 'N\_D\*N\_f\*kappa'. The statement intentionally does not prove that the circuit block entry equals this target entry; the normalized block equality and final extraction flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3540](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3targetentrydata). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3FactorEntryLedger" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3FactorEntryLedger")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 factor entry ledger”; its local proof does not by itself complete the broader paper route. The gamma3 factor-entry ledger joins the existing single-gate transcript bridges.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The gamma3 factor-entry ledger joins the existing single-gate transcript bridges. This is the next theorem-facing interface for the future 'one\_term\_gamma3\_signal\_block\_entry' proof. It packages the target-entry side, the clean 'O\_f' entry, the 'O\_DT^S' ket-zero entry, the boundary 'Ry\_boundary' ket-zero entry, and the active global-source 'O\_D^BS' cleanup map. It is still a ledger: the normalized block equality, LCU composition, cleanup promotion, and final extraction fields remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3622](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3factorentryledger). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3SignalBlockProductEntry" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3SignalBlockProductEntry")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 signal block product entry”; its local proof does not by itself complete the broader paper route. The gamma3 signal-block entry is the concrete seven-gate product entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The gamma3 signal-block entry is the concrete seven-gate product entry. This is a matrix-semantics bridge, not the final coefficient theorem. It consumes the factor-entry ledger and exposes that the signal-zero projected entry is an entry of 'evalGateMatrices' over the Fig. 1-term Robin gate list. The finite product still has to be related to the Eq. 'ROBIN clarified' coefficient, so the normalized-block, LCU, projection, and extraction flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3845](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3signalblockproductentry). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3AkCoefficientEntryContract" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3AkCoefficientEntryContract")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 ak coefficient entry contract”; its local proof does not by itself complete the broader paper route. The gamma3 coefficient-entry contract is now tied to the Ak target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The gamma3 coefficient-entry contract is now tied to the Ak target. This is still a contract bridge, not the finite coefficient theorem. It reuses the concrete signal-block product entry, the factor-entry ledger, and the Ak target expansion 'oneTermRobinAkMatrix n i j = f(x\_i) \* D\_ij'. The product-to-coefficient equality, LCU composition, oracle analytic correctness, cleanup, unitarity, projection, and final extraction flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:3982](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3akcoefficiententrycontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProductToCoefficientObligation" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProductToCoefficientObligation")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 product to coefficient obligation”. Named product-to-coefficient obligation for the gamma3 entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Named product-to-coefficient obligation for the gamma3 entry. The future theorem must multiply the already ledgered factor entries in the signal-zero product into the normalized Ak entry. This declaration only names that remaining finite entry theorem; it does not assert the equality.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4220](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3producttocoefficientobligation). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProductToCoefficientObligation_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProductToCoefficientObligation_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 product to coefficient obligation transcript”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4228](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3producttocoefficientobligation-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3ProductToCoefficientInterface" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3ProductToCoefficientInterface")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 product to coefficient interface”; its local proof does not by itself complete the broader paper route. Interface for the exact finite product-to-coefficient theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Interface for the exact finite product-to-coefficient theorem. This guard consumes the compiled gamma3 Ak coefficient-entry contract and exposes the remaining theorem-facing obligation: the signal-zero product entry must equal the Ak coefficient normalized by 'N\_D\*N\_f\*kappa'. It keeps the entry obligation, LCU composition, projection, cleanup, unitarity, and final extraction flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4245](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3producttocoefficientinterface). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3ProjectionPathAudit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3ProjectionPathAudit_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 projection path audit n 3”; its local proof does not by itself complete the broader paper route. Focused path-state audit for the current 'n = 3' gamma3 product attempt.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused path-state audit for the current 'n = 3' gamma3 product attempt. The signal-zero projection sends system entry '(2, 5)' to the full entry '(2, 5)'. The executable gate images then show that the projected-column forward path and the existing factor-entry ledger columns are not one coherent seven-gate path. This is a register-layout audit only: it does not unfold the full product and does not promote any semantic proof flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4417](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3projectionpathaudit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3PaperBasisIndex" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3PaperBasisIndex")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 paper basis index”. Full-basis index for the clean 'gamma3' ket layout in Eq.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Full-basis index for the clean 'gamma3' ket layout in Eq. 'ROBIN clarified'. This is a Phase 1 layout helper, not a new projection convention. It places the trailing rotation ancilla at bit '0', the system register in bits '\[1, 1+n)', the padded 'O\_D^BS' zero register next, and the sparse slot above that padded register, with all higher 'm\_f' and indicator workspace bits set to zero.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4492](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3paperbasisindex). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3PaperBasisLayout_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3PaperBasisLayout_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 paper basis layout n 3”; its local proof does not by itself complete the broader paper route. Layout contract for the next gamma3 path attempt at 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Layout contract for the next gamma3 path attempt at 'n = 3'. Eq. 'ROBIN clarified' places the clean 'gamma3' basis states for system entry '(2, 5)' at full indices '(4, 10)' when the sparse slot is '0'. The existing 'signalSystemBlockProjection' convention instead selects full indices '(2, 5)'. This theorem records that mismatch together with the relevant clean-register extractions, so the product-to-coefficient route can choose a coherent block index before applying the reusable unique-path product lemma.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4507](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3paperbasislayout-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3PaperBasisPathAudit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3PaperBasisPathAudit_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 paper basis path audit n 3”; its local proof does not by itself complete the broader paper route. Focused Fig.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused Fig. 1-term Robin path audit for the clean 'gamma3' paper-basis endpoints at 'n = 3'. Starting from the paper clean-column index '10', the ket-zero branch follows the active seven-gate images to final dagger row '198', not to the paper clean-row index '4'. The first decisive drift is the active 'O\_D^BS' sparse-slot-zero address: after 'U\_indic' and the identity 'Ry\_boundary' branch, it writes address '3', so SWAP exposes system row '3' before the dagger cleanup. This is a path-state audit only; it does not apply the unique-path product lemma and does not promote any semantic proof flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4565](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3paperbasispathaudit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3SparseSlotAlignment_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3SparseSlotAlignment_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 sparse slot alignment n 3”; its local proof does not by itself complete the broader paper route. Sparse-slot alignment audit for the focused 'n = 3' gamma3 coefficient 'D\_\{2,5\}'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Sparse-slot alignment audit for the focused 'n = 3' gamma3 coefficient 'D\_\{2,5\}'. The slot-zero paper-basis path remains useful negative evidence: it maps source column '5' to address '3', so it cannot be the route for target row '2'. The finite global-slot table instead selects slot '5', the '-3' diagonal, for the coefficient from source column '5' to target row '2'. This theorem only chooses the slot and clean endpoint data needed by the next path isolation packet; it does not apply the unique-path multiplication lemma or promote any semantic proof flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4648](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3sparseslotalignment-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProjectionSlotConventionObligation" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProjectionSlotConventionObligation")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 projection slot convention obligation”. Source-contract obligation for the gamma3 projection-slot convention.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Source-contract obligation for the gamma3 projection-slot convention. Eq. 'ROBIN clarified' sums the clean 'gamma3' branch over sparse slots. The finite path audit for a matrix entry therefore needs an interface that relates the slot-specific clean basis state with 's' satisfying 'r\_\{s,j\}=i' to the theorem-level signal-zero block projection or sparse-register summation. This declaration names that missing convention without proving it.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4717](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3projectionslotconventionobligation). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProjectionSlotConventionObligation_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProjectionSlotConventionObligation_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 projection slot convention obligation transcript”; its local proof does not by itself complete the broader paper route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The source declaration has no docstring. The reader cue above is generated from its kind and name and does not replace the Lean signature.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4725](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3projectionslotconventionobligation-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3ProjectionSlotConventionMap_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3ProjectionSlotConventionMap_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 projection slot convention map n 3”; its local proof does not by itself complete the broader paper route. Focused projection-slot contract map for the compiled 'n = 3' gamma3 audit.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused projection-slot contract map for the compiled 'n = 3' gamma3 audit. The previous slot-alignment audit shows that the coefficient for the system entry '(2, 5)' uses sparse slot '5', not slot '0'. This theorem packages the slot-specific clean endpoints '90' and '84' and records that they are still not the generic signal-zero projection endpoints '(2, 5)'. The remaining projection-slot convention is deliberately kept as an unproved obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4742](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3projectionslotconventionmap-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3Slot5PathAudit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3Slot5PathAudit_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 slot 5 path audit n 3”; its local proof does not by itself complete the broader paper route. Focused Fig.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused Fig. 1-term Robin path audit for the slot-'5' clean 'gamma3' endpoints at 'n = 3'. The slot-alignment map gives the clean endpoint chain '90 -> 42 -> 84' if the path starts directly at 'O\_D^BS'. The actual seven-gate circuit first applies 'U\_indic', which flips the indicator bit for system column '5', so the active path starts from '218'. The ket-zero branch then reaches final dagger row '228', not the slot-specific clean row '84'. This declaration records the adjacent states only; it does not apply a product lemma or promote any semantic proof flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4811](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3slot5pathaudit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3Slot5ProjectionRegisterAuditCheck_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3Slot5ProjectionRegisterAuditCheck_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 slot 5 projection register audit check n 3”. Executable field check for the slot-'5' gamma3 projection/register audit.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Executable field check for the slot-'5' gamma3 projection/register audit. The checked path is the ket-zero branch '90 -> 218 -> 218 -> 218 -> 170 -> 170 -> 212 -> 228'. The Boolean records the indicator, ancilla, system-row, padded-zero, sparse-index, 'm\_f' workspace, and active-source fields for the clean source, adjacent states, final endpoint, and clean Eq. ROBIN endpoint.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:4925](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3slot5projectionregisterauditcheck-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3Slot5ProjectionRegisterAudit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3Slot5ProjectionRegisterAudit_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 slot 5 projection register audit n 3”; its local proof does not by itself complete the broader paper route. Projection/register audit for the slot-'5' gamma3 path at 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Projection/register audit for the slot-'5' gamma3 path at 'n = 3'. The first field-level mismatch between the final seven-gate endpoint '228' and the clean Eq. ROBIN endpoint '84' is the indicator bit: the full path keeps the bulk indicator set to '1', while the clean endpoint has indicator bit '0'. The sparse-index field also differs ('6' versus '5'). No semantic proof flag is promoted.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5068](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3slot5projectionregisteraudit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3ProjectionRegisterConventionDecision" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3ProjectionRegisterConventionDecision")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 projection register convention decision”. A proposition-valued field is a requirement until a constructor supplies it. Middle-agent decision record for the blocked gamma3 projection/register convention at 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Middle-agent decision record for the blocked gamma3 projection/register convention at 'n = 3'. The source transcript provides Eq. ROBIN clarified, Fig. 1-term ROBIN, and the block-encoding projection definition, but it does not specify the finite basis bridge that would identify the full seven-gate endpoint '228' with the clean slot-'5' endpoint '84'. This record keeps product search blocked until that convention is stated precisely.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5100](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3projectionregisterconventiondecision). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProjectionRegisterConventionDecision_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProjectionRegisterConventionDecision_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 projection register convention decision n 3”. The focused gamma3 endpoint mismatch is a source-contract gap, not a finite matrix multiplication target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The focused gamma3 endpoint mismatch is a source-contract gap, not a finite matrix multiplication target.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5121](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3projectionregisterconventiondecision-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProjectionRegisterConventionDecision_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3ProjectionRegisterConventionDecision_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 projection register convention decision n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the middle decision record.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the middle decision record. This theorem deliberately preserves the false semantic flags. It only records that the compiled register audit has converted the next step into a projection/register convention decision before any product-to-coefficient proof search may continue.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5162](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3projectionregisterconventiondecision-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3SparseRegisterSummationConvention" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3SparseRegisterSummationConvention")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 sparse register summation convention”. A proposition-valued field is a requirement until a constructor supplies it. Chosen theorem-facing convention for the focused 'n = 3' gamma3 entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Chosen theorem-facing convention for the focused 'n = 3' gamma3 entry. Eq. 'ROBIN clarified' writes the gamma3 contribution as a sum over sparse slots, so the next interface selects sparse-register summation. The compiled slot-'5' audit also found an indicator-bit mismatch between the full endpoint '228' and the clean endpoint '84'; that mismatch is kept as a separate false obligation instead of being hidden by the summation choice.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5195](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3sparseregistersummationconvention). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SparseRegisterSummationConvention_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SparseRegisterSummationConvention_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 sparse register summation convention n 3”. Sparse-register summation convention selected for the slot-'5' gamma3 audit.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Sparse-register summation convention selected for the slot-'5' gamma3 audit. This is a contract map only. It records the source-supported summation over 's = 0, ..., kappa - 1', but it does not prove that the current block projection implements that summation. The indicator mismatch remains open.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5228](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3sparseregistersummationconvention-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SparseRegisterSummationConvention_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SparseRegisterSummationConvention_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 sparse register summation convention n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the selected sparse-register summation convention.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the selected sparse-register summation convention. The theorem proves only the compiled contract map and endpoint facts. It keeps product-to-coefficient search blocked and preserves all semantic false flags.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5292](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3sparseregistersummationconvention-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SparseRegisterSummation_indicatorGap_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3SparseRegisterSummation_indicatorGap_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 sparse register summation indicator gap n 3”; its local proof does not by itself complete the broader paper route. Indicator-field gap after selecting sparse-register summation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Indicator-field gap after selecting sparse-register summation. The sparse-register summation convention is source-backed by Eq. 'ROBIN clarified', but it does not explain why the full seven-gate endpoint keeps the indicator bit set. This theorem packages that remaining field-level source contract gap and keeps product-to-coefficient search blocked.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5332](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3sparseregistersummation-indicatorgap-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3IndicatorProjectionConvention" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3IndicatorProjectionConvention")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 indicator projection convention”. A proposition-valued field is a requirement until a constructor supplies it. Indicator-field projection/register convention for the focused 'n = 3' gamma3 endpoint pair.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Indicator-field projection/register convention for the focused 'n = 3' gamma3 endpoint pair. After sparse-register summation has been selected, the remaining question is whether the theorem-level block projection sums, ignores, resets, or permutes the indicator field that differs between full endpoint '228' and clean endpoint '84'. The GHL2025 transcript has not yet supplied that rule, so the convention is recorded as a false source-contract obligation rather than a product proof.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5380](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3indicatorprojectionconvention). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3IndicatorProjectionConvention_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3IndicatorProjectionConvention_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 indicator projection convention n 3”. The active gamma3 indicator convention is still an explicit source-contract gap.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The active gamma3 indicator convention is still an explicit source-contract gap. This declaration is deliberately theorem-facing but not a semantic proof. It reuses the sparse-register summation gap and keeps all block-encoding flags false until a source-backed projection/register rule is stated.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5408](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3indicatorprojectionconvention-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3IndicatorProjectionConvention_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3IndicatorProjectionConvention_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 indicator projection convention n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the active gamma3 indicator convention.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the active gamma3 indicator convention. The theorem packages the endpoint and false-obligation facts needed by the next proof step. It does not identify endpoints '228' and '84', and it does not promote product-to-coefficient, LCU, projection, block, or final extraction flags.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5458](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3indicatorprojectionconvention-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BulkIndicatorSourceAudit" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BulkIndicatorSourceAudit")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 bulk indicator source audit”. A proposition-valued field is a requirement until a constructor supplies it. Focused source audit for the bulk-indicator field in the 'n = 3' gamma3 endpoint pair.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused source audit for the bulk-indicator field in the 'n = 3' gamma3 endpoint pair. For the entry using system column '5', the paper's bulk window 'K1 <= j <= K2' classifies the column as bulk. The source-backed 'U\_indic' behavior therefore sets the indicator to '1', which matches the full Fig. 1-term Robin endpoint '228' and not the clean endpoint '84'. This refines the active blocker without closing it: the source still does not state a projection/register rule that identifies the two endpoints, and all product, LCU, projection, block, and extraction flags remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5514](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3bulkindicatorsourceaudit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BulkIndicatorSourceAudit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BulkIndicatorSourceAudit_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 bulk indicator source audit n 3”. Source-backed refinement of the active indicator convention blocker.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Source-backed refinement of the active indicator convention blocker. The focused column '5' is in the bulk window for 'n = 3', so the indicator value '1' at endpoint '228' is not accidental; it is exactly the value produced by the 'U\_indic' source paragraph. Endpoint '84' remains the clean displayed slot endpoint, and no reset/projection rule is promoted.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5544](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3bulkindicatorsourceaudit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BulkIndicatorSourceAudit_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BulkIndicatorSourceAudit_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 bulk indicator source audit n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the bulk-indicator source audit.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the bulk-indicator source audit. This theorem only records the source-backed branch classification and the remaining false obligations. It does not replace the missing projection/register convention and does not resume product multiplication.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5581](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3bulkindicatorsourceaudit-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BranchCorrectSourceMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BranchCorrectSourceMap")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 branch correct source map”. A proposition-valued field is a requirement until a constructor supplies it. Branch-correct source map for the focused 'n = 3' gamma3 transcript.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Branch-correct source map for the focused 'n = 3' gamma3 transcript. The older endpoint audit compared the bulk column 'j = 5' against the displayed boundary summand of Eq. 'ROBIN clarified'. This record keeps that bulk audit as omitted-branch memory and introduces a boundary-focused endpoint with 'j = 0', where 'U\_indic' leaves the indicator at '0'. It is a transcript map only; both branch product obligations remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5632](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3branchcorrectsourcemap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BranchCorrectSourceMap_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BranchCorrectSourceMap_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 branch correct source map n 3”. Compiled branch-correct gamma3 transcript for 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled branch-correct gamma3 transcript for 'n = 3'. The boundary target uses 'j = 0', satisfying the displayed condition '0 <= j < K1'. The old 'j = 5' target satisfies 'K1 <= j <= K2', so it belongs to the omitted bulk summand hidden by '+ ...'. Lower proof search may now target one branch-specific product interface at a time, but no theorem-level semantic flag is promoted here.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5670](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3branchcorrectsourcemap-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BranchCorrectSourceMap_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BranchCorrectSourceMap_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 branch correct source map n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the branch-correct gamma3 source map.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the branch-correct gamma3 source map. This theorem is the handoff boundary between the old bulk endpoint audit and the next lower packet. It proves only branch classification and endpoint facts; the boundary and bulk product-to-coefficient obligations, LCU composition, projection, block correctness, and final extraction stay false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5731](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3branchcorrectsourcemap-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryBranchPathAudit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryBranchPathAudit_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary branch path audit n 3”; its local proof does not by itself complete the broader paper route. Boundary-focused path audit for the displayed gamma3 branch at 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Boundary-focused path audit for the displayed gamma3 branch at 'n = 3'. The branch-correct source map chooses the boundary column 'j = 0', so 'U\_indic' leaves the indicator bit at '0'. For the target entry '(0, 0)', the sparse slot that maps the source column back to row '0' is slot '2' (offset '0'), not slot '0' (offset '6'). This theorem records the resulting slot-'2' clean path through the Fig. 1-term Robin gate images. It is only a path-state audit: the product-to-coefficient obligation and all block-encoding semantic flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5792](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundarybranchpathaudit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BulkProductInterface" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BulkProductInterface")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 bulk product interface”. A proposition-valued field is a requirement until a constructor supplies it. Bulk-specific interface for the omitted gamma3 product branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Bulk-specific interface for the omitted gamma3 product branch. The old focused column 'j = 5' is bulk for 'n = 3', 'K1 = 2', and 'K2 = 5'. It therefore belongs to the summand hidden by the '+ ...' in Eq. 'ROBIN clarified', not to the displayed boundary branch. This interface uses the source-backed full endpoint with indicator '1'; it does not compare that endpoint with the displayed boundary endpoint and does not prove the final product-to-coefficient theorem.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5908](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3bulkproductinterface). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BulkProductToCoefficientInterface_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BulkProductToCoefficientInterface_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin block encoding proof route gamma 3 bulk product to coefficient interface n 3”. Compiled product interface for the omitted bulk branch at 'n = 3', system entry '(2,5)', and global sparse slot '5'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled product interface for the omitted bulk branch at 'n = 3', system entry '(2,5)', and global sparse slot '5'. The factor list follows the Fig. 1-term Robin gate order 'U\_indic', 'O\_DT^S', 'Ry\_boundary', 'O\_D^BS', 'O\_f', 'SWAP', 'O\_D^BS†'. Because the column is bulk, 'U\_indic' sets the indicator bit to '1', 'O\_DT^S' supplies the derivative-amplitude factor, and 'Ry\_boundary' acts as identity.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:5957](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3bulkproducttocoefficientinterface-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BulkProductToCoefficientInterface_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BulkProductToCoefficientInterface_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 bulk product to coefficient interface n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the omitted bulk product interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the omitted bulk product interface. This theorem proves only branch classification, endpoint data, and the gate-factor ledger for the source-backed bulk path. The unique-path support, indicator projection convention, product-to-coefficient equality, LCU composition, block projection, block correctness, and final extraction remain false obligations.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6054](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3bulkproducttocoefficientinterface-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProductInterface" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProductInterface")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary product interface”. A proposition-valued field is a requirement until a constructor supplies it. Boundary-specific interface for the next gamma3 product theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Boundary-specific interface for the next gamma3 product theorem. The displayed boundary branch of Eq. 'ROBIN clarified' at 'n = 3', '(i,j) = (0,0)' uses sparse slot '2'. The compiled path audit isolates the seven Fig. 1-term Robin factors for the ket-zero branch, but this record does not claim that the full matrix product has already been reduced to that path. The unique-path support facts and product-to-coefficient equality remain false obligations.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6178](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryproductinterface). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductToCoefficientInterface_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductToCoefficientInterface_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin block encoding proof route gamma 3 boundary product to coefficient interface n 3”. Compiled boundary product interface for the 'n = 3', '(0,0)', sparse-slot-'2' gamma3 packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled boundary product interface for the 'n = 3', '(0,0)', sparse-slot-'2' gamma3 packet. The factor list follows the gate order 'U\_indic', 'O\_DT^S', 'Ry\_boundary', 'O\_D^BS', 'O\_f', 'SWAP', 'O\_D^BS†'. The ket-zero branch factors are recorded, but applying 'Matrix.evalWith\_mul\_unique\_path' is left to the next finite support proof.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6218](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundaryproducttocoefficientinterface-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductToCoefficientInterface_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductToCoefficientInterface_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary product to coefficient interface n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the boundary product interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the boundary product interface. This proves the branch-specific data and factor list used by the next unique-path product attempt. It deliberately keeps the unique-path support obligation, product-to-coefficient obligation, projection-slot convention, LCU composition, block projection, block correctness, and final extraction false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6304](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundaryproducttocoefficientinterface-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryUniquePathSupportAudit" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryUniquePathSupportAudit")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary unique path support audit”. A proposition-valued field is a requirement until a constructor supplies it. Boundary unique-path support audit for the displayed 'n = 3' gamma3 branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Boundary unique-path support audit for the displayed 'n = 3' gamma3 branch. This record is intentionally narrower than the final product theorem. It proves the concrete adjacent-branch zero entries currently available from the gate skeletons, then names the first missing global support interface needed before 'Matrix.evalWith\_mul\_unique\_path' can isolate the full seven-gate product.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6410](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryuniquepathsupportaudit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryUniquePathSupportAudit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryUniquePathSupportAudit_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin block encoding proof route gamma 3 boundary unique path support audit n 3”. Compiled audit for the first boundary unique-path support packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled audit for the first boundary unique-path support packet. The target path is the ket-zero branch '32 -> 32 -> 32 -> 32 -> 0 -> 0 -> 0 -> 32'. The adjacent boundary-rotation ket-one branch reaches the row-'33' endpoint, and its contribution to target row '32' is killed by concrete zero entries in the current 'O\_f' and dagger matrices. The remaining all-other-path support theorem is still an explicit false obligation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6449](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundaryuniquepathsupportaudit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryUniquePathSupport_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryUniquePathSupport_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary unique path support n 3”; its local proof does not by itself complete the broader paper route. First boundary unique-path support result.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* First boundary unique-path support result. This theorem compiles the concrete zero entries for the adjacent ket-one branch and records the remaining missing prefix-support theorem. It deliberately does not prove the all-path support condition, does not apply 'Matrix.evalWith\_mul\_unique\_path' to the seven-gate product, and does not promote any product, projection, LCU, block-correctness, or extraction flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6521](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundaryuniquepathsupport-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixParameters_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixParameters_n3")
*Plain-English reading.* This abbreviation gives a shorter name to the type or expression used for “one term robin gamma 3 boundary prefix parameters n 3”. Parameters for the focused 'n = 3' displayed-boundary gamma3 prefix packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Parameters for the focused 'n = 3' displayed-boundary gamma3 prefix packet.

*Declaration kind.* abbrev.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6578](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixparameters-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixDim_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixDim_n3")
*Plain-English reading.* This abbreviation gives a shorter name to the type or expression used for “one term robin gamma 3 boundary prefix dim n 3”. Full matrix dimension for the focused boundary gamma3 prefix packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Full matrix dimension for the focused boundary gamma3 prefix packet.

*Declaration kind.* abbrev.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6583](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixdim-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixSource_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixSource_n3")
*Plain-English reading.* This abbreviation gives a shorter name to the type or expression used for “one term robin gamma 3 boundary prefix source n 3”. Full source column '32' for the focused boundary gamma3 prefix packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Full source column '32' for the focused boundary gamma3 prefix packet.

*Declaration kind.* abbrev.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6588](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixsource-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixRow0_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixRow0_n3")
*Plain-English reading.* This abbreviation gives a shorter name to the type or expression used for “one term robin gamma 3 boundary prefix row 0 n 3”. Prefix row '0', the ket-zero image after the forward 'O\_D^BS' gate.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Prefix row '0', the ket-zero image after the forward 'O\_D^BS' gate.

*Declaration kind.* abbrev.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6593](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixrow0-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixRow1_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixRow1_n3")
*Plain-English reading.* This abbreviation gives a shorter name to the type or expression used for “one term robin gamma 3 boundary prefix row 1 n 3”. Prefix row '1', the adjacent ket-one image after the forward 'O\_D^BS' gate.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Prefix row '1', the adjacent ket-one image after the forward 'O\_D^BS' gate.

*Declaration kind.* abbrev.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6598](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixrow1-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixMatrix_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary du prefix matrix n 3”. Two-gate prefix 'O\_DT^S \* U\_indic' for the displayed-boundary gamma3 packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Two-gate prefix 'O\_DT^S \* U\_indic' for the displayed-boundary gamma3 packet.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6607](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryduprefixmatrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixMatrix_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary rdu prefix matrix n 3”. Three-gate prefix 'Ry\_boundary \* O\_DT^S \* U\_indic'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Three-gate prefix 'Ry\_boundary \* O\_DT^S \* U\_indic'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6615](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrduprefixmatrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixMatrix_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prefix matrix n 3”. Four-gate prefix 'O\_D^BS \* Ry\_boundary \* O\_DT^S \* U\_indic'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Four-gate prefix 'O\_D^BS \* Ry\_boundary \* O\_DT^S \* U\_indic'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6623](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixmatrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixSupport_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixSupport_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary du prefix support n 3”; its local proof does not by itself complete the broader paper route. The two-gate boundary prefix has no evaluated support away from source column '32'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The two-gate boundary prefix has no evaluated support away from source column '32'. This is an evaluated-matrix support theorem. It does not simplify the raw symbolic 'Coeff' fold and does not promote the product-to-coefficient obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6746](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryduprefixsupport-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixSupport_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixSupport_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary rdu prefix support n 3”; its local proof does not by itself complete the broader paper route. The three-gate boundary prefix has evaluated support only in rows '32' and '33'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The three-gate boundary prefix has evaluated support only in rows '32' and '33'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6764](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrduprefixsupport-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryPrefixSupport_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryPrefixSupport_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary prefix support n 3”; its local proof does not by itself complete the broader paper route. Boundary prefix support for the displayed gamma3 branch at 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Boundary prefix support for the displayed gamma3 branch at 'n = 3'. For the branch-correct source column '32', the evaluated four-gate prefix 'O\_D^BS \* Ry\_boundary \* O\_DT^S \* U\_indic' can land only in rows '0' and '1'. This is the missing prefix-support block named by the previous audit. It does not prove the seven-gate product equality, projection-slot convention, LCU composition, block projection, block correctness, or final extraction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6789](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundaryprefixsupport-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryOfSwapMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryOfSwapMatrix_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary of swap matrix n 3”. Two-gate suffix 'SWAP \* O\_f' for the displayed-boundary gamma3 packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Two-gate suffix 'SWAP \* O\_f' for the displayed-boundary gamma3 packet.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6809](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryofswapmatrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySuffixMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySuffixMatrix_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary suffix matrix n 3”. Three-gate suffix '(O\_D^BS)^† \* SWAP \* O\_f'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Three-gate suffix '(O\_D^BS)^† \* SWAP \* O\_f'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6816](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysuffixmatrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySevenGateMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySevenGateMatrix_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary seven gate matrix n 3”. Full seven-gate matrix for the focused displayed-boundary gamma3 packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Full seven-gate matrix for the focused displayed-boundary gamma3 packet. This is only the finite matrix product for the branch-correct 'n = 3', row-'32', column-'32' support proof. It does not promote any semantic obligation on the theorem route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6830](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysevengatematrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryOfSwapRow0Col1_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryOfSwapRow0Col1_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary of swap row 0 col 1 zero n 3”; its local proof does not by itself complete the broader paper route. After 'O\_f' and 'SWAP', the adjacent ket-one column has no evaluated support at row '0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* After 'O\_f' and 'SWAP', the adjacent ket-one column has no evaluated support at row '0'. This is the suffix-side companion to the prefix support theorem. It uses the compiled clean-workspace zero entry 'O\_f\[0,1\] = 0' and SWAP row-'0' support instead of expanding the full symbolic product.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6899](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryofswaprow0col1-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySuffixRow32Col1_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySuffixRow32Col1_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary suffix row 32 col 1 zero n 3”; its local proof does not by itself complete the broader paper route. The suffix '(O\_D^BS)^† \* SWAP \* O\_f' kills the adjacent row-'1' branch when the target row is the boundary row '32'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The suffix '(O\_D^BS)^† \* SWAP \* O\_f' kills the adjacent row-'1' branch when the target row is the boundary row '32'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6923](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysuffixrow32col1-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundarySevenGateSupport_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundarySevenGateSupport_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary seven gate support n 3”; its local proof does not by itself complete the broader paper route. Seven-gate support for the displayed 'n = 3' gamma3 boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Seven-gate support for the displayed 'n = 3' gamma3 boundary branch. For the full product written as 'suffix \* prefix', every evaluated contribution from source column '32' to target row '32' vanishes unless the intermediate row between the prefix and suffix is row '0'. Rows outside '\{0,1\}' are killed by the compiled prefix-support theorem; row '1' is killed by the suffix-side 'O\_f'/SWAP/dagger support above. Product-to-coefficient, projection, LCU, block-correctness, and final-extraction obligations remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6947](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundarysevengatesupport-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundarySevenGateUniquePath_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundarySevenGateUniquePath_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary seven gate unique path n 3”; its local proof does not by itself complete the broader paper route. One-step unique-path reduction for the focused seven-gate boundary entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* One-step unique-path reduction for the focused seven-gate boundary entry. This applies the generic evaluated-product reducer to the already isolated row-'0' intermediate branch. It is not the gamma3 coefficient theorem and it does not change any 'proved' flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6972](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundarysevengateuniquepath-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixEntryEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixEntryEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary du prefix entry eval n 3”; its local proof does not by itself complete the broader paper route. The two-gate 'O\_DT^S \* U\_indic' prefix contributes unit amplitude on the boundary source column '32'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The two-gate 'O\_DT^S \* U\_indic' prefix contributes unit amplitude on the boundary source column '32'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:6997](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryduprefixentryeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixEntryEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixEntryEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary rdu prefix entry eval n 3”; its local proof does not by itself complete the broader paper route. The three-gate 'Ry\_boundary \* O\_DT^S \* U\_indic' prefix contributes the boundary half-angle cosine on source column '32'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The three-gate 'Ry\_boundary \* O\_DT^S \* U\_indic' prefix contributes the boundary half-angle cosine on source column '32'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7047](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrduprefixentryeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixEntryEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixEntryEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary prefix entry eval n 3”; its local proof does not by itself complete the broader paper route. The four-gate prefix entry from source column '32' to row '0' is the boundary half-angle cosine.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The four-gate prefix entry from source column '32' to row '0' is the boundary half-angle cosine.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7089](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixentryeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryOfSwapEntryEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryOfSwapEntryEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary of swap entry eval n 3”; its local proof does not by itself complete the broader paper route. The 'SWAP \* O\_f' suffix prefix on row/column '0' contributes the clean function-oracle amplitude 'f\_3\_0 \* N\_f\_inv'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The 'SWAP \* O\_f' suffix prefix on row/column '0' contributes the clean function-oracle amplitude 'f\_3\_0 \* N\_f\_inv'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7142](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryofswapentryeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySuffixEntryEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySuffixEntryEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary suffix entry eval n 3”; its local proof does not by itself complete the broader paper route. The three-gate suffix entry from row '32' to the row-'0' intermediate state is the clean function-oracle amplitude.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The three-gate suffix entry from row '32' to the row-'0' intermediate state is the clean function-oracle amplitude.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7193](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysuffixentryeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductEntryEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductEntryEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary product entry eval n 3”; its local proof does not by itself complete the broader paper route. Evaluated seven-gate product entry for the displayed boundary 'gamma3' packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Evaluated seven-gate product entry for the displayed boundary 'gamma3' packet. This proves the finite row-'32', column-'32' branch product after the compiled unique-path reduction. It is still only the branch product evaluation: the paper-level product-to-'A\_k' coefficient theorem, sparse-register projection convention, LCU composition, block projection, block correctness, and final extraction remain separate false obligations.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7240](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundaryproductentryeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixCol0Support_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixCol0Support_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary du prefix col 0 support n 3”; its local proof does not by itself complete the broader paper route. Two-gate 'O\_DT^S \* U\_indic' prefix support at column '0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Two-gate 'O\_DT^S \* U\_indic' prefix support at column '0'. Both 'U\_indic' and 'O\_DT^S' act as the identity on state '|0⟩' (indicator bit is zero), so the DU prefix at column '0' has support only at row '0'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7324](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryduprefixcol0support-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixCol0Support_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixCol0Support_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary rdu prefix col 0 support n 3”; its local proof does not by itself complete the broader paper route. Three-gate 'Ry \* O\_DT^S \* U\_indic' prefix support at column '0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Three-gate 'Ry \* O\_DT^S \* U\_indic' prefix support at column '0'. Since 'DU' feeds only row '0' into 'Ry', and 'Ry' at column '0' acts on the pair '\{0, 1\}', the RDU prefix at column '0' has support only at rows '\{0, 1\}'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7424](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrduprefixcol0support-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixCol0Support_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixCol0Support_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary prefix col 0 support n 3”; its local proof does not by itself complete the broader paper route. Four-gate prefix 'O\_D^BS \* Ry \* O\_DT^S \* U\_indic' support at column '0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Four-gate prefix 'O\_D^BS \* Ry \* O\_DT^S \* U\_indic' support at column '0'. The RDU prefix feeds rows '\{0, 1\}' into 'O\_D^BS'. Since 'image(0) = 96' and 'image(1) = 97', the full prefix at column '0' has support only at rows '\{96, 97\}'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7447](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixcol0support-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixCol0EntryEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryDUPrefixCol0EntryEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary du prefix col 0 entry eval n 3”; its local proof does not by itself complete the broader paper route. The two-gate prefix at column '0' contributes unit amplitude on row '0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The two-gate prefix at column '0' contributes unit amplitude on row '0'. This is the column-'0' analogue of 'oneTermRobinGamma3BoundaryDUPrefixEntryEval\_n3'; it feeds the two-path decomposition for the active '\[0,0\]' entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7473](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryduprefixcol0entryeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixRow0Col0_eval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixRow0Col0_eval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary rdu prefix row 0 col 0 eval n 3”; its local proof does not by itself complete the broader paper route. The three-gate column-'0' prefix row '0' is the slot-'0' boundary cosine entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The three-gate column-'0' prefix row '0' is the slot-'0' boundary cosine entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7520](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrduprefixrow0col0-eval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixRow1Col0_eval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRDUPrefixRow1Col0_eval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary rdu prefix row 1 col 0 eval n 3”; its local proof does not by itself complete the broader paper route. The three-gate column-'0' prefix row '1' is the slot-'0' boundary sine entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The three-gate column-'0' prefix row '1' is the slot-'0' boundary sine entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7559](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrduprefixrow1col0-eval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixRow96Col0_eval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixRow96Col0_eval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary prefix row 96 col 0 eval n 3”; its local proof does not by itself complete the broader paper route. The four-gate prefix row '96', column '0' evaluates to the slot-'0' boundary cosine half-angle entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The four-gate prefix row '96', column '0' evaluates to the slot-'0' boundary cosine half-angle entry. This is one of the two prefix factors required by 'oneTermRobinBlockEncodingProofRoute\_gamma3BoundarySevenGateTwoPath\_n3'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7604](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixrow96col0-eval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixRow97Col0_eval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPrefixRow97Col0_eval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary prefix row 97 col 0 eval n 3”; its local proof does not by itself complete the broader paper route. The four-gate prefix row '97', column '0' evaluates to the slot-'0' boundary sine half-angle entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The four-gate prefix row '97', column '0' evaluates to the slot-'0' boundary sine half-angle entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7661](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprefixrow97col0-eval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryCol0SupportAnalysis" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryCol0SupportAnalysis")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary col 0 support analysis”. A proposition-valued field is a requirement until a constructor supplies it. QBE-AUTO-002 column-'0' support analysis record for the '\[0,0\]' entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* QBE-AUTO-002 column-'0' support analysis record for the '\[0,0\]' entry. The '\[0,0\]' entry of the seven-gate product 'suffix \* prefix' at column '0' requires a different support analysis from the '\[32,32\]' entry: 1. 'U\_indic' at column '0': identity (indicator condition not triggered for state '0'). Support only at row '0'. Compiled. 2. 'O\_DT^S' at column '0': identity (indicator bit '0'). Support only at row '0'. Compiled. 3. 'DU = O\_DT^S \* U\_indic' at column '0': support only at row '0'. Compiled. 4. 'Ry\_boundary' at column '0': acts on the '(0, 1)' rotation pair. 'Ry\[0, 0\] = cosHalf' and 'Ry\[1, 0\] = sinHalf' are both non-zero. Support at rows '\{0, 1\}'. Compiled. 5. 'RDU = Ry \* DU' at column '0': since 'DU' feeds only row '0' into 'Ry', the RDU prefix has support at rows '\{0, 1\}' (both Ry targets of row '0'). Compiled. 6. 'prefix = O\_D^BS \* RDU' at column '0': maps rows '\{0, 1\}' through 'O\_D^BS'. The prefix has support at '\{image(0), image(1)\} = \{96, 97\}'. Both images compiled. Prefix support compiled. The next proof obligation is: - Add the suffix-side support for row '0' (dagger concentrates at column '96', SWAP maps to row '12', 'O\_f' spreads from there) - Build the two-path reduction for '\[0,0\]' through intermediate rows '\{96, 97\}' - Compare the resulting entry with the backend fold under HWKappa This record does not promote any 'proved' flag.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7743](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycol0supportanalysis). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCol0SupportAnalysis_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCol0SupportAnalysis_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary col 0 support analysis n 3”. Compiled column-'0' support analysis for the '\[0,0\]' seven-gate entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled column-'0' support analysis for the '\[0,0\]' seven-gate entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7767](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycol0supportanalysis-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundarySevenGateTwoPath_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundarySevenGateTwoPath_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary seven gate two path n 3”; its local proof does not by itself complete the broader paper route. Two-path reduction for the '\[0,0\]' entry of the seven-gate boundary matrix.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Two-path reduction for the '\[0,0\]' entry of the seven-gate boundary matrix. The prefix at column '0' has support only at intermediate rows '\{96, 97\}' (compiled in 'oneTermRobinGamma3BoundaryPrefixCol0Support\_n3'). All other intermediate rows contribute zero to the matrix product 'suffix \* prefix' at position '\[0, 0\]'. This applies 'Matrix.evalWith\_mul\_two\_path' from CircuitSemantics and does not promote any 'proved' flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:7840](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundarysevengatetwopath-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRyCoefficientBridge" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRyCoefficientBridge")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary ry coefficient bridge”. A proposition-valued field is a requirement until a constructor supplies it. Focused false bridge for the displayed boundary 'gamma3' branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused false bridge for the displayed boundary 'gamma3' branch. The compiled seven-gate product contributes the 'Ry\_boundary' half-angle entry 'boundary\_cos\_half\_0\_2'. Eq. 'ROBIN clarified' needs the normalized derivative coefficient 'D\_0^(2) / N\_D'. The paper angle line states 'theta\_0^2 = arccos(D\_0^(2) / N\_D)', so identifying the half-angle matrix entry itself with the normalized coefficient is a separate source-contract gap. This record names that gap without changing any matrix convention or promoting the product-to-coefficient theorem.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8567](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrycoefficientbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyCoefficientBridge_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyCoefficientBridge_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary ry coefficient bridge n 3”. Compiled focused bridge for the 'n = 3', row-'0', column-'0', global-slot-'2' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled focused bridge for the 'n = 3', row-'0', column-'0', global-slot-'2' boundary branch. The bridge records exactly the factor mismatch left after 'oneTermRobinBlockEncodingProofRoute\_gamma3BoundaryProductEntryEval\_n3'. It keeps the 'R\_y' angle convention, product-to-coefficient equality, LCU, projection, block correctness, and final extraction as false obligations.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8600](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrycoefficientbridge-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyCoefficientBridge_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyCoefficientBridge_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary ry coefficient bridge n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the focused boundary 'R\_y' coefficient bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the focused boundary 'R\_y' coefficient bridge. This theorem proves only the typed wiring of the source-contract gap. The bridge obligation and every theorem-level semantic flag remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8654](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrycoefficientbridge-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRyAngleConventionDecision" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRyAngleConventionDecision")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary ry angle convention decision”. A proposition-valued field is a requirement until a constructor supplies it. Human/source decision packet for the boundary 'R\_y' angle convention.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Human/source decision packet for the boundary 'R\_y' angle convention. The focused bridge proves that the compiled seven-gate product uses the standard 'R\_y' half-angle entry 'boundary\_cos\_half\_0\_2', while Eq. 'ROBIN clarified' needs the normalized coefficient 'D\_0^(2) / N\_D'. This packet is the theorem-facing freeze requested by the source audit: product-to-coefficient search stays blocked until a paper-backed convention or human decision supplies the missing rule.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8720](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryryangleconventiondecision). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyAngleConventionDecision_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyAngleConventionDecision_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary ry angle convention decision n 3”. Compiled decision packet for the focused boundary branch at 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled decision packet for the focused boundary branch at 'n = 3'. This declaration does not choose a new matrix convention. It records that the source currently supports only the bridge obligation, and that lower product proof search must wait for either a source-backed half-angle convention or an accepted decision to keep the standard 'R\_y' entry as an explicit theorem gap.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8747](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryryangleconventiondecision-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyAngleConventionDecision_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyAngleConventionDecision_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary ry angle convention decision n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the boundary 'R\_y' angle-convention decision packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the boundary 'R\_y' angle-convention decision packet. Only the source-backed decision boundary is checked here. The bridge obligation, product-to-coefficient theorem, LCU composition, block projection, block correctness, and final extraction remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8793](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryryangleconventiondecision-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRyLowerPacketGuard" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRyLowerPacketGuard")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary ry lower packet guard”. A proposition-valued field is a requirement until a constructor supplies it. Lower-packet guard for the boundary 'R\_y' decision freeze.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Lower-packet guard for the boundary 'R\_y' decision freeze. This record is deliberately non-semantic. It packages the current source decision state so future lower packets can test that product-to-coefficient proof search is disabled until a source-backed convention or human decision is recorded. Source-backed convention work and reviewer audit remain allowed.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8846](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrylowerpacketguard). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyLowerPacketGuard_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyLowerPacketGuard_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary ry lower packet guard n 3”. Compiled lower-packet guard for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled lower-packet guard for the focused 'n = 3' boundary branch. The guard does not choose an angle convention. It only freezes lower product-to-coefficient proof search around the existing decision packet while preserving the option to add a source-backed convention packet.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8870](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrylowerpacketguard-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyLowerPacketGuard_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyLowerPacketGuard_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary ry lower packet guard n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the lower-packet guard.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the lower-packet guard. The theorem checks only the freeze state and false semantic flags. It is a guard against accidentally resuming the focused product proof before the boundary 'R\_y' convention gap is resolved.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8906](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrylowerpacketguard-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRyCorrectedAngleSourceDecision" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRyCorrectedAngleSourceDecision")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary ry corrected angle source decision”. A proposition-valued field is a requirement until a constructor supplies it. Source-backed correction decision for the focused boundary 'R\_y' route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Source-backed correction decision for the focused boundary 'R\_y' route. The local GHL2025 text states 'theta\_j^s = arccos(D\_j^(s) / N\_D)', but the paper uses the standard one-qubit 'R\_y' convention elsewhere and the companion implementation computes boundary correction angles as '2 \* arccos(...)'. Therefore the next faithful lower packet should use the corrected input angle '2 \* arccos(D\_j^(s) / N\_D)' with the standard 'R\_y' matrix. This decision only unblocks product-to-coefficient work; it does not promote the product, LCU, projection, block-correctness, unitarity, or final-extraction flags.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8954](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrycorrectedanglesourcedecision). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyCorrectedAngleSourceDecision_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyCorrectedAngleSourceDecision_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary ry corrected angle source decision n 3”. Compiled corrected-angle decision for the 'n = 3', row-'0', slot-'2' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled corrected-angle decision for the 'n = 3', row-'0', slot-'2' boundary branch. This records the source audit result needed before the next lower packet: the boundary rotation should be represented as the standard 'R\_y' gate with input angle '2 \* arccos(D\_0^(2) / N\_D)', so its clean ket-zero entry is the normalized coefficient. All theorem-facing semantic claims remain unproved.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:8986](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrycorrectedanglesourcedecision-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyCorrectedAngleSourceDecision_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRyCorrectedAngleSourceDecision_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary ry corrected angle source decision n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the corrected-angle source decision.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the corrected-angle source decision. The theorem checks only the decision state. It explicitly leaves the product-to-coefficient theorem and all downstream semantic flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9032](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrycorrectedanglesourcedecision-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryCorrectedCoefficientInterface" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryCorrectedCoefficientInterface")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary corrected coefficient interface”. A proposition-valued field is a requirement until a constructor supplies it. Corrected-angle coefficient interface for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Corrected-angle coefficient interface for the focused boundary branch. The record is deliberately conditional: the source-backed angle correction allows the 'Ry\_boundary' clean entry to be treated as the normalized boundary coefficient, but the product-to-coefficient theorem and all block-encoding semantics remain false until separate Lean theorems prove them.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9073](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycorrectedcoefficientinterface). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCorrectedCoefficientInterface_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCorrectedCoefficientInterface_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary corrected coefficient interface n 3”. Compiled interface for replacing the boundary free factor by the corrected normalized coefficient in the 'n = 3', row-'0', column-'0', slot-'2' branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled interface for replacing the boundary free factor by the corrected normalized coefficient in the 'n = 3', row-'0', column-'0', slot-'2' branch.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9093](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycorrectedcoefficientinterface-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCorrectedCoefficientInterface_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCorrectedCoefficientInterface_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary corrected coefficient interface n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the corrected-angle coefficient interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the corrected-angle coefficient interface. This checks that the interface uses the global sparse-slot normalized coefficient and that every theorem-facing semantic claim remains unproved.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9133](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycorrectedcoefficientinterface-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductEntryEval_correctedAngle_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductEntryEval_correctedAngle_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary product entry eval corrected angle n 3”; its local proof does not by itself complete the broader paper route. Conditional evaluated-product interface for the corrected boundary angle.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional evaluated-product interface for the corrected boundary angle. Once the corrected-angle entry hypothesis is supplied for the environment, the compiled seven-gate boundary product is expressed using 'boundaryRotationNormalizedCoefficient' rather than the unresolved free symbol. This is not the final product-to-coefficient theorem.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9167](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundaryproductentryeval-correctedangle-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductEntryEval_correctedCoefficientExpanded_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute_gamma3BoundaryProductEntryEval_correctedCoefficientExpanded_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin block encoding proof route gamma 3 boundary product entry eval corrected coefficient expanded n 3”; its local proof does not by itself complete the broader paper route. Expanded corrected-angle product entry for the displayed boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Expanded corrected-angle product entry for the displayed boundary branch. This is the strongest local coefficient statement currently available for the focused 'n = 3', '(0,0)', slot-'2' packet. Under the corrected-entry hypothesis, the seven-gate product is the clean 'O\_f' amplitude times the global-slot boundary coefficient normalized by 'N\_D'. The theorem deliberately does not insert the theorem-level sparse-summation/'kappa' factor or promote the product-to-coefficient obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9195](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobinblockencodingproofroute-gamma3boundaryproductentryeval-correctedcoefficientexpanded-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryAkEntry_matches_globalSlot2_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryAkEntry_matches_globalSlot2_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary ak entry matches global slot 2 n 3”; its local proof does not by itself complete the broader paper route. The focused boundary target entry uses the same global slot-'2' coefficient.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The focused boundary target entry uses the same global slot-'2' coefficient. This closes the local stencil-side comparison for '(A\_k)\_\{0,0\}'. The remaining gap is not the Robin matrix entry; it is the theorem-level quotient/projection convention that must turn the branch-local product into '(A\_k)\_\{0,0\}/(N\_D N\_f kappa)'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9228](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryakentry-matches-globalslot2-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProductToCoefficientObstruction" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProductToCoefficientObstruction")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary product to coefficient obstruction”. A proposition-valued field is a requirement until a constructor supplies it. Precise remaining obstruction for the focused boundary product-to-coefficient route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Precise remaining obstruction for the focused boundary product-to-coefficient route. The corrected-angle product has been reduced to '(f\_3\_0 \* N\_f\_inv) \* (D\_0^(2) \* N\_D\_inv)', and the target entry has been identified as 'f\_3\_0 \* D\_0^(2)'. What is still missing is an exact Lean convention relating this branch-local product to the theorem's normalized block entry with normalizer 'N\_D \* N\_f \* kappa', including the sparse-register summation/projection factor. This record keeps the theorem-facing obligation false instead of changing the scientific contract.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9248](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryproducttocoefficientobstruction). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductToCoefficientObstruction_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductToCoefficientObstruction_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary product to coefficient obstruction n 3”. Compiled obstruction packet for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled obstruction packet for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9269](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryproducttocoefficientobstruction-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductToCoefficientObstruction_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductToCoefficientObstruction_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary product to coefficient obstruction n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the focused boundary product-to-coefficient obstruction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the focused boundary product-to-coefficient obstruction. This theorem records the smallest remaining Lean-local obstruction after the corrected-angle expansion and target-entry comparison. It keeps all semantic flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9319](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryproducttocoefficientobstruction-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryNormalizerProjectionConvention" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryNormalizerProjectionConvention")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary normalizer projection convention”. A proposition-valued field is a requirement until a constructor supplies it. Theorem-level normalizer/projection convention packet for the focused boundary 'gamma3' product route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Theorem-level normalizer/projection convention packet for the focused boundary 'gamma3' product route. The preceding local theorems have reduced the branch product to '(f\_3\_0 \* N\_f\_inv) \* (D\_0^(2) \* N\_D\_inv)' and the target entry to 'f\_3\_0 \* D\_0^(2)'. This packet ties those facts to the theorem normalizer 'N\_D\*N\_f\*kappa', while keeping the quotient interpretation of 'N\_D\_inv', 'N\_f\_inv', and the sparse-register 'kappa' projection as explicit false obligations.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9363](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarynormalizerprojectionconvention). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryNormalizerProjectionConvention_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryNormalizerProjectionConvention_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary normalizer projection convention n 3”. Compiled normalizer/projection convention interface for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled normalizer/projection convention interface for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0'. This is a typed convention packet, not the final product-to-coefficient proof. It records that the finite-composition contract uses the same normalizer 'GHL2025.oneTermRobinNormalizer', and that the remaining work is the symbolic inverse convention plus the sparse-register projection factor contributing the 'kappa' denominator.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9398](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarynormalizerprojectionconvention-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryNormalizerProjectionConvention_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryNormalizerProjectionConvention_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary normalizer projection convention n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the focused normalizer/projection convention packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the focused normalizer/projection convention packet. The theorem checks the wiring to the compiled obstruction, the target-entry comparison, and the finite-composition normalizer. All theorem-facing semantic claims remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9449](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarynormalizerprojectionconvention-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryNormalizerSplitTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryNormalizerSplitTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary normalizer split target”. A proposition-valued field is a requirement until a constructor supplies it. Middle-agent split target for the next focused boundary 'gamma3' packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Middle-agent split target for the next focused boundary 'gamma3' packet. The existing normalizer/projection convention already identifies the two remaining blockers. This record makes them explicit as separate lower-agent targets while reusing the same theorem route: \* symbolic inverse semantics for 'N\_D\_inv' and 'N\_f\_inv'; \* the sparse-register projection factor that contributes '1/kappa'. It is still a convention packet, not a proof of the product-to-coefficient obligation.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9533](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarynormalizersplittarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryNormalizerSplitTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryNormalizerSplitTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary normalizer split target n 3”. Lean-facing lower packet target after the boundary normalizer/projection convention compiled.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Lean-facing lower packet target after the boundary normalizer/projection convention compiled. The target keeps the fixed theorem-facing obligation 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0', but it splits the next proof work into two non-overlapping subgoals: the symbolic inverse interpretation of 'N\_D\_inv'/'N\_f\_inv', and the sparse-register 'kappa' projection factor. All semantic flags remain false.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9565](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarynormalizersplittarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryNormalizerSplitTarget_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryNormalizerSplitTarget_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary normalizer split target n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the split target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the split target. It checks that the two named sub-obligations are exactly the fields of the compiled normalizer/projection convention and that no semantic flag has been promoted.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9600](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarynormalizersplittarget-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySymbolicInverseEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySymbolicInverseEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary symbolic inverse eval n 3”; its local proof does not by itself complete the broader paper route. Conditional symbolic-inverse evaluation for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional symbolic-inverse evaluation for the focused boundary branch. This proves the local algebraic part of the split target: if the coefficient environment interprets 'N\_D\_inv' and 'N\_f\_inv' as right inverses of 'N\_D' and 'N\_f', then the corrected branch-local product recovers the target entry after multiplication by the 'N\_D\*N\_f' part of the theorem normalizer. The lemma does not supply those inverse hypotheses and does not account for the separate '1/kappa' sparse-register projection factor.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9650](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysymbolicinverseeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundarySymbolicInverseSemantics" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundarySymbolicInverseSemantics")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary symbolic inverse semantics”. A proposition-valued field is a requirement until a constructor supplies it. Transcript packet for the symbolic-inverse half of the boundary split target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript packet for the symbolic-inverse half of the boundary split target. The conditional evaluation lemma above is compiled, but the theorem route still needs actual inverse semantics for the environment and still needs the separate 'kappa' projection factor. The product-to-coefficient and block-composition flags therefore remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9714](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysymbolicinversesemantics). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySymbolicInverseSemantics_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySymbolicInverseSemantics_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary symbolic inverse semantics n 3”. Compiled symbolic-inverse packet for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled symbolic-inverse packet for the focused boundary branch. This reuses 'oneTermRobinGamma3BoundaryNormalizerSplitTarget\_n3' and reduces only the 'N\_D\_inv'/'N\_f\_inv' algebra under explicit environment hypotheses. It does not prove the sparse-register '1/kappa' projection or the final product-to-coefficient obligation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9744](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysymbolicinversesemantics-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySymbolicInverseSemantics_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySymbolicInverseSemantics_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary symbolic inverse semantics n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the symbolic-inverse packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the symbolic-inverse packet. It confirms that the new packet consumes exactly the split target's symbolic inverse obligation and leaves the 'kappa' projection and theorem-level composition obligations unproved.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9780](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysymbolicinversesemantics-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryUniformSparseRegisterPreparationObligation_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryUniformSparseRegisterPreparationObligation_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary uniform sparse register preparation obligation n 3”. Uniform sparse-register preparation obligation for the focused boundary 'gamma3' route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Uniform sparse-register preparation obligation for the focused boundary 'gamma3' route. GHL2025 Eq. 'arbitrary sparcity' defines 'H\_W^(kappa)' as the state preparation that gives each sparse slot amplitude '1/sqrt(kappa)'. For the boundary product-to-coefficient route, the missing projection convention is that the preparation amplitude and the matching sparse-register projection contribute the remaining '1/kappa' factor. This obligation records that source dependency without treating the cited implementation as formalized.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9828](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryuniformsparseregisterpreparationobligation-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryKappaProjectionTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryKappaProjectionTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary kappa projection target”. A proposition-valued field is a requirement until a constructor supplies it. Middle-agent packet target for the sparse-register 'kappa' projection factor.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Middle-agent packet target for the sparse-register 'kappa' projection factor. The symbolic 'N\_D\_inv'/'N\_f\_inv' algebra now has a compiled conditional lemma. This target isolates the remaining source/projection convention: the sparse register is prepared by 'H\_W^(kappa)' with amplitude '1/sqrt(kappa)', and the matching projection onto the focused slot contributes another '1/sqrt(kappa)'. The packet is intentionally contract-only; it does not prove the projection factor or the product-to-coefficient theorem.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9846](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarykappaprojectiontarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary kappa projection target n 3”. Compiled sparse-register 'kappa' projection target for the focused boundary entry '(0,0)' and global sparse slot '2'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled sparse-register 'kappa' projection target for the focused boundary entry '(0,0)' and global sparse slot '2'. This is the next lower-agent packet target after 'oneTermRobinGamma3BoundarySymbolicInverseSemantics\_n3'. It keeps all theorem-facing obligations false and records that the sparse-register factor depends on the 'H\_W^(kappa)' uniform-preparation contract rather than on a new gate-level proof in this batch.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9889](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarykappaprojectiontarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionTarget_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionTarget_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary kappa projection target n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the sparse-register 'kappa' projection target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the sparse-register 'kappa' projection target. The theorem only checks packet wiring: the focused sparse slot is '2', the source and target clean basis index is '32', the cited uniform-preparation dependency is named, and all product/composition/projection flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:9941](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarykappaprojectiontarget-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary kappa projection eval n 3”; its local proof does not by itself complete the broader paper route. Conditional sparse-register 'kappa' projection evaluation for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional sparse-register 'kappa' projection evaluation for the focused boundary branch. This combines the already compiled 'N\_D\_inv'/'N\_f\_inv' cancellation lemma with a separate symbolic 'kappa\_inv' projection factor. Under explicit environment hypotheses, the projected branch-local product multiplied by the theorem normalizer evaluates to the target entry. The theorem does not prove that the circuit actually prepares or projects the sparse register with amplitude '1/sqrt(kappa)'; that source/projection convention remains an obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10003](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarykappaprojectioneval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryKappaProjectionSemantics" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryKappaProjectionSemantics")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary kappa projection semantics”. A proposition-valued field is a requirement until a constructor supplies it. Compiled packet for the conditional 'kappa\_inv' projection evaluation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled packet for the conditional 'kappa\_inv' projection evaluation. The packet records the Lean algebra that would finish the normalizer part once the sparse-register preparation/projection convention is available. It keeps the uniform-preparation, projection, finite-composition, and theorem-facing product obligations false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10082](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarykappaprojectionsemantics). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionSemantics_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionSemantics_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary kappa projection semantics n 3”. Boundary 'gamma3' sparse-register projection packet for 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Boundary 'gamma3' sparse-register projection packet for 'n = 3'. The field 'projectedBranchProduct' is the corrected branch-local product multiplied by a symbolic 'kappa\_inv' factor. The compiled evaluation lemma checks only rational cancellation under explicit environment hypotheses; it is not a gate-level proof of 'H\_W^(kappa)' or block projection.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10113](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarykappaprojectionsemantics-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionSemantics_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryKappaProjectionSemantics_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary kappa projection semantics n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the conditional sparse-register projection packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the conditional sparse-register projection packet. It checks that the packet reuses the middle-agent target, names 'oneTermRobinGamma3BoundaryKappaProjectionEval\_n3' as the compiled algebra lemma, and preserves all semantic proof flags as false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10151](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarykappaprojectionsemantics-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionSourceContract" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionSourceContract")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary projection source contract”. A proposition-valued field is a requirement until a constructor supplies it. Source-backed projection contract for the inserted 'kappa\_inv' factor.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Source-backed projection contract for the inserted 'kappa\_inv' factor. The compiled cancellation lemma treats 'Coeff.symbol "kappa\_inv"' as an explicit factor in the projected branch product. This contract records the paper-facing source of that factor: 'H\_W^(kappa)' prepares the sparse register with amplitude '1/sqrt(kappa)' on the focused slot, and the matching block-projection bra contributes the second '1/sqrt(kappa)'. The actual state-preparation circuit, projection convention, normalized block equality, and focused product-to-coefficient equality remain obligations.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10201](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsourcecontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSourceContract_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSourceContract_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary projection source contract n 3”. Compiled source/projection contract for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled source/projection contract for the focused boundary branch. This packet connects the existing conditional 'kappa\_inv' algebra to the paper source and the cited uniform-state-preparation result. It deliberately does not prove that the circuit supplies the factor; the relevant fields remain false obligations for a later block-projection packet.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10241](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsourcecontract-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSourceContract_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSourceContract_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection source contract n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the boundary projection source contract.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the boundary projection source contract. It checks that the contract reuses the compiled 'kappa\_inv' packet, points to the cited uniform-preparation row, fixes the focused slot data, and leaves all semantic obligations false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10292](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsourcecontract-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorIndex_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorIndex_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection factor index n 3”; its local proof does not by itself complete the broader paper route. Finite index check for the boundary projection-factor packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Finite index check for the boundary projection-factor packet. This theorem proves only the local bookkeeping part of the sparse-register projection factor: the prepared sparse slot and the projected sparse slot are the same focused slot '2', and both use the clean basis index generated by 'oneTermRobinGamma3PaperBasisIndex'. It does not prove the amplitude of 'H\_W^(kappa)', the matching projection amplitude, or the block-composition equality.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10350](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionfactorindex-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionFactorSemantics" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionFactorSemantics")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary projection factor semantics”. A proposition-valued field is a requirement until a constructor supplies it. Finite projection-factor interface for the inserted 'kappa\_inv' factor.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Finite projection-factor interface for the inserted 'kappa\_inv' factor. The source contract says where the factor must come from. This packet adds the finite Lean-side index interface: the preparation and projection are both focused on sparse slot '2' and clean basis index '32', so the only remaining meaning of 'Coeff.symbol "kappa\_inv"' is the amplitude theorem for the uniform sparse-register preparation and its matching block projection.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10382](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionfactorsemantics). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorSemantics_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorSemantics_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary projection factor semantics n 3”. Compiled finite projection-factor interface for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled finite projection-factor interface for the focused boundary branch. This declaration reduces the projection-source gap to the exact missing semantic theorem: QBE still has to prove that the cited 'H\_W^(kappa)' preparation and the matching block projection contribute the symbolic factor 'kappa\_inv'. The finite slot and basis-index alignment is build-tested here.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10425](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionfactorsemantics-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorSemantics_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorSemantics_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection factor semantics n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the finite projection-factor interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the finite projection-factor interface. The theorem checks the compiled index lemma, the focused sparse slot, the clean basis index, the projected branch product, and every false semantic flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10475](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionfactorsemantics-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionFactorObstruction" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionFactorObstruction")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary projection factor obstruction”. A proposition-valued field is a requirement until a constructor supplies it. Smallest current obstruction for proving the focused projection factor.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest current obstruction for proving the focused projection factor. The finite slot and basis-index interface is compiled, and the conditional 'kappa\_inv' cancellation lemma is compiled. What remains is not another finite-index calculation: QBE still needs a formal source for the 'H\_W^(kappa)' per-slot amplitude and a matching block-projection convention for the same sparse slot. This packet separates those two obligations while keeping the product-to-coefficient route false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10539](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionfactorobstruction). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorObstruction_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorObstruction_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary projection factor obstruction n 3”. Compiled obstruction packet for the projection-factor semantics of the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled obstruction packet for the projection-factor semantics of the focused boundary branch. This is deliberately not a proof of 'kappa\_inv'. It records that the cited uniform-preparation amplitude and the QBE matching projection convention are the two separate missing ingredients before the existing conditional algebra can feed the product-to-coefficient route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10576](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionfactorobstruction-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorObstruction_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorObstruction_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection factor obstruction n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the projection-factor obstruction packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the projection-factor obstruction packet. The theorem confirms that the obstruction reuses the compiled finite projection-factor interface and does not promote product equality, LCU, projection, block correctness, normalized equality, or final extraction.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10621](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionfactorobstruction-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryMatchingProjectionConvention" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryMatchingProjectionConvention")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary matching projection convention”. A proposition-valued field is a requirement until a constructor supplies it. Local matching-projection convention for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Local matching-projection convention for the focused boundary branch. The projection-factor obstruction has already separated the cited 'H\_W^(kappa)' preparation amplitude from QBE's matching block-projection convention. This packet records only the local convention side: the projected bra is the same sparse slot '2' and the same clean basis index '32' used by the prepared branch. It does not prove that the bra contributes amplitude '1/sqrt(kappa)' and does not identify the two amplitude factors with 'Coeff.symbol "kappa\_inv"'.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10680](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionconvention). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionConvention_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionConvention_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary matching projection convention n 3”. Compiled local matching-projection convention for sparse slot '2'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled local matching-projection convention for sparse slot '2'. The convention reuses the compiled projection-factor obstruction and finite index lemma. It narrows the local missing ingredient to the semantic theorem that the block projection onto the matching sparse slot contributes the second '1/sqrt(kappa)' amplitude.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10720](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionconvention-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionConvention_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionConvention_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary matching projection convention n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the matching-projection convention packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the matching-projection convention packet. The theorem checks the local slot and basis-index wiring and confirms that the matching projection, projection-factor semantics, finite normalized equality, product-to-coefficient equality, and downstream block-encoding claims remain unproved.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10768](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionconvention-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorProductEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionFactorProductEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection factor product eval n 3”; its local proof does not by itself complete the broader paper route. Symbolic product check for the two sparse-register amplitude factors.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Symbolic product check for the two sparse-register amplitude factors. This is only coefficient algebra: if an environment interprets the two '1/sqrt(kappa)' factors as 'sqrt\_kappa\_inv' and their product as 'kappa\_inv', then the symbolic product evaluates to 'kappa\_inv'. It does not prove the cited uniform-preparation amplitude or the matching projection amplitude.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10835](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionfactorproducteval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryMatchingProjectionAmplitudeObstruction" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryMatchingProjectionAmplitudeObstruction")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary matching projection amplitude obstruction”. A proposition-valued field is a requirement until a constructor supplies it. Smallest current obstruction for the matching-projection amplitude packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest current obstruction for the matching-projection amplitude packet. The local convention already fixes the projected bra to sparse slot '2' and clean basis index '32'. This packet separates the remaining amplitude work: the ket-side '1/sqrt(kappa)' factor is an external contract through 'H\_W^(kappa)', the bra-side '1/sqrt(kappa)' factor is a local QBE block-projection obligation, and the product must be identified with the symbolic factor 'kappa\_inv' before the conditional normalizer lemma can close the focused product route.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10857](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionamplitudeobstruction). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionAmplitudeObstruction_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionAmplitudeObstruction_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary matching projection amplitude obstruction n 3”. Compiled obstruction packet for the focused matching-projection amplitude.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled obstruction packet for the focused matching-projection amplitude. This reuses the matching-projection convention and adds the smallest symbolic factor interface needed by the next proof block. It does not prove either '1/sqrt(kappa)' amplitude and keeps product equality, finite normalized equality, LCU, block projection, block correctness, and final extraction false.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10901](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionamplitudeobstruction-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionAmplitudeObstruction_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionAmplitudeObstruction_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary matching projection amplitude obstruction n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the matching-projection amplitude obstruction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the matching-projection amplitude obstruction. The theorem checks that the obstruction is downstream of the compiled matching-projection convention and that it introduces no semantic promotion.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:10959](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionamplitudeobstruction-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryMatchingProjectionAmplitudeContract" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryMatchingProjectionAmplitudeContract")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary matching projection amplitude contract”. A proposition-valued field is a requirement until a constructor supplies it. Focused contract for the bra-side matching projection amplitude.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused contract for the bra-side matching projection amplitude. The preceding obstruction already separates the cited ket amplitude from the local projection side. This packet gives the local side a precise interface: the block-projection bra is the clean branch for sparse slot '2', basis index '32', and its expected amplitude factor is the symbol 'sqrt\_kappa\_inv'. It is still a contract, not a projection theorem, so all semantic flags remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11031](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionamplitudecontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionAmplitudeContract_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionAmplitudeContract_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary matching projection amplitude contract n 3”. Compiled bra-side projection-amplitude contract for the focused boundary route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled bra-side projection-amplitude contract for the focused boundary route. This is the QBE-local complement to the cited 'H\_W^(kappa)' preparation-amplitude contract. It narrows the remaining block-projection obligation to one finite branch and one expected symbolic amplitude factor.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11072](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionamplitudecontract-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionAmplitudeContract_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryMatchingProjectionAmplitudeContract_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary matching projection amplitude contract n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the focused bra-side projection-amplitude contract.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the focused bra-side projection-amplitude contract. It checks that the new contract is downstream of the existing obstruction, uses the same slot and basis index, exposes the expected 'sqrt\_kappa\_inv' factor, and preserves all false theorem-facing obligations.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11128](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarymatchingprojectionamplitudecontract-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionAmplitudeSemantics" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionAmplitudeSemantics")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary projection amplitude semantics”. A proposition-valued field is a requirement until a constructor supplies it. Phase-1 projection-amplitude semantics for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Phase-1 projection-amplitude semantics for the focused boundary branch. The bra-side matching projection amplitude has now been narrowed to the symbol 'sqrt\_kappa\_inv', and the ket-side amplitude remains the cited 'H\_W^(kappa)' contract. This packet accepts both as explicit contracts for the current GHL theorem transcript, while keeping the actual amplitude, factor-semantics, finite-composition, and product-to-coefficient obligations false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11193](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionamplitudesemantics). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeSemantics_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeSemantics_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary projection amplitude semantics n 3”. Compiled projection-amplitude semantics packet for the focused 'gamma3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled projection-amplitude semantics packet for the focused 'gamma3' boundary branch. This is not a proof of the sparse-register amplitude. It is the precise Phase-1 contract interface needed before the route can use the symbolic product lemma and later discharge 'factorSemanticsObligation'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11240](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionamplitudesemantics-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeContractProductEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeContractProductEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection amplitude contract product eval n 3”; its local proof does not by itself complete the broader paper route. Conditional product evaluation for the accepted sparse-register amplitude contracts.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional product evaluation for the accepted sparse-register amplitude contracts. The theorem only performs symbolic coefficient algebra. It does not prove the cited 'H\_W^(kappa)' ket amplitude, the QBE matching bra amplitude, or the factor-semantics obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11301](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionamplitudecontractproducteval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeSemantics_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeSemantics_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection amplitude semantics n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the projection-amplitude semantics packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the projection-amplitude semantics packet. It verifies that the packet consumes the existing bra-side amplitude contract, accepts the ket and bra amplitudes only as Phase-1 contracts, and keeps all semantic proof flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11321](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionamplitudesemantics-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeFactorEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeFactorEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection amplitude factor eval n 3”; its local proof does not by itself complete the broader paper route. Conditional factor-semantics evaluation for the accepted sparse-register amplitude contracts.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional factor-semantics evaluation for the accepted sparse-register amplitude contracts. This combines the local symbolic product lemma for the two 'sqrt\_kappa\_inv' factors with the existing conditional 'kappa\_inv' normalizer lemma. The hypotheses are explicit coefficient-environment semantics; the theorem does not prove the cited 'H\_W^(kappa)' amplitude, the matching projection amplitude, or the theorem-facing product obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11397](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionamplitudefactoreval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionAmplitudeFactorSemantics" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionAmplitudeFactorSemantics")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary projection amplitude factor semantics”. A proposition-valued field is a requirement until a constructor supplies it. Compiled packet for the conditional factor-semantics bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled packet for the conditional factor-semantics bridge. The packet records that the accepted ket and bra amplitude contracts can feed the existing 'kappa\_inv' normalizer lemma only under the explicit product hypothesis. It keeps all amplitude, factor-semantics, finite-composition, and product-to-coefficient proof flags false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11460](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionamplitudefactorsemantics). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeFactorSemantics_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeFactorSemantics_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary projection amplitude factor semantics n 3”. Factor-semantics bridge for the focused boundary 'gamma3' packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Factor-semantics bridge for the focused boundary 'gamma3' packet. The projected branch product uses the two accepted 'sqrt\_kappa\_inv' amplitude contracts directly. The conditional lemma shows that this product has the same normalizer behavior as the earlier inserted 'kappa\_inv' factor when the environment supplies the product identity.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11501](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionamplitudefactorsemantics-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeFactorSemantics_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionAmplitudeFactorSemantics_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection amplitude factor semantics n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the conditional factor-semantics bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the conditional factor-semantics bridge. It checks the bridge wiring and confirms that no amplitude, projection, finite-composition, product-to-coefficient, LCU, block-correctness, or final extraction flag has been promoted.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11557](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionamplitudefactorsemantics-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryFactorSemanticsContractMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryFactorSemanticsContractMap")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary factor semantics contract map”. A proposition-valued field is a requirement until a constructor supplies it. Source-backed contract map for the factor-semantics obligation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Source-backed contract map for the factor-semantics obligation. The conditional factor bridge is already compiled. This packet records the four remaining sources that must be supplied before the bridge can discharge the actual factor-semantics obligation: the cited ket amplitude, the local bra projection amplitude, the symbolic square-root product hypothesis, and the finite normalized block-composition equality. It keeps the theorem-facing obligation false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11626](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryfactorsemanticscontractmap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFactorSemanticsContractMap_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFactorSemanticsContractMap_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary factor semantics contract map n 3”. Compiled contract map for the focused boundary factor-semantics obligation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled contract map for the focused boundary factor-semantics obligation. This is a Phase-1 transcript object. It says precisely what would make 'oneTermRobinGamma3BoundaryProjectionAmplitudeFactorEval\_n3' usable as the factor-semantics step, while preserving the false status of the real semantic obligations.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11667](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryfactorsemanticscontractmap-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFactorSemanticsContractMapEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFactorSemanticsContractMapEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary factor semantics contract map eval n 3”; its local proof does not by itself complete the broader paper route. Conditional evaluation through the contract-map fields.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional evaluation through the contract-map fields. The theorem does not prove the source obligations. It only shows that if the environment supplies the four stated coefficient hypotheses, then the contract map's projected branch product normalizes to the expected target entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11722](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryfactorsemanticscontractmapeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFactorSemanticsContractMap_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFactorSemanticsContractMap_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary factor semantics contract map n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the focused factor-semantics contract map.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the focused factor-semantics contract map. It checks that the map is downstream of the compiled factor bridge, separates the ket, bra, product-hypothesis, and finite-composition blockers, and keeps all semantic proof flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11747](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryfactorsemanticscontractmap-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBraProjectionAmplitudeSourceMap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBraProjectionAmplitudeSourceMap")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary bra projection amplitude source map”. A proposition-valued field is a requirement until a constructor supplies it. Source map for the remaining bra-side projection-amplitude obstruction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Source map for the remaining bra-side projection-amplitude obstruction. The focused projection-amplitude contract already fixes sparse slot '2', clean basis index '32', and the expected factor 'sqrt\_kappa\_inv'. What is still missing is not another finite index lemma: QBE has not yet introduced the concrete sparse-register preparation/projection matrix, or an equivalent adjoint-entry contract, that would make the bra amplitude a Lean theorem.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11819](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybraprojectionamplitudesourcemap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBraProjectionAmplitudeSourceMap_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBraProjectionAmplitudeSourceMap_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary bra projection amplitude source map n 3”. Compiled source map for the focused bra-side amplitude packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled source map for the focused bra-side amplitude packet. This is the smaller obstruction requested by the lower packet. It records the precise semantic object needed to prove the local bra amplitude, instead of pretending that the current block-projection API already supplies it.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11858](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybraprojectionamplitudesourcemap-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBraProjectionAmplitudeSourceMap_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBraProjectionAmplitudeSourceMap_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary bra projection amplitude source map n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the bra-side projection-amplitude source map.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the bra-side projection-amplitude source map. This theorem checks only the source mapping and false-flag discipline. It does not prove the 'H\_W^(kappa)' adjoint entry, the block-projection amplitude, the factor-semantics obligation, finite normalized equality, or the focused product-to-coefficient theorem.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11917](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybraprojectionamplitudesourcemap-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaDaggerProjectionEntryContract" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaDaggerProjectionEntryContract")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary hw kappa dagger projection entry contract”. A proposition-valued field is a requirement until a constructor supplies it. Typed contract for the focused 'H\_W^(kappa)' dagger projection entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed contract for the focused 'H\_W^(kappa)' dagger projection entry. The source map already identified the missing semantic object. This contract turns that object into a Lean-facing interface for the exact entry needed by the boundary gamma3 route: the bra projection from sparse slot '2' to the clean sparse-register branch contributes 'sqrt\_kappa\_inv' at clean basis index '32'. It is accepted only as a Phase-1 contract; the actual matrix entry theorem and all downstream semantic obligations remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:11983](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggerprojectionentrycontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerProjectionEntryContract_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerProjectionEntryContract_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary hw kappa dagger projection entry contract n 3”. Compiled Phase-1 contract for the focused bra projection entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled Phase-1 contract for the focused bra projection entry. The contract is downstream of 'oneTermRobinGamma3BoundaryBraProjectionAmplitudeSourceMap\_n3' and rewires the same bra-amplitude obligation into 'oneTermRobinGamma3BoundaryFactorSemanticsContractMap\_n3'. It does not prove the entry of 'H\_W^(kappa)^dagger'; it records the precise contract that a future semantic matrix theorem must instantiate.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12027](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggerprojectionentrycontract-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerProjectionEntryContract_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerProjectionEntryContract_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa dagger projection entry contract n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the focused 'H\_W^(kappa)' dagger entry contract.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the focused 'H\_W^(kappa)' dagger entry contract. This checks that the new contract is wired to both the bra-source map and the factor-semantics contract map. The entry is still a contract-only interface: the actual dagger entry, bra amplitude, factor semantics, finite normalized equality, product-to-coefficient theorem, and final extraction remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12090](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggerprojectionentrycontract-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaDaggerEmbeddedEntryInterface" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaDaggerEmbeddedEntryInterface")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary hw kappa dagger embedded entry interface”. A proposition-valued field is a requirement until a constructor supplies it. Embedded-entry interface for the focused 'H\_W^(kappa)^dagger' contract.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Embedded-entry interface for the focused 'H\_W^(kappa)^dagger' contract. The preceding contract names the required local sparse-register entry '<0|H\_W^(kappa)^dagger|2>'. This packet refines that contract to the exact finite layout used by the boundary gamma3 route for 'n = 3': the sparse register has width 'ceil(log2 kappa) = 3', local column '2' is in the 'kappa = 7' source domain and the eight-dimensional register, and the ambient clean branch is basis index '32'. It still does not define the 'H\_W^(kappa)' matrix or prove the entry.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12162](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggerembeddedentryinterface). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerEmbeddedEntryInterface_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerEmbeddedEntryInterface_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary hw kappa dagger embedded entry interface n 3”. Compiled embedded-entry interface for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled embedded-entry interface for the focused boundary branch. This is the strict local interface that a future concrete 'H\_W^(kappa)^dagger' matrix theorem should instantiate. It is narrower than the source map because the local sparse-register entry, the 'kappa = 7' domain check, the '2^3 = 8' ambient sparse-register dimension, and the clean gamma3 basis index are all fixed and build-tested.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12211](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggerembeddedentryinterface-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerEmbeddedEntryInterface_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerEmbeddedEntryInterface_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa dagger embedded entry interface n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the embedded-entry interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the embedded-entry interface. This theorem proves only finite layout wiring for the focused interface. It does not prove the 'H\_W^(kappa)^dagger' matrix entry, the bra amplitude, the factor-semantics obligation, finite normalized equality, or the focused product-to-coefficient theorem.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12272](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggerembeddedentryinterface-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerEntryFromUniformColumn_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerEntryFromUniformColumn_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa dagger entry from uniform column n 3”; its local proof does not by itself complete the broader paper route. Conditional adjoint-entry lemma for the focused 'H\_W^(kappa)' slot.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional adjoint-entry lemma for the focused 'H\_W^(kappa)' slot. If a sparse-register preparation matrix has clean-column entry 'H\_W^(kappa)\[2,0\] = sqrt\_kappa\_inv', and the local adjoint-entry convention identifies the dagger entry with that clean-column entry, then the focused row-'0', column-'2' dagger entry has the expected value. This is only the local matrix-entry algebra; it does not provide the cited uniform-column contract or a concrete 'H\_W^(kappa)' matrix.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12348](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggerentryfromuniformcolumn-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaDaggerUniformColumnContract" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaDaggerUniformColumnContract")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary hw kappa dagger uniform column contract”. A proposition-valued field is a requirement until a constructor supplies it. Uniform-column and adjoint-entry contract split for the focused dagger entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Uniform-column and adjoint-entry contract split for the focused dagger entry. The embedded interface fixes the local row and column. This record splits the remaining semantic source into the cited clean-column amplitude 'H\_W^(kappa)\[2,0\] = 1/sqrt(kappa)' and the QBE adjoint-entry convention that turns that column entry into the bra-side dagger entry. Both source inputs remain obligations; the only compiled theorem is the conditional entry lemma above.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12370](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggeruniformcolumncontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerUniformColumnContract_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerUniformColumnContract_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary hw kappa dagger uniform column contract n 3”. Compiled contract split for row '0', column '2' of 'H\_W^(kappa)^dagger'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled contract split for row '0', column '2' of 'H\_W^(kappa)^dagger'. This refines the embedded-entry interface without proving the uniform preparation result or the adjoint-entry convention. The compiled conditional lemma records exactly what a future concrete sparse-register matrix theorem must instantiate.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12424](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggeruniformcolumncontract-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerUniformColumnContract_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerUniformColumnContract_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa dagger uniform column contract n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the uniform-column contract split.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the uniform-column contract split. The theorem checks that the split is tied to the embedded-entry interface, that the compiled conditional entry lemma has the expected shape, and that all semantic proof flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12505](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggeruniformcolumncontract-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerTransposeMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerTransposeMatrix_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary hw kappa dagger transpose matrix n 3”. Local transpose-style dagger for the focused symbolic 'H\_W^(kappa)' matrix.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Local transpose-style dagger for the focused symbolic 'H\_W^(kappa)' matrix. The current 'Coeff' backend is a symbolic real-coefficient matrix layer with no conjugation operation. For this Phase-1 packet the only needed adjoint fact is therefore the focused transpose entry used by the row-'0', column-'2' boundary route.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12592](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggertransposematrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerTransposeEntryConvention_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerTransposeEntryConvention_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa dagger transpose entry convention n 3”; its local proof does not by itself complete the broader paper route. Focused adjoint-entry convention for the boundary 'H\_W^(kappa)' packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused adjoint-entry convention for the boundary 'H\_W^(kappa)' packet. This proves only the matrix-interface convention 'H\_W^(kappa)^dagger\[0,2\] = H\_W^(kappa)\[2,0\]' for the local transpose-style dagger. It does not provide the cited clean-column amplitude.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12603](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggertransposeentryconvention-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerEntryFromTransposeUniformColumn_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerEntryFromTransposeUniformColumn_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa dagger entry from transpose uniform column n 3”; its local proof does not by itself complete the broader paper route. Focused dagger-entry theorem under the external uniform-column contract.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused dagger-entry theorem under the external uniform-column contract. The adjoint-entry convention is now supplied by the local transpose-style matrix interface; the theorem remains conditional on the clean-column amplitude from the cited 'H\_W^(kappa)' state-preparation contract.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12617](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggerentryfromtransposeuniformcolumn-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaDaggerAdjointEntryConvention" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaDaggerAdjointEntryConvention")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary hw kappa dagger adjoint entry convention”. A proposition-valued field is a requirement until a constructor supplies it. Adjoint-entry convention packet for the focused 'H\_W^(kappa)' dagger entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Adjoint-entry convention packet for the focused 'H\_W^(kappa)' dagger entry. This refines 'oneTermRobinGamma3BoundaryHWKappaDaggerUniformColumnContract\_n3' by supplying the QBE local transpose-style adjoint convention for row '0', column '2'. The Shukla--Vedula clean-column amplitude remains contract-only, so the full dagger entry and all downstream product/block obligations remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12639](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggeradjointentryconvention). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerAdjointEntryConvention_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerAdjointEntryConvention_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary hw kappa dagger adjoint entry convention n 3”. Compiled local adjoint-entry convention for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled local adjoint-entry convention for the focused boundary branch. Only the local transpose convention is proved here. The uniform clean-column entry remains an external cited contract, so this packet cannot discharge the bra-amplitude or focused product-to-coefficient obligations by itself.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12691](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggeradjointentryconvention-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerAdjointEntryConvention_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaDaggerAdjointEntryConvention_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa dagger adjoint entry convention n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the local adjoint-entry convention packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the local adjoint-entry convention packet. The QBE transpose-style convention is now compiled and marked proved in this local packet. The external uniform-column source, full dagger entry, bra-amplitude route, factor semantics, finite normalized equality, focused product theorem, and all block-correctness flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12765](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappadaggeradjointentryconvention-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaCleanColumnContract" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryHWKappaCleanColumnContract")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary hw kappa clean column contract”. A proposition-valued field is a requirement until a constructor supplies it. External clean-column contract bridge for the focused 'H\_W^(kappa)' entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* External clean-column contract bridge for the focused 'H\_W^(kappa)' entry. This packet accepts the GHL2025 Eq. 'arbitrary sparcity' clean-column entry only as a typed external contract through the existing Shukla--Vedula cited row. It then records that the accepted entry is the exact hypothesis consumed by the compiled transpose-style dagger bridge. No cited theorem is formalized and no product, projection, LCU, block-correctness, or final-extraction flag is promoted.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12856](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappacleancolumncontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaCleanColumnContract_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaCleanColumnContract_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary hw kappa clean column contract n 3”. Compiled clean-column contract bridge for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled clean-column contract bridge for the focused boundary branch. The bridge records the external contract 'H\_W^(kappa)\[2,0\] = sqrt\_kappa\_inv' and ties it to the already-compiled transpose convention. The clean-column source remains 'contract-only'; the actual dagger entry and downstream bra-amplitude route remain unproved.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12909](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappacleancolumncontract-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaCleanColumnContract_feedsTransposeBridge_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaCleanColumnContract_feedsTransposeBridge_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa clean column contract feeds transpose bridge n 3”; its local proof does not by itself complete the broader paper route. The clean-column contract is exactly the hypothesis consumed by the transpose dagger bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The clean-column contract is exactly the hypothesis consumed by the transpose dagger bridge. This theorem is conditional on a matrix satisfying the external clean-column entry. It does not prove that any concrete 'H\_W^(kappa)' matrix satisfies that entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:12979](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappacleancolumncontract-feedstransposebridge-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaCleanColumnContract_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaCleanColumnContract_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary hw kappa clean column contract n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the clean-column contract bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the clean-column contract bridge. The theorem checks that the bridge uses the Shukla--Vedula cited row as a contract-only source, feeds the accepted entry through the transpose lemma, and keeps the theorem-facing semantic flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13007](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappacleancolumncontract-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryCleanColumnBraRouteContract" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryCleanColumnBraRouteContract")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary clean column bra route contract”. A proposition-valued field is a requirement until a constructor supplies it. Route contract from the accepted clean-column input to the existing bra amplitude and factor-semantics obligations.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Route contract from the accepted clean-column input to the existing bra amplitude and factor-semantics obligations. The clean-column bridge supplies a conditional focused dagger entry under the external Shukla--Vedula uniform-column contract. This packet records that the same entry is exactly the bra-side amplitude source needed by 'oneTermRobinGamma3BoundaryBraProjectionAmplitudeSourceMap\_n3' and the same bra-amplitude obligation consumed by 'oneTermRobinGamma3BoundaryFactorSemanticsContractMap\_n3'. It is still only a route contract: the external clean-column theorem, the actual bra amplitude, factor semantics, finite normalized equality, and product-to-coefficient obligation remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13102](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycleancolumnbraroutecontract). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnBraRouteContract_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnBraRouteContract_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary clean column bra route contract n 3”. Compiled clean-column to bra-route contract for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled clean-column to bra-route contract for the focused boundary branch. This declaration connects the contract-only clean-column bridge to the exact bra-amplitude and factor-semantics fields already present in the route. It does not prove the Shukla--Vedula clean-column input or discharge the internal projection-amplitude obligation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13159](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycleancolumnbraroutecontract-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnBraRouteContract_feedsBraAmplitude_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnBraRouteContract_feedsBraAmplitude_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary clean column bra route contract feeds bra amplitude n 3”; its local proof does not by itself complete the broader paper route. The clean-column bridge feeds the expected bra-amplitude factor conditionally.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The clean-column bridge feeds the expected bra-amplitude factor conditionally. This theorem only rewrites the existing transpose bridge through the new route contract. The uniform-column hypothesis remains external.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13231](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycleancolumnbraroutecontract-feedsbraamplitude-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnBraRouteContract_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnBraRouteContract_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary clean column bra route contract n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the clean-column to bra-route contract.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the clean-column to bra-route contract. This checks that the route points at the same bra-amplitude obligation in the source map and the factor-semantics contract map, while every semantic proof flag remains false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13259](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycleancolumnbraroutecontract-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRoute" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRoute")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary clean column factor semantics route”. A proposition-valued field is a requirement until a constructor supplies it. Under-contract route from the clean-column bra factor to factor semantics.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Under-contract route from the clean-column bra factor to factor semantics. The route records that the clean-column-to-bra bridge supplies the bra-side factor expected by the factor-semantics contract map. It also keeps the external uniform amplitude, ket amplitude, square-root product convention, finite normalized equality, and focused product theorem as explicit false obligations.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13369](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycleancolumnfactorsemanticsroute). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRoute_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRoute_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary clean column factor semantics route n 3”. Compiled clean-column to factor-semantics route for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled clean-column to factor-semantics route for the focused boundary branch. This declaration is not a proof of the Shukla--Vedula preparation theorem or the final product-to-coefficient obligation. It only connects the clean bra-factor route to the already compiled conditional factor-map evaluation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13424](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycleancolumnfactorsemanticsroute-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRouteEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRouteEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary clean column factor semantics route eval n 3”; its local proof does not by itself complete the broader paper route. Conditional evaluation for the clean-column to factor-semantics route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional evaluation for the clean-column to factor-semantics route. The theorem explicitly consumes the external clean-column hypothesis and the coefficient-environment hypotheses. It proves only the local conditional bridge and the already compiled factor-map evaluation under those contracts.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13495](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycleancolumnfactorsemanticsrouteeval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRoute_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRoute_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary clean column factor semantics route n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the clean-column to factor-semantics route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the clean-column to factor-semantics route. It checks that the route connects the clean-column bra factor to the factor contract map and preserves all theorem-facing semantic flags as false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13539](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarycleancolumnfactorsemanticsroute-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProductUnderContractsRoute" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProductUnderContractsRoute")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary product under contracts route”. A proposition-valued field is a requirement until a constructor supplies it. Product-under-contracts route for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Product-under-contracts route for the focused boundary branch. The clean-column factor-semantics route already supplies the conditional coefficient calculation. This packet ties that route to the fixed 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0' and names the exact remaining bridge: the finite block-composition contract must identify the projected branch product with the theorem's normalized block entry. No semantic proof flag is promoted here.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13637](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryproductundercontractsroute). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductUnderContractsRoute_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductUnderContractsRoute_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary product under contracts route n 3”. Compiled product-under-contracts route for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled product-under-contracts route for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0'. The route uses the clean-column factor-semantics calculation as its local coefficient engine, then records the remaining theorem-facing bridge to the finite block-composition contract. The product obligation remains false.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13689](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryproductundercontractsroute-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductUnderContractsEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductUnderContractsEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary product under contracts eval n 3”; its local proof does not by itself complete the broader paper route. Conditional product-under-contracts evaluation for the focused boundary route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional product-under-contracts evaluation for the focused boundary route. This is only the Lean-local algebra under explicit contracts. It reuses 'oneTermRobinGamma3BoundaryCleanColumnFactorSemanticsRouteEval\_n3' and does not prove the finite block-composition bridge or the product-to-coefficient obligation.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13756](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryproductundercontractseval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductUnderContractsRoute_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProductUnderContractsRoute_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary product under contracts route n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the product-under-contracts route.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the product-under-contracts route. The theorem confirms that the new packet starts from the clean-column factor route, points at the fixed boundary product obligation, and leaves the finite-composition bridge and product-to-coefficient theorem unproved.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13795](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryproductundercontractsroute-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFiniteProjectionBlockEntryIndex_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFiniteProjectionBlockEntryIndex_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary finite projection block entry index n 3”; its local proof does not by itself complete the broader paper route. Finite signal-block index lemma for the focused product/projection bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Finite signal-block index lemma for the focused product/projection bridge. The conditional product route works with the branch basis index '32', where sparse slot '2' and system column '0' are embedded in the full circuit basis. The finite block-composition contract, however, exposes the signal-zero block entry at compound row and column '0' for the '(0,0)' system entry. This lemma records that finite indexing fact without claiming that the branch product has already been summed into the block entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13884](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryfiniteprojectionblockentryindex-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryFiniteProjectionProductBridge" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryFiniteProjectionProductBridge")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary finite projection product bridge”. A proposition-valued field is a requirement until a constructor supplies it. Finite projection/product bridge packet for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Finite projection/product bridge packet for the focused boundary branch. This consumes 'oneTermRobinGamma3BoundaryProductUnderContractsRoute\_n3' and connects it to the exact finite block-composition entry interface. The compiled part is the index bridge: the signal-zero block entry is the full unitary entry at compound row and column '0', while the branch-local product has been calculated at the embedded sparse-slot basis index '32'. The missing field is now explicit: QBE still needs a branch-decomposition/projection theorem identifying the route's projected branch product with the finite signal-zero block entry before the product obligation can be promoted.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13924](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryfiniteprojectionproductbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFiniteProjectionProductBridge_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFiniteProjectionProductBridge_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary finite projection product bridge n 3”. Compiled finite projection/product bridge for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled finite projection/product bridge for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0'. The bridge deliberately does not assert that the branch-local product is the finite block entry. It records the exact indexing mismatch and names the missing branch-decomposition theorem as the current Lean-local obstruction.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:13970](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryfiniteprojectionproductbridge-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFiniteProjectionProductBridge_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryFiniteProjectionProductBridge_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary finite projection product bridge n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the finite projection/product bridge packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the finite projection/product bridge packet. This checks that the bridge consumes the active product-under-contracts route, that the finite signal block uses row and column '0' while the focused branch uses basis index '32', and that all theorem-facing proof flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14043](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryfiniteprojectionproductbridge-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBranchDecompositionSlot2" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBranchDecompositionSlot2")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary branch decomposition slot 2”. A proposition-valued field is a requirement until a constructor supplies it. Branch-decomposition interface for the focused slot-'2' boundary product.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Branch-decomposition interface for the focused slot-'2' boundary product. The finite projection bridge proves only the index fact: Definition 'def:block-encoding' reads the signal-zero block entry at full '\[0,0\]', while the branch-local route is attached to the embedded sparse-slot entry '\[32,32\]'. This packet names the missing finite theorem that must decompose the signal-zero entry into sparse-branch contributions and identify the slot-'2' contribution with the route's projected branch product. It is an obstruction/interface record, not a proof of the branch sum. All theorem-facing proof flags therefore remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14119](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchdecompositionslot2). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchDecompositionSlot2_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchDecompositionSlot2_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary branch decomposition slot 2 n 3”. Compiled branch-decomposition interface for the fixed boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled branch-decomposition interface for the fixed boundary branch. The record consumes 'oneTermRobinGamma3BoundaryFiniteProjectionProductBridge\_n3' and makes the next missing theorem precise: QBE needs a finite branch-sum or projection-summation theorem that sends the slot-'2' projected branch product at '\[32,32\]' into the signal-zero block entry '\[0,0\]'. No semantic flag is promoted.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14171](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchdecompositionslot2-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchDecompositionSlot2_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchDecompositionSlot2_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary branch decomposition slot 2 n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the slot-'2' branch-decomposition interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the slot-'2' branch-decomposition interface. The theorem checks that the packet starts from the finite projection bridge, keeps the signal-zero entry '\[0,0\]' separate from the branch-local entry '\[32,32\]', and leaves the projection-summation theorem and all semantic flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14238](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchdecompositionslot2-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionSummationTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionSummationTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary projection summation target”. A proposition-valued field is a requirement until a constructor supplies it. Typed projection-summation target for the focused slot-'2' boundary packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed projection-summation target for the focused slot-'2' boundary packet. The earlier branch-decomposition record names the missing theorem in prose. This target exposes the actual coefficient objects that the theorem must relate: the signal-zero block entry selected by Definition 'def:block-encoding' and the compiled branch-local seven-gate matrix entry at '\[32,32\]'. The record does not assert that these entries are equal or that the branch contribution has already been summed into the signal-zero block.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14315](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsummationtarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary projection summation target n 3”. Compiled typed target for the missing branch projection/summation theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled typed target for the missing branch projection/summation theorem. The signal-zero block entry is taken from the finite block-composition contract, while the branch entry is the local seven-gate boundary matrix entry at the slot-'2' basis index. The missing theorem is now a typed bridge between these two 'Coeff' objects rather than only a string-level obligation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14367](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsummationtarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationTarget_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationTarget_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection summation target n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the typed projection-summation target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the typed projection-summation target. The theorem checks that the target keeps the signal block entry '\[0,0\]' and the branch matrix entry '\[32,32\]' as typed coefficient objects, names the existing evaluation lemma, and leaves branch selection, projection-summation, normalized equality, and product-to-coefficient flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14474](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsummationtarget-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBranchEntrySelection" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBranchEntrySelection")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary branch entry selection”. A proposition-valued field is a requirement until a constructor supplies it. Conditional branch-entry selection packet for the focused slot-'2' boundary target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional branch-entry selection packet for the focused slot-'2' boundary target. The selected local branch entry is the seven-gate matrix entry at '\[32,32\]'. The route's 'projectedBranchProduct' already includes the two sparse-register projection amplitudes, so the compiled theorem below multiplies the selected branch entry by the existing projection-amplitude factor. The theorem is still conditional on the corrected boundary-rotation entry; it does not prove the projection/summation theorem from the signal-zero block entry '\[0,0\]'.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14544](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchentryselection). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchEntrySelection_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchEntrySelection_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary branch entry selection n 3”. Compiled branch-entry selection interface for the focused projection target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled branch-entry selection interface for the focused projection target. This packet reuses the typed projection-summation target and records the conditional local theorem that selects the branch entry '\[32,32\]' and feeds it to the route product after the sparse-register projection-amplitude factor is attached. All source obligations and theorem-facing flags remain false.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14583](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchentryselection-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchEntrySelectionEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchEntrySelectionEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary branch entry selection eval n 3”; its local proof does not by itself complete the broader paper route. Conditional branch-entry selection for the focused projection target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Conditional branch-entry selection for the focused projection target. Under the corrected 'Ry\_boundary' entry hypothesis, the selected seven-gate entry '\[32,32\]', multiplied by the existing sparse-register projection amplitude factor, evaluates to the route's typed 'projectedBranchProduct'. This is not the signal-block projection/summation theorem.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14633](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchentryselectioneval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchEntrySelection_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchEntrySelection_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary branch entry selection n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the branch-entry selection packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the branch-entry selection packet. The theorem records the new conditional local lemma and checks that the actual branch-entry selection, projection/summation, product bridge, normalized equality, and product-to-coefficient obligations remain unproved.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14673](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchentryselection-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionSummationObstruction" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryProjectionSummationObstruction")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary projection summation obstruction”. A proposition-valued field is a requirement until a constructor supplies it. Typed obstruction for the remaining finite projection/summation step.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed obstruction for the remaining finite projection/summation step. The selected slot-'2' contribution is now a concrete 'Coeff': the branch-local entry '\[32,32\]' multiplied by the two sparse-register projection amplitudes. What QBE still lacks is a finite matrix-semantics field that presents the signal-zero entry '\[0,0\]' as a sum over sparse-branch contributions and then selects the slot-'2' summand. This record names that missing field without asserting the sum.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14746](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsummationobstruction). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationObstruction_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationObstruction_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary projection summation obstruction n 3”. Compiled typed obstruction for the focused boundary projection/summation bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled typed obstruction for the focused boundary projection/summation bridge. The object is the next theorem-facing interface for 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0': it records the slot domain '0, ..., 6', identifies slot '2', and exposes the selected contribution as a typed coefficient. The sparse-branch contribution family itself is absent from the current finite matrix semantics.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14799](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsummationobstruction-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationObstruction_selectedSlotEval_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationObstruction_selectedSlotEval_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection summation obstruction selected slot eval n 3”; its local proof does not by itself complete the broader paper route. The new obstruction reuses the accepted branch-entry selection lemma.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The new obstruction reuses the accepted branch-entry selection lemma. Under the corrected boundary-rotation entry hypothesis, the typed selected slot contribution evaluates to the route's projected branch product. This still does not prove that the signal-zero block entry is the sparse-branch sum.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14870](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsummationobstruction-selectedsloteval-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationObstruction_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryProjectionSummationObstruction_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary projection summation obstruction n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the typed projection/summation obstruction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the typed projection/summation obstruction. The theorem checks that the sparse-slot domain and selected contribution are typed, names the exact missing branch-contribution family, and keeps every projection, block-composition, and theorem-facing flag false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14899](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryprojectionsummationobstruction-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionFocusedSlot" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionFocusedSlot")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary branch contribution focused slot”. Focused sparse slot for the branch-contribution interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused sparse slot for the branch-contribution interface. The source boundary branch of Eq. 'ROBIN clarified' uses the global sparse slot '2' for system entry '(0,0)' in the finite 'n = 3', 'κ = 7' witness.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14985](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontributionfocusedslot). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionSum" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionSum")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary branch contribution sum”. Typed sparse-branch sum over the seven one-term Robin sparse slots.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed sparse-branch sum over the seven one-term Robin sparse slots. This is intentionally a project-local 'List.finRange' fold instead of a 'Finset.sum', because 'Coeff' is a syntactic coefficient language rather than an additive commutative monoid. It provides the Lean type that the missing projection/summation theorem must target.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:14996](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontributionsum). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionPlaceholder_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionPlaceholder_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary branch contribution placeholder n 3”. Placeholder branch-contribution family for the focused projection/summation interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Placeholder branch-contribution family for the focused projection/summation interface. Only slot '2' is identified with the already compiled selected contribution. The other slots remain opaque symbolic placeholders; this definition does not assert that their sum is the signal-zero block entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15008](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontributionplaceholder-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBranchContributionFamily" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBranchContributionFamily")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary branch contribution family”. A proposition-valued field is a requirement until a constructor supplies it. Typed branch-contribution family required by the finite projection/summation bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed branch-contribution family required by the finite projection/summation bridge. The record supplies the missing shape 'branchContribution : Fin 7 -> Coeff', proves only the selected slot-'2' identity, and leaves the statement 'signalBlockEntry = branchContributionSum' as a typed unproved proposition.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15026](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontributionfamily). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionFamily_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionFamily_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary branch contribution family n 3”. Compiled branch-contribution family for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled branch-contribution family for the focused 'n = 3' boundary branch. This turns the previous string-level interface into a typed Lean family. It does not prove that the signal-zero block entry is the sparse-branch sum.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15059](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontributionfamily-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContribution_selectedSlot_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContribution_selectedSlot_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary branch contribution selected slot n 3”; its local proof does not by itself complete the broader paper route. The typed branch-contribution family selects the accepted slot-'2' contribution.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The typed branch-contribution family selects the accepted slot-'2' contribution. This is only the local selected-slot identity. It is not the sparse-branch summation theorem for the signal-zero block entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15108](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontribution-selectedslot-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBranchContributionObstruction" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBranchContributionObstruction")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary branch contribution obstruction”. A proposition-valued field is a requirement until a constructor supplies it. Typed obstruction after introducing the branch-contribution family.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed obstruction after introducing the branch-contribution family. The selected slot theorem is now compiled, but the QBE-local finite matrix semantics still lacks the summation proof connecting the signal-zero block entry to the branch-contribution fold.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15121](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontributionobstruction). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionObstruction_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionObstruction_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary branch contribution obstruction n 3”. Current obstruction for the focused projection/summation bridge after the branch-contribution family has been made a typed Lean interface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Current obstruction for the focused projection/summation bridge after the branch-contribution family has been made a typed Lean interface.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15146](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontributionobstruction-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionObstruction_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBranchContributionObstruction_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary branch contribution obstruction n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the branch-contribution-family obstruction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the branch-contribution-family obstruction. The theorem verifies that the focused family is typed, slot '2' is selected, and every theorem-facing semantic flag remains false except the local selected-slot interface theorem.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15181](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybranchcontributionobstruction-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContributionPredicate_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContributionPredicate_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend branch contribution predicate n 3”. Predicate that a backend-sourced sparse-branch contribution family must satisfy for the focused boundary projection/summation theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Predicate that a backend-sourced sparse-branch contribution family must satisfy for the focused boundary projection/summation theorem. This is the next-run target, not a new assumption. A candidate family must come from the finite projection semantics, select slot '2' as the accepted branch contribution, and sum to the signal-zero block entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15240](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontributionpredicate-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendProjectionSummationFieldTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendProjectionSummationFieldTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary backend projection summation field target”. A proposition-valued field is a requirement until a constructor supplies it. Smallest backend field still missing from the focused projection bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest backend field still missing from the focused projection bridge. The previous packet supplied a placeholder 'branchContribution' family so Lean could type the selected-slot and branch-sum statements. This record prevents that placeholder from being mistaken for the finite matrix-semantics field: the actual field must be sourced from the 'BlockExtractionTarget'/projection backend and satisfy 'oneTermRobinGamma3BoundaryBackendBranchContributionPredicate\_n3'.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15257](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendprojectionsummationfieldtarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendProjectionSummationFieldTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendProjectionSummationFieldTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend projection summation field target n 3”. Concrete backend-field target for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete backend-field target for the focused 'n = 3' boundary branch. No theorem-facing flag is promoted. The record says that the placeholder family is useful only for typing the statements; the missing semantic field is a backend-sourced 'Fin 7 -> Coeff' family for the signal-zero entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15291](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendprojectionsummationfieldtarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBlockExtractionBranchContributionTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBlockExtractionBranchContributionTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary block extraction branch contribution target n 3”. Generic block-extraction branch-contribution target for the focused boundary entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Generic block-extraction branch-contribution target for the focused boundary entry. This uses the new QBE-local backend interface to type the seven-slot family at 'contract.expectedTarget.blockMatrix\[0,0\]'. The family is still the current placeholder from the Robin obstruction, so the backend-source and branch-sum obligations stay false. This target exists only to make the next required backend theorem precise.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15392](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryblockextractionbranchcontributiontarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBlockExtractionBackendGap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBlockExtractionBackendGap")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary block extraction backend gap”. A proposition-valued field is a requirement until a constructor supplies it. Smallest obstruction after inspecting the current 'BlockExtractionTarget' backend.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest obstruction after inspecting the current 'BlockExtractionTarget' backend. The backend gives a concrete 'blockMatrix\[0,0\]' entry and the corresponding full-unitary entry. It does not yet expose a sparse-slot contribution family for that entry. This record is therefore a narrower obstruction than the generic backend-field target: it points at the existing 'BlockExtractionTarget' fields and names the missing projection-summand interface.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15474](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryblockextractionbackendgap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBlockExtractionBackendGap_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBlockExtractionBackendGap_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary block extraction backend gap n 3”. Concrete backend gap for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete backend gap for the focused 'n = 3' boundary branch. This does not change 'BlockExtractionTarget' or prove the branch sum. It records that the available backend data reaches only the signal-zero block entry and its full-unitary index bridge.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15524](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryblockextractionbackendgap-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBlockExtractionBackendGap_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBlockExtractionBackendGap_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary block extraction backend gap n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the block-extraction backend gap.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the block-extraction backend gap. The theorem checks that the gap is tied to the actual 'BlockExtractionTarget' entry and that all theorem-facing semantic flags remain false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15579](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryblockextractionbackendgap-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend branch full index n 3”. Full-basis branch index map for the focused 'n = 3' boundary backend packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Full-basis branch index map for the focused 'n = 3' boundary backend packet. For the system column '0', this maps each sparse slot to the clean paper-basis index used by the displayed 'gamma3' register expression. The map is typed as a full circuit basis index; it does not by itself provide the branch summand formula or the branch-sum theorem for the signal-zero block entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15651](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchfullindex-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_selected_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_selected_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch full index selected n 3”; its local proof does not by itself complete the broader paper route. The backend branch-index map sends the focused slot '2' to the accepted clean branch basis index '32'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The backend branch-index map sends the focused slot '2' to the accepted clean branch basis index '32'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15675](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchfullindex-selected-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_slotZero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_slotZero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch full index slot zero n 3”; its local proof does not by itself complete the broader paper route. The backend branch-index map sends sparse slot '0' to the active signal-zero full basis index '0'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The backend branch-index map sends sparse slot '0' to the active signal-zero full basis index '0'. This is the active-entry side of the current raw-fold obstruction: the uncast '\[0,0\]' entry is attached to the slot-'0' diagonal, while the backend fold still contains all seven sparse-slot summands.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15690](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchfullindex-slotzero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_value_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_value_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch full index value n 3”; its local proof does not by itself complete the broader paper route. The all-slot backend branch-index map embeds sparse slot 's' at full basis index '16 \* s'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The all-slot backend branch-index map embeds sparse slot 's' at full basis index '16 \* s'. This is the reusable index feeder for future slot support or cancellation lemmas in the full-unitary fold; it does not prove any summand vanishes and does not assert the branch-sum theorem.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15705](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchfullindex-value-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_injective_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFullIndex_injective_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch full index injective n 3”; its local proof does not by itself complete the broader paper route. The seven backend sparse slots occupy distinct full-basis indices.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The seven backend sparse slots occupy distinct full-basis indices. This is a support feeder for the full-unitary fold frontier: later slot-by-slot support or cancellation lemmas can use it to rule out accidental branch-index collisions. It does not prove that any summand vanishes or that the fold equals the signal-zero unitary entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15722](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchfullindex-injective-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendSlotOneDaggerAfterSwap_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendSlotOneDaggerAfterSwap_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend slot one dagger after swap zero n 3”; its local proof does not by itself complete the broader paper route. Slot-'1' clean path support mismatch for the backend diagonal branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Slot-'1' clean path support mismatch for the backend diagonal branch. The backend slot maps to full index '16'; the forward sparse-access image is '112', and SWAP sends that image to '14'. The transpose-style dagger row for the original slot-'1' index has zero entry at column '14', so the clean slot-'1' path cannot close the diagonal branch through the dagger. This is a strict support feeder for a future slot-'1' vanish proof; it proves no full fold equality and promotes no semantic flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15741](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendslotonedaggerafterswap-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendSelectedBranchSummandFormula_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendSelectedBranchSummandFormula_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend selected branch summand formula n 3”; its local proof does not by itself complete the broader paper route. The selected contribution in the generic branch target is the already compiled slot-'2' seven-gate summand formula.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The selected contribution in the generic branch target is the already compiled slot-'2' seven-gate summand formula. This proves only the selected branch formula. It does not construct the all-slot backend family and does not prove that the signal-zero block entry is the seven-branch fold.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15837](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendselectedbranchsummandformula-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendBranchIndexMapObstruction" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendBranchIndexMapObstruction")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary backend branch index map obstruction”. A proposition-valued field is a requirement until a constructor supplies it. Narrow obstruction after adding the branch-to-full-index map.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Narrow obstruction after adding the branch-to-full-index map. The selected branch now has a typed full-basis index and a compiled selected summand formula. The remaining backend gap is smaller: QBE still lacks the all-slot summand formula that would compute every 'branchContribution s' from the projection backend and then prove the folded sum equals 'contract.expectedTarget.blockMatrix\[0,0\]'.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15866](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchindexmapobstruction). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchIndexMapObstruction_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchIndexMapObstruction_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend branch index map obstruction n 3”. Focused 'n = 3' backend branch-index map obstruction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused 'n = 3' backend branch-index map obstruction. This packet is the current smallest Lean-facing interface: the full-basis index map for the seven sparse slots is present, and slot '2' is connected to the selected summand. The all-slot summand formula and branch-sum predicate remain unavailable.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:15912](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchindexmapobstruction-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend branch contribution n 3”. All-slot backend summand formula for the focused 'n = 3' boundary packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* All-slot backend summand formula for the focused 'n = 3' boundary packet. Each sparse slot is mapped through the compiled branch-to-full-index map and then read from the focused seven-gate matrix. The two sparse-register projection amplitudes are attached uniformly. This supplies the all-slot formula requested by the projection backend, but it is not yet the theorem that the signal-zero block entry is the fold of these seven summands.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:16035](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_selected_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_selected_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch contribution selected n 3”; its local proof does not by itself complete the broader paper route. The all-slot backend summand formula selects the accepted slot-'2' contribution.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The all-slot backend summand formula selects the accepted slot-'2' contribution. This proves the selected branch clause of 'oneTermRobinGamma3BoundaryBackendBranchContributionPredicate\_n3'. The branch-sum clause remains a separate projection/summation theorem.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:16051](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-selected-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotZero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotZero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch contribution slot zero n 3”; its local proof does not by itself complete the broader paper route. The slot-'0' backend summand is the active '\[0,0\]' seven-gate diagonal multiplied by the sparse-register projection amplitude factor.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The slot-'0' backend summand is the active '\[0,0\]' seven-gate diagonal multiplied by the sparse-register projection amplitude factor. This is a smaller compiled term identification for the raw uncast backend-expansion target. It does not prove that the active '\[0,0\]' entry is the full seven-slot fold; it shows that the fold's slot-'0' term is the active diagonal term with the projection weight attached.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:16071](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-slotzero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotZeroEval_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotZeroEval_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch contribution slot zero eval zero n 3”; its local proof does not by itself complete the broader paper route. The slot-'0' backend branch contribution vanishes after coefficient evaluation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The slot-'0' backend branch contribution vanishes after coefficient evaluation. This packages the active column-'0' vanish fact with the backend summand formula. It is a local support lemma for the active/prepared entry frontier; the all-slot fold and active/prepared equality remain open.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:16092](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-slotzeroeval-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotOneEval_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotOneEval_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch contribution slot one eval zero n 3”; its local proof does not by itself complete the broader paper route. The slot-'1' backend branch contribution vanishes after coefficient evaluation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The slot-'1' backend branch contribution vanishes after coefficient evaluation. This is the first full slot-'1' vanish feeder: the all-slot backend summand formula maps slot '1' to the full diagonal entry '\[16,16\]', and the finite seven-gate matrix entry is zero for the focused backend. It does not prove the active/prepared equality, the full unitary fold, or any oracle/block flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:16434](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-slotoneeval-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotThreeEval_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotThreeEval_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch contribution slot three eval zero n 3”; its local proof does not by itself complete the broader paper route. The slot-'3' backend branch contribution vanishes after coefficient evaluation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The slot-'3' backend branch contribution vanishes after coefficient evaluation. This is the first full evaluated remaining-slot vanish feeder. It uses the slot-'3' full index '48', the seven-gate diagonal support at '\[48,48\]', and the existing backend branch summand formula. It does not prove the active/prepared equality, the full unitary fold, or any oracle/block flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:16764](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-slotthreeeval-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotFourEval_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotFourEval_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch contribution slot four eval zero n 3”; its local proof does not by itself complete the broader paper route. The slot-'4' backend branch contribution vanishes after coefficient evaluation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The slot-'4' backend branch contribution vanishes after coefficient evaluation. This is a full evaluated remaining-slot feeder at index '64', following the same local support route as the compiled slot-'3' proof. It does not prove the active/prepared equality, the full unitary fold, or any oracle/block flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:17093](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-slotfoureval-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotFiveEval_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotFiveEval_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch contribution slot five eval zero n 3”; its local proof does not by itself complete the broader paper route. The slot-'5' backend branch contribution vanishes after coefficient evaluation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The slot-'5' backend branch contribution vanishes after coefficient evaluation. This is the post-slot-'4' full evaluated remaining-slot feeder at index '80'. It only advances the local finite matrix-semantics DAG for the all-slot backend fold; it does not prove the active/prepared equality, the full unitary fold, or any oracle/block flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:17423](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-slotfiveeval-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotSixEval_zero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContribution_slotSixEval_zero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch contribution slot six eval zero n 3”; its local proof does not by itself complete the broader paper route. The slot-'6' backend branch contribution vanishes after coefficient evaluation.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The slot-'6' backend branch contribution vanishes after coefficient evaluation. This closes the last remaining evaluated backend-slot vanish feeder at full index '96'. It only advances the local finite matrix-semantics DAG for the all-slot backend fold; it does not prove the active/prepared equality, the full unitary fold, or any oracle/block flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:17753](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontribution-slotsixeval-zero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFoldEval_eq_selectedSlotContribution_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFoldEval_eq_selectedSlotContribution_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch fold eval eq selected slot contribution n 3”; its local proof does not by itself complete the broader paper route. After the compiled vanish feeders for slots '0', '1', '3', '4', '5', and '6', the evaluated seven-slot backend fold collapses to the selected slot-'2' contribution.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* After the compiled vanish feeders for slots '0', '1', '3', '4', '5', and '6', the evaluated seven-slot backend fold collapses to the selected slot-'2' contribution. This is a backend-side feeder for 'ActiveUncastToPreparedEntry'; it does not prove the active/prepared equality and promotes no theorem-facing oracle, projection, block-correctness, or final-extraction flag.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:17790](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchfoldeval-eq-selectedslotcontribution-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFold_expandedSlotZero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFold_expandedSlotZero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch fold expanded slot zero n 3”; its local proof does not by itself complete the broader paper route. Concrete seven-summand expansion of the backend branch fold.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete seven-summand expansion of the backend branch fold. This is the smaller compiled obstruction for the current backend-expansion target: the first summand is the active row-'0' diagonal branch, weighted by the sparse-register projection amplitude, and the remaining six summands stay as the all-slot backend contribution family. It does not prove that the active signal-zero entry equals this fold.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:17841](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchfold-expandedslotzero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFold_expandedAllSlots_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchFold_expandedAllSlots_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch fold expanded all slots n 3”; its local proof does not by itself complete the broader paper route. Concrete seven-slot expansion of the backend branch fold.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete seven-slot expansion of the backend branch fold. This support lemma exposes every sparse-slot summand as the corresponding full-basis diagonal entry of 'oneTermRobinGamma3BoundarySevenGateMatrix\_n3', weighted by the sparse-register projection amplitude. It does not prove that the active signal-zero entry equals this fold.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:17872](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchfold-expandedallslots-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContributionTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchContributionTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend branch contribution target n 3”. Backend branch-contribution target using the all-slot summand formula.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Backend branch-contribution target using the all-slot summand formula. Unlike 'oneTermRobinGamma3BoundaryBlockExtractionBranchContributionTarget\_n3', this target no longer uses the placeholder family. The 'backendSource' and 'branchSummationCorrect' obligations remain false until the finite projection backend proves that this seven-slot family is exactly the signal-zero block expansion.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18019](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchcontributiontarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendAllSlotSummandFormula" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendAllSlotSummandFormula")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary backend all slot summand formula”. A proposition-valued field is a requirement until a constructor supplies it. Follow-up packet after the branch-index obstruction.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Follow-up packet after the branch-index obstruction. The all-slot summand formula is now a concrete 'Fin 7 -> Coeff' family sourced from the branch full-index map and the focused seven-gate matrix. The packet proves only the selected slot-'2' clause. The remaining theorem is still the finite projection/summation equality that identifies the signal-zero block entry with the fold of this backend family.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18097](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendallslotsummandformula). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendAllSlotSummandFormula_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendAllSlotSummandFormula_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend all slot summand formula n 3”. Concrete all-slot backend summand formula packet for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete all-slot backend summand formula packet for the focused boundary branch. This supersedes the previous branch-index obstruction only for the all-slot formula itself: 'backendBranchContribution s' is now defined for every 's : Fin 7'. The full backend predicate remains unproved because its second clause is the missing signal-block branch-sum theorem.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18143](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendallslotsummandformula-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendBranchSumClosure" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendBranchSumClosure")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary backend branch sum closure”. A proposition-valued field is a requirement until a constructor supplies it. Final focused obstruction for the current backend branch-sum packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Final focused obstruction for the current backend branch-sum packet. The selected sparse slot is proved and the predicate closure is conditional on one equality. The unproved equality is precisely the QBE-local projection summation statement: the signal-zero block entry must be the fold of the backend seven-slot branch family.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18308](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchsumclosure). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchSumClosure_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchSumClosure_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend branch sum closure n 3”. Concrete branch-sum closure target for the focused 'n = 3' boundary packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete branch-sum closure target for the focused 'n = 3' boundary packet. This record is the narrow fallback for the current lower task: it does not claim the branch sum, but it proves that the selected clause is no longer a blocker and names the single remaining proposition.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18348](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchsumclosure-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchSumClosure_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendBranchSumClosure_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend branch sum closure n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the backend branch-sum closure target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the backend branch-sum closure target. The theorem verifies that the new packet consumes the all-slot summand formula, proves the selected predicate clause, and keeps the actual projection summation statement and every theorem-facing semantic flag false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18405](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendbranchsumclosure-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendProjectionStatement_signalEntry_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendProjectionStatement_signalEntry_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend projection statement signal entry n 3”; its local proof does not by itself complete the broader paper route. The signal entry used in the Robin-local obstruction is the block entry of the generic backend branch-contribution target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The signal entry used in the Robin-local obstruction is the block entry of the generic backend branch-contribution target. This is an index/record bridge only. It does not assert that the block entry equals the folded branch contribution family.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18483](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendprojectionstatement-signalentry-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendProjectionStatementObstruction" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendProjectionStatementObstruction")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary backend projection statement obstruction”. A proposition-valued field is a requirement until a constructor supplies it. Smallest obstruction after attempting the generic projection statement.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest obstruction after attempting the generic projection statement. The previous declarations provide the all-slot branch family and the selected slot theorem. This packet records the remaining missing backend theorem: 'BlockExtractionTarget' exposes the signal-zero block entry, but it does not yet expose a proof that this entry expands as the fold over the backend sparse-branch contributions.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18573](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendprojectionstatementobstruction). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendProjectionStatementObstruction_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendProjectionStatementObstruction_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend projection statement obstruction n 3”. Compiled obstruction for the current lower target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled obstruction for the current lower target. No theorem-facing flag is promoted. The packet only names the exact missing projection-backend field required to turn the current all-slot family into the signal-zero block-entry sum.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18612](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendprojectionstatementobstruction-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendExpansionBridge" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendExpansionBridge")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary backend expansion bridge”. A proposition-valued field is a requirement until a constructor supplies it. Proof-DAG packet for the remaining backend-expansion theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Proof-DAG packet for the remaining backend-expansion theorem. The packet records that the generic backend-expansion interface is now available and that it conditionally closes the focused projection statement. The actual sparse-slot fold theorem is still absent, so all theorem-facing semantic flags remain false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18792](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendexpansionbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendExpansionBridge_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendExpansionBridge_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend expansion bridge n 3”. Compiled backend-expansion bridge packet for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled backend-expansion bridge packet for the focused boundary branch. This is an interface refinement, not a proof of the sparse-branch expansion. It keeps the current 'oneTermRobinGamma3ProductToCoefficientObligation 3 0 0' blocked until Lean proves the backend expansion statement.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18833](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendexpansionbridge-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendExpansionBridge_n3_transcript" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendExpansionBridge_n3_transcript")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend expansion bridge n 3 transcript”; its local proof does not by itself complete the broader paper route. Transcript theorem for the backend-expansion bridge packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Transcript theorem for the backend-expansion bridge packet. The theorem verifies that the packet uses the generic proof-DAG interface, records the Robin-local equivalence, and keeps the backend expansion and all theorem-facing semantic flags false.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:18886](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendexpansionbridge-n3-transcript). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendUnitaryEntryFoldTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendUnitaryEntryFoldTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary backend unitary entry fold target”. A proposition-valued field is a requirement until a constructor supplies it. Smallest current projection-backend target after moving from the cached block entry to the full finite product entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest current projection-backend target after moving from the cached block entry to the full finite product entry. The record points at the exact next theorem: the signal-zero full-unitary entry selected by 'def:block-encoding' must be expanded as the seven-slot backend fold. It keeps the backend expansion, product-to-coefficient theorem, LCU, block projection, block correctness, and final extraction flags false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19027](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendunitaryentryfoldtarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendUnitaryEntryFoldTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendUnitaryEntryFoldTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend unitary entry fold target n 3”. Concrete unitary-entry fold target for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete unitary-entry fold target for the focused 'n = 3' boundary branch. This is the accepted fallback when the preferred backend expansion theorem is not available: it replaces the broad block-matrix fold obligation by the full-product entry fold that a finite projection backend must provide.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19067](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendunitaryentryfoldtarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendUnitaryEntryFoldSupportTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryBackendUnitaryEntryFoldSupportTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary backend unitary entry fold support target”. A proposition-valued field is a requirement until a constructor supplies it. Support packet for the remaining full-unitary entry fold.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Support packet for the remaining full-unitary entry fold. The packet records the finite fold domain, proves that the focused slot '2' is inside that domain, and keeps the actual theorem 'signalUnitaryEntry = blockExtractionBranchContributionSum ...' as the remaining projection-backend obligation.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19197](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendunitaryentryfoldsupporttarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendUnitaryEntryFoldSupportTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendUnitaryEntryFoldSupportTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary backend unitary entry fold support target n 3”. Concrete fold-support target for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete fold-support target for the focused 'n = 3' boundary branch. This refines the obstruction from "prove a seven-slot fold" to the exact remaining backend theorem: the fold domain contains slot '2' and the slot is already identified with the accepted summand, but Lean still lacks the finite product/projection proof that the full signal-zero entry equals the complete seven-slot fold.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19244](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendunitaryentryfoldsupporttarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedBranchContribution_formula_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedBranchContribution_formula_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary prepared branch contribution formula n 3”; its local proof does not by itself complete the broader paper route. Every backend sparse-slot contribution is the corresponding branch-diagonal seven-gate entry, multiplied by the two sparse-register projection amplitudes.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Every backend sparse-slot contribution is the corresponding branch-diagonal seven-gate entry, multiplied by the two sparse-register projection amplitudes. This is the all-slot formula that was implicit in 'oneTermRobinGamma3BoundaryBackendBranchContribution\_n3'. It is not the full-entry fold theorem: it only identifies the summands of that fold.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19368](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedbranchcontribution-formula-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryPreparedBranchExpansionTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryPreparedBranchExpansionTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary prepared branch expansion target”. A proposition-valued field is a requirement until a constructor supplies it. Typed target for the prepared branch expansion still missing from the focused projection bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed target for the prepared branch expansion still missing from the focused projection bridge. The current 'CircuitMatrixSemantics' exposes the raw seven-gate product entry selected by the signal-zero block convention. The branch fold, however, also uses the external sparse-register preparation/projection amplitudes. This packet proves the all-slot summand formula and records the missing backend field as a prepared-projection theorem, rather than promoting the fold itself.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19390](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedbranchexpansiontarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedBranchExpansionTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedBranchExpansionTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared branch expansion target n 3”. Concrete prepared-branch expansion target for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete prepared-branch expansion target for the focused 'n = 3' boundary branch. The packet narrows the missing interface: the summands are now proved to be the prepared branch entries, and the only absent theorem is the backend proof that the raw signal-zero entry expands through those prepared branches.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19445](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedbranchexpansiontarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySparseCleanIndex_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySparseCleanIndex_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary sparse clean index n 3”. Clean sparse-register column index for the focused 'H\_W^(kappa)' packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Clean sparse-register column index for the focused 'H\_W^(kappa)' packet.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19589](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysparsecleanindex-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySparseSlotIndex_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySparseSlotIndex_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary sparse slot index n 3”. Embed one of the seven paper sparse slots into the eight-dimensional register.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Embed one of the seven paper sparse slots into the eight-dimensional register.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19593](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysparseslotindex-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaUniformColumnAllSlotsStatement_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryHWKappaUniformColumnAllSlotsStatement_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary hw kappa uniform column all slots statement n 3”. Focused uniform-column statement for the sparse-register preparation matrix.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Focused uniform-column statement for the sparse-register preparation matrix. This is the exact local shape of the Shukla--Vedula contract needed by the prepared projection bridge: each of the seven paper slots has clean-column amplitude 'sqrt\_kappa\_inv'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19603](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryhwkappauniformcolumnallslotsstatement-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedProjectionSandwichContribution_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedProjectionSandwichContribution_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared projection sandwich contribution n 3”. Prepared sandwich contribution for one sparse slot.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Prepared sandwich contribution for one sparse slot. The expression is the local branch-diagonal seven-gate entry multiplied by the ket-side 'H\_W^(kappa)' clean-column amplitude and the matching transpose-style bra amplitude. It is the smallest matrix object missing from the raw 'CircuitMatrixSemantics' block entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19618](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedprojectionsandwichcontribution-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedProjectionSandwichSum_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedProjectionSandwichSum_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared projection sandwich sum n 3”. Fold the prepared sandwich contributions over the seven paper sparse slots.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Fold the prepared sandwich contributions over the seven paper sparse slots.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19632](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedprojectionsandwichsum-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryPreparedProjectionSandwichBackendTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryPreparedProjectionSandwichBackendTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary prepared projection sandwich backend target”. A proposition-valued field is a requirement until a constructor supplies it. Smallest prepared-projection backend field still missing from the current matrix semantics.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest prepared-projection backend field still missing from the current matrix semantics. QBE can now prove that a prepared 'H\_W^(kappa)^dagger \* U \* H\_W^(kappa)' sandwich fold specializes to the backend branch sum. What remains absent is a field or theorem connecting the raw signal-zero entry exposed by 'CircuitMatrixSemantics' to that prepared sandwich fold.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19719](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedprojectionsandwichbackendtarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedProjectionSandwichBackendTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedProjectionSandwichBackendTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared projection sandwich backend target n 3”. Concrete prepared-sandwich backend target for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete prepared-sandwich backend target for the focused 'n = 3' boundary branch. This is a strict reduction of the previous obstruction: the branch summands and their fold are now connected to an explicit 'H\_W^(kappa)' clean-column matrix contract. The missing theorem is only the raw-entry-to-prepared-fold backend field.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19760](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedprojectionsandwichbackendtarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRawEntryPreparedSandwichCircuitField" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryRawEntryPreparedSandwichCircuitField")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary raw entry prepared sandwich circuit field”. A proposition-valued field is a requirement until a constructor supplies it. Typed raw-entry field needed by the prepared-sandwich backend.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed raw-entry field needed by the prepared-sandwich backend. The previous packet proved that a prepared sparse-register sandwich fold specializes to the backend branch fold under the clean-column contract. This record names the smaller remaining finite matrix field: the actual signal-zero entry exposed by 'CircuitMatrixSemantics' must equal that prepared sandwich fold. It does not assert that field.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19891](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrawentrypreparedsandwichcircuitfield). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRawEntryPreparedSandwichCircuitField_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRawEntryPreparedSandwichCircuitField_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary raw entry prepared sandwich circuit field n 3”. Concrete raw-entry prepared-sandwich field for the focused boundary packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete raw-entry prepared-sandwich field for the focused boundary packet. The matrix 'H' is the sparse-register preparation matrix named by the source contract. The record keeps the Shukla--Vedula clean-column contract separate from the QBE-local raw circuit-entry theorem.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:19925](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrawentrypreparedsandwichcircuitfield-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRawUnitaryEntry_contractMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryRawUnitaryEntry_contractMatrix_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary raw unitary entry contract matrix n 3”; its local proof does not by itself complete the broader paper route. The raw entry in the focused packet is the active seven-gate circuit product entry selected by the finite block-extraction contract.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The raw entry in the focused packet is the active seven-gate circuit product entry selected by the finite block-extraction contract. This is smaller than the prepared-sandwich theorem: it identifies the source of the raw entry without asserting that the active circuit product already contains the sparse-register preparation and its adjoint.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20126](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryrawunitaryentry-contractmatrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySparsePreparationGates_absent_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySparsePreparationGates_absent_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary sparse preparation gates absent n 3”; its local proof does not by itself complete the broader paper route. The active Fig.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The active Fig. 1-term Robin gate list does not include the external 'H\_W^(kappa)' sparse-register preparation block or its adjoint. The missing prepared-sandwich theorem therefore cannot be obtained by simply unfolding 'oneTermRobinGateMatrixPlaceholders'; QBE still needs either a prepared circuit semantics object or a theorem identifying the active raw entry with that prepared circuit entry.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20142](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysparsepreparationgates-absent-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryPreparedCircuitSemanticsGap" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryPreparedCircuitSemanticsGap")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary prepared circuit semantics gap”. A proposition-valued field is a requirement until a constructor supplies it. Smallest prepared-circuit semantics gap after exposing the raw entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest prepared-circuit semantics gap after exposing the raw entry. The current raw entry is the active seven-gate 'CircuitMatrixSemantics' entry at '\[0,0\]'. The prepared-sandwich equality needs a circuit-matrix field for the source-preparation sandwich 'H\_W^(kappa)^dagger \* U \* H\_W^(kappa)', or an equivalent theorem relating the active raw entry to that prepared entry. This record does not add an assumption and does not promote any theorem-facing semantic flag.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20161](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcircuitsemanticsgap). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCircuitSemanticsGap_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCircuitSemanticsGap_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared circuit semantics gap n 3”. Compiled prepared-circuit semantics gap for the focused 'n = 3' boundary packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compiled prepared-circuit semantics gap for the focused 'n = 3' boundary packet. This is a strict refinement of the raw-entry field: Lean now knows that the raw entry is sourced from the active seven-gate contract matrix and that no 'H\_W^(kappa)' preparation gate is present in that active gate list. The next field must therefore be a prepared circuit semantics matrix, not another restatement of the same raw-entry equality.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20195](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcircuitsemanticsgap-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCircuitSparseMatrix_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCircuitSparseMatrix_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared circuit sparse matrix n 3”. Compressed prepared sparse-register sandwich matrix for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Compressed prepared sparse-register sandwich matrix for the focused boundary branch. Rows and columns are sparse-register indices. The clean-clean entry is the seven-slot fold for the prepared 'H\_W^(kappa)^dagger \* oneTermRobinGamma3BoundarySevenGateMatrix\_n3 \* H\_W^(kappa)' sandwich. This is a local matrix-interface block; it does not assert that the active raw circuit entry equals this prepared entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20294](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcircuitsparsematrix-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCompositeGate_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCompositeGate_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared composite gate n 3”. Composite prepared sparse-register gate for the focused boundary packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Composite prepared sparse-register gate for the focused boundary packet. This is a local semantics object for the source-side prepared product 'H\_W^(kappa)^dagger \* U \* H\_W^(kappa)' on the sparse register. Its unitarity claim stays false because the cited state-preparation and diagonal-product certificates are not being proved in this lower packet.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20376](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcompositegate-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCompositeCircuit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCompositeCircuit_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared composite circuit n 3”. Singleton circuit for the prepared sparse-register composite gate.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Singleton circuit for the prepared sparse-register composite gate.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20391](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcompositecircuit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCompositeGateMatchesCircuit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCompositeGateMatchesCircuit_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary prepared composite gate matches circuit n 3”; its local proof does not by itself complete the broader paper route. The prepared composite gate matrix matches its singleton circuit label.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The prepared composite gate matrix matches its singleton circuit label.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20396](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcompositegatematchescircuit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCompositeCircuitSemantics_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCompositeCircuitSemantics_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared composite circuit semantics n 3”. Circuit-matrix semantics for the prepared sparse-register composite.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Circuit-matrix semantics for the prepared sparse-register composite. This is not the active seven-gate Fig. 1-term Robin circuit. It is the prepared-side matrix object that the source projection step requires before one can relate the active signal-zero entry to a prepared clean entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20411](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcompositecircuitsemantics-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryPreparedCircuitMatrixInterface" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryPreparedCircuitMatrixInterface")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary prepared circuit matrix interface”. A proposition-valued field is a requirement until a constructor supplies it. Prepared-circuit matrix interface for the current projection backend.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Prepared-circuit matrix interface for the current projection backend. This packet supplies the missing prepared sparse-register matrix object and proves its clean entry is the prepared sandwich fold. It leaves the theorem connecting the active raw 'CircuitMatrixSemantics' entry to this prepared matrix entry as the exact remaining obstruction.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20493](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcircuitmatrixinterface). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCircuitMatrixInterface_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryPreparedCircuitMatrixInterface_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary prepared circuit matrix interface n 3”. Concrete prepared-circuit matrix interface for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete prepared-circuit matrix interface for the focused 'n = 3' boundary branch. The prepared sparse matrix is now a Lean object. The active route remains blocked only on the raw-entry theorem identifying 'signalUnitaryEntry' with that prepared matrix's clean-clean entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20533](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarypreparedcircuitmatrixinterface-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActiveFullDim_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActiveFullDim_n3")
*Plain-English reading.* This abbreviation gives a shorter name to the type or expression used for “one term robin gamma 3 boundary active full dim n 3”. Full active matrix dimension for the focused 'n = 3' boundary packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Full active matrix dimension for the focused 'n = 3' boundary packet.

*Declaration kind.* abbrev.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20687](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivefulldim-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActiveCleanIndex_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActiveCleanIndex_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary active clean index n 3”. Clean active full-basis index for the focused signal-zero/system-zero entry.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Clean active full-basis index for the focused signal-zero/system-zero entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20692](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivecleanindex-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedEntryTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedEntryTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary active prepared entry target n 3”. Typed active-entry/prepared-entry target for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Typed active-entry/prepared-entry target for the focused boundary branch. The active entry is the current signal-zero entry from the seven-gate 'CircuitMatrixSemantics' product. The prepared entry is the clean-clean entry of the local sparse-register sandwich matrix. This target names the exact composition equality that is still missing; it does not prove that equality.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:20919](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivepreparedentrytarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryActivePreparedCompositionFieldTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryActivePreparedCompositionFieldTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary active prepared composition field target”. A proposition-valued field is a requirement until a constructor supplies it. Smallest prepared-composition field target now missing from the matrix backend.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest prepared-composition field target now missing from the matrix backend. The previous packet produced the prepared sparse-register matrix and proved its clean entry. This packet exposes the next field as a generic 'PreparedCircuitEntryTarget': relate the active seven-gate signal-zero entry to the clean entry of the prepared sandwich matrix. All theorem-facing flags stay false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21094](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivepreparedcompositionfieldtarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedCompositionFieldTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedCompositionFieldTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary active prepared composition field target n 3”. Concrete prepared-composition field target for the focused 'n = 3' boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete prepared-composition field target for the focused 'n = 3' boundary branch. This is the accepted fallback for the active-entry proof attempt: it is smaller than the previous interface because it uses the generic prepared-entry target and states the exact missing 'CircuitMatrixSemantics' composition field.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21131](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivepreparedcompositionfieldtarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedCompositeEvalStatement_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedCompositeEvalStatement_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary active prepared composite eval statement n 3”. Evaluation-level active/prepared composite entry statement.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Evaluation-level active/prepared composite entry statement. The active side is the signal-zero entry selected by Definition 'def:block-encoding'. The prepared side is the clean entry of the local singleton 'CircuitMatrixSemantics' object for 'H\_W^(kappa)^dagger \* U\_gamma3\_boundary \* H\_W^(kappa)'. This is not asserted by the current backend; it is the exact composition field still missing.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21547](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivepreparedcompositeevalstatement-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryUncastActivePreparedCompositeEvalStatement_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryUncastActivePreparedCompositeEvalStatement_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary uncast active prepared composite eval statement n 3”. Uncast active-entry form of the active/prepared singleton statement.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Uncast active-entry form of the active/prepared singleton statement. This removes the signal-system block wrapper and dimension cast from the fixed active/prepared target. The remaining equality is exactly the evaluated Fig. '1 term ROBIN' active entry '\[0,0\]' against the prepared singleton clean entry. It does not prove that equality.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21564](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryuncastactivepreparedcompositeevalstatement-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedSparseEvalStatement_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedSparseEvalStatement_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary active prepared sparse eval statement n 3”. Evaluation-level active/prepared sparse-matrix entry statement.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Evaluation-level active/prepared sparse-matrix entry statement. This is the same active entry compared directly with the prepared sparse matrix's clean-clean entry, bypassing the singleton 'evalGateMatrices' wrapper.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21659](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivepreparedsparseevalstatement-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryUncastPreparedSandwichEvalStatement_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryUncastPreparedSandwichEvalStatement_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary uncast prepared sandwich eval statement n 3”. Named evaluated target for the current prepared-sandwich equality.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Named evaluated target for the current prepared-sandwich equality. This is the right-hand side of 'oneTermRobinGamma3BoundaryUncastActivePreparedCompositeEval\_iff\_preparedSandwich\_n3': the active Fig. 'fig:1 term ROBIN' uncast '\[0,0\]' entry must evaluate to the prepared sandwich fold. The definition names the target only; it does not assert the equality.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21792](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryuncastpreparedsandwichevalstatement-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedCircuitLabels_distinct_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedCircuitLabels_distinct_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary active prepared circuit labels distinct n 3”; its local proof does not by itself complete the broader paper route. The active seven-gate circuit and the prepared singleton circuit have distinct gate labels.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The active seven-gate circuit and the prepared singleton circuit have distinct gate labels. This is a structural guard for the missing composition theorem: the prepared entry cannot be obtained by unfolding the active gate list.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21897](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivepreparedcircuitlabels-distinct-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryActivePreparedCircuitFieldTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryActivePreparedCircuitFieldTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary active prepared circuit field target”. A proposition-valued field is a requirement until a constructor supplies it. Circuit-semantics field target for the active/prepared clean-entry bridge.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Circuit-semantics field target for the active/prepared clean-entry bridge. Both sides now have concrete 'CircuitMatrixSemantics' objects: the active seven-gate Fig. 'fig:1 term ROBIN' semantics and the prepared singleton semantics for 'H\_W^(kappa)^dagger \* U \* H\_W^(kappa)'. The packet records the exact entry comparison still missing and the evaluation-level bridge to the prepared sparse matrix. It does not add an assumption and leaves every theorem-facing flag false.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21917](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivepreparedcircuitfieldtarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedCircuitFieldTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActivePreparedCircuitFieldTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary active prepared circuit field target n 3”. Concrete active/prepared circuit-semantics field target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete active/prepared circuit-semantics field target. This is the smallest current obstruction after the prepared singleton semantics packet: the prepared object is typed and its selected entry evaluates to the prepared sparse matrix, but QBE still lacks the composition theorem that identifies the active signal-zero entry with that prepared singleton entry.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:21963](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactivepreparedcircuitfieldtarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundarySourcePreparedProjectionTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundarySourcePreparedProjectionTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary source prepared projection target”. A proposition-valued field is a requirement until a constructor supplies it. Theorem-facing prepared projection target for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Theorem-facing prepared projection target for the focused boundary branch. The selected entry is the clean entry of the prepared singleton semantics for 'H\_W^(kappa)^dagger \* U\_gamma3\_boundary \* H\_W^(kappa)'. The active signal-zero entry remains a separate missing field; this target prevents the projection backend from silently treating the raw seven-gate entry as the source-prepared entry.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:22214](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysourcepreparedprojectiontarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedProjectionTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedProjectionTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary source prepared projection target n 3”. Concrete theorem-facing prepared projection target for 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete theorem-facing prepared projection target for 'n = 3'. It selects the prepared singleton clean entry and records the conditional evaluation bridge to the backend fold under the existing all-slot 'H\_W^(kappa)' clean-column contract. The active projection backend still needs a finite composition theorem before this target can close the H-free fold.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:22257](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysourcepreparedprojectiontarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedProjection_to_backendFold_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedProjection_to_backendFold_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary source prepared projection to backend fold n 3”; its local proof does not by itself complete the broader paper route. Named lower2 leaf from the source-prepared projection entry to the backend fold.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Named lower2 leaf from the source-prepared projection entry to the backend fold. This is only the source-prepared wrapper requested by the current projection/product packet. It consumes the explicit 'H\_W^(kappa)' clean-column contract through the existing target-level bridge and does not revive the H-free active row-'0' feeder or the refuted backend-expansion parent.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:22498](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysourcepreparedprojection-to-backendfold-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendFold_to_slot2ProjectedProduct_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendFold_to_slot2ProjectedProduct_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend fold to slot 2 projected product n 3”; its local proof does not by itself complete the broader paper route. Named lower2 bridge from the backend fold to the focused slot-'2' projected branch product.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Named lower2 bridge from the backend fold to the focused slot-'2' projected branch product. The proof composes only the compiled backend-fold collapse with the compiled selected-slot evaluator under the explicit boundary-entry convention. It does not use the rejected backend-expansion parent, the H-free evaluated fold, or the old selected-slot feeder.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:22521](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendfold-to-slot2projectedproduct-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedProjection_slot2_to_projectedBranchProduct_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedProjection_slot2_to_projectedBranchProduct_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary source prepared projection slot 2 to projected branch product n 3”; its local proof does not by itself complete the broader paper route. Named composite lower2 leaf from the source-prepared projection entry to the focused slot-'2' projected branch product.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Named composite lower2 leaf from the source-prepared projection entry to the focused slot-'2' projected branch product. This is only DAG wiring through the two compiled bridge leaves. The sparse preparation hypothesis enters through the source-prepared/backend-fold bridge, and the boundary-entry convention enters through the backend-fold/product bridge.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:22556](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysourcepreparedprojection-slot2-to-projectedbranchproduct-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryEvaluatedBackendFoldStatement_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryEvaluatedBackendFoldStatement_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary evaluated backend fold statement n 3”. Evaluation-level backend-fold statement for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Evaluation-level backend-fold statement for the focused boundary branch. This is the H-free form of the remaining projection theorem: after interpreting symbolic 'Coeff' terms in an environment, the active signal-zero entry must equal the seven-slot backend branch fold. It is weaker than the raw 'Coeff' equality and does not assert the missing finite projection theorem.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:22963](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryevaluatedbackendfoldstatement-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySelectedSlotContribution_allOne_nonzero_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySelectedSlotContribution_allOne_nonzero_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary selected slot contribution all one nonzero n 3”; its local proof does not by itself complete the broader paper route. Concrete obstruction witness for the retired all-environment H-free backend fold.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete obstruction witness for the retired all-environment H-free backend fold. Under an all-one environment for the selected branch symbols, the selected slot-'2' contribution evaluates to '1'. This formalizes the finite counterexample side of the current proof-DAG packet; it does not prove or use the retired row-'0' backend fold.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:23203](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryselectedslotcontribution-allone-nonzero-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActiveSelectedSlotIndexSplit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryActiveSelectedSlotIndexSplit_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary active selected slot index split n 3”; its local proof does not by itself complete the broader paper route. Index split for the active strict-feeder frontier.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Index split for the active strict-feeder frontier. The active 'evalGateMatrices' entry in the strict feeder is the signal-zero full-basis entry '\[0,0\]', while the selected backend contribution is the source slot-'2' branch at full basis index '32'. This is only a compiled calibration guard: it does not prove the feeder and it leaves the required projection/path-normal-form theorem open.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:23254](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryactiveselectedslotindexsplit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendExpansionStatement_not_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendExpansionStatement_not_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend expansion statement not n 3”; its local proof does not by itself complete the broader paper route. No-go guard for the current backend-expansion statement.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* No-go guard for the current backend-expansion statement. The all-one selected-branch environment makes the focused selected-slot contribution evaluate to '1', while any backend-expansion proof would force the same evaluated contribution to vanish through the evaluated backend fold.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:23644](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendexpansionstatement-not-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendProjectionSummationStatement_not_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryBackendProjectionSummationStatement_not_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary backend projection summation statement not n 3”; its local proof does not by itself complete the broader paper route. No-go guard for the generic projection-summation surface.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* No-go guard for the generic projection-summation surface. The generic 'BlockExtractionBranchContributionTarget.projectionSummationStatement' is equivalent to the backend-expansion statement for the current target. The unchanged backend-expansion route is already refuted by 'oneTermRobinGamma3BoundaryBackendExpansionStatement\_not\_n3', so this theorem records that the active lower target must be restated as a corrected source-backed branch statement before it can be proved.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:23688](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarybackendprojectionsummationstatement-not-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryEvaluatedBackendFoldTarget" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryEvaluatedBackendFoldTarget")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary evaluated backend fold target”. A proposition-valued field is a requirement until a constructor supplies it. Smallest current evaluated projection-backend target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Smallest current evaluated projection-backend target. The source-prepared target has selected the correct prepared singleton entry. This packet removes the matrix 'H' from the statement that still has to be proved: the active signal-zero entry must evaluate to the evaluated backend fold. The external clean-column contract is recorded only as the bridge needed to compare this H-free statement with the active/prepared singleton field.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:24133](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryevaluatedbackendfoldtarget). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryEvaluatedBackendFoldTarget_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryEvaluatedBackendFoldTarget_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary evaluated backend fold target n 3”. Concrete evaluated backend-fold target for 'n = 3'.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete evaluated backend-fold target for 'n = 3'. No semantic flag is promoted. The packet records that the remaining local theorem is an evaluated equality between the active signal-zero entry and the backend branch fold; a raw 'Coeff' proof would be stronger but is still absent.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:24165](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryevaluatedbackendfoldtarget-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundarySourcePreparedProductProjectionObligation" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundarySourcePreparedProductProjectionObligation")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary source prepared product projection obligation”. A proposition-valued field is a requirement until a constructor supplies it. Source-prepared product/projection proof-DAG packet for the focused boundary leaf.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Source-prepared product/projection proof-DAG packet for the focused boundary leaf. The packet starts from the clean projection of the full prepared sandwich '(H\_W^kappa)^dagger \* U\_gamma3\_boundary \* H\_W^kappa', reuses the compiled prepared-backend evaluator, and records the fixed product-to-coefficient obligation. It explicitly forbids the stale backend-expansion parent and does not consume the product route or promote any downstream theorem-facing flag.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:24938](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysourcepreparedproductprojectionobligation). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedProductProjectionObligation_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedProductProjectionObligation_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary source prepared product projection obligation n 3”. Concrete 'n = 3' source-prepared product/projection packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete 'n = 3' source-prepared product/projection packet. This is bookkeeping only: the prepared clean entry evaluator is compiled, but the slot-'2' projection/product bridge and normalizer algebra are still open.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:24962](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysourcepreparedproductprojectionobligation-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundarySourcePreparedNormalizedProjectionBridge" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundarySourcePreparedNormalizedProjectionBridge")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary source prepared normalized projection bridge”. A proposition-valued field is a requirement until a constructor supplies it. Source-prepared finite normalized-projection bridge packet for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Source-prepared finite normalized-projection bridge packet for the focused boundary branch. This is route bookkeeping. It attaches the source-prepared projection packet to the finite projection/product bridge and the finite block-composition contract for 'n = 3'. It does not prove the fixed product-to-coefficient obligation or promote any LCU, normalized-block, block, or extraction flag.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:25219](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysourcepreparednormalizedprojectionbridge). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedNormalizedProjectionBridge_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundarySourcePreparedNormalizedProjectionBridge_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary source prepared normalized projection bridge n 3”. Concrete 'n = 3' source-prepared finite normalized-projection packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete 'n = 3' source-prepared finite normalized-projection packet. The packet consumes only already compiled route memory: 'oneTermRobinGamma3BoundarySourcePreparedProductProjectionObligation\_n3', 'oneTermRobinGamma3BoundaryFiniteProjectionProductBridge\_n3', 'oneTermRobinFiniteBlockCompositionContract 3', and the conditional normalizer bridge by name. The root obligation remains false.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:25269](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarysourcepreparednormalizedprojectionbridge-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryTheoremFacingFiniteBlockContractAudit" (lean := "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinGamma3BoundaryTheoremFacingFiniteBlockContractAudit")
*Plain-English reading.* This record groups the data and proof fields needed for “one term robin gamma 3 boundary theorem facing finite block contract audit”. A proposition-valued field is a requirement until a constructor supplies it. Theorem-facing finite block-contract audit for the focused boundary branch.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Theorem-facing finite block-contract audit for the focused boundary branch. This packet records that the finite block-composition contract is still wired to the active seven-gate backend while the source-facing Fig. 4 transcript is a larger circuit. It is an audit object only: no normalized-block equality, LCU claim, block projection, final extraction, oracle correctness, unitarity, resource claim, or product-to-coefficient flag is promoted.

*Declaration kind.* structure.

Source: [QuantumBlockEncoding/RobinMatrix.lean:25426](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarytheoremfacingfiniteblockcontractaudit). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryTheoremFacingFiniteBlockContractAudit_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryTheoremFacingFiniteBlockContractAudit_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary theorem facing finite block contract audit n 3”. Concrete 'n = 3' theorem-facing finite block-contract audit packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete 'n = 3' theorem-facing finite block-contract audit packet. The packet consumes only existing transcript guards and compiled route memory. It records the source-translation gap between the theorem-facing Fig. 4 circuit and the active backend currently used by 'oneTermRobinFiniteBlockCompositionContract 3'.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:25484](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarytheoremfacingfiniteblockcontractaudit-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::definition "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryTheoremFacingFiniteBlockProjectionInterface_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryTheoremFacingFiniteBlockProjectionInterface_n3")
*Plain-English reading.* This definition gives the library's named construction or computation for “one term robin gamma 3 boundary theorem facing finite block projection interface n 3”. Concrete 'n = 3' theorem-facing finite block/projection interface packet.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Concrete 'n = 3' theorem-facing finite block/projection interface packet. The packet records that the source-prepared projection target is the clean prepared entry, while the finite block-composition contract still consumes 'oneTermRobinCircuitSemantics 3'. It does not substitute the Fig. 4 circuit for the active backend and does not prove the root product-to-coefficient obligation.

*Declaration kind.* def.

Source: [QuantumBlockEncoding/RobinMatrix.lean:25726](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarytheoremfacingfiniteblockprojectioninterface-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryEvaluatedBackendFoldStatement_diagnostic_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryEvaluatedBackendFoldStatement_diagnostic_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary evaluated backend fold statement diagnostic n 3”; its local proof does not by itself complete the broader paper route. Diagnostic/H-free route: the evaluated backend fold follows from the raw Coeff equality 'signalUnitaryEntry = blockExtractionBranchContributionSum' via the bridge theorem.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* Diagnostic/H-free route: the evaluated backend fold follows from the raw Coeff equality 'signalUnitaryEntry = blockExtractionBranchContributionSum' via the bridge theorem. This is not the source-correct route; the source-correct route goes through 'oneTermRobinGamma3BoundaryEvaluatedBackendFoldStatement\_of\_activePreparedEval\_n3'.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:26934](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryevaluatedbackendfoldstatement-diagnostic-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryUnitaryEntry_ne_backendFold_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryUnitaryEntry_ne_backendFold_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary unitary entry ne backend fold n 3”; its local proof does not by itself complete the broader paper route. The historical H-free raw fold is false for the current symbolic target.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The historical H-free raw fold is false for the current symbolic target. This closes the old diagnostic route by rejection rather than by an axiom. It combines the compiled equivalence to the backend-expansion statement with the explicit all-one counterexample above. The source-prepared route remains a separate conditional interface and is never allowed to reuse this rejected parent.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:26952](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundaryunitaryentry-ne-backendfold-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::

:::theorem "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryGateMatrixList_n3" (lean := "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinGamma3BoundaryGateMatrixList_n3")
*Plain-English reading.* Lean checks the research-module proposition indexed as “one term robin gamma 3 boundary gate matrix list n 3”; its local proof does not by itself complete the broader paper route. The seven active gate matrices have the exact paper-facing order recorded by the circuit semantics layer.

*Formal status.* Compiled by the full ASPBE gate in a research-level module. The displayed theorem is checked, but it does not promote a broader paper route or an external oracle contract.

*Why it is in this chapter.* Compiled Robin-matrix research included in the full ASPBE gate; local results are separated from the broader paper route and external contracts.

*Technical source note.* The seven active gate matrices have the exact paper-facing order recorded by the circuit semantics layer. The project-local symbolic 'Coeff' matrix multiplication stores syntax trees, so differently parenthesized products are not definitionally equal. This structural theorem is the correct raw certificate; algebraic regrouping must be stated after 'Coeff.evalWith', where rational associativity is available.

*Declaration kind.* theorem.

Source: [QuantumBlockEncoding/RobinMatrix.lean:26970](../../../../library/modules/robinmatrix/#decl-quantumblockencoding-examples-robinheat-onetermrobingamma3boundarygatematrixlist-n3). A commit-pinned external link is added by the publication build when the source exists at the published ref.
:::
