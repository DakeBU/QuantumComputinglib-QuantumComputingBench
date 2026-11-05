import QuantumBlockEncoding.BlockEncodingClassics
import Mathlib.NumberTheory.SumFourSquares

/-!
# Cubic grid state-preparation operator benchmark

This module records task `QBE-OP-CUBIC-STATEPREP-001`.

The user-facing statement

`O |0^n> = sum_j (j / 2^n)^3 |j>`

does not define a unitary state-preparation map, because the right hand side is
not normalized in general.  ABEIS therefore fixes the operator target as the
rank-one map `O_n = |v_n><0^n|`, where `v_n[j] = (j / 2^n)^3`.  A block
encoding may use any explicit normalizer.  Exact finite gate synthesis is not
expected to be the useful route for this target; the task is configured to
enter approximate search with tolerance `1e-10` when exact search stalls.
-/

namespace QuantumBlockEncoding
namespace CubicStatePreparation

/-- Task identifier used by the retrieval and verifier ledgers. -/
def taskId : String := "QBE-OP-CUBIC-STATEPREP-001"

/-- User-requested error tolerance `1e-10`. -/
def requestedEpsilon : Rat := (1 : Rat) / 10000000000

/-- Grid point `x_j = j / 2^n`. -/
def gridPoint (n : Nat) (j : Fin (gridSize n)) : Rat :=
  (j.val : Rat) / (gridSize n : Rat)

/-- Cubic amplitude `f(x_j) = x_j^3`. -/
def cubicAmplitude (n : Nat) (j : Fin (gridSize n)) : Rat :=
  (gridPoint n j) ^ 3

/--
The rank-one operator `O_n = |v_n><0^n|`.  In column-vector convention this
maps the input basis state `|0^n>` to the unnormalized vector with entries
`(j / 2^n)^3`, and maps every other input basis state to zero.
-/
def cubicOperator (n : Nat) : Matrix (gridSize n) (gridSize n) Rat :=
  fun row col => if col.val = 0 then cubicAmplitude n row else 0

/--
Exact rational squared norm of the unnormalized target vector.  The analytic
normalizer is its square root; this rational quantity is the cheap diagnostic
used before any approximate rotation-synthesis route is accepted.
-/
def cubicNormSq (n : Nat) : Rat :=
  (List.finRange (gridSize n)).foldl
    (fun acc j => acc + cubicAmplitude n j ^ 2) 0

/--
A conservative rational normalizer.  It is not intended to be optimal; it is a
stable placeholder until the approximate synthesis backend proves a sharper
normalizer and error bound.
-/
def conservativeNormalizer (n : Nat) : Rat :=
  (gridSize n : Rat)

/-- Operator-first target record used by the ABEIS harness. -/
def cubicTarget (n : Nat) : QueryOperatorTarget Rat (gridSize n) (gridSize n) where
  operator := cubicOperator n
  normalizer := conservativeNormalizer n
  source := "QBE-OP-CUBIC-STATEPREP-001: O_n = |v_n><0^n|, v_j=(j/2^n)^3"
  semanticContract :=
    "rank-one unnormalized cubic grid state-preparation operator; approximate BE target epsilon=1e-10"
  freeParameters := [
    "n positive",
    "epsilon = 1e-10",
    "exact search first, then Scenario 2 approximate arithmetic synthesis"
  ]

/-- Resource floor used for the first Scenario 2 run. -/
def defaultRequiredCost : BlockEncodingCost where
  auxiliaryQubits := 4
  gateCount := 0
  depth := 0
  oracleCalls := 0

/--
Adaptive search policy for the cubic benchmark.  The zero gate/depth fields in
`defaultRequiredCost` deliberately mean "discover a concrete candidate and then
rank it"; the active search is expected to relax from exact to approximate
construction after a small exact-search stall window.
-/
def defaultPolicy : AdaptiveBlockEncodingPolicy Rat where
  maxExactIterations := 2
  exactStallIterations := 1
  requiredCost := defaultRequiredCost
  requestedEpsilon := requestedEpsilon
  allowRelaxedEpsilon := true
  maxUpperAgents := 4
  maxMiddleAgents := 5
  maxLowerAgents := 8

/-- First arithmetic-route precision seed for Scenario 2. -/
def arithmeticCubicDefaultPrecision : Nat := 40

/--
Register layout for the first arithmetic-transduction candidate route.

The single signal qubit is the clean block selector.  The pure workspace keeps
an address copy, reversible square/cube work registers, and fixed-point
precision workspace.  This is a candidate interface only; it does not certify
the arithmetic or rotation subroutines.
-/
def arithmeticCubicLayout (n precision : Nat) : RegisterLayout where
  systemQubits := n
  signalQubits := 1
  pureAncillas := 3 * n + precision + 2

/--
Oracle-level transcript for the scalable cubic route.

The clean branch is intended to compute `j / 2^n`, reversibly form the cubic
fixed-point amplitude, apply one amplitude-transduction rotation, and uncompute
the arithmetic workspace.  Each label remains a semantic proof obligation.
-/
def arithmeticCubicCircuit (_n _precision : Nat) : Circuit :=
  [ Gate.oracleCall "cubic-load-j-over-2^n"
  , Gate.oracleCall "cubic-square-fixed-point"
  , Gate.oracleCall "cubic-multiply-by-x"
  , Gate.oracleCall "cubic-amplitude-transduction-Ry"
  , Gate.oracleCall "(cubic-multiply-by-x)^dagger"
  , Gate.oracleCall "(cubic-square-fixed-point)^dagger"
  , Gate.oracleCall "(cubic-load-j-over-2^n)^dagger"
  ]

/-- Local resource count for the unexpanded oracle-level transcript. -/
def arithmeticCubicResource (n precision : Nat) : Resource :=
  (arithmeticCubicCircuit n precision).resource

/-- Normalizer used by the first arithmetic-transduction route. -/
def arithmeticCubicNormalizer (n : Nat) : Rat :=
  conservativeNormalizer n

/-- Candidate score extracted from the arithmetic-route layout and transcript. -/
def arithmeticCubicCost (n precision : Nat) : BlockEncodingCost :=
  BlockEncodingCost.fromLayoutAndResource
    (arithmeticCubicLayout n precision)
    (arithmeticCubicResource n precision)

/-- Resource tuple in QBE candidate-population order. -/
def arithmeticCubicResourceTuple (n precision : Nat) : Nat × Nat × Nat × Nat :=
  ( (arithmeticCubicCost n precision).gateCount
  , (arithmeticCubicCost n precision).depth
  , (arithmeticCubicCost n precision).auxiliaryQubits
  , (arithmeticCubicCost n precision).oracleCalls
  )

/-- The oracle-level transcript has seven unresolved calls and depth seven. -/
theorem arithmeticCubicResource_eq (n precision : Nat) :
    arithmeticCubicResource n precision =
      Resource.ofCountsWithDepth 0 0 7 0 7 := by
  rfl

/-- The first arithmetic route records one signal qubit plus pure workspace. -/
theorem arithmeticCubicLayout_auxiliaryQubits (n precision : Nat) :
    (arithmeticCubicLayout n precision).auxiliaryQubits =
      1 + (3 * n + precision + 2) := by
  rfl

/--
Human-facing construction claim for the first scalable route.  This claim is an
unproved candidate record, not a certified block encoding.
-/
def arithmeticCubicClaim : ConstructionClaim where
  name := "arithmetic-cubic-amplitude-transduction"
  source := "QBE-OP-CUBIC-STATEPREP-001 exploratory candidate CUBIC-CAND-001"
  target := "O_n = |v_n><0^n|, v_n[j] = (j / 2^n)^3"
  normalization := "alpha = conservativeNormalizer n"
  layout := "one signal qubit plus 3*n + precision + 2 pure arithmetic ancillas"
  resource := {
    gates :=
      CostExpr.atom "poly(n, precision)" +
      CostExpr.atom "rotation_synthesis(precision)"
    pureAncilla :=
      (3 : CostExpr) * CostExpr.atom "n" + CostExpr.atom "precision" + 2
  }

/--
Rank-one wrapper layout for the arithmetic cubic route.

The extra pure workspace is reserved for a zero-input filter and row-generation
wrapper.  This is still an oracle-level interface: it repairs the register
shape of the candidate transcript, but it does not certify the wrapper
semantics.
-/
def arithmeticRankOneCubicLayout (n precision : Nat) : RegisterLayout where
  systemQubits := n
  signalQubits := 1
  pureAncillas := (arithmeticCubicLayout n precision).pureAncillas + n + 1

/--
Rank-one candidate transcript around the arithmetic middle block.

The first two calls are the missing wrapper from `CUBIC-CAND-SHAPE-001`: reject
nonzero input columns from the clean branch, then generate the output row
register on the zero-input branch.  The final call is a placeholder cleanup for
the zero-input filter.  The row-generation step is intentionally not uncomputed,
because the output row is the system output of the rank-one operator.
-/
def arithmeticRankOneCubicCircuit (n precision : Nat) : Circuit :=
  [ Gate.oracleCall "rank-one-zero-input-clean-filter"
  , Gate.oracleCall "rank-one-row-generation-on-zero-input"
  ] ++
  arithmeticCubicCircuit n precision ++
  [ Gate.oracleCall "rank-one-zero-input-filter-cleanup" ]

/-- Oracle-level resource count for the rank-one wrapped transcript. -/
def arithmeticRankOneCubicResource (n precision : Nat) : Resource :=
  (arithmeticRankOneCubicCircuit n precision).resource

/-- Normalizer used by the rank-one wrapped arithmetic route. -/
def arithmeticRankOneCubicNormalizer (n : Nat) : Rat :=
  arithmeticCubicNormalizer n

/-- Candidate score for the rank-one wrapped arithmetic route. -/
def arithmeticRankOneCubicCost (n precision : Nat) : BlockEncodingCost :=
  BlockEncodingCost.fromLayoutAndResource
    (arithmeticRankOneCubicLayout n precision)
    (arithmeticRankOneCubicResource n precision)

/-- Resource tuple in QBE candidate-population order for the wrapped route. -/
def arithmeticRankOneCubicResourceTuple (n precision : Nat) :
    Nat × Nat × Nat × Nat :=
  ( (arithmeticRankOneCubicCost n precision).gateCount
  , (arithmeticRankOneCubicCost n precision).depth
  , (arithmeticRankOneCubicCost n precision).auxiliaryQubits
  , (arithmeticRankOneCubicCost n precision).oracleCalls
  )

/-- The rank-one wrapper adds three oracle-level calls to the middle block. -/
theorem arithmeticRankOneCubicResource_eq (n precision : Nat) :
    arithmeticRankOneCubicResource n precision =
      Resource.ofCountsWithDepth 0 0 10 0 10 := by
  rfl

/-- Auxiliary qubits for the wrapped route include the zero-test workspace. -/
theorem arithmeticRankOneCubicLayout_auxiliaryQubits (n precision : Nat) :
    (arithmeticRankOneCubicLayout n precision).auxiliaryQubits =
      1 + ((arithmeticCubicLayout n precision).pureAncillas + n + 1) := by
  rfl

/-- Default small diagnostic score for the wrapped route at `n = 2`, `p = 40`. -/
theorem arithmeticRankOneCubicResourceTuple_n2_default :
    arithmeticRankOneCubicResourceTuple 2 arithmeticCubicDefaultPrecision =
      (10, 10, 52, 10) := by
  decide +kernel

/--
Human-facing construction claim for the rank-one wrapped scalable route.  This
still records obligations, not a verified block-encoding certificate.
-/
def arithmeticRankOneCubicClaim : ConstructionClaim where
  name := "rank-one-arithmetic-cubic-amplitude-transduction"
  source := "QBE-OP-CUBIC-STATEPREP-001 exploratory candidate CUBIC-CAND-SHAPE-001"
  target := "O_n = |v_n><0^n|, v_n[j] = (j / 2^n)^3"
  normalization := "alpha = conservativeNormalizer n"
  layout := "one signal qubit plus arithmetic workspace, zero-input filter, and row-generation workspace"
  resource := {
    gates :=
      CostExpr.atom "zero_input_filter(n)" +
      CostExpr.atom "row_generation(n, precision)" +
      CostExpr.atom "poly(n, precision)" +
      CostExpr.atom "rotation_synthesis(precision)"
    pureAncilla :=
      (4 : CostExpr) * CostExpr.atom "n" + CostExpr.atom "precision" + 3
  }

/--
Workspace seed for the Hadamard-counting mutation.

This is an oracle-level interface budget for the reversible cube/comparator
workspace.  It is not a gate-level implementation of multiplication.
-/
def hadamardCountingCubicWorkspace (n : Nat) : Nat :=
  4 * n + 3

/--
Register layout for the exact Hadamard-counting candidate.

The signal qubit is the reject flag.  Pure ancillas are the nonzero-input flag,
the `R,T` path registers of total width `4*n`, and the reversible
cube/comparator workspace.  Nonzero input columns set the reject signal before
the `nz` cleanup, so the clean projection cannot leak identity entries.
-/
def hadamardCountingCubicLayout (n : Nat) : RegisterLayout where
  systemQubits := n
  signalQubits := 1
  pureAncillas := 1 + 4 * n + hadamardCountingCubicWorkspace n

/--
Oracle-level transcript for the Hadamard-counting route.

The row XOR is not uncomputed, because it writes the output system row for the
rank-one operator.  The separate nonzero-column reject signal is applied before
the `nz` cleanup, so nonzero input columns keep a clean-projection rejection
witness.  The Hadamard layers and reversible arithmetic are still semantic
obligations at this interface tier.
-/
def hadamardCountingCubicCircuit (_n : Nat) : Circuit :=
  [ Gate.oracleCall "hcount-zero-input-flag"
  , Gate.oracleCall "hcount-nonzero-column-reject"
  , Gate.oracleCall "hcount-path-H-on-R-T"
  , Gate.oracleCall "hcount-row-xor-R-into-system"
  , Gate.oracleCall "hcount-cubic-threshold-compare"
  , Gate.oracleCall "(hcount-cubic-threshold-compare)^dagger"
  , Gate.oracleCall "hcount-path-H-on-R-T"
  , Gate.oracleCall "(hcount-zero-input-flag)^dagger"
  ]

/--
The repaired transcript records a separate nonzero-column reject signal before
the final `nz` cleanup.  This is the compiled surface for
`CUBIC-HCOUNT-REJECT-REPAIR-001`; semantic clean-block correctness remains a
future proof leaf.
-/
theorem hadamardCountingCubicCircuit_rejectSignalRepair (n : Nat) :
    hadamardCountingCubicCircuit n =
      [ Gate.oracleCall "hcount-zero-input-flag"
      , Gate.oracleCall "hcount-nonzero-column-reject"
      , Gate.oracleCall "hcount-path-H-on-R-T"
      , Gate.oracleCall "hcount-row-xor-R-into-system"
      , Gate.oracleCall "hcount-cubic-threshold-compare"
      , Gate.oracleCall "(hcount-cubic-threshold-compare)^dagger"
      , Gate.oracleCall "hcount-path-H-on-R-T"
      , Gate.oracleCall "(hcount-zero-input-flag)^dagger"
      ] := by
  rfl

/-- Oracle-level resource count for the Hadamard-counting route. -/
def hadamardCountingCubicResource (n : Nat) : Resource :=
  (hadamardCountingCubicCircuit n).resource

/-- Normalizer used by the Hadamard-counting route. -/
def hadamardCountingCubicNormalizer (n : Nat) : Rat :=
  conservativeNormalizer n

/-- Candidate score for the Hadamard-counting route. -/
def hadamardCountingCubicCost (n : Nat) : BlockEncodingCost :=
  BlockEncodingCost.fromLayoutAndResource
    (hadamardCountingCubicLayout n)
    (hadamardCountingCubicResource n)

/-- Resource tuple in QBE candidate-population order. -/
def hadamardCountingCubicResourceTuple (n : Nat) : Nat × Nat × Nat × Nat :=
  ( (hadamardCountingCubicCost n).gateCount
  , (hadamardCountingCubicCost n).depth
  , (hadamardCountingCubicCost n).auxiliaryQubits
  , (hadamardCountingCubicCost n).oracleCalls
  )

/-- The Hadamard-counting interface has eight unresolved oracle-level calls. -/
theorem hadamardCountingCubicResource_eq (n : Nat) :
    hadamardCountingCubicResource n =
      Resource.ofCountsWithDepth 0 0 8 0 8 := by
  rfl

/-- Auxiliary qubits for the counting route include reject, `nz`, path, and workspace registers. -/
theorem hadamardCountingCubicLayout_auxiliaryQubits (n : Nat) :
    (hadamardCountingCubicLayout n).auxiliaryQubits =
      1 + (1 + 4 * n + hadamardCountingCubicWorkspace n) := by
  rfl

/-- Default small diagnostic score for the counting route at `n = 2`. -/
theorem hadamardCountingCubicResourceTuple_n2 :
    hadamardCountingCubicResourceTuple 2 = (8, 8, 21, 8) := by
  decide +kernel

/--
Human-facing construction claim for the Hadamard-counting exact route.  This is
an unproved candidate record, not a certified block encoding.
-/
def hadamardCountingCubicClaim : ConstructionClaim where
  name := "hadamard-counting-cubic-rank-one"
  source := "QBE-OP-CUBIC-STATEPREP-001 exploratory candidate CUBIC-HCOUNT-IFACE-001"
  target := "O_n = |v_n><0^n|, v_n[j] = (j / 2^n)^3"
  normalization := "alpha = conservativeNormalizer n"
  layout := "one reject signal qubit plus nz flag, 4*n path qubits, and reversible cube/comparator workspace"
  resource := {
    gates :=
      CostExpr.atom "path_hadamards(4*n)" +
      CostExpr.atom "zero_input_test(n)" +
      CostExpr.atom "nonzero_column_reject(n)" +
      CostExpr.atom "row_xor(n)" +
      CostExpr.atom "cube_compare(n)"
    pureAncilla :=
      (8 : CostExpr) * CostExpr.atom "n" + 4
  }

/--
Hard Mode panel escalation schedule. The four entries are the planned
parallel-agent counts for levels 0 through 3. Upper agents should only move to
the next level after the active proof leaf has stalled and the reviewer has
confirmed that the blocker is not just stale memory.
-/
def hardModeUpperAgentSchedule : List Nat := [1, 2, 3, 4]

def hardModeMiddleAgentSchedule : List Nat := [1, 2, 3, 4]

def hardModeLowerAgentSchedule : List Nat := [3, 4, 5, 6]

/-- Number of consecutive cycles without a closed leaf before the first escalation. -/
def hardModeExactStallWindow : Nat := 1

/--
Number of consecutive cycles without an improving certified or finite
candidate before the next Hard Mode level is considered.
-/
def hardModeConstructionStallWindow : Nat := 1

/-- Per-level cycle budgets before the upper panel must explicitly review progress. -/
def hardModeLevelCycleBudget : List Nat := [1, 1, 1, 1]

/--
Scenario 2 epsilon ladder.  The first entry is the user-requested tolerance.
Later entries are relaxed exploratory waypoints used only if the exact or
requested-epsilon search stalls; a relaxed waypoint is not a substitute for a
certificate at `requestedEpsilon`.
-/
def relaxedEpsilonLadder : List Rat :=
  [requestedEpsilon, (1 : Rat) / 100000000, (1 : Rat) / 1000000]

theorem relaxedEpsilonLadder_startsWithRequested :
    relaxedEpsilonLadder.head? = some requestedEpsilon := by
  rfl

theorem hardModeSchedules_have_four_levels :
    hardModeUpperAgentSchedule.length = 4 ∧
    hardModeMiddleAgentSchedule.length = 4 ∧
    hardModeLowerAgentSchedule.length = 4 ∧
    hardModeLevelCycleBudget.length = 4 := by
  decide +kernel

theorem hardModeLowerAgentSchedule_final :
    hardModeLowerAgentSchedule.getLast? = some 6 := by
  decide +kernel

/--
Current expected phase.  This is a planning declaration, not a proof of
impossibility: it records that exact finite gate synthesis should not consume
the full budget before approximate arithmetic/state-preparation search starts.
-/
def initialExpectedPhase : BlockEncodingSearchPhase :=
  BlockEncodingSearchPhase.relaxedApproxSearch

theorem gridSize_pos (n : Nat) : 0 < gridSize n := by
  simpa [gridSize] using (Nat.pow_pos (by decide : 0 < 2) : 0 < 2 ^ n)

theorem cubicOperator_first_column (n : Nat) (row : Fin (gridSize n)) :
    cubicOperator n row ⟨0, gridSize_pos n⟩ = cubicAmplitude n row := by
  simp [cubicOperator]

theorem cubicOperator_only_first_column (n : Nat)
    (row col : Fin (gridSize n)) (h : col.val ≠ 0) :
    cubicOperator n row col = 0 := by
  simp [cubicOperator, h]

/--
Entrywise clean-block contract for a rank-one cubic candidate.

The first field states the scaled clean first column.  The second field states
that all other input columns vanish in the clean block.  This is a semantic
obligation for a future unitary/circuit proof, not a proof that the current
oracle labels already realize the contract.
-/
def rankOneCleanBlockContract (n : Nat) (alpha : Rat)
    (block : Matrix (gridSize n) (gridSize n) Rat) : Prop :=
  (∀ row : Fin (gridSize n),
      alpha * block row ⟨0, gridSize_pos n⟩ = cubicAmplitude n row) ∧
  (∀ row col : Fin (gridSize n), col.val ≠ 0 → block row col = 0)

/-- Candidate-specific clean-block contract for the repaired rank-one route. -/
def arithmeticRankOneCubicCleanBlockContract (n : Nat)
    (block : Matrix (gridSize n) (gridSize n) Rat) : Prop :=
  rankOneCleanBlockContract n (arithmeticRankOneCubicNormalizer n) block

/--
The rank-one clean-block contract is exactly the target matrix, entry by entry,
after multiplying by its normalizer.
-/
theorem rankOneCleanBlockContract_pointwise_eq {n : Nat} {alpha : Rat}
    {block : Matrix (gridSize n) (gridSize n) Rat}
    (h : rankOneCleanBlockContract n alpha block) :
    Matrix.PointwiseEq
      (fun row col => alpha * block row col)
      (cubicOperator n) := by
  intro row col
  by_cases hcol : col.val = 0
  · have hcolZero : col = ⟨0, gridSize_pos n⟩ := by
      apply Fin.ext
      exact hcol
    subst col
    simpa [cubicOperator] using h.1 row
  · have hzero := h.2 row col hcol
    simp [cubicOperator, hcol, hzero]

/--
Candidate-specific bridge from the repaired wrapper's clean-block contract to
the fixed cubic target.
-/
theorem arithmeticRankOneCubicCleanBlockContract_pointwise_eq {n : Nat}
    {block : Matrix (gridSize n) (gridSize n) Rat}
    (h : arithmeticRankOneCubicCleanBlockContract n block) :
    Matrix.PointwiseEq
      (fun row col => arithmeticRankOneCubicNormalizer n * block row col)
      (cubicOperator n) :=
  rankOneCleanBlockContract_pointwise_eq h

/-- Candidate-specific clean-block contract for the Hadamard-counting route. -/
def hadamardCountingCubicCleanBlockContract (n : Nat)
    (block : Matrix (gridSize n) (gridSize n) Rat) : Prop :=
  rankOneCleanBlockContract n (hadamardCountingCubicNormalizer n) block

/--
Candidate-specific bridge from the Hadamard-counting clean-block contract to
the fixed cubic target.
-/
theorem hadamardCountingCubicCleanBlockContract_pointwise_eq {n : Nat}
    {block : Matrix (gridSize n) (gridSize n) Rat}
    (h : hadamardCountingCubicCleanBlockContract n block) :
    Matrix.PointwiseEq
      (fun row col => hadamardCountingCubicNormalizer n * block row col)
      (cubicOperator n) :=
  rankOneCleanBlockContract_pointwise_eq h

