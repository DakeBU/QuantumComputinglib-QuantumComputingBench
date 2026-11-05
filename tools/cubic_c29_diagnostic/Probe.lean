module

import all QuantumBlockEncoding.CubicStatePreparation
import Lean
meta import Lean

/- Diagnostic candidate only. NOT RUN by decoder; no mathematical acceptance.
   The hosting process must bind raw source, fresh output and provider hashes.
   QBE_EXPECT_FRESH_OLEAN must name the exact fresh target artifact. -/

open Lean Elab Command

set_option pp.universes true
set_option pp.fullNames true
set_option pp.privateNames true
set_option pp.explicit true
set_option pp.notation false
set_option pp.proofs true
set_option pp.funBinderTypes true
set_option pp.piBinderTypes true

namespace CubicBlindDiagnosticCandidate

structure RootSpec where
  userName : Name
  privateRoot : Bool
  sourceKind : String

def expectedRoots : Array RootSpec := #[
  { userName := `QuantumBlockEncoding.CubicStatePreparation.taskId, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.requestedEpsilon, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridPoint, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicOperator, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.conservativeNormalizer, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicTarget, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.defaultRequiredCost, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.defaultPolicy, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicDefaultPrecision, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicLayout, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicCircuit, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResource, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicNormalizer, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicCost, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResourceTuple, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicResource_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicLayout_auxiliaryQubits, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticCubicClaim, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicLayout, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCircuit, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResource, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicNormalizer, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCost, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResourceTuple, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResource_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicLayout_auxiliaryQubits, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicResourceTuple_n2_default, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicClaim, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicWorkspace, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicLayout, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCircuit, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCircuit_rejectSignalRepair, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResource, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicNormalizer, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCost, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResourceTuple, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResource_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicLayout_auxiliaryQubits, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicResourceTuple_n2, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicClaim, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hardModeUpperAgentSchedule, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hardModeMiddleAgentSchedule, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hardModeLowerAgentSchedule, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hardModeExactStallWindow, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hardModeConstructionStallWindow, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hardModeLevelCycleBudget, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.relaxedEpsilonLadder, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.relaxedEpsilonLadder_startsWithRequested, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hardModeSchedules_have_four_levels, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hardModeLowerAgentSchedule_final, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.initialExpectedPhase, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridSize_pos, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicOperator_first_column, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicOperator_only_first_column, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.rankOneCleanBlockContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCleanBlockContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.rankOneCleanBlockContract_pointwise_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.arithmeticRankOneCubicCleanBlockContract_pointwise_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCleanBlockContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubicCleanBlockContract_pointwise_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.rat_cube_sq_eq_sixth, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_sq_eq_gridPoint_sixth, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_sixthPowerFold, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_ne_zero, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_pos, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.rat_div_cube_div_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_div_conservativeNormalizer_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridSize_three_mul_eq_cube, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridSize_four_mul_eq_fourth, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdCountP_finRange, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdFilterLength, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_threshold_le_pathCapacity, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.hadamardCountingCubic_thresholdPathCount, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridPoint_nonneg, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridPoint_lt_one, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridPoint_le_one, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.rat_pow_le_one_of_nonneg_le_one, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicAmplitude_sq_le_one, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.foldl_add_le_add_length, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_gridSize, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.gridSize_rat_le_sq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_conservativeNormalizer_sq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_arithmeticCubicNormalizer_sq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_le_hadamardCountingCubicNormalizer_sq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n1, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n2, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicStatePreparation.cubicNormSq_n3, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.taskId, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalOperator, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.exactNormalizer, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalTarget, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalOperator, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalTarget, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlockContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlockContract_pointwise_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCleanBlock_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalExactCleanBlockFromPointwise, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalExactCleanBlockFromPointwise_clean_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract.exactPayload, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalInputBEContract.clean_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householderZero, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.dot8, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus_normSq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8E0Minus_normSq_ne_zero, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8_clean_entry, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.delta8, privateRoot := true, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fin8_exhaust, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.dot8_delta_delta, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.dot8_delta_left, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.dot8_delta_right, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.dot8_sub_sub, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8_columnDot, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8_symm, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8_rowDot, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.columnInner_eq_dot8, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rowInner_eq_dot8, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.householder8_isRationalOrthogonal, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8SystemIndex, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8AncillaIndex, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8Embed, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8Embed_val, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8SystemIndex_embed, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8AncillaIndex_embed, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8SystemIndex_productIndex, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8AncillaIndex_productIndex, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_productIndex_eta, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_identity_same_branch, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_branchNontrivial_of_clean, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_clean_entry, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_zero_of_all_zero, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_eq_identity_of_system_ne, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_column_off_branch_summand_zero, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_column_summand_productIndex, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_row_off_branch_summand_zero, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_row_summand_productIndex, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8BranchFiber, privateRoot := true, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8_productIndex_left_injective, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8BranchFiber_mem_iff, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_unique_of_nodup, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_nodup_map_of_injective, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_finRange_nodup, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8BranchFiber_nodup, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_perm_cons_erase_of_mem, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_perm_of_nodup_mem_iff, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_perm, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_filter_of_zero_acc, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_filter_of_zero, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_congr_acc, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_congr, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8BranchFiber_filter_perm, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_productIndex, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_columnInner_eq_branch, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_productIndex, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_eq_branch, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_rowInner_eq_identity_of_system_ne, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_isRationalOrthogonal, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalRationalCompletion, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_clean, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_unit, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_of_fourSquareWitnesses, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_exists, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_branchData, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalRationalCompletion_backendSupport, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderCircuit, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderResource, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderResource_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract_clean_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalHouseholderInputBEContract_complete, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ratAbs, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.IsDiagonalRatMatrix, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.DiagonalRatOperatorNormBridge, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ratSquaredEuclideanNorm, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ratMatrixErrorAction, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanOperatorNormErrorAtMost, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.diagonalFoldlAddZero, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.diagonalFoldlAddUnique, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.diagonalNodupMapOfInjective, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.diagonalFinRangeNodup, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.diagonalFoldlAddLe, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ratMatrixErrorAction_eq_diagonal, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ratAbs_nonneg, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_eq_ratAbs_mul_self, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_nonneg, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_le_of_abs_le, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_product_self, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rat_mul_self_vector_le_of_abs_le, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanDiagonalOperatorNormBridge, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ratEuclideanOperatorNormErrorAtMost_not_vacuous, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_isDiagonal, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalOperator_isDiagonal, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalEntrywiseErrorAtMost, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_entrywise_error, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_operatorNorm_error_of_contract, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.approxDiagonalOperator_operatorNorm_error, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector_clean, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.rationalCircleBranchVector_unit, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.controlledHouseholder8DirectSum_clean_entry_of_branchValue, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_clean, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_unit, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.CubicDiagonalRationalCompletion, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_of_fourSquareWitnesses, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_exists, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_lt_one, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalRationalCompletion_backendSupport, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.CubicDiagonalExactBEContract, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract_clean_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalHouseholderExactBEContract_complete, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_foldl_add_unique_finRange, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_mul_entry, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_square_mul_entry, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonal_cube_eq_cubicDiagonalOperator, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate_target_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalCubicProductCertificate_clean_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTPolynomial, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTPolynomial_gridPoint_abs_le_one, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTLocalSideConditions, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicQSVTLocalSideConditions, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics.output_eq_cubic_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.CubicQSVTExternalSemantics.consumerContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleLayout, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleCircuit, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResource, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleCost, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResourceTuple, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResource_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleResourceTuple_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.diagonalCleanBlockContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.diagonalCleanBlockContract_pointwise_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveOracleCleanBlock_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_le_one, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.cubicAmplitude_nonneg, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleDimension, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleUnitary, privateRoot := false, sourceKind := "opaque" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleIsUnitary, privateRoot := false, sourceKind := "opaque" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCleanBlockExtracts, privateRoot := false, sourceKind := "opaque" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract_unitary, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleSemanticContract_cleanBlock_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleLayout, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleLayout_auxiliaryQubits, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleNormalizer_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.StandardRyCleanEntryScalarTier, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedRyCleanEntryForCubicAmplitudes, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedRyCleanEntryForCubicAmplitudes_of_standardTier, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude, privateRoot := false, sourceKind := "opaque" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ExpandedCubicArithmeticBackend, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendComputesCubicAmplitude, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend_computes, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendBridge, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude_of_backendBridge, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticBackendBridge_iff_of_computes, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitude_of_symbolicBackendBridge, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.symbolicExpandedCubicArithmeticBackend_bridge_iff, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicPayload_lt_capacity, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicAmplitude_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend_computes, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedArithmeticComputesCubicAmplitudeTransparent, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticRouteTransparent, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicArithmeticBackend_bridge_iff, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngle, privateRoot := false, sourceKind := "opaque" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngleTransparent, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomControlledRyRouteTransparent, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyBackendBridge, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyUsesCubicAngle_of_backendBridge, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyBackendBridge_iff_of_standardTier, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ExpandedControlledRyWorkspaceReadonlyWitness, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedControlledRyWorkspaceReadonlyTransparent, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputed, privateRoot := false, sourceKind := "opaque" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.ExpandedArithmeticCleanUncomputeWitness, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputedTransparent, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedWorkspaceCleanUncomputedTransparent_of_witness, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicModAddSub_eq_self, privateRoot := true, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicComputeStep, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicUncomputeStep, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicComputeStep_matches_backend_on_clean, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomCubicUncomputeStep_after_compute, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomExpandedArithmeticCleanUncomputeWitness, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomWorkspaceCleanUncomputedTransparent, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalValueBackend, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalValueBackendComputesGridPoint, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalValueBackend, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalValueBackend_computes, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.LinearDiagonalValueCleanUncomputeWitness, privateRoot := false, sourceKind := "structure" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalWorkspaceCleanUncomputedTransparent, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalWorkspaceCleanUncomputedTransparent_of_witness, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalComputeStep, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalUncomputeStep, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalComputeStep_matches_backend_on_clean, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalUncomputeStep_after_compute, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalCleanUncomputeWitness, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomLinearDiagonalWorkspaceCleanUncomputedTransparent, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockExtracts, privateRoot := false, sourceKind := "opaque" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract_diagonal, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleCleanBlockContract_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleSemanticContract, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.expandedAmplitudeOracleSemanticContract_cleanBlock_eq_target, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_costTuple_eq, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_unitary_from_contract, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleCandidate_block_from_contract, privateRoot := false, sourceKind := "theorem" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.primitiveAmplitudeOracleVerified, privateRoot := false, sourceKind := "def" },
  { userName := `QuantumBlockEncoding.CubicDiagonalOracle.amplitudeOracleClaim, privateRoot := false, sourceKind := "def" }
]

