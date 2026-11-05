# C20 internal complex saved-stage transport — statement seal

Author identity: /root/literal_complex_review_c18, now acting as author only. This is a NEW C_INTERNAL_PROVIDER; the C18 independent review remains frozen. No self-review credit, production admission or scientific ROOT claim.

Frozen literal inputs: SavedStageInterpreter.Instruction width (rational RY physical angle and CX control,target,distinct), intervalWord from intervalIdentity, stageCenter entrywise rational midpoint, stageEta = 2^width * actual max entry radius. Existing compileInstruction/compileWord and primitiveBasisLEEquiv are reused unchanged. No substituted circuit, assumed error witness, new semantic carrier or discarded terminal sector.

Stage carrier: `EuclideanSpace ℂ (PrimitiveBasis width)`. Nominal matrix: ACTUAL `evalPrimitiveCircuit (compileWord word)`. Surrogate matrix: ACTUAL `namedCast (stageCenter word degree bits)` (literal real-to-complex inclusion reindexed by existing q0LSB equivalence). Error: ACTUAL `(stageEta word degree bits : ℝ)`.

Sealed final interfaces (namespace HermiteComplexStageTransport):

```lean
theorem stage_operator_error {width : ℕ} (word : List (Instruction width))
    (degree bits : ℕ) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (namedCast (stageCenter word degree bits) -
        evalPrimitiveCircuit (compileWord word))‖ ≤ (stageEta word degree bits : ℝ)

theorem nominal_contraction {width : ℕ} (word : List (Instruction width)) :
    ‖Matrix.toEuclideanCLM (𝕜 := ℂ)
      (evalPrimitiveCircuit (compileWord word))‖ ≤ 1

theorem actual_stages_valid {width : ℕ} (words : List (List (Instruction width)))
    (degree bits : ℕ) : Valid (actualStages words degree bits)

theorem nominalProduct_eq_flatten {width : ℕ}
    (words : List (List (Instruction width))) (degree bits : ℕ) :
    nominalProduct (actualStages words degree bits) =
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten))

theorem actual_flatten_product_error {width : ℕ}
    (words : List (List (Instruction width))) (degree bits : ℕ) :
    ‖surrogateProduct (actualStages words degree bits) -
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten))‖ ≤
      growth (actualStages words degree bits) - 1

theorem actual_flatten_apply_error {width : ℕ}
    (words : List (List (Instruction width))) (degree bits : ℕ)
    (x : EuclideanSpace ℂ (PrimitiveBasis width)) :
    ‖surrogateProduct (actualStages words degree bits) x -
      Matrix.toEuclideanCLM (𝕜 := ℂ)
        (evalPrimitiveCircuit (compileWord words.flatten)) x‖ ≤
      (growth (actualStages words degree bits) - 1) * ‖x‖
```

Binder audit: width is TYPING; word/words, degree/bits and arbitrary complex x are literal contract data (SOURCE original internal contract). CX distinctness is inherited from the actual instruction. Public roots accept NO Valid, contraction, operator equality, error bound, normalization, clean sector, real-vector restriction or source correctness premise. EXCESS = none. Internal generic matrix lemmas may take an entry-radius bound, which must be discharged from actual stage suppliers inside these roots.

Definition audit: all stage fields and map operations are literal; no quotient/phase equivalence, representative choice or fallback. The complete terminal carrier, all spectator patterns and garbage sectors remain present. Width zero retains one basis coordinate and empty instruction words. Chronological list evaluation remains later-left multiplication; angles retain their signed theta/2 convention.

Source/construction topology: actual midpoint enclosure AND C18 exact evaluator identification AND existing q0LSB reindexing => complex entry norm error; triangle inequality AND finite real Cauchy–Schwarz AND complex Euclidean norm-square identity => complex induced operator bound N*r=stageEta. Existing primitive unitarity => nominal contraction. Error nonnegativity from actual enclosing intervals AND operator bound AND contraction => internally derived Valid. Existing nonunitary product theorem AND actual circuit append/flatten identity => chronological product/apply growth bound. Entrywise error is an ingredient, never the final norm.

Excluded/open: full QR, finite-bit implementation/runtime, physical-local/global support lift, uniform family error/resource budget, scientific X2/ROOT, independent C20 review, repository/site integration and purification. These remain separate obligations.

Method fingerprint: actual-complex-entry-enclosure; arbitrary-complex-CS; canonical-unitary-nominal; chronological-nonunitary-growth. Expected information gain: close complex actual-stage precision/flatten interface without a conditional validity premise. No subagents.