theorem rat_cube_sq_eq_sixth (x : Rat) : (x ^ 3) ^ 2 = x ^ 6 := by
  apply Rat.ext
  · change (x.num ^ 3) ^ 2 = x.num ^ 6
    rw [← Int.pow_mul]
  · change (x.den ^ 3) ^ 2 = x.den ^ 6
    rw [← Nat.pow_mul]

theorem cubicAmplitude_sq_eq_gridPoint_sixth (n : Nat)
    (j : Fin (gridSize n)) :
    cubicAmplitude n j ^ 2 = gridPoint n j ^ 6 := by
  simpa [cubicAmplitude] using rat_cube_sq_eq_sixth (gridPoint n j)

theorem cubicNormSq_sixthPowerFold (n : Nat) :
    cubicNormSq n =
      (List.finRange (gridSize n)).foldl
        (fun acc j => acc + gridPoint n j ^ 6) 0 := by
  simp [cubicNormSq, cubicAmplitude_sq_eq_gridPoint_sixth]

/-- The rational grid dimension is nonzero, for denominator side conditions. -/
theorem gridSize_rat_ne_zero (n : Nat) : (gridSize n : Rat) ≠ 0 := by
  intro h
  exact Nat.ne_of_gt (gridSize_pos n) (Rat.natCast_eq_zero_iff.mp h)

/-- The rational grid dimension is positive. -/
theorem gridSize_rat_pos (n : Nat) : (0 : Rat) < (gridSize n : Rat) := by
  rw [Rat.natCast_pos]
  exact gridSize_pos n

/-- Core rational normalization for the Hadamard-counting path ratio. -/
theorem rat_div_cube_div_eq (a b : Rat) :
    (a / b) ^ 3 / b = a ^ 3 / b ^ 4 := by
  simp [Rat.div_def, Rat.pow_succ, Rat.inv_mul_rev, Rat.mul_assoc]
  grind [Rat.mul_comm, Rat.mul_assoc]

/--
Arithmetic bridge for the Hadamard-counting path formula.

After scaling by `alpha = conservativeNormalizer n = gridSize n`, the candidate
clean-block entry `j^3 / gridSize^4` recovers the cubic target amplitude.
-/
theorem cubicAmplitude_div_conservativeNormalizer_eq (n : Nat)
    (j : Fin (gridSize n)) :
    cubicAmplitude n j / conservativeNormalizer n =
      (j.val : Rat) ^ 3 / (gridSize n : Rat) ^ 4 := by
  simpa [cubicAmplitude, gridPoint, conservativeNormalizer] using
    rat_div_cube_div_eq (j.val : Rat) (gridSize n : Rat)

/-- Path-register capacity identity for the Hadamard-counting route. -/
theorem gridSize_three_mul_eq_cube (n : Nat) :
    gridSize (3 * n) = gridSize n ^ 3 := by
  rw [Nat.mul_comm 3 n]
  simp [gridSize, Nat.pow_mul]

/-- Four-register path-space identity for the Hadamard-counting denominator. -/
theorem gridSize_four_mul_eq_fourth (n : Nat) :
    gridSize (4 * n) = gridSize n ^ 4 := by
  rw [Nat.mul_comm 4 n]
  simp [gridSize, Nat.pow_mul]

/--
Reusable threshold count over `List.finRange`.

If the threshold `k` fits in an `m`-element register, exactly `k` entries of
`List.finRange m` have value strictly below `k`.
-/
theorem hadamardCountingCubic_thresholdCountP_finRange
    (m k : Nat) (hk : k ≤ m) :
    List.countP (fun t : Fin m => t.val < k) (List.finRange m) = k := by
  induction m generalizing k with
  | zero =>
      have hk0 : k = 0 := Nat.eq_zero_of_le_zero hk
      subst k
      rfl
  | succ m ih =>
      cases k with
      | zero =>
          simp
      | succ k =>
          have hk' : k ≤ m := Nat.le_of_succ_le_succ hk
          rw [List.finRange_succ, List.countP_cons, List.countP_map]
          have hcomp :
              List.countP
                ((fun t : Fin (m + 1) =>
                    decide (t.val < Nat.succ k)) ∘ Fin.succ)
                (List.finRange m) =
              List.countP
                (fun t : Fin m => decide (t.val < k))
                (List.finRange m) := by
            congr 1
            funext t
            simp [Function.comp, Fin.succ]
          rw [hcomp, ih k hk']
          simp

theorem hadamardCountingCubic_thresholdFilterLength
    (m k : Nat) (hk : k ≤ m) :
    ((List.finRange m).filter (fun t => t.val < k)).length = k := by
  rw [← List.countP_eq_length_filter]
  exact hadamardCountingCubic_thresholdCountP_finRange m k hk

/-- The cubic threshold for row `j` fits in the `3*n`-qubit path register. -/
theorem hadamardCountingCubic_threshold_le_pathCapacity
    (n : Nat) (j : Fin (gridSize n)) :
    j.val ^ 3 <= gridSize (3 * n) := by
  have hle : j.val ^ 3 ≤ gridSize n ^ 3 :=
    Nat.pow_le_pow_left (Nat.le_of_lt j.isLt) 3
  simpa [gridSize_three_mul_eq_cube] using hle

/--
Symbolic accepted-path count for the Hadamard-counting threshold register.

For fixed output row `j`, the `3*n`-qubit threshold register contributes
exactly `j.val ^ 3` accepted values.
-/
theorem hadamardCountingCubic_thresholdPathCount
    (n : Nat) (j : Fin (gridSize n)) :
    ((List.finRange (gridSize (3 * n))).filter
        (fun t => t.val < j.val ^ 3)).length = j.val ^ 3 := by
  exact hadamardCountingCubic_thresholdFilterLength
    (gridSize (3 * n)) (j.val ^ 3)
    (hadamardCountingCubic_threshold_le_pathCapacity n j)

theorem gridPoint_nonneg (n : Nat) (j : Fin (gridSize n)) :
    (0 : Rat) ≤ gridPoint n j := by
  unfold gridPoint
  rw [← Rat.not_lt]
  intro h
  rw [Rat.div_lt_iff (gridSize_rat_pos n)] at h
  rw [Rat.zero_mul] at h
  exact (Rat.not_lt.mpr Rat.natCast_nonneg) h

theorem gridPoint_lt_one (n : Nat) (j : Fin (gridSize n)) :
    gridPoint n j < 1 := by
  unfold gridPoint
  rw [Rat.div_lt_iff (gridSize_rat_pos n)]
  rw [Rat.one_mul]
  exact (Rat.natCast_lt_natCast).mpr j.isLt

theorem gridPoint_le_one (n : Nat) (j : Fin (gridSize n)) :
    gridPoint n j ≤ 1 := by
  exact Rat.le_of_lt (gridPoint_lt_one n j)

theorem rat_pow_le_one_of_nonneg_le_one (x : Rat) (k : Nat)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1) :
    x ^ k ≤ 1 := by
  induction k with
  | zero =>
      simp
  | succ k ih =>
      rw [Rat.pow_succ]
      have hmul : x ^ k * x ≤ 1 * x :=
        Rat.mul_le_mul_of_nonneg_right ih hx0
      have hx : 1 * x ≤ 1 := by
        simpa [Rat.one_mul] using hx1
      exact Rat.le_trans hmul hx

theorem cubicAmplitude_sq_le_one (n : Nat) (j : Fin (gridSize n)) :
    cubicAmplitude n j ^ 2 ≤ 1 := by
  rw [cubicAmplitude_sq_eq_gridPoint_sixth]
  exact rat_pow_le_one_of_nonneg_le_one (gridPoint n j) 6
    (gridPoint_nonneg n j) (gridPoint_le_one n j)

theorem foldl_add_le_add_length {α : Type u} (xs : List α) (f : α → Rat)
    (h : ∀ x, x ∈ xs → f x ≤ 1) (acc : Rat) :
    xs.foldl (fun acc x => acc + f x) acc ≤ acc + (xs.length : Rat) := by
  induction xs generalizing acc with
  | nil =>
      simp [Rat.add_zero]
  | cons x xs ih =>
      simp [List.foldl]
      have hx : f x ≤ 1 := h x (by simp)
      have hxs : ∀ y, y ∈ xs → f y ≤ 1 := by
        intro y hy
        exact h y (by simp [hy])
      have hih := ih hxs (acc + f x)
      have hacc : acc + f x ≤ acc + 1 :=
        (Rat.add_le_add_left).mpr hx
      have hstep :
          (acc + f x) + (xs.length : Rat) ≤
            (acc + 1) + (xs.length : Rat) :=
        (Rat.add_le_add_right).mpr hacc
      have htarget :
          (acc + 1) + (xs.length : Rat) =
            acc + ((xs.length + 1 : Nat) : Rat) := by
        simp [Rat.add_comm, Rat.add_left_comm]
      exact Rat.le_trans hih
        (by simpa [htarget, Nat.succ_eq_add_one] using hstep)

theorem cubicNormSq_le_gridSize (n : Nat) :
    cubicNormSq n ≤ (gridSize n : Rat) := by
  unfold cubicNormSq
  have hfold := foldl_add_le_add_length
    (List.finRange (gridSize n))
    (fun j : Fin (gridSize n) => cubicAmplitude n j ^ 2)
    (by
      intro j _
      exact cubicAmplitude_sq_le_one n j)
    (0 : Rat)
  simpa [List.length_finRange, Rat.zero_add] using hfold

theorem gridSize_rat_le_sq (n : Nat) :
    (gridSize n : Rat) ≤ (gridSize n : Rat) ^ 2 := by
  have hOneLe : (1 : Rat) ≤ (gridSize n : Rat) := by
    exact (Rat.natCast_le_natCast).mpr (Nat.succ_le_of_lt (gridSize_pos n))
  have hNonneg : (0 : Rat) ≤ (gridSize n : Rat) :=
    Rat.le_of_lt (gridSize_rat_pos n)
  have hmul :
      (1 : Rat) * (gridSize n : Rat) ≤
        (gridSize n : Rat) * (gridSize n : Rat) :=
    Rat.mul_le_mul_of_nonneg_right hOneLe hNonneg
  simpa [Rat.one_mul, Rat.pow_succ] using hmul

theorem cubicNormSq_le_conservativeNormalizer_sq (n : Nat) :
    cubicNormSq n ≤ conservativeNormalizer n ^ 2 := by
  exact Rat.le_trans (cubicNormSq_le_gridSize n) (by
    simpa [conservativeNormalizer] using gridSize_rat_le_sq n)

/--
Candidate-specific normalizer bridge for the first arithmetic route.  This does
not certify the candidate unitary; it only records that the route's current
choice `alpha = arithmeticCubicNormalizer n` inherits the compiled conservative
norm bound.
-/
theorem cubicNormSq_le_arithmeticCubicNormalizer_sq (n : Nat) :
    cubicNormSq n ≤ arithmeticCubicNormalizer n ^ 2 := by
  simpa [arithmeticCubicNormalizer] using
    cubicNormSq_le_conservativeNormalizer_sq n

/--
Candidate-specific normalizer bridge for the Hadamard-counting route.  This
does not certify the Hadamard-sandwich semantics; it only records that the
route's normalizer inherits the compiled conservative norm bound.
-/
theorem cubicNormSq_le_hadamardCountingCubicNormalizer_sq (n : Nat) :
    cubicNormSq n ≤ hadamardCountingCubicNormalizer n ^ 2 := by
  simpa [hadamardCountingCubicNormalizer] using
    cubicNormSq_le_conservativeNormalizer_sq n

theorem cubicNormSq_n1 :
    cubicNormSq 1 = (1 : Rat) / 64 := by
  decide +kernel

theorem cubicNormSq_n2 :
    cubicNormSq 2 = (397 : Rat) / 2048 := by
  decide +kernel

theorem cubicNormSq_n3 :
    cubicNormSq 3 = (46205 : Rat) / 65536 := by
  decide +kernel

end CubicStatePreparation

namespace CubicDiagonalOracle

/-- Task identifier used by the retrieval and verifier ledgers. -/
def taskId : String := "QBE-OP-CUBIC-DIAGONAL-001"

/-- The diagonal cubic oracle target `D_n[row,col] = (row/2^n)^3` if `row=col`, else zero. -/
def cubicDiagonalOperator (n : Nat) :
    Matrix (gridSize n) (gridSize n) Rat :=
  fun row col =>
    if row = col then CubicStatePreparation.cubicAmplitude n row else 0

/-- Exact normalizer for the diagonal target at the primitive amplitude-oracle tier. -/
def exactNormalizer (_n : Nat) : Rat := 1

/-- Operator-first target record for the diagonal cubic oracle. -/
def cubicDiagonalTarget (n : Nat) :
    QueryOperatorTarget Rat (gridSize n) (gridSize n) where
  operator := cubicDiagonalOperator n
  normalizer := exactNormalizer n
  source :=
    "QBE-OP-CUBIC-DIAGONAL-001: D_n=sum_j (j/2^n)^3 |j><j|"
  semanticContract :=
    "diagonal cubic oracle; exact primitive amplitude-oracle route first"
  freeParameters := [
    "n positive",
    "diagonal target, not rank-one state preparation",
    "score order inside one tier: gateCount, depth, auxiliaryQubits, oracleCalls"
  ]

/--
Hinted linear diagonal target `O_0[row,col] = row/2^n` if `row=col`, else zero.

This is the input operator for the task-local QSVT consumer route.  It is only
the target matrix; a block-encoding circuit for this matrix is a separate proof
obligation.
-/
def linearDiagonalOperator (n : Nat) :
    Matrix (gridSize n) (gridSize n) Rat :=
  fun row col =>
    if row = col then CubicStatePreparation.gridPoint n row else 0

/-- Operator-first target record for the hinted linear diagonal input `O_0`. -/
def linearDiagonalTarget (n : Nat) :
    QueryOperatorTarget Rat (gridSize n) (gridSize n) where
  operator := linearDiagonalOperator n
  normalizer := exactNormalizer n
  source :=
    "QBE-OP-CUBIC-DIAGONAL-001: O_0=sum_j (j/2^n) |j><j|"
  semanticContract :=
    "linear diagonal input target for compiled product and optional QSVT x^3 routes"
  freeParameters := [
    "n positive",
    "exact input block encoding required before QSVT consumption",
    "QSVT consumer remains contract-only until a stronger theorem is named"
  ]

/-- Clean-block contract for the hinted linear diagonal input target. -/
def linearDiagonalCleanBlockContract (n : Nat)
    (block : Matrix (gridSize n) (gridSize n) Rat) : Prop :=
  ∀ row col,
    block row col =
      if row = col then CubicStatePreparation.gridPoint n row else 0

theorem linearDiagonalCleanBlockContract_pointwise_eq
    (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat)
    (h : linearDiagonalCleanBlockContract n block) :
    Matrix.PointwiseEq block (linearDiagonalOperator n) := by
  intro row col
  simpa [linearDiagonalOperator] using h row col

theorem linearDiagonalCleanBlock_eq_target
    (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat)
    (h : linearDiagonalCleanBlockContract n block) :
    Matrix.PointwiseEq block (linearDiagonalTarget n).operator := by
  simpa [linearDiagonalTarget] using
    (linearDiagonalCleanBlockContract_pointwise_eq n block h)

/--
Package a supplied clean-block equality for the hinted linear diagonal target
as an `ExactCleanBlock` payload.

This is semantic glue only.  The caller still owns the unitary proof, cleanup
proof, concrete circuit, and resource tuple for the matrix `U`.
-/
def linearDiagonalExactCleanBlockFromPointwise
    {n total : Nat}
    (U : Matrix total total Rat)
    (embed : Fin (gridSize n) -> Fin total)
    (h :
      Matrix.PointwiseEq
        (BlockEncodingClassics.cleanBlockBy embed U)
        (linearDiagonalOperator n)) :
    BlockEncodingClassics.ExactCleanBlock (gridSize n) total where
  U := U
  A := linearDiagonalOperator n
  embed := embed
  blockProof := h

theorem linearDiagonalExactCleanBlockFromPointwise_clean_eq_target
    {n total : Nat}
    (U : Matrix total total Rat)
    (embed : Fin (gridSize n) -> Fin total)
    (h :
      Matrix.PointwiseEq
        (BlockEncodingClassics.cleanBlockBy embed U)
        (linearDiagonalOperator n)) :
    Matrix.PointwiseEq
      (BlockEncodingClassics.ExactCleanBlock.clean
        (linearDiagonalExactCleanBlockFromPointwise U embed h))
      (linearDiagonalTarget n).operator := by
  simpa [linearDiagonalTarget, linearDiagonalExactCleanBlockFromPointwise] using
    (BlockEncodingClassics.ExactCleanBlock.clean_eq_target
      (linearDiagonalExactCleanBlockFromPointwise U embed h))

/--
Interface for a concrete block encoding of the hinted linear diagonal input.

This names the fields a backend must supply before the exact clean-block
payload can be used as a real input certificate.  It is not itself a backend:
the cleanup and resource propositions must describe the chosen circuit family.
-/
structure LinearDiagonalInputBEContract (n total : Nat) where
  U : Matrix total total Rat
  embed : Fin (gridSize n) -> Fin total
  unitaryProof : BlockEncodingClassics.IsRationalOrthogonal U
  cleanupStatement : Prop
  cleanupDescription : String
  cleanupProof : cleanupStatement
  cleanBlockProof :
    Matrix.PointwiseEq
      (BlockEncodingClassics.cleanBlockBy embed U)
      (linearDiagonalOperator n)
  normalizerProof : (linearDiagonalTarget n).normalizer = 1
  resource : Resource
  resourceStatement : Prop
  resourceProof : resourceStatement

namespace LinearDiagonalInputBEContract

/--
Extract the reusable exact clean-block payload from a concrete linear-diagonal
input contract.
-/
def exactPayload {n total : Nat}
    (cert : LinearDiagonalInputBEContract n total) :
    BlockEncodingClassics.ExactCleanBlock (gridSize n) total :=
  linearDiagonalExactCleanBlockFromPointwise cert.U cert.embed cert.cleanBlockProof

/-- The extracted clean block equals the hinted linear diagonal target. -/
theorem clean_eq_target {n total : Nat}
    (cert : LinearDiagonalInputBEContract n total) :
    Matrix.PointwiseEq
      (BlockEncodingClassics.ExactCleanBlock.clean cert.exactPayload)
      (linearDiagonalTarget n).operator := by
  exact
    linearDiagonalExactCleanBlockFromPointwise_clean_eq_target
      cert.U cert.embed cert.cleanBlockProof

end LinearDiagonalInputBEContract

/-- Clean basis index for the 8-dimensional rational Householder signal block. -/
def householderZero : Fin 8 := 0

/-- Explicit rational dot product for the 8-dimensional Householder support leaf. -/
def dot8 (u v : Fin 8 -> Rat) : Rat :=
  u 0 * v 0 + u 1 * v 1 + u 2 * v 2 + u 3 * v 3 +
    u 4 * v 4 + u 5 * v 5 + u 6 * v 6 + u 7 * v 7

/-- Vector `e_0 - v` used in the rational Householder reflection. -/
def householder8E0Minus (v : Fin 8 -> Rat) : Fin 8 -> Rat :=
  fun i => (if i = householderZero then 1 else 0) - v i

/--
Rational 8-by-8 Householder block used by the hinted `O_0` backend route.

The later backend still has to supply rational unit-vector completions for the
grid values and prove orthogonality of this block family.
-/
def householder8 (v : Fin 8 -> Rat) : Matrix 8 8 Rat :=
  fun row col =>
    (if row = col then 1 else 0) -
      (2 / dot8 (householder8E0Minus v) (householder8E0Minus v)) *
        householder8E0Minus v row * householder8E0Minus v col

/-- Norm identity for `e_0 - v` under the rational unit-vector hypothesis. -/
theorem householder8E0Minus_normSq
    (v : Fin 8 -> Rat)
    (hunit : dot8 v v = 1) :
    dot8 (householder8E0Minus v) (householder8E0Minus v) =
      2 * (1 - v householderZero) := by
  unfold dot8 householder8E0Minus householderZero at *
  grind

/-- The Householder denominator is nonzero when the clean coordinate is not one. -/
theorem householder8E0Minus_normSq_ne_zero
    (v : Fin 8 -> Rat)
    (hunit : dot8 v v = 1)
    (hnot : v householderZero ≠ 1) :
    dot8 (householder8E0Minus v) (householder8E0Minus v) ≠ 0 := by
  rw [householder8E0Minus_normSq v hunit]
  grind

/--
Active leaf `HINT-HOUSEHOLDER8-CLEAN-ENTRY`: the clean entry of the rational
Householder block is the first coordinate of the supplied unit vector.
-/
theorem householder8_clean_entry
    (v : Fin 8 -> Rat)
    (hunit : dot8 v v = 1)
    (hnot : v householderZero ≠ 1) :
    householder8 v householderZero householderZero =
      v householderZero := by
  have hden := householder8E0Minus_normSq_ne_zero v hunit hnot
  unfold householder8
  rw [householder8E0Minus_normSq v hunit]
  unfold householder8E0Minus householderZero at *
  grind

private def delta8 (i : Fin 8) : Fin 8 -> Rat :=
  fun k => if k = i then 1 else 0

private theorem fin8_exhaust (i : Fin 8) :
    i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 ∨ i = 7 := by
  have hval : i.val = 0 ∨ i.val = 1 ∨ i.val = 2 ∨ i.val = 3 ∨
      i.val = 4 ∨ i.val = 5 ∨ i.val = 6 ∨ i.val = 7 := by
    omega
  rcases hval with h0 | h1 | h2 | h3 | h4 | h5 | h6 | h7
  · left
    apply Fin.ext
    simpa using h0
  · right; left
    apply Fin.ext
    simpa using h1
  · right; right; left
    apply Fin.ext
    simpa using h2
  · right; right; right; left
    apply Fin.ext
    simpa using h3
  · right; right; right; right; left
    apply Fin.ext
    simpa using h4
  · right; right; right; right; right; left
    apply Fin.ext
    simpa using h5
  · right; right; right; right; right; right; left
    apply Fin.ext
    simpa using h6
  · right; right; right; right; right; right; right
    apply Fin.ext
    simpa using h7

private theorem dot8_delta_delta (i j : Fin 8) :
    dot8 (delta8 i) (delta8 j) = Matrix.identity 8 Rat i j := by
  rcases fin8_exhaust i with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
  rcases fin8_exhaust j with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    unfold dot8 delta8 Matrix.identity <;>
    grind

private theorem dot8_delta_left (i : Fin 8) (w : Fin 8 -> Rat) :
    dot8 (delta8 i) w = w i := by
  rcases fin8_exhaust i with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    unfold dot8 delta8 <;>
    grind

private theorem dot8_delta_right (u : Fin 8 -> Rat) (j : Fin 8) :
    dot8 u (delta8 j) = u j := by
  rcases fin8_exhaust j with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    unfold dot8 delta8 <;>
    grind

private theorem dot8_sub_sub (a b u v : Fin 8 -> Rat) (c x y : Rat) :
    dot8 (fun k => a k - c * u k * x) (fun k => b k - c * v k * y) =
      dot8 a b - c * x * dot8 u b - c * y * dot8 a v +
        c * c * x * y * dot8 u v := by
  unfold dot8
  grind [Rat.mul_comm, Rat.mul_assoc]