def constantKind : ConstantInfo → String
  | .axiomInfo _ => "axiomInfo"
  | .defnInfo _ => "defnInfo"
  | .thmInfo _ => "thmInfo"
  | .opaqueInfo _ => "opaqueInfo"
  | .quotInfo _ => "quotInfo"
  | .inductInfo _ => "inductInfo"
  | .ctorInfo _ => "ctorInfo"
  | .recInfo _ => "recInfo"

def jsonNames (ns : Array Name) : Json :=
  .arr (ns.map fun n => .str n.toString)

def opaqueObservation (sourceKind : String) (ci : ConstantInfo) : String :=
  if sourceKind != "opaque" then "NOT_SOURCE_OPAQUE"
  else match ci with
    | .axiomInfo _ => "SOURCE_OPAQUE_ACTUAL_AXIOM_INFO"
    | .opaqueInfo _ => "SOURCE_OPAQUE_ACTUAL_OPAQUE_INFO"
    | _ => "SOURCE_OPAQUE_OTHER_ACTUAL_KIND_REQUIRES_REVIEW"

def exactTypeText (ci : ConstantInfo) : CommandElabM String :=
  liftTermElabM do
    return toString (← Meta.ppExpr ci.type)

def emit (tag : String) (value : Json) : CommandElabM Unit := do
  IO.println (tag ++ " " ++ value.compress)