private theorem householder8_columnDot
    (v : Fin 8 -> Rat)
    (hunit : dot8 v v = 1)
    (hnot : v householderZero ≠ 1) :
    ∀ i j : Fin 8,
      dot8 (fun k => householder8 v k i) (fun k => householder8 v k j) =
        Matrix.identity 8 Rat i j := by
  intro i j
  let u := householder8E0Minus v
  let d := dot8 u u
  let c := 2 / d
  have hdne : d ≠ 0 := by
    dsimp [d, u]
    exact householder8E0Minus_normSq_ne_zero v hunit hnot
  have hcoeff : -c * u i * u j - c * u j * u i +
      c * c * u i * u j * d = 0 := by
    dsimp [c]
    grind [Rat.mul_comm, Rat.mul_assoc]
  calc
    dot8 (fun k => householder8 v k i) (fun k => householder8 v k j)
        = dot8 (fun k => delta8 i k - c * u k * u i)
            (fun k => delta8 j k - c * u k * u j) := by
          unfold householder8 delta8
          dsimp [u, c, d]
    _ = dot8 (delta8 i) (delta8 j) - c * (u i) * dot8 u (delta8 j) -
          c * (u j) * dot8 (delta8 i) u + c * c * (u i) * (u j) * dot8 u u := by
          exact dot8_sub_sub (delta8 i) (delta8 j) u u c (u i) (u j)
    _ = Matrix.identity 8 Rat i j := by
          rw [dot8_delta_delta, dot8_delta_right, dot8_delta_left]
          dsimp [d] at hcoeff
          grind [Rat.mul_comm, Rat.mul_assoc]

private theorem householder8_symm (v : Fin 8 -> Rat) (i j : Fin 8) :
    householder8 v i j = householder8 v j i := by
  unfold householder8
  grind [Rat.mul_comm, Rat.mul_assoc]

private theorem householder8_rowDot
    (v : Fin 8 -> Rat)
    (hunit : dot8 v v = 1)
    (hnot : v householderZero ≠ 1) :
    ∀ i j : Fin 8,
      dot8 (fun k => householder8 v i k) (fun k => householder8 v j k) =
        Matrix.identity 8 Rat i j := by
  intro i j
  have hleft : (fun k => householder8 v i k) = (fun k => householder8 v k i) := by
    funext k
    exact householder8_symm v i k
  have hright : (fun k => householder8 v j k) = (fun k => householder8 v k j) := by
    funext k
    exact householder8_symm v j k
  rw [hleft, hright]
  exact householder8_columnDot v hunit hnot i j

private theorem columnInner_eq_dot8 (U : Matrix 8 8 Rat) (i j : Fin 8) :
    BlockEncodingClassics.columnInner U i j =
      dot8 (fun k => U k i) (fun k => U k j) := by
  unfold BlockEncodingClassics.columnInner dot8
  simp [List.finRange]

private theorem rowInner_eq_dot8 (U : Matrix 8 8 Rat) (i j : Fin 8) :
    BlockEncodingClassics.rowInner U i j =
      dot8 (fun k => U i k) (fun k => U j k) := by
  unfold BlockEncodingClassics.rowInner dot8
  simp [List.finRange]

/--
Active leaf `HINT-HOUSEHOLDER8-ORTHO`: the rational 8-dimensional Householder
block is orthogonal whenever the input vector has `dot8 v v = 1` and does not
equal the clean basis vector.
-/
theorem householder8_isRationalOrthogonal
    (v : Fin 8 -> Rat)
    (hunit : dot8 v v = 1)
    (hnot : v householderZero ≠ 1) :
    BlockEncodingClassics.IsRationalOrthogonal (householder8 v) := by
  constructor
  · intro i j
    rw [columnInner_eq_dot8]
    exact householder8_columnDot v hunit hnot i j
  · intro i j
    rw [rowInner_eq_dot8]
    exact householder8_rowDot v hunit hnot i j

/-- System component for the task-local `ancilla × system` direct-sum matrix. -/
def controlledHouseholder8SystemIndex (n : Nat)
    (idx : Fin (8 * gridSize n)) : Fin (gridSize n) :=
  ⟨idx.val % gridSize n, Nat.mod_lt _ (CubicStatePreparation.gridSize_pos n)⟩

/-- Ancilla component for the task-local `ancilla × system` direct-sum matrix. -/
def controlledHouseholder8AncillaIndex (n : Nat)
    (idx : Fin (8 * gridSize n)) : Fin 8 :=
  ⟨idx.val / gridSize n, by
    have hlt : idx.val < gridSize n * 8 := by
      have hraw : idx.val < 8 * gridSize n := idx.isLt
      omega
    exact Nat.div_lt_of_lt_mul hlt⟩

/-- Clean embedding for the controlled Householder direct sum. -/
def controlledHouseholder8Embed (n : Nat) :
    Fin (gridSize n) -> Fin (8 * gridSize n) :=
  BlockEncodingClassics.productIndex householderZero

/-- Task-local controlled direct sum of supplied Householder blocks over system branches. -/
def controlledHouseholder8DirectSum
    (n : Nat) (v : Fin (gridSize n) -> Fin 8 -> Rat) :
    Matrix (8 * gridSize n) (8 * gridSize n) Rat :=
  fun row col =>
    if controlledHouseholder8SystemIndex n row =
        controlledHouseholder8SystemIndex n col then
      householder8 (v (controlledHouseholder8SystemIndex n row))
        (controlledHouseholder8AncillaIndex n row)
        (controlledHouseholder8AncillaIndex n col)
    else 0

private theorem controlledHouseholder8Embed_val
    (n : Nat) (j : Fin (gridSize n)) :
    (controlledHouseholder8Embed n j).val = j.val := by
  simp [controlledHouseholder8Embed, BlockEncodingClassics.productIndex,
    householderZero]

private theorem controlledHouseholder8SystemIndex_embed
    (n : Nat) (j : Fin (gridSize n)) :
    controlledHouseholder8SystemIndex n (controlledHouseholder8Embed n j) = j := by
  apply Fin.ext
  simp [controlledHouseholder8SystemIndex, controlledHouseholder8Embed_val,
    Nat.mod_eq_of_lt j.isLt]

private theorem controlledHouseholder8AncillaIndex_embed
    (n : Nat) (j : Fin (gridSize n)) :
    controlledHouseholder8AncillaIndex n (controlledHouseholder8Embed n j) =
      householderZero := by
  apply Fin.ext
  simp [controlledHouseholder8AncillaIndex, controlledHouseholder8Embed_val,
    householderZero, Nat.div_eq_of_lt j.isLt]

private theorem controlledHouseholder8SystemIndex_productIndex
    (n : Nat) (a : Fin 8) (s : Fin (gridSize n)) :
    controlledHouseholder8SystemIndex n
        (BlockEncodingClassics.productIndex a s) = s := by
  apply Fin.ext
  simp [controlledHouseholder8SystemIndex, BlockEncodingClassics.productIndex,
    Nat.mod_eq_of_lt s.isLt]

private theorem controlledHouseholder8AncillaIndex_productIndex
    (n : Nat) (a : Fin 8) (s : Fin (gridSize n)) :
    controlledHouseholder8AncillaIndex n
        (BlockEncodingClassics.productIndex a s) = a := by
  apply Fin.ext
  have hpos : 0 < gridSize n := CubicStatePreparation.gridSize_pos n
  simp [controlledHouseholder8AncillaIndex, BlockEncodingClassics.productIndex]
  rw [Nat.add_comm]
  rw [Nat.mul_comm a.val (gridSize n)]
  rw [Nat.add_mul_div_left]
  · rw [Nat.div_eq_of_lt s.isLt, Nat.zero_add]
  · exact hpos

private theorem controlledHouseholder8_productIndex_eta
    (n : Nat) (idx : Fin (8 * gridSize n)) :
    BlockEncodingClassics.productIndex
      (controlledHouseholder8AncillaIndex n idx)
      (controlledHouseholder8SystemIndex n idx) = idx := by
  apply Fin.ext
  simp [BlockEncodingClassics.productIndex, controlledHouseholder8AncillaIndex,
    controlledHouseholder8SystemIndex]
  have hdiv := Nat.div_add_mod idx.val (gridSize n)
  have hcomm :
      idx.val / gridSize n * gridSize n + idx.val % gridSize n =
        gridSize n * (idx.val / gridSize n) + idx.val % gridSize n := by
    rw [Nat.mul_comm]
  exact hcomm.trans hdiv

private theorem controlledHouseholder8_identity_same_branch
    (n : Nat) (i j : Fin (8 * gridSize n))
    (hsys :
      controlledHouseholder8SystemIndex n i =
        controlledHouseholder8SystemIndex n j) :
    Matrix.identity (8 * gridSize n) Rat i j =
      Matrix.identity 8 Rat
        (controlledHouseholder8AncillaIndex n i)
        (controlledHouseholder8AncillaIndex n j) := by
  by_cases hanc :
      controlledHouseholder8AncillaIndex n i =
        controlledHouseholder8AncillaIndex n j
  · have hij : i = j := by
      calc
        i = BlockEncodingClassics.productIndex
              (controlledHouseholder8AncillaIndex n i)
              (controlledHouseholder8SystemIndex n i) := by
                exact (controlledHouseholder8_productIndex_eta n i).symm
        _ = BlockEncodingClassics.productIndex
              (controlledHouseholder8AncillaIndex n j)
              (controlledHouseholder8SystemIndex n j) := by
                rw [hanc, hsys]
        _ = j := controlledHouseholder8_productIndex_eta n j
    subst j
    simp [Matrix.identity]
  · have hij : i ≠ j := by
      intro hij
      apply hanc
      simp [hij]
    simp [Matrix.identity, hij, hanc]

/--
Grid branches for the linear diagonal input never have clean Householder
coordinate equal to one.
-/
theorem controlledHouseholder8_branchNontrivial_of_clean
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (branchClean :
      forall j : Fin (gridSize n),
        v j householderZero = CubicStatePreparation.gridPoint n j) :
    forall j : Fin (gridSize n), v j householderZero ≠ 1 := by
  intro j hEq
  have hlt := CubicStatePreparation.gridPoint_lt_one n j
  have hclean := branchClean j
  rw [hEq] at hclean
  rw [← hclean] at hlt
  exact Rat.lt_irrefl hlt

/--
Active leaf `HINT-CONTROLLED-DIRECT-SUM`: the clean block of the controlled
Householder direct sum is the hinted linear diagonal operator.
-/
theorem controlledHouseholder8DirectSum_clean_entry
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (branchUnit :
      forall j : Fin (gridSize n), dot8 (v j) (v j) = 1)
    (branchClean :
      forall j : Fin (gridSize n),
        v j householderZero = CubicStatePreparation.gridPoint n j)
    (branchNontrivial :
      forall j : Fin (gridSize n), v j householderZero ≠ 1) :
    Matrix.PointwiseEq
      (BlockEncodingClassics.cleanBlockBy
        (controlledHouseholder8Embed n)
        (controlledHouseholder8DirectSum n v))
      (linearDiagonalOperator n) := by
  intro row col
  by_cases hrowcol : row = col
  · subst col
    calc
      BlockEncodingClassics.cleanBlockBy
          (controlledHouseholder8Embed n)
          (controlledHouseholder8DirectSum n v) row row
          = householder8 (v row) householderZero householderZero := by
              simp [BlockEncodingClassics.cleanBlockBy,
                controlledHouseholder8DirectSum,
                controlledHouseholder8SystemIndex_embed,
                controlledHouseholder8AncillaIndex_embed]
      _ = v row householderZero :=
              householder8_clean_entry (v row) (branchUnit row)
                (branchNontrivial row)
      _ = CubicStatePreparation.gridPoint n row := branchClean row
      _ = linearDiagonalOperator n row row := by
              simp [linearDiagonalOperator]
  · have hsys_ne :
        controlledHouseholder8SystemIndex n
            (controlledHouseholder8Embed n row) ≠
          controlledHouseholder8SystemIndex n
            (controlledHouseholder8Embed n col) := by
      intro hsys
      have hrow : row = col := by
        rw [controlledHouseholder8SystemIndex_embed] at hsys
        rw [controlledHouseholder8SystemIndex_embed] at hsys
        exact hsys
      exact hrowcol hrow
    simp [BlockEncodingClassics.cleanBlockBy, controlledHouseholder8DirectSum,
      linearDiagonalOperator, hrowcol, hsys_ne]

private theorem linearDiagonal_foldl_add_zero_of_all_zero {β : Type u}
    (ks : List β) (f : β -> Rat) (acc : Rat)
    (hzero : ∀ k, k ∈ ks -> f k = 0) :
    ks.foldl (fun acc k => acc + f k) acc = acc := by
  induction ks generalizing acc with
  | nil => rfl
  | cons k ks ih =>
      have hkzero : f k = 0 := hzero k (by simp)
      have htail : ∀ k', k' ∈ ks -> f k' = 0 := by
        intro k' hk'
        exact hzero k' (by simp [hk'])
      calc
        (k :: ks).foldl (fun acc k => acc + f k) acc =
            ks.foldl (fun acc k => acc + f k) (acc + f k) := rfl
        _ = ks.foldl (fun acc k => acc + f k) acc := by
            rw [hkzero, Rat.add_zero]
        _ = acc := ih acc htail

/--
Column-inner bridge for the controlled Householder direct sum in the
cross-branch case.

This is a support leaf for `HINT-CONTROLLED-DIRECT-SUM-ORTHO`: if two columns
belong to different system branches, every path contribution through the
block-diagonal direct sum vanishes, so the column inner product agrees with the
off-diagonal identity entry.
-/
theorem controlledHouseholder8DirectSum_columnInner_eq_identity_of_system_ne
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (i j : Fin (8 * gridSize n))
    (hsys :
      controlledHouseholder8SystemIndex n i ≠
        controlledHouseholder8SystemIndex n j) :
    BlockEncodingClassics.columnInner (controlledHouseholder8DirectSum n v) i j =
      Matrix.identity (8 * gridSize n) Rat i j := by
  have hzero :
      BlockEncodingClassics.columnInner (controlledHouseholder8DirectSum n v) i j = 0 := by
    unfold BlockEncodingClassics.columnInner
    exact linearDiagonal_foldl_add_zero_of_all_zero
      (List.finRange (8 * gridSize n))
      (fun k : Fin (8 * gridSize n) =>
        controlledHouseholder8DirectSum n v k i *
          controlledHouseholder8DirectSum n v k j)
      0
      (by
        intro k _hmem
        by_cases hki :
            controlledHouseholder8SystemIndex n k =
              controlledHouseholder8SystemIndex n i
        · simp [controlledHouseholder8DirectSum, hki, hsys]
        · simp [controlledHouseholder8DirectSum, hki])
  rw [hzero]
  have hij : i ≠ j := by
    intro hij
    exact hsys (by simp [hij])
  simp [Matrix.identity, hij]

/--
Support leaf `CDS-FIBER-ZERO-COL`: in the same-branch column-fold proof, any
summation index outside the shared decoded system branch contributes zero.
-/
private theorem controlledHouseholder8DirectSum_column_off_branch_summand_zero
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (s : Fin (gridSize n))
    (i j k : Fin (8 * gridSize n))
    (hi : controlledHouseholder8SystemIndex n i = s)
    (_hj : controlledHouseholder8SystemIndex n j = s)
    (hk : controlledHouseholder8SystemIndex n k ≠ s) :
    controlledHouseholder8DirectSum n v k i *
      controlledHouseholder8DirectSum n v k j = 0 := by
  have hki : controlledHouseholder8SystemIndex n k ≠
      controlledHouseholder8SystemIndex n i := by
    intro h
    exact hk (h.trans hi)
  simp [controlledHouseholder8DirectSum, hki]

private theorem controlledHouseholder8DirectSum_column_summand_productIndex
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (s : Fin (gridSize n))
    (a ai aj : Fin 8) :
    controlledHouseholder8DirectSum n v
        (BlockEncodingClassics.productIndex a s)
        (BlockEncodingClassics.productIndex ai s) *
      controlledHouseholder8DirectSum n v
        (BlockEncodingClassics.productIndex a s)
        (BlockEncodingClassics.productIndex aj s) =
    householder8 (v s) a ai * householder8 (v s) a aj := by
  simp [controlledHouseholder8DirectSum,
    controlledHouseholder8SystemIndex_productIndex,
    controlledHouseholder8AncillaIndex_productIndex]

private theorem controlledHouseholder8DirectSum_row_off_branch_summand_zero
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (s : Fin (gridSize n))
    (i j k : Fin (8 * gridSize n))
    (hi : controlledHouseholder8SystemIndex n i = s)
    (_hj : controlledHouseholder8SystemIndex n j = s)
    (hk : controlledHouseholder8SystemIndex n k ≠ s) :
    controlledHouseholder8DirectSum n v i k *
      controlledHouseholder8DirectSum n v j k = 0 := by
  have hik : controlledHouseholder8SystemIndex n i ≠
      controlledHouseholder8SystemIndex n k := by
    intro h
    exact hk (h.symm.trans hi)
  simp [controlledHouseholder8DirectSum, hik]

private theorem controlledHouseholder8DirectSum_row_summand_productIndex
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (s : Fin (gridSize n))
    (a ai aj : Fin 8) :
    controlledHouseholder8DirectSum n v
        (BlockEncodingClassics.productIndex ai s)
        (BlockEncodingClassics.productIndex a s) *
      controlledHouseholder8DirectSum n v
        (BlockEncodingClassics.productIndex aj s)
        (BlockEncodingClassics.productIndex a s) =
    householder8 (v s) ai a * householder8 (v s) aj a := by
  simp [controlledHouseholder8DirectSum,
    controlledHouseholder8SystemIndex_productIndex,
    controlledHouseholder8AncillaIndex_productIndex]

private def controlledHouseholder8BranchFiber
    (n : Nat) (s : Fin (gridSize n)) :
    List (Fin (8 * gridSize n)) :=
  (List.finRange 8).map
    (fun a : Fin 8 => BlockEncodingClassics.productIndex a s)

private theorem controlledHouseholder8_productIndex_left_injective
    (n : Nat) (s : Fin (gridSize n)) :
    Function.Injective
      (fun a : Fin 8 => BlockEncodingClassics.productIndex a s) := by
  intro a b h
  have hanc :=
    congrArg (fun idx => controlledHouseholder8AncillaIndex n idx) h
  simpa [controlledHouseholder8AncillaIndex_productIndex] using hanc

private theorem controlledHouseholder8BranchFiber_mem_iff
    (n : Nat) (s : Fin (gridSize n)) (k : Fin (8 * gridSize n)) :
    k ∈ controlledHouseholder8BranchFiber n s ↔
      controlledHouseholder8SystemIndex n k = s := by
  constructor
  · intro hk
    rcases List.mem_map.mp hk with ⟨a, _ha, hprod⟩
    rw [← hprod]
    exact controlledHouseholder8SystemIndex_productIndex n a s
  · intro hsys
    rw [controlledHouseholder8BranchFiber, List.mem_map]
    refine ⟨controlledHouseholder8AncillaIndex n k,
      List.mem_finRange _, ?_⟩
    simpa [hsys] using controlledHouseholder8_productIndex_eta n k

private theorem linearDiagonal_foldl_add_unique_of_nodup {β : Type u}
    [DecidableEq β] (ks : List β) (f : β -> Rat) (k0 : β)
    (hnodup : ks.Nodup)
    (hmem : k0 ∈ ks)
    (hzero : ∀ k, k ∈ ks -> k ≠ k0 -> f k = 0) :
    ks.foldl (fun acc k => acc + f k) 0 = f k0 := by
  induction ks with
  | nil => cases hmem
  | cons k ks ih =>
      rw [List.nodup_cons] at hnodup
      rcases hnodup with ⟨hk_not_mem, hks_nodup⟩
      rw [List.mem_cons] at hmem
      rcases hmem with hhead | htailmem
      · subst hhead
        have htail_zero : ∀ k', k' ∈ ks -> f k' = 0 := by
          intro k' hk'
          have hne : k' ≠ k0 := by
            intro h_eq
            apply hk_not_mem
            simpa [h_eq] using hk'
          exact hzero k' (by simp [hk']) hne
        calc
          (k0 :: ks).foldl (fun acc k => acc + f k) 0 =
              ks.foldl (fun acc k => acc + f k) (0 + f k0) := rfl
          _ = ks.foldl (fun acc k => acc + f k) (f k0) := by
              rw [Rat.zero_add]
          _ = f k0 :=
              linearDiagonal_foldl_add_zero_of_all_zero ks f (f k0)
                htail_zero
      · have hk_zero : f k = 0 := by
          have hne : k ≠ k0 := by
            intro h_eq
            apply hk_not_mem
            simpa [h_eq] using htailmem
          exact hzero k (by simp) hne
        have htail_zero : ∀ k', k' ∈ ks -> k' ≠ k0 -> f k' = 0 := by
          intro k' hk' hne
          exact hzero k' (by simp [hk']) hne
        calc
          (k :: ks).foldl (fun acc k => acc + f k) 0 =
              ks.foldl (fun acc k => acc + f k) (0 + f k) := rfl
          _ = ks.foldl (fun acc k => acc + f k) 0 := by
              rw [hk_zero, Rat.zero_add]
          _ = f k0 := ih hks_nodup htailmem htail_zero

private theorem linearDiagonal_nodup_map_of_injective {α : Type u} {β : Type v}
    [DecidableEq β] {f : α -> β} (hf : Function.Injective f)
    {xs : List α} (hxs : xs.Nodup) :
    (xs.map f).Nodup := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      rw [List.nodup_cons] at hxs
      rcases hxs with ⟨hx_not_mem, hxs_nodup⟩
      change (f x :: xs.map f).Nodup
      rw [List.nodup_cons]
      constructor
      · intro hmem
        rcases List.mem_map.mp hmem with ⟨y, hy_mem, hy_eq⟩
        apply hx_not_mem
        have hxy : y = x := hf hy_eq
        simpa [hxy] using hy_mem
      · exact ih hxs_nodup

private theorem linearDiagonal_finRange_nodup (n : Nat) :
    (List.finRange n).Nodup := by
  induction n with
  | zero => simp [List.finRange_zero]
  | succ n ih =>
      rw [List.finRange_succ]
      rw [List.nodup_cons]
      constructor
      · intro hmem
        rcases List.mem_map.mp hmem with ⟨k, _hk_mem, hk_zero⟩
        exact Fin.succ_ne_zero k hk_zero
      · apply linearDiagonal_nodup_map_of_injective
        · intro a b h
          apply Fin.eq_of_val_eq
          have hv := congrArg (fun x : Fin (n + 1) => x.val) h
          simpa using Nat.succ.inj hv
        · exact ih

private theorem controlledHouseholder8BranchFiber_nodup
    (n : Nat) (s : Fin (gridSize n)) :
    (controlledHouseholder8BranchFiber n s).Nodup := by
  exact linearDiagonal_nodup_map_of_injective
    (controlledHouseholder8_productIndex_left_injective n s)
    (linearDiagonal_finRange_nodup 8)

private theorem linearDiagonal_perm_cons_erase_of_mem {α : Type u}
    [BEq α] [LawfulBEq α] (x : α) :
    ∀ {ys : List α}, x ∈ ys -> ys.Perm (x :: ys.erase x)
  | [], h => by cases h
  | y :: ys, h => by
      by_cases hy : y = x
      · subst y
        simp [List.erase_cons_head]
      · have htail : x ∈ ys := by
          rw [List.mem_cons] at h
          rcases h with hxy | htail
          · exact False.elim (hy hxy.symm)
          · exact htail
        have htail_perm := linearDiagonal_perm_cons_erase_of_mem x htail
        have herase : (y :: ys).erase x = y :: ys.erase x := by
          rw [List.erase_cons_tail]
          intro hbeq
          exact hy (beq_iff_eq.mp hbeq)
        rw [herase]
        exact (List.Perm.cons y htail_perm).trans
          (List.Perm.swap x y (ys.erase x))

private theorem linearDiagonal_perm_of_nodup_mem_iff {α : Type u}
    [BEq α] [LawfulBEq α] {xs ys : List α}
    (hxs : xs.Nodup) (hys : ys.Nodup)
    (hmem : ∀ x, x ∈ xs ↔ x ∈ ys) :
    xs.Perm ys := by
  induction xs generalizing ys with
  | nil =>
      cases ys with
      | nil => exact List.Perm.refl []
      | cons y ys =>
          have hy_nil : y ∈ ([] : List α) := (hmem y).2 (by simp)
          cases hy_nil
  | cons x xs ih =>
      rw [List.nodup_cons] at hxs
      rcases hxs with ⟨hx_not_mem, hxs_nodup⟩
      have hx_mem_ys : x ∈ ys := (hmem x).1 (by simp)
      have hys_perm : ys.Perm (x :: ys.erase x) :=
        linearDiagonal_perm_cons_erase_of_mem x hx_mem_ys
      have hys_erase_nodup : (ys.erase x).Nodup := hys.erase x
      have hmem_tail : ∀ z, z ∈ xs ↔ z ∈ ys.erase x := by
        intro z
        constructor
        · intro hzxs
          have hzx : z ≠ x := by
            intro hzx
            exact hx_not_mem (by simpa [hzx] using hzxs)
          have hzys : z ∈ ys := (hmem z).1 (by simp [hzxs])
          exact (List.mem_erase_of_ne hzx).2 hzys
        · intro hzerase
          have hzys : z ∈ ys := List.mem_of_mem_erase hzerase
          have hz_cons : z ∈ x :: xs := (hmem z).2 hzys
          rw [List.mem_cons] at hz_cons
          rcases hz_cons with hzx | hzxs
          · have hx_in_erase : x ∈ ys.erase x := by
              simpa [hzx] using hzerase
            exact False.elim (hys.not_mem_erase hx_in_erase)
          · exact hzxs
      have htail_perm : xs.Perm (ys.erase x) :=
        ih hxs_nodup hys_erase_nodup hmem_tail
      exact (List.Perm.cons x htail_perm).trans hys_perm.symm

private theorem linearDiagonal_foldl_add_perm {β : Type u}
    (xs ys : List β) (f : β -> Rat) (hperm : xs.Perm ys) :
    xs.foldl (fun acc x => acc + f x) 0 =
      ys.foldl (fun acc x => acc + f x) 0 := by
  exact hperm.foldl_eq'
    (by
      intro x _hx y _hy z
      grind [Rat.add_assoc, Rat.add_comm, Rat.add_left_comm])
    0

private theorem linearDiagonal_foldl_add_filter_of_zero_acc {β : Type u}
    (xs : List β) (p : β -> Bool) (f : β -> Rat) (acc : Rat)
    (hzero : ∀ x, x ∈ xs -> p x = false -> f x = 0) :
    xs.foldl (fun acc x => acc + f x) acc =
      (xs.filter p).foldl (fun acc x => acc + f x) acc := by
  induction xs generalizing acc with
  | nil => rfl
  | cons x xs ih =>
      have htail : ∀ y, y ∈ xs -> p y = false -> f y = 0 := by
        intro y hy hpfalse
        exact hzero y (by simp [hy]) hpfalse
      cases hpx : p x
      · have hxzero : f x = 0 := hzero x (by simp) hpx
        simp [List.filter, hpx]
        rw [hxzero, Rat.add_zero]
        exact ih acc htail
      · simp [List.filter, hpx]
        exact ih (acc + f x) htail

private theorem linearDiagonal_foldl_add_filter_of_zero {β : Type u}
    (xs : List β) (p : β -> Bool) (f : β -> Rat)
    (hzero : ∀ x, x ∈ xs -> p x = false -> f x = 0) :
    xs.foldl (fun acc x => acc + f x) 0 =
      (xs.filter p).foldl (fun acc x => acc + f x) 0 := by
  exact linearDiagonal_foldl_add_filter_of_zero_acc xs p f 0 hzero

private theorem linearDiagonal_foldl_add_congr_acc {β : Type u}
    (xs : List β) (f g : β -> Rat) (acc : Rat)
    (hfg : ∀ x, x ∈ xs -> f x = g x) :
    xs.foldl (fun acc x => acc + f x) acc =
      xs.foldl (fun acc x => acc + g x) acc := by
  induction xs generalizing acc with
  | nil => rfl
  | cons x xs ih =>
      have hx : f x = g x := hfg x (by simp)
      have htail : ∀ y, y ∈ xs -> f y = g y := by
        intro y hy
        exact hfg y (by simp [hy])
      simp only [List.foldl_cons]
      rw [hx]
      exact ih (acc + g x) htail

private theorem linearDiagonal_foldl_add_congr {β : Type u}
    (xs : List β) (f g : β -> Rat)
    (hfg : ∀ x, x ∈ xs -> f x = g x) :
    xs.foldl (fun acc x => acc + f x) 0 =
      xs.foldl (fun acc x => acc + g x) 0 := by
  exact linearDiagonal_foldl_add_congr_acc xs f g 0 hfg

private theorem controlledHouseholder8BranchFiber_filter_perm
    (n : Nat) (s : Fin (gridSize n)) :
    ((List.finRange (8 * gridSize n)).filter
        (fun k : Fin (8 * gridSize n) =>
          decide (controlledHouseholder8SystemIndex n k = s))).Perm
      (controlledHouseholder8BranchFiber n s) := by
  apply linearDiagonal_perm_of_nodup_mem_iff
  · exact (List.filter_sublist
      (p := fun k : Fin (8 * gridSize n) =>
        decide (controlledHouseholder8SystemIndex n k = s))
      (l := List.finRange (8 * gridSize n))).nodup
      (linearDiagonal_finRange_nodup (8 * gridSize n))
  · exact controlledHouseholder8BranchFiber_nodup n s
  · intro k
    constructor
    · intro hk
      rw [List.mem_filter] at hk
      exact (controlledHouseholder8BranchFiber_mem_iff n s k).2
        (of_decide_eq_true hk.2)
    · intro hk
      rw [List.mem_filter]
      constructor
      · exact List.mem_finRange k
      · exact decide_eq_true_iff.mpr
          ((controlledHouseholder8BranchFiber_mem_iff n s k).1 hk)

private theorem controlledHouseholder8DirectSum_columnInner_productIndex
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (s : Fin (gridSize n))
    (ai aj : Fin 8) :
    BlockEncodingClassics.columnInner
      (controlledHouseholder8DirectSum n v)
      (BlockEncodingClassics.productIndex ai s)
      (BlockEncodingClassics.productIndex aj s) =
    BlockEncodingClassics.columnInner
      (householder8 (v s)) ai aj := by
  unfold BlockEncodingClassics.columnInner
  calc
    (List.finRange (8 * gridSize n)).foldl
        (fun acc k =>
          acc +
            controlledHouseholder8DirectSum n v k
                (BlockEncodingClassics.productIndex ai s) *
              controlledHouseholder8DirectSum n v k
                (BlockEncodingClassics.productIndex aj s))
        0 =
      ((List.finRange (8 * gridSize n)).filter
          (fun k : Fin (8 * gridSize n) =>
            decide (controlledHouseholder8SystemIndex n k = s))).foldl
        (fun acc k =>
          acc +
            controlledHouseholder8DirectSum n v k
                (BlockEncodingClassics.productIndex ai s) *
              controlledHouseholder8DirectSum n v k
                (BlockEncodingClassics.productIndex aj s))
        0 := by
          apply linearDiagonal_foldl_add_filter_of_zero
          intro k _hk hkfalse
          have hk_ne : controlledHouseholder8SystemIndex n k ≠ s :=
            decide_eq_false_iff_not.mp hkfalse
          exact controlledHouseholder8DirectSum_column_off_branch_summand_zero
            n v s (BlockEncodingClassics.productIndex ai s)
            (BlockEncodingClassics.productIndex aj s) k
            (controlledHouseholder8SystemIndex_productIndex n ai s)
            (controlledHouseholder8SystemIndex_productIndex n aj s) hk_ne
    _ =
      (controlledHouseholder8BranchFiber n s).foldl
        (fun acc k =>
          acc +
            controlledHouseholder8DirectSum n v k
                (BlockEncodingClassics.productIndex ai s) *
              controlledHouseholder8DirectSum n v k
                (BlockEncodingClassics.productIndex aj s))
        0 := by
          exact linearDiagonal_foldl_add_perm _ _
            (fun k : Fin (8 * gridSize n) =>
              controlledHouseholder8DirectSum n v k
                  (BlockEncodingClassics.productIndex ai s) *
                controlledHouseholder8DirectSum n v k
                  (BlockEncodingClassics.productIndex aj s))
            (controlledHouseholder8BranchFiber_filter_perm n s)
    _ =
      (List.finRange 8).foldl
        (fun acc a =>
          acc + householder8 (v s) a ai * householder8 (v s) a aj)
        0 := by
          unfold controlledHouseholder8BranchFiber
          rw [List.foldl_map]
          apply linearDiagonal_foldl_add_congr
          intro a _ha
          exact controlledHouseholder8DirectSum_column_summand_productIndex
            n v s a ai aj

/--
Support leaf `CDS-COL-FOLD`: inside one decoded system branch, the column inner
product of the controlled direct sum is the column inner product of that
branch's Householder block.
-/
theorem controlledHouseholder8DirectSum_columnInner_eq_branch
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (i j : Fin (8 * gridSize n))
    (hsys :
      controlledHouseholder8SystemIndex n i =
        controlledHouseholder8SystemIndex n j) :
    BlockEncodingClassics.columnInner
      (controlledHouseholder8DirectSum n v) i j =
    BlockEncodingClassics.columnInner
      (householder8 (v (controlledHouseholder8SystemIndex n i)))
      (controlledHouseholder8AncillaIndex n i)
      (controlledHouseholder8AncillaIndex n j) := by
  have hi :
      BlockEncodingClassics.productIndex
        (controlledHouseholder8AncillaIndex n i)
        (controlledHouseholder8SystemIndex n i) = i :=
    controlledHouseholder8_productIndex_eta n i
  have hj :
      BlockEncodingClassics.productIndex
        (controlledHouseholder8AncillaIndex n j)
        (controlledHouseholder8SystemIndex n i) = j := by
    rw [hsys]
    exact controlledHouseholder8_productIndex_eta n j
  calc
    BlockEncodingClassics.columnInner
        (controlledHouseholder8DirectSum n v) i j =
      BlockEncodingClassics.columnInner
        (controlledHouseholder8DirectSum n v)
        (BlockEncodingClassics.productIndex
          (controlledHouseholder8AncillaIndex n i)
          (controlledHouseholder8SystemIndex n i))
        (BlockEncodingClassics.productIndex
          (controlledHouseholder8AncillaIndex n j)
          (controlledHouseholder8SystemIndex n i)) := by
          rw [hi, hj]
    _ =
      BlockEncodingClassics.columnInner
        (householder8 (v (controlledHouseholder8SystemIndex n i)))
        (controlledHouseholder8AncillaIndex n i)
        (controlledHouseholder8AncillaIndex n j) :=
          controlledHouseholder8DirectSum_columnInner_productIndex
            n v (controlledHouseholder8SystemIndex n i)
            (controlledHouseholder8AncillaIndex n i)
            (controlledHouseholder8AncillaIndex n j)

private theorem controlledHouseholder8DirectSum_rowInner_productIndex
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (s : Fin (gridSize n))
    (ai aj : Fin 8) :
    BlockEncodingClassics.rowInner
      (controlledHouseholder8DirectSum n v)
      (BlockEncodingClassics.productIndex ai s)
      (BlockEncodingClassics.productIndex aj s) =
    BlockEncodingClassics.rowInner
      (householder8 (v s)) ai aj := by
  unfold BlockEncodingClassics.rowInner
  calc
    (List.finRange (8 * gridSize n)).foldl
        (fun acc k =>
          acc +
            controlledHouseholder8DirectSum n v
                (BlockEncodingClassics.productIndex ai s) k *
              controlledHouseholder8DirectSum n v
                (BlockEncodingClassics.productIndex aj s) k)
        0 =
      ((List.finRange (8 * gridSize n)).filter
          (fun k : Fin (8 * gridSize n) =>
            decide (controlledHouseholder8SystemIndex n k = s))).foldl
        (fun acc k =>
          acc +
            controlledHouseholder8DirectSum n v
                (BlockEncodingClassics.productIndex ai s) k *
              controlledHouseholder8DirectSum n v
                (BlockEncodingClassics.productIndex aj s) k)
        0 := by
          apply linearDiagonal_foldl_add_filter_of_zero
          intro k _hk hkfalse
          have hk_ne : controlledHouseholder8SystemIndex n k ≠ s :=
            decide_eq_false_iff_not.mp hkfalse
          exact controlledHouseholder8DirectSum_row_off_branch_summand_zero
            n v s (BlockEncodingClassics.productIndex ai s)
            (BlockEncodingClassics.productIndex aj s) k
            (controlledHouseholder8SystemIndex_productIndex n ai s)
            (controlledHouseholder8SystemIndex_productIndex n aj s) hk_ne
    _ =
      (controlledHouseholder8BranchFiber n s).foldl
        (fun acc k =>
          acc +
            controlledHouseholder8DirectSum n v
                (BlockEncodingClassics.productIndex ai s) k *
              controlledHouseholder8DirectSum n v
                (BlockEncodingClassics.productIndex aj s) k)
        0 := by
          exact linearDiagonal_foldl_add_perm _ _
            (fun k : Fin (8 * gridSize n) =>
              controlledHouseholder8DirectSum n v
                  (BlockEncodingClassics.productIndex ai s) k *
                controlledHouseholder8DirectSum n v
                  (BlockEncodingClassics.productIndex aj s) k)
            (controlledHouseholder8BranchFiber_filter_perm n s)
    _ =
      (List.finRange 8).foldl
        (fun acc a =>
          acc + householder8 (v s) ai a * householder8 (v s) aj a)
        0 := by
          unfold controlledHouseholder8BranchFiber
          rw [List.foldl_map]
          apply linearDiagonal_foldl_add_congr
          intro a _ha
          exact controlledHouseholder8DirectSum_row_summand_productIndex
            n v s a ai aj

/--
Support leaf `CDS-ROW-FOLD`: inside one decoded system branch, the row inner
product of the controlled direct sum is the row inner product of that branch's
Householder block.
-/
theorem controlledHouseholder8DirectSum_rowInner_eq_branch
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (i j : Fin (8 * gridSize n))
    (hsys :
      controlledHouseholder8SystemIndex n i =
        controlledHouseholder8SystemIndex n j) :
    BlockEncodingClassics.rowInner
      (controlledHouseholder8DirectSum n v) i j =
    BlockEncodingClassics.rowInner
      (householder8 (v (controlledHouseholder8SystemIndex n i)))
      (controlledHouseholder8AncillaIndex n i)
      (controlledHouseholder8AncillaIndex n j) := by
  have hi :
      BlockEncodingClassics.productIndex
        (controlledHouseholder8AncillaIndex n i)
        (controlledHouseholder8SystemIndex n i) = i :=
    controlledHouseholder8_productIndex_eta n i
  have hj :
      BlockEncodingClassics.productIndex
        (controlledHouseholder8AncillaIndex n j)
        (controlledHouseholder8SystemIndex n i) = j := by
    rw [hsys]
    exact controlledHouseholder8_productIndex_eta n j
  calc
    BlockEncodingClassics.rowInner
        (controlledHouseholder8DirectSum n v) i j =
      BlockEncodingClassics.rowInner
        (controlledHouseholder8DirectSum n v)
        (BlockEncodingClassics.productIndex
          (controlledHouseholder8AncillaIndex n i)
          (controlledHouseholder8SystemIndex n i))
        (BlockEncodingClassics.productIndex
          (controlledHouseholder8AncillaIndex n j)
          (controlledHouseholder8SystemIndex n i)) := by
          rw [hi, hj]
    _ =
      BlockEncodingClassics.rowInner
        (householder8 (v (controlledHouseholder8SystemIndex n i)))
        (controlledHouseholder8AncillaIndex n i)
        (controlledHouseholder8AncillaIndex n j) :=
          controlledHouseholder8DirectSum_rowInner_productIndex
            n v (controlledHouseholder8SystemIndex n i)
            (controlledHouseholder8AncillaIndex n i)
            (controlledHouseholder8AncillaIndex n j)

/--
Row-inner bridge for the controlled Householder direct sum in the cross-branch
case.

This completes the branch split needed by
`controlledHouseholder8DirectSum_isRationalOrthogonal`: if two rows belong to
different decoded system branches, no summation path can hit both blocks.
-/
theorem controlledHouseholder8DirectSum_rowInner_eq_identity_of_system_ne
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (i j : Fin (8 * gridSize n))
    (hsys :
      controlledHouseholder8SystemIndex n i ≠
        controlledHouseholder8SystemIndex n j) :
    BlockEncodingClassics.rowInner (controlledHouseholder8DirectSum n v) i j =
      Matrix.identity (8 * gridSize n) Rat i j := by
  have hzero :
      BlockEncodingClassics.rowInner (controlledHouseholder8DirectSum n v) i j = 0 := by
    unfold BlockEncodingClassics.rowInner
    exact linearDiagonal_foldl_add_zero_of_all_zero
      (List.finRange (8 * gridSize n))
      (fun k : Fin (8 * gridSize n) =>
        controlledHouseholder8DirectSum n v i k *
          controlledHouseholder8DirectSum n v j k)
      0
      (by
        intro k _hmem
        by_cases hik :
            controlledHouseholder8SystemIndex n i =
              controlledHouseholder8SystemIndex n k
        · have hjk_ne : controlledHouseholder8SystemIndex n j ≠
              controlledHouseholder8SystemIndex n k := by
            intro hjk
            exact hsys (hik.trans hjk.symm)
          simp [controlledHouseholder8DirectSum, hik, hjk_ne]
        · simp [controlledHouseholder8DirectSum, hik])
  rw [hzero]
  have hij : i ≠ j := by
    intro hij
    exact hsys (by simp [hij])
  simp [Matrix.identity, hij]