run_cmd do
  let target := `QuantumBlockEncoding.CubicStatePreparation
  let some expectedPathString ← IO.getEnv "QBE_EXPECT_FRESH_OLEAN"
    | throwError "C29_FAIL: missing QBE_EXPECT_FRESH_OLEAN"
  let actualPath ← findOLean target
  let actualRealPath ← IO.FS.realPath actualPath
  let expectedRealPath ← IO.FS.realPath (System.FilePath.mk expectedPathString)
  unless actualRealPath == expectedRealPath do
    throwError "C29_FAIL: fresh target olean not first in actual search path"

  let env := (← getEnv).setExporting false
  withEnv env do
    let some targetIdx := env.getModuleIdx? target
      | throwError "C29_FAIL: target module absent from imported environment"
    let owned := env.constants.toList.filter fun pair =>
      env.getModuleIdxFor? pair.1 == some targetIdx
    unless expectedRoots.size == 319 do
      throwError "C29_FAIL: expected explicit root vector is not 319"
    unless (expectedRoots.filter fun r => r.privateRoot).size == 50 do
      throwError "C29_FAIL: expected private root vector is not 50"
    unless (expectedRoots.filter fun r => r.sourceKind == "opaque").size == 7 do
      throwError "C29_FAIL: source opaque vector is not 7"
    unless (expectedRoots.filter fun r => r.sourceKind == "structure").size == 11 do
      throwError "C29_FAIL: source structure vector is not 11"

    -- Resolve ALL roots before emitting any root-completion claim.
    -- No construction, parsing or guessing of numeric private name components.
    let mut resolved : Array (RootSpec × Name × ConstantInfo) := #[]
    let mut seenActual : Array Name := #[]
    let mut seenUsers : Array Name := #[]
    for spec in expectedRoots do
      if seenUsers.contains spec.userName then
        throwError "C29_FAIL: duplicated source user name {spec.userName}"
      let choices := owned.filter fun pair =>
        if spec.privateRoot then
          isPrivateName pair.1 && privateToUserName? pair.1 == some spec.userName
        else
          !isPrivateName pair.1 && pair.1 == spec.userName
      match choices with
      | [(actual, ci)] =>
        if seenActual.contains actual then
          throwError "C29_FAIL: actual name reused across explicit roots {actual}"
        let some kernelInfo := env.toKernelEnv.find? actual
          | throwError "C29_FAIL: resolved root missing from checked kernel environment {actual}"
        unless constantKind kernelInfo == constantKind ci do
          throwError "C29_FAIL: kernel/elaboration ConstantInfo kind mismatch {actual}"
        seenActual := seenActual.push actual
        seenUsers := seenUsers.push spec.userName
        resolved := resolved.push (spec, actual, ci)
      | [] => throwError "C29_FAIL: missing explicit root {spec.userName}"
      | _ => throwError "C29_FAIL: ambiguous explicit root {spec.userName}"

    let mut projectionOwners : Array (Name × Name) := #[]
    let mut structureNames : Array Name := #[]
    let mut structureRows : Array Json := #[]
    for (spec, actual, ci) in resolved do
      if spec.sourceKind == "structure" then
        let some sinfo := getStructureInfo? env actual
          | throwError "C29_FAIL: source structure lacks actual StructureInfo {actual}"
        let .inductInfo iv := ci
          | throwError "C29_FAIL: source structure is not actual inductInfo {actual}"
        structureNames := structureNames.push actual
        let mut fields : Array Json := #[]
        for field in sinfo.fieldInfo do
          let some fieldInfo := env.find? field.projFn
            | throwError "C29_FAIL: structure projection absent {field.projFn}"
          unless env.getModuleIdxFor? field.projFn == some targetIdx do
            throwError "C29_FAIL: structure projection belongs to unexpected module {field.projFn}"
          projectionOwners := projectionOwners.push (field.projFn, actual)
          fields := fields.push (Json.mkObj [
            ("fieldName", .str field.fieldName.toString),
            ("projection", .str field.projFn.toString),
            ("actualKind", .str (constantKind fieldInfo))])
        structureRows := structureRows.push (Json.mkObj [
          ("sourceUserName", .str spec.userName.toString),
          ("actualName", .str actual.toString),
          ("constructors", jsonNames iv.ctors.toArray),
          ("fields", .arr fields)])

    emit "C29_BINDING_JSON" (Json.mkObj [
      ("targetModule", .str target.toString),
      ("actualResolvedOleanPath", .str actualRealPath.toString),
      ("freshOleanPathComparisonPassed", .bool true),
      ("expectedNamedRoots", toJson expectedRoots.size),
      ("observedTargetOwnedConstants", toJson owned.length),
      ("sourceOpaqueCount", toJson (expectedRoots.filter fun r => r.sourceKind == "opaque").size),
      ("actualStructures", .arr structureRows),
      ("sourceAgreement", .null), ("nativeAccepted", .bool false)])

    let mut ordinal := 0
    for (spec, actual, ci) in resolved do
      ordinal := ordinal + 1
      let typeText ← exactTypeText ci
      let axioms ← collectAxioms actual
      -- This is the same public collector used by builtin #print axioms.
      -- Never infer an empty array from a missing name or a lexical opaque tag.
      emit "C29_ROOT_JSON" (Json.mkObj [
        ("ordinal", toJson ordinal),
        ("sourceUserName", .str spec.userName.toString),
        ("sourcePrivate", .bool spec.privateRoot),
        ("sourceKind", .str spec.sourceKind),
        ("actualName", .str actual.toString),
        ("actualPrivate", .bool (isPrivateName actual)),
        ("actualKind", .str (constantKind ci)),
        ("opaqueClassification", .str (opaqueObservation spec.sourceKind ci)),
        ("kernelRootPresent", .bool true),
        ("universeParameters", jsonNames ci.levelParams.toArray),
        ("typePrettyExplicit", .str typeText),
        ("actualHasValueAllowOpaque", .bool (ci.hasValue (allowOpaque := true))),
        ("isUnsafe", .bool ci.isUnsafe),
        ("axioms", jsonNames (axioms.qsort Name.lt)),
        ("selfOccursInAxioms", .bool (axioms.contains actual)),
        ("sourceAgreement", .null), ("nativeAccepted", .bool false)])

    let mut generatedCount := 0
    for (name, ci) in owned do
      unless seenActual.contains name do
        generatedCount := generatedCount + 1
        let mut association := "OTHER_TARGET_OWNED_GENERATED_RESIDUAL"
        let mut parents : Array Name := #[]
        for (projection, owner) in projectionOwners do
          if name == projection then
            association := "STRUCTURE_FIELD_PROJECTION_METADATA"
            parents := parents.push owner
        match ci with
        | .ctorInfo v =>
          if structureNames.contains v.induct then
            association := "STRUCTURE_CONSTRUCTOR_METADATA"
            parents := parents.push v.induct
        | .recInfo v =>
          for owner in v.all do
            if structureNames.contains owner then
              association := "STRUCTURE_RECURSOR_METADATA"
              parents := parents.push owner
        | _ => pure ()
        emit "C29_GENERATED_JSON" (Json.mkObj [
          ("actualName", .str name.toString),
          ("userNameViaActualAPI", .str (privateToUserName name).toString),
          ("actualPrivate", .bool (isPrivateName name)),
          ("actualKind", .str (constantKind ci)),
          ("classification", .str association),
          ("structureParents", jsonNames parents),
          ("includedIn319ExplicitRootCount", .bool false),
          ("typeAxiomAuditScope", .str "NOT_REQUESTED_FOR_GENERATED_RESIDUAL_METADATA_ONLY")])

    emit "C29_SUMMARY_JSON" (Json.mkObj [
      ("status", .str "RUNTIME_DIAGNOSTIC_COMPLETE_NOT_SCIENTIFIC_ACCEPTANCE"),
      ("explicitRootsCompleted", toJson ordinal),
      ("explicitPrivateCompleted", toJson (resolved.filter fun r => r.1.privateRoot).size),
      ("generatedTargetOwnedConstants", toJson generatedCount),
      ("observedTargetOwnedConstants", toJson owned.length),
      ("actualStructureCount", toJson structureNames.size),
      ("allExplicitNamesResolvedUniquely", .bool true),
      ("axiomPolicyPass", .null), ("sourceAgreement", .null),
      ("publicationBinding", .null), ("nativeAccepted", .bool false)])

end CubicBlindDiagnosticCandidate