/--
Active leaf `HINT-CONTROLLED-DIRECT-SUM-ORTHO`: branchwise rational
orthogonality for the controlled direct sum of supplied 8-dimensional
Householder blocks.
-/
theorem controlledHouseholder8DirectSum_isRationalOrthogonal
    (n : Nat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (branchUnit :
      forall j : Fin (gridSize n), dot8 (v j) (v j) = 1)
    (branchNontrivial :
      forall j : Fin (gridSize n), v j householderZero ≠ 1) :
    BlockEncodingClassics.IsRationalOrthogonal
      (controlledHouseholder8DirectSum n v) := by
  constructor
  · intro i j
    by_cases hsys :
        controlledHouseholder8SystemIndex n i =
          controlledHouseholder8SystemIndex n j
    · rw [controlledHouseholder8DirectSum_columnInner_eq_branch n v i j hsys]
      have hbranch :=
        (householder8_isRationalOrthogonal
          (v (controlledHouseholder8SystemIndex n i))
          (branchUnit (controlledHouseholder8SystemIndex n i))
          (branchNontrivial (controlledHouseholder8SystemIndex n i))).1
          (controlledHouseholder8AncillaIndex n i)
          (controlledHouseholder8AncillaIndex n j)
      rw [hbranch]
      exact (controlledHouseholder8_identity_same_branch n i j hsys).symm
    · exact controlledHouseholder8DirectSum_columnInner_eq_identity_of_system_ne n v i j hsys
  · intro i j
    by_cases hsys :
        controlledHouseholder8SystemIndex n i =
          controlledHouseholder8SystemIndex n j
    · rw [controlledHouseholder8DirectSum_rowInner_eq_branch n v i j hsys]
      have hbranch :=
        (householder8_isRationalOrthogonal
          (v (controlledHouseholder8SystemIndex n i))
          (branchUnit (controlledHouseholder8SystemIndex n i))
          (branchNontrivial (controlledHouseholder8SystemIndex n i))).2
          (controlledHouseholder8AncillaIndex n i)
          (controlledHouseholder8AncillaIndex n j)
      rw [hbranch]
      exact (controlledHouseholder8_identity_same_branch n i j hsys).symm
    · exact controlledHouseholder8DirectSum_rowInner_eq_identity_of_system_ne n v i j hsys

/--
Branch-vector completion contract for the rational Householder backend of
the hinted linear diagonal input `O_0`.

This predicate records only the supplied vector family needed by the compiled
Householder direct-sum support.  Existence for every grid point remains blocked
on the cited four-squares obligation.
-/
def LinearDiagonalRationalCompletion (n : Nat) : Prop :=
  exists v : Fin (gridSize n) -> Fin 8 -> Rat,
    (forall j : Fin (gridSize n), dot8 (v j) (v j) = 1) ∧
    (forall j : Fin (gridSize n),
      v j householderZero = CubicStatePreparation.gridPoint n j)

/--
Branch vector obtained from a four-square completion of the residual
`(2^n)^2 - j^2`.

The first coordinate is the grid value `j / 2^n`; the next four coordinates
carry the rationalized square witnesses.
-/
def linearDiagonalFourSquareBranchVector
    (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) : Fin 8 -> Rat :=
  fun i =>
    if i = (0 : Fin 8) then (j.val : Rat) / (gridSize n : Rat)
    else if i = (1 : Fin 8) then (a : Rat) / (gridSize n : Rat)
    else if i = (2 : Fin 8) then (b : Rat) / (gridSize n : Rat)
    else if i = (3 : Fin 8) then (c : Rat) / (gridSize n : Rat)
    else if i = (4 : Fin 8) then (d : Rat) / (gridSize n : Rat)
    else 0

theorem linearDiagonalFourSquareBranchVector_clean
    (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) :
    linearDiagonalFourSquareBranchVector n j a b c d householderZero =
      CubicStatePreparation.gridPoint n j := by
  simp [linearDiagonalFourSquareBranchVector, householderZero,
    CubicStatePreparation.gridPoint]

theorem linearDiagonalFourSquareBranchVector_unit
    (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat)
    (hsq :
      gridSize n ^ 2 =
        j.val ^ 2 + a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) :
    dot8 (linearDiagonalFourSquareBranchVector n j a b c d)
      (linearDiagonalFourSquareBranchVector n j a b c d) = 1 := by
  unfold dot8 linearDiagonalFourSquareBranchVector
  have hsqRat :
      (gridSize n : Rat) ^ 2 =
        (j.val : Rat) ^ 2 + (a : Rat) ^ 2 + (b : Rat) ^ 2 +
          (c : Rat) ^ 2 + (d : Rat) ^ 2 := by
    simpa using congrArg (fun x : Nat => (x : Rat)) hsq
  have hNne : (gridSize n : Rat) ≠ 0 :=
    CubicStatePreparation.gridSize_rat_ne_zero n
  grind [Rat.div_def, Rat.pow_succ, Rat.mul_assoc, Rat.mul_comm,
    Rat.add_assoc, Rat.add_comm, Rat.add_left_comm]

/--
Adapter from explicit four-square witnesses to the rational-completion
predicate.  This is the local consumer of the still-external
`Nat.sum_four_squares` dependency; it does not prove that the witnesses exist.
-/
theorem linearDiagonalRationalCompletion_of_fourSquareWitnesses
    (n : Nat)
    (a b c d : Fin (gridSize n) -> Nat)
    (hsq : forall j : Fin (gridSize n),
      gridSize n ^ 2 =
        j.val ^ 2 + a j ^ 2 + b j ^ 2 + c j ^ 2 + d j ^ 2) :
    LinearDiagonalRationalCompletion n := by
  refine ⟨fun j => linearDiagonalFourSquareBranchVector n j (a j) (b j) (c j) (d j),
    ?_, ?_⟩
  · intro j
    exact linearDiagonalFourSquareBranchVector_unit n j (a j) (b j) (c j) (d j)
      (hsq j)
  · intro j
    exact linearDiagonalFourSquareBranchVector_clean n j (a j) (b j) (c j) (d j)

/--
Every dyadic grid value has an unconditional rational unit-vector completion.
The only number-theoretic ingredient is Lagrange's four-square theorem applied
to `gridSize n ^ 2 - j.val ^ 2`.
-/
theorem linearDiagonalRationalCompletion_exists (n : Nat) :
    LinearDiagonalRationalCompletion n := by
  classical
  choose a b c d habcd using fun j : Fin (gridSize n) =>
    Nat.sum_four_squares (gridSize n ^ 2 - j.val ^ 2)
  apply linearDiagonalRationalCompletion_of_fourSquareWitnesses n a b c d
  intro j
  have hj : j.val ^ 2 ≤ gridSize n ^ 2 :=
    Nat.pow_le_pow_left (Nat.le_of_lt j.isLt) 2
  have hsplit : j.val ^ 2 + (gridSize n ^ 2 - j.val ^ 2) = gridSize n ^ 2 :=
    Nat.add_sub_of_le hj
  calc
    gridSize n ^ 2 = j.val ^ 2 + (gridSize n ^ 2 - j.val ^ 2) := hsplit.symm
    _ = j.val ^ 2 +
        (a j ^ 2 + b j ^ 2 + c j ^ 2 + d j ^ 2) := by rw [habcd j]
    _ = j.val ^ 2 + a j ^ 2 + b j ^ 2 + c j ^ 2 + d j ^ 2 := by omega

/--
Adapter leaf for `HINT-O0-RATIONAL-COMPLETION`: a rational-completion witness
also supplies the nontrivial clean-coordinate side condition needed by the
Householder block.
-/
theorem linearDiagonalRationalCompletion_branchData
    (n : Nat)
    (h : LinearDiagonalRationalCompletion n) :
    exists v : Fin (gridSize n) -> Fin 8 -> Rat,
      (forall j : Fin (gridSize n), dot8 (v j) (v j) = 1) ∧
      (forall j : Fin (gridSize n),
        v j householderZero = CubicStatePreparation.gridPoint n j) ∧
      (forall j : Fin (gridSize n), v j householderZero ≠ 1) := by
  rcases h with ⟨v, branchUnit, branchClean⟩
  exact ⟨v, branchUnit, branchClean,
    controlledHouseholder8_branchNontrivial_of_clean n v branchClean⟩

/--
A rational-completion witness supplies the clean-block equality and rational
orthogonality facts for the controlled Householder direct sum.

This still does not package a complete `LinearDiagonalInputBEContract`: cleanup
integration, normalizer/resource fields, and a concrete existence theorem are
separate proof obligations.
-/
theorem linearDiagonalRationalCompletion_backendSupport
    (n : Nat)
    (h : LinearDiagonalRationalCompletion n) :
    exists v : Fin (gridSize n) -> Fin 8 -> Rat,
      Matrix.PointwiseEq
        (BlockEncodingClassics.cleanBlockBy
          (controlledHouseholder8Embed n)
          (controlledHouseholder8DirectSum n v))
        (linearDiagonalOperator n) ∧
      BlockEncodingClassics.IsRationalOrthogonal
        (controlledHouseholder8DirectSum n v) := by
  rcases h with ⟨v, branchUnit, branchClean⟩
  have branchNontrivial :
      forall j : Fin (gridSize n), v j householderZero ≠ 1 :=
    controlledHouseholder8_branchNontrivial_of_clean n v branchClean
  exact ⟨v,
    controlledHouseholder8DirectSum_clean_entry n v branchUnit branchClean
      branchNontrivial,
    controlledHouseholder8DirectSum_isRationalOrthogonal n v branchUnit
      branchNontrivial⟩

/-- Oracle-label circuit for the proved rational Householder realization of `O_0`. -/
def linearDiagonalHouseholderCircuit (_n : Nat) : Circuit :=
  [Gate.oracleCall "controlled-rational-householder-linear-diagonal"]

def linearDiagonalHouseholderResource (n : Nat) : Resource :=
  (linearDiagonalHouseholderCircuit n).resource

theorem linearDiagonalHouseholderResource_eq (n : Nat) :
    linearDiagonalHouseholderResource n =
      Resource.ofCountsWithDepth 0 0 1 0 1 := by
  rfl

/--
Unconditional exact matrix-level block encoding of the hinted input `O_0`.

Unlike the earlier interface-only payload, this certificate contains the
concrete controlled Householder matrix, its rational orthogonality theorem,
the clean-block theorem, the exact normalizer, and an auditable oracle-label
resource equality.
-/
noncomputable def linearDiagonalHouseholderInputBEContract (n : Nat) :
    LinearDiagonalInputBEContract n (8 * gridSize n) := by
  classical
  let support := linearDiagonalRationalCompletion_backendSupport n
    (linearDiagonalRationalCompletion_exists n)
  let v := Classical.choose support
  have hv := Classical.choose_spec support
  have hclean := hv.1
  have horthogonal := hv.2
  exact {
    U := controlledHouseholder8DirectSum n v
    embed := controlledHouseholder8Embed n
    unitaryProof := horthogonal
    cleanupStatement :=
      Matrix.PointwiseEq
        (BlockEncodingClassics.cleanBlockBy
          (controlledHouseholder8Embed n)
          (controlledHouseholder8DirectSum n v))
        (linearDiagonalOperator n)
    cleanupDescription :=
      "block-diagonal Householder branches preserve the system index and use no workspace"
    cleanupProof := hclean
    cleanBlockProof := hclean
    normalizerProof := rfl
    resource := linearDiagonalHouseholderResource n
    resourceStatement :=
      linearDiagonalHouseholderResource n =
        Resource.ofCountsWithDepth 0 0 1 0 1
    resourceProof := linearDiagonalHouseholderResource_eq n
  }

theorem linearDiagonalHouseholderInputBEContract_clean_eq_target (n : Nat) :
    Matrix.PointwiseEq
      (BlockEncodingClassics.ExactCleanBlock.clean
        (linearDiagonalHouseholderInputBEContract n).exactPayload)
      (linearDiagonalTarget n).operator := by
  exact (linearDiagonalHouseholderInputBEContract n).clean_eq_target

/--
Root certificate for the hinted input operator `O_0`.  This theorem exposes
all matrix-level facts needed by a downstream polynomial consumer in one
place, so the harness does not reopen the four-square, Householder, cleanup,
normalizer, or resource leaves after they have compiled.
-/
theorem linearDiagonalHouseholderInputBEContract_complete (n : Nat) :
    BlockEncodingClassics.IsRationalOrthogonal
        (linearDiagonalHouseholderInputBEContract n).U ∧
      Matrix.PointwiseEq
        (BlockEncodingClassics.cleanBlockBy
          (linearDiagonalHouseholderInputBEContract n).embed
          (linearDiagonalHouseholderInputBEContract n).U)
        (linearDiagonalTarget n).operator ∧
      (linearDiagonalTarget n).normalizer = 1 ∧
      (linearDiagonalHouseholderInputBEContract n).resource =
        Resource.ofCountsWithDepth 0 0 1 0 1 := by
  refine ⟨(linearDiagonalHouseholderInputBEContract n).unitaryProof, ?_,
    (linearDiagonalHouseholderInputBEContract n).normalizerProof,
    (linearDiagonalHouseholderInputBEContract n).resourceProof⟩
  simpa [linearDiagonalTarget] using
    (linearDiagonalHouseholderInputBEContract n).cleanBlockProof

/--
Supplied diagonal matrix for the first Scenario 2 approximate route.

The function `q` is only a proposed rational diagonal value.  Approximation to
the cubic target and the operator-norm bridge remain separate obligations.
-/
def approxDiagonalOperator (n : Nat) (q : Fin (gridSize n) -> Rat) :
    Matrix (gridSize n) (gridSize n) Rat :=
  fun row col => if row = col then q row else 0

/-- Task-local rational absolute value used before a project norm API exists. -/
def ratAbs (x : Rat) : Rat := if 0 ≤ x then x else -x

/-- Project-local rational matrices whose off-diagonal entries are zero. -/
def IsDiagonalRatMatrix (dim : Nat) (A : Matrix dim dim Rat) : Prop :=
  ∀ row col : Fin dim, row ≠ col -> A row col = 0

/--
Typed contract for the missing rational-matrix operator-norm bridge.

This structure is deliberately conditional: it does not assert that the bridge
is already available in this repository.  A future Mathlib-backed proof or a
human-accepted external contract must supply this record before an approximate
block-encoding certificate may consume the norm bound.
-/
structure DiagonalRatOperatorNormBridge (dim : Nat) where
  opNormErrorAtMost : Matrix dim dim Rat -> Matrix dim dim Rat -> Rat -> Prop
  diagonal_entrywise_error_operatorNorm_le :
    ∀ (A B : Matrix dim dim Rat) (epsilon : Rat),
      IsDiagonalRatMatrix dim A ->
      IsDiagonalRatMatrix dim B ->
      0 ≤ epsilon ->
      (∀ j : Fin dim, ratAbs (A j j - B j j) ≤ epsilon) ->
      opNormErrorAtMost A B epsilon

/-- Squared Euclidean norm on project-local finite rational vectors. -/
def ratSquaredEuclideanNorm {dim : Nat} (v : Fin dim -> Rat) : Rat :=
  (List.finRange dim).foldl (fun acc j => acc + v j * v j) 0

/-- Action of the matrix error `A - B` on a finite rational vector. -/
def ratMatrixErrorAction {dim : Nat}
    (A B : Matrix dim dim Rat) (v : Fin dim -> Rat) : Fin dim -> Rat :=
  fun row =>
    (List.finRange dim).foldl
      (fun acc col => acc + (A row col - B row col) * v col) 0

/--
Non-vacuous squared Euclidean induced operator-norm error semantics.

For nonnegative `epsilon`, this states `||(A-B)v||₂² ≤ ||epsilon v||₂²`
for every rational vector `v`.  Squared norms avoid introducing square roots
while retaining the finite-dimensional Euclidean operator-norm statement.
-/
def ratEuclideanOperatorNormErrorAtMost {dim : Nat}
    (A B : Matrix dim dim Rat) (epsilon : Rat) : Prop :=
  0 ≤ epsilon ∧
    ∀ v : Fin dim -> Rat,
      ratSquaredEuclideanNorm (ratMatrixErrorAction A B v) ≤
        ratSquaredEuclideanNorm (fun j => epsilon * v j)

private theorem diagonalFoldlAddZero {β : Type u}
    (xs : List β) (f : β -> Rat) (acc : Rat)
    (hzero : ∀ x, x ∈ xs -> f x = 0) :
    xs.foldl (fun total x => total + f x) acc = acc := by
  induction xs generalizing acc with
  | nil => rfl
  | cons x xs ih =>
      have hx : f x = 0 := hzero x (by simp)
      have htail : ∀ y, y ∈ xs -> f y = 0 := by
        intro y hy
        exact hzero y (by simp [hy])
      calc
        (x :: xs).foldl (fun total x => total + f x) acc =
            xs.foldl (fun total x => total + f x) (acc + f x) := rfl
        _ = xs.foldl (fun total x => total + f x) acc := by
          rw [hx, Rat.add_zero]
        _ = acc := ih acc htail

private theorem diagonalFoldlAddUnique {β : Type u} [DecidableEq β]
    (xs : List β) (f : β -> Rat) (x0 : β)
    (hnodup : xs.Nodup) (hmem : x0 ∈ xs)
    (hzero : ∀ x, x ∈ xs -> x ≠ x0 -> f x = 0) :
    xs.foldl (fun total x => total + f x) 0 = f x0 := by
  induction xs with
  | nil => cases hmem
  | cons x xs ih =>
      rw [List.nodup_cons] at hnodup
      rcases hnodup with ⟨hx_not_mem, hxs_nodup⟩
      rw [List.mem_cons] at hmem
      rcases hmem with hhead | htailmem
      · subst hhead
        have htail_zero : ∀ y, y ∈ xs -> f y = 0 := by
          intro y hy
          have hyne : y ≠ x0 := by
            intro heq
            apply hx_not_mem
            simpa [heq] using hy
          exact hzero y (by simp [hy]) hyne
        calc
          (x0 :: xs).foldl (fun total x => total + f x) 0 =
              xs.foldl (fun total x => total + f x) (0 + f x0) := rfl
          _ = xs.foldl (fun total x => total + f x) (f x0) := by
            rw [Rat.zero_add]
          _ = f x0 := diagonalFoldlAddZero xs f (f x0) htail_zero
      · have hxzero : f x = 0 := by
          have hxne : x ≠ x0 := by
            intro heq
            apply hx_not_mem
            simpa [heq] using htailmem
          exact hzero x (by simp) hxne
        have htail_zero : ∀ y, y ∈ xs -> y ≠ x0 -> f y = 0 := by
          intro y hy hyne
          exact hzero y (by simp [hy]) hyne
        calc
          (x :: xs).foldl (fun total x => total + f x) 0 =
              xs.foldl (fun total x => total + f x) (0 + f x) := rfl
          _ = xs.foldl (fun total x => total + f x) 0 := by
            rw [hxzero, Rat.zero_add]
          _ = f x0 := ih hxs_nodup htailmem htail_zero

private theorem diagonalNodupMapOfInjective {α : Type u} {β : Type v}
    [DecidableEq β] {f : α -> β} (hf : Function.Injective f)
    {xs : List α} (hxs : xs.Nodup) : (xs.map f).Nodup := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      rw [List.nodup_cons] at hxs
      rcases hxs with ⟨hx_not_mem, hxs_nodup⟩
      change (f x :: xs.map f).Nodup
      rw [List.nodup_cons]
      constructor
      · intro hmem
        rcases List.mem_map.mp hmem with ⟨y, hy, hfy⟩
        apply hx_not_mem
        have hyx : y = x := hf hfy
        simpa [hyx] using hy
      · exact ih hxs_nodup

private theorem diagonalFinRangeNodup (dim : Nat) :
    (List.finRange dim).Nodup := by
  induction dim with
  | zero => simp [List.finRange_zero]
  | succ dim ih =>
      rw [List.finRange_succ, List.nodup_cons]
      constructor
      · intro hmem
        rcases List.mem_map.mp hmem with ⟨j, _hj, hjzero⟩
        exact Fin.succ_ne_zero j hjzero
      · apply diagonalNodupMapOfInjective
        · intro a b h
          apply Fin.eq_of_val_eq
          have hv := congrArg (fun x : Fin (dim + 1) => x.val) h
          simpa using Nat.succ.inj hv
        · exact ih

private theorem diagonalFoldlAddLe {β : Type u}
    (xs : List β) (f g : β -> Rat)
    (hpoint : ∀ x, x ∈ xs -> f x ≤ g x)
    (left right : Rat) (hacc : left ≤ right) :
    xs.foldl (fun acc x => acc + f x) left ≤
      xs.foldl (fun acc x => acc + g x) right := by
  induction xs generalizing left right with
  | nil => exact hacc
  | cons x xs ih =>
      have hx : f x ≤ g x := hpoint x (by simp)
      have htail : ∀ y, y ∈ xs -> f y ≤ g y := by
        intro y hy
        exact hpoint y (by simp [hy])
      have hleft : left + f x ≤ right + f x :=
        (Rat.add_le_add_right).mpr hacc
      have hright : right + f x ≤ right + g x :=
        (Rat.add_le_add_left).mpr hx
      exact ih htail (left + f x) (right + g x)
        (Rat.le_trans hleft hright)

theorem ratMatrixErrorAction_eq_diagonal {dim : Nat}
    (A B : Matrix dim dim Rat) (v : Fin dim -> Rat) (row : Fin dim)
    (hA : IsDiagonalRatMatrix dim A)
    (hB : IsDiagonalRatMatrix dim B) :
    ratMatrixErrorAction A B v row = (A row row - B row row) * v row := by
  unfold ratMatrixErrorAction
  apply diagonalFoldlAddUnique
  · exact diagonalFinRangeNodup dim
  · exact List.mem_finRange row
  · intro col _ hne
    have hrowcol : row ≠ col := Ne.symm hne
    rw [hA row col hrowcol, hB row col hrowcol]
    have hzero : (0 : Rat) - 0 = 0 := by exact Rat.sub_self
    rw [hzero, Rat.zero_mul]

theorem ratAbs_nonneg (x : Rat) : 0 ≤ ratAbs x := by
  unfold ratAbs
  split <;> grind

theorem rat_mul_self_eq_ratAbs_mul_self (x : Rat) :
    x * x = ratAbs x * ratAbs x := by
  unfold ratAbs
  split <;> grind

theorem rat_mul_self_nonneg (x : Rat) : 0 ≤ x * x := by
  rw [rat_mul_self_eq_ratAbs_mul_self]
  exact Rat.mul_nonneg (ratAbs_nonneg x) (ratAbs_nonneg x)

theorem rat_mul_self_le_of_abs_le (x epsilon : Rat)
    (hepsilon : 0 ≤ epsilon) (habs : ratAbs x ≤ epsilon) :
    x * x ≤ epsilon * epsilon := by
  rw [rat_mul_self_eq_ratAbs_mul_self]
  have hfirst : ratAbs x * ratAbs x ≤ epsilon * ratAbs x :=
    Rat.mul_le_mul_of_nonneg_right habs (ratAbs_nonneg x)
  have hsecond : epsilon * ratAbs x ≤ epsilon * epsilon :=
    Rat.mul_le_mul_of_nonneg_left habs hepsilon
  exact Rat.le_trans hfirst hsecond

private theorem rat_mul_product_self (a b : Rat) :
    (a * b) * (a * b) = (a * a) * (b * b) := by
  rw [Rat.mul_assoc]
  rw [← Rat.mul_assoc b a b]
  rw [Rat.mul_comm b a]
  rw [Rat.mul_assoc a b b]
  rw [← Rat.mul_assoc a a (b * b)]

theorem rat_mul_self_vector_le_of_abs_le (x epsilon value : Rat)
    (hepsilon : 0 ≤ epsilon) (habs : ratAbs x ≤ epsilon) :
    (x * value) * (x * value) ≤
      (epsilon * value) * (epsilon * value) := by
  rw [rat_mul_product_self, rat_mul_product_self]
  exact Rat.mul_le_mul_of_nonneg_right
    (rat_mul_self_le_of_abs_le x epsilon hepsilon habs)
    (rat_mul_self_nonneg value)

/-- Concrete proof that diagonal entrywise bounds imply the squared Euclidean bound. -/
def ratEuclideanDiagonalOperatorNormBridge (dim : Nat) :
    DiagonalRatOperatorNormBridge dim where
  opNormErrorAtMost := ratEuclideanOperatorNormErrorAtMost
  diagonal_entrywise_error_operatorNorm_le := by
    intro A B epsilon hA hB hepsilon hdiag
    refine ⟨hepsilon, ?_⟩
    intro v
    unfold ratSquaredEuclideanNorm
    apply diagonalFoldlAddLe
    · intro row _
      rw [ratMatrixErrorAction_eq_diagonal A B v row hA hB]
      exact rat_mul_self_vector_le_of_abs_le
        (A row row - B row row) epsilon (v row) hepsilon (hdiag row)
    · exact Rat.le_refl

/-- The local Euclidean error predicate is observably non-vacuous. -/
theorem ratEuclideanOperatorNormErrorAtMost_not_vacuous :
    ¬ ratEuclideanOperatorNormErrorAtMost
      (Matrix.identity 1 Rat) (Matrix.zero 1 1 Rat) 0 := by
  intro h
  have hunit := h.2 (fun _ => 1)
  have hnot :
      ¬ ratSquaredEuclideanNorm
          (ratMatrixErrorAction
            (Matrix.identity 1 Rat) (Matrix.zero 1 1 Rat) (fun _ => 1)) ≤
        ratSquaredEuclideanNorm (fun _ : Fin 1 => (0 : Rat) * 1) := by
    decide +kernel
  exact hnot hunit

/-- The supplied approximate diagonal matrix has zero off-diagonal entries. -/
theorem approxDiagonalOperator_isDiagonal
    (n : Nat) (q : Fin (gridSize n) -> Rat) :
    IsDiagonalRatMatrix (gridSize n) (approxDiagonalOperator n q) := by
  intro row col hne
  simp [approxDiagonalOperator, hne]

/-- The exact cubic diagonal target has zero off-diagonal entries. -/
theorem cubicDiagonalOperator_isDiagonal
    (n : Nat) :
    IsDiagonalRatMatrix (gridSize n) (cubicDiagonalOperator n) := by
  intro row col hne
  simp [cubicDiagonalOperator, hne]

/--
Entrywise scalar-error predicate for the Scenario 2 approximate diagonal route.

This is strictly weaker than the open operator-norm bridge: it says only that
each supplied diagonal value `q j` is close to the target cubic amplitude.
-/
def approxDiagonalEntrywiseErrorAtMost
    (n : Nat) (q : Fin (gridSize n) -> Rat) (epsilon : Rat) : Prop :=
  ∀ j : Fin (gridSize n),
    ratAbs (q j - CubicStatePreparation.cubicAmplitude n j) ≤ epsilon

/--
Local entrywise bridge for `APPROX-DIAG-NORM`: diagonal scalar errors transfer
to every matrix entry of the supplied diagonal operator.

This does not prove an operator-norm bound; it is the reusable finite-matrix
side of the still-open diagonal norm obligation.
-/
theorem approxDiagonalOperator_entrywise_error
    (n : Nat) (q : Fin (gridSize n) -> Rat) (epsilon : Rat)
    (hdiag : approxDiagonalEntrywiseErrorAtMost n q epsilon)
    (hepsilon : 0 ≤ epsilon) :
    ∀ row col : Fin (gridSize n),
      ratAbs
        (approxDiagonalOperator n q row col -
          cubicDiagonalOperator n row col) ≤ epsilon := by
  intro row col
  by_cases hrowcol : row = col
  · subst col
    simpa [approxDiagonalOperator, cubicDiagonalOperator,
      approxDiagonalEntrywiseErrorAtMost] using hdiag row
  · have hentry :
        approxDiagonalOperator n q row col -
          cubicDiagonalOperator n row col = 0 := by
      simp [approxDiagonalOperator, cubicDiagonalOperator, hrowcol]
    simpa [hentry, ratAbs] using hepsilon

/--
Conditional adapter from the compiled diagonal entrywise theorem to the
task-local operator-norm contract.

This theorem is the narrow QBE-side consumer promised by the proof DAG.  It
does not close `DIAGONAL-ENTRYWISE-ERROR-OPNORM` unconditionally; the supplied
`bridge` remains the explicit external/classical obligation.
-/
theorem approxDiagonalOperator_operatorNorm_error_of_contract
    (n : Nat) (q : Fin (gridSize n) -> Rat) (epsilon : Rat)
    (bridge : DiagonalRatOperatorNormBridge (gridSize n))
    (hdiag : approxDiagonalEntrywiseErrorAtMost n q epsilon)
    (hepsilon : 0 ≤ epsilon) :
    bridge.opNormErrorAtMost
      (approxDiagonalOperator n q)
      (cubicDiagonalOperator n)
      epsilon := by
  apply bridge.diagonal_entrywise_error_operatorNorm_le
  · exact approxDiagonalOperator_isDiagonal n q
  · exact cubicDiagonalOperator_isDiagonal n
  · exact hepsilon
  · intro j
    simpa [approxDiagonalOperator, cubicDiagonalOperator,
      approxDiagonalEntrywiseErrorAtMost] using hdiag j

/--
Unconditional local Euclidean operator-norm bound for the supplied diagonal
approximation.  This closes the former external bridge gap using the concrete
finite rational semantics above.
-/
theorem approxDiagonalOperator_operatorNorm_error
    (n : Nat) (q : Fin (gridSize n) -> Rat) (epsilon : Rat)
    (hdiag : approxDiagonalEntrywiseErrorAtMost n q epsilon)
    (hepsilon : 0 ≤ epsilon) :
    ratEuclideanOperatorNormErrorAtMost
      (approxDiagonalOperator n q)
      (cubicDiagonalOperator n)
      epsilon := by
  exact approxDiagonalOperator_operatorNorm_error_of_contract
    n q epsilon (ratEuclideanDiagonalOperatorNormBridge (gridSize n))
    hdiag hepsilon

/--
Two-coordinate rational unit-circle branch vector for the approximate
controlled-Householder route.
-/
def rationalCircleBranchVector (q r : Rat) : Fin 8 -> Rat :=
  fun i =>
    if i = (0 : Fin 8) then q
    else if i = (1 : Fin 8) then r
    else 0

theorem rationalCircleBranchVector_clean (q r : Rat) :
    rationalCircleBranchVector q r householderZero = q := by
  simp [rationalCircleBranchVector, householderZero]

theorem rationalCircleBranchVector_unit
    (q r : Rat)
    (hcircle : q ^ 2 + r ^ 2 = 1) :
    dot8 (rationalCircleBranchVector q r)
      (rationalCircleBranchVector q r) = 1 := by
  unfold dot8 rationalCircleBranchVector
  grind [Rat.pow_succ, Rat.add_assoc]

/--
Approximate-route support leaf `APPROX-CDS-CLEAN`: if each controlled
Householder branch has clean coordinate `q j`, then the clean block is the
supplied diagonal matrix `diag(q)`.

This is not an approximate certificate.  It proves only the local clean-block
shape for supplied branch vectors.
-/
theorem controlledHouseholder8DirectSum_clean_entry_of_branchValue
    (n : Nat)
    (q : Fin (gridSize n) -> Rat)
    (v : Fin (gridSize n) -> Fin 8 -> Rat)
    (branchUnit :
      forall j : Fin (gridSize n), dot8 (v j) (v j) = 1)
    (branchClean :
      forall j : Fin (gridSize n), v j householderZero = q j)
    (branchNontrivial :
      forall j : Fin (gridSize n), v j householderZero ≠ 1) :
    Matrix.PointwiseEq
      (BlockEncodingClassics.cleanBlockBy
        (controlledHouseholder8Embed n)
        (controlledHouseholder8DirectSum n v))
      (approxDiagonalOperator n q) := by
  intro row col
  by_cases hrowcol : row = col
  · subst col
    calc
      BlockEncodingClassics.cleanBlockBy
          (controlledHouseholder8Embed n)
          (controlledHouseholder8DirectSum n v) row row
          = householder8 (v row) householderZero householderZero := by
              simp [BlockEncodingClassics.cleanBlockBy,
                controlledHouseholder8DirectSum,
                controlledHouseholder8SystemIndex_embed,
                controlledHouseholder8AncillaIndex_embed]
      _ = v row householderZero :=
              householder8_clean_entry (v row) (branchUnit row)
                (branchNontrivial row)
      _ = q row := branchClean row
      _ = approxDiagonalOperator n q row row := by
              simp [approxDiagonalOperator]
  · have hsys_ne :
        controlledHouseholder8SystemIndex n
            (controlledHouseholder8Embed n row) ≠
          controlledHouseholder8SystemIndex n
            (controlledHouseholder8Embed n col) := by
      intro hsys
      have hrow : row = col := by
        rw [controlledHouseholder8SystemIndex_embed] at hsys
        rw [controlledHouseholder8SystemIndex_embed] at hsys
        exact hsys
      exact hrowcol hrow
    simp [BlockEncodingClassics.cleanBlockBy, controlledHouseholder8DirectSum,
      approxDiagonalOperator, hrowcol, hsys_ne]

/-- Rational branch vector whose clean coordinate is `(j / 2^n)^3`. -/
def cubicDiagonalFourSquareBranchVector
    (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) : Fin 8 -> Rat :=
  fun i =>
    if i = (0 : Fin 8) then (j.val : Rat) ^ 3 / (gridSize n : Rat) ^ 3
    else if i = (1 : Fin 8) then (a : Rat) / (gridSize n : Rat) ^ 3
    else if i = (2 : Fin 8) then (b : Rat) / (gridSize n : Rat) ^ 3
    else if i = (3 : Fin 8) then (c : Rat) / (gridSize n : Rat) ^ 3
    else if i = (4 : Fin 8) then (d : Rat) / (gridSize n : Rat) ^ 3
    else 0

theorem cubicDiagonalFourSquareBranchVector_clean
    (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat) :
    cubicDiagonalFourSquareBranchVector n j a b c d householderZero =
      CubicStatePreparation.cubicAmplitude n j := by
  simp only [cubicDiagonalFourSquareBranchVector, householderZero, if_pos]
  change (j.val : Rat) ^ 3 / (gridSize n : Rat) ^ 3 =
    ((j.val : Rat) / (gridSize n : Rat)) ^ 3
  exact (div_pow (j.val : Rat) (gridSize n : Rat) 3).symm

theorem cubicDiagonalFourSquareBranchVector_unit
    (n : Nat) (j : Fin (gridSize n)) (a b c d : Nat)
    (hsq :
      gridSize n ^ 6 =
        j.val ^ 6 + a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) :
    dot8 (cubicDiagonalFourSquareBranchVector n j a b c d)
      (cubicDiagonalFourSquareBranchVector n j a b c d) = 1 := by
  unfold dot8 cubicDiagonalFourSquareBranchVector
  have hsqRat :
      (gridSize n : Rat) ^ 6 =
        (j.val : Rat) ^ 6 + (a : Rat) ^ 2 + (b : Rat) ^ 2 +
          (c : Rat) ^ 2 + (d : Rat) ^ 2 := by
    simpa using congrArg (fun x : Nat => (x : Rat)) hsq
  have hNne : (gridSize n : Rat) ≠ 0 :=
    CubicStatePreparation.gridSize_rat_ne_zero n
  grind [Rat.div_def, Rat.pow_succ, Rat.mul_assoc, Rat.mul_comm,
    Rat.add_assoc, Rat.add_comm, Rat.add_left_comm]

def CubicDiagonalRationalCompletion (n : Nat) : Prop :=
  exists v : Fin (gridSize n) -> Fin 8 -> Rat,
    (forall j : Fin (gridSize n), dot8 (v j) (v j) = 1) ∧
    (forall j : Fin (gridSize n),
      v j householderZero = CubicStatePreparation.cubicAmplitude n j)

theorem cubicDiagonalRationalCompletion_of_fourSquareWitnesses
    (n : Nat)
    (a b c d : Fin (gridSize n) -> Nat)
    (hsq : forall j : Fin (gridSize n),
      gridSize n ^ 6 =
        j.val ^ 6 + a j ^ 2 + b j ^ 2 + c j ^ 2 + d j ^ 2) :
    CubicDiagonalRationalCompletion n := by
  refine ⟨fun j => cubicDiagonalFourSquareBranchVector n j (a j) (b j) (c j) (d j),
    ?_, ?_⟩
  · intro j
    exact cubicDiagonalFourSquareBranchVector_unit n j (a j) (b j) (c j) (d j)
      (hsq j)
  · intro j
    exact cubicDiagonalFourSquareBranchVector_clean n j (a j) (b j) (c j) (d j)

theorem cubicDiagonalRationalCompletion_exists (n : Nat) :
    CubicDiagonalRationalCompletion n := by
  classical
  choose a b c d habcd using fun j : Fin (gridSize n) =>
    Nat.sum_four_squares (gridSize n ^ 6 - j.val ^ 6)
  apply cubicDiagonalRationalCompletion_of_fourSquareWitnesses n a b c d
  intro j
  have hj : j.val ^ 6 ≤ gridSize n ^ 6 :=
    Nat.pow_le_pow_left (Nat.le_of_lt j.isLt) 6
  have hsplit : j.val ^ 6 + (gridSize n ^ 6 - j.val ^ 6) = gridSize n ^ 6 :=
    Nat.add_sub_of_le hj
  calc
    gridSize n ^ 6 = j.val ^ 6 + (gridSize n ^ 6 - j.val ^ 6) := hsplit.symm
    _ = j.val ^ 6 +
        (a j ^ 2 + b j ^ 2 + c j ^ 2 + d j ^ 2) := by rw [habcd j]
    _ = j.val ^ 6 + a j ^ 2 + b j ^ 2 + c j ^ 2 + d j ^ 2 := by omega

theorem cubicAmplitude_lt_one
    (n : Nat) (j : Fin (gridSize n)) :
    CubicStatePreparation.cubicAmplitude n j < 1 := by
  let x := CubicStatePreparation.gridPoint n j
  have hx0 : 0 ≤ x := CubicStatePreparation.gridPoint_nonneg n j
  have hx1 : x < 1 := CubicStatePreparation.gridPoint_lt_one n j
  have hx2 : x ^ 2 ≤ 1 :=
    CubicStatePreparation.rat_pow_le_one_of_nonneg_le_one x 2 hx0
      (Rat.le_of_lt hx1)
  have hmul : x ^ 2 * x ≤ 1 * x :=
    Rat.mul_le_mul_of_nonneg_right hx2 hx0
  have hcube : x ^ 3 ≤ x := by
    simpa [Rat.pow_succ] using hmul
  simpa [CubicStatePreparation.cubicAmplitude, x] using
    (lt_of_le_of_lt hcube hx1)

theorem cubicDiagonalRationalCompletion_backendSupport
    (n : Nat) :
    exists v : Fin (gridSize n) -> Fin 8 -> Rat,
      Matrix.PointwiseEq
        (BlockEncodingClassics.cleanBlockBy
          (controlledHouseholder8Embed n)
          (controlledHouseholder8DirectSum n v))
        (cubicDiagonalOperator n) ∧
      BlockEncodingClassics.IsRationalOrthogonal
        (controlledHouseholder8DirectSum n v) := by
  rcases cubicDiagonalRationalCompletion_exists n with ⟨v, branchUnit, branchClean⟩
  have branchNontrivial :
      forall j : Fin (gridSize n), v j householderZero ≠ 1 := by
    intro j h
    have hlt := cubicAmplitude_lt_one n j
    rw [← branchClean j, h] at hlt
    exact (lt_irrefl (1 : Rat)) hlt
  exact ⟨v,
    (by
      intro row col
      have h := controlledHouseholder8DirectSum_clean_entry_of_branchValue
        n (fun j => CubicStatePreparation.cubicAmplitude n j) v
        branchUnit branchClean branchNontrivial row col
      simpa [approxDiagonalOperator, cubicDiagonalOperator] using h),
    controlledHouseholder8DirectSum_isRationalOrthogonal
      n v branchUnit branchNontrivial⟩

/-- Strong exact certificate for the cubic target, including orthogonality. -/
structure CubicDiagonalExactBEContract (n total : Nat) where
  exactPayload : BlockEncodingClassics.ExactCleanBlock (gridSize n) total
  unitaryProof : BlockEncodingClassics.IsRationalOrthogonal exactPayload.U
  normalizerProof : (cubicDiagonalTarget n).normalizer = 1
  cleanupStatement : Prop
  cleanupProof : cleanupStatement
  resource : Resource
  resourceStatement : Prop
  resourceProof : resourceStatement

noncomputable def cubicDiagonalHouseholderExactBEContract (n : Nat) :
    CubicDiagonalExactBEContract n (8 * gridSize n) := by
  classical
  let support := cubicDiagonalRationalCompletion_backendSupport n
  let v := Classical.choose support
  have hv := Classical.choose_spec support
  exact {
    exactPayload := {
      U := controlledHouseholder8DirectSum n v
      A := cubicDiagonalOperator n
      embed := controlledHouseholder8Embed n
      blockProof := hv.1
    }
    unitaryProof := hv.2
    normalizerProof := rfl
    cleanupStatement :=
      Matrix.PointwiseEq
        (BlockEncodingClassics.cleanBlockBy
          (controlledHouseholder8Embed n)
          (controlledHouseholder8DirectSum n v))
        (cubicDiagonalOperator n)
    cleanupProof := hv.1
    resource := linearDiagonalHouseholderResource n
    resourceStatement :=
      linearDiagonalHouseholderResource n =
        Resource.ofCountsWithDepth 0 0 1 0 1
    resourceProof := linearDiagonalHouseholderResource_eq n
  }

theorem cubicDiagonalHouseholderExactBEContract_clean_eq_target (n : Nat) :
    Matrix.PointwiseEq
      (cubicDiagonalHouseholderExactBEContract n).exactPayload.clean
      (cubicDiagonalTarget n).operator := by
  exact (cubicDiagonalHouseholderExactBEContract n).exactPayload.blockProof

/--
Unconditional exact root certificate for the cubic diagonal operator.  The
conjunction deliberately includes the unitary predicate, clean-block target,
normalizer, and resource equality; a clean-block-only arithmetic wrapper is
not sufficient to close an operator block-encoding task.
-/
theorem cubicDiagonalHouseholderExactBEContract_complete (n : Nat) :
    BlockEncodingClassics.IsRationalOrthogonal
        (cubicDiagonalHouseholderExactBEContract n).exactPayload.U ∧
      Matrix.PointwiseEq
        (cubicDiagonalHouseholderExactBEContract n).exactPayload.clean
        (cubicDiagonalTarget n).operator ∧
      (cubicDiagonalTarget n).normalizer = 1 ∧
      (cubicDiagonalHouseholderExactBEContract n).resource =
        Resource.ofCountsWithDepth 0 0 1 0 1 := by
  exact ⟨
    (cubicDiagonalHouseholderExactBEContract n).unitaryProof,
    cubicDiagonalHouseholderExactBEContract_clean_eq_target n,
    (cubicDiagonalHouseholderExactBEContract n).normalizerProof,
    (cubicDiagonalHouseholderExactBEContract n).resourceProof
  ⟩

private theorem linearDiagonal_foldl_add_unique_finRange {n : Nat}
    (f : Fin n -> Rat) (k0 : Fin n)
    (hzero : ∀ k : Fin n, k ≠ k0 -> f k = 0) :
    (List.finRange n).foldl (fun acc k => acc + f k) 0 = f k0 := by
  exact linearDiagonal_foldl_add_unique_of_nodup (List.finRange n) f k0
    (linearDiagonal_finRange_nodup n) (List.mem_finRange k0)
    (by
      intro k _hmem hne
      exact hzero k hne)

private theorem linearDiagonal_mul_entry (n : Nat)
    (row col : Fin (gridSize n)) :
    Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n) row col =
      if row = col then
        CubicStatePreparation.gridPoint n row * CubicStatePreparation.gridPoint n row
      else 0 := by
  unfold Matrix.mul linearDiagonalOperator
  by_cases h : row = col
  · subst col
    rw [if_pos rfl]
    have hunique := linearDiagonal_foldl_add_unique_finRange
      (fun k : Fin (gridSize n) =>
        (if row = k then CubicStatePreparation.gridPoint n row else 0) *
          if k = row then CubicStatePreparation.gridPoint n k else 0)
      row
      (by
        intro k hk
        have hrowk : row ≠ k := by
          intro hrowk
          exact hk hrowk.symm
        simp [hrowk])
    simpa using hunique
  · rw [if_neg h]
    exact linearDiagonal_foldl_add_zero_of_all_zero
      (List.finRange (gridSize n))
      (fun k : Fin (gridSize n) =>
        (if row = k then CubicStatePreparation.gridPoint n row else 0) *
          if k = col then CubicStatePreparation.gridPoint n k else 0)
      0
      (by
        intro k _hmem
        by_cases hrk : row = k
        · subst k
          simp [h]
        · simp [hrk])

private theorem linearDiagonal_square_mul_entry (n : Nat)
    (row col : Fin (gridSize n)) :
    Matrix.mul
        (Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n))
        (linearDiagonalOperator n) row col =
      if row = col then
        (CubicStatePreparation.gridPoint n row * CubicStatePreparation.gridPoint n row) *
          CubicStatePreparation.gridPoint n row
      else 0 := by
  change (List.finRange (gridSize n)).foldl
      (fun acc k =>
        acc +
          Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n) row k *
            linearDiagonalOperator n k col)
      0 =
    if row = col then
      (CubicStatePreparation.gridPoint n row * CubicStatePreparation.gridPoint n row) *
        CubicStatePreparation.gridPoint n row
    else 0
  by_cases h : row = col
  · subst col
    rw [if_pos rfl]
    have hunique := linearDiagonal_foldl_add_unique_finRange
      (fun k : Fin (gridSize n) =>
        Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n) row k *
          linearDiagonalOperator n k row)
      row
      (by
        intro k hk
        have hrowk : row ≠ k := by
          intro hrowk
          exact hk hrowk.symm
        have hsquare :
            Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n) row k = 0 := by
          rw [linearDiagonal_mul_entry]
          simp [hrowk]
        simp [hsquare])
    simpa [linearDiagonal_mul_entry, linearDiagonalOperator] using hunique
  · rw [if_neg h]
    exact linearDiagonal_foldl_add_zero_of_all_zero
      (List.finRange (gridSize n))
      (fun k : Fin (gridSize n) =>
        Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n) row k *
          linearDiagonalOperator n k col)
      0
      (by
        intro k _hmem
        by_cases hrk : row = k
        · subst k
          simp [linearDiagonalOperator, h]
        · have hsquare :
              Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n) row k = 0 := by
            rw [linearDiagonal_mul_entry]
            simp [hrk]
          simp [hsquare])

/--
Target-identification leaf for the hinted route:
the project-local matrix cube of `O_0` is the cubic diagonal target `D_n`.
-/
theorem linearDiagonal_cube_eq_cubicDiagonalOperator (n : Nat) :
    Matrix.PointwiseEq
      (Matrix.mul
        (Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n))
        (linearDiagonalOperator n))
      (cubicDiagonalOperator n) := by
  intro row col
  rw [linearDiagonal_square_mul_entry]
  by_cases h : row = col
  · subst col
    rw [if_pos rfl]
    simp [cubicDiagonalOperator, CubicStatePreparation.cubicAmplitude]
    rw [Rat.pow_succ, Rat.pow_succ, Rat.pow_succ]
    simp
  · rw [if_neg h]
    simp [cubicDiagonalOperator, h]

/--
The compiled non-QSVT polynomial consumer for the human hint.  It reuses the
exact `O_0` clean-block payload three times through the library's product card.
-/
noncomputable def linearDiagonalCubicProductCertificate (n : Nat) :
    BlockEncodingClassics.LCUCertificate (gridSize n) :=
  let input :=
    BlockEncodingClassics.ExactCleanBlock.toLCUCertificate
      (linearDiagonalHouseholderInputBEContract n).exactPayload
  BlockEncodingClassics.productCleanBlockCertificate
    (BlockEncodingClassics.productCleanBlockCertificate input input) input

theorem linearDiagonalCubicProductCertificate_target_eq (n : Nat) :
    Matrix.PointwiseEq
      (linearDiagonalCubicProductCertificate n).target
      (cubicDiagonalTarget n).operator := by
  change Matrix.PointwiseEq
    (((linearDiagonalOperator n).mul (linearDiagonalOperator n)).mul
      (linearDiagonalOperator n))
    (cubicDiagonalOperator n)
  exact linearDiagonal_cube_eq_cubicDiagonalOperator n

theorem linearDiagonalCubicProductCertificate_clean_eq_target (n : Nat) :
    Matrix.PointwiseEq
      (linearDiagonalCubicProductCertificate n).cleanBlock
      (cubicDiagonalTarget n).operator := by
  intro row col
  exact Eq.trans
    ((linearDiagonalCubicProductCertificate n).blockProof row col)
    (linearDiagonalCubicProductCertificate_target_eq n row col)

/-- The polynomial selected by the human-hinted QSVT route. -/
def cubicQSVTPolynomial (x : Rat) : Rat := x ^ 3

/-- The cubic QSVT polynomial is bounded on every spectral value used by `O_0`. -/
theorem cubicQSVTPolynomial_gridPoint_abs_le_one
    (n : Nat) (j : Fin (gridSize n)) :
    Rat.abs (cubicQSVTPolynomial (CubicStatePreparation.gridPoint n j)) ≤ 1 := by
  rw [cubicQSVTPolynomial,
    Rat.abs_of_nonneg (Rat.pow_nonneg (CubicStatePreparation.gridPoint_nonneg n j))]
  exact CubicStatePreparation.rat_pow_le_one_of_nonneg_le_one
    (CubicStatePreparation.gridPoint n j) 3
    (CubicStatePreparation.gridPoint_nonneg n j)
    (CubicStatePreparation.gridPoint_le_one n j)

/-- Locally checkable side conditions for the cubic polynomial on the `O_0` spectrum. -/
structure CubicQSVTLocalSideConditions (n : Nat) where
  degree : Nat
  degree_eq : degree = 3
  oddParity : Bool
  oddParity_eq : oddParity = true
  boundedOnInputSpectrum :
    forall j : Fin (gridSize n),
      Rat.abs (cubicQSVTPolynomial (CubicStatePreparation.gridPoint n j)) ≤ 1

def cubicQSVTLocalSideConditions (n : Nat) :
    CubicQSVTLocalSideConditions n := by
  exact {
    degree := 3
    degree_eq := rfl
    oddParity := true
    oddParity_eq := rfl
    boundedOnInputSpectrum := cubicQSVTPolynomial_gridPoint_abs_le_one n
  }

/--
Single external boundary for the hinted route.

The supplier must provide a certified `O_0` block encoding and the transformed
clean block.  This interface replaces unconstrained QSVT proof search: all
project-local leaves are compiled, while phase synthesis and the QSVT semantic
theorem remain one explicit dependency.
-/
structure CubicQSVTExternalSemantics (n inputTotal outputTotal : Nat) where
  input : LinearDiagonalInputBEContract n inputTotal
  output : BlockEncodingClassics.ExactCleanBlock (gridSize n) outputTotal
  outputUnitary : BlockEncodingClassics.IsRationalOrthogonal output.U
  outputIsCubicTransform :
    Matrix.PointwiseEq output.A
      (Matrix.mul
        (Matrix.mul (linearDiagonalOperator n) (linearDiagonalOperator n))
        (linearDiagonalOperator n))
  globalPolynomialAdmissibility : Prop
  globalPolynomialAdmissibilityDescription : String
  globalPolynomialAdmissibilityProof : globalPolynomialAdmissibility
  cleanupStatement : Prop
  cleanupDescription : String
  cleanupProof : cleanupStatement
  resource : Resource
  resourceStatement : Prop
  resourceProof : resourceStatement

namespace CubicQSVTExternalSemantics

theorem output_eq_cubic_target {n inputTotal outputTotal : Nat}
    (semantics : CubicQSVTExternalSemantics n inputTotal outputTotal) :
    Matrix.PointwiseEq semantics.output.A (cubicDiagonalTarget n).operator := by
  intro row col
  exact Eq.trans (semantics.outputIsCubicTransform row col)
    (linearDiagonal_cube_eq_cubicDiagonalOperator n row col)

/-- Instantiate the generic consumer boundary without reopening QSVT search. -/
def consumerContract {n inputTotal outputTotal : Nat}
    (semantics : CubicQSVTExternalSemantics n inputTotal outputTotal) :
    BlockEncodingClassics.QSVTConsumerContract (gridSize n) inputTotal where
  input := semantics.input.exactPayload
  polynomialDescription := "P(x)=x^3; degree 3; odd; bounded on [-1,1]"
  sideConditions :=
    Nonempty (CubicQSVTLocalSideConditions n) ∧
      semantics.globalPolynomialAdmissibility
  outputStatement :=
    Matrix.PointwiseEq semantics.output.A (cubicDiagonalTarget n).operator
  sideConditionProof :=
    ⟨⟨cubicQSVTLocalSideConditions n⟩,
      semantics.globalPolynomialAdmissibilityProof⟩
  outputProof := semantics.output_eq_cubic_target

end CubicQSVTExternalSemantics

/-- One signal qubit and no pure workspace at the oracle-label tier. -/
def amplitudeOracleLayout (n : Nat) : RegisterLayout where
  systemQubits := n
  signalQubits := 1
  pureAncillas := 0

/-- Oracle-level exact diagonal amplitude transcript. -/
def amplitudeOracleCircuit (_n : Nat) : Circuit :=
  [Gate.oracleCall "diag-cubic-amplitude-oracle"]

/-- Resource of the oracle-label diagonal candidate. -/
def amplitudeOracleResource (n : Nat) : Resource :=
  (amplitudeOracleCircuit n).resource

/-- Candidate score for the oracle-label diagonal candidate. -/
def amplitudeOracleCost (n : Nat) : BlockEncodingCost :=
  BlockEncodingCost.fromLayoutAndResource
    (amplitudeOracleLayout n) (amplitudeOracleResource n)

/-- Tuple in the QBE score order `(gateCount, depth, auxiliaryQubits, oracleCalls)`. -/
def amplitudeOracleResourceTuple (n : Nat) : Nat × Nat × Nat × Nat :=
  ( (amplitudeOracleCost n).gateCount
  , (amplitudeOracleCost n).depth
  , (amplitudeOracleCost n).auxiliaryQubits
  , (amplitudeOracleCost n).oracleCalls
  )

theorem amplitudeOracleResource_eq (n : Nat) :
    amplitudeOracleResource n = Resource.ofCountsWithDepth 0 0 1 0 1 := by
  rfl

theorem amplitudeOracleResourceTuple_eq (n : Nat) :
    amplitudeOracleResourceTuple n = (1, 1, 1, 1) := by
  simp [amplitudeOracleResourceTuple, amplitudeOracleCost, amplitudeOracleLayout,
    amplitudeOracleResource, amplitudeOracleCircuit, BlockEncodingCost.fromLayoutAndResource,
    RegisterLayout.auxiliaryQubits, Circuit.resource, Gate.resource, Resource.gates, Resource.ofCountsWithDepth]

/-- Clean-block contract for the diagonal cubic candidate. -/
def diagonalCleanBlockContract (n : Nat)
    (block : Matrix (gridSize n) (gridSize n) Rat) : Prop :=
  ∀ row col,
    block row col =
      if row = col then CubicStatePreparation.cubicAmplitude n row else 0

theorem diagonalCleanBlockContract_pointwise_eq
    (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat)
    (h : diagonalCleanBlockContract n block) :
    Matrix.PointwiseEq block (cubicDiagonalOperator n) := by
  intro row col
  simpa [cubicDiagonalOperator] using h row col

theorem primitiveOracleCleanBlock_eq_target
    (n : Nat) (block : Matrix (gridSize n) (gridSize n) Rat)
    (h : diagonalCleanBlockContract n block) :
    Matrix.PointwiseEq block (cubicDiagonalTarget n).operator := by
  simpa [cubicDiagonalTarget] using
    (diagonalCleanBlockContract_pointwise_eq n block h)

/-- Amplitude range needed by the one-signal diagonal construction. -/
theorem cubicAmplitude_le_one (n : Nat) (j : Fin (gridSize n)) :
    CubicStatePreparation.cubicAmplitude n j ≤ 1 := by
  exact CubicStatePreparation.rat_pow_le_one_of_nonneg_le_one
    (CubicStatePreparation.gridPoint n j) 3
    (CubicStatePreparation.gridPoint_nonneg n j)
    (CubicStatePreparation.gridPoint_le_one n j)

theorem cubicAmplitude_nonneg (n : Nat) (j : Fin (gridSize n)) :
    0 ≤ CubicStatePreparation.cubicAmplitude n j := by
  simpa [CubicStatePreparation.cubicAmplitude] using
    (Rat.pow_nonneg (CubicStatePreparation.gridPoint_nonneg n j) :
      0 ≤ CubicStatePreparation.gridPoint n j ^ 3)

/-- Full matrix dimension of the unexpanded one-signal primitive oracle. -/
def primitiveAmplitudeOracleDimension (n : Nat) : Nat :=
  gridSize (n + (amplitudeOracleLayout n).auxiliaryQubits)

/--
External primitive matrix supplied by the oracle-label tier.

This is only a named object for the semantic contract below.  The current file
does not prove that this opaque matrix is a gate-expanded unitary.
-/
opaque primitiveAmplitudeOracleUnitary (n : Nat) :
    Matrix (primitiveAmplitudeOracleDimension n)
      (primitiveAmplitudeOracleDimension n) Rat

/-- Explicit unitarity obligation for the primitive oracle-label matrix. -/
opaque primitiveAmplitudeOracleIsUnitary (n : Nat)
    (unitary : Matrix (primitiveAmplitudeOracleDimension n)
      (primitiveAmplitudeOracleDimension n) Rat) : Prop

/-- Explicit clean-block extraction obligation for the primitive oracle-label matrix. -/
opaque primitiveAmplitudeOracleCleanBlockExtracts (n : Nat)
    (unitary : Matrix (primitiveAmplitudeOracleDimension n)
      (primitiveAmplitudeOracleDimension n) Rat)
    (block : Matrix (gridSize n) (gridSize n) Rat) : Prop

/--
Primitive one-signal amplitude-oracle semantic contract.

This contract keeps the unexpanded primitive tier honest: it requires both a
unitarity obligation for the named oracle matrix and a clean-block extraction
obligation whose extracted block satisfies the diagonal target contract.
-/
def primitiveAmplitudeOracleSemanticContract (n : Nat) : Prop :=
  primitiveAmplitudeOracleIsUnitary n (primitiveAmplitudeOracleUnitary n) ∧
    ∃ block : Matrix (gridSize n) (gridSize n) Rat,
      primitiveAmplitudeOracleCleanBlockExtracts n
        (primitiveAmplitudeOracleUnitary n) block ∧
        diagonalCleanBlockContract n block

theorem primitiveAmplitudeOracleSemanticContract_unitary
    (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) :
    primitiveAmplitudeOracleIsUnitary n (primitiveAmplitudeOracleUnitary n) :=
  h.1

theorem primitiveAmplitudeOracleSemanticContract_cleanBlock_eq_target
    (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) :
    ∃ block : Matrix (gridSize n) (gridSize n) Rat,
      primitiveAmplitudeOracleCleanBlockExtracts n
        (primitiveAmplitudeOracleUnitary n) block ∧
        Matrix.PointwiseEq block (cubicDiagonalTarget n).operator := by
  rcases h with ⟨_hUnitary, block, hExtract, hClean⟩
  exact ⟨block, hExtract, primitiveOracleCleanBlock_eq_target n block hClean⟩

/--
Expanded arithmetic route layout.

The workspace count is explicit because the reversible arithmetic, angle
synthesis, and uncomputation proof are not yet fixed to one resource backend.
-/
def expandedAmplitudeOracleLayout (n workspaceQubits : Nat) : RegisterLayout where
  systemQubits := n
  signalQubits := 1
  pureAncillas := workspaceQubits

theorem expandedAmplitudeOracleLayout_auxiliaryQubits
    (n workspaceQubits : Nat) :
    (expandedAmplitudeOracleLayout n workspaceQubits).auxiliaryQubits =
      1 + workspaceQubits := by
  rfl

/-- The expanded route targets the same exact normalizer `alpha = 1`. -/
theorem expandedAmplitudeOracleNormalizer_eq (n _workspaceQubits : Nat) :
    exactNormalizer n = 1 := by
  rfl

/--
Scalar-tier contract for the standard `R_y` clean-entry identity.

The project-local matrix layer is still exact `Rat`, so `arccos` and `cos`
are represented here by backend-supplied scalar functions.  The contract keeps
the standard convention explicit: for every rational amplitude `a` in `[0, 1]`,
the clean signal entry of `R_y (2 * arccos a)` is exactly `a` after embedding
into the backend scalar tier.
-/
structure StandardRyCleanEntryScalarTier where
  Scalar : Type
  ratAmplitude : Rat -> Scalar
  thetaForAmplitude : Scalar -> Scalar
  cleanEntry : Scalar -> Scalar
  cleanEntry_of_range :
    ∀ a : Rat, 0 ≤ a -> a ≤ 1 ->
      cleanEntry (thetaForAmplitude (ratAmplitude a)) = ratAmplitude a
  thetaFormula : String := "theta = 2 * arccos(amplitude)"
  cleanEntryFormula : String := "cos(theta / 2)"

/--
Indexwise clean-entry obligation for the cubic diagonal amplitudes in a chosen
standard-`R_y` scalar tier.
-/
def expandedRyCleanEntryForCubicAmplitudes
    (tier : StandardRyCleanEntryScalarTier) (n : Nat) : Prop :=
  ∀ j : Fin (gridSize n),
    tier.cleanEntry
        (tier.thetaForAmplitude
          (tier.ratAmplitude (CubicStatePreparation.cubicAmplitude n j))) =
      tier.ratAmplitude (CubicStatePreparation.cubicAmplitude n j)

/--
`DIAG-EXP-RY-001`: the standard scalar-tier `R_y` clean-entry contract applies
to every cubic grid amplitude because the existing Lean range lemmas prove
`0 <= (j / 2^n)^3 <= 1`.
-/
theorem expandedRyCleanEntryForCubicAmplitudes_of_standardTier
    (tier : StandardRyCleanEntryScalarTier) (n : Nat) :
    expandedRyCleanEntryForCubicAmplitudes tier n := by
  intro j
  exact tier.cleanEntry_of_range
    (CubicStatePreparation.cubicAmplitude n j)
    (cubicAmplitude_nonneg n j)
    (cubicAmplitude_le_one n j)

/--
Semantic obligation that the expanded reversible arithmetic computes
`a_j = (j / 2^n)^3` into the named workspace.
-/
opaque expandedArithmeticComputesCubicAmplitude
    (n workspaceQubits : Nat) : Prop

/--
Backend-level shape for the expanded reversible arithmetic compute phase.

The structure records only the compute half of the route: starting from a
clean workspace, the backend returns the same system index together with a
workspace whose distinguished amplitude register contains
`CubicStatePreparation.cubicAmplitude n j`.  Clean uncompute remains the
separate obligation `expandedWorkspaceCleanUncomputed`.
-/
structure ExpandedCubicArithmeticBackend (n workspaceQubits : Nat) where
  Workspace : Type
  workspaceQubitCount : Nat
  workspaceQubitCount_eq : workspaceQubitCount = workspaceQubits
  zeroWorkspace : Workspace
  amplitudeRegister : Workspace -> Rat
  compute : Fin (gridSize n) -> Workspace -> Fin (gridSize n) × Workspace

/--
Symbolic compute-phase backend for `DIAG-EXP-ARITH-BACKEND-001`.

This witness records only the pointwise arithmetic value written by the compute
phase.  It does not certify a reversible gate implementation, clean uncompute,
or the bridge to `expandedArithmeticComputesCubicAmplitude`.
-/
def symbolicExpandedCubicArithmeticBackend (n workspaceQubits : Nat) :
    ExpandedCubicArithmeticBackend n workspaceQubits where
  Workspace := Rat
  workspaceQubitCount := workspaceQubits
  workspaceQubitCount_eq := rfl
  zeroWorkspace := 0
  amplitudeRegister := fun a => a
  compute := fun j _workspace =>
    (j, CubicStatePreparation.cubicAmplitude n j)

/--
Pointwise arithmetic-backend semantics for `DIAG-EXP-ARITH-001`.

For each system index `j`, the compute phase preserves `j` and writes exactly
the cubic diagonal amplitude into its distinguished amplitude register.
-/
def expandedArithmeticBackendComputesCubicAmplitude
    {n workspaceQubits : Nat}
    (backend : ExpandedCubicArithmeticBackend n workspaceQubits) : Prop :=
  backend.workspaceQubitCount = workspaceQubits ∧
    ∀ j : Fin (gridSize n),
      (backend.compute j backend.zeroWorkspace).1 = j ∧
        backend.amplitudeRegister ((backend.compute j backend.zeroWorkspace).2) =
          CubicStatePreparation.cubicAmplitude n j

/--
The symbolic backend satisfies the pointwise compute contract for every system
index.  The opaque expanded-route predicate still requires a separate backend
bridge witness.
-/
theorem symbolicExpandedCubicArithmeticBackend_computes
    (n workspaceQubits : Nat) :
    expandedArithmeticBackendComputesCubicAmplitude
      (symbolicExpandedCubicArithmeticBackend n workspaceQubits) := by
  constructor
  · rfl
  · intro j
    constructor <;> rfl

/--
Bridge obligation from a concrete arithmetic backend to the expanded route
predicate.  This is conditional for the same reason as the rotation bridge:
the backend must still justify that its pointwise compute semantics are the
semantics of the route predicate used by the block-encoding contract.
-/
def expandedArithmeticBackendBridge
    {n workspaceQubits : Nat}
    (backend : ExpandedCubicArithmeticBackend n workspaceQubits) : Prop :=
  expandedArithmeticBackendComputesCubicAmplitude backend ->
    expandedArithmeticComputesCubicAmplitude n workspaceQubits

theorem expandedArithmeticComputesCubicAmplitude_of_backendBridge
    {n workspaceQubits : Nat}
    (backend : ExpandedCubicArithmeticBackend n workspaceQubits)
    (hBackend : expandedArithmeticBackendComputesCubicAmplitude backend)
    (hBridge : expandedArithmeticBackendBridge backend) :
    expandedArithmeticComputesCubicAmplitude n workspaceQubits :=
  hBridge hBackend

/--
General normal form for arithmetic backend bridge proof search.

Once a backend's pointwise compute contract is available, proving its bridge is
equivalent to proving the opaque expanded-route predicate itself.  This lemma
is a proof-reduction aid; it does not supply the route semantics.
-/
theorem expandedArithmeticBackendBridge_iff_of_computes
    {n workspaceQubits : Nat}
    (backend : ExpandedCubicArithmeticBackend n workspaceQubits)
    (hBackend : expandedArithmeticBackendComputesCubicAmplitude backend) :
    expandedArithmeticBackendBridge backend ↔
      expandedArithmeticComputesCubicAmplitude n workspaceQubits := by
  constructor
  · intro hBridge
    exact expandedArithmeticComputesCubicAmplitude_of_backendBridge
      backend hBackend hBridge
  · intro hRoute
    intro _hBackend
    exact hRoute

/--
Specialized conditional closure for the symbolic arithmetic backend.

This does not prove the backend bridge witness; it only packages the already
compiled pointwise compute proof with a future honest bridge witness for
`DIAG-ARITH-BACKEND-BRIDGE-001`.
-/
theorem expandedArithmeticComputesCubicAmplitude_of_symbolicBackendBridge
    (n workspaceQubits : Nat)
    (hBridge :
      expandedArithmeticBackendBridge
        (symbolicExpandedCubicArithmeticBackend n workspaceQubits)) :
    expandedArithmeticComputesCubicAmplitude n workspaceQubits := by
  exact expandedArithmeticComputesCubicAmplitude_of_backendBridge
    (symbolicExpandedCubicArithmeticBackend n workspaceQubits)
    (symbolicExpandedCubicArithmeticBackend_computes n workspaceQubits)
    hBridge

/--
Normal form for the symbolic arithmetic bridge obligation.

For the symbolic backend, the pointwise compute proof is already compiled, so
the bridge obligation is logically equivalent to the opaque expanded-route
predicate itself.  This is a proof-reduction lemma, not a bridge witness: it
keeps `DIAG-ARITH-BACKEND-BRIDGE-001` blocked until a concrete route-semantics
representation proves `expandedArithmeticComputesCubicAmplitude`.
-/
theorem symbolicExpandedCubicArithmeticBackend_bridge_iff
    (n workspaceQubits : Nat) :
    expandedArithmeticBackendBridge
        (symbolicExpandedCubicArithmeticBackend n workspaceQubits) ↔
      expandedArithmeticComputesCubicAmplitude n workspaceQubits := by
  exact expandedArithmeticBackendBridge_iff_of_computes
    (symbolicExpandedCubicArithmeticBackend n workspaceQubits)
    (symbolicExpandedCubicArithmeticBackend_computes n workspaceQubits)

/--
`DIAG-ARITH-FIXED-DENOM-CAP-001`: the fixed-denominator cubic payload fits in
the `3 * n`-qubit workspace register.
-/
theorem fixedDenomCubicPayload_lt_capacity
    (n : Nat) (j : Fin (gridSize n)) :
    j.val ^ 3 < gridSize (3 * n) := by
  have hlt : j.val ^ 3 < gridSize n ^ 3 :=
    Nat.pow_lt_pow_left j.isLt (by decide : 3 ≠ 0)
  simpa [CubicStatePreparation.gridSize_three_mul_eq_cube] using hlt

/--
`DIAG-ARITH-FIXED-DENOM-ALG-001`: projecting the fixed-denominator payload
`j.val ^ 3` by the `3 * n`-qubit denominator recovers the cubic grid
amplitude.
-/
theorem fixedDenomCubicAmplitude_eq
    (n : Nat) (j : Fin (gridSize n)) :
    (j.val : Rat) ^ 3 / (gridSize (3 * n) : Rat) =
      CubicStatePreparation.cubicAmplitude n j := by
  rw [CubicStatePreparation.gridSize_three_mul_eq_cube]
  simpa [CubicStatePreparation.cubicAmplitude, CubicStatePreparation.gridPoint]
    using
      (show (j.val : Rat) ^ 3 / (gridSize n : Rat) ^ 3 =
          ((j.val : Rat) / (gridSize n : Rat)) ^ 3 by
        simp [Rat.div_def, Rat.pow_succ, Rat.inv_mul_rev, Rat.mul_assoc]
        grind [Rat.mul_comm, Rat.mul_assoc])

/--
`DIAG-ARITH-FIXED-DENOM-BACKEND-001`: concrete compute-phase backend whose
`3 * n`-qubit workspace stores the fixed-denominator payload `j.val ^ 3`.
-/
def fixedDenomCubicArithmeticBackend (n : Nat) :
    ExpandedCubicArithmeticBackend n (3 * n) where
  Workspace := Fin (gridSize (3 * n))
  workspaceQubitCount := 3 * n
  workspaceQubitCount_eq := rfl
  zeroWorkspace := ⟨0, CubicStatePreparation.gridSize_pos (3 * n)⟩
  amplitudeRegister := fun payload =>
    (payload.val : Rat) / (gridSize (3 * n) : Rat)
  compute := fun j _workspace =>
    (j, ⟨j.val ^ 3, fixedDenomCubicPayload_lt_capacity n j⟩)

/--
Pointwise compute contract for the fixed-denominator arithmetic backend.

This closes the backend leaf only; the bridge to
`expandedArithmeticComputesCubicAmplitude` remains a separate semantic
obligation.
-/
theorem fixedDenomCubicArithmeticBackend_computes
    (n : Nat) :
    expandedArithmeticBackendComputesCubicAmplitude
      (fixedDenomCubicArithmeticBackend n) := by
  constructor
  · rfl
  · intro j
    constructor
    · rfl
    · exact fixedDenomCubicAmplitude_eq n j

/--
Transparent arithmetic-route interface for `DIAG-ARITH-ROUTE-TRANSPARENT-001`.

This records that some explicit backend satisfies the pointwise compute
contract.  It is intentionally weaker than the opaque expanded-route predicate:
using it as a route certificate still requires a later named bridge or contract
refactor.
-/
def expandedArithmeticComputesCubicAmplitudeTransparent
    (n workspaceQubits : Nat) : Prop :=
  Exists fun backend : ExpandedCubicArithmeticBackend n workspaceQubits =>
    expandedArithmeticBackendComputesCubicAmplitude backend

/--
Fixed-denominator witness for the transparent arithmetic route interface.

This packages the already compiled fixed-denominator backend and its pointwise
compute theorem.  It does not prove
`expandedArithmeticComputesCubicAmplitude n (3 * n)`.
-/
theorem fixedDenomCubicArithmeticRouteTransparent
    (n : Nat) :
    expandedArithmeticComputesCubicAmplitudeTransparent n (3 * n) := by
  exact ⟨fixedDenomCubicArithmeticBackend n,
    fixedDenomCubicArithmeticBackend_computes n⟩

/--
Fixed-denominator normal form for the arithmetic bridge obligation.

The concrete backend's pointwise compute proof is available, so direct bridge
search is equivalent to proving the opaque expanded-route predicate itself.
This records the remaining route-semantics gap without supplying a bridge
witness.
-/
theorem fixedDenomCubicArithmeticBackend_bridge_iff
    (n : Nat) :
    expandedArithmeticBackendBridge (fixedDenomCubicArithmeticBackend n) ↔
      expandedArithmeticComputesCubicAmplitude n (3 * n) := by
  exact expandedArithmeticBackendBridge_iff_of_computes
    (fixedDenomCubicArithmeticBackend n)
    (fixedDenomCubicArithmeticBackend_computes n)

/--
Semantic obligation for the standard `R_y` convention on the signal qubit:
for each basis index `j`, the route uses
`theta_j = 2 * arccos ((j / 2^n)^3)`, so the clean entry is
`cos (theta_j / 2) = (j / 2^n)^3`.
-/
opaque expandedControlledRyUsesCubicAngle
    (n workspaceQubits : Nat) : Prop

/--
Transparent controlled-`R_y` angle-convention interface for
`DIAG-RY-TRANSPARENT-INTERFACE-001`.

This records only the already compiled scalar clean-entry fact for every
standard tier.  It does not prove the opaque route predicate
`expandedControlledRyUsesCubicAngle`.
-/
def expandedControlledRyUsesCubicAngleTransparent
    (n _workspaceQubits : Nat) : Prop :=
  forall tier : StandardRyCleanEntryScalarTier,
    expandedRyCleanEntryForCubicAmplitudes tier n

/--
Fixed-denominator wrapper for the transparent controlled-`R_y` route.

This packages the scalar-tier theorem at workspace size `3 * n`.  It does not
provide a backend witness for `expandedControlledRyUsesCubicAngle`.
-/
theorem fixedDenomControlledRyRouteTransparent
    (n : Nat) :
    expandedControlledRyUsesCubicAngleTransparent n (3 * n) := by
  intro tier
  exact expandedRyCleanEntryForCubicAmplitudes_of_standardTier tier n

/--
Backend bridge obligation from the scalar-tier `R_y` clean-entry interface to
the expanded route predicate.

This is intentionally conditional: the file already proves the scalar
clean-entry fact for cubic amplitudes, but a concrete backend must still justify
that this fact is the semantics of the controlled rotation used by the route.
-/
def expandedControlledRyBackendBridge
    (tier : StandardRyCleanEntryScalarTier)
    (n workspaceQubits : Nat) : Prop :=
  expandedRyCleanEntryForCubicAmplitudes tier n ->
    expandedControlledRyUsesCubicAngle n workspaceQubits

theorem expandedControlledRyUsesCubicAngle_of_backendBridge
    (tier : StandardRyCleanEntryScalarTier)
    (n workspaceQubits : Nat)
    (hBridge : expandedControlledRyBackendBridge tier n workspaceQubits) :
    expandedControlledRyUsesCubicAngle n workspaceQubits :=
  hBridge (expandedRyCleanEntryForCubicAmplitudes_of_standardTier tier n)

/--
Normal form for controlled-rotation backend-bridge proof search.

The scalar-tier clean-entry theorem is already compiled, so proving a backend
bridge for the controlled rotation is equivalent to proving the opaque route
predicate itself.  This is a proof-reduction lemma for
`DIAG-RY-BACKEND-WITNESS-001`; it does not supply the missing backend
semantics.
-/
theorem expandedControlledRyBackendBridge_iff_of_standardTier
    (tier : StandardRyCleanEntryScalarTier)
    (n workspaceQubits : Nat) :
    expandedControlledRyBackendBridge tier n workspaceQubits ↔
      expandedControlledRyUsesCubicAngle n workspaceQubits := by
  constructor
  · intro hBridge
    exact expandedControlledRyUsesCubicAngle_of_backendBridge
      tier n workspaceQubits hBridge
  · intro hRoute
    intro _hScalar
    exact hRoute

/--
Transparent readonly-rotation interface for
`DIAG-RY-WORKSPACE-READONLY-001`.

This records that the controlled signal rotation may read the arithmetic
workspace payload while preserving both the system index and workspace value.
It does not prove `expandedWorkspaceCleanUncomputed` or any opaque route
predicate.
-/
structure ExpandedControlledRyWorkspaceReadonlyWitness
    (n workspaceQubits : Nat) where
  backend : ExpandedCubicArithmeticBackend n workspaceQubits
  angleConvention :
    expandedControlledRyUsesCubicAngleTransparent n workspaceQubits
  rotationStep :
    Fin (gridSize n) -> backend.Workspace -> Fin 2 ->
      Prod (Prod (Fin (gridSize n)) backend.Workspace) (Fin 2)
  preserves_index :
    forall j w signal, (rotationStep j w signal).1.1 = j
  preserves_workspace :
    forall j w signal, (rotationStep j w signal).1.2 = w

/--
Transparent predicate for a controlled-rotation step that preserves the
arithmetic workspace.

This is intentionally separate from route-level cleanup; a later packet must
choose either a transparent cleanup contract refactor or a nontrivial bridge.
-/
def expandedControlledRyWorkspaceReadonlyTransparent
    (n workspaceQubits : Nat) : Prop :=
  Nonempty (ExpandedControlledRyWorkspaceReadonlyWitness n workspaceQubits)

/-- Semantic obligation that the arithmetic workspace is returned clean. -/
opaque expandedWorkspaceCleanUncomputed
    (n workspaceQubits : Nat) : Prop

/--
Transparent clean-uncompute interface for
`DIAG-EXP-UNCOMP-TRANSPARENT-INTERFACE-001`.

This records the data needed to state honest reversible cleanup: a compute step
matching the backend on clean workspace, an uncompute step that preserves the
system index, and a two-sided cleanup condition after compute.  It does not
prove the opaque route predicate `expandedWorkspaceCleanUncomputed`.
-/
structure ExpandedArithmeticCleanUncomputeWitness
    (n workspaceQubits : Nat) where
  backend : ExpandedCubicArithmeticBackend n workspaceQubits
  computes : expandedArithmeticBackendComputesCubicAmplitude backend
  computeStep :
    Fin (gridSize n) -> backend.Workspace ->
      Prod (Fin (gridSize n)) backend.Workspace
  uncomputeStep :
    Fin (gridSize n) -> backend.Workspace ->
      Prod (Fin (gridSize n)) backend.Workspace
  computeStep_matches_backend_on_clean :
    forall j,
      computeStep j backend.zeroWorkspace =
        backend.compute j backend.zeroWorkspace
  compute_preserves_index :
    forall j w, (computeStep j w).1 = j
  uncompute_preserves_index :
    forall j w, (uncomputeStep j w).1 = j
  uncompute_after_compute :
    forall j w, uncomputeStep j (computeStep j w).2 = (j, w)

/--
Transparent cleanup predicate backed by an explicit reversible witness.

This is intentionally separate from `expandedWorkspaceCleanUncomputed`; a later
route must either instantiate this interface and refactor a contract to consume
it, or supply a nontrivial bridge to the opaque predicate.
-/
def expandedWorkspaceCleanUncomputedTransparent
    (n workspaceQubits : Nat) : Prop :=
  Nonempty (ExpandedArithmeticCleanUncomputeWitness n workspaceQubits)

theorem expandedWorkspaceCleanUncomputedTransparent_of_witness
    {n workspaceQubits : Nat}
    (w : ExpandedArithmeticCleanUncomputeWitness n workspaceQubits) :
    expandedWorkspaceCleanUncomputedTransparent n workspaceQubits := by
  exact ⟨w⟩

private theorem fixedDenomCubicModAddSub_eq_self
    {modulus workspace payload : Nat}
    (hWorkspace : workspace < modulus) (hPayload : payload < modulus) :
    ((workspace + payload) % modulus + modulus - payload) % modulus =
      workspace := by
  by_cases hlt : workspace + payload < modulus
  · have hmod : (workspace + payload) % modulus =
        workspace + payload := Nat.mod_eq_of_lt hlt
    calc
      ((workspace + payload) % modulus + modulus - payload) % modulus
          = (workspace + payload + modulus - payload) % modulus := by
              rw [hmod]
      _ = (workspace + modulus) % modulus := by
            congr 1
            omega
      _ = workspace % modulus := by
            rw [Nat.add_mod_right]
      _ = workspace := Nat.mod_eq_of_lt hWorkspace
  · have hge : workspace + payload ≥ modulus := by omega
    have hsum_lt : workspace + payload < 2 * modulus := by omega
    have hsub_lt : workspace + payload - modulus < modulus := by omega
    have hmod : (workspace + payload) % modulus =
        workspace + payload - modulus := by
      rw [Nat.mod_eq_sub_mod hge]
      exact Nat.mod_eq_of_lt hsub_lt
    calc
      ((workspace + payload) % modulus + modulus - payload) % modulus
          = (workspace + payload - modulus + modulus - payload) % modulus := by
              rw [hmod]
      _ = workspace % modulus := by
            congr 1
            omega
      _ = workspace := Nat.mod_eq_of_lt hWorkspace

/--
Fixed-denominator reversible compute lift for
`DIAG-EXP-UNCOMP-FIXED-DENOM-WITNESS-001`.

This modular-add step agrees with `fixedDenomCubicArithmeticBackend` on clean
workspace, but unlike the backend's overwrite-style compute field it is
invertible on every workspace value.
-/
def fixedDenomCubicComputeStep (n : Nat) :
    Fin (gridSize n) -> (fixedDenomCubicArithmeticBackend n).Workspace ->
      Prod (Fin (gridSize n)) (fixedDenomCubicArithmeticBackend n).Workspace :=
  fun j workspace =>
    (j, ⟨(workspace.val + j.val ^ 3) % gridSize (3 * n),
      Nat.mod_lt _ (CubicStatePreparation.gridSize_pos (3 * n))⟩)

/-- Modular-subtract inverse for `fixedDenomCubicComputeStep`. -/
def fixedDenomCubicUncomputeStep (n : Nat) :
    Fin (gridSize n) -> (fixedDenomCubicArithmeticBackend n).Workspace ->
      Prod (Fin (gridSize n)) (fixedDenomCubicArithmeticBackend n).Workspace :=
  fun j workspace =>
    (j, ⟨(workspace.val + gridSize (3 * n) - j.val ^ 3) % gridSize (3 * n),
      Nat.mod_lt _ (CubicStatePreparation.gridSize_pos (3 * n))⟩)

theorem fixedDenomCubicComputeStep_matches_backend_on_clean
    (n : Nat) (j : Fin (gridSize n)) :
    fixedDenomCubicComputeStep n j
        (fixedDenomCubicArithmeticBackend n).zeroWorkspace =
      (fixedDenomCubicArithmeticBackend n).compute j
        (fixedDenomCubicArithmeticBackend n).zeroWorkspace := by
  simp [fixedDenomCubicComputeStep, fixedDenomCubicArithmeticBackend,
    Nat.mod_eq_of_lt (fixedDenomCubicPayload_lt_capacity n j)]

theorem fixedDenomCubicUncomputeStep_after_compute
    (n : Nat) (j : Fin (gridSize n))
    (workspace : (fixedDenomCubicArithmeticBackend n).Workspace) :
    fixedDenomCubicUncomputeStep n j
        (fixedDenomCubicComputeStep n j workspace).2 =
      (j, workspace) := by
  apply Prod.ext
  · rfl
  · apply Fin.ext
    simp [fixedDenomCubicComputeStep, fixedDenomCubicUncomputeStep]
    exact fixedDenomCubicModAddSub_eq_self workspace.isLt
      (fixedDenomCubicPayload_lt_capacity n j)

/--
Fixed-denominator witness for the transparent clean-uncompute interface.

This packages modular add/sub cleanup only.  It does not prove the opaque
predicate `expandedWorkspaceCleanUncomputed`, does not state controlled-rotation
workspace-readonly semantics, and does not close extraction or unitarity.
-/
def fixedDenomExpandedArithmeticCleanUncomputeWitness
    (n : Nat) : ExpandedArithmeticCleanUncomputeWitness n (3 * n) where
  backend := fixedDenomCubicArithmeticBackend n
  computes := fixedDenomCubicArithmeticBackend_computes n
  computeStep := fixedDenomCubicComputeStep n
  uncomputeStep := fixedDenomCubicUncomputeStep n
  computeStep_matches_backend_on_clean := by
    intro j
    exact fixedDenomCubicComputeStep_matches_backend_on_clean n j
  compute_preserves_index := by
    intro j workspace
    rfl
  uncompute_preserves_index := by
    intro j workspace
    rfl
  uncompute_after_compute := by
    intro j workspace
    exact fixedDenomCubicUncomputeStep_after_compute n j workspace

theorem fixedDenomWorkspaceCleanUncomputedTransparent
    (n : Nat) :
    expandedWorkspaceCleanUncomputedTransparent n (3 * n) := by
  exact expandedWorkspaceCleanUncomputedTransparent_of_witness
    (fixedDenomExpandedArithmeticCleanUncomputeWitness n)

/--
Backend-level shape for computing the hinted linear diagonal value
`x_j = j / 2^n`.

This is a transparent value-computation support interface for `HINT-O0-BACKEND`.
It does not provide the signal rotation, rational orthogonal matrix, or
clean-block equality required by `LinearDiagonalInputBEContract`.
-/
structure LinearDiagonalValueBackend (n workspaceQubits : Nat) where
  Workspace : Type
  workspaceQubitCount : Nat
  workspaceQubitCount_eq : workspaceQubitCount = workspaceQubits
  zeroWorkspace : Workspace
  amplitudeRegister : Workspace -> Rat
  compute : Fin (gridSize n) -> Workspace -> Fin (gridSize n) × Workspace

/--
Pointwise value-computation contract for a linear diagonal backend.

On clean workspace the backend preserves the system index and writes exactly
`CubicStatePreparation.gridPoint n j` into its distinguished value register.
-/
def linearDiagonalValueBackendComputesGridPoint
    {n workspaceQubits : Nat}
    (backend : LinearDiagonalValueBackend n workspaceQubits) : Prop :=
  backend.workspaceQubitCount = workspaceQubits ∧
    ∀ j : Fin (gridSize n),
      (backend.compute j backend.zeroWorkspace).1 = j ∧
        backend.amplitudeRegister ((backend.compute j backend.zeroWorkspace).2) =
          CubicStatePreparation.gridPoint n j

/--
Fixed-denominator value backend for `O_0`.

The workspace stores the numerator `j` in an `n`-qubit register and interprets
it as the rational value `j / 2^n`.
-/
def fixedDenomLinearDiagonalValueBackend (n : Nat) :
    LinearDiagonalValueBackend n n where
  Workspace := Fin (gridSize n)
  workspaceQubitCount := n
  workspaceQubitCount_eq := rfl
  zeroWorkspace := ⟨0, CubicStatePreparation.gridSize_pos n⟩
  amplitudeRegister := fun payload =>
    (payload.val : Rat) / (gridSize n : Rat)
  compute := fun j _workspace =>
    (j, ⟨j.val, j.isLt⟩)

/-- The fixed-denominator linear backend computes `x_j = j / 2^n` on clean workspace. -/
theorem fixedDenomLinearDiagonalValueBackend_computes
    (n : Nat) :
    linearDiagonalValueBackendComputesGridPoint
      (fixedDenomLinearDiagonalValueBackend n) := by
  constructor
  · rfl
  · intro j
    constructor
    · rfl
    · rfl

/--
Transparent cleanup witness for a linear value backend.

The witness uses an invertible compute/uncompute pair around the backend's
clean-workspace value contract.  It is intentionally separate from the missing
controlled-rotation and full clean-block obligations.
-/
structure LinearDiagonalValueCleanUncomputeWitness
    (n workspaceQubits : Nat) where
  backend : LinearDiagonalValueBackend n workspaceQubits
  computes : linearDiagonalValueBackendComputesGridPoint backend
  computeStep :
    Fin (gridSize n) -> backend.Workspace ->
      Prod (Fin (gridSize n)) backend.Workspace
  uncomputeStep :
    Fin (gridSize n) -> backend.Workspace ->
      Prod (Fin (gridSize n)) backend.Workspace
  computeStep_matches_backend_on_clean :
    forall j,
      computeStep j backend.zeroWorkspace =
        backend.compute j backend.zeroWorkspace
  compute_preserves_index :
    forall j w, (computeStep j w).1 = j
  uncompute_preserves_index :
    forall j w, (uncomputeStep j w).1 = j
  uncompute_after_compute :
    forall j w, uncomputeStep j (computeStep j w).2 = (j, w)

/-- Transparent predicate for honest compute/uncompute cleanup of an `O_0` value backend. -/
def linearDiagonalWorkspaceCleanUncomputedTransparent
    (n workspaceQubits : Nat) : Prop :=
  Nonempty (LinearDiagonalValueCleanUncomputeWitness n workspaceQubits)

theorem linearDiagonalWorkspaceCleanUncomputedTransparent_of_witness
    {n workspaceQubits : Nat}
    (w : LinearDiagonalValueCleanUncomputeWitness n workspaceQubits) :
    linearDiagonalWorkspaceCleanUncomputedTransparent n workspaceQubits := by
  exact ⟨w⟩

/-- Modular-add compute step for the fixed-denominator linear backend. -/
def fixedDenomLinearDiagonalComputeStep (n : Nat) :
    Fin (gridSize n) -> (fixedDenomLinearDiagonalValueBackend n).Workspace ->
      Prod (Fin (gridSize n)) (fixedDenomLinearDiagonalValueBackend n).Workspace :=
  fun j workspace =>
    (j, ⟨(workspace.val + j.val) % gridSize n,
      Nat.mod_lt _ (CubicStatePreparation.gridSize_pos n)⟩)

/-- Modular-subtract inverse for `fixedDenomLinearDiagonalComputeStep`. -/
def fixedDenomLinearDiagonalUncomputeStep (n : Nat) :
    Fin (gridSize n) -> (fixedDenomLinearDiagonalValueBackend n).Workspace ->
      Prod (Fin (gridSize n)) (fixedDenomLinearDiagonalValueBackend n).Workspace :=
  fun j workspace =>
    (j, ⟨(workspace.val + gridSize n - j.val) % gridSize n,
      Nat.mod_lt _ (CubicStatePreparation.gridSize_pos n)⟩)

theorem fixedDenomLinearDiagonalComputeStep_matches_backend_on_clean
    (n : Nat) (j : Fin (gridSize n)) :
    fixedDenomLinearDiagonalComputeStep n j
        (fixedDenomLinearDiagonalValueBackend n).zeroWorkspace =
      (fixedDenomLinearDiagonalValueBackend n).compute j
        (fixedDenomLinearDiagonalValueBackend n).zeroWorkspace := by
  simp [fixedDenomLinearDiagonalComputeStep,
    fixedDenomLinearDiagonalValueBackend, Nat.mod_eq_of_lt j.isLt]

theorem fixedDenomLinearDiagonalUncomputeStep_after_compute
    (n : Nat) (j : Fin (gridSize n))
    (workspace : (fixedDenomLinearDiagonalValueBackend n).Workspace) :
    fixedDenomLinearDiagonalUncomputeStep n j
        (fixedDenomLinearDiagonalComputeStep n j workspace).2 =
      (j, workspace) := by
  apply Prod.ext
  · rfl
  · apply Fin.ext
    simp [fixedDenomLinearDiagonalComputeStep,
      fixedDenomLinearDiagonalUncomputeStep]
    exact fixedDenomCubicModAddSub_eq_self workspace.isLt j.isLt

/--
Fixed-denominator cleanup witness for the hinted `O_0` value backend.

This closes only the transparent value-compute/cleanup support leaf for
`HINT-O0-BACKEND`; a full `LinearDiagonalInputBEContract` instance still needs
a signal-amplitude matrix with `IsRationalOrthogonal`, clean-block equality,
and resource accounting.
-/
def fixedDenomLinearDiagonalCleanUncomputeWitness
    (n : Nat) : LinearDiagonalValueCleanUncomputeWitness n n where
  backend := fixedDenomLinearDiagonalValueBackend n
  computes := fixedDenomLinearDiagonalValueBackend_computes n
  computeStep := fixedDenomLinearDiagonalComputeStep n
  uncomputeStep := fixedDenomLinearDiagonalUncomputeStep n
  computeStep_matches_backend_on_clean := by
    intro j
    exact fixedDenomLinearDiagonalComputeStep_matches_backend_on_clean n j
  compute_preserves_index := by
    intro j workspace
    rfl
  uncompute_preserves_index := by
    intro j workspace
    rfl
  uncompute_after_compute := by
    intro j workspace
    exact fixedDenomLinearDiagonalUncomputeStep_after_compute n j workspace

theorem fixedDenomLinearDiagonalWorkspaceCleanUncomputedTransparent
    (n : Nat) :
    linearDiagonalWorkspaceCleanUncomputedTransparent n n := by
  exact linearDiagonalWorkspaceCleanUncomputedTransparent_of_witness
    (fixedDenomLinearDiagonalCleanUncomputeWitness n)

/-- Clean-block extraction obligation for the expanded arithmetic/rotation route. -/
opaque expandedAmplitudeOracleCleanBlockExtracts
    (n workspaceQubits : Nat)
    (block : Matrix (gridSize n) (gridSize n) Rat) : Prop

/--
Expanded-route clean-block contract for `DIAG-EXPANDED-CONTRACT-001`.

This is an interface, not a proof of the expanded circuit.  It keeps the
transparent arithmetic witness, transparent controlled-rotation witness, and
clean-uncompute obligations explicit and requires the extracted clean block to
satisfy the existing diagonal contract.
-/
def expandedAmplitudeOracleCleanBlockContract
    (n workspaceQubits : Nat)
    (block : Matrix (gridSize n) (gridSize n) Rat) : Prop :=
  expandedArithmeticComputesCubicAmplitudeTransparent n workspaceQubits ∧
    expandedControlledRyUsesCubicAngleTransparent n workspaceQubits ∧
    expandedWorkspaceCleanUncomputed n workspaceQubits ∧
    expandedAmplitudeOracleCleanBlockExtracts n workspaceQubits block ∧
    diagonalCleanBlockContract n block

theorem expandedAmplitudeOracleCleanBlockContract_diagonal
    (n workspaceQubits : Nat)
    (block : Matrix (gridSize n) (gridSize n) Rat)
    (h : expandedAmplitudeOracleCleanBlockContract n workspaceQubits block) :
    diagonalCleanBlockContract n block := by
  exact h.2.2.2.2

theorem expandedAmplitudeOracleCleanBlockContract_eq_target
    (n workspaceQubits : Nat)
    (block : Matrix (gridSize n) (gridSize n) Rat)
    (h : expandedAmplitudeOracleCleanBlockContract n workspaceQubits block) :
    Matrix.PointwiseEq block (cubicDiagonalTarget n).operator := by
  exact primitiveOracleCleanBlock_eq_target n block
    (expandedAmplitudeOracleCleanBlockContract_diagonal n workspaceQubits block h)

/--
Conditional semantic interface for an expanded arithmetic/rotation route with
an explicit workspace size.
-/
def expandedAmplitudeOracleSemanticContract
    (n workspaceQubits : Nat) : Prop :=
  ∃ block : Matrix (gridSize n) (gridSize n) Rat,
    expandedAmplitudeOracleCleanBlockContract n workspaceQubits block

theorem expandedAmplitudeOracleSemanticContract_cleanBlock_eq_target
    (n workspaceQubits : Nat)
    (h : expandedAmplitudeOracleSemanticContract n workspaceQubits) :
    ∃ block : Matrix (gridSize n) (gridSize n) Rat,
      expandedAmplitudeOracleCleanBlockExtracts n workspaceQubits block ∧
        Matrix.PointwiseEq block (cubicDiagonalTarget n).operator := by
  rcases h with ⟨block, hContract⟩
  exact ⟨block, hContract.2.2.2.1,
    expandedAmplitudeOracleCleanBlockContract_eq_target
      n workspaceQubits block hContract⟩

/-- Conditional candidate at the primitive oracle-label tier. -/
def primitiveAmplitudeOracleCandidate (n : Nat) :
    OperatorBlockEncodingCandidate Rat n where
  auxiliaryQubits := (amplitudeOracleLayout n).auxiliaryQubits
  target := cubicDiagonalTarget n
  unitary := primitiveAmplitudeOracleUnitary n
  layout := amplitudeOracleLayout n
  circuit := amplitudeOracleCircuit n
  resource := amplitudeOracleResource n
  layoutMatches := rfl
  isUnitary :=
    primitiveAmplitudeOracleIsUnitary n (primitiveAmplitudeOracleUnitary n)
  blockContainsTarget :=
    ∃ block : Matrix (gridSize n) (gridSize n) Rat,
      primitiveAmplitudeOracleCleanBlockExtracts n
        (primitiveAmplitudeOracleUnitary n) block ∧
        Matrix.PointwiseEq block (cubicDiagonalTarget n).operator

theorem primitiveAmplitudeOracleCandidate_costTuple_eq (n : Nat) :
    ( (primitiveAmplitudeOracleCandidate n).cost.gateCount
    , (primitiveAmplitudeOracleCandidate n).cost.depth
    , (primitiveAmplitudeOracleCandidate n).cost.auxiliaryQubits
    , (primitiveAmplitudeOracleCandidate n).cost.oracleCalls
    ) = (1, 1, 1, 1) := by
  simp [OperatorBlockEncodingCandidate.cost, primitiveAmplitudeOracleCandidate,
    amplitudeOracleLayout, amplitudeOracleResource, amplitudeOracleCircuit,
    RegisterLayout.auxiliaryQubits, Circuit.resource, Gate.resource,
    Resource.gates, Resource.ofCountsWithDepth]

theorem primitiveAmplitudeOracleCandidate_unitary_from_contract
    (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) :
    (primitiveAmplitudeOracleCandidate n).isUnitary := by
  simpa [primitiveAmplitudeOracleCandidate] using
    primitiveAmplitudeOracleSemanticContract_unitary n h

theorem primitiveAmplitudeOracleCandidate_block_from_contract
    (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) :
    (primitiveAmplitudeOracleCandidate n).blockContainsTarget := by
  simpa [primitiveAmplitudeOracleCandidate] using
    primitiveAmplitudeOracleSemanticContract_cleanBlock_eq_target n h

/--
Conditional exact certificate for the primitive oracle-label tier.

This packages a verified block encoding only from an explicit proof of
`primitiveAmplitudeOracleSemanticContract n`; the contract itself remains an
open primitive-oracle obligation until such a proof or accepted primitive
axiom is supplied.
-/
def primitiveAmplitudeOracleVerified
    (n : Nat) (h : primitiveAmplitudeOracleSemanticContract n) :
    VerifiedOperatorBlockEncoding Rat n where
  candidate := primitiveAmplitudeOracleCandidate n
  unitaryProof := primitiveAmplitudeOracleCandidate_unitary_from_contract n h
  blockProof := primitiveAmplitudeOracleCandidate_block_from_contract n h

/-- Human-facing construction claim for the first exact diagonal route. -/
def amplitudeOracleClaim : ConstructionClaim where
  name := "diagonal-cubic-amplitude-oracle"
  source := "QBE-OP-CUBIC-DIAGONAL-001 exploratory exact candidate"
  target := "D_n = sum_j (j/2^n)^3 |j><j|"
  normalization := "alpha = 1"
  layout := "one signal qubit, no pure ancilla at the oracle-label tier"
  resource := {
    gates := CostExpr.atom "diag_cubic_amplitude_oracle"
    pureAncilla := 0
  }

end CubicDiagonalOracle
end QuantumBlockEncoding
